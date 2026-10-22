import hashlib
from datetime import datetime, timedelta

import numpy as np
import pytest

from culling.config import DEFAULTS
from culling.grouping import check_every_photo_once, group_photos, identity_relation, split_evenly

T0 = datetime(2024, 6, 15, 16, 0, 0)
DIM = 16
CFG = dict(DEFAULTS["grouping"])


def unit(i):
    v = np.zeros(DIM, np.float32)
    v[i] = 1.0
    return v


def mix(base, other, sim):
    """Unit vector with cosine similarity `sim` to `base` (base and other orthonormal)."""
    v = sim * base + np.sqrt(1 - sim ** 2) * other
    return (v / np.linalg.norm(v)).astype(np.float32)


class Shoot:
    """Builds synthetic photo records + embeddings."""

    def __init__(self):
        self.photos, self.embeddings = [], {}

    def add(self, seconds, vec, camera="SN1", status="ok", time=True):
        n = len(self.photos)
        sha = hashlib.sha256(str(n).encode()).hexdigest()
        self.photos.append({
            "id": sha[:16], "sha256": sha, "primary_path": f"C:/w/DSC_{n:04d}.NEF",
            "nef_path": f"C:/w/DSC_{n:04d}.NEF", "jpg_path": None,
            "capture_time": (T0 + timedelta(seconds=seconds)).isoformat() if time else None,
            "camera_id": camera, "status": status, "flags": [],
        })
        if status == "ok":
            self.embeddings[sha] = vec
        return sha[:16]

    def groups(self, **overrides):
        return group_photos(self.photos, self.embeddings, {**CFG, **overrides})


def ids_per_group(groups):
    return [g["photo_ids"] for g in groups]


def test_burst_of_similar_photos_is_one_group():
    s = Shoot()
    ids = [s.add(i * 0.2, mix(unit(0), unit(1), 0.97)) for i in range(5)]
    assert ids_per_group(s.groups()) == [ids]


def test_large_time_gap_splits_even_identical_photos():
    s = Shoot()
    a = s.add(0, unit(0))
    b = s.add(300, unit(0))  # beyond extended_gap_seconds and lookback_seconds
    assert ids_per_group(s.groups()) == [[a], [b]]


def test_different_content_splits_even_within_a_burst():
    s = Shoot()
    a = s.add(0.0, unit(0))
    b = s.add(0.3, unit(1))
    assert ids_per_group(s.groups()) == [[a], [b]]


def test_extended_gap_needs_high_similarity():
    s = Shoot()
    a = s.add(0, unit(0))
    b = s.add(8, mix(unit(0), unit(1), 0.95))   # 8 s, very similar -> joins
    c = s.add(16, mix(unit(0), unit(2), 0.80))  # 8 s, only medium similar -> new group
    assert ids_per_group(s.groups()) == [[a, b], [c]]


def test_lookback_returns_to_earlier_scene():
    # Scene A, then something else, then scene A again 20 s later.
    s = Shoot()
    a1 = s.add(0, unit(0))
    other = s.add(10, unit(1))
    a2 = s.add(20, mix(unit(0), unit(2), 0.95))
    groups = s.groups()
    assert ids_per_group(groups) == [[a1, a2], [other]]
    assert groups[0]["joined_by"] == ["lookback"]
    assert "lookback" in groups[0]["flags"]
    assert groups[0]["consecutive_gaps_seconds"] == [20.0]


def test_lookback_needs_high_similarity():
    # 0.87 is typical for a DIFFERENT person at the same spot: must not be merged.
    s = Shoot()
    a1 = s.add(0, unit(0))
    other = s.add(10, unit(1))
    a2 = s.add(20, mix(unit(0), unit(2), 0.87))  # below lookback_similarity_threshold 0.90
    assert ids_per_group(s.groups()) == [[a1], [other], [a2]]


def test_photo_joins_the_most_similar_group_not_just_the_neighbour():
    # p1 starts its own group (16 s gap, only 0.79 to p0). p2 fits p1 by the neighbour
    # rule (0.84 after 8 s) but is much more similar to p0 (0.92): it must join p0.
    s = Shoot()
    p0 = s.add(0, np.array([1, 0, 0] + [0] * (DIM - 3), np.float32))
    p1 = s.add(16, np.array([0.79, 0.2888, 0.5408] + [0] * (DIM - 3), np.float32))
    p2 = s.add(24, np.array([0.92, 0.3919, 0] + [0] * (DIM - 3), np.float32))
    groups = s.groups()
    assert ids_per_group(groups) == [[p0, p2], [p1]]
    assert groups[0]["joined_by"] == ["lookback"]


