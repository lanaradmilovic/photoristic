"""Feedback page for a meeting with the agency (`python cull.py meeting`).

One local page, in Serbian, that leads through the meeting and saves every answer at once:

  1. disputed pairs: two photos, "would you deliver one or both?" (three answers);
  2. excerpts of the real grouping: the agency only clicks where a group is wrong
     (cut inside a group, join two neighbouring groups); "the rest is fine" confirms
     every pair of that excerpt they did not touch;
  3. questions: one question per screen with a few written answers. Where earlier answers
     contradict each other, the examples are shown next to each other ("sides"), each
     with what was said then. A side's optional `context` is every frame of that moment: the
     page shows them as a small strip with their count and marks the side's photos in it, so
     two frames are not judged without knowing how many there are.

What is shown comes from `meeting.json` in the meeting folder, written by hand:

    {"title":     "Pitanja posle sastanka",
     "cases":     [{"out": "data/out-4a", "a": "_KAD0141.NEF", "b": "_KAD0142.NEF", "kind": "wide-tight"}],
     "excerpts":  [{"out": "data/out-4a", "title": "Crkva", "first": "_KAD9796.NEF", "last": "_KAD9900.NEF"}],
     "questions": [{"id": "siri-uzi", "title": "Širi i uži kadar", "text": "…", "ask": "Šta program treba da zadrži?",
                    "sides": [{"out": "data/out-4a", "photos": ["_KAD9930.NEF", "_KAD9931.NEF"],
                               "label": "Kod stolova", "said": "obe", "tone": "keep", "why": "…",
                               "context": ["_KAD9926.NEF", "…", "_KAD9933.NEF"]}],
                    "options": [{"id": "obe", "text": "Uvek obe"}, {"id": "jedna", "text": "Uvek jednu"}]}]}

`out` is an output folder of the pipeline (absolute, or relative to the working directory);
the excerpts may come from different folders, so the previews in use are copied into the
meeting folder. Nothing leaves the machine.

Answers go to `meeting_answers.json`: {updated, pairs, notes, choices}. A pair has the
fields of a label in labels.json (a_sha, b_sha, a_name, b_name, label, labeled_at) plus
`source` (click / confirmed / case), `part` ("case" or the excerpt's title), and for a case
its `answer` (one / both / different) and `kind`. So `cull.py score --labels` can measure
any grouping against them; pairs of another wedding are skipped there. `choices` holds the
answer to every question: {question id: {option, text, question, at}}.
"""
import html
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

from culling.grouping import _sort_key, load_groups
from culling.ingest import load_photos
from culling.labels import load_labels, normalise_labels, pair_key

DEFINITION_FILE = "meeting.json"
ANSWERS_FILE = "meeting_answers.json"
PAGE_FILE = "meeting.html"
CASE_KEYS = {"out", "a", "b", "kind"}
EXCERPT_KEYS = {"out", "title", "first", "last"}
QUESTION_KEYS, QUESTION_OPTIONAL = {"id", "title", "ask", "options"}, {"text", "sides"}
SIDE_KEYS, SIDE_OPTIONAL = {"out", "photos"}, {"label", "said", "why", "tone", "context"}
TONES = ("keep", "cut")    # colour of a side's "said": kept more / kept fewer
OTHER = "other"            # the answer the page adds to every question: something else, in the note
DEFAULT_TITLE = "Pregled grupisanja"
SOURCES = ("click", "confirmed", "case")
ANSWERS = {"one": "same", "both": "same", "different": "different"}   # a case's answer -> label


# ----------------------------------------------------------------------- meeting.json

def _is_text(value):
    return isinstance(value, str) and bool(value.strip())


def _check_question(q, i):
    """One entry of 'questions': id, title, the question itself ('ask'), two or more written
    answers and, optionally, an introduction ('text') and the examples it is about ('sides')."""
    where = f"{DEFINITION_FILE}: questions[{i}]"
    if not isinstance(q, dict) or not QUESTION_KEYS <= set(q) or set(q) - QUESTION_KEYS - QUESTION_OPTIONAL:
        raise ValueError(f"{where} needs id, title, ask and options; text and sides are optional")
    if not all(_is_text(q[k]) for k in ("id", "title", "ask")) or not isinstance(q.get("text", ""), str):
        raise ValueError(f"{where}: id, title, ask and text must be text")
    options = q["options"]
    if not isinstance(options, list) or len(options) < 2 or not all(
            isinstance(o, dict) and set(o) == {"id", "text"} and _is_text(o["id"]) and _is_text(o["text"])
            for o in options):
        raise ValueError(f"{where}: options must be two or more of {{id, text}}")
    ids = [o["id"] for o in options]
    if len(set(ids)) != len(ids) or OTHER in ids:
        raise ValueError(f"{where}: option ids must be unique and not '{OTHER}'")
    if not isinstance(q.get("sides", []), list):
        raise ValueError(f"{where}: sides must be a list")
    for side in q.get("sides", []):
        if not isinstance(side, dict) or not SIDE_KEYS <= set(side) or set(side) - SIDE_KEYS - SIDE_OPTIONAL:
            raise ValueError(f"{where}: a side needs out and photos; label, said, why, tone and context are optional")
        if not _is_text(side["out"]) or not isinstance(side["photos"], list) or not side["photos"] \
                or not all(_is_text(name) for name in side["photos"]):
            raise ValueError(f"{where}: a side needs an output folder and one or more photo names")
        if not all(isinstance(side.get(k, ""), str) for k in ("label", "said", "why")) \
                or side.get("tone", TONES[0]) not in TONES:
            raise ValueError(f"{where}: label, said and why must be text, tone one of {', '.join(TONES)}")
        context = side.get("context", [])
        if not isinstance(context, list) or not all(_is_text(name) for name in context)                 or ("context" in side and not {n.lower() for n in side["photos"]} <= {n.lower() for n in context}):
            raise ValueError(f"{where}: context must list photo names and include the side's photos")


