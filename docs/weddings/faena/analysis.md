---
wedding: faena
id: FAE
date: 2026-10-03
analysed: 2026-11-28
editor: unknown (the agency's editor)
program: Photo Mechanic
cameras: 4
photos_before: 3822
rejected: 1291
codebook: 2
reviewed_by: eight agent reviewers (one per part); a second, blind reviewer on 129 rejects (10 %); 17 `yes` losses checked by the main agent, 13 of them by eye
day_parts: overview sheets, corrected from the reviewers' strip notes; approximate to a few minutes
couple_identities: B and C, checked by eye on the face sheets
status: draft
---
# Faena: what the agency rejects

Numbers: [summary.json](summary.json). Rows: `<out>/analysis/photos.csv` (out = `data` in
[wedding.json](wedding.json)). Reviewers' material (brief, strips, answers, what the editor does
strip by strip): `<out>/posle-analiza/review/`.

## Context

- Before: 3,822 JPG from four cameras. About 820 file numbers are missing: the photographers
  deleted failed frames before the hand-over, so this cull is a second sieve.
- After: kept photos in folders `1` (NIK_), `2` (DAVN), `3` (JAS_ and MIL_), rejected in
  `obrisano`. No file is in both. `00 Nove Montaze` was left out.
- The day: groom's home (DAVN) and bride's home (NIK_), church, couple session at the venue, civil
  ceremony in the hall at 17:04, posed photos with guest groups at the flower wall, first dance,
  party, cake.

| Camera | Role | Photos | Rejected |
|---|---|---|---|
| NIK_ | main | 1,948 | 45 % |
| DAVN | second | 1,167 | 23 % |
| JAS_ | decor (decor, guests, table portraits, party) | 582 | 22 % |
| MIL_ | guests (hall entrance) | 125 | 6 % |

## Numbers

| Part of the day | Photos | Rejected | Main | Second |
|---|---|---|---|---|
| couple | 222 | 47 % | 47 % | – |
| civil | 153 | 43 % | 49 % | 38 % |
| prep | 876 | 40 % | 46 % | 32 % |
| church | 519 | 39 % | 52 % | 22 % |
| cake | 183 | 38 % | 38 % | – |
| first_dance | 263 | 37 % | 49 % | 24 % |
| formals | 178 | 35 % | 54 % | 25 % |
| party | 376 | 30 % | 31 % | 29 % |
| reception_line | 652 | 27 % | 41 % | 7 % |
| arrival | 400 | 11 % | – | 17 % |

Near-identical neighbours (≤ 2 s, similarity ≥ 0.93): 980 pairs, both kept 176 (18 %), one
rejected 689, both rejected 115. Bursts keep about half of their frames whatever their size
(2: 52 %, 3–4: 53 %, 5+: 57 %); 55 pairs and 6 bursts of 3–4 lose every frame. Frames in no
burst: 24 % rejected.

## Reasons

Codebook version 2. 1,291 rejects coded, one reviewer each.

| Code | Rejects | Main / second / decor / guests |
|---|---|---|
| SAME | 380 | 318 / 37 / 22 / 3 |
| EXPR | 273 | 175 / 67 / 31 / 0 |
| EYES | 143 | 106 / 33 / 4 / 0 |
| COMP | 132 | 76 / 43 / 13 / 0 |
| FACE | 95 | 52 / 26 / 17 / 0 |
| MOMENT | 67 | 46 / 15 / 6 / 0 |
| VERSION | 52 | 26 / 10 / 13 / 3 |
| UNCLEAR | 44 | 26 / 14 / 4 / 0 |
| NOCOUPLE | 43 | 22 / 14 / 7 / 0 |
| EXPO | 27 | 21 / 6 / 0 / 0 |
| DETAIL | 20 | 6 / 4 / 8 / 2 |
| FOCUS | 9 | 4 / 3 / 2 / 0 |
| CREW | 6 | 6 / 0 / 0 / 0 |

