# 0026 — Fixed checks for labelling a boundary

- Status: proposed (applied to the labels of 4a and Talići 1 on 2026-11-25; three checks wait for
  the agency's answer)
- Date: 2026-11-25
- Decided by: the user asked for one consistent rule after the review of the labels; the checks
  were written by the agent from her decisions on the disputed pairs

## Context
[0025](0025-group-definition-v3.md) says what a group is, but "a new pose taken on purpose" left
room for judgement. When the user and the agent labelled the same pairs, a raised arm, a kiss a
few seconds later, a turned body and scenery from another spot got both answers
([research](../research/2026-11-25-labels-v3-and-signal-ceiling.md)).

## Options considered
1. **Keep labelling by judgement** — the answers changed from pair to pair, also for one labeller.
2. **Every visible difference is a new group** — rejected in 0025 (the walk and the kiss).
3. **A fixed list of checks, applied in order.**

## Decision
Option 3. For the boundary between two adjacent photos:

1. Other main people, or another person (or their hand) entering the frame → `different`.
2. The same arrangement of bodies (who sits, stands, lies, hugs or faces whom) → `same`. Framing,
   orientation, distance, black-and-white, flash, background, gaze, expression, a turn of the head,
   a hand resting elsewhere and one person alone turning the body do not count.
3. The arrangement changed (kiss, embrace, moving apart, an arm raised or flung out, a leg kicked
   up): `same` when the gap is 2 s or less (the action is still going on), otherwise `different`.
4. The photographer went to the opposite side of the subjects (front against back) → `different`.
   A step closer or a tilt is `same`.
5. Scenery, decor, details: the same thing from about the same spot, or closer and wider, →
   `same`; another view the photographer walked to → `different`.
6. A walk, an entrance, a dance in progress is one action while it lasts (0025).
7. When the pose cannot be seen (people tiny in a wide shot) or the checks do not settle it →
   `unsure`, not a guess.

## Consequences
- The labels of 4a (333) and Talići 1 (710) follow these checks for every pair that was discussed;
  the other pairs were labelled with the same intent but not re-checked one by one.
- Checks 3, 4 and 5 are ours. They are asked on the question page (`nova-poza`, `druga-strana`,
  `prostor`); an answer from the agency replaces them
  ([requirements Q11–Q13](../requirements.md#open-questions)).
- The 2 s in check 3 is a labelling convention, not a pipeline threshold.

## Evidence
[research/2026-11-25-labels-v3-and-signal-ceiling.md](../research/2026-11-25-labels-v3-and-signal-ceiling.md),
Peđa's M6 and M13 for check 2 and X8 for check 3
([record](../interviews/2026-11-19-pedja-slika-po-slika.md)).