def load_definition(meeting_dir):
    """meeting.json, checked: unknown or missing keys are errors."""
    path = Path(meeting_dir) / DEFINITION_FILE
    if not path.exists():
        raise ValueError(f"No {DEFINITION_FILE} in {meeting_dir}")
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, dict) or set(raw) - {"title", "cases", "excerpts", "questions"}:
        raise ValueError(f"{DEFINITION_FILE}: expected an object with 'title', 'cases', 'excerpts' and 'questions' only")
    definition = {"title": raw.get("title") or DEFAULT_TITLE, "cases": raw.get("cases") or [],
                  "excerpts": raw.get("excerpts") or [], "questions": raw.get("questions") or []}
    if not _is_text(definition["title"]) or not isinstance(definition["questions"], list):
        raise ValueError(f"{DEFINITION_FILE}: title must be text and questions a list")
    for i, q in enumerate(definition["questions"]):
        _check_question(q, i)
    ids = [q["id"] for q in definition["questions"]]
    if len(set(ids)) != len(ids):
        raise ValueError(f"{DEFINITION_FILE}: question ids must be unique")
    for name, keys in (("cases", CASE_KEYS), ("excerpts", EXCERPT_KEYS)):
        for i, item in enumerate(definition[name]):
            if not isinstance(item, dict) or set(item) != keys or not all(isinstance(v, str) and v for v in item.values()):
                raise ValueError(f"{DEFINITION_FILE}: {name}[{i}] must have exactly the keys "
                                 f"{', '.join(sorted(keys))}, all non-empty strings")
    titles = [x["title"] for x in definition["excerpts"]]
    if len(set(titles)) != len(titles) or "case" in titles:
        raise ValueError(f"{DEFINITION_FILE}: excerpt titles must be unique and not 'case'")
    if not definition["cases"] and not definition["excerpts"] and not definition["questions"]:
        raise ValueError(f"{DEFINITION_FILE}: nothing to show")
    return definition


def _photo(p, folder):
    return {"sha": p["sha256"], "name": Path(p["primary_path"]).name,
            "preview": f"previews/{folder}/{Path(p['preview_file']).name}", "source": p["preview_file"]}


