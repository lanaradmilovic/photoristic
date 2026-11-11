# PLAN — wedding photo culling

The working plan for all sessions. Read this together with [README.md](README.md),
which describes the architecture, file formats and commands. Update the **Status**
column and the phase notes at the end of every session.

## Goal and the hard rule

- **Input:** 2,000–3,000 photos per wedding, always from two photographers, in Nikon NEF and/or JPG.
- **Today:** about 3 hours of manual culling. **Target:** about 20 minutes of review.
- **The agency's constraint:** they will not train tools like Aftershoot or Imagen themselves. They want a ready-made solution.
- **Hard rule: never lose a good photo.** False "keep" decisions are cheap; false "reject" decisions are the failure we optimise against. Every uncertain decision goes to the photographer for review.

## Fixed constraints

- **Development environment:** Windows, Python 3.11, CPU-only workstation.
- **VLM:** Qwen3.5-9B on vLLM, AWS EC2 g6.xlarge (L4 24 GB, Frankfurt).
  - Reached through an SSH tunnel at `http://localhost:8000/v1` (OpenAI-compatible API).
  - Runs with `--max-model-len 16384` and thinking disabled.
  - The instance runs only during work sessions, so the pipeline must work without it (steps 1–2) and must resume.
- **Swappable VLM client:** a later comparison with Claude Haiku 5.5 on AWS Bedrock must be possible. The endpoint and model name come from `config.yaml`.
- **Privacy:** photos show guests' faces.
  - Nothing goes to external services except the user's own vLLM server. Embeddings are computed locally.
  - Image content is never logged.
- **Code style:** simple, readable code with no over-abstraction. Tunables live in `config.yaml`.
- **No model training** until phase 7.
- **No GUI** except static HTML reports.

## Phases

| # | Phase | Status |
|---|---|---|
| 0 | Project setup, docs, config | **done** (session 1) |
| 1 | Ingest: previews + metadata | **done** (session 1); needs validation on real NEFs |
| 2 | Grouping + HTML report | **done** (session 1); thresholds need tuning on a real wedding |
| 3 | VLM scoring per group | next |
| 4 | Export: JSON/CSV + XMP for Lightroom | planned |
| 5 | Evaluation against past agency selections | planned |
| 6 | Second VLM: Claude Haiku 5.5 on Bedrock | planned |
| 7 | Learning from photographer corrections | planned |

## Open work

The list a new session reads first. Remove an item when it is done; record the result in the session log.

- **Grouping: a person added to or missing from a group photo must split the group.** Rule decided
  by the user 2026-11-11 (README, "What a group is"). Today `identity_relation` (`culling/grouping.py`)
  returns None for a partial overlap ({A,B,C} vs {A,B,C,D}), so DINOv2 similarity decides and such
  pairs merge (also seen on Talici 1: a group of 3 men joined with a group of 4). Proposed rule: a
  known identity present on one side and absent on the other blocks the join. Risk: a turned head
  hides a face while the person is still there, so measure with `cull.py score` on 4a before and
  after, and look at Talici 1 party groups. The VLM prompt already carries the rule.
- **VLM judge: first real run.** Needs the user's choice of model and server or API key. Commands
  and the port-8000 tunnel note are in README, "VLM judge".
- **Merge branches.** `labels`, `segments` and `judge` are not in `master`; waiting for the user's review.
- **Labels for Talici 1.** Only 4a is labelled (`data/out-4a/labels.json`, 333 pairs). Talici 1 is
  the over-splitting extreme and is needed next to 4a for every grouping change.
- **Labelling tool: look-back joins.** Only adjacent pairs can be labelled; "photo 5 belongs with
  photo 2" cannot be recorded. Add such a label if the user sees it often.
