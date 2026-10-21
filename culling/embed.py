"""Image embeddings for visual similarity (DINOv2 CLS token, L2-normalized).

Runs locally on CPU. The model weights are downloaded once from Hugging Face;
no image ever leaves the machine. Embeddings are cached in embeddings.npz keyed
by file sha256, so re-runs only embed new photos.

Each thumbnail is resized to a full square (no center crop) so the edges of the
frame count too: two shots that differ only at the border should still differ.
"""
import logging
import os
from pathlib import Path

import numpy as np
from PIL import Image
from tqdm import tqdm

log = logging.getLogger(__name__)

EMBEDDINGS_FILE = "embeddings.npz"

# Keep Hugging Face from sending usage telemetry.
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")


def load_cache(out_dir, model_name):
    path = Path(out_dir) / EMBEDDINGS_FILE
    if not path.exists():
        return {}
    data = np.load(path, allow_pickle=False)
    if str(data["model_name"]) != model_name:
        log.info("Embedding model changed (%s -> %s); recomputing", data["model_name"], model_name)
        return {}
    return dict(zip(data["keys"].tolist(), data["vectors"]))


def save_cache(out_dir, model_name, cache):
    path = Path(out_dir) / EMBEDDINGS_FILE
    keys = sorted(cache)
    vectors = np.stack([cache[k] for k in keys]) if keys else np.zeros((0, 0), np.float32)
    tmp = path.with_name("embeddings.tmp.npz")
    np.savez(tmp, keys=np.array(keys), vectors=vectors, model_name=np.array(model_name))
    os.replace(tmp, path)


def normalize_exposure(arr, target, max_gain):
    """Scale an RGB float array (0..1) so its mean brightness becomes `target`
    (0..1). The gain is clamped to [1/max_gain, max_gain] so a nearly black
    frame is not amplified into pure noise. `target` <= 0 turns it off.
    Why: DINOv2 reacts to exposure - the same cufflinks shot dark and bright
    scored 0.61 (talici 2, 8895/8896) although the frames are identical."""
    if target <= 0:
        return arr
    mean = float(arr.mean())
    if mean <= 0:
        return arr
    gain = min(max(target / mean, 1.0 / max_gain), max_gain)
    return np.clip(arr * gain, 0.0, 1.0)


def _prepare_batch(paths, size, mean, std, exposure_target=0.0, max_gain=4.0):
    arrays = []
    for p in paths:
        with Image.open(p) as img:
            img = img.convert("RGB").resize((size, size), Image.Resampling.BICUBIC)
            arr = np.asarray(img, dtype=np.float32) / 255.0
            arrays.append(normalize_exposure(arr, exposure_target, max_gain))
    batch = (np.stack(arrays) - mean) / std
    return batch.transpose(0, 3, 1, 2)  # NHWC -> NCHW


def compute_embeddings(photos, out_dir, config):
    """Return {sha256: unit vector} for all photos with status 'ok'."""
    emb_cfg = config["embedding"]
    model_name = emb_cfg["model_name"]
    exposure_target = float(emb_cfg.get("exposure_target", 0.0))
    max_gain = float(emb_cfg.get("exposure_max_gain", 4.0))
    # Preprocessing is part of the cache identity: changing it recomputes everything.
    cache_tag = model_name if exposure_target <= 0 else f"{model_name}|exposure={exposure_target:g}/{max_gain:g}"
    out_dir = Path(out_dir)
    cache = load_cache(out_dir, cache_tag)

    todo = [p for p in photos if p["status"] == "ok" and p["sha256"] not in cache]
    # Byte-identical copies share a sha256; embed each content once.
    todo = list({p["sha256"]: p for p in todo}.values())
    log.info("Embeddings: %d cached, %d to compute (%s)", len(cache), len(todo), model_name)

    if todo:
        import torch
        from transformers import AutoImageProcessor, AutoModel

        processor = AutoImageProcessor.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name).to(emb_cfg["device"]).eval()
        mean = np.array(processor.image_mean, dtype=np.float32)
        std = np.array(processor.image_std, dtype=np.float32)
        size = emb_cfg["input_size"]
        bs = emb_cfg["batch_size"]

        for start in tqdm(range(0, len(todo), bs), desc="Embed", unit="batch"):
            chunk = todo[start:start + bs]
            batch = _prepare_batch([out_dir / p["thumb_file"] for p in chunk], size, mean, std,
                                   exposure_target, max_gain)
            with torch.inference_mode():
                out = model(pixel_values=torch.from_numpy(batch).to(emb_cfg["device"]))
            vectors = out.pooler_output.float().cpu().numpy()
            vectors /= np.linalg.norm(vectors, axis=1, keepdims=True) + 1e-12
            for p, v in zip(chunk, vectors):
                cache[p["sha256"]] = v
            if (start // bs) % 20 == 19:
                save_cache(out_dir, cache_tag, cache)
        save_cache(out_dir, cache_tag, cache)
    return cache
