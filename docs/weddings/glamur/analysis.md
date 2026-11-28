---
wedding: glamur
id: GLA
date: 2026-11-08
analysed: 2026-11-26
editor: Ksenija
program: Photo Mechanic 5
cameras: 4
photos_before: 3432
rejected: 962
codebook: 1
reviewed_by: six agent reviewers (one per part, no second reviewer); spot check of 16 by the main agent
day_parts: from the reviewers' strip notes, approximate to a few minutes
couple_identities: B and C, from their frequency, not checked by eye
status: draft
---
# Glamur: what the agency rejects

Numbers: [summary.json](summary.json). Rows: `<out>/analysis/photos.csv` (out = `data` in
[wedding.json](wedding.json)). First write-up with method details and the full rule table:
[research 2026-11-26](../../research/2026-11-26-glamur-cull.md). The user's page with every
reject and its reason: `<out>/posle-analiza/index.html`.

## Context

- Before: 3,432 JPG from four cameras. About 1,150 file numbers are missing: the photographers
  deleted their failed frames before the hand-over, so this cull is a second sieve.
- After: kept photos in folders `1` (KNEZ), `2` (LPZ), `3` (JAS and VAL), rejected in
  `obrisano`. 4 files are in both (`LPZ_4052`, `JAS_3273`, `JAS_3557`, `JAS_3595`), left out of
  the rates.

| Camera | Role | Photos | Rejected |
|---|---|---|---|
| KNEZ | main | 1,852 | 31 % |
| LPZ_ | second | 873 | 35 % |
| JAS_ | decor (decor, tables, guests) | 536 | 14 % |
| VAL | guests (logo wall) | 167 | 9 % |

## Numbers

| Part of the day | Photos | Rejected |
|---|---|---|
| formals | 65 | 46 % |
| cake | 302 | 44 % |
| civil | 155 | 37 % |
| first_dance | 221 | 34 % |
| party | 611 | 31 % |
| reception_line | 673 | 28 % |
| church | 343 | 27 % |
| prep | 435 | 25 % |
| couple | 156 | 24 % |
| arrival | 467 | 12 % |

Near-identical neighbours (≤ 2 s, similarity ≥ 0.93): 498 pairs, both kept 133 (27 %), one
rejected 340, both rejected 25. Bursts of 3–4 keep 67 % of their frames and never lose all.

## Reasons

Codebook version 1. 962 rejects coded, one reviewer each.

| Code | Rejects | Main / second / decor / guests |
|---|---|---|
| DUP | 475 | 373 / 81 / 12 / 9 |
| EXPR | 114 | 52 / 43 / 17 / 2 |
| NOCOUPLE | 99 | 17 / 66 / 13 / 3 |
| COMP | 96 | 57 / 33 / 6 / 0 |
| MOMENT | 42 | 15 / 13 / 14 / 0 |
| CROP | 29 | 0 / 28 / 1 / 0 |
| EXPO | 25 | 11 / 14 / 0 / 0 |
| DETAIL | 24 | 21 / 2 / 1 / 0 |
| UNCLEAR | 24 | 2 / 14 / 7 / 1 |
| EYES | 18 | 11 / 6 / 1 / 0 |
| CREW | 13 | 10 / 2 / 1 / 0 |
| FOCUS | 3 | 1 / 1 / 1 / 0 |

Trust: face, eye and occlusion codes held in the spot check; `DUP` did not (3 of 8 were a worse
twin), so `DUP` is too high and the face codes too low. v1 `EXPR` also holds hidden faces
(v2 `FACE`).

## Findings

- **GLA-F01** The editor culls in Photo Mechanic 5 and marks rejects with colour class 1
  ("Winner") before moving them to `obrisano`.
  evidence: file · XMP `photomechanic:ColorClass="1"` in 949 of 962 rejects
  bears on: Q16 · holds elsewhere: FAE-F01 yes
- **GLA-F02** Technical faults are almost absent among the rejects: the photographers removed
  them before the hand-over.
  evidence: judged · FOCUS + EXPO = 28 of 962 (3 %); measured · whole-image brightness and
  sharpness have the same distributions in kept and rejected (research)
  bears on: B2, B3 · holds elsewhere: FAE-F02 yes
- **GLA-F03** The editor culls each camera alone; she does not choose the better of two
  photographers.
  evidence: measured · `cross_camera.second`: rejected 32.9 % when the main camera shot within
  3 s, 36.4 % when not
  bears on: S5 · holds elsewhere: FAE-F03 yes
- **GLA-F04** Main and second photographer lose about a third; decor and guest cameras little.
  The second photographer loses about half in the first dance and the cake.
  evidence: measured · `by_role`; `by_role_day_part` second: first_dance 54 %, cake 56 %,
  party 41 %; main: first_dance 22 %, cake 40 %
  bears on: S3 · holds elsewhere: FAE-F04 no (main 45 %, second 23 %)
- **GLA-F05** A reject is relative to a twin: the same frame without its twin would stay.
  evidence: judged · 737 of 962 rejects have a kept frame of similarity ≥ 0.8 in the same camera
  within 60 s (research); measured · no absolute measure separates kept from rejected
  bears on: K2, B1, B4 · holds elsewhere: FAE-F05 yes
