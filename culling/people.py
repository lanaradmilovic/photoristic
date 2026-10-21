"""Person detection: does a photo contain people? (YOLOS-tiny, local CPU)

Used by grouping: photos WITHOUT people (decor, food, detail shots) are safe to
group more aggressively, because the "different person, same spot and pose"
failure mode of DINOv2 similarity cannot occur. Photos WITH people keep the
strict thresholds.

Results are cached in people.json keyed by file sha256, like embeddings.npz.
Tiny background figures are ignored: a person only counts if the detection
score reaches `score_threshold` and the box covers at least
`min_box_area_fraction` of the image.
"""
import json
import logging
import os
from pathlib import Path

from PIL import Image
from tqdm import tqdm

log = logging.getLogger(__name__)

PEOPLE_FILE = "people.json"

os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")


def load_cache(out_dir, model_name):
    path = Path(out_dir) / PEOPLE_FILE
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if data.get("model_name") != model_name:
        log.info("Person detection model changed (%s -> %s); recomputing",
                 data.get("model_name"), model_name)
        return {}
    return data["has_people"]


def save_cache(out_dir, model_name, cache):
    path = Path(out_dir) / PEOPLE_FILE
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"model_name": model_name, "has_people": cache}, f)
    os.replace(tmp, path)


def detect_people(photos, out_dir, config):
    """Return {sha256: bool} for all photos with status 'ok'.

    When `people.enabled` is false, returns {} - grouping then treats every
    photo as containing people (the conservative pre-detection behaviour).
    """
    cfg = config["people"]
    if not cfg["enabled"]:
        return {}
    model_name = cfg["model_name"]
    out_dir = Path(out_dir)
    cache = load_cache(out_dir, model_name)

    todo = [p for p in photos if p["status"] == "ok" and p["sha256"] not in cache]
    todo = list({p["sha256"]: p for p in todo}.values())
    log.info("Person detection: %d cached, %d to compute (%s)", len(cache), len(todo), model_name)

    if todo:
        import torch
        from transformers import AutoImageProcessor, AutoModelForObjectDetection

        processor = AutoImageProcessor.from_pretrained(model_name)
        model = AutoModelForObjectDetection.from_pretrained(model_name).eval()
        person_ids = {i for i, name in model.config.id2label.items() if name == "person"}
        min_area = cfg["min_box_area_fraction"]

        for p in tqdm(todo, desc="People", unit="img"):
            with Image.open(out_dir / p["thumb_file"]) as img:
                img = img.convert("RGB")
                inputs = processor(images=img, return_tensors="pt")
                with torch.inference_mode():
                    outputs = model(**inputs)
                target = torch.tensor([[img.height, img.width]])
                result = processor.post_process_object_detection(
                    outputs, threshold=cfg["score_threshold"], target_sizes=target)[0]
                area = img.width * img.height
                found = False
                for label, box in zip(result["labels"].tolist(), result["boxes"].tolist()):
                    if label in person_ids:
                        x0, y0, x1, y1 = box
                        if (x1 - x0) * (y1 - y0) >= min_area * area:
                            found = True
                            break
                cache[p["sha256"]] = found
            if len(cache) % 100 == 0:
                save_cache(out_dir, model_name, cache)
        save_cache(out_dir, model_name, cache)
    return cache
