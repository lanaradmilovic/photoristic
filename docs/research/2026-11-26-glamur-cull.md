# What the agency rejects: Glamur before and after Ksenija's cull (2026-11-26)

Question: the agency gave Glamur twice, as handed over by the photographers (`pre`, 3,432 JPG)
and after their editor's cull (`posle`). What does the editor reject, why, and what does that mean
for the selection step ([K1–K12](../requirements.md#how-many-frames-of-a-group-stay))? Nothing in
the pipeline was changed. Dataset: [datasets.md](../datasets.md#glamur). Report for the user (local,
Serbian, with a gallery of all rejects): `<out>/posle-analiza/index.html`.

## The two packages

- `posle` holds folders `1` (KNEZ, 1,282), `2` (LPZ, 571), `3` (JAS and VAL, 617) and
  `obrisano` (966 JPG + 10 PSD). Every `pre` file name occurs in `posle`; nothing was edited.
- **The editor culls in Photo Mechanic 5.** Rejects carry embedded XMP
  `photomechanic:ColorClass="1"`, `xmp:Label="Winner"` (PM's default name of colour class 1), which
  is why each is 126 bytes larger than its `pre` copy. 949 rejects are marked, 17 were moved
  without a mark; 54 kept photos carry PM XMP with class 0 (marked and unmarked, or touched).
- 4 files are in a kept folder and in `obrisano` (`LPZ_4052`, `JAS_3273`, `JAS_3557`,
  `JAS_3595`); left out of the numbers below.
- About 1,150 file numbers were already missing from `pre`
  ([glamur grouping](2026-11-26-glamur-grouping.md#how-it-differs-from-talići)): the photographers
  deleted their failed frames first. So this cull is a second sieve.

## Numbers

962 of 3,428 rejected (28 %): KNEZ 570/1,852 (31 %), LPZ 303/873 (35 %), JAS 74/536 (14 %),
VAL 15/167 (9 %). LPZ during the party loses about half (19 h 52 %, 22 h 56 %).

| Measure | Result |
|---|---|
| Whole-image brightness, sharpness (Laplacian, Tenengrad), clipping | Same distributions for kept and rejected (mean 85 vs 85, Laplacian 1,000 vs 977) |
| Sharpness of the largest face | Weak: 58 % of rejects in a mixed group are below the group's kept median (chance 50 %) |
| Bursts (≤ 2 s, sim ≥ 0.9) where exactly one was kept (260) | The sharpest face is hers in 122; chance gives 126. First frame is hers in 161 |
| Adjacent pairs ≤ 2 s, similarity ≥ 0.93 (498) | Both kept 133 (27 %), one rejected 340, both rejected 25 |
| Bursts of 5–8 frames | About two thirds kept; never none |
| Lone frames (no neighbour within 2 s) | 269 of 1,398 rejected (19 %): not dedup |
| LPZ rejected when KNEZ shot within 3 s / not | 33 % / 36 %: she culls each camera alone, no cross-camera choice |
| Couple (face identities B and C) in frame, KNEZ | Rejected more often: both 37 %, one 27 %, neither 23 % (the couple is shot in bursts) |
| Mean brightness < 0.5 of the median of ±3 neighbours | 14 of 34 rejected: dark frames are often intended |
| Rejected with a kept frame of similarity ≥ 0.8 in the same camera within 60 s | 737 of 962 |

Simple thinning rules scored against her decisions (`rules.py`):

| Rule | Drops | Of them she kept | Of her rejects caught |
|---|---|---|---|
| Burst ≤ 2 s, sim ≥ 0.95, keep sharpest face | 365 | 215 (59 %) | 16 % |
| Burst ≤ 2 s, sim ≥ 0.93, keep sharpest face | 498 | 303 (61 %) | 20 % |
| Burst ≤ 2 s, sim ≥ 0.9, keep half | 578 | 344 (60 %) | 24 % |
| Burst ≤ 5 s, sim ≥ 0.9, keep sharpest face | 825 | 517 (63 %) | 32 % |

**Every burst-thinning rule drops more photos she kept than photos she rejected.** One winner
per variant is far stricter than the agency.

## Reasons, by eye

Six parallel agent reviewers, each on 20 sheets of strips (consecutive frames of one camera, green
kept, red rejected), opened the 1536 px preview whenever the thumbnail did not show the reason.
Brief, assignment files and answers: `<out>/posle-analiza/review/`. Codes are a reviewer's
judgement, not the editor's word.

| Code | Rejects | Meaning |
|---|---|---|
| DUP | 475 | near-identical to a kept frame |
| EXPR | 114 | worse face than the kept twin: mid-word, grimace, looking away, face hidden |
| NOCOUPLE | 99 | guests only, low interest |
| COMP | 96 | something blocks (head, arm, priest's robe, waiter, phone), subject cut |
| MOMENT | 42 | in-between instant, backs |
| CROP | 29 | in-camera crop duplicates a kept frame or the reverse |
| EXPO | 25 | flash did not fire, coloured stage light on faces |
| DETAIL | 24 | redundant detail or decor |
| UNCLEAR | 24 | no visible reason |
| EYES | 18 | closed or half-closed eyes |
| CREW | 13 | videographer, other photographer or gear in frame (always rejected) |
| FOCUS | 3 | missed focus |

Loss as judged by the reviewers: no 845, maybe 113, yes 4.

Spot check by the main agent, 16 random answers: face, eyes and occlusion calls hold; **3 of 8
`DUP` are a worse sibling, not a copy** (`KNEZ4275` bride looks down, `LPZ_3862` weaker
expression, `LPZ_4418` backs and darker). Plain thinning is therefore below half, and the face
reasons are under-counted.

Reviewers disagreed on the order inside posed pairs (part 3: first kept; part 4: second kept after
a pause). Counted over isolated pairs ≤ 1 s, neither order dominates and both-kept is common.

The four "yes" losses, checked against all cameras with corrected clocks: `KNEZ3929`/`3930`
(crowned couple, frontal, sharp, red blur of the priest's robe at the edge; no camera kept the
moment) and `LPZ_4116` (groom's parents clapping) are real; `LPZ_4128` is covered by `KNEZ4371`.
`LPZ_3810` and `LPZ_4776`/`4777` (close, tender frames) are covered only by KNEZ wides: taste.

## What it means

1. The selection must be relative to a twin: the reasons are differences between frames of the
   same moment (eyes, face visible, occlusion, crew, flash), not absolute quality.
2. A technical filter has little to do on a package the photographers already cleaned (FOCUS and
   EXPO are 3 % of rejects).
3. The safe default of K2/K7 (drop only bad frames and exact copies, keep the rest) matches the
   editor better than one winner per variant: she keeps both of a near-identical pair in a
   quarter of cases.
4. This pair of packages is the first ground truth of "what the agency keeps". A score of tool
   suggestions against it (her keeps that the tool would drop; her rejects it catches) is the
   measure a selection change needs. One wedding, one editor.
5. Photo Mechanic reads XMP colour classes: suggestions could reach her in her own program.

## Limits

- One wedding, one editor; reasons are inferred, not asked.
- Reviewers saw only one camera's strip; covering frames in other cameras were checked only for
  the "yes" losses.
- Eyes of people at the back of wide groups are not visible at the sheet size; `DUP` may hide
  `EYES`/`EXPR` there.
- Face identities B and C were taken as the couple from their frequency, not checked by eye.

## Reproduce

Scripts in `<out>/posle-analiza/scripts/` (run with `.venv\Scripts\python`, argument = a working
folder): `match.py`, `xmpall.py` (Photo Mechanic marks), `master.py` (one row per photo: status,
group, metrics), `stats1.py`–`stats4.py`, `rules.py`, `sheets.py` (strips), `merge.py`,
`montage.py`, `report.py` (page from `report_template.html` and `text.html`). Results:
`master3.json`, `reasons.json`, `xcam_check.json`, `xmp.json`. Paths inside the scripts point at
the scratchpad they were written in; change `S` to the output folder to rerun.
