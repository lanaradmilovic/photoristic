"""Ground-truth labels for the grouping and the scoring against them.

A label describes the boundary between two time-adjacent photos of the same camera:
"same" (they belong in one group), "different" or "unsure". Labels are stored by the
sha256 of both photos, not by group id, so they survive re-grouping:

    labels.json = [{a_sha, b_sha, a_name, b_name, label, labeled_at}, ...]

Known limitation: look-back joins (a photo returning to an earlier, non-adjacent group)
are not labelled; only adjacent pairs are.
"""
import json
import logging
import os
from datetime import datetime
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from culling.grouping import _sort_key

log = logging.getLogger(__name__)

LABELS_FILE = "labels.json"
LABEL_VALUES = ("same", "different", "unsure")
THUMB_EDGE = 160  # px, long edge of a thumbnail on the errors sheet


# ------------------------------------------------------------------ labels I/O

def pair_key(a_sha, b_sha):
    return f"{a_sha}|{b_sha}"


def normalise_labels(raw):
    """Validate the content of labels.json (or a POST body). Returns a clean list of
    dicts with exactly the known fields; raises ValueError on anything unexpected."""
    if not isinstance(raw, list):
        raise ValueError("labels must be a JSON list")
    clean = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"label {i}: not an object")
        for field in ("a_sha", "b_sha"):
            value = item.get(field)
            if not isinstance(value, str) or not value or any(c not in "0123456789abcdef" for c in value.lower()):
                raise ValueError(f"label {i}: {field} must be a hex string")
        if item.get("label") not in LABEL_VALUES:
            raise ValueError(f"label {i}: label must be one of {', '.join(LABEL_VALUES)}")
        clean.append({
            "a_sha": item["a_sha"].lower(), "b_sha": item["b_sha"].lower(),
            "a_name": str(item.get("a_name") or ""), "b_name": str(item.get("b_name") or ""),
            "label": item["label"],
            "labeled_at": str(item.get("labeled_at") or datetime.now().isoformat(timespec="seconds")),
        })
    return clean


def load_labels(out_dir):
    path = Path(out_dir) / LABELS_FILE
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return normalise_labels(json.load(f))


def save_labels(out_dir, labels):
    path = Path(out_dir) / LABELS_FILE
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(labels, f, indent=1, ensure_ascii=False)
    os.replace(tmp, path)
    return path


# ------------------------------------------------------------------ boundaries

def group_of(groups_data):
    """photo id -> group id."""
    return {pid: g["group_id"] for g in groups_data["groups"] for pid in g["photo_ids"]}


def _groups_sims(groups_data):
    """Similarity/gap between time-adjacent photos as far as groups.json records them:
    the first photo of each group (boundary_*) and 'neighbour' joins. Look-back and moved
    photos are skipped because their values refer to another photo."""
    out = {}
    if not groups_data:
        return out
    for g in groups_data["groups"]:
        ids = g["photo_ids"]
        if g.get("boundary_similarity") is not None:
            out[ids[0]] = (g["boundary_similarity"], g["boundary_gap_seconds"])
        joined = g.get("joined_by") or ["neighbour"] * (len(ids) - 1)
        for k in range(1, len(ids)):
            if joined[k - 1] == "neighbour":
                out[ids[k]] = (g["consecutive_similarities"][k - 1], g["consecutive_gaps_seconds"][k - 1])
    return out


def boundaries(photos, groups_data=None, embeddings=None):
    """All boundaries between time-adjacent photos of one camera, in capture order,
    cameras sorted as in grouping. Similarity comes from `embeddings` (sha256 -> unit
    vector) when available, otherwise from groups.json where it records that very pair,
    otherwise None. `pipeline` is 'same'/'different' by groups.json, None when a photo is
    missing from it."""
    by_camera = {}
    for p in photos:
        if p.get("status") == "ok" and p.get("capture_time"):
            by_camera.setdefault(p.get("camera_id") or "unknown-camera", []).append(p)
    gid = group_of(groups_data) if groups_data else {}
    fallback = _groups_sims(groups_data)
    embeddings = embeddings or {}

    def sim_of(a, b):
        va, vb = embeddings.get(a["sha256"]), embeddings.get(b["sha256"])
        if va is not None and vb is not None:
            return round(float(np.dot(va, vb)), 4)
        rec = fallback.get(b["id"])
        return rec[0] if rec else None

    out = []
    for camera_id in sorted(by_camera):
        ordered = sorted(by_camera[camera_id], key=_sort_key)
        for a, b in zip(ordered, ordered[1:]):
            gap = (datetime.fromisoformat(b["capture_time"]) - datetime.fromisoformat(a["capture_time"])).total_seconds()
            ga, gb = gid.get(a["id"]), gid.get(b["id"])
            pipeline = None if ga is None or gb is None else ("same" if ga == gb else "different")
            out.append({
                "camera_id": camera_id,
                "a_id": a["id"], "b_id": b["id"], "a_sha": a["sha256"], "b_sha": b["sha256"],
                "a_name": Path(a["primary_path"]).name, "b_name": Path(b["primary_path"]).name,
                "a_thumb": a.get("thumb_file") or "", "b_thumb": b.get("thumb_file") or "",
                "a_preview": a.get("preview_file") or "", "b_preview": b.get("preview_file") or "",
                "a_time": a["capture_time"], "b_time": b["capture_time"],
                "gap": round(gap, 2), "sim": sim_of(a, b), "pipeline": pipeline,
            })
    return out


