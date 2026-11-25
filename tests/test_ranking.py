"""Ranking (best photo per group): variants, the answer parser, the safety rules, the
run loop with resume, and the report captions. Synthetic data only, no network."""
import io
import json

import pytest
from PIL import Image

from culling import ranking as R
from culling.config import DEFAULTS
from culling.report import write_report
from culling.vlm import VLMError, VLMUnavailable
from tests.test_grouping import mix, unit
from tests.test_judge import Shoot, make_output
from tests.test_labels import groups_of

CFG = dict(DEFAULTS["ranking"])
A, B = unit(0), unit(1)


def near(sim):
    """A frame with similarity `sim` to A."""
    return mix(A, B, sim)


def answer(order, issues=None, reason="sharpest, eyes open"):
    issues = issues or ["none"] * len(order)
    return json.dumps({"photos": [{"photo": k + 1, "issue": issue} for k, issue in enumerate(issues)],
                       "order": order, "reason": reason})


class FakeClient:
    """Canned answers: a str is returned by ask(), an exception is raised by it."""

    def __init__(self, replies, model="fake-model"):
        self.replies, self.model, self.base_url = list(replies), model, "http://fake/v1"
        self.last_usage, self.calls, self.pings = {}, [], 0

    def ping(self):
        self.pings += 1
        return [self.model]

    def ask(self, prompt, images, schema, **kwargs):
        self.calls.append({"prompt": prompt, "images": images, "schema": schema, **kwargs})
        if not self.replies:
            raise AssertionError("FakeClient ran out of replies")
        reply = self.replies.pop(0)
        if isinstance(reply, BaseException):
            raise reply
        self.last_usage = {"prompt_tokens": 2000, "completion_tokens": 60}
        return reply


def variants_of(shoot, groups, **overrides):
    return R.build_variants(shoot.photos, groups, shoot.embeddings, shoot.signatures, {**CFG, **overrides})


def ids_by_variant(variants):
    return [v["photo_ids"] for v in variants]


# ------------------------------------------------------------------- variants

def test_near_duplicates_are_one_variant_and_a_new_pose_is_another():
    s = Shoot()
    a, b, c = s.add(0, A), s.add(1, near(0.97)), s.add(9, near(0.80))
    variants = variants_of(s, groups_of([a, b, c]))
    assert ids_by_variant(variants) == [[a, b], [c]]
    assert [v["kind"] for v in variants] == ["multi", "single"]
    assert [v["index"] for v in variants] == [1, 2]
    assert variants[0]["span_seconds"] == 1.0


def test_a_photo_must_match_every_frame_of_the_variant():
    # b is close to a and to c, but a and c are not close: c must not chain on through b.
    s = Shoot()
    a, b, c = s.add(0, A), s.add(1, near(0.95)), s.add(2, near(0.80))
    assert float(s.embeddings[s.photos[1]["sha256"]] @ s.embeddings[s.photos[2]["sha256"]]) > 0.90
    assert ids_by_variant(variants_of(s, groups_of([a, b, c]))) == [[a, b], [c]]


def test_only_frames_of_one_burst_share_a_variant():
    # Pedja P1: 0.95 but 5 s apart is not a burst; both frames stay (decision 0027).
    s = Shoot()
    a, b, c = s.add(0, A), s.add(1, near(0.97)), s.add(6, near(0.97))
    groups = groups_of([a, b, c])
    assert ids_by_variant(variants_of(s, groups)) == [[a, b], [c]]
    assert ids_by_variant(variants_of(s, groups, variant_max_gap_seconds=0)) == [[a, b, c]]


def test_a_burst_is_measured_from_its_last_frame():
    # Nine frames in 4 s (the smoke kiss) are one burst although the first and the last
    # are more than 2 s apart.
    s = Shoot()
    ids = [s.add(1.5 * k, near(0.97)) for k in range(4)]
    assert ids_by_variant(variants_of(s, groups_of(ids))) == [ids]


def test_orientation_splits_only_when_configured():
    s = Shoot()
    a, b = s.add(0, A), s.add(1, near(0.97))
    s.photos[0].update(preview_w=1536, preview_h=1024)
    s.photos[1].update(preview_w=1024, preview_h=1536)
    assert ids_by_variant(variants_of(s, groups_of([a, b]))) == [[a], [b]]
    assert ids_by_variant(variants_of(s, groups_of([a, b]), variant_split_orientation=False)) == [[a, b]]


