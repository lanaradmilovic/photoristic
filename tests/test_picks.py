"""Best-photo picks: the items, picks.json validation, the server endpoint, the page and
the comparison with ranking.json. Synthetic data only."""
import json
import urllib.error

import pytest

from culling import picks as P
from tests.test_judge import Shoot
from tests.test_labels import _request, groups_of, server  # noqa: F401 (fixture)
from tests.test_grouping import unit


def shoot_with_groups(tmp_path=None):
    s = Shoot(tmp_path)
    ids = [s.add(k, unit(k % 3)) for k in range(6)]
    failed = s.add(9, None, status="error")
    s.photos[-1]["preview_file"] = None
    groups = groups_of(ids[0:3], ids[3:4], [ids[4], failed], ids[5:6])
    return s, ids, groups


def sha(s, pid):
    return next(p["sha256"] for p in s.photos if p["id"] == pid)


def test_items_are_the_multi_photo_groups_with_previews():
    s, ids, groups = shoot_with_groups()
    items = P.build_items(s.photos, groups)
    assert [it["group_id"] for it in items] == ["g0001"]          # g0003 has only one usable photo
    assert [p["sha"] for p in items[0]["photos"]] == [sha(s, i) for i in ids[0:3]]
    assert items[0]["key"] == P.group_key(sha(s, i) for i in reversed(ids[0:3]))   # order-independent key


def test_normalise_picks():
    key = "a|b|c"
    ok = P.normalise_picks({key: {"picked": ["b", "b"], "tossup": True, "names": ["x"]},
                            "d|e": {"picked": [], "none": False},          # nothing chosen: not done, dropped
                            "f|g": {"none": True, "tossup": True}})
    assert ok[key]["picked"] == ["b"] and ok[key]["tossup"] is True
    assert "d|e" not in ok and ok["f|g"] == {**ok["f|g"], "none": True, "tossup": False}
    for bad in ([1], {key: {"picked": ["zzz"]}}, {key: {"picked": ["a"], "none": True}}, {key: "x"}):
        with pytest.raises(ValueError):
            P.normalise_picks(bad)


def test_server_stores_picks(server, tmp_path):  # noqa: F811
    srv, base = server
    assert _request(base + "/picks") == (200, {})
    body = {"a|b": {"picked": ["a"], "names": ["A.NEF", "B.NEF"]}}
    assert _request(base + "/picks", json.dumps(body).encode()) == (200, {"saved": 1})
    assert P.load_picks(tmp_path)["a|b"]["picked"] == ["a"]
    with pytest.raises(urllib.error.HTTPError) as err:
        _request(base + "/picks", json.dumps({"a|b": {"picked": ["c"]}}).encode())
    assert err.value.code == 400 and P.load_picks(tmp_path)["a|b"]["picked"] == ["a"]


def test_page_holds_rules_and_data_but_no_program_choice(tmp_path):
    s, ids, groups = shoot_with_groups(tmp_path)
    page = P.write_page(tmp_path, P.build_items(s.photos, groups)).read_text(encoding="utf-8")
    assert "Pravila" in page and "svejedno" in page and sha(s, ids[0]) in page
    assert "http://" not in page and "https://" not in page          # nothing from the internet
    assert "keep" not in page and "rank" not in page.lower().replace("frank", "")