# ------------------------------------------------------------------ scoring

def _ratio(num, den):
    return num / den if den else None


def score(labels, photos, groups_data):
    """Compare labels with a groups file. 'unsure' labels are skipped; so are pairs whose
    photo is unknown (not in photos.json or not in any group). Metrics are for the
    positive class 'same': a false merge is pipeline same / label different, a missed
    merge is pipeline different / label same."""
    id_by_sha = {p["sha256"]: p["id"] for p in photos if p.get("sha256")}
    gid = group_of(groups_data)
    tp = tn = fp = fn = n_unsure = n_missing = 0
    errors = []
    for lab in labels:
        if lab["label"] == "unsure":
            n_unsure += 1
            continue
        ga = gid.get(id_by_sha.get(lab["a_sha"]))
        gb = gid.get(id_by_sha.get(lab["b_sha"]))
        if ga is None or gb is None:
            n_missing += 1
            continue
        pipeline = "same" if ga == gb else "different"
        if pipeline == lab["label"]:
            if pipeline == "same":
                tp += 1
            else:
                tn += 1
            continue
        kind = "false_merge" if pipeline == "same" else "missed_merge"
        if kind == "false_merge":
            fp += 1
        else:
            fn += 1
        errors.append({"kind": kind, "a_sha": lab["a_sha"], "b_sha": lab["b_sha"],
                       "a_name": lab["a_name"], "b_name": lab["b_name"],
                       "label": lab["label"], "pipeline": pipeline})
    precision, recall = _ratio(tp, tp + fp), _ratio(tp, tp + fn)
    f1 = None if precision is None or recall is None or precision + recall == 0 \
        else 2 * precision * recall / (precision + recall)
    n_scored = tp + tn + fp + fn
    return {
        "n_labels": len(labels), "n_scored": n_scored, "n_unsure": n_unsure, "n_missing": n_missing,
        "correct": tp + tn, "false_merges": fp, "missed_merges": fn, "tp": tp, "tn": tn,
        "precision": precision, "recall": recall, "f1": f1, "accuracy": _ratio(tp + tn, n_scored),
        "errors": errors,
    }


def attach_boundary_info(errors, bounds):
    """Add sim, gap, thumbs and the camera from boundaries() to each error (None when
    the pair is not adjacent any more). Modifies and returns `errors`."""
    by_key = {pair_key(b["a_sha"], b["b_sha"]): b for b in bounds}
    for err in errors:
        b = by_key.get(pair_key(err["a_sha"], err["b_sha"]))
        err["sim"] = b["sim"] if b else None
        err["gap"] = b["gap"] if b else None
        err["a_thumb"] = b["a_thumb"] if b else None
        err["b_thumb"] = b["b_thumb"] if b else None
        err["camera_id"] = b["camera_id"] if b else None
    return errors


def _fmt(value, spec):
    return format(value, spec) if value is not None else "n/a"


def _error_line(err):
    kind = "FALSE MERGE " if err["kind"] == "false_merge" else "MISSED MERGE"
    return (f"{kind}  {err['a_name']} -> {err['b_name']}  sim {_fmt(err.get('sim'), '.3f')}  "
            f"gap {_fmt(err.get('gap'), '.1f')} s  (label {err['label']}, pipeline {err['pipeline']})")


def sorted_errors(errors):
    return sorted(errors, key=lambda e: (e["kind"] != "false_merge", e["a_name"]))


def format_report(name, result):
    r = result
    lines = [f"== {name}",
             f"labels {r['n_labels']}  scored {r['n_scored']}  unsure (skipped) {r['n_unsure']}  "
             f"missing in groups (skipped) {r['n_missing']}",
             f"correct {r['correct']}  false merges {r['false_merges']}  missed merges {r['missed_merges']}",
             f"same: precision {_fmt(r['precision'], '.3f')}  recall {_fmt(r['recall'], '.3f')}  "
             f"F1 {_fmt(r['f1'], '.3f')}  accuracy {_fmt(r['accuracy'], '.3f')}"]
    if r["errors"]:
        lines.append(f"errors ({len(r['errors'])}):")
        lines += ["  " + _error_line(e) for e in sorted_errors(r["errors"])]
    return "\n".join(lines)


