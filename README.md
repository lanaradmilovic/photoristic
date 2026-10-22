# Photoristic — automatic culling of wedding photos

Pre-selects wedding photos for a photo agency. After each wedding the agency has
2,000–3,000 photos from **two photographers** (Nikon NEF and/or JPG). Manual culling
takes about 3 hours; the goal is about 20 minutes of review.

**The one rule that overrides everything else: never lose a good photo.**
Keeping too many is acceptable, dropping an important moment is not. Every
uncertain decision is routed to the photographer for review.

See [PLAN.md](PLAN.md) for phases, status and open questions.

---

## Architecture

```
 wedding folder (NEF / JPG, any sub-folder layout)
        │
        ▼
 1. INGEST            culling/ingest.py, culling/metadata.py        [done]
    pair NEF+JPG, sha256, EXIF (time+subsec, camera serial, orientation),
    embedded JPEG preview (no RAW decoding), orient, downscale
        │  photos.json, previews/, thumbs/
        ▼
 2. GROUP             culling/embed.py, culling/people.py,          [done]
                      culling/faces.py, culling/grouping.py
    DINOv2 embeddings + person detection + face identities (all local, CPU)
    + per-camera time/similarity grouping
        │  embeddings.npz, people.json, faces.npz, identities.json,
        │  groups.json, report.html (culling/report.py)
        ▼
 3. SCORE (VLM)       Qwen3.5-9B on vLLM, one request per group     [planned]
    structured JSON per photo: decision, rank, eyes, blur, distractions,
    moment type, reason
        │  scores/<group_id>.json
        ▼
 4. EXPORT            JSON / CSV + XMP sidecars for Lightroom       [planned]
        ▼
 5. EVALUATE          vs. the agency's real selections from past weddings  [planned]
        ▼
 6./7. Compare VLMs (Claude Haiku 5.5 on Bedrock), learn from photographer corrections  [planned]
```

Each step reads the previous step's files from the output folder and writes its own.
This means:
- Steps can be re-run independently, e.g. re-group with new thresholds without re-ingesting.
- The pipeline can resume after an interruption.
- Steps 1–2 run **without the VLM server**. The EC2 instance is only needed for step 3.

### Design decisions

