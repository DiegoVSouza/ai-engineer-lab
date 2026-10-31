"""Exercise the approved metadata migration against real temporary Git/SQLite stores."""

import copy
import json
import os
import sqlite3
import subprocess
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

import migrate_p02_operation as migration
from live_free_account import AccountBlocked, SharedAccount, machine_lease


class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="migration-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        source = Path(__file__).resolve().parents[2]
        for name in migration.SOURCE_PATHS:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((source / name).read_bytes())
        self.before = json.loads((self.root / migration.BASELINE).read_text())
        self.after = migration.proposed_policy(self.before)
        self.write(migration.POLICY, self.after)
        self.git("init", "-q")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Offline fixture")
        self.git("add", "--", *migration.SOURCE_PATHS)
        self.git("commit", "-qm", "test: freeze migration fixture")
        p00 = self.root / "projects/p00"
        campaign_source = p00 / "scripts/campaign_execution.py"
        campaign_source.parent.mkdir(parents=True, exist_ok=True)
        # The migration pins one historical blob; P00 has evolved since it was
        # applied, so read the pinned blob, not the current working file.
        pinned = subprocess.run(
            [
                "git",
                "-C",
                str(Path(__file__).resolve().parents[2] / "projects/p00"),
                "cat-file",
                "blob",
                migration.P00_CAMPAIGN_SOURCE_SHA,
            ],
            check=True,
            capture_output=True,
        ).stdout
        campaign_source.write_bytes(pinned)
        subprocess.run(["git", "init", "-q"], cwd=p00, check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "fixture@example.invalid"],
            cwd=p00,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Offline fixture"],
            cwd=p00,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "add", "--", "scripts/campaign_execution.py"],
            cwd=p00,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-qm", "test: freeze campaign lock source"],
            cwd=p00,
            check=True,
            capture_output=True,
        )
        (self.root / ".runtime/llm-live-readiness").mkdir(parents=True, exist_ok=True)
        (self.root / ".runtime/llm-live-readiness/campaign.lock").write_bytes(b"\0")
        account = SharedAccount(self.root, self.before)
        account.register("p00")
        account.register("p01")
        attempt = account.reserve("p00", "local-live-operation-v1", "case", 1, 1, 1475, 256)
        account.complete("p00", attempt, status="transport_error")
        self.registry = self.root / ".runtime/llm-live-readiness/ledger-references.json"

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True)

    def write(self, name, value):
        (self.root / name).write_text(json.dumps(value), encoding="utf-8")

    def run_migration(self, apply=False):
        return migration.migrate(self.root, apply=apply)

    def test_p02_operation_cap_and_protected_evaluation(self):
        self.run_migration(True)
        account = SharedAccount(self.root, self.after)
        account.register("p02")
        with self.assertRaisesRegex(AccountBlocked, "protected_p02_allocation"):
            account.reserve("p02", "evaluation", "case", 1, 1, 10, 5)
        for index in range(4):
            attempt = account.reserve("p02", "local-operation-v1", f"case-{index}", 1, 1, 10, 5)
            account.complete("p02", attempt, input_tokens=10, output_tokens=5)
        with self.assertRaisesRegex(AccountBlocked, "operational_allocation_exhausted"):
            account.reserve("p02", "local-operation-v1", "extra", 1, 1, 10, 5)

    def test_p02_failure_blocks_new_identity(self):
        self.run_migration(True)
        account = SharedAccount(self.root, self.after)
        account.register("p02")
        attempt = account.reserve("p02", "local-operation-v1", "first", 1, 1, 10, 5)
        account.complete("p02", attempt, status="transport_error")
        with self.assertRaisesRegex(AccountBlocked, "prior_operational_failure_requires_review"):
            account.reserve("p02", "local-operation-v1", "new-id", 1, 1, 10, 5)

    def test_dry_run_writes_nothing_and_apply_preserves_unknown_usage_and_uuids(self):
        before = {
            p.relative_to(self.root): p.read_bytes()
            for p in self.root.rglob("*")
            if p.is_file()
        }
        result = self.run_migration()
        self.assertEqual(result["status"], "READY_FOR_APPROVED_MIGRATION")
        after_dry = {
            p.relative_to(self.root): p.read_bytes()
            for p in self.root.rglob("*")
            if p.is_file()
        }
        self.assertEqual(
            set(before),
            set(after_dry),
            f"file set changed: {set(after_dry) ^ set(before)}",
        )
        self.assertEqual(before, after_dry)
        original = json.loads(self.registry.read_text())
        with self.assertRaises(AccountBlocked):
            SharedAccount(self.root, self.after).snapshot()
        result = self.run_migration(True)
        self.assertEqual(result["status"], "APPLIED")
        self.assertEqual(result["projects"], original["projects"])
        self.assertEqual(result["usage"]["input_tokens"], 1475)
        self.assertEqual(result["usage"]["unknown_usage_attempts"], 1)
        self.assertEqual(len(migration.read_audit(self.root)), 2)
        self.assertFalse(migration.marker_path(self.root).exists())
        self.assertEqual(self.run_migration(True)["status"], "ALREADY_APPLIED")
        self.assertEqual(len(migration.read_audit(self.root)), 2)
        with self.assertRaises(AccountBlocked):
            SharedAccount(self.root, self.before).snapshot()

    def test_p01_logical_ledger_without_project_column_is_preserved(self):
        path = self.root / "projects/p01/artifacts/evals/live/ledger.sqlite"
        path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(path)) as db:
            db.execute("CREATE TABLE events(sequence INTEGER PRIMARY KEY, campaign_id TEXT, case_id TEXT, trial INTEGER, event TEXT, reserved_calls INTEGER, reserved_input_tokens INTEGER, reserved_output_tokens INTEGER, reserved_cost_usd TEXT)")
            db.execute("INSERT INTO events VALUES(1,'historical','case',1,'reserved',4,8192,1024,'0.0009216')")
            db.execute("INSERT INTO events VALUES(2,'historical','case',1,'completed',4,8192,1024,'0.0009216')")
            db.commit()
        before = path.read_bytes()
        self.assertEqual(self.run_migration(True)["status"], "APPLIED")
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(self.run_migration(True)["status"], "ALREADY_APPLIED")

    def test_dirty_staged_and_untracked_sources_are_denied(self):
        path = self.root / migration.POLICY
        original = path.read_bytes()
        path.write_bytes(original + b"\n")
        with self.assertRaisesRegex(migration.MigrationBlocked, "not_committed"):
            self.run_migration(True)

        self.git("add", migration.POLICY)
        with self.assertRaisesRegex(migration.MigrationBlocked, "not_committed"):
            self.run_migration(True)
        self.git("reset", "--quiet", "HEAD", "--", migration.POLICY)
        path.write_bytes(original)
        self.git("rm", "--cached", migration.POLICY)
        with self.assertRaisesRegex(migration.MigrationBlocked, "not_committed"):
            self.run_migration(True)

    def test_separate_p00_campaign_source_must_match_committed_blob(self):
        p00 = self.root / "projects/p00"
        source = p00 / "scripts/campaign_execution.py"
        original = source.read_bytes()
        source.write_bytes(original + b"\n")
        with self.assertRaisesRegex(
            migration.MigrationBlocked, "p00_campaign_source_not_committed"
        ):
            self.run_migration(True)
        source.write_bytes(original + b"\n")
        subprocess.run(
            ["git", "-C", str(p00), "add", "--", "scripts/campaign_execution.py"],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "-C", str(p00), "commit", "-qm", "test: change campaign source"],
            check=True,
            capture_output=True,
        )
        with self.assertRaisesRegex(
            migration.MigrationBlocked, "p00_campaign_source_changed"
        ):
            self.run_migration(True)

    def test_unapproved_delta_is_denied_before_any_write(self):
        changed = copy.deepcopy(self.after)
        changed["projects"]["p01"]["requests"] += 1
        self.write(migration.POLICY, changed)
        with self.assertRaisesRegex(
            migration.MigrationBlocked, "unapproved_policy_delta"
        ):
            self.run_migration(True)
        self.assertFalse(migration.audit_path(self.root).exists())

    def test_inflight_work_blocks_migration(self):
        account = SharedAccount(self.root, self.before)
        account.reserve("p01", "local-operation-v1", "case", 1, 1, 100, 20)
        with self.assertRaisesRegex(migration.MigrationBlocked, "inflight"):
            self.run_migration(True)

    def test_logical_reserved_event_blocks_migration(self):
        path = self.root / "projects/p00/artifacts/evals/live/ledger.sqlite"
        path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(path)) as db:
            db.execute("""
                CREATE TABLE events(
                    sequence INTEGER PRIMARY KEY, project TEXT, campaign_id TEXT,
                    case_id TEXT, trial INTEGER, event TEXT, reserved_calls INTEGER,
                    reserved_input_tokens INTEGER, reserved_output_tokens INTEGER,
                    reserved_cost_usd TEXT, actual_input_tokens INTEGER,
                    actual_output_tokens INTEGER, actual_cost_usd TEXT, outcome TEXT,
                    error_class TEXT, created_at_utc TEXT)
            """)
            db.execute(
                "INSERT INTO events VALUES(1,'p00','active','case',1,'reserved',1,100,20,'0.00001',NULL,NULL,NULL,NULL,NULL,'now')"
            )
            db.commit()
        with self.assertRaisesRegex(migration.MigrationBlocked, "inflight"):
            self.run_migration(True)

    def test_interruptions_recover_once_before_and_after_registry_replace(self):
        replace = os.replace
        with (
            patch.object(migration.os, "replace", side_effect=OSError("fixture")),
            self.assertRaises(OSError),
        ):
            self.run_migration(True)
        self.assertEqual(len(migration.read_audit(self.root)), 1)
        self.assertTrue(migration.marker_path(self.root).exists())
        with self.assertRaisesRegex(AccountBlocked, "policy_migration_pending"):
            SharedAccount(self.root, self.before).snapshot()

        def interrupted(*args):
            replace(*args)
            raise OSError("fixture after atomic replace")

        with (
            patch.object(migration.os, "replace", side_effect=interrupted),
            self.assertRaises(OSError),
        ):
            self.run_migration(True)
        with self.assertRaisesRegex(AccountBlocked, "policy_migration_pending"):
            SharedAccount(self.root, self.after).snapshot()
        self.assertEqual(self.run_migration(True)["status"], "RECOVERED_APPLIED")
        self.assertEqual(len(migration.read_audit(self.root)), 2)
        self.assertFalse(migration.marker_path(self.root).exists())

    def test_applied_audit_before_marker_removal_stays_blocked_until_recovery(self):
        original_unlink = Path.unlink

        def interrupted(path, *args, **kwargs):
            if path == migration.marker_path(self.root):
                raise OSError("fixture before pending marker removal")
            return original_unlink(path, *args, **kwargs)

        with (
            patch.object(Path, "unlink", interrupted),
            self.assertRaises(OSError),
        ):
            self.run_migration(True)
        self.assertEqual(len(migration.read_audit(self.root)), 2)
        with self.assertRaisesRegex(AccountBlocked, "policy_migration_pending"):
            SharedAccount(self.root, self.after).snapshot()
        self.assertEqual(self.run_migration(True)["status"], "RECOVERED_APPLIED")
        self.assertFalse(migration.marker_path(self.root).exists())

    def test_audit_is_append_only_and_registry_rollback_is_denied(self):
        original = self.registry.read_bytes()
        self.run_migration(True)
        with closing(sqlite3.connect(migration.audit_path(self.root))) as db:
            for statement in (
                "DELETE FROM events",
                "UPDATE events SET event='prepared'",
            ):
                with self.assertRaises(sqlite3.IntegrityError):
                    db.execute(statement)
        self.registry.write_bytes(original)
        with self.assertRaisesRegex(migration.MigrationBlocked, "rollback"):
            self.run_migration(True)

    def test_new_registry_without_audit_and_unknown_hash_are_denied(self):
        registry = json.loads(self.registry.read_text())
        for sha, reason in (
            (migration.NEW_SHA, "without_audit"),
            ("unknown", "policy_unknown"),
        ):
            registry["policy_sha256"] = sha
            self.registry.write_text(json.dumps(registry))
            with self.assertRaisesRegex(migration.MigrationBlocked, reason):
                self.run_migration(True)

    def test_missing_registered_ledger_and_corrupt_audit_fail_closed(self):
        ledger = self.root / "projects/p00/artifacts/evals/live/provider-usage.sqlite"
        ledger.unlink()
        with self.assertRaisesRegex(AccountBlocked, "missing_or_replaced"):
            self.run_migration(True)
        self.assertFalse(migration.audit_path(self.root).exists())

        self.setUp()
        self.run_migration(True)
        with closing(sqlite3.connect(migration.audit_path(self.root))) as db:
            db.execute("DROP TRIGGER no_migration_update")
            db.execute("UPDATE events SET payload='{}'")
            db.commit()
        with self.assertRaisesRegex(
            migration.MigrationBlocked, "audit_(invalid|not_append_only)"
        ):
            self.run_migration(True)

    def test_shared_lease_contention_blocks_without_audit_writes(self):
        with (
            machine_lease(self.root / ".runtime/llm-live-readiness/account.lock"),
            self.assertRaisesRegex(AccountBlocked, "account_lease_busy"),
        ):
            self.run_migration(True)
        self.assertFalse(migration.audit_path(self.root).exists())

    def test_linked_authorization_input_is_rejected(self):
        auth = self.root / migration.AUTH
        moved = auth.with_suffix(".moved")
        auth.rename(moved)
        try:
            auth.symlink_to(moved)
        except OSError:
            try:
                os.link(moved, auth)
            except OSError:
                moved.rename(auth)
                self.skipTest("filesystem does not permit links")
        with self.assertRaisesRegex(migration.MigrationBlocked, "linked_path"):
            self.run_migration(True)

    def test_idempotency_preserves_later_project_registration_and_usage(self):
        self.run_migration(True)
        account = SharedAccount(self.root, self.after)
        account.register("p02")
        attempt = account.reserve("p02", "local-operation-v1", "case", 1, 1, 100, 20)
        account.complete("p02", attempt, input_tokens=80, output_tokens=10)
        result = self.run_migration(True)
        self.assertIn("p02", result["projects"])
        self.assertEqual(result["usage"]["requests"], 2)
        self.assertEqual(len(migration.read_audit(self.root)), 2)


if __name__ == "__main__":
    unittest.main()
