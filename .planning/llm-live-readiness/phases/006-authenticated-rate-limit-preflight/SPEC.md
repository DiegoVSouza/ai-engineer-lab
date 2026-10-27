# Phase 006 — Authenticated rate-limit preflight

Status: PLANNED. The provider transport currently authenticates the model catalog before dispatch but discards rate-limit headers from that response. The user's requirement that smaller authenticated limits win therefore needs an explicit guard integration before P00 generation.

## Contract

- Perform the existing GET catalog preflight using only unique `GROQ_API_KEY_1..4` entries from the lab-root `.env`; never return or hash credential material.
- Keep model access checks and the fixed `openai/gpt-oss-20b` model. Do not generate completions as part of preflight.
- Sanitize only the documented numeric rate-limit/reset headers. Across the four keys, use the most restrictive observed request/token ceilings and remaining capacity because they share one organization quota. Never let authenticated headers raise the published policy maxima.
- Apply authenticated request/day and token/minute ceilings, remaining requests/tokens and reset windows to the shared guard before any reservation. The same guard applies after process restart using the newly authenticated preflight; normal completion headers remain durable history.
- Missing daily-token, tier or authenticated rate-limit data stays explicitly UNKNOWN/PENDING. Rate-limit headers do not establish billing tier or daily token balance.
- Catalog/preflight failure blocks all model dispatch. No fallback, retries, ledger resets or policy changes.

## Non-goals

No policy-budget change, provider completion, campaign allocation, model change, key rotation, new dependency, project-source import, or modification of provider/account histories. Paid spend remains USD 0.
