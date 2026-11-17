# Todo

The list a new session reads first. Ordered by priority. When an item is done, remove it here and
write one line in [log.md](log.md). Items that need the user are marked **(user)**.

## Now

- **Phase 3: switch `ranking.py` to judging each photo alone.** Comparing frames in one request
  is position-biased with both the 4-bit and the full model (same winner in both orders 15 and 12
  of 53). Judging each photo alone and ranking in code is stable (eyes/focus/expression agree in
  95–98 % between 1024 and 1280 px), but ties at the top in ~55 % of variants
  ([research](research/2026-11-14-ranking-full-model-and-per-photo.md)). To do: per-photo request
  and schema in `ranking.py` (prompt and penalties from the experiment), cache per photo sha256,
  ties at the top all `keep` (safe) or broken by a pairwise question asked in both orders.
  Decide after the ground truth below shows whether the per-photo winners are right.
- **Pairwise report prompt (2026-11-15): consistent, not selective.** Fixed checks, `A / B / same`,
  both orders, agreement in code: 0 invented differences on identical pairs, 3 of 576 answers
  depend on the order, but only 10 of 53 variants get one winner (85 % of photos kept)
  ([research](research/2026-11-15-report-prompt-both-orders.md)). Not in `ranking.py`. Decide
  (user): accept "tie = keep all" with this keep rate, or add a taste step for ties. To try:
  face crops for the eyes check, log-probabilities instead of the three answers.
- **Ground truth for "best photo" (user, ~20 min on 4a). Blocks the step above.** The tool is
  ready: `cull.py pick --output data\out-4a` (79 groups), rules on the page. Afterwards
  `cull.py pick-score` for `ranking.json`, and the saved per-photo / describe-first answers in
  `data/out-4a/` measured against the picks. Without it
  `ranking.variant_similarity` (0.90 keeps 72 % of the wedding, 0.85 61 %, one winner per group
  40 %; [research](research/2026-11-11-ranking-variants-dry-run.md)) and the prompt cannot be tuned.

## Next

- **Check 4a and Talici 1 labels against the new group rule (user).** They were made 2026-11-10, partly under
  the old "wide vs tight = separate" rule ([0013](decisions/0013-group-definition-v1.md)).
- **Day segments: 4 missed cuts.** At 300 s four real part-of-day changes are not cut; pauses cannot
  separate them ([0017](decisions/0017-segments-gap-300s.md)). Needs content (VLM segment
  classification), not another threshold.

- **Open review findings (2026-11-11), smaller ones not fixed at merge:** label server checks no
  Origin; failed save falls back to localStorage that server mode never reads; thresholds copied in
  `judge.py` docstring and report JS; double VLM ping; duplicated helpers (`_write_json`, `_ratio`,
  `_time`, `_clock`); `partial_blocks` treats an unrecognised face as a different person (measure
  with `cull.py score` first); segments: `load_people` skips the model check, stale
  `identities.json` used when faces are off, filters hide segment bars only by camera, burst
  cutoff and sheet sizes not in config.

## Later / ideas

- **Labelling tool: look-back joins.** Only adjacent pairs can be labelled; "photo 5 belongs with
  photo 2" cannot be recorded. Add such a label if the user sees it often.
- **Ranking: oversized variants.** A variant longer than `ranking.max_images` is cut into parts
  with one keep each; a play-off between the part winners would save keeps if such variants are common.
- **VLM judge again with a stronger model.** Parked ([0020](decisions/0020-vlm-judge-parked.md)).
  When the full Qwen3.5-9B (g6) or a larger model runs, re-run `cull.py judge` on 4a (~10 min) and
  try a v3 prompt that limits "person added/missing" to posed group photos.
- **Garbage face identities.** A size filter was rejected ([0012](decisions/0012-no-face-size-filter.md));
  another feature (blur, position, co-occurrence) might work.
- Phase 1 checks on a two-camera wedding ([plan](plan.md#phase-1--ingest)).
