# Peđa's choices against the signals the pipeline has (2026-11-23)

Question: can the two numbers the pipeline already has — DINOv2 similarity and how many frames were
shot around a pair — explain when Peđa keeps one frame and when both, and where he cuts a group?
What he said for each photo is in the
[photo-by-photo record](../interviews/2026-11-19-pedja-slika-po-slika.md); the rules are in
[requirements.md](../requirements.md).

Method: cosine similarity of the cached embeddings (`embeddings.npz`), capture-time gap, number of
photos of the folder within 60 s before the first and after the last frame, group in the current
`groups.json`. Small sample: 20 pairs, 23 groups, 4 clicks. The agent also looked at every pair
and group as a contact sheet; what is visible is noted in the record under **[slika]**.

## Disputed pairs

| # | Pair | Answer | Similarity | Gap s | Frames ±60 s | Our grouping | Orientation |
|---|---|---|---|---|---|---|---|
| M1 | 9971 / 9973 | both | 0.915 | 29.4 | 8 | same group | V V |
| M2 | 9872 / 9873 | both | 0.951 | 1.2 | 7 | same | V V |
| M3 | 9877 / 9878 | one | 0.955 | 0.6 | 5 | same | H H |
| M4 | 9862 / 9863 | one | 0.840 | 0.7 | 12 | same | V V |
| M5 | 9930 / 9931 | both | 0.865 | 3.8 | 7 | same | H V |
| M6 | 8404 / 8405 | one | 0.924 | 29.9 | 4 | same | V V |
| M7 | 8412 / 8413 | – ("nothing", too dark) | 0.966 | 0.7 | 11 | same | V V |
| M8 | 9309 / 9310 | both | 0.934 | 0.9 | 28 | same | V V |
| M9 | 8144 / 8145 | one | 0.708 | 7.4 | 10 | same | V V (B&W / colour) |
| M10 | 8637 / 8638 | both | 0.860 | 2.4 | 9 | same | V H |
| M11 | 9078 / 9079 | both | 0.927 | 29.4 | 4 | same | V V |
| M12 | 9425 / 9426 | – ("different, both") | 0.917 | 0.8 | 20 | same | V V |
| M13 | 9440 / 9443 | one | 0.959 | 2.9 | 21 | same | V V |
| M14 | 9037 / 9038 | both | 0.805 | 0.6 | 18 | same | V V (flash / no flash) |
| M15 | 9410 / 9411 | one | 0.923 | 2.0 | 15 | same | V H |
| M16 | 9659 / 9662 | different | 0.908 | 33.9 | 16 | same | V V |
| M17 | 0600 / 0601 | both (said: different moment) | 0.905 | 1.3 | 40 | same | V V |
| M18 | 0395 / 0396 | one | 0.873 | 6.0 | 7 | same | H H |
| M19 | 0197 / 0198 | both | 0.727 | 7.3 | 11 | split | H H |
| M20 | 0417 / 0418 | one | 0.705 | 2.9 | 17 | split | H V |

- "One": similarity 0.705–0.959, frames around 4–21.
- "Both": similarity 0.727–0.951, frames around 4–40.
- The current grouping holds 18 of the 20 pairs in one group, among them M16, M12 and M17, which
  he called different.

## Best-photo groups (Talići 4a)

