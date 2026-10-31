# Verification — frontend platform

Status: F0–F3 done locally; F4 and F5 pending. Nothing is deployed.

| Phase | Gate | Result |
| --- | --- | --- |
| F0 | ADR-001, SPEC, PLAN | done (commit `bfbe159`) |
| F1 | `projects/p08` `check_full.py` (contrast table, axe with contrast, reduced motion, budget, pack) | PASS_LOCAL, 0.3.0, 40 tests, 4.7 KB gzip; evidence `projects/p08/artifacts/evidence/colagem-ui-001/` |
| F2 | `projects/p07` `check_full.py` + squint screenshots | PASS_LOCAL, 20 tests, 78.6 KB gzip of 100 KB; evidence `projects/p07/artifacts/evidence/portfolio-001/` |
| F3 | `projects/p06` `check_full.py` + offline browser e2e + wake test | PASS_LOCAL, 30 tests, 92.0 KB gzip of 120 KB, Docker image builds; real-stack e2e not rerun; evidence `projects/p06/artifacts/evidence/frontend-platform/` |
| F4 | P05 CORS tests + Keycloak client test | PASS_LOCAL: P05 `tests/test_cors.py` 14 passed and `check_fast.py` exit 0 (P05 commit `a2bfd17`, evidence `projects/p05/artifacts/evidence/cors-035/`); lab `scripts/harness/test_idp_clients.py` 6 passed, `test_fly_ops` still passes (24 tests together). Not run: P05 `check_full.py`, a real Keycloak apply. P05 version bump, wheel and `projects.lock.json` pin are left to F5 |
| F5 | Public e2e with axe against Pages URLs; rollback rehearsal | PENDING. Prepared, not executed: `ops/pages/deploy.ps1` (dry run by default; `scripts/harness/test_pages_ops.py`, 5 passed against a fake wrangler) and `rollback.md`. Blocker: every deploy needs the owner's go |

Open points for the owner: squint screenshots of P07 and P06 (`review_mode=human_pending`); Cloudflare account and the choice of Pages project names; a go for each of `wrangler pages deploy` and `fly deploy`.

## Update 2026-10-31 (portfolio rounds W1b to W9)

- F1: `colagem-ui` is now 0.4.0 (FlowDiagram, build-time `colagem-ui/layout`, ten content blocks, MIT in the tarball). P08 `check_full.py` exit 0, 62 tests, real-Chrome axe with contrast in both themes. Evidence: `projects/p08/artifacts/evidence/colagem-ui-040/check-full.txt`. P06 and P07 pin the new tarball (`docs/harness/sources.lock.json`).
- F2: P07 was rebuilt as a prerendered site, 28 routes in English and Portuguese. `check_full.py` exit 0; worst route 95.1 KB gzip. Evidence: `projects/p07/artifacts/evidence/portfolio-w7/`.
- F3: P06 `check_fast.py` exit 0 on the new package; its contract check ignores CRLF. The client was regenerated for the additive `llm_steps` field. `check_full.py` (Docker image build, offline e2e) was **not** rerun on 0.4.0.
- F4: unchanged. P05 `demo-live-v1` adds a persistent ledger, key failover and `llm_steps` (17 tests against PostgreSQL 16, no provider contacted). P05 version bump and wheel: not done.
- F5: **still PENDING.** No Cloudflare project, no Fly deploy, no rollback rehearsal, no public e2e. Repositories were pushed **privately** to GitHub on 2026-10-31 to get hosted CI on Linux runners; none was made public.
- F6: **not started** (3D scene).