def test_sample_shows_only_the_listed_groups_in_its_order(tmp_path):
    s = Shoot()
    ids = [s.add(k, unit(k % 3)) for k in range(7)]
    groups = groups_of(ids[0:3], ids[3:5], ids[5:6], ids[6:7])
    path = tmp_path / "sample.json"
    path.write_text(json.dumps([{"photo": "DSC_0004.NEF", "kind": "burst"}, {"photo": "dsc_0001.nef"}]), encoding="utf-8")
    items = P.build_items(s.photos, groups, P.load_sample(path))
    assert [it["group_id"] for it in items] == ["g0002", "g0001"] and not any(it.get("ask") for it in items)
    asked = P.build_items(s.photos, groups, [{"photo": "DSC_0004.NEF", "ask": True}])
    assert asked[0]["ask"] is True and "Da je program ostavio" in P.write_page(tmp_path, asked, meeting=True).read_text(encoding="utf-8")
    for bad in (["DSC_0005.NEF"], ["nope.NEF"], ["DSC_0000.NEF", "DSC_0002.NEF"]):   # single, unknown, same group twice
        with pytest.raises(ValueError):
            P.build_items(s.photos, groups, [{"photo": name} for name in bad])
    with pytest.raises(ValueError):                                                  # the question needs two photos
        P.build_items(s.photos, groups, [{"photo": "DSC_0000.NEF", "ask": True}])
    for bad in ("{}", "[]", '[{"photo": 1}]', '[{"photo": "a", "why": "x"}]', '[{"photo": "a", "ask": "yes"}]'):
        path.write_text(bad, encoding="utf-8")
        with pytest.raises(ValueError):
            P.load_sample(path)


def test_reasons_notes_and_the_meeting_page(tmp_path):
    ok = P.normalise_picks({"a|b": {"picked": ["a"], "reasons": ["moment", "eyes"], "note": " baka žmuri "},
                            "c|d": {"none": True, "reasons": ["eyes"], "note": "sve mutne"},
                            "e|f": {"picked": ["e"], "swap_ok": True}, "g|h": {"picked": ["g"], "swap_ok": False, "tossup": True},
                            "i|j": {"none": True, "swap_ok": True}})
    assert (ok["e|f"]["swap_ok"], ok["e|f"]["tossup"]) == (True, True)        # "the other would do" is a toss-up
    assert (ok["g|h"]["swap_ok"], ok["g|h"]["tossup"]) == (False, False) and "swap_ok" not in ok["i|j"]
    assert "1 of 2 said it would" in P.format_reasons(ok)
    assert ok["a|b"]["reasons"] == ["eyes", "moment"] and ok["a|b"]["note"] == "baka žmuri"
    assert "reasons" not in ok["c|d"] and ok["c|d"]["note"] == "sve mutne" and "note" not in ok["e|f"]
    with pytest.raises(ValueError):
        P.normalise_picks({"a|b": {"picked": ["a"], "reasons": ["luck"]}})
    text = P.format_reasons(ok)
    assert "1 of 3 groups with a pick" in text and "eyes 1" in text and "sve mutne" in text
    s, ids, groups = shoot_with_groups(tmp_path)
    items = P.build_items(s.photos, groups)
    assert '<details id="rules">' in P.write_page(tmp_path, items, meeting=True).read_text(encoding="utf-8")
    assert '<details id="rules" open>' in P.write_page(tmp_path, items).read_text(encoding="utf-8")


def test_compare_picks_and_a_separate_picks_file(tmp_path):
    def e(picked, **extra):
        return {"picked": picked, "none": False, "tossup": False, "names": ["A.NEF", "B.NEF"], **extra}
    mine = {"a|b": e(["a"]), "c|d": e(["c", "d"]), "e|f": e(["e"]), "g|h": e(["g"], tossup=True), "i|j": e(["i"])}
    theirs = {"a|b": e(["a"]), "c|d": e(["d"]), "e|f": e(["f"]), "g|h": e(["h"])}
    r = P.compare_picks(theirs, mine)
    assert (r["both"], r["same"], r["overlap"], len(r["different"])) == (3, 1, 1, 1)
    assert "same choice 1" in P.format_comparison(r, "picks.agency.json", "picks.json")
    P.save_picks(tmp_path, theirs, "picks.agency.json")
    assert P.load_picks(tmp_path) == {} and P.load_picks(tmp_path, "picks.agency.json")["c|d"]["picked"] == ["d"]
    from culling.labelserver import make_server
    import threading
    srv = make_server(tmp_path, port=0, picks_file="picks.agency.json")
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        base = f"http://127.0.0.1:{srv.server_address[1]}"
        assert _request(base + "/picks")[1]["a|b"]["picked"] == ["a"]
        _request(base + "/picks", json.dumps({"a|b": {"picked": ["b"], "reasons": ["focus"]}}).encode())
    finally:
        srv.shutdown()
        srv.server_close()
    assert P.load_picks(tmp_path, "picks.agency.json") == {**P.load_picks(tmp_path, "picks.agency.json")}
    assert P.load_picks(tmp_path, "picks.agency.json")["a|b"]["reasons"] == ["focus"] and P.load_picks(tmp_path) == {}


