#!/usr/bin/env python3
"""Create and initialize an independent project from a Harness Kit profile."""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
KIT = ROOT / "harness-kit"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="directory-safe project name, e.g. ticket-triage")
    parser.add_argument("--type", default="agent-app", help="profile in harness-kit/profiles")
    parser.add_argument("--projects-dir", type=pathlib.Path, default=ROOT / "projects")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.name):
        parser.error("name must use lowercase letters, digits, and hyphens")
    profile = KIT / "profiles" / f"{args.type}.yaml"
    if not profile.exists():
        choices = ", ".join(sorted(p.stem for p in (KIT / "profiles").glob("*.yaml")))
        parser.error(f"unknown project type {args.type!r}; choose one of: {choices}")
    destination = args.projects_dir.resolve() / args.name
    destination.mkdir(parents=True, exist_ok=True)
    config_path = destination / "harness.yaml"
    if not config_path.exists():
        text = profile.read_text(encoding="utf-8")
        text = re.sub(r"(?m)^(  name:) .*$", rf"\1 {args.name}", text, count=1)
        config_path.write_text(text, encoding="utf-8")
    else:
        print(f"new-project: resuming existing scaffold: {destination}")
    result = subprocess.run(
        [sys.executable, str(KIT / "bootstrap/harness_init.py"), "--project-dir", str(destination)],
        text=True,
    )
    if result.returncode:
        return result.returncode
    subprocess.run([sys.executable, str(ROOT / 'scripts/harness/setup-project-git.py'), '--project-dir', str(destination)], check=True)
    ignore = destination / '.gitignore'
    if not ignore.exists():
        ignore.write_text('__pycache__/\n*.py[cod]\n.venv/\n.env\n.env.*\n!.env.example\n*.pem\n*.key\n.pytest_cache/\n.ruff_cache/\n', encoding='utf-8')
    subprocess.run(['git', '-C', str(destination), 'add', '.'], check=True)
    subprocess.run(['git', '-C', str(destination), 'commit', '-m', 'chore(harness): initialize project repository'], check=True)
    print(f"new-project: OK: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