def build_page_data(definition):
    """{title, cases: [{out, kind, a, b}], excerpts: [{out, title, groups: [{group_id, photos}]}],
    questions: [{id, title, text, ask, options, sides: [{out, label, said, why, tone, photos, context}]}],
    folders: {out: folder name under previews/}}; a photo is {sha, name, preview, source}
    (`source` is its preview inside `out`). An excerpt is every group whose first photo was
    taken between `first` and `last` on the same camera, in the order of groups.json."""
    loaded, folders = {}, {}

    def shoot(out):
        if out not in loaded:
            photos = load_photos(out)
            if not photos:
                raise ValueError(f"No photos.json in {out}")
            folders[out] = f"o{len(folders) + 1}"
            usable = [p for p in photos if p.get("sha256") and p.get("preview_file")]
            loaded[out] = ({Path(p["primary_path"]).name.lower(): p for p in reversed(usable)},
                           {p["id"]: p for p in usable})
        return loaded[out]

    def named(out, name):
        p = shoot(out)[0].get(name.lower())
        if p is None:
            raise ValueError(f"{DEFINITION_FILE}: no photo {name} with a preview in {out}")
        return p

    cases = [{"out": c["out"], "kind": c["kind"],
              "a": _photo(named(c["out"], c["a"]), folders[c["out"]]),
              "b": _photo(named(c["out"], c["b"]), folders[c["out"]])} for c in definition["cases"]]
    excerpts = []
    for x in definition["excerpts"]:
        first, last = named(x["out"], x["first"]), named(x["out"], x["last"])
        if not first.get("capture_time") or not last.get("capture_time") or _sort_key(first) > _sort_key(last):
            raise ValueError(f"{DEFINITION_FILE}: excerpt {x['title']}: 'first' must be taken before 'last'")
        by_id = shoot(x["out"])[1]
        groups = []
        for g in load_groups(x["out"])["groups"]:
            members = [by_id[pid] for pid in g["photo_ids"] if pid in by_id]
            head = members[0] if members else None
            if head is None or not head.get("capture_time") or head.get("camera_id") != first.get("camera_id") \
                    or not _sort_key(first) <= _sort_key(head) <= _sort_key(last):
                continue
            groups.append({"group_id": g["group_id"], "photos": [_photo(p, folders[x["out"]]) for p in members]})
        if not groups:
            raise ValueError(f"{DEFINITION_FILE}: excerpt {x['title']} has no group")
        excerpts.append({"out": x["out"], "title": x["title"], "groups": groups})
    # One pair has one answer: a pair shown twice would overwrite its first answer.
    seen = set()
    for a, b in [(c["a"], c["b"]) for c in cases] + [(l["a"], l["b"]) for x in excerpts for l in excerpt_links(x)]:
        if pair_key(a["sha"], b["sha"]) in seen:
            raise ValueError(f"{DEFINITION_FILE}: the pair {a['name']} / {b['name']} is shown twice "
                             f"(a disputed pair inside an excerpt, or overlapping excerpts)")
        seen.add(pair_key(a["sha"], b["sha"]))
    questions = []
    for q in definition["questions"]:
        sides = []
        for side in q.get("sides", []):
            photos = [named(side["out"], name) for name in side["photos"]]
            sides.append({"out": side["out"], "label": side.get("label", ""), "said": side.get("said", ""),
                          "why": side.get("why", ""), "tone": side.get("tone", ""),
                          "photos": [_photo(p, folders[side["out"]]) for p in photos],
                          "context": [_photo(named(side["out"], name), folders[side["out"]])
                                      for name in side.get("context", [])]})
        questions.append({"id": q["id"], "title": q["title"], "text": q.get("text", ""), "ask": q["ask"],
                          "options": q["options"], "sides": sides})
    return {"title": definition["title"], "cases": cases, "excerpts": excerpts, "questions": questions,
            "folders": folders}


def excerpt_links(excerpt):
    """Every pair the agency can judge in an excerpt: neighbours inside a group (the program
    says 'same') and the last photo of a group with the first of the next ('different')."""
    links, previous = [], None
    for g in excerpt["groups"]:
        if previous:
            links.append({"a": previous, "b": g["photos"][0], "pipeline": "different"})
        for a, b in zip(g["photos"], g["photos"][1:]):
            links.append({"a": a, "b": b, "pipeline": "same"})
        previous = g["photos"][-1]
    return links


def copy_previews(meeting_dir, data):
    """Copy the previews the page shows into <meeting_dir>/previews/<folder>/. Returns the
    number of files copied now."""
    meeting_dir, copied = Path(meeting_dir), 0
    photos = [(c["out"], c[side]) for c in data["cases"] for side in ("a", "b")]
    photos += [(x["out"], p) for x in data["excerpts"] for g in x["groups"] for p in g["photos"]]
    photos += [(side["out"], p) for q in data["questions"] for side in q["sides"]
               for p in side["photos"] + side["context"]]
    for out, p in photos:
        src, dst = Path(out) / p["source"], meeting_dir / p["preview"]
        if not src.exists():
            raise ValueError(f"Preview missing: {src}")
        if not dst.exists() or dst.stat().st_size != src.stat().st_size:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied += 1
    return copied


# --------------------------------------------------------------- meeting_answers.json

def normalise_answers(raw):
    """Validate what the page POSTs: {pairs: [...], notes: {key: text}, choices: {question
    id: {option, text, question, at}}}. Raises ValueError on anything malformed; a pair
    that appears twice keeps its last entry."""
    if not isinstance(raw, dict) or not isinstance(raw.get("pairs", []), list) \
            or not isinstance(raw.get("notes", {}), dict) or not isinstance(raw.get("choices", {}), dict):
        raise ValueError("answers must be an object with a list 'pairs' and objects 'notes' and 'choices'")
    pairs = {}
    for item, clean in zip(raw.get("pairs", []), normalise_labels(raw.get("pairs", []))):
        source, answer = item.get("source", "click"), item.get("answer") or ""
        if source not in SOURCES:
            raise ValueError(f"source must be one of {', '.join(SOURCES)}")
        if (source == "case") != (answer in ANSWERS) or (answer and ANSWERS.get(answer) != clean["label"]):
            raise ValueError("a case needs an answer (one / both / different) that matches its label")
        clean.update(source=source, part=str(item.get("part") or ""), answer=answer, kind=str(item.get("kind") or ""))
        pairs[pair_key(clean["a_sha"], clean["b_sha"])] = clean
    notes = {str(k): str(v).strip()[:2000] for k, v in raw.get("notes", {}).items() if str(v).strip()}
    choices = {}
    for qid, c in raw.get("choices", {}).items():
        if not isinstance(c, dict) or not _is_text(c.get("option")):
            raise ValueError("a choice needs an 'option'")
        # The wording is kept with the answer: meeting.json may be rewritten later.
        choices[str(qid)] = {"option": c["option"].strip(), "text": str(c.get("text") or "").strip()[:500],
                             "question": str(c.get("question") or "").strip()[:500], "at": str(c.get("at") or "")[:19]}
    return {"pairs": list(pairs.values()), "notes": notes, "choices": choices}


