# Plan — free envelope migration

## Tasks

1. Record the explicit budget authorization, immutable baseline policy, exact arithmetic and all remaining commitments. Review SPEC/PLAN/VERIFY manually with independent review still pending; commit planning before implementation.
2. Add red/green tests and implement a narrow migration helper with read-only dry-run, exact-delta/committed-source checks, shared lease, ledger/UUID/history continuity, append-only audit and atomic/idempotent registry transition. Amend only the approved policy fields.
3. Run locked/standard-library guard, transport and migration regressions, then real locked P00/P01 gates under their owning plans. Save commands/exits/output, inspect staged diff/secrets and commit migration/policy inputs before production metadata mutation.
4. Dry-run and apply the already authorized migration once, verify real identities/events/reservations and all remaining funding, save sanitized evidence and commit the handoff. No provider/key/catalog call occurs here.

allowed_write_paths:
- `.planning/llm-live-readiness/phases/005-free-envelope-migration/**`
- `.planning/llm-live-readiness/AUTHORIZATION.md`
- `.planning/llm-live-readiness/STATUS.md`
- `scripts/harness/migrate_free_envelope.py`
- `scripts/harness/test_migrate_free_envelope.py`
- `shared/policies/groq-free-campaign.json`
- `artifacts/evidence/llm-live-readiness/envelope-migration/**`
- `.runtime/llm-live-readiness/ledger-references.json` (only approved atomic policy-SHA transition, UUIDs preserved)
- `.runtime/llm-live-readiness/policy-migrations.sqlite*` (new append-only migration audit, not usage accounting)
- `.runtime/llm-live-readiness/account.lock` and `.runtime/llm-live-readiness/ledger-references.policy-migration.tmp` (scoped coordination/atomic write)
- `projects/p00/.runtime/llm-live-readiness/campaign.lock` (acquire P00 execution lease before account lease so the logical trial journal cannot change during inspection; preserve any lock metadata)
- `projects/p00/artifacts/evidence/private-review-ui/tmp-envelope-migration-gate/**` (isolated P00 locked-gate scratch directory; owned project evidence only)
- `docs/knowledge/free-envelope-migration.md`

forbidden_changes: all provider/logical usage ledgers, historical campaign artifacts, raw/private answers, credentials, per-call/trial/free-rate/model/pricing/paid limits, other project allocations, kit, product source without its own phase, Docker/services, retries/fallback and external effects.

llm_mode: offline only. Provider/catalog/credential access and paid spend: zero. Only the exact ten-call free envelope is authorized; no additional allocation is inferred.

Validation commands:
- `python -S -m unittest discover -s scripts/harness -p test_live_free_account.py -v`
- `python -S -m unittest discover -s scripts/harness -p test_live_provider_transport.py -v`
- `python -S -m unittest discover -s scripts/harness -p test_migrate_free_envelope.py -v`
- P00: `P00_PYTEST_BASETEMP=artifacts/evidence/private-review-ui/tmp-envelope-migration-gate uv run --locked python scripts/check_full.py` with isolated pytest evidence; retain existing temp trees.
- P01: `uv run --locked --group frameworks python scripts/check_full.py`.
- `python -S scripts/harness/migrate_free_envelope.py --dry-run`, then `--apply` only after valid source/gates/commit.

Stop on registry/UUID/history drift, active reserved work, unregistered usage, unauthorized delta, source dirtiness, unsafe paths, missing audit provenance or lease contention. Never repair by resetting or editing usage history. Independent/human approval remains pending except for the recorded budget authorization itself.
