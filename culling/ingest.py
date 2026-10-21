"""Step 1 - ingest: scan a wedding folder, extract oriented previews and metadata.

Output (in the output folder):
  photos.json         one record per photo, failures included (status="error")
  previews/<id>.jpg   oriented preview, long edge = ingest.preview_long_edge
  thumbs/<id>.jpg     oriented thumbnail, long edge = ingest.thumb_long_edge

A NEF and a JPG with the same name in the same folder are one photo: the preview
comes from the JPG (falls back to the NEF's embedded JPEG), metadata from the NEF
first. RAW data is never decoded.

Resume: a record from an earlier photos.json is reused when the file's path, size
and mtime are unchanged and its preview files exist.
"""
import hashlib
import io
import json
import logging
import math
import os
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import rawpy
from PIL import Image, ImageOps
from tqdm import tqdm

from culling.metadata import camera_id, merge_metadata, read_metadata

log = logging.getLogger(__name__)

NEF_EXTS = {".nef"}
JPG_EXTS = {".jpg", ".jpeg"}

PHOTOS_FILE = "photos.json"
PREVIEW_DIR = "previews"
THUMB_DIR = "thumbs"

# PIL transpose operations for EXIF orientation values 2..8.
ORIENTATION_OPS = {
    2: [Image.Transpose.FLIP_LEFT_RIGHT],
    3: [Image.Transpose.ROTATE_180],
    4: [Image.Transpose.FLIP_TOP_BOTTOM],
    5: [Image.Transpose.TRANSPOSE],
    6: [Image.Transpose.ROTATE_270],
    7: [Image.Transpose.TRANSVERSE],
    8: [Image.Transpose.ROTATE_90],
}


# --------------------------------------------------------------------------- scan

APPLEDOUBLE_MAGIC = b"\x00\x05\x16\x07"


def is_appledouble(path):
    """macOS writes '._<name>' companion files (AppleDouble metadata, a few KB) when
    copying to non-Mac drives. They share the photo's extension but contain no image."""
    if not path.name.startswith("._"):
        return False
    with open(path, "rb") as f:
        return f.read(4) == APPLEDOUBLE_MAGIC


def scan_folder(input_dir, exclude_dir=None):
    """Find NEF/JPG files recursively and pair them by (folder, lowercase stem).

    `exclude_dir` (the output folder) is skipped in case it lies inside the input.
    Returns a list of sources: {"nef_path": str|None, "jpg_path": str|None}.
    """
    input_dir = Path(input_dir)
    exclude_dir = Path(exclude_dir).resolve() if exclude_dir else None
    pairs = defaultdict(dict)
    n_appledouble = 0
    for path in sorted(input_dir.rglob("*")):
        if not path.is_file():
            continue
        ext = path.suffix.lower()
        if ext in NEF_EXTS:
            kind = "nef_path"
        elif ext in JPG_EXTS:
            kind = "jpg_path"
        else:
            continue
        if exclude_dir and exclude_dir in path.resolve().parents:
            continue
        if is_appledouble(path):
            n_appledouble += 1
            continue
        key = (str(path.parent).lower(), path.stem.lower())
        if kind in pairs[key]:
            log.warning("Two %s files share the name %s; keeping %s, the other becomes a separate photo",
                        kind[:3].upper(), path.stem, pairs[key][kind])
            pairs[(key[0], key[1], str(path))] = {kind: str(path)}
            continue
        pairs[key][kind] = str(path)
    if n_appledouble:
        log.info("Skipped %d macOS '._' metadata files (not photos)", n_appledouble)
    return [
        {"nef_path": p.get("nef_path"), "jpg_path": p.get("jpg_path")}
        for _, p in sorted(pairs.items())
    ]


# --------------------------------------------------------------------------- per photo

