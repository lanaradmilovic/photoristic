import json

import pytest

from culling.agency import (CULL_FILE, build_cull, delete_originals, import_cull,
                            read_rejected_list, scan_after_folder)
from culling.config import DEFAULTS
from culling.ingest import DELETED_MARKER, run_ingest, save_photos


def photo(tmp_path, folder, name, pid, preview=True, status="ok"):
    """A processed photo: original file in the input, preview and thumbnail in the output."""
    f = tmp_path / "pre" / folder / name
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_bytes(b"x" * 100)
    out = tmp_path / "out"
    for d in ("previews", "thumbs"):
        (out / d).mkdir(parents=True, exist_ok=True)
        if preview:
            (out / d / f"{pid}.jpg").write_bytes(b"p")
    return {"id": pid, "status": status, "primary_path": str(f), "jpg_path": str(f), "nef_path": None,
            "file_size": 100, "preview_file": f"previews/{pid}.jpg", "thumb_file": f"thumbs/{pid}.jpg"}


def groups(*photos):
    return {"groups": [{"photo_ids": [p["id"] for p in photos]}]}


def test_rejected_list_takes_names_from_dir_output_and_paths(tmp_path):
    f = tmp_path / "obrisano.txt"
    f.write_text("﻿KNEZ3820.JPG\n\nC:\\x\\obrisano\\LPZ_4052.jpg\n01 B&W.psd\nnotes\n", encoding="utf-8")
    assert read_rejected_list(f) == ["KNEZ3820.JPG", "LPZ_4052.jpg"]


def test_after_folder_gives_kept_rejected_both_missing_and_unmatched(tmp_path):
    photos = [photo(tmp_path, "01", n, f"id{i}") for i, n in enumerate(["A1.JPG", "A2.JPG", "A3.JPG", "A4.JPG"])]
    after = tmp_path / "posle"
    for rel in ["1/A1.JPG", "obrisano/A2.JPG", "2/A3.JPG", "Obrisano/A3.JPG", "obrisano/X9.JPG", "obrisano/m.psd"]:
        (after / rel).parent.mkdir(parents=True, exist_ok=True)
        (after / rel).write_bytes(b"y")
    seen, files = scan_after_folder(after, "obrisano")
    cull = build_cull(photos, seen, after, complete=True)
    decisions = {v["name"]: v["decision"] for v in cull["photos"].values()}
    assert decisions == {"A1.JPG": "kept", "A2.JPG": "rejected", "A3.JPG": "both", "A4.JPG": "missing"}
    assert cull["unmatched"] == ["x9"]
    assert len(files) == 5                      # the PSD is not a photo


def test_after_folder_skips_excluded_folders(tmp_path):
    after = tmp_path / "posle"
    for rel in ["00 Nove Montaze/M1.jpg", "1/A1.JPG"]:
        (after / rel).parent.mkdir(parents=True, exist_ok=True)
        (after / rel).write_bytes(b"y")
    seen, files = scan_after_folder(after, "obrisano", exclude_names=["00 nove montaze"])
    assert set(seen) == {"a1"} and len(files) == 1


def test_rejected_list_counts_everything_else_as_kept(tmp_path):
    photos = [photo(tmp_path, "01", "A1.JPG", "a"), photo(tmp_path, "01", "A2.JPG", "b")]
    cull = build_cull(photos, {"a2": {"rejected"}}, "list", complete=False)
    assert cull["photos"]["a"]["decision"] == "kept" and cull["photos"]["b"]["decision"] == "rejected"


def test_same_file_name_in_two_folders_is_ambiguous(tmp_path):
    photos = [photo(tmp_path, "01", "A1.JPG", "a"), photo(tmp_path, "02", "A1.JPG", "b")]
    cull = build_cull(photos, {"a1": {"rejected"}}, "list", complete=False)
    assert {v["decision"] for v in cull["photos"].values()} == {"ambiguous"}


def test_delete_only_fully_processed_originals_and_their_after_copies(tmp_path):
    out = tmp_path / "out"
    good = photo(tmp_path, "01", "A1.JPG", "a")
    no_preview = photo(tmp_path, "01", "A2.JPG", "b", preview=False)
    failed = photo(tmp_path, "01", "A3.JPG", "c", status="error")
    ungrouped = photo(tmp_path, "01", "A4.JPG", "d")
    other = tmp_path / "pre" / "01" / "montage.psd"
    other.write_bytes(b"z")
    after = tmp_path / "posle" / "obrisano"
    after.mkdir(parents=True)
    (after / "A1.JPG").write_bytes(b"y")
    (after / "A2.JPG").write_bytes(b"y")
    photos = [good, no_preview, failed, ungrouped]
    n, _ = delete_originals(out, tmp_path / "pre", photos, groups(good, no_preview, failed),
                            after_files=[after / "A1.JPG", after / "A2.JPG"])
    assert n == 2
    assert not (tmp_path / "pre/01/A1.JPG").exists() and not (after / "A1.JPG").exists()
    for kept in ["pre/01/A2.JPG", "pre/01/A3.JPG", "pre/01/A4.JPG", "pre/01/montage.psd", "posle/obrisano/A2.JPG"]:
        assert (tmp_path / kept).exists(), kept
    assert "A1.JPG" in (out / DELETED_MARKER).read_text(encoding="utf-8")


def test_changed_file_is_not_deleted(tmp_path):
    p = photo(tmp_path, "01", "A1.JPG", "a")
    (tmp_path / "pre/01/A1.JPG").write_bytes(b"x" * 101)
    n, _ = delete_originals(tmp_path / "out", tmp_path / "pre", [p], groups(p))
    assert n == 0 and (tmp_path / "pre/01/A1.JPG").exists()


def test_import_cull_writes_the_file(tmp_path):
    out = tmp_path / "out"
    photos = [photo(tmp_path, "01", "A1.JPG", "a")]
    save_photos(out, photos, tmp_path / "pre")
    lst = tmp_path / "obrisano.txt"
    lst.write_text("A1.JPG\n", encoding="utf-8")
    import_cull(out, DEFAULTS, rejected_list=lst)
    data = json.loads((out / CULL_FILE).read_text(encoding="utf-8"))
    assert data["counts"] == {"rejected": 1}


def test_ingest_refuses_after_originals_were_deleted(tmp_path):
    (tmp_path / "pre").mkdir()
    (tmp_path / "out").mkdir()
    (tmp_path / "out" / DELETED_MARKER).write_text("x", encoding="utf-8")
    with pytest.raises(RuntimeError, match="deleted"):
        run_ingest(tmp_path / "pre", tmp_path / "out", DEFAULTS)
