# 0027 — Same people return to a group only at 0.82; a variant is one burst

- Status: accepted
- Date: 2026-11-25
- Decided by: the user asked to implement what does not depend on the agency's open answers; the
  two changes and their values were chosen by the agent from the measurements below

## Context
Two parts of the pipeline were built for the group rule of [0014](0014-group-definition-v2.md),
where the same people in a new pose stayed one group:

- the relaxed look-back for the same identified people (`faces_lookback_similarity_threshold`
  0.70, set from "the couple at the same spot in a new pose scores 0.72");
- the variants of [0022](0022-variants-in-code-model-ranks.md): frames with similarity 0.90 to
  each other are interchangeable, however far apart in time.

[0025](0025-group-definition-v3.md) makes a new pose a new group, and Peđa cut exactly two such
look-back joins. His picks show that similar frames seconds apart are both delivered
([requirements C2, K3–K7](../requirements.md#principle)). The thresholds for neighbours are at
their limit ([research](../research/2026-11-25-labels-v3-and-signal-ceiling.md)), and the open
answers of the agency ([Q11–Q14](../requirements.md#open-questions)) do not touch these two points.

## Options considered
1. **Wait for the answers** — neither change depends on them.
2. **A shorter look-back window for photos with people** (new key, 70 s) — removes both cuts, but
   the value sits between two points (75 s and the confirmed 59 s) and adds a key.
3. **Turn the relaxed look-back off** (0.90 as for everybody) — 9 labelled pairs worse.
4. **Same-people look-back at 0.82**, the value neighbours need beyond `time_gap_seconds`.
5. **Variants limited to one burst** (`variant_max_gap_seconds`), measured at 1, 2, 3 and 5 s.
6. **A higher `variant_similarity` instead** (0.95) — fewer lost picks, but it also splits real
   bursts (keeps 96 % on 4a) and has no reading in the requirements.

## Decision
Options 4 and 5.

- `grouping.faces_lookback_similarity_threshold`: 0.70 → 0.82.
- New `ranking.variant_max_gap_seconds`: 2.0. A frame joins a variant only within 2 s of the
  variant's last frame, so a long burst stays one variant. 2 s is the gap below which labelled
  pairs are nearly always the same moment (259 of 270).

## Consequences
- Both look-back joins Peđa cut (8020|8029, 8028|8032) are gone; the return he confirmed
  (9789 → 9796) stays. Labels: 4a 310 → 310 of 333, Talići 1 649 → 648 of 710. Look-back joins on
  Talići 1: 31 → 16.
- Of the 59 photos Peđa picked in 23 groups, 11 instead of 20 cannot all be `keep`. Keeps rise
  from 79 % to 91 % on 4a and from 68 % to 83 % on Talići 1. Nothing is rejected in either case:
  what is not `keep` is `maybe`.
- The 11 that remain are bursts where he keeps every frame (the smoke kiss, the exit from the
  church). No rule of similarity and time gives that; it needs the importance of the moment or
  his answer to [Q14](../requirements.md#open-questions).
- The review gets less shorter. That is the direction the agency asked for (C1–C3).
- `ranking.json` files made before this decision use the old variants; run `cull.py rank` again.
- Look-back joins are still not covered by labels; inside the ceremony some join different steps
  (4a: 0043 with 0057).

## Evidence
[research/2026-11-25-lookback-and-burst-variants.md](../research/2026-11-25-lookback-and-burst-variants.md);
`tests/test_grouping.py`, `tests/test_ranking.py`.
