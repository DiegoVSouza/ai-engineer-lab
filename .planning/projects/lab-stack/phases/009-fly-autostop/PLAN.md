# Plan

1. Tests first in `scripts/harness/test_fly_ops.py` and new `scripts/harness/test_process_pair.py`.
2. `infra/logging/pair.py` in the P04 and P05 images; `fly/*.toml`, `ops/fly/*.ps1`.
3. Snapshot the database and Redis volumes, run `fly-up`, confirm private apps have no public address, then e2e.
4. Prove machines stop at idle and wake on a request. Document.

allowed_write_paths: `fly/**`, `ops/fly/**`, `scripts/harness/test_fly_ops.py`, `scripts/harness/test_process_pair.py`, `README.md`, `docs/**`, `.planning/**`, `artifacts/evidence/lab-stack/fly-autostop-009/**`, P04 and P05 `infra/logging/**`.

forbidden_changes: a public address on `db`, `redis`, `sns` or `jaeger`, destroying volumes, P04 fingerprinted paths, Compose behaviour, apps outside the inventory.

llm_mode: fake. budget: Fly usage; memory of P04 and P05 machines rises to 512 MB while awake. validation: `python scripts/e2e_fly.py`. rollback: revert the commit and run `fly-up`. stop conditions: three failed attempts on one failure, or any public address on a private app.
