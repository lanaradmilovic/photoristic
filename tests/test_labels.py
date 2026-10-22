"""Ground-truth labels, scoring and the label server, on synthetic data."""
import hashlib
import json
import threading
import urllib.error
import urllib.request
from datetime import datetime, timedelta

import numpy as np
import pytest
from PIL import Image

from culling.labels import (LABELS_FILE, attach_boundary_info, boundaries, errors_sheet_name,
                            format_comparison, format_report, load_labels, normalise_labels,
                            save_labels, score, write_errors_sheet)
from culling.labelserver import make_server
from culling.report import write_report

T0 = datetime(2024, 6, 15, 16, 0, 0)


def photo(n, seconds, camera="SN1", status="ok", time=True):
    sha = hashlib.sha256(str(n).encode()).hexdigest()
    return {"id": sha[:16], "sha256": sha, "primary_path": f"C:/w/DSC_{n:04d}.NEF",
            "nef_path": f"C:/w/DSC_{n:04d}.NEF", "jpg_path": None,
            "thumb_file": f"thumbs/{sha[:16]}.jpg", "preview_file": f"previews/{sha[:16]}.jpg",
            "capture_time": (T0 + timedelta(seconds=seconds)).isoformat() if time else None,
            "camera_id": camera, "status": status, "flags": []}


def groups_of(*id_lists):
    """Minimal groups.json content: one group per id list."""
    return {"groups": [{"group_id": f"g{i:04d}", "photo_ids": list(ids), "joined_by": ["neighbour"] * (len(ids) - 1),
                        "consecutive_similarities": [0.9] * (len(ids) - 1),
                        "consecutive_gaps_seconds": [1.0] * (len(ids) - 1),
                        "boundary_similarity": 0.5 if i else None, "boundary_gap_seconds": 10.0 if i else None}
                       for i, ids in enumerate(id_lists, start=1)]}


def label(a, b, value, when="2026-10-22T10:00:00"):
    return {"a_sha": a["sha256"], "b_sha": b["sha256"], "a_name": "DSC_a.NEF", "b_name": "DSC_b.NEF",
            "label": value, "labeled_at": when}


# ------------------------------------------------------------------ boundaries

def test_boundaries_are_per_camera_in_capture_order():
    p = [photo(0, 10), photo(1, 0), photo(2, 5, camera="SN2"), photo(3, 20),
         photo(4, 2, camera="SN2"), photo(5, 30, status="error"), photo(6, 40, time=False)]
    groups = groups_of([p[1]["id"], p[0]["id"]], [p[3]["id"]], [p[4]["id"], p[2]["id"]])
    bs = boundaries(p, groups)
    pairs = [(b["camera_id"], b["a_name"], b["b_name"], b["pipeline"], b["gap"]) for b in bs]
    assert pairs == [("SN1", "DSC_0001.NEF", "DSC_0000.NEF", "same", 10.0),
                     ("SN1", "DSC_0000.NEF", "DSC_0003.NEF", "different", 10.0),
                     ("SN2", "DSC_0004.NEF", "DSC_0002.NEF", "same", 3.0)]
    assert bs[0]["a_sha"] == p[1]["sha256"] and bs[0]["b_thumb"] == p[0]["thumb_file"]


def test_boundary_similarity_from_embeddings_else_groups_json():
    p = [photo(0, 0), photo(1, 1), photo(2, 2)]
    v = np.array([1.0, 0.0], np.float32)
    emb = {p[0]["sha256"]: v, p[1]["sha256"]: np.array([0.6, 0.8], np.float32)}
    groups = groups_of([p[0]["id"], p[1]["id"]], [p[2]["id"]])
    bs = boundaries(p, groups, emb)
    assert bs[0]["sim"] == pytest.approx(0.6)
    assert bs[1]["sim"] == 0.5  # boundary_similarity of the second group (no embedding for photo 2)
    assert boundaries(p, groups)[0]["sim"] == 0.9  # consecutive_similarities fallback
    assert boundaries(p, None)[0]["sim"] is None and boundaries(p, None)[0]["pipeline"] is None


def test_boundary_pipeline_none_when_photo_missing_from_groups():
    p = [photo(0, 0), photo(1, 1)]
    assert boundaries(p, groups_of([p[0]["id"]]))[0]["pipeline"] is None


# ------------------------------------------------------------------ scoring

