"""Prepare fixed P02 migration inputs without applying or accessing providers."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[4]
out = Path(__file__).resolve().parent
phase = root / '.planning/llm-live-readiness/phases/031-p02-operation-envelope'
policy_path = root / 'shared/policies/groq-free-campaign.json'
before = json.loads(policy_path.read_text())
old = hashlib.sha256(json.dumps(before, sort_keys=True).encode()).hexdigest()
assert old == '6c87609c7ebc7e58de8d5e9054fe1984ebcd20fec58bf26d0a60f73257ebbfeb'
out.joinpath('policy-before.json').write_text(json.dumps(before, indent=2) + '\n')
after = json.loads(json.dumps(before))
from decimal import Decimal
for caps in (after['campaign_caps'], after['projects']['p02']):
    for key, amount in [('requests', 4), ('input_tokens', 16384), ('output_tokens', 2048)]:
        caps[key] += amount
    caps['estimated_cost_usd'] = str(Decimal(caps['estimated_cost_usd']) + Decimal('0.0018432'))
new = hashlib.sha256(json.dumps(after, sort_keys=True).encode()).hexdigest()
policy_path.write_text(json.dumps(after, indent=2, sort_keys=True) + '\n')
auth = json.loads((root / '.planning/llm-live-readiness/phases/029-p01-operation-envelope/AUTHORIZATION.json').read_text())
auth.update(authorization_id='p02-local-operation-plus4-v1', project='p02', additional_calls=4)
phase.joinpath('AUTHORIZATION.json').write_text(json.dumps(auth, indent=2) + '\n')
source = (root / 'scripts/harness/migrate_p01_operation.py').read_text()
source = source.replace('p01', 'p02').replace('P01', 'P02').replace('eight-call', 'four-call').replace('plus8', 'plus4')
source = source.replace('029-p02-operation-envelope', '031-p02-operation-envelope')
source = source.replace('6b678227c7d6ee138ed3495229e8bb365b930cafc9c241dece4df8d42cb6a12c', old)
source = source.replace('NEW_SHA = "' + old + '"', 'NEW_SHA = "' + new + '"')
source = source.replace('("requests", 8)', '("requests", 4)').replace('"additional_calls": 8', '"additional_calls": 4')
source = source.replace('    "artifacts/evidence/llm-live-readiness/p02-operation-envelope/plan-check.md",\n', '')
root.joinpath('scripts/harness/migrate_p02_operation.py').write_text(source)
tests = (root / 'scripts/harness/test_migrate_p01_operation.py').read_text().replace('migrate_p01_operation', 'migrate_p02_operation')
root.joinpath('scripts/harness/test_migrate_p02_operation.py').write_text(tests)
print(json.dumps({'old': old, 'new': new, 'additional_calls': 4, 'provider_accessed': False}))
