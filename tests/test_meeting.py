"""Agency meeting page: meeting.json, the excerpts, meeting_answers.json, the server
endpoint, the summary and scoring against the answers. Synthetic data only."""
import json
import urllib.error

import pytest

from culling import labels as L
from culling import meeting as M
from culling.ingest import save_photos
from tests.test_grouping import unit
from tests.test_judge import Shoot
from tests.test_labels import _request, groups_of, label, server  # noqa: F401 (fixture)


def wedding(folder, n=7):
    """An output folder with n photos 10 s apart, grouped [0,1,2] [3] [4,5] [6]."""
    folder.mkdir()
    s = Shoot(folder)
    ids = [s.add(10 * k, unit(k % 3)) for k in range(n)]
    save_photos(folder, s.photos)
    groups = groups_of(ids[0:3], ids[3:4], ids[4:6], ids[6:7])
    (folder / "groups.json").write_text(json.dumps(groups), encoding="utf-8")
    return s, ids


def name(s, k):
    return f"DSC_{k:04d}.NEF"


def define(meeting_dir, definition):
    meeting_dir.mkdir(exist_ok=True)
    (meeting_dir / M.DEFINITION_FILE).write_text(json.dumps(definition), encoding="utf-8")
    return M.load_definition(meeting_dir)


def setup(tmp_path):
    s, ids = wedding(tmp_path / "out")
    out = str(tmp_path / "out")
    definition = define(tmp_path / "meeting", {
        "cases": [{"out": out, "a": name(s, 0), "b": name(s, 1), "kind": "wide-tight"}],
        "excerpts": [{"out": out, "title": "Crkva", "first": name(s, 3), "last": name(s, 6)}]})
    return s, out, M.build_page_data(definition)


def test_excerpt_is_the_groups_that_start_in_the_range(tmp_path):
    s, out, data = setup(tmp_path)
    x = data["excerpts"][0]
    assert [[p["name"] for p in g["photos"]] for g in x["groups"]] == [[name(s, 3)], [name(s, 4), name(s, 5)], [name(s, 6)]]
    links = M.excerpt_links(x)
    assert [(l["a"]["name"], l["b"]["name"], l["pipeline"]) for l in links] == [
        (name(s, 3), name(s, 4), "different"), (name(s, 4), name(s, 5), "same"), (name(s, 5), name(s, 6), "different")]
    assert data["cases"][0]["a"]["sha"] == s.photos[0]["sha256"] and data["cases"][0]["b"]["preview"].startswith("previews/o1/")


def test_definition_errors_are_clear(tmp_path):
    s, ids = wedding(tmp_path / "out")
    out, m = str(tmp_path / "out"), tmp_path / "meeting"
    case = {"out": out, "a": name(s, 0), "b": name(s, 1), "kind": "k"}
    for bad in ({"cases": [], "excerpts": []}, {"cases": [case], "extra": 1}, {"cases": [{**case, "note": "x"}]},
                {"cases": [{"out": out, "a": name(s, 0)}]},
                {"excerpts": [{"out": out, "title": "t", "first": name(s, 0), "last": name(s, 1)}] * 2}):
        with pytest.raises(ValueError):
            define(m, bad)
    for bad in ({"cases": [{**case, "b": "nope.NEF"}]},
                {"cases": [case], "excerpts": [{"out": out, "title": "t", "first": name(s, 0), "last": name(s, 2)}]},  # pair shown twice
                {"excerpts": [{"out": out, "title": "t", "first": name(s, 5), "last": name(s, 2)}]},
                {"cases": [{**case, "out": str(tmp_path / "missing")}]}):
        with pytest.raises(ValueError):
            M.build_page_data(define(m, bad))


def test_previews_are_copied_and_the_page_is_local(tmp_path):
    s, out, data = setup(tmp_path)
    m = tmp_path / "meeting"
    assert M.copy_previews(m, data) == 6 and M.copy_previews(m, data) == 0     # 2 case photos + 4 in the excerpt
    assert (m / data["cases"][0]["a"]["preview"]).exists()
    page = M.write_page(m, data).read_text(encoding="utf-8")
    assert "Crkva" in page and s.photos[4]["sha256"] in page
    assert "http://" not in page and "https://" not in page and out.replace("\\", "\\\\") not in page


