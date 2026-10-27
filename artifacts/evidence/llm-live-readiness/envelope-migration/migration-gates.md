# Migration implementation gates

All commands ran offline. None loaded credentials or contacted a provider.

| Check | Command | Exit | Result |
| --- | --- | ---: | --- |
| Migration regressions | `python -S -m unittest discover -s scripts/harness -p test_migrate_free_envelope.py -v` | 0 | 14 passed; includes no-write dry-run, exact delta, both Git roots, UUID/history continuity, unknown reservation, all apply crash windows, append-only audit, rollback denial, linked paths, missing ledger, lease contention, idempotency and later registration. |
| Shared account guard | `python -S -m unittest discover -s scripts/harness -p test_live_free_account.py -v` | 0 | 21 passed, including pending-marker dispatch denial. |
| Shared provider transport | `python -S -m unittest discover -s scripts/harness -p test_live_provider_transport.py -v` | 0 | 15 passed. |
| Migration lint | `projects/p00/.venv/Scripts/ruff.exe check scripts/harness/migrate_free_envelope.py scripts/harness/test_migrate_free_envelope.py` | 0 | All checks passed. |
| Migration format | `projects/p00/.venv/Scripts/ruff.exe format --check scripts/harness/migrate_free_envelope.py scripts/harness/test_migrate_free_envelope.py` | 0 | Both files formatted. |
| P00 locked gate | `uv run --locked python scripts/check_full.py` from `projects/p00` | 0 | Fast, lint, format, compile, 142 tests, dataset contract and Compose config passed. Optional service E2E remains INCOMPLETE. Existing detailed owned evidence: `projects/p00/artifacts/evidence/private-review-ui/check-full.txt`. |
| P01 locked gate | `uv run --locked --group frameworks python scripts/check_full.py` from `projects/p01` | 0 | 60 tests, six synthetic runner comparison slots, demo and source/lock checks passed. Live execution remains disabled and quality metrics PENDING. |

An initial migration test exposed transient SQLite WAL `-wal` and `-shm` files during read-only inspection. The migration now holds the P00 campaign lease and then the shared account lease, tracks auxiliary files after acquiring both, closes read connections and removes only auxiliary files created by this inspection. The dry-run regression confirms the fixture file set and bytes remain identical. Fourteen migration regressions pass after these fixes.

A crash-window review found that the shared account guard needed an explicit durable stop between registry replacement and applied-audit commit. The helper now writes a fixed pending marker after its prepared audit, the ordinary shared account guard refuses while it exists, and migration-only read inspection verifies history before appending `applied` and removing the marker. Regressions cover crashes before registry replacement, after replacement, and after `applied` but before marker removal. P00's separate source repository is pinned to the reviewed lock-bearing blob and must be clean and committed.

Plan review was performed by the implementing agent only. No independent review or human/dataset/rubric approval is claimed. The real policy file contains the exact authorized delta; the real account registry and ledgers have not yet been migrated. Apply remains gated on committed sources and successful production dry-run/reconciliation.


An earlier P00 gate capture against the amended shared cap failed one stale assertion that still expected the original primary limit of 126 calls. Phase 019 updated the assertion and campaign scope; the rerun above is the current full gate and passed 142 tests. The earlier output is retained in P00 phase evidence as history, not treated as a pass.
