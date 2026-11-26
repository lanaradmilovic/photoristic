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

| Claim | GLA | Bears on |
|---|---|---|
| Rejects are relative to a twin, not absolute quality ([GLA-F05](glamur/analysis.md#findings)) | yes | K2, B1 |
| Burst thinning drops more frames the agency kept than rejected ([GLA-F07](glamur/analysis.md#findings)) | yes | K2, K7 |
| The editor culls each camera alone ([GLA-F03](glamur/analysis.md#findings)) | yes | S5 |
| Crew in the frame is always rejected ([GLA-F10](glamur/analysis.md#findings)) | yes | N1 |
| A head or arm at the edge is a reason to reject when a cleaner twin exists, against N1 ([GLA-F11](glamur/analysis.md#findings)) | yes | N1, R6 |
