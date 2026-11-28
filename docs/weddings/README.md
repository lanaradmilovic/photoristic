# Weddings before and after the agency's cull

One folder per wedding that the agency gave us twice: as the photographers handed it over and
after their editor's cull. Each analysis has the same shape
([spec](../spec/wedding-analysis.md)), uses the same reason codes ([codebook](codebook.md)) and
states every finding as a numbered claim with its evidence. These analyses are the ground truth
for "what the agency keeps": requirements ([requirements.md](../requirements.md)) and the
selection step are checked against them.

## Weddings

| Id | Date | Cameras | Before | Rejected | Editor | Codebook | Status | Files |
|---|---|---|---|---|---|---|---|---|
| GLA | 2026-11-08 | 4 | 3,432 | 962 (28 %) | Ksenija, Photo Mechanic | 1 | draft | [glamur/](glamur/analysis.md) |
| FAE | 2026-10-03 | 4 | 3,822 | 1,291 (34 %) | unknown, Photo Mechanic | 2 | draft | [faena/](faena/analysis.md) |

## Adding a wedding

1. `cull.py agency --input <pre> --after <posle> --output <out>` (prepare and the agency's cull).
2. Write `docs/weddings/<id>/wedding.json`: camera roles and clocks, parts of the day (from the
   group sheets or the reviewers' strip notes), the couple's identities from `faces_sheets/`.
3. Reviewers code every reject into `<out>/analysis/reasons.jsonl` with the current
   [codebook](codebook.md), a second reviewer about 10 % of them.
4. `cull.py analysis --output <out> --wedding docs/weddings/<id>`.
5. Write `analysis.md` from the template in the spec; claims get the next free ids.
6. Compare (below) and add a row to the table above.

## Comparing (for an agent)

Read in this order, and stop as soon as the question is answered:

1. This file and every `analysis.md` front matter: which weddings, which codebook, how checked.
2. Every `summary.json`: the same keys, so one table per key across weddings. Rates are of
   `kept` + `rejected` only. When the codebook versions differ, compare reasons on the merged
   groups the codebook names.
3. The claims (`XXX-Fnn`) of every `analysis.md`: for each claim of one wedding, does the other
   wedding's summary or photos.csv confirm it, contradict it, or have no data? Write the answer
   into the claim's `holds elsewhere` and into the table below.
4. Only then `photos.csv` (in the output folders, see each `wedding.json` `data`), for a number
   no summary has. Load it with pandas; never open the photos for a comparison unless a claim
   is about what a photo shows.

Report claims that hold on every wedding separately from those seen once. A claim with evidence
`judged` on both weddings is still a judgement. Never change a wedding's claim text; add.

## Claims across weddings

Compared 2026-11-28. Reasons were coded with codebook 1 on Glamur and 2 on Faena, so reasons
compare only on the merged groups.

| Claim | GLA | FAE | Bears on |
|---|---|---|---|
| Rejects are relative to a twin, not absolute quality ([GLA-F05](glamur/analysis.md#findings), [FAE-F05](faena/analysis.md#findings)) | yes (77 %) | yes (85 %) | K2, B1 |
| Burst thinning drops about as many frames the agency kept as rejected ([GLA-F07](glamur/analysis.md#findings), [FAE-F07](faena/analysis.md#findings)) | yes (51 % of drops) | yes (46 %) | K2, K7 |
| The editor culls each camera alone ([GLA-F03](glamur/analysis.md#findings), [FAE-F03](faena/analysis.md#findings)) | yes | yes | S5 |
| Rejects carry Photo Mechanic colour class 1 ([GLA-F01](glamur/analysis.md#findings), [FAE-F01](faena/analysis.md#findings)) | yes (949 of 962) | yes (all) | Q16 |
| Technical faults are about 3 % of the rejects ([GLA-F02](glamur/analysis.md#findings), [FAE-F02](faena/analysis.md#findings)) | yes | yes | B2, B3 |
| Frames with the couple are rejected more often ([GLA-F12](glamur/analysis.md#findings), [FAE-F13](faena/analysis.md#findings)) | yes | yes | K4 |
| Frames in no burst: 24 % rejected (`lone_frames`) | 24.1 % | 24.1 % | K1 |
| The first frame of a single-keep burst is the kept one in about 62 % ([GLA-F15](glamur/analysis.md#findings), [FAE-F08](faena/analysis.md#findings)) | 62 % | 63 % | W2, W3 |
| Guests at the arrival are almost all kept ([GLA-F14](glamur/analysis.md#findings), [FAE-F15](faena/analysis.md#findings)) | yes (12 %) | yes (11 %) | K6, S2 |
| A head, arm or robe in the foreground is a reason to reject when a cleaner twin exists, against N1 ([GLA-F11](glamur/analysis.md#findings), [FAE-F12](faena/analysis.md#findings)) | yes | yes | N1, R6 |
| Crew in the frame is always rejected ([GLA-F10](glamur/analysis.md#findings), [FAE-F11](faena/analysis.md#findings)) | yes | **no** | N1 |
| Both of two near-identical frames are often kept ([GLA-F06](glamur/analysis.md#findings), [FAE-F06](faena/analysis.md#findings)) | 27 % | weaker, 18 % | K2, C2 |
| Main and second photographer lose about the same ([GLA-F04](glamur/analysis.md#findings), [FAE-F04](faena/analysis.md#findings)) | yes (31 % / 35 %) | **no** (45 % / 23 %) | S3 |
| The kept twin is sometimes the worse one ([FAE-F09](faena/analysis.md#findings)) | no data | yes (5 pairs seen) | B1, W2 |
