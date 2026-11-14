"""Ground truth for "best photo": the user marks, per multi-photo group, the photo(s) the
agency would deliver (`python cull.py pick`). Then `python cull.py pick-score` checks
ranking.json against those picks.

  build_items        the multi-photo groups of groups.json, in capture order
  write_page         picks.html: one group per screen, click to pick, rules on the page
  load/save_picks    picks.json, keyed by the member photos' sha256 (survives re-grouping)
  score_ranking      ranking.json vs picks: is every picked photo kept, how many extra keeps,
                     does the model's choice match the user's

By default the page shows nothing of the program's own choice, so the picks are not
steered by it. `cull.py pick --review-model` is the other mode (build_model_items): one
variant that the model ranked per screen, with the model's winner, its reason and the
flaws it named, so the user can see how the model decides and only agree or correct it.
Those picks are marked `seen_model` in picks.json.
"""
import html
import json
import os
from datetime import datetime
from pathlib import Path

PICKS_FILE = "picks.json"
PAGE_FILE = "picks.html"
REVERSED_FILE = "ranking_reversed.json"  # optional reversed-order check, read by the review mode


def group_key(shas):
    """A group's id in picks.json: its photos' sha256, sorted and joined."""
    return "|".join(sorted(shas))


def build_items(photos, groups_data):
    """[{key, group_id, photos: [{sha, name, preview}]}] for every group with two or more
    usable photos (ingested, with a preview), in the order of groups.json."""
    by_id = {p["id"]: p for p in photos}
    items = []
    for g in groups_data["groups"]:
        members = [by_id[pid] for pid in g["photo_ids"]
                   if pid in by_id and by_id[pid].get("sha256") and by_id[pid].get("preview_file")]
        if len(members) < 2:
            continue
        items.append({"key": group_key(p["sha256"] for p in members), "group_id": g["group_id"],
                      "photos": [{"sha": p["sha256"], "name": Path(p["primary_path"]).name,
                                  "preview": p["preview_file"]} for p in members]})
    return items


def build_model_items(photos, ranking, reversed_rows=None):
    """Items for the review mode: every multi-frame variant of ranking.json that has a valid
    answer, with what the model said: {key, group_id, title, photos, model: {winner, order,
    issues: {sha: issue}, reason, reversed}}. Photos are in the order the model saw them, so
    "photo 2" in its reason is tile 2.

    `reversed_rows` is optional: rows {photo_ids, winner_reversed, reason_reversed} of a
    check that asked the same variant with the photos in reversed order. `reversed` is then
    {winner, reason}; a different winner means the answer depended on the order."""
    by_id = {p["id"]: p for p in photos}
    reversed_by_ids = {tuple(r["photo_ids"]): r for r in reversed_rows or [] if r.get("photo_ids")}
    items = []
    for v in ranking.get("variants") or []:
        answer = (ranking.get("answers") or {}).get(v["key"])
        members = [by_id.get(pid) for pid in v["photo_ids"]]
        if v["kind"] != "multi" or not answer or not answer.get("order") or not all(
                p and p.get("sha256") and p.get("preview_file") for p in members):
            continue
        sha = {p["id"]: p["sha256"] for p in members}
        model = {"winner": sha[answer["order"][0]], "order": [sha[pid] for pid in answer["order"] if pid in sha],
                 "issues": {sha[pid]: issue for pid, issue in (answer.get("issues") or {}).items() if pid in sha},
                 "reason": answer.get("reason") or "", "reversed": None}
        rev = reversed_by_ids.get(tuple(v["photo_ids"]))
        if rev and rev.get("winner_reversed") in sha:
            model["reversed"] = {"winner": sha[rev["winner_reversed"]], "reason": rev.get("reason_reversed") or ""}
        items.append({"key": group_key(sha.values()), "group_id": v["group_id"],
                      "title": f"{v['group_id']} · varijanta {v['index']}",
                      "photos": [{"sha": p["sha256"], "name": Path(p["primary_path"]).name,
                                  "preview": p["preview_file"]} for p in members],
                      "model": model})
    return items


