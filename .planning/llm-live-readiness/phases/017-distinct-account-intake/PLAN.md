# Plan

1. Record the corrected user-supplied account topology and inspect the existing single-account transport.
2. Define migration prerequisites and preserve aggregate funding, UUIDs, receipts and unknown reservations.

allowed_write_paths:
- .planning/llm-live-readiness/phases/017-distinct-account-intake/SPEC.md
- .planning/llm-live-readiness/phases/017-distinct-account-intake/PLAN.md
- .planning/llm-live-readiness/phases/017-distinct-account-intake/VERIFY.md
- .planning/llm-live-readiness/AUTHORIZATION.md

forbidden_changes: runtime, policies, ledgers, historical campaigns, secrets, project repositories, Docker stacks.
llm_mode: offline; zero provider calls and USD 0 paid.
validation_command: git diff --check
stop_condition: account identity or Free billing evidence is unavailable; leave dependent dispatch INCOMPLETE.

Plan-check: PASS (self-check only). Two documentation tasks, explicit paths, no budget expansion or runtime mutation. Runtime migration requires its own executable SDD phase before edits.
