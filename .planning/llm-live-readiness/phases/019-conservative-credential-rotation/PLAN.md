# Plan

1. Add a deterministic credential selector driven by durable reserved-attempt count and test rotation across sessions and provider errors.
2. Run offline account/transport regressions, save command/exit/output and inspect staged changes before commit.

allowed_write_paths:
- scripts/harness/live_provider_transport.py
- scripts/harness/test_live_provider_transport.py
- .planning/llm-live-readiness/phases/019-conservative-credential-rotation/**
- artifacts/evidence/llm-live-readiness/credential-rotation/**
forbidden_changes: ledgers, policy, budgets, credentials, historical campaigns, project files, dataset/rubric, provider requests.
llm_mode: fake fixtures only; paid USD 0; zero provider calls.
validation_command: python -S -m unittest discover -s scripts/harness -p test_live_provider_transport.py -v
stop_condition: regression failure or unknown billing; dependent generation remains INCOMPLETE.
Plan-check: PASS (self-check); two tasks, concrete paths, no inferred account capacity. Separate-account optimization remains INCOMPLETE.

Coordination follow-up allowed_write_paths: .planning/llm-live-readiness/STATUS.md and this phase VERIFY.md, to reference owning P00 phase 021 without duplicating authoritative ledgers.
