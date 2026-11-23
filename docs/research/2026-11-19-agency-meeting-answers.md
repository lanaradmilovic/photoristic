# Agency meeting 2026-11-19: what was saved on the two pages

What Peđa answered on `cull.py meeting` and on the pick sample, as numbers. What was said is in the
[interview summary](../interviews/2026-11-19-pedja-ksenija-grupisanje-i-izbor.md).

Caveat for everything below: the disputed pairs, the excerpts and the pick sample were chosen from
metadata, and nobody checked before the meeting that a pair shows what its `kind` says.

## Disputed pairs (18 of 20 answered)

| Answer | Pairs |
|---|---|
| one is enough | 8 |
| same moment, deliver both | 9 |
| different moment / people | 1 |
| no answer (notes: "ništa" for a dark pair, "različite, obe") | 2 |

| Kind (as chosen from metadata) | Answers |
|---|---|
| ista-poza-posle-pauze | both, one, both ("bitan momenat, prvi susret"), different |
| osoba-vise-manje | both, both, "različite, obe" (note only), "ništa" (note only) |
| razliciti-gosti | one, both ("mlada na obe ok"), one, one |
| siri-uzi | one, one, both, both |
| uspravna-polozena | both ("sa najbližima sve"), both, one ("širu jer su iste"), one |

No kind got one consistent answer. The notes and the recording say why: the answer follows the
importance of the moment and of the people, not the kind of difference between the frames.

## Excerpts (not done)

Four pairs clicked, no excerpt confirmed, Deo 3 not opened.

| Excerpt | Click | The user's `labels.json` |
|---|---|---|
| Deo 1 (4a) | cut `_KAD9815` / `_KAD9817` | same |
| Deo 1 (4a) | join `_KAD9847` + `_KAD9848` | different |
| Deo 2 (Talici 1) | cut `_KAD8020` / `_KAD8029` | – |
| Deo 2 (Talici 1) | cut `_KAD8028` / `_KAD8032` | – |

Too few to score a grouping against.

## Best photo (23 of 23 groups, 78 photos)

- Picked: 59 of 78 photos (76 %).
- Photos picked per group: 1 in 8 groups, 2 in 7, 3 in 4, 4 in 2, all 8 in one, all 9 in one.
- "Would it matter if the program had kept the other photo?": answered on 5 of the 8 pairs that
  had the question, 5 times "it would not".
- Reason buttons: used in 0 groups. Notes in 8 groups, mostly "all, there are few of them" and
  "important moment".
- `ranking.json` (one keep per variant) keeps 35 of the 59 picked photos; the other 24 are `maybe`.
  The model's winner was picked in 19 of 22 variants, which says little when most photos are picked.
- Groups the model was "sure" about (g0050, g0075): both photos picked.
- g0126 (every frame "eyes closed" by the per-photo check, scores 9): all 9 picked.
- g0008, the one group the user had also done: the user picked `_KAD9794`, Peđa `_KAD9795`.

## What it means

- One winner per variant is stricter than what the agency does: on this sample it would move 24 of
  59 delivered photos to `maybe`.
- The pairwise report prompt that keeps both frames unless a defect is found (85 % of photos kept
  on 4a, [research](2026-11-15-report-prompt-both-orders.md)) is closer to their 76 % than the
  ranking is. Not measured photo by photo yet.
- How many frames of a moment stay depends on things the pipeline does not have: how important the
  moment is, who is in the frame, how many frames of the moment exist.

## Files

`data/meeting/meeting_answers.json`, `data/out-4a/picks.agency.json`, `data/meeting/meeting.json`,
`data/meeting/picks_sample.json`; transcripts `propmt-images/meeting-1.txt`, `meeting-2.txt` (not in git).
Reproduce: `cull.py meeting-score --output data\meeting`,
`cull.py pick-score --output data\out-4a --picks-file picks.agency.json --compare picks.json`.
