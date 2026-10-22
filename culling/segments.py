"""Day segmentation: cut a wedding into parts of the day at pauses in shooting.

Why: a wedding is not one continuous session. Preparations, family formals, the
church, the couple session, the garden, speeches, the first dance and the party are
shot in very different rhythms (single frames 5-40 s apart vs. bursts), and one set
of grouping thresholds cannot fit them all. Before grouping can use per-segment
profiles, and before a VLM can label what each part of the day is, the pipeline has
to know where the parts are. This step is deterministic and needs no model.

Per camera (the two bodies' clocks are not synchronised), photos are sorted by
capture time and a new segment starts wherever the gap between two neighbours is
longer than `segments.gap_seconds`. Photos without a capture time (or that failed
ingest) go to one "unknown" segment. Per segment, simple statistics describe the
rhythm (median / 90th percentile gap, share of burst gaps), the content (share of
photos without people, faces per photo, the known identities present, portrait
share) and how the grouping relates to it (groups inside, groups crossing a
boundary - which should never happen because grouping never joins across such a
gap). Segments with fewer than `segments.min_photos` photos are only flagged
"tiny", never merged.

Output: segments.json, and with --sheets one contact sheet per segment in
segments_sheets/ (up to `sheet_max_thumbs` thumbnails sampled evenly in time).
"""
import json
import logging
import os
from collections import Counter
from datetime import datetime
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from culling.faces import known_identities, load_identities
from culling.grouping import GROUPS_FILE, _sort_key, _time, load_groups
from culling.people import PEOPLE_FILE

log = logging.getLogger(__name__)

SEGMENTS_FILE = "segments.json"
SHEETS_DIR = "segments_sheets"
UNKNOWN_ID = "unknown"
BURST_GAP_SECONDS = 2.0  # a gap shorter than this counts as "burst" shooting


# ------------------------------------------------------------------ segmentation

def segment_photos(photos, gap_seconds, min_photos=5):
    """Cut the photos of each camera into segments at gaps longer than `gap_seconds`.

    Returns a list of segments in camera order, then time order: {segment_id ("S01"...),
    camera_id, start, end, duration_seconds, n_photos, photo_ids, flags}. Photos without
    a capture time or with status != "ok" form one trailing segment with segment_id
    "unknown" (camera_id None, no times) and a `reasons` list parallel to photo_ids;
    it is omitted when there are none. `flags` contains "tiny" for segments with fewer
    than `min_photos` photos. Statistics are added by `segment_stats` / `build_segments`.
    """
    by_camera, unknown = {}, []
    for p in photos:
        if p.get("status") != "ok":
            unknown.append((p, "ingest_error"))
        elif not p.get("capture_time"):
            unknown.append((p, "no_timestamp"))
        else:
            by_camera.setdefault(p.get("camera_id") or "unknown-camera", []).append(p)

    runs = []
    for camera_id in sorted(by_camera):
        ordered = sorted(by_camera[camera_id], key=_sort_key)
        current = [ordered[0]]
        for prev, photo in zip(ordered, ordered[1:]):
            if (_time(photo) - _time(prev)).total_seconds() > gap_seconds:
                runs.append((camera_id, current))
                current = []
            current.append(photo)
        runs.append((camera_id, current))

    segments = []
    for i, (camera_id, members) in enumerate(runs, start=1):
        start, end = _time(members[0]), _time(members[-1])
        segments.append({
            "segment_id": f"S{i:02d}",
            "camera_id": camera_id,
            "start": members[0]["capture_time"],
            "end": members[-1]["capture_time"],
            "duration_seconds": round((end - start).total_seconds(), 2),
            "n_photos": len(members),
            "photo_ids": [p["id"] for p in members],
            "flags": ["tiny"] if len(members) < min_photos else [],
        })
    if unknown:
        unknown.sort(key=lambda item: item[0]["primary_path"])
        segments.append({
            "segment_id": UNKNOWN_ID,
            "camera_id": None,
            "start": None, "end": None, "duration_seconds": None,
            "n_photos": len(unknown),
            "photo_ids": [p["id"] for p, _ in unknown],
            "reasons": [reason for _, reason in unknown],
            "flags": ["unknown"] + (["tiny"] if len(unknown) < min_photos else []),
        })
    return segments