# ----------------------------------------------------------------------- picks.json

def normalise_picks(raw):
    """Validate what the page POSTs: {key: {picked: [sha], none: bool, tossup: bool,
    names: [..], at: iso, seen_model: bool}}; seen_model marks a pick made in the review
    mode, with the model's choice on the screen. A group with nothing picked and `none` false is dropped
    (not done). Raises ValueError on anything malformed."""
    if not isinstance(raw, dict):
        raise ValueError("picks must be a JSON object")
    out = {}
    for key, entry in raw.items():
        if not isinstance(key, str) or not isinstance(entry, dict):
            raise ValueError("every pick must be an object under a string key")
        members = set(key.split("|"))
        picked = entry.get("picked") or []
        if not isinstance(picked, list) or not all(isinstance(s, str) and s in members for s in picked):
            raise ValueError(f"picked photos must belong to their group ({key[:20]}...)")
        none = bool(entry.get("none"))
        if none and picked:
            raise ValueError("a group cannot have picks and 'none' at the same time")
        if not picked and not none:
            continue
        out[key] = {"picked": sorted(set(picked)), "none": none, "tossup": bool(entry.get("tossup")) and not none,
                    "names": [str(n) for n in entry.get("names") or []][:50],
                    "at": str(entry.get("at") or datetime.now().isoformat(timespec="seconds"))}
        if entry.get("seen_model"):
            out[key]["seen_model"] = True
    return out


def load_picks(out_dir):
    path = Path(out_dir) / PICKS_FILE
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f).get("groups", {})


def save_picks(out_dir, picks):
    path = Path(out_dir) / PICKS_FILE
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"updated": datetime.now().isoformat(timespec="seconds"), "groups": picks}, f,
                  indent=1, ensure_ascii=False)
    os.replace(tmp, path)


# ------------------------------------------------------------------------- the page

RULES = """
<h2>Pravila</h2>
<ol>
<li>Za svaku grupu označi <b>svaku sliku koju bi agencija isporučila mladencima</b>. Obično je to
<b>jedna</b>.</li>
<li><b>Dve ili više</b> označi samo kad bi zaista isporučila obe: drugačiji kadar (širok i krupan,
uspravan i položen), drugačiji trenutak ili izraz koji vredi imati, ili su u grupi pomešani
različiti ljudi ili momenti.</li>
<li>Ako su dve slike skoro iste i stvarno ne možeš da odlučiš, <b>izaberi jednu</b> i pritisni
<b>T</b> („svejedno je“). Te grupe se ne računaju kad merimo da li je program pogodio.</li>
<li>Ako nijednu ne bi isporučila (sve mutne, zatvorene oči…), pritisni <b>N</b> („nijedna“).</li>
<li>Gledaj kao fotograf: oštrina i oči glavnih ljudi, izraz, trenutak, kompozicija. Gosti u
pozadini se ne računaju.</li>
<li>Ne razmišljaj predugo: 10–20 sekundi po grupi je sasvim dovoljno.</li>
</ol>
<h2>Kako</h2>
<table>
<tr><td><b>klik</b> na sliku ili taster <b>1</b>–<b>9</b></td><td>označi / skini oznaku</td></tr>
<tr><td><b>lupa 🔍</b> ili <b>Z</b> pa broj</td><td>slika preko celog ekrana (tamo: <b>Space</b> označi, <b>←/→</b>, <b>Esc</b>)</td></tr>
<tr><td><b>Enter</b></td><td>sledeća neurađena grupa</td></tr>
<tr><td><b>←</b> / <b>→</b></td><td>prethodna / sledeća grupa</td></tr>
<tr><td><b>N</b></td><td>nijedna slika nije za isporuku</td></tr>
<tr><td><b>T</b></td><td>svejedno je (izbor između skoro istih)</td></tr>
</table>
<p>Sve se čuva odmah u <code>picks.json</code>. Možeš da prekineš kad hoćeš i nastaviš kasnije istom
komandom.</p>
"""

