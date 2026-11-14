# 0022 — Code decides how many photos a group keeps; the model only ranks; no reject

- Status: accepted (narrows [0019](0019-safety-rules-in-code.md): the reject rules there are postponed)
- Date: 2026-11-11
- Decided by: agent, approved by the user

## Context
Nothing defined how many photos a group keeps. A group ([0014](0014-group-definition-v2.md)) is
not a set of duplicates: it may hold a wide and a tight framing, a vertical and a horizontal one,
and it may be a grouping mistake (two group photos that differ by one person,
[0021](0021-partial-overlap-does-not-split.md)). The judge run showed that the model does not
notice a change of action or of people and that its confidence is always 0.95–0.99
([research](../research/2026-11-11-judge-first-real-run.md)). The agency's past selections are not
available.

## Options considered
1. **Exactly one winner per group** — fewest keeps (40 % of the five Talici folders), but loses
   the second framing and every photo of a wrongly merged group except one.
2. **Tighten grouping until one winner is right** — more groups, longer review; undoes 0014.
3. **The model picks "a few best"** — leaves the count and the mixed-group question to a model
   that failed exactly there.
4. **Code splits a group into variants of near-duplicates; the model orders one variant; the
   best of every variant is kept.**

## Decision
Option 4. The number of keeps follows from signals that are already measured (DINOv2 similarity,
face identities, orientation), is tunable in `config.yaml` and can be checked without the server.
The model does the one thing it can plausibly do: compare a few near-identical frames.

Also decided for this version:
- **No `reject`.** Everything that is not `keep` is `maybe`, ordered by rank. The 0019 rule
  "a low-confidence reject becomes maybe" has nothing to work with while confidence is constant.
- A variant without a valid answer is `maybe` as a whole (it is asked again on the next run).
- Defaults are conservative: `variant_similarity` 0.90 (the people look-back threshold, below
  which DINOv2 does not separate a different guest at the same spot), people and orientation
  splits on.

## Consequences
- Keeps on the five folders: 72 % at the defaults, 61 % at 0.85, 40 % with one winner per group
  ([research](../research/2026-11-11-ranking-variants-dry-run.md)). The reduction is modest until
  `variant_similarity` is lowered, and that needs ground truth: the user marks the best photos of
  4a, or an agency selection arrives (phase 5).
- A false split of a variant costs one extra `keep`; no setting can lose a photo.
- Config: `ranking.variant_similarity`, `variant_split_orientation`, `variant_split_people`,
  `max_images`.

## Evidence
[spec/vlm-scoring.md](../spec/vlm-scoring.md); `tests/test_ranking.py`.
