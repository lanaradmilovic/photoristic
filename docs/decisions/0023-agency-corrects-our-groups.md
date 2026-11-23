# 0023 — The agency corrects our groups instead of labelling from scratch

- Status: accepted
- Date: 2026-11-17
- Decided by: agent, approved by the user

## Context
The group rule ([0014](0014-group-definition-v2.md)) and all labels were made by the user; the
agency has never confirmed them. The user wants a feedback meeting on the grouping that is smooth
for the agency and still gives feedback clear enough to tune against.

## Options considered
1. **The agency labels boundaries in label mode** — 333 decisions on 4a alone; tedious, and the
   page is in English with similarities and gaps.
2. **Show `report.html`** — passive; the answer would be "looks fine", which cannot be measured.
3. **A page that shows our groups and takes a click only where they are wrong**, plus about ten
   disputed pairs shown without our decision.

## Decision
Option 3: `cull.py meeting` ([spec](../spec/labels.md#agency-meeting-page)). The disputed pairs
test the group rule itself, one kind of case at a time, before the agency sees our groups. The
excerpts test the grouping as it is. Answers are stored as pairs in the label format, so
`cull.py score --labels` measures any later grouping against them.

## Consequences
- Pairs confirmed without a click were answered with our grouping on the screen and lean towards
  it; `source` separates them from clicks.
- A disputed pair has three answers because "deliver both" does not mean "different group".
- The content of a meeting is a hand-written `meeting.json`, not a config key.
- If the agency's answers contradict 0014, the rule gets a new decision and the 4a / Talici 1
  labels are redone.

## Evidence
Interviews: [2026-10-07](../interviews/2026-10-07-pedja-mitar-ksenija.md) (re-checking everything
is the main complaint about existing tools). Tests: `tests/test_meeting.py`.
