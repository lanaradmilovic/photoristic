# How the program sees two pairs that Peđa judged differently (2026-11-24)

Question from the user: on the question page, pair A (the couple at the altar) looks almost
identical to the eye and pair B (leaving the church) differs by a whole step of the couple. What
does the program see? Context: [requirements Q2](../requirements.md#open-questions), record items
P1 and M2 of the [photo-by-photo record](../interviews/2026-11-19-pedja-slika-po-slika.md).

## Numbers (Talići 4a, current `groups.json`, `ranking.json`, `identities.json`)

| | A: `_KAD9843` / `_KAD9844` | B: `_KAD9872` / `_KAD9873` |
|---|---|---|
| Peđa | one is enough ("very similar") | both ("not quite the same", important moment) |
| What differs to the eye | the best man in the background, the groom's gaze | the couple's step, the bride's hand |
| Capture gap | 5.1 s | 1.2 s |
| DINOv2 similarity | 0.953 | 0.951 |
| Same group | yes | yes |
| Known faces, face count | A, B, E, F / 4 on both frames | A, B / 5 and A, B, P / 5 |
| Variant ([0022](../decisions/0022-variants-in-code-model-ranks.md)) | one variant of two frames | two variants of one frame |
| The program would keep | one | both |

## What it means

1. **For the similarity signal the two pairs are the same.** 0.953 against 0.951. The embedding
   is one vector for the whole frame, made from a 224 px copy; it describes the scene. In B the
   couple is a small part of a frame that is mostly the church wall, so a different step changes
   almost nothing in it.
2. **The program gets Peđa's result for B, for the wrong reason.** The two frames of B are separate
   variants because one bystander at the door was recognised (identity P) on the second frame and
   not on the first; a known person present on one side and absent on the other splits a variant.
   Nothing in the program looked at the couple's step.
3. **So "exactly the same" (requirements `K2`) has no signal yet.** A pair like B without a
   bystander would be one variant and lose a frame to `maybe`; a pair like A with a face that
   flickers between frames would keep both. Both errors are cheap by the hard rule (nothing is
   rejected), but the count of kept frames follows chance.

## The couple only (measured the same day)

Method: person boxes from RT-DETR v2 on the 1536 px preview; for every main person (the two or
three most frequent identities of the folder that are recognised on both frames) the smallest box
that holds the face in its upper part; the union of those boxes plus 5 %; the crop resized to
224 x 224 and embedded with the same DINOv2-small. "Crop" is the cosine of the pooled vectors,
"patches" the mean cosine of the 256 patch tokens at the same grid position, "person" the lowest
crop similarity of the single persons. The crops of A and B were checked by eye.

| Pair | Peđa | Whole frame | Crop | Patches | Person | Main people found | Crop, share of frame |
|---|---|---|---|---|---|---|---|
| **A** P1 altar | one | 0.953 | 0.974 | 0.880 | 0.935 | both | 57 % / 57 % |
| **B** M2 church exit | both | 0.951 | 0.929 | 0.648 | 0.883 | both | 8 % / 13 % |
| M6 bride, old town | one | 0.924 | 0.773 | 0.561 | 0.773 | one | 5 % / 9 % |
| M13 couple, pier | one | 0.959 | 0.875 | 0.656 | 0.875 | one of two | 39 % / 30 % |
| M15 pier, vertical / horizontal | one | 0.923 | 0.819 | 0.422 | 0.827 | both | 16 % / 28 % |
| M9 groom, B&W / colour | one | 0.708 | 0.787 | 0.566 | 0.787 | one | 61 % / 63 % |
| M3 group photo | one (groom looks away) | 0.955 | 0.892 | 0.526 | 0.728 | three | 40 % / 46 % |
| M4 hug | one (groom looks bad) | 0.840 | 0.788 | 0.620 | 0.788 | one | 84 % / 81 % |
| M5 tables, horizontal / vertical | both | 0.865 | 0.892 | 0.654 | 0.814 | both | 8 % / 22 % |
| P3 led in by her brother | both | 0.917 | 0.877 | 0.486 | 0.877 | one | 6 % / 12 % |
| P9 bride at the tables | both | 0.949 | 0.895 | 0.846 | 0.895 | one | 30 % / 29 % |
| P10 groom's entrance | both | 0.911 | 0.856 | 0.609 | 0.877 | two | 23 % / 31 % |
| P15 couple, ribbon | both | 0.910 | 0.832 | 0.623 | 0.832 | one of two | 11 % / 14 % |
| M8 first meeting | both | 0.934 | 0.945 | 0.662 | 0.945 | one of two | 18 % / 26 % |
| M11 groom waits | both | 0.927 | 0.869 | 0.541 | 0.869 | one | 24 % / 17 % |
| M12 pier, kiss / look | both ("different") | 0.917 | 0.900 | 0.359 | 0.900 | one of two | 18 % / 33 % |
| M14 groom, flash / none | both | 0.805 | 0.849 | 0.621 | 0.849 | one | 49 % / 68 % |
| M16 church | different | 0.908 | 0.784 | 0.523 | 0.784 | one of two | 12 % / 24 % |
| M17 first dance | both ("different") | 0.905 | 0.767 | 0.426 | 0.756 | two | 23 % / 13 % |
| M7 dark alley | – (too dark) | 0.966 | 0.809 | 0.717 | 0.809 | one of two | 9 % / 8 % |

1. **For A and B the crop sees what the eye sees.** A becomes more alike (0.953 → 0.974, patches
   0.88), B less (0.951 → 0.929, patches 0.65). The couple fills 57 % of the frame in A and about
   a tenth in B, which is why the whole frame could not show the step.
2. **It does not separate Peđa's "one" from "both" in general.** "One" pairs: crop 0.77–0.97,
   patches 0.42–0.88. "Both" pairs: crop 0.77–0.95, patches 0.36–0.85. P9 (kept both, "a bride
   wants all her photos") is as identical as A; M6 and M13 (one, "very similar") score like the
   pairs he kept both of. His answer follows who is in the frame and how important the moment is,
   as in the [first measurement](2026-11-23-meeting-choices-vs-signals.md).
3. **Where the crop itself fails:** a change of orientation (M15: the patch grid no longer lines
   up), black-and-white against colour (M9), flash against none (M14), and pairs where only one of
   the couple is recognised on both frames, so the crop is one person (M13, M12, M8, P15).
4. **What it is good for:** a narrow test for requirements `K2`, "nothing differs on the main
   people", inside a burst of one orientation and one exposure. Not a rule for one or both, and
   no threshold from twenty hand-picked pairs.

## Reproduce

Cosine of the vectors in `data/out-4a/embeddings.npz`; `photo_signatures(load_identities(out), 10)`
and `identity_relation(a, b, partial_blocks=True)` for the faces; the variants are in
`data/out-4a/ranking.json`. The crop measurement was a one-off script, not in the repository: face
boxes and identity labels from `faces.npz` and `identities.json` (same order per photo), person
boxes from `PekingU/rtdetr_v2_r18vd` at score 0.6, embeddings as in `culling/embed.py`.
