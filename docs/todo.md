# Todo

The list a new session reads first. Ordered by priority. When an item is done, remove it here and
write one line in [log.md](log.md). Items that need the user are marked **(user)**.

## Now

- **Phase 3: VLM scoring (pick the best photo per group).** Next big step
  ([design](spec/vlm-scoring.md), [0020](decisions/0020-vlm-judge-parked.md)). The server runs on a
  T4 with the 4-bit model ([aws-setup.md](aws-setup.md)); check how many images per request fit
  there. Do not rely on the model to flag a mixed group: the judge run showed it misses changes of
  action ([research](research/2026-11-11-judge-first-real-run.md)), and groups may still mix two
  group photos that differ by one person ([0021](decisions/0021-partial-overlap-does-not-split.md)).

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
- **VLM judge again with a stronger model.** Parked ([0020](decisions/0020-vlm-judge-parked.md)).
  When the full Qwen3.5-9B (g6) or a larger model runs, re-run `cull.py judge` on 4a (~10 min) and
  try a v3 prompt that limits "person added/missing" to posed group photos.
- **Garbage face identities.** A size filter was rejected ([0012](decisions/0012-no-face-size-filter.md));
  another feature (blur, position, co-occurrence) might work.
- Phase 1 checks on a two-camera wedding ([plan](plan.md#phase-1--ingest)).
