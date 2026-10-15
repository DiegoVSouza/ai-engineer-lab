"""Verify local project isolation, hook behavior, ignore rules, and initial commit."""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import tempfile


def run(root: pathlib.Path, args: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", type=pathlib.Path, required=True)
    args = parser.parse_args()
    root = args.project_dir.resolve()
    records: list[tuple[str, int, str, str, bool]] = []

    def record(label: str, command: list[str], expected: bool = True) -> tuple[int, str, str]:
        code, out, err = run(root, command)
        records.append(("git " + " ".join(command), code, out, err, code == 0 if expected else code != 0))
        return code, out, err

    root_code, root_out, root_err = record("repository root", ["rev-parse", "--show-toplevel"])
    records[-1] = (records[-1][0], root_code, root_out, root_err, root_code == 0 and pathlib.Path(root_out).resolve() == root)
    branch_code, branch_out, branch_err = record("branch main", ["branch", "--show-current"])
    records[-1] = (records[-1][0], branch_code, branch_out, branch_err, branch_code == 0 and branch_out == "main")
    hooks_code, hooks_out, hooks_err = record("configured hooks path", ["config", "--local", "--get", "core.hooksPath"])
    records[-1] = (records[-1][0], hooks_code, hooks_out, hooks_err, hooks_code == 0 and hooks_out == ".githooks")
    record("configured author identity", ["var", "GIT_AUTHOR_IDENT"])
    record("initial commit exists", ["rev-parse", "--verify", "HEAD"])

    with tempfile.TemporaryDirectory(prefix="hook-check-", dir=root) as temp_dir:
        invalid = pathlib.Path(temp_dir) / "invalid.txt"
        valid = pathlib.Path(temp_dir) / "valid.txt"
        invalid.write_text("invalid commit message\n", encoding="utf-8")
        valid.write_text("test(git): verify commit message hook\n", encoding="utf-8")
        record("invalid commit message rejected", ["hook", "run", "commit-msg", "--", str(invalid)], expected=False)
        record("valid Conventional Commit accepted", ["hook", "run", "commit-msg", "--", str(valid)])

    for path in (".env", ".venv/bin/python", "__pycache__/module.pyc", ".pytest_cache/cache", "secret.pem", "private.key"):
        code, out, err = record(f"ignored {path}", ["check-ignore", "--no-index", path])
        records[-1] = (records[-1][0], code, out, err, code == 0)
    code, out, err = record(".env.example remains trackable", ["check-ignore", "--no-index", ".env.example"], expected=False)
    records[-1] = (records[-1][0], code, out, err, code != 0)

    evidence = root / "artifacts" / "evidence" / "git-setup.md"
    evidence.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Git setup verification", "", f"Project: `{root}`", "", "Commands are executed from the project root. Expected rejection for the invalid hook message is recorded as PASS.", ""]
    for command, code, out, err, passed in records:
        if command == "git var GIT_AUTHOR_IDENT":
            out = re.sub(r"<[^>]+>", "<redacted>", out)
        lines.extend([f"## {'PASS' if passed else 'FAIL'} — `{command}`", f"- Exit code: `{code}`", f"- stdout: `{out or '(empty)'}`", f"- stderr: `{err or '(empty)'}`", ""])
    evidence.write_text("\n".join(lines), encoding="utf-8")
    failed = [entry for entry in records if not entry[4]]
    print(f"git-audit: {'FAIL' if failed else 'PASS'}; evidence={evidence}; checks={len(records)}; failed={len(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
