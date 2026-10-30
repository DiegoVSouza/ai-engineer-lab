#!/usr/bin/env python3
"""Shared free-only limits over authoritative per-project provider usage logs."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import random
import sqlite3
import subprocess
import sys
import time
import uuid
from contextlib import closing, contextmanager
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parents[2]
PROJECTS = tuple(f"p{number:02d}" for number in range(6))
MODEL = "openai/gpt-oss-20b"
COUNTERS = ("requests", "input_tokens", "output_tokens", "estimated_cost_usd")
FEEDBACK = {
    "request_limit",
    "token_limit",
    "remaining_requests",
    "remaining_tokens",
    "request_reset_seconds",
    "token_reset_seconds",
    "retry_after_seconds",
}


class AccountBlocked(RuntimeError):
    """A sanitized fail-closed reason, never a provider/credential exception."""


def integer(value, minimum=0):
    if type(value) is not int or value < minimum:
        raise AccountBlocked("invalid_resource_count")
    return value


def duration(value):
    if not isinstance(value, str):
        return None
    try:
        result = float(value)
    except ValueError:
        parts = re.findall(r"(\d+(?:\.\d+)?)(ms|s|m|h)", value)
        if not parts or "".join(number + unit for number, unit in parts) != value:
            return None
        result = sum(
            float(number) * {"ms": 0.001, "s": 1, "m": 60, "h": 3600}[unit]
            for number, unit in parts
        )
    return result if math.isfinite(result) and 0 <= result <= 86400 else None


def feedback(headers):
    """Return only numeric, allowlisted Groq rate-limit fields."""
    normalized = {}
    headers = {str(key).lower(): value for key, value in headers.items()}
    for header, field in {
        "x-ratelimit-limit-requests": "request_limit",
        "x-ratelimit-limit-tokens": "token_limit",
        "x-ratelimit-remaining-requests": "remaining_requests",
        "x-ratelimit-remaining-tokens": "remaining_tokens",
    }.items():
        value = headers.get(header)
        if isinstance(value, str) and value.isascii() and value.isdigit():
            normalized[field] = int(value)
    for header, field in {
        "x-ratelimit-reset-requests": "request_reset_seconds",
        "x-ratelimit-reset-tokens": "token_reset_seconds",
        "retry-after": "retry_after_seconds",
    }.items():
        seconds = duration(headers.get(header))
        if seconds is not None:
            normalized[field] = seconds
    return normalized


def money(value):
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise AccountBlocked("invalid_estimated_cost") from None
    if not result.is_finite() or result < 0:
        raise AccountBlocked("invalid_estimated_cost")
    return result


@contextmanager
def machine_lease(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open("a+b")
    locked = False
    try:
        handle.seek(0, 2)
        if not handle.tell():
            handle.write(b"\0")
            handle.flush()
        handle.seek(0)
        try:
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise AccountBlocked("account_lease_busy") from None
        locked = True
        yield
    finally:
        if locked:
            handle.seek(0)
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()


class SharedAccount:
    def __init__(
        self,
        root: Path,
        policy: dict,
        *,
        clock=time.time,
        allow_pending_migration=False,
    ):
        self.root = root.resolve()
        self.policy = policy
        self.clock = clock
        self.runtime = self.root / ".runtime/llm-live-readiness"
        self.lock = self.runtime / "account.lock"
        self.registry = self.runtime / "ledger-references.json"
        self.pending_migration = self.runtime / "policy-migration.pending"
        self.allow_pending_migration = allow_pending_migration
        self.authenticated_feedback = {}
        if (
            policy.get("model") != MODEL
            or money(policy.get("authorized_paid_spend_usd")) != 0
        ):
            raise AccountBlocked("free_only_policy_required")
        if set(policy.get("projects", {})) != set(PROJECTS):
            raise AccountBlocked("all_six_projects_required")
        for caps in [policy["campaign_caps"], *policy["projects"].values()]:
            for field in COUNTERS[:-1]:
                integer(caps[field], 1)
            money(caps[COUNTERS[-1]])
        for project, caps in policy["projects"].items():
            original_input = 2048 if project in {"p00", "p01"} else 4096
            original_output = 256 if project in {"p00", "p01"} else 512
            if (
                integer(caps["input_tokens_per_call"], 1) > original_input
                or integer(caps["output_tokens_per_call"], 1) > original_output
            ):
                raise AccountBlocked("original_per_call_caps_exceeded")
            if (
                integer(caps["calls_per_trial"], 1)
                > {"p00": 1, "p01": 4, "p02": 1, "p03": 1, "p04": 3, "p05": 4}[project]
            ):
                raise AccountBlocked("original_trial_call_cap_exceeded")
        money(policy["pricing_per_million"]["input_usd"])
        money(policy["pricing_per_million"]["output_usd"])
        published = {
            "requests_per_minute": 30,
            "requests_per_day": 1000,
            "tokens_per_minute": 8000,
            "tokens_per_day": 200000,
        }
        for field, maximum in published.items():
            if integer(policy["free_limits"][field], 1) > maximum:
                raise AccountBlocked("free_plan_ceiling_exceeded")
        self.policy_hash = hashlib.sha256(
            json.dumps(policy, sort_keys=True).encode()
        ).hexdigest()

    def path(self, project):
        if project not in PROJECTS:
            raise AccountBlocked("unregistered_project")
        return (
            self.root
            / "projects"
            / project
            / "artifacts/evals/live/provider-usage.sqlite"
        )

    def _references(self):
        pending_exists = (
            self.pending_migration.exists()
            or self.pending_migration.is_symlink()
            or self.pending_migration.is_junction()
        )
        if pending_exists and not self.allow_pending_migration:
            raise AccountBlocked("policy_migration_pending")
        if not self.registry.exists():
            return {}
        try:
            data = json.loads(self.registry.read_text(encoding="utf-8"))
            if data["policy_sha256"] != self.policy_hash or not set(
                data["projects"]
            ) <= set(PROJECTS):
                raise AccountBlocked("account_policy_or_registry_changed")
            return data["projects"]
        except (OSError, ValueError, KeyError, TypeError):
            raise AccountBlocked("invalid_account_registry") from None

    def _read(self, project):
        path = self.path(project)
        if not path.exists():
            return None, []
        try:
            with closing(sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)) as db:
                db.row_factory = sqlite3.Row
                identity = db.execute("SELECT identity FROM identity").fetchall()
                if len(identity) != 1:
                    raise AccountBlocked("invalid_project_ledger_identity")
                rows = [
                    dict(row)
                    for row in db.execute(
                        "SELECT * FROM usage_events ORDER BY sequence"
                    )
                ]
            return identity[0][0], rows
        except sqlite3.Error:
            raise AccountBlocked("unreadable_project_usage_ledger") from None

    def _history(self):
        references = self._references()
        attempts = []
        for project in PROJECTS:
            identity, rows = self._read(project)
            if project in references and identity != references[project]:
                raise AccountBlocked("registered_project_ledger_missing_or_replaced")
            if project not in references and rows:
                raise AccountBlocked("usage_exists_without_registry_reference")
            latest = {}
            for row in rows:
                attempt = row["attempt_id"]
                if row["event"] == "reserved":
                    if attempt in latest:
                        raise AccountBlocked("duplicate_usage_reservation")
                elif (
                    row["event"] != "completed"
                    or attempt not in latest
                    or latest[attempt]["event"] != "reserved"
                ):
                    raise AccountBlocked("orphan_or_duplicate_usage_outcome")
                if row["event"] == "completed" and any(
                    row[field] != latest[attempt][field]
                    for field in (
                        "ordinal",
                        "campaign",
                        "case_id",
                        "trial",
                        "call_index",
                        "reserved_at",
                        "reserved_input",
                        "reserved_output",
                        "reserved_cost",
                    )
                ):
                    raise AccountBlocked("reservation_metadata_changed")
                if (row["event"] == "reserved" and row["status"] is not None) or (
                    row["event"] == "completed"
                    and row["status"]
                    not in {
                        "ok",
                        "provider_error",
                        "transport_error",
                        "quota",
                        "model_mismatch",
                    }
                ):
                    raise AccountBlocked("invalid_usage_event_status")
                integer(row["ordinal"], 1)
                for field in ("reserved_input", "reserved_output"):
                    integer(row[field], 1)
                money(row["reserved_cost"])
                for field in ("actual_input", "actual_output"):
                    if row[field] is not None:
                        integer(row[field])
                if row["actual_cost"] is not None:
                    money(row["actual_cost"])
                if not math.isfinite(row["reserved_at"]) or row["reserved_at"] < 0:
                    raise AccountBlocked("invalid_usage_timestamp")
                latest[attempt] = {**row, "project": project}
            attempts.extend(latest.values())
        if sorted(row["ordinal"] for row in attempts) != list(
            range(1, len(attempts) + 1)
        ):
            raise AccountBlocked("usage_sequence_gap_or_duplicate")
        return attempts

    def register(self, project):
        """Initialize only an owning project's log, before any provider call."""
        path = self.path(project)
        with machine_lease(self.lock):
            self._history()
            refs = self._references()
            if project in refs:
                return
            path.parent.mkdir(parents=True, exist_ok=True)
            with closing(sqlite3.connect(path)) as db:
                db.execute("PRAGMA journal_mode=WAL")
                db.execute("PRAGMA synchronous=FULL")
                db.executescript("""
                    CREATE TABLE IF NOT EXISTS identity(identity TEXT PRIMARY KEY);
                    CREATE TABLE IF NOT EXISTS usage_events(
                      sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                      attempt_id TEXT NOT NULL, event TEXT NOT NULL,
                      ordinal INTEGER NOT NULL, campaign TEXT NOT NULL, case_id TEXT NOT NULL,
                      trial INTEGER NOT NULL, call_index INTEGER NOT NULL, reserved_at REAL NOT NULL,
                      reserved_input INTEGER NOT NULL, reserved_output INTEGER NOT NULL,
                      reserved_cost TEXT NOT NULL, actual_input INTEGER, actual_output INTEGER,
                      actual_cost TEXT, status TEXT, feedback TEXT,
                      UNIQUE(attempt_id,event), UNIQUE(campaign,case_id,trial,call_index,event));
                    CREATE TRIGGER IF NOT EXISTS no_usage_update BEFORE UPDATE ON usage_events
                      BEGIN SELECT RAISE(ABORT,'append-only usage'); END;
                    CREATE TRIGGER IF NOT EXISTS no_usage_delete BEFORE DELETE ON usage_events
                      BEGIN SELECT RAISE(ABORT,'append-only usage'); END;
                """)
                if not db.execute("SELECT 1 FROM identity").fetchone():
                    db.execute("INSERT INTO identity VALUES(?)", (uuid.uuid4().hex,))
                identity = db.execute("SELECT identity FROM identity").fetchone()[0]
                db.commit()
            refs[project] = identity
            self.runtime.mkdir(parents=True, exist_ok=True)
            temporary = self.registry.with_suffix(".tmp")
            with temporary.open("w", encoding="utf-8", newline="\n") as stream:
                json.dump(
                    {"policy_sha256": self.policy_hash, "projects": refs},
                    stream,
                    sort_keys=True,
                )
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.registry)

    @staticmethod
    def usage(row):
        return {
            "requests": 1,
            "input_tokens": row["actual_input"]
            if row["actual_input"] is not None
            else row["reserved_input"],
            "output_tokens": row["actual_output"]
            if row["actual_output"] is not None
            else row["reserved_output"],
            "estimated_cost_usd": money(
                row["actual_cost"]
                if row["actual_cost"] is not None
                else row["reserved_cost"]
            ),
        }

    def _check(self, rows, project, reservation):
        now = self.clock()
        if type(now) not in (int, float) or not math.isfinite(now) or now < 0:
            raise AccountBlocked("invalid_account_clock")
        for selected, caps in (
            (rows, self.policy["campaign_caps"]),
            (
                [row for row in rows if row["project"] == project],
                self.policy["projects"][project],
            ),
        ):
            for field in COUNTERS:
                total = (
                    sum(self.usage(row)[field] for row in selected) + reservation[field]
                )
                cap = (
                    money(caps[field]) if field == "estimated_cost_usd" else caps[field]
                )
                if total > cap:
                    raise AccountBlocked("cumulative_account_or_project_cap")
        limits = dict(self.policy["free_limits"])
        for row in rows:
            actual = self.usage(row)
            if row["status"] == "model_mismatch":
                raise AccountBlocked("provider_model_mismatch_requires_review")
            if (
                actual["input_tokens"] > row["reserved_input"]
                or actual["output_tokens"] > row["reserved_output"]
                or actual["estimated_cost_usd"] > money(row["reserved_cost"])
            ):
                raise AccountBlocked("accounting_overrun_requires_reconciliation")
            feedback = json.loads(row["feedback"]) if row["feedback"] else {}
            if feedback.get("request_limit") is not None:
                limits["requests_per_day"] = min(
                    limits["requests_per_day"], feedback["request_limit"]
                )
            if feedback.get("token_limit") is not None:
                limits["tokens_per_minute"] = min(
                    limits["tokens_per_minute"], feedback["token_limit"]
                )
            observed = feedback.get("observed_at", 0)
            if now < observed + feedback.get("retry_after_seconds", 0):
                raise AccountBlocked("provider_cooldown_checkpoint")
            later = [
                r
                for r in rows
                if r["ordinal"] > feedback.get("account_ordinal", len(rows))
            ]
            if (
                "remaining_requests" in feedback
                and now < observed + feedback.get("request_reset_seconds", 86400)
                and len(later) + 1 > feedback["remaining_requests"]
            ):
                raise AccountBlocked("provider_request_capacity_checkpoint")
            if "remaining_tokens" in feedback and now < observed + feedback.get(
                "token_reset_seconds", 60
            ):
                charged = sum(
                    self.usage(r)["input_tokens"] + self.usage(r)["output_tokens"]
                    for r in later
                )
                if (
                    charged + reservation["input_tokens"] + reservation["output_tokens"]
                    > feedback["remaining_tokens"]
                ):
                    raise AccountBlocked("provider_token_capacity_checkpoint")
        preflight = self.authenticated_feedback
        if preflight.get("request_limit") is not None:
            limits["requests_per_day"] = min(
                limits["requests_per_day"], preflight["request_limit"]
            )
        if preflight.get("token_limit") is not None:
            limits["tokens_per_minute"] = min(
                limits["tokens_per_minute"], preflight["token_limit"]
            )
        observed = preflight.get("observed_at", 0)
        if now < observed + preflight.get("retry_after_seconds", 0):
            raise AccountBlocked("provider_cooldown_checkpoint")
        later = [
            row
            for row in rows
            if row["ordinal"] > preflight.get("account_ordinal", len(rows))
        ]
        if (
            "remaining_requests" in preflight
            and now < observed + preflight.get("request_reset_seconds", 86400)
            and len(later) + 1 > preflight["remaining_requests"]
        ):
            raise AccountBlocked("provider_request_capacity_checkpoint")
        if "remaining_tokens" in preflight and now < observed + preflight.get(
            "token_reset_seconds", 60
        ):
            charged = sum(
                self.usage(row)["input_tokens"] + self.usage(row)["output_tokens"]
                for row in later
            )
            if (
                charged + reservation["input_tokens"] + reservation["output_tokens"]
                > preflight["remaining_tokens"]
            ):
                raise AccountBlocked("provider_token_capacity_checkpoint")
        for seconds, suffix in ((60, "minute"), (86400, "day")):
            active = [row for row in rows if row["reserved_at"] >= now - seconds]
            if len(active) + 1 > limits[f"requests_per_{suffix}"]:
                raise AccountBlocked(f"free_request_{suffix}_checkpoint")
            total = sum(
                self.usage(row)["input_tokens"] + self.usage(row)["output_tokens"]
                for row in active
            )
            if (
                total + reservation["input_tokens"] + reservation["output_tokens"]
                > limits[f"tokens_per_{suffix}"]
            ):
                raise AccountBlocked(f"free_token_{suffix}_checkpoint")

    def set_authenticated_feedback(self, values):
        """Bind sanitized authenticated headers to this process's dispatch guard."""
        if not isinstance(values, dict) or set(values) - FEEDBACK:
            raise AccountBlocked("invalid_authenticated_rate_feedback")
        clean = {}
        integer_fields = {
            "request_limit": 1,
            "token_limit": 1,
            "remaining_requests": 0,
            "remaining_tokens": 0,
        }
        for name, minimum in integer_fields.items():
            if name in values:
                clean[name] = integer(values[name], minimum)
        for name in (
            "request_reset_seconds",
            "token_reset_seconds",
            "retry_after_seconds",
        ):
            if name in values:
                value = values[name]
                if (
                    type(value) not in (int, float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 86400
                ):
                    raise AccountBlocked("invalid_authenticated_rate_feedback")
                clean[name] = float(value)
        with machine_lease(self.lock):
            rows = self._history()
            clean["observed_at"] = self.clock()
            clean["account_ordinal"] = len(rows)
            self.authenticated_feedback = clean

    def _prepare_reservation(
        self, project, campaign, case_id, trial, call_index, input_tokens, output_tokens
    ):
        caps = self.policy["projects"].get(project)
        if caps is None or any(
            not isinstance(value, str)
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}", value)
            for value in (campaign, case_id)
        ):
            raise AccountBlocked("invalid_attempt_identity")
        if integer(trial, 1) > 3 or integer(call_index, 1) > caps["calls_per_trial"]:
            raise AccountBlocked("attempt_limit_exceeded")
        if (
            integer(input_tokens, 1) > caps["input_tokens_per_call"]
            or integer(output_tokens, 1) > caps["output_tokens_per_call"]
        ):
            raise AccountBlocked("per_call_token_cap")
        price = self.policy["pricing_per_million"]
        cost = (
            input_tokens * money(price["input_usd"])
            + output_tokens * money(price["output_usd"])
        ) / 1000000
        return cost

    def _approve(
        self,
        project,
        campaign,
        case_id,
        trial,
        call_index,
        input_tokens,
        output_tokens,
        cost,
        *,
        reservation=False,
    ):
        rows = self._history()
        if project not in self._references():
            raise AccountBlocked("owning_project_not_initialized")
        if project in {"p01", "p04"} and campaign == "local-operation-v1":
            logical = self.root / ("projects/" + project + "/artifacts/evals/live/ledger.sqlite")
            if logical.exists():
                try:
                    with closing(sqlite3.connect(logical.resolve().as_uri() + "?mode=ro", uri=True)) as db:
                        stopped = db.execute("SELECT 1 FROM events WHERE campaign_id='local-operation-v1' AND event='completed' AND outcome!='ok'").fetchone()
                except sqlite3.Error:
                    raise AccountBlocked("unreadable_logical_operation_history") from None
                if stopped:
                    raise AccountBlocked("logical_operation_stopped_requires_review")
        if project == "p00" and self.policy["projects"]["p00"]["requests"] == 219:
            if campaign != "local-live-operation-v1":
                raise AccountBlocked("protected_p00_allocation")
            p00 = [row for row in rows if row["project"] == "p00"]
            operation = [row for row in p00 if row["campaign"] == campaign]
            if len(p00) >= 75 or len(operation) >= 10:
                raise AccountBlocked("operational_allocation_exhausted")
        expanded = {"p01": 1000, "p04": 747}
        if project in expanded and self.policy["projects"][project]["requests"] == expanded[project]:
            self._reviewed_revalidation(
                rows, project, campaign, case_id, trial, call_index, reservation
            )
        if project == "p01" and self.policy["projects"]["p01"]["requests"] in {992, 996}:
            if campaign == "local-diagnostic-2-v1" and self.policy["projects"]["p01"]["requests"] == 996:
                self._reviewed_p01_second_diagnostic(rows, case_id, trial)
            elif campaign == "local-diagnostic-v1":
                self._reviewed_p01_diagnostic(rows, case_id, trial)
            elif campaign != "local-operation-v1":
                raise AccountBlocked("protected_p01_allocation")
            operation_p01 = [row for row in rows if row["project"] == "p01" and row["campaign"] in {"local-operation-v1", "local-diagnostic-v1", "local-diagnostic-2-v1"}]
            if len(operation_p01) >= (6 if campaign in {"local-diagnostic-v1", "local-diagnostic-2-v1"} else 8):
                raise AccountBlocked("operational_allocation_exhausted")
        if project == "p02" and self.policy["projects"]["p02"]["requests"] == 310:
            if campaign != "local-operation-v1":
                raise AccountBlocked("protected_p02_allocation")
            operation_p02 = [row for row in rows if row["project"] == "p02" and row["campaign"] == campaign]
            if len(operation_p02) >= 4:
                raise AccountBlocked("operational_allocation_exhausted")
            if any(row["event"] == "completed" and row["status"] != "ok" for row in operation_p02):
                raise AccountBlocked("prior_operational_failure_requires_review")
        if project == "p03" and self.policy["projects"]["p03"]["requests"] == 160:
            if campaign != "local-operation-v1":
                raise AccountBlocked("protected_p03_allocation")
            operation_p03 = [row for row in rows if row["project"] == "p03" and row["campaign"] == campaign]
            if len(operation_p03) >= 4:
                raise AccountBlocked("operational_allocation_exhausted")
            if any(row["event"] == "completed" and row["status"] != "ok" for row in operation_p03):
                raise AccountBlocked("prior_operational_failure_requires_review")
        service_operations = {"p04": (744, 6), "p05": (1712, 8)}
        if project in service_operations and self.policy["projects"][project]["requests"] == service_operations[project][0]:
            if project == "p04" and campaign == "local-diagnostic-v1":
                self._reviewed_p04_diagnostic(rows, case_id, trial)
            elif campaign != "local-operation-v1":
                raise AccountBlocked("protected_" + project + "_allocation")
            service_rows = [row for row in rows if row["project"] == project and row["campaign"] in ({"local-operation-v1", "local-diagnostic-v1"} if project == "p04" else {campaign})]
            if len(service_rows) >= (4 if project == "p04" and campaign == "local-diagnostic-v1" else service_operations[project][1]):
                raise AccountBlocked("operational_allocation_exhausted")
            if any(row["event"] == "completed" and row["status"] != "ok" for row in service_rows):
                raise AccountBlocked("prior_operational_failure_requires_review")
        if any(row["event"] == "reserved" for row in rows):
            raise AccountBlocked("uncertain_attempt_requires_reconciliation")
        if any(
            row["project"] == project
            and (row["campaign"], row["case_id"], row["trial"], row["call_index"])
            == (campaign, case_id, trial, call_index)
            for row in rows
        ):
            raise AccountBlocked("attempt_already_reserved_or_completed")
        self._check(
            rows,
            project,
            {
                "requests": 1,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "estimated_cost_usd": cost,
            },
        )
        if project == "p00" and self.policy["projects"]["p00"]["requests"] == 219:
            if any(row["event"] == "completed" and row["status"] != "ok" for row in operation):
                raise AccountBlocked("prior_operational_failure_requires_review")
        if project == "p01" and self.policy["projects"]["p01"]["requests"] in {992, 996}:
            if any(row["event"] == "completed" and row["status"] != "ok" for row in operation_p01):
                raise AccountBlocked("prior_operational_failure_requires_review")
        return rows

    def _reviewed_revalidation(
        self, rows, project, campaign, case_id, trial, call_index, reservation
    ):
        """Permit only the approved new workflow against exact retained history."""
        scopes = {
            "p01": ("local-reviewed-operation-027-v1", "fixture-reviewed-operation-027", 1),
            "p04": ("local-reviewed-operation-038-v1", "fixture-reviewed-operation-038", 1),
        }
        if (campaign, case_id, trial) != scopes.get(project):
            raise AccountBlocked("reviewed_revalidation_scope_required")
        name = ".planning/llm-live-readiness/phases/039-p01-p04-reviewed-revalidation/AUTHORIZATION.json"
        try:
            if project == "p04":
                new_auth = ".planning/llm-live-readiness/phases/045-current-candidate-authority-proposal/AUTHORIZATION.json"
                authority = json.loads((self.root / new_auth).read_text(encoding="utf-8"))
                expected_scope = {"additional_full_fake_gates": 1, "operation_id": campaign,
                                  "case_id": case_id, "max_workflows": 1, "max_provider_calls": 3,
                                  "max_input_tokens": 12288, "max_output_tokens": 1536,
                                  "provider_timeout_seconds": 30, "model": "openai/gpt-oss-20b",
                                  "paid_usd": "0.00", "no_replay": True}
                if (authority.get("authorization_id") != "current-candidate-validation-045-v1"
                        or authority.get("authority") != "explicit_user_reply"
                        or authority.get("decision") != "faz" or authority.get("p04") != expected_scope):
                    raise ValueError()
                for command in (["git", "ls-files", "--error-unmatch", "--", new_auth],
                                ["git", "diff", "--quiet", "HEAD", "--", new_auth]):
                    if subprocess.run(command, cwd=self.root, capture_output=True, timeout=10).returncode:
                        raise ValueError()
            expected = {'authorization_id': 'p01-p04-reviewed-revalidation-v1', 'authority': 'explicit_user_reply', 'decision': 'pode fazer', 'projects': {'p01': {'additional_calls': 4, 'input_tokens': 8192, 'output_tokens': 1024, 'prior_reserved_calls_retained': 12, 'max_workflows': 1}, 'p04': {'additional_calls': 3, 'input_tokens': 12288, 'output_tokens': 1536, 'prior_reserved_calls_retained': 6, 'max_workflows': 1}}, 'additional_calls': 7, 'additional_input_tokens': 20480, 'additional_output_tokens': 2560, 'additional_economic_estimate_usd': '0.0023040', 'authorized_paid_spend_usd': '0.00', 'condition': 'validated_owning_migration_phase', 'free_only': True, 'human_review': 'PENDING', 'migration_applied': False}
            if json.loads((self.root / name).read_text(encoding="utf-8")) != expected:
                raise ValueError()
            for command in (["git", "ls-files", "--error-unmatch", "--", name], ["git", "diff", "--quiet", "HEAD", "--", name]):
                if subprocess.run(command, cwd=self.root, capture_output=True, timeout=10).returncode:
                    raise ValueError()
            prior = [r for r in rows if r["project"] == project and r["campaign"] != campaign]
            expected_rows = {
                "p01": [
                    ("9b174b5ca0fa40f6a0b177ec9f4f2523", "local-operation-v1", "fixture-local-01", 1, 1, 1470, 256, "0.00018705", 235, 46, "0.000031425"),
                    ("bed97cb14f7146f0845588762940e7d4", "local-operation-v1", "fixture-local-01", 1, 2, 1448, 256, "0.0001854", 228, 183, "0.000072"),
                    ("0182eacdb9694423a846400b64f4d321", "local-diagnostic-2-v1", "fixture-diagnostic-02", 1, 1, 1608, 256, "0.0001974", 258, 76, "0.00004215"),
                    ("81182b5c41e04b46882e8cbca05c09fa", "local-diagnostic-2-v1", "fixture-diagnostic-02", 1, 2, 1587, 256, "0.000195825", 251, 58, "0.000036225"),
                ],
                "p04": [
                    ("196cae46b57b4312afeee02aa89d813e", "local-operation-v1", "fixture-local-01", 1, 1, 753, 512, "0.000210075", 105, 51, "0.000023175"),
                    ("832a16f2af404791b39534b130dbfbc2", "local-diagnostic-v1", "fixture-diagnostic-01", 1, 1, 886, 512, "0.00022005", 148, 38, "0.0000225"),
                    ("5f6e80683f9c4a19960f5ce8f74c0187", "local-diagnostic-v1", "fixture-diagnostic-01", 1, 2, 869, 512, "0.000218775", 144, 33, "0.0000207"),
                ],
            }[project]
            if [(r["attempt_id"], r["campaign"], r["case_id"], r["trial"], r["call_index"], r["reserved_input"], r["reserved_output"], r["reserved_cost"], r["actual_input"], r["actual_output"], r["actual_cost"]) for r in prior] != expected_rows or any(r["event"] != "completed" or r["status"] != "ok" for r in prior):
                raise ValueError()
            path = self.root / "projects" / project / "artifacts/evals/live/ledger.sqlite"
            with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as db:
                history = db.execute("SELECT campaign_id,case_id,trial,event,reserved_calls,reserved_input_tokens,reserved_output_tokens,reserved_cost_usd,outcome,error_class,actual_input_tokens,actual_output_tokens FROM events ORDER BY sequence").fetchall()
            expected_history = {
                "p01": [("local-operation-v1","fixture-local-01",1,"reserved",4,8192,1024,"0.0009216",None,None,None,None),("local-operation-v1","fixture-local-01",1,"completed",4,8192,1024,"0.0009216","incomplete","unknown",None,None),("local-diagnostic-v1","fixture-diagnostic-01",1,"reserved",4,8192,1024,"0.0009216",None,None,None,None),("local-diagnostic-v1","fixture-diagnostic-01",1,"completed",4,8192,1024,"0.0009216","incomplete","unknown",None,None),("local-diagnostic-2-v1","fixture-diagnostic-02",1,"reserved",4,8192,1024,"0.0009216",None,None,None,None),("local-diagnostic-2-v1","fixture-diagnostic-02",1,"completed",4,8192,1024,"0.0009216","incomplete","unknown",None,None)],
                "p04": [("local-operation-v1","fixture-local-01",1,"reserved",3,12288,1536,"0.0013824",None,None,None,None),("local-operation-v1","fixture-local-01",1,"completed",3,12288,1536,"0.0013824","incomplete","unknown",None,None),("local-diagnostic-v1","fixture-diagnostic-01",1,"reserved",3,12288,1536,"0.0013824",None,None,None,None),("local-diagnostic-v1","fixture-diagnostic-01",1,"completed",3,12288,1536,"0.0013824","ok",None,292,71)],
            }[project]
            if history[:len(expected_history)] != expected_history:
                raise ValueError()
            tail = history[len(expected_history):]
            calls = 4 if project == "p01" else 3
            expected_tail = [
                (campaign, case_id, 1, "reserved", calls,
                 {"p01": 8192, "p04": 12288}[project],
                 {"p01": 1024, "p04": 1536}[project],
                 {"p01": "0.0009216", "p04": "0.0013824"}[project], None, None, None, None)
            ]
            if tail not in ([], expected_tail):
                raise ValueError()
            current = [r for r in rows if r["project"] == project and r["campaign"] == campaign]
            indexes = [r["call_index"] for r in current]
            if (len(current) >= calls or indexes != list(range(1, len(current) + 1))
                    or call_index != len(current) + 1
                    or any(r["case_id"] != case_id or r["trial"] != 1 or r["event"] != "completed" or r["status"] != "ok" for r in current)
                    or sum(r["reserved_input"] for r in current) > {"p01": 8192, "p04": 12288}[project]
                    or sum(r["reserved_output"] for r in current) > {"p01": 1024, "p04": 1536}[project]):
                raise ValueError()
            if reservation and tail != expected_tail:
                raise ValueError()
        except Exception:
            raise AccountBlocked("reviewed_revalidation_authority_or_history_invalid") from None

    def _reviewed_p01_diagnostic(self, rows, case_id, trial):
        """One explicit diagnostic scope; original failed workflow stays immutable."""
        if case_id != "fixture-diagnostic-01" or trial != 1:
            raise AccountBlocked("reviewed_diagnostic_scope_required")
        name = ".planning/llm-live-readiness/phases/033-p01-reviewed-diagnostic/AUTHORIZATION.json"
        expected = {
            "authorization_id": "p01-reviewed-diagnostic-v1", "authority": "explicit_user_reply_2026-10-29",
            "decision": "Autorizar o diagnóstico separado", "original_result": "INCOMPLETE",
            "original_failure_category": "unknown_unrecoverable", "original_reserved_calls_retained": 4,
            "diagnostic_campaign": "local-diagnostic-v1", "diagnostic_case": "fixture-diagnostic-01",
            "max_workflows": 1, "max_provider_calls": 4, "existing_total_logical_call_ceiling": 8,
            "authorized_paid_usd": 0, "quality_human_holdout_promotion": "PENDING",
            "original_receipts": ["9b174b5ca0fa40f6a0b177ec9f4f2523", "bed97cb14f7146f0845588762940e7d4"],
        }
        try:
            if json.loads((self.root / name).read_text(encoding="utf-8")) != expected:
                raise ValueError()
            for command in (["git", "ls-files", "--error-unmatch", "--", name],
                            ["git", "diff", "--quiet", "HEAD", "--", name]):
                if subprocess.run(command, cwd=self.root, capture_output=True, timeout=10).returncode:
                    raise ValueError()
            original = sorted((r for r in rows if r["project"] == "p01" and r["campaign"] == "local-operation-v1"), key=lambda r: r["call_index"])
            if len(original) != 2:
                raise ValueError()
            for index, row in enumerate(original):
                if (row["case_id"] != "fixture-local-01" or row["trial"] != 1 or row["call_index"] != index + 1
                        or row["attempt_id"] != expected["original_receipts"][index]
                        or row["event"] != "completed" or row["status"] != "ok"
                        or (row["actual_input"], row["actual_output"]) != ((235, 46), (228, 183))[index]):
                    raise ValueError()
            path = self.root / "projects/p01/artifacts/evals/live/ledger.sqlite"
            with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as db:
                events = db.execute("SELECT event,reserved_calls,reserved_input_tokens,reserved_output_tokens,reserved_cost_usd,outcome,error_class,actual_input_tokens,actual_output_tokens,actual_cost_usd FROM events WHERE campaign_id='local-operation-v1' AND case_id='fixture-local-01' AND trial=1 ORDER BY sequence").fetchall()
            if (len(events) != 2 or [r[0] for r in events] != ["reserved", "completed"]
                    or any(r[1:5] != (4,8192,1024,"0.0009216") for r in events)
                    or events[-1][5:] != ("incomplete", "unknown", None, None, None)):
                raise ValueError()
            with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as db:
                closed = db.execute("SELECT 1 FROM events WHERE campaign_id='local-diagnostic-v1' AND event='completed'").fetchone()
                scopes = db.execute("SELECT DISTINCT case_id,trial FROM events WHERE campaign_id='local-diagnostic-v1'").fetchall()
            if closed or any(scope != ("fixture-diagnostic-01", 1) for scope in scopes):
                raise ValueError()
            if any(r["project"] == "p01" and r["campaign"] not in {"local-operation-v1", "local-diagnostic-v1"} for r in rows):
                raise ValueError()
        except Exception:
            raise AccountBlocked("reviewed_diagnostic_authority_or_history_invalid") from None

    def _reviewed_p01_second_diagnostic(self, rows, case_id, trial):
        """One explicit diagnostic scope; original failed workflow stays immutable."""
        if case_id != "fixture-diagnostic-02" or trial != 1:
            raise AccountBlocked("reviewed_diagnostic_scope_required")
        name = ".planning/llm-live-readiness/phases/038-p01-second-diagnostic/AUTHORIZATION.json"
        expected = {'authorization_id': 'p01-second-diagnostic-v1', 'authority': 'explicit_user_reply_2026-10-29', 'decision': 'Autorizar uma segunda opera\xe7\xe3o separada', 'project': 'p01', 'original_reserved_calls_retained': 8, 'diagnostic_campaign': 'local-diagnostic-2-v1', 'diagnostic_case': 'fixture-diagnostic-02', 'max_workflows': 1, 'max_provider_calls': 4, 'existing_total_logical_call_ceiling': 12, 'additional_calls': 4, 'additional_input_tokens': 8192, 'additional_output_tokens': 1024, 'additional_economic_estimate_usd': '0.0009216', 'authorized_paid_spend_usd': '0.00', 'free_only': True, 'condition': 'validated_owning_migration_phase', 'other_project_caps_changed': False, 'confirmation_changed': False, 'human_dataset_rubric_independent_review': 'PENDING', 'promotion': 'PENDING'}
        try:
            if json.loads((self.root / name).read_text(encoding="utf-8")) != expected:
                raise ValueError()
            for command in (["git", "ls-files", "--error-unmatch", "--", name],
                            ["git", "diff", "--quiet", "HEAD", "--", name]):
                if subprocess.run(command, cwd=self.root, capture_output=True, timeout=10).returncode:
                    raise ValueError()
            original = sorted((r for r in rows if r["project"] == "p01" and r["campaign"] == "local-operation-v1"), key=lambda r: r["call_index"])
            if len(original) != 2:
                raise ValueError()
            for index, row in enumerate(original):
                if (row["case_id"] != "fixture-local-01" or row["trial"] != 1 or row["call_index"] != index + 1
                        or row["attempt_id"] != ["9b174b5ca0fa40f6a0b177ec9f4f2523", "bed97cb14f7146f0845588762940e7d4"][index]
                        or row["event"] != "completed" or row["status"] != "ok"
                        or (row["actual_input"], row["actual_output"]) != ((235, 46), (228, 183))[index]):
                    raise ValueError()
            path = self.root / "projects/p01/artifacts/evals/live/ledger.sqlite"
            with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as db:
                events = db.execute("SELECT event,reserved_calls,reserved_input_tokens,reserved_output_tokens,reserved_cost_usd,outcome,error_class,actual_input_tokens,actual_output_tokens,actual_cost_usd FROM events WHERE campaign_id='local-operation-v1' AND case_id='fixture-local-01' AND trial=1 ORDER BY sequence").fetchall()
            if (len(events) != 2 or [r[0] for r in events] != ["reserved", "completed"]
                    or any(r[1:5] != (4,8192,1024,"0.0009216") for r in events)
                    or events[-1][5:] != ("incomplete", "unknown", None, None, None)):
                raise ValueError()
            with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as db:
                first = db.execute("SELECT event,reserved_calls,reserved_input_tokens,reserved_output_tokens,reserved_cost_usd,outcome,error_class,actual_input_tokens,actual_output_tokens,actual_cost_usd FROM events WHERE campaign_id='local-diagnostic-v1' AND case_id='fixture-diagnostic-01' AND trial=1 ORDER BY sequence").fetchall()
            if (len(first) != 2 or [r[0] for r in first] != ["reserved", "completed"]
                    or any(r[1:5] != (4,8192,1024,"0.0009216") for r in first)
                    or first[-1][5:] != ("incomplete", "unknown", None, None, None)
                    or any(r["project"] == "p01" and r["campaign"] == "local-diagnostic-v1" for r in rows)):
                raise ValueError()
            with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as db:
                closed = db.execute("SELECT 1 FROM events WHERE campaign_id='local-diagnostic-2-v1' AND event='completed'").fetchone()
                scopes = db.execute("SELECT DISTINCT case_id,trial FROM events WHERE campaign_id='local-diagnostic-2-v1'").fetchall()
            if closed or any(scope != ("fixture-diagnostic-02", 1) for scope in scopes):
                raise ValueError()
            if any(r["project"] == "p01" and r["campaign"] not in {"local-operation-v1", "local-diagnostic-v1", "local-diagnostic-2-v1"} for r in rows):
                raise ValueError()
        except Exception:
            raise AccountBlocked("reviewed_diagnostic_authority_or_history_invalid") from None

    def _reviewed_p04_diagnostic(self, rows, case_id, trial):
        """One explicit diagnostic scope; original failed workflow stays immutable."""
        if case_id != "fixture-diagnostic-01" or trial != 1:
            raise AccountBlocked("reviewed_diagnostic_scope_required")
        name = ".planning/llm-live-readiness/phases/035-p04-reviewed-diagnostic/AUTHORIZATION.json"
        expected = {
            "authorization_id": "p04-reviewed-diagnostic-v1", "authority": "explicit_user_reply_2026-10-29",
            "decision": "Autorizar diagnóstico separado de P04", "original_result": "INCOMPLETE",
            "original_failure_category": "unknown_unrecoverable", "original_reserved_calls_retained": 3,
            "diagnostic_campaign": "local-diagnostic-v1", "diagnostic_case": "fixture-diagnostic-01",
            "max_workflows": 1, "max_provider_calls": 3, "existing_total_logical_call_ceiling": 6,
            "authorized_paid_usd": 0, "quality_human_holdout_promotion": "PENDING",
            "original_receipts": ["196cae46b57b4312afeee02aa89d813e"],
        }
        try:
            if json.loads((self.root / name).read_text(encoding="utf-8")) != expected:
                raise ValueError()
            for command in (["git", "ls-files", "--error-unmatch", "--", name],
                            ["git", "diff", "--quiet", "HEAD", "--", name]):
                if subprocess.run(command, cwd=self.root, capture_output=True, timeout=10).returncode:
                    raise ValueError()
            original = sorted((r for r in rows if r["project"] == "p04" and r["campaign"] == "local-operation-v1"), key=lambda r: r["call_index"])
            if len(original) != 1:
                raise ValueError()
            for index, row in enumerate(original):
                if (row["case_id"] != "fixture-local-01" or row["trial"] != 1 or row["call_index"] != index + 1
                        or row["attempt_id"] != expected["original_receipts"][index]
                        or row["event"] != "completed" or row["status"] != "ok"
                        or (row["actual_input"], row["actual_output"]) != ((105, 51),)[index]):
                    raise ValueError()
            path = self.root / "projects/p04/artifacts/evals/live/ledger.sqlite"
            with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as db:
                events = db.execute("SELECT event,reserved_calls,reserved_input_tokens,reserved_output_tokens,reserved_cost_usd,outcome,error_class,actual_input_tokens,actual_output_tokens,actual_cost_usd FROM events WHERE campaign_id='local-operation-v1' AND case_id='fixture-local-01' AND trial=1 ORDER BY sequence").fetchall()
            if (len(events) != 2 or [r[0] for r in events] != ["reserved", "completed"]
                    or any(r[1:5] != (3,12288,1536,"0.0013824") for r in events)
                    or events[-1][5:] != ("incomplete", "unknown", None, None, None)):
                raise ValueError()
            with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as db:
                closed = db.execute("SELECT 1 FROM events WHERE campaign_id='local-diagnostic-v1' AND event='completed'").fetchone()
                scopes = db.execute("SELECT DISTINCT case_id,trial FROM events WHERE campaign_id='local-diagnostic-v1'").fetchall()
            if closed or any(scope != ("fixture-diagnostic-01", 1) for scope in scopes):
                raise ValueError()
            step_path = self.root / "projects/p04/artifacts/evals/live/operations.sqlite"
            with closing(sqlite3.connect(step_path.resolve().as_uri() + "?mode=ro", uri=True)) as db:
                steps = db.execute("SELECT operation,step,status,receipt,input_tokens,output_tokens FROM attempts").fetchall()
            if steps != [("fixture-local-01", "triage", "reserved", None, None, None)]:
                raise ValueError()
            if any(r["project"] == "p04" and r["campaign"] not in {"local-operation-v1", "local-diagnostic-v1"} for r in rows):
                raise ValueError()
        except Exception:
            raise AccountBlocked("reviewed_diagnostic_authority_or_history_invalid") from None

    def preview(
        self, project, campaign, case_id, trial, call_index, input_tokens, output_tokens
    ):
        cost = self._prepare_reservation(
            project, campaign, case_id, trial, call_index, input_tokens, output_tokens
        )
        with machine_lease(self.lock):
            self._approve(
                project,
                campaign,
                case_id,
                trial,
                call_index,
                input_tokens,
                output_tokens,
                cost,
            )
        return {
            "status": "approved",
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost_usd": str(cost),
        }

    def reserve(
        self, project, campaign, case_id, trial, call_index, input_tokens, output_tokens,
        *, credential_slots=None,
    ):
        if credential_slots is not None and (
            not isinstance(credential_slots, tuple)
            or not credential_slots
            or any(type(slot) is not int or not 0 <= slot <= 4 for slot in credential_slots)
            or len(set(credential_slots)) != len(credential_slots)
        ):
            raise AccountBlocked("invalid_credential_slots")
        cost = self._prepare_reservation(
            project, campaign, case_id, trial, call_index, input_tokens, output_tokens
        )
        with machine_lease(self.lock):
            rows = self._approve(
                project,
                campaign,
                case_id,
                trial,
                call_index,
                input_tokens,
                output_tokens,
                cost,
                reservation=True,
            )
            attempt = uuid.uuid4().hex
            slot = credential_slots[len(rows) % len(credential_slots)] if credential_slots else None
            try:
                with closing(sqlite3.connect(self.path(project))) as db:
                    db.execute("PRAGMA synchronous=FULL")
                    db.execute(
                        "INSERT INTO usage_events(attempt_id,event,ordinal,campaign,case_id,trial,call_index,reserved_at,reserved_input,reserved_output,reserved_cost,feedback) VALUES(?,'reserved',?,?,?,?,?,?,?,?,?,?)",
                        (
                            attempt,
                            len(rows) + 1,
                            campaign,
                            case_id,
                            trial,
                            call_index,
                            self.clock(),
                            input_tokens,
                            output_tokens,
                            str(cost),
                            json.dumps({"credential_slot": slot}) if slot is not None else None,
                        ),
                    )
                    db.commit()
            except sqlite3.IntegrityError:
                raise AccountBlocked("attempt_already_reserved_or_completed") from None
            return (attempt, slot) if slot is not None else attempt

    def complete(
        self,
        project,
        attempt_id,
        *,
        input_tokens=None,
        output_tokens=None,
        status="ok",
        feedback=None,
    ):
        if status not in {
            "ok",
            "provider_error",
            "transport_error",
            "quota",
            "model_mismatch",
        }:
            raise AccountBlocked("invalid_sanitized_provider_status")
        for value in (input_tokens, output_tokens):
            if value is not None:
                integer(value)
        clean = dict(feedback or {})
        if not set(clean) <= FEEDBACK:
            raise AccountBlocked("unknown_provider_feedback_field")
        for field, value in clean.items():
            if field.endswith("seconds"):
                if (
                    type(value) not in (int, float)
                    or not math.isfinite(value)
                    or not 0 <= value <= 86400
                ):
                    raise AccountBlocked("invalid_provider_reset")
            else:
                integer(value)
        if status == "quota":
            clean["retry_after_seconds"] = 86400
        with machine_lease(self.lock):
            rows = self._history()
            matches = [
                row
                for row in rows
                if row["attempt_id"] == attempt_id and row["project"] == project
            ]
            if len(matches) != 1 or matches[0]["event"] != "reserved":
                raise AccountBlocked("attempt_not_reserved_or_already_completed")
            clean.update(observed_at=self.clock(), account_ordinal=len(rows))
            price = self.policy["pricing_per_million"]
            cost = (
                None
                if input_tokens is None
                or output_tokens is None
                or status == "model_mismatch"
                else str(
                    (
                        input_tokens * money(price["input_usd"])
                        + output_tokens * money(price["output_usd"])
                    )
                    / 1000000
                )
            )
            with closing(sqlite3.connect(self.path(project))) as db:
                db.execute("PRAGMA synchronous=FULL")
                db.execute(
                    """INSERT INTO usage_events(attempt_id,event,ordinal,campaign,case_id,trial,call_index,reserved_at,reserved_input,reserved_output,reserved_cost,actual_input,actual_output,actual_cost,status,feedback)
                    SELECT attempt_id,'completed',ordinal,campaign,case_id,trial,call_index,reserved_at,reserved_input,reserved_output,reserved_cost,?,?,?,?,? FROM usage_events WHERE attempt_id=? AND event='reserved'""",
                    (
                        input_tokens,
                        output_tokens,
                        cost,
                        status,
                        json.dumps(clean, sort_keys=True),
                        attempt_id,
                    ),
                )
                db.commit()

    def snapshot(self):
        rows = self._history()
        return {
            "accounted_attempts": len(rows),
            "uncertain_attempts": sum(row["event"] == "reserved" for row in rows),
            "registered_projects": sorted(self._references()),
            "cumulative_accounted_usage": {
                field: str(sum(self.usage(row)[field] for row in rows))
                for field in COUNTERS
            },
            "provider_billed_cost_usd": "PENDING",
            "provider_remaining_daily_tokens": "PENDING",
            "historical_unmanaged_provider_usage": "PENDING",
        }


