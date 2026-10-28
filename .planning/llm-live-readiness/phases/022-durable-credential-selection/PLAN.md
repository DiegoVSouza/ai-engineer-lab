# Plan

1. Add injected offline regressions for atomic reservation/slot binding, concurrent selection, crash and restart, immutable history, and no secret or hash persistence.
2. Implement deterministic numbered-slot binding within the existing reservation transaction and use that exact slot for the one HTTP request; preserve existing API behavior for non-provider callers.
3. Run account and transport tests in the locked P00 environment, record sanitized output and inspect explicit staged paths. Preserve production ledgers and historical attribution; do not run a provider.

allowed_write_paths: `.planning/llm-live-readiness/phases/022-durable-credential-selection/**`, `scripts/harness/live_free_account.py`, `scripts/harness/live_provider_transport.py`, `scripts/harness/test_live_free_account.py`, `scripts/harness/test_live_provider_transport.py`, `artifacts/evidence/llm-live-readiness/durable-credential-selection-022/**`. forbidden_changes: actual ledgers and registry, policy, secret values/hashes, historical campaign results, other project sources, provider access, allocations, holdout, fallback and approvals.

Fake mode; USD 0 and zero provider calls. Stop on ambiguity about historical ledger compatibility, uncontrolled credential configuration, test failures or uncertain accounting. Source changes alter P00 fingerprint and cannot resume historical C2. Replacement 36 plus holdout 84 needs 120 calls against 107 primary remaining: deficit 13; 60 confirmation calls protected. Plan-check is self-assessment, independent review PENDING.
