# VLM scoring (step 3) — design

Status: **planned, not implemented** (phase 3). This is the agreed design; update it when the
code lands. Decisions: [0018](../decisions/0018-swappable-vlm-client-own-server.md),
[0019](../decisions/0019-safety-rules-in-code.md). Context budget research:
[2026-10-19](../research/2026-10-19-vlm-context-budget.md).

**Goal:** one VLM request per group returns structured JSON for every photo in it.

## Components

- **`culling/vlm.py`** — one small client class per provider with the same method (the
  OpenAI-compatible client already exists for the judge):

  ```python
  class OpenAICompatibleClient:   # vLLM; later BedrockClient with the same signature
      def score_group(self, group: dict, images: list[bytes]) -> list[dict]: ...
  ```

  `make_client(config["vlm"])` picks the provider. No framework and no plugin system.
- **`culling/scoring.py`:** builds the prompt; resizes previews to `vlm.image_long_edge` (1024)
  and base64-encodes them in memory (never logged); calls the client and validates the response;
  writes `scores/<group_id>.json`; **resumes** by skipping groups with a valid score file.
- **CLI:** `cull.py score-vlm --output <out>` (name TBD; `score` is taken by label scoring), fails
  fast if the server is unreachable.

## Per-photo output schema

Enforced with vLLM structured outputs (`response_format` JSON schema):

```json
{"photo_index": 0, "decision": "keep|maybe|reject", "rank_in_group": 1,
 "eyes": "open|closed|partly|not_visible|na", "blur": "none|slight|strong",
 "background_distraction": "none|minor|major", "moment_type": "ceremony|first_kiss|portrait|...",
 "confidence": 0.0, "reason": "short text"}
```

The prompt also asks whether the group shows different people or different moments; such a group
is then treated as separate photos and nothing is rejected on the basis of the group comparison.

## Safety rules (in code, after the answer)

- Every multi-photo group keeps at least one photo: the best ranked one becomes `keep`.
- A `reject` with confidence below a configurable threshold becomes `maybe` (review).
- Singletons are never auto-rejected unless the reason is strong blur or closed eyes with high
  confidence, and even then they start as `maybe` until phase 5 shows that it is safe.
- Photos flagged in steps 1–2 (`ingest_error`, `no_timestamp`, `preview_fallback`) always go to review.
- An invalid or missing JSON answer after retries puts the whole group into review; never dropped.

## Group size vs context

Formula: prompt ~1,000 + N × (image ~680 tokens for Qwen at 1024 px / ~930 for Haiku) + N × ~120
output. Qwen with `--max-model-len 16384` fits ≈ 17 photos, 32768 ≈ 35. Groups are not split in
grouping ([0009](../decisions/0009-no-group-size-split.md)); an oversized group is scored in
overlapping chunks, carrying the best photo of the previous chunk forward, or with a lower
`image_long_edge`.

Proposed vLLM start (to verify on the instance; drop to 16384 if memory fails):

```
vllm serve Qwen/Qwen3.5-9B --max-model-len 32768 --reasoning-parser qwen3 \
  --limit-mm-per-prompt '{"image": 16, "video": 0}' --gpu-memory-utilization 0.92
```

## Acceptance

- A full wedding can be scored across several EC2 sessions with no duplicate work.
- Every photo gets a decision.
- Score files validate against the schema.

## Open questions

- Exact prompt wording and the `moment_type` vocabulary, to be decided with the agency.
- Whether to send the group's neighbouring photos for context.