- **Day segments: 4 missed cuts.** At `gap_seconds: 300` four real part-of-day changes are not cut
  (Talici 3 bride portraits | first look, groom | bride prep, car | church; Talici 4 guest candids |
  sunset session). Pauses cannot separate them from superfluous cuts (both 189-266 s), so this needs
  content (VLM segment classification), not another threshold.

---

### Phase 0 — Setup (done)

**Delivered:**
- `cull.py` CLI
- `config.yaml` and `culling/config.py`, which rejects unknown keys
- `requirements.txt` and `pytest.ini`
- `README.md` and `PLAN.md`

### Phase 1 — Ingest (done, pending real-data check)

**Delivered:** `culling/ingest.py`, `culling/metadata.py`, `tests/test_ingest.py`.

- **Scanning:** recursive scan; NEF+JPG with the same stem in the same folder are one photo.
- **Hash:** streamed SHA-256 of the primary file (the NEF if present).
- **Metadata (exifread):**
  - `DateTimeOriginal` + `SubSecTimeOriginal`
  - serial number: `EXIF BodySerialNumber`, then `MakerNote SerialNumber`
  - make, model, orientation
- **Preview:**
  - from the JPG if present, otherwise from the NEF's embedded JPEG (`rawpy.extract_thumb`) rotated by the NEF's orientation
  - fast decoding via `Image.draft`
  - saved as preview (1536) + thumb (320)
- **Parallelism:** a `ProcessPoolExecutor`.
- **Resume:** unchanged path, size and mtime plus existing outputs → the record is reused. `photos.json` is checkpointed every `save_every` photos.
- **Failures:** kept as `status: error` records, never dropped.

**Acceptance:**
- [x] Unit tests pass (synthetic JPGs).
- [x] Real NEF files from one photographer (`talici 4a`, 334 photos, Nikon D5):
  - every NEF yielded a full-size embedded preview (5568×3712)
  - the serial was found (`SN6501320`)
  - sub-seconds were present on all photos
  - ingest took about 57 s from OneDrive
- [ ] A wedding with **both** cameras: distinct `camera_id` per body; orientation of portrait shots checked visually.

**Real-data finding:** folders copied from a Mac contain `._<name>.NEF` AppleDouble files of 4 KB, one per photo. Ingest now skips them by name plus the magic bytes `00 05 16 07`, and logs how many it skipped. It also skips the output folder if that folder is inside the input.
- [ ] Ingest time for about 2,500 NEF files is acceptable, roughly under 15 minutes on the workstation. Record the actual time here.

**Open questions / risks:**
- Some Nikon bodies may not write `BodySerialNumber`. The fallback is `MakerNote SerialNumber`, then make+model, which logs a warning. Check this on real files.
- If a body embeds only a small preview, `original_preview_w/h` will show it. The fallback would be a RAW decode with `rawpy.postprocess(half_size=True)`; it is not implemented because it is slow.
- Full SHA-256 of about 100 GB of NEF files is I/O-bound. It is cached, so it is paid once per wedding.

### Phase 2 — Grouping + report (done, needs tuning)

**Delivered:** `culling/embed.py`, `culling/grouping.py`, `culling/report.py`, `tests/test_grouping.py`.

- **Embeddings:** DINOv2-small CLS embeddings on CPU, from the 320 px thumbnail resized to 224×224 with no crop. They are cached in `embeddings.npz` by sha256.
- **Grouping:** per camera, in time order. A photo joins the open group when (current defaults, see tuning round 1):
  - (gap ≤ 4 s **and** similarity ≥ 0.75), **or**
  - (gap ≤ 20 s **and** similarity ≥ 0.82),
  - **and** its mean similarity to the group's photos is ≥ 0.70 (until round 3 this compared against the first photo only).
  - **Look-back:** a group of the last 120 s is also a candidate if the best match is ≥ 0.90 and the group spans ≤ 180 s. The photo joins the most similar candidate.
  - The drift guard uses the *mean* similarity to the group.
  - Afterwards, `refine_boundaries` moves border photos to the group they resemble more (see tuning rounds 2 and 3).
