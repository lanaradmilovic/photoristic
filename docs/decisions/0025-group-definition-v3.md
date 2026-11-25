# 0025 — Group = literally the same moment; a new pose taken on purpose is a new group

- Status: accepted (supersedes [0014](0014-group-definition-v2.md))
- Date: 2026-11-24
- Decided by: the user, after the agency meeting of 2026-11-19

## Context
Peđa asked for stricter grouping: a group is "literally the same moment, not a similar moment"
([requirements G1–G8](../requirements.md#groups)). He cut three of our groups, each where the pose
changed, and left a ten-frame walk and a five-frame kiss as one group
([record X1–X12](../interviews/2026-11-19-pedja-slika-po-slika.md#pregled-grupa-isečci)).
[0014](0014-group-definition-v2.md) kept a new pose in the group. The labels need one rule to be
redone against; the user decided the two borderline cases on 2026-11-24.

## Options considered
1. **Keep 0014** — contradicts his cuts.
2. **Every visible change of pose is a new group** — contradicts the walk and the kiss he left
   whole; nearly every frame would become its own group.
3. **Wide and tight framing are separate groups** ([0013](0013-group-definition-v1.md)) — he says
   orientation and framing are not the criterion, the moment is.
4. **One moment = the photographer kept shooting the same thing; a pose taken on purpose starts a
   new group.**

## Decision
Option 4.

The same group:
- frames of one continuous action in the same set-up: a change of expression, gesture or step a
  second or two later (the walk through the church; the kiss with the look before and the smile
  after);
- the same pose in the same moment framed wider or tighter, or horizontal and vertical;
- the same pose taken again after a short pause;
- black-and-white and colour; with flash and without;
- details of the same object from different distances.

A new group:
- a new pose taken on purpose, or a new framing together with a new pose, also seconds later with
  the same people at the same place (his three cuts);
- a return to the same people and place later, in another pose;
- different people, including a person added to or missing from a posed group photo (as in 0014);
- a new activity or a new place.

A group is the set of frames the selection rules are applied to, not "keep one of these". How many
frames of a group stay is a separate decision ([requirements K1–K12](../requirements.md#how-many-frames-of-a-group-stay)).
When in doubt, split.

## Consequences
- **Labels.** Every pair labelled `same` in 4a and Talići 1 is checked again by the user, except
  bursts (2 s apart at most, similarity 0.93 or more), which stay `same` under any reading. Labels
  `different` stay: only 3 of 155 (4a) and 1 of 219 (Talići 1) are close and similar enough to be
  old wide/tight splits. The labels as they were are in `labels.before-v3.json` next to
  `labels.json`.
- **Thresholds** are not tuned to this rule yet. A higher similarity threshold alone does not give
  it; the look-back join is the first candidate
  ([research](../research/2026-11-23-meeting-choices-vs-signals.md)).
- The VLM judge prompt and [spec/grouping.md](../spec/grouping.md#what-a-group-is) quote the rule.
- `meeting_answers.json`: an answer "same moment, both" is not a label for this rule
  ([requirements Q7](../requirements.md#open-questions)).

## Evidence
[requirements.md](../requirements.md), the
[photo-by-photo record](../interviews/2026-11-19-pedja-slika-po-slika.md),
[research/2026-11-23-meeting-choices-vs-signals.md](../research/2026-11-23-meeting-choices-vs-signals.md).
