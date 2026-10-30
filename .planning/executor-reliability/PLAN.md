# Plan

1. Add project-local high reasoning effort and a streaming, read-only JSONL diagnostic that exports only allowlisted metadata and counts.
2. Verify malformed/truncated records, phase classification, model switches and content exclusion; save evidence and commit the implementation.

allowed_write_paths: `.codex/config.toml`, `scripts/harness/audit_codex_rollout.py`, `scripts/harness/test_audit_codex_rollout.py`, `.planning/executor-reliability/**`, `artifacts/evidence/executor-reliability/**`.

forbidden_changes: user-level Codex config, runtime binaries, provider calls, project sources/ledgers, live counters, permissions, automatic continuation hooks, other pending files.

Validation: Python unittest offline; TOML parse; diagnostic against an explicitly selected local rollout. max_tries: 3 total for this new offline diagnostic only. This does not authorize any llm-live-readiness gate. Paid/provider use: zero. Stop on credential exposure or unclear path ownership.

Plan-check: implementer self-assessment PASS; this is root tooling, not a harness-kit change. Local logs cannot establish API wire behavior. No independent review claimed.
