"""Validate final source/ledger/evidence references without provider access."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(root / 'scripts/harness'))
from live_free_account import SharedAccount

sources = {
    'p00': ('artifacts/evidence/funded-replacement-028/full-attempt1.txt', r'148 passed'),
    'p01': ('artifacts/evidence/transport-regression-015/final-root3316217/check_fast.txt', r'Ran 71 tests'),
    'p02': ('artifacts/evidence/fixture-retrieval-012/full.txt', r'Ran 64 tests|64 passed'),
    'p03': ('artifacts/evidence/current-service-recheck-021/run/check-full.txt', r'56 passed|Ran 56 tests'),
    'p04': ('artifacts/evidence/current-full-privacy-027/full-attempt2-run4.txt', r'87 passed'),
    'p05': ('artifacts/evidence/span-status-privacy-025/offline-tests.txt', None),
}
projects = {}
for name, (relative, expected) in sources.items():
    owner = root / 'projects' / name
    path = owner / relative
    content = path.read_text(encoding='utf-8')
    if name == 'p05':
        completed = sum(len(match.group(1)) for match in re.finditer(r'^([.]+)\s+\[\s*\d+%\]', content, re.MULTILINE))
        assert completed == 138, 'p05_missing_138_success_markers'
        metadata = (owner / 'artifacts/evidence/span-status-privacy-025/offline-tests.meta.txt').read_text()
        assert re.search(r'exit[_ ]code\s*[:=]\s*0', metadata, re.IGNORECASE), 'p05_missing_exit_zero'
    else:
        assert re.search(expected, content), name + '_missing_test_evidence'
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=owner, capture_output=True, text=True, check=True).stdout.strip()
    status = subprocess.run(['git', 'status', '--short'], cwd=owner, capture_output=True, text=True, check=True).stdout.splitlines()
    projects[name] = {'head': head, 'local_evidence': relative, 'evidence_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'local_gate': 'PASS_SCOPED', 'git_status': status}
policy = json.loads((root / 'shared/policies/groq-free-campaign.json').read_text())
account = SharedAccount(root, policy)
snapshot = account.snapshot()
assert snapshot['accounted_attempts'] == 65
assert snapshot['uncertain_attempts'] == 0
assert snapshot['cumulative_accounted_usage']['requests'] == '65'
report = json.loads((root / 'projects/p00/artifacts/evals/live/free-dev-c2r1/report.json').read_text())
assert (report['recorded_trials'], report['passed_trials'], report['status']) == (36, 27, 'FAIL_PROVISIONAL')
assert report['resume_command'] is None and report['unfinalized_trial_artifacts'] == 0
manifest = json.loads((root / 'projects/p00/artifacts/evals/live/free-dev-c2r1/manifest.json').read_text())
for name, digest in manifest['files_sha256'].items():
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest, 'evaluated_source_changed'
historical = json.loads((root / 'projects/p00/artifacts/evidence/funded-candidate-continuation/transport-regression-027/reconciliation.json').read_text())
final = json.loads((root / 'projects/p00/artifacts/evidence/funded-replacement-028/final-reconciliation.json').read_text())
for campaign in historical['campaigns']:
    assert historical['campaigns'][campaign] == final['campaigns'][campaign], 'historical_campaign_changed'
allocation = json.loads((root / 'projects/p00/artifacts/evidence/funded-replacement-028/final-allocation.json').read_text())['candidate']
assert allocation['remaining_capacity_by_project']['p00']['primary_remaining'] == 84
assert allocation['p00_confirmation_protected']['requests'] == 60
assert allocation['policy_registry_sha256_matches'] is True
result = {
    'status': 'PASS_METADATA_AND_EVIDENCE_RECONCILIATION',
    'overall_live_readiness': 'INCOMPLETE', 'provider_accessed': False, 'credentials_read': False,
    'projects': projects, 'account': snapshot,
    'p00_development': {'status': 'FAIL_PROVISIONAL', 'candidate': manifest['candidate_commit'], 'trials': 36, 'passes': 27, 'all_three_cases': 9, 'unique_cases': 12, 'remaining_primary_holdout': 84, 'confirmation_protected': 60},
    'pending_external_prerequisites': {
        'p00': ['actual human/independent/dataset/rubric review of cases 025/026/037 and contract resolution', 'explicit fresh corrected-development funding before changing/re-evaluating candidate', 'original holdout sealing/approvals; development currently fails'],
        'p01': ['eligible owned KB/billing source/version, trusted principal/tenant ACL contract and verification environment'],
        'p02': ['eligible owned corpus/identity/source/model contract for actual external retrieval and entailment'],
        'p03': ['production backend/service identity and external operational acceptance; actual human/independent review'],
        'p04': ['owned RAG corpus/tenant/source contract, production backend acceptance and actual review'],
        'p05': ['external IdP issuer/audience/scopes/delegation/revocation acceptance contract and actual model/human review'],
    },
    'promotion': 'PENDING_ALL_APPLICABLE_QUALITY_REVIEW_HOLDOUT_CANARY_ROLLBACK_GATES',
}
print(json.dumps(result, indent=2, sort_keys=True))
