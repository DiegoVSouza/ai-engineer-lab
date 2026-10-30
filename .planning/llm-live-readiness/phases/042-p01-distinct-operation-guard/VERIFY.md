# Verification

Offline guard verification PASS: `python -m unittest discover -s scripts/harness -p test_p01_p04_revalidation.py -v` exit0, seven tests. It checks rejected consumed P01 and cross-project identities, new P01 and unchanged P04 scope, preview/open reservations, completed workflows and modified history. Attempt1 failed because the fixture used the pre-migration policy against the current registry; fixture now uses the applied policy, retaining exact history checks. Both attempts saved under `artifacts/evidence/llm-live-readiness/p01-distinct-guard-042/`.

Root account and provider transport regression suites both exit0; exact commands and output in `root-regressions.json`. No credentials/provider used. This verifies the shared guard only; P01 controller, committed binding, isolated full gate and live operation remain PENDING.
