import csv
import json
from datetime import datetime

import numpy as np
import pytest

from culling.agency import CULL_FILE
from culling.analysis import (ANALYSIS_DIR, CSV_COLUMNS, PHOTOS_CSV, REASONS_FILE, SUMMARY_FILE,
                              camera_of, day_part, load_wedding, run_analysis)
from culling.config import DEFAULTS

CAMERAS = [{"prefix": "KNEZ", "role": "main", "clock_offset_s": 0},
           {"prefix": "LPZ_", "role": "second", "clock_offset_s": -300}]
PARTS = [{"part": "couple", "start": "15:00", "end": "16:00", "cameras": ["KNEZ"]},
         {"part": "arrival", "start": "15:00", "end": "16:00"},
         {"part": "party", "start": "16:00", "end": "24:00"}]


def wedding_dir(tmp_path, **extra):
    d = tmp_path / "wedding"
    d.mkdir()
    w = {"wedding": "test", "cameras": CAMERAS, "day_parts": PARTS, **extra}
    (d / "wedding.json").write_text(json.dumps(w), encoding="utf-8")
    return d


def output(tmp_path, frames, reasons=()):
    """frames: (file, capture time, vector, decision, couple ids)."""
    out = tmp_path / "out"
    out.mkdir()
    photos, cull, ident, keys, vecs = [], {}, {}, [], []
    for i, (name, t, vec, decision, ids) in enumerate(frames):
        pid, sha = f"id{i}", f"sha{i}"
        photos.append({"id": pid, "sha256": sha, "status": "ok", "primary_path": f"C:\\x\\{name}",
                       "capture_time": t, "camera_id": "SN1"})
        cull[pid] = {"name": name, "decision": decision}
        ident[sha] = {"ids": ids, "n_faces": len(ids)}
        v = np.array(vec, dtype=np.float32)
        keys.append(sha)
        vecs.append(v / np.linalg.norm(v))
    (out / "photos.json").write_text(json.dumps({"photos": photos}), encoding="utf-8")
    (out / CULL_FILE).write_text(json.dumps({"source": "C:\\posle", "photos": cull}), encoding="utf-8")
    (out / "identities.json").write_text(json.dumps({"photos": ident}), encoding="utf-8")
    np.savez(out / "embeddings.npz", keys=np.array(keys), vectors=np.stack(vecs), model_name=np.array("m"))
    if reasons:
        (out / ANALYSIS_DIR).mkdir()
        (out / ANALYSIS_DIR / REASONS_FILE).write_text(
            "".join(json.dumps(r) + "\n" for r in reasons), encoding="utf-8")
    return out


def config():
    return {"analysis": dict(DEFAULTS["analysis"])}


def test_camera_by_longest_prefix_and_day_part_by_camera_then_time():
    cams = CAMERAS + [{"prefix": "KNEZ2", "role": "decor"}]
    assert camera_of("knez2_001.jpg", cams)["role"] == "decor"
    assert camera_of("KNEZ001.JPG", cams)["role"] == "main"
    assert camera_of("VAL001.JPG", cams) is None
    t = datetime(2026, 11, 8, 15, 30)
    assert day_part(t, "KNEZ", PARTS) == "couple"
    assert day_part(t, "LPZ_", PARTS) == "arrival"
    assert day_part(datetime(2026, 11, 8, 9, 0), "KNEZ", PARTS) == "other"


def test_wedding_with_unknown_role_or_part_is_an_error(tmp_path):
    d = tmp_path / "w"
    d.mkdir()
    (d / "wedding.json").write_text(json.dumps(
        {"wedding": "x", "cameras": [{"prefix": "A", "role": "boss"}], "day_parts": []}), encoding="utf-8")
    with pytest.raises(ValueError, match="role"):
        load_wedding(d)