def format_comparison(name_a, res_a, name_b, res_b):
    """Metrics side by side plus every boundary whose verdict differs between the two."""
    rows = [("labels scored", res_a["n_scored"], res_b["n_scored"]),
            ("correct", res_a["correct"], res_b["correct"]),
            ("false merges", res_a["false_merges"], res_b["false_merges"]),
            ("missed merges", res_a["missed_merges"], res_b["missed_merges"]),
            ("precision", _fmt(res_a["precision"], ".3f"), _fmt(res_b["precision"], ".3f")),
            ("recall", _fmt(res_a["recall"], ".3f"), _fmt(res_b["recall"], ".3f")),
            ("F1", _fmt(res_a["f1"], ".3f"), _fmt(res_b["f1"], ".3f")),
            ("accuracy", _fmt(res_a["accuracy"], ".3f"), _fmt(res_b["accuracy"], ".3f"))]
    w = max(len(name_a), len(name_b), 10)
    lines = [f"== comparison: A = {name_a}, B = {name_b}",
             f"{'':16}{'A':>{w}}  {'B':>{w}}"]
    lines += [f"{k:16}{str(a):>{w}}  {str(b):>{w}}" for k, a, b in rows]
    err_a = {pair_key(e["a_sha"], e["b_sha"]): e for e in res_a["errors"]}
    err_b = {pair_key(e["a_sha"], e["b_sha"]): e for e in res_b["errors"]}
    fixed = [err_a[k] for k in err_a if k not in err_b]
    broken = [err_b[k] for k in err_b if k not in err_a]
    changed = [(err_a[k], err_b[k]) for k in err_a if k in err_b and err_a[k]["kind"] != err_b[k]["kind"]]
    lines.append(f"differences: {len(fixed)} fixed in B, {len(broken)} broken in B, "
                 f"{len(changed)} wrong in both but differently")
    for e in sorted_errors(fixed):
        lines.append(f"  fixed in B   {_error_line(e)}")
    for e in sorted_errors(broken):
        lines.append(f"  broken in B  {_error_line(e)}")
    for ea, eb in changed:
        lines.append(f"  A: {_error_line(ea)}")
        lines.append(f"  B: {_error_line(eb)}")
    return "\n".join(lines)


# ------------------------------------------------------------------ errors sheet

def errors_sheet_name(groups_file):
    """groups.json -> errors.jpg; groups.nofaces.json -> errors.nofaces.jpg"""
    stem = Path(groups_file).stem
    suffix = stem[len("groups."):] if stem.startswith("groups.") else ("" if stem == "groups" else stem)
    return f"errors.{suffix}.jpg" if suffix else "errors.jpg"


def _thumb(out_dir, rel, edge):
    canvas = Image.new("RGB", (edge, int(edge * 2 / 3)), (200, 200, 200))
    if not rel or not (out_dir / rel).exists():
        return canvas
    with Image.open(out_dir / rel) as img:
        img = img.convert("RGB")
        img.thumbnail((edge, edge))
        canvas = Image.new("RGB", (edge, edge), "white")
        canvas.paste(img, ((edge - img.width) // 2, (edge - img.height) // 2))
    return canvas


def write_errors_sheet(out_dir, errors, filename="errors.jpg", cols=3, edge=THUMB_EDGE):
    """Contact sheet of all scoring errors: thumb a | thumb b per cell, false merges first.
    Returns the path, or None (and removes a stale sheet) when there are no errors."""
    out_dir = Path(out_dir)
    path = out_dir / filename
    if not errors:
        if path.exists():
            path.unlink()
        return None
    errors = sorted_errors(errors)
    cell_w, cell_h, cap = 2 * edge + 24, edge + 36, 14
    rows = -(-len(errors) // cols)
    canvas = Image.new("RGB", (cols * cell_w, 24 + rows * cell_h), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((6, 5), f"{len(errors)} errors: {sum(e['kind'] == 'false_merge' for e in errors)} false merges "
                      f"(pipeline joined, label different), "
                      f"{sum(e['kind'] == 'missed_merge' for e in errors)} missed merges "
                      f"(pipeline split, label same)", fill="black")
    for k, err in enumerate(errors):
        x, y = (k % cols) * cell_w + 8, 24 + (k // cols) * cell_h
        canvas.paste(_thumb(out_dir, err.get("a_thumb"), edge), (x, y))
        canvas.paste(_thumb(out_dir, err.get("b_thumb"), edge), (x + edge + 8, y))
        colour = (190, 30, 30) if err["kind"] == "false_merge" else (30, 90, 190)
        draw.rectangle([x - 3, y - 3, x + 2 * edge + 10, y + edge + 2], outline=colour, width=2)
        title = "FALSE MERGE" if err["kind"] == "false_merge" else "MISSED MERGE"
        draw.text((x, y + edge + 4), f"{title}  sim {_fmt(err.get('sim'), '.2f')}  +{_fmt(err.get('gap'), '.1f')} s",
                  fill=colour)
        draw.text((x, y + edge + 4 + cap), f"{err['a_name']} -> {err['b_name']}", fill="black")
    canvas.save(path, "JPEG", quality=85)
    log.info("Errors sheet: %s", path)
    return path
