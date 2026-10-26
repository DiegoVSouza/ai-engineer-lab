from __future__ import annotations

import json
import unittest

from live_campaign_dryrun import summarize_project, validate_payload


def stage(stage_name: str, cases: int, calls: int) -> dict:
    return {
        "stage": stage_name,
        "cases": cases,
        "logical_trials": cases,
        "max_provider_calls": calls,
        "blockers": ["quota pending"],
    }


class AggregateDryRunTests(unittest.TestCase):
    def test_all_six_project_plan_shapes_normalize(self) -> None:
        base_stages = {
            "pilot": stage("pilot", 6, 6),
            "development": stage("development", 4, 12),
            "holdout": stage("holdout", 6, 18),
        }
        shared = {
            "primary_campaign_max_calls": 30,
            "primary_campaign_max_input_tokens": 300,
            "primary_campaign_max_output_tokens": 90,
            "confirmation_max_calls": 12,
            "confirmation_max_input_tokens": 120,
            "confirmation_max_output_tokens": 36,
            "all_stages_max_calls_if_additive": 48,
        }
        shapes = {
            "p00": {**base_stages["pilot"], "planned_reservations": shared},
            "p01": {**base_stages["pilot"], "planned_reservations": shared},
            "p02": {**base_stages["pilot"], "campaign_plan": shared},
            "p03": {**base_stages["pilot"], "campaign_plan": shared},
            "p04": {**base_stages["pilot"], "campaign_plan": shared},
            "p05": {
                **base_stages["pilot"],
                "planned_primary_calls": 30,
                "planned_confirmation_calls": 12,
                "planned_all_stages_calls_if_additive": 48,
                "planned_primary_input_tokens": 300,
                "planned_primary_output_tokens": 90,
                "confirmation_max_input_tokens": 120,
                "confirmation_max_output_tokens": 36,
            },
        }
        for project, pilot in shapes.items():
            with self.subTest(project=project):
                result = summarize_project(
                    project,
                    {
                        **base_stages,
                        "pilot": pilot,
                    },
                )
                self.assertEqual(result["primary"]["max_calls"], 30)
                self.assertEqual(result["confirmation_max_calls"], 12)
                self.assertTrue(result["additive_cross_check"]["matches_config"])

    def test_normalizes_supported_project_reservation_shapes(self) -> None:
        reports = {
            "pilot": {
                **stage("pilot", 6, 6),
                "planned_reservations": {
                    "primary_campaign_max_calls": 30,
                    "confirmation_max_calls": 12,
                    "all_stages_max_calls_if_additive": 48,
                },
            },
            "development": stage("development", 4, 12),
            "holdout": stage("holdout", 6, 18),
        }
        result = summarize_project("p04", reports)
        self.assertEqual(result["cases"]["unique_total"], 10)
        self.assertEqual(result["primary"]["max_calls"], 30)
        self.assertEqual(result["confirmation_max_calls"], 12)
        self.assertEqual(result["all_stages_max_calls_if_additive"], 48)
        self.assertTrue(result["additive_cross_check"]["matches_config"])

    def test_accepts_p05_legacy_plan_names(self) -> None:
        reports = {
            "pilot": {
                **stage("pilot", 6, 24),
                "planned_primary_calls": 1440,
                "planned_confirmation_calls": 240,
                "planned_all_stages_calls_if_additive": 1704,
            },
            "development": stage("development", 36, 432),
            "holdout": stage("holdout", 84, 1008),
        }
        result = summarize_project("p05", reports)
        self.assertEqual(result["all_stages_max_calls_if_additive"], 1704)
        self.assertTrue(result["additive_cross_check"]["matches_config"])

    def test_missing_confirmation_is_not_reported_as_zero(self) -> None:
        reports = {
            "pilot": {**stage("pilot", 6, 6), "primary_campaign_max_calls": 20},
            "development": stage("development", 4, 8),
            "holdout": stage("holdout", 6, 12),
        }
        result = summarize_project("p02", reports)
        self.assertIsNone(result["confirmation_max_calls"])
        self.assertIsNone(result["all_stages_max_calls_if_additive"])
        self.assertIsNone(result["additive_cross_check"]["matches_config"])

    def test_payload_validation_rejects_failure_malformed_flags_and_missing_caps(self) -> None:
        valid = {
            "project": "p02",
            "stage": "pilot",
            "cases": 6,
            "logical_trials": 6,
            "max_provider_calls": 6,
            "blockers": ["quota pending"],
            "generation_authorized": False,
            "provider_accessed": False,
            "credentials_read": False,
            "docker_mutated": False,
        }
        summary, error = validate_payload("p02", "pilot", 0, json.dumps(valid))
        self.assertIsNone(error)
        self.assertEqual(summary["max_provider_calls"], 6)
        self.assertEqual(
            validate_payload("p02", "pilot", 1, "{}")[1],
            "dry-run returned nonzero exit",
        )
        self.assertEqual(
            validate_payload("p02", "pilot", 0, "not json")[1],
            "output is not JSON",
        )
        without_calls = {**valid}
        without_calls.pop("max_provider_calls")
        self.assertEqual(
            validate_payload("p02", "pilot", 0, json.dumps(without_calls))[1],
            "call ceiling missing",
        )
        unsafe = {**valid, "credentials_read": True}
        self.assertIn(
            "credentials_read",
            validate_payload("p02", "pilot", 0, json.dumps(unsafe))[1],
        )


if __name__ == "__main__":
    unittest.main()