def ranking_of(s, decisions):
    """ranking.json 'photos' from {photo_id: (decision, why)}."""
    return {"photos": {pid: {"decision": d, "why": why, "group_id": "g0001", "rank": 1, "variant": 1}
                       for pid, (d, why) in decisions.items()}}


def test_score_ranking():
    s, ids, groups = shoot_with_groups()
    a, b, c = (sha(s, i) for i in ids[0:3])
    x, y = sha(s, ids[3]), sha(s, ids[4])
    ranking = ranking_of(s, {ids[0]: ("keep", "best_of_variant"), ids[1]: ("maybe", "ranked_lower"),
                             ids[2]: ("keep", "only_frame"), ids[3]: ("keep", "best_of_variant"),
                             ids[4]: ("maybe", "ranked_lower")})
    picks = {P.group_key([a, b, c]): {"picked": [b, c], "none": False, "tossup": False, "names": []},
             P.group_key([x, y]): {"picked": [x], "none": False, "tossup": True, "names": []},
             P.group_key(["unknown", a]): {"picked": [a], "none": False, "tossup": False, "names": []}}
    r = P.score_ranking(picks, s.photos, ranking)
    assert (r["groups"], r["tossup_groups"], r["not_in_ranking"]) == (2, 1, 1)
    assert (r["picked"], r["picked_kept"]) == (3, 2)            # b was picked but is only maybe
    assert r["extra_keeps"] == 1                                 # a kept, not picked
    assert (r["model_variants"], r["model_hits"]) == (1, 0)     # model chose a, the user b and c; toss-up excluded
    assert [m["sha"] for m in r["missed"]] == [b]
    text = P.format_score(r, {b: "DSC_0001.NEF"})
    assert "picked photos kept: 2 of 3" in text and "DSC_0001.NEF" in text


def test_model_items_show_the_models_choice_per_ranked_variant(tmp_path):
    s, ids, groups = shoot_with_groups(tmp_path)
    a, b, c = (sha(s, i) for i in ids[0:3])
    ranking = {"variants": [{"key": "k1", "group_id": "g0001", "index": 1, "kind": "multi", "photo_ids": ids[0:2]},
                            {"key": "k2", "group_id": "g0001", "index": 2, "kind": "single", "photo_ids": ids[2:3]},
                            {"key": "k3", "group_id": "g0002", "index": 1, "kind": "multi", "photo_ids": ids[3:5]}],
               "answers": {"k1": {"order": [ids[1], ids[0]], "reason": "eyes <open>",
                                  "issues": {ids[0]: "eyes_closed", ids[1]: "none"}},
                           "k3": {"order": None, "error": "x"}}}
    reversed_rows = [{"photo_ids": ids[0:2], "winner_reversed": ids[0], "reason_reversed": "first"}]
    items = P.build_model_items(s.photos, ranking, reversed_rows)
    assert len(items) == 1                                     # single and unanswered variants are left out
    it = items[0]
    assert it["key"] == P.group_key([a, b]) and [p["sha"] for p in it["photos"]] == [a, b]
    assert it["model"]["winner"] == b and it["model"]["order"] == [b, a]
    assert it["model"]["issues"] == {a: "eyes_closed", b: "none"}
    assert it["model"]["reversed"] == {"winner": a, "reason": "first"}
    assert P.build_model_items(s.photos, ranking)[0]["model"]["reversed"] is None
    page = P.write_page(tmp_path, items, review=True).read_text(encoding="utf-8")
    assert "Izbor modela" in page and "eyes <open>" not in page.split('id="data"')[0]
    # a pick made with the model on the screen is marked
    kept = P.normalise_picks({it["key"]: {"picked": [b], "seen_model": True}, "x|y": {"picked": ["x"]}})
    assert kept[it["key"]]["seen_model"] is True and "seen_model" not in kept["x|y"]