- **GLA-F06** She often keeps both of two near-identical frames.
  evidence: measured · `near_identical_pairs.both_kept_share` 0.267
  bears on: K2, W3, C2 · holds elsewhere: FAE-F06 weaker (0.18)
- **GLA-F07** Every burst-thinning rule drops more frames she kept than frames she rejected.
  evidence: measured · `rules.burst_keep_first`: 254 of 498 drops she kept (51 %), catches 25 %
  of her rejects; "keep the sharpest face" is worse, 61 % (research)
  bears on: K2, K7, C3 · holds elsewhere: FAE-F07 yes
- **GLA-F08** Expression beats sharpness: where one frame of a burst was kept, the sharpest face
  is hers no more often than chance.
  evidence: measured · 122 of 260, chance 126 (research)
  bears on: W2, B4 · holds elsewhere: FAE no data
- **GLA-F09** The couple's faces must be visible: a frame with a hidden or turned-away face of
  the bride or groom goes, even inside an important moment.
  evidence: judged · v1 `EXPR` notes ("face hidden", "backs"), strip notes of the first dance
  and the cake
  bears on: K3, K4, B4 · holds elsewhere: FAE-F10 yes
- **GLA-F10** A videographer, another photographer or their gear in the frame: always rejected.
  evidence: judged · 13 `CREW`, no kept counterexample seen by the reviewers
  bears on: N1 · holds elsewhere: FAE-F11 no (kept frames with the video rig)
- **GLA-F11** Something blocking at the edge (a guest's head, an arm, the priest's robe, a
  waiter) is a reason to reject when a cleaner twin exists. This is stricter than Peđa (N1:
  heads at the edge are retouched, not rejected).
  evidence: judged · 96 `COMP`; `KNEZ3929`/`3930` rejected for robe blur at the edge
  bears on: N1, R6 · holds elsewhere: FAE-F12 yes
- **GLA-F12** Frames with the couple are rejected more often than frames without, because the
  couple is shot in bursts.
  evidence: measured · `couple_in_frame`: 38 % with both, 29 % with one, 21 % with neither
  bears on: K4 · holds elsewhere: FAE-F13 yes
- **GLA-F13** Of an in-camera crop and its wide frame, usually one stays, not both; same for
  colour and B/W, horizontal and vertical.
  evidence: judged · 29 `CROP`, strip notes of the reception line (LPZ)
  bears on: K10, Q1 · holds elsewhere: FAE-F14 partly (one per framing)
- **GLA-F14** Guests without the couple go easily in the ceremony and the party; at the
  arrival and the logo wall one frame per guest or pair stays.
  evidence: judged · 99 `NOCOUPLE`, 66 of them LPZ; measured · arrival rejects 12 %
  bears on: K6, S2 · holds elsewhere: FAE-F15 yes
- **GLA-F15** No rule "always the first frame": in posed pairs the first and the second stay
  about equally often.
  evidence: measured · first frame is hers in 161 of 260 single-keep bursts (research);
  judged · reviewers disagreed between parts
  bears on: W2 · holds elsewhere: FAE-F08 same share (63 %), read there as a default

## Losses

Reviewers marked 4 rejects `yes` and 113 `maybe`. Checked against all cameras:
`KNEZ3929`/`3930` (crowned couple, frontal, red blur at the edge; no camera kept the moment) and
`LPZ_4116` (groom's parents clapping) are real losses; `LPZ_4128` is covered by `KNEZ4371`;
`LPZ_3810`, `LPZ_4776`/`4777` are covered only by wide frames (taste). The 113 `maybe` are in
the user's page under the filter "gubitak: možda", not yet looked at.

## Questions for the agency

1. Do you always cull camera by camera? Would the same moment from the other camera next to it
   help? (GLA-F03)
2. Does the red mark "Winner" mean delete? Would the tool's proposal as a colour mark in Photo
   Mechanic suit you? (GLA-F01)
3. When two frames are nearly the same, when do you keep both? (GLA-F06)
4. `KNEZ3929`/`3930`, the crowned couple, rejected for the red blur at the edge: on purpose, or
   would you keep them as the only frontal frame? (GLA-F11)
5. Guests without the couple and the second photographer in the party: a rule or judgement?
   (GLA-F14)
6. Do the 2,466 go to the couple as they are, or is there another selection? (Q17)
7. The four files in both kept and `obrisano`: which is right?

## Limits

- One wedding, one editor; reasons are inferred, not asked.
- One reviewer per reject, no agreement measured; spot check of 16 only.
- Reviewers saw one camera's strip; covering frames of other cameras were checked only for the
  `yes` losses.
- Eyes of people at the back of wide groups are not visible at the sheet size.
- VAL's clock is not checked; parts of the day are approximate.

## Reproduce

`cull.py analysis --output "<out>" --wedding docs\weddings\glamur` from `agency_cull.json` and
`<out>/analysis/reasons.jsonl` (converted from `posle-analiza/review/part*.result.jsonl`).
Numbers marked "research" come from the scripts in `<out>/posle-analiza/scripts/`.