def test_score_counts_and_metrics():
    p = [photo(i, i) for i in range(8)]
    groups = groups_of([p[0]["id"], p[1]["id"], p[2]["id"]], [p[3]["id"], p[4]["id"]], [p[5]["id"]],
                       [p[6]["id"], p[7]["id"]])
    labels = [label(p[0], p[1], "same"),        # tp
              label(p[1], p[2], "different"),   # false merge
              label(p[2], p[3], "different"),   # tn
              label(p[3], p[4], "same"),        # tp
              label(p[4], p[5], "same"),        # missed merge
              label(p[5], p[6], "unsure"),      # skipped
              label(p[6], p[7], "same")]        # tp
    r = score(labels, p, groups)
    assert (r["n_labels"], r["n_scored"], r["n_unsure"], r["n_missing"]) == (7, 6, 1, 0)
    assert (r["tp"], r["tn"], r["false_merges"], r["missed_merges"], r["correct"]) == (3, 1, 1, 1, 4)
    assert r["precision"] == pytest.approx(3 / 4) and r["recall"] == pytest.approx(3 / 4)
    assert r["f1"] == pytest.approx(0.75) and r["accuracy"] == pytest.approx(4 / 6)
    kinds = {(e["a_sha"], e["kind"]) for e in r["errors"]}
    assert kinds == {(p[1]["sha256"], "false_merge"), (p[4]["sha256"], "missed_merge")}


def test_score_skips_photos_missing_from_groups_or_photos():
    p = [photo(0, 0), photo(1, 1), photo(2, 2)]
    stranger = photo(99, 99)
    groups = groups_of([p[0]["id"], p[1]["id"]])  # photo 2 not grouped
    labels = [label(p[0], p[1], "same"), label(p[1], p[2], "different"), label(p[2], stranger, "same")]
    r = score(labels, p, groups)
    assert (r["n_scored"], r["n_missing"], r["tp"], r["errors"]) == (1, 2, 1, [])


def test_score_with_nothing_to_score_has_no_metrics():
    p = [photo(0, 0), photo(1, 1)]
    r = score([label(p[0], p[1], "unsure")], p, groups_of([p[0]["id"], p[1]["id"]]))
    assert r["n_scored"] == 0 and r["precision"] is None and r["f1"] is None and r["accuracy"] is None
    assert "n/a" in format_report("groups.json", r)


def test_attach_boundary_info_and_comparison_text():
    p = [photo(i, i) for i in range(4)]
    a = groups_of([p[0]["id"], p[1]["id"]], [p[2]["id"]], [p[3]["id"]])         # 0-1 joined, 2-3 split
    b = groups_of([p[0]["id"]], [p[1]["id"]], [p[2]["id"], p[3]["id"]])         # 0-1 split, 2-3 joined
    labels = [label(p[0], p[1], "different"), label(p[2], p[3], "same")]
    ra, rb = score(labels, p, a), score(labels, p, b)
    attach_boundary_info(ra["errors"], boundaries(p, a))
    assert ra["errors"][0]["gap"] == 1.0 and ra["errors"][0]["a_thumb"] == p[0]["thumb_file"]
    attach_boundary_info(ra["errors"], [])  # pair not adjacent any more
    assert ra["errors"][0]["sim"] is None
    text = format_comparison("a.json", ra, "b.json", rb)
    assert "2 fixed in B, 0 broken in B" in text and "F1" in text
    assert "fixed in B   FALSE MERGE" in text and "fixed in B   MISSED MERGE" in text
    text_rev = format_comparison("b.json", rb, "a.json", ra)
    assert "0 fixed in B, 2 broken in B" in text_rev


# ------------------------------------------------------------------ labels file

def test_labels_round_trip(tmp_path):
    p = [photo(0, 0), photo(1, 1)]
    labels = [{**label(p[0], p[1], "same"), "a_name": "Šđž.NEF"}]
    assert load_labels(tmp_path) == []
    save_labels(tmp_path, labels)
    assert (tmp_path / LABELS_FILE).exists() and not (tmp_path / "labels.tmp").exists()
    assert load_labels(tmp_path) == labels
    assert json.loads((tmp_path / LABELS_FILE).read_text("utf-8"))[0]["a_name"] == "Šđž.NEF"


def test_normalise_labels_rejects_bad_input():
    p = [photo(0, 0), photo(1, 1)]
    with pytest.raises(ValueError):
        normalise_labels({"a_sha": "x"})
    with pytest.raises(ValueError):
        normalise_labels([label(p[0], p[1], "maybe")])
    with pytest.raises(ValueError):
        normalise_labels([{"a_sha": "zz", "b_sha": "00", "label": "same"}])
    clean = normalise_labels([{"a_sha": p[0]["sha256"].upper(), "b_sha": p[1]["sha256"], "label": "same"}])
    assert clean[0]["a_sha"] == p[0]["sha256"] and clean[0]["a_name"] == "" and clean[0]["labeled_at"]


# ------------------------------------------------------------------ errors sheet

