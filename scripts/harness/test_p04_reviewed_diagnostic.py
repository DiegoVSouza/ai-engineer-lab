import json
import sqlite3
import subprocess
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import live_free_account as module
from live_free_account import AccountBlocked, SharedAccount

ROOT = Path(__file__).resolve().parents[2]
AUTH = ".planning/llm-live-readiness/phases/035-p04-reviewed-diagnostic/AUTHORIZATION.json"


class DiagnosticTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        auth = self.root / AUTH
        auth.parent.mkdir(parents=True)
        auth.write_bytes((ROOT / AUTH).read_bytes())
        for args in (("init", "-q"), ("config", "user.email", "fixture@example.invalid"),
                     ("config", "user.name", "Fixture"), ("add", AUTH), ("commit", "-qm", "test: freeze approval")):
            subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True)
        policy = json.loads((ROOT / "shared/policies/groq-free-campaign.json").read_text())
        # This diagnostic predates the later revalidation allocation; keep the
        # current policy and guard, and select only the historical p04 scope.
        policy["projects"]["p04"]["requests"] = 744
        self.account = SharedAccount(self.root, policy)
        self.account.register("p04")
        ids = ["196cae46b57b4312afeee02aa89d813e"]
        for index, usage in enumerate(((105, 51),), 1):
            with patch.object(module.uuid, "uuid4", return_value=SimpleNamespace(hex=ids[index - 1])):
                receipt = self.account.reserve("p04", "local-operation-v1", "fixture-local-01", 1, index, 2048, 256)
            self.account.complete("p04", receipt, input_tokens=usage[0], output_tokens=usage[1])
        self.logical = self.root / "projects/p04/artifacts/evals/live/ledger.sqlite"
        with closing(sqlite3.connect(self.logical)) as db:
            db.execute("CREATE TABLE events(sequence INTEGER PRIMARY KEY,campaign_id TEXT,case_id TEXT,trial INTEGER,event TEXT,reserved_calls INTEGER,reserved_input_tokens INTEGER,reserved_output_tokens INTEGER,reserved_cost_usd TEXT,outcome TEXT,error_class TEXT,actual_input_tokens INTEGER,actual_output_tokens INTEGER,actual_cost_usd TEXT)")
            for sequence, event in ((1, "reserved"), (2, "completed")):
                db.execute("INSERT INTO events VALUES(?, 'local-operation-v1','fixture-local-01',1,?,3,12288,1536,'0.0013824',?,?,NULL,NULL,NULL)",
                           (sequence,event,"incomplete" if sequence == 2 else None,"unknown" if sequence == 2 else None))
            db.commit()

        with closing(sqlite3.connect(self.logical.parent / "operations.sqlite")) as db:
            db.execute("CREATE TABLE attempts(operation TEXT,step TEXT,status TEXT,receipt TEXT,input_tokens INTEGER,output_tokens INTEGER)")
            db.execute("INSERT INTO attempts VALUES('fixture-local-01','triage','reserved',NULL,NULL,NULL)")
            db.commit()

    def test_closed_diagnostic_cannot_resume_with_remaining_provider_capacity(self):
        with closing(sqlite3.connect(self.logical)) as db:
            db.execute("INSERT INTO events(sequence,campaign_id,case_id,trial,event) VALUES(3,'local-diagnostic-v1','fixture-diagnostic-01',1,'completed')")
            db.commit()
        with self.assertRaisesRegex(AccountBlocked,"authority_or_history"):
            self.reserve()

    def test_original_step_mutation_is_denied(self):
        with closing(sqlite3.connect(self.logical.parent / "operations.sqlite")) as db:
            db.execute("UPDATE attempts SET status='ok'")
            db.commit()
        with self.assertRaisesRegex(AccountBlocked,"authority_or_history"):
            self.reserve()

    def test_failed_original_cannot_be_bypassed_with_a_new_case(self):
        with self.assertRaisesRegex(AccountBlocked,"logical_operation_stopped"):
            self.account.reserve("p04", "local-operation-v1", "fixture-renamed", 1, 1, 2048,256)

    def reserve(self, case="fixture-diagnostic-01", index=1):
        return self.account.reserve("p04", "local-diagnostic-v1", case, 1, index, 2048, 256)

    def test_narrow_scope_is_finite_and_preserves_original_reserve(self):
        before = self.logical.read_bytes()
        for index in range(1,4):
            receipt = self.reserve(index=index)
            self.account.complete("p04", receipt, input_tokens=100, output_tokens=20)
        with self.assertRaises(AccountBlocked):
            self.reserve(index=3)
        self.assertEqual(self.logical.read_bytes(), before)
        with self.assertRaises(AccountBlocked):
            self.account.reserve("p04", "local-operation-v1", "fixture-local-01", 1, 1, 2048,256)

    def test_missing_or_modified_authority_is_denied(self):
        auth = self.root / AUTH
        auth.write_text("{}")
        with self.assertRaisesRegex(AccountBlocked,"authority_or_history"):
            self.reserve()

    def test_changed_retained_reservation_is_denied(self):
        with closing(sqlite3.connect(self.logical)) as db:
            db.execute("UPDATE events SET reserved_calls=2")
            db.commit()
        with self.assertRaisesRegex(AccountBlocked,"authority_or_history"):
            self.reserve()

    def test_other_identity_and_uncertain_replay_denied(self):
        with self.assertRaisesRegex(AccountBlocked,"scope_required"):
            self.reserve("fixture-new")
        self.reserve()
        with self.assertRaisesRegex(AccountBlocked,"uncertain_attempt"):
            self.reserve(index=2)

    def test_failed_diagnostic_cannot_continue(self):
        receipt = self.reserve()
        self.account.complete("p04",receipt,status="transport_error")
        with self.assertRaisesRegex(AccountBlocked,"prior_operational_failure"):
            self.reserve(index=2)