def test_analysis_writes_rows_bursts_rules_and_reasons(tmp_path):
    a, b = [1, 0, 0], [0, 1, 0]
    frames = [
        # a burst of three on KNEZ (0.5 s apart, identical): agency keeps the first and the last
        ("KNEZ1.JPG", "2026-11-08T15:10:00.0", a, "kept", ["B", "C"]),
        ("KNEZ2.JPG", "2026-11-08T15:10:00.5", a, "rejected", ["B", "C"]),
        ("KNEZ3.JPG", "2026-11-08T15:10:01.0", a, "kept", ["B"]),
        # a different scene 1 s later: no burst
        ("KNEZ4.JPG", "2026-11-08T15:10:02.0", b, "rejected", []),
        # second camera, clock 300 s ahead: 16:04 on its clock is 15:59 on KNEZ, 1 s from nothing
        ("LPZ_1.JPG", "2026-11-08T16:04:00.0", b, "kept", []),
        ("LPZ_2.JPG", "2026-11-08T16:15:02.0", b, "both", []),
    ]
    reasons = [{"file": "KNEZ2.JPG", "primary": "DUP", "secondary": "", "kept_alt": "KNEZ1.JPG",
                "loss": "no", "conf": "high", "note": "same", "reviewer": "r1", "codebook": 1},
               {"file": "knez4.jpg", "primary": "EYES", "loss": "yes", "conf": "low", "codebook": 1}]
    out = output(tmp_path, frames, reasons)
    wd = wedding_dir(tmp_path, couple_identities=["B", "C"])

    summary = run_analysis(out, wd, config())

    with open(out / ANALYSIS_DIR / PHOTOS_CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert list(rows[0]) == CSV_COLUMNS
    by = {r["file"]: r for r in rows}
    assert [by[n]["burst_size"] for n in ("KNEZ1.JPG", "KNEZ2.JPG", "KNEZ3.JPG", "KNEZ4.JPG")] == ["3", "3", "3", "1"]
    assert by["LPZ_1.JPG"]["time_ref"].startswith("2026-11-08T15:59:00")
    assert by["LPZ_1.JPG"]["day_part"] == "arrival" and by["KNEZ1.JPG"]["day_part"] == "couple"
    assert by["LPZ_2.JPG"]["day_part"] == "party"
    assert by["KNEZ1.JPG"]["couple"] == "2" and by["KNEZ4.JPG"]["couple"] == "0"
    assert by["KNEZ2.JPG"]["reason"] == "DUP" and by["KNEZ4.JPG"]["loss"] == "yes"

    assert json.loads((wd / SUMMARY_FILE).read_text(encoding="utf-8")) == summary
    assert summary["counts"]["both"] == 1
    assert summary["by_role"]["main"] == {"photos": 4, "rejected": 2, "rate": 0.5}
    assert summary["near_identical_pairs"] == {"pairs": 2, "both_kept": 0, "one_rejected": 2,
                                               "both_rejected": 0, "both_kept_share": 0.0}
    # keep-first drops KNEZ2 (rejected) and KNEZ3 (kept): one false reject, one of two rejects caught
    assert summary["rules"]["burst_keep_first"] == {
        "drops": 2, "drops_agency_kept": 1, "drops_agency_kept_share": 0.5,
        "agency_rejects_caught": 1, "agency_rejects_caught_share": 0.5}
    assert summary["rules"]["burst_keep_half"]["drops"] == 1
    assert summary["couple_in_frame"]["2"]["rejected"] == 1
    assert summary["reasons"]["by_code"] == {"DUP": 1, "EYES": 1}
    assert summary["reasons"]["loss_yes"] == ["KNEZ4.JPG"]
    assert summary["cull_source"] == "posle"


def test_analysis_without_agency_cull_says_what_to_run(tmp_path):
    out = tmp_path / "out"
    out.mkdir()
    (out / "photos.json").write_text(json.dumps({"photos": []}), encoding="utf-8")
    with pytest.raises(FileNotFoundError, match="cull.py agency"):
        run_analysis(out, wedding_dir(tmp_path), config())
