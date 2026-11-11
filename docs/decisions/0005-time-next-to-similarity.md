# 0005 — Keep capture time next to similarity

- Status: accepted
- Date: 2026-10-19
- Decided by: agent, from measurements

## Context
Could grouping use similarity alone?

## Options considered
1. **Similarity only.**
2. **Similarity with time windows** (burst rule, extended-gap rule, look-back window, max span).

## Decision
Option 2. Similarity alone either merges distinct moments (0.75 → one group of 147 photos over
140 min) or misses bursts (0.93 → 240 of 334 photos single). Time is a brake (9 pairs ≥ 0.90 shot
105 min apart) and an accelerator (20 % of neighbour joins are < 0.85 and joined only because they
were 0.7–3.5 s apart).

## Consequences
Returns to a scene after a long pause stay separate groups (costs review time).

## Evidence
[research/2026-10-19-grouping-tuning-4a.md](../research/2026-10-19-grouping-tuning-4a.md#why-capture-time-stays-next-to-similarity).
