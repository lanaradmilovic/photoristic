"""Step 2 - grouping: put bursts and near-identical shots into groups.

Grouping runs separately per camera, because the two cameras' clocks are not
synchronized. Within one camera, photos are walked in capture-time order. For each
photo there can be two kinds of candidate groups (see config.yaml, section `grouping`):

  - the previous photo's group, if the photo is close in time and similar to the
    previous photo (`should_join`), and
  - an earlier group the photographer returns to after shooting something else
    ("look-back", `find_lookback_group`). Such groups are not continuous in time.

The photo joins the candidate it is most similar to, or starts a new group.
Afterwards `refine_boundaries` moves a photo at the border of two groups to the
other group if it clearly belongs there (it could not know that while walking,
because the later photos had not been seen yet).

Photos that cannot be grouped safely (failed ingest, no timestamp, no embedding)
become single-photo groups with a flag. Every photo ends up in exactly one group.
"""
import json
import math
import os
from datetime import datetime
from pathlib import Path

import numpy as np

GROUPS_FILE = "groups.json"


def _sort_key(photo):
    return (photo["capture_time"], Path(photo["primary_path"]).name.lower())


def _time(photo):
    return datetime.fromisoformat(photo["capture_time"])


def _similarity(a, b):
    return float(np.dot(a, b))


def _mean_similarity(vec, members, embeddings):
    """Average similarity of a photo to all photos of a group."""
    return float(np.mean([_similarity(vec, embeddings[m["sha256"]]) for m in members]))


def should_join(gap_seconds, sim_prev, mean_sim_group, cfg, no_people=False):
    """Decide whether a photo can continue the previous photo's group.

    `mean_sim_group` is the drift guard: the photo must resemble the group as a
    whole, not only the previous photo, so a slowly changing scene is cut.
    `no_people` is true when neither photo contains a person: decor/food/detail
    shots cannot hit the "different person, same spot" failure, so they may join
    across a longer gap and lower similarity (same subject, different crop).
    """
    if mean_sim_group < cfg["min_mean_similarity_to_group"]:
        return False
    if gap_seconds <= cfg["time_gap_seconds"] and sim_prev >= cfg["similarity_threshold"]:
        return True
    if gap_seconds <= cfg["extended_gap_seconds"] and sim_prev >= cfg["high_similarity_threshold"]:
        return True
    if no_people and gap_seconds <= cfg["nopeople_gap_seconds"] \
            and sim_prev >= cfg["nopeople_similarity_threshold"]:
        return True
    return False


def split_evenly(items, max_size):
    """Split a list into the fewest consecutive chunks of size <= max_size, balanced
    (13 with max 12 -> 7 + 6, not 12 + 1)."""
    n_chunks = math.ceil(len(items) / max_size)
    base, extra = divmod(len(items), n_chunks)
    chunks, start = [], 0
    for i in range(n_chunks):
        size = base + (1 if i < extra else 0)
        chunks.append(items[start:start + size])
        start += size
    return chunks


def split_at_weakest(members, max_size):
    """Split described members into the fewest consecutive chunks of size <= max_size,
    cutting where consecutive similarity is lowest (ties resolve towards balanced
    chunks). Better than a purely even split: the cut lands on a real change of
    framing instead of the middle of a burst of near-identical photos."""
    n = len(members)
    n_chunks = math.ceil(n / max_size)
    if n_chunks == 1:
        return [members]
    # cost of cutting before member i: its similarity to the previous member
    # (cutting between near-identical photos is expensive), plus a small balance
    # term so equal similarities still split evenly.
    target = n / n_chunks

    def cost(i, chunk_len):
        sim = members[i][2] if members[i][2] is not None else 1.0
        return sim + 0.001 * (chunk_len - target) ** 2

    INF = float("inf")
    # best[j][i]: min cost of splitting members[:i] into j chunks (each 1..max_size)
    best = [[INF] * (n + 1) for _ in range(n_chunks + 1)]
    back = [[None] * (n + 1) for _ in range(n_chunks + 1)]
    best[0][0] = 0.0
    for j in range(1, n_chunks + 1):
        for i in range(j, n + 1):
            for prev in range(max(j - 1, i - max_size), i):
                if best[j - 1][prev] == INF:
                    continue
                c = best[j - 1][prev] + (cost(prev, i - prev) if prev else 0.0)
                if c < best[j][i]:
                    best[j][i], back[j][i] = c, prev
    cuts, i = [], n
    for j in range(n_chunks, 0, -1):
        cuts.append(i)
        i = back[j][i]
    cuts = [0] + cuts[::-1]
    return [members[a:b] for a, b in zip(cuts, cuts[1:])]


