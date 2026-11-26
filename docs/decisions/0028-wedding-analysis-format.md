# 0028 — Every before/after wedding gets the same analysis: rows, summary, numbered claims

- Status: accepted
- Date: 2026-11-27
- Decided by: the user, after review

## Context
The agency now gives weddings twice, before and after their editor's cull. Each pair is the
ground truth for "what the agency keeps", and Claude agents will compare the weddings to define
requirements and the selection step. The first analysis (Glamur, 2026-11-26) was one HTML page
plus ad-hoc JSON: facts, measurements, reviewers' judgements and proposals mixed in prose;
tables by camera name and by hour of one camera's clock, which no other wedding has; reason
codes defined only in the reviewers' brief, and `DUP` already drifting (3 of 8 were a worse
twin).

## Options considered
1. **One report page per wedding, as for Glamur** — good for the user, but an agent cannot tell
   evidence from opinion, and nothing lines up across weddings.
2. **Fixed shape per wedding** — `photos.csv` (one row per photo, same columns), `summary.json`
   (same keys), `analysis.md` (front matter and numbered claims with their evidence), one
   versioned codebook; the HTML page is generated from them.
3. **A database of all weddings** — more than needed for a handful of weddings; no frameworks.

## Decision
Option 2. It follows practice for error analysis (fixed taxonomy, counts), qualitative coding
(codebook with definitions, when to use and not, examples, agreement of two coders) and
documents read by agents (small summary first, details on demand, evidence marked). Roles
(main, second, decor, guests) and parts of the day replace camera names and hours so weddings
line up. Claims carry ids so a comparison can say per claim where it holds.

## Consequences
- New command `cull.py analysis`; config section `analysis` (burst 2 s / 0.93, cross-camera 3 s)
  must stay fixed, or every summary is regenerated.
- A new rule or summary key goes into `culling/analysis.py` and all summaries are rerun.
- Codebook version 2 (`SAME`, `FACE`, `VERSION`) is for the next wedding; Glamur stays on v1.
- Reviews need a second reviewer on about 10 % of the rejects.

## Evidence
[spec](../spec/wedding-analysis.md), [codebook](../weddings/codebook.md),
[Glamur analysis](../weddings/glamur/analysis.md), [research](../research/2026-11-26-glamur-cull.md).
