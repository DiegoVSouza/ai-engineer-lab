#!/usr/bin/env python3
"""Clone each repository to an empty directory and run its documented fast gate, as a stranger would."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAIL = 1500


def run(command: list[str], cwd: Path, env: dict, timeout: int) -> dict:
    started = time.monotonic()
    try:
        result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, errors="replace", timeout=timeout)
        return {"command": " ".join(command), "exit": result.returncode, "seconds": round(time.monotonic() - started),
                "tail": (result.stdout + result.stderr)[-TAIL:]}
    except subprocess.TimeoutExpired:
        return {"command": " ".join(command), "exit": "timeout", "seconds": timeout, "tail": ""}


def check(name: str, base: Path, timeout: int) -> dict:
    source = ROOT / "projects" / name
    target = base / name
    env = {key: value for key, value in os.environ.items() if key not in {"VIRTUAL_ENV", "PYTHONPATH"}}
    steps = [run(["git", "clone", "--quiet", str(source), str(target)], base, env, 120)]
    if steps[0]["exit"] != 0:
        return {"steps": steps, "passed": False}
    if (target / "package.json").exists():
        steps.append(run([shutil.which("npm") or "npm", "ci", "--ignore-scripts"], target, env, timeout))
        steps.append(run([sys.executable, "scripts/check_fast.py"], target, env, timeout))
    else:
        steps.append(run([shutil.which("uv") or "uv", "sync", "--locked", "--all-extras"], target, env, timeout))
        steps.append(run([shutil.which("uv") or "uv", "run", "python", "scripts/check_fast.py"], target, env, timeout))
    return {"steps": steps, "passed": all(step["exit"] == 0 for step in steps)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=ROOT / "artifacts/evidence/public-readiness/clean-clone.json")
    parser.add_argument("--timeout", type=int, default=420)
    parser.add_argument("--only", nargs="*", default=[f"p{n:02d}" for n in range(9)])
    args = parser.parse_args()
    args.base.mkdir(parents=True, exist_ok=True)
    report = {}
    for name in args.only:
        report[name] = check(name, args.base, args.timeout)
        print(name, "PASS" if report[name]["passed"] else "FAIL", [step["exit"] for step in report[name]["steps"]], flush=True)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return 0 if all(item["passed"] for item in report.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
