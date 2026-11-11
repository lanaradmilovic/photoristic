# VLM judge: dry-run on the five talici folders

Date: 2026-10-23 (branch `judge`, 118 tests). No real VLM call yet. Spec:
[vlm-judge.md](../spec/vlm-judge.md).

## Pairs per folder (default config, band 0.80–0.90)

| Folder | Pairs | of which look-back | at sim_low 0.79 | at 0.78 |
|---|---|---|---|---|
| talici 4a | 115 | 59 | 126 | 136 |
| Talici 1 | 118 | 64 | 131 | 141 |
| Talici 2 | 23 | 13 | 23 | 25 |
| Talici 3 | 204 | 123 | 223 | 234 |
| talici 4 | 226 | 130 | 255 | 278 |

Total 686 pairs, ~790k prompt tokens, ~46 min at 4 s/call. Estimated prompt tokens per call:
1114 / 1122 / 1314 (compare with `usage.prompt_tokens` on the first real run).

## Expected cases

- T1 8028→8029 (0.894, split) and 8028→8030 are asked; 8134–8138 and 8033→8049 are decided by
  faces or below the band.
- 4a 9975/9976 vs 9982 are below the band (0.78/0.69); 9852–9856 vs 9860/9861 excluded (faces different).
- T4 dancing couple 0625→0626 (0.796) and 0627→0628 (0.793) miss the band by a hair (`sim_low`
  0.79 would catch them); 0636 vs 0637–0641 vs 0642–0643 are three different couples, blocked by
  faces correctly.

## Redundancy (visual inspection of the pair sheets)

- ~17 % of pairs are joined bursts (gap < 2 s or sim ≥ 0.88).
- ~22 % are look-back pairs that repeat one anchor photo against every frame of a later group.
- The genuine grey zone is 35–55 % per folder.
- To cut cost: dedupe look-back per pair of groups, skip joined bursts, consider `sim_low` 0.79.

Joins that look wrong to the eye: 4a `_KAD0178/0179` (full-length vs 3/4 framing — fine under the
new group rule), T1 party groups (3 vs 4 men, a group of 4 vs 6 — wrong under the new rule).
