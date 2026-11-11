# Photoristic — automatic culling of wedding photos

Pre-selects wedding photos for a photo agency. After each wedding the agency has
2,000–3,000 photos from **two photographers** (Nikon NEF and/or JPG). Manual culling
takes about 3 hours; the goal is about 20 minutes of review.

**The one rule that overrides everything else: never lose a good photo.**
Keeping too many is acceptable, dropping an important moment is not. Every
uncertain decision is routed to the photographer for review.

Documentation: [docs/plan.md](docs/plan.md) (goal, constraints, phases),
[docs/todo.md](docs/todo.md) (what is next), [docs/spec/](docs/spec/) (how it works),
[docs/decisions/](docs/decisions/README.md) (why).

## Architecture

```
 wedding folder (NEF / JPG, any sub-folder layout)
        │
        ▼
 1. INGEST            culling/ingest.py, culling/metadata.py        [done]     docs/spec/ingest.md
    pair NEF+JPG, sha256, EXIF, embedded JPEG preview, orient, downscale
        │  photos.json, previews/, thumbs/
        ▼
 2. GROUP             culling/embed.py, people.py, faces.py,        [done]     docs/spec/grouping.md
                      grouping.py, report.py
    DINOv2 embeddings + person detection + face identities (local, CPU)
    + per-camera time/similarity grouping
        │  embeddings.npz, people.json, faces.npz, identities.json, groups.json, report.html
        │
        │  2b. LABELS / SCORE   culling/labels.py, labelserver.py    [done]     docs/spec/labels.md
        │  2c. JUDGE (VLM)      culling/vlm.py, judge.py              [dry-run]  docs/spec/vlm-judge.md
        ▼
 3. SCORE (VLM)       Qwen3.5-9B on vLLM, one request per group     [planned]  docs/spec/vlm-scoring.md
        ▼
 4. EXPORT            JSON / CSV + XMP sidecars for Lightroom       [planned]
        ▼
 5. EVALUATE          vs. the agency's real selections              [planned]
        ▼
 6./7. Compare VLMs (Claude Haiku 5.5 on Bedrock), learn from corrections  [planned]
```

Each step reads the previous step's files from the output folder and writes its own
([output format](docs/spec/output-format.md)): steps re-run independently, the pipeline resumes
after an interruption, and steps 1–2 run **without the VLM server**.

## Setup (Windows, Python 3.11)

```bash
python -m venv .venv
.venv\Scripts\python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
.venv\Scripts\python -m pip install -r requirements.txt
```

The first `prepare` downloads `facebook/dinov2-small` (~90 MB) and `PekingU/rtdetr_v2_r18vd`
from Hugging Face into `%USERPROFILE%\.cache\huggingface`. After that, set `HF_HUB_OFFLINE=1`
to forbid any network access during steps 1–2.

The face models are not downloaded automatically. Put `scrfd_10g_bnkps.onnx` and
`glintr100.onnx` from the Hugging Face repo `fal/AuraFace-v1` (Apache 2.0) into
`models/auraface/`, or point `faces.detector_path` / `faces.embedder_path` elsewhere.

## Usage

```bash
.venv\Scripts\python cull.py prepare --input "D:\Weddings\2024-06-15 Ana i Marko" --output "D:\cull\2024-06-15"
```

Then open `D:\cull\2024-06-15\report.html` in a browser.

| Command | What it does |
|---|---|
| `prepare --input X --output Y` | Ingest → embeddings → grouping → report. Safe to re-run: unchanged files are not re-processed. |
| `ingest --input X --output Y` | Step 1 only. |
| `group --output Y` | Embeddings, people, faces (all cached) → grouping → report. Use it after changing thresholds. |
| `faces --output Y [--sheets]` | Face detection + identity clustering only; `--sheets` writes `faces_sheets/` for review. |
| `report --output Y` | Rebuild `report.html` from the existing JSON files. |
| `label --output Y [--port 8765] [--no-browser]` | Serve the report on `127.0.0.1` and save ground-truth labels to `labels.json` ([labels](docs/spec/labels.md)). |
| `score --output Y [--groups F [F]]` | Compare `labels.json` with `groups.json` (or the given files) and write `errors.jpg`. |
| `judge --output Y [--dry-run] [--include-faces-decided] [--max-pairs N]` | Grey-zone pairs for the VLM judge ([vlm-judge](docs/spec/vlm-judge.md)). Not part of `prepare`. |
| `ping-vlm` | Check that the VLM server (`vlm` in the config) answers and serves the configured model. |

Every command accepts `--config path\to\config.yaml` (default: `config.yaml` next to `cull.py`).

```bash
.venv\Scripts\python -m pytest
```

## Code map

```
cull.py               CLI
config.yaml           all tunables
culling/config.py     defaults + YAML loading (unknown keys are errors)
culling/metadata.py   EXIF via exifread
culling/ingest.py     scan, pair, hash, previews, photos.json, resume
culling/embed.py      DINOv2 embeddings + cache
culling/people.py     person detection (RT-DETR) + cache
culling/faces.py      face detection (SCRFD), alignment, ArcFace embeddings, identity clustering
culling/grouping.py   grouping algorithm + groups.json
culling/report.py     report.html (group view + label mode)
culling/labels.py     labels.json I/O, boundaries between adjacent photos, scoring, errors.jpg
culling/labelserver.py local http server for `cull.py label` (GET/POST /labels)
culling/vlm.py        VLM client: OpenAI-compatible chat completions over urllib, error mapping, ping
culling/judge.py      VLM judge: pair selection, pair images, prompt + schema, judging loop with resume
tests/                pytest, synthetic data only
docs/                 plan, todo, log, decisions, spec, research, datasets (see CLAUDE.md)
```