def numbered_key_slots(root):
    try:
        lines = (root / ".env").read_text(encoding="utf-8").splitlines()
    except OSError:
        raise AccountBlocked("root_credentials_unavailable") from None
    names = {"GROQ_API_KEY", *(f"GROQ_API_KEY_{index}" for index in range(1, 5))}
    values = {}
    for raw in lines:
        name, separator, value = raw.strip().removeprefix("export ").partition("=")
        if separator and name.strip() in names:
            value = value.strip().strip('"').strip("'")
            if value:
                values[name.strip()] = value
    keys = []
    for name in sorted(values):
        if values[name] not in (key for _, key in keys):
            keys.append((0 if name == "GROQ_API_KEY" else int(name.rsplit("_", 1)[1]), values[name]))
    if not keys:
        raise AccountBlocked("numbered_credentials_missing")
    return keys


def numbered_keys(root):
    return [key for _, key in numbered_key_slots(root)]


class NoMetadataRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def metadata_request(req, *, timeout):
    return build_opener(NoMetadataRedirect()).open(req, timeout=timeout)


def catalog_request(request, req, *, sleep=time.sleep, jitter=random.uniform):
    """Bounded same-key retries for read-only catalog connection failures only."""
    if req.get_method() != "GET" or req.full_url != "https://api.groq.com/openai/v1/models":
        raise AccountBlocked("metadata_retry_scope_denied")
    for attempt in range(3):
        try:
            return request(req, timeout=4)
        except HTTPError:
            raise
        except (URLError, TimeoutError, ConnectionError):
            if attempt == 2:
                raise
            delay = jitter(0, 0.25 * (2 ** attempt))
            if type(delay) not in (int, float) or not math.isfinite(delay) or not 0 <= delay <= 0.25 * (2 ** attempt):
                raise AccountBlocked("invalid_retry_jitter")
            sleep(delay)


