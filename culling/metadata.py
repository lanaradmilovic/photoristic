"""Read the EXIF fields the pipeline needs (time, camera, orientation) with exifread.

exifread parses NEF (TIFF-based) and JPG headers without decoding pixels.
Capture times are naive datetimes in camera-local time: the two cameras' clocks
are not synchronized, which is why grouping is done per camera.
"""
import logging
from datetime import datetime, timedelta

import exifread

log = logging.getLogger(__name__)

EXIF_TIME_FORMAT = "%Y:%m:%d %H:%M:%S"


def _tag_str(tags, name):
    tag = tags.get(name)
    if tag is None:
        return None
    value = str(tag.printable).strip().strip("\x00").strip()
    return value or None


def _tag_int(tags, name):
    tag = tags.get(name)
    if tag is None:
        return None
    try:
        return int(tag.values[0])
    except (TypeError, ValueError, IndexError):
        return None


def parse_exif_time(value, subsec=None):
    """'2024:06:15 16:23:45' + '37' -> datetime(2024, 6, 15, 16, 23, 45, 370000).

    Returns (datetime or None, has_subsec).
    """
    if not value:
        return None, False
    try:
        dt = datetime.strptime(value.strip()[:19], EXIF_TIME_FORMAT)
    except ValueError:
        return None, False
    digits = "".join(c for c in (subsec or "") if c.isdigit())
    if not digits:
        return dt, False
    # SubSecTime is the decimal fraction of a second: "37" -> 0.37, "5" -> 0.5
    fraction = float("0." + digits)
    return dt + timedelta(microseconds=round(fraction * 1_000_000)), True


def read_metadata(path):
    """Return a dict with capture_time, camera fields and orientation for one file.

    Missing fields are None; this never raises on bad EXIF.
    """
    result = {
        "capture_time": None,
        "capture_time_has_subsec": False,
        "camera_make": None,
        "camera_model": None,
        "camera_serial": None,
        "orientation": 1,
    }
    try:
        with open(path, "rb") as f:
            # details=True is needed to parse the Nikon MakerNote (serial number).
            tags = exifread.process_file(f, details=True)
    except Exception as e:  # exifread can raise on unusual files
        log.warning("Could not read EXIF from %s: %s", path, e)
        return result

    dt, has_subsec = parse_exif_time(
        _tag_str(tags, "EXIF DateTimeOriginal"), _tag_str(tags, "EXIF SubSecTimeOriginal")
    )
    if dt is None:
        dt, has_subsec = parse_exif_time(
            _tag_str(tags, "Image DateTime"), _tag_str(tags, "EXIF SubSecTime")
        )
    result["capture_time"] = dt
    result["capture_time_has_subsec"] = has_subsec
    result["camera_make"] = _tag_str(tags, "Image Make")
    result["camera_model"] = _tag_str(tags, "Image Model")
    result["camera_serial"] = _tag_str(tags, "EXIF BodySerialNumber") or _tag_str(
        tags, "MakerNote SerialNumber"
    )
    result["orientation"] = _tag_int(tags, "Image Orientation") or 1
    return result


def merge_metadata(primary, secondary):
    """Fill fields missing in `primary` (usually the NEF) from `secondary` (the JPG)."""
    merged = dict(primary)
    for key, value in secondary.items():
        if merged.get(key) in (None, False) and value not in (None, False):
            merged[key] = value
    if primary.get("capture_time") is not None:
        # Keep time and its subsec flag from the same source.
        merged["capture_time_has_subsec"] = primary["capture_time_has_subsec"]
    return merged


def camera_id(meta):
    """Stable camera identifier: serial number if known, else make + model."""
    if meta.get("camera_serial"):
        return f"SN{meta['camera_serial']}"
    make_model = " ".join(p for p in (meta.get("camera_make"), meta.get("camera_model")) if p)
    return make_model or "unknown-camera"
