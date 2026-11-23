# Talici: gaps in the camera's file numbers (2026-11-19)

Question: are the five Talici folders everything the camera shot, or was something deleted before
the agency handed them over? Method: file names only (`_KADnnnn.NEF`), all photos of the five
folders sorted by capture time; a step larger than 1 between neighbours counts as missing files.

## Result

- One camera (SN6501320). The numbers run without a break through both days, from `_KAD7969` to
  `_KAD1018` (the counter wraps at 9999). No large jump, no photo in two folders: the five folders
  are consecutive slices of one sequence.
- At least 3,050 frames shot, 2,575 present, 475 missing (16 %).

| Folder | Time | Numbers | Present | Missing | Missing % | Longest run without a gap |
|---|---|---|---|---|---|---|
| Talici 1 | 31.8. 10:52–20:33 | 7969–8789 | 711 | 110 | 13 % | 79 |
| Talici 2 | 31.8. 20:35 – 1.9. 10:55 | 8790–8996 | 174 | 33 | 16 % | 28 |
| Talici 3 | 1.9. 10:58–15:07 | 8999–9783 | 661 | 124 | 16 % | 54 |
| talici 4a | 1.9. 15:08–17:58 | 9784–0183 | 334 | 66 | 16 % | 31 |
| talici 4 | 1.9. 18:04–23:44 | 0184–1018 | 695 | 140 | 17 % | 44 |

- The gaps are small and spread over the whole day: 345 places; 1 file missing 257 times, 2 files
  60 times, 3 files 16 times, 4–5 files 12 times. Per hour 5–8 % on the first morning, otherwise
  12–24 %, 37 % in the last hour (46 frames).
- NEF headers of 4a (334 files): every rating is 0, no colour label, the only tool named is the
  camera firmware, no sidecar files. The other four folders were not checked this way.
- The per-photo check of the 27B on 124 photos of 4a found `focus: sharp` and `exposure: ok` on all
  124 ([research](2026-11-14-ranking-full-model-and-per-photo.md)).

## Reading

- No folder is untouched and none is more culled than the others: all five are in the same state.
- The pattern is single bad frames removed, not a selection; series of similar frames are still
  there (79 of 150 groups in 4a have two or more photos).
- So the pipeline has never seen the plainly bad frames (blur, missed focus, test shots), which is
  the agency's first priority.

## Not known

- Who deleted and when (in the camera or afterwards). Not asked at the 2026-11-19 meeting.
- 3,050 is a lower bound: frames deleted before the first or after the last present file do not
  show, and video clips use the same counter.
- How many photos Peđa delivered: the folder with the edited JPEGs is not on this machine.