- **Splitting:** groups larger than 12 are split into balanced chunks linked by `split_from`.
- **Report:** `report.html` with the time gap and similarity under each thumbnail, flagged groups, filters and a lightbox.

**Acceptance:**
- [x] Unit tests pass. Invariant: every photo is in exactly one group.
- [ ] On a real wedding, the user checks the report:
  - bursts and repeated frames are together
  - different moments are not merged
  - the group-size distribution is sensible
- [ ] Final thresholds are recorded here with the reasoning, e.g. "0.80 merged first kiss and walk-out; raised to 0.85".

**Tuning round 1 (`talici 4a`, 334 photos, one camera):**
- **What the user saw:** the first defaults (2 s @ 0.80, 15 s @ 0.92) left many visually near-identical photos ungrouped.
- **Why:** this photographer mostly shoots single frames, not bursts.
  - Consecutive gaps: median 6.8 s, 75th percentile 13 s.
  - Same-scene neighbours had similarity of about 0.8–0.95 even 4–15 s apart.
  - Different scenes were mostly below 0.7, with few pairs in the 0.7–0.8 range.
- **Results on the same 334 photos:**

  | Variant | Groups | Singles | Cuts between neighbours with sim ≥ 0.85 |
  |---|---|---|---|
  | Old defaults (2 s @ 0.80, 15 s @ 0.92) | 244 | 196 | 55 |
  | A (3 s @ 0.75, 15 s @ 0.85) | 190 | 115 | 6 |
  | **B (4 s @ 0.75, 20 s @ 0.82) — new default** | **168** | **89** | **4** |
  | C (5 s @ 0.72, 30 s @ 0.80) | 161 | 79 | 3 |

- **Pending:** the user's visual check of B. If B still under-groups, try C. If B merges different moments, go back toward A.
- **Known limit (fixed in round 2):** only *consecutive* photos were compared, so a return to an earlier scene started a new group.

**Tuning round 2 (2026-10-19, same 334 photos) — look-back:**
- The user listed 12 group pairs that looked like the same scene.
- **Diagnosis (numbers only):**
  - 8 pairs were *returns*: 1–6 other groups in between, 3–101 s later, and DINOv2 similarity of 0.85–0.94 to the earlier group.
  - 4 pairs were neighbours with similarity 0.71–0.81, just under the rules (0.75 within 4 s, 0.82 within 20 s).
- **Model check:** four local models were compared on these pairs: DINOv2-small CLS, DINOv2-small mean-of-patches, DINOv2-base and CLIP B/32. None was clearly better; all ranked the pairs around the 90–95th percentile of nearby photo pairs. **Decision:** keep DINOv2-small. Mean-of-patches helped the 4 neighbour cases but shifts the whole similarity scale; revisit only if needed.
- **Implemented look-back** (`find_lookback_group`): a photo that does not fit the previous photo joins the most similar group from the last 120 s if:
  - its best match there is ≥ 0.85,
  - it passes the first-photo guard,
  - the group spans ≤ 180 s.
- **Result:**
  - Groups: 168 → 154. Singles: 89 → 80. 14 groups contain look-back photos (18 photos).
  - 7 of the 12 listed pairs are now merged.
  - g0128+g0130 stays apart only because the group would span 180.2 s. With `max_group_span_seconds: 240` it merges, but g0120+g0125 then separates (8/12).
- **Still apart** (similarity below thresholds): g0097+g0098 (0.81), g0115+g0116 (0.76), g0146+g0147 (0.71), g0153+g0154 (0.79). Lowering the thresholds that far would also merge different scenes. Keeping them separate costs review time but cannot lose a photo.
- **Pending:** the user's visual check of the 14 look-back groups (filter "only flagged groups" in the report).

