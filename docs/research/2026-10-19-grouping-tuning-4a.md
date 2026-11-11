# Grouping tuning rounds 1–3 on talici 4a

Dates: 2026-10-16 to 2026-10-19. Data: talici 4a (334 NEF, one camera). Model: DINOv2-small CLS.
Outcome: decisions [0005](../decisions/0005-time-next-to-similarity.md),
[0006](../decisions/0006-lookback-and-boundary-refinement.md),
[0004](../decisions/0004-dinov2-small-local.md). Later work changed several values; current
values are in `config.yaml`.

## Round 1 — base thresholds

- **What the user saw:** the first defaults (2 s @ 0.80, 15 s @ 0.92) left many near-identical photos ungrouped.
- **Why:** this photographer mostly shoots single frames, not bursts. Consecutive gaps: median
  6.8 s, 75th percentile 13 s. Same-scene neighbours were ~0.8–0.95 even 4–15 s apart. Different
  scenes were mostly below 0.7, few pairs in 0.7–0.8.

| Variant | Groups | Singles | Cuts between neighbours with sim ≥ 0.85 |
|---|---|---|---|
| Old defaults (2 s @ 0.80, 15 s @ 0.92) | 244 | 196 | 55 |
| A (3 s @ 0.75, 15 s @ 0.85) | 190 | 115 | 6 |
| **B (4 s @ 0.75, 20 s @ 0.82) — chosen** | **168** | **89** | **4** |
| C (5 s @ 0.72, 30 s @ 0.80) | 161 | 79 | 3 |

Known limit: only consecutive photos were compared, so a return to an earlier scene started a new group.

## Round 2 — look-back (2026-10-19)

The user listed 12 group pairs that looked like the same scene.
- 8 were *returns*: 1–6 other groups in between, 3–101 s later, similarity 0.85–0.94 to the earlier group.
- 4 were neighbours at 0.71–0.81, just under the rules.

**Model check:** DINOv2-small CLS, DINOv2-small mean-of-patches, DINOv2-base and CLIP B/32 compared
on these pairs. None clearly better; all ranked the pairs around the 90–95th percentile of nearby
pairs. Mean-of-patches helped the 4 neighbour cases but shifts the whole scale.

Look-back at 0.85 / 120 s / span ≤ 180 s: groups 168 → 154, singles 89 → 80, 7 of 12 pairs
merged. g0128+g0130 stayed apart only because the span would be 180.2 s (at 240 s it merges but
g0120+g0125 separates). Still apart below thresholds: g0097+g0098 (0.81), g0115+g0116 (0.76),
g0146+g0147 (0.71), g0153+g0154 (0.79).

## Round 3 — A+B+C+D (2026-10-19)

Causes found in the user's 11 cases:
1. **The embedding does not distinguish people.** In g0023 and g0067 a different person at the
   same spot and pose joined by look-back at 0.88; a good return (g0003, `_KAD9797`) had only 0.85.
   No threshold separates the two. This is the most dangerous error type.
2. **The drift guard compared only with the first photo**, so it cut in the middle of a 6 s kiss
   burst (g0128/g0129: neighbours 0.83–0.94, `_KAD0121` 0.64 to the first photo).
3. **The neighbour rule won even when an earlier group fit better** (`_KAD0156`: 0.84 to its
   neighbour, 0.92 to `_KAD0154`).
4. Borderline similarities (13/15 0.849 vs 0.85; 106/107 0.76 at 17 s; 135/136 0.71 at 0.8 s), left as is.

The model also sees kiss vs no kiss as nearly the same frame (0.87).

Simulated fixes: **A** look-back 0.90; **B** guard on mean similarity to the group; **C** join the
most similar eligible group; **D** boundary refinement (move a border photo when its mean
similarity is higher by > 0.02).

| Variant | Correct (of 11) | Notes |
|---|---|---|
| Before | 2 | |
| B+C or B+C+D | 5 | no regressions |
| **A+B+C+D — chosen** | 6 | separates the different people in g0023/g0067; g0003 loses `_KAD9797` (costs review time, not a photo) |

Result: 158 groups, 82 singles, largest 10.

## Why capture time stays next to similarity

| Similarity-only threshold (no time) | Largest group | Its span |
|---|---|---|
| 0.75 | 147 photos | 140 min |
| 0.85 | 55 photos | 105 min |
| 0.93 | — (240 of 334 stay single) | — |

- **Brake:** 9 pairs have similarity ≥ 0.90 but are ~105 min apart (`_KAD9893–9898` 16:11 vs `_KAD0170–0171` 17:55).
- **Accelerator:** 32 of 162 neighbour joins (20 %) are below 0.85 and joined only because they were 0.7–3.5 s apart.

## Measured limits for people photos (2026-10-19 review)

- Wrong-merge counterexamples at 0.883 (different guests, g0072~g0075) and 0.884 (veil close-up
  vs hug, g0025~g0029) ⇒ people look-back cannot go below ~0.89.
- Wanted-but-unsafe merges at 0.845–0.896 (0082~0085 bride 0.856, 9808~9833 couple 0.896) ⇒ only
  face recognition can unlock those.
- No-people photos overlap too: shrimp recut 0.853 (good) vs head-table-wide ~ box-close-up 0.853
  (bad) ⇒ `nopeople_lookback_similarity_threshold` 0.86.
