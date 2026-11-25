"""Step 3 - pick the best photo(s) of every group.

A group (decision 0014) is the same main people in the same moment at the same place,
so it may hold frames the agency would deliver side by side: a wide and a tight
framing, a vertical and a horizontal one. It may also be a grouping mistake (two group
photos that differ by one person). How many photos a group keeps is therefore decided
by code, and the model only ranks frames that code already considers interchangeable
(decision 0022):

  split_variants   a group -> variants: frames that are near-duplicates of each other
                   (DINOv2 similarity to EVERY frame of the variant, same orientation,
                   no difference in identified people)
  PROMPT, build_schema, parse_answer
                   one request per variant with two or more frames: every frame as its
                   own numbered image; the model returns the order, best first, and the
                   main flaw of each frame
  decide           the safety rules (decision 0019): the best frame of every variant is
                   `keep`, everything else is `maybe`. Nothing is rejected in this
                   version, and a variant without a valid answer is `maybe` as a whole.
  run_ranking      the loop: retries, a save after every request, resume

Output: ranking.json (see docs/spec/vlm-scoring.md). Answers are stored per variant
under a key made of the member photos' sha256, so they survive a re-grouping that
leaves the variant unchanged.

Privacy: the images leave the machine only towards `vlm.base_url` (the user's own
server). Nothing of the images or the prompt is logged.
"""
import hashlib
import io
import json
import logging
import math
import sys
import time
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw

from culling.embed import load_cache as load_embeddings
from culling.faces import load_identities, photo_signatures
from culling.grouping import GROUPS_FILE, identity_relation, load_groups
from culling.ingest import load_photos
from culling.judge import PATCH_PX, _font, _now, _write_json
from culling.vlm import VLMError, VLMUnavailable, make_client

log = logging.getLogger(__name__)

RANKING_FILE = "ranking.json"
ISSUES = ("none", "eyes_closed", "blurred", "bad_expression", "obstructed", "exposure")
REVIEW_FLAGS = ("no_timestamp", "preview_fallback")  # photos flagged by ingest always go to review
TEXT_TOKENS = 350      # prompt + chat template, on top of the image tokens
TOKENS_PER_PHOTO = 30  # answer: one {"photo", "issue"} object and one number in `order`

# The prompt does not ask whether the frames show the same people or the same moment:
# the judge run showed that this model cannot tell (docs/research/2026-11-11-judge-first-
# real-run.md), so code decides what is compared (split_variants). There is no confidence
# field either: the model answered 0.95-0.99 for everything. "Main people" is spelled out
# because other culling tools reject a sharp couple for a blurred guest in the background
# (docs/research/2026-11-10-culling-complaints.md).
PROMPT = """These {n} wedding photos are numbered 1 to {n} in the top-left corner. The same \
photographer took them within {span} seconds; they show the same people in the same moment. \
The photographer will deliver the best one.

Answer with JSON:
- photos: for every photo, in the order 1 to {n}, its number and "issue": the most serious flaw of \
the MAIN people in it (ignore guests in the background). "eyes_closed": a main person blinks. \
"blurred": the main people are out of focus or motion-blurred. "bad_expression": an awkward face, \
mouth or grimace. "obstructed": a main person is covered or cut off. "exposure": far too dark or \
too bright. Otherwise "none".
- order: all photo numbers from the best to the worst. The best photo has the main people sharp, \
with open eyes and the best expression and emotion, at the peak of the action rather than just \
before or after it; then the better composition.
- reason: why the first photo is the best, fewer than 15 words."""


def build_schema(n):
    """The JSON schema of the answer for a variant of `n` photos."""
    number = {"type": "integer", "minimum": 1, "maximum": n}
    return {
        "type": "object",
        "properties": {
            "photos": {"type": "array", "minItems": n, "maxItems": n, "items": {
                "type": "object",
                "properties": {"photo": number, "issue": {"type": "string", "enum": list(ISSUES)}},
                "required": ["photo", "issue"], "additionalProperties": False}},
            "order": {"type": "array", "minItems": n, "maxItems": n, "items": number},
            "reason": {"type": "string"},
        },
        "required": ["photos", "order", "reason"],
        "additionalProperties": False,
    }