Merged groups for comparing with Glamur (codebook 1): thinning `SAME+VERSION` 432 (33 %; Glamur
`DUP+CROP` 504, 52 %), faces `EYES+EXPR+FACE` 511 (40 %; Glamur `EYES+EXPR` 132, 14 %). The shift
is mostly the codebook: v1 `DUP` was known to hide worse twins.

Trust, from the second reviewer (129 rejects, every tenth per camera in time order, blind):

- Same primary code in 78 of 129 (60 %), Cohen's kappa 0.52. On the merged groups 69 %, kappa
  0.55. The primary of one reviewer is the primary or secondary of the other in 78 %.
- `SAME` holds best (32 of 37). `EXPR` 15 of 29, `FACE` 9 of 17, `EYES` 7 of 12, `COMP` 3 of 9,
  `NOCOUPLE` 2 of 6, `UNCLEAR` 0 of 2. Most frequent confusions: `FACE`↔`COMP`, `EXPR`↔`EYES`,
  `EXPR`↔`SAME`. So "thinning or a face reason" is fairly reliable; which face code is not.
- `loss`: both said `no` on 99 and `maybe` on 9; they differ on 21 (`no`/`maybe`). The one `yes`
  in the sample (`DAVN1767`) was `maybe` for the second reviewer.
- Confidence: high 370, medium 782, low 139.

## Findings

- **FAE-F01** The editor culls in Photo Mechanic and marks rejects with colour class 1
  ("Winner") before moving them to `obrisano`. 20 kept frames carry class 2 ("Winner alt") and
  98 more kept frames were touched in the program without a class.
  evidence: file · XMP `photomechanic:ColorClass="1"` in 1,291 of 1,291 rejects (`posle-analiza/xmp.json`)
  bears on: Q16 · holds elsewhere: GLA-F01 yes
- **FAE-F02** Technical faults are almost absent among the rejects.
  evidence: judged · `FOCUS` + `EXPO` = 36 of 1,291 (3 %)
  bears on: B2, B3 · holds elsewhere: GLA-F02 yes
- **FAE-F03** The editor culls each camera alone: the second photographer's frame is not rejected
  more often when the main camera shot the same seconds.
  evidence: measured · `cross_camera.second`: rejected 20.5 % when the main camera shot within
  3 s, 25.2 % when not
  bears on: S5 · holds elsewhere: GLA-F03 yes
- **FAE-F04** The main photographer loses almost half, the second photographer and the decor
  camera under a quarter. The main camera loses about half in the church, the formals, the civil
  ceremony and the first dance.
  evidence: measured · `by_role` main 45 %, second 23 %, decor 22 %, guests 6 %;
  `by_role_day_part` main: formals 54 %, church 52 %, first_dance 49 %, civil 49 %
  bears on: S3 · holds elsewhere: GLA-F04 no (Glamur: main 31 %, second 35 %)
- **FAE-F05** A reject is relative to a twin.
  evidence: measured · 1,091 of 1,291 rejects (85 %) have a kept frame of similarity ≥ 0.8 in
  the same camera within 60 s (`scripts/twins.py`)
  bears on: K2, B1, B4 · holds elsewhere: GLA-F05 yes (77 %)
- **FAE-F06** She keeps both of two near-identical frames less often than the Glamur editor.
  evidence: measured · `near_identical_pairs.both_kept_share` 0.18
  bears on: K2, W3, C2 · holds elsewhere: GLA-F06 weaker (0.267)
- **FAE-F07** Burst-thinning rules still drop almost as many frames she kept as frames she
  rejected.
  evidence: measured · `rules.burst_keep_first`: 454 of 980 drops she kept (46 %), catches 41 %
  of her rejects; `burst_keep_half`: 43 %, catches 34 %
  bears on: K2, K7, C3 · holds elsewhere: GLA-F07 yes (51 %, catches 25 %)
- **FAE-F08** In a pair shot 0.2–0.3 s apart the first frame is her default; the second stays
  when the first has a blink or another flaw.
  evidence: measured · first frame is hers in 221 of 351 single-keep bursts (63 %), last in 112;
  pairs: first kept 213, second kept 107 (`scripts/twins.py`); judged · reviewers of parts 5–8
  independently, e.g. `NIK_1781`→`1782`, `NIK_2058`→`2059`
  bears on: W2, W3 · holds elsewhere: GLA-F15 same share (62 %), read there as "no rule"
