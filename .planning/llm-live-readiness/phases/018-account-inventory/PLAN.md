# Plan

1. Implement an offline inventory command emitting only approved variable names, nonsecret aliases and pending identity/billing fields.
2. Validate deterministic offline output and record commands, exits and output; review staged diff and commit.

allowed_write_paths:
- scripts/harness/account_inventory.py
- .planning/llm-live-readiness/phases/018-account-inventory/**
- artifacts/evidence/llm-live-readiness/account-inventory/**
forbidden_changes: secrets, ledgers, transport, policy, datasets, candidate sources, project repositories.
llm_mode: offline; no network or provider completions; paid budget USD 0.
validation_command: python -S scripts/harness/account_inventory.py
stop_condition: identity/billing cannot be established offline; preserve dependent generation as INCOMPLETE.
Plan-check: PASS, self-check only; two tasks with bounded paths and zero external effects. Human/independent approval PENDING.
