import copy
import hashlib
import json
from decimal import Decimal
from pathlib import Path

root = Path(__file__).resolve().parents[4]
directory = Path(__file__).resolve().parent
before = json.loads((root / "shared/policies/groq-free-campaign.json").read_text())
after = copy.deepcopy(before)
for item in (after["campaign_caps"], after["projects"]["p01"]):
    item["requests"] += 8
    item["input_tokens"] += 16384
    item["output_tokens"] += 2048
    item["estimated_cost_usd"] = str(Decimal(item["estimated_cost_usd"]) + Decimal("0.0018432"))
digest = lambda value: hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()
assert after["projects"]["p00"] == before["projects"]["p00"]
assert all(after["projects"][name] == before["projects"][name] for name in ("p02", "p03", "p04", "p05"))
for name, value in (("policy-before.json", before), ("policy-after.json", after)):
    (directory / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", newline="\n")
report = {"status": "PASS_PROPOSAL_ONLY", "old_sha256": digest(before), "new_sha256": digest(after), "additional_calls": 8, "additional_input_tokens": 16384, "additional_output_tokens": 2048, "additional_economic_estimate_usd": "0.0018432", "paid_authorization_usd": "0.00", "provider_accessed": False, "credentials_read": False}
(directory / "proposal.json").write_text(json.dumps(report, indent=2) + "\n", newline="\n")
print(json.dumps(report))