RULES_REVIEW = """
<h2>Šta gledaš</h2>
<ol>
<li>Na svakom ekranu je jedna <b>varijanta</b>: slike koje je program proglasio skoro istim. Model
je dobio baš te slike, tim redom i sa tim brojevima, i izabrao najbolju.</li>
<li><b>Plavi isprekidani okvir i „MODEL ★“</b> je slika koju je model izabrao. Ispod slika je
njegovo obrazloženje (na engleskom), a ispod svake slike mesto koje joj je dao i mana koju je naveo.</li>
<li>Ako postoji provera <b>obrnutim redosledom</b>, piše da li je model izabrao istu sliku kad su
mu iste slike date unazad. Ako nije, izbor je zavisio od redosleda, a ne od slike.</li>
</ol>
<h2>Šta radiš</h2>
<ol>
<li>Ako je izbor modela u redu, pritisni <b>A</b> („slažem se“).</li>
<li>Ako bi ti izabrala drugu, klikni na nju (ili taster <b>1</b>–<b>9</b>).</li>
<li>Ako je svejedno koja se isporuči, pritisni <b>T</b>: uzima se izbor modela i varijanta se ne računa.</li>
<li>Ako nijedna nije za isporuku, pritisni <b>N</b>.</li>
</ol>
<table>
<tr><td><b>A</b></td><td>slažem se sa modelom</td></tr>
<tr><td><b>klik</b> ili <b>1</b>–<b>9</b></td><td>označi / skini oznaku</td></tr>
<tr><td><b>lupa 🔍</b> ili <b>Z</b> pa broj</td><td>slika preko celog ekrana (<b>Space</b> označi, <b>←/→</b>, <b>Esc</b>)</td></tr>
<tr><td><b>Enter</b></td><td>sledeća neurađena</td></tr>
<tr><td><b>←</b> / <b>→</b></td><td>prethodna / sledeća</td></tr>
<tr><td><b>T</b> / <b>N</b></td><td>svejedno je / nijedna</td></tr>
</table>
<p>Sve se čuva odmah u <code>picks.json</code>.</p>
"""

