"""Day segmentation on synthetic data (no models, no real photos)."""
import hashlib
import json
from datetime import datetime, timedelta

import pytest
from PIL import Image

from culling.config import DEFAULTS
from culling.report import write_report
from culling.segments import (SEGMENTS_FILE, SHEETS_DIR, attach_groups, build_segments, load_segments,
                              run_segments, sample_evenly, segment_photos, segment_stats,
                              write_segment_sheets)

T0 = datetime(2024, 6, 15, 16, 0, 0)
CFG = dict(DEFAULTS["segments"])


def photo(n, seconds, camera="SN1", status="ok", time=True, w=1536, h=1024):
    sha = hashlib.sha256(str(n).encode()).hexdigest()
    return {"id": sha[:16], "sha256": sha, "primary_path": f"C:/w/DSC_{n:04d}.NEF",
            "nef_path": f"C:/w/DSC_{n:04d}.NEF", "jpg_path": None,
            "thumb_file": f"thumbs/{sha[:16]}.jpg", "preview_file": f"previews/{sha[:16]}.jpg",
            "capture_time": (T0 + timedelta(seconds=seconds)).isoformat() if time else None,
            "camera_id": camera, "status": status, "flags": [] if time else ["no_timestamp"],
            "preview_w": w, "preview_h": h}


def groups_of(*id_lists):
    return {"groups": [{"group_id": f"g{i:04d}", "photo_ids": list(ids), "size": len(ids),
                        "camera_id": "SN1", "start": None, "end": None, "flags": [],
                        "consecutive_similarities": [0.9] * (len(ids) - 1),
                        "consecutive_gaps_seconds": [1.0] * (len(ids) - 1), "joined_by": [],
                        "min_similarity": None, "boundary_similarity": None, "boundary_gap_seconds": None,
                        "split_from": None, "split_part": None}
                       for i, ids in enumerate(id_lists, start=1)],
            "config_used": {"report_low_similarity": 0.85}}


# ------------------------------------------------------------------ cutting

def test_cut_at_gap_longer_than_threshold():
    p = [photo(0, 0), photo(1, 1), photo(2, 2), photo(3, 400), photo(4, 401)]
    segs = segment_photos(p, 300)
    assert [s["segment_id"] for s in segs] == ["S01", "S02"]
    assert segs[0]["photo_ids"] == [p[0]["id"], p[1]["id"], p[2]["id"]]
    assert segs[1]["photo_ids"] == [p[3]["id"], p[4]["id"]]
    assert segs[0]["start"] == p[0]["capture_time"] and segs[0]["end"] == p[2]["capture_time"]
    assert segs[0]["duration_seconds"] == 2.0 and segs[0]["n_photos"] == 3
    assert segs[1]["camera_id"] == "SN1"


def test_gap_equal_to_threshold_does_not_cut():
    p = [photo(0, 0), photo(1, 300)]
    assert len(segment_photos(p, 300)) == 1
    assert len(segment_photos(p, 299)) == 2


def test_photos_are_sorted_by_time_not_by_input_order():
    p = [photo(0, 500), photo(1, 0), photo(2, 501)]
    segs = segment_photos(p, 300)
    assert [s["photo_ids"] for s in segs] == [[p[1]["id"]], [p[0]["id"], p[2]["id"]]]


def test_cameras_are_segmented_separately():
    # Two cameras shooting at the same minutes: their timelines never mix, even when one
    # camera's pause is "filled" by the other camera's photos.
    p = [photo(0, 0), photo(1, 10, camera="SN2"), photo(2, 200, camera="SN2"), photo(3, 400),
         photo(4, 410, camera="SN2")]
    segs = segment_photos(p, 300)
    assert [(s["segment_id"], s["camera_id"], s["photo_ids"]) for s in segs] == [
        ("S01", "SN1", [p[0]["id"]]), ("S02", "SN1", [p[3]["id"]]),
        ("S03", "SN2", [p[1]["id"], p[2]["id"], p[4]["id"]])]


