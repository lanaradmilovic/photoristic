"""Face detection, recognition and identity clustering (local ONNX models, CPU).

Why: DINOv2 similarity cannot tell "the same couple in a new pose" (should be one
group) from "a different guest at the same spot" (must stay apart); both score
~0.85-0.90. Face identities can. Grouping uses them as an extra signal: photos that
show exactly the same identified people may join under relaxed thresholds, photos
whose identified people do not overlap at all never join (see grouping.py).

Pipeline per photo (the 1536 px preview, not the thumbnail):
  1. SCRFD-10G detects faces with 5 keypoints (eyes, nose, mouth corners).
  2. Each face is aligned to the ArcFace 112x112 template by a similarity transform.
  3. glintr100 (AuraFace, ArcFace ResNet100) gives a 512-d L2-normalised embedding.
Results are cached in faces.npz keyed by file sha256, like embeddings.npz: re-runs
only process new photos. The cache is invalidated when the models or detection
settings change.

Per wedding, faces are clustered into identities (Chinese Whispers on the graph of
faces whose cosine similarity reaches `identity_threshold`) and labelled A, B, C, ...
by decreasing number of faces, so the couple normally comes out as A and B. The
result is written to identities.json for grouping and the report.

No image or embedding leaves the machine. Logs contain counts and timings only.
"""
import json
import logging
import os
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from tqdm import tqdm

log = logging.getLogger(__name__)

FACES_FILE = "faces.npz"
IDENTITIES_FILE = "identities.json"
SHEETS_DIR = "faces_sheets"
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Standard ArcFace 112x112 template (InsightFace): left eye, right eye, nose,
# left mouth corner, right mouth corner.
ARCFACE_TEMPLATE = np.array([
    [38.2946, 51.6963],
    [73.5318, 51.5014],
    [56.0252, 71.7366],
    [41.5493, 92.3655],
    [70.7299, 92.2041],
], dtype=np.float32)
FACE_SIZE = 112
EMBEDDING_DIM = 512

# SCRFD-10G "bnkps" head: three feature maps (strides 8/16/32), two anchors per cell,
# outputs ordered [scores x3, box distances x3, keypoint offsets x3].
SCRFD_STRIDES = (8, 16, 32)
SCRFD_ANCHORS = 2


# --------------------------------------------------------------------------- cache

def model_signature(cfg):
    """Everything that changes the cached faces: model files and detection settings."""
    return (f"{Path(cfg['detector_path']).name}+{Path(cfg['embedder_path']).name}"
            f"@{cfg['det_size']}/{cfg['det_threshold']}/{cfg['min_face_size']}")


def load_cache(out_dir, signature):
    """Return {sha256: [face, ...]} for every photo processed with this signature.
    A face is {"bbox": (4,), "score": float, "kps": (5, 2), "embedding": (512,)}."""
    path = Path(out_dir) / FACES_FILE
    if not path.exists():
        return {}
    data = np.load(path, allow_pickle=False)
    if str(data["model_name"]) != signature:
        log.info("Face models/settings changed (%s -> %s); recomputing", data["model_name"], signature)
        return {}
    cache = {key: [] for key in data["photo_keys"].tolist()}
    for key, bbox, score, kps, emb in zip(data["face_key"].tolist(), data["face_bbox"],
                                          data["face_score"], data["face_kps"], data["face_emb"]):
        cache[key].append({"bbox": bbox, "score": float(score), "kps": kps, "embedding": emb})
    return cache


def save_cache(out_dir, signature, cache):
    path = Path(out_dir) / FACES_FILE
    keys = sorted(cache)
    faces = [(key, face) for key in keys for face in cache[key]]

    def stack(field, shape):
        return np.array([face[field] for _, face in faces], np.float32).reshape((len(faces),) + shape)

    tmp = path.with_name("faces.tmp.npz")
    np.savez(tmp, model_name=np.array(signature),
             photo_keys=np.array(keys, dtype=str),
             face_key=np.array([key for key, _ in faces], dtype=str),
             face_bbox=stack("bbox", (4,)), face_score=stack("score", ()),
             face_kps=stack("kps", (5, 2)), face_emb=stack("embedding", (EMBEDDING_DIM,)))
    os.replace(tmp, path)


# ------------------------------------------------------------------- detection

def _model_path(value):
    path = Path(value)
    return path if path.is_absolute() else PROJECT_ROOT / path