- **FAE-F09** The kept twin is sometimes the worse one: her choice is not always a quality
  judgement, so her cull is not a clean ground truth for "which frame of a pair".
  evidence: judged · main agent at preview size: kept `NIK_1608`, `NIK_1662` (a guest's eyes
  closed), `NIK_1708`, `NIK_1738` (groom's eye half shut) against clean rejected twins
  `NIK_1609`, `1663`, `1707`, `1737`; kept `DAVN1496` (fist blocks the foreground) against
  `DAVN1497`. Reviewers name more, not checked: `DAVN1222`, `DAVN1741`, `DAVN2474`, `NIK_1557`,
  `NIK_1660`, `NIK_0918`
  bears on: B1, W2, K2 · holds elsewhere: GLA no data (not looked for)
- **FAE-F10** Faces decide most rejects that are not plain thinning, and in posed groups anyone's
  blink or mid-word mouth decides, not only the couple's.
  evidence: judged · `EYES+EXPR+FACE` 511 of 1,291; four reviewers on formals and the flower
  wall (`NIK_1371`, `1411`, `1441`, `DAVN1281`, `DAVN1289`)
  bears on: B1, B4, N2, W1 · holds elsewhere: GLA-F09 yes (couple's faces)
- **FAE-F11** A videographer or his gear in the frame is rejected when a clean twin exists, but
  is not a reason by itself.
  evidence: judged · `CREW` 6 primary, 6 secondary; kept `NIK_2151` shows the video rig over the
  right third like its rejected twin `NIK_2150` (main agent at preview size); kept `NIK_0854`,
  `JAS_4795` per reviewers
  bears on: N1 · holds elsewhere: GLA-F10 no
- **FAE-F12** Something blocking in the foreground (the priest's robe or back, a guest's head, the
  registrar's arm, a blurred shoulder) is a reason to reject when a cleaner frame exists.
  evidence: judged · 132 `COMP`; `NIK_0635`–`0637`, `NIK_0851`/`0852`, `NIK_1296`–`1299`,
  `DAVN2318`; agreement on `COMP` is poor (3 of 9)
  bears on: N1, R6 · holds elsewhere: GLA-F11 yes
- **FAE-F13** Frames with the couple are rejected more often than frames without.
  evidence: measured · `couple_in_frame`: 49 % with both, 37 % with one, 20 % with neither
  bears on: K4 · holds elsewhere: GLA-F12 yes
- **FAE-F14** Posed groups get one frame per framing: one vertical and one horizontal, or one
  full-length and one tight, per group of people. Posed couple portraits get two per pose.
  evidence: judged · strip notes of parts 1, 5, 6, 7, 8 (`NIK_0911`–`0937`, `DAVN1266`–`1400`,
  `NIK_1795`–`1800`; couple `NIK_1041`–`1043`, `1047`–`1049`); 52 `VERSION`
  bears on: K8, K10, G3, Q1 · holds elsewhere: GLA-F13 partly (there one of crop and wide)
- **FAE-F15** Guests at the arrival and at the hall entrance are almost all kept; guests without
  the couple are cut in the homes and the party.
  evidence: measured · arrival 11 %, guests camera 6 %; judged · 43 `NOCOUPLE`, 29 of them in prep
  bears on: K6, S2 · holds elsewhere: GLA-F14 yes
- **FAE-F16** Whole runs go when the series is weak, also when it is the only view of a moment.
  evidence: measured · 55 pairs and 6 bursts of 3–4 with nothing kept; judged · `NIK_0629`–`0639`
  (frontal candles, faces in shadow), `NIK_1291`–`1299` (witnesses' answers), `NIK_1847`–`1854`
  (wide smoke frames), `JAS_4440`–`4443` (head table)
  bears on: K3, C3 · holds elsewhere: GLA-F11 (`KNEZ3929`/`3930`) one case
- **FAE-F17** The second photographer's tight portraits at the flower wall are nearly all kept
  while the main camera's groups there are halved.
  evidence: measured · `by_role_day_part` reception_line: second 7 % of 233, main 41 % of 368
  bears on: S3, K10 · holds elsewhere: GLA no (second 22 %, main 33 %)

## Losses

Reviewers marked 17 rejects `yes` and 169 `maybe`. The 17, checked against all cameras; 13 opened
by the main agent, the others marked "not opened":

- **The better twin was rejected (5):** `NIK_1609`, `NIK_1663`, `NIK_1707`, `NIK_1737`,
  `DAVN1497` (FAE-F09).
- **Nothing kept shows it (4):** `NIK_0631` (the bride alone with the candle; the groom's
  `NIK_0628` is kept), `NIK_0633` (the couple frontal with candles, faces in shadow; kept frames
  are profiles), `NIK_0597` (the couple posed at the car; kept frames show her getting out),
  `NIK_1297` (a witness answers into the microphone; the registrar's arm blocks a third).
- **Covered by the other camera (2):** `NIK_0712` by `DAVN1761` (tying the hands), `DAVN1560` by
  `NIK_0499`/`0501` (the couple at the bride's door).
- **Covered only by a wide frame, taste (2):** `DAVN1767` (bound hands; `NIK_0714` wide),
  `NIK_1344` (tight first kiss; `NIK_1345`/`1347` wide with the parents).
- **Not opened (4):** guest candids `DAVN1945`, `JAS_4637`, `JAS_4839` (no similar kept frame
  within a minute); `JAS_4443` (head table; `DAVN1780`/`1796` are similar at 0.85).

The 169 `maybe` were not looked at.

## Questions for the agency

1. `NIK_1608`/`1609`, `1662`/`1663`, `1707`/`1708`, `1737`/`1738`: the kept frame has closed or
   half-closed eyes and the rejected one is clean. A slip, or a reason we do not see? (FAE-F09)
2. Of two frames 0.3 s apart, is the first kept by habit when both look fine? (FAE-F08)
3. The frontal candle series `NIK_0629`–`0639` and the bride alone `NIK_0631`: rejected for the
   dark faces? Would a recovered version be delivered? (FAE-F16, B6)
4. The witnesses' answers `NIK_1291`–`1299`: is the moment not needed, or only these frames bad?
5. A videographer in the frame: when does the frame stay? (FAE-F11)
6. The main photographer loses 45 % here and 31 % on Glamur, the second 23 % against 35 %. The
   photographer, the editor, or the day? Who was the editor? (FAE-F04)
7. "Winner alt" on 20 kept frames: what does it mean? (FAE-F01)

## Limits

- One editor, not named; reasons are inferred, not asked.
- Agreement between two reviewers is moderate (60 %, kappa 0.52). The split between thinning and
  face reasons can be trusted more than a single code.
- Reviewers of parts 1, 2, 5, 6, 7 and 8 judged from their own montages of the previews (about
  440 to 1,000 px per frame) with zooms where needed, not from every 1,536 px preview. Small
  blinks in wide frames are under-detected, so `SAME` is an upper bound. How parts 3 and 4
  looked is not recorded.
- The share of `SAME` differs a lot between reviewers (part 2: 8 of 167; part 7: 85 of 154).
  Part of it is content (guest candids against posed pairs), part is the reviewer.
- 154 rejects have no `kept_alt`; `JAS_4646` names a rejected frame as its `kept_alt`.
- Reviewers saw one camera's strip; other cameras were checked only for the 17 `yes` losses.
- Clocks of JAS_ and MIL_ are not checked; parts of the day are approximate, and the couple's
  minute alone in the church (15:07–15:09) counts as formals.

## Reproduce

`posle-analiza/scripts/merge.py` writes `<out>/analysis/reasons.jsonl` from
`review/part*.result.jsonl`; then `cull.py analysis --output "<out>" --wedding docs\weddings\faena`.
Agreement: `scripts/agreement.py`. Twin coverage and first-frame counts: `scripts/twins.py`.
Coverage of the `yes` losses: `scripts/losses.py`. The scripts need pandas (system Python).
