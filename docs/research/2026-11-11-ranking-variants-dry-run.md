# Ranking variants without the model: how many photos would be kept

Date: 2026-11-11. Spec: [vlm-scoring.md](../spec/vlm-scoring.md). Decision:
[0022](../decisions/0022-variants-in-code-model-ranks.md).

## Setup

`build_variants` (`culling/ranking.py`) on the existing outputs of the five Talici folders
([datasets](../datasets.md)); no VLM request. After a full run every variant has exactly one
`keep`, so **keeps = number of variants** whatever the model answers. 4a uses the current
`groups.json`; the other four are the outputs of 2026-10-21 (older grouping settings), so their
numbers are indicative. `max_images` 8.

## Keeps (share of all photos)

| Folder | Photos | Groups (= one winner per group) | sim 0.85, people + orientation | sim 0.85, orientation only | sim 0.90, people + orientation (default) | sim 0.90, orientation only |
|---|---|---|---|---|---|---|
| talici 4a | 334 | 150 (45 %) | 235 (70 %) | 210 (63 %) | 263 (79 %) | 250 (75 %) |
| Talici 1 | 711 | 221 (31 %) | 378 (53 %) | 365 (51 %) | 485 (68 %) | 470 (66 %) |
| Talici 2 | 174 | 62 (36 %) | 95 (55 %) | 92 (53 %) | 115 (66 %) | 113 (65 %) |
| Talici 3 | 661 | 184 (28 %) | 364 (55 %) | 305 (46 %) | 423 (64 %) | 378 (57 %) |
| talici 4 | 695 | 334 (48 %) | 505 (73 %) | 460 (66 %) | 556 (80 %) | 533 (77 %) |
| **all** | 2575 | 951 (37 %) | 1577 (61 %) | 1432 (56 %) | 1842 (72 %) | 1744 (68 %) |

With no similarity, people or orientation split (one variant per group, only cut at 8 images)
the keeps are 1030 (40 %).

## 4a in detail

| `variant_similarity` | people + orientation | orientation only | people only | neither |
|---|---|---|---|---|
| 0.00 | 204 | 167 | 191 | 153 |
| 0.70 | 206 | 171 | 193 | 157 |
| 0.75 | 213 | 178 | 200 | 165 |
| 0.80 | 218 | 187 | 206 | 174 |
| 0.85 | 235 | 210 | 227 | 198 |
| 0.90 | 263 | 250 | 263 | 249 |

Requests at the default: 53 (124 photos, largest variant 5 frames), ~110k tokens in total, largest
request ~4,000 tokens.

## Reading

- The floor is the number of groups: 37 % of this wedding are single moments. Ranking can only
  work on the rest.
- The similarity threshold is the main lever: 0.90 → 0.85 removes 265 keeps (10 points). At 0.90
  some groups fall into 10–21 variants (complete linkage: every frame must match every other).
- The people split costs 4–9 points. [0021](../decisions/0021-partial-overlap-does-not-split.md)
  measured that most such differences are a face not recognised in one frame, not a real change;
  here the cost is an extra `keep`, not a broken group.
- Nothing here says which setting is *right*: that needs the user's or the agency's picks.