def catalog_preflight(root, *, request=metadata_request, keys=None):
    keys = numbered_keys(root) if keys is None else keys
    valid = 0
    failures = {}
    observations = []
    checked = 0
    for key in keys:
        checked += 1
        req = Request(
            "https://api.groq.com/openai/v1/models",
            headers={
                "Authorization": "Bearer " + key,
                "Accept": "application/json",
                "User-Agent": "supportops-lab-readiness/1.0",
            },
        )
        try:
            with catalog_request(request, req) as response:
                observed = feedback(getattr(response, "headers", {}))
                if observed:
                    observations.append(observed)
                raw = response.read(1000001)
                if len(raw) > 1000000:
                    raise ValueError("catalog response too large")
                payload = json.loads(raw)
            data = payload.get("data") if isinstance(payload, dict) else None
            if not isinstance(data, list) or not all(
                isinstance(item, dict) for item in data
            ):
                raise ValueError("invalid catalog schema")
            if any(
                item.get("id") == MODEL and item.get("active", True) for item in data
            ):
                valid += 1
            else:
                failures["model_access"] = failures.get("model_access", 0) + 1
        except HTTPError as exc:
            observed = feedback(exc.headers or {})
            if observed:
                observations.append(observed)
            label = "http_" + str(exc.code)
            failures[label] = failures.get(label, 0) + 1
            exc.close()
            if exc.code == 429:
                break
        except URLError as exc:
            label = "transport_" + type(exc.reason).__name__
            failures[label] = failures.get(label, 0) + 1
        except (OSError, ValueError, KeyError, TypeError):
            failures["catalog_schema_or_transport"] = (
                failures.get("catalog_schema_or_transport", 0) + 1
            )
    effective = {}
    for name in (
        "request_limit",
        "token_limit",
        "remaining_requests",
        "remaining_tokens",
    ):
        values = [row[name] for row in observations if name in row]
        if values:
            effective[name] = min(values)
    for name in ("request_reset_seconds", "token_reset_seconds", "retry_after_seconds"):
        values = [row[name] for row in observations if name in row]
        if values:
            # Use the longest observed window for the most restrictive remaining value.
            effective[name] = max(values)
    return {
        "status": "PASS" if keys and valid == len(keys) else "INCOMPLETE",
        "model": MODEL,
        "unique_credentials_checked": checked,
        "unique_credentials_selected": len(keys),
        "model_access_count": valid,
        "provider_accessed": True,
        "credentials_read": True,
        "generation_calls": 0,
        "authenticated_rate_limits": effective,
        "rate_limit_headers_observed": sorted(effective),
        "account_billing_tier_verified": False,
        "remaining_daily_tokens": "PENDING",
        "failures": failures,
    }