def test_photos_without_time_or_failed_go_to_unknown_segment():
    p = [photo(0, 0), photo(1, 1), photo(2, 2, time=False), photo(3, 3, status="error")]
    segs = segment_photos(p, 300)
    assert [s["segment_id"] for s in segs] == ["S01", "unknown"]
    assert segs[0]["photo_ids"] == [p[0]["id"], p[1]["id"]]
    unknown = segs[1]
    assert unknown["camera_id"] is None and unknown["start"] is None
    assert unknown["photo_ids"] == [p[2]["id"], p[3]["id"]]
    assert unknown["reasons"] == ["no_timestamp", "ingest_error"]
    assert "unknown" in unknown["flags"]
    # no unknown segment when every photo has a time
    assert [s["segment_id"] for s in segment_photos(p[:2], 300)] == ["S01"]


def test_tiny_flag_and_counts():
    p = [photo(i, i) for i in range(5)] + [photo(9, 1000)]
    data = build_segments(p, {**CFG, "gap_seconds": 300, "min_photos": 5})
    assert [s["flags"] for s in data["segments"]] == [[], ["tiny"]]
    assert data["n_segments"] == 2 and data["n_tiny"] == 1 and data["n_unknown_photos"] == 0
    assert data["gap_seconds"] == 300 and data["groups_crossing"] == []
    assert all(s["group_ids"] == [] for s in data["segments"])


# ------------------------------------------------------------------ statistics

def test_stats_without_people_or_identities_do_not_fail():
    p = [photo(0, 0), photo(1, 1)]
    st = segment_stats(p, None, None)
    assert st["median_gap_s"] == 1.0 and st["burst_share"] == 1.0
    assert st["no_people_share"] is None and st["median_faces"] is None and st["identities"] == []
    assert st["portrait_share"] == 0.0
    single = segment_stats([photo(0, 0, w=None, h=None)], {}, None)
    assert single["median_gap_s"] is None and single["p90_gap_s"] is None
    assert single["burst_share"] is None and single["portrait_share"] is None


def test_stats_on_a_small_hand_made_example():
    # gaps: 1, 1, 8, 10 -> median 4.5, two of four below 2 s
    p = [photo(0, 0), photo(1, 1), photo(2, 2, w=1024, h=1536), photo(3, 10), photo(4, 20)]
    people = {p[0]["sha256"]: True, p[1]["sha256"]: False, p[2]["sha256"]: True,
              p[3]["sha256"]: False, p[4]["sha256"]: True}
    identities = {
        "min_identity_faces": 2,
        "identities": {"A": {"n_faces": 4, "n_photos": 4}, "B": {"n_faces": 3, "n_photos": 3},
                       "Z": {"n_faces": 1, "n_photos": 1}},
        "photos": {p[0]["sha256"]: {"ids": ["A", "B"], "faces": ["A", "B"], "n_faces": 2},
                   p[1]["sha256"]: {"ids": ["A"], "faces": ["A"], "n_faces": 1},
                   p[2]["sha256"]: {"ids": ["A", "B", "Z"], "faces": ["A", "B", "Z"], "n_faces": 3},
                   p[3]["sha256"]: {"ids": [], "faces": [], "n_faces": 0},
                   p[4]["sha256"]: {"ids": ["A", "B"], "faces": ["A", "B"], "n_faces": 2}},
    }
    st = segment_stats(p, people, identities)
    assert st["median_gap_s"] == 4.5
    assert st["p90_gap_s"] == pytest.approx(9.4)
    assert st["burst_share"] == 0.5
    assert st["no_people_share"] == 0.4
    assert st["median_faces"] == 2.0
    assert st["identities"] == [["A", 4], ["B", 3]]  # Z has too few faces to be known
    assert st["portrait_share"] == 0.2


def test_identities_limited_to_top_ten_sorted_by_count_then_label():
    p = [photo(i, i) for i in range(3)]
    labels = [chr(65 + i) for i in range(12)]
    identities = {"min_identity_faces": 1,
                  "identities": {l: {"n_faces": 5, "n_photos": 3} for l in labels},
                  "photos": {q["sha256"]: {"ids": labels, "faces": labels, "n_faces": 12} for q in p}}
    st = segment_stats(p, {}, identities)
    assert len(st["identities"]) == 10
    assert st["identities"][0] == ["A", 3] and st["identities"][-1] == ["J", 3]


# ------------------------------------------------------------------ groups

