#!/usr/bin/env python3
"""Clone a project at HEAD into an empty directory and run its gates in a Linux container.

Hosted CI runs on Linux, so a Windows-only pass proves little. The clone is made on the host
(P00 through a bundle, because its .git belongs to another user) and mounted into a container,
where the same steps as the project's workflow run. Nothing from the host working tree leaks in.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAIL = 2500
PYTHON_IMAGE = "python:3.13-slim-bookworm"
NODE_IMAGE = "mcr.microsoft.com/playwright:v1.64.1-noble"  # matches @playwright/test 1.64.1 in P06, P07 and P08
UV_VERSION = "0.12.7"


def sh(command: list[str], cwd: Path | None = None, timeout: int = 900) -> dict:
    started = time.monotonic()
    try:
        done = subprocess.run(command, cwd=cwd, capture_output=True, text=True, errors="replace", timeout=timeout)
        return {"command": " ".join(command[:6]) + (" ..." if len(command) > 6 else ""), "exit": done.returncode,
                "seconds": round(time.monotonic() - started), "tail": (done.stdout + done.stderr)[-TAIL:]}
    except subprocess.TimeoutExpired:
        return {"command": " ".join(command[:6]), "exit": "timeout", "seconds": timeout, "tail": ""}


def clone(name: str, base: Path) -> dict:
    source = ROOT / "projects" / name
    target = base / name
    if target.exists():
        shutil.rmtree(target, ignore_errors=True)
    if name == "p00":
        bundle = base / f"{name}.bundle"
        # P00's .git is owned by another Windows user; a bundle avoids touching safe.directory.
        made = sh(["git", "-C", str(source), "bundle", "create", str(bundle), "HEAD"], timeout=300)
        if made["exit"] != 0:
            return made
        return sh(["git", "clone", "--quiet", str(bundle), str(target)], timeout=300)
    return sh(["git", "clone", "--quiet", str(source), str(target)], timeout=300)


def docker_run(image: str, mount: Path, script: str, timeout: int) -> dict:
    # Mount read-write at /work; the container user owns nothing on the host beyond the scratch clone.
    return sh(["docker", "run", "--rm", "-v", f"{mount}:/work", "-w", "/work", "-e", "LLM_MODE=fake", image, "bash", "-lc", script],
              timeout=timeout)


def python_script(gates: list[str]) -> str:
    steps = [f"pip install --quiet uv=={UV_VERSION}", "uv sync --locked --all-extras --all-groups"] + gates
    return " && ".join(steps)


def node_script(gates: list[str]) -> str:
    return " && ".join(["npm ci --ignore-scripts"] + gates)


def check(name: str, base: Path, timeout: int, full: bool, node_image: str) -> dict:
    steps = [clone(name, base)]
    if steps[0]["exit"] != 0:
        return {"steps": steps, "passed": False}
    target = base / name
    if (target / "package.json").exists():
        gates = ["npx playwright install chrome", "python3 scripts/check_full.py"] if full else ["python3 scripts/check_fast.py"]
        # The Playwright image has Node, Python 3 and the browsers' system libraries.
        steps.append(docker_run(node_image, target, node_script(gates), timeout))
    else:
        gates = ["uv run --locked python scripts/check_full.py"] if full else ["uv run --locked python scripts/check_fast.py"]
        steps.append(docker_run(PYTHON_IMAGE, target, python_script(gates), timeout))
    return {"steps": steps, "passed": all(step["exit"] == 0 for step in steps)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=ROOT / "artifacts/evidence/public-readiness/linux-clean-clone.json")
    parser.add_argument("--timeout", type=int, default=1500)
    parser.add_argument("--full", action="store_true", help="run check_full.py instead of check_fast.py")
    parser.add_argument("--node-image", default=NODE_IMAGE)
    parser.add_argument("--only", nargs="*", default=[f"p{n:02d}" for n in range(9)])
    args = parser.parse_args()
    args.base.mkdir(parents=True, exist_ok=True)
    report = {}
    for name in args.only:
        report[name] = check(name, args.base, args.timeout, args.full, args.node_image)
        print(name, "PASS" if report[name]["passed"] else "FAIL", [step["exit"] for step in report[name]["steps"]], flush=True)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return 0 if all(item["passed"] for item in report.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
