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
| 01.09.Talici 1 | 711 | couple session (boat, old town, single frames 5–40 s apart, mostly B&W) + start of party | `21-10-2026-v1` | over-splits the couple session |
| 01.09. Talici 2 | 174 | evening party + groom prep details | `21-10-2026-talici2` | good; exposure jumps break DINOv2 (cufflinks 0.61) |
| Talici 3 | 661 | groom, bride prep, family formals, couple at car/pier, church (burst style, median gap 3.9 s) | `21-10-2026-talici3` | good |
| talici 4 | 695 | garden party, speeches, first dance, cake, dancing | `21-10-2026-talici4` | candids mostly legit singles; dancing couple split 3–4 ways |
| talici 4a | 334 | church + outdoor ceremony | `data/out-4a` | reference for wrong-merge counterexamples; **labelled** (333 pairs) |

Regenerate: `.venv\Scripts\python cull.py prepare --input "<folder>" --output "<out>"`
(~2 min for 4a, ~8–10 min per 700 photos on CPU). Re-group only: `cull.py group --output <out>`.
Use `.venv\Scripts\python.exe`; the system Python has no `rawpy`.