def load_answers(out_dir):
    path = Path(out_dir) / ANSWERS_FILE
    if not path.exists():
        return {"pairs": [], "notes": {}, "choices": {}}
    with open(path, encoding="utf-8") as f:
        return normalise_answers(json.load(f))


def save_answers(out_dir, answers):
    path = Path(out_dir) / ANSWERS_FILE
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"updated": datetime.now().isoformat(timespec="seconds"), **answers}, f,
                  indent=1, ensure_ascii=False)
    os.replace(tmp, path)
    return path


# --------------------------------------------------------------------------- summary

def summary(answers, data):
    """What the agency said, as text: the cases with their answers, per excerpt how many
    pairs were looked at and which were corrected, the answer to every question, and where
    the agency's answer differs from the user's own labels.json of that output folder."""
    by_key = {pair_key(p["a_sha"], p["b_sha"]): p for p in answers["pairs"]}
    notes = answers["notes"]
    said = {"one": "one is enough", "both": "same moment, deliver both", "different": "different moment / people"}
    lines = []
    if data["cases"]:
        lines.append(f"== disputed pairs: {sum(p['source'] == 'case' for p in answers['pairs'])} "
                     f"of {len(data['cases'])} answered")
    for c in data["cases"]:
        key = pair_key(c["a"]["sha"], c["b"]["sha"])
        answer = said[by_key[key]["answer"]] if key in by_key else "-"
        note = f"  note: {notes['case:' + key]}" if "case:" + key in notes else ""
        lines.append(f"  {c['kind']:<18} {c['a']['name']} / {c['b']['name']}: {answer}{note}")
    for x in data["excerpts"]:
        links = excerpt_links(x)
        seen = [(l, by_key[pair_key(l["a"]["sha"], l["b"]["sha"])]) for l in links
                if pair_key(l["a"]["sha"], l["b"]["sha"]) in by_key]
        wrong = [(l, p) for l, p in seen if p["label"] != l["pipeline"]]
        cuts = [l for l, p in wrong if p["label"] == "different"]
        joins = [l for l, p in wrong if p["label"] == "same"]
        lines.append(f"== {x['title']}: {len(x['groups'])} groups, {len(seen)} of {len(links)} pairs looked at, "
                     f"{len(cuts)} cuts (the program joined wrongly), {len(joins)} joins (the program split wrongly)")
        lines += [f"  CUT   {l['a']['name']} | {l['b']['name']}" for l in cuts]
        lines += [f"  JOIN  {l['a']['name']} + {l['b']['name']}" for l in joins]
        if "excerpt:" + x["title"] in notes:
            lines.append(f"  note: {notes['excerpt:' + x['title']]}")
    if data["questions"]:
        choices = answers["choices"]
        lines.append(f"== questions: {sum(q['id'] in choices for q in data['questions'])} "
                     f"of {len(data['questions'])} answered")
    for q in data["questions"]:
        choice = choices.get(q["id"])
        answer = "-" if choice is None else f"[{choice['option']}] {choice['text']}"
        lines.append(f"  {q['title']}: {answer}")
        if "question:" + q["id"] in notes:
            lines.append(f"    note: {notes['question:' + q['id']]}")
    differ = []
    for out in data["folders"]:
        for lab in load_labels(out):
            p = by_key.get(pair_key(lab["a_sha"], lab["b_sha"]))
            if p and lab["label"] != "unsure" and p["label"] != lab["label"]:
                differ.append(f"  {lab['a_name']} -> {lab['b_name']}: agency {p['label']} ({p['source']}), "
                              f"labels.json {lab['label']}")
    lines.append(f"== agency against the user's labels.json: {len(differ)} pairs differ")
    return "\n".join(lines + differ)


# -------------------------------------------------------------------------- the page

