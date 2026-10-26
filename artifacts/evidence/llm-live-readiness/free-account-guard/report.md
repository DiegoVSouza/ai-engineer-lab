# Free-account guard foundation

Offline foundation: PASS. Full campaign/promotion: INCOMPLETE.

`python -S scripts/harness/test_live_free_account.py -v`: exit 0, 20 tests passed. Coverage includes project/campaign switches, cumulative request/input/output/economic caps, minute/day windows, stricter provider feedback, unknown usage, quota cooldown, immutable attempts, missing/replaced ledgers, concurrency and cross-process lease death/recovery. Synthetic test mistakes are preserved separately; expected safety assertions were not weakened.

`python -S scripts/harness/live_free_account.py`: exit 0 for credential-free inventory; generation remains unauthorized by this foundation CLI and account/provider unknowns remain explicit.

`python -S scripts/harness/live_free_account.py --catalog-preflight`: exit 0, target `openai/gpt-oss-20b` accessible for all four deduplicated numbered credentials. Only GET metadata requests were made, no generation. Initial incomplete metadata response is preserved; adding explicit application/Accept headers and aggregate failure categories produced a successful preflight. No raw headers, credential identities/values/hashes or provider content were saved.

The [policy](../../../../shared/policies/groq-free-campaign.json) records finite campaign/project maxima from the existing additive call reservations and unchanged per-call token caps. These include pilot, primary and fresh confirmation capacity, with promotion/canary still gated separately. The economic estimate ceiling is a conservative token-price valuation, not paid authorization or a bill. Authorized paid spend is USD 0. The user's free-plan attestation does not establish billing status through the API; billing and remaining daily tokens remain unknown.

References were checked on 2026-10-26: [official rate limits](https://console.groq.com/docs/rate-limits) and [official pricing/model reference](https://console.groq.com/docs/models). Enforce whichever account/model limit is tighter, and checkpoint on exhaustion. Request headers expose remaining daily requests and remaining minute tokens; the latter must never be labeled remaining daily tokens.

Human review is deferred at the user's request and remains PENDING. No production project usage databases were initialized; no Docker service changed. Next phase: bounded provider transport and per-project launcher binding under the common guard, preserving candidate/split provenance and review requirements.