def find_lookback_group(t, vec, groups, embeddings, cfg, exclude=None, photo_no_people=False,
                        group_no_people=None):
    """Find an earlier group of the same camera this photo returns to.

    `groups` is a list of lists of photos. A group qualifies if:
      - its last photo is at most `lookback_seconds` old,
      - the group would not span more than `max_group_span_seconds`,
      - the photo passes the drift guard (`min_mean_similarity_to_group`), and
      - the photo's best match among the group's photos has similarity
        >= `lookback_similarity_threshold`.
    `exclude` is a group index to skip (the one the neighbour rule already accepted).
    When the photo and every photo of the earlier group are free of people
    (`photo_no_people`, `group_no_people(gi)`), the lower
    `nopeople_lookback_similarity_threshold` applies (see `should_join`).

    Returns (group index, best similarity) or None.
    """
    if cfg["lookback_seconds"] <= 0:
        return None
    best = None
    for gi, members in enumerate(groups):
        if gi == exclude:
            continue
        if (t - _time(members[-1])).total_seconds() > cfg["lookback_seconds"]:
            continue
        if (t - _time(members[0])).total_seconds() > cfg["max_group_span_seconds"]:
            continue
        if _mean_similarity(vec, members, embeddings) < cfg["min_mean_similarity_to_group"]:
            continue
        threshold = cfg["lookback_similarity_threshold"]
        if photo_no_people and group_no_people is not None and group_no_people(gi):
            threshold = cfg["nopeople_lookback_similarity_threshold"]
        sim = max(_similarity(vec, embeddings[m["sha256"]]) for m in members)
        if sim >= threshold and (best is None or sim > best[1]):
            best = (gi, sim)
    return best


def _assign(photos, embeddings, cfg, people=None):
    """Walk photos in time order and put each into a group.

    `people` maps sha256 -> True if the photo contains a person; a missing entry
    counts as "has people" (the conservative assumption).
    Returns (groups, how): groups is a list of lists of photos; how maps photo id to
    "start", "neighbour" or "lookback" (how the photo joined its group).
    """
    people = people or {}

    def no_people(p):
        return people.get(p["sha256"], True) is False

    groups, group_of, how = [], {}, {}
    prev = None
    for photo in photos:
        t = _time(photo)
        vec = embeddings[photo["sha256"]]
        photo_np = no_people(photo)
        candidates = []  # (similarity, group index, how)
        if prev is not None:
            prev_gi = group_of[prev["id"]]
            gap = (t - _time(prev)).total_seconds()
            sim_prev = _similarity(vec, embeddings[prev["sha256"]])
            mean_sim = _mean_similarity(vec, groups[prev_gi], embeddings)
            if should_join(gap, sim_prev, mean_sim, cfg, no_people=photo_np and no_people(prev)):
                # Rank by best match in the group, the same measure the look-back uses.
                sim_group = max(_similarity(vec, embeddings[m["sha256"]]) for m in groups[prev_gi])
                candidates.append((sim_group, prev_gi, "neighbour"))
            # Also look back, even when the neighbour rule passed: an earlier group may fit better.
            exclude = prev_gi if candidates else None
            found = find_lookback_group(
                t, vec, groups, embeddings, cfg, exclude=exclude, photo_no_people=photo_np,
                group_no_people=lambda gi: all(no_people(m) for m in groups[gi]))
            if found:
                candidates.append((found[1], found[0], "lookback"))

        if candidates:
            _, gi, kind = max(candidates)  # the most similar candidate wins
            groups[gi].append(photo)
        else:
            groups.append([photo])
            gi, kind = len(groups) - 1, "start"
        group_of[photo["id"]] = gi
        how[photo["id"]] = kind
        prev = photo
    return groups, how