CSS = """
:root { --bg:#f6f6f4; --card:#fff; --text:#1d1d1f; --muted:#6b6b70; --line:#e2e2e0; --pick:#15803d;
        --accent:#2f6fde; --warn:#b45309; }
@media (prefers-color-scheme: dark) {
  :root { --bg:#161618; --card:#202024; --text:#ececee; --muted:#9a9aa2; --line:#33333a; --pick:#4ade80;
          --accent:#6ea0ff; --warn:#fbbf24; } }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--text); font:15px/1.45 system-ui, "Segoe UI", sans-serif; }
header { position:sticky; top:0; z-index:2; background:var(--bg); border-bottom:1px solid var(--line);
         padding:10px 18px; display:flex; flex-wrap:wrap; gap:14px; align-items:center; }
header button { font:inherit; padding:4px 12px; border:1px solid var(--line); border-radius:6px;
                background:var(--card); color:var(--text); cursor:pointer; }
header button.on { background:var(--accent); color:#fff; border-color:transparent; }
.muted { color:var(--muted); } #status.err { color:#b91c1c; font-weight:600; }
.bar { flex:1; min-width:120px; height:8px; background:var(--line); border-radius:4px; overflow:hidden; }
.bar div { height:100%; background:var(--pick); }
main { padding:14px 18px 40px; }
.grid { display:flex; flex-wrap:wrap; gap:12px; align-items:flex-start; }
.tile { position:relative; background:var(--card); border:4px solid transparent; border-radius:8px; padding:4px;
        cursor:pointer; }
.tile.picked { border-color:var(--pick); }
.tile img { display:block; max-width:var(--tw); max-height:var(--tw); border-radius:4px; }
.tile .num { position:absolute; top:10px; left:10px; background:rgba(0,0,0,.7); color:#fff; font-weight:700;
             padding:1px 8px; border-radius:4px; }
.tile .star { position:absolute; top:8px; right:10px; font-size:26px; color:var(--pick); display:none;
              text-shadow:0 0 3px #000; }
.tile.picked .star { display:block; }
.tile .zoom { position:absolute; bottom:30px; right:10px; background:rgba(0,0,0,.6); color:#fff; border:0;
              border-radius:4px; padding:2px 7px; cursor:zoom-in; font-size:15px; }
.tile .cap { font-size:12px; color:var(--muted); padding-top:3px; }
.state { margin:10px 0 14px; font-size:16px; } .state b.none { color:var(--warn); }
#rules { max-width:860px; background:var(--card); border:1px solid var(--line); border-radius:8px;
         padding:6px 20px 12px; margin-bottom:16px; }
#rules td { padding:2px 14px 2px 0; }
#big { position:fixed; inset:0; background:rgba(0,0,0,.92); display:none; z-index:5; align-items:center;
       justify-content:center; flex-direction:column; color:#eee; }
.tile.model { outline:4px dashed var(--accent); outline-offset:2px; }
.tile .mbadge { position:absolute; top:10px; left:44px; background:var(--accent); color:#fff; font-weight:700;
                padding:1px 8px; border-radius:4px; }
.tile .cap b { color:var(--text); } .tile .cap .flaw { color:var(--warn); font-weight:600; }
#model { max-width:980px; background:var(--card); border:1px solid var(--line); border-left:5px solid var(--accent);
         border-radius:8px; padding:10px 16px; margin-top:16px; display:none; }
#model.on { display:block; } #model p { margin:6px 0; } #model q { font-style:italic; }
#model .ok { color:var(--pick); font-weight:600; } #model .bad { color:var(--warn); font-weight:600; }
#agree { display:none; }
#big.open { display:flex; } #big img { max-width:96vw; max-height:88vh; border:5px solid transparent; }
#big img.picked { border-color:#4ade80; }
"""

