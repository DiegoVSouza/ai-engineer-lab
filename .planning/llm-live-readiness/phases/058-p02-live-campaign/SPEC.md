# Phase 058: P02 development campaign guard

## Goal
Let the root free-account guard approve provider attempts of one P02 campaign, `p02-dev-v1`, without loosening any other allocation. P02 keeps its policy total (310 requests); today the `p02` branch of `scripts/harness/live_free_account.py` admits only `local-operation-v1` and at most 4 attempts.

## Authority
Owner reply 2026-11-09 (verbatim): "pode usar os modelos da groq tem as env ai documentada" and "faz a 1 mesmo". Free Groq keys, model `openai/gpt-oss-20b`, `authorized_paid_spend_usd` 0.00, owner total-loss cap USD 5.00, shared free window 200,000 tokens per day and 8,000 per minute. Third-party IdP and device FPS stay on hold. Independent review is `WAIVED_BY_OWNER` (owner approval, never independent verification).

## Behaviour
- Campaign `p02-dev-v1` is admitted only if `AUTHORIZATION.json` is tracked, unmodified against HEAD and equals the expected content (id `p02-live-campaign-058-v1`, project p02, `max_attempts` 24, `trials_per_case` 1, `policy_requests` 310, paid 0.00, holdout and confirmation unfunded).
- At most 24 attempts of that campaign (24 development cases, one provider call each). A non-ok completed attempt in it blocks further attempts (`prior_operational_failure_requires_review`), as for the other operations.
- `local-operation-v1` keeps its 4-attempt cap and its failure rule. Any other campaign name stays `protected_p02_allocation`.
- No change to the p00, p01, p03, p04 or p05 branches, to the policy file, to per-call caps, pricing or the model.