def test_mean_guard_keeps_a_burst_together():
    # A 3-second burst where the subject moves: each photo is very similar to the
    # previous one, the last is only 0.65 to the first but 0.83 to the group on average.
    s = Shoot()
    ids = [s.add(i, (np.cos(a) * unit(0) + np.sin(a) * unit(1)).astype(np.float32))
           for i, a in enumerate(np.radians([0, 20, 35, 49.5]))]
    assert ids_per_group(s.groups()) == [ids]


def test_boundary_photo_moves_to_the_group_it_resembles():
    # p0 p1 | p2 p3: while walking, p1 joined p0 (0.81). Later photos show that p1 is
    # more similar to p2 and p3 (0.80 and 0.87, mean 0.835 > 0.81 + margin).
    gram = np.array([
        [1.00, 0.81, 0.69, 0.72],
        [0.81, 1.00, 0.80, 0.87],
        [0.69, 0.80, 1.00, 0.86],
        [0.72, 0.87, 0.86, 1.00],
    ])
    vecs = np.linalg.cholesky(gram).astype(np.float32)  # rows have exactly these similarities
    s = Shoot()
    ids = [s.add(t, np.pad(v, (0, DIM - 4))) for t, v in zip([0, 4, 9.1, 10.4], vecs)]
    groups = s.groups()
    assert ids_per_group(groups) == [[ids[0]], ids[1:]]
    assert "moved" in groups[1]["flags"]
    assert ids_per_group(s.groups(refine_boundaries=False)) == [ids[:2], ids[2:]]


def test_lookback_window_and_span_limits():
    s = Shoot()
    a1 = s.add(0, unit(0))
    other = s.add(10, unit(1))
    a2 = s.add(40, unit(0))
    # Group a1 is 40 s old: allowed by lookback_seconds=120 but not by span 30 s.
    assert ids_per_group(s.groups(max_group_span_seconds=30)) == [[a1], [other], [a2]]
    # Last photo of group a1 is 40 s old: too old for lookback_seconds=30.
    assert ids_per_group(s.groups(lookback_seconds=30)) == [[a1], [other], [a2]]
    assert ids_per_group(s.groups()) == [[a1, a2], [other]]


def test_lookback_can_be_turned_off():
    s = Shoot()
    a1 = s.add(0, unit(0))
    other = s.add(10, unit(1))
    a2 = s.add(20, unit(0))
    assert ids_per_group(s.groups(lookback_seconds=0)) == [[a1], [other], [a2]]


def test_lookback_never_mixes_cameras():
    s = Shoot()
    a1 = s.add(0, unit(0), camera="SN1")
    b1 = s.add(10, unit(0), camera="SN2")
    assert ids_per_group(s.groups()) == [[a1], [b1]]


def test_cameras_are_never_mixed():
    s = Shoot()
    a1 = s.add(0.0, unit(0), camera="SN1")
    b1 = s.add(0.1, unit(0), camera="SN2")
    a2 = s.add(0.2, unit(0), camera="SN1")
    b2 = s.add(0.3, unit(0), camera="SN2")
    groups = s.groups()
    assert ids_per_group(groups) == [[a1, a2], [b1, b2]]
    assert [g["camera_id"] for g in groups] == ["SN1", "SN2"]


def test_drift_guard_cuts_slowly_changing_chain():
    # Each step rotates by a small angle: neighbours are ~0.99 similar,
    # but over 12 photos the scene turns by 90 degrees (first vs last: 0.0).
    s = Shoot()
    angles = np.linspace(0, np.pi / 2, 12)
    ids = [s.add(i * 0.5, (np.cos(a) * unit(0) + np.sin(a) * unit(1)).astype(np.float32))
           for i, a in enumerate(angles)]
    groups = s.groups()
    assert len(groups) > 1
    group_of = {pid: g["group_id"] for g in groups for pid in g["photo_ids"]}
    assert group_of[ids[0]] != group_of[ids[-1]]


