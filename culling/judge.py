"""Step 2c - VLM judge for the grey zone of grouping.

DINOv2 similarity between 0.80 and 0.90 is a grey zone: it holds pairs that belong
together (the same couple in a new pose) and pairs that must stay apart (another
guest at the same spot). Face identities (culling/faces.py) settle part of it; for
the rest (profiles, backs, small faces) a vision-language model that sees both
frames is asked. This module does everything around that call:

  select_pairs          which pairs to ask about: time-adjacent photos in the band
                        and look-back candidates (an earlier group of the same camera
                        within grouping.lookback_seconds), minus what faces or the
                        no-people rules already decide
  pair_image            one JPEG per pair: both previews side by side, labelled 1 and 2
  PROMPT, VERDICT_SCHEMA  the question and the JSON the model must answer with
  run_judging           the loop over the pairs: retries, per-pair saves, resume
  compare_with_labels   the verdicts against labels.json (from `cull.py label`)

Files in the output folder: judge_pairs.json, judge_pairs.jpg (contact sheet, split
into judge_pairs_02.jpg ... when very long), judge_pairs/<a>_<b>.jpg (exactly what
is sent) and judge_verdicts.json. The verdicts are not used by grouping yet; this
step measures the model.

Privacy: the pair images leave the machine only towards `vlm.base_url` (the user's
own server). Nothing of the images or the prompt is logged.
"""
import hashlib
import json
import logging
import math
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from culling.embed import load_cache as load_embeddings
from culling.faces import load_identities, photo_signatures
from culling.grouping import GROUPS_FILE, _sort_key, identity_relation, load_groups
from culling.ingest import load_photos
from culling.labels import _thumb, group_of, load_labels, pair_key
from culling.people import load_cache as load_people
from culling.vlm import VLMError, VLMUnavailable, make_client

log = logging.getLogger(__name__)

PAIRS_FILE = "judge_pairs.json"
VERDICTS_FILE = "judge_verdicts.json"
SHEET_FILE = "judge_pairs.jpg"
PAIR_DIR = "judge_pairs"
GUTTER = 24            # px between the two frames of a pair image
PATCH_PX = 32          # Qwen3.5: one visual token per 32x32 px (patch 16, merge 2)
TEXT_TOKENS = 330      # prompt + chat template + answer, on top of the image tokens
SHEET_THUMB = 120      # px, long edge of a tile on the contact sheet
SHEET_COLS = 4
SHEET_MAX_HEIGHT = 16000  # px; JPEG viewers and the PIL encoder dislike taller sheets

# The prompt says nothing about the DINOv2 similarity or the pipeline's decision: the
# judge must look at the frames, not confirm a number. The time gap is given because
# a photographer would use it too (3 s apart is a burst, 90 s apart may be a new
# pose). "Interchangeable" is the group semantics of this project (decided by the
# user 2026-11-11): the same main people in the same moment at the same place are one
# group, even with a wider or tighter framing or a new pose; another guest (a hug in
# the congratulation line), a person added to or missing from a group photo, or
# another activity is another group.
# A stricter v2 (describe each photo's action first, "doubt -> different") was tried on
# 2026-11-11 and was much worse (26 of 56 labelled pairs vs 48 for this one): it split on
# background people. Text and analysis: docs/research/2026-11-11-judge-first-real-run.md.
PROMPT = """These are two wedding photos by the same photographer, labelled 1 (left) and 2 (right), \
taken {gap} seconds apart.

Answer with JSON:
- same_people: "yes" if the main person or people are the same in both photos, "no" if not, \
"unsure" if you cannot tell. If a person was added to or is missing from the group, the answer \
is "no".
- interchangeable: "yes" if both photos show the same main people in the same moment at the same \
place, so that the photographer would pick the best of them; a wider or tighter framing, a change \
of pose or expression, or a vertical versus a horizontal frame is still "yes". "no" if the main \
people differ (for example hugging another guest, or one person more or fewer in the group) or \
the activity or place changed. "unsure" if you cannot tell.
- verdict: "same_group" when the photos are interchangeable, "different_group" when they show \
different people or a different moment or place, otherwise "unsure".
- confidence: a number from 0 to 1.
- reason: fewer than 20 words."""

VERDICT_SCHEMA = {
    "type": "object",
    "properties": {
        "same_people": {"type": "string", "enum": ["yes", "no", "unsure"]},
        "interchangeable": {"type": "string", "enum": ["yes", "no", "unsure"]},
        "verdict": {"type": "string", "enum": ["same_group", "different_group", "unsure"]},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "reason": {"type": "string"},
    },
    "required": ["same_people", "interchangeable", "verdict", "confidence", "reason"],
    "additionalProperties": False,
}
_ENUMS = {field: tuple(VERDICT_SCHEMA["properties"][field]["enum"])
          for field in ("same_people", "interchangeable", "verdict")}


def _now():
    return datetime.now().isoformat(timespec="seconds")


def _time(photo):
    return datetime.fromisoformat(photo["capture_time"])


def _write_json(path, data):
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    os.replace(tmp, path)


