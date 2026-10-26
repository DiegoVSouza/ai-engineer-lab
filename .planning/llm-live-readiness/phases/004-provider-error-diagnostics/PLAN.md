# Plan

- allowed_write_paths: `.planning/llm-live-readiness/phases/004-provider-error-diagnostics/**`, `scripts/harness/live_provider_transport.py`, `scripts/harness/test_live_provider_transport.py`, `artifacts/evidence/llm-live-readiness/provider-diagnostics/**`.
- llm_mode: fake; simulated HTTP only. No provider, production accounting writes, product source/artifact edits, quota changes, Docker or public effects.
- Validation: explicit error-code/body-redaction tests and all prior transport/account tests, lint/format/compile; capture commands/exits.
- Stop condition: diagnosis would require raw persistent content or replaying an actual failed semantic trial. Preserve the historical unknown cause.

1. Add categorical HTTP/code extraction and stable classifications, retaining only allowlisted codes and fixed labels.
2. Test JSON-generation/tool/schema/auth/quota/transient/unknown paths, no retry and no error-body content leakage.
3. Save offline evidence and remaining owning-project binding requirements; review staged diff and commit locally.

Plan review: accepted. This corrects measured diagnostic loss, preserves prior evidence and does not change prompts, graders, accounting caps, retry policy or model output limits. No new generation in this phase; independent verification remains pending.
