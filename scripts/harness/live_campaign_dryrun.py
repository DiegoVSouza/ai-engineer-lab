#!/usr/bin/env python3
"""Aggregate offline dry-runs for the six independent live campaigns."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECTS = ("p00", "p01", "p02", "p03", "p04", "p05")
STAGES = ("pilot", "development", "holdout")
REQUIRED_FALSE_FLAGS = ("provider_accessed", "credentials_read", "docker_mutated")
SHARED_BLOCKERS = (
    "Groq account free-tier quota evidence: PENDING",
    "Shared cumulative request/input/output/spend ceilings: PENDING",
    "Cross-project account-wide ledger and lease enforcement: PENDING",
    "Independent reviewer approval and human review capacity: PENDING",
    "Authenticated model catalog preflight: REQUIRED BEFORE GENERATION",
)


@dataclass(frozen=True)
class Invocation:
    project: str
    stage: str
    exit_code: int
    summary: dict[str, Any] | None
    error: str | None = None


def _find_number(value: Any, names: tuple[str, ...]) -> int | None:
    if isinstance(value, dict):
        for name in names:
            candidate = value.get(name)
            if isinstance(candidate, int) and not isinstance(candidate, bool):
                return candidate
        for child in value.values():
            result = _find_number(child, names)
            if result is not None:
                return result
    elif isinstance(value, list):
        for child in value:
            result = _find_number(child, names)
            if result is not None:
                return result
    return None


def summarize_project(project: str, stages: dict[str, dict[str, Any]]) -> dict[str, Any]:
    pilot = stages["pilot"]
    development = stages["development"]
    holdout = stages["holdout"]
    plan = pilot
    primary_planned = _find_number(
        plan,
        ("primary_campaign_max_calls", "planned_primary_calls"),
    )
    confirmation = _find_number(
        plan,
        ("confirmation_max_calls", "planned_confirmation_calls"),
    )
    explicit_additive = _find_number(
        plan,
        ("all_stages_max_calls_if_additive", "planned_all_stages_calls_if_additive"),
    )
    primary_observed = development["max_provider_calls"] + holdout["max_provider_calls"]
    primary_input = _find_number(
        plan,
        ("primary_campaign_max_input_tokens", "planned_primary_input_tokens"),
    )
    primary_output = _find_number(
        plan,
        ("primary_campaign_max_output_tokens", "planned_primary_output_tokens"),
    )
    confirmation_input = _find_number(plan, ("confirmation_max_input_tokens",))
    confirmation_output = _find_number(plan, ("confirmation_max_output_tokens",))
    expected_additive = (
        primary_observed + pilot["max_provider_calls"] + confirmation
        if confirmation is not None
        else None
    )
    blockers = sorted(
        {
            blocker
            for stage in stages.values()
            for blocker in stage.get("blockers", [])
            if isinstance(blocker, str)
        }
    )
    return {
        "project": project,
        "safety": {
            "provider_accessed": False,
            "credentials_read": False,
            "docker_mutated": False,
        },
        "cases": {
            "development": development["cases"],
            "holdout": holdout["cases"],
            "unique_total": development["cases"] + holdout["cases"],
        },
        "pilot": {
            "cases": pilot["cases"],
            "logical_trials": pilot["logical_trials"],
            "max_provider_calls": pilot["max_provider_calls"],
        },
        "primary": {
            "development_max_calls": development["max_provider_calls"],
            "holdout_max_calls": holdout["max_provider_calls"],
            "max_calls": primary_observed,
            "config_planned_max_calls": primary_planned,
            "max_input_tokens": primary_input,
            "max_output_tokens": primary_output,
        },
        "confirmation_max_calls": confirmation,
        "confirmation_max_input_tokens": confirmation_input,
        "confirmation_max_output_tokens": confirmation_output,
        "all_stages_max_calls_if_additive": explicit_additive,
        "additive_cross_check": {
            "computed_from_pilot_primary_confirmation": expected_additive,
            "matches_config": (
                expected_additive == explicit_additive
                if expected_additive is not None and explicit_additive is not None
                else None
            ),
        },
        "blockers": blockers,
        "stages": stages,
    }


def validate_payload(
    project: str, stage: str, exit_code: int, stdout: str
) -> tuple[dict[str, Any] | None, str | None]:
    if exit_code != 0:
        return None, "dry-run returned nonzero exit"
    try:
        report = json.loads(stdout)
    except json.JSONDecodeError:
        return None, "output is not JSON"
    if not isinstance(report, dict):
        return None, "output is not an object"
    for flag in REQUIRED_FALSE_FLAGS:
        if report.get(flag) is not False:
            return None, f"required safety flag {flag}=false is missing"
    if report.get("generation_authorized") is not False:
        return None, "generation_authorized is not false"
    if report.get("project") not in {None, project}:
        return None, "project identity mismatch"
    if report.get("stage") != stage:
        return None, "stage identity mismatch"
    cases = report.get("cases")
    logical_trials = report.get(
        "logical_trials", report.get("logical_cases_trials_ceiling")
    )
    if not isinstance(cases, int) or not isinstance(logical_trials, int):
        return None, "case/trial counts missing"
    max_calls = report.get(
        "max_provider_calls", report.get("gross_provider_call_reservation_ceiling")
    )
    if not isinstance(max_calls, int):
        return None, "call ceiling missing"
    blockers = report.get("blockers")
    if not isinstance(blockers, list) or not blockers:
        return None, "pending blockers missing"
    report["cases"] = cases
    report["logical_trials"] = logical_trials
    report["max_provider_calls"] = max_calls
    return report, None


def invoke(project: str, stage: str) -> Invocation:
    project_root = ROOT / "projects" / project
    command = [
        sys.executable,
        "-S",
        str(project_root / "scripts" / "run_live_campaign.py"),
        "--stage",
        stage,
        "--dry-run",
    ]
    child_env = os.environ.copy()
    for name in tuple(child_env):
        if name.startswith("GROQ_API_KEY"):
            child_env.pop(name, None)
    child_env["LLM_MODE"] = "fake"
    try:
        result = subprocess.run(
            command,
            cwd=project_root,
            env=child_env,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return Invocation(project, stage, 124, None, "dry-run timed out")
    report, error = validate_payload(project, stage, result.returncode, result.stdout)
    if error is not None:
        return Invocation(project, stage, result.returncode, None, error)
    assert report is not None
    return Invocation(project, stage, result.returncode, report)


def run_all() -> dict[str, Any]:
    invocations = [invoke(project, stage) for project in PROJECTS for stage in STAGES]
    project_reports: dict[str, Any] = {}
    errors: list[dict[str, Any]] = []
    for item in invocations:
        if item.summary is None:
            errors.append(
                {
                    "project": item.project,
                    "stage": item.stage,
                    "exit_code": item.exit_code,
                    "error": item.error,
                }
            )
            continue
        project_reports.setdefault(item.project, {})[item.stage] = item.summary
    normalized = {
        project: summarize_project(project, stages)
        for project, stages in project_reports.items()
        if all(stage in stages for stage in STAGES)
    }
    total_unique_cases = sum(row["cases"]["unique_total"] for row in normalized.values())
    pilot_calls = sum(row["pilot"]["max_provider_calls"] for row in normalized.values())
    primary_calls = sum(row["primary"]["max_calls"] for row in normalized.values())
    confirmation_calls = sum(
        row["confirmation_max_calls"] or 0 for row in normalized.values()
    )
    additive_calls = sum(
        row["all_stages_max_calls_if_additive"] or 0 for row in normalized.values()
    )
    primary_input_values = [
        row["primary"]["max_input_tokens"] for row in normalized.values()
    ]
    primary_output_values = [
        row["primary"]["max_output_tokens"] for row in normalized.values()
    ]
    confirmation_input_values = [
        row["confirmation_max_input_tokens"] for row in normalized.values()
    ]
    confirmation_output_values = [
        row["confirmation_max_output_tokens"] for row in normalized.values()
    ]
    cross_check_failures = [
        project
        for project, row in normalized.items()
        if row["additive_cross_check"]["matches_config"] is not True
    ]
    token_gaps = [
        f"{project}.{label} token ceiling missing from project dry-run contract"
        for project, row in normalized.items()
        for label, value in (
            ("primary_input", row["primary"]["max_input_tokens"]),
            ("primary_output", row["primary"]["max_output_tokens"]),
            ("confirmation_input", row["confirmation_max_input_tokens"]),
            ("confirmation_output", row["confirmation_max_output_tokens"]),
        )
        if value is None
    ]
    complete_project_set = set(normalized) == set(PROJECTS)
    return {
        "status": "INCOMPLETE",
        "campaign_spec": "llm-live-readiness-v1",
        "generated_by": "root offline coordinator",
        "project_count": len(normalized),
        "expected_project_count": len(PROJECTS),
        "unique_semantic_cases": total_unique_cases,
        "planned_calls": {
            "pilot_max_calls": pilot_calls,
            "primary_max_calls": primary_calls,
            "fresh_confirmation_max_calls": confirmation_calls,
            "all_additive_max_calls": additive_calls,
        },
        "planned_tokens": {
            "primary_input": (
                sum(primary_input_values)
                if all(isinstance(value, int) for value in primary_input_values)
                else None
            ),
            "primary_output": (
                sum(primary_output_values)
                if all(isinstance(value, int) for value in primary_output_values)
                else None
            ),
            "confirmation_input": (
                sum(confirmation_input_values)
                if all(isinstance(value, int) for value in confirmation_input_values)
                else None
            ),
            "confirmation_output": (
                sum(confirmation_output_values)
                if all(isinstance(value, int) for value in confirmation_output_values)
                else None
            ),
        },
        "shared_blockers": list(SHARED_BLOCKERS),
        "reservation_gaps": token_gaps,
        "errors": errors,
        "cross_check_failures": cross_check_failures,
        "generation_authorized": False,
        "provider_accessed": False,
        "credentials_read": False,
        "docker_mutated": False,
        "complete_project_set": complete_project_set,
        "projects": normalized,
        "invocations": [
            {
                "project": item.project,
                "stage": item.stage,
                "command": [
                    "python",
                    "-S",
                    f"projects/{item.project}/scripts/run_live_campaign.py",
                    "--stage",
                    item.stage,
                    "--dry-run",
                ],
                "exit_code": item.exit_code,
                "provider_accessed": False,
                "credentials_read": False,
                "docker_mutated": False,
                "result": "PASS" if item.summary is not None else "INCOMPLETE",
                "error": item.error,
            }
            for item in invocations
        ],
    }


def main() -> int:
    report = run_all()
    output_dir = ROOT / "artifacts/evidence/llm-live-readiness/global-dry-run"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "report.md").write_text(render_markdown(report), encoding="utf-8")
    compact = {
        key: report[key]
        for key in (
            "status",
            "project_count",
            "expected_project_count",
            "unique_semantic_cases",
            "planned_calls",
            "shared_blockers",
            "errors",
            "planned_tokens",
            "reservation_gaps",
            "cross_check_failures",
            "generation_authorized",
            "provider_accessed",
            "credentials_read",
            "docker_mutated",
        )
    }
    print(json.dumps(compact, ensure_ascii=False, sort_keys=True, indent=2))
    return (
        0
        if report["complete_project_set"]
        and not report["errors"]
        and not report["cross_check_failures"]
        else 2
    )


def render_markdown(report: dict[str, Any]) -> str:
    tokens = report["planned_tokens"]
    lines = [
        "# Account-wide campaign dry-run",
        "",
        f"Status: `{report['status']}`. Generation authorized: `false`.",
        "",
        f"Projects: {report['project_count']}/{report['expected_project_count']}; "
        f"unique semantic cases: {report['unique_semantic_cases']}.",
        "",
        "| Project | Dev | Holdout | Pilot calls | Primary calls | Confirmation calls | Additive calls |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for project in PROJECTS:
        row = report["projects"].get(project)
        if row is None:
            lines.append(f"| {project} | INCOMPLETE | INCOMPLETE | — | — | — | — |")
            continue
        lines.append(
            f"| {project} | {row['cases']['development']} | {row['cases']['holdout']} | "
            f"{row['pilot']['max_provider_calls']} | {row['primary']['max_calls']} | "
            f"{row['confirmation_max_calls']} | {row['all_stages_max_calls_if_additive']} |"
        )
    lines.extend(
        [
            "",
            f"Aggregate planned calls: pilot {report['planned_calls']['pilot_max_calls']}, "
            f"primary {report['planned_calls']['primary_max_calls']}, "
            f"confirmation {report['planned_calls']['fresh_confirmation_max_calls']}, "
            f"all additive {report['planned_calls']['all_additive_max_calls']}.",
            "",
            "Token ceilings: primary input="
            f"{tokens['primary_input'] if tokens['primary_input'] is not None else 'PENDING'}, "
            "primary output="
            f"{tokens['primary_output'] if tokens['primary_output'] is not None else 'PENDING'}, "
            "confirmation input="
            f"{tokens['confirmation_input'] if tokens['confirmation_input'] is not None else 'PENDING'}, "
            "confirmation output="
            f"{tokens['confirmation_output'] if tokens['confirmation_output'] is not None else 'PENDING'}.",
            "",
            "Shared blockers:",
            "",
        ]
    )
    lines.extend(f"- {blocker}" for blocker in report["shared_blockers"])
    lines.extend(f"- Reservation gap: {gap}." for gap in report["reservation_gaps"])
    for error in report["errors"]:
        lines.append(
            f"- {error['project']} {error['stage']} dry-run failed: {error['error']} "
            f"(exit {error['exit_code']})."
        )
    lines.extend(["", "No provider or Docker access occurred.", ""])
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
