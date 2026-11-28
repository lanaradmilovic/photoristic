# Test datasets

All test data is outside git (`data/` is ignored). One wedding ("talici", one Nikon D5,
2026-08-31/09-01) split into five folders. These five are the regression set: a grouping change
is checked at least on **Talici 1 (over-splitting) and 4a (wrong merges)**, ideally on all five.

- Source: `<OneDrive>/Documents/Documents/photoristicxtajna/talici/talici/`
- Outputs: `<OneDrive>/Documents/Documents/photoristicxtajna/output/<output>/`
- 4a is also extracted locally to `data/talici/talici 4a/` with output `data/out-4a/`.
- The user's review notes (`faces_ocena.txt`, `segments_ocena.txt`, before/after sheets) are in
  the same `output/` folder.

| Folder | Photos | Content | Output | Behaviour |
|---|---|---|---|---|
| 01.09.Talici 1 | 711 | couple session (boat, old town, single frames 5–40 s apart, mostly B&W) + start of party | `21-10-2026-v1` | over-splits the couple session; **labelled** for rule 0025 (710 pairs, 392 by the agent, [research](research/2026-11-25-labels-v3-and-signal-ceiling.md)) |
| 01.09. Talici 2 | 174 | evening party + groom prep details | `21-10-2026-talici2` | good; exposure jumps break DINOv2 (cufflinks 0.61) |
| Talici 3 | 661 | groom, bride prep, family formals, couple at car/pier, church (burst style, median gap 3.9 s) | `21-10-2026-talici3` | good |
| talici 4 | 695 | garden party, speeches, first dance, cake, dancing | `21-10-2026-talici4` | candids mostly legit singles; dancing couple split 3–4 ways |
| talici 4a | 334 | church + outdoor ceremony | `data/out-4a` | reference for wrong-merge counterexamples; **labelled** for rule 0025 (333 pairs) |

Regenerate: `.venv\Scripts\python cull.py prepare --input "<folder>" --output "<out>"`
(~2 min for 4a, ~8–10 min per 700 photos on CPU). Re-group only: `cull.py group --output <out>`.
Use `.venv\Scripts\python.exe`; the system Python has no `rawpy`.

## Glamur

One wedding, 8 Nov 2026, four cameras, JPG only, 3,432 photos. Not part of the regression set;
measured once without tuning ([research](research/2026-11-26-glamur-grouping.md)).

- Source: `<OneDrive>/Documents/Documents/photoristicxtajna/svadbe/1-glamur/pre/08.11. Glamur/` (moved
  there 2026-11-26; `photos.json` still names the old path `photoristicxtajna/08.11. Glamur/`) (folders 01–29,
  `POSLEDNJA KARTICA`, `Luka mejl` are card dumps; `00 Nove Montaze` holds Photoshop montages).
- Output: `<OneDrive>/Documents/Documents/photoristicxtajna/output/2026-11-26-glamur/`
- Regenerate (80 min on CPU):
  `.venv\Scripts\python cull.py prepare --input "<source>" --output "<out>" --exclude "00 Nove Montaze"`
- Cameras by file prefix: `KNEZ` Canon R5 II (1,852), `LPZ_` Nikon Z6 III (874), `JAS_` Nikon D750
  (539), `VAL` Canon R6 II (167). Their clocks differ: LPZ is 298 s ahead of KNEZ, JAS 68 s
  behind; VAL unknown.
- **Labelled** by the agent for rule 0025: 1,904 pairs (all 1,704 of 2–40 s, 100 sampled under
  2 s, 100 over 40 s), 141 of them `unsure`. Score 1,561 of 1,763. The user's check of 120 pairs
  is `review/` in the output folder.
- **The agency's cull** is `svadbe/1-glamur/posle/08.11. Glamur/`: kept photos in `1` (KNEZ), `2`
  (LPZ), `3` (JAS, VAL), rejects in `obrisano`, marked in Photo Mechanic
  ([research](research/2026-11-26-glamur-cull.md)). Analysis and report: `posle-analiza/` in the output folder;
  in the fixed format: [weddings/glamur](weddings/glamur/analysis.md), rows in `analysis/photos.csv`.
- Also in the output folder: `labelling/` (sheets, protocol, answers), `group_sheets/`, `clocks/`,
  `cross_camera/`, `scripts/`.

## Faena

Wedding of 2026-10-03, four cameras (NIK_ main, DAVN second, JAS_ decor, MIL_ guests), JPG only,
given before and after the agency's cull. Not labelled, grouping not scored.

- Source: `<OneDrive>/Documents/Documents/photoristicxtajna/svadbe/2-faena/03.10. Faena/pre` (3,822 JPG);
  the agency's cull in `posle/03.10. Faena` (folders `1`, `2`, `3` kept, `obrisano` rejected).
- Output: `<OneDrive>/Documents/Documents/photoristicxtajna/output/2026-11-27-faena/`; rows in
  `analysis/photos.csv`, reasons in `analysis/reasons.jsonl`, reviewers' material and scripts in
  `posle-analiza/`.
- Analysis: [weddings/faena](weddings/faena/analysis.md).