**Tuning round 3 (2026-10-19): A+B+C+D implemented.**
- **Config changes:**
  - `min_similarity_to_group_first` was replaced by `min_mean_similarity_to_group` (0.70);
  - `lookback_similarity_threshold` went from 0.85 to 0.90;
  - new keys `refine_boundaries` and `refine_margin`.
- **Result on talici 4a:** 158 groups, 82 singles, largest group 10. 12 groups have look-back photos and 2 have moved photos.
- **User cases:** 6 of 11 are as wanted.
  - **Fixed:** 23, 67, 128/129, 138/139, 142/143.
  - **Kept:** 72.
  - **Expected trade-off:** g0003's `_KAD9797` is now its own group.
  - **Still apart (borderline similarity):** 13/15, 106/107, 135/136.
- **The 104/105/110 scene was rearranged:**
  - `_KAD0047–0050` are now their own group.
  - `_KAD0046` and `0051–0059` form one family with `0066–0073` (split 8+8).
  - The rest of old g0110 is spread over 4 groups.
- **Pending:** the user's visual check.

**Tuning round 3 diagnosis (the analysis that led to A+B+C+D):**

*Causes found:*
1. **The embedding does not distinguish people.** In g0023 and g0067, a different person at the same spot and pose joined by look-back with similarity 0.88. A good return (g0003, `_KAD9797`) had only 0.85. No threshold separates the two. This is the most dangerous error type: two different guests in one group means one may be rejected.
2. **The drift guard compares only with the first photo, so it cuts in the wrong place.** In g0128/g0129 (a 6 s burst), neighbours were 0.83–0.94, but `_KAD0121` was 0.64 to the first photo and the cut fell in the middle of the kiss.
3. **The neighbour rule wins even when an earlier group fits better.** `_KAD0156` joined `_KAD0155` (0.84) although it is 0.92 to `_KAD0154`. Similarly, `_KAD0148` stayed with `_KAD0147` (0.81) although it is 0.87 to `_KAD0150`.
4. **Borderline similarities.** 13/15 is 0.849 against a 0.85 threshold, 106/107 is 0.76 at 17 s, and 135/136 is 0.71 at 0.8 s. These are left as they are.

The model also sees kiss vs no kiss as nearly the same frame (0.87).

*Simulated fixes (11 user cases):*
- **A:** look-back threshold 0.90.
- **B:** the guard uses the mean similarity to all group photos instead of the first photo.
- **C:** join the most similar eligible group (neighbour or look-back) instead of preferring the neighbour.
- **D:** a refinement pass that moves a boundary photo to the adjacent group if its mean similarity there is higher by more than 0.02.

| Variant | Correct (of 11) | Notes |
|---|---|---|
| Current | 2 | |
| B+C or B+C+D | 5 | no regressions |
| A+B+C+D | 6 | separates the different people in g0023/g0067; g0003 loses `_KAD9797` to its own group (costs review time, not a photo) |

*Phase 3 safety net:* the VLM prompt should report when a group shows different people or different moments. Such a group is then treated as separate photos, and nothing is rejected on the basis of the group comparison. This covers what DINOv2 cannot see.

**Why capture time is kept next to similarity (measured on the same 334 photos):**
- **Similarity alone either merges distinct moments or misses bursts:**

  | Similarity-only threshold (no time) | Largest group | Span of that group |
  |---|---|---|
  | 0.75 | 147 photos | 140 min |
  | 0.85 | 55 photos | 105 min |
  | 0.93 | — (240 of 334 photos stay single) | — |

- **Time as a brake:** 9 pairs have similarity ≥ 0.90 but were shot about 105 minutes apart (`_KAD9893–9898` at 16:11 vs `_KAD0170–0171` at 17:55). They are probably the same place at a different moment, and merging them could cost one of the moments.
- **Time as an accelerator:** 32 of 162 neighbour joins (20%) have similarity below 0.85 and were joined only because they were 0.7–3.5 s apart. People move and blink within a burst, so the embedding changes.