def refine_boundaries(groups, how, embeddings, cfg):
    """Move a photo at the border of two consecutive groups to the other group when
    its mean similarity there is higher by more than `refine_margin`.

    Example: A A A | B B where the last A looks more like the Bs than like the other
    As. While walking, the last A could only be compared with photos taken before it.
    Moved photos are marked "moved" in `how`.
    """
    if not cfg["refine_boundaries"]:
        return groups
    margin = cfg["refine_margin"]

    def clearly_closer(photo, other_group, own_rest):
        vec = embeddings[photo["sha256"]]
        return _mean_similarity(vec, other_group, embeddings) > \
            _mean_similarity(vec, own_rest, embeddings) + margin

    for _ in range(2):
        ordered = sorted(groups, key=lambda g: _time(g[0]))
        for a, b in zip(ordered, ordered[1:]):
            # Only real borders: A ends before B starts, and not too far apart.
            gap = (_time(b[0]) - _time(a[-1])).total_seconds()
            if gap < 0 or gap > cfg["extended_gap_seconds"]:
                continue
            if len(a) > 1 and clearly_closer(a[-1], b, a[:-1]):
                b.insert(0, a.pop())
                how[b[0]["id"]] = "moved"
            elif len(b) > 1 and clearly_closer(b[0], a, b[1:]):
                a.append(b.pop(0))
                how[a[-1]["id"]] = "moved"
    return [g for g in groups if g]


def _describe(groups, how, photos, embeddings):
    """Turn groups of photos into groups of members (photo, gap_s, sim, how) for groups.json.

    First member: gap/sim to the previous photo of the camera (why the group starts there).
    Other members: gap since the previous photo of the group, and similarity to it;
    for "lookback" photos the similarity to the best-matching earlier photo of the group.
    """
    previous_of = {p["id"]: (photos[i - 1] if i else None) for i, p in enumerate(photos)}
    described = []
    for group in groups:
        group = sorted(group, key=_sort_key)
        members = []
        for k, photo in enumerate(group):
            vec = embeddings[photo["sha256"]]
            if k == 0:
                prev = previous_of[photo["id"]]
                kind = "moved" if how[photo["id"]] == "moved" else "start"
                if prev is None:
                    members.append((photo, None, None, kind))
                else:
                    members.append((photo, (_time(photo) - _time(prev)).total_seconds(),
                                    _similarity(vec, embeddings[prev["sha256"]]), kind))
                continue
            kind = how[photo["id"]]
            if kind == "start":  # became a later member after a boundary move
                kind = "neighbour" if previous_of[photo["id"]] is group[k - 1] else "lookback"
            gap = (_time(photo) - _time(group[k - 1])).total_seconds()
            if kind == "lookback":
                sim = max(_similarity(vec, embeddings[m["sha256"]]) for m in group[:k])
            else:
                sim = _similarity(vec, embeddings[group[k - 1]["sha256"]])
            members.append((photo, gap, sim, kind))
        described.append(members)
    return described


def _group_one_camera(photos, embeddings, cfg, people=None):
    """Group the photos of one camera; returns a list of member lists (see _describe)."""
    photos = sorted(photos, key=_sort_key)
    groups, how = _assign(photos, embeddings, cfg, people)
    groups = refine_boundaries(groups, how, embeddings, cfg)
    return _describe(groups, how, photos, embeddings)


