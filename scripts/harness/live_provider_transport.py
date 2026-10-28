#!/usr/bin/env python3
"""Versioned JSON-lines boundary for accounted, synthetic-only Groq attempts."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

from live_free_account import (
    MODEL,
    ROOT,
    AccountBlocked,
    SharedAccount,
    catalog_preflight,
    integer,
    numbered_keys,
)

MAX_PROTOCOL_BYTES = 131072
PROVIDER_ERROR_CODES = {
    "json_validate_failed": "output_schema",
    "tool_use_failed": "tool_selection",
    "context_length_exceeded": "request_schema",
    "invalid_request_error": "request_schema",
    "invalid_api_key": "credential",
    "authentication_error": "credential",
    "model_not_found": "model_access",
    "model_permission_blocked": "model_access",
    "rate_limit_exceeded": "rate_limit",
    "insufficient_quota": "quota",
    "billing_hard_limit_reached": "quota",
    "blocked_api_access": "quota",
}


def error_diagnostic(status, raw):
    try:
        parsed = json.loads(raw)
        error = parsed.get("error", {}) if isinstance(parsed, dict) else {}
    except (ValueError, TypeError):
        error = {}
    code = error.get("code") if isinstance(error, dict) else None
    code = code if isinstance(code, str) and code in PROVIDER_ERROR_CODES else "OTHER"
    message = (
        error.get("message", "")
        if isinstance(error, dict)
        else raw.decode("utf-8", errors="replace")
    )
    message = message.lower() if isinstance(message, str) else ""
    if status in {401, 403}:
        category = (
            "model_access" if code == "model_permission_blocked" else "credential"
        )
    elif code in {
        "insufficient_quota",
        "billing_hard_limit_reached",
        "blocked_api_access",
    } or (
        status == 429
        and any(term in message for term in ("per day", "daily", "insufficient_quota"))
    ):
        category = "quota"
    elif status == 429:
        category = "rate_limit"
    elif code in PROVIDER_ERROR_CODES:
        category = PROVIDER_ERROR_CODES[code]
    elif status == 404:
        category = "model_access"
    else:
        category = (
            "transport"
            if status in {408, 409, 499} or status >= 500
            else "request_schema"
        )
    return category, code


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request_https(request, *, timeout):
    return build_opener(NoRedirect()).open(request, timeout=timeout)


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


def encode_payload(payload, caps):
    allowed = {
        "model",
        "messages",
        "max_completion_tokens",
        "temperature",
        "response_format",
        "tools",
        "tool_choice",
        "parallel_tool_calls",
        "reasoning_effort",
        "include_reasoning",
    }
    if not isinstance(payload, dict) or not set(payload) <= allowed:
        raise AccountBlocked("unsupported_request_fields")
    body = dict(payload)
    if (
        body.get("model", MODEL) != MODEL
        or body.get("include_reasoning", False) is not False
    ):
        raise AccountBlocked("fixed_model_and_hidden_reasoning_required")
    messages = body.get("messages")
    if (
        not isinstance(messages, list)
        or not 1 <= len(messages) <= 16
        or any(
            not isinstance(item, dict)
            or item.get("role") not in {"system", "user", "assistant", "tool"}
            or (
                item.get("content") is not None and not isinstance(item["content"], str)
            )
            for item in messages
        )
    ):
        raise AccountBlocked("invalid_messages")
    tools = body.get("tools", [])
    if (
        not isinstance(tools, list)
        or len(tools) > 8
        or any(
            not isinstance(tool, dict) or tool.get("type") != "function"
            for tool in tools
        )
    ):
        raise AccountBlocked("only_bounded_local_function_tools_supported")
    output = integer(body.get("max_completion_tokens"), 1)
    if output > caps["output_tokens_per_call"]:
        raise AccountBlocked("original_output_cap_exceeded")
    if body.get("reasoning_effort", "low") not in {"low", "medium", "high"}:
        raise AccountBlocked("unsupported_reasoning_configuration")
    temperature = body.get("temperature", 0)
    if (
        type(temperature) not in (int, float)
        or not math.isfinite(temperature)
        or not 0 <= temperature <= 1
    ):
        raise AccountBlocked("invalid_generation_temperature")
    body.update(
        model=MODEL,
        stream=False,
        include_reasoning=False,
        reasoning_effort=body.get("reasoning_effort", "low"),
    )
    encoded = json.dumps(
        body, ensure_ascii=False, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    # Byte-level BPE cannot need more tokens than UTF-8 bytes; add bounded
    # chat/tool framing slack, and stop if observed usage ever exceeds it.
    input_bound = len(encoded) + 256 + 64 * len(messages) + 128 * len(tools)
    if input_bound > caps["input_tokens_per_call"]:
        raise AccountBlocked("full_request_input_bound_exceeds_cap")
    return encoded, input_bound, output


class ProviderSession:
    def __init__(self, root, project, policy, *, request=request_https, mode=None):
        self.root = Path(root)
        self.project = project
        self.account = SharedAccount(self.root, policy)
        if (mode if mode is not None else os.getenv("LLM_MODE", "fake")) != "live":
            raise AccountBlocked("explicit_live_mode_required")
        try:
            owner = json.loads(
                (
                    self.root / "projects" / project / "evals/live-execution.json"
                ).read_text()
            )
        except (OSError, ValueError):
            raise AccountBlocked("owning_project_execution_manifest_missing") from None
        if (
            owner.get("project") != project
            or owner.get("execution_enabled") is not True
            or owner.get("synthetic_only") is not True
            or owner.get("account_policy") != policy["policy_id"]
        ):
            raise AccountBlocked("owning_project_execution_not_authorized")
        timeout = owner.get("provider_timeout_seconds")
        if (
            type(timeout) not in (int, float)
            or not math.isfinite(timeout)
            or not 0 < timeout <= 30
        ):
            raise AccountBlocked("finite_provider_timeout_required")
        self.timeout = timeout
        self._request = request
        self._keys = numbered_keys(self.root)
        self.preflight = catalog_preflight(self.root, request=request, keys=self._keys)
        if self.preflight["status"] != "PASS":
            raise AccountBlocked("authenticated_model_catalog_incomplete")
        self.account.register(project)
        self.account.set_authenticated_feedback(
            self.preflight.get("authenticated_rate_limits", {})
        )

    def preview(self, envelope):
        caps = self.account.policy["projects"][self.project]
        _, input_bound, output_bound = encode_payload(envelope.get("payload"), caps)
        return self.account.preview(
            self.project,
            envelope["campaign_id"],
            envelope["case_id"],
            envelope["trial"],
            envelope["call_index"],
            input_bound,
            output_bound,
        )

    def complete(self, envelope):
        if not isinstance(envelope, dict) or set(envelope) - {
            "campaign_id",
            "case_id",
            "trial",
            "call_index",
            "payload",
            "timeout_seconds",
        }:
            raise AccountBlocked("invalid_attempt_envelope")
        caps = self.account.policy["projects"][self.project]
        encoded, input_bound, output_bound = encode_payload(
            envelope.get("payload"), caps
        )
        timeout = envelope.get("timeout_seconds", self.timeout)
        if (
            type(timeout) not in (int, float)
            or not math.isfinite(timeout)
            or not 0 < timeout <= self.timeout
        ):
            raise AccountBlocked("request_timeout_exceeds_owner_limit")
        attempt = self.account.reserve(
            self.project,
            envelope["campaign_id"],
            envelope["case_id"],
            envelope["trial"],
            envelope["call_index"],
            input_bound,
            output_bound,
        )
        req = Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=encoded,
            headers={
                "Authorization": "Bearer " + self._keys[
                    (self.account.snapshot()["accounted_attempts"] - 1) % len(self._keys)
                ],
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "supportops-lab-readiness/1.0",
            },
            method="POST",
        )
        started = time.monotonic()
        try:
            with self._request(req, timeout=timeout) as response:
                observed_limits = feedback(response.headers)
                raw = response.read(2000001)
            if len(raw) > 2000000:
                raise ValueError("response too large")
            result = json.loads(raw)
        except HTTPError as exc:
            observed_limits = feedback(exc.headers or {})
            status = exc.code
            # Only whitelisted categorical codes survive this boundary.
            category, code = error_diagnostic(status, exc.read(65536))
            exc.close()
            self.account.complete(
                self.project,
                attempt,
                status="quota" if category == "quota" else "provider_error",
                feedback=observed_limits,
            )
            return {
                "status": "INCOMPLETE",
                "reason": category,
                "http_status": status,
                "provider_error_code": code,
                "attempt_id": attempt,
            }
        except (URLError, OSError, TimeoutError):
            self.account.complete(self.project, attempt, status="transport_error")
            return {
                "status": "INCOMPLETE",
                "reason": "transport",
                "attempt_id": attempt,
            }
        except (ValueError, TypeError):
            self.account.complete(self.project, attempt, status="provider_error")
            return {
                "status": "INCOMPLETE",
                "reason": "output_schema",
                "attempt_id": attempt,
            }
        try:
            usage = result["usage"]
            inp, out = (
                integer(usage["prompt_tokens"]),
                integer(usage["completion_tokens"]),
            )
            if "total_tokens" in usage and integer(usage["total_tokens"]) != inp + out:
                raise AccountBlocked("inconsistent_provider_usage")
            details = usage.get("completion_tokens_details") or {}
            if integer(details.get("reasoning_tokens", 0)) > out:
                raise AccountBlocked("reasoning_usage_inconsistent")
        except (AccountBlocked, KeyError, TypeError):
            self.account.complete(
                self.project, attempt, status="provider_error", feedback=observed_limits
            )
            return {
                "status": "INCOMPLETE",
                "reason": "accounting",
                "attempt_id": attempt,
            }
        model_matches = result.get("model") == MODEL
        self.account.complete(
            self.project,
            attempt,
            input_tokens=inp,
            output_tokens=out,
            status="ok" if model_matches else "model_mismatch",
            feedback=observed_limits,
        )
        if not model_matches:
            return {
                "status": "INCOMPLETE",
                "reason": "model_access",
                "attempt_id": attempt,
            }
        if inp > input_bound or out > output_bound:
            return {
                "status": "INCOMPLETE",
                "reason": "accounting_overrun",
                "attempt_id": attempt,
            }
        try:
            choice = result["choices"][0]
            message = choice["message"]
            content = message.get("content") or ""
            tool_calls = message.get("tool_calls") or []
            if (
                result["model"] != MODEL
                or not isinstance(content, str)
                or not isinstance(tool_calls, list)
            ):
                raise ValueError("model or schema mismatch")
        except (KeyError, IndexError, TypeError, ValueError):
            return {
                "status": "INCOMPLETE",
                "reason": "model_or_output_schema",
                "attempt_id": attempt,
            }
        return {
            "status": "ok",
            "model": MODEL,
            "content": content,
            "tool_calls": tool_calls,
            "finish_reason": choice.get("finish_reason"),
            "attempt_id": attempt,
            "usage": {"input_tokens": inp, "output_tokens": out},
            "latency_ms": round((time.monotonic() - started) * 1000, 3),
        }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project", required=True, choices=tuple(f"p{n:02d}" for n in range(6))
    )
    args = parser.parse_args(argv)
    try:
        policy = json.loads(
            (ROOT / "shared/policies/groq-free-campaign.json").read_text()
        )
        session = ProviderSession(ROOT, args.project, policy)
        print(
            json.dumps(
                {
                    "protocol_version": 1,
                    "status": "ready",
                    "preflight": session.preflight,
                }
            ),
            flush=True,
        )
        while line := sys.stdin.buffer.readline(MAX_PROTOCOL_BYTES + 1):
            if len(line) > MAX_PROTOCOL_BYTES or not line.endswith(b"\n"):
                raise AccountBlocked("invalid_protocol_frame")
            try:
                envelope = json.loads(line)
                operation = envelope.pop("operation", "complete")
                if operation not in {"preview", "complete"}:
                    raise AccountBlocked("unknown_protocol_operation")
                response = (
                    session.preview(envelope)
                    if operation == "preview"
                    else session.complete(envelope)
                )
            except AccountBlocked as exc:
                response = {"status": "INCOMPLETE", "reason": str(exc)}
            print(json.dumps(response, ensure_ascii=False), flush=True)
        return 0
    except AccountBlocked as exc:
        print(json.dumps({"status": "INCOMPLETE", "reason": str(exc)}), flush=True)
        return 2
    except Exception:  # noqa: BLE001 - No raw response, request, or credential-bearing exception may escape.
        print(
            json.dumps({"status": "INCOMPLETE", "reason": "provider_protocol_failure"}),
            flush=True,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
