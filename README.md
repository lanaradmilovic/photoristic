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
 2d. SEGMENTS         culling/segments.py                          [done]     docs/spec/segments.md
    cut the day into parts at shooting pauses, per-segment statistics
        │  segments.json, segments_sheets/ (--sheets)
        ▼
 3. RANK (VLM)        culling/ranking.py, variants + best frame     [dry-run]  docs/spec/vlm-scoring.md
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
| `prepare --input X --output Y [--exclude FOLDER ...]` | Ingest → embeddings → grouping → report. Safe to re-run: unchanged files are not re-processed. `--exclude` skips folders inside X that hold no photos of the day (montages, exports). |
| `agency --input X --output Y [--exclude ...] [--rejected F \| --after D] [--keep-originals]` | For a wedding from the agency: `prepare`, then their cull from a list of rejected names (`dir /b > obrisano.txt`) or their culled folder → `agency_cull.json`, then **deletes the originals** (and the copies in D) of every photo that has its preview and group; the list is `originals_deleted.txt`, and ingest refuses to run after that ([spec](docs/spec/ingest.md#agency-packages)). |
| `analysis --output Y --wedding docs/weddings/<id>` | One wedding before and after the agency's cull, in the fixed format for comparing weddings: `Y/analysis/photos.csv` and `summary.json` next to `wedding.json` ([spec](docs/spec/wedding-analysis.md)). Needs `agency_cull.json`. |
| `ingest --input X --output Y [--exclude FOLDER ...]` | Step 1 only. |
| `group --output Y` | Embeddings, people, faces (all cached) → grouping → segments → report. Use it after changing thresholds. |
| `faces --output Y [--sheets]` | Face detection + identity clustering only; `--sheets` writes `faces_sheets/` for review. |
| `segments --output Y [--sheets]` | Cut the day into segments at shooting pauses → `segments.json`; `--sheets` writes `segments_sheets/`. |
| `report --output Y` | Rebuild `report.html` from the existing JSON files. |
| `label --output Y [--port 8765] [--no-browser]` | Serve the report on `127.0.0.1` and save ground-truth labels to `labels.json` ([labels](docs/spec/labels.md)). |
| `score --output Y [--groups F [F]] [--labels FILE]` | Compare `labels.json` (or another labels file, e.g. the agency's `meeting_answers.json`) with `groups.json` (or the given files) and write `errors.jpg`. |
| `meeting --output M` / `meeting-score --output M` | Feedback page for a meeting with the agency (disputed pairs, excerpts of the grouping, questions), built from `M/meeting.json`; summary of the answers ([labels](docs/spec/labels.md#agency-meeting-page)). |
| `judge --output Y [--dry-run] [--include-faces-decided] [--max-pairs N]` | Grey-zone pairs for the VLM judge ([vlm-judge](docs/spec/vlm-judge.md)). Not part of `prepare`. |
| `rank --output Y [--dry-run] [--max-requests N]` | Best photo(s) per group: keep / maybe in `ranking.json` and the report ([vlm-scoring](docs/spec/vlm-scoring.md)). Not part of `prepare`. |
| `pick --output Y [--sample F] [--picks-file N]` / `pick-score --output Y [--picks-file N] [--compare N]` | Mark the best photo(s) per group in the browser, with optional reasons and notes; compare `ranking.json` with them ([labels](docs/spec/labels.md#best-photo-picks)). |
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
culling/agency.py     the agency's cull (agency_cull.json), deleting originals after prepare
culling/analysis.py   before/after analysis of one wedding: photos.csv, summary.json
culling/embed.py      DINOv2 embeddings + cache
culling/people.py     person detection (RT-DETR) + cache
culling/faces.py      face detection (SCRFD), alignment, ArcFace embeddings, identity clustering
culling/grouping.py   grouping algorithm + groups.json
culling/segments.py   day segments at shooting pauses + segments.json + segments_sheets/
culling/report.py     report.html (group view + label mode)
culling/labels.py     labels.json I/O, boundaries between adjacent photos, scoring, errors.jpg
culling/labelserver.py local http server for `cull.py label`, `pick` and `meeting` (GET/POST /labels, /picks, /meeting)
culling/vlm.py        VLM client: OpenAI-compatible chat completions over urllib, error mapping, ping
culling/judge.py      VLM judge: pair selection, pair images, prompt + schema, judging loop with resume
culling/picks.py      best-photo picks: picks.html, picks.json, comparison with ranking.json
culling/meeting.py    agency meeting page: meeting.json -> meeting.html, meeting_answers.json, summary
culling/ranking.py    best photo per group: variants, prompt + schema, safety rules, ranking loop with resume
tests/                pytest, synthetic data only
docs/                 plan, todo, log, decisions, spec, research, datasets (see CLAUDE.md)
```