def bounded_catalog_preflight():
    """Kill a stalled metadata-only worker; never replay a timed-out request."""
    try:
        result = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--catalog-preflight-worker"],
            cwd=ROOT,
            env={name: value for name, value in os.environ.items() if not name.startswith("GROQ_API_KEY")},
            capture_output=True,
            timeout=80,
            check=False,
        )
        report = json.loads(result.stdout)
        if result.returncode not in {0, 2} or not isinstance(report, dict) or report.get("status") not in {"PASS", "INCOMPLETE"}:
            raise ValueError("invalid worker report")
        return report
    except (subprocess.TimeoutExpired, OSError, ValueError):
        return {
            "status": "INCOMPLETE",
            "reason": "metadata_worker_timeout_or_failure",
            "generation_calls": 0,
            "provider_accessed": "UNKNOWN",
            "credentials_read": "UNKNOWN",
        }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog-preflight", action="store_true")
    parser.add_argument("--catalog-preflight-worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        if args.catalog_preflight_worker:
            report = catalog_preflight(ROOT)
        elif args.catalog_preflight:
            report = bounded_catalog_preflight()
        else:
            policy = json.loads(
                (ROOT / "shared/policies/groq-free-campaign.json").read_text()
            )
            report = {
                "status": "INCOMPLETE",
                "policy": policy,
                "usage": SharedAccount(ROOT, policy).snapshot(),
                "provider_accessed": False,
                "credentials_read": False,
                "generation_authorized": False,
            }
        print(json.dumps(report, sort_keys=True, indent=2))
        return 0 if report["status"] == "PASS" or not (args.catalog_preflight or args.catalog_preflight_worker) else 2
    except (AccountBlocked, OSError, ValueError) as exc:
        reason = (
            str(exc) if isinstance(exc, AccountBlocked) else "account_input_unavailable"
        )
        print(json.dumps({"status": "INCOMPLETE", "reason": reason}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