# ------------------------------------------------------------------ statistics

def load_people(out_dir):
    """{sha256: has_people} from people.json, or {} when the file is missing."""
    path = Path(out_dir) / PEOPLE_FILE
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f).get("has_people", {})


def _share(hits, total):
    return round(hits / total, 3) if total else None


def segment_stats(members, people=None, identities=None):
    """Statistics for the photos of one segment (records in time order).

    `people` is {sha256: bool} (people.json) or empty; `identities` the content of
    identities.json or None. Fields that cannot be computed are None, never missing.
    """
    timed = [p for p in members if p.get("capture_time")]
    gaps = [(_time(b) - _time(a)).total_seconds() for a, b in zip(timed, timed[1:])]
    stats = {
        "median_gap_s": round(float(np.median(gaps)), 2) if gaps else None,
        "p90_gap_s": round(float(np.percentile(gaps, 90)), 2) if gaps else None,
        "burst_share": _share(sum(1 for g in gaps if g < BURST_GAP_SECONDS), len(gaps)),
        "no_people_share": None,
        "median_faces": None,
        "identities": [],
        "portrait_share": None,
        "n_groups": None,
        "n_groups_crossing": None,
    }
    people = people or {}
    known = [people[p["sha256"]] for p in members if p.get("sha256") in people]
    stats["no_people_share"] = _share(sum(1 for has in known if not has), len(known))

    if identities:
        min_faces = identities.get("min_identity_faces", 1)
        trusted = known_identities(identities, min_faces)
        infos = [identities["photos"][p["sha256"]] for p in members
                 if p.get("sha256") in identities["photos"]]
        if infos:
            stats["median_faces"] = float(np.median([info["n_faces"] for info in infos]))
            counts = Counter(label for info in infos for label in info["ids"] if label in trusted)
            stats["identities"] = [[label, n] for label, n in
                                   sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:10]]

    sized = [p for p in members if p.get("preview_w") and p.get("preview_h")]
    stats["portrait_share"] = _share(sum(1 for p in sized if p["preview_h"] > p["preview_w"]), len(sized))
    return stats


def attach_groups(segments, groups_data):
    """Add `group_ids` (groups whose first photo lies in the segment, in groups.json
    order) and stats.n_groups / stats.n_groups_crossing to every segment. A crossing
    group has photos in more than one segment; grouping never joins across a gap
    longer than its own limits, so with a sensible gap this is zero. Returns the list
    of crossing group ids."""
    seg_of_photo = {pid: seg["segment_id"] for seg in segments for pid in seg["photo_ids"]}
    by_id = {seg["segment_id"]: seg for seg in segments}
    for seg in segments:
        seg["group_ids"] = []
        seg["stats"]["n_groups"] = 0
        seg["stats"]["n_groups_crossing"] = 0
    crossing = []
    for g in groups_data["groups"]:
        touched = {seg_of_photo[pid] for pid in g["photo_ids"] if pid in seg_of_photo}
        if not touched:
            continue
        home = seg_of_photo.get(g["photo_ids"][0]) or sorted(touched)[0]
        by_id[home]["group_ids"].append(g["group_id"])
        if len(touched) == 1:
            by_id[home]["stats"]["n_groups"] += 1
        else:
            crossing.append(g["group_id"])
            for sid in touched:
                by_id[sid]["stats"]["n_groups_crossing"] += 1
    if crossing:
        log.warning("%d group(s) cross a segment boundary: %s", len(crossing), ", ".join(crossing))
    return crossing


