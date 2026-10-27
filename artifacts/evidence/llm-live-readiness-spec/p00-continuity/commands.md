# P00 continuity handoff validation

Command from the lab root: `python -S artifacts/evidence/llm-live-readiness-spec/p00-continuity/validate.py`.

Exit code: 0. Complete output: `validation.json`. Local links resolve; the handoff agrees with the owning P00 reconciliation, committed-source rejection probe and actual local private-review probe. No product source is imported and no provider or credential is accessed. This documentation check does not approve allocation, quality, human review or promotion.

The lab staged diff is limited to `STATUS.md` and this evidence directory. Product files remain exclusively in the P00 Git. Existing unrelated lab paths and project temporary output are preserved. No root policy/runtime, shared kit, provider registry, service or campaign record changed.