class FaceModels:
    """The two ONNX sessions (detector + embedder) on CPU."""

    def __init__(self, cfg):
        import onnxruntime as ort
        options = ort.SessionOptions()
        options.log_severity_level = 3  # the models declare fixed output shapes; mismatch warnings are expected
        providers = ["CPUExecutionProvider"]
        self.det = ort.InferenceSession(str(_model_path(cfg["detector_path"])), options, providers=providers)
        self.emb = ort.InferenceSession(str(_model_path(cfg["embedder_path"])), options, providers=providers)
        self.det_input = self.det.get_inputs()[0].name
        self.emb_input = self.emb.get_inputs()[0].name


def detector_input(img, det_size):
    """Downscale so the long edge is `det_size`, pad each side up to a multiple of 32
    (the network is fully convolutional, so a 3:2 frame needs no square letterbox).
    Returns (blob 1x3xHxW float32, (scale_x, scale_y)) with scale = detector px / image px."""
    w, h = img.size
    scale = det_size / max(w, h)
    nw, nh = max(1, round(w * scale)), max(1, round(h * scale))
    resized = img.resize((nw, nh), Image.Resampling.BILINEAR)
    pw, ph = -(-nw // 32) * 32, -(-nh // 32) * 32
    canvas = np.zeros((ph, pw, 3), np.float32)
    canvas[:nh, :nw] = np.asarray(resized, dtype=np.float32)
    blob = ((canvas - 127.5) / 128.0).transpose(2, 0, 1)[None]
    return np.ascontiguousarray(blob), (nw / w, nh / h)


def decode_scrfd(outputs, height, width, threshold):
    """Turn the 9 raw SCRFD outputs for an input of `height` x `width` into
    (boxes Nx4 [x1,y1,x2,y2], scores N, keypoints Nx5x2) in input pixels, keeping
    anchors with score >= threshold. Box and keypoint outputs are distances from the
    anchor centre in units of the stride."""
    boxes, scores, kps = [], [], []
    n_maps = len(SCRFD_STRIDES)
    for i, stride in enumerate(SCRFD_STRIDES):
        sc = np.asarray(outputs[i]).reshape(-1)
        fh, fw = height // stride, width // stride
        if sc.shape[0] != fh * fw * SCRFD_ANCHORS:
            raise ValueError(f"SCRFD output size {sc.shape[0]} does not match input "
                             f"{height}x{width} at stride {stride}")
        keep = np.nonzero(sc >= threshold)[0]
        if not len(keep):
            continue
        ys, xs = np.mgrid[:fh, :fw]
        centres = np.stack([xs, ys], axis=-1).reshape(-1, 2).astype(np.float32) * stride
        centres = np.repeat(centres, SCRFD_ANCHORS, axis=0)[keep]
        dist = np.asarray(outputs[i + n_maps]).reshape(-1, 4)[keep] * stride
        offs = np.asarray(outputs[i + 2 * n_maps]).reshape(-1, 5, 2)[keep] * stride
        boxes.append(np.stack([centres[:, 0] - dist[:, 0], centres[:, 1] - dist[:, 1],
                               centres[:, 0] + dist[:, 2], centres[:, 1] + dist[:, 3]], axis=1))
        kps.append(offs + centres[:, None, :])
        scores.append(sc[keep])
    if not boxes:
        return np.zeros((0, 4), np.float32), np.zeros(0, np.float32), np.zeros((0, 5, 2), np.float32)
    return np.concatenate(boxes), np.concatenate(scores), np.concatenate(kps)


def nms(boxes, scores, iou_threshold):
    """Greedy non-maximum suppression; returns kept indices, best score first."""
    x1, y1, x2, y2 = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
    areas = np.maximum(x2 - x1, 0) * np.maximum(y2 - y1, 0)
    order = scores.argsort()[::-1]
    keep = []
    while order.size:
        i = order[0]
        keep.append(int(i))
        rest = order[1:]
        iw = np.maximum(0, np.minimum(x2[i], x2[rest]) - np.maximum(x1[i], x1[rest]))
        ih = np.maximum(0, np.minimum(y2[i], y2[rest]) - np.maximum(y1[i], y1[rest]))
        inter = iw * ih
        iou = inter / (areas[i] + areas[rest] - inter + 1e-9)
        order = rest[iou <= iou_threshold]
    return keep


# ------------------------------------------------------------------- alignment

def similarity_transform(src, dst):
    """Least-squares similarity transform (rotation + uniform scale + translation)
    mapping points `src` (Nx2) onto `dst` (Nx2), as a 2x3 matrix M:
    dst ~= M @ [x, y, 1]. Umeyama's closed form, as skimage's SimilarityTransform."""
    src = np.asarray(src, np.float64)
    dst = np.asarray(dst, np.float64)
    mu_s, mu_d = src.mean(axis=0), dst.mean(axis=0)
    s0, d0 = src - mu_s, dst - mu_d
    cov = d0.T @ s0 / len(src)
    U, S, Vt = np.linalg.svd(cov)
    d = np.ones(2)
    if np.linalg.det(U) * np.linalg.det(Vt) < 0:
        d[1] = -1  # no reflection
    R = U @ np.diag(d) @ Vt
    var_s = (s0 ** 2).sum() / len(src)
    scale = (S * d).sum() / var_s
    t = mu_d - scale * R @ mu_s
    return np.hstack([scale * R, t[:, None]])


def align_face(img, kps, size=FACE_SIZE):
    """Crop and warp a face so its 5 keypoints land on the ArcFace template.
    `img` is a PIL RGB image, `kps` 5x2 in image pixels. Returns a size x size image."""
    template = ARCFACE_TEMPLATE * (size / FACE_SIZE)
    forward = np.vstack([similarity_transform(kps, template), [0.0, 0.0, 1.0]])
    inverse = np.linalg.inv(forward)  # PIL maps output pixels back to input pixels
    return img.transform((size, size), Image.Transform.AFFINE, data=tuple(inverse[:2].ravel()),
                         resample=Image.Resampling.BILINEAR)


# -------------------------------------------------------------------- embedding

def embed_faces(models, crops):
    """512-d L2-normalised embeddings for aligned 112x112 RGB crops (one batch)."""
    batch = np.stack([(np.asarray(c, dtype=np.float32) - 127.5) / 127.5 for c in crops])
    batch = np.ascontiguousarray(batch.transpose(0, 3, 1, 2))
    out = models.emb.run(None, {models.emb_input: batch})[0].astype(np.float32)
    out /= np.linalg.norm(out, axis=1, keepdims=True) + 1e-12
    return out


def detect_in_image(models, img, cfg):
    """All faces of one PIL RGB image: detect, align, embed. Sorted by score."""
    blob, (sx, sy) = detector_input(img, cfg["det_size"])
    outputs = models.det.run(None, {models.det_input: blob})
    boxes, scores, kps = decode_scrfd(outputs, blob.shape[2], blob.shape[3], cfg["det_threshold"])
    if not len(boxes):
        return []
    keep = nms(boxes, scores, cfg["nms_threshold"])
    boxes = boxes[keep] / np.array([sx, sy, sx, sy], np.float32)
    kps = kps[keep] / np.array([sx, sy], np.float32)
    scores = scores[keep]
    # Tiny background faces give unreliable embeddings and cost ~0.1 s each: skip them.
    sides = np.maximum(boxes[:, 2] - boxes[:, 0], boxes[:, 3] - boxes[:, 1])
    big = sides >= cfg["min_face_size"]
    boxes, kps, scores = boxes[big], kps[big], scores[big]
    if not len(boxes):
        return []
    crops = [align_face(img, k) for k in kps]
    embeddings = embed_faces(models, crops)
    return [{"bbox": b.astype(np.float32), "score": float(s), "kps": k.astype(np.float32), "embedding": e}
            for b, s, k, e in zip(boxes, scores, kps, embeddings)]


def detect_faces(photos, out_dir, config):
    """Return {sha256: [face, ...]} for all photos with status 'ok' (empty list = no face).
    Returns {} when `faces.enabled` is false."""
    cfg = config["faces"]
    if not cfg["enabled"]:
        return {}
    out_dir = Path(out_dir)
    signature = model_signature(cfg)
    cache = load_cache(out_dir, signature)

    todo = [p for p in photos if p["status"] == "ok" and p["sha256"] not in cache]
    todo = list({p["sha256"]: p for p in todo}.values())
    log.info("Faces: %d cached, %d to compute (%s)", len(cache), len(todo), signature)

    if todo:
        models = FaceModels(cfg)
        for n, p in enumerate(tqdm(todo, desc="Faces", unit="img"), start=1):
            with Image.open(out_dir / p["preview_file"]) as img:
                cache[p["sha256"]] = detect_in_image(models, img.convert("RGB"), cfg)
            if n % 100 == 0:
                save_cache(out_dir, signature, cache)
        save_cache(out_dir, signature, cache)
    n_faces = sum(len(f) for f in cache.values())
    log.info("Faces: %d faces in %d photos (%d photos without a face)",
             n_faces, len(cache), sum(1 for f in cache.values() if not f))
    return cache


# ------------------------------------------------------------------- identities

def chinese_whispers(vectors, threshold, seed=0, max_iter=20):
    """Cluster unit vectors: nodes are faces, edges connect pairs with cosine similarity
    >= threshold (weight = similarity). Each node repeatedly adopts the label with the
    largest total edge weight among its neighbours. Transitive like single linkage
    (profile and frontal views of one person connect through 3/4 views), but a lone
    bridge face cannot glue two well-connected clusters together. Deterministic for a
    given seed. Returns an integer label per vector."""
    n = len(vectors)
    labels = np.arange(n)
    if n == 0:
        return labels
    neighbours = [None] * n
    for start in range(0, n, 1024):  # blockwise: only edges are kept, not the full matrix
        sims = vectors[start:start + 1024] @ vectors.T
        for r in range(sims.shape[0]):
            i = start + r
            row = sims[r]
            row[i] = 0.0
            idx = np.nonzero(row >= threshold)[0]
            neighbours[i] = (idx, row[idx].astype(np.float64))
    rng = np.random.default_rng(seed)
    for _ in range(max_iter):
        changed = False
        for i in rng.permutation(n):
            idx, weights = neighbours[i]
            if not len(idx):
                continue
            totals = np.bincount(labels[idx], weights=weights, minlength=n)
            best = int(totals.argmax())
            if best != labels[i]:
                labels[i] = best
                changed = True
        if not changed:
            break
    return labels


def merge_clusters(vectors, labels, threshold):
    """Merge clusters whose unit centroids have cosine similarity >= threshold, most
    similar pair first, until none is left. Chinese Whispers keeps two tightly knit
    communities apart even when they are the same person (Talici 1: the bride with
    and without heart sunglasses, centroid similarity 0.59, while centroids of
    different people stay below ~0.35 on both test weddings). Returns new labels."""
    labels = labels.copy()
    if threshold >= 1.0 or len(labels) == 0:
        return labels
    ids = sorted(set(labels.tolist()))
    sums = {l: vectors[labels == l].sum(axis=0) for l in ids}
    while len(ids) > 1:
        C = np.stack([sums[l] for l in ids])
        C /= np.linalg.norm(C, axis=1, keepdims=True) + 1e-12
        S = C @ C.T
        np.fill_diagonal(S, -1.0)
        i, j = np.unravel_index(int(S.argmax()), S.shape)
        if S[i, j] < threshold:
            break
        keep, gone = ids[i], ids[j]
        labels[labels == gone] = keep
        sums[keep] = sums[keep] + sums.pop(gone)
        ids.remove(gone)
    return labels


def identity_label(i):
    """0 -> A, 25 -> Z, 26 -> AA, ... (spreadsheet column style)."""
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def cluster_identities(faces, cfg):
    """Cluster all faces of a wedding into identities.

    Returns {"threshold", "identities": {label: {"n_faces", "n_photos"}},
             "photos": {sha256: {"ids": [labels], "faces": [label per face], "n_faces"}}}.
    Labels are assigned by decreasing number of faces (A = most frequent person).
    """
    threshold = cfg["identity_threshold"]
    keys = [(sha, i) for sha in sorted(faces) for i in range(len(faces[sha]))]
    photos = {sha: {"ids": [], "faces": [], "n_faces": len(faces[sha])} for sha in faces}
    identities = {}
    if keys:
        vectors = np.stack([faces[sha][i]["embedding"] for sha, i in keys]).astype(np.float32)
        raw = chinese_whispers(vectors, threshold)
        raw = merge_clusters(vectors, raw, cfg["identity_merge_threshold"])
        counts = Counter(raw.tolist())
        order = sorted(counts, key=lambda l: (-counts[l], l))
        names = {l: identity_label(rank) for rank, l in enumerate(order)}
        photos_of = defaultdict(set)
        for (sha, i), l in zip(keys, raw.tolist()):
            photos[sha]["faces"].append(names[l])
            photos_of[names[l]].add(sha)
        for sha in photos:
            photos[sha]["ids"] = sorted(set(photos[sha]["faces"]))
        identities = {names[l]: {"n_faces": counts[l], "n_photos": len(photos_of[names[l]])}
                      for l in order}
    log.info("Identities: %d faces -> %d identities (%d with >= 2 faces); threshold %.2f",
             len(keys), len(identities), sum(1 for v in identities.values() if v["n_faces"] > 1),
             threshold)
    return {"threshold": threshold, "min_identity_faces": cfg["min_identity_faces"],
            "identities": identities, "photos": photos}


def known_identities(identities, min_faces):
    """Labels of identities seen on at least `min_faces` faces. A face seen once or twice
    (a guest in the background, a blurred profile, the bride behind the veil) is an
    unknown person, not evidence that two photos show different people."""
    return {label for label, info in identities["identities"].items() if info["n_faces"] >= min_faces}


def photo_signatures(identities, min_faces=1):
    """{sha256: (frozenset of known identity labels, number of faces)} for grouping.
    Only identities with at least `min_faces` faces count (see `known_identities`);
    the face count includes every detected face. None when identities are not
    available (faces disabled)."""
    if not identities:
        return None
    known = known_identities(identities, min_faces)
    return {sha: (frozenset(l for l in info["ids"] if l in known), info["n_faces"])
            for sha, info in identities["photos"].items()}


def save_identities(out_dir, identities):
    path = Path(out_dir) / IDENTITIES_FILE
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(identities, f)
    os.replace(tmp, path)


def load_identities(out_dir):
    path = Path(out_dir) / IDENTITIES_FILE
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ------------------------------------------------------------- review sheets

def write_identity_sheets(out_dir, photos, faces, identities, cols=12, max_faces=120):
    """One contact sheet per identity in <out>/faces_sheets/<label>.jpg (aligned 112 px
    crops with the file name and detection score); identities with a single face all
    go on _singletons.jpg. For checking the clustering by eye; no other step uses it."""
    out_dir = Path(out_dir)
    sheets_dir = out_dir / SHEETS_DIR
    sheets_dir.mkdir(exist_ok=True)
    for old in sheets_dir.glob("*.jpg"):
        old.unlink()
    photo_by_sha = {p["sha256"]: p for p in photos if p["status"] == "ok"}
    members = defaultdict(list)  # label -> [(photo, face)]
    for sha, info in identities["photos"].items():
        if sha not in photo_by_sha:
            continue
        for face, label in zip(faces.get(sha, []), info["faces"]):
            members[label].append((photo_by_sha[sha], face, label))
    by_size = sorted(members.items(), key=lambda kv: (-len(kv[1]), kv[0]))

    def crops_of(items, with_label=False):
        items = sorted(items, key=lambda x: (x[0].get("capture_time") or "", x[0]["primary_path"]))
        out, cache = [], {}
        for photo, face, label in items[:max_faces]:
            if photo["sha256"] not in cache:
                with Image.open(out_dir / photo["preview_file"]) as img:
                    cache[photo["sha256"]] = img.convert("RGB")
            crop = align_face(cache[photo["sha256"]], face["kps"])
            caption = f"{Path(photo['primary_path']).stem[-4:]} {face['score']:.2f}"
            if with_label:
                caption = f"{label} {caption}"
            out.append((crop, caption))
        return out

    def sheet(path, title, crops):
        cell, cap = FACE_SIZE + 4, 14
        rows = max(1, -(-len(crops) // cols))
        canvas = Image.new("RGB", (cols * cell, 20 + rows * (cell + cap)), "white")
        draw = ImageDraw.Draw(canvas)
        draw.text((4, 3), title, fill="black")
        for k, (crop, caption) in enumerate(crops):
            x, y = (k % cols) * cell, 20 + (k // cols) * (cell + cap)
            canvas.paste(crop, (x + 2, y))
            draw.text((x + 2, y + FACE_SIZE + 1), caption, fill="black")
        canvas.save(path, "JPEG", quality=85)

    singles = []
    for label, items in by_size:
        if len(items) == 1:
            singles.extend(items)
            continue
        n_photos = identities["identities"][label]["n_photos"]
        sheet(sheets_dir / f"{label}.jpg", f"{label}: {len(items)} faces in {n_photos} photos",
              crops_of(items))
    if singles:
        sheet(sheets_dir / "_singletons.jpg", f"{len(singles)} single-face identities",
              crops_of(singles, with_label=True))
    log.info("Identity sheets: %s", sheets_dir)
    return sheets_dir