def pair(a, b, value, **extra):
    return {**label(a, b, value), **extra}


def test_normalise_answers():
    a, b, c = ({"sha256": ch * 64} for ch in "abc")
    ok = M.normalise_answers({"pairs": [pair(a, b, "same", source="confirmed", part="Crkva"),
                                        pair(a, b, "different", part="Crkva"),            # the later entry wins
                                        pair(b, c, "same", source="case", answer="both", kind="wide-tight", part="case")],
                              "notes": {"excerpt:Crkva": " baka je ušla ", "case:x": "  "}})
    assert [(p["label"], p["source"], p["answer"]) for p in ok["pairs"]] == [("different", "click", ""), ("same", "case", "both")]
    assert ok["pairs"][1]["kind"] == "wide-tight" and ok["notes"] == {"excerpt:Crkva": "baka je ušla"}
    for bad in ([], {"pairs": {}}, {"pairs": [pair(a, b, "same", source="guess")]},
                {"pairs": [pair(a, b, "same", source="case")]},                               # a case needs an answer
                {"pairs": [pair(a, b, "same", source="case", answer="different")]},           # ... that matches the label
                {"pairs": [pair(a, b, "same", answer="one")]}, {"pairs": [{"a_sha": "zz"}]}):
        with pytest.raises(ValueError):
            M.normalise_answers(bad)


def test_server_stores_answers(server, tmp_path):  # noqa: F811
    srv, base = server
    assert _request(base + "/meeting") == (200, {"pairs": [], "notes": {}, "choices": {}})
    a, b = {"sha256": "a" * 64}, {"sha256": "b" * 64}
    body = {"pairs": [pair(a, b, "different", part="Crkva")], "notes": {"excerpt:Crkva": "x"}}
    assert _request(base + "/meeting", json.dumps(body).encode()) == (200, {"saved": 1})
    saved = M.load_answers(tmp_path)
    assert saved["pairs"][0]["source"] == "click" and saved["notes"] == {"excerpt:Crkva": "x"}
    body["choices"] = {"siri-uzi": {"option": "obe", "text": "Uvek obe"}}
    assert _request(base + "/meeting", json.dumps(body).encode()) == (200, {"saved": 2})
    assert M.load_answers(tmp_path)["choices"]["siri-uzi"]["option"] == "obe"
    with pytest.raises(urllib.error.HTTPError) as err:
        _request(base + "/meeting", json.dumps({"pairs": [pair(a, b, "maybe")]}).encode())
    assert err.value.code == 400 and len(M.load_answers(tmp_path)["pairs"]) == 1


def test_summary_and_score_against_the_answers(tmp_path):
    s, out, data = setup(tmp_path)
    p = s.photos
    answers = M.normalise_answers({"pairs": [
        pair(p[0], p[1], "same", source="case", answer="one", kind="wide-tight", part="case"),
        pair(p[3], p[4], "same", part="Crkva"),                           # join: the program split
        pair(p[4], p[5], "different", part="Crkva"),                      # cut: the program joined
        pair(p[5], p[6], "different", source="confirmed", part="Crkva"),
        pair({"sha256": "e" * 64}, {"sha256": "f" * 64}, "same", part="other wedding")],
        "notes": {"excerpt:Crkva": "drugi ljudi"}})
    L.save_labels(out, [label(p[3], p[4], "different"), label(p[5], p[6], "different")])   # the user's own labels
    text = M.summary(answers, data)
    assert "1 of 1 answered" in text and "one is enough" in text
    assert "3 of 3 pairs looked at, 1 cuts" in text and "1 joins" in text
    assert f"CUT   {name(s, 4)} | {name(s, 5)}" in text and f"JOIN  {name(s, 3)} + {name(s, 4)}" in text
    assert "drugi ljudi" in text and "1 pairs differ" in text and "agency same (click), labels.json different" in text

    path = M.save_answers(tmp_path / "meeting", answers)
    result = L.score(L.read_labels_file(path), p, json.loads((tmp_path / "out" / "groups.json").read_text()))
    assert (result["n_scored"], result["n_missing"]) == (4, 1)            # the other wedding's pair is skipped
    assert (result["correct"], result["false_merges"], result["missed_merges"]) == (2, 1, 1)