def build_segments(photos, cfg, people=None, identities=None, groups_data=None):
    """Segment + statistics + group counts. `cfg` is config["segments"]. Returns the
    content of segments.json."""
    segments = segment_photos(photos, cfg["gap_seconds"], cfg["min_photos"])
    by_id = {p["id"]: p for p in photos}
    for seg in segments:
        seg["stats"] = segment_stats([by_id[pid] for pid in seg["photo_ids"]], people, identities)
    crossing = attach_groups(segments, groups_data) if groups_data else []
    if not groups_data:
        for seg in segments:
            seg["group_ids"] = []
    return {
        "created": datetime.now().isoformat(timespec="seconds"),
        "gap_seconds": cfg["gap_seconds"],
        "min_photos": cfg["min_photos"],
        "n_segments": sum(1 for s in segments if s["segment_id"] != UNKNOWN_ID),
        "n_tiny": sum(1 for s in segments if "tiny" in s["flags"]),
        "n_unknown_photos": sum(s["n_photos"] for s in segments if s["segment_id"] == UNKNOWN_ID),
        "groups_crossing": crossing,
        "segments": segments,
    }


# ------------------------------------------------------------------ I/O + log

def save_segments(out_dir, data):
    path = Path(out_dir) / SEGMENTS_FILE
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    os.replace(tmp, path)
    return path


def load_segments(out_dir):
    path = Path(out_dir) / SEGMENTS_FILE
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _clock(iso):
    return datetime.fromisoformat(iso).strftime("%H:%M:%S") if iso else "--:--:--"


def _pct(share):
    return f"{100 * share:.0f}%" if share is not None else "n/a"


def _num(value, spec=".1f"):
    return format(value, spec) if value is not None else "n/a"


def identities_text(stats, limit=5):
    return ", ".join(f"{label} {n}" for label, n in stats["identities"][:limit]) or "-"


def format_table(data):
    """Readable summary of segments.json for the log / console."""
    rows = [("seg", "camera", "from", "to", "min", "n", "med gap", "p90", "burst", "no ppl", "faces",
             "groups", "identities", "flags")]
    for seg in data["segments"]:
        st = seg["stats"]
        rows.append((
            seg["segment_id"], str(seg["camera_id"] or "-"), _clock(seg["start"]), _clock(seg["end"]),
            _num(seg["duration_seconds"] / 60 if seg["duration_seconds"] is not None else None),
            str(seg["n_photos"]), _num(st["median_gap_s"]), _num(st["p90_gap_s"]),
            _pct(st["burst_share"]), _pct(st["no_people_share"]), _num(st["median_faces"]),
            str(st["n_groups"]) if st["n_groups"] is not None else "n/a",
            identities_text(st), ",".join(seg["flags"]) or "-",
        ))
    widths = [max(len(r[i]) for r in rows) for i in range(len(rows[0]))]
    lines = ["  ".join(cell.ljust(w) for cell, w in zip(row, widths)).rstrip() for row in rows]
    lines.append(f"{data['n_segments']} segments ({data['n_tiny']} tiny) at gap > {data['gap_seconds']} s"
                 + (f"; {data['n_unknown_photos']} photos without time" if data["n_unknown_photos"] else "")
                 + (f"; GROUPS CROSSING A BOUNDARY: {', '.join(data['groups_crossing'])}"
                    if data["groups_crossing"] else ""))
    return "\n".join(lines)


# ------------------------------------------------------------------ contact sheets

def _font(size):
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # older Pillow
        return ImageFont.load_default()