CSS = """
:root { --bg:#f6f6f4; --card:#fff; --text:#1d1d1f; --muted:#6b6b70; --line:#d9d9d6; --same:#15803d;
        --cut:#c2410c; --accent:#2f6fde; }
@media (prefers-color-scheme: dark) {
  :root { --bg:#161618; --card:#202024; --text:#ececee; --muted:#9a9aa2; --line:#3a3a42; --same:#4ade80;
          --cut:#fb923c; --accent:#6ea0ff; } }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--text); font:16px/1.45 system-ui, "Segoe UI", sans-serif; }
button, input { font:inherit; }
header { position:sticky; top:0; z-index:2; background:var(--bg); border-bottom:1px solid var(--line);
         padding:10px 18px; display:flex; gap:14px; align-items:center; }
header button, .big-btn, .answers button { padding:5px 14px; border:1px solid var(--line); border-radius:6px;
         background:var(--card); color:var(--text); cursor:pointer; }
.muted { color:var(--muted); } #status.err { color:#b91c1c; font-weight:600; }
.bar { flex:1; min-width:100px; height:8px; background:var(--line); border-radius:4px; overflow:hidden; }
.bar div { height:100%; background:var(--same); }
main { padding:14px 18px 60px; }
h1 { font-size:22px; margin:4px 0 6px; } .q { font-size:18px; margin:0 0 14px; max-width:980px; }
.pair { display:flex; gap:14px; justify-content:center; align-items:flex-start; }
.pair img { max-width:calc(50vw - 30px); max-height:66vh; border-radius:6px; cursor:zoom-in; }
.answers { display:flex; flex-wrap:wrap; gap:12px; justify-content:center; margin:18px 0 12px; }
.answers button { font-size:17px; padding:12px 20px; }
.answers button.on { background:var(--accent); color:#fff; border-color:transparent; }
.answers kbd { opacity:.65; margin-right:8px; }
.note { display:block; width:min(760px, 100%); margin:10px auto; padding:8px 10px; border:1px solid var(--line);
        border-radius:6px; background:var(--card); color:var(--text); }
.flow { display:flex; flex-wrap:wrap; gap:14px 0; align-items:center; }
.group { display:flex; flex-wrap:wrap; align-items:center; gap:6px 0; background:var(--card);
         border:3px solid var(--line); border-radius:10px; padding:6px; }
.group img { display:block; height:190px; border-radius:4px; cursor:zoom-in; }
.cut, .join { border:0; background:none; cursor:pointer; color:var(--muted); align-self:stretch; }
.unit { display:flex; align-items:center; max-width:100%; }
.cut { width:30px; font-size:17px; opacity:.75; }
.cut:hover, .join:hover { opacity:1; color:var(--text); background:var(--line); border-radius:4px; }
.cut.on { opacity:1; width:44px; color:#fff; background:var(--cut); border-radius:4px; margin:0 6px; font-weight:700; }
.join { width:70px; font-size:14px; opacity:.85; min-height:60px; white-space:nowrap; }
.join.on { opacity:1; color:#fff; background:var(--same); border-radius:4px; font-weight:700; }
.group.joined { border-color:var(--same); }
.finish { margin:26px 0 0; display:flex; flex-wrap:wrap; gap:14px; align-items:center; }
.big-btn { font-size:18px; padding:12px 22px; background:var(--accent); color:#fff; border-color:transparent; }
.finish .note { margin:0; flex:1; min-width:260px; }
.sides { display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:14px; margin:0 0 12px; }
.side { background:var(--card); border:1px solid var(--line); border-radius:10px; padding:8px 12px; }
.side-head { color:var(--muted); margin:0 0 6px; } .side-head b { color:var(--text); margin-right:6px; }
.shots { display:flex; flex-wrap:wrap; gap:6px; justify-content:center; align-items:center; }
.shots img { max-width:calc((100% - (var(--n) - 1) * 6px) / var(--n)); max-height:30vh; border-radius:4px;
             cursor:zoom-in; }
.shots.many img { max-height:15vh; }
.context { margin:8px 0 0; color:var(--muted); }
.context .strip { display:flex; flex-wrap:wrap; gap:3px; margin:4px 0 0; }
.context img { height:44px; border-radius:2px; opacity:.55; cursor:zoom-in; outline:2px solid transparent; }
.context img.asked { opacity:1; outline-color:var(--accent); }
.said { margin:8px 0 0; } .said .tag { font-size:17px; margin-right:8px; }
.tag { display:inline-block; padding:1px 11px; border-radius:999px; background:var(--muted); color:var(--card);
       font-weight:700; }
.tag.t-keep { background:var(--same); } .tag.t-cut { background:var(--cut); }
.ask { font-weight:600; text-align:center; max-width:none; margin:0; }
.answers.list { flex-direction:column; align-items:stretch; width:min(780px, 100%); margin:10px auto; gap:7px; }
.answers.list button { text-align:left; font-size:16px; padding:7px 14px; }
.recap { display:flex; flex-direction:column; gap:8px; width:min(900px, 100%); }
.recap button { display:block; text-align:left; padding:9px 14px; border:1px solid var(--line); border-radius:6px;
                background:var(--card); color:var(--text); cursor:pointer; }
.recap b, .recap i { display:block; } .recap i { color:var(--muted); }
#big { position:fixed; inset:0; background:rgba(0,0,0,.93); display:none; z-index:5; align-items:center;
       justify-content:center; }
#big.open { display:flex; } #big img { max-width:97vw; max-height:96vh; }
"""