JS = """
const D = JSON.parse(document.getElementById('data').textContent);
const items = D.items;
let picks = {}, pos = 0, zoomed = -1, zoomArmed = false;
const $ = id => document.getElementById(id);
const done = it => { const p = picks[it.key]; return !!p && (p.none || p.picked.length > 0); };

async function load() {
  try { const r = await fetch('/picks', {cache:'no-store'}); if (r.ok) picks = await r.json(); }
  catch (e) { status('Otvori stranicu komandom "cull.py pick" - kao fajl ne može da čuva.', true); }
  const first = items.findIndex(it => !done(it));
  pos = first < 0 ? 0 : first;
  if (Object.keys(picks).length) $('rules').open = false;
  render();
}
let saving = null, again = false;
async function save() {
  if (saving) { again = true; return; }
  saving = (async () => {
    try {
      const r = await fetch('/picks', {method:'POST', headers:{'Content-Type':'application/json'},
                                       body: JSON.stringify(picks)});
      if (!r.ok) throw new Error('HTTP ' + r.status);
      status('sačuvano', false);
    } catch (e) { status('NIJE sačuvano: ' + e.message, true); }
  })();
  await saving; saving = null;
  if (again) { again = false; save(); }
}
function status(text, err) { const s = $('status'); s.textContent = text; s.className = err ? 'err' : 'muted'; }
function entry(it) {
  const e = picks[it.key] || (picks[it.key] = {picked: [], none: false, tossup: false,
                                               names: it.photos.map(p => p.name)});
  if (it.model) e.seen_model = true;
  return e;
}
const esc = t => String(t).replace(/[&<>"]/g, c => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;'}[c]));
const ISSUE = {none: 'bez mane', eyes_closed: 'zatvorene oči', blurred: 'mutno', bad_expression: 'loš izraz',
               obstructed: 'zaklonjeno / odsečeno', exposure: 'ekspozicija'};
function agree() {
  const it = items[pos]; if (!it.model) return;
  const e = entry(it); e.none = false; e.picked = [it.model.winner];
  touch(it);
}
function modelBox(it) {
  const m = it.model, n = it.photos.length, num = sha => it.photos.findIndex(p => p.sha === sha) + 1;
  let h = `<p><b>Model bira sliku ${num(m.winner)}.</b> <q>${esc(m.reason)}</q></p>` +
          `<p class="muted">Redosled modela, od najbolje: ${m.order.map(num).join(', ')}</p>`;
  if (m.reversed) {
    const same = m.reversed.winner === m.winner;
    h += `<p>Iste slike u obrnutom redosledu: ` + (same
      ? `<span class="ok">isti izbor (slika ${num(m.winner)})</span>`
      : `<span class="bad">drugi izbor: slika ${num(m.reversed.winner)}</span> — izbor zavisi od redosleda`) +
      `. <q>${esc(m.reversed.reason)}</q> <span class="muted">(u tom pitanju brojevi su bili obrnuti: ` +
      `tamo „Photo 1“ = ovde slika ${n}, „Photo ${n}“ = ovde slika 1)</span></p>`;
  }
  return h;
}
function touch(it) {
  const e = entry(it); e.at = new Date().toISOString().slice(0, 19);
  if (!e.none && !e.picked.length) { delete picks[it.key]; }
  save(); render();
}
function toggle(k) {
  const it = items[pos], ph = it.photos[k]; if (!ph) return;
  const e = entry(it); e.none = false;
  const i = e.picked.indexOf(ph.sha);
  if (i >= 0) e.picked.splice(i, 1); else e.picked.push(ph.sha);
  if (!e.picked.length) e.tossup = false;
  touch(it);
}
function setNone() {
  const it = items[pos], e = entry(it);
  e.none = !e.none; if (e.none) { e.picked = []; e.tossup = false; }
  touch(it);
}
function setTossup() {
  const it = items[pos], e = entry(it);
  if (!e.picked.length && it.model) e.picked = [it.model.winner];
  if (!e.picked.length) { status('Prvo izaberi sliku, pa T.', true); return; }
  e.tossup = !e.tossup; touch(it);
}
function go(i) { pos = Math.max(0, Math.min(items.length - 1, i)); closeBig(); render(); window.scrollTo(0, 0); }
function nextTodo() {
  for (let k = 1; k <= items.length; k++) { const i = (pos + k) % items.length; if (!done(items[i])) return go(i); }
  status('Sve grupe su urađene. Hvala!', false);
}
function render() {
  const it = items[pos], e = picks[it.key];
  const n = items.filter(done).length;
  $('progress').textContent = `grupa ${pos + 1} / ${items.length} · urađeno ${n}`;
  $('fill').style.width = (100 * n / items.length) + '%';
  $('none').className = e && e.none ? 'on' : '';
  $('tossup').className = e && e.tossup ? 'on' : '';
  const tw = it.photos.length <= 2 ? 620 : it.photos.length <= 4 ? 440 : it.photos.length <= 6 ? 360 : 290;
  document.body.style.setProperty('--tw', tw + 'px');
  let state = 'Još nije urađeno.';
  if (e && e.none) state = '<b class="none">Nijedna</b> slika nije za isporuku.';
  else if (e && e.picked.length) state = `Izabrano: <b>${e.picked.length}</b>` + (e.tossup ? ' · svejedno je' : '');
  const m = it.model;
  if (m && e && e.picked.length && !e.tossup)
    state += e.picked.includes(m.winner) ? ' · slažeš se sa modelom' : ' · <b class="none">ne slažeš se sa modelom</b>';
  $('state').innerHTML = `${it.title || it.group_id} · ${it.photos.length} slika · ${state}`;
  $('agree').style.display = m ? 'inline-block' : 'none';
  $('model').className = m ? 'on' : ''; $('model').innerHTML = m ? modelBox(it) : '';
  $('grid').innerHTML = it.photos.map((p, k) => {
    const on = (e && e.picked.includes(p.sha) ? ' picked' : '') + (m && m.winner === p.sha ? ' model' : '');
    let cap = p.name;
    if (m) {
      const issue = m.issues[p.sha], place = m.order.indexOf(p.sha) + 1;
      cap += ` · model: <b>#${place}</b> · ` + (issue && issue !== 'none'
        ? `<span class="flaw">${ISSUE[issue] || esc(issue)}</span>` : (ISSUE[issue] || 'bez ocene'));
    }
    return `<div class="tile${on}" data-k="${k}"><img src="${p.preview}" alt="">` +
      `<span class="num">${k + 1}</span>` + (m && m.winner === p.sha ? '<span class="mbadge">MODEL ★</span>' : '') +
      `<span class="star">★</span>` +
      `<button class="zoom" data-z="${k}" title="preko celog ekrana (Z pa ${k + 1})">🔍</button>` +
      `<div class="cap">${cap}</div></div>`;
  }).join('');
  if (zoomed >= 0) showBig(zoomed);
}
function showBig(k) {
  const it = items[pos]; if (!it.photos[k]) return; zoomed = k; status('', false);
  const e = picks[it.key], p = it.photos[k];
  $('bigimg').src = p.preview; $('bigimg').className = e && e.picked.includes(p.sha) ? 'picked' : '';
  $('bigcap').textContent = `${k + 1} / ${it.photos.length} · ${p.name} · Space označi · ←/→ · Esc`;
  $('big').classList.add('open');
}
function closeBig() { zoomed = -1; $('big').classList.remove('open'); }

$('grid').addEventListener('click', ev => {
  const z = ev.target.closest('.zoom'); if (z) { showBig(+z.dataset.z); return; }
  const t = ev.target.closest('.tile'); if (t) toggle(+t.dataset.k);
});
$('big').addEventListener('click', () => closeBig());
$('prev').onclick = () => go(pos - 1); $('next').onclick = () => go(pos + 1);
$('todo').onclick = nextTodo; $('none').onclick = setNone; $('tossup').onclick = setTossup;
$('agree').onclick = agree;
document.addEventListener('keydown', ev => {
  if (ev.ctrlKey || ev.metaKey || ev.altKey) return;
  const k = ev.key;
  if (zoomed >= 0) {
    if (k === 'Escape') closeBig();
    else if (k === ' ') { toggle(zoomed); }
    else if (k === 'ArrowRight') showBig(Math.min(zoomed + 1, items[pos].photos.length - 1));
    else if (k === 'ArrowLeft') showBig(Math.max(zoomed - 1, 0));
    else return;
    ev.preventDefault(); return;
  }
  if (/^[1-9]$/.test(k)) { if (zoomArmed) { zoomArmed = false; showBig(+k - 1); } else toggle(+k - 1); }
  else if (k === 'z' || k === 'Z') { zoomArmed = true; status('Z: pritisni broj slike', false); return; }
  else if (k === 'Enter') nextTodo();
  else if (k === 'ArrowRight') go(pos + 1);
  else if (k === 'ArrowLeft') go(pos - 1);
  else if (k === 'n' || k === 'N') setNone();
  else if (k === 't' || k === 'T') setTossup();
  else if (k === 'a' || k === 'A') agree();
  else return;
  zoomArmed = false; ev.preventDefault();
});
load();
"""