def test_a_person_added_splits_only_when_configured():
    s = Shoot()
    a, b = s.add(0, A, ids="ABC"), s.add(1, near(0.97), ids="ABCD")
    assert ids_by_variant(variants_of(s, groups_of([a, b]))) == [[a], [b]]
    assert ids_by_variant(variants_of(s, groups_of([a, b]), variant_split_people=False)) == [[a, b]]


def test_unidentified_faces_do_not_split():
    s = Shoot()
    a, b = s.add(0, A, ids="AB"), s.add(1, near(0.97), ids="", n_faces=2)
    assert ids_by_variant(variants_of(s, groups_of([a, b]))) == [[a, b]]


def test_a_long_variant_is_cut_into_parts():
    s = Shoot()
    ids = [s.add(k, near(1 - 0.001 * k)) for k in range(7)]
    variants = variants_of(s, groups_of(ids), max_images=3)
    assert ids_by_variant(variants) == [ids[0:3], ids[3:6], ids[6:7]]
    assert [v["kind"] for v in variants] == ["multi", "multi", "single"]


def test_flagged_and_failed_photos_are_review_variants_and_every_photo_is_placed_once():
    s = Shoot()
    a, b = s.add(0, A), s.add(1, near(0.97))
    failed = s.add(2, None, status="error")
    flagged = s.add(3, near(0.96))
    s.photos[3]["flags"] = ["preview_fallback"]
    variants = variants_of(s, groups_of([a, b, failed, flagged]))
    assert [(v["kind"], v["photo_ids"]) for v in variants] == [
        ("multi", [a, b]), ("review", [failed]), ("review", [flagged])]
    assert sorted(pid for v in variants for pid in v["photo_ids"]) == sorted(p["id"] for p in s.photos)


def test_variant_key_depends_on_the_photos_not_on_the_group():
    s = Shoot()
    a, b, c = s.add(0, A), s.add(1, near(0.97)), s.add(60, B)
    one = variants_of(s, groups_of([a, b], [c]))
    other = variants_of(s, groups_of([c], [a, b]))  # the same photos under other group ids
    assert one[0]["key"] == other[1]["key"] and one[0]["group_id"] != other[1]["group_id"]
    assert one[0]["key"] != one[1]["key"]


# --------------------------------------------------------------------- answers

def test_schema_fixes_the_number_of_photos():
    schema = R.build_schema(3)
    assert schema["properties"]["order"]["minItems"] == schema["properties"]["order"]["maxItems"] == 3
    assert schema["properties"]["order"]["items"]["maximum"] == 3
    assert "confidence" not in schema["properties"]


def test_parse_answer_valid_and_fenced():
    parsed = R.parse_answer(answer([2, 3, 1], ["eyes_closed", "none", "blurred"]), 3)
    assert parsed == {"order": [2, 3, 1], "issues": ["eyes_closed", "none", "blurred"],
                      "reason": "sharpest, eyes open", "repaired": False}
    assert R.parse_answer("```json\n" + answer([1, 2]) + "\n```", 2)["order"] == [1, 2]


def test_parse_answer_repairs_everything_but_the_first_place():
    parsed = R.parse_answer(json.dumps({"photos": [{"photo": 1, "issue": "nonsense"}],
                                        "order": [3, 3, 9], "reason": "x"}), 4)
    assert parsed["order"] == [3, 1, 2, 4] and parsed["repaired"] is True
    assert parsed["issues"] == [None, None, None, None]


@pytest.mark.parametrize("text", [
    "not json", "[1, 2]", json.dumps({"order": [], "reason": "x"}), json.dumps({"order": [5, 1], "reason": "x"}),
    json.dumps({"order": [True, 2], "reason": "x"}), json.dumps({"order": [1, 2]}), None])
def test_parse_answer_rejects_an_unusable_first_place(text):
    with pytest.raises(ValueError):
        R.parse_answer(text, 2)


# ---------------------------------------------------------------- safety rules

