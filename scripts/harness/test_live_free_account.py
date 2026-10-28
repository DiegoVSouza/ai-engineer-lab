from __future__ import annotations

import copy
import io
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from decimal import Decimal
from pathlib import Path

from live_free_account import (
    AccountBlocked,
    SharedAccount,
    catalog_preflight,
    machine_lease,
    numbered_keys,
)

SOURCE = Path(__file__).resolve().parent
POLICY = json.loads(
    (SOURCE.parents[1] / "shared/policies/groq-free-campaign.json").read_text()
)


class AccountTests(unittest.TestCase):
    def test_metadata_parent_timeout_is_single_attempt_and_sanitized(self):
        import subprocess
        from unittest.mock import patch
        import live_free_account as module

        with patch.object(module.subprocess, "run", side_effect=subprocess.TimeoutExpired("PRIVATE", 80)) as runner:
            result = module.bounded_catalog_preflight()
        self.assertEqual(runner.call_count, 1)
        self.assertEqual(runner.call_args.kwargs["timeout"], 80)
        self.assertFalse(any(name.startswith("GROQ_API_KEY") for name in runner.call_args.kwargs["env"]))
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(result["generation_calls"], 0)
        self.assertNotIn("PRIVATE", json.dumps(result))

    def test_catalog_429_stops_before_another_credential(self):
        from urllib.error import HTTPError

        calls = []
        body = io.BytesIO(b"PRIVATE")

        def limited(req, *, timeout):
            calls.append(req)
            raise HTTPError(req.full_url, 429, "PRIVATE", {}, body)

        result = catalog_preflight(self.root, request=limited, keys=["fixture-a", "fixture-b"])
        self.assertEqual(len(calls), 1)
        self.assertEqual(result["unique_credentials_checked"], 1)
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertTrue(body.closed)
        self.assertNotIn("PRIVATE", json.dumps(result))

    def test_catalog_default_transport_denies_redirects(self):
        from unittest.mock import patch
        from urllib.request import Request
        import live_free_account as module

        req = Request("https://api.groq.com/openai/v1/models")
        with patch.object(module, "build_opener") as factory:
            module.metadata_request(req, timeout=4)
        handler = factory.call_args.args[0]
        self.assertIsNone(handler.redirect_request(req, None, 302, "fixture", {}, "https://example.invalid"))

    def test_catalog_rejects_oversized_body_and_closes_response(self):
        class Oversized(io.BytesIO):
            headers = {}

            def read(self, size=-1):
                self.requested_size = size
                return b" " * 1000001

        response = Oversized()
        result = catalog_preflight(self.root, request=lambda *a, **k: response, keys=["fixture"])
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(response.requested_size, 1000001)
        self.assertTrue(response.closed)

    def test_metadata_retry_is_bounded_same_request_and_never_retries_http(self):
        from live_free_account import catalog_request
        from urllib.request import Request
        from urllib.error import URLError, HTTPError
        req = Request('https://api.groq.com/openai/v1/models')
        calls, waits = [], []
        def unavailable(request, *, timeout):
            calls.append((request, timeout))
            raise URLError('fixture')
        with self.assertRaises(URLError):
            catalog_request(unavailable, req, sleep=waits.append, jitter=lambda lo, hi: hi)
        self.assertEqual(calls, [(req, 4)] * 3)
        self.assertEqual(waits, [0.25, 0.5])
        calls.clear()
        def limited(request, *, timeout):
            calls.append(request)
            raise HTTPError(req.full_url, 429, 'fixture', {}, None)
        with self.assertRaises(HTTPError):
            catalog_request(limited, req, sleep=waits.append)
        self.assertEqual(calls, [req])
        with self.assertRaises(AccountBlocked):
            catalog_request(unavailable, Request('https://api.groq.com/openai/v1/chat/completions', data=b'{}'))

    def test_unnumbered_credential_has_stable_slot_and_deduplicates(self):
        from live_free_account import numbered_key_slots
        (self.root / '.env').write_text('GROQ_API_KEY=fixture-a\nGROQ_API_KEY_1=fixture-a\nGROQ_API_KEY_3=fixture-b\n')
        self.assertEqual(numbered_key_slots(self.root), [(0, 'fixture-a'), (3, 'fixture-b')])
        account = self.account()
        attempt, slot = account.reserve('p00', 'fixture', 'case', 1, 1, 100, 50, credential_slots=(0, 3))
        self.assertEqual(slot, 0)
        with closing(sqlite3.connect(account.path('p00'))) as db:
            self.assertEqual(json.loads(db.execute("SELECT feedback FROM usage_events WHERE attempt_id=?", (attempt,)).fetchone()[0]), {'credential_slot': 0})

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="free-account-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.policy = copy.deepcopy(POLICY)
        self.now = [1000000.0]

    def account(self):
        account = SharedAccount(self.root, self.policy, clock=lambda: self.now[0])
        account.register("p00")
        account.register("p02")
        return account

    def test_published_policy_totals_match_unchanged_per_call_maxima(self):
        for caps in POLICY["projects"].values():
            self.assertEqual(
                caps["input_tokens"], caps["requests"] * caps["input_tokens_per_call"]
            )
            self.assertEqual(
                caps["output_tokens"], caps["requests"] * caps["output_tokens_per_call"]
            )
        for field in ("requests", "input_tokens", "output_tokens"):
            self.assertEqual(
                POLICY["campaign_caps"][field],
                sum(caps[field] for caps in POLICY["projects"].values()),
            )

    def reserve(self, account, project="p00", case="case-1", campaign="baseline"):
        return account.reserve(project, campaign, case, 1, 1, 100, 50)

    def test_switching_project_campaign_and_process_does_not_reset_caps(self):
        self.policy["campaign_caps"]["requests"] = 1
        first = self.account()
        attempt = self.reserve(first)
        first.complete("p00", attempt, input_tokens=80, output_tokens=30)
        recovered = self.account()
        with self.assertRaisesRegex(AccountBlocked, "cumulative_account"):
            self.reserve(recovered, "p02", campaign="new-candidate")
        self.assertEqual(recovered.snapshot()["accounted_attempts"], 1)

    def test_unknown_usage_keeps_reservation_and_blocks_until_reconciled(self):
        account = self.account()
        attempt = self.reserve(account)
        with self.assertRaisesRegex(AccountBlocked, "uncertain_attempt"):
            self.reserve(account, "p02")
        account.complete("p00", attempt, status="transport_error")
        self.assertEqual(
            account.snapshot()["cumulative_accounted_usage"]["input_tokens"], "100"
        )
        self.assertEqual(account.snapshot()["uncertain_attempts"], 0)
        self.assertGreater(
            Decimal(
                account.snapshot()["cumulative_accounted_usage"]["estimated_cost_usd"]
            ),
            0,
        )
        self.reserve(account, "p02")

    def test_slot_reservation_survives_restart_and_blocks_other_dispatch(self):
        account = self.account()
        attempt, slot = account.reserve(
            "p00", "campaign", "case", 1, 1, 100, 50, credential_slots=(1, 3)
        )
        self.assertEqual(slot, 1)
        with closing(sqlite3.connect(account.path("p00"))) as db:
            feedback = db.execute(
                "SELECT feedback FROM usage_events WHERE attempt_id=? AND event='reserved'", (attempt,)
            ).fetchone()[0]
        self.assertEqual(json.loads(feedback), {"credential_slot": 1})
        restarted = self.account()
        with self.assertRaisesRegex(AccountBlocked, "uncertain_attempt"):
            restarted.reserve("p02", "campaign", "other", 1, 1, 100, 50, credential_slots=(1, 3))
        restarted.complete("p00", attempt, input_tokens=10, output_tokens=10)
        _, next_slot = restarted.reserve(
            "p02", "campaign", "other", 1, 1, 100, 50, credential_slots=(1, 3)
        )
        self.assertEqual(next_slot, 3)

    def test_cumulative_token_and_economic_caps_apply_across_projects(self):
        for field, cap in (
            ("input_tokens", 150),
            ("output_tokens", 75),
            ("estimated_cost_usd", "0.00003"),
        ):
            with (
                self.subTest(field=field),
                tempfile.TemporaryDirectory(prefix="free-cap-") as directory,
            ):
                policy = copy.deepcopy(POLICY)
                policy["campaign_caps"][field] = cap
                account = SharedAccount(Path(directory), policy)
                account.register("p00")
                account.register("p02")
                attempt = self.reserve(account)
                account.complete("p00", attempt, status="transport_error")
                with self.assertRaisesRegex(AccountBlocked, "cumulative_account"):
                    self.reserve(account, "p02")

    def test_project_cap_does_not_reset_or_consume_another_project_allowance(self):
        self.policy["projects"]["p00"]["requests"] = 1
        account = self.account()
        attempt = self.reserve(account)
        account.complete("p00", attempt, input_tokens=10, output_tokens=10)
        with self.assertRaisesRegex(AccountBlocked, "cumulative_account_or_project"):
            self.reserve(account, case="case-2")
        self.reserve(account, "p02")

    def test_malformed_usage_cannot_be_interpreted_as_zero(self):
        account = self.account()
        with closing(sqlite3.connect(account.path("p00"))) as db:
            db.execute(
                "INSERT INTO usage_events(attempt_id,event,ordinal,campaign,case_id,trial,call_index,reserved_at,reserved_input,reserved_output,reserved_cost) VALUES('bad','reserved',1,'campaign','case',1,1,1000000,-1,50,'0')"
            )
            db.commit()
        with self.assertRaisesRegex(AccountBlocked, "invalid_resource_count"):
            self.reserve(account, "p02")

    def test_repeated_identity_and_completion_cannot_be_replayed(self):
        account = self.account()
        attempt = self.reserve(account)
        account.complete("p00", attempt, input_tokens=80, output_tokens=30)
        with self.assertRaisesRegex(AccountBlocked, "already_reserved"):
            self.reserve(account)
        with self.assertRaisesRegex(AccountBlocked, "already_completed"):
            account.complete("p00", attempt, input_tokens=0, output_tokens=0)

    def test_rolling_minute_and_day_tokens_stop_across_projects(self):
        self.policy["free_limits"]["tokens_per_minute"] = 150
        self.policy["free_limits"]["tokens_per_day"] = 200
        account = self.account()
        attempt = self.reserve(account)
        account.complete("p00", attempt, status="transport_error")
        with self.assertRaisesRegex(AccountBlocked, "free_token_minute"):
            self.reserve(account, "p02")
        self.now[0] += 61
        with self.assertRaisesRegex(AccountBlocked, "free_token_day"):
            self.reserve(account, "p02")
        self.now[0] += 86400
        self.reserve(account, "p02")

    def test_rolling_day_requests_and_provider_remaining_are_not_per_key(self):
        self.policy["free_limits"]["requests_per_day"] = 1
        account = self.account()
        attempt = self.reserve(account)
        account.complete("p00", attempt, input_tokens=10, output_tokens=10)
        self.now[0] += 61
        with self.assertRaisesRegex(AccountBlocked, "free_request_day"):
            self.reserve(account, "p02")

    def test_smaller_authenticated_capacity_and_reset_are_honored(self):
        account = self.account()
        attempt = self.reserve(account)
        account.complete(
            "p00",
            attempt,
            input_tokens=10,
            output_tokens=10,
            feedback={"remaining_tokens": 149, "token_reset_seconds": 70},
        )
        with self.assertRaisesRegex(AccountBlocked, "provider_token_capacity"):
            self.reserve(account, "p02")
        self.now[0] += 71
        next_attempt = self.reserve(account, "p02")
        account.complete(
            "p02",
            next_attempt,
            input_tokens=10,
            output_tokens=10,
            feedback={"remaining_requests": 0, "request_reset_seconds": 90},
        )
        with self.assertRaisesRegex(AccountBlocked, "provider_request_capacity"):
            self.reserve(account, "p00", case="case-2")

    def test_quota_stops_all_projects_after_restart(self):
        account = self.account()
        attempt = self.reserve(account)
        account.complete("p00", attempt, status="quota")
        with self.assertRaisesRegex(AccountBlocked, "cooldown"):
            self.reserve(self.account(), "p02")

    def test_actual_overrun_is_retained_and_blocks_new_dispatch(self):
        account = self.account()
        attempt = self.reserve(account)
        account.complete("p00", attempt, input_tokens=101, output_tokens=50)
        self.assertEqual(
            account.snapshot()["cumulative_accounted_usage"]["input_tokens"], "101"
        )
        with self.assertRaisesRegex(AccountBlocked, "overrun"):
            self.reserve(account, "p02")

    def test_missing_ledger_or_lost_registry_does_not_reset_usage(self):
        account = self.account()
        attempt = self.reserve(account)
        account.complete("p00", attempt, status="transport_error")
        content = account.registry.read_bytes()
        account.registry.unlink()
        with self.assertRaisesRegex(AccountBlocked, "without_registry"):
            account.snapshot()
        account.registry.write_bytes(content)
        account.path("p00").unlink()
        with self.assertRaisesRegex(AccountBlocked, "missing_or_replaced"):
            account.snapshot()

    def test_usage_is_append_only_and_logs_contain_no_provider_content(self):
        account = self.account()
        attempt = self.reserve(account)
        account.complete("p00", attempt, status="transport_error")
        with closing(sqlite3.connect(account.path("p00"))) as db:
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("UPDATE usage_events SET reserved_input=0")
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("DELETE FROM usage_events")
        with self.assertRaisesRegex(AccountBlocked, "unknown_provider_feedback"):
            account.complete("p00", attempt, feedback={"authorization": "do-not-log"})
        self.assertNotIn("do-not-log", json.dumps(account.snapshot()))

    def test_concurrent_projects_cannot_both_reserve(self):
        account = self.account()

        def reserve(project):
            try:
                self.reserve(account, project)
                return "reserved"
            except AccountBlocked:
                return "blocked"

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(reserve, ("p00", "p02")))
        self.assertEqual(sorted(results), ["blocked", "reserved"])

    def test_lease_contends_across_processes_and_recovers_after_death(self):
        lock = self.root / "process.lock"
        code = """
import os,sys
from pathlib import Path
from live_free_account import machine_lease, AccountBlocked
try:
    with machine_lease(Path(sys.argv[1])):
        os._exit(23)
except AccountBlocked:
    sys.exit(2)
"""

        def child():
            return subprocess.run(
                [sys.executable, "-c", code, str(lock)],
                cwd=SOURCE,
                capture_output=True,
                timeout=10,
                check=False,
            )

        with machine_lease(lock):
            self.assertEqual(child().returncode, 2)
        self.assertEqual(child().returncode, 23)
        with machine_lease(lock):
            pass

    def test_changed_policy_cannot_reset_preexisting_account(self):
        self.account()
        self.policy["campaign_caps"]["requests"] += 1
        with self.assertRaisesRegex(AccountBlocked, "policy_or_registry_changed"):
            SharedAccount(self.root, self.policy).snapshot()

    def test_pending_policy_migration_marker_blocks_account_dispatch(self):
        account = self.account()
        marker = self.root / ".runtime/llm-live-readiness/policy-migration.pending"
        marker.write_text('{"migration_id":"in-progress"}', encoding="utf-8")
        with self.assertRaisesRegex(AccountBlocked, "policy_migration_pending"):
            account.snapshot()
        with self.assertRaisesRegex(AccountBlocked, "policy_migration_pending"):
            self.reserve(account)

    def test_invalid_or_paid_policy_is_rejected(self):
        for value in (True, "PENDING", -1):
            policy = copy.deepcopy(POLICY)
            policy["campaign_caps"]["requests"] = value
            with self.assertRaises(AccountBlocked):
                SharedAccount(self.root, policy)
        for value in ("NaN", "Infinity", "0.01"):
            policy = copy.deepcopy(POLICY)
            policy["authorized_paid_spend_usd"] = value
            with self.assertRaises(AccountBlocked):
                SharedAccount(self.root, policy)

    def test_keys_come_only_from_authorized_root_file_entries_and_deduplicate(self):
        (self.root / ".env").write_text(
            "GROQ_API_KEY=excluded\nGROQ_API_KEY_1='synthetic-a'\nGROQ_API_KEY_2=synthetic-a\nOTHER_API_KEY=excluded\nGROQ_API_KEY_4=synthetic-b\n"
        )
        self.assertEqual(numbered_keys(self.root), ["excluded", "synthetic-a", "synthetic-b"])
        (self.root / ".env").write_text("GROQ_API_KEY=excluded\n")
        self.assertEqual(numbered_keys(self.root), ["excluded"])
        (self.root / ".env").write_text("OTHER_API_KEY=excluded\n")
        with self.assertRaises(AccountBlocked):
            numbered_keys(self.root)

    def test_catalog_preflight_is_metadata_only_and_never_returns_credentials(self):
        (self.root / ".env").write_text(
            "GROQ_API_KEY_1=synthetic-secret-a\nGROQ_API_KEY_2=synthetic-secret-b\n"
        )
        responses = iter(
            [
                {
                    "x-ratelimit-limit-requests": "1000",
                    "x-ratelimit-limit-tokens": "8000",
                },
                {
                    "x-ratelimit-limit-requests": "200",
                    "x-ratelimit-limit-tokens": "400",
                    "x-ratelimit-remaining-requests": "3",
                    "x-ratelimit-remaining-tokens": "120",
                    "x-ratelimit-reset-tokens": "45s",
                    "x-private-provider-header": "header-secret",
                },
            ]
        )

        class CatalogResponse(io.BytesIO):
            def __init__(self, payload, headers):
                super().__init__(payload)
                self.headers = headers

        def response(request, *, timeout):
            self.assertEqual(request.full_url, "https://api.groq.com/openai/v1/models")
            self.assertEqual(request.get_method(), "GET")
            self.assertEqual(timeout, 4)
            return CatalogResponse(
                json.dumps({"data": [{"id": POLICY["model"]}]}).encode(),
                next(responses),
            )

        result = catalog_preflight(self.root, request=response)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["generation_calls"], 0)
        self.assertEqual(
            result["authenticated_rate_limits"],
            {
                "request_limit": 200,
                "token_limit": 400,
                "remaining_requests": 3,
                "remaining_tokens": 120,
                "token_reset_seconds": 45,
            },
        )
        self.assertFalse(result["account_billing_tier_verified"])
        self.assertEqual(result["remaining_daily_tokens"], "PENDING")
        self.assertNotIn("synthetic-secret", json.dumps(result))
        self.assertNotIn("header-secret", json.dumps(result))

    def test_missing_or_malformed_rate_headers_do_not_raise_policy_limits(self):
        (self.root / ".env").write_text(
            "GROQ_API_KEY_1=synthetic-a\nGROQ_API_KEY_2=synthetic-b\n"
        )
        response_headers = iter(
            [
                {
                    "x-ratelimit-limit-requests": "999999",
                    "x-ratelimit-limit-tokens": "999999",
                },
                {
                    "x-ratelimit-limit-requests": "999999",
                    "x-ratelimit-limit-tokens": "8000;secret",
                    "x-ratelimit-remaining-requests": "not-a-number",
                    "x-ratelimit-remaining-tokens": "-1",
                    "x-ratelimit-reset-tokens": "999999s",
                    "x-private-provider-header": "must-not-be-returned",
                },
            ]
        )

        class CatalogResponse(io.BytesIO):
            def __init__(self, headers):
                super().__init__(
                    json.dumps({"data": [{"id": POLICY["model"]}]}).encode()
                )
                self.headers = headers

        def response(request, *, timeout):
            return CatalogResponse(next(response_headers))

        result = catalog_preflight(self.root, request=response)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(
            result["authenticated_rate_limits"],
            {"request_limit": 999999, "token_limit": 999999},
        )
        self.assertEqual(
            result["rate_limit_headers_observed"], ["request_limit", "token_limit"]
        )
        self.assertEqual(result["remaining_daily_tokens"], "PENDING")
        self.assertNotIn("must-not-be-returned", json.dumps(result))
        account = self.account()
        account.set_authenticated_feedback(result["authenticated_rate_limits"])
        self.reserve(account)
        self.assertEqual(account.snapshot()["accounted_attempts"], 1)

    def test_authenticated_preflight_limits_are_conservative_and_in_memory(self):
        account = self.account()
        account.set_authenticated_feedback({"request_limit": 1000, "token_limit": 100})
        with self.assertRaisesRegex(AccountBlocked, "free_token_minute_checkpoint"):
            self.reserve(account)
        self.assertEqual(account.snapshot()["accounted_attempts"], 0)

    def test_authenticated_remaining_capacity_and_reset_apply_before_reservation(self):
        account = self.account()
        account.set_authenticated_feedback(
            {
                "remaining_requests": 0,
                "remaining_tokens": 1000,
                "request_reset_seconds": 30,
                "token_reset_seconds": 30,
            }
        )
        with self.assertRaisesRegex(
            AccountBlocked, "provider_request_capacity_checkpoint"
        ):
            self.reserve(account)
        self.assertEqual(account.snapshot()["accounted_attempts"], 0)


if __name__ == "__main__":
    unittest.main()
