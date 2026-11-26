"""One wedding's "before and after" analysis in a fixed shape, so weddings can be compared.

Inputs: the pipeline output folder (photos.json, groups.json, segments.json, people.json,
identities.json, embeddings.npz, agency_cull.json from `cull.py agency`), the wedding's
hand-written facts `wedding.json` (camera roles, clock offsets, parts of the day, the couple's
face identities), and optionally the reviewers' reasons `<out>/analysis/reasons.jsonl`.

Outputs: `<out>/analysis/photos.csv` (one row per photo, the same columns for every wedding;
stays next to the photos, outside git) and `summary.json` next to wedding.json (numbers with
the same keys for every wedding; no image content, only file names). Format:
docs/spec/wedding-analysis.md.
"""
import bisect
import csv
import json
import logging
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

from culling.agency import CULL_FILE
from culling.embed import EMBEDDINGS_FILE
from culling.faces import load_identities
from culling.grouping import GROUPS_FILE, load_groups
from culling.ingest import load_photos
from culling.segments import load_people, load_segments

log = logging.getLogger(__name__)

SCHEMA_VERSION = 1
WEDDING_FILE = "wedding.json"
SUMMARY_FILE = "summary.json"
ANALYSIS_DIR = "analysis"
PHOTOS_CSV = "photos.csv"
REASONS_FILE = "reasons.jsonl"

ROLES = ("main", "second", "decor", "guests", "other")
DAY_PARTS = ("prep", "church", "civil", "formals", "couple", "arrival", "reception_line",
             "first_dance", "cake", "party", "other")
DECIDED = ("kept", "rejected")

CSV_COLUMNS = [
    "file", "photo_id", "camera", "role", "time_camera", "time_ref", "day_part",
    "decision", "group_id", "group_size", "segment_id", "has_people", "n_faces", "couple",
    "prev_gap_s", "prev_sim", "burst_id", "burst_size", "burst_pos",
    "reason", "reason2", "kept_alt", "loss", "conf", "reviewer", "codebook", "note",
]


# ------------------------------------------------------------------ wedding.json

def load_wedding(wedding_dir):
    """wedding.json, checked: known roles and parts of the day, HH:MM times."""
    path = Path(wedding_dir) / WEDDING_FILE
    with open(path, encoding="utf-8") as f:
        w = json.load(f)
    for key in ("wedding", "cameras", "day_parts"):
        if key not in w:
            raise ValueError(f"{path}: '{key}' is missing")
    for cam in w["cameras"]:
        if cam.get("role") not in ROLES:
            raise ValueError(f"{path}: camera {cam.get('prefix')}: role must be one of {ROLES}")
    for part in w["day_parts"]:
        if part.get("part") not in DAY_PARTS:
            raise ValueError(f"{path}: day part '{part.get('part')}' must be one of {DAY_PARTS}")
        _minutes(part["start"]), _minutes(part["end"])
    return w