def write_page(out_dir, items, review=False):
    """picks.html in the output folder; previews by relative path, nothing from the internet.
    `review` only changes the title and the rules; the model's choice is shown for every
    item that has a `model` (build_model_items)."""
    title = "Izbor modela: najbolja slika" if review else "Najbolja slika iz grupe"
    data = json.dumps({"items": items}, ensure_ascii=False).replace("</", "<\\/")
    page = f"""<!doctype html>
<html lang="sr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><style>{CSS}</style></head>
<body>
<header>
  <b>{title}</b>
  <button id="prev" title="←">← prethodna</button><button id="next" title="→">sledeća →</button>
  <button id="todo" title="Enter">sledeća neurađena (Enter)</button>
  <button id="agree" title="A">slažem se sa modelom (A)</button>
  <button id="none" title="N">nijedna (N)</button><button id="tossup" title="T">svejedno je (T)</button>
  <span id="progress"></span><div class="bar"><div id="fill"></div></div><span id="status" class="muted"></span>
</header>
<main>
<details id="rules" open><summary><b>Pravila i tasteri</b> (klikni da sakriješ / prikažeš)</summary>{RULES_REVIEW if review else RULES}</details>
<div class="state" id="state"></div>
<div class="grid" id="grid"></div>
<div id="model"></div>
</main>
<div id="big"><img id="bigimg" alt=""><div id="bigcap"></div></div>
<script id="data" type="application/json">{data}</script>
<script>{JS}</script>
</body></html>"""
    path = Path(out_dir) / PAGE_FILE
    path.write_text(page, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------- score

def score_ranking(picks, photos, ranking):
    """ranking.json against picks.json, on the groups the user has done.

    - picked_kept: picked photos that the ranking keeps (anything else is a good photo the
      ranking would only show in review: today `maybe`, later possibly lost);
    - extra_keeps: kept photos the user did not pick (review time);
    - model_hits: variants the model ranked (not toss-ups) whose winner was picked.
    Photos are matched by sha256, so picks made under another grouping still count."""
    sha_of = {p["id"]: p["sha256"] for p in photos if p.get("sha256")}
    decision = {sha_of[pid]: d for pid, d in (ranking.get("photos") or {}).items() if pid in sha_of}
    r = {"groups": 0, "none_groups": 0, "tossup_groups": 0, "picked": 0, "picked_kept": 0, "extra_keeps": 0,
         "model_variants": 0, "model_hits": 0, "not_in_ranking": 0, "missed": []}
    for key, entry in picks.items():
        members = key.split("|")
        if not all(s in decision for s in members):
            r["not_in_ranking"] += 1
            continue
        r["groups"] += 1
        r["none_groups"] += entry["none"]
        r["tossup_groups"] += entry["tossup"]
        picked = set(entry["picked"])
        for s in members:
            d = decision[s]
            if s in picked:
                r["picked"] += 1
                if d["decision"] == "keep":
                    r["picked_kept"] += 1
                else:
                    r["missed"].append({"sha": s, "why": d["why"], "group": d["group_id"]})
            elif d["decision"] == "keep":
                r["extra_keeps"] += 1
        if entry["tossup"] or entry["none"]:
            continue
        winners = {s for s in members if decision[s]["why"] == "best_of_variant"}
        for s in winners:
            r["model_variants"] += 1
            r["model_hits"] += s in picked
    return r


def format_score(r, names):
    """`names` is {sha256: file name}."""
    lines = [f"picks vs ranking.json: {r['groups']} groups done ({r['none_groups']} 'none', "
             f"{r['tossup_groups']} toss-ups); {r['not_in_ranking']} picked groups not in ranking.json"]
    if r["picked"]:
        lines.append(f"picked photos kept: {r['picked_kept']} of {r['picked']} "
                     f"({100 * r['picked_kept'] / r['picked']:.0f} %; the rest are only 'maybe')")
    lines.append(f"kept but not picked: {r['extra_keeps']} (review time)")
    if r["model_variants"]:
        lines.append(f"model's choice in a variant was picked: {r['model_hits']} of {r['model_variants']} "
                     f"(toss-ups and 'none' excluded)")
    for m in r["missed"]:
        lines.append(f"  picked but maybe: {names.get(m['sha'], m['sha'][:12])} ({m['group']}, {m['why']})")
    return "\n".join(lines)
