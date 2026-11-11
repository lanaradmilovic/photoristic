# 0001 — NEF and JPG with the same name are one photo

- Status: accepted
- Date: 2026-10-16
- Decided by: agent, approved by the user

## Context
Photographers shoot RAW+JPG. Both files of a pair are the same moment; counting them twice would
double the review and break grouping.

## Options considered
1. **Treat each file as a photo** — simple, but every moment appears twice.
2. **Pair by stem within one folder** — one record with `nef_path` and `jpg_path`.

## Decision
Option 2. The preview comes from the JPG (fallback: the NEF's embedded JPEG); metadata from the NEF
first; the primary file (hash, id) is the NEF if present. XMP sidecars will go next to the NEF.

## Consequences
Pairing is by stem *in the same folder*: a JPG exported elsewhere is a separate photo.

## Evidence
[spec/ingest.md](../spec/ingest.md).
