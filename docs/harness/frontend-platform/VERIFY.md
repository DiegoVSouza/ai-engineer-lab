# Verification — frontend platform

Status: F0–F3 done locally; F4 and F5 pending. Nothing is deployed.

| Phase | Gate | Result |
| --- | --- | --- |
| F0 | ADR-001, SPEC, PLAN | done (commit `bfbe159`) |
| F1 | `projects/p08` `check_full.py` (contrast table, axe with contrast, reduced motion, budget, pack) | PASS_LOCAL, 0.3.0, 40 tests, 4.7 KB gzip; evidence `projects/p08/artifacts/evidence/colagem-ui-001/` |
| F2 | `projects/p07` `check_full.py` + squint screenshots | PASS_LOCAL, 20 tests, 78.6 KB gzip of 100 KB; evidence `projects/p07/artifacts/evidence/portfolio-001/` |
| F3 | `projects/p06` `check_full.py` + offline browser e2e + wake test | PASS_LOCAL, 30 tests, 92.0 KB gzip of 120 KB, Docker image builds; real-stack e2e not rerun; evidence `projects/p06/artifacts/evidence/frontend-platform/` |
| F4 | P05 CORS tests + Keycloak client test | PENDING |
| F5 | Public e2e with axe against Pages URLs; rollback rehearsal | PENDING, needs a go from the owner |

Open points for the owner: squint screenshots of P07 and P06 (`review_mode=human_pending`); Cloudflare account and the choice of Pages project names; a go for each of `wrangler pages deploy` and `fly deploy`.
