# Fresh check_full gates, 2026-11-09

Command per project (cwd = project, `LLM_MODE=fake`, private TEMP): `uv run --locked python scripts/check_full.py` (P06 and P08: `python scripts/check_full.py`). P07 was not run: another session edits its scene files and uses port 44173.

| Project | Exit | Result |
| --- | --- | --- |
| P00 | 0 | `PRODUCT_CHECK=PASS; OPTIONAL_SERVICE_E2E=INCOMPLETE unless separately executed` |
| P01 | 0 | pass |
| P02 | 0 | `check-full: PASS; failures=[]` |
| P03 | 0 | `check-full: PASS; failures=0; incomplete=0` |
| P04 | 2 | `INCOMPLETE explicit Terraform workspace/mirror/config/network/endpoint required`. A first run exited 1 because of a stale git-ignored `artifacts/evidence/.pytest-tmp` from 2026-10-27; that folder was removed and the gate rerun. |
| P05 | 2 | `INCOMPLETE; service integration/E2E/crash recovery` (services not started for this run; another session was editing P05 while it ran) |
| P06 | 0 | `PASS`; real-stack e2e needs the root stack |
| P08 | 0 | `PASS` |

Each `pN-check-full.txt` holds the command, start/end times, the last 60 lines and the exit code. The label changes: none. These runs confirm the existing `PASS_LOCAL` records and do not close any pending axis.
