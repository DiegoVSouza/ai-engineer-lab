import copy
import json
import shutil
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path
from contextlib import closing
from unittest.mock import patch
import migrate_p01_p04_revalidation as migration
from live_free_account import AccountBlocked, SharedAccount

ROOT=Path(__file__).resolve().parents[2]

class RevalidationTests(unittest.TestCase):
    def setUp(self):
        self.before=json.loads((ROOT/migration.BASELINE).read_text(encoding="utf-8"))
        self.after=migration.proposed_policy(self.before)

    def test_exact_finite_delta_and_other_project_caps(self):
        self.assertEqual(self.after["campaign_caps"]["requests"]-self.before["campaign_caps"]["requests"],7)
        self.assertEqual(self.after["projects"]["p01"]["requests"],1000)
        self.assertEqual(self.after["projects"]["p04"]["requests"],747)
        for project in ("p00","p02","p03","p05"):
            self.assertEqual(self.after["projects"][project],self.before["projects"][project])
        self.assertEqual(self.after["authorized_paid_spend_usd"],"0.00")
        self.assertEqual(self.after,json.loads((ROOT/"artifacts/evidence/llm-live-readiness/p01-p04-revalidation/policy-proposed.json").read_text()))

    def test_baseline_mutation_is_rejected(self):
        changed=copy.deepcopy(self.before)
        changed["projects"]["p01"]["requests"]+=1
        with self.assertRaisesRegex(migration.MigrationBlocked,"baseline_changed"):
            migration.proposed_policy(changed)

    def test_expanded_caps_fail_closed_without_reviewed_operation_guard(self):
        account=SharedAccount(ROOT,self.after,allow_pending_migration=True)
        with patch.object(account,"_history",return_value=[]), patch.object(account,"_references",return_value={"p01":"fixture","p04":"fixture"}):
            for project in ("p01","p04"):
                with self.assertRaisesRegex(AccountBlocked,"reviewed_revalidation_scope_required"):
                    account._approve(project,"new-scope","fixture-case",1,1,100,20,0)

    def reviewed_fixture(self, project):
        temp = tempfile.TemporaryDirectory(prefix="reviewed-revalidation-")
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        auth = root / ".planning/llm-live-readiness/phases/039-p01-p04-reviewed-revalidation/AUTHORIZATION.json"
        auth.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / migration.AUTH, auth)
        logical = root / "projects" / project / "artifacts/evals/live/ledger.sqlite"
        logical.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / "projects" / project / "artifacts/evals/live/ledger.sqlite", logical)
        account = SharedAccount(root, self.after)
        source = SharedAccount(ROOT, self.before)
        rows = [row for row in source._history() if row["project"] == project]
        git_ok = lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 0, b"", b"")
        return account, rows, logical, patch("live_free_account.subprocess.run", side_effect=git_ok)

    def insert_workflow_reservation(self, logical, project, event="reserved"):
        calls, input_tokens, output_tokens, cost = (
            (4, 8192, 1024, "0.0009216") if project == "p01"
            else (3, 12288, 1536, "0.0013824")
        )
        with closing(sqlite3.connect(logical)) as db:
            db.execute(
                "INSERT INTO events(campaign_id,case_id,trial,event,reserved_calls,reserved_input_tokens,reserved_output_tokens,reserved_cost_usd,outcome,error_class,created_at_utc) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                ("local-revalidation-v1", "fixture-revalidation-01", 1, event,
                 calls, input_tokens, output_tokens, cost,
                 "ok" if event == "completed" else None, None, "2026-10-29T00:00:00+00:00"),
            )
            db.commit()

    def test_preview_does_not_authorize_provider_reservation_without_logical_reserve(self):
        for project in ("p01", "p04"):
            with self.subTest(project=project):
                account, rows, _, git = self.reviewed_fixture(project)
                with git:
                    account._reviewed_revalidation(
                        rows, project, "local-revalidation-v1", "fixture-revalidation-01", 1, 1, False
                    )
                    with self.assertRaisesRegex(AccountBlocked, "authority_or_history_invalid"):
                        account._reviewed_revalidation(
                            rows, project, "local-revalidation-v1", "fixture-revalidation-01", 1, 1, True
                        )

    def test_exact_open_logical_reservation_authorizes_next_contiguous_call(self):
        for project in ("p01", "p04"):
            with self.subTest(project=project):
                account, rows, logical, git = self.reviewed_fixture(project)
                self.insert_workflow_reservation(logical, project)
                with git:
                    account._reviewed_revalidation(
                        rows, project, "local-revalidation-v1", "fixture-revalidation-01", 1, 1, True
                    )
                    with self.assertRaisesRegex(AccountBlocked, "authority_or_history_invalid"):
                        account._reviewed_revalidation(
                            rows, project, "local-revalidation-v1", "fixture-revalidation-01", 1, 2, True
                        )

    def test_completed_workflow_and_mutated_history_are_closed(self):
        account, rows, logical, git = self.reviewed_fixture("p01")
        self.insert_workflow_reservation(logical, "p01", event="completed")
        with git, self.assertRaisesRegex(AccountBlocked, "authority_or_history_invalid"):
            account._reviewed_revalidation(
                rows, "p01", "local-revalidation-v1", "fixture-revalidation-01", 1, 1, True
            )
        account, rows, logical, git = self.reviewed_fixture("p04")
        with closing(sqlite3.connect(logical)) as db:
            db.execute("DROP TRIGGER events_no_update")
            db.execute("UPDATE events SET reserved_calls=2 WHERE sequence=1")
            db.commit()
        with git, self.assertRaisesRegex(AccountBlocked, "authority_or_history_invalid"):
            account._reviewed_revalidation(
                rows, "p04", "local-revalidation-v1", "fixture-revalidation-01", 1, 1, False
            )

if __name__=="__main__":unittest.main()