def test_errors_sheet_written_and_removed(tmp_path):
    (tmp_path / "thumbs").mkdir()
    p = [photo(0, 0), photo(1, 1), photo(2, 2)]
    Image.new("RGB", (120, 80), "red").save(tmp_path / p[0]["thumb_file"])  # photo 1, 2 have no thumb
    errors = [{"kind": "missed_merge", "a_name": "a", "b_name": "b", "label": "same", "pipeline": "different",
               "a_sha": p[0]["sha256"], "b_sha": p[1]["sha256"], "sim": 0.8, "gap": 2.0,
               "a_thumb": p[0]["thumb_file"], "b_thumb": p[1]["thumb_file"]},
              {"kind": "false_merge", "a_name": "b", "b_name": "c", "label": "different", "pipeline": "same",
               "a_sha": p[1]["sha256"], "b_sha": p[2]["sha256"], "sim": None, "gap": None,
               "a_thumb": None, "b_thumb": None}]
    path = write_errors_sheet(tmp_path, errors, "errors.nofaces.jpg")
    assert path == tmp_path / "errors.nofaces.jpg" and path.stat().st_size > 0
    with Image.open(path) as img:
        assert img.format == "JPEG" and img.width > 300
    assert write_errors_sheet(tmp_path, [], "errors.nofaces.jpg") is None
    assert not path.exists()


def test_errors_sheet_name():
    assert errors_sheet_name("groups.json") == "errors.jpg"
    assert errors_sheet_name("D:/x/groups.nofaces.json") == "errors.nofaces.jpg"
    assert errors_sheet_name("other.json") == "errors.other.jpg"


# ------------------------------------------------------------------ server

@pytest.fixture
def server(tmp_path):
    (tmp_path / "report.html").write_text("<html>report</html>", encoding="utf-8")
    srv = make_server(tmp_path, port=0)
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    yield srv, f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()
    srv.server_close()


def _request(url, data=None):
    req = urllib.request.Request(url, data=data, method="POST" if data is not None else "GET",
                                 headers={"Content-Type": "application/json"} if data is not None else {})
    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8") or "null")


def test_server_get_labels_and_static_files(server):
    srv, base = server
    assert _request(base + "/labels") == (200, [])
    with urllib.request.urlopen(base + "/report.html", timeout=5) as resp:
        assert resp.status == 200 and b"report" in resp.read()


def test_server_post_writes_labels_json(server, tmp_path):
    srv, base = server
    p = [photo(0, 0), photo(1, 1)]
    labels = [label(p[0], p[1], "different")]
    assert _request(base + "/labels", json.dumps(labels).encode()) == (200, {"saved": 1})
    assert load_labels(tmp_path) == labels
    assert _request(base + "/labels") == (200, labels)
    assert _request(base + "/labels", b"[]") == (200, {"saved": 0})
    assert load_labels(tmp_path) == []


def test_server_post_rejects_invalid_body(server, tmp_path):
    srv, base = server
    p = [photo(0, 0), photo(1, 1)]
    _request(base + "/labels", json.dumps([label(p[0], p[1], "same")]).encode())
    for body in (b"not json", b'{"a": 1}', json.dumps([label(p[0], p[1], "maybe")]).encode()):
        with pytest.raises(urllib.error.HTTPError) as exc:
            _request(base + "/labels", body)
        assert exc.value.code == 400
    assert len(load_labels(tmp_path)) == 1  # unchanged
    with pytest.raises(urllib.error.HTTPError) as exc:
        _request(base + "/other", b"[]")
    assert exc.value.code == 404


# ------------------------------------------------------------------ report

def test_report_embeds_label_data(tmp_path):
    p = [photo(0, 0), photo(1, 1)]
    groups = {"groups": [{"group_id": "g0001", "camera_id": "SN1", "photo_ids": [p[0]["id"], p[1]["id"]],
                          "size": 2, "start": p[0]["capture_time"], "end": p[1]["capture_time"],
                          "consecutive_similarities": [0.9], "consecutive_gaps_seconds": [1.0],
                          "joined_by": ["neighbour"], "min_similarity": 0.9, "boundary_similarity": None,
                          "boundary_gap_seconds": None, "split_from": None, "split_part": None, "flags": []}],
              "config_used": {"report_low_similarity": 0.85}}
    label_data = {"boundaries": boundaries(p, groups), "labels": [label(p[0], p[1], "same")]}
    html = write_report(tmp_path, p, groups, "D:/w </script>", None, label_data).read_text("utf-8")
    assert 'id="labelData"' in html and 'id="labelMode"' in html
    start = html.index('id="labelData"')
    block = html[start:html.index("</script>", start)]
    assert p[0]["sha256"] in block and '"label": "same"' in block.replace('":"', '": "')
    assert "<\\/script>" in block  # input_dir escaped inside the JSON block
    plain = write_report(tmp_path, p, groups, None, None, None).read_text("utf-8")
    assert 'id="labelData"' not in plain and 'id="labelMode" disabled' in plain
