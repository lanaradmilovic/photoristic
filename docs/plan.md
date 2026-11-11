# Plan — wedding photo culling

Where we are going and what must not change. The next concrete steps are in [todo.md](todo.md);
how things work today is in [spec/](spec/); why, in [decisions/](decisions/).

## Goal and the hard rule

- **Input:** 2,000–3,000 photos per wedding, always from two photographers, Nikon NEF and/or JPG.
- **Today:** about 3 hours of manual culling. **Target:** about 20 minutes of review.
- **The agency's constraint:** they will not train tools like Aftershoot or Imagen themselves. They
  want a ready-made solution.
- **Hard rule: never lose a good photo.** False "keep" decisions are cheap; false "reject"
  decisions are the failure we optimise against. Every uncertain decision goes to the photographer.

## Fixed constraints

- **Development environment:** Windows, Python 3.11, CPU-only workstation.
- **VLM:** Qwen3.5-9B on vLLM, AWS EC2 g6.xlarge (L4 24 GB, Frankfurt)
  ([0018](decisions/0018-swappable-vlm-client-own-server.md)).
  - Reached through an SSH tunnel at `http://localhost:8000/v1` (OpenAI-compatible API; locally
    port 8001, see [vlm-judge](spec/vlm-judge.md#running)).
  - Runs with `--max-model-len 16384` and thinking disabled.
  - The instance runs only during work sessions, so the pipeline must work without it (steps 1–2)
    and every VLM step must resume.
- **Swappable VLM client:** a later comparison with Claude Haiku 5.5 on AWS Bedrock must be
  possible. Endpoint and model name come from `config.yaml`.
- **Privacy:** photos show guests' faces.
  - Nothing goes to external services except the user's own vLLM server. Embeddings, person
    detection and face recognition run locally; Hugging Face only downloads weights once
    (telemetry off, `HF_HUB_OFFLINE=1` afterwards).
  - Face identities are anonymous letters, never names, and stay in the output folder.
  - Image content and base64 are never logged. The report has no external scripts, fonts or CDNs.
- **Code style:** simple, readable code with no over-abstraction. Tunables live in `config.yaml`.
- **No model training** until phase 7.
- **No GUI** except static HTML reports.

## Phases

| # | Phase | Status |
|---|---|---|
| 0 | Project setup, docs, config | done |
| 1 | Ingest: previews + metadata | done; needs a two-camera wedding |
| 2 | Grouping + HTML report (+ faces, labels, judge dry-run, segments) | done; tuning with labels; judge not yet run |
| 3 | VLM scoring per group | next ([design](spec/vlm-scoring.md)) |
| 4 | Export: JSON/CSV + XMP for Lightroom | planned |
| 5 | Evaluation against past agency selections | planned |
| 6 | Second VLM: Claude Haiku 5.5 on Bedrock | planned |
| 7 | Learning from photographer corrections | planned |

### Phase 1 — Ingest

Done ([spec](spec/ingest.md)). Still to check:
- [ ] A wedding with **both** cameras: distinct `camera_id` per body; orientation of portrait shots checked visually.
- [ ] Ingest time for ~2,500 NEF is acceptable (roughly < 15 min). Record the actual time in the log.
- Risks: bodies without `BodySerialNumber`; bodies that embed only a small preview (fallback
  RAW decode not implemented).

### Phase 2 — Grouping

Done ([spec](spec/grouping.md)). Acceptance:
- [x] Invariant: every photo in exactly one group.
- [x] Ground truth exists for 4a ([labels](spec/labels.md)).
- [ ] Ground truth for Talici 1; scores recorded for every grouping change.
- [ ] The VLM judge measured against labels before it influences grouping ([0016](decisions/0016-vlm-judge-grey-zone-only.md)).

Direction (2026-10-21): per-segment grouping profiles (segments at > 5 min pauses), face identities,
and the VLM judge only in the 0.80–0.90 band.

### Phase 3 — VLM scoring

Design in [spec/vlm-scoring.md](spec/vlm-scoring.md). Acceptance: a full wedding scored across
several EC2 sessions with no duplicate work; every photo gets a decision; score files validate.

### Phase 4 — Export

- `culling/export.py` writes `results.csv` and `results.json`, one row per photo (group, decision, rank, attributes).
- **XMP sidecars** (`<name>.xmp` next to the NEF): `xmp:Rating` keep = 3–5 by rank, maybe = 2,
  reject = 1; `xmp:Label` (colour) for "needs review"; `dc:subject` keywords (`cull:keep`, `moment:first_kiss`).
- An existing `.xmp` is **never overwritten** without a backup (`.xmp.bak`); the photographer's edits are merged where possible.
- **Open — JPG-only photos:** Lightroom reads sidecars only for RAW; for JPG it reads embedded XMP.
  Options: (a) write into the JPG (modifies the original; needs the agency's consent), or (b) a
  Lightroom plugin / catalog import. Decide with the agency.
- Optional: a review HTML showing only `maybe` photos, for the 20-minute check.

### Phase 5 — Evaluation

- **Input:** past weddings with the agency's real selection (exported files, a list of names, or
  XMP ratings). Format to agree with the agency.
- `cull.py evaluate --output <out> --truth <selection>` reports:
  - **recall of agency-selected photos** (primary; target ≥ 99 % counting keep + maybe; every miss listed with its thumbnail);
  - reduction: the share auto-rejected;
  - review load: number of `maybe` photos (≈ the 20-minute target);
  - per group: whether the agency's pick is in our top ranks.
- Thresholds and prompt are tuned only against these numbers.

### Phase 6 — Second VLM (Claude Haiku 5.5 on Bedrock)

- `BedrockClient` with the same `score_group` signature, `vlm.provider: bedrock`.
- **Privacy:** sends images to AWS Bedrock; the agency must approve before any real wedding.
- Compare both models on phase 5 metrics, cost and time per wedding.

### Phase 7 — Learning from corrections

- Log the photographer's changes: final Lightroom ratings vs our proposal (from XMP or the catalog).
- Train a small model (logistic regression or gradient boosting) over VLM attributes, group context and EXIF.
- Per agency, with no image data stored beyond the attributes.
- The hard rule still applies ([0019](decisions/0019-safety-rules-in-code.md)).