def _minutes(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def camera_of(file_name, cameras):
    """The camera whose prefix starts the file name (longest prefix wins), or None."""
    hits = [c for c in cameras if file_name.upper().startswith(c["prefix"].upper())]
    return max(hits, key=lambda c: len(c["prefix"])) if hits else None


def day_part(ref_time, camera_prefix, parts):
    """First part (in file order) whose start <= time < end and that names this camera or no camera."""
    minute = ref_time.hour * 60 + ref_time.minute
    for p in parts:
        if p.get("cameras") and camera_prefix not in p["cameras"]:
            continue
        if _minutes(p["start"]) <= minute < _minutes(p["end"]):
            return p["part"]
    return "other"


# ------------------------------------------------------------------ rows

def load_reasons(path):
    """{file name lower case: reason row} from reasons.jsonl, or {}."""
    path = Path(path)
    if not path.exists():
        return {}
    out = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                out[row["file"].lower()] = row
    return out


def _load_embeddings(out_dir):
    path = Path(out_dir) / EMBEDDINGS_FILE
    if not path.exists():
        return {}
    data = np.load(path, allow_pickle=False)
    return dict(zip(data["keys"].tolist(), data["vectors"]))


def build_rows(out_dir, wedding, params):
    """One dict per photo with a capture time, ordered by camera and time."""
    out_dir = Path(out_dir)
    cull_path = out_dir / CULL_FILE
    if not cull_path.exists():
        raise FileNotFoundError(f"No {CULL_FILE} in {out_dir}: run 'cull.py agency --after ...' first")
    cull = json.loads(cull_path.read_text(encoding="utf-8"))["photos"]
    groups = load_groups(out_dir)["groups"] if (out_dir / GROUPS_FILE).exists() else []
    group_of = {pid: (g["group_id"], g["size"]) for g in groups for pid in g["photo_ids"]}
    segs = (load_segments(out_dir) or {}).get("segments", [])
    seg_of = {pid: s["segment_id"] for s in segs for pid in s["photo_ids"]}
    people = load_people(out_dir)
    ident = (load_identities(out_dir) or {}).get("photos", {})
    couple_ids = set(wedding.get("couple_identities") or [])
    vectors = _load_embeddings(out_dir)
    reasons = load_reasons(out_dir / ANALYSIS_DIR / REASONS_FILE)

    rows = []
    for p in load_photos(out_dir):
        if p.get("status") != "ok" or not p.get("capture_time"):
            continue
        name = Path(p["primary_path"]).name
        cam = camera_of(name, wedding["cameras"])
        t = datetime.fromisoformat(p["capture_time"])
        tref = t + timedelta(seconds=(cam or {}).get("clock_offset_s", 0))
        prefix = cam["prefix"] if cam else p.get("camera_id", "")
        faces = ident.get(p.get("sha256"), {})
        gid, gsize = group_of.get(p["id"], ("", ""))
        r = reasons.get(name.lower(), {})
        rows.append({
            "file": name, "photo_id": p["id"], "camera": prefix,
            "role": cam["role"] if cam else "other",
            "time_camera": t.isoformat(timespec="milliseconds"),
            "time_ref": tref.isoformat(timespec="milliseconds"),
            "day_part": day_part(tref, prefix, wedding["day_parts"]),
            "decision": cull.get(p["id"], {}).get("decision", "unknown"),
            "group_id": gid, "group_size": gsize, "segment_id": seg_of.get(p["id"], ""),
            "has_people": "" if p.get("sha256") not in people else int(bool(people[p["sha256"]])),
            "n_faces": faces.get("n_faces", ""),
            "couple": len(couple_ids & set(faces.get("ids", []))) if couple_ids and ident else "",
            "reason": r.get("primary", ""), "reason2": r.get("secondary", ""),
            "kept_alt": r.get("kept_alt", ""), "loss": r.get("loss", ""), "conf": r.get("conf", ""),
            "reviewer": r.get("reviewer", ""), "codebook": r.get("codebook", ""), "note": r.get("note", ""),
            "_t": t, "_tref": tref, "_vec": vectors.get(p.get("sha256")),
        })
    rows.sort(key=lambda r: (r["camera"], r["_t"], r["file"]))
    _add_neighbours_and_bursts(rows, params)
    return rows


def _add_neighbours_and_bursts(rows, params):
    """Gap and similarity to the previous frame of the same camera; bursts are chains of
    neighbours within burst_gap_seconds and at least burst_similarity."""
    prev, n = None, 0
    bursts = []
    for r in rows:
        r["prev_gap_s"] = r["prev_sim"] = ""
        joined = False
        if prev is not None and prev["camera"] == r["camera"]:
            gap = (r["_t"] - prev["_t"]).total_seconds()
            r["prev_gap_s"] = round(gap, 2)
            if r["_vec"] is not None and prev["_vec"] is not None:
                sim = float(np.dot(r["_vec"], prev["_vec"]))
                r["prev_sim"] = round(sim, 4)
                joined = gap <= params["burst_gap_seconds"] and sim >= params["burst_similarity"]
        if joined:
            bursts[-1].append(r)
        else:
            bursts.append([r])
        prev = r
    for members in bursts:
        n += 1
        for k, r in enumerate(members):
            r["burst_id"] = f"b{n:05d}"
            r["burst_size"] = len(members)
            r["burst_pos"] = k


def write_csv(rows, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


# ------------------------------------------------------------------ summary

def _rate(rows):
    decided = [r for r in rows if r["decision"] in DECIDED]
    rej = sum(r["decision"] == "rejected" for r in decided)
    return {"photos": len(decided), "rejected": rej,
            "rate": round(rej / len(decided), 3) if decided else None}


def _by(rows, key):
    out = defaultdict(list)
    for r in rows:
        out[key(r)].append(r)
    return {k: _rate(v) for k, v in sorted(out.items())}


def _bursts(rows):
    out = defaultdict(list)
    for r in rows:
        out[r["burst_id"]].append(r)
    return list(out.values())


def score_rule(rows, keep):
    """A thinning rule against the agency: `keep(burst)` returns the frames it keeps.
    drops_agency_kept are the false rejects (the failure that must not happen)."""
    drops = []
    for b in _bursts(rows):
        if all(r["decision"] in DECIDED for r in b):
            kept = {id(r) for r in keep(b)}
            drops += [r for r in b if id(r) not in kept]
    rejects = sum(r["decision"] == "rejected" for r in rows)
    caught = sum(r["decision"] == "rejected" for r in drops)
    return {"drops": len(drops), "drops_agency_kept": len(drops) - caught,
            "drops_agency_kept_share": round((len(drops) - caught) / len(drops), 3) if drops else None,
            "agency_rejects_caught": caught,
            "agency_rejects_caught_share": round(caught / rejects, 3) if rejects else None}


RULES = {
    "burst_keep_first": lambda b: b[:1],
    "burst_keep_half": lambda b: b[::2],                 # every other frame, from the first: ceil(n/2)
}


def summarize(rows, wedding, params, cull_source=None):
    decided = [r for r in rows if r["decision"] in DECIDED]
    counts = Counter(r["decision"] for r in rows)

    # Adjacent near-identical pairs: does the agency keep both?
    pairs = Counter()
    for a, b in zip(rows, rows[1:]):
        if a["burst_id"] == b["burst_id"] and a["decision"] in DECIDED and b["decision"] in DECIDED:
            pairs[sum(x["decision"] == "rejected" for x in (a, b))] += 1
    n_pairs = sum(pairs.values())

    burst_stats = {}
    for label, lo, hi in (("2", 2, 2), ("3-4", 3, 4), ("5+", 5, 10**6)):
        bs = [b for b in _bursts(decided) if lo <= len(b) <= hi]
        frames = sum(len(b) for b in bs)
        kept = sum(r["decision"] == "kept" for b in bs for r in b)
        burst_stats[label] = {"bursts": len(bs), "frames": frames,
                              "kept_share": round(kept / frames, 3) if frames else None,
                              "none_kept": sum(all(r["decision"] == "rejected" for r in b) for b in bs)}

    summary = {
        "schema": SCHEMA_VERSION,
        "wedding": wedding["wedding"],
        "created": datetime.now().isoformat(timespec="seconds"),
        "cull_source": cull_source,
        "params": dict(params),
        "counts": {"photos": len(rows), **{k: counts.get(k, 0) for k in
                   ("kept", "rejected", "both", "missing", "ambiguous", "unknown")}},
        "reject_rate": _rate(rows)["rate"],
        "by_role": _by(rows, lambda r: r["role"]),
        "by_day_part": _by(rows, lambda r: r["day_part"]),
        "by_role_day_part": _by(rows, lambda r: f'{r["role"]}/{r["day_part"]}'),
        "near_identical_pairs": {
            "pairs": n_pairs, "both_kept": pairs[0], "one_rejected": pairs[1], "both_rejected": pairs[2],
            "both_kept_share": round(pairs[0] / n_pairs, 3) if n_pairs else None},
        "bursts_by_size": burst_stats,
        "lone_frames": _rate([r for r in rows if r["burst_size"] == 1]),
        "rules": {name: score_rule(rows, keep) for name, keep in RULES.items()},
    }
    if wedding.get("couple_identities"):
        summary["couple_in_frame"] = _by([r for r in rows if r["couple"] != ""],
                                         lambda r: str(r["couple"]))
    summary["cross_camera"] = _cross_camera(rows, params["cross_camera_seconds"])
    summary["reasons"] = _reasons(rows)
    return summary


def _cross_camera(rows, window):
    """Rejection rate of other roles' frames when the main camera shot within `window` s, and when not."""
    main_times = sorted(r["_tref"].timestamp() for r in rows if r["role"] == "main")
    if not main_times:
        return {}

    def near_main(r):
        t = r["_tref"].timestamp()
        i = bisect.bisect_left(main_times, t - window)
        return i < len(main_times) and main_times[i] <= t + window

    out = {}
    for role in ROLES:
        rs = [r for r in rows if r["role"] == role and role != "main"]
        if rs:
            out[role] = {"main_within_window": _rate([r for r in rs if near_main(r)]),
                         "no_main": _rate([r for r in rs if not near_main(r)])}
    return out


def _reasons(rows):
    reviewed = [r for r in rows if r["reason"]]
    if not reviewed:
        return {"reviewed": 0}
    by_code_role = defaultdict(Counter)
    for r in reviewed:
        by_code_role[r["reason"]][r["role"]] += 1
    return {
        "reviewed": len(reviewed),
        "codebook": sorted({str(r["codebook"]) for r in reviewed}),
        "by_code": dict(Counter(r["reason"] for r in reviewed).most_common()),
        "by_code_role": {k: dict(v) for k, v in sorted(by_code_role.items())},
        "loss": dict(Counter(r["loss"] for r in reviewed)),
        "conf": dict(Counter(r["conf"] for r in reviewed)),
        "loss_yes": sorted(r["file"] for r in reviewed if r["loss"] == "yes"),
    }


# ------------------------------------------------------------------ command

def run_analysis(out_dir, wedding_dir, config):
    """Write photos.csv and summary.json; returns the summary."""
    out_dir, wedding_dir = Path(out_dir), Path(wedding_dir)
    params = config["analysis"]
    wedding = load_wedding(wedding_dir)
    rows = build_rows(out_dir, wedding, params)
    csv_path = out_dir / ANALYSIS_DIR / PHOTOS_CSV
    write_csv(rows, csv_path)
    cull_source = json.loads((out_dir / CULL_FILE).read_text(encoding="utf-8")).get("source")
    summary = summarize(rows, wedding, params, Path(cull_source).name if cull_source else None)
    (wedding_dir / SUMMARY_FILE).write_text(json.dumps(summary, indent=1, ensure_ascii=False),
                                            encoding="utf-8")
    log.info("Analysis of %s: %d photos -> %s, %s", wedding["wedding"], len(rows), csv_path,
             wedding_dir / SUMMARY_FILE)
    unknown_parts = sum(r["day_part"] == "other" for r in rows)
    if unknown_parts:
        log.warning("%d photos fall in no day part of %s", unknown_parts, WEDDING_FILE)
    return summary

