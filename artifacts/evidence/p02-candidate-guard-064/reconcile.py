"""Read-only P02 development usage reconciliation; no credentials or provider access."""
from pathlib import Path
import json
import sqlite3
import sys

root = Path(__file__).resolve().parents[3]
base = root / "projects/p02/artifacts/evals/live"

def readonly(path):
    return sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)

with readonly(base / "provider-usage.sqlite") as db:
    provider = db.execute("SELECT campaign,event,status,COUNT(*) FROM usage_events GROUP BY campaign,event,status ORDER BY campaign,event,status").fetchall()
    provider_keys = db.execute("SELECT case_id,trial,call_index,event,status FROM usage_events WHERE campaign='p02-dev-v1'").fetchall()
with readonly(base / "p02-dev-v1/ledger.sqlite") as db:
    logical = db.execute("SELECT campaign_id,event,outcome,COUNT(*) FROM events GROUP BY campaign_id,event,outcome ORDER BY campaign_id,event,outcome").fetchall()
    logical_keys = db.execute("SELECT case_id,trial,event,outcome FROM events WHERE campaign_id='p02-dev-v1'").fetchall()
development = sum(count for campaign, event, status, count in provider if campaign.startswith("p02-dev-") and event == "reserved")
v1_reserved = sum(count for campaign, event, status, count in provider if campaign == "p02-dev-v1" and event == "reserved")
v1_ok = sum(count for campaign, event, status, count in provider if campaign == "p02-dev-v1" and event == "completed" and status == "ok")
v1_logical = sum(count for campaign, event, outcome, count in logical if campaign == "p02-dev-v1" and event == "completed" and outcome == "graded")
result = {"provider_events": provider, "logical_events": logical, "development_reserved": development,
          "development_limit": 72, "v1_reserved": v1_reserved, "v1_ok": v1_ok, "v1_logical_graded": v1_logical,
          "provider_accessed": False, "credentials_read": False}
provider_reserved = {(case, trial) for case, trial, call, event, status in provider_keys if call == 1 and event == "reserved"}
provider_completed = {(case, trial) for case, trial, call, event, status in provider_keys if call == 1 and event == "completed" and status == "ok"}
logical_reserved = {(case, trial) for case, trial, event, outcome in logical_keys if event == "reserved"}
logical_completed = {(case, trial) for case, trial, event, outcome in logical_keys if event == "completed" and outcome == "graded"}
matched = len(provider_reserved) == 24 and provider_reserved == provider_completed == logical_reserved == logical_completed
result["case_reservations_match"] = matched
result["status"] = "PASS" if matched and v1_reserved == v1_ok == v1_logical == 24 and development <= 48 else "INCOMPLETE"
rendered = json.dumps(result, indent=2)
(Path(__file__).parent / "reconciliation.json").write_text(rendered + "\n", encoding="utf-8", newline="\n")
print(rendered)
sys.exit(0 if result["status"] == "PASS" else 2)
