# The current grouping on a four-camera JPG wedding (Glamur, 2026-11-26)

Question: how well does the grouping of branch `grouping-v3` (after
[0027](../decisions/0027-lookback-and-burst-variants.md)) work on a wedding it was never tuned
on, and what does a wedding with several cameras mean for grouping across cameras
([S5](../requirements.md#scope), [0003](../decisions/0003-camera-by-serial-group-per-camera.md))?
Nothing was tuned; this is a measurement. Dataset: [datasets.md](../datasets.md#glamur).

## The wedding

One wedding, 8 Nov 2026, 3,432 JPG in 31 card-dump folders, no RAW. `cull.py prepare` with
`--exclude "00 Nove Montaze"` (9 montage JPGs skipped) took 80 minutes on CPU: ingest 10,
embeddings 4, person detection 31, faces 34.

Ingest: 0 failures, 0 flags, every camera has a serial number, no file name occurs twice, one
photo has no sub-second time.

| Camera | Body | Photos | Shooting | Median gap | Groups | Single | 2 | 3–5 | 6–10 | 11+ | Largest |
|---|---|---|---|---|---|---|---|---|---|---|---|
| KNEZ | Canon R5 II | 1,852 | 11:32–22:22 | 1.8 s | 561 | 247 | 142 | 112 | 26 | 34 | 56 |
| LPZ | Nikon Z6 III | 874 | 11:12–22:18 | 3.9 s | 566 | 415 | 102 | 39 | 7 | 3 | 29 |
| JAS | Nikon D750 | 539 | 14:46–20:37 | 15.7 s | 400 | 322 | 50 | 23 | 4 | 1 | 11 |
| VAL | Canon R6 II | 167 | 15:58–17:35 | 3.5 s | 71 | 6 | 39 | 25 | 1 | 0 | 6 |
| all | | 3,432 | | | 1,598 | 990 | 333 | 199 | 38 | 38 | 56 |

2,442 photos are in a group of two or more (4.0 photos per such group); 147 photos joined by
look-back, in 73 groups. Gaps between neighbours of one camera: 1,377 under 2 s, 1,704 of 2–40 s,
347 over 40 s.

## How it differs from Talići

- **Four cameras with different jobs.** KNEZ follows the couple all day in bursts. LPZ stands
  next to KNEZ for much of the day. JAS shoots decor, tables and guests. VAL only photographs
  arriving guests in front of the venue's logo wall and never shows what another camera shows.
- **Printing workflow.** Most of the evening is a line of guests posing with the couple at one
  spot (the gazebo, the head table), one line-up every 10–30 s: the photos printed and sold
  during the wedding, which the agency says the tool is not for
  ([S2](../requirements.md#scope)). They are about a third of the labelled pairs.
- **In-camera crops.** Photographers cut a tight frame of one or two people out of a posed photo
  in the camera. The crop gets a new file number but keeps the capture time of its source: on LPZ
  131 photos in 61 sets share the exact capture time with another photo, 65 of them smaller than
  the full frame; KNEZ 18 photos in 8 sets; JAS 8 in 4. Another 90 (LPZ) and 79 (JAS, Nikon trim
  sizes) are crops whose source frame is not in the folders.
- **File order is not time order.** Neighbours in capture order whose file number goes down:
  LPZ 47, KNEZ 20, JAS 17. The pipeline sorts by capture time, so this only matters for a human
  reading file names.
- **Frames were deleted before hand-over.** Missing file numbers inside each camera's range:
  JAS 529 of 1,068, LPZ 403 of 1,277, KNEZ 208 of 2,060, VAL 15 of 182. As on Talići
  ([gaps](2026-11-19-file-number-gaps.md)) the pipeline did not see plainly bad frames.
- **JPG only, several sizes** per camera (crop modes and trims); previews come from the JPG.

## Camera clocks

`scripts/clocks.py` counts, for every shift of one camera's clock, the pairs of two cameras that
look alike (DINOv2) and fall within 2 s of each other.

| Cameras | Offset | Evidence |
|---|---|---|
| LPZ against KNEZ | LPZ is 297.9 s ahead | 473 alike pairs at that shift, at most 193 at 99.9 % of all other shifts, 32 at shift 0; median of 395 pairs, 10–90 % 295.0–300.6 s |
| KNEZ against JAS | KNEZ is 67.8 s ahead | weak peak (91 against 61); 89 pairs, 65.3–70.5 s |
| LPZ against JAS | LPZ is 366.9 s ahead | weak peak (49 against 35); 67.8 + 297.9 = 365.7, so the three agree within 1.2 s |
| VAL against any | could not be checked | no pair with similarity 0.80 or more at any shift |

Checked by eye on `clocks/clocks_KNEZ_LPZ_shifted.jpg` (12 of 12 pairs show the same instant from
two positions) and `clocks_JAS_KNEZ_shifted.jpg` (the three most similar pairs are the same
instant: entrance, first dance, bride with a guest; the rest are other guests at the same spot).
**The clocks do not agree: with the times as written, the same moment is 5 or 6 minutes apart
between cameras.**

## Labels

Rule [0025](../decisions/0025-group-definition-v3.md), checks
[0026](../decisions/0026-labelling-checks.md), written out with the sheet format in
`labelling/PROTOCOL.md`.

- Labelled: all 1,704 pairs 2–40 s apart, 100 random pairs under 2 s, 100 random over 40 s.
- First pass: ten parallel agent passes, each on its own stretch of contact sheets (24 thumbnails
  of 320 px per sheet), without groups or similarity on the sheet. Result: 1,207 different, 617
  same, 80 unsure. On three sheets the main agent labelled blind beforehand, 48 of 52 answers
  were the same (the four others: scenery from another spot, and one crop of a group).
- The passes disagreed with each other on one kind of pair: a posed group next to a tight frame
  of only some of the same people, nobody moved. Check 1 says different, check 2 says same. It
  was ruled `unsure` for the second look; first-pass answers of this kind that were not looked at
  again keep their first label (see Limits).
- Second look, six passes, 480 px per photo, random order, blind to the first answer and to the
  grouping: the 251 pairs where first label and pipeline disagreed, the 80 unsure, and 150 random
  pairs where they agreed. A pair keeps a label only when both looks gave the same `same` or
  `different`; otherwise it is `unsure`.
  - disagreements: 202 repeated, 26 turned to the pipeline's side, 23 unsure;
  - unsure: 33 stayed, 47 got an answer in the second look but stay `unsure` by the rule;
  - controls: 138 of 150 the same, 6 the opposite, 6 unsure.

Final `labels.json`: 1,904 pairs, 604 same, 1,159 different, 141 unsure.

## Score

`cull.py score`: **1,561 of 1,763 correct (88.5 %), 91 false merges, 111 missed merges**;
precision 0.844, recall 0.816 for "same". Talići 1: 648 of 710 (91.3 %), 4a: 310 of 333 (93.1 %).

| Gap | Pairs | Same | Similarity | Different | Similarity | Unsure | False merges | Missed | Correct |
|---|---|---|---|---|---|---|---|---|---|
| < 2 s (sample) | 100 | 78 | 0.93 [0.84–0.98] | 5 | 0.65 [0.57–0.81] | 17 | 1 | 4 | 78 of 83 |
| 2–5 s | 533 | 339 | 0.86 [0.72–0.95] | 136 | 0.65 [0.39–0.80] | 58 | 20 | 47 | 408 of 475 |
| 5–15 s | 589 | 157 | 0.84 [0.67–0.93] | 381 | 0.64 [0.39–0.81] | 51 | 36 | 47 | 455 of 538 |
| 15–40 s | 582 | 30 | 0.80 [0.62–0.93] | 539 | 0.62 [0.38–0.78] | 13 | 34 | 13 | 522 of 569 |
| > 40 s (sample) | 100 | 0 | | 98 | 0.58 [0.20–0.75] | 2 | 0 | 0 | 98 of 98 |

| Camera | Scored | Correct | False merges | Missed |
|---|---|---|---|---|
| KNEZ | 785 | 658 (83.8 %) | 50 | 77 |
| LPZ | 459 | 432 (94.1 %) | 13 | 14 |
| JAS | 380 | 345 (90.8 %) | 19 | 16 |
| VAL | 139 | 126 (90.6 %) | 9 | 4 |

The two assumptions hold here too: over 40 s no sampled pair is the same moment and the pipeline
joins none; under 2 s 78 of 83 are the same. Under 2 s the five `different` and most of the 17
`unsure` are in-camera crops next to their source frame.

## Kinds of mistakes

False merges (91), the error that can lose a photo:

| Kind | About | Examples | Similarity |
|---|---|---|---|
| Other guests with the couple at the same spot, 10–36 s later | 40 | `KNEZ4042`/`4043`, `4052`/`4053`, `4462`/`4463`, `4474`/`4475`, `4506`/`4507`, `4569`/`4572` | 0.72–0.96 |
| A person added to or gone from a posed group | 18 | `VAL14972`/`14974`, `VAL15115`/`15116`, `JAS_3574`/`3575`, `JAS_4158`/`4159`, `KNEZ3653`/`3654` | 0.74–0.90 |
| A new pose or gesture seconds later (kiss, hug, arm) | 23 | `KNEZ3626`/`3627` (2.3 s), `KNEZ4237`/`4238`, `LPZ_3595`/`3596`, `LPZ_4602`/`4604` | 0.73–0.97 |
| Another table's centrepiece | 9 | `JAS_3464`/`3465` to `JAS_3468`/`3469` | 0.82–0.90 |

The first kind is the known DINOv2 failure (another guest at the same spot scores 0.85–0.88) at
full scale. The largest group, `g0318`, is 56 photos of about eleven different line-ups at the
gazebo (`KNEZ4450`–`4512`, 188 s, 8 look-back joins); it is the first row of
`group_sheets/largest_01.jpg`. The couple is in every frame and the guests are not identities, so
the faces signal cannot separate them. Under one winner per group this would drop ten families.

Missed merges (111), which cost review time:

| Kind | About | Examples | Similarity |
|---|---|---|---|
| Same pose wider and tighter, vertical and horizontal, detail and whole | 45 | `KNEZ4075`/`4076` (0.24), `KNEZ4130`/`4131`, `KNEZ4222`/`4223`, `JAS_3311`/`3312`, `VAL15055`/`15056` | 0.24–0.85 |
| One action going on (walk, first dance, ceremony, cake, procession) | 48 | `KNEZ3797`/`3798`, `KNEZ3865`/`3866`, `LPZ_3716`/`3717`, `LPZ_4420`/`4421`, `JAS_4005`/`4006` | 0.39–0.86 |
| Details and flat lays, closer and wider | 18 | `KNEZ3499`–`3502`, `KNEZ3514`/`3515`, `KNEZ3808`–`3812`, `KNEZ4087`/`4088` | 0.39–0.80 |

Both sides are the finding of [the Talići measurement](2026-11-25-labels-v3-and-signal-ceiling.md):
whole-frame similarity sees the picture, the rule asks who stands how. The ranges of same and
different overlap in every gap bucket.

## Across cameras

`scripts/cross_camera.py`, per-camera groups unchanged, only counted.

| | Clocks as written | Clocks corrected |
|---|---|---|
| Photos with a photo of another camera within 2 s | 603 (18 %) | 1,220 (36 %) |
| Pairs of two cameras within 2 s | 501 | 1,496 (1,153 are KNEZ + LPZ) |
| Their similarity, median [10–90 %] | 0.48 [0.17–0.70] | 0.63 [0.33–0.81] |
| Similarity 0.75 or more | 22 | 333 |
| Pairs that pass the neighbour rule of one camera | 66 | 830, linking 143 pairs of groups; 171 groups (895 photos) have a partner in another camera |

By eye, 36 random pairs within 2 s with corrected clocks (`cross_camera/corrected_01, 03, 05.jpg`):
22 show the same moment, 14 do not (another subject of the same event, or guests elsewhere). Of
the 22, eight are one camera's tight frame of a few people from the other camera's line-up. Only
8 of the 22 pass the similarity rule (median similarity 0.69, lowest 0.46); 1 of the 14 passes.

What it means for S5 and 0003:

1. **Merging by capture time needs a clock offset per camera first.** As written, time alone
   would pair unrelated photos. The offset can be estimated from the photos when two cameras
   shoot the same scenes (LPZ: clear; JAS: weak but consistent); for a camera that never does
   (VAL) it cannot, and that camera has to stay on its own timeline.
2. **Two cameras do shoot the same moment often**: about a third of the photos have a partner
   within 2 s once the clocks are corrected, and roughly six in ten of those pairs are the same
   moment.
3. **The neighbour rule of one camera does not carry over.** Across cameras the same moment is
   seen from another position or as a tight frame of part of the group, so similarity is low
   (0.46–0.91); the rule finds about a third of the same-moment pairs. Time is the stronger
   signal there, similarity the weaker.
4. 0003 stays right as the safe default: per-camera groups lose nothing. Cross-camera merging is
   a separate step on top (offset, then pairing of groups), and choosing "the better frame across
   both" inherits the open question of a wide frame against a tight frame of some of the people.

## Limits: what was not checked

- The labels are the agent's, from thumbnails; the user has not seen them yet. The review page
  measures that (`review/`, 120 pairs).
- 6 of 150 control pairs got the opposite answer in the second look (4 %). About 1,290 pairs were
  labelled once and agree with the pipeline; at that rate some 50 of them carry a wrong label, so
  the 88.5 % is an upper estimate. The second look went to disagreements, which can only move a
  pair out of the errors.
- "Tight frame of some of the people" was ruled `unsure` only for pairs seen twice. First-pass
  answers of that kind (labelled `different` by most passes) that agree with the pipeline's split
  count as correct.
- Pairs under 2 s and over 40 s: 100 of 1,377 and 100 of 347 were sampled; the rest have no label.
- Look-back joins (147 photos) are not adjacent pairs and are not scored; `g0318` shows they join
  different line-ups.
- VAL's clock; the offsets of JAS rest on a weak peak plus three pairs checked by eye.
- Whether in-camera crops should be grouped with their source frame (the checks do not say).
- Faces, segments and ranking output were not reviewed.
- Checks 3, 4 and 5 of 0026 are still ours, not the agency's (Q11–Q13).

## Reproduce

Output folder `<OneDrive>/…/photoristicxtajna/output/2026-11-26-glamur/`. Scripts are in its
`scripts/` folder (outside git): `overview.py` (tables above), `clocks.py`, `label_sheets.py`,
`assign.py`, `collect_labels.py`, `pass2_sheets.py`, `final_labels.py` (labels.json and the gap
table), `cross_camera.py asis|corrected`, `group_sheets.py`, `review_page.py`. The labellers'
answers with their notes are `labelling/pass1_*.txt` and `pass2_*.txt`; every pair with both
answers, the pipeline's decision and the similarity is `labelling/final.json`. All errors:
`errors.jpg`. Review page: `cull.py meeting --output <out>\review`, then
`cull.py meeting-score --output <out>\review` (its last block lists where the user's answer
differs from `labels.json`).
