# 0006 — Look-back, mean drift guard, best candidate, boundary refinement

- Status: accepted
- Date: 2026-10-19
- Decided by: the user, after reviewing simulated variants

## Context
Comparing only consecutive photos split returns to an earlier scene; the drift guard on the first
photo cut bursts in the middle; the neighbour always won even when an earlier group fit better.

## Options considered
- **A:** look-back threshold 0.90 (instead of 0.85).
- **B:** drift guard on the mean similarity to the group.
- **C:** join the most similar eligible group.
- **D:** boundary refinement (margin 0.02).

Simulated on the user's 11 cases: before 2/11, B+C(+D) 5/11, A+B+C+D 6/11.

## Decision
A+B+C+D. The higher look-back threshold separates different people at the same spot (0.88) at the
cost of one good return (0.85) becoming its own group — review time, not a lost photo.

## Consequences
Config keys `min_mean_similarity_to_group`, `lookback_*`, `refine_boundaries`, `refine_margin`.
Look-back joins cannot be labelled ([0015](0015-labels-per-adjacent-boundary.md)).

## Evidence
[research/2026-10-19-grouping-tuning-4a.md](../research/2026-10-19-grouping-tuning-4a.md#round-3--abcd-2026-10-19).
