# SupportOps e2e, local and Fly, 2026-11-09

Browser e2e (`projects/p06`, Playwright): local 3 passed 1 skipped (`local-run1.txt`); Fly 3 passed 1 skipped three times
(`fly-run1.txt`, `fly-run2.txt`, and `fly-run3-cold-p04-mcp.txt` with p04 and mcp machines stopped first).
API failure-mode probe (`probe.py`, 55 expectations: auth, tampering, tenant isolation, validation, idempotency, approvals, tasks, headers):
local 55/55 (`probe-local-run4.txt`), Fly 55/55 (`probe-fly-run6.txt`), stricter expectations included.

## Findings
1. BUG, fixed: a NUL byte in ticket/feedback text returned HTTP 500 (`UntranslatableCharacter`, PostgreSQL cannot store it). Now 422.
   p05 commit 8e0e494 (test written first, red in `projects/p05/artifacts/evidence/nul-input-20261109/red.txt`), deployed to Fly (`fly-deploy-p05.txt`).
2. OPERATIONAL, not a code bug: after `power.ps1 -Action Stop` the public apps have autostart disabled, so every URL answers 503
   until `power.ps1 -Action Start` (`cold-web.txt`). Start took 92 s and waits for health checks (`cold-start-timing.txt`).
   Keycloak alone needs about 60 to 90 s after an idle auto-stop; requests in that window get 503 from the Fly proxy.
3. LOW, fixed: an invalid approval decision returned 409 and a numeric string `"12"` was accepted as an amount. Both are 422 now
   (p05 commit with test first, `projects/p05/artifacts/evidence/strict-input-20261109/`; contract and client regenerated in p06).
4. PROD, fixed: Keycloak took 346 s to answer after an idle auto-stop on 1 shared vCPU (502/503 meanwhile; boot 198 s plus 142 s bootstrap,
   `idp-cold-poll.txt`). `fly/idp/fly.toml` now asks for 2 shared vCPUs; two cold starts measured at 19 s (`idp-cold-poll-2cpu.txt`).
   The earlier 90 s figure was with a warm CPU, so the slow case looks like shared-CPU throttling after repeated boots; not proven.

The stack is left started (autostart on), so idle machines stop and wake on request.
