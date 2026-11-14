# "Four steps" ranking prompt on Qwen3.8-27B (4-bit)

Date: 2026-11-14 (evening). Follows [the 27B run](2026-11-14-qwen38-27b-int4.md). Question, from
the user: does a prompt that gives the model a role (an experienced wedding photographer who
culls) and makes it describe, name the best moment and compare before it ranks give a better
ranking than the short prompt with the flaw list?

## Setup

Same server, model, variants (53 multi-frame, 40 of them pairs) and numbered 1024 px images as the
27B run. Every variant was asked twice: capture order and reversed order. The answer is JSON with
the fields in the order of the steps: `photos` (one sentence per photo: what is happening),
`best_moment`, `comparison`, `order`. No flaw list, no time span. The prompt text is stored in the
result file.

## Results

| | Short prompt | Four steps |
|---|---|---|
| Same winner in both orders (53) | 26 | **22** |
| Same winner in both orders, pairs (40) | 19 | 17 (a coin: ~20) |
| Winner = photo 1 as shown, forward / reversed run | 22 / – | 13 / 16 |
| Seconds per request, median | 8.4 | 20.6 |

- **The bias moved to the last photo.** Of the 23 pairs where the two orders disagree, 19 picked
  "photo 2" both times and 4 "photo 1" both times.
- **The texts read well and do not decide anything.** The descriptions name real differences
  ("the groom looks down", "the boy yawns widely", "wider view of the table"), but the comparison
  argues for whichever photo is shown as number 2, with opposite arguments in the two runs (wide
  is "more context" in one, "cluttered" in the other).
- Variants of 3+ photos: same winner 5 of 13.
- Stable with both prompts: 11 variants; the same winner in 6 of them.
- No request failed, was repaired or retried; the longest answer was 485 tokens.

## Conclusion

A role and step-by-step reasoning do not make this model's choice between near-identical frames
depend on the photos. Three prompts (flaw list, per photo, four steps) and two model sizes give
the same picture: it sees the differences and cannot weigh them.

## Files (in `data/out-4a/`)

| File | Content |
|---|---|
| `ranking_steps.q38-27b-int4.json` | both runs, all texts, the prompt |
| `ranking.json`, `ranking_reversed.json` | the same answers in the shape the review page reads (`cull.py pick --review-model`); `reason` is `best_moment` + `comparison` |
| `ranking.q38-27b-int4.json` | the short-prompt 27B ranking (was `ranking.json`) |