def test_decide_applies_the_safety_rules():
    s = Shoot()
    a, b, c = s.add(0, A), s.add(1, near(0.97)), s.add(2, near(0.96))
    lone = s.add(9, near(0.80))
    failed = s.add(10, None, status="error")
    x, y = s.add(60, B), s.add(61, mix(B, A, 0.97))
    variants = variants_of(s, groups_of([a, b, c, lone, failed], [x, y]))
    ranked = {variants[0]["key"]: {"order": [b, c, a], "issues": {a: "eyes_closed", b: "none", c: "blurred"}}}
    d = R.decide(variants, ranked)
    assert (d[b]["decision"], d[b]["rank"], d[b]["why"]) == ("keep", 1, "best_of_variant")
    assert (d[c]["decision"], d[c]["rank"], d[c]["issue"]) == ("maybe", 2, "blurred")
    assert (d[a]["decision"], d[a]["rank"], d[a]["issue"]) == ("maybe", 3, "eyes_closed")
    assert (d[lone]["decision"], d[lone]["why"], d[lone]["variant"]) == ("keep", "only_frame", 2)
    assert (d[failed]["decision"], d[failed]["why"]) == ("maybe", "flagged")
    assert {d[x]["why"], d[y]["why"]} == {"not_ranked"} and d[x]["decision"] == "maybe"
    assert set(d) == {p["id"] for p in s.photos}                      # every photo gets a decision
    assert "reject" not in {v["decision"] for v in d.values()}       # nothing is ever rejected

    errored = {**ranked, variants[-1]["key"]: {"order": None, "error": "VLMError: boom"}}
    assert R.decide(variants, errored)[x]["why"] == "no_valid_answer"
    # An answer about other photos (a stale key collision, a hand-edited file) is not used.
    stale = {variants[0]["key"]: {"order": [a, b, "someone-else"]}}
    assert R.decide(variants, stale)[a]["why"] == "not_ranked"


# -------------------------------------------------------------------- the loop

def two_groups(tmp_path):
    s = Shoot(tmp_path)
    a, b, c = s.add(0, A), s.add(1, near(0.97)), s.add(2, near(0.96))
    x, y = s.add(60, B), s.add(61, mix(B, A, 0.97))
    lone = s.add(120, unit(2))
    config = make_output(tmp_path, s, groups_of([a, b, c], [x, y], [lone]))
    return s, config, (a, b, c, x, y, lone)


def test_numbered_image_is_scaled_not_cropped(tmp_path):
    s = Shoot(tmp_path)
    s.add(0, A, preview=(300, 200))
    with Image.open(io.BytesIO(R.numbered_image(tmp_path, s.photos[0], 2, 150))) as img:
        assert img.size == (150, 100) and img.format == "JPEG"


def test_run_ranks_every_multi_variant_and_resumes(tmp_path, capsys):
    s, config, (a, b, c, x, y, lone) = two_groups(tmp_path)
    client = FakeClient([answer([2, 1, 3], ["blurred", "none", "none"]), answer([1, 2])])
    data = R.run_ranking(tmp_path, config, client_factory=lambda cfg: client)
    assert client.pings == 1 and len(client.calls) == 2
    first = client.calls[0]
    assert len(first["images"]) == 3 and first["schema"] == R.build_schema(3)
    assert "numbered 1 to 3" in first["prompt"] and "within 2 seconds" in first["prompt"]
    decisions = {pid: (d["decision"], d["rank"]) for pid, d in data["photos"].items()}
    assert decisions == {b: ("keep", 1), a: ("maybe", 2), c: ("maybe", 3), x: ("keep", 1), y: ("maybe", 2),
                         lone: ("keep", 1)}
    assert data["photos"][a]["issue"] == "blurred"
    assert data["model"] == "fake-model" and data["prompt_hash"] == R.prompt_hash()
    assert "keep 3, maybe 3 (0 of them not ranked yet)" in capsys.readouterr().out
    assert json.loads((tmp_path / R.RANKING_FILE).read_text(encoding="utf-8"))["photos"] == data["photos"]

    again = FakeClient([])  # everything is answered: a second run sends nothing
    assert R.run_ranking(tmp_path, config, client_factory=lambda cfg: again)["photos"] == data["photos"]
    assert again.calls == []


def test_an_invalid_answer_is_retried_then_left_for_review_and_asked_again_next_run(tmp_path):
    s, config, (a, b, c, x, y, lone) = two_groups(tmp_path)
    config["vlm"]["max_retries"] = 1
    client = FakeClient(["nonsense", VLMError("HTTP 500"), answer([2, 1])])
    data = R.run_ranking(tmp_path, config, client_factory=lambda cfg: client)
    assert {data["photos"][p]["why"] for p in (a, b, c)} == {"no_valid_answer"}
    assert {data["photos"][p]["decision"] for p in (a, b, c)} == {"maybe"}
    assert data["photos"][y]["decision"] == "keep"

    retry = FakeClient([answer([3, 1, 2])])
    data = R.run_ranking(tmp_path, config, client_factory=lambda cfg: retry)
    assert len(retry.calls) == 1 and data["photos"][c]["decision"] == "keep"


