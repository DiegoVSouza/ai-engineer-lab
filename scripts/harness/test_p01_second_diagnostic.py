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
AUTH = ".planning/llm-live-readiness/phases/038-p01-second-diagnostic/AUTHORIZATION.json"


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
        self.account = SharedAccount(self.root, json.loads((ROOT / "artifacts/evidence/llm-live-readiness/p01-second-diagnostic/policy-proposed.json").read_text()))
        self.account.register("p01")
        ids = ["9b174b5ca0fa40f6a0b177ec9f4f2523", "bed97cb14f7146f0845588762940e7d4"]
        for index, usage in enumerate(((235, 46), (228, 183)), 1):
            with patch.object(module.uuid, "uuid4", return_value=SimpleNamespace(hex=ids[index - 1])):
                receipt = self.account.reserve("p01", "local-operation-v1", "fixture-local-01", 1, index, 2048, 256)
            self.account.complete("p01", receipt, input_tokens=usage[0], output_tokens=usage[1])
        self.logical = self.root / "projects/p01/artifacts/evals/live/ledger.sqlite"
        with closing(sqlite3.connect(self.logical)) as db:
            db.execute("CREATE TABLE events(sequence INTEGER PRIMARY KEY,campaign_id TEXT,case_id TEXT,trial INTEGER,event TEXT,reserved_calls INTEGER,reserved_input_tokens INTEGER,reserved_output_tokens INTEGER,reserved_cost_usd TEXT,outcome TEXT,error_class TEXT,actual_input_tokens INTEGER,actual_output_tokens INTEGER,actual_cost_usd TEXT)")
            for sequence, event in ((1, "reserved"), (2, "completed")):
                db.execute("INSERT INTO events VALUES(?, 'local-operation-v1','fixture-local-01',1,?,4,8192,1024,'0.0009216',?,?,NULL,NULL,NULL)",
                           (sequence,event,"incomplete" if sequence == 2 else None,"unknown" if sequence == 2 else None))
            db.commit()

        with closing(sqlite3.connect(self.logical)) as db:
            for sequence,event in ((3,"reserved"),(4,"completed")):
                db.execute("INSERT INTO events VALUES(?,'local-diagnostic-v1','fixture-diagnostic-01',1,?,4,8192,1024,'0.0009216',?,?,NULL,NULL,NULL)",(sequence,event,"incomplete" if sequence==4 else None,"unknown" if sequence==4 else None))
            db.commit()

    def test_changed_first_diagnostic_history_is_denied(self):
        with closing(sqlite3.connect(self.logical)) as db:
            db.execute("UPDATE events SET outcome='ok' WHERE sequence=4")
            db.commit()
        with self.assertRaisesRegex(AccountBlocked,"authority_or_history"):
            self.reserve()

    def test_failed_original_cannot_be_bypassed_with_a_new_case(self):
        with self.assertRaisesRegex(AccountBlocked,"logical_operation_stopped"):
            self.account.reserve("p01", "local-operation-v1", "fixture-renamed", 1, 1, 2048,256)

    def test_closed_diagnostic_cannot_continue(self):
        with closing(sqlite3.connect(self.logical)) as db:
            db.execute("INSERT INTO events(sequence,campaign_id,case_id,trial,event) VALUES(5,'local-diagnostic-2-v1','fixture-diagnostic-02',1,'completed')")
            db.commit()
        with self.assertRaisesRegex(AccountBlocked,"authority_or_history"):
            self.reserve()

    def reserve(self, case="fixture-diagnostic-02", index=1):
        return self.account.reserve("p01", "local-diagnostic-2-v1", case, 1, index, 2048, 256)

    def test_narrow_scope_is_finite_and_preserves_original_reserve(self):
        before = self.logical.read_bytes()
        for index in range(1,5):
            receipt = self.reserve(index=index)
            self.account.complete("p01", receipt, input_tokens=100, output_tokens=20)
        with self.assertRaises(AccountBlocked):
            self.reserve(index=4)
        self.assertEqual(self.logical.read_bytes(), before)
        with self.assertRaises(AccountBlocked):
            self.account.reserve("p01", "local-operation-v1", "fixture-local-01", 1, 1, 2048,256)

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
        self.account.complete("p01",receipt,status="transport_error")
        with self.assertRaisesRegex(AccountBlocked,"prior_operational_failure"):
            self.reserve(index=2)
