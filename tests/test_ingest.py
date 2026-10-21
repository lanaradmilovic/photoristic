from datetime import datetime
from pathlib import Path

from PIL import Image

from culling.config import DEFAULTS
from culling.ingest import assign_unique_ids, load_photos, process_source, run_ingest, scan_folder
from culling.metadata import parse_exif_time

INGEST_CFG = {**DEFAULTS["ingest"], "workers": 1, "preview_long_edge": 400, "thumb_long_edge": 100}


def make_jpg(path, size=(600, 400), orientation=1, time="2024:06:15 16:23:45", subsec="37",
             serial="3012345", model="NIKON Z 6_2"):
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", size, (200, 30, 30))
    # Mark the top-left corner so orientation can be checked.
    img.paste((0, 0, 255), (0, 0, 50, 50))
    exif = Image.Exif()
    exif[0x0112] = orientation
    exif[0x010F] = "NIKON CORPORATION"
    exif[0x0110] = model
    sub = exif.get_ifd(0x8769)
    if time:
        sub[0x9003] = time
    if subsec:
        sub[0x9291] = subsec
    if serial:
        sub[0xA431] = serial
    img.save(path, "JPEG", exif=exif)
    return path


def test_parse_exif_time_with_and_without_subsec():
    assert parse_exif_time("2024:06:15 16:23:45", "37") == (datetime(2024, 6, 15, 16, 23, 45, 370000), True)
    assert parse_exif_time("2024:06:15 16:23:45", "5") == (datetime(2024, 6, 15, 16, 23, 45, 500000), True)
    assert parse_exif_time("2024:06:15 16:23:45", None) == (datetime(2024, 6, 15, 16, 23, 45), False)
    assert parse_exif_time("0000:00:00 00:00:00", None) == (None, False)
    assert parse_exif_time(None, "12") == (None, False)


def test_scan_pairs_nef_and_jpg_by_folder_and_name(tmp_path):
    for name in ["a/DSC_0001.NEF", "a/DSC_0001.JPG", "a/DSC_0002.nef", "b/DSC_0001.jpg", "b/notes.txt"]:
        (tmp_path / name).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / name).write_bytes(b"x")
    sources = scan_folder(tmp_path)
    as_names = sorted(
        (Path(s["nef_path"] or s["jpg_path"]).parent.name,
         Path(s["nef_path"]).name if s["nef_path"] else "-",
         Path(s["jpg_path"]).name if s["jpg_path"] else "-")
        for s in sources
    )
    assert as_names == [
        ("a", "DSC_0001.NEF", "DSC_0001.JPG"),
        ("a", "DSC_0002.nef", "-"),
        ("b", "-", "DSC_0001.jpg"),
    ]


def test_scan_skips_macos_appledouble_files_and_output_folder(tmp_path):
    (tmp_path / "_KAD0001.NEF").write_bytes(b"real raw bytes")
    (tmp_path / "._KAD0001.NEF").write_bytes(b"\x00\x05\x16\x07" + b"\x00" * 100)
    (tmp_path / "._odd.jpg").write_bytes(b"not appledouble")  # kept: content is not AppleDouble
    (tmp_path / "out" / "previews").mkdir(parents=True)
    (tmp_path / "out" / "previews" / "abc.jpg").write_bytes(b"x")
    sources = scan_folder(tmp_path, exclude_dir=tmp_path / "out")
    names = sorted(Path(s["nef_path"] or s["jpg_path"]).name for s in sources)
    assert names == ["._odd.jpg", "_KAD0001.NEF"]


def test_process_jpg_reads_metadata_and_applies_orientation(tmp_path):
    src = make_jpg(tmp_path / "in" / "DSC_0001.JPG", orientation=6)  # rotate 90° CW
    out = tmp_path / "out"
    (out / "previews").mkdir(parents=True)
    (out / "thumbs").mkdir()
    rec = process_source({"nef_path": None, "jpg_path": str(src)}, str(out), INGEST_CFG)

    assert rec["status"] == "ok", rec["error"]
    assert rec["capture_time"] == "2024-06-15T16:23:45.370000"
    assert rec["capture_time_has_subsec"] is True
    assert rec["camera_serial"] == "3012345"
    assert rec["camera_id"] == "SN3012345"
    assert rec["orientation"] == 6
    assert (rec["preview_w"], rec["preview_h"]) == (267, 400)  # landscape became portrait
    assert (rec["original_preview_w"], rec["original_preview_h"]) == (600, 400)
    with Image.open(out / rec["preview_file"]) as p:
        # After a 90° CW rotation the blue top-left corner is at the top-right.
        r, g, b = p.convert("RGB").getpixel((p.width - 5, 5))
        assert b > 150 and r < 100
    with Image.open(out / rec["thumb_file"]) as t:
        assert max(t.size) == 100


def test_missing_serial_and_time_are_flagged(tmp_path):
    src = make_jpg(tmp_path / "x.jpg", time=None, subsec=None, serial=None)
    out = tmp_path / "out"
    (out / "previews").mkdir(parents=True)
    (out / "thumbs").mkdir()
    rec = process_source({"nef_path": None, "jpg_path": str(src)}, str(out), INGEST_CFG)
    assert rec["status"] == "ok"
    assert rec["capture_time"] is None
    assert rec["camera_id"] == "NIKON CORPORATION NIKON Z 6_2"
    assert set(rec["flags"]) == {"no_timestamp", "no_camera_serial"}


def test_broken_file_is_recorded_not_dropped(tmp_path):
    bad = tmp_path / "broken.NEF"
    bad.write_bytes(b"not a raw file")
    out = tmp_path / "out"
    (out / "previews").mkdir(parents=True)
    (out / "thumbs").mkdir()
    rec = process_source({"nef_path": str(bad), "jpg_path": None}, str(out), INGEST_CFG)
    assert rec["status"] == "error"
    assert rec["error"]
    assert rec["sha256"]  # still hashed and identifiable


def test_duplicate_content_gets_unique_ids():
    photos = [
        {"primary_path": "b.jpg", "sha256": "ab" * 32, "flags": []},
        {"primary_path": "a.jpg", "sha256": "ab" * 32, "flags": []},
        {"primary_path": "c.jpg", "sha256": None, "flags": []},
    ]
    ids = {p["primary_path"]: p["id"] for p in assign_unique_ids(photos)}
    assert ids["a.jpg"] == "ab" * 8
    assert ids["b.jpg"] == "ab" * 8 + "-dup1"
    assert ids["c.jpg"].startswith("err-")


def test_run_ingest_resumes_without_reprocessing(tmp_path):
    for i in range(3):
        make_jpg(tmp_path / "in" / f"DSC_{i:04d}.JPG", subsec=str(i))
    out = tmp_path / "out"
    config = {**DEFAULTS, "ingest": INGEST_CFG}

    first = run_ingest(tmp_path / "in", out, config)
    assert len(first) == 3 and all(p["status"] == "ok" for p in first)
    mtimes = {p["id"]: (out / p["preview_file"]).stat().st_mtime_ns for p in first}

    make_jpg(tmp_path / "in" / "DSC_0003.JPG", subsec="3")
    second = run_ingest(tmp_path / "in", out, config)
    assert len(second) == 4
    for p in second:
        if p["id"] in mtimes:
            assert (out / p["preview_file"]).stat().st_mtime_ns == mtimes[p["id"]]
    assert len(load_photos(out)) == 4
