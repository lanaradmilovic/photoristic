# 0018 — Own vLLM server first, swappable client, no framework

- Status: accepted
- Date: 2026-10-16
- Decided by: the user

## Context
Photos show guests' faces; the agency has not approved sending them to a cloud provider. A
comparison with a commercial model is wanted later.

## Options considered
1. **Cloud VLM API** — no infrastructure, but images leave the user's control.
2. **Qwen3.5-9B on the user's vLLM** (EC2 g6.xlarge, L4 24 GB, Frankfurt), via SSH tunnel.
3. **An agent/LLM framework** for clients.

## Decision
Option 2, behind a small client class per provider with one method (`OpenAICompatibleClient`, later
`BedrockClient`), chosen by `vlm.provider` in config. No framework; stdlib `urllib`.
Claude Haiku 5.5 on Bedrock only after the agency approves (phase 6).

## Consequences
The instance runs only during sessions, so every VLM step must resume. Steps 1–2 never need it.

## Evidence
[plan.md](../plan.md#fixed-constraints), [research/2026-10-19-vlm-context-budget.md](../research/2026-10-19-vlm-context-budget.md).
