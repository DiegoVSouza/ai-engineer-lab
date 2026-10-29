"""Prepare a fixed four-call P03 amendment, without applying it."""
import hashlib
import json
from decimal import Decimal
from pathlib import Path

root = Path(__file__).resolve().parents[4]
out = Path(__file__).resolve().parent
phase = root / '.planning/llm-live-readiness/phases/032-p03-operation-envelope'
path = root / 'shared/policies/groq-free-campaign.json'
before = json.loads(path.read_text())
old = hashlib.sha256(json.dumps(before, sort_keys=True).encode()).hexdigest()
assert old == '196fb3503db9c68964e928d3f18494043c44ceeaf8ac2046981ec3c84c3ed66f'
out.joinpath('policy-before.json').write_text(json.dumps(before, indent=2) + '\n', newline='\n')
after = json.loads(json.dumps(before))
for caps in (after['campaign_caps'], after['projects']['p03']):
    for key, amount in [('requests', 4), ('input_tokens', 16384), ('output_tokens', 2048)]:
        caps[key] += amount
    caps['estimated_cost_usd'] = str(Decimal(caps['estimated_cost_usd']) + Decimal('0.0018432'))
new = hashlib.sha256(json.dumps(after, sort_keys=True).encode()).hexdigest()
path.write_text(json.dumps(after, indent=2, sort_keys=True) + '\n', newline='\n')
auth = json.loads((root / '.planning/llm-live-readiness/phases/031-p02-operation-envelope/AUTHORIZATION.json').read_text())
auth.update(authorization_id='p03-local-operation-plus4-v1', project='p03')
phase.joinpath('AUTHORIZATION.json').write_text(json.dumps(auth, indent=2) + '\n', newline='\n')
source = (root / 'scripts/harness/migrate_p02_operation.py').read_text().replace('p02', 'p03').replace('P02', 'P03')
source = source.replace('031-p03-operation-envelope', '032-p03-operation-envelope')
source = source.replace('6c87609c7ebc7e58de8d5e9054fe1984ebcd20fec58bf26d0a60f73257ebbfeb', old)
source = source.replace('NEW_SHA = "' + old + '"', 'NEW_SHA = "' + new + '"')
root.joinpath('scripts/harness/migrate_p03_operation.py').write_text(source, newline='\n')
tests = (root / 'scripts/harness/test_migrate_p02_operation.py').read_text().replace('migrate_p02_operation', 'migrate_p03_operation').replace('test_p02_', 'test_p03_').replace('"p02"', '"p03"').replace('protected_p02_', 'protected_p03_')
root.joinpath('scripts/harness/test_migrate_p03_operation.py').write_text(tests, newline='\n')
print(json.dumps({'old': old, 'new': new, 'provider_accessed': False}))
