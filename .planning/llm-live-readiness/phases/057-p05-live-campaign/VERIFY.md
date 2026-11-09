# Verify

Status: INCOMPLETE until saved evidence exists in `artifacts/evidence/llm-live-readiness/p05-dev-campaign/`.

- [ ] New guard tests fail before the change and pass after.
- [ ] `python -m unittest discover -s scripts/harness -p "test_live_*.py"` passes (baseline 79).
- [ ] `AUTHORIZATION.json` committed and unmodified.