def test_oversized_group_is_split_evenly_and_linked():
    s = Shoot()
    ids = [s.add(i * 0.1, unit(0)) for i in range(13)]
    groups = s.groups(max_group_size=12)
    assert sorted(g["size"] for g in groups) == [6, 7]  # balanced, not 12 + 1
    assert sum(ids_per_group(groups), []) == ids
    assert groups[0]["split_from"] == groups[1]["split_from"] == groups[0]["group_id"]
    assert groups[0]["split_part"] == [1, 2] and groups[1]["split_part"] == [2, 2]


def test_unusable_photos_become_flagged_singletons():
    s = Shoot()
    ok1 = s.add(0.0, unit(0))
    ok2 = s.add(0.2, unit(0))
    bad = s.add(0.4, unit(0), status="error")
    no_time = s.add(0.6, unit(0), time=False)
    groups = s.groups()
    assert ids_per_group(groups)[0] == [ok1, ok2]
    flags = {g["photo_ids"][0]: g["flags"] for g in groups if g["size"] == 1}
    assert flags[bad] == ["ingest_error"]
    assert flags[no_time] == ["no_timestamp"]


def test_every_photo_lands_in_exactly_one_group():
    rng = np.random.default_rng(0)
    s = Shoot()
    t = 0.0
    for i in range(300):
        t += float(rng.choice([0.1, 0.5, 3.0, 20.0]))
        v = rng.normal(size=DIM).astype(np.float32)
        s.add(t, v / np.linalg.norm(v), camera=f"SN{i % 2}")
    groups = s.groups()
    ids = [pid for g in groups for pid in g["photo_ids"]]
    assert sorted(ids) == sorted(p["id"] for p in s.photos)
    assert [g["group_id"] for g in groups] == [f"g{i:04d}" for i in range(1, len(groups) + 1)]


def test_invariant_check_catches_lost_photo():
    s = Shoot()
    s.add(0, unit(0))
    s.add(1, unit(0))
    groups = s.groups()
    groups[0]["photo_ids"] = groups[0]["photo_ids"][:1]
    with pytest.raises(AssertionError):
        check_every_photo_once(s.photos, groups)


@pytest.mark.parametrize("n,max_size,expected", [
    (12, 12, [12]), (13, 12, [7, 6]), (25, 12, [9, 8, 8]), (1, 12, [1]),
])
def test_split_evenly(n, max_size, expected):
    chunks = split_evenly(list(range(n)), max_size)
    assert [len(c) for c in chunks] == expected
    assert sum(chunks, []) == list(range(n))


def _people_map(shoot, flags):
    """sha256 -> has_people for the photos of `shoot`, in order of creation."""
    return {p["sha256"]: f for p, f in zip(shoot.photos, flags)}


def test_nopeople_photos_join_across_longer_gap_and_lower_similarity():
    # Lemonade jars, recut 24 s later at 0.85 (talici 4a: 9883 -> 9886).
    s = Shoot()
    a = s.add(0, unit(0))
    b = s.add(24, mix(unit(0), unit(1), 0.85))
    people = _people_map(s, [False, False])
    assert ids_per_group(group_photos(s.photos, s.embeddings, CFG, people)) == [[a, b]]
    # Same numbers WITH people (or without a people map): stays split.
    assert ids_per_group(s.groups()) == [[a], [b]]
    people = _people_map(s, [True, False])
    assert ids_per_group(group_photos(s.photos, s.embeddings, CFG, people)) == [[a], [b]]


def test_nopeople_lookback_uses_relaxed_threshold():
    # Detail shot, something else, the same detail again at 0.88 (< 0.90, >= 0.86).
    s = Shoot()
    a1 = s.add(0, unit(0))
    other = s.add(10, unit(1))
    a2 = s.add(60, mix(unit(0), unit(2), 0.88))
    people = _people_map(s, [False, True, False])
    assert ids_per_group(group_photos(s.photos, s.embeddings, CFG, people)) == [[a1, a2], [other]]
    # With people anywhere in the pair, 0.88 stays below the strict 0.90.
    assert ids_per_group(s.groups()) == [[a1], [other], [a2]]


def test_oversized_group_splits_at_the_weakest_similarity():
    # 13 photos: a change of framing (0.80) after the 4th photo; the cut must land
    # there, not in the middle of the near-identical run.
    s = Shoot()
    first = [s.add(i * 0.2, mix(unit(0), unit(1), 0.99)) for i in range(4)]
    rest = [s.add(0.8 + i * 0.2, mix(unit(2), unit(3), 0.99)) for i in range(9)]
    groups = s.groups(max_group_size=12, min_mean_similarity_to_group=0.0,
                      similarity_threshold=0.0, refine_boundaries=False,
                      lookback_seconds=0)
    assert [g["size"] for g in groups] == [4, 9]
    assert ids_per_group(groups) == [first, rest]