def prompt_hash():
    """Short hash of PROMPT and the schema: answers of another prompt must not be resumed."""
    text = PROMPT + json.dumps(build_schema(2), sort_keys=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


# -------------------------------------------------------------------- variants

def _name(photo):
    return Path(photo["primary_path"]).name if photo.get("primary_path") else photo["id"]


def orientation(photo):
    """"portrait" / "landscape" from the oriented preview; None when its size is unknown."""
    w, h = photo.get("preview_w"), photo.get("preview_h")
    if not w or not h:
        return None
    return "portrait" if h > w else "landscape"


def needs_review(photo, embeddings):
    """Photos that are never compared: ingest failed or flagged them, or there is nothing
    to compare (no embedding, no preview). They go to review on their own."""
    return (photo.get("status") != "ok" or not photo.get("preview_file")
            or photo.get("sha256") not in embeddings
            or any(f in REVIEW_FLAGS for f in photo.get("flags") or []))


def split_variants(members, embeddings, signatures, cfg):
    """Split the photos of one group (capture order) into variants: lists of frames that
    are interchangeable enough for the model to pick one.

    A photo joins an existing variant only if it is compatible with EVERY photo in it
    (so a slowly changing series does not chain into one variant):
      - DINOv2 similarity >= ranking.variant_similarity;
      - the same orientation (ranking.variant_split_orientation): a vertical and a
        horizontal frame of one moment are both kept;
      - no difference in identified people (ranking.variant_split_people): a known person
        present in one photo and absent in the other. A head turned away also looks like
        that; the cost is one more `keep`, never a lost photo.
    With ranking.variant_max_gap_seconds above 0 the photo must also follow the variant's
    last photo within that many seconds: only frames of one burst are interchangeable
    (decision 0027).
    Among several compatible variants the one with the highest weakest similarity wins.
    A variant longer than ranking.max_images is cut into consecutive parts of at most
    that size, each with its own winner. Returns the variants ordered by first photo.
    """
    threshold = float(cfg["variant_similarity"])
    signatures = signatures or {}

    def compatible(a, b):
        sim = float(embeddings[a["sha256"]] @ embeddings[b["sha256"]])
        if sim < threshold:
            return None
        if cfg["variant_split_orientation"] and None not in (orientation(a), orientation(b)) \
                and orientation(a) != orientation(b):
            return None
        if cfg["variant_split_people"] and identity_relation(
                signatures.get(a["sha256"]), signatures.get(b["sha256"]), partial_blocks=True) == "different":
            return None
        return sim

    max_gap = float(cfg["variant_max_gap_seconds"])

    def in_burst(photo, variant):
        if max_gap <= 0 or not photo.get("capture_time") or not variant[-1].get("capture_time"):
            return True
        gap = datetime.fromisoformat(photo["capture_time"]) - datetime.fromisoformat(variant[-1]["capture_time"])
        return abs(gap.total_seconds()) <= max_gap

    variants = []
    for photo in members:
        best, best_sim = None, None
        for variant in variants:
            if not in_burst(photo, variant):
                continue
            sims = [compatible(photo, other) for other in variant]
            if None not in sims and (best is None or min(sims) > best_sim):
                best, best_sim = variant, min(sims)
        if best is None:
            variants.append([photo])
        else:
            best.append(photo)
    size = max(2, int(cfg["max_images"]))
    return [v[k:k + size] for v in variants for k in range(0, len(v), size)]


def variant_key(members):
    """Stable id of a variant: a hash of its photos' sha256, in order."""
    text = "|".join(p["sha256"] for p in members)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def build_variants(photos, groups_data, embeddings, signatures, cfg):
    """Every photo of groups.json in exactly one variant. A variant is {key, group_id,
    index (1-based in its group), kind, photo_ids, names, span_seconds}; kind is
    "review" (a photo that is never compared, alone), "single" or "multi"."""
    by_id = {p["id"]: p for p in photos}
    out = []
    for group in groups_data["groups"]:
        members = [by_id[pid] for pid in group["photo_ids"] if pid in by_id]
        review = [p for p in members if needs_review(p, embeddings)]
        usable = [p for p in members if not needs_review(p, embeddings)]
        parts = [("review", [p]) for p in review]
        parts += [("multi" if len(v) > 1 else "single", v) for v in split_variants(usable, embeddings, signatures, cfg)]
        order = {p["id"]: i for i, p in enumerate(members)}
        parts.sort(key=lambda part: order[part[1][0]["id"]])
        for index, (kind, variant) in enumerate(parts, start=1):
            times = [datetime.fromisoformat(p["capture_time"]) for p in variant if p.get("capture_time")]
            out.append({
                "key": variant_key(variant) if kind != "review" else f"review-{variant[0]['id']}",
                "group_id": group["group_id"], "index": index, "kind": kind,
                "photo_ids": [p["id"] for p in variant], "names": [_name(p) for p in variant],
                "span_seconds": round((max(times) - min(times)).total_seconds(), 1) if times else 0.0,
            })
    return out


# ---------------------------------------------------------------------- images

def numbered_image(out_dir, photo, number, long_edge):
    """The preview scaled to `long_edge` with a black box holding a white number in the
    top-left corner, as JPEG bytes. Scaled down only, never cropped."""
    with Image.open(Path(out_dir) / photo["preview_file"]) as img:
        img = img.convert("RGB")
    img.thumbnail((long_edge, long_edge), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(img)
    font = _font(max(12, int(long_edge * 0.05)))
    pad = max(3, long_edge // 100)
    left, top, right, bottom = draw.textbbox((0, 0), str(number), font=font)
    box = [8, 8, 8 + (right - left) + 2 * pad, 8 + (bottom - top) + 2 * pad]
    draw.rectangle(box, fill="black")
    draw.text((box[0] + pad - left, box[1] + pad - top), str(number), fill="white", font=font)
    buffer = io.BytesIO()
    img.save(buffer, "JPEG", quality=90)
    return buffer.getvalue()


def estimate_tokens(photos, long_edge):
    """Prompt + answer tokens of one request for Qwen3.5: one visual token per 32x32 px
    of every image (a 3:2 frame when the preview size is unknown) plus the text."""
    total = TEXT_TOKENS
    for p in photos:
        w, h = p.get("preview_w") or 3, p.get("preview_h") or 2
        scale = min(1.0, long_edge / max(w, h)) if max(w, h) > 3 else long_edge / 3
        total += math.ceil(w * scale / PATCH_PX) * math.ceil(h * scale / PATCH_PX) + TOKENS_PER_PHOTO
    return total


# --------------------------------------------------------------------- answers

def parse_answer(text, n):
    """The model's answer -> {order: [numbers 1..n, best first], issues: [issue of photo
    1..n, None when missing], reason, repaired}. Accepts a ``` fence around the JSON.

    Only the first place must be right: a number repeated later in `order` is dropped and
    numbers the model left out are appended in photo order (`repaired` is then True), as
    every photo after the first is `maybe` anyway. Raises ValueError when the answer is not
    JSON, has no usable first place or no reason (the caller retries)."""
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
    raw = data.get("order")
    if not isinstance(raw, list) or not raw:
        raise ValueError("order must be a non-empty list")

    def valid(number):
        return isinstance(number, int) and not isinstance(number, bool) and 1 <= number <= n

    if not valid(raw[0]):
        raise ValueError(f"order must start with a photo number from 1 to {n}, got {str(raw[0])[:40]!r}")
    order = []
    for number in raw:
        if valid(number) and number not in order:
            order.append(number)
    missing = [k for k in range(1, n + 1) if k not in order]
    issues = [None] * n
    entries = data.get("photos")
    for entry in entries if isinstance(entries, list) else []:
        if isinstance(entry, dict) and valid(entry.get("photo")) and entry.get("issue") in ISSUES:
            issues[entry["photo"] - 1] = entry["issue"]
    reason = data.get("reason")
    if not isinstance(reason, str):
        raise ValueError("reason must be a string")
    return {"order": order + missing, "issues": issues, "reason": reason.strip(),
            "repaired": bool(missing) or len(order) != len(raw)}


def rank_variant(client, variant, images, max_retries):
    """Ask the model to order the photos of one variant. Up to 1 + max_retries attempts
    when a request fails (VLMError) or the answer is unusable (ValueError); after that the
    answer has an `error` and no order. VLMUnavailable is not retried: the server is gone,
    the caller stops and resumes later. Returns the stored answer: photo ids, not numbers."""
    n = len(images)
    prompt = PROMPT.format(n=n, span=f"{variant['span_seconds']:.0f}")
    started = time.time()
    attempts, last_error, parsed = 0, None, None
    while parsed is None and attempts <= max_retries:
        attempts += 1
        try:
            parsed = parse_answer(client.ask(prompt, images, build_schema(n), schema_name="group_ranking",
                                             max_tokens=80 + 2 * TOKENS_PER_PHOTO * n), n)
        except VLMUnavailable:
            raise
        except (VLMError, ValueError) as e:
            last_error = e
            log.warning("%s variant %d (%s ...), attempt %d of %d failed: %s", variant["group_id"],
                        variant["index"], variant["names"][0], attempts, 1 + max_retries, e)
    answer = {"group_id": variant["group_id"], "photo_ids": variant["photo_ids"], "names": variant["names"],
              "attempts": attempts, "elapsed_s": round(time.time() - started, 2), "ranked_at": _now()}
    if parsed is None:
        return {**answer, "order": None, "error": f"{type(last_error).__name__}: {str(last_error)[:200]}"}
    usage = getattr(client, "last_usage", None) or {}
    ids = variant["photo_ids"]
    return {**answer, "order": [ids[k - 1] for k in parsed["order"]],
            "issues": {ids[k]: issue for k, issue in enumerate(parsed["issues"])},
            "reason": parsed["reason"], "repaired": parsed["repaired"],
            "prompt_tokens": usage.get("prompt_tokens"), "completion_tokens": usage.get("completion_tokens")}


def answered(answer, variant):
    """Whether `answer` is a usable ranking of exactly this variant's photos."""
    return bool(answer) and bool(answer.get("order")) and sorted(answer["order"]) == sorted(variant["photo_ids"])


# ---------------------------------------------------------------- safety rules

def decide(variants, answers):
    """The decision for every photo, from the variants and the model's answers. These are
    the safety rules of decision 0019, applied in code after the answer:

      - a photo that is never compared (ingest flag, no preview)   -> maybe, "flagged"
      - the only frame of its variant                              -> keep,  "only_frame"
      - the first of the model's order in a variant                -> keep,  "best_of_variant"
      - every other ranked photo                                   -> maybe, "ranked_lower"
      - a variant without a valid answer (not asked yet, or error) -> maybe for all of it

    There is no `reject`: the model's confidence carries no information, so nothing is
    removed from review until phase 5 has measured it. Returns {photo_id: {group_id,
    variant, decision, rank, issue, why}}; rank is None where nothing was ranked."""
    out = {}
    for v in variants:
        answer = answers.get(v["key"])
        base = {"group_id": v["group_id"], "variant": v["index"]}
        if v["kind"] == "review":
            out[v["photo_ids"][0]] = {**base, "decision": "maybe", "rank": None, "issue": None, "why": "flagged"}
        elif v["kind"] == "single":
            out[v["photo_ids"][0]] = {**base, "decision": "keep", "rank": 1, "issue": None, "why": "only_frame"}
        elif answered(answer, v):
            for rank, pid in enumerate(answer["order"], start=1):
                out[pid] = {**base, "decision": "keep" if rank == 1 else "maybe", "rank": rank,
                            "issue": (answer.get("issues") or {}).get(pid),
                            "why": "best_of_variant" if rank == 1 else "ranked_lower"}
        else:
            why = "no_valid_answer" if answer and answer.get("error") else "not_ranked"
            for pid in v["photo_ids"]:
                out[pid] = {**base, "decision": "maybe", "rank": None, "issue": None, "why": why}
    return out


# ----------------------------------------------------------------------- files

def load_ranking(out_dir):
    path = Path(out_dir) / RANKING_FILE
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_ranking(out_dir, data):
    data["updated"] = _now()
    _write_json(Path(out_dir) / RANKING_FILE, data)


def ranking_for_report(out_dir, groups_data):
    """ranking.json -> {photo_id: decision record} for report.html, or None when there is
    no ranking or it belongs to another grouping (the groups were rebuilt since)."""
    data = load_ranking(out_dir)
    if not data:
        return None
    if data.get("groups_created") != groups_data.get("created"):
        log.warning("%s was made for another grouping; rerun 'rank' to show it in the report", RANKING_FILE)
        return None
    return data.get("photos") or None


def summarise(variants, decisions, todo, photos_by_id, long_edge):
    kinds = {k: [v for v in variants if v["kind"] == k] for k in ("single", "multi", "review")}
    tokens = sorted(estimate_tokens([photos_by_id[pid] for pid in v["photo_ids"]], long_edge) for v in todo)
    return {
        "photos": len(decisions), "groups": len({v["group_id"] for v in variants}), "variants": len(variants),
        "single_variants": len(kinds["single"]), "multi_variants": len(kinds["multi"]),
        "photos_in_multi_variants": sum(len(v["photo_ids"]) for v in kinds["multi"]),
        "largest_variant": max((len(v["photo_ids"]) for v in variants), default=0),
        "review_photos": len(kinds["review"]),
        "keep": sum(1 for d in decisions.values() if d["decision"] == "keep"),
        "maybe": sum(1 for d in decisions.values() if d["decision"] == "maybe"),
        "not_ranked_photos": sum(1 for d in decisions.values() if d["why"] in ("not_ranked", "no_valid_answer")),
        "requests_to_send": len(todo), "tokens_to_send": sum(tokens), "largest_request_tokens": tokens[-1] if tokens else 0,
    }


def format_summary(s, cfg, dry_run):
    """`keep` after a full run = single variants + multi variants (one winner each)."""
    final_keep = s["single_variants"] + s["multi_variants"]
    lines = [f"Ranking{' dry-run' if dry_run else ''}: {s['photos']} photos in {s['groups']} groups -> "
             f"{s['variants']} variants (variant_similarity {cfg['variant_similarity']})",
             f"  single-frame variants   {s['single_variants']:5}   keep without asking the model",
             f"  multi-frame variants    {s['multi_variants']:5}   {s['photos_in_multi_variants']} photos, largest "
             f"{s['largest_variant']}; one request and one keep each",
             f"  flagged photos          {s['review_photos']:5}   always review",
             f"now: keep {s['keep']}, maybe {s['maybe']} ({s['not_ranked_photos']} of them not ranked yet)",
             f"after a full run: keep {final_keep} of {s['photos']} "
             f"({100 * final_keep / max(s['photos'], 1):.0f} %), the rest maybe, ordered inside each variant"]
    if s["requests_to_send"]:
        lines.append(f"{'would send' if dry_run else 'still to send'}: {s['requests_to_send']} requests, "
                     f"~{s['tokens_to_send']} tokens, largest request ~{s['largest_request_tokens']} tokens")
    lines.append(f"file: {RANKING_FILE}" + ("; no request was sent" if dry_run else ""))
    return "\n".join(lines)


# ---------------------------------------------------------------- orchestrator

def run_ranking(out_dir, config, dry_run=False, max_requests=None, client_factory=make_client):
    """Split the groups into variants, ask the model about every multi-frame variant
    that has no valid answer yet, apply the safety rules and write ranking.json after
    every request, so an interrupted run resumes. With `dry_run` nothing is sent: the
    variants and the decisions so far are written and the summary printed.
    `max_requests` (> 0) stops after that many requests. Returns the file content."""
    out_dir = Path(out_dir)
    cfg, vlm_cfg = config["ranking"], config["vlm"]
    client = None
    if not dry_run:
        try:
            client = client_factory(vlm_cfg)
        except ValueError as e:  # unknown vlm.provider
            sys.exit(str(e))
        client.ping()  # fail fast, before any other work

    photos = load_photos(out_dir)
    if not photos:
        sys.exit(f"No photos.json in {out_dir} - run 'prepare' first.")
    if not (out_dir / GROUPS_FILE).exists():
        sys.exit(f"No {GROUPS_FILE} in {out_dir} - run 'group' first.")
    groups_data = load_groups(out_dir)
    embeddings = load_embeddings(out_dir, config["embedding"]["model_name"])
    if not embeddings:
        sys.exit(f"No embeddings for {config['embedding']['model_name']} in {out_dir} - run 'group' first.")
    identities = load_identities(out_dir) if config["faces"]["enabled"] else None
    signatures = photo_signatures(identities, config["faces"]["min_identity_faces"])
    photos_by_id = {p["id"]: p for p in photos}
    variants = build_variants(photos, groups_data, embeddings, signatures, cfg)

    data = load_ranking(out_dir) or {"created": _now(), "answers": {}}
    answers = data.setdefault("answers", {})
    if client is not None and answers:
        if data.get("model") != client.model:
            sys.exit(f"{out_dir / RANKING_FILE} holds answers of {data.get('model')}; move or delete it "
                     f"before ranking with {client.model}.")
        if data.get("prompt_hash") != prompt_hash():
            sys.exit(f"{out_dir / RANKING_FILE} holds answers of another prompt (hash {data.get('prompt_hash')}, "
                     f"now {prompt_hash()}); move or delete it before ranking, so the two are not mixed.")
    if client is not None:
        data.update(model=client.model, base_url=client.base_url, prompt_hash=prompt_hash())
    data.update(groups_created=groups_data.get("created"),
                config={**cfg, "image_long_edge": vlm_cfg["image_long_edge"]},
                variants=variants)

    todo = [v for v in variants if v["kind"] == "multi" and not answered(answers.get(v["key"]), v)]
    if max_requests and len(todo) > max_requests:
        log.info("Ranking: %d of %d open requests this run (--max-requests)", max_requests, len(todo))
        todo = todo[:max_requests]

    def save():
        data["photos"] = decide(variants, answers)
        save_ranking(out_dir, data)

    if dry_run:
        save()
        summary = summarise(variants, data["photos"], todo, photos_by_id, vlm_cfg["image_long_edge"])
        print(format_summary(summary, cfg, True))
        return data

    log.info("Ranking %d variants with %s at %s", len(todo), client.model, client.base_url)
    for n, variant in enumerate(todo, start=1):
        images = [numbered_image(out_dir, photos_by_id[pid], k, int(vlm_cfg["image_long_edge"]))
                  for k, pid in enumerate(variant["photo_ids"], start=1)]
        try:
            answer = rank_variant(client, variant, images, int(vlm_cfg["max_retries"]))
        except VLMUnavailable as e:
            log.error("VLM server gone after %d of %d requests (%s); progress is saved in %s, rerun to resume",
                      n - 1, len(todo), e, RANKING_FILE)
            save()
            raise
        answers[variant["key"]] = answer
        save()
        best = answer["names"][answer["photo_ids"].index(answer["order"][0])] if answer["order"] else "no valid answer"
        log.info("[%d/%d] %s variant %d, %d photos: best %s (%d attempt(s), %.1f s, %s prompt tokens)",
                 n, len(todo), variant["group_id"], variant["index"], len(images), best,
                 answer["attempts"], answer["elapsed_s"], answer.get("prompt_tokens"))
    save()
    left = [v for v in variants if v["kind"] == "multi" and not answered(answers.get(v["key"]), v)]
    print(format_summary(summarise(variants, data["photos"], left, photos_by_id, vlm_cfg["image_long_edge"]),
                         cfg, False))
    return data
