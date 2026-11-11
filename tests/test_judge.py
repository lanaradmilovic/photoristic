"""VLM judge: pair selection, pair images, dry-run, verdicts, resume, the labels
comparison and the client. Synthetic data only, no network."""
import base64
import hashlib
import io
import json
import logging
import re
import socket
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from culling import judge as J
from culling.config import DEFAULTS, load_config
from culling.embed import save_cache as save_embeddings
from culling.ingest import save_photos
from culling.labels import save_labels
from culling.people import save_cache as save_people
from culling.vlm import OpenAICompatibleClient, VLMError, VLMUnavailable, make_client
from tests.test_grouping import DIM, mix, unit
from tests.test_labels import groups_of

T0 = datetime(2024, 6, 15, 16, 0, 0)
JUDGE = dict(DEFAULTS["judge"])
GROUPING = dict(DEFAULTS["grouping"])
VLM = dict(DEFAULTS["vlm"])
GOOD = '{"same_people": "yes", "interchangeable": "yes", "verdict": "same_group", "confidence": 0.9, "reason": "same pose"}'
DIFFERENT = '{"same_people": "no", "interchangeable": "no", "verdict": "different_group", "confidence": 0.8, "reason": "other guest"}'
UNSURE = '{"same_people": "unsure", "interchangeable": "unsure", "verdict": "unsure", "confidence": 0.3, "reason": "backs"}'


# ------------------------------------------------------------------ helpers

