"""Face module tests on synthetic data: no ONNX model is loaded."""
import numpy as np
import pytest
from PIL import Image

from culling.faces import (ARCFACE_TEMPLATE, SCRFD_ANCHORS, SCRFD_STRIDES, align_face,
                           chinese_whispers, cluster_identities, decode_scrfd, detector_input,
                           identity_label, load_cache, merge_clusters, nms, photo_signatures,
                           save_cache, similarity_transform)

FACES_CFG = {"identity_threshold": 0.5, "identity_merge_threshold": 0.45, "min_identity_faces": 3}


# ------------------------------------------------------------------ alignment

def test_similarity_transform_recovers_rotation_scale_translation():
    angle, scale, shift = np.radians(30), 2.5, np.array([40.0, -15.0])
    R = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    src = ARCFACE_TEMPLATE.astype(np.float64)
    dst = (scale * src @ R.T) + shift
    M = similarity_transform(src, dst)
    mapped = src @ M[:, :2].T + M[:, 2]
    assert np.allclose(mapped, dst, atol=1e-6)
    assert np.isclose(np.linalg.det(M[:, :2]), scale ** 2)  # uniform scale, no reflection


def test_align_face_puts_keypoints_on_the_template():
    # A 400x300 image with a coloured dot at each (rotated, scaled, shifted) keypoint.
    angle, scale, shift = np.radians(-20), 1.8, np.array([120.0, 60.0])
    R = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    kps = scale * ARCFACE_TEMPLATE.astype(np.float64) @ R.T + shift
    colours = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)]
    img = Image.new("RGB", (400, 300), (0, 0, 0))
    px = img.load()
    for (x, y), colour in zip(kps, colours):
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                px[int(round(x)) + dx, int(round(y)) + dy] = colour
    aligned = np.asarray(align_face(img, kps))
    assert aligned.shape == (112, 112, 3)
    for (tx, ty), colour in zip(ARCFACE_TEMPLATE, colours):
        patch = aligned[int(ty) - 1:int(ty) + 2, int(tx) - 1:int(tx) + 2].reshape(-1, 3)
        # The dot's colour dominates the 3x3 patch around the template point.
        assert (np.abs(patch.astype(int) - colour).sum(axis=1) < 120).mean() > 0.5


# ------------------------------------------------------------------ detection

def test_detector_input_scales_and_pads_to_multiples_of_32():
    img = Image.new("RGB", (1536, 1024), (127, 127, 127))
    blob, (sx, sy) = detector_input(img, 640)
    assert blob.shape == (1, 3, 448, 640)  # 1024 * 640/1536 = 426.7 -> 427 -> padded 448
    assert np.isclose(sx, 640 / 1536) and np.isclose(sy, 427 / 1024)
    assert np.allclose(blob[0, :, :427, :], (127 - 127.5) / 128, atol=1e-6)
    assert np.allclose(blob[0, :, 427:, :], -127.5 / 128)  # padding is black


def _scrfd_outputs(height, width, hits):
    """Raw outputs with the given anchors set: hits = {(stride, y, x, anchor): (score, dist4, kps10)}."""
    outputs = []
    for kind_size in (1, 4, 10):
        for stride in SCRFD_STRIDES:
            fh, fw = height // stride, width // stride
            arr = np.zeros((fh * fw * SCRFD_ANCHORS, kind_size), np.float32)
            for (s, y, x, a), (score, dist, kps) in hits.items():
                if s == stride:
                    row = (y * fw + x) * SCRFD_ANCHORS + a
                    arr[row] = {1: [score], 4: dist, 10: kps}[kind_size]
            outputs.append(arr)
    return outputs


def test_decode_scrfd_maps_anchor_distances_to_pixels():
    hits = {(16, 3, 5, 1): (0.9, [1.0, 2.0, 1.5, 0.5], [0.0, 0.0, 1.0, 0.0, 0.5, 0.5, 0.0, 1.0, 1.0, 1.0]),
            (8, 0, 0, 0): (0.2, [1, 1, 1, 1], [0] * 10)}  # below threshold
    boxes, scores, kps = decode_scrfd(_scrfd_outputs(96, 128, hits), 96, 128, 0.5)
    assert len(boxes) == 1 and scores[0] == pytest.approx(0.9)
    cx, cy = 5 * 16, 3 * 16
    assert np.allclose(boxes[0], [cx - 16, cy - 32, cx + 24, cy + 8])
    assert np.allclose(kps[0], [[cx, cy], [cx + 16, cy], [cx + 8, cy + 8], [cx, cy + 16], [cx + 16, cy + 16]])


def test_decode_scrfd_rejects_mismatched_input_size():
    with pytest.raises(ValueError):
        decode_scrfd(_scrfd_outputs(96, 128, {}), 128, 128, 0.5)


def test_nms_keeps_best_of_overlapping_boxes():
    boxes = np.array([[0, 0, 100, 100], [5, 5, 105, 105], [200, 200, 260, 260]], np.float32)
    scores = np.array([0.8, 0.9, 0.7], np.float32)
    assert nms(boxes, scores, 0.4) == [1, 2]
    assert nms(boxes, scores, 0.95) == [1, 0, 2]


# ------------------------------------------------------------------- cache

