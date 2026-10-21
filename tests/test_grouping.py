import hashlib
from datetime import datetime, timedelta

import numpy as np
import pytest

from culling.config import DEFAULTS
from culling.grouping import check_every_photo_once, group_photos, split_evenly

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