JS = """
const D = JSON.parse(document.getElementById('data').textContent);
const steps = D.cases.map(c => ({type: 'case', c})).concat(D.excerpts.map(x => ({type: 'excerpt', x})),
                D.questions.map(q => ({type: 'question', q})), [{type: 'end'}]);
const LABEL = {one: 'same', both: 'same', different: 'different'};
const TEXT = {one: 'Ista slika — dovoljna je jedna', both: 'Isti trenutak, ali idu obe',
              different: 'Različit trenutak ili drugi ljudi'};
// Every question also offers "something else": the answer is then in the note.
const options = q => q.options.concat([{id: 'other', text: 'Drugačije (upišite ispod)'}]);
let P = {}, notes = {}, C = {}, pos = 0, bigList = [], big = -1;
const $ = id => document.getElementById(id);
const key = (a, b) => a.sha + '|' + b.sha;
const esc = t => String(t).replace(/[&<>"]/g, c => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;'}[c]));
const now = () => new Date().toISOString().slice(0, 19);
const mk = (a, b, label, source, part) => ({a_sha: a.sha, b_sha: b.sha, a_name: a.name, b_name: b.name,
                                            label, source, part, labeled_at: now()});

function links(x) {
  const out = []; let prev = null;
  for (const g of x.groups) {
    if (prev) out.push({a: prev, b: g.photos[0], pipeline: 'different'});
    for (let k = 1; k < g.photos.length; k++) out.push({a: g.photos[k - 1], b: g.photos[k], pipeline: 'same'});
    prev = g.photos[g.photos.length - 1];
  }
  return out;
}
const stepDone = s => s.type === 'case' ? !!P[key(s.c.a, s.c.b)]
                    : s.type === 'excerpt' ? links(s.x).every(l => P[key(l.a, l.b)])
                    : s.type === 'question' ? !!C[s.q.id] : false;

async function load() {
  try {
    const r = await fetch('/meeting', {cache: 'no-store'});
    if (r.ok) {
      const a = await r.json();
      for (const p of a.pairs) P[p.a_sha + '|' + p.b_sha] = p;
      notes = a.notes; C = a.choices || {};
    }
  } catch (e) { status('Otvori stranicu komandom "cull.py meeting" - kao fajl ne može da čuva.', true); }
  const first = steps.findIndex(s => s.type !== 'end' && !stepDone(s));
  pos = first < 0 ? steps.length - 1 : first;
  render();
}
let saving = null, again = false;
async function save() {
  if (saving) { again = true; return; }
  saving = (async () => {
    try {
      const r = await fetch('/meeting', {method: 'POST', headers: {'Content-Type': 'application/json'},
                                         body: JSON.stringify({pairs: Object.values(P), notes, choices: C})});
      if (!r.ok) throw new Error('HTTP ' + r.status);
      status('sačuvano', false);
    } catch (e) { status('NIJE sačuvano: ' + e.message, true); }
  })();
  await saving; saving = null;
  if (again) { again = false; save(); }
}
function status(text, err) { const s = $('status'); s.textContent = text; s.className = err ? 'err' : 'muted'; }
function go(i) { pos = Math.max(0, Math.min(steps.length - 1, i)); closeBig(); render(); window.scrollTo(0, 0); }

function answer(ans) {
  const c = steps[pos].c, r = mk(c.a, c.b, LABEL[ans], 'case', 'case');
  r.answer = ans; r.kind = c.kind; P[key(c.a, c.b)] = r;
  save(); go(pos + 1);
}
function toggle(k) {
  const x = steps[pos].x, l = links(x).find(l => key(l.a, l.b) === k); if (!l) return;
  const done = stepDone(steps[pos]), r = P[k];
  if (r && r.source === 'click') {
    delete P[k];
    if (done) P[k] = mk(l.a, l.b, l.pipeline, 'confirmed', x.title);
  } else P[k] = mk(l.a, l.b, l.pipeline === 'same' ? 'different' : 'same', 'click', x.title);
  save(); render();
}
function confirmRest() {
  const x = steps[pos].x;
  for (const l of links(x)) if (!P[key(l.a, l.b)]) P[key(l.a, l.b)] = mk(l.a, l.b, l.pipeline, 'confirmed', x.title);
  save(); go(pos + 1);
}
function choose(id) {
  const q = steps[pos].q, o = options(q).find(o => o.id === id); if (!o) return;
  C[q.id] = {option: o.id, text: o.text, question: q.ask, at: now()};
  save();
  if (id === 'other') { render(); $('note').focus(); } else go(pos + 1);
}
function noteKey() {
  const s = steps[pos];
  return s.type === 'case' ? 'case:' + key(s.c.a, s.c.b) : s.type === 'question' ? 'question:' + s.q.id
       : 'excerpt:' + s.x.title;
}
function noteBox() {
  return `<input class="note" id="note" placeholder="Napomena (zašto?) — nije obavezno" value="${esc(notes[noteKey()] || '')}">`;
}

function render() {
  const s = steps[pos], n = steps.filter(stepDone).length, total = steps.length - 1;
  $('progress').textContent = s.type === 'end' ? `urađeno ${n} / ${total}` : `${pos + 1} / ${total}`;
  $('fill').style.width = (100 * n / total) + '%';
  bigList = [];
  let h = '';
  if (s.type === 'case') {
    const r = P[key(s.c.a, s.c.b)];
    bigList = [s.c.a.preview, s.c.b.preview];
    h = `<p class="q">Da li biste mladencima isporučili <b>jednu</b> od ove dve slike ili <b>obe</b>?</p>` +
        `<div class="pair">${bigList.map((p, i) => `<img src="${p}" data-i="${i}" alt="">`).join('')}</div>` +
        `<div class="answers">` + ['one', 'both', 'different'].map((a, i) =>
          `<button data-ans="${a}" class="${r && r.answer === a ? 'on' : ''}"><kbd>${i + 1}</kbd>${TEXT[a]}</button>`).join('') +
        `</div>` + noteBox();
  } else if (s.type === 'excerpt') {
    const x = s.x; let prev = null;
    h = `<h1>${esc(x.title)}</h1><p class="q">Svaki okvir je jedna grupa: slike istog trenutka, od kojih kasnije ` +
        `ostaje najbolja. Kliknite <b>✂</b> između dve slike ako ne pripadaju zajedno, ili <b>spoji</b> između dva ` +
        `okvira ako su isti trenutak. Ono što je u redu ne dirajte.</p><div class="flow">`;
    const same = (a, b) => { const r = P[key(a, b)]; return !!r && r.label === 'same'; };
    x.groups.forEach((g, gi) => {
      // The join button travels with the group to its right, so a line break never orphans it.
      const next = x.groups[gi + 1], joined = !!prev && same(prev, g.photos[0]);
      const joinedNext = !!next && same(g.photos[g.photos.length - 1], next.photos[0]);
      h += `<div class="unit">`;
      if (prev)
        h += `<button class="join${joined ? ' on' : ''}" data-k="${key(prev, g.photos[0])}" ` +
             `title="ovaj i prethodni okvir su isti trenutak">${joined ? 'isto ✓' : '← spoji'}</button>`;
      h += `<div class="group${joined || joinedNext ? ' joined' : ''}">`;
      g.photos.forEach((p, j) => {
        if (j) {
          const k = key(g.photos[j - 1], p), on = !!P[k] && P[k].label === 'different';
          h += `<button class="cut${on ? ' on' : ''}" data-k="${k}" title="preseci ovde">✂</button>`;
        }
        h += `<img src="${p.preview}" data-i="${bigList.length}" loading="lazy" alt="">`;
        bigList.push(p.preview);
      });
      h += `</div></div>`;
      prev = g.photos[g.photos.length - 1];
    });
    h += `</div><div class="finish"><button class="big-btn" id="rest">Ostalo je u redu, dalje (Enter)</button>` +
         noteBox() + `</div>`;
  } else if (s.type === 'question') {
    // The examples a question is about stand next to each other, each with what was said
    // then: answers given one pair at a time are easier to reconcile when seen together.
    const q = s.q, c = C[q.id];
    h = `<h1>${esc(q.title)}</h1>` + (q.text ? `<p class="q">${esc(q.text)}</p>` : '') + `<div class="sides">`;
    q.sides.forEach((side, i) => {
      const n = side.photos.length;
      h += `<div class="side"><div class="side-head">` + (q.sides.length > 1 ? `<b>${'ABCD'[i] || ''}</b>` : '') +
           `${esc(side.label)}</div><div class="shots${n > 5 ? ' many' : ''}" style="--n:${Math.min(n, 5)}">`;
      for (const p of side.photos) {
        h += `<img src="${p.preview}" data-i="${bigList.length}" loading="lazy" alt="">`;
        bigList.push(p.preview);
      }
      if (side.context.length) {
        // The whole moment, small: two frames alone look different enough to keep both.
        const asked = new Set(side.photos.map(p => p.sha)), n = side.context.length;
        const word = n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 12 || n % 100 > 14) ? 'slike' : 'slika';
        h += `</div><div class="context">U albumu je ovaj trenutak <b>${n} ${word}</b>; ` +
             `pitamo za označene:<div class="strip">`;
        for (const p of side.context) {
          h += `<img src="${p.preview}" data-i="${bigList.length}" loading="lazy" alt=""${asked.has(p.sha) ? ' class="asked"' : ''}>`;
          bigList.push(p.preview);
        }
        h += `</div>`;
      }
      if (side.said || side.why)
        h += `</div><div class="said">` + (side.said ? `Rekli ste: <span class="tag t-${esc(side.tone)}">${esc(side.said)}</span>` : '') +
             `<span class="muted">${esc(side.why)}</span>`;
      h += `</div></div>`;
    });
    h += `</div><p class="q ask">${esc(q.ask)}</p><div class="answers list">` + options(q).map((o, i) =>
           `<button data-opt="${esc(o.id)}" class="${c && c.option === o.id ? 'on' : ''}"><kbd>${i + 1}</kbd>${esc(o.text)}</button>`).join('') +
         `</div>` + noteBox();
  } else {
    const cuts = Object.values(P).filter(p => p.source === 'click' && p.label === 'different').length;
    const joins = Object.values(P).filter(p => p.source === 'click' && p.label === 'same').length;
    h = `<h1>Hvala!</h1><p class="q">Urađeno ${n} od ${total} koraka. ` +
        (D.excerpts.length ? `Presečeno ${cuts}, spojeno ${joins}. ` : '') + `Sve je sačuvano.</p>`;
    if (D.questions.length)
      h += `<div class="recap">` + steps.map((st, i) => st.type !== 'question' ? '' :
             `<button data-go="${i}"><b>${esc(st.q.title)}</b>` +
             (!C[st.q.id] ? '— bez odgovora' : C[st.q.id].option === 'other' ? 'Drugačije' : esc(C[st.q.id].text)) +
             (notes['question:' + st.q.id] ? `<i>${esc(notes['question:' + st.q.id])}</i>` : '') + `</button>`).join('') +
           `</div>`;
  }
  $('main').innerHTML = h;
}
function showBig(i) { if (!bigList[i]) return; big = i; $('bigimg').src = bigList[i]; $('big').classList.add('open'); }
function closeBig() { big = -1; $('big').classList.remove('open'); }

$('main').addEventListener('click', ev => {
  const t = ev.target;
  if (t.closest('[data-ans]')) answer(t.closest('[data-ans]').dataset.ans);
  else if (t.closest('[data-opt]')) choose(t.closest('[data-opt]').dataset.opt);
  else if (t.closest('[data-go]')) go(+t.closest('[data-go]').dataset.go);
  else if (t.closest('[data-k]')) toggle(t.closest('[data-k]').dataset.k);
  else if (t.id === 'rest') confirmRest();
  else if (t.dataset.i !== undefined) showBig(+t.dataset.i);
});
$('main').addEventListener('change', ev => {
  if (ev.target.id !== 'note') return;
  const text = ev.target.value.trim();
  if (text) notes[noteKey()] = text; else delete notes[noteKey()];
  save();
});
$('big').addEventListener('click', closeBig);
$('prev').onclick = () => go(pos - 1); $('next').onclick = () => go(pos + 1);
document.addEventListener('keydown', ev => {
  if (ev.ctrlKey || ev.metaKey || ev.altKey) return;
  const k = ev.key, s = steps[pos];
  if (ev.target.tagName === 'INPUT') { if (k === 'Escape' || k === 'Enter') ev.target.blur(); return; }
  if (big >= 0) {
    if (k === 'Escape') closeBig();
    else if (k === 'ArrowRight') showBig(Math.min(big + 1, bigList.length - 1));
    else if (k === 'ArrowLeft') showBig(Math.max(big - 1, 0));
    else return;
  }
  else if (s.type === 'case' && /^[123]$/.test(k)) answer(['one', 'both', 'different'][+k - 1]);
  else if (s.type === 'question' && /^[1-9]$/.test(k) && options(s.q)[+k - 1]) choose(options(s.q)[+k - 1].id);
  else if (s.type === 'excerpt' && k === 'Enter') confirmRest();
  else if (k === 'ArrowRight') go(pos + 1);
  else if (k === 'ArrowLeft') go(pos - 1);
  else return;
  ev.preventDefault();
});
load();
"""