def test_a_lost_server_keeps_the_progress(tmp_path):
    s, config, (a, b, c, x, y, lone) = two_groups(tmp_path)
    client = FakeClient([answer([1, 2, 3]), VLMUnavailable("tunnel closed")])
    with pytest.raises(VLMUnavailable):
        R.run_ranking(tmp_path, config, client_factory=lambda cfg: client)
    saved = R.load_ranking(tmp_path)
    assert saved["photos"][a]["decision"] == "keep" and saved["photos"][x]["why"] == "not_ranked"

    rest = FakeClient([answer([2, 1])])
    data = R.run_ranking(tmp_path, config, client_factory=lambda cfg: rest)
    assert len(rest.calls) == 1 and data["photos"][y]["decision"] == "keep"


def test_dry_run_and_max_requests(tmp_path, capsys):
    s, config, (a, b, c, x, y, lone) = two_groups(tmp_path)

    def no_client(cfg):
        raise AssertionError("a dry-run must not create a client")

    data = R.run_ranking(tmp_path, config, dry_run=True, client_factory=no_client)
    out = capsys.readouterr().out
    assert "would send: 2 requests" in out and "no request was sent" in out
    assert "after a full run: keep 3 of 6" in out
    assert data["photos"][lone]["decision"] == "keep" and data["photos"][a]["why"] == "not_ranked"

    client = FakeClient([answer([1, 2, 3])])
    data = R.run_ranking(tmp_path, config, max_requests=1, client_factory=lambda cfg: client)
    assert len(client.calls) == 1 and data["photos"][x]["why"] == "not_ranked"


def test_answers_of_another_model_or_prompt_are_not_mixed(tmp_path, monkeypatch):
    s, config, _ = two_groups(tmp_path)
    R.run_ranking(tmp_path, config, client_factory=lambda cfg: FakeClient([answer([1, 2, 3]), answer([1, 2])]))
    with pytest.raises(SystemExit, match="holds answers of fake-model"):
        R.run_ranking(tmp_path, config, client_factory=lambda cfg: FakeClient([], model="other"))
    monkeypatch.setattr(R, "PROMPT", R.PROMPT + " changed")
    with pytest.raises(SystemExit, match="another prompt"):
        R.run_ranking(tmp_path, config, client_factory=lambda cfg: FakeClient([]))


def test_nothing_of_the_images_or_the_prompt_is_logged(tmp_path, caplog):
    s, config, _ = two_groups(tmp_path)
    with caplog.at_level("DEBUG"):
        R.run_ranking(tmp_path, config, client_factory=lambda cfg: FakeClient([answer([1, 2, 3]), answer([1, 2])]))
    assert "wedding photos" not in caplog.text and "base64" not in caplog.text


# ---------------------------------------------------------------------- report

def test_report_shows_the_decisions_only_for_the_current_grouping(tmp_path):
    s, config, (a, b, c, x, y, lone) = two_groups(tmp_path)
    groups = json.loads((tmp_path / "groups.json").read_text(encoding="utf-8"))
    groups.update(created="2026-11-11T10:00:00", config_used={})
    for g in groups["groups"]:
        g.update(camera_id="SN1", size=len(g["photo_ids"]), flags=[], min_similarity=None, split_part=None, start=None, end=None)
    (tmp_path / "groups.json").write_text(json.dumps(groups), encoding="utf-8")
    R.run_ranking(tmp_path, config, client_factory=lambda cfg: FakeClient(
        [answer([2, 1, 3], ["eyes_closed", "none", "none"]), answer([1, 2])]))

    ranking = R.ranking_for_report(tmp_path, groups)
    page = write_report(tmp_path, s.photos, groups, ranking=ranking).read_text(encoding="utf-8")
    assert page.count('<figure class="keep"') == 3 and page.count('<figure class="maybe"') == 3
    assert "maybe #2 · v1 · eyes_closed" in page and "keep 1 of 3" in page

    assert R.ranking_for_report(tmp_path, {**groups, "created": "2026-11-12T09:00:00"}) is None
    plain = write_report(tmp_path, s.photos, groups).read_text(encoding="utf-8")
    assert '<figure class="keep"' not in plain and "keep 1 of 3" not in plain
