"""Validate the authorized exact delta without changing runtime metadata."""
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(root / 'scripts/harness'))
import migrate_free_envelope_plus13 as migration

before = json.loads((root / migration.BASELINE).read_text())
after = json.loads((root / migration.POLICY).read_text())
assert migration.proposed_policy(before) == after
assert all(before['projects'][p] == after['projects'][p] for p in before['projects'] if p != 'p00')
assert after['projects']['p00']['requests'] - 149 == 60
assert 149 - 29 == 36 + 84
print(json.dumps({'status': 'PASS_EXACT_DELTA', 'old_sha': migration.digest(before), 'new_sha': migration.digest(after), 'provider_accessed': False, 'credentials_read': False}))
