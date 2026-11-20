# Fly production acceptance, 2026-11-20

Read-only scan of Jaeger on Fly (`supportops-lab-jaeger`, over `fly proxy`) after the 55-case failure-mode probe ran against production (`probe-fly-after-fix.txt`, 55/55, exit 0).

- Scanned 340 traces (338 `p05-runtime`, 2 `p05-mcp`) and 987 spans: span tags and span log fields. `scan_jaeger.py` prints counts and key names only, never values.
- Needles: probe ticket text, the SQL-injection string, tenant and user names, `Bearer `, JWT prefix `eyJ`, `password`, `client_secret`, `@`. Hits: 0.
- Span tag keys are a fixed, content-free set (`http.*`, `gen_ai.*`, `supportops.llm.*`, `mcp.*`, `url.path`, ...). No `db.statement`, no request or response body.
- 72 span logs carry `exception.*`. The messages are the fixed domain strings (`ticket not found`, `approval is already decided`, `a valid idempotency key is required`, ...), never user text. Stack traces show code paths.
- `url.path` carries ids (task uuids), not content.

Limits: one probe run, the API and MCP paths. A worker-side failure was not provoked in production, and no real model run was made (no cost or quality measurement). Terraform apply and load test were not executed (owner chose Fly on 2026-11-20).

Two production bugs found and fixed on the way (`cold-chain-after-fix.txt` first, then `cold-chain-after-db-fix.txt`):
1. The worker called `store.migrate()` once. A stopped Postgres answers "the database system is starting up", the worker exited 1 and the process pair rebooted the machine: users saw 502 for about 40 s on a cold chain. `migrate()` now waits with a capped backoff (p05 `37cfb4c`, red and green in `database-wake-20261120/`).
2. nginx now retries safe requests on 502/503/504 while an upstream wakes (p06, `fix(web)` commit).
After the fixes: 3 of 3 fully cold chains answered 200 in about 15 s (before: 502 at 40 s).
