# Plan — Account-wide campaign dry-run

## Execution controls

- `llm_mode`: `fake`; invoke only project `--dry-run` commands under Python `-S`.
- `allowed_write_paths`:
  - `.planning/llm-live-readiness/phases/001-global-campaign-dryrun/**`
  - `scripts/harness/live_campaign_dryrun.py`
  - `scripts/harness/test_live_campaign_dryrun.py`
  - `artifacts/evidence/llm-live-readiness/global-dry-run/**`
- `forbidden_changes`: project source/artifacts, project `.env`, root `.env`, untracked root user files, campaign configs/datasets/reviews/budgets, provider/network access, SDK construction, Docker/services, public deployment, external effects, or push.
- Budget: USD 0 paid. No Groq request. Account quota/cumulative caps remain `PENDING` and are reported, never inferred.
- Validation: test JSON contract normalization with synthetic inputs; execute the real `--help`-documented `pilot --dry-run` for all projects; save sanitized aggregate output and exits in the allowed evidence folder.
- Stop condition: any invocation uses an undocumented CLI or touches credentials/services; aggregate errors stay `INCOMPLETE`.

## Tasks

1. **Define aggregate report contract** — preserve project distinctions, combine only actual numeric values, and expose missing shared account limits as blockers.
2. **Implement offline coordinator** — invoke each project CLI sequentially with Python `-S`, collect JSON and exits, and reject any output claiming provider access or missing required safety flags.
3. **Validate and report** — unit-test normalization, run all six real dry-runs, capture evidence, inspect only explicitly owned root paths, and commit atomically.

## Plan review

Reviewed against root AGENTS.md, the broad readiness SPEC, and each project's current CLI contract. The coordinator uses subprocess interfaces only, does not create a cross-repository runtime dependency, and cannot dispatch. All writes are within the four paths listed above. Accepted for offline implementation on 2026-10-26; clean-context verifier remains pending.
