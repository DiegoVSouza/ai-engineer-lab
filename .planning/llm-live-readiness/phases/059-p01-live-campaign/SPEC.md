# Phase 059: P01 development campaign guard

## Goal
Let the root free-account guard approve provider attempts of one P01 campaign, `p01-dev-v1`, without loosening any other allocation. P01 keeps its policy total (1000 requests). Today, with `p01.requests == 1000`, the only admitted P01 scope is the single reviewed revalidation workflow (`_reviewed_revalidation`): any other campaign name is refused with `reviewed_revalidation_scope_required`.

## Authority
Owner reply 2026-11-09 (verbatim): "pode usar os modelos da groq tem as env ai documentada" and "faz a 1 mesmo". Free Groq keys, model `openai/gpt-oss-20b`, `authorized_paid_spend_usd` 0.00, owner total-loss cap USD 5.00, shared free window 200,000 tokens per day and 8,000 per minute. Third-party IdP and device FPS stay on hold. Independent review is `WAIVED_BY_OWNER` (owner approval, never independent verification).

## Behaviour
- Campaign `p01-dev-v1` is admitted only if `AUTHORIZATION.json` is tracked, unmodified against HEAD and equals the expected content (id `p01-live-campaign-059-v1`, project p01, `max_attempts` 76, `trials_per_case` 1, `policy_requests` 1000, paid 0.00, holdout and confirmation unfunded).
- `max_attempts` is 76: 18 development cases x 1 trial x 4 provider calls = 72, plus a margin of 4 for nothing but accounting slack. It is a ceiling, not a target; the P01 logical ledger reserves exactly 4 calls per trial.
- A non-ok completed attempt in that campaign blocks further attempts (`prior_operational_failure_requires_review`).
- While that campaign is admitted, the reviewed-revalidation scope check is skipped only for that campaign name. Every other campaign name still goes through `_reviewed_revalidation` and is refused.
- No change to the p00, p02, p03, p04 or p05 branches, to the p01 992/996 diagnostics branch, to the policy file, to per-call caps, pricing or the model.
