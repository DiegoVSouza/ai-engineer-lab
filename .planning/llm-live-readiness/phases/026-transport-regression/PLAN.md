# Plan

1. Reproduce response-boundary defects with injected responses and record the baseline.
2. Correct bounded metadata reads and completion error-response cleanup, deny metadata redirects, stop catalog traversal on 429 and block completion-session initialization when unnumbered credential Free eligibility is unresolved. Run locked root regressions and owning consumer gates.
3. Record transport audit findings and maintain the finite coordination work table.

allowed_write_paths:
- scripts/harness/live_free_account.py
- scripts/harness/live_provider_transport.py
- scripts/harness/test_live_free_account.py
- scripts/harness/test_live_provider_transport.py
- .planning/llm-live-readiness/phases/026-transport-regression/**
- .planning/llm-live-readiness/WORK.md
- artifacts/evidence/llm-live-readiness/transport-regression-026/**

forbidden_changes: credentials, policies, budgets, live ledgers, historical manifests/results, provider access, retrying completions, sibling product sources, Docker lifecycle.

Plan-check: implementer self-assessment; independent verification pending. LLM_MODE=fake. max_tries: 3 per failure, persisted in evidence. Stop affected work on exhausted corrections or external prerequisites; continue independent tasks. Source changes invalidate historical candidate continuity.