def _thumb(out_dir, rel, edge):
    """Thumbnail fitted into an edge x edge white square; grey when missing."""
    if not rel or not (out_dir / rel).exists():
        return Image.new("RGB", (edge, edge), (200, 200, 200))
    with Image.open(out_dir / rel) as img:
        img = img.convert("RGB")
        img.thumbnail((edge, edge))
        canvas = Image.new("RGB", (edge, edge), "white")
        canvas.paste(img, ((edge - img.width) // 2, (edge - img.height) // 2))
    return canvas


def sample_evenly(items, n):
    """Up to n items spread evenly over the list, order kept."""
    if len(items) <= n:
        return list(items)
    idx = sorted(set(int(round(x)) for x in np.linspace(0, len(items) - 1, n)))
    return [items[i] for i in idx]


def write_segment_sheets(out_dir, photos, data, max_thumbs=48, cols=8, edge=160):
    """One contact sheet per segment in <out>/segments_sheets/<segment_id>.jpg: a header
    with the segment's key facts and up to `max_thumbs` thumbnails sampled evenly through
    the segment in time order, each captioned with the last four digits of the file name
    and the clock time. For review by eye only."""
    out_dir = Path(out_dir)
    sheets_dir = out_dir / SHEETS_DIR
    sheets_dir.mkdir(exist_ok=True)
    for old in sheets_dir.glob("*.jpg"):
        old.unlink()
    by_id = {p["id"]: p for p in photos}
    header_font, cap_font = _font(16), _font(12)
    head_h, cap_h = 48, 16
    cell_w, cell_h = edge + 8, edge + cap_h + 6

    for seg in data["segments"]:
        members = [by_id[pid] for pid in seg["photo_ids"] if pid in by_id]
        shown = sample_evenly(members, max_thumbs)
        st = seg["stats"]
        rows = max(1, -(-len(shown) // cols))
        canvas = Image.new("RGB", (cols * cell_w + 8, head_h + rows * cell_h), "white")
        draw = ImageDraw.Draw(canvas)
        title = (f"{seg['segment_id']} · {seg['camera_id'] or 'no camera'} · "
                 f"{_clock(seg['start'])} - {_clock(seg['end'])} · {seg['n_photos']} photos")
        if len(shown) < len(members):
            title += f" ({len(shown)} shown)"
        if seg["flags"]:
            title += " · " + ", ".join(seg["flags"])
        detail = (f"median gap {_num(st['median_gap_s'])} s · burst {_pct(st['burst_share'])} · "
                  f"no people {_pct(st['no_people_share'])} · faces/photo {_num(st['median_faces'])} · "
                  f"groups {st['n_groups'] if st['n_groups'] is not None else 'n/a'} · "
                  f"identities: {identities_text(st, 8)}")
        draw.text((6, 4), title, fill="black", font=header_font)
        draw.text((6, 26), detail, fill=(60, 60, 60), font=cap_font)
        for k, photo in enumerate(shown):
            x, y = 4 + (k % cols) * cell_w, head_h + (k // cols) * cell_h
            canvas.paste(_thumb(out_dir, photo.get("thumb_file"), edge), (x, y))
            caption = f"{Path(photo['primary_path']).stem[-4:]} {_clock(photo.get('capture_time'))}"
            draw.text((x + 2, y + edge + 1), caption, fill="black", font=cap_font)
        canvas.save(sheets_dir / f"{seg['segment_id']}.jpg", "JPEG", quality=85)
    log.info("Segment sheets: %s", sheets_dir)
    return sheets_dir


# ------------------------------------------------------------------ entry point

def run_segments(out_dir, config, photos=None, sheets=False):
    """Segment the wedding in `out_dir`, write segments.json, log the table and
    optionally the sheets. people.json, identities.json and groups.json are used
    when present. Returns the segments data."""
    from culling.ingest import load_photos

    out_dir = Path(out_dir)
    cfg = config["segments"]
    if photos is None:
        photos = load_photos(out_dir)
    people = load_people(out_dir)
    identities = load_identities(out_dir)
    groups_data = load_groups(out_dir) if (out_dir / GROUPS_FILE).exists() else None
    data = build_segments(photos, cfg, people, identities, groups_data)
    path = save_segments(out_dir, data)
    log.info("Segments (gap > %s s, people %s, identities %s, groups %s):\n%s",
             cfg["gap_seconds"], "yes" if people else "no", "yes" if identities else "no",
             "yes" if groups_data else "no", format_table(data))
    log.info("Segments written: %s", path)
    if sheets:
        write_segment_sheets(out_dir, photos, data, max_thumbs=cfg["sheet_max_thumbs"])
    return data