class Shoot:
    """Synthetic photos with embeddings, people flags, face signatures and, when an
    output folder is given, small previews and thumbs on disk."""

    def __init__(self, out_dir=None):
        self.out_dir = out_dir
        self.photos, self.embeddings, self.people, self.signatures = [], {}, {}, {}
        if out_dir:
            (out_dir / "previews").mkdir(exist_ok=True)
            (out_dir / "thumbs").mkdir(exist_ok=True)

    def add(self, seconds, vec, camera="SN1", people=None, ids=None, n_faces=None, status="ok",
            time=True, name=None, preview=(90, 60)):
        n = len(self.photos)
        sha = hashlib.sha256(f"judge{n}".encode()).hexdigest()
        name = name or f"DSC_{n:04d}.NEF"
        photo = {"id": sha[:16], "sha256": sha, "primary_path": f"C:/w/{name}", "nef_path": f"C:/w/{name}",
                 "jpg_path": None, "thumb_file": f"thumbs/{sha[:16]}.jpg", "preview_file": f"previews/{sha[:16]}.jpg",
                 "capture_time": (T0 + timedelta(seconds=seconds)).isoformat() if time else None,
                 "camera_id": camera, "status": status, "flags": []}
        self.photos.append(photo)
        if status == "ok" and vec is not None:
            self.embeddings[sha] = vec
        if people is not None:
            self.people[sha] = people
        if ids is not None:
            self.signatures[sha] = (frozenset(ids), len(ids) if n_faces is None else n_faces)
        if self.out_dir and preview:
            colour = ((n * 70) % 256, (n * 130) % 256, (n * 190) % 256)
            Image.new("RGB", preview, colour).save(self.out_dir / photo["preview_file"])
            Image.new("RGB", (preview[0] // 2, preview[1] // 2), colour).save(self.out_dir / photo["thumb_file"])
        return photo["id"]

    def select(self, groups, include_faces_decided=False, max_pairs=0, grouping=None, **overrides):
        cfg = {**JUDGE, **overrides}
        return J.select_pairs(self.photos, self.embeddings, groups, cfg, {**GROUPING, **(grouping or {})},
                              self.people, self.signatures, include_faces_decided, max_pairs)

    def by_id(self):
        return {p["id"]: p for p in self.photos}


def summary(pairs):
    return [(p["a_id"], p["b_id"], p["kind"], p["similarity"], p["pipeline_same_group"]) for p in pairs]


def make_output(tmp_path, shoot, groups):
    """A minimal output folder (photos.json, groups.json, embeddings.npz, people.json)
    and a config with faces off; the judge reads nothing else."""
    save_photos(tmp_path, shoot.photos, "C:/w")
    (tmp_path / "groups.json").write_text(json.dumps(groups), encoding="utf-8")
    save_embeddings(tmp_path, DEFAULTS["embedding"]["model_name"], shoot.embeddings)
    save_people(tmp_path, DEFAULTS["people"]["model_name"], shoot.people)
    config = load_config()
    config["faces"]["enabled"] = False
    return config


class FakeClient:
    """Canned answers: a str is returned by ask(), an exception is raised by it."""

    def __init__(self, replies, model="fake-model", ping_error=None):
        self.replies, self.model, self.ping_error = list(replies), model, ping_error
        self.base_url, self.last_usage, self.prompts, self.images, self.pings = "http://fake/v1", {}, [], [], 0

    def ping(self):
        self.pings += 1
        if self.ping_error:
            raise self.ping_error
        return [self.model]

    def ask(self, prompt, images, schema, **kwargs):
        self.prompts.append(prompt)
        self.images.append(images)
        assert schema is J.VERDICT_SCHEMA
        if not self.replies:
            raise AssertionError("FakeClient ran out of replies")
        reply = self.replies.pop(0)
        if isinstance(reply, BaseException):
            raise reply
        self.last_usage = {"prompt_tokens": 1000 + len(self.prompts), "completion_tokens": 30}
        return reply


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def read(self):
        return self.payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def fake_urlopen(responses):
    """urlopen stand-in: records (request, timeout) and answers from `responses`
    (a dict is sent as JSON, bytes as they are, an exception is raised)."""
    calls = []

    def opener(request, timeout=None):
        calls.append((request, timeout))
        reply = responses.pop(0)
        if isinstance(reply, BaseException):
            raise reply
        return FakeResponse(json.dumps(reply).encode("utf-8") if isinstance(reply, dict) else reply)

    opener.calls = calls
    return opener


def http_error(code, body=b""):
    return urllib.error.HTTPError("http://localhost:8000/v1/x", code, "error", {}, io.BytesIO(body))


def client_with(responses, cfg=None):
    return OpenAICompatibleClient(cfg or VLM, opener=fake_urlopen(responses))


# ------------------------------------------------------------ pair selection

def test_neighbour_pairs_in_band_joined_and_split():
    s = Shoot()
    a = s.add(0, unit(0))
    b = s.add(10, mix(unit(0), unit(1), 0.85))
    c = s.add(20, mix(s.embeddings[s.photos[1]["sha256"]], unit(2), 0.83))
    pairs, stats = s.select(groups_of([a, b], [c]))
    assert summary(pairs) == [(a, b, "neighbour", 0.85, True), (b, c, "neighbour", 0.83, False)]
    assert pairs[0]["gap_seconds"] == 10.0 and pairs[0]["a_name"] == "DSC_0000.NEF" and pairs[0]["b_name"] == "DSC_0001.NEF"
    assert pairs[0]["faces_relation"] is None and pairs[0]["image"] is None and pairs[0]["camera_id"] == "SN1"
    assert stats["neighbour_in_band"] == 2 and stats["lookback_in_band"] == 0 and stats["selected"] == 2
    assert stats["photos"] == 3 and stats["cameras"] == 1


def test_band_is_half_open():
    s = Shoot()
    a = s.add(0, unit(0))
    b = s.add(5, mix(unit(0), unit(1), 0.80))   # exactly sim_low: in
    c = s.add(10, mix(unit(0), unit(2), 0.90))  # exactly sim_high to a: out, and not joined
    pairs, stats = s.select(groups_of([a], [b], [c]))
    assert summary(pairs) == [(a, b, "neighbour", 0.8, False)]
    assert stats["above_band_not_joined"] == 1


def test_lookback_pair_to_the_best_earlier_group_not_joined():
    s = Shoot()
    a1 = s.add(0, unit(0))
    other = s.add(10, unit(1))
    a2 = s.add(30, mix(unit(0), unit(3), 0.87))
    pairs, stats = s.select(groups_of([a1], [other], [a2]))
    assert summary(pairs) == [(a1, a2, "lookback", 0.87, False)]
    assert pairs[0]["gap_seconds"] == 30.0 and stats["lookback_in_band"] == 1


def test_lookback_window_counts_from_the_latest_earlier_member():
    s = Shoot()
    a1 = s.add(0, unit(0))
    a2 = s.add(50, unit(4))
    other = s.add(60, unit(1))
    b = s.add(170, mix(unit(0), unit(3), 0.85))  # a2 is exactly 120 s old: the group qualifies
    pairs, _ = s.select(groups_of([a1, a2], [other], [b]))
    assert summary(pairs) == [(a1, b, "lookback", 0.85, False)]  # best member, even though 170 s old
    s.photos[-1]["capture_time"] = (T0 + timedelta(seconds=171)).isoformat()
    pairs, stats = s.select(groups_of([a1, a2], [other], [b]))
    assert pairs == [] and stats["lookback_in_band"] == 0


def test_lookback_uses_only_photos_before_b_and_flags_lookback_joins():
    # A = [a1, a3] where a3 came back by look-back. b (between them in time) may only be
    # compared with a1; a3's join to its own group at 0.81 is a possible false merge.
    s = Shoot()
    a1 = s.add(0, unit(0))
    other = s.add(5, unit(1))
    b = s.add(10, mix(unit(0), unit(2), 0.85))
    a3 = s.add(20, mix(s.embeddings[s.photos[2]["sha256"]], unit(4), 0.95))  # 0.95 to b, 0.8075 to a1
    pairs, stats = s.select(groups_of([a1, a3], [other], [b]))
    assert summary(pairs) == [(a1, b, "lookback", 0.85, False), (a1, a3, "lookback", 0.8075, True)]
    assert stats["above_band_not_joined"] == 1  # a3 vs b at 0.95, kept apart by groups.json


def test_lookback_join_above_band_is_not_a_pair():
    s = Shoot()
    a1 = s.add(0, unit(0))
    other = s.add(10, unit(1))
    a2 = s.add(30, mix(unit(0), unit(2), 0.95))
    pairs, stats = s.select(groups_of([a1, a2], [other]))
    assert pairs == [] and stats["above_band_not_joined"] == 0


def test_single_best_group_wins_the_lookback():
    s = Shoot()
    a = s.add(0, unit(0))
    c = s.add(10, (0.6 * unit(0) + 0.8 * unit(1)).astype(np.float32))
    other = s.add(20, unit(3))
    vec = np.zeros(DIM, np.float32)
    vec[0], vec[1] = 0.85, 0.4625                          # 0.85 to a, 0.88 to c
    vec[2] = np.sqrt(1 - vec[0] ** 2 - vec[1] ** 2)
    b = s.add(30, vec)
    pairs, _ = s.select(groups_of([a], [c], [other], [b]))
    assert summary(pairs) == [(c, b, "lookback", 0.88, False)]


def test_lookback_never_duplicates_a_neighbour_pair():
    s = Shoot()
    a = s.add(0, unit(0))
    b = s.add(10, mix(unit(0), unit(1), 0.85))
    pairs, stats = s.select(groups_of([a], [b]))
    assert summary(pairs) == [(a, b, "neighbour", 0.85, False)]
    assert stats["neighbour_in_band"] == 1 and stats["lookback_in_band"] == 0


def test_above_band_not_joined_is_counted_without_a_pair():
    s = Shoot()
    a1 = s.add(0, unit(0))
    other = s.add(10, unit(1))
    a2 = s.add(30, mix(unit(0), unit(2), 0.95))
    pairs, stats = s.select(groups_of([a1], [other], [a2]))
    assert pairs == [] and stats["above_band_not_joined"] == 1


def test_cameras_never_cross():
    s = Shoot()
    a = s.add(0, unit(0), camera="SN1")
    b = s.add(5, mix(unit(0), unit(1), 0.85), camera="SN2")
    pairs, stats = s.select(groups_of([a], [b]))
    assert pairs == [] and stats["cameras"] == 2


def test_faces_decided_pairs_are_excluded_unless_asked():
    s = Shoot()
    p0 = s.add(0, unit(0), ids=["A", "B"])
    p1 = s.add(10, mix(unit(0), unit(1), 0.85), ids=["A", "B"])                              # same
    p2 = s.add(20, mix(s.embeddings[s.photos[1]["sha256"]], unit(2), 0.85), ids=["C"])      # different
    p3 = s.add(30, mix(s.embeddings[s.photos[2]["sha256"]], unit(3), 0.85), ids=["C", "D"])  # partial overlap
    groups = groups_of([p0], [p1], [p2], [p3])
    pairs, stats = s.select(groups)
    assert [(p["a_id"], p["faces_relation"]) for p in pairs] == [(p2, None)]
    assert stats["excluded_faces_same"] == 1 and stats["excluded_faces_different"] == 1
    pairs, stats = s.select(groups, include_faces_decided=True)
    assert [(p["a_id"], p["faces_relation"]) for p in pairs] == [(p0, "same"), (p1, "different"), (p2, None)]
    assert stats["excluded_faces_same"] == 0 and stats["excluded_faces_different"] == 0
    # With faces_partial_overlap_blocks a partial overlap ({C} vs {C, D}) is "different" too.
    pairs, stats = s.select(groups, grouping={"faces_partial_overlap_blocks": True})
    assert pairs == [] and stats["excluded_faces_different"] == 2


def test_no_people_on_both_sides_is_excluded():
    s = Shoot()
    p0 = s.add(0, unit(0), people=False)
    p1 = s.add(10, mix(unit(0), unit(1), 0.85), people=False)
    p2 = s.add(20, mix(s.embeddings[s.photos[1]["sha256"]], unit(2), 0.85), people=True)
    p3 = s.add(30, mix(s.embeddings[s.photos[2]["sha256"]], unit(3), 0.85))   # no entry = has people
    p4 = s.add(40, mix(s.embeddings[s.photos[3]["sha256"]], unit(4), 0.85), people=False)
    pairs, stats = s.select(groups_of([p0], [p1], [p2], [p3], [p4]))
    assert [p["a_id"] for p in pairs] == [p1, p2, p3]
    assert stats["excluded_no_people"] == 1


def test_max_pairs_cuts_the_time_ordered_list_deterministically():
    s = Shoot()
    ids = [s.add(0, unit(0))]
    for k in range(1, 5):
        ids.append(s.add(10 * k, mix(s.embeddings[s.photos[-1]["sha256"]], unit(k), 0.85)))
    groups = groups_of(*[[i] for i in ids])
    full, _ = s.select(groups)
    assert len(full) == 4
    cut, stats = s.select(groups, max_pairs=2)
    assert summary(cut) == summary(full)[:2] and stats["cut_by_max_pairs"] == 2 and stats["selected"] == 2
    assert summary(s.select(groups, max_pairs=2)[0]) == summary(cut)


def test_unusable_photos_are_skipped_and_do_not_break_adjacency():
    s = Shoot()
    a = s.add(0, unit(0))
    bad = s.add(2, unit(0), status="error")
    no_time = s.add(4, unit(0), time=False)
    no_emb = s.add(6, None)
    b = s.add(10, mix(unit(0), unit(1), 0.85))
    stranger = s.add(12, unit(0))  # not in groups.json
    pairs, stats = s.select(groups_of([a], [bad], [no_time], [no_emb], [b]))
    assert summary(pairs) == [(a, b, "neighbour", 0.85, False)]
    assert stats["skipped_photos"] == 4 and stats["photos"] == 2


# ------------------------------------------------------------------- images

def test_pair_image_layout_and_corner_labels(tmp_path):
    s = Shoot(tmp_path)
    a = s.add(0, unit(0), preview=None)
    b = s.add(1, unit(0), preview=None)
    Image.new("RGB", (90, 60), "red").save(tmp_path / s.photos[0]["preview_file"], format="PNG")  # lossless
    Image.new("RGB", (60, 90), "blue").save(tmp_path / s.photos[1]["preview_file"], format="PNG")
    img = J.pair_image(tmp_path, s.photos[0], s.photos[1], 60)
    assert img.size == (60 + J.GUTTER + 40, 60)
    assert img.getpixel((50, 35)) == (255, 0, 0)                  # left frame 60x40
    assert img.getpixel((30, 50)) == (128, 128, 128)              # below it: canvas (top-aligned frames)
    assert img.getpixel((60 + J.GUTTER // 2, 30)) == (128, 128, 128)
    assert img.getpixel((60 + J.GUTTER + 20, 80 - 25)) == (0, 0, 255)  # right frame 40x60
    for x0 in (0, 60 + J.GUTTER):
        assert img.getpixel((x0 + 9, 9)) == (0, 0, 0)             # black label box
        box = img.crop((x0 + 8, 8, x0 + 30, 30))
        assert np.asarray(box).sum(axis=2).max() > 600  # the (anti-aliased) white digit


def test_pair_image_grey_tile_when_preview_missing(tmp_path):
    s = Shoot(tmp_path)
    a = s.add(0, unit(0), preview=None)
    b = s.add(1, unit(0), preview=(60, 90))
    img = J.pair_image(tmp_path, s.photos[0], s.photos[1], 60)
    assert img.size == (60 + J.GUTTER + 40, 60) and img.getpixel((50, 30)) == (200, 200, 200)
    assert J.pair_image(tmp_path, None, None, 60).size == (60 + J.GUTTER + 60, 40)


def test_write_pair_images_names_and_sizes(tmp_path):
    s = Shoot(tmp_path)
    a = s.add(0, unit(0), name="_KAD8026.NEF", preview=(1536, 1024))
    b = s.add(5, unit(0), name="_KAD8030.NEF", preview=(1024, 1536))
    c = s.add(10, unit(0), name="_KAD8030.NEF", preview=(1536, 1024))  # same stem as b
    pairs = [{"a_id": a, "b_id": b}, {"a_id": a, "b_id": c}]
    (tmp_path / "judge_pairs").mkdir()
    (tmp_path / "judge_pairs" / "stale.jpg").write_bytes(b"x")
    J.write_pair_images(tmp_path, s.by_id(), pairs, 768)
    assert pairs[0]["image"] == "judge_pairs/_KAD8026__KAD8030.jpg" and pairs[0]["image_size"] == [768 + J.GUTTER + 512, 768]
    assert pairs[1]["image"] == f"judge_pairs/_KAD8026__KAD8030_{a}_{c}.jpg" and pairs[1]["image_size"] == [1560, 512]
    assert sorted(p.name for p in (tmp_path / "judge_pairs").iterdir()) == sorted(Path(p["image"]).name for p in pairs)
    with Image.open(tmp_path / pairs[1]["image"]) as img:
        assert img.format == "JPEG" and img.size == (1560, 512)


def test_estimate_tokens():
    assert J.estimate_tokens((1560, 512)) == 49 * 16 + J.TEXT_TOKENS == 1114
    assert J.estimate_tokens((768 + 24 + 512, 768)) == 41 * 24 + J.TEXT_TOKENS


def test_pairs_sheet_is_split_and_stale_sheets_removed(tmp_path, monkeypatch):
    s = Shoot(tmp_path)
    ids = [s.add(k, unit(0)) for k in range(11)]
    pairs = [{"a_id": ids[k], "b_id": ids[k + 1], "a_name": f"a{k}", "b_name": f"b{k}", "kind": "neighbour",
              "similarity": 0.85, "gap_seconds": 1.0, "pipeline_same_group": k % 2 == 0, "faces_relation": None}
             for k in range(10)]
    (tmp_path / "judge_pairs_03.jpg").write_bytes(b"x")
    monkeypatch.setattr(J, "SHEET_MAX_HEIGHT", 24 + 2 * (J.SHEET_THUMB + 36))  # two rows per sheet
    paths = J.write_pairs_sheet(tmp_path, pairs, s.by_id())
    assert [p.name for p in paths] == ["judge_pairs.jpg", "judge_pairs_02.jpg"]
    assert not (tmp_path / "judge_pairs_03.jpg").exists()
    with Image.open(paths[0]) as img:
        assert img.size == (4 * (2 * J.SHEET_THUMB + 40), 24 + 2 * (J.SHEET_THUMB + 36))
    assert J.write_pairs_sheet(tmp_path, [], s.by_id()) == [] and not (tmp_path / "judge_pairs.jpg").exists()


# ------------------------------------------------------------------ dry-run

def test_dry_run_writes_files_and_never_creates_a_client(tmp_path, capsys):
    s = Shoot(tmp_path)
    a = s.add(0, unit(0))
    b = s.add(10, mix(unit(0), unit(1), 0.85))
    other = s.add(20, unit(2))
    a3 = s.add(40, mix(unit(0), unit(3), 0.86))
    config = make_output(tmp_path, s, groups_of([a, b], [other], [a3]))

    def no_client(cfg):
        raise AssertionError("client created in a dry-run")

    result = J.run_judge(tmp_path, config, dry_run=True, client_factory=no_client)
    assert [p["kind"] for p in result["pairs"]] == ["neighbour", "lookback"]
    data = json.loads((tmp_path / "judge_pairs.json").read_text("utf-8"))
    assert set(data) >= {"created", "sim_low", "sim_high", "lookback_seconds", "stats", "pairs"}
    assert data["sim_low"] == 0.8 and data["sim_high"] == 0.9 and data["lookback_seconds"] == GROUPING["lookback_seconds"]
    assert data["stats"]["selected"] == 2 and [p["image"] for p in data["pairs"]] == \
        ["judge_pairs/DSC_0000_DSC_0001.jpg", "judge_pairs/DSC_0000_DSC_0003.jpg"]
    assert data["pairs"][0]["image_size"] == [90 + J.GUTTER + 90, 60]
    assert (tmp_path / "judge_pairs.jpg").exists() and len(list((tmp_path / "judge_pairs").glob("*.jpg"))) == 2
    assert not (tmp_path / "judge_verdicts.json").exists()
    out = capsys.readouterr().out
    assert "VLM judge dry-run: 2 pairs selected" in out and "neighbour      1   pipeline joined 1, split 0" in out
    assert "lookback       1   pipeline joined 0, split 1" in out and "no request was sent" in out
    assert re.search(r"faces decided same +0 ", out) and re.search(r"above band, not joined +0 ", out)
    tokens = J.estimate_tokens((90 + J.GUTTER + 90, 60))
    assert f"min {tokens}  median {tokens}  max {tokens}  total {2 * tokens}" in out
    assert "2 x 4.0 s = 0.1 min" in out


def test_run_judge_exits_clearly_without_grouping_outputs(tmp_path):
    config = load_config()
    with pytest.raises(SystemExit, match="photos.json"):
        J.run_judge(tmp_path, config, dry_run=True)
    s = Shoot(tmp_path)
    s.add(0, unit(0))
    save_photos(tmp_path, s.photos, "C:/w")
    with pytest.raises(SystemExit, match="groups.json"):
        J.run_judge(tmp_path, config, dry_run=True)
    (tmp_path / "groups.json").write_text(json.dumps(groups_of([s.photos[0]["id"]])), encoding="utf-8")
    with pytest.raises(SystemExit, match="embeddings"):
        J.run_judge(tmp_path, config, dry_run=True)


# ----------------------------------------------------------------- verdicts

def test_parse_verdict():
    v = J.parse_verdict(GOOD)
    assert v == {"same_people": "yes", "interchangeable": "yes", "verdict": "same_group", "confidence": 0.9,
                 "reason": "same pose"}
    assert J.parse_verdict("```json\n" + GOOD + "\n```")["verdict"] == "same_group"
    assert J.parse_verdict('{"same_people": "no", "interchangeable": "no", "verdict": "different_group", '
                           '"confidence": 1, "reason": "x", "extra": 1}')["confidence"] == 1.0
    for bad in ("not json", "[]", GOOD.replace("same_group", "maybe"), GOOD.replace("0.9", "1.5"),
                GOOD.replace("0.9", '"high"'), GOOD.replace("0.9", "true"), GOOD.replace('"same pose"', "3"),
                '{"same_people": "yes"}', None):
        with pytest.raises(ValueError):
            J.parse_verdict(bad)


def pair_record(a="a", b="b", gap=12.3, sim=0.853, kind="neighbour", joined=False):
    return {"a_id": a, "b_id": b, "a_name": f"{a}.NEF", "b_name": f"{b}.NEF", "kind": kind, "similarity": sim,
            "gap_seconds": gap, "pipeline_same_group": joined, "faces_relation": None,
            "image": "judge_pairs/x.jpg", "image_size": [1560, 512]}


def test_judge_pair_retries_bad_json_then_succeeds():
    client = FakeClient(["oops", GOOD])
    verdict = J.judge_pair(client, pair_record(), b"jpeg", max_retries=3)
    assert verdict["verdict"] == "same_group" and verdict["attempts"] == 2 and verdict["prompt_tokens"] == 1002
    assert verdict["a_id"] == "a" and verdict["kind"] == "neighbour" and verdict["judged_at"]
    assert client.images == [[b"jpeg"], [b"jpeg"]]
    prompt = client.prompts[0]
    assert "12.3 seconds apart" in prompt
    assert "0.85" not in prompt and "pipeline" not in prompt.lower() and "joined" not in prompt.lower()
    assert "split" not in prompt.lower() and "similar" not in prompt.lower()


def test_judge_pair_gives_up_after_max_retries():
    client = FakeClient([VLMError("HTTP 500"), "bad", "bad", "bad"])
    verdict = J.judge_pair(client, pair_record(), b"jpeg", max_retries=3)
    assert verdict["verdict"] == "error" and verdict["attempts"] == 4 and verdict["prompt_tokens"] is None
    assert verdict["reason"].startswith("ValueError") and verdict["confidence"] == 0.0
    assert J.judge_pair(FakeClient([VLMError("HTTP 500"), GOOD]), pair_record(), b"jpeg", 1)["attempts"] == 2
    with pytest.raises(VLMUnavailable):
        J.judge_pair(FakeClient([VLMUnavailable("gone")]), pair_record(), b"jpeg", 3)


def _three_pairs(tmp_path):
    s = Shoot(tmp_path)
    ids = [s.add(0, unit(0))]
    for k in range(1, 4):
        ids.append(s.add(10 * k, mix(s.embeddings[s.photos[-1]["sha256"]], unit(k), 0.85)))
    config = make_output(tmp_path, s, groups_of([ids[0], ids[1]], [ids[2]], [ids[3]]))
    return s, ids, config


def test_run_judge_saves_after_every_pair_and_resumes(tmp_path, caplog):
    s, ids, config = _three_pairs(tmp_path)
    first = FakeClient([GOOD, VLMUnavailable("tunnel closed")])
    with pytest.raises(VLMUnavailable):
        J.run_judge(tmp_path, config, client_factory=lambda cfg: first)
    data = json.loads((tmp_path / "judge_verdicts.json").read_text("utf-8"))
    assert list(data["verdicts"]) == [f"{ids[0]}|{ids[1]}"] and data["model"] == "fake-model"
    assert data["sim_low"] == 0.8 and data["created"] and data["updated"] and data["labels"] is None
    assert first.pings == 2 and len(first.prompts) == 2

    second = FakeClient([DIFFERENT, UNSURE])
    result = J.run_judge(tmp_path, config, client_factory=lambda cfg: second)
    assert len(second.prompts) == 2
    verdicts = result["verdicts"]["verdicts"]
    assert [verdicts[f"{a}|{b}"]["verdict"] for a, b in zip(ids, ids[1:])] == ["same_group", "different_group", "unsure"]
    assert json.loads((tmp_path / "judge_verdicts.json").read_text("utf-8"))["verdicts"] == verdicts

    # Nothing left: no request. A planted error entry is asked again.
    third = FakeClient([])
    J.run_judge(tmp_path, config, client_factory=lambda cfg: third)
    assert third.prompts == [] and third.pings == 2
    data = json.loads((tmp_path / "judge_verdicts.json").read_text("utf-8"))
    data["verdicts"][f"{ids[2]}|{ids[3]}"]["verdict"] = "error"
    (tmp_path / "judge_verdicts.json").write_text(json.dumps(data), encoding="utf-8")
    fourth = FakeClient([GOOD])
    J.run_judge(tmp_path, config, client_factory=lambda cfg: fourth)
    assert len(fourth.prompts) == 1
    data = json.loads((tmp_path / "judge_verdicts.json").read_text("utf-8"))
    assert data["verdicts"][f"{ids[2]}|{ids[3]}"]["verdict"] == "same_group"
    assert not (tmp_path / "judge_verdicts.tmp").exists()


def test_ping_failure_happens_before_any_request(tmp_path):
    s, ids, config = _three_pairs(tmp_path)
    client = FakeClient([GOOD], ping_error=VLMError("serves [], not fake-model"))
    with pytest.raises(VLMError, match="not fake-model"):
        J.run_judge(tmp_path, config, client_factory=lambda cfg: client)
    assert client.prompts == [] and not (tmp_path / "judge_verdicts.json").exists()
    assert not (tmp_path / "judge_pairs.json").exists()  # the ping comes before any work
    with pytest.raises(VLMError):
        J.run_judging(tmp_path, [pair_record()], client, VLM)
    assert client.prompts == []


def test_verdicts_of_another_model_are_not_mixed(tmp_path):
    s, ids, config = _three_pairs(tmp_path)
    J.run_judge(tmp_path, config, client_factory=lambda cfg: FakeClient([GOOD, GOOD, GOOD]))
    with pytest.raises(SystemExit, match="fake-model"):
        J.run_judge(tmp_path, config, client_factory=lambda cfg: FakeClient([GOOD], model="other-model"))


# ------------------------------------------------------------------- labels

def test_compare_with_labels_counts_and_text():
    s = Shoot()
    ids = [s.add(k, unit(0)) for k in range(10)]
    photos = s.photos
    sha = {p["id"]: p["sha256"] for p in photos}

    def pair(k, joined, kind="neighbour"):
        return pair_record(ids[k], ids[k + 1], gap=1.0, sim=0.85, kind=kind, joined=joined)

    pairs = [pair(0, True), pair(1, False), pair(2, False), pair(3, True), pair(4, True), pair(5, False),
             pair(6, False), pair(7, True), pair(8, False, kind="lookback"), pair(8, False)]

    def verdict(k, value):
        return (f"{ids[k]}|{ids[k + 1]}", {"verdict": value, "confidence": 0.7, "reason": f"r{k}"})

    verdicts = dict([verdict(0, "same_group"), verdict(1, "same_group"), verdict(2, "different_group"),
                     verdict(3, "unsure"), verdict(4, "different_group"), verdict(5, "same_group"),
                     verdict(6, "same_group"), verdict(8, "error")])
    labels = [{"a_sha": sha[ids[k]], "b_sha": sha[ids[k + 1]], "label": value}
              for k, value in [(0, "same"), (1, "different"), (2, "same"), (3, "same"), (4, "different"),
                               (5, "unsure"), (7, "same"), (8, "different")]]
    labels.append({"a_sha": sha[ids[0]], "b_sha": sha[ids[9]], "label": "different"})  # not a selected pair
    r = J.compare_with_labels(pairs, verdicts, labels, photos)
    assert (r["n_neighbour_pairs"], r["n_labelled"], r["n_unsure_labels"], r["n_unjudged"]) == (9, 7, 1, 1)
    assert (r["n_labels"], r["n_labels_matched"]) == (9, 8)
    j, p = r["judge"], r["pipeline"]
    assert (j["correct"], j["wrong"], j["abstained"], j["abstained_same"]) == (2, 2, 2, 1)
    assert (j["tp"], j["fp"], j["fn"], j["fixes"], j["breaks"]) == (1, 1, 1, 1, 1)
    assert j["precision"] == 0.5 and j["recall"] == 0.5 and j["recall_strict"] == pytest.approx(1 / 3, abs=1e-4)
    assert (p["correct"], p["wrong"], p["tp"], p["fp"], p["fn"]) == (4, 2, 2, 1, 1)
    assert p["precision"] == pytest.approx(2 / 3, abs=1e-4) and p["recall"] == pytest.approx(2 / 3, abs=1e-4)
    assert [(w["a_name"], w["label"], w["verdict"], w["pipeline"], w["reason"]) for w in r["wrong_pairs"]] == \
        [(f"{ids[1]}.NEF", "different", "same_group", "different", "r1"),
         (f"{ids[2]}.NEF", "same", "different_group", "different", "r2")]
    text = J.format_labels_comparison(r)
    assert "labels 9, matching a selected neighbour pair 8 (of 9 neighbour pairs): scored 7" in text
    assert "judge:    correct 2  wrong 2  abstained 2 (unsure/error; 1 of them labelled same)  of 6" in text
    assert "pipeline: correct 4  wrong 2  of 6" in text and "precision 0.500  recall 0.500" in text
    assert "strict recall 0.333" in text and "fixes 1 pipeline errors and breaks 1" in text
    assert "wrong (2):" in text and "label different, judge same_group (0.70), pipeline different: r1" in text
    empty = J.compare_with_labels([], {}, labels, photos)
    assert empty["judge"]["precision"] is None and "n/a" in J.format_labels_comparison(empty)


def test_run_judge_compares_with_labels_when_present(tmp_path, capsys):
    s, ids, config = _three_pairs(tmp_path)
    sha = {p["id"]: p["sha256"] for p in s.photos}
    save_labels(tmp_path, [{"a_sha": sha[ids[0]], "b_sha": sha[ids[1]], "label": "different"},
                           {"a_sha": sha[ids[1]], "b_sha": sha[ids[2]], "label": "different"}])
    J.run_judge(tmp_path, config, client_factory=lambda cfg: FakeClient([GOOD, DIFFERENT, GOOD]))
    data = json.loads((tmp_path / "judge_verdicts.json").read_text("utf-8"))
    assert data["labels"]["judge"]["correct"] == 1 and data["labels"]["judge"]["wrong"] == 1
    assert data["labels"]["pipeline"]["wrong"] == 1 and data["labels"]["judge"]["fixes"] == 0
    assert "== judge vs labels.json" in capsys.readouterr().out


# ------------------------------------------------------------------- client

def _chat_reply(content, usage=None):
    return {"choices": [{"message": {"role": "assistant", "content": content}}],
            "usage": usage or {"prompt_tokens": 1114, "completion_tokens": 40, "total_tokens": 1154}}


def test_client_request_body_headers_and_url(monkeypatch):
    monkeypatch.delenv("VLM_API_KEY", raising=False)
    client = client_with([_chat_reply(GOOD)])
    image = b"\xff\xd8\xff\xe0JPEG-BYTES-0123456789"
    text = client.ask("the prompt", [image], J.VERDICT_SCHEMA)
    assert text == GOOD and client.last_usage["prompt_tokens"] == 1114
    request, timeout = client._open.calls[0]
    assert request.full_url == "http://localhost:8000/v1/chat/completions" and request.get_method() == "POST"
    assert timeout == 120 and request.get_header("Content-type") == "application/json"
    assert request.get_header("Authorization") is None
    body = json.loads(request.data.decode("utf-8"))
    assert body["model"] == "Qwen/Qwen3.5-9B" and body["max_tokens"] == 256 and body["temperature"] == 0.0
    assert body["chat_template_kwargs"] == {"enable_thinking": False}
    assert body["response_format"] == {"type": "json_schema", "json_schema": {
        "name": "pair_verdict", "schema": J.VERDICT_SCHEMA, "strict": True}}
    content = body["messages"][0]["content"]
    assert body["messages"][0]["role"] == "user" and len(content) == 2
    assert content[0] == {"type": "image_url", "image_url": {
        "url": "data:image/jpeg;base64," + base64.b64encode(image).decode("ascii")}}
    assert content[1] == {"type": "text", "text": "the prompt"}

    monkeypatch.setenv("VLM_API_KEY", "secret-key")
    client = client_with([_chat_reply(GOOD)])
    client.ask("p", [image], J.VERDICT_SCHEMA)
    assert client._open.calls[0][0].get_header("Authorization") == "Bearer secret-key"


def test_client_failure_mapping():
    for reason in (ConnectionRefusedError(10061, "refused"), socket.gaierror(11001, "getaddrinfo failed"),
                   ConnectionResetError(10054, "reset")):
        with pytest.raises(VLMUnavailable):
            client_with([urllib.error.URLError(reason)]).ask("p", [b"x"], J.VERDICT_SCHEMA)
    with pytest.raises(VLMUnavailable):
        client_with([ConnectionResetError(10054, "reset")]).ask("p", [b"x"], J.VERDICT_SCHEMA)
    with pytest.raises(VLMError, match="HTTP 500") as exc:
        client_with([http_error(500, b'{"error": "boom"}')]).ask("p", [b"x"], J.VERDICT_SCHEMA)
    assert not isinstance(exc.value, VLMUnavailable) and "boom" in str(exc.value)
    for failure in (TimeoutError("timed out"), socket.timeout("timed out"), urllib.error.URLError(TimeoutError()),
                    {"choices": []}, {"error": "x"}, _chat_reply(None), b"<html>not json</html>"):
        with pytest.raises(VLMError) as exc:
            client_with([failure]).ask("p", [b"x"], J.VERDICT_SCHEMA)
        assert not isinstance(exc.value, VLMUnavailable)


def test_client_ping():
    client = client_with([{"data": [{"id": "Qwen/Qwen3.5-9B"}, {"id": "other"}]}])
    assert client.ping() == ["Qwen/Qwen3.5-9B", "other"]
    request, timeout = client._open.calls[0]
    assert request.full_url == "http://localhost:8000/v1/models" and request.get_method() == "GET" and timeout == 10
    with pytest.raises(VLMError, match="not Qwen/Qwen3.5-9B"):
        client_with([{"data": [{"id": "other"}]}]).ping()
    with pytest.raises(VLMUnavailable):
        client_with([urllib.error.URLError(ConnectionRefusedError())]).ping()
    with pytest.raises(VLMError):
        client_with([{"object": "list"}]).ping()


def test_make_client():
    assert isinstance(make_client(VLM), OpenAICompatibleClient)
    assert make_client({**VLM, "base_url": "http://localhost:8000/v1/"}).base_url == "http://localhost:8000/v1"
    with pytest.raises(ValueError, match="bedrock"):
        make_client({**VLM, "provider": "bedrock"})


def test_image_data_never_reaches_logs_or_errors(caplog):
    image = bytes(range(256)) * 4
    encoded = base64.b64encode(image).decode("ascii")
    caplog.set_level(logging.DEBUG)
    client = client_with([_chat_reply(GOOD)])
    client.ask("PROMPT-TEXT-7f3a-must-not-be-logged", [image], J.VERDICT_SCHEMA)
    assert "VLM request: 1 image(s), 1024 bytes" in caplog.text
    assert encoded not in caplog.text and encoded[:40] not in caplog.text and "7f3a" not in caplog.text
    echo = ('{"detail": [{"msg": "invalid", "input": "data:image/jpeg;base64,' + encoded + '"}]}').encode()
    with pytest.raises(VLMError) as exc:
        client_with([http_error(422, echo)]).ask("p", [image], J.VERDICT_SCHEMA)
    assert encoded[:40] not in str(exc.value) and "<base64>" in str(exc.value) and len(str(exc.value)) < 400
    assert encoded[:40] not in caplog.text


# ------------------------------------------------- added after the review

def test_lookback_off_in_grouping_means_no_lookback_pairs():
    # grouping.lookback_seconds: 0 turns look-back off; same-second photos must not slip through.
    s = Shoot()
    a = s.add(0, unit(0))
    x = s.add(0, unit(1))
    b = s.add(0, mix(unit(0), unit(2), 0.85))
    pairs, stats = s.select(groups_of([a], [x], [b]), grouping={"lookback_seconds": 0})
    assert pairs == [] and stats["lookback_in_band"] == 0 and stats["above_band_not_joined"] == 0
    s.photos[2]["capture_time"] = (T0 + timedelta(seconds=5)).isoformat()
    assert summary(s.select(groups_of([a], [x], [b]))[0]) == [(a, b, "lookback", 0.85, False)]


def test_lookback_skips_groups_blocked_by_different_people():
    # The best-matching group shows different people: the pipeline skipped it, so the next
    # group is the real candidate. With --include-faces-decided the blocked pair comes too.
    s = Shoot()
    a = s.add(0, unit(0), ids=["C"])
    c = s.add(10, (0.6 * unit(0) + 0.8 * unit(1)).astype(np.float32))
    other = s.add(20, unit(3))
    vec = np.zeros(DIM, np.float32)
    vec[0], vec[1] = 0.88, 0.4025                           # 0.88 to a (blocked), 0.85 to c
    vec[2] = np.sqrt(1 - vec[0] ** 2 - vec[1] ** 2)
    b = s.add(40, vec, ids=["A", "B"])
    groups = groups_of([a], [c], [other], [b])
    pairs, stats = s.select(groups)
    assert summary(pairs) == [(c, b, "lookback", 0.85, False)]
    assert stats["lookback_blocked_by_faces"] == 1 and stats["above_band_not_joined"] == 0
    pairs, _ = s.select(groups, include_faces_decided=True)
    assert summary(pairs) == [(a, b, "lookback", 0.88, False), (c, b, "lookback", 0.85, False)]
    assert [p["faces_relation"] for p in pairs] == ["different", None]
    # Blocked above the band: counted as blocked, never as "above band, not joined".
    s.embeddings[s.photos[3]["sha256"]] = mix(unit(0), unit(2), 0.95)
    pairs, stats = s.select(groups)
    assert pairs == [] and stats["lookback_blocked_by_faces"] == 1 and stats["above_band_not_joined"] == 0


def test_lookback_join_recorded_in_groups_json_is_a_false_merge_candidate():
    # [a1, prev, b] where b joined through an earlier member (joined_by "lookback") because
    # its similarity to prev (0.75) failed the neighbour rule: the in-band match to a1 is a
    # possible false merge. The same photos joined by "neighbour" are not a candidate.
    s = Shoot()
    a1 = s.add(0, unit(0))
    prev = s.add(10, mix(unit(0), unit(1), 0.90))
    vec = np.zeros(DIM, np.float32)
    vec[0], vec[1] = 0.85, (0.75 - 0.90 * 0.85) / np.sqrt(1 - 0.90 ** 2)
    vec[2] = np.sqrt(1 - vec[0] ** 2 - vec[1] ** 2)
    b = s.add(20, vec)
    groups = groups_of([a1, prev, b])
    groups["groups"][0]["joined_by"] = ["neighbour", "lookback"]
    assert summary(s.select(groups)[0]) == [(a1, b, "lookback", 0.85, True)]
    groups["groups"][0]["joined_by"] = ["neighbour", "neighbour"]
    assert s.select(groups)[0] == []
    del groups["groups"][0]["joined_by"]  # an older groups.json: adjacency decides
    assert s.select(groups)[0] == []


def test_relaxed_lookback_join_is_kept_even_when_faces_or_people_decided_it():
    s = Shoot()
    a1 = s.add(0, unit(0), ids=["A", "B"], people=False)
    other = s.add(10, unit(1), ids=["C"])
    a2 = s.add(30, mix(unit(0), unit(3), 0.85), ids=["A", "B"], people=False)
    pairs, stats = s.select(groups_of([a1, a2], [other]))
    assert summary(pairs) == [(a1, a2, "lookback", 0.85, True)] and pairs[0]["faces_relation"] == "same"
    assert stats["excluded_faces_same"] == 0 and stats["excluded_no_people"] == 0


def test_above_band_match_lost_to_a_closer_own_group_is_counted_apart():
    s = Shoot()
    a1 = s.add(0, unit(0))
    b_vec = (0.92 * unit(0) + 0.392 * unit(1)).astype(np.float32)
    b0 = s.add(5, mix(b_vec, unit(3), 0.95))
    b = s.add(20, b_vec)
    pairs, stats = s.select(groups_of([a1], [b0, b]))
    assert [p["kind"] for p in pairs] == ["neighbour"]  # a1 -> b0 at 0.874
    assert stats["above_band_closer_group"] == 1 and stats["above_band_not_joined"] == 0


def test_negative_max_pairs_means_all():
    s = Shoot()
    ids = [s.add(0, unit(0))]
    for k in range(1, 4):
        ids.append(s.add(10 * k, mix(s.embeddings[s.photos[-1]["sha256"]], unit(k), 0.85)))
    pairs, stats = s.select(groups_of(*[[i] for i in ids]), max_pairs=-3)
    assert len(pairs) == 3 and stats["cut_by_max_pairs"] == 0


def test_adjacent_join_is_not_a_lookback_join_candidate():
    # [a1, a2, b]: b joined through a2 (neighbour, 0.85) and is 0.88 to a1. That is an
    # intra-group similarity, not a look-back join: no second pair.
    s = Shoot()
    a1 = s.add(0, unit(0))
    a2 = s.add(10, mix(unit(0), unit(1), 0.90))
    vec = np.zeros(DIM, np.float32)
    vec[0], vec[1] = 0.88, (0.85 - 0.90 * 0.88) / np.sqrt(1 - 0.90 ** 2)
    vec[2] = np.sqrt(1 - vec[0] ** 2 - vec[1] ** 2)
    b = s.add(20, vec)
    pairs, _ = s.select(groups_of([a1, a2, b]))
    assert summary(pairs) == [(a2, b, "neighbour", 0.85, True)]


def test_faces_relation_uses_the_grouping_allow_unknown_setting():
    s = Shoot()
    p0 = s.add(0, unit(0), ids=["A", "B"])
    p1 = s.add(10, mix(unit(0), unit(1), 0.85), ids=["B"], n_faces=2)  # B plus one unknown face
    groups = groups_of([p0], [p1])
    assert [p["faces_relation"] for p in s.select(groups)[0]] == [None]
    pairs, stats = s.select(groups, grouping={"faces_same_allows_unknown": True})
    assert pairs == [] and stats["excluded_faces_same"] == 1


def test_format_dry_run_lists_every_exclusion():
    stats = {"photos": 9, "cameras": 1, "skipped_photos": 6, "neighbour_in_band": 0, "lookback_in_band": 0,
             "excluded_faces_same": 1, "excluded_faces_different": 2, "excluded_no_people": 3,
             "lookback_blocked_by_faces": 7, "above_band_not_joined": 4, "above_band_closer_group": 8,
             "cut_by_max_pairs": 5, "selected": 1}
    pair = {"kind": "lookback", "pipeline_same_group": True, "faces_relation": "different", "image_size": [1560, 512]}
    out = J.format_dry_run([pair], stats, JUDGE)
    for label, n in (("faces decided same", 1), ("faces decided different", 2), ("no people on both sides", 3),
                     ("above band, not joined", 4), ("cut by max_pairs", 5), ("photos not usable", 6),
                     ("look-back blocked, faces", 7), ("above band, closer group", 8)):
        assert re.search(rf"{re.escape(label)} +{n}(?!\d)", out), label
    assert "lookback       1   pipeline joined 1, split 0  (joined = look-back joins" in out
    assert "faces already decided: same 0, different 1" in out


def test_pairs_sheet_frame_colour_follows_the_pipeline(tmp_path):
    s = Shoot(tmp_path)
    ids = [s.add(k, unit(0)) for k in range(3)]
    pairs = [{"a_id": ids[k], "b_id": ids[k + 1], "a_name": "a", "b_name": "b", "kind": "neighbour",
              "similarity": 0.85, "gap_seconds": 1.0, "pipeline_same_group": k == 0, "faces_relation": None}
             for k in range(2)]
    path = J.write_pairs_sheet(tmp_path, pairs, s.by_id())[0]
    cell_w = 2 * J.SHEET_THUMB + 40
    with Image.open(path) as img:
        joined = img.getpixel((8 + 20, 24 - 3))            # top edge of the first frame
        split = img.getpixel((cell_w + 8 + 20, 24 - 3))    # second cell
    assert joined[1] > joined[0] + 50 and split[0] > split[1] + 50  # green vs red


def test_run_judge_overrides_config_and_reads_identities(tmp_path, capsys):
    from culling.faces import save_identities
    s = Shoot(tmp_path)
    p0 = s.add(0, unit(0))
    p1 = s.add(10, mix(unit(0), unit(1), 0.85))
    p2 = s.add(20, mix(s.embeddings[s.photos[1]["sha256"]], unit(2), 0.85))
    config = make_output(tmp_path, s, groups_of([p0, p1], [p2]))
    config["faces"]["enabled"] = True
    sha = {p["id"]: p["sha256"] for p in s.photos}
    save_identities(tmp_path, {"threshold": 0.4, "min_identity_faces": 10,
                               "identities": {"A": {"n_faces": 20, "n_photos": 20}, "B": {"n_faces": 20, "n_photos": 20}},
                               "photos": {sha[p0]: {"ids": ["A", "B"], "faces": ["A", "B"], "n_faces": 2},
                                          sha[p1]: {"ids": ["A", "B"], "faces": ["A", "B"], "n_faces": 2},
                                          sha[p2]: {"ids": [], "faces": [], "n_faces": 0}}})
    result = J.run_judge(tmp_path, config, dry_run=True)
    assert [(p["a_id"], p["faces_relation"]) for p in result["pairs"]] == [(p1, None)]
    assert result["stats"]["excluded_faces_same"] == 1
    result = J.run_judge(tmp_path, config, dry_run=True, include_faces_decided=True, max_pairs=1)
    assert [(p["a_id"], p["faces_relation"]) for p in result["pairs"]] == [(p0, "same")]
    assert result["stats"]["cut_by_max_pairs"] == 1
    assert re.search(r"cut by max_pairs +1(?!\d)", capsys.readouterr().out)


def test_run_judging_uses_the_configured_max_retries(tmp_path):
    s, ids, config = _three_pairs(tmp_path)
    client = FakeClient(["bad", GOOD, DIFFERENT, UNSURE])
    result = J.run_judge(tmp_path, config, client_factory=lambda cfg: client)
    assert result["verdicts"]["verdicts"][f"{ids[0]}|{ids[1]}"]["attempts"] == 2
    (tmp_path / "judge_verdicts.json").unlink()
    config["vlm"]["max_retries"] = 0
    client = FakeClient(["bad", GOOD, GOOD])
    result = J.run_judge(tmp_path, config, client_factory=lambda cfg: client)
    first = result["verdicts"]["verdicts"][f"{ids[0]}|{ids[1]}"]
    assert first["verdict"] == "error" and first["attempts"] == 1


def test_unknown_provider_exits_cleanly(tmp_path):
    s, ids, config = _three_pairs(tmp_path)
    config["vlm"]["provider"] = "bedrock"
    with pytest.raises(SystemExit, match="bedrock"):
        J.run_judge(tmp_path, config)
    assert not (tmp_path / "judge_pairs.json").exists()


def test_client_ignores_system_proxies(monkeypatch):
    # The default opener must not consult HTTP_PROXY: images go to base_url only. With a
    # proxy pointing at a closed local port the request still goes to base_url (also a
    # closed local port) and fails with "cannot reach", never through the proxy.
    import urllib.request
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        free_port = probe.getsockname()[1]
    monkeypatch.setenv("HTTP_PROXY", f"http://127.0.0.1:{free_port}")
    monkeypatch.setenv("http_proxy", f"http://127.0.0.1:{free_port}")
    monkeypatch.delenv("NO_PROXY", raising=False)
    monkeypatch.delenv("no_proxy", raising=False)
    client = OpenAICompatibleClient({**VLM, "base_url": "http://127.0.0.1:1/v1", "timeout_seconds": 5})
    with pytest.raises(VLMUnavailable, match="cannot reach http://127.0.0.1:1/v1"):
        client.ping()
    assert urllib.request.getproxies().get("http", "").endswith(str(free_port))  # the env was really set


def test_client_maps_http_client_exceptions():
    import http.client
    for failure in (http.client.IncompleteRead(b"x", 10), http.client.BadStatusLine("HELLO THERE"),
                    http.client.InvalidURL("nonnumeric port")):
        with pytest.raises(VLMError) as exc:
            client_with([failure]).ask("p", [b"x"], J.VERDICT_SCHEMA)
        assert not isinstance(exc.value, VLMUnavailable) and type(failure).__name__ in str(exc.value)

    class Cut(FakeResponse):
        def read(self):
            raise http.client.IncompleteRead(b"partial", 400)

    client = OpenAICompatibleClient(VLM, opener=lambda request, timeout=None: Cut(b""))
    with pytest.raises(VLMError, match="IncompleteRead"):
        client.ask("p", [b"x"], J.VERDICT_SCHEMA)
    with pytest.raises(VLMUnavailable):  # the server hanging up before any reply stays "unavailable"
        client_with([http.client.RemoteDisconnected("Remote end closed connection")]).ask("p", [b"x"], J.VERDICT_SCHEMA)