**Tuning loop:** edit `config.yaml` → `python cull.py group --output <out>` → reload `report.html`.

**Notes for tuning:**
- The similarity values come from DINOv2-small CLS vectors and are untested on wedding data. Expect to move `similarity_threshold` somewhere in the range 0.7–0.9.
- Merging too much is worse than splitting too much, because the VLM ranks *within* a group. A wrongly merged moment risks losing its best frame to a different scene. When in doubt, split.
- If DINOv2-small is not discriminative enough, try `facebook/dinov2-base` by changing `embedding.model_name`; the cache is invalidated automatically.

---

### Phase 3 — VLM scoring (next)

**Goal:** one VLM request per group returns structured JSON for every photo in it.

**Deliverables:**
- **`culling/vlm.py` — one small client class per provider with the same method:**

  ```python
  class OpenAICompatibleClient:   # vLLM; later BedrockClient with the same signature
      def score_group(self, group: dict, images: list[bytes]) -> list[dict]: ...
  ```

  - `make_client(config["vlm"])` picks the provider.
  - No framework and no plugin system.
- **`culling/scoring.py`:**
  - builds the prompt
  - resizes previews to `vlm.image_long_edge` (1024) and base64-encodes them in memory; they are never logged
  - calls the client and validates the response
  - writes `scores/<group_id>.json`
  - **resumes** by skipping groups that already have a valid score file
- **CLI:**
  - `python cull.py score --output <out>`, which fails fast with a clear message if the server is unreachable
  - `python cull.py ping-vlm`
- **Per-photo output schema** (enforced with vLLM structured outputs / `response_format` JSON schema):

  ```json
  {"photo_index": 0, "decision": "keep|maybe|reject", "rank_in_group": 1,
   "eyes": "open|closed|partly|not_visible|na", "blur": "none|slight|strong",
   "background_distraction": "none|minor|major", "moment_type": "ceremony|first_kiss|portrait|...",
   "confidence": 0.0, "reason": "short text"}
  ```

**Safety rules, applied in code after the VLM answer and never left to the model alone:**
- Every multi-photo group keeps at least one photo: the best ranked one becomes `keep`.
- A `reject` with confidence below a configurable threshold becomes `maybe`, which goes to review.
- Singletons are never auto-rejected unless the reason is strong blur or closed eyes with high confidence. Even then they start as `maybe` until phase 5 shows that it is safe.
- Photos flagged in phase 1–2 (`ingest_error`, `no_timestamp`, `preview_fallback`) always go to review.
- An invalid or missing JSON answer after retries puts the whole group into review. It is never dropped.

**Context budget (researched 2026-10-19; confirm with one real request and read `usage.prompt_tokens`):**

*Qwen3.5-9B* (sources: the Hugging Face model card, `config.json` and `preprocessor_config.json`):
- **Architecture:** 32 layers. Only 8 are full attention (4 KV heads × head_dim 256); the other 24 are Gated DeltaNet linear attention with a fixed-size state. Native context is 262,144 tokens. BF16 weights are about 19–20 GB (HF lists 10B parameters including the vision encoder).
- **Image tokens:** patch 16 × merge 2, so **one visual token per 32×32 px**. tokens ≈ (W/32) × (H/32), with sides rounded to multiples of 32.

  | Preview size | Tokens per image |
  |---|---|
  | 1024×683 | ≈ 672 |
  | 1536×1024 | ≈ 1,536 |
  | 768×512 | ≈ 384 |

  The default processor cap is 16.7 MP per image (`longest_edge` 16,777,216 px). An unresized full-size NEF preview would therefore cost about 16k tokens, so **always resize client-side** (`vlm.image_long_edge`).
- **KV cache (own estimate):** only the 8 full-attention layers grow with context: 8 × 2 × 4 × 256 × 2 B ≈ **32 KB per token**.

  | `--max-model-len` | KV cache per sequence |
  |---|---|
  | 16k | ≈ 0.5 GB |
  | 32k | ≈ 1 GB |
  | 262k | ≈ 8 GB (does not fit next to the BF16 weights on a 24 GB L4) |

  The linear-attention state adds roughly 50 MB per sequence.
