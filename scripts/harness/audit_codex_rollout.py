"""Summarize local rollout metadata without exporting message or tool content."""
import argparse
import json
from collections import Counter
from pathlib import Path


def summarize(lines):
    turns = []
    malformed = 0
    for line in lines:
        try:
            record = json.loads(line)
        except (ValueError, UnicodeError):
            malformed += 1
            continue
        if not isinstance(record, dict):
            malformed += 1
            continue
        payload = record.get("payload", {})
        if not isinstance(payload, dict):
            malformed += 1
            continue
        if record.get("type") == "turn_context":
            # Model identifiers and effort are the only string fields exported.
            model = payload.get("model")
            model = model if isinstance(model, str) and model.startswith("gpt-") and all(
                c.isalnum() or c in "-." for c in model
            ) else "UNKNOWN"
            effort = payload.get("effort", payload.get("reasoning_effort"))
            if effort not in ("none", "minimal", "low", "medium", "high", "xhigh", "max", "ultra"):
                effort = "UNKNOWN"
            turns.append({"turn": len(turns) + 1, "model": model, "effort": effort,
                          "messages": Counter(), "tool_calls": 0,
                          "termination_reason": "UNKNOWN"})
        elif turns and record.get("type") == "response_item":
            if payload.get("type") in ("function_call", "custom_tool_call"):
                turns[-1]["tool_calls"] += 1
            if payload.get("type") == "message" and payload.get("role") == "assistant":
                phase = payload.get("phase")
                if phase not in ("commentary", "final_answer"):
                    phase = "missing_or_unknown"
                turns[-1]["messages"][phase] += 1
    return {"turns": turns, "malformed_records": malformed,
            "scope": "local_metadata_only", "wire_phase_preservation": "NOT_VERIFIED"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rollout", type=Path)
    args = parser.parse_args()
    try:
        with args.rollout.open(encoding="utf-8", errors="replace") as stream:
            report = summarize(stream)
    except OSError:
        print(json.dumps({"error": "rollout_unreadable"}))
        return 2
    print(json.dumps(report, indent=2))
    return 1 if report["malformed_records"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
