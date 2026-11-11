# 0014 — Group = same main people, same moment, same place

- Status: accepted (supersedes [0013](0013-group-definition-v1.md))
- Date: 2026-11-11
- Decided by: the user

## Context
The user's review of face-driven changes and the labelling of 4a showed that the old rule did not
match what the photographer wants to pick from.

## Decision
- Same main people in the same moment at the same place = **one** group, even with a wider or
  tighter framing, a new pose or expression, or a different orientation.
- **A person added to or missing from a group photo = a different group**; both frames are kept.
- Hugs with different guests stay separate (different people).
- A new activity or a new place = a different group.

## Consequences
- The rule is in [spec/grouping.md](../spec/grouping.md#what-a-group-is) and in the VLM judge prompt.
- `identity_relation` in `culling/grouping.py` returns None for a partial overlap, so such pairs
  still merge; the fix is in [todo](../todo.md), to be measured on the 4a labels.
- 4a labels may need relabelling of wide/tight pairs.

## Evidence
[research/2026-10-21-faces.md](../research/2026-10-21-faces.md#reviews); commit f4fec57.