def test_groups_inside_and_crossing_a_boundary():
    p = [photo(0, 0), photo(1, 1), photo(2, 2), photo(3, 400), photo(4, 401), photo(5, 402)]
    groups = groups_of([p[0]["id"], p[1]["id"]], [p[2]["id"], p[3]["id"]], [p[4]["id"], p[5]["id"]])
    data = build_segments(p, {**CFG, "gap_seconds": 300}, groups_data=groups)
    s1, s2 = data["segments"]
    assert s1["group_ids"] == ["g0001", "g0002"] and s2["group_ids"] == ["g0003"]
    assert s1["stats"]["n_groups"] == 1 and s2["stats"]["n_groups"] == 1
    assert s1["stats"]["n_groups_crossing"] == 1 and s2["stats"]["n_groups_crossing"] == 1
    assert data["groups_crossing"] == ["g0002"]


def test_attach_groups_ignores_groups_of_unknown_photos_only():
    p = [photo(0, 0), photo(1, 1, time=False)]
    segs = segment_photos(p, 300)
    for s in segs:
        s["stats"] = segment_stats([p[i] for i in range(2) if p[i]["id"] in s["photo_ids"]])
    crossing = attach_groups(segs, groups_of([p[0]["id"]], [p[1]["id"]]))
    assert crossing == []
    assert segs[0]["group_ids"] == ["g0001"] and segs[1]["group_ids"] == ["g0002"]


# ------------------------------------------------------------------ files + sheets

def test_run_segments_without_optional_files(tmp_path):
    p = [photo(0, 0), photo(1, 1), photo(2, 900)]
    (tmp_path / "photos.json").write_text(json.dumps({"created": "x", "input_dir": None, "photos": p}),
                                          encoding="utf-8")
    data = run_segments(tmp_path, {"segments": dict(CFG)})
    assert (tmp_path / SEGMENTS_FILE).exists()
    saved = load_segments(tmp_path)
    assert saved["n_segments"] == 2 and saved["segments"][0]["stats"]["no_people_share"] is None
    assert saved["segments"][0]["group_ids"] == [] and saved["segments"][0]["stats"]["n_groups"] is None
    assert data["n_segments"] == saved["n_segments"]
    assert load_segments(tmp_path / "nowhere") is None


def test_sample_evenly_keeps_ends_and_order():
    assert sample_evenly(list(range(3)), 5) == [0, 1, 2]
    picked = sample_evenly(list(range(100)), 4)
    assert picked[0] == 0 and picked[-1] == 99 and picked == sorted(picked) and len(picked) == 4


def test_segment_sheets_written(tmp_path):
    p = [photo(i, i) for i in range(10)] + [photo(20, 1000)]
    (tmp_path / "thumbs").mkdir()
    for q in p[:6]:  # the rest have no thumbnail on disk -> grey tile, no error
        Image.new("RGB", (20, 14), (120, 160, 200)).save(tmp_path / q["thumb_file"])
    p[7]["thumb_file"] = None
    data = build_segments(p, {**CFG, "gap_seconds": 300})
    sheets = write_segment_sheets(tmp_path, p, data, max_thumbs=4, cols=2, edge=30)
    assert sheets == tmp_path / SHEETS_DIR
    assert sorted(f.name for f in sheets.glob("*.jpg")) == ["S01.jpg", "S02.jpg"]
    with Image.open(sheets / "S01.jpg") as img:
        assert img.size[1] > 48 and img.size[0] == 2 * 38 + 8
    # stale sheets are removed on the next run
    (sheets / "S99.jpg").write_bytes(b"x")
    write_segment_sheets(tmp_path, p, data, max_thumbs=4, cols=2, edge=30)
    assert not (sheets / "S99.jpg").exists()


def test_report_shows_segment_bars_only_with_segments(tmp_path):
    p = [photo(0, 0), photo(1, 1), photo(2, 900)]
    groups = groups_of([p[0]["id"], p[1]["id"]], [p[2]["id"]])
    for g in groups["groups"]:
        g["start"] = g["end"] = p[0]["capture_time"]
    data = build_segments(p, {**CFG, "gap_seconds": 300}, groups_data=groups)
    html = write_report(tmp_path, p, groups, None, None, None).read_text(encoding="utf-8")
    assert 'class="seghead"' not in html
    html = write_report(tmp_path, p, groups, None, None, None, segments_data=data).read_text(encoding="utf-8")
    assert html.count('class="seghead"') == 2
    assert 'href="segments_sheets/S01.jpg"' in html and ">S02<" in html
    assert html.index('>S01<') < html.index('>g0001<') < html.index('>S02<') < html.index('>g0002<')