def verdict_key(pair):
    return f"{pair['a_id']}|{pair['b_id']}"


# ------------------------------------------------------------- pair selection

def _usable(photos, embeddings, gid):
    """Photos the judge can work with, per camera, in capture order: ingested, dated,
    embedded and present in groups.json. Returns ({camera: [photo]}, n_skipped)."""
    by_camera, skipped = {}, 0
    for p in photos:
        if p.get("status") != "ok" or not p.get("capture_time") or p.get("sha256") not in embeddings \
                or p["id"] not in gid:
            skipped += 1
            continue
        by_camera.setdefault(p.get("camera_id") or "unknown-camera", []).append(p)
    return {c: sorted(ps, key=_sort_key) for c, ps in sorted(by_camera.items())}, skipped


def select_pairs(photos, embeddings, groups_data, judge_cfg, grouping_cfg, people=None,
                 signatures=None, include_faces_decided=False, max_pairs=0):
    """The pairs whose grouping decision is uncertain: similarity in the half-open band
    [sim_low, sim_high) between

      - neighbours: time-adjacent photos of one camera (`kind` "neighbour"), joined or
        not by the pipeline;
      - look-back candidates (`kind` "lookback"): for each photo, the best-matching
        earlier photo of another group whose latest earlier photo is at most
        grouping.lookback_seconds old (the single best group, as the pipeline joins the
        most similar candidate; like find_lookback_group, a group whose best photo shows
        different identified people is skipped and only counted). The pipeline did not
        join these. A best match at or above sim_high that the pipeline still did not
        join is only counted: `stats["above_band_closer_group"]` when the photo's own
        group matched even better, else `stats["above_band_not_joined"]` (drift guard,
        group span or faces blocked it).
        Also: a photo the pipeline joined to its group by look-back (groups.json says
        so, or its previous photo is not in its group) whose best match in that group is
        in the band - a possible false merge through the relaxed look-back rules. Such
        pairs are kept even when faces or the no-people rules decided them: that
        decision is exactly what is being checked.

    `a` is always the earlier photo. A look-back pair that is also a neighbour pair is
    kept once, as the neighbour pair. Excluded afterwards and counted in `stats`: pairs
    whose face identities already say "same" or "different" (unless
    `include_faces_decided`; the relation is recorded on every kept pair), pairs where
    person detection found nobody on both sides (the nopeople_* rules decide those;
    a missing entry counts as "has people"), and everything past `max_pairs` (> 0) in
    the (camera, time) order. Similarities are rounded to 4 decimals first.

    Returns (pairs, stats). A pair is {a_id, b_id, a_name, b_name, camera_id, a_time,
    b_time, kind, similarity, gap_seconds, pipeline_same_group, faces_relation, image,
    image_size}; image and image_size are filled by write_pair_images.
    """
    people = people or {}
    signatures = signatures or {}
    sim_low, sim_high = float(judge_cfg["sim_low"]), float(judge_cfg["sim_high"])
    lookback = float(grouping_cfg["lookback_seconds"])
    allow_unknown = bool(grouping_cfg.get("faces_same_allows_unknown", False))
    partial_blocks = bool(grouping_cfg.get("faces_partial_overlap_blocks", False))
    gid = group_of(groups_data)
    how_joined = {}  # photo id -> "neighbour" / "lookback" / "moved" from groups.json (first photos absent)
    for g in groups_data["groups"]:
        if g.get("joined_by") is not None:
            how_joined.update(zip(g["photo_ids"][1:], g["joined_by"]))
    by_camera, n_skipped = _usable(photos, embeddings, gid)
    stats = {"photos": sum(len(ps) for ps in by_camera.values()), "cameras": len(by_camera),
             "skipped_photos": n_skipped, "neighbour_in_band": 0, "lookback_in_band": 0,
             "excluded_faces_same": 0, "excluded_faces_different": 0, "excluded_no_people": 0,
             "lookback_blocked_by_faces": 0, "above_band_not_joined": 0, "above_band_closer_group": 0,
             "cut_by_max_pairs": 0, "selected": 0}
    candidates = {}  # (a_id, b_id) -> (pair, a, b); neighbour pairs come first per photo

    def in_band(sim):
        return sim_low <= sim < sim_high

    def relation(a, b):
        if not signatures:
            return None
        return identity_relation(signatures.get(a["sha256"]), signatures.get(b["sha256"]), allow_unknown,
                                 partial_blocks)

    def nobody(p):
        return people.get(p["sha256"], True) is False

    def add(camera_id, a, b, kind, sim, same_group):
        key = (a["id"], b["id"])
        if key in candidates:
            return
        candidates[key] = ({
            "a_id": a["id"], "b_id": b["id"],
            "a_name": Path(a["primary_path"]).name, "b_name": Path(b["primary_path"]).name,
            "camera_id": camera_id, "a_time": a["capture_time"], "b_time": b["capture_time"],
            "kind": kind, "similarity": sim,
            "gap_seconds": round((_time(b) - _time(a)).total_seconds(), 3),
            "pipeline_same_group": bool(same_group), "faces_relation": None,
            "image": None, "image_size": None,
        }, a, b)
        stats[f"{kind}_in_band"] += 1

    for camera_id, ordered in by_camera.items():
        vectors = np.stack([embeddings[p["sha256"]] for p in ordered]).astype(np.float64)
        sims = np.round(vectors @ vectors.T, 4)
        times = [_time(p) for p in ordered]
        earlier = {}  # group id -> indices of its photos seen so far, in time order
        for i, b in enumerate(ordered):
            own_group = gid[b["id"]]
            if i:
                prev = ordered[i - 1]
                sim = float(sims[i - 1, i])
                if in_band(sim):
                    add(camera_id, prev, b, "neighbour", sim, gid[prev["id"]] == own_group)
                # Look-back: every other group still in the window, its best earlier photo,
                # most similar group first. As in find_lookback_group a group whose best
                # photo shows different identified people is skipped (the pipeline never
                # joined it); the first remaining group is the pipeline's real candidate.
                ranked = []  # (similarity, index of the best earlier photo)
                for group_id, idx in (earlier.items() if lookback > 0 else ()):
                    if group_id == own_group or (times[i] - times[idx[-1]]).total_seconds() > lookback:
                        continue
                    j = max(idx, key=lambda k: sims[k, i])
                    ranked.append((float(sims[j, i]), j))
                own_best = max((float(sims[k, i]) for k in earlier.get(own_group, [])), default=None)
                for sim, j in sorted(ranked, reverse=True):
                    if relation(ordered[j], b) == "different":
                        if sim >= sim_low:
                            stats["lookback_blocked_by_faces"] += 1
                        if include_faces_decided and in_band(sim):
                            add(camera_id, ordered[j], b, "lookback", sim, False)
                        continue
                    if in_band(sim):
                        add(camera_id, ordered[j], b, "lookback", sim, False)
                    elif sim >= sim_high:
                        closer = own_best is not None and own_best >= sim
                        stats["above_band_closer_group" if closer else "above_band_not_joined"] += 1
                    break
                # A look-back join by the pipeline (groups.json says so, or b's previous photo
                # is not in b's group although the group has earlier photos): the best earlier
                # photo of the group, in the band, may be a false merge.
                own = earlier.get(own_group)
                if own and (how_joined.get(b["id"]) == "lookback" or gid[prev["id"]] != own_group):
                    j = max(own, key=lambda k: sims[k, i])
                    if in_band(float(sims[j, i])):
                        add(camera_id, ordered[j], b, "lookback", float(sims[j, i]), True)
            earlier.setdefault(own_group, []).append(i)

    pairs = []
    for pair, a, b in candidates.values():
        rel = relation(a, b)
        pair["faces_relation"] = rel
        # A look-back join the pipeline made is kept whatever decided it: the relaxed
        # faces / no-people rules are exactly what such a pair double-checks.
        relaxed_join = pair["kind"] == "lookback" and pair["pipeline_same_group"]
        if rel in ("same", "different") and not include_faces_decided and not relaxed_join:
            stats[f"excluded_faces_{rel}"] += 1
            continue
        if nobody(a) and nobody(b) and not relaxed_join:
            stats["excluded_no_people"] += 1
            continue
        pairs.append(pair)
    pairs.sort(key=lambda p: (p["camera_id"], p["b_time"], p["a_time"], p["kind"]))
    if max_pairs > 0 and len(pairs) > max_pairs:
        stats["cut_by_max_pairs"] = len(pairs) - max_pairs
        pairs = pairs[:max_pairs]
    stats["selected"] = len(pairs)
    return pairs, stats


