"""Validate final report references and immutable acceptance boundaries without providers."""
import hashlib,json,subprocess,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
r=json.loads((OUT/'report-closure.json').read_text())
policy=json.loads((ROOT/'shared/policies/groq-free-campaign.json').read_text())
registry=json.loads((ROOT/'.runtime/llm-live-readiness/ledger-references.json').read_text())
assert hashlib.sha256(json.dumps(policy,sort_keys=True).encode()).hexdigest()==r['policy_sha256']==registry['policy_sha256']
assert policy['campaign_caps']['requests']==4141
assert sum(int(v['requests']) for v in r['provider_usage_by_project'].values())==86
assert sum(int(v['input_tokens']) for v in r['provider_usage_by_project'].values())==30717
assert sum(int(v['output_tokens']) for v in r['provider_usage_by_project'].values())==8119
assert {name for name,p in r['projects'].items() if p['current_matches_recorded']}=={'p00','p02','p03','p05'}
assert r['projects']['p04']['owner_source_changes_since_recorded_candidate']==[]
phases={'p00':'036-second-diagnostic-allocation-binding','p01':'024-strict-worker-schema','p02':'016-accounted-local-operation','p03':'025-accounted-local-live','p04':'031-reviewed-separate-diagnostic','p05':'030-current-policy-operation'}
for name,phase in phases.items():
 project=ROOT/'projects'/name
 assert (project/'.planning/phases'/phase/'VERIFY.md').is_file()
 actual=subprocess.run(['git','rev-parse','HEAD'],cwd=project,capture_output=True,text=True,check=True).stdout.strip()
 assert actual==r['projects'][name]['head']
 for revision in (actual,r['projects'][name]['recorded_candidate']):
  assert subprocess.run(['git','cat-file','-e',revision+'^{commit}'],cwd=project,capture_output=True).returncode==0
protected=json.loads((ROOT/'projects/p01/artifacts/evidence/strict-worker-schema-024/snapshot-preservation.json').read_text())['after']
assert all(hashlib.sha256((ROOT/'projects/p01'/name).read_bytes()).hexdigest()==digest for name,digest in protected.items())
for name,path in {'p00':'second-diagnostic-allocation-036/reconciliation.json','p01':'second-reviewed-diagnostic-023/reconciliation.json','p02':'accounted-local-operation-016/reconciled.json','p03':'accounted-local-live-025/reconciliation.json','p04':'reviewed-diagnostic-031/reconciliation.json','p05':'current-policy-operation-030/live-verification.json'}.items():
 assert (ROOT/'projects'/name/'artifacts/evidence'/path).is_file()
for name,path in {'p04':'reviewed-diagnostic-031/service-attempt1/service-result.json','p05':'current-policy-operation-030/attempt1/service-result.json'}.items():
 result=json.loads((ROOT/'projects'/name/'artifacts/evidence'/path).read_text())
 assert result=={'gate_exit_code':0,'cleanup_exit_code':0,'prior_resources_preserved':True,'phase_containers_remaining':False}
for name in ('STATUS.md','CONTINUATION-PLAN.md','EXECUTOR-HANDOFF.md'):
 p=ROOT/'.planning/llm-live-readiness'/name
 raw=p.read_bytes()
 assert b'Authoritative final checkpoint' in raw and b'037-final-technical-audit/FINAL-REPORT.md' in raw
 assert (p.parent/'phases/037-final-technical-audit/FINAL-REPORT.md').is_file()
report=(ROOT/'.planning/llm-live-readiness/phases/037-final-technical-audit/FINAL-REPORT.md').read_text()
assert all('| '+task+' |' in report for task in ('T0','T1','T2','T3','T4','T5','T6','T7'))
assert 'not an all-live-ready' in report and 'P01 remains INCOMPLETE' in report
assert '30717input/8119output' in report and 'USD0.004739475' in report
print(json.dumps({'status':'PASS','projects':6,'provider_attempts':86,'policy_registry_match':True,'protected_user_outputs_unchanged':True,'native_references_and_commits_valid':True,'human_annotations_written':False,'provider_accessed':False,'credentials_read':False}))
