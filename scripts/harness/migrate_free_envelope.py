"""Apply only the explicitly authorized ten-call free P00 policy amendment.

No credential/provider path exists here. Usage ledgers are always opened read-only.
The audit database records migration metadata, never provider consumption.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import sqlite3
import subprocess
from contextlib import closing
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

from live_free_account import (
    PROJECTS,
    ROOT,
    AccountBlocked,
    SharedAccount,
    machine_lease,
)

MIGRATION_ID = "p00-free-envelope-plus10-v1"
OLD_SHA = "ec7ccca5e2bece8cb677cab24dfd9822255bf9fbb791807f956837e62db5ce8d"
NEW_SHA = "1c87eb87ba3a653235aca546180602f288993e49424d6eecdedb01f4688c2a16"
P00_CAMPAIGN_SOURCE_SHA = "2acb058782c79ab66aa4dbec76afa1f0b8713819"
BASELINE = "artifacts/evidence/llm-live-readiness/envelope-migration/policy-before.json"
AUTH = (
    ".planning/llm-live-readiness/phases/005-free-envelope-migration/AUTHORIZATION.json"
)
PENDING_MARKER = ".runtime/llm-live-readiness/policy-migration.pending"
POLICY = "shared/policies/groq-free-campaign.json"
SOURCE_PATHS = (
    BASELINE,
    AUTH,
    ".planning/llm-live-readiness/phases/005-free-envelope-migration/SPEC.md",
    ".planning/llm-live-readiness/phases/005-free-envelope-migration/PLAN.md",
    ".planning/llm-live-readiness/phases/005-free-envelope-migration/VERIFY.md",
    "artifacts/evidence/llm-live-readiness/envelope-migration/plan-check.md",
    "artifacts/evidence/llm-live-readiness/envelope-migration/validate_plan.py",
    POLICY,
    ".planning/llm-live-readiness/AUTHORIZATION.md",
    "scripts/harness/migrate_free_envelope.py",
    "scripts/harness/live_free_account.py",
    "scripts/harness/live_provider_transport.py",
)


class MigrationBlocked(RuntimeError):
    """A fixed metadata-only stop reason."""


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def safe_path(root, path):
    root, path = root.resolve(), path.absolute()
    if not path.is_relative_to(root) or not path.resolve().is_relative_to(root):
        raise MigrationBlocked("migration_path_outside_root")
    for part in (path, *path.parents):
        if part == root:
            break
        if part.is_symlink() or part.is_junction():
            raise MigrationBlocked("migration_linked_path")
        if part.is_file() and part.stat().st_nlink != 1:
            raise MigrationBlocked("migration_linked_path")
    return path


def read_json(root, path):
    path = safe_path(root, path)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise MigrationBlocked("migration_json_unavailable") from None
    if not isinstance(value, dict):
        raise MigrationBlocked("migration_json_invalid")
    return value


def proposed_policy(before):
    if digest(before) != OLD_SHA:
        raise MigrationBlocked("migration_baseline_changed")
    after = copy.deepcopy(before)
    for caps in (after["campaign_caps"], after["projects"]["p00"]):
        for field, amount in (
            ("requests", 10),
            ("input_tokens", 20480),
            ("output_tokens", 2560),
        ):
            caps[field] += amount
        caps["estimated_cost_usd"] = str(
            Decimal(caps["estimated_cost_usd"]) + Decimal("0.002304")
        )
    if digest(after) != NEW_SHA:
        raise MigrationBlocked("migration_delta_invalid")
    return after


def require_inputs(root):
    before = read_json(root, root / BASELINE)
    after = read_json(root, root / POLICY)
    authorization = read_json(root, root / AUTH)
    expected = {
        "authorization_id": MIGRATION_ID,
        "authority": "explicit_user_reply",
        "project": "p00",
        "additional_calls": 10,
        "additional_input_tokens": 20480,
        "additional_output_tokens": 2560,
        "additional_economic_estimate_usd": "0.002304",
        "authorized_paid_spend_usd": "0.00",
        "free_only": True,
        "condition": "validated_owning_migration_phase",
        "other_project_caps_changed": False,
        "confirmation_changed": False,
        "human_dataset_rubric_independent_review": "PENDING",
        "promotion": "PENDING",
    }
    if any(authorization.get(key) != value for key, value in expected.items()):
        raise MigrationBlocked("migration_authorization_invalid")
    if after != proposed_policy(before):
        raise MigrationBlocked("migration_unapproved_policy_delta")
    for name in SOURCE_PATHS:
        safe_path(root, root / name)
    for command in (
        ["git", "ls-files", "--error-unmatch", "--", *SOURCE_PATHS],
        ["git", "diff", "--quiet", "HEAD", "--", *SOURCE_PATHS],
    ):
        if subprocess.run(
            command, check=False, cwd=root, capture_output=True, timeout=15
        ).returncode:
            raise MigrationBlocked("migration_inputs_not_committed")
    p00 = root / "projects/p00"
    source = "scripts/campaign_execution.py"
    if not safe_path(root, p00 / source).is_file():
        raise MigrationBlocked("migration_p00_campaign_source_unavailable")
    for command in (
        ["git", "-C", str(p00), "ls-files", "--error-unmatch", "--", source],
        ["git", "-C", str(p00), "diff", "--quiet", "HEAD", "--", source],
    ):
        if subprocess.run(
            command, check=False, cwd=p00, capture_output=True, timeout=15
        ).returncode:
            raise MigrationBlocked("migration_p00_campaign_source_not_committed")
    blob = subprocess.run(
        ["git", "-C", str(p00), "rev-parse", f"HEAD:{source}"],
        check=False,
        cwd=p00,
        capture_output=True,
        timeout=15,
        text=True,
    )
    if blob.returncode or blob.stdout.strip() != P00_CAMPAIGN_SOURCE_SHA:
        raise MigrationBlocked("migration_p00_campaign_source_changed")
    SharedAccount(root, before)
    SharedAccount(root, after)
    return before, after


def audit_path(root):
    return safe_path(
        root, root / ".runtime/llm-live-readiness/policy-migrations.sqlite"
    )


def marker_path(root):
    return safe_path(root, root / PENDING_MARKER)


def marker_bytes():
    return json.dumps(
        {
            "migration_id": MIGRATION_ID,
            "old_policy_sha256": OLD_SHA,
            "new_policy_sha256": NEW_SHA,
        },
        sort_keys=True,
    ).encode("utf-8")


def ensure_marker(root, *, create):
    path = marker_path(root)
    if path.exists():
        if not path.is_file() or path.read_bytes() != marker_bytes():
            raise MigrationBlocked("migration_pending_marker_invalid")
        return path
    if not create:
        raise MigrationBlocked("migration_pending_marker_missing")
    with path.open("xb") as stream:
        stream.write(marker_bytes())
        stream.flush()
        os.fsync(stream.fileno())
    return path


def read_audit(root):
    path = audit_path(root)
    if not path.exists():
        return []
    try:
        with closing(sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)) as db:
            rows = db.execute(
                "SELECT migration_id,event,payload FROM events ORDER BY sequence"
            ).fetchall()
            triggers = {
                name: " ".join(sql.lower().split())
                for name, sql in db.execute(
                    "SELECT name,sql FROM sqlite_master WHERE type='trigger'"
                )
            }
    except sqlite3.Error:
        raise MigrationBlocked("migration_audit_invalid") from None
    for name, action in (
        ("no_migration_update", "before update on events"),
        ("no_migration_delete", "before delete on events"),
    ):
        sql = triggers.get(name, "")
        if action not in sql or "raise(abort,'append-only migration audit')" not in sql:
            raise MigrationBlocked("migration_audit_not_append_only")
    records = []
    for migration_id, event, payload in rows:
        if migration_id != MIGRATION_ID:
            raise MigrationBlocked("migration_audit_unknown_event")
        try:
            data = json.loads(payload)
        except (ValueError, TypeError):
            raise MigrationBlocked("migration_audit_invalid") from None
        if (
            event not in {"prepared", "applied"}
            or not isinstance(data, dict)
            or data.get("old_policy_sha256") != OLD_SHA
            or data.get("new_policy_sha256") != NEW_SHA
        ):
            raise MigrationBlocked("migration_audit_invalid")
        records.append((event, data))
    if [event for event, _ in records] not in (
        [],
        ["prepared"],
        ["prepared", "applied"],
    ):
        raise MigrationBlocked("migration_audit_sequence_invalid")
    if len(records) == 2:
        prepared, applied = records[0][1], records[1][1]
        if {
            key: value for key, value in applied.items() if key != "verified_usage"
        } != prepared or applied.get("verified_usage") != prepared.get("usage_before"):
            raise MigrationBlocked("migration_audit_continuity_invalid")
    return records


def append_audit(root, event, payload):
    path = audit_path(root)
    # Existing stores must be readable before any append; never recreate/reset one.
    if path.exists():
        read_audit(root)
    with closing(sqlite3.connect(path)) as db:
        db.execute("PRAGMA synchronous=FULL")
        db.executescript("""
            CREATE TABLE IF NOT EXISTS events(
              sequence INTEGER PRIMARY KEY AUTOINCREMENT,
              migration_id TEXT NOT NULL,
              event TEXT NOT NULL CHECK(event IN ('prepared','applied')),
              payload TEXT NOT NULL, created_at_utc TEXT NOT NULL,
              UNIQUE(migration_id,event));
            CREATE TRIGGER IF NOT EXISTS no_migration_update BEFORE UPDATE ON events
              BEGIN SELECT RAISE(ABORT,'append-only migration audit'); END;
            CREATE TRIGGER IF NOT EXISTS no_migration_delete BEFORE DELETE ON events
              BEGIN SELECT RAISE(ABORT,'append-only migration audit'); END;
        """)
        db.execute(
            "INSERT INTO events(migration_id,event,payload,created_at_utc) VALUES(?,?,?,?)",
            (
                MIGRATION_ID,
                event,
                json.dumps(payload, sort_keys=True),
                datetime.now(UTC).isoformat(),
            ),
        )
        db.commit()


def read_rows(root, path, table):
    path = safe_path(root, path)
    if not path.exists():
        return None
    try:
        with closing(sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)) as db:
            db.row_factory = sqlite3.Row
            return [
                dict(row)
                for row in db.execute("SELECT * FROM " + table + " ORDER BY sequence")
            ]
    except sqlite3.Error:
        raise MigrationBlocked("migration_history_unreadable") from None


def validate_logical_history(rows):
    latest = {}
    keys = ("project", "campaign_id", "case_id", "trial")
    reservation_fields = (
        "reserved_calls",
        "reserved_input_tokens",
        "reserved_output_tokens",
        "reserved_cost_usd",
    )
    for row in rows:
        key = tuple(row[field] for field in keys)
        if row["event"] == "reserved":
            if key in latest:
                raise MigrationBlocked("migration_logical_history_invalid")
        elif (
            row["event"] != "completed"
            or key not in latest
            or latest[key]["event"] != "reserved"
        ) or any(row[field] != latest[key][field] for field in reservation_fields):
            raise MigrationBlocked("migration_logical_history_invalid")
        latest[key] = row
    if any(row["event"] == "reserved" for row in latest.values()):
        raise MigrationBlocked("migration_inflight_or_uncertain_attempt")


def snapshot(root, policy):
    registry_path = safe_path(
        root, root / ".runtime/llm-live-readiness/ledger-references.json"
    )
    registry = read_json(root, registry_path)
    account = SharedAccount(root, policy, allow_pending_migration=True)
    for project in PROJECTS:
        safe_path(root, account.path(project))
    attempts = account._history()
    if any(row["event"] == "reserved" for row in attempts):
        raise MigrationBlocked("migration_inflight_or_uncertain_attempt")
    provider, logical = {}, {}
    for project in PROJECTS:
        identity, rows = account._read(project)
        if identity is not None:
            provider[project] = {"uuid": identity, "rows": rows}
        rows = read_rows(
            root,
            root / "projects" / project / "artifacts/evals/live/ledger.sqlite",
            "events",
        )
        if rows is not None:
            validate_logical_history(rows)
            logical[project] = {"rows": rows}
    usage = {
        field: sum(account.usage(row)[field] for row in attempts)
        for field in ("requests", "input_tokens", "output_tokens", "estimated_cost_usd")
    }
    usage["estimated_cost_usd"] = str(usage["estimated_cost_usd"])
    usage["unknown_usage_attempts"] = sum(
        row["actual_input"] is None or row["actual_output"] is None for row in attempts
    )
    prefixes = {}
    for label, ledgers in (("provider", provider), ("logical", logical)):
        prefixes[label] = {
            project: {
                "event_count": len(data["rows"]),
                "events_sha256": digest(data["rows"]),
                **({"uuid": data["uuid"]} if "uuid" in data else {}),
            }
            for project, data in ledgers.items()
        }
    return {
        "registry": registry,
        "provider": provider,
        "logical": logical,
        "prefixes": prefixes,
        "usage": usage,
    }


def verify_prefixes(prepared, current):
    for project, identity in prepared["projects"].items():
        if current["registry"]["projects"].get(project) != identity:
            raise MigrationBlocked("migration_uuid_changed")
    for label in ("provider", "logical"):
        for project, old in prepared["prefixes"][label].items():
            now = current[label].get(project)
            if (
                now is None
                or len(now["rows"]) < old["event_count"]
                or digest(now["rows"][: old["event_count"]]) != old["events_sha256"]
                or ("uuid" in old and old["uuid"] != now.get("uuid"))
            ):
                raise MigrationBlocked("migration_history_changed")


def metadata(current, state):
    return {
        "status": state,
        "migration_id": MIGRATION_ID,
        "old_policy_sha256": OLD_SHA,
        "new_policy_sha256": NEW_SHA,
        "projects": current["registry"]["projects"],
        "usage": current["usage"],
        "ledger_prefixes": current["prefixes"],
        "provider_accessed": False,
        "credentials_read": False,
        "authorized_paid_spend_usd": "0.00",
        "actual_billed_usd": None,
        "human_independent_dataset_rubric_review": "PENDING",
        "promotion": "PENDING",
    }


def migrate(root=ROOT, *, apply=False):
    root = Path(root).resolve()
    before, after = require_inputs(root)
    registry_path = safe_path(
        root, root / ".runtime/llm-live-readiness/ledger-references.json"
    )
    lock_path = safe_path(root, root / ".runtime/llm-live-readiness/account.lock")
    campaign_lock = safe_path(
        root,
        root / ".runtime/llm-live-readiness/campaign.lock",
    )

    def inspect_and_apply():
        registry = read_json(root, registry_path)
        sha = registry.get("policy_sha256")
        if sha not in {OLD_SHA, NEW_SHA}:
            raise MigrationBlocked("migration_registry_policy_unknown")
        records = read_audit(root)
        current = snapshot(root, before if sha == OLD_SHA else after)
        prepared = records[0][1] if records else None
        applied = len(records) == 2
        pending = marker_path(root).exists()
        if pending:
            ensure_marker(root, create=False)
        if sha == NEW_SHA:
            if prepared is None:
                raise MigrationBlocked("migration_new_registry_without_audit")
            if applied and not pending:
                verify_prefixes(prepared, current)
                return metadata(current, "ALREADY_APPLIED")
            ensure_marker(root, create=False)
            verify_prefixes(prepared, current)
            if apply:
                if not applied:
                    append_audit(
                        root,
                        "applied",
                        {**prepared, "verified_usage": current["usage"]},
                    )
                marker_path(root).unlink()
            return metadata(
                current,
                "RECOVERED_APPLIED" if apply else "READY_TO_RECOVER_APPLIED",
            )
        if applied:
            raise MigrationBlocked("migration_registry_rollback_detected")
        payload = {
            "authorization_id": MIGRATION_ID,
            "old_policy_sha256": OLD_SHA,
            "new_policy_sha256": NEW_SHA,
            "projects": registry["projects"],
            "prefixes": current["prefixes"],
            "usage_before": current["usage"],
        }
        if prepared is not None and prepared != payload:
            raise MigrationBlocked("migration_prepared_state_changed")
        if pending and prepared is None:
            raise MigrationBlocked("migration_pending_marker_without_audit")
        if not apply:
            return metadata(current, "READY_FOR_APPROVED_MIGRATION")
        if prepared is None:
            append_audit(root, "prepared", payload)
        ensure_marker(root, create=True)
        temporary = safe_path(
            root,
            root / ".runtime/llm-live-readiness/ledger-references.policy-migration.tmp",
        )
        encoded = json.dumps(
            {**registry, "policy_sha256": NEW_SHA}, sort_keys=True
        ).encode("utf-8")
        if temporary.exists():
            if temporary.read_bytes() != encoded:
                raise MigrationBlocked("migration_unexpected_temporary_state")
        else:
            with temporary.open("xb") as stream:
                stream.write(encoded)
                stream.flush()
                os.fsync(stream.fileno())
        os.replace(temporary, registry_path)
        verified = snapshot(root, after)
        verify_prefixes(payload, verified)
        if (
            verified["prefixes"] != current["prefixes"]
            or verified["usage"] != current["usage"]
            or verified["registry"]["projects"] != registry["projects"]
        ):
            raise MigrationBlocked("migration_post_commit_state_changed")
        append_audit(root, "applied", {**payload, "verified_usage": verified["usage"]})
        marker_path(root).unlink()
        return metadata(verified, "APPLIED")

    # Read-only SQLite connections to WAL databases may create transient -wal/-shm
    # coordination files. Hold the account lease and remove only auxiliary files
    # that did not exist before this inspection, after every connection has closed.
    with machine_lease(campaign_lock), machine_lease(lock_path):
        require_inputs(root)
        auxiliaries = []
        for project in PROJECTS:
            for base in (
                root / ".runtime/llm-live-readiness" / f"{project}.sqlite",
                root
                / "projects"
                / project
                / "artifacts/evals/live/provider-usage.sqlite",
                root / "projects" / project / "artifacts/evals/live/ledger.sqlite",
            ):
                for suffix in ("-wal", "-shm"):
                    candidate = safe_path(root, Path(str(base) + suffix))
                    auxiliaries.append((candidate, candidate.exists()))
        try:
            return inspect_and_apply()
        finally:
            for path, existed in auxiliaries:
                if (
                    not existed
                    and path.exists()
                    and path.is_file()
                    and not path.is_symlink()
                ):
                    path.unlink()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = migrate(apply=args.apply)
    except (MigrationBlocked, AccountBlocked) as error:
        print(
            json.dumps(
                {
                    "status": "INCOMPLETE",
                    "reason": str(error),
                    "provider_accessed": False,
                    "credentials_read": False,
                }
            )
        )
        return 2
    except (
        OSError,
        sqlite3.Error,
        ValueError,
        TypeError,
        KeyError,
        RuntimeError,
        subprocess.SubprocessError,
    ):
        print(
            json.dumps(
                {
                    "status": "INCOMPLETE",
                    "reason": "migration_interrupted_inspect_registry_and_audit",
                    "provider_accessed": False,
                    "credentials_read": False,
                }
            )
        )
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
