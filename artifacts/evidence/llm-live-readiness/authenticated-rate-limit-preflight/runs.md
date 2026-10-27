# Phase 006 command record

All calls below are offline. The fake tests use synthetic credentials and mocked HTTP responses. No environment credential was read and no provider was contacted by these checks.

| Check | Command | Exit | Result |
| --- | --- | ---: | --- |
| Account guard | `python -S -m unittest discover -s scripts/harness -p test_live_free_account.py -v` | 0 | 24 passed |
| Provider transport | `python -S -m unittest discover -s scripts/harness -p test_live_provider_transport.py -v` | 0 | 17 passed |
| Allocation migration regression | `python -S -m unittest discover -s scripts/harness -p test_migrate_free_envelope.py -v` | 0 | 14 passed |
| Ruff | `python -m ruff check scripts/harness/live_free_account.py scripts/harness/live_provider_transport.py scripts/harness/test_live_free_account.py scripts/harness/test_live_provider_transport.py` | 0 | Passed |
| Ruff format | `python -m ruff format --check scripts/harness/live_free_account.py scripts/harness/live_provider_transport.py scripts/harness/test_live_free_account.py scripts/harness/test_live_provider_transport.py` | 0 | Passed |
| P00 locked gate | `P00_PYTEST_BASETEMP=artifacts/evidence/funded-candidate-continuation/tmp-phase006-verification-final-20261027 .venv/Scripts/python.exe scripts/check_full.py` (run from `projects/p00`) | 0 | 144 passed; product checks PASS; optional service E2E INCOMPLETE |