def file_sha256(path):
    with open(path, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def _draft_and_load(img, long_edge):
    """Let the JPEG decoder downscale by 1/2, 1/4 or 1/8 while staying >= long_edge."""
    w, h = img.size
    if img.format == "JPEG" and max(w, h) > long_edge:
        scale = long_edge / max(w, h)
        img.draft("RGB", (math.ceil(w * scale), math.ceil(h * scale)))
    img.load()
    return img


def _apply_orientation(img, orientation):
    for op in ORIENTATION_OPS.get(orientation or 1, []):
        img = img.transpose(op)
    return img


def load_jpg_preview(jpg_path, long_edge):
    """Open a JPG and orient it by its own EXIF. Returns (image, original_size, orientation)."""
    img = Image.open(jpg_path)
    original_size = img.size
    orientation = img.getexif().get(0x0112, 1)
    img = _draft_and_load(img, long_edge)
    img = ImageOps.exif_transpose(img)
    return img, original_size, orientation


def load_nef_preview(nef_path, orientation, long_edge):
    """Extract the NEF's embedded preview (no RAW decoding), oriented by the NEF's EXIF.

    The embedded JPEG's own orientation tag is ignored; Nikon stores the rotation
    in the NEF's IFD0.
    """
    with rawpy.imread(nef_path) as raw:
        thumb = raw.extract_thumb()
    if thumb.format == rawpy.ThumbFormat.JPEG:
        img = Image.open(io.BytesIO(thumb.data))
        original_size = img.size
        img = _draft_and_load(img, long_edge)
    elif thumb.format == rawpy.ThumbFormat.BITMAP:
        img = Image.fromarray(thumb.data)
        original_size = img.size
    else:
        raise ValueError(f"Unsupported embedded preview format: {thumb.format}")
    return _apply_orientation(img, orientation), original_size


def _save_jpeg(img, path, quality):
    """Write via a temp file and rename, so an interrupted run never leaves a half file."""
    tmp = path.with_suffix(".tmp")
    img.save(tmp, "JPEG", quality=quality, optimize=True)
    os.replace(tmp, path)


def _resized(img, long_edge):
    img = img.copy()
    img.thumbnail((long_edge, long_edge), Image.Resampling.LANCZOS)
    return img


def process_source(source, out_dir, ingest_cfg):
    """Hash, read metadata and write preview + thumb for one photo. Never raises."""
    nef_path, jpg_path = source["nef_path"], source["jpg_path"]
    primary = nef_path or jpg_path
    record = {
        "id": None,
        "sha256": None,
        "primary_path": primary,
        "nef_path": nef_path,
        "jpg_path": jpg_path,
        "preview_source": None,
        "preview_file": None,
        "thumb_file": None,
        "capture_time": None,
        "capture_time_has_subsec": False,
        "camera_id": None,
        "camera_serial": None,
        "camera_make": None,
        "camera_model": None,
        "orientation": None,
        "preview_w": None,
        "preview_h": None,
        "original_preview_w": None,
        "original_preview_h": None,
        "file_size": None,
        "mtime_ns": None,
        "status": "ok",
        "error": None,
        "flags": [],
    }
    try:
        stat = os.stat(primary)
        record["file_size"] = stat.st_size
        record["mtime_ns"] = stat.st_mtime_ns
        record["sha256"] = file_sha256(primary)
        record["id"] = record["sha256"][:16]

        nef_meta = read_metadata(nef_path) if nef_path else None
        jpg_meta = read_metadata(jpg_path) if jpg_path else None
        if nef_meta and jpg_meta:
            meta = merge_metadata(nef_meta, jpg_meta)
        else:
            meta = nef_meta or jpg_meta
        record["capture_time"] = meta["capture_time"].isoformat() if meta["capture_time"] else None
        record["capture_time_has_subsec"] = meta["capture_time_has_subsec"]
        for key in ("camera_serial", "camera_make", "camera_model"):
            record[key] = meta[key]
        record["camera_id"] = camera_id(meta)
        if not meta["capture_time"]:
            record["flags"].append("no_timestamp")
        if not meta["camera_serial"]:
            record["flags"].append("no_camera_serial")

        long_edge = ingest_cfg["preview_long_edge"]
        img, errors = None, []
        if jpg_path:
            try:
                img, original_size, orientation = load_jpg_preview(jpg_path, long_edge)
                record["preview_source"] = "jpg"
            except Exception as e:
                errors.append(f"jpg preview: {e}")
        if img is None and nef_path:
            try:
                orientation = nef_meta["orientation"]
                img, original_size = load_nef_preview(nef_path, orientation, long_edge)
                record["preview_source"] = "nef_embedded"
            except Exception as e:
                errors.append(f"nef preview: {type(e).__name__}: {e}")
        if img is None:
            raise RuntimeError("; ".join(errors) or "no preview source")
        if errors:
            record["flags"].append("preview_fallback")

        img = img.convert("RGB")
        preview = _resized(img, long_edge)
        thumb = _resized(preview, ingest_cfg["thumb_long_edge"])
        out_dir = Path(out_dir)
        record["preview_file"] = f"{PREVIEW_DIR}/{record['id']}.jpg"
        record["thumb_file"] = f"{THUMB_DIR}/{record['id']}.jpg"
        _save_jpeg(preview, out_dir / record["preview_file"], ingest_cfg["jpeg_quality"])
        _save_jpeg(thumb, out_dir / record["thumb_file"], ingest_cfg["jpeg_quality"])
        record["orientation"] = orientation
        record["preview_w"], record["preview_h"] = preview.size
        record["original_preview_w"], record["original_preview_h"] = original_size
    except Exception as e:
        record["status"] = "error"
        record["error"] = f"{type(e).__name__}: {e}"
    return record


# --------------------------------------------------------------------------- photos.json

def read_photos_file(out_dir):
    """Return the whole photos.json dict ({created, input_dir, photos}), or None."""
    path = Path(out_dir) / PHOTOS_FILE
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_photos(out_dir):
    data = read_photos_file(out_dir)
    return data["photos"] if data else []


def save_photos(out_dir, photos, input_dir=None):
    path = Path(out_dir) / PHOTOS_FILE
    tmp = path.with_suffix(".tmp")
    data = {
        "created": datetime.now().isoformat(timespec="seconds"),
        "input_dir": str(input_dir) if input_dir else None,
        "photos": photos,
    }
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    os.replace(tmp, path)


def _reusable(record, out_dir):
    """True if an earlier record still matches the file on disk and its outputs exist."""
    if record.get("status") != "ok":
        return False  # always retry failures
    try:
        stat = os.stat(record["primary_path"])
    except OSError:
        return False
    return (
        stat.st_size == record["file_size"]
        and stat.st_mtime_ns == record["mtime_ns"]
        and (Path(out_dir) / record["preview_file"]).exists()
        and (Path(out_dir) / record["thumb_file"]).exists()
    )


def assign_unique_ids(photos):
    """id = first 16 hex chars of sha256; byte-identical copies get a '-dupN' suffix.

    Copies share the same preview files (same content) but stay separate photos,
    so nothing disappears from the pipeline.
    """
    photos.sort(key=lambda p: p["primary_path"])
    seen = defaultdict(int)
    for p in photos:
        p["flags"] = [f for f in p["flags"] if f != "duplicate_file"]
        if not p.get("sha256"):
            # Hashing failed: derive a stable id from the path.
            p["id"] = "err-" + hashlib.sha256(p["primary_path"].encode()).hexdigest()[:12]
            continue
        base = p["sha256"][:16]
        seen[base] += 1
        if seen[base] == 1:
            p["id"] = base
        else:
            p["id"] = f"{base}-dup{seen[base] - 1}"
            p["flags"].append("duplicate_file")
            log.warning("Duplicate file content: %s", p["primary_path"])
    return photos


def run_ingest(input_dir, out_dir, config):
    input_dir, out_dir = Path(input_dir), Path(out_dir)
    if not input_dir.is_dir():
        raise FileNotFoundError(f"Input folder not found: {input_dir}")
    (out_dir / PREVIEW_DIR).mkdir(parents=True, exist_ok=True)
    (out_dir / THUMB_DIR).mkdir(parents=True, exist_ok=True)
    ingest_cfg = config["ingest"]

    sources = scan_folder(input_dir, exclude_dir=out_dir)
    n_nef = sum(1 for s in sources if s["nef_path"])
    n_jpg = sum(1 for s in sources if s["jpg_path"])
    n_pairs = sum(1 for s in sources if s["nef_path"] and s["jpg_path"])
    log.info("Found %d photos (%d with NEF, %d with JPG, %d NEF+JPG pairs) in %s",
             len(sources), n_nef, n_jpg, n_pairs, input_dir)

    previous = {p["primary_path"]: p for p in load_photos(out_dir)}
    done, todo = [], []
    for source in sources:
        primary = source["nef_path"] or source["jpg_path"]
        old = previous.get(primary)
        if old and old.get("jpg_path") == source["jpg_path"] and _reusable(old, out_dir):
            done.append(old)
        else:
            todo.append(source)
    log.info("Reusing %d photos from a previous run, processing %d", len(done), len(todo))

    if todo:
        workers = max(1, int(ingest_cfg["workers"]))
        with ProcessPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(process_source, s, str(out_dir), ingest_cfg) for s in todo]
            for i, future in enumerate(tqdm(as_completed(futures), total=len(futures),
                                            desc="Ingest", unit="photo"), start=1):
                record = future.result()
                if record["status"] == "error":
                    log.error("Failed: %s (%s)", record["primary_path"], record["error"])
                done.append(record)
                if i % ingest_cfg["save_every"] == 0:
                    save_photos(out_dir, done, input_dir)

    photos = assign_unique_ids(done)
    save_photos(out_dir, photos, input_dir)

    n_err = sum(1 for p in photos if p["status"] == "error")
    cameras = defaultdict(int)
    for p in photos:
        cameras[p["camera_id"]] += 1
    log.info("Ingest done: %d photos, %d failed, cameras: %s", len(photos), n_err, dict(cameras))
    no_serial = sorted({p["camera_id"] for p in photos
                        if p["status"] == "ok" and "no_camera_serial" in p["flags"]})
    if no_serial:
        log.warning("No serial number for camera(s) %s - photographers using the same model "
                    "would be merged into one camera", no_serial)
    return photos
