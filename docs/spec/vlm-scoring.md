# Ranking: the best photo(s) of every group (step 3)

Status: **implemented; first real run 2026-11-12 works technically, but the model's order follows
the position of the photos, so its winners are not usable yet**
([research](../research/2026-11-12-ranking-first-real-run.md)) (`culling/ranking.py`,
`cull.py rank`). Decisions: [0022](../decisions/0022-variants-in-code-model-ranks.md),
[0019](../decisions/0019-safety-rules-in-code.md),
[0018](../decisions/0018-swappable-vlm-client-own-server.md). Numbers without the model:
[research](../research/2026-11-11-ranking-variants-dry-run.md).

**Principle:** code decides *what is compared* and *how many photos are kept*; the model only
orders frames that code already considers interchangeable.

## Steps

1. **Variants (code).** Every group is split into variants: frames that are near-duplicates of
   each other. A photo joins a variant only if it is compatible with *every* frame in it:
   - DINOv2 similarity ≥ `ranking.variant_similarity`;
   - the same orientation (`ranking.variant_split_orientation`);
   - no difference in identified people (`ranking.variant_split_people`): a known identity in one
     frame and not in the other, the "person added to a group photo" case of
     [0014](../decisions/0014-group-definition-v2.md).

   Among several compatible variants the one with the highest weakest similarity wins. Photos
   that are never compared (ingest error, `no_timestamp`, `preview_fallback`, no embedding, no
   preview) are a `review` variant each.
2. **One request per variant with two or more frames.** Every frame is its own image, scaled to
   `vlm.image_long_edge`, with its number in the top-left corner. The model answers (structured
   output, schema built for the number of frames):

   ```json
   {"photos": [{"photo": 1, "issue": "none|eyes_closed|blurred|bad_expression|obstructed|exposure"}],
    "order": [2, 1, 3], "reason": "why the first is the best"}
   ```

   No confidence (the judge run showed it carries no information) and no question about whether
   the frames belong together (the model cannot tell,
   [0020](../decisions/0020-vlm-judge-parked.md)). Only the first place of `order` must be valid:
   repeated numbers are dropped and missing ones appended (`repaired: true`).
3. **Safety rules (code)**, below.

Single-frame variants and single-photo groups are never sent.

## Safety rules (in code, after the answer)

| Photo | Decision | `why` |
|---|---|---|
| never compared (flagged by ingest, no preview) | `maybe` | `flagged` |
| the only frame of its variant | `keep` | `only_frame` |
| first in the model's order | `keep` | `best_of_variant` |
| ranked lower | `maybe`, with its rank | `ranked_lower` |
| its variant has no valid answer (after `vlm.max_retries`) | `maybe` | `no_valid_answer` |
| its variant was not asked yet | `maybe` | `not_ranked` |

- **There is no `reject`.** Nothing leaves review until phase 5 has measured that it is safe.
- Every answered group has at least one `keep`; a group has as many `keep` as it has variants.
- An answer is used only if it orders exactly the variant's photos.

## Group size vs context

Measured on the T4: a request is ~240 + N × ~675 tokens in and ~50 + N × ~25 out, 9 s for two
photos and 16 s for five. A variant longer than `ranking.max_images` is cut into consecutive parts, each with its own
winner (one extra `keep`, never a lost photo). Groups themselves are not split
([0009](../decisions/0009-no-group-size-split.md)).

## Running

```
cull.py rank --output <out> --dry-run        # variants, decisions so far, token estimate; sends nothing
cull.py rank --output <out> [--max-requests N]
```

- A real run pings the server first and fails fast; the tunnel is described in
  [vlm-judge](vlm-judge.md#running).
- `ranking.json` is written after every request. A second run sends only what has no valid
  answer (including earlier errors), so a wedding can be ranked across several EC2 sessions.
- Answers of another model or another prompt are never mixed: the command stops and asks to move
  the file.
- Afterwards `report.html` is rebuilt: a green frame and `★ keep · v1` on kept photos,
  `maybe #2 · v1 · eyes_closed` on the others, `keep 2 of 5` in the group header. A ranking made
  for an older `groups.json` is not shown.

## `ranking.json`

| Field | Meaning |
|---|---|
| `model`, `base_url`, `prompt_hash` | What produced the answers (absent after a dry-run only) |
| `groups_created` | `created` of the `groups.json` the decisions were made for |
| `config` | `ranking` settings plus `image_long_edge` |
| `variants[]` | `{key, group_id, index, kind: single / multi / review, photo_ids, names, span_seconds}` |
| `answers{key}` | Resume state per variant: `{group_id, photo_ids, names, order (photo ids, best first; null on error), issues{photo_id}, reason, repaired, error, attempts, elapsed_s, prompt_tokens, completion_tokens, ranked_at}` |
| `photos{photo_id}` | The result: `{group_id, variant, decision: keep / maybe, rank, issue, why}`; every photo of `groups.json` has one |

`key` is a hash of the variant's photo sha256 values, so an answer survives a re-grouping that
leaves the variant unchanged. Changing `variant_similarity` changes the variants and therefore
which answers apply; old answers stay in the file.

## Not done yet

- **No measurement.** There is no ground truth for "best photo" and no agency selection; the
  defaults are conservative, not tuned ([todo](../todo.md)).
- **Position bias**: with Qwen3.5-9B, 4-bit and full, the first photo wins most requests
  whatever it shows. The request design (step 2) has to change before the decisions mean
  anything; judging each photo alone is the measured alternative
  ([research](../research/2026-11-14-ranking-full-model-and-per-photo.md)).
- The server must allow the images: `--limit-mm-per-prompt '{"image": 8, ...}` for `max_images` 8.
- `moment_type` and per-photo attributes beyond `issue` (the original design) are dropped until
  something uses them: every output token costs ~0.07 s on the T4.
- `BedrockClient` (phase 6): `ranking.py` needs only `ping()` and `ask()`.
