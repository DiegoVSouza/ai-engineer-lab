# Free-only campaign authorization

## Additional credential topology attestation — 2026-10-28

The user explicitly authorized GROQ_API_KEY in addition to GROQ_API_KEY_1..4 and stated that the credentials belong to different organizations. Slot 0 identifies the unnumbered variable. This does not authorize additional campaign calls or paid use; the existing explicit Free attestation covered numbered keys only, so unnumbered-key billing eligibility remains unverified. Retry authorization permits bounded same-key read-only metadata retries, not rotation around quota or replay of uncertain model work.

On 2026-10-26 the user requested implementation of the remaining readiness work and limited quota/ceilings to Groq's free plan. The user will perform human review once technical preparation/results are ready. This supersedes earlier absence of authorization to conduct a free-tier campaign; it does not turn pending human review into approval or authorize paid use.

- Authorized paid spend: USD 0, with no upgrade, billing changes, alternate model/provider or silent fallback.
- Account/model rate ceilings: published free-plan maxima, reduced by any smaller authenticated limits or available capacity. Keys share account limits. Stop and checkpoint on exhaustion; resume later without resetting cumulative campaign usage.
- Scope: synthetic local evaluation, development fixes/regressions, local service integration and review preparation. Preserve the original 390-case target and three trials per case, original output caps, sealed split protocol and finite reservations.
- Human/dataset/rubric/candidate review: PENDING. Results generated before review are provisional; no promotion/generalization claim can pass until applicable review is complete. A reviewer-directed expectation/prompt correction after examining holdout consumes that holdout and requires fresh confirmation.
- Public deployment, customer data, external messages, real refunds, push and paid usage remain outside this authorization.

Policy evidence: [Groq rate limits](https://console.groq.com/docs/rate-limits), [model/pricing reference](https://console.groq.com/docs/models). Published rate ceilings are not proof of account tier, remaining quota or zero economic value of inference. Billed cost stays unknown without billing evidence; the user-designated free plan has no authorized paid charges.

## Explicit budget amendment — 2026-10-27

Authorization ID: `p00-free-envelope-plus10-v1`. After receiving the exact deficit and concrete proposal, the user replied: “Autorizar esse envelope adicional, somente gratuito, mediante fase de migração validada”. This authorizes only ten additional P00 calls / 20,480 input tokens / 2,560 output tokens / USD 0.002304 economic estimate. P00 calls become 186→196 and global calls 4,074→4,084 through phase 005's validated migration. Paid authorization remains USD 0; no upgrade, provider/model fallback, free-rate/per-call/trial increase, other-project reduction or implicit correction/judge/canary funding is authorized.

Registry UUIDs, provider/logical histories, receipts and unknown reservations must survive the migration. Confirmation remains protected. Budget approval is not human/dataset/rubric/independent review or promotion approval; those remain PENDING. The historical P00 campaigns remain immutable, and a fresh candidate must be planned, validated, committed and frozen separately before any generation.

## User correction: distinct accounts — 2026-10-27

The user states that the configured credentials belong to different accounts and asks to continue. Treat account topology as user-supplied distinct accounts, superseding the earlier blanket single-account assumption. This does not increase campaign allocations or authorize paid usage. Phase 017 records required identity and quota migration; existing aggregate accounting and unknown historical reservations remain authoritative until validated migration. Account billing verification and pending human reviews are separate requirements.

## Free account attestation — 2026-10-27

After clarifying that keys belong to distinct accounts, the user answered the per-variable Free-tier question with: todas free. This is recorded as user attestation covering authorized GROQ_API_KEY_1..4, not API-verified billing or organization identity. Controlled funded development may proceed under conservative existing aggregate ceilings; no per-account capacity multiplication, policy reset, paid usage, fallback or uncertain replay is authorized. Human review remains deferred/PENDING. The metadata API still does not expose billing or daily token balances.