def question(s, out, **extra):
    return {"id": "siri-uzi", "title": "Širi i uži kadar", "ask": "Šta program treba da zadrži?",
            "sides": [{"out": out, "photos": [name(s, 0), name(s, 1)], "label": "Kod stolova", "said": "obe", "tone": "keep"},
                      {"out": out, "photos": [name(s, 4)], "said": "jedna", "tone": "cut", "why": "iste su"}],
            "options": [{"id": "obe", "text": "Uvek obe"}, {"id": "jedna", "text": "Uvek jednu"}], **extra}


def test_questions_show_their_examples_side_by_side(tmp_path):
    s, ids = wedding(tmp_path / "out")
    out, m = str(tmp_path / "out"), tmp_path / "meeting"
    data = M.build_page_data(define(m, {"title": "Pitanja <posle>", "questions": [question(s, out)]}))
    q = data["questions"][0]
    assert [[p["name"] for p in side["photos"]] for side in q["sides"]] == [[name(s, 0), name(s, 1)], [name(s, 4)]]
    assert (q["sides"][0]["said"], q["sides"][1]["tone"], q["sides"][0]["why"], q["text"]) == ("obe", "cut", "", "")
    assert M.copy_previews(m, data) == 3
    page = M.write_page(m, data).read_text(encoding="utf-8")
    assert "Pitanja &lt;posle&gt;" in page and "Uvek jednu" in page and "iste su" in page
    assert "http://" not in page and out.replace("\\", "\\\\") not in page


def test_question_errors_are_clear(tmp_path):
    s, ids = wedding(tmp_path / "out")
    out, m = str(tmp_path / "out"), tmp_path / "meeting"
    q = question(s, out)
    for bad in ({**q, "id": ""}, {**q, "extra": 1}, {k: v for k, v in q.items() if k != "ask"},
                {**q, "options": q["options"][:1]}, {**q, "options": q["options"] * 2},
                {**q, "options": q["options"] + [{"id": "other", "text": "x"}]},          # the page's own answer
                {**q, "sides": [{"out": out, "photos": []}]}, {**q, "sides": [{"photos": [name(s, 0)]}]},
                {**q, "sides": [{**q["sides"][0], "tone": "red"}]}):
        with pytest.raises(ValueError):
            define(m, {"questions": [bad]})
    with pytest.raises(ValueError):
        define(m, {"questions": [q, q]})                                                  # the same id twice
    with pytest.raises(ValueError):
        M.build_page_data(define(m, {"questions": [{**q, "sides": [{"out": out, "photos": ["nope.NEF"]}]}]}))


def test_choices_keep_the_wording_they_were_given_with():
    ok = M.normalise_answers({"choices": {"siri-uzi": {"option": " obe ", "text": "Uvek obe", "question": "Šta?",
                                                       "at": "2026-11-26T12:00:00.123"}}})
    assert ok == {"pairs": [], "notes": {}, "choices": {"siri-uzi": {
        "option": "obe", "text": "Uvek obe", "question": "Šta?", "at": "2026-11-26T12:00:00"}}}
    for bad in ({"choices": []}, {"choices": {"q": "obe"}}, {"choices": {"q": {"option": ""}}}):
        with pytest.raises(ValueError):
            M.normalise_answers(bad)


def test_summary_lists_the_answers_to_questions(tmp_path):
    s, ids = wedding(tmp_path / "out")
    out = str(tmp_path / "out")
    second = {**question(s, out), "id": "gosti", "title": "Gosti", "sides": []}
    data = M.build_page_data(define(tmp_path / "meeting", {"questions": [question(s, out), second]}))
    answers = M.normalise_answers({"choices": {"siri-uzi": {"option": "other", "text": "Drugačije"}},
                                   "notes": {"question:siri-uzi": "zavisi od stola"}})
    text = M.summary(answers, data)
    assert "questions: 1 of 2 answered" in text and "Širi i uži kadar: [other] Drugačije" in text
    assert "note: zavisi od stola" in text and "Gosti: -" in text and "disputed pairs" not in text
