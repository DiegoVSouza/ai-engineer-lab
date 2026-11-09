# Phase 057: P05 development campaign guard

## Goal
Let the root free-account guard approve provider attempts of one P05 campaign, `p05-dev-v1`, without loosening any other allocation. P05 keeps its policy total (1712 requests); today the `service_operations` branch of `scripts/harness/live_free_account.py` only admits `local-operation-v1` (8 attempts). This is a code-guard change tied to a committed, unmodified `AUTHORIZATION.json`, not a policy-total change.

## Authority
Owner reply 2026-11-09 (verbatim): "pode usar os modelos da groq tem as env ai documentada" and "faz a 1 mesmo". Free Groq keys, model `openai/gpt-oss-20b`, `authorized_paid_spend_usd` 0.00, owner total-loss cap USD 5.00, shared free window (200,000 tokens/day, 8,000 tokens/minute). Independent review `WAIVED_BY_OWNER`. Holdout and confirmation not funded. Third-party IdP and device FPS on hold.

## Behaviour
- Campaign `p05-dev-v1` is admitted only if `AUTHORIZATION.json` is tracked, unmodified against HEAD and equals the expected content (id `p05-live-campaign-057-v1`, project p05, `max_attempts` 64, `trials_per_case` 1, `policy_requests` 1712).
- At most 64 attempts of that campaign; a non-ok completed attempt in it blocks further attempts (`prior_operational_failure_requires_review`), as for the other operations.
- `local-operation-v1` keeps its 8-attempt cap and its failure rule; any other campaign name stays `protected_p05_allocation`.
- No change to p00, p01, p02, p03, p04 branches, to the policy file, to per-call caps, pricing or the model.
