# 0019 — Safety rules are applied in code, never left to the model

- Status: accepted (to be implemented in phase 3)
- Date: 2026-10-19
- Decided by: the user (follows from the hard rule)

## Context
The hard rule is "never lose a good photo". A VLM can be wrong, overconfident or return invalid JSON.

## Decision
After every VLM answer, code enforces:
- each multi-photo group keeps at least one `keep`;
- low-confidence rejects become `maybe`;
- singletons are not auto-rejected (at most `maybe`) until phase 5 proves it safe;
- photos flagged in steps 1–2 always go to review;
- an invalid answer sends the whole group to review.

A later learned model (phase 7) may only move photos *into* review or keep.

## Evidence
[spec/vlm-scoring.md](../spec/vlm-scoring.md#safety-rules-in-code-after-the-answer).
