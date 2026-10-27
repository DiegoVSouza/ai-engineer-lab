# Phase 006 — Authenticated rate-limit preflight

Status: IMPLEMENTED; OFFLINE PASS; ACCOUNT LIMIT PROOF INCOMPLETE. The provider transport authenticated the model catalog before dispatch but discarded rate-limit headers from that response. This phase adds their sanitized enforcement to the shared guard. Authenticated model access later passed for 4/4 unique root credentials, but no rate-limit headers were returned. Billing tier and exact daily token remainder remain unknown; generation stays blocked at paid authorization USD 0.

## Contract

- Perform the existing GET catalog preflight using only unique `GROQ_API_KEY_1..4` entries from the lab-root `.env`; never return or hash credential material.
- Keep model access checks and the fixed `openai/gpt-oss-20b` model. Do not generate completions as part of preflight.
- Sanitize only the documented numeric rate-limit/reset headers. Across the four keys, use the most restrictive observed request/token ceilings and remaining capacity because they share one organization quota. Never let authenticated headers raise the published policy maxima.
- Apply authenticated request/day and token/minute ceilings, remaining requests/tokens and reset windows to the shared guard before any reservation. The same guard applies after process restart using the newly authenticated preflight; normal completion headers remain durable history.
- Missing daily-token, tier or authenticated rate-limit data stays explicitly UNKNOWN/PENDING. Rate-limit headers do not establish billing tier or daily token balance.
- Catalog/preflight failure blocks all model dispatch. No fallback, retries, ledger resets or policy changes.

## Non-goals

No policy-budget change, provider completion, campaign allocation, model change, key rotation, new dependency, project-source import, or modification of provider/account histories. Paid spend remains USD 0.

## Official limit contract checked on 2026-10-27

Groq's [rate-limit documentation](https://console.groq.com/docs/rate-limits) says these limits apply at organization level and documents `x-ratelimit-limit-requests` and `x-ratelimit-remaining-requests` as RPD, `x-ratelimit-limit-tokens` and `x-ratelimit-remaining-tokens` as TPM, their corresponding reset headers, and `retry-after` in seconds. The same page says exact limits are account-specific; its published Free table lists `openai/gpt-oss-20b` at 30 RPM / 1,000 RPD / 8,000 TPM / 200,000 TPD. These public values do not verify this account's tier or its remaining daily tokens. Only authenticated response headers constrain the existing shared guard, and they can only lower the configured ceilings.