| Decision | Why |
|---|---|
| NEF and JPG with the same name in the same folder are **one photo** | The photographer shoots RAW+JPG; both files are the same moment. The preview comes from the JPG (falling back to the NEF's embedded JPEG). Metadata comes from the NEF first. XMP will go next to the NEF. |
| No RAW decoding | `rawpy.extract_thumb()` returns the embedded full-size JPEG, which is fast and good enough for judging. |
| Orientation from the **NEF's** EXIF | Nikon's embedded preview is stored unrotated; the rotation lives in the NEF's IFD0. JPGs use their own EXIF orientation. |
| Camera identified by **serial number** from EXIF, never by folder | Folder layouts vary between weddings. If there is no serial, make+model is used and a warning is logged, because two bodies of the same model would merge. |
| Grouping **per camera** | The two cameras' clocks are not synchronized, so their timestamps cannot be compared. |
| DINOv2-small embeddings on CPU, local | DINOv2 captures visual layout and composition, which is what matters for near-duplicates; CLIP captures semantic meaning instead. The model is small enough for CPU, and no image leaves the machine. |
| Face identities (SCRFD + AuraFace/ArcFace, ONNX on CPU) as a second grouping signal | DINOv2 cannot tell "the same couple in a new pose" (should merge, 0.72–0.90) from "a different guest at the same spot" (must not, ~0.88). Face identities can: exactly the same people → relaxed thresholds; no identity in common → never merged. Models are Apache 2.0 and run locally (`models/auraface/`). |
| Whole-frame resize (no center crop) before embedding | Shots that differ only at the frame edges should still differ. |
| Failed or undated photos become **single-photo groups with a flag** | Nothing is dropped silently. They show up in the report under *Problems*. |
| Invariant check: every photo is in exactly one group | Enforced in code (`check_every_photo_once`) and tests. |
| Swappable VLM client (phase 3) | Results will be compared against Claude Haiku 5.5 on Bedrock; the endpoint and model name come from config. |

---

## Grouping algorithm (step 2)

For each camera, photos are sorted by capture time (with sub-seconds when the
camera writes `SubSecTimeOriginal`, then by filename). Walking in order, each photo
collects **candidate groups** and joins the one it is most similar to; with no
candidate it starts a new group.

**Candidate 1: the previous photo's group** (`should_join`). It qualifies when either holds:
- **(a)** gap to the previous photo ≤ `time_gap_seconds` **and** cosine similarity ≥ `similarity_threshold` (a burst), or
- **(b)** gap ≤ `extended_gap_seconds` **and** similarity ≥ `high_similarity_threshold` (the same frame taken again a few seconds later).

**Drift guard.** In both cases, the photo's *average* similarity to all photos of the group
must also be ≥ `min_mean_similarity_to_group` (0.70). This stops a slowly changing scene
from chaining on. Because the average is used, a burst where the subject moves is not cut
in the middle.

**Candidate 2: look-back** (`find_lookback_group`). The photo may be a *return* to an earlier
scene: the photographer shot something else for a few frames and came back. An earlier group
of the same camera is a candidate when all of these hold:
- the group's last photo is at most `lookback_seconds` old (120);
- the photo's best match in that group has similarity ≥ `lookback_similarity_threshold` (0.90);
- the photo passes the drift guard;
- the group would not span more than `max_group_span_seconds` (180).

The look-back threshold is high on purpose. DINOv2 does not tell people apart: a different
guest photographed at the same spot and pose scores 0.85–0.88. Merging two guests is the error
that could lose a photo; a missed merge only costs review time.

Look-back groups are not continuous in time. Their photos are marked ↩ in the report, and the
group gets the flag `lookback`. Set `lookback_seconds: 0` to turn look-back off.

**Boundary refinement** (`refine_boundaries`). While walking, a photo is compared only with
photos taken before it. Afterwards, for every two consecutive groups at most
`extended_gap_seconds` apart, the last photo of the first group (or the first photo of the
second) moves to the other group when its average similarity there is higher by more than
`refine_margin` (0.02). Moved photos are marked ⇄, and the group gets the flag `moved`.
Turn it off with `refine_boundaries: false`.

**Face identities** (`culling/faces.py`, section `faces` in the config). Every preview is
run through a face detector (SCRFD-10G, 5 keypoints); each face is aligned to the ArcFace
template and embedded with AuraFace (ArcFace ResNet100, 512-d). Per wedding, faces are
clustered into identities (Chinese Whispers on faces with cosine similarity ≥
`identity_threshold`, then clusters whose centroids are ≥ `identity_merge_threshold` apart
are merged, which joins e.g. the bride with and without sunglasses) and labelled `A`, `B`, …
by number of faces, so the couple is normally `A` and `B`. Only identities with at least
`min_identity_faces` faces are *known*; rarer faces (a profile, a background guest) are
unknown and never speak for or against a merge. Each photo gets a signature: its set of
known identities and its number of faces. When two photos are compared (neighbour,
look-back, boundary refinement):

- **same people** (identical identity sets, same number of faces): the relaxed `faces_*`
  rules apply as well — gap ≤ `faces_gap_seconds` and similarity ≥
  `faces_similarity_threshold`, look-back at `faces_lookback_similarity_threshold`, drift
  guard at `faces_min_mean_similarity_to_group`. This merges a couple session where the
  same two people pose differently at the same spot.
- **different people** (both have known identities, none in common): the photos do not join
  by the extended-gap, look-back or no-people rules even when DINOv2 would allow it. A burst
  (within `time_gap_seconds`) is never blocked: a face hidden in one frame is not a change
  of people.
- With `faces_same_allows_unknown: true`, an unidentified face may stand in for a missing
  known person (`{A,B}` vs `{B}` + one unknown face counts as the same couple). More of a
  couple session merges, but an unknown face may also be the next guest in a hug line.
- anything else (no identified face on one side, partial overlap such as the bride with two
  different guests): the usual rules, unchanged.

The report shows the number of faces and the identity labels under each photo (`👤2 A,B`),
and badges *joined: same people* / *kept apart: different people* on the groups face
identity changed. `python cull.py faces --output … --sheets` writes one contact sheet per
identity to `faces_sheets/` for checking the clustering by eye. `faces.enabled: false`
restores the previous behaviour exactly.

Groups are not split by size (`max_group_size: 0`, the default). Setting it to a positive number
re-enables the old behaviour: larger groups are cut at their weakest consecutive similarity into
chunks linked through `split_from` and `split_part`. Context limits of the VLM step should be
handled there (overlapping chunks), not by cutting real groups.

All thresholds are in `config.yaml` under `grouping`. To tune them:

```bash
python cull.py group --output D:\cull\wedding-2024-06-15
```

This re-groups from the cached embeddings and rewrites `report.html` in seconds.

---

## Output folder

| File | Written by | Content |
|---|---|---|
| `photos.json` | ingest | `{created, input_dir, photos: [record…]}`, one record per photo, failures included |
| `previews/<id>.jpg` | ingest | oriented preview, long edge `ingest.preview_long_edge` (1536); input for the VLM |
| `thumbs/<id>.jpg` | ingest | oriented thumbnail, long edge `ingest.thumb_long_edge` (320); used for the report and embeddings |
| `embeddings.npz` | group | `keys` (sha256), `vectors` (L2-normalized), `model_name` |
| `people.json` | group | `{model_name, has_people: {sha256: bool}}` from person detection |
| `faces.npz` | group / faces | per face: `face_key` (sha256), `face_bbox`, `face_score`, `face_kps` (5×2, preview px), `face_emb` (512-d); `photo_keys` lists every processed photo |
| `identities.json` | group / faces | `{threshold, identities: {label: {n_faces, n_photos}}, photos: {sha256: {ids, faces, n_faces}}}` |
| `faces_sheets/<label>.jpg` | faces --sheets | contact sheet of all faces of one identity (review only) |
| `groups.json` | group | `{created, config_used, n_groups, n_photos, groups: [group…]}` |
| `report.html` | group / report | visual check of the groups |
| `cull.log` | all | file names, counts, timings and errors; never image content |

**Photo record** (`photos.json`):

| Field | Meaning |
|---|---|
| `id` | First 16 hex characters of the SHA-256 of the primary file (the NEF if present). Byte-identical copies get a `-dupN` suffix. Failed hashing gives `err-…`. |
| `sha256` | Full hash of the primary file. Used as the cache key for embeddings. |
| `primary_path`, `nef_path`, `jpg_path` | Absolute paths. `primary_path` is the NEF if present. |
| `preview_source` | `jpg` or `nef_embedded`. |
| `preview_file`, `thumb_file` | Paths relative to the output folder. |
| `capture_time` | ISO 8601 local camera time, e.g. `2024-06-15T16:23:45.370000`. `null` if unknown. |
| `capture_time_has_subsec` | Whether sub-second precision came from EXIF. |
| `camera_id` | `SN<serial>`, or `<make> <model>` if there is no serial. |
| `camera_serial`, `camera_make`, `camera_model` | Raw EXIF values. |
| `orientation` | EXIF orientation (1–8) that was applied to the preview. |
| `preview_w/h`, `original_preview_w/h` | Size of the saved preview and of the source JPEG. |
| `file_size`, `mtime_ns` | Used for resume. |
| `status`, `error` | `ok` or `error`, plus the reason. |
| `flags` | Any of `no_timestamp`, `no_camera_serial`, `preview_fallback`, `duplicate_file`. |

**Group record** (`groups.json`):

| Field | Meaning |
|---|---|
| `group_id` | e.g. `g0001` |
| `camera_id` | Camera the group belongs to. |
| `photo_ids` | Photo ids in capture order. |
| `size`, `start`, `end` | Number of photos and time span. |
| `consecutive_similarities`, `consecutive_gaps_seconds` | Between neighbours; length is `size-1`. For a look-back photo they are the time since the group's last photo and the similarity to its best-matching photo. |
| `joined_by` | For each photo after the first: `neighbour`, `lookback`, or `moved` (moved by boundary refinement). |
| `min_similarity` | Weakest link in the group. |
| `boundary_similarity`, `boundary_gap_seconds` | Between this group's first photo and the previous photo of the same camera, i.e. why the cut happened. |
| `split_from`, `split_part` | Set when an oversized group was split, e.g. `split_part: [2, 3]`. |
| `flags` | `split`, `lookback`, `moved`, `faces` (a photo joined only because both show the same identified people), `faces_split` (a join the usual rules allowed was blocked because the identified people differ), `ingest_error`, `no_timestamp`, `no_embedding`. |

---

## Setup (Windows, Python 3.11)

```bash
python -m venv .venv
```

```bash
.venv\Scripts\python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
```

```bash
.venv\Scripts\python -m pip install -r requirements.txt
```

The first `prepare` downloads `facebook/dinov2-small` (about 90 MB) and
`PekingU/rtdetr_v2_r18vd` from Hugging Face into `%USERPROFILE%\.cache\huggingface`. After
that, set `HF_HUB_OFFLINE=1` to forbid any network access during steps 1–2.

The face models are not downloaded automatically. Put `scrfd_10g_bnkps.onnx` and
`glintr100.onnx` from the Hugging Face repo `fal/AuraFace-v1` (Apache 2.0) into
`models/auraface/`, or point `faces.detector_path` / `faces.embedder_path` elsewhere.

## Usage

Run the whole of steps 1–2 for one wedding:

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

Every command accepts `--config path\to\config.yaml` (default: `config.yaml` next to `cull.py`).

Run the tests:

```bash
.venv\Scripts\python -m pytest
```

### Report

- **Top:** totals, a group-size histogram, photos per camera and the thresholds used.
- **Body:** one row per group, by camera and in time order.
  - Under each thumbnail are the time gap and the similarity to the previous photo. For the first photo of a group these describe the cut from the previous group.
  - Low similarities are highlighted.
  - Click a thumbnail for the preview; use ←/→ to move and Esc to close.
  - Filters: hide single photos, only flagged groups (split or low similarity), and one camera.
- **End:** the *Problems* section lists failed and undated files.

---

## Privacy

The photos contain the faces of wedding guests.

- No image or derived data is sent anywhere except the user's own vLLM server, reached through an SSH tunnel (phase 3).
- Embeddings, person detection and face recognition are computed locally. Hugging Face is contacted only to download the model weights once, with telemetry disabled (`HF_HUB_DISABLE_TELEMETRY=1`).
- Face embeddings and identity labels stay in the output folder (`faces.npz`, `identities.json`); identities are anonymous letters, never names.
- The report is a static local file with no external scripts, fonts or CDNs.
- Logs contain file names, counts, timings and errors, never image content or base64.

## Infrastructure (for phase 3)

- **VLM:** Qwen3.5-9B served by vLLM on AWS EC2 g6.xlarge (NVIDIA L4 24 GB, eu-central-1), with `--max-model-len 16384` and thinking disabled.
- **Access:** an SSH tunnel to `http://localhost:8000/v1` (OpenAI-compatible API).
- The instance runs only during work sessions, so the scoring step must resume per group.
- The endpoint, model name and API-key environment variable are in `config.yaml` → `vlm`.

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
culling/report.py     report.html
tests/                pytest, synthetic data only
```
