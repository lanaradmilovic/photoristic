# Can the pipeline tell a recoverable dark or bright frame from a lost one? (2026-11-26)

Question: Peđa's rule ([B3](../requirements.md#what-makes-a-frame-bad)) is in pixel values:
highlights at 250–255 and blacks at 0–5 are lost, everything else can be pulled back (a lot from
RAW, a little from JPG). Can we measure that per photo, with tools we already have, and use it to
decide "passes culling" / "mark as dark" / "lost"?

Scripts were one-off (scratchpad, not in the repo): numpy over the preview, `rawpy` over the NEF.
No new dependency.

## What was measured

Per photo, on the preview (the JPG the camera embeds in the NEF, or the JPG itself):

- `blown`: share of pixels with any channel ≥ 250;
- `crushed`: share of pixels with every channel ≤ 5;
- `mean`: mean brightness 0–255.

Per NEF, on the raw sensor data (`rawpy.raw_image_visible`, black and white level from the file):

- `raw_sat`: share of pixels at the sensor's white level, i.e. really lost highlights;
- `raw_p50`, `raw_p99`: median and 99th percentile of the linear signal (0–1);
- `stops_to_mid`: how many stops the median is below middle grey (how much it must be brightened);
- `headroom`: how many stops the frame can be brightened before its brightest 1 % clips.

## Talići (NEF), photos Peđa commented on and the extremes of two folders

| Photo | What it is | preview `blown` | preview `crushed` | preview mean | RAW saturated | stops to mid | headroom |
|---|---|---|---|---|---|---|---|
| T1 8412, 8413 | M7: couple in a dark alley, "I would give nothing before I fix it" | 0 % | 3 % | 70 | 0 % | 3.3 | 2.0 |
| T1 8041, 8044, 8046 | X10: the "dark" boat frames (flash did not fire) | 0.5 % | 2–3 % | 123–126 | 0 % | 1.4 | 2.0 |
| T1 8040 | X10: the bright frame next to them | 1.7 % | 0.1 % | 148 | 0 % | 0.7 | 0.9 |
| T3 9038 | M14: groom without flash, "better, only brighten it" | 0.9 % | 18 % | 70 | 0.02 % | 3.6 | 1.6 |
| T1 8625, 8699, 8748 | darkest of Talići 1: night party | 0–0.2 % | 12–35 % | 28–41 | 0–0.15 % | 5.3–5.6 | 3.6–4.8 |
| T3 9762, 9046 | darkest of Talići 3: candles in church, bride in a dark room | 0 % | 16–24 % | 35–55 | 0 % | 4.3–5.0 | 3.5–4.0 |
| T3 9553 | couple at a white door, preview looks white | **72 %** | 0 % | 242 | **4.5 %** | −1.3 | 0 |
| T3 9207 | white tablecloth, preview looks white | **62 %** | 0 % | 240 | **0.9 %** | −1.5 | 0 |
| T3 9385 | sea and sky | **51 %** | 0 % | 203 | **0 %** | −0.1 | 0.7 |
| T1 8386 | bride in front of a white wall | 52 % | 0 % | 220 | **27 %** | −1.2 | 0 |
| T1 8529 | landscape into the sun | 47 % | 0 % | 183 | **40 %** | 0.4 | 0 |

## Findings

1. **On NEF the preview cannot decide "lost highlights".** The embedded preview of these files
   is a strong black-and-white picture style; in it 50–70 % of a frame reads 250–255 although the
   sensor clipped 0–5 % (9553, 9207, 9385). The RAW number separates them from the really lost
   ones (8386: 27 %, 8529: 40 %). Reading the raw data with `rawpy` takes about a second per file.
2. **No dark frame here is lost.** Even the darkest night frames have almost no pixels at the
   sensor's black and 3.5–5 stops of headroom: they can be brightened, as Peđa said. The frames
   he called dark (M7, X10, M14) need 1.4–3.6 stops. So "too dark to judge" is a mark, never a
   reject, on RAW.
3. **The X10 "dark" frames are not dark in the preview** (mean 123–126 against 148 for the frame
   with flash). What Peđa sees as dark is a difference to the neighbouring frame, not a level.
   A rule "mark as dark" must compare with the frames of the same moment, or it misses these.
4. **The share of the whole frame is the wrong unit.** A white sky or wall can be blown without
   harm; a blown face or dress is the loss Peđa means ("a strong flash burns a white dress at
   230"). The number has to be taken inside the people: the pipeline already finds faces and
   people ([faces](../spec/grouping.md)), but does not store the person boxes (`people.json` keeps
   only yes/no).

## Proposal (not decided)

- RAW: `raw_sat` inside the boxes of the main people > a few % → "lost highlights"; median
  more than ~2 stops below middle grey → mark "dark, brighten first" (`B6`); never reject on
  darkness alone.
- JPG (Glamur, restaurant weddings): the JPG is the only data, so Peđa's 0–5 / 250–255 rule applies
  to it directly, again inside the people. A JPG has far less room: brightening by more than about
  one stop shows noise and banding. The thresholds need the agency's examples.
- Blur (`B2`) is a separate number: the variance of the Laplacian (sharpness of edges), again on
  the face or person crop. Not measured here.
- Before any of this becomes a rule: the agency's answer to `tamne` (mark or not) and a set of
  frames they really threw out for exposure (the culled Glamur, if it exists).

## Glamur (JPG)

The same preview numbers on all 3,432 photos (the previews are made from the JPG, so here they are
the real data).

| | 1 % | 5 % | 25 % | median | 75 % | 95 % | 99 % |
|---|---|---|---|---|---|---|---|
| `blown` (share ≥ 250) | 0 | 0 | 0.2 % | 0.8 % | 3 % | 13 % | 25 % |
| `crushed` (share ≤ 5) | 0 | 0 | 0 | 0.1 % | 1.5 % | 17 % | 32 % |
| mean brightness | 29 | 40 | 64 | 85 | 111 | 151 | 173 |

- More than 10 % of the frame blown: 279 photos; more than 10 % crushed: 291. As a reject rule
  that would remove about 1 photo in 6, nearly all of them good.
- **The most blown frames are good photos**: family at a table in front of a bright window
  (JAS_3549 42 %, JAS_3609 39 %), the couple under a tower against the sky (KNEZ4236–4238 37–40 %,
  KNEZ4091). The people are well exposed; the window and the sky are white.
- **The darkest frames are of two kinds**: frames where the people are well lit against a black
  background (guest at the logo wall VAL15074, dancing guest KNEZ5527) and frames where the people
  themselves are dark: the first dance on LPZ_4408–4415 (19:07, mean 9–22, the couple barely
  visible). Only the second kind is a candidate for "too dark", and only the numbers inside the
  people tell them apart.
- So on JPG too the whole-frame share does not work; the same conclusion as finding 4 above.
  Whether the agency would throw out LPZ_4408–4415 or brighten them is a good example to show.
