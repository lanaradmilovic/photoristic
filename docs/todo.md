# Todo

The list a new session reads first. Ordered by priority. When an item is done, remove it here and
write one line in [log.md](log.md). Items that need the user are marked **(user)**.

## Now

- **Grouping: a person added to or missing from a group photo must split the group.** Rule:
  [0014](decisions/0014-group-definition-v2.md). Today `identity_relation` (`culling/grouping.py`)
  returns None for a partial overlap ({A,B,C} vs {A,B,C,D}), so DINOv2 decides and such pairs merge
  (also Talici 1: a group of 3 men joined with a group of 4). Proposed: a known identity present on
  one side and absent on the other blocks the join. Risk: a turned head hides a face while the
  person is still there — measure with `cull.py score` on 4a before and after, and look at Talici 1
  party groups. The VLM prompt already carries the rule.
- **VLM judge: first real run (user).** Needs the user's choice of model and server or API key.
  Steps: [spec/vlm-judge.md](spec/vlm-judge.md#running). Before paying for ~690 calls consider:
  dedupe look-back per pair of groups, skip joined bursts, `sim_low` 0.79
  ([research](research/2026-10-23-judge-dry-run.md#redundancy-visual-inspection-of-the-pair-sheets)).
- **Merge branches (user).** `labels`, `segments`, `judge` and `docs` are not in `main`; waiting
  for the user's review.

## Next

- **Labels for Talici 1 (user).** Only 4a is labelled (`data/out-4a/labels.json`, 333 pairs).
  Talici 1 is the over-splitting extreme and is needed next to 4a for every grouping change.
- **Check 4a labels against the new group rule (user).** They were made 2026-11-10, partly under
  the old "wide vs tight = separate" rule ([0013](decisions/0013-group-definition-v1.md)).
- **Day segments: 4 missed cuts.** At 300 s four real part-of-day changes are not cut; pauses cannot
  separate them ([0017](decisions/0017-segments-gap-300s.md)). Needs content (VLM segment
  classification), not another threshold.

## Later / ideas

- **Labelling tool: look-back joins.** Only adjacent pairs can be labelled; "photo 5 belongs with
  photo 2" cannot be recorded. Add such a label if the user sees it often.
- **Garbage face identities.** A size filter was rejected ([0012](decisions/0012-no-face-size-filter.md));
  another feature (blur, position, co-occurrence) might work.
- Phase 1 checks on a two-camera wedding ([plan](plan.md#phase-1--ingest)).
