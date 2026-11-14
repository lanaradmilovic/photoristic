# Ranking: first real run on talici 4a, and a position-bias check

Date: 2026-11-12 (run 2026-11-11 23:59 – 2026-11-12 00:20). Spec:
[vlm-scoring.md](../spec/vlm-scoring.md). Variants without the model:
[2026-11-11](2026-11-11-ranking-variants-dry-run.md).

## Setup

- Server: `g4dn.xlarge` (T4), vLLM, `Intel/Qwen3.5-9B-int4-AutoRound`, `--max-model-len 8192
  --max-num-seqs 4 --enforce-eager`, thinking off, temperature 0. `--limit-mm-per-prompt` raised
  from 2 to 8 images in `~/start-vllm.sh` (the old script is `~/start-vllm.sh.bak-image2`); the
  restart took ~3 min.
- `cull.py rank --output data/out-4a`, default config: 53 multi-frame variants (124 photos),
  images at 1024 px.

## Technical result: works

- 53 of 53 answers valid on the first attempt, none repaired. Several images per request work on
  the T4 (up to 5 tried).
- Prompt tokens ≈ 240 + 675 per image (2 images 1,590; 3 images 2,265; 5 images 3,613): the
  estimate in `ranking.py` (~110k for the run) was 14 % high (96k measured).
- Completion ≈ 50 + 25 per photo (103–177 tokens).
- Seconds per request: 2 photos 8.8 (median), 3 photos 11.3, 4 photos 14.1, 5 photos 16.5; the
  whole folder 8.5 min. A 2,575-photo wedding at the default settings is ~500 requests, roughly
  1.5 hours.

## Quality result: the order follows the position, not the photo

First signs in the run itself: the winner was photo 1 in 42 of 53 requests (32 of 40 pairs), the
answer repeated the input order in 41, and no winner ever had an `issue` while 54 of 71 losers
did (one variant: photo 1 `none`, photos 2–5 all `blurred`).

Check: every variant was asked again with the photos in **reversed** order (same prompt, same
images, numbers swapped; a one-off script, results in `data/out-4a/ranking_reversed_check.json`).

| Variant size | Requests | Same winner in both orders | Reversed run picked its photo 1 |
|---|---|---|---|
| 2 | 40 | 10 | 34 |
| 3 | 10 | 4 | 7 |
| 4 | 1 | 0 | 1 |
| 5 | 2 | 1 | 2 |
| **all** | 53 | **15** | 44 |

A model that looked only at the photos would give the same winner 53 times; a coin gives ~20 of
40 on the pairs. 10 of 40 means the position decides most answers. The `issue` values are
suspect for the same reason: they look written to justify the order.

Some answers are real: `_KAD9794/9795` (picked photo 2, "photo 1 captures him mid-yawn") and
`_KAD9852–9856` (picked photo 5, eyes closed on the first three). The 15 stable winners are the
candidates for "the model actually saw a difference".

## Conclusion

- The pipeline around the model (variants, safety rules, resume, report) works and loses nothing:
  every loser is `maybe`.
- **The winners in `data/out-4a/ranking.json` are not trustworthy** and must not be used to judge
  the approach or tune `variant_similarity`.
- Not tried: asking in both orders and keeping a winner only when they agree (doubles the time,
  15 of 53 agreed here); judging each photo alone (flaws per photo, no comparison, so no
  position) and ranking in code; a side-by-side image as in the judge; shuffling; the full model
  on g6.
