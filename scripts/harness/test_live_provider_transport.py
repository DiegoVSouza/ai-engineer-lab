from __future__ import annotations

import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from urllib.error import HTTPError, URLError

from live_free_account import MODEL, AccountBlocked, SharedAccount
from live_provider_transport import (
    ProviderSession,
    duration,
    encode_payload,
    error_diagnostic,
    feedback,
)

POLICY = json.loads(
    (
        Path(__file__).resolve().parents[2] / "shared/policies/groq-free-campaign.json"
    ).read_text()
)


class Response(io.BytesIO):
    def __init__(self, payload, headers=None):
        super().__init__(json.dumps(payload).encode())
        self.headers = headers or {}


class ProviderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="provider-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.policy = copy.deepcopy(POLICY)
        self.owner = self.root / "projects/p00/evals/live-execution.json"
        self.owner.parent.mkdir(parents=True)
        self.owner.write_text(
            json.dumps(
                {
                    "project": "p00",
                    "execution_enabled": True,
                    "synthetic_only": True,
                    "account_policy": POLICY["policy_id"],
                    "provider_timeout_seconds": 15,
                }
            )
        )
        (self.root / ".env").write_text(
            "GROQ_API_KEY_1=synthetic-a\nGROQ_API_KEY_2=synthetic-b\n"
        )
        self.posts = []
        self.catalog_headers = {}
        self.reply = {
            "model": MODEL,
            "choices": [
                {
                    "finish_reason": "stop",
                    "message": {
                        "content": "private synthetic answer",
                        "reasoning": "never return chain of thought",
                    },
                }
            ],
            "usage": {
                "prompt_tokens": 20,
                "completion_tokens": 10,
                "total_tokens": 30,
                "completion_tokens_details": {"reasoning_tokens": 5},
            },
        }
        self.failure = None
        self.envelope = {
            "campaign_id": "candidate-1",
            "case_id": "case-1",
            "trial": 1,
            "call_index": 1,
            "payload": {
                "messages": [{"role": "user", "content": "Synthetic support question"}],
                "max_completion_tokens": 256,
            },
        }

    def request(self, request, *, timeout):
        if request.get_method() == "GET":
            return Response({"data": [{"id": MODEL}]}, self.catalog_headers)
        self.posts.append((request.full_url, json.loads(request.data), timeout))
        account = SharedAccount(self.root, self.policy)
        self.assertEqual(
            account.snapshot()["uncertain_attempts"], 1, "reserve before HTTP"
        )
        if self.failure:
            raise self.failure
        return Response(
            self.reply,
            {
                "x-ratelimit-limit-requests": "1000",
                "x-ratelimit-limit-tokens": "8000",
                "unrecognized-secret-header": "never store",
            },
        )

    def session(self):
        return ProviderSession(
            self.root, "p00", self.policy, request=self.request, mode="live"
        )

    def test_accounted_single_attempt_reconciles_usage_without_content_logs(self):
        session = self.session()
        result = session.complete(self.envelope)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["usage"], {"input_tokens": 20, "output_tokens": 10})
        self.assertNotIn("reasoning", result)
        self.assertEqual(len(self.posts), 1)
        url, body, timeout = self.posts[0]
        self.assertEqual(url, "https://api.groq.com/openai/v1/chat/completions")
        self.assertIs(body["include_reasoning"], False)
        self.assertEqual(body["reasoning_effort"], "low")
        self.assertEqual(timeout, 15)
        state = session.account.snapshot()
        self.assertEqual(state["uncertain_attempts"], 0)
        self.assertEqual(state["cumulative_accounted_usage"]["input_tokens"], "20")
        content = session.account.path("p00").read_bytes()
        self.assertNotIn(b"private synthetic answer", content)
        self.assertNotIn(b"never store", content)
        self.assertNotIn(b"synthetic-a", content)

    def test_reservation_preview_checks_limits_without_consuming_or_dispatching(self):
        self.policy["campaign_caps"]["requests"] = 1
        session = self.session()
        for _ in range(3):
            self.assertEqual(session.preview(self.envelope)["status"], "approved")
        self.assertEqual(session.account.snapshot()["accounted_attempts"], 0)
        self.assertEqual(self.posts, [])
        session.complete(self.envelope)
        self.envelope["case_id"] = "case-2"
        with self.assertRaisesRegex(AccountBlocked, "cumulative_account"):
            session.preview(self.envelope)

    def test_lower_authenticated_preflight_token_limit_blocks_before_reservation(self):
        self.catalog_headers = {
            "x-ratelimit-limit-requests": "1000",
            "x-ratelimit-limit-tokens": "1",
            "x-ratelimit-remaining-tokens": "1000",
            "x-ratelimit-reset-tokens": "30s",
        }
        session = self.session()
        with self.assertRaisesRegex(AccountBlocked, "free_token_minute_checkpoint"):
            session.complete(self.envelope)
        self.assertEqual(self.posts, [])
        self.assertEqual(session.account.snapshot()["accounted_attempts"], 0)

    def test_authenticated_remaining_tokens_block_before_provider_http(self):
        self.catalog_headers = {
            "x-ratelimit-limit-requests": "1000",
            "x-ratelimit-limit-tokens": "8000",
            "x-ratelimit-remaining-tokens": "1",
            "x-ratelimit-reset-tokens": "45s",
        }
        session = self.session()
        with self.assertRaisesRegex(
            AccountBlocked, "provider_token_capacity_checkpoint"
        ):
            session.complete(self.envelope)
        self.assertEqual(self.posts, [])
        self.assertEqual(session.account.snapshot()["accounted_attempts"], 0)

    def test_owner_opt_in_and_explicit_live_mode_precede_keys_or_writes(self):
        (self.root / ".env").unlink()
        with self.assertRaisesRegex(AccountBlocked, "explicit_live"):
            ProviderSession(self.root, "p00", self.policy, mode="fake")
        self.owner.unlink()
        with self.assertRaisesRegex(AccountBlocked, "manifest_missing"):
            ProviderSession(self.root, "p00", self.policy, mode="live")
        self.assertFalse((self.root / "projects/p00/artifacts").exists())

    def test_schema_tools_and_multibyte_text_are_in_full_input_bound(self):
        session = self.session()
        self.envelope["payload"]["messages"][0]["content"] = "界" * 700
        with self.assertRaisesRegex(AccountBlocked, "full_request_input_bound"):
            session.complete(self.envelope)
        self.envelope["payload"]["messages"][0]["content"] = "short"
        self.envelope["payload"]["tools"] = [
            {
                "type": "function",
                "function": {"name": "lookup", "description": "x" * 2500},
            }
        ]
        with self.assertRaisesRegex(AccountBlocked, "full_request_input_bound"):
            session.complete(self.envelope)
        self.assertEqual(self.posts, [])
        self.assertEqual(session.account.snapshot()["accounted_attempts"], 0)

    def test_output_caps_and_builtin_tools_cannot_be_enabled(self):
        caps = self.policy["projects"]["p00"]
        for update in (
            {"max_completion_tokens": 257},
            {"model": "alternate"},
            {"include_reasoning": True},
            {"tools": [{"type": "browser_search"}]},
        ):
            payload = {**self.envelope["payload"], **update}
            with self.assertRaises(AccountBlocked):
                encode_payload(payload, caps)

    def test_provider_quota_never_rotates_keys_or_retries(self):
        session = self.session()
        self.failure = HTTPError(
            "https://api.groq.com/openai/v1/chat/completions",
            429,
            "sensitive error",
            {"Retry-After": "3"},
            io.BytesIO(b'{"error":"daily quota"}'),
        )
        result = session.complete(self.envelope)
        self.assertEqual((result["status"], result["reason"]), ("INCOMPLETE", "quota"))
        self.assertNotIn("sensitive", json.dumps(result))
        self.assertEqual(len(self.posts), 1)
        self.envelope["case_id"] = "case-2"
        with self.assertRaisesRegex(AccountBlocked, "cooldown"):
            session.complete(self.envelope)

    def test_transport_timeout_keeps_full_reservation(self):
        session = self.session()
        self.failure = URLError("sensitive transport body")
        result = session.complete(self.envelope)
        self.assertEqual(result["reason"], "transport")
        self.assertEqual(len(self.posts), 1)
        self.assertEqual(
            session.account.snapshot()["cumulative_accounted_usage"]["output_tokens"],
            "256",
        )

    def test_authentication_failure_does_not_rotate_or_expose_response(self):
        session = self.session()
        self.failure = HTTPError(
            "https://api.groq.com/openai/v1/chat/completions",
            401,
            "private error",
            {},
            io.BytesIO(b"private provider diagnostic"),
        )
        result = session.complete(self.envelope)
        self.assertEqual(result["reason"], "credential")
        self.assertEqual(len(self.posts), 1)
        self.assertNotIn("private", json.dumps(result))

    def test_json_generation_failure_keeps_categorical_code_without_failed_content(
        self,
    ):
        session = self.session()
        body = {
            "error": {
                "code": "json_validate_failed",
                "message": "PRIVATE_DIAGNOSTIC",
                "failed_generation": "PRIVATE_GENERATION",
            }
        }
        self.failure = HTTPError(
            "https://api.groq.com/openai/v1/chat/completions",
            400,
            "private error",
            {},
            io.BytesIO(json.dumps(body).encode()),
        )
        result = session.complete(self.envelope)
        self.assertEqual(
            (result["reason"], result["http_status"], result["provider_error_code"]),
            ("output_schema", 400, "json_validate_failed"),
        )
        self.assertNotIn("PRIVATE", json.dumps(result))
        self.assertEqual(len(self.posts), 1)
        self.assertEqual(
            session.account.snapshot()["cumulative_accounted_usage"]["output_tokens"],
            "256",
        )

    def test_error_taxonomy_preserves_only_allowlisted_codes(self):
        examples = [
            (400, "tool_use_failed", "tool_selection"),
            (400, "context_length_exceeded", "request_schema"),
            (401, "invalid_api_key", "credential"),
            (403, "model_permission_blocked", "model_access"),
            (429, "insufficient_quota", "quota"),
            (429, "rate_limit_exceeded", "rate_limit"),
            (503, None, "transport"),
            (408, None, "transport"),
            (409, None, "transport"),
            (400, "PRIVATE_SECRET_CODE", "request_schema"),
        ]
        for status, code, category in examples:
            with self.subTest(status=status, code=code):
                diagnostic = error_diagnostic(
                    status,
                    json.dumps(
                        {
                            "error": {
                                "code": code,
                                "message": "PRIVATE_DIAGNOSTIC",
                                "failed_generation": "PRIVATE_BODY",
                            }
                        }
                    ).encode(),
                )
                self.assertEqual(diagnostic[0], category)
                self.assertNotIn("PRIVATE", json.dumps(diagnostic))

    def test_semantic_output_and_truncation_are_returned_once_for_product_grading(self):
        session = self.session()
        self.reply["choices"][0]["finish_reason"] = "length"
        self.reply["choices"][0]["message"]["content"] = '{"truncated":'
        result = session.complete(self.envelope)
        self.assertEqual(result["finish_reason"], "length")
        self.assertEqual(len(self.posts), 1)
        with self.assertRaisesRegex(AccountBlocked, "already_reserved"):
            session.complete(self.envelope)

    def test_invalid_usage_is_not_credited_as_zero(self):
        session = self.session()
        self.reply["usage"]["total_tokens"] = 999
        result = session.complete(self.envelope)
        self.assertEqual(result["reason"], "accounting")
        charged = session.account.snapshot()["cumulative_accounted_usage"]
        self.assertGreater(int(charged["input_tokens"]), 20)
        self.assertEqual(charged["output_tokens"], "256")

    def test_observed_model_mismatch_stops_all_later_attempts(self):
        session = self.session()
        self.reply["model"] = "unexpected-model"
        result = session.complete(self.envelope)
        self.assertEqual(result["reason"], "model_access")
        self.envelope["case_id"] = "case-2"
        with self.assertRaisesRegex(AccountBlocked, "model_mismatch_requires_review"):
            session.complete(self.envelope)
        self.assertEqual(len(self.posts), 1)

    def test_actual_usage_over_input_bound_is_retained_and_stops(self):
        session = self.session()
        self.reply["usage"] = {"prompt_tokens": 2100, "completion_tokens": 10}
        result = session.complete(self.envelope)
        self.assertEqual(result["reason"], "accounting_overrun")
        self.assertEqual(
            session.account.snapshot()["cumulative_accounted_usage"]["input_tokens"],
            "2100",
        )
        self.envelope["case_id"] = "case-2"
        with self.assertRaisesRegex(AccountBlocked, "overrun"):
            session.complete(self.envelope)

    def test_header_normalization_keeps_only_numeric_scope_correct_metadata(self):
        result = feedback(
            {
                "X-RateLimit-Remaining-Tokens": "123",
                "Authorization": "secret",
                "x-ratelimit-reset-requests": "2m3.5s",
                "retry-after": "Infinity",
            }
        )
        self.assertEqual(
            result, {"remaining_tokens": 123, "request_reset_seconds": 123.5}
        )
        self.assertNotIn("daily_tokens", json.dumps(result))
        self.assertIsNone(duration("untrusted value"))


if __name__ == "__main__":
    unittest.main()
