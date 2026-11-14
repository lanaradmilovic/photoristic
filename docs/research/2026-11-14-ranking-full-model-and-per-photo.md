# Ranking with the full model, and judging each photo alone

Date: 2026-11-14 (runs 2026-11-13 23:00 – 2026-11-14 00:45). Follows
[2026-11-12](2026-11-12-ranking-first-real-run.md). Spec: [vlm-scoring.md](../spec/vlm-scoring.md).

## Setup

- Server: `g6.xlarge` (L4 24 GB), vLLM 0.33, full `Qwen/Qwen3.5-9B` (bf16), `--max-model-len 16384
  --max-num-seqs 4`, thinking off, temperature 0 (setup notes in [aws-setup](../aws-setup.md)).
- Data: talici 4a, default `ranking` config: 53 multi-frame variants, 124 photos.
- The T4 answers are kept as `data/out-4a/ranking.t4-int4.json`; `ranking.json` now holds the
  full model's answers.

## 1. Full model, current prompt (all frames of a variant in one request)

- 53 of 53 valid, 7.6 s median per request (T4: 8.9 s), 7.3 min for the folder.
- Winner = photo 1 in 41 of 53; the answer repeats the input order in 41.
- **Reversed-order check: same winner in 12 of 53** (pairs 7 of 40; the reversed run picked its
  photo 1 in 37 of 40). T4 4-bit: 15 of 53. The stronger model does **not** remove the position
  bias. Data: `data/out-4a/ranking_reversed_check.g6.json`.

## 2. Each photo judged alone, ranking in code (one-off script, not in the repo)

One request per photo, no comparison, so the photo's position cannot matter. The model returns
`eyes` (open / some_closed / not_visible), `focus` (sharp / slightly_soft / blurred),
`expression` (good / neutral / awkward / not_visible), `obstructed` (no / yes), `exposure`
(ok / too_dark / too_bright) and `score` 1–10 for the album, all for the **main** people. Code
ranks by `score` minus penalties (eyes closed −3, blurred −4, slightly soft −1, awkward −2, good
expression +1, obstructed −2, exposure −2).

- 124 photos, 4.2 s median, 8.7 min (one image per request; slower per photo than ranking
  together, ~3.4 s per photo there).
- **Stable under a change of input:** the same photos at 1280 px instead of 1024 px: eyes same in
  122 of 124, expression 119, focus 118, exposure 120, obstructed 115; score identical in 90,
  within 1 in 122. Code winners: the same set in 37 of 53 variants, overlapping in 50; where both
  runs had one clear winner (15), it was the same in 15.
- **Coarse:** the top is tied in 29 of 53 variants (32 at 1280 px). Keeping every tied photo would
  add 35 keeps to 263 (of 334). Scores cluster at 7–9.
- **Agreement with the comparative answers:** of the 12 variants where the comparative ranking gave
  the same winner in both orders, the per-photo winner set contains it in 11 (9 at 1280 px).
- **Suspect fields:** `obstructed: yes` for 61 of 124 photos and `eyes: not_visible` for 54 look
  too frequent for ceremony photos; not checked against the photos (no ground truth).

## Conclusion

- Asking the model to compare frames is unusable with Qwen3.5-9B, 4-bit or full: the order of the
  input decides.
- Judging each photo alone gives answers that do not depend on order and barely depend on image
  size, so it is the only direction measured so far that can carry a decision. It separates the
  frames of a variant in only about half of the cases; the rest are ties.
- Whether its winners are the photos a photographer would pick is **unknown**: there is still no
  ground truth. Next steps in [todo](../todo.md).

## 3. "Describe each photo, then choose" (same day, full model)

Prompted by a single test on two of the user's own photos, where this prompt picked the same
photo in both orders. The model first writes one or two sentences per photo, then `best` and
`why`; every variant asked forward and reversed (106 requests, 12 s median, 19.7 min; one tunnel
drop, resumed). Data: `data/out-4a/describe_first_g6.json`.

- **Same winner in both orders: 15 of 53** (pairs 12 of 40) — no better than before.
- The bias **flipped from the first to the last photo**: in pairs the last photo was picked in 64
  of 80 requests (the earlier prompt: the first). Describing first only moves where the bias sits.
- The two-photo test was therefore not evidence: its result fits "pick the first" forward and
  "pick the last" reversed only by chance of the two orders agreeing.
- Of the 15 stable winners, 14 are in the per-photo top (clear and identical: 5). Stable winners of
  this prompt and of the earlier one overlap in 4 variants and agree in 2.

Conclusion unchanged: with Qwen3.5-9B, comparing frames in one request is decided by position.