| # | Frames | Picked | Lowest similarity in the group | Span s | Frames ±60 s |
|---|---|---|---|---|---|
| P1 | 9843, 9844 | 1 of 2 | 0.953 | 5 | 6 |
| P2 | 9852–9856 | 3 of 5 | 0.917 | 3 | 13 |
| P3 | 0033, 0034 | 2 of 2 | 0.917 | 5 | 7 |
| P4 | 9794, 9795 | 1 of 2 | 0.917 | 15 | 11 |
| P5 | 9904, 9906, 9907 | 1 of 3 | 0.860 | 16 | 12 |
| P6 | 9806–9811, 9820–9823 | 4 of 10 | 0.733 | 28 | 20 |
| P7 | 0026–0029 | 4 of 4 | 0.772 | 6 | 23 |
| P8 | 9916, 9917 | 1 of 2 | 0.903 | 7 | 10 |
| P9 | 9928, 9929 | 2 of 2 | 0.949 | 8 | 9 |
| P10 | 0011, 0012 | 2 of 2 | 0.911 | 1 | 24 |
| P11 | 9923–9925 | 3 of 3 | 0.854 | 18 | 10 |
| P12 | 9908, 9909 | 1 of 2 | 0.909 | 10 | 13 |
| P13 | 0063–0079 (8) | 8 of 8 | 0.729 | 130 | 25 |
| P14 | 9983, 9985 | 2 of 2 | 0.923 | 3 | 8 |
| P15 | 0139, 0140 | 2 of 2 | 0.910 | 0 | 33 |
| P16 | 9953, 9954 | 1 of 2 | 0.913 | 6 | 8 |
| P17 | 0095–0097 | 3 of 3 | 0.842 | 7 | 13 |
| P18 | 0174, 0175 | 2 of 2 (one would do) | 0.938 | 6 | 9 |
| P19 | 9970, 9971, 9973 | 3 of 3 | 0.817 | 32 | 8 |
| P20 | 0177–0180 | 2 of 4 | 0.855 | 11 | 10 |
| P21 | 0124–0132 (9) | 9 of 9 | 0.708 | 4 | 28 |
| P22 | 0154, 0156 | 1 of 2 | 0.920 | 24 | 9 |
| P23 | 0155, 0164 | 1 of 2 | 0.941 | 93 | 17 |

- Two-frame groups where he kept one: 0.903–0.953. Where he kept both: 0.910–0.949.

## His clicks and comments on our groups

| Folder | Frames | What he did | Similarity | Gap s |
|---|---|---|---|---|
| 4a | 9815 / 9817 | cut | 0.820 | 2.1 |
| Talići 1 | 8020 / 8029 | cut (look-back join) | 0.727 | 117.0 |
| Talići 1 | 8028 / 8032 | cut (look-back join) | 0.782 | 74.7 |
| 4a | 9847 + 9848 | joined | 0.651 | 9.5 |
| 4a | 9785 / 9786 | said: same group | 0.804 | 3.2 |
| 4a | 9787 / 9788 / 9789 / 9796 | said: group is good | 0.908, 0.852, 0.859 | 2.9, 9.6, 59.4 |

Frames of one burst where the flash did not fire (Talići 1, the group of 11 he treated as one):
8040 / 8041 0.844 at 1.1 s, 8043 / 8044 0.771 at 1.2 s.

## Findings

1. **Similarity does not tell "one" from "both".** The two ranges overlap completely, for the pairs
   and for the two-frame groups. Neither does the number of frames shot around the pair.
2. **What he gave as reasons is content:** who is in the frame (couple, closest family, guest),
   how important the moment is, a defect on one frame. None of these is a pipeline signal yet.
3. **A higher similarity threshold alone does not give his groups.** Confirmed-same pairs are at
   0.80–0.91 and cut pairs at 0.73–0.82. Pairs he calls the same picture go down to 0.65–0.71
   (horizontal against vertical, black-and-white against colour, details of one object), and a
   flash that did not fire costs up to 0.2 of similarity inside one burst.
4. **Two of three cuts are look-back joins** over 75 and 117 s, where the pose changed in between.
   The third is at 2 s, where orientation, framing and pose all change. Shortening or tightening
   the look-back for photos with people is the first candidate to measure.
5. **Reading his "same moment, both" clicks as "same group" is unsafe** (M17, and M12 without a
   click): [requirements Q7](../requirements.md#open-questions).

## Limits

- One wedding, one person, a handful of cuts. Nothing here is a threshold recommendation.
- The pairs were chosen from metadata as hard cases; they are not a sample of the wedding.
- `picks.agency.json`: the entry of the nine-frame group (P21) carries a save time of 2026-11-23
  (the page was opened again); the selection equals the one reported on 2026-11-19.

## Reproduce

Similarities: cosine of the vectors in `<out>/embeddings.npz` for the sha256 of the two frames in
`<out>/photos.json`. Pairs and groups: `data/meeting/meeting.json`, `data/meeting/picks_sample.json`,
`data/meeting/meeting_answers.json`, `data/out-4a/picks.agency.json`.
