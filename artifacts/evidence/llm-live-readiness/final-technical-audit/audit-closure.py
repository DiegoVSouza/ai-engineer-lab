"""Read-only coordination audit; product inspection runs in each owning interpreter."""
import json,subprocess,sys,sqlite3,hashlib
from pathlib import Path
from contextlib import closing
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
records=[]
def command(c,cwd):
 r=subprocess.run(c,cwd=cwd,capture_output=True,text=True,timeout=30)
 records.append(dict(command=c,cwd=str(cwd),exit_code=r.returncode,output=r.stdout+r.stderr))
 return r
projects={}
for number in range(6):
 name=f'p{number:02d}';project=ROOT/'projects'/name
 head=command(['git','rev-parse','HEAD'],project).stdout.strip()
 status=command(['git','status','--short'],project).stdout
 manifests={'p00':'local-live-operation-v1/current-036-binding.json','p01':'local-diagnostic-2-v1/manifest.json','p02':'local-operation-v1/manifest.json','p03':'local-operation-v1/manifest.json','p04':'local-diagnostic-v1/manifest.json','p05':'local-operation-v1/current-030.json'}
 manifest=json.loads((project/'artifacts/evals/live'/manifests[name]).read_text())
 if name=='p00':
  code="import json,hashlib;from scripts.campaign_execution import fingerprint;from pathlib import Path;p=Path.cwd();v=fingerprint(p,p.parents[1]/'shared/policies/groq-free-campaign.json');print(hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest())"
 else:
  module='diagnostic_operation' if name in {'p01','p04'} else ('current_operation' if name=='p05' else 'local_operation')
  code=f'from scripts.{module} import fingerprint;print(fingerprint())'
 result=command([str(project/'.venv/Scripts/python.exe'),'-c',code],project)
 assert result.returncode==0,result.stdout+result.stderr
 current=result.stdout.strip()
 own=command(['git','diff','--name-only',manifest['candidate'],'HEAD','--','src','supportops_foundation','supportops_toolkit','supportops_obs','supportops_async','supportops_platform','scripts','tests','agent','evals','stack','alerts','pyproject.toml','uv.lock','harness.yaml'],project).stdout.splitlines()
 projects[name]=dict(owner_source_changes_since_recorded_candidate=own,head=head,existing_changes_preserved=status,recorded_candidate=manifest.get('candidate'),recorded_fingerprint=manifest.get('fingerprint',manifest.get('source_fingerprint')),current_fingerprint=current,current_matches_recorded=current==manifest.get('fingerprint',manifest.get('source_fingerprint')))
sys.path.insert(0,str(ROOT/'scripts/harness'))
from live_free_account import SharedAccount,AccountBlocked
policy=json.loads((ROOT/'shared/policies/groq-free-campaign.json').read_text())
account=SharedAccount(ROOT,policy)
rows=account._history()
usage={name:{field:str(sum(account.usage(r)[field] for r in rows if r['project']==name)) for field in ('requests','input_tokens','output_tokens','estimated_cost_usd')} for name in projects}
assert len(rows)==86
stops={}
for name in ('p01','p04'):
 for campaign,case in (('local-operation-v1','fixture-renamed-audit'),('local-diagnostic-v1','fixture-diagnostic-01')):
  try:account.preview(name,campaign,case,1,3,2048,256)
  except AccountBlocked as error:stops[name+'/'+campaign]=str(error)
  else:raise AssertionError('closed operation was allowed')
try:account.preview('p01','local-diagnostic-2-v1','fixture-diagnostic-02',1,3,2048,256)
except AccountBlocked as error:stops['p01/local-diagnostic-2-v1']=str(error)
else:raise AssertionError('closed second diagnostic was allowed')
try:account.preview('p05','local-operation-v1','fixture-unfunded-audit',1,1,4096,512)
except AccountBlocked as error:stops['p05/operating-envelope']=str(error)
else:raise AssertionError('exhausted P05 envelope was allowed')
logical={}
for name in ('p01','p04'):
 path=ROOT/'projects'/name/'artifacts/evals/live/ledger.sqlite'
 with closing(sqlite3.connect(path.resolve().as_uri()+'?mode=ro',uri=True)) as db:
  logical[name]=db.execute("SELECT campaign_id,event,reserved_calls,outcome,error_class,actual_input_tokens,actual_output_tokens FROM events ORDER BY sequence").fetchall()
assert logical['p01'][1][3:]==('incomplete','unknown',None,None)
assert logical['p01'][3][3:]==('incomplete','unknown',None,None)
assert logical['p01'][5][3:]==('incomplete','unknown',None,None)
assert sum(r[2] for r in logical['p01'] if r[1]=='reserved')==12
assert logical['p04'][1][3:]==('incomplete','unknown',None,None)
assert logical['p04'][3][3:] == ('ok',None,292,71)
unknown=[dict(project=r['project'],receipt=r['attempt_id'],reserved_input=r['reserved_input'],reserved_output=r['reserved_output']) for r in rows if r['actual_input'] is None or r['actual_output'] is None]
assert len(unknown)==1 and unknown[0]['reserved_input']==1475 and unknown[0]['reserved_output']==256
protected=json.loads((ROOT/'projects/p01/artifacts/evidence/strict-worker-schema-024/snapshot-preservation.json').read_text())['after']
assert all(hashlib.sha256((ROOT/'projects/p01'/name).read_bytes()).hexdigest()==digest for name,digest in protected.items())
report=dict(status='PASS_READ_ONLY_RECONCILIATION',projects=projects,provider_usage_by_project=usage,total_provider_attempts=len(rows),unknown_provider_reservations=unknown,logical_original_and_diagnostic=logical,terminal_guards=stops,policy_sha256=account.policy_hash,registry_projects=account._references(),paid_authorization_usd=0,actual_billing='UNKNOWN',human_quality_holdout_promotion='PENDING',provider_accessed=False,credentials_read=False,p01_user_output_hashes_unchanged=True)
(OUT/'commands-closure.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8',newline='\n')
(OUT/'report-closure.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'status':report['status'],'provider_attempts':len(rows),'current_matches':{k:v['current_matches_recorded'] for k,v in projects.items()},'terminal_guards':stops}))
