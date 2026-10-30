import json
import unittest

from audit_codex_rollout import summarize


def row(kind, **payload):
    return json.dumps({"type": kind, "payload": payload})


class RolloutAuditTests(unittest.TestCase):
    def test_model_switches_and_phase_are_not_conflated(self):
        report = summarize([
            row("turn_context", model="gpt-6-luna", effort="medium"),
            row("response_item", type="message", role="assistant", phase="commentary"),
            row("response_item", type="function_call", arguments="SECRET"),
            row("response_item", type="message", role="assistant", phase="final_answer"),
            row("turn_context", model="gpt-6.1-sol", effort="high"),
            row("response_item", type="message", role="assistant"),
        ])
        first, second = report["turns"]
        self.assertEqual(first["messages"], {"commentary": 1, "final_answer": 1})
        self.assertEqual(first["tool_calls"], 1)
        self.assertEqual(second["messages"], {"missing_or_unknown": 1})
        self.assertEqual(second["model"], "gpt-6.1-sol")
        self.assertEqual(second["termination_reason"], "UNKNOWN")
        self.assertNotIn("SECRET", json.dumps(report))

    def test_truncated_and_invalid_records_are_reported(self):
        report = summarize(['{"type":', '[]', '{"payload": null}'])
        self.assertEqual(report["malformed_records"], 3)
        self.assertEqual(report["turns"], [])

    def test_content_and_unrecognized_metadata_are_excluded(self):
        report = summarize([
            row("turn_context", model="SECRET", effort="SECRET", cwd="SECRET"),
            row("response_item", type="message", role="assistant", phase="SECRET", content="SECRET"),
            row("event_msg", type="error", message="SECRET"),
        ])
        self.assertNotIn("SECRET", json.dumps(report))
        self.assertEqual(report["wire_phase_preservation"], "NOT_VERIFIED")


if __name__ == "__main__":
    unittest.main()
