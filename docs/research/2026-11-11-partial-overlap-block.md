# Grouping: a partial overlap of face identities as a split

Date: 2026-11-11. Decision: [0021](../decisions/0021-partial-overlap-does-not-split.md).
Config key: `grouping.faces_partial_overlap_blocks` (implemented, off).

## What was tried

[0014](../decisions/0014-group-definition-v2.md) says a person added to or missing from a group
photo is another group. `identity_relation` returned None for a partial overlap ({A,B,C} vs
{A,B,C,D}), so DINOv2 decided and such pairs merged. With the flag on, any known identity present
on one side and absent on the other makes the relation "different": no extended-gap, look-back or
relaxed join, no boundary move; a burst (gap ≤ `time_gap_seconds`, similarity ≥
`similarity_threshold`) still joins.

## Results (`cull.py score`, labels of both folders)

| | 4a off | 4a on | Talici 1 off | Talici 1 on |
|---|---|---|---|---|
| labels | 333 | 333 | 710 | 710 |
| correct | 316 | 304 | 673 | 656 |
| false merges | 3 | 2 | 6 | 4 |
| missed merges | 14 | 27 | 31 | 50 |
| F1 | 0.951 | 0.912 | 0.961 | 0.942 |
| groups | 150 | 162 | 221 | 232 |

Fixed by the flag: 4a _KAD0148/0149 (false merge), _KAD0025/0026, _KAD0147/0148; Talici 1
_KAD8571/8572, _KAD8582/8585 (false merges), _KAD8059/8060. Broken: 15 on 4a, 20 on Talici 1,
all new missed merges.

## Why it breaks

Known identities that differ in the 18 changed 4a pairs (face height relative to the largest face
in the photo):

- the bride (A) or the groom (B) recognised in one frame and not in the other, the frame still
  showing them (head turned, profile): _KAD0053/0054, _KAD0063/0065, _KAD0072/0073 ({A,B} vs {B} +
  one unknown face), _KAD0102/0103;
- a person walking into the frame or standing behind (officiant, a guest), which the labels count
  as the same group: _KAD0101/0102 (E appears, 2 → 3 faces), _KAD9788/9789, _KAD9838/9839,
  _KAD0076/0077;
- crowd frames where one of 6–8 known guests drops in or out: _KAD9979/9980, _KAD9980/9981.

Neither face size (the differing person is often as large as the couple, 0.6–1.0) nor the face
count (a real addition and an unrecognised head both change or keep it) separates a real change of
people from a missed recognition. The VLM judge's prompt v2 failed on the same distinction
([research](2026-11-11-judge-first-real-run.md)).

Diagnostic script: a one-off in the session scratchpad (identities.json + faces.npz per pair), not
in the repo.