def write_page(meeting_dir, data):
    """meeting.html in the meeting folder; previews by relative path, nothing from the
    internet. The page gets only what it shows: no folder paths, no `kind` hints beyond
    what the answers need."""
    def photo(p):
        return {"sha": p["sha"], "name": p["name"], "preview": p["preview"]}
    shown = {"cases": [{"kind": c["kind"], "a": photo(c["a"]), "b": photo(c["b"])} for c in data["cases"]],
             "excerpts": [{"title": x["title"],
                           "groups": [{"photos": [photo(p) for p in g["photos"]]} for g in x["groups"]]}
                          for x in data["excerpts"]],
             "questions": [{"id": q["id"], "title": q["title"], "text": q["text"], "ask": q["ask"],
                            "options": q["options"],
                            "sides": [{"label": side["label"], "said": side["said"], "why": side["why"],
                                       "tone": side["tone"], "photos": [photo(p) for p in side["photos"]],
                                       "context": [photo(p) for p in side["context"]]}
                                      for side in q["sides"]]}
                           for q in data["questions"]]}
    payload = json.dumps(shown, ensure_ascii=False).replace("</", "<\\/")
    title = html.escape(data["title"])
    page = f"""<!doctype html>
<html lang="sr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><style>{CSS}</style></head>
<body>
<header>
  <b>{title}</b>
  <button id="prev" title="←">← nazad</button><button id="next" title="→">dalje →</button>
  <span id="progress"></span><div class="bar"><div id="fill"></div></div><span id="status" class="muted"></span>
</header>
<main id="main"></main>
<div id="big"><img id="bigimg" alt=""></div>
<script id="data" type="application/json">{payload}</script>
<script>{JS}</script>
</body></html>"""
    path = Path(meeting_dir) / PAGE_FILE
    path.write_text(page, encoding="utf-8")
    return path
