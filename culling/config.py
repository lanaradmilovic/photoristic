"""Load config.yaml and merge it over built-in defaults.

The config is a plain nested dict: config["grouping"]["time_gap_seconds"], etc.
Unknown keys raise an error so typos in threshold names do not go unnoticed.
"""
import copy
from pathlib import Path

import yaml

DEFAULTS = {
    "ingest": {
        "preview_long_edge": 1536,
        "thumb_long_edge": 320,
        "jpeg_quality": 88,
        "workers": 4,
        "save_every": 100,
    },
    "embedding": {
        "model_name": "facebook/dinov2-small",
        "batch_size": 32,
        "device": "cpu",
        "input_size": 224,
    },
    "people": {
        # Person detection gates the relaxed "no people" grouping rules below.
        "enabled": True,
        "model_name": "PekingU/rtdetr_v2_r18vd",
        "score_threshold": 0.6,
        "min_box_area_fraction": 0.02,
    },
    "faces": {
        # Face detection + recognition (local ONNX, CPU); identities feed grouping.
        "enabled": True,
        "detector_path": "models/auraface/scrfd_10g_bnkps.onnx",
        "embedder_path": "models/auraface/glintr100.onnx",
        "det_size": 640,
        "det_threshold": 0.5,
        "nms_threshold": 0.4,
        "min_face_size": 24,
        "identity_threshold": 0.4,
        "identity_merge_threshold": 0.45,
        "min_identity_faces": 10,
    },
    "grouping": {
        "time_gap_seconds": 4.0,
        "similarity_threshold": 0.75,
        "extended_gap_seconds": 20.0,
        "high_similarity_threshold": 0.82,
        "min_mean_similarity_to_group": 0.70,
        "lookback_seconds": 120,
        "lookback_similarity_threshold": 0.90,
        # Relaxed rules when NEITHER photo contains a person (decor, food, details):
        # the "different person, same spot" risk does not exist, so same-subject
        # shots may join across longer gaps and lower similarity.
        "nopeople_gap_seconds": 45.0,
        "nopeople_similarity_threshold": 0.80,
        "nopeople_lookback_similarity_threshold": 0.86,
        # Relaxed rules when BOTH photos show exactly the same identified people
        # (faces.enabled): the same couple in a new pose is one group even when
        # DINOv2 similarity is low. Photos with no identity in common never join.
        "faces_gap_seconds": 60.0,
        "faces_similarity_threshold": 0.70,
        "faces_lookback_similarity_threshold": 0.70,
        "faces_min_mean_similarity_to_group": 0.65,
        # Let an unidentified face stand in for a missing known person when deciding
        # "same people" ({A,B} vs {B}+1 unknown). Off: an unknown face could be the
        # next guest in a congratulation line.
        "faces_same_allows_unknown": False,
        "max_group_span_seconds": 180,
        "refine_boundaries": True,
        "refine_margin": 0.02,
        "max_group_size": 0,  # 0 = never split groups (chunking belongs to the VLM step)
        "report_low_similarity": 0.85,
    },
    "segments": {
        # Day segmentation: a new segment starts at a shooting pause longer than gap_seconds.
        "enabled": True,
        "gap_seconds": 300,
        "min_photos": 5,
        "sheet_max_thumbs": 48,
    },
    "vlm": {
        "provider": "openai_compatible",
        "base_url": "http://localhost:8000/v1",
        "model": "Qwen/Qwen3.5-9B",
        "api_key_env": "VLM_API_KEY",
        "timeout_seconds": 120,
        "max_retries": 3,
        "image_long_edge": 1024,
    },
}


def load_config(path=None):
    config = copy.deepcopy(DEFAULTS)
    if path is None:
        return config
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, encoding="utf-8") as f:
        user = yaml.safe_load(f) or {}
    for section, values in user.items():
        if section not in config:
            raise ValueError(f"Unknown config section '{section}' in {path}")
        for key, value in (values or {}).items():
            if key not in config[section]:
                raise ValueError(f"Unknown config key '{section}.{key}' in {path}")
            config[section][key] = value
    return config
