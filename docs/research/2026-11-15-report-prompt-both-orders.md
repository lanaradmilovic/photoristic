# "Report, not verdict" prompt asked in both orders (27B)

Date: 2026-11-15. Follows [the four-steps prompt](2026-11-14-steps-prompt-27b.md). Question, from
the user: the four-steps prompt describes the same pair from two different perspectives in the two
orders and changes the winner (g0020, `_KAD9843` / `_KAD9844`). Can a prompt or a flow make the
choice consistent, on any wedding, without telling the model that "the moment" beats everything?

## What the four-steps answers show (53 variants, both orders, saved run)

- **The description is free text, so it is a different description every time.** Only 4 of 124
  per-photo sentences are near-identical in the two orders. In g0020 the groom's gaze is reported
  the same way twice, but the forward run adds the man in the background and the reversed run the
  bride's gaze. Relative words ("wider", "closer", "high-angle") are assigned relative to the other
  photo and sometimes swap.
- **The winner is chosen in step 2, before the comparison.** `best_moment` names a photo in 52 of
  106 answers; it is the final winner in 52 of 52. Step 3 then argues for it.
- **The criteria are invented per answer.** Looking forward is "solemn" in one run, looking down
  "more balanced" in the other; wide is "context" or "cluttered"; symmetrical is "less engaging"
  or "balanced and grand".
- **Many pairs have no right answer.** Wide vs tight, profile vs rear view, with and without
  sunglasses: differences of taste, where both frames may be delivered.

## Literature (searched 2026-11-15; measured results only)

- Asking in both orders and counting a win only when both agree is the standard fix for judge
  position bias (https://arxiv.org/abs/2306.05685). Shuffling images changes 25–40 % of answers of
  open multi-image VLMs (https://arxiv.org/abs/2503.13792).
- Explanations rationalise an answer driven by option order (https://arxiv.org/abs/2305.04388);
  "describe each, then compare" did not help on subtle image pairs (https://arxiv.org/abs/2603.07888).
- Boolean checklists aggregated in code agree better across evaluators than holistic scores; text
  tasks only (https://arxiv.org/abs/2403.18771).
- Separate images beat a side-by-side composite (same subtle-pairs paper). Subtle pair differences
  are a known weak spot: Qwen2.5-VL-72B 65 %, humans 96 %.
- Not found measured: role prompts, text labels vs burned-in numbers, face crops.

## The flow tested

One request per pair of a variant, **in both orders**. System prompt = the rules; user message =
`Photo A:` image, `Photo B:` image, one line. The model does not pick: for six fixed checks
(sharpness, eyes, visibility, expression, exposure, moment) it answers `A` / `B` / `same`. Gaze,
pose, framing and angle are named as taste and are never a difference. Code keeps a check only when
both orders name the same photo; a photo wins a pair when all kept checks point to it; otherwise
the pair is a tie and both stay. No free-text reasoning, no ranking, no numbers burned into the image.

R1: "answer `same` when the difference is small or you are not sure". R2: "`same` only when you see
no difference", plus a seventh field `overall` (which one to deliver). Full texts are in the result
files (`system`, `user`).

## Results (RedHatAI/Qwen3.8-27B-INT4, 1024 px, temperature 0)

Control pairs, where the right answer is known:

| Test | R1 | R2 |
|---|---|---|
| Same image twice (25): any difference reported | 0 | 0 |
| Original vs Gaussian blur 1.5 px: found in both orders, on `sharpness` | 24 of 25 | 12 of 12 |
| Original vs blur 3 px | 25 of 25 | – |
| Original vs brightness × 0.3, on `exposure` | 25 of 25 | – |
| False verdicts on other checks in these pairs | 0 | 4 (one order only, dropped) |

The 96 real pairs of the 53 variants of 4a:

| | Four steps | R1 | R2 |
|---|---|---|---|
| Check answers where the two orders name different photos | – | 3 of 576 | 16 of 672 (9 in `overall`) |
| Check answers kept (both orders agree on a photo) | – | 25 | 81 |
| Seen in one order only (dropped) | – | 24 | 46 |
| 2-photo variants with a winner (40) | 17 same in both orders | 8 | 10 |
| Variants with exactly one photo left (53) | 22 | 10 | 11 (12 with `overall`) |
| Photos kept (124) | 53 by construction | 108 | 105 (102 with `overall`) |
| Seconds per request, median | 20.6 | 8.8 | 9.7 |

- g0020: every check `same` in both orders with both prompts; both frames stay.
- `overall` in R2: both orders agree on a photo in 27 pairs and contradict in 9, so it is not a
  coin, but it adds a winner in one variant only.
- User picks exist for three variants. R1 leaves all three undecided. R2 decides one, against the
  pick: `_KAD9794` (the boy yawns) loses on `expression`, and the user picked it.

## Conclusion

- **Consistency is solved by the flow, not by wording**: fixed checks, three allowed answers, both
  orders, agreement in code. The model no longer argues, and it does see blur and exposure when
  they are there.
- **The cost is selectivity.** On real near-duplicates the model reports a defect difference in
  about a quarter of the pairs, so most variants keep all their frames (85 % of photos vs 43 % with
  one winner per variant). What the four-steps prompt decided beyond that was position.
- **A general rule can be wrong for a photographer**: "awkward expression is worse" rejected the
  yawn the user picked. One case; the picks are needed to say more.
- Requests: n·(n−1) per variant instead of 1; 192 for 4a (~15 min with two in parallel).

Not tested: face crops for the eyes check; log-probabilities of `A` / `B` / `same` averaged over
both orders as a finer score; the same prompt on the 9B.

## Files (in `data/out-4a/`)

| File | Content |
|---|---|
| `r1_real.json`, `r2_real.json` | 96 pairs, both orders, with the prompt |
| `r1_identical.json`, `r1_softblur.json`, `r1_blur.json`, `r1_dark.json` | R1 control pairs |
| `r2_identical.json`, `r2_softblur.json` | R2 control pairs |