# ------------------------------------------------------------------ pair images

def _font(size):
    try:
        return ImageFont.load_default(size=size)
    except Exception:  # Pillow without FreeType: the fixed bitmap font
        return ImageFont.load_default()


def _frame(out_dir, photo, long_edge):
    """The preview of a photo scaled to `long_edge`, or a grey tile when it is missing."""
    rel = photo.get("preview_file") if photo else None
    path = Path(out_dir) / rel if rel else None
    if path is None or not path.exists():
        return Image.new("RGB", (long_edge, int(long_edge * 2 / 3)), (200, 200, 200))
    with Image.open(path) as img:
        img = img.convert("RGB")
    img.thumbnail((long_edge, long_edge), Image.Resampling.LANCZOS)
    return img


def pair_image(out_dir, a, b, long_edge):
    """Both previews side by side on a mid-grey canvas (gap GUTTER px, frames aligned at
    the top), with a black box holding a white "1" / "2" in each frame's top-left corner.
    The previews (ingest.preview_long_edge, orientation already applied) are only
    scaled down, never cropped."""
    left, right = _frame(out_dir, a, long_edge), _frame(out_dir, b, long_edge)
    canvas = Image.new("RGB", (left.width + GUTTER + right.width, max(left.height, right.height)), (128, 128, 128))
    canvas.paste(left, (0, 0))
    canvas.paste(right, (left.width + GUTTER, 0))
    draw = ImageDraw.Draw(canvas)
    font = _font(max(12, int(long_edge * 0.05)))
    pad = max(3, long_edge // 100)
    for text, x in (("1", 0), ("2", left.width + GUTTER)):
        l, t, r, b_ = draw.textbbox((0, 0), text, font=font)
        box = [x + 8, 8, x + 8 + (r - l) + 2 * pad, 8 + (b_ - t) + 2 * pad]
        draw.rectangle(box, fill="black")
        draw.text((box[0] + pad - l, box[1] + pad - t), text, fill="white", font=font)
    return canvas


def _stem(photo, fallback):
    return Path(photo["primary_path"]).stem if photo and photo.get("primary_path") else fallback


def write_pair_images(out_dir, photos_by_id, pairs, long_edge):
    """Write judge_pairs/<a_stem>_<b_stem>.jpg for every pair (ids appended when two
    pairs would share a name) and fill in pair["image"] / pair["image_size"]. Files of
    an earlier selection are removed first."""
    out_dir = Path(out_dir)
    pair_dir = out_dir / PAIR_DIR
    pair_dir.mkdir(parents=True, exist_ok=True)
    for old in list(pair_dir.glob("*.jpg")) + list(pair_dir.glob("*.tmp")):
        old.unlink()
    used = set()
    for pair in pairs:
        a, b = photos_by_id.get(pair["a_id"]), photos_by_id.get(pair["b_id"])
        name = f"{_stem(a, pair['a_id'])}_{_stem(b, pair['b_id'])}"
        if name in used:
            name = f"{name}_{pair['a_id']}_{pair['b_id']}"
        used.add(name)
        img = pair_image(out_dir, a, b, long_edge)
        path = pair_dir / f"{name}.jpg"
        tmp = path.with_suffix(".tmp")
        img.save(tmp, "JPEG", quality=90)
        os.replace(tmp, path)
        pair["image"] = f"{PAIR_DIR}/{name}.jpg"
        pair["image_size"] = [img.width, img.height]
    return pair_dir


def estimate_tokens(image_size):
    """Prompt tokens of one request for Qwen3.5: one visual token per 32x32 px of the
    pair image (sides rounded up) plus the text allowance."""
    w, h = image_size
    return math.ceil(w / PATCH_PX) * math.ceil(h / PATCH_PX) + TEXT_TOKENS


# ------------------------------------------------------------------ pairs files

def save_pairs(out_dir, pairs, stats, judge_cfg, grouping_cfg):
    _write_json(Path(out_dir) / PAIRS_FILE, {
        "created": _now(),
        "sim_low": judge_cfg["sim_low"], "sim_high": judge_cfg["sim_high"],
        "lookback_seconds": grouping_cfg["lookback_seconds"],
        "pair_image_long_edge": judge_cfg["pair_image_long_edge"],
        "include_faces_decided": bool(judge_cfg["include_faces_decided"]),
        "max_pairs": judge_cfg["max_pairs"],
        "stats": stats, "pairs": pairs,
    })


def load_pairs(out_dir):
    path = Path(out_dir) / PAIRS_FILE
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_pairs_sheet(out_dir, pairs, photos_by_id, cols=SHEET_COLS, edge=SHEET_THUMB):
    """Contact sheet of the selected pairs (thumb a | thumb b per cell, in the order of
    judge_pairs.json, numbered from 1). Green frame: the pipeline joined the pair, red:
    it did not. Sheets taller than SHEET_MAX_HEIGHT are split into judge_pairs.jpg,
    judge_pairs_02.jpg, ... Returns the paths (none when there are no pairs)."""
    out_dir = Path(out_dir)
    for old in out_dir.glob("judge_pairs*.jpg"):  # stale sheets of an earlier selection
        old.unlink()
    if not pairs:
        return []
    cell_w, cell_h, cap = 2 * edge + 40, edge + 36, 14
    per_sheet = max(1, (SHEET_MAX_HEIGHT - 24) // cell_h) * cols
    chunks = [pairs[k:k + per_sheet] for k in range(0, len(pairs), per_sheet)]
    paths = []
    for s, chunk in enumerate(chunks, start=1):
        rows = -(-len(chunk) // cols)
        canvas = Image.new("RGB", (cols * cell_w, 24 + rows * cell_h), "white")
        draw = ImageDraw.Draw(canvas)
        part = f", sheet {s}/{len(chunks)}" if len(chunks) > 1 else ""
        draw.text((6, 5), f"{len(pairs)} grey-zone pairs for the VLM judge{part}: "
                          f"green frame = pipeline joined, red = pipeline split; nb = neighbours, lb = look-back",
                  fill="black")
        for k, pair in enumerate(chunk):
            n = (s - 1) * per_sheet + k + 1
            x, y = (k % cols) * cell_w + 8, 24 + (k // cols) * cell_h
            a, b = photos_by_id.get(pair["a_id"]), photos_by_id.get(pair["b_id"])
            canvas.paste(_thumb(out_dir, a.get("thumb_file") if a else None, edge), (x, y))
            canvas.paste(_thumb(out_dir, b.get("thumb_file") if b else None, edge), (x + edge + 8, y))
            joined = pair["pipeline_same_group"]
            colour = (30, 140, 60) if joined else (190, 30, 30)
            draw.rectangle([x - 3, y - 3, x + 2 * edge + 10, y + edge + 2], outline=colour, width=2)
            faces = {"same": "same", "different": "diff"}.get(pair["faces_relation"], "-")
            draw.text((x, y + edge + 4),
                      f"#{n} {'nb' if pair['kind'] == 'neighbour' else 'lb'} sim {pair['similarity']:.2f} "
                      f"+{pair['gap_seconds']:.1f} s {'JOINED' if joined else 'SPLIT'} faces:{faces}", fill=colour)
            draw.text((x, y + edge + 4 + cap), f"{pair['a_name']} -> {pair['b_name']}", fill="black")
        path = out_dir / (SHEET_FILE if s == 1 else f"judge_pairs_{s:02d}.jpg")
        canvas.save(path, "JPEG", quality=85)
        paths.append(path)
    return paths


# --------------------------------------------------------------------- dry-run

def format_dry_run(pairs, stats, judge_cfg):
    """What a real run would send, without sending anything."""
    kinds = {"neighbour": [p for p in pairs if p["kind"] == "neighbour"],
             "lookback": [p for p in pairs if p["kind"] == "lookback"]}
    lines = [f"VLM judge dry-run: {len(pairs)} pairs selected (band {judge_cfg['sim_low']:.2f} <= similarity "
             f"< {judge_cfg['sim_high']:.2f}; {stats['photos']} photos, {stats['cameras']} camera(s))"]
    for kind, ps in kinds.items():
        joined = sum(1 for p in ps if p["pipeline_same_group"])
        note = "  (joined = look-back joins by the pipeline, kept as possible false merges)" \
            if kind == "lookback" and joined else ""
        lines.append(f"  {kind:10} {len(ps):5}   pipeline joined {joined}, split {len(ps) - joined}{note}")
    kept = {r: sum(1 for p in pairs if p["faces_relation"] == r) for r in ("same", "different")}
    if kept["same"] or kept["different"]:
        lines.append(f"  of these, faces already decided: same {kept['same']}, different {kept['different']}")
    lines += ["excluded:",
              f"  faces decided same       {stats['excluded_faces_same']:5}   (identities say the same people;"
              f" --include-faces-decided sends them too)",
              f"  faces decided different  {stats['excluded_faces_different']:5}   (no identity in common)",
              f"  no people on both sides  {stats['excluded_no_people']:5}   (the nopeople_* rules decide those)",
              f"  look-back blocked, faces {stats['lookback_blocked_by_faces']:5}   (best match shows different "
              f"people; the pipeline skipped that group too)",
              f"  above band, not joined   {stats['above_band_not_joined']:5}   (look-back match >= "
              f"{judge_cfg['sim_high']:.2f} the pipeline still kept apart: drift guard, group span or faces)",
              f"  above band, closer group {stats['above_band_closer_group']:5}   (look-back match >= "
              f"{judge_cfg['sim_high']:.2f} but the photo's own group matched even better)",
              f"  cut by max_pairs         {stats['cut_by_max_pairs']:5}"]
    if stats.get("skipped_photos"):
        lines.append(f"  photos not usable        {stats['skipped_photos']:5}   (ingest error, no timestamp, "
                     f"no embedding or not in groups.json)")
    tokens = sorted(estimate_tokens(p["image_size"]) for p in pairs if p.get("image_size"))
    if tokens:
        lines.append(f"tokens per pair (Qwen3.5: 1 per {PATCH_PX}x{PATCH_PX} px + ~{TEXT_TOKENS} text): "
                     f"min {tokens[0]}  median {tokens[len(tokens) // 2]}  max {tokens[-1]}  total {sum(tokens)}")
    seconds = len(pairs) * float(judge_cfg["seconds_per_call"])
    lines.append(f"estimated duration: {len(pairs)} x {float(judge_cfg['seconds_per_call']):.1f} s = "
                 f"{seconds / 60:.1f} min (judge.seconds_per_call)")
    lines.append(f"files: {PAIRS_FILE}, {SHEET_FILE}, {PAIR_DIR}/ ({len(pairs)} images); no request was sent")
    return "\n".join(lines)


# -------------------------------------------------------------------- verdicts

def parse_verdict(text):
    """The model's answer -> {same_people, interchangeable, verdict, confidence, reason}.
    Accepts a ``` fence around the JSON. Raises ValueError for anything that is not a
    valid verdict (the caller retries)."""
    if not isinstance(text, str):
        raise ValueError("answer is not text")
    body = text.strip()
    if body.startswith("```"):
        body = body.split("\n", 1)[1] if "\n" in body else ""
        body = body.rsplit("```", 1)[0]
    try:
        data = json.loads(body)
    except ValueError as e:
        raise ValueError(f"answer is not JSON: {e}") from None
    if not isinstance(data, dict):
        raise ValueError("answer is not a JSON object")
    out = {}
    for field, allowed in _ENUMS.items():
        if data.get(field) not in allowed:
            raise ValueError(f"{field} must be one of {', '.join(allowed)}, got {str(data.get(field))[:40]!r}")
        out[field] = data[field]
    confidence = data.get("confidence")
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
        raise ValueError(f"confidence must be a number between 0 and 1, got {str(confidence)[:40]!r}")
    out["confidence"] = round(float(confidence), 3)
    reason = data.get("reason")
    if not isinstance(reason, str):
        raise ValueError("reason must be a string")
    out["reason"] = reason.strip()
    return out


def judge_pair(client, pair, jpeg, max_retries):
    """Ask the model about one pair. Up to 1 + max_retries attempts when a request fails
    (VLMError) or the answer is not a valid verdict (ValueError); after that the verdict
    is "error" with the last message as reason. VLMUnavailable is not retried: the server
    is gone, the caller stops and resumes later."""
    prompt = PROMPT.format(gap=f"{pair['gap_seconds']:.1f}")
    started = time.time()
    attempts, last_error, verdict = 0, None, None
    while verdict is None and attempts <= max_retries:
        attempts += 1
        try:
            verdict = parse_verdict(client.ask(prompt, [jpeg], VERDICT_SCHEMA))
        except VLMUnavailable:
            raise
        except (VLMError, ValueError) as e:
            last_error = e
            log.warning("Pair %s -> %s, attempt %d of %d failed: %s",
                        pair["a_name"], pair["b_name"], attempts, 1 + max_retries, e)
    if verdict is None:
        verdict = {"same_people": "unsure", "interchangeable": "unsure", "verdict": "error",
                   "confidence": 0.0, "reason": f"{type(last_error).__name__}: {str(last_error)[:200]}"}
        usage = {}
    else:
        usage = getattr(client, "last_usage", None) or {}
    return {"a_id": pair["a_id"], "b_id": pair["b_id"], "a_name": pair["a_name"], "b_name": pair["b_name"],
            "kind": pair["kind"], **verdict, "attempts": attempts,
            "elapsed_s": round(time.time() - started, 2),
            "prompt_tokens": usage.get("prompt_tokens"), "judged_at": _now()}


def prompt_hash():
    """Short hash of PROMPT and VERDICT_SCHEMA: verdicts of another prompt must not be resumed."""
    text = PROMPT + json.dumps(VERDICT_SCHEMA, sort_keys=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def load_verdicts(out_dir):
    path = Path(out_dir) / VERDICTS_FILE
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_verdicts(out_dir, data):
    data["updated"] = _now()
    _write_json(Path(out_dir) / VERDICTS_FILE, data)


def run_judging(out_dir, pairs, client, vlm_cfg, sim_low=None, sim_high=None):
    """Judge every pair that has no verdict yet (or an "error" one) and save
    judge_verdicts.json after each pair, so an interrupted run resumes. Pings the server
    first (VLMError when it does not answer or serves another model). A VLMUnavailable
    during the run is logged and re-raised with the progress on disk. Returns the
    verdicts file content."""
    out_dir = Path(out_dir)
    client.ping()
    data = load_verdicts(out_dir) or {"created": _now(), "updated": None, "model": client.model,
                                      "prompt_hash": prompt_hash(),
                                      "base_url": client.base_url, "sim_low": sim_low, "sim_high": sim_high,
                                      "verdicts": {}, "labels": None}
    if data.get("model") != client.model:
        sys.exit(f"{out_dir / VERDICTS_FILE} holds verdicts of {data.get('model')}; move or delete it "
                 f"before judging with {client.model}.")
    if data.get("prompt_hash") != prompt_hash():
        sys.exit(f"{out_dir / VERDICTS_FILE} holds verdicts of another prompt (hash {data.get('prompt_hash')}, "
                 f"now {prompt_hash()}); move or delete it before judging, so the two are not mixed.")
    data["base_url"] = client.base_url
    if sim_low is not None:
        data["sim_low"], data["sim_high"] = sim_low, sim_high
    verdicts = data.setdefault("verdicts", {})
    todo = [p for p in pairs if verdicts.get(verdict_key(p), {}).get("verdict", "error") == "error"]
    n_retry = sum(1 for p in todo if verdict_key(p) in verdicts)
    log.info("Judging %d of %d pairs with %s at %s (%d already judged, %d earlier errors retried)",
             len(todo), len(pairs), client.model, client.base_url, len(pairs) - len(todo), n_retry)
    estimate_logged = False
    for n, pair in enumerate(todo, start=1):
        with open(out_dir / pair["image"], "rb") as f:
            jpeg = f.read()
        try:
            verdict = judge_pair(client, pair, jpeg, int(vlm_cfg["max_retries"]))
        except VLMUnavailable as e:
            log.error("VLM server gone after %d of %d pairs (%s); progress is saved in %s, rerun to resume",
                      n - 1, len(todo), e, VERDICTS_FILE)
            raise
        verdicts[verdict_key(pair)] = verdict
        save_verdicts(out_dir, data)
        if not estimate_logged and verdict.get("prompt_tokens"):
            log.info("First pair: %s prompt tokens on the server, local estimate %d",
                     verdict["prompt_tokens"], estimate_tokens(pair["image_size"]))
            estimate_logged = True
        log.info("[%d/%d] %s -> %s: %s (confidence %.2f, %d attempt(s), %.1f s)", n, len(todo),
                 pair["a_name"], pair["b_name"], verdict["verdict"], verdict["confidence"],
                 verdict["attempts"], verdict["elapsed_s"])
    return data


# ------------------------------------------------------------ labels comparison

def _ratio(num, den):
    return round(num / den, 4) if den else None


def compare_with_labels(pairs, verdicts, labels, photos):
    """The verdicts against labels.json on the pairs both cover. Labels describe
    time-adjacent photos (by sha256), so only neighbour pairs can match; look-back pairs
    are not compared. Label "unsure" is skipped. Verdicts "unsure" / "error" are
    "abstained": listed, excluded from the decided precision/recall, counted as misses
    in the strict recall. The pipeline's decision on the same pairs is the baseline."""
    sha_by_id = {p["id"]: p["sha256"] for p in photos if p.get("sha256")}
    label_of = {pair_key(l["a_sha"], l["b_sha"]): l["label"] for l in labels}
    counts = {"n_labels": len(label_of), "n_labels_matched": 0, "n_neighbour_pairs": 0, "n_labelled": 0,
              "n_unsure_labels": 0, "n_unjudged": 0}
    judge = {k: 0 for k in ("correct", "wrong", "abstained", "abstained_same", "tp", "fp", "fn", "fixes", "breaks")}
    pipeline = {k: 0 for k in ("correct", "wrong", "tp", "fp", "fn")}
    wrong = []
    for pair in pairs:
        if pair["kind"] != "neighbour":
            continue
        counts["n_neighbour_pairs"] += 1
        label = label_of.get(pair_key(sha_by_id.get(pair["a_id"], ""), sha_by_id.get(pair["b_id"], "")))
        if label is None:
            continue
        counts["n_labels_matched"] += 1
        if label == "unsure":
            counts["n_unsure_labels"] += 1
            continue
        counts["n_labelled"] += 1
        verdict = verdicts.get(verdict_key(pair))
        if verdict is None:
            counts["n_unjudged"] += 1
            continue
        truth_same = label == "same"
        pipe_same = bool(pair["pipeline_same_group"])
        pipe_ok = pipe_same == truth_same
        pipeline["correct" if pipe_ok else "wrong"] += 1
        if pipe_same:
            pipeline["tp" if truth_same else "fp"] += 1
        elif truth_same:
            pipeline["fn"] += 1
        if verdict["verdict"] not in ("same_group", "different_group"):
            judge["abstained"] += 1
            if truth_same:
                judge["abstained_same"] += 1
            continue
        said_same = verdict["verdict"] == "same_group"
        ok = said_same == truth_same
        judge["correct" if ok else "wrong"] += 1
        if said_same:
            judge["tp" if truth_same else "fp"] += 1
        elif truth_same:
            judge["fn"] += 1
        if ok and not pipe_ok:
            judge["fixes"] += 1
        if not ok and pipe_ok:
            judge["breaks"] += 1
        if not ok:
            wrong.append({"a_name": pair["a_name"], "b_name": pair["b_name"],
                          "similarity": pair["similarity"], "gap_seconds": pair["gap_seconds"],
                          "label": label, "verdict": verdict["verdict"], "confidence": verdict["confidence"],
                          "reason": verdict["reason"], "pipeline": "same" if pipe_same else "different"})
    judge["precision"] = _ratio(judge["tp"], judge["tp"] + judge["fp"])
    judge["recall"] = _ratio(judge["tp"], judge["tp"] + judge["fn"])
    judge["recall_strict"] = _ratio(judge["tp"], judge["tp"] + judge["fn"] + judge["abstained_same"])
    pipeline["precision"] = _ratio(pipeline["tp"], pipeline["tp"] + pipeline["fp"])
    pipeline["recall"] = _ratio(pipeline["tp"], pipeline["tp"] + pipeline["fn"])
    return {"note": "labels describe time-adjacent photos, so only neighbour pairs are compared",
            **counts, "judge": judge, "pipeline": pipeline, "wrong_pairs": wrong}


def _fmt(value):
    return "n/a" if value is None else f"{value:.3f}"


def format_labels_comparison(result):
    j, p = result["judge"], result["pipeline"]
    scored = j["correct"] + j["wrong"] + j["abstained"]
    lines = [f"== judge vs labels.json ({result['note']})",
             f"labels {result['n_labels']}, matching a selected neighbour pair {result['n_labels_matched']} "
             f"(of {result['n_neighbour_pairs']} neighbour pairs): scored {result['n_labelled']}  "
             f"unsure labels (skipped) {result['n_unsure_labels']}  not judged yet {result['n_unjudged']}",
             f"judge:    correct {j['correct']}  wrong {j['wrong']}  abstained {j['abstained']} "
             f"(unsure/error; {j['abstained_same']} of them labelled same)  of {scored}",
             f"pipeline: correct {p['correct']}  wrong {p['wrong']}  of {scored} (same pairs, the baseline)",
             f"same_group: judge precision {_fmt(j['precision'])}  recall {_fmt(j['recall'])} (decided only)  "
             f"strict recall {_fmt(j['recall_strict'])} (abstained = missed)",
             f"            pipeline precision {_fmt(p['precision'])}  recall {_fmt(p['recall'])}",
             f"judge fixes {j['fixes']} pipeline errors and breaks {j['breaks']} pipeline decisions"]
    if result["wrong_pairs"]:
        lines.append(f"wrong ({len(result['wrong_pairs'])}):")
        for w in result["wrong_pairs"]:
            lines.append(f"  {w['a_name']} -> {w['b_name']}  sim {w['similarity']:.3f}  gap {w['gap_seconds']:.1f} s  "
                         f"label {w['label']}, judge {w['verdict']} ({w['confidence']:.2f}), pipeline {w['pipeline']}: "
                         f"{w['reason']}")
    return "\n".join(lines)


# ---------------------------------------------------------------- orchestrator

def run_judge(out_dir, config, dry_run=False, include_faces_decided=None, max_pairs=None,
              client_factory=make_client):
    """Select the pairs, write judge_pairs.json, the pair images and the contact sheet;
    then either print the dry-run summary or judge the pairs with the configured server
    and compare them with labels.json when it exists. `include_faces_decided` and
    `max_pairs` override config["judge"] when not None. Exits with a message when the
    grouping outputs are missing. The client is only created (and pinged, before any
    other work) for a real run."""
    out_dir = Path(out_dir)
    judge_cfg = dict(config["judge"])
    if include_faces_decided is not None:
        judge_cfg["include_faces_decided"] = bool(include_faces_decided)
    if max_pairs is not None:
        judge_cfg["max_pairs"] = int(max_pairs)
    grouping_cfg = config["grouping"]
    client = None
    if not dry_run:
        # Fail fast: without a server there is no point in selecting pairs and writing
        # images (run_judging pings again; a GET /models is cheap).
        try:
            client = client_factory(config["vlm"])
        except ValueError as e:  # unknown vlm.provider
            sys.exit(str(e))
        client.ping()

    photos = load_photos(out_dir)
    if not photos:
        sys.exit(f"No photos.json in {out_dir} - run 'prepare' first.")
    if not (out_dir / GROUPS_FILE).exists():
        sys.exit(f"No {GROUPS_FILE} in {out_dir} - run 'group' first.")
    groups_data = load_groups(out_dir)
    embeddings = load_embeddings(out_dir, config["embedding"]["model_name"])
    if not embeddings:
        sys.exit(f"No embeddings for {config['embedding']['model_name']} in {out_dir} - run 'group' first.")
    people = load_people(out_dir, config["people"]["model_name"]) if config["people"]["enabled"] else {}
    identities = load_identities(out_dir) if config["faces"]["enabled"] else None
    if config["faces"]["enabled"] and identities is None:
        log.warning("No identities.json in %s: faces cannot exclude decided pairs", out_dir)
    signatures = photo_signatures(identities, config["faces"]["min_identity_faces"])

    pairs, stats = select_pairs(photos, embeddings, groups_data, judge_cfg, grouping_cfg, people, signatures,
                                judge_cfg["include_faces_decided"], judge_cfg["max_pairs"])
    photos_by_id = {p["id"]: p for p in photos}
    write_pair_images(out_dir, photos_by_id, pairs, judge_cfg["pair_image_long_edge"])
    save_pairs(out_dir, pairs, stats, judge_cfg, grouping_cfg)
    sheets = write_pairs_sheet(out_dir, pairs, photos_by_id)
    log.info("Judge: %d pairs selected (%d neighbour, %d look-back); excluded faces same %d, different %d, "
             "no people %d; sheet %s", len(pairs), sum(p["kind"] == "neighbour" for p in pairs),
             sum(p["kind"] == "lookback" for p in pairs), stats["excluded_faces_same"],
             stats["excluded_faces_different"], stats["excluded_no_people"],
             ", ".join(str(s) for s in sheets) or "none")
    if dry_run:
        print(format_dry_run(pairs, stats, judge_cfg))
        return {"pairs": pairs, "stats": stats, "verdicts": None}
    if not pairs:
        log.info("Nothing to judge")
        return {"pairs": pairs, "stats": stats, "verdicts": None}

    data = run_judging(out_dir, pairs, client, config["vlm"], judge_cfg["sim_low"], judge_cfg["sim_high"])
    labels = load_labels(out_dir)
    if labels:
        data["labels"] = compare_with_labels(pairs, data["verdicts"], labels, photos)
        save_verdicts(out_dir, data)
        print(format_labels_comparison(data["labels"]))
    else:
        log.info("No labels.json in %s: nothing to compare the verdicts with", out_dir)
    return {"pairs": pairs, "stats": stats, "verdicts": data}
