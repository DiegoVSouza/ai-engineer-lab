"""Prepare exact finite P04/P05 amendments and derived migration controls."""
import hashlib
import json
from decimal import Decimal
from pathlib import Path

root = Path(__file__).resolve().parents[4]
out = Path(__file__).resolve().parent
phase = root / '.planning/llm-live-readiness/phases/034-service-operation-envelopes'
policy = root / 'shared/policies/groq-free-campaign.json'
before = json.loads(policy.read_text())
old = hashlib.sha256(json.dumps(before, sort_keys=True).encode()).hexdigest()
assert old == '417a3103d117f4329c2de4a9ca2b00c82296aa512ed544bf468160fe6f19d9b7'
out.joinpath('policy-before.json').write_text(json.dumps(before, indent=2) + '\n', newline='\n')
after = json.loads(json.dumps(before))
for owner, calls in [('p04', 6), ('p05', 8)]:
    for caps in (after['campaign_caps'], after['projects'][owner]):
        for key, amount in [('requests', calls), ('input_tokens', calls * 4096), ('output_tokens', calls * 512)]:
            caps[key] += amount
        caps['estimated_cost_usd'] = str(Decimal(caps['estimated_cost_usd']) + Decimal(calls) * Decimal('0.0004608'))
new = hashlib.sha256(json.dumps(after, sort_keys=True).encode()).hexdigest()
policy.write_text(json.dumps(after, indent=2, sort_keys=True) + '\n', newline='\n')
auth = json.loads((root / '.planning/llm-live-readiness/phases/032-p03-operation-envelope/AUTHORIZATION.json').read_text())
auth.update(authorization_id='service-local-operations-v1', project='p04+p05', additional_calls=14,
            additional_input_tokens=57344, additional_output_tokens=7168, additional_economic_estimate_usd='0.0064512',
            other_project_caps_changed=False)
phase.joinpath('AUTHORIZATION.json').write_text(json.dumps(auth, indent=2) + '\n', newline='\n')
source = (root / 'scripts/harness/migrate_p03_operation.py').read_text()
source = source.replace('p03-local-operation-plus4-v1', 'service-local-operations-v1')
source = source.replace('032-p03-operation-envelope','034-service-operation-envelopes').replace('p03-operation-envelope','service-operation-envelopes')
source = source.replace('policy-migrations-p03-operation','policy-migrations-service-operations').replace('migrate_p03_operation.py','migrate_service_operations.py')
source = source.replace('196fb3503db9c68964e928d3f18494043c44ceeaf8ac2046981ec3c84c3ed66f',old)
source = source.replace('NEW_SHA = "'+old+'"','NEW_SHA = "'+new+'"')
start = source.index('    for caps in (after["campaign_caps"], after["projects"]["p03"]):')
end = source.index('    if digest(after) != NEW_SHA:',start)
source = source[:start] + '''    for project, calls in (("p04", 6), ("p05", 8)):
        for caps in (after["campaign_caps"], after["projects"][project]):
            for field, amount in (("requests", calls), ("input_tokens", calls * 4096), ("output_tokens", calls * 512)):
                caps[field] += amount
            caps["estimated_cost_usd"] = str(Decimal(caps["estimated_cost_usd"]) + Decimal(calls) * Decimal("0.0004608"))
''' + source[end:]
source = source.replace('"project": "p03"','"project": "p04+p05"').replace('"additional_calls": 4','"additional_calls": 14')
source = source.replace('"additional_input_tokens": 16384','"additional_input_tokens": 57344').replace('"additional_output_tokens": 2048','"additional_output_tokens": 7168').replace('"additional_economic_estimate_usd": "0.0018432"','"additional_economic_estimate_usd": "0.0064512"')
root.joinpath('scripts/harness/migrate_service_operations.py').write_text(source, newline='\n')
tests = (root / 'scripts/harness/test_migrate_p03_operation.py').read_text().replace('migrate_p03_operation','migrate_service_operations')
tests = tests.replace('test_p03_','test_p04_').replace('"p03"','"p04"').replace('protected_p03_', 'protected_p04_')
tests = tests.replace('range(4)', 'range(6)')
root.joinpath('scripts/harness/test_migrate_service_operations.py').write_text(tests,newline='\n')
print(json.dumps({'old':old,'new':new,'p04_added_calls':6,'p05_added_calls':8,'provider_accessed':False}))