def _make_group(camera_id, members, flags):
    photos = [m[0] for m in members]
    # The first member's gap/similarity refer to the previous group, so skip it.
    sims = [round(m[2], 4) for m in members[1:]]
    gaps = [round(m[1], 3) for m in members[1:]]
    joined_by = [m[3] for m in members[1:]]
    times = [p["capture_time"] for p in photos if p.get("capture_time")]
    flags = list(flags)
    if "lookback" in joined_by:
        flags.append("lookback")
    if "moved" in joined_by or (members and members[0][3] == "moved"):
        flags.append("moved")
    return {
        "group_id": None,
        "camera_id": camera_id,
        "photo_ids": [p["id"] for p in photos],
        "size": len(photos),
        "start": min(times) if times else None,
        "end": max(times) if times else None,
        "consecutive_similarities": sims,
        "consecutive_gaps_seconds": gaps,
        # How each photo after the first joined: "neighbour", "lookback" (returned to the
        # scene) or "moved" (moved here from the neighbouring group by refine_boundaries).
        "joined_by": joined_by,
        "min_similarity": min(sims) if sims else None,
        # Similarity/gap to the previous photo of the same camera, even across groups.
        "boundary_similarity": round(members[0][2], 4) if members[0][2] is not None else None,
        "boundary_gap_seconds": round(members[0][1], 3) if members[0][1] is not None else None,
        "split_from": None,
        "split_part": None,
        "flags": flags,
    }


def group_photos(photos, embeddings, cfg, people=None):
    """Group photos. `embeddings` maps sha256 -> unit vector; `cfg` is config['grouping'];
    `people` maps sha256 -> True/False (photo contains a person); None or a missing
    entry means "assume people" and keeps the strict thresholds."""
    groupable, singles = {}, []
    for p in photos:
        if p["status"] != "ok":
            singles.append((p, ["ingest_error"]))
        elif not p.get("capture_time"):
            singles.append((p, ["no_timestamp"]))
        elif p["sha256"] not in embeddings:
            singles.append((p, ["no_embedding"]))
        else:
            groupable.setdefault(p["camera_id"] or "unknown-camera", []).append(p)

    groups = []
    for camera_id in sorted(groupable):
        for members in _group_one_camera(groupable[camera_id], embeddings, cfg, people):
            max_size = cfg.get("max_group_size") or 0
            if max_size <= 0 or len(members) <= max_size:
                groups.append(_make_group(camera_id, members, []))
                continue
            chunks = split_at_weakest(members, max_size)
            parts = [_make_group(camera_id, chunk, ["split"]) for chunk in chunks]
            for i, part in enumerate(parts, start=1):
                part["split_part"] = [i, len(parts)]
                part["_split_family"] = id(members)
            groups.extend(parts)

    groups.sort(key=lambda g: (g["camera_id"], g["start"]))
    for p, flags in sorted(singles, key=lambda s: s[0]["primary_path"]):
        groups.append(_make_group(p["camera_id"] or "unknown-camera", [(p, None, None, "start")], flags))

    for i, g in enumerate(groups, start=1):
        g["group_id"] = f"g{i:04d}"
    first_of_family = {}
    for g in groups:
        family = g.pop("_split_family", None)
        if family is not None:
            first_of_family.setdefault(family, g["group_id"])
            g["split_from"] = first_of_family[family]

    check_every_photo_once(photos, groups)
    return groups


def check_every_photo_once(photos, groups):
    """Safety invariant: grouping must never lose or duplicate a photo."""
    ids = [pid for g in groups for pid in g["photo_ids"]]
    expected = sorted(p["id"] for p in photos)
    if sorted(ids) != expected or len(ids) != len(set(ids)):
        missing = set(expected) - set(ids)
        raise AssertionError(
            f"Grouping invariant broken: {len(expected)} photos, {len(ids)} grouped, "
            f"missing={sorted(missing)[:10]}"
        )


def save_groups(out_dir, groups, cfg):
    path = Path(out_dir) / GROUPS_FILE
    tmp = path.with_suffix(".tmp")
    data = {
        "created": datetime.now().isoformat(timespec="seconds"),
        "config_used": dict(cfg),
        "n_groups": len(groups),
        "n_photos": sum(g["size"] for g in groups),
        "groups": groups,
    }
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)
    os.replace(tmp, path)


def load_groups(out_dir):
    with open(Path(out_dir) / GROUPS_FILE, encoding="utf-8") as f:
        return json.load(f)