def test_cache_round_trip_keeps_photos_without_faces(tmp_path):
    rng = np.random.default_rng(1)
    emb = rng.normal(size=512).astype(np.float32)
    cache = {
        "a" * 64: [{"bbox": np.array([1, 2, 30, 40], np.float32), "score": 0.9,
                    "kps": np.arange(10, dtype=np.float32).reshape(5, 2), "embedding": emb}],
        "b" * 64: [],
    }
    save_cache(tmp_path, "sig", cache)
    loaded = load_cache(tmp_path, "sig")
    assert set(loaded) == set(cache) and loaded["b" * 64] == []
    face = loaded["a" * 64][0]
    assert np.allclose(face["bbox"], [1, 2, 30, 40]) and face["score"] == pytest.approx(0.9)
    assert np.allclose(face["kps"], np.arange(10).reshape(5, 2)) and np.allclose(face["embedding"], emb)
    assert load_cache(tmp_path, "other-signature") == {}
    save_cache(tmp_path, "sig", {})
    assert load_cache(tmp_path, "sig") == {}


# --------------------------------------------------------------- clustering

def _cluster(centre, n, rng, spread=0.15):
    """n unit vectors around `centre`, pairwise similarity well above 0.5."""
    out = []
    for _ in range(n):
        v = centre + spread * rng.normal(size=len(centre))
        out.append((v / np.linalg.norm(v)).astype(np.float32))
    return out


def _basis(i, dim=16):
    v = np.zeros(dim, np.float32)
    v[i] = 1
    return v


def test_chinese_whispers_finds_three_people_and_leaves_singletons():
    rng = np.random.default_rng(0)
    vecs = _cluster(_basis(0), 12, rng) + _cluster(_basis(1), 6, rng) + _cluster(_basis(2), 3, rng)
    vecs += [_basis(3), _basis(4)]  # two faces of people seen once
    labels = chinese_whispers(np.stack(vecs), 0.5)
    assert len(set(labels[:12])) == 1 and len(set(labels[12:18])) == 1 and len(set(labels[18:21])) == 1
    assert len({labels[0], labels[12], labels[18], labels[21], labels[22]}) == 5


def test_chinese_whispers_bridge_face_does_not_merge_two_people():
    rng = np.random.default_rng(2)
    a, b = _cluster(_basis(0), 10, rng, spread=0.15), _cluster(_basis(1), 10, rng, spread=0.15)
    bridge = (_basis(0) + _basis(1)) / np.sqrt(2)  # 0.71 to both centres
    labels = chinese_whispers(np.stack(a + b + [bridge]), 0.5)
    assert len(set(labels[:10])) == 1 and len(set(labels[10:20])) == 1
    assert labels[0] != labels[10]


def test_merge_clusters_joins_two_views_of_one_person_but_not_two_people():
    # Two tight communities of the same person (sunglasses on / off): members are 0.9
    # similar within, ~0.55 across. Chinese Whispers keeps them apart because the
    # within-community weight dominates; the centroid merge joins them.
    rng = np.random.default_rng(4)
    c1 = _basis(0)
    c2 = (0.55 * _basis(0) + np.sqrt(1 - 0.55 ** 2) * _basis(1)).astype(np.float32)
    far = _basis(2)
    vecs = np.stack(_cluster(c1, 10, rng, 0.1) + _cluster(c2, 10, rng, 0.1) + _cluster(far, 5, rng, 0.1))
    labels = chinese_whispers(vecs, 0.4)
    assert len(set(labels[:10])) == 1 and len(set(labels[10:20])) == 1 and len(set(labels[20:])) == 1
    merged = merge_clusters(vecs, labels, 0.45)
    assert len(set(merged[:20])) == 1          # the two views became one identity
    assert merged[0] != merged[20]              # the other person stays separate
    assert np.array_equal(merge_clusters(vecs, labels, 1.0), labels)
    assert len(set(merge_clusters(vecs, labels, -1.0))) == 1  # no threshold: everything merges


def test_identity_labels_are_spreadsheet_columns():
    assert [identity_label(i) for i in (0, 1, 25, 26, 27, 51, 52)] == ["A", "B", "Z", "AA", "AB", "AZ", "BA"]


def test_cluster_identities_labels_by_frequency_and_builds_signatures():
    rng = np.random.default_rng(3)
    bride, groom, guest = _cluster(_basis(0), 4, rng), _cluster(_basis(1), 3, rng), _cluster(_basis(2), 1, rng)

    def face(v):
        return {"bbox": np.zeros(4, np.float32), "score": 0.9, "kps": np.zeros((5, 2), np.float32), "embedding": v}

    faces = {
        "p1": [face(bride[0]), face(groom[0])],
        "p2": [face(bride[1]), face(groom[1])],
        "p3": [face(bride[2])],
        "p4": [face(groom[2]), face(bride[3]), face(guest[0])],
        "p5": [],
    }
    ids = cluster_identities(faces, FACES_CFG)
    assert ids["threshold"] == 0.5 and ids["min_identity_faces"] == 3
    assert list(ids["identities"]) == ["A", "B", "C"]
    assert ids["identities"]["A"] == {"n_faces": 4, "n_photos": 4}
    assert ids["identities"]["B"] == {"n_faces": 3, "n_photos": 3}
    assert ids["photos"]["p4"]["faces"] == ["B", "A", "C"] and ids["photos"]["p4"]["ids"] == ["A", "B", "C"]
    assert ids["photos"]["p5"] == {"ids": [], "faces": [], "n_faces": 0}
    sigs = photo_signatures(ids)
    assert sigs["p1"] == (frozenset({"A", "B"}), 2)
    assert sigs["p3"] == (frozenset({"A"}), 1)
    assert sigs["p5"] == (frozenset(), 0)
    assert photo_signatures(None) is None
    # With min_faces=3, the guest seen once (C) is unknown: not in the set, still counted.
    sigs = photo_signatures(ids, min_faces=3)
    assert sigs["p4"] == (frozenset({"A", "B"}), 3)


def test_cluster_identities_with_no_faces():
    ids = cluster_identities({"p1": []}, FACES_CFG)
    assert ids["identities"] == {} and ids["photos"]["p1"]["n_faces"] == 0
