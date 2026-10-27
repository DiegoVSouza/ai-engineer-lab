"""Validate the exact authorized policy amendment and remaining funded commitments."""

import copy
import hashlib
import json
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
phase = ROOT / ".planning/llm-live-readiness/phases/005-free-envelope-migration"
for name in ("SPEC.md","PLAN.md","VERIFY.md","AUTHORIZATION.json"):
    assert (phase / name).is_file()
before_path = ROOT / "artifacts/evidence/llm-live-readiness/envelope-migration/policy-before.json"
before = json.loads(before_path.read_text())
canonical = hashlib.sha256(json.dumps(before, sort_keys=True).encode()).hexdigest()
assert canonical == "ec7ccca5e2bece8cb677cab24dfd9822255bf9fbb791807f956837e62db5ce8d"
authorization = json.loads((phase / "AUTHORIZATION.json").read_text())
assert authorization["authorization_id"] == "p00-free-envelope-plus10-v1"
assert authorization["additional_calls"] == 10 and authorization["additional_input_tokens"] == 20480 and authorization["additional_output_tokens"] == 2560
assert authorization["free_only"] is True and authorization["authorized_paid_spend_usd"] == "0.00"
after = copy.deepcopy(before)
for caps in (after["campaign_caps"], after["projects"]["p00"]):
    for field, amount in (("requests",10),("input_tokens",20480),("output_tokens",2560)):
        caps[field] += amount
    caps["estimated_cost_usd"] = str(Decimal(caps["estimated_cost_usd"]) + Decimal("0.002304"))
assert after["campaign_caps"]["requests"] == sum(caps["requests"] for caps in after["projects"].values()) == 4084
assert after["campaign_caps"]["input_tokens"] == sum(caps["input_tokens"] for caps in after["projects"].values()) == 14311424
assert after["campaign_caps"]["output_tokens"] == sum(caps["output_tokens"] for caps in after["projects"].values()) == 1788928
assert after["campaign_caps"]["estimated_cost_usd"] == "1.6100352"
current = json.loads((ROOT / "shared/policies/groq-free-campaign.json").read_text())
assert current == after
proposed_sha = hashlib.sha256(json.dumps(after,sort_keys=True).encode()).hexdigest()
assert proposed_sha == "1c87eb87ba3a653235aca546180602f288993e49424d6eecdedb01f4688c2a16"
assert all(after["projects"][project] == before["projects"][project] for project in ("p01","p02","p03","p04","p05"))
assert 120 + 744 + 246 + 96 + 558 + 1464 + 840 == 4084 - 16
print(json.dumps({"plan_check":"PASS","old_policy_sha256":canonical,"proposed_policy_sha256":proposed_sha,"global_after":after["campaign_caps"],"p00_after":after["projects"]["p00"],"remaining_calls":4068,"remaining_original_primary_commitments":3228,"protected_confirmation_calls":840,"migration_registry_writes":0,"usage_ledger_writes":0,"provider_accessed":False,"credentials_read":False,"human_and_independent_review":"PENDING"},indent=2))