- **vLLM:** the model card's command uses `--max-model-len 262144 --reasoning-parser qwen3`. Thinking is turned off per request with `extra_body={"chat_template_kwargs": {"enable_thinking": False}}`.
- **Non-thinking sampling** from the model card: temperature 0.7, top_p 0.8, top_k 20, presence_penalty 1.5.

*Claude Haiku 5.5* (sources: the Claude vision docs and this repo's Claude API reference):
- **Context and output:** 1M-token context, 128K max output.
- **Image tokens:** ⌈W/28⌉ × ⌈H/28⌉, on the high-resolution tier (max 2576 px long edge / 4784 tokens per image). 1024×683 ≈ 925 tokens.
- **Image limits:**
  - up to 600 images per request;
  - with more than 20 images in a request, every image must be ≤ 2000 px per side;
  - max 5 MB per image (base64) on Bedrock;
  - Bedrock and Google Cloud accept base64 images only, and their request-size limit is below 32 MB.
- **Price on the Claude API:** $0.10 / $0.50 per MTok input / output for prompts ≤ 100K tokens. Bedrock pricing is separate and still to be checked.
- **Thinking:** on by default at effort `medium`. Use effort `low` for scoring and leave room in `max_tokens`.

*Budget per group:*
- Formula: prompt ~1,000 + N × (image ~680 for Qwen / ~930 for Haiku) + N × ~120 output.
- **Qwen at 1024 px:**

  | `--max-model-len` | Max photos per group (10% margin) |
  |---|---|
  | 16,384 | ≈ 17 |
  | 32,768 | ≈ 35 |

- **Haiku:** context is not the limit.
- **Decision (revised 2026-10-21):** `max_group_size: 0` - groups are never split in grouping. On the five talici folders the cut at 12 caused 15 of the 49 boundaries where neighbours were more similar than 0.85 (e.g. 9564|9565 at 0.95 / 1 s). Context limits are a VLM-step concern: score oversized groups in overlapping chunks.
- If a group does not fit, lower `image_long_edge` or score the group in overlapping chunks, carrying the best photo of the previous chunk forward.

*Proposed vLLM start (to verify on the instance):*

```
vllm serve Qwen/Qwen3.5-9B --max-model-len 32768 --reasoning-parser qwen3 \
  --limit-mm-per-prompt '{"image": 16, "video": 0}' --gpu-memory-utilization 0.92
```

If startup fails for lack of memory, drop to `--max-model-len 16384`.

**Acceptance:**
- A full wedding can be scored across several EC2 sessions with no duplicate work.
- Every photo gets a decision.
- Score files validate against the schema.

**Open questions:**
- Exact prompt wording and the `moment_type` vocabulary, to be decided with the agency.
- Whether to send the group's neighbouring photos for context.

### Phase 4 — Export

- `culling/export.py` writes `results.csv` and `results.json`, one row per photo, with the group, decision, rank and attributes.
- **XMP sidecars** (`<name>.xmp` next to the NEF):
  - `xmp:Rating`: keep = 3–5 by rank, maybe = 2, reject = 1
  - `xmp:Label` (colour) for "needs review"
  - `dc:subject` keywords, e.g. `cull:keep`, `moment:first_kiss`
- An existing `.xmp` is **never overwritten** without a backup (`.xmp.bak`), and edits by the photographer are merged where possible.
- **Open issue — JPG-only photos:** Lightroom reads sidecars only for RAW files. For JPG it reads embedded XMP. Options are (a) write the metadata into the JPG (it modifies the original, so the agency must agree), or (b) use a Lightroom plugin or catalog import. Decide with the agency.
- Optional: a review HTML (like report.html) showing only `maybe` photos, for the 20-minute check.

### Phase 5 — Evaluation

- **Input:** past weddings with the agency's real selection, for example the exported selected files, a list of file names, or XMP ratings from Lightroom. The format still has to be agreed with the agency.
- `python cull.py evaluate --output <out> --truth <selection>` reports:
  - **Recall of agency-selected photos**, the primary metric. Target ≥ 99% counting keep + maybe; every miss is listed with its thumbnail.
  - Reduction: the share of photos auto-rejected.
  - Review load: the number of `maybe` photos, which approximates the 20-minute target.
  - Per-group analysis: whether the agency's pick is in our top ranks.
- The thresholds and prompt are tuned only against these numbers, and the results are recorded in this file.

### Phase 6 — Second VLM (Claude Haiku 5.5 on Bedrock)

- Add `BedrockClient` with the same `score_group` signature, and select it with `vlm.provider: bedrock`.
- **Privacy:** this sends images to AWS Bedrock. The agency must approve it before any real wedding is sent.
- Compare both models with the phase 5 metrics on the same weddings, and also on cost and time per wedding.

### Phase 7 — Learning from corrections

- Log the photographer's changes: the final Lightroom ratings vs. our proposal, read back from XMP or the catalog.
- Train a small model (logistic regression or gradient boosting) over the VLM attributes, group context and EXIF to predict keep/reject.
- Train it per agency, with no image data stored beyond the attributes.
- The hard rule still applies: the learned model can only move photos *into* review or keep, until evaluation proves otherwise.

---

## Session log

- **Session 1 (2026-10-16):** phases 0–2 implemented and 21 unit tests pass.
  - A smoke test on synthetic JPGs passed.
  - First real run on `talici 4a` (334 NEF files from one camera):
    - NEF ingest works.
    - AppleDouble `._` files are now skipped.
    - Grouping thresholds were retuned (see tuning round 1).
    - 22 tests pass.
  - **Still open:** the user's visual check of the retuned groups, and a two-camera wedding.
- **Session 2 (2026-10-19):**
  - Diagnosed the user's 12 missed pairs and compared 4 embedding models.
  - Added look-back grouping (tuning round 2).
  - 27 tests pass.
- **Session 3 (2026-10-21): face identities as a grouping signal** (`culling/faces.py`, `tests/test_faces.py`).
  - **Why:** on all five talici folders DINOv2 cannot separate "same couple, new pose" (wanted merge, measured 0.72–0.90 on Talici 1: 8033→8049 0.72 after 94 s, 8137→8138 0.74, 8134→8135 0.75) from "different guest, same spot" (forbidden, 0.88 on 4a). Threshold tuning cannot fix feature overlap.
  - **What:** SCRFD-10G face detection on the 1536 px preview + ArcFace alignment (numpy similarity transform, PIL warp; no OpenCV) + AuraFace/glintr100 512-d embeddings, both ONNX on CPU (`models/auraface/`, Apache 2.0). Cached in `faces.npz` by sha256. Per wedding, Chinese-Whispers clustering into identities at `faces.identity_threshold`, labels A, B, … by frequency (`identities.json`).
  - **Rule in grouping:** photo signature = (identity set, number of faces). Same people → relaxed `faces_*` thresholds (60 s / 0.70 / look-back 0.70 / drift guard 0.65). No identity in common → never joined. Anything else → unchanged. Groups changed by the rule carry flags `faces` / `faces_split` and badges in the report. `faces.enabled: false` reproduces the old output exactly (tested).
  - **Speed (CPU, 16 cores):** 0.31 s/photo on Talici 1 (2 faces/photo), 0.42 s/photo on 4a (3.4 faces/photo); detection 0.09 s, embedding 0.09 s per face. `det_size` 1024 found only 3 more faces per 50 ceremony photos for +0.11 s/photo, so 640 stays.
  - **Identity clustering, measured:** AuraFace cosine similarity needs 0.40, not the usual 0.5 (at 0.5 the 4a bride split into frontal + veil/profile clusters). Chinese Whispers at 0.4 still kept the Talici 1 bride with heart sunglasses (228 faces) apart from without (209): centroid similarity 0.59, while centroids of different people stay ≤ 0.32 on both folders ⇒ second pass merges clusters at centroid similarity ≥ 0.45 (`identity_merge_threshold`). Small clusters are often one person's odd angle (groom kissing in profile = own 3-face identity), so only identities with ≥ 10 faces count for grouping (`min_identity_faces`); rarer faces are "unknown" and neutral. One-off faces are ~0.3 to every centroid, the same as unrelated faces, so they cannot be soft-assigned.
  - **Rule details, measured:** "different people" must not break a burst (within `time_gap_seconds`): at the 4a altar the groom's face is hidden in one frame and the bride's in the next (9852→9853, 0.6 s), which split a 5-photo group. Blocking now applies only to the extended-gap, look-back and no-people joins.
  - **Results (faces off → on, same DINOv2 config):**

    | Folder | Groups | Singles | Largest | Face-merged groups | Blocked joins | Test pairs |
    |---|---|---|---|---|---|---|
    | talici 4a (334) | 155 → 150 | 79 → 71 | 16 → 10 | 8 | 1 | 9975/9976↔9982 and 9852–9856↔9860/9861 stay apart ✓ |
    | Talici 1 (711) | 279 → 221 | 152 → 117 | 27 → 37 | 37 | 0 | 8134–8138 ✓, 8033–8049 ✓, 8026–8030 ✗ (bride in profile unidentified in 8029/8030) |

    Identities: 4a 1108 faces → bride and groom 100/105 faces, both pure; Talici 1 1266 faces → bride 437, groom 337, both pure; ~15 % of faces are one-off profiles/background faces.
  - **Trade-offs seen in the review sheets:** the relaxed look-back at 0.70 (needed for 8033→8049 at 0.72) also chains different compositions of one scene: Talici 1 g0077 (21 photos: dark alley far, bright alley walking, posed at the wall; weakest links 0.72), 4a g0111 (altar close-ups + the wide shot with the officiant, 0.71 after 115 s). `faces_lookback_similarity_threshold: 0.80` would avoid these but loses 8033–8049.
  - `faces_same_allows_unknown: true` (an unidentified face may stand in for a missing known person) merges 8026–8030 (Talici 1 → 213 groups) but on 4a (→ 145 groups) also joins the couple walking in (0041, two unknown guests) with the altar sequence and the vows close-ups (0095–0097) with 0074/0075. Left off by default; the user decides.
  - Known structural limit: when the guest's face is hidden in both frames of two different hugs, faces see `{bride}` vs `{bride}` and cannot tell the hugs apart (9857/9859 happened to be the same guest). The VLM step's "different people in group" check remains the safety net.
  - 54 tests pass. Not committed: pending the user's review of `report.html` and `faces_sheets/` on both folders.
- **Session 4 (2026-11-10/11): the user's reviews and decisions.**
  - **Labels:** 4a labelled (333 pairs). Current grouping scores 319 correct, 4 false merges, 10 missed merges (F1 0.959).
  - **Group rule changed:** the same main people in the same moment at the same place are one group even with a wider or tighter framing (replaces "wide vs tight = separate"). A person added or missing = a different group. Both are in README, "What a group is", and in the VLM prompt.
  - **Faces:** the user rated 39 of 47 face-driven changes on Talici 2-4 good, 4 bad; faces stay on with the current settings. A face-size filter (`identity_min_face_size: 48`) cleaned the identities but was rejected: it also drops the couple's faces in wide shots and split groups the user had rated good (4a score 319 → 316).
  - **Segments:** `gap_seconds` stays 300 (180 made 4 good and 6 superfluous cuts).
