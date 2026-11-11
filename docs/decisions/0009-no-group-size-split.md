# 0009 — Do not split groups by size

- Status: accepted (replaces the original split at 12)
- Date: 2026-10-21
- Decided by: the user

## Context
Groups larger than 12 were split into balanced chunks to fit the VLM context.

## Options considered
1. **Split in grouping** at `max_group_size: 12`.
2. **Never split in grouping** (`max_group_size: 0`); handle context limits in the VLM step.

## Decision
Option 2. On the five talici folders the cut at 12 caused 15 of the 49 boundaries where neighbours
were more similar than 0.85 (e.g. 9564|9565 at 0.95 / 1 s). The VLM step scores oversized groups in
overlapping chunks instead.

## Consequences
The scoring step must handle groups of 30+ photos
([spec/vlm-scoring.md](../spec/vlm-scoring.md#group-size-vs-context)).

## Evidence
[research/2026-10-19-vlm-context-budget.md](../research/2026-10-19-vlm-context-budget.md); measured on the five talici folders (session 3, [log](../log.md)).