# ------------------------------------------------------------ face identities

def _identity_map(shoot, sigs):
    """sha256 -> (frozenset of identity labels, n_faces) in order of creation."""
    return {p["sha256"]: (frozenset(ids), n) for p, (ids, n) in zip(shoot.photos, sigs)}


def test_identity_relation():
    same = (frozenset({"A", "B"}), 2)
    assert identity_relation(same, (frozenset({"A", "B"}), 2)) == "same"
    assert identity_relation(same, (frozenset({"A", "B"}), 3)) is None     # extra unidentified face
    assert identity_relation(same, (frozenset({"A", "C"}), 2)) is None     # partial overlap
    assert identity_relation(same, (frozenset({"C"}), 1)) == "different"
    assert identity_relation(same, (frozenset(), 0)) is None              # nobody identified
    assert identity_relation(same, None) is None
    assert identity_relation((frozenset(), 1), (frozenset(), 1)) is None
    # An unknown face may stand in for a missing known person only when allowed.
    profile = (frozenset({"B"}), 2)
    assert identity_relation(same, profile) is None
    assert identity_relation(same, profile, allow_unknown=True) == "same"
    assert identity_relation(profile, same, allow_unknown=True) == "same"
    assert identity_relation(same, (frozenset({"B"}), 1), allow_unknown=True) is None   # counts differ
    assert identity_relation(same, (frozenset({"C"}), 2), allow_unknown=True) == "different"


def test_different_people_never_break_a_burst():
    # A face hidden in one frame of a 0.6 s burst is not a change of people.
    s = Shoot()
    a = s.add(0, unit(0))
    b = s.add(0.6, mix(unit(0), unit(1), 0.95))
    ids = _identity_map(s, [(["A"], 1), (["B"], 1)])
    groups = group_photos(s.photos, s.embeddings, CFG, None, ids)
    assert ids_per_group(groups) == [[a, b]] and groups[0]["flags"] == []
    # The same pair 10 s apart is only an extended-gap join: blocked.
    s = Shoot()
    a = s.add(0, unit(0))
    b = s.add(10, mix(unit(0), unit(1), 0.95))
    ids = _identity_map(s, [(["A"], 1), (["B"], 1)])
    assert ids_per_group(group_photos(s.photos, s.embeddings, CFG, None, ids)) == [[a], [b]]


def test_unknown_face_can_complete_the_couple_when_allowed():
    # 8028 {A,B} -> 8029 {B}+1 unknown at 0.894 after 48 s (Talici 1).
    s = Shoot()
    a = s.add(0, unit(0))
    b = s.add(48, mix(unit(0), unit(1), 0.894))
    ids = _identity_map(s, [(["A", "B"], 2), (["B"], 2)])
    assert ids_per_group(group_photos(s.photos, s.embeddings, CFG, None, ids)) == [[a], [b]]
    cfg = {**CFG, "faces_same_allows_unknown": True}
    groups = group_photos(s.photos, s.embeddings, cfg, None, ids)
    assert ids_per_group(groups) == [[a, b]] and "faces" in groups[0]["flags"]


def test_same_people_merge_low_similarity_lookback_and_neighbour():
    # Talici 1 shapes: 8033 -> 8049 at 0.72 after 94 s with other groups between
    # (look-back); 8137 -> 8138 at 0.74 after 6 s (neighbour). Both show the couple.
    s = Shoot()
    a1 = s.add(0, unit(0))
    o1 = s.add(30, unit(1))
    o2 = s.add(60, unit(2))
    a2 = s.add(94, mix(unit(0), unit(3), 0.72))
    a3 = s.add(100, mix(s.embeddings[s.photos[-1]["sha256"]], unit(4), 0.80))  # 0.80 to a2, 0.58 to a1
    couple = (["A", "B"], 2)
    ids = _identity_map(s, [couple, (["C"], 1), (["C"], 1), couple, couple])
    groups = group_photos(s.photos, s.embeddings, CFG, None, ids)
    assert ids_per_group(groups) == [[a1, a2, a3], [o1], [o2]]
    assert groups[0]["joined_by"] == ["lookback", "neighbour"]
    assert "faces" in groups[0]["flags"]
    # Without identities the same numbers stay apart (0.72 < 0.90 look-back, 0.80 < 0.82).
    assert ids_per_group(s.groups()) == [[a1], [o1], [o2], [a2], [a3]]


def test_different_people_block_a_join_the_usual_rules_allow():
    # Two guests at the same spot, DINOv2 0.95: the usual rules would merge them.
    s = Shoot()
    a = s.add(0, unit(0))
    b = s.add(1, mix(unit(0), unit(1), 0.95))
    c = s.add(2, mix(unit(0), unit(2), 0.95))
    ids = _identity_map(s, [(["C"], 1), (["D"], 1), (["C"], 1)])
    groups = group_photos(s.photos, s.embeddings, CFG, None, ids)
    assert ids_per_group(groups) == [[a, b, c]]          # 1 s apart: a burst is never blocked
    # 10 s apart (extended-gap rule) the different people keep them apart.
    s = Shoot()
    a = s.add(0, unit(0))
    b = s.add(10, mix(unit(0), unit(1), 0.95))
    c = s.add(20, mix(unit(0), unit(2), 0.95))
    ids = _identity_map(s, [(["C"], 1), (["D"], 1), (["C"], 1)])
    groups = group_photos(s.photos, s.embeddings, CFG, None, ids)
    assert ids_per_group(groups) == [[a, c], [b]]        # c returns to a by look-back
    assert "faces_split" in groups[1]["flags"]
    assert "faces_split" in groups[0]["flags"]           # c's neighbour join to b was blocked
    assert ids_per_group(s.groups()) == [[a, b, c]]


def test_neutral_relations_change_nothing():
    s = Shoot()
    a = s.add(0, unit(0))
    b = s.add(1, mix(unit(0), unit(1), 0.95))      # joins by the usual rule
    c = s.add(30, mix(unit(0), unit(2), 0.80))     # too weak for look-back, stays apart
    for sigs in ([(["A"], 1), ([], 0), ([], 0)],            # nobody identified on one side
                 [(["A", "B"], 2), (["A", "C"], 2), (["A"], 1)],  # partial overlap
                 [(["A"], 1), (["A"], 2), (["A"], 3)]):           # same person, extra faces
        ids = _identity_map(s, sigs)
        groups = group_photos(s.photos, s.embeddings, CFG, None, ids)
        assert ids_per_group(groups) == [[a, b], [c]]
        assert not any(f.startswith("faces") for g in groups for f in g["flags"])


def test_refine_never_moves_a_photo_next_to_different_people():
    # Same gram matrix as test_boundary_photo_moves_to_the_group_it_resembles, but p1
    # shows a different person than p2/p3: it must stay with p0.
    gram = np.array([
        [1.00, 0.81, 0.69, 0.72],
        [0.81, 1.00, 0.80, 0.87],
        [0.69, 0.80, 1.00, 0.86],
        [0.72, 0.87, 0.86, 1.00],
    ])
    vecs = np.linalg.cholesky(gram).astype(np.float32)
    s = Shoot()
    ids_ = [s.add(t, np.pad(v, (0, DIM - 4))) for t, v in zip([0, 4, 9.1, 10.4], vecs)]
    ids = _identity_map(s, [(["A"], 1), (["A"], 1), (["B"], 1), (["B"], 1)])
    assert ids_per_group(group_photos(s.photos, s.embeddings, CFG, None, ids)) == [ids_[:2], ids_[2:]]
    # p1 unidentified: neutral everywhere, so the boundary move happens as without faces.
    ids = _identity_map(s, [(["A"], 1), ([], 1), (["B"], 1), (["B"], 1)])
    assert ids_per_group(group_photos(s.photos, s.embeddings, CFG, None, ids)) == [[ids_[0]], ids_[1:]]


def test_no_identities_is_identical_to_the_current_behaviour():
    rng = np.random.default_rng(0)
    s = Shoot()
    t = 0.0
    for i in range(300):
        t += float(rng.choice([0.1, 0.5, 3.0, 20.0]))
        v = rng.normal(size=DIM).astype(np.float32)
        s.add(t, v / np.linalg.norm(v), camera=f"SN{i % 2}")
    without = group_photos(s.photos, s.embeddings, CFG)
    empty = group_photos(s.photos, s.embeddings, CFG, None, {p["sha256"]: (frozenset(), 0) for p in s.photos})
    assert ids_per_group(without) == ids_per_group(empty)
    assert [g["flags"] for g in without] == [g["flags"] for g in empty]
