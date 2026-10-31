#!/usr/bin/env python3
"""Audit each repository before it goes public. Read-only; never prints or stores a secret value.

Scans every blob in full Git history for credential patterns and for the literal values of the
local secret files, then reviews tracked files. Findings carry location and pattern name only.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import subprocess
import sys
import tarfile
import threading
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPOS = {"lab": ROOT, **{f"p{n:02d}": ROOT / "projects" / f"p{n:02d}" for n in range(9)}}
MAX_BLOB = 20_000_000
PATTERNS = {
    "groq_key": rb"gsk_[A-Za-z0-9]{20,}",
    "openai_key": rb"sk-(?:proj-)?[A-Za-z0-9_-]{32,}",
    "openrouter_key": rb"sk-or-[A-Za-z0-9_-]{20,}",
    "anthropic_key": rb"sk-ant-[A-Za-z0-9_-]{20,}",
    "huggingface_token": rb"hf_[A-Za-z0-9]{30,}",
    "github_token": rb"gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}",
    "aws_key": rb"AKIA[0-9A-Z]{16}",
    "google_key": rb"AIza[0-9A-Za-z_-]{35}",
    "fly_token": rb"FlyV1 [A-Za-z0-9+/=_-]{20,}|fo1_[A-Za-z0-9_-]{20,}",
    "cloudflare_token": rb"(?i)cloudflare[_-]?api[_-]?token\s*[=:]\s*['\"]?[A-Za-z0-9_-]{30,}",
    "private_key": rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
    "real_jwt": rb"eyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{20,}",
    "assigned_password": rb"(?i)(?:password|passwd|secret|api[_-]?key)\s*[=:]\s*['\"][^'\"\s$<{]{10,}['\"]",
}
COMPILED = {name: re.compile(pattern) for name, pattern in PATTERNS.items()}
PLACEHOLDER = re.compile(rb"(?i)example|placeholder|changeme|dummy|fake|test|sample|redacted|xxxx|your[_-]")
PERSONAL = {
    "local_user_path": re.compile(rb"(?i)c:[\\/]+users[\\/]+dvsdi|/c/users/dvsdi"),
    "personal_email": re.compile(rb"dvsdiegovieira@gmail\.com"),
    "cloudflare_account": re.compile(rb"66bc26517997320ab58e682aed7f3118"),
}
CREDENTIAL_NAME = re.compile(r"(?i)key|token|secret|password|dsn|credential")
SUSPECT_NAME = re.compile(r"(?i)(^|/)(\.env(\.[^/]*)?|.*\.pem|.*\.key|.*\.p12|id_rsa|credentials.*|.*secrets?\.json)$")
BINARY_STATE = re.compile(r"(?i)\.(sqlite3?|db|sqlite-wal|sqlite-shm|parquet|pkl|bin)$")


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=True).stdout


def known_values(paths: list[Path]) -> list[bytes]:
    """Literal secret values, kept in memory only, to catch a key no pattern knows."""
    values: set[str] = set()
    for path in paths:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if path.suffix == ".json":
            try:
                document = json.loads(text)
            except ValueError:
                continue
            if isinstance(document, dict):
                values.update(value for key, value in document.items() if isinstance(value, str) and CREDENTIAL_NAME.search(key))
            continue
        for line in text.splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                name, value = line.split("=", 1)
                if CREDENTIAL_NAME.search(name):  # GROQ_MODEL holds a public model id, not a secret
                    values.add(value.strip().strip("'\""))
    return sorted((value.encode() for value in values if len(value) >= 16 and not value.isdigit()), key=len)


def blobs(repo: Path) -> dict[str, str]:
    """Every blob reachable from any ref, mapped to one path that held it."""
    found: dict[str, str] = {}
    for line in git(repo, "rev-list", "--all", "--objects").splitlines():
        sha, _, path = line.partition(" ")
        if path and sha not in found:
            found[sha] = path
    return found


def read_blobs(repo: Path, wanted: dict[str, str]):
    process = subprocess.Popen(["git", "-C", str(repo), "cat-file", "--batch"], stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE)
    request = "".join(f"{sha}\n" for sha in wanted).encode()

    def feed() -> None:
        # A separate writer: git blocks on a full stdout pipe, so writing all input first deadlocks.
        process.stdin.write(request)
        process.stdin.close()

    threading.Thread(target=feed, daemon=True).start()
    while True:
        header = process.stdout.readline()
        if not header:
            break
        parts = header.split()
        if len(parts) != 3:
            continue
        sha, kind, size = parts[0].decode(), parts[1], int(parts[2])
        data = process.stdout.read(size)
        process.stdout.read(1)
        if kind == b"blob":
            yield sha, data
    process.wait()


def members(path: str, data: bytes):
    """Files inside a tracked archive: a key baked into a wheel or tarball is still published."""
    try:
        if re.search(r"(?i)\.(whl|zip)$", path):
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                for name in archive.namelist():
                    if not name.endswith("/"):
                        yield f"{path}!{name}", archive.read(name)
        elif re.search(r"(?i)\.(tar|tgz|tar\.gz)$", path):
            with tarfile.open(fileobj=io.BytesIO(data)) as archive:
                for member in archive.getmembers():
                    if member.isfile():
                        yield f"{path}!{member.name}", archive.extractfile(member).read()
    except (zipfile.BadZipFile, tarfile.TarError, OSError, EOFError):
        yield f"{path}!UNREADABLE", b""


def scan(repo: Path, secrets: list[bytes]) -> dict:
    wanted = blobs(repo)
    secret_hits: list[dict] = []
    personal: dict[str, set[str]] = {name: set() for name in PERSONAL}
    scanned = skipped = 0
    for sha, data in read_blobs(repo, wanted):
        path = wanted[sha]
        if len(data) > MAX_BLOB:
            skipped += 1
            continue
        scanned += 1
        for item_path, content in [(path, data), *members(path, data)]:
            for value in secrets:
                if value in content:
                    line = content[: content.index(value)].count(b"\n") + 1
                    secret_hits.append({"kind": "LOCAL_SECRET_VALUE", "path": item_path, "line": line, "blob": sha[:12]})
            for name, pattern in COMPILED.items():
                for match in pattern.finditer(content):
                    if PLACEHOLDER.search(match.group(0)):
                        continue
                    line = content[: match.start()].count(b"\n") + 1
                    secret_hits.append({"kind": name, "path": item_path, "line": line, "blob": sha[:12]})
            for name, pattern in PERSONAL.items():
                if pattern.search(content):
                    personal[name].add(item_path)
    message_hits = []
    log = subprocess.run(["git", "-C", str(repo), "log", "--all", "--format=%H%x00%B%x00"], capture_output=True).stdout
    for name, pattern in COMPILED.items():
        if name != "assigned_password" and pattern.search(log):
            message_hits.append(name)
    if any(value in log for value in secrets):
        message_hits.append("LOCAL_SECRET_VALUE")
    return {"blobs_scanned": scanned, "blobs_skipped_too_large": skipped, "secret_findings": secret_hits,
            "commit_message_findings": message_hits,
            "personal_data": {name: {"files": len(paths), "sample": sorted(paths)[:5]} for name, paths in personal.items()}}


def tracked(repo: Path) -> dict:
    files = git(repo, "ls-files").splitlines()
    large = []
    for file in files:
        path = repo / file
        if path.is_file() and path.stat().st_size > 1_000_000:
            large.append({"path": file, "mb": round(path.stat().st_size / 1_048_576, 1)})
    workflows = [f for f in files if f.startswith(".github/workflows/")]
    return {
        "tracked_files": len(files),
        "suspect_names": [f for f in files if SUSPECT_NAME.search(f) and not f.endswith(".example")],
        "state_files": [f for f in files if BINARY_STATE.search(f)][:20],
        "large_files": large[:20],
        "license": any(re.fullmatch(r"(?i)licen[cs]e(\.[a-z]+)?", f) for f in files),
        "readme": "README.md" in files,
        "ci_workflows": workflows,
        "remote": git(repo, "remote").strip() or None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "artifacts/evidence/public-readiness/report.json")
    parser.add_argument("--only", nargs="*", default=sorted(REPOS))
    parser.add_argument("--secret-file", type=Path, nargs="*", default=[ROOT / ".env"])
    args = parser.parse_args()
    secrets = known_values(args.secret_file)
    report = {"known_secret_values_checked": len(secrets), "repositories": {}}
    for name in args.only:
        repo = REPOS[name]
        report["repositories"][name] = {**scan(repo, secrets), **tracked(repo)}
        item = report["repositories"][name]
        print(f"{name}: blobs={item['blobs_scanned']} secret_findings={len(item['secret_findings'])} "
              f"messages={len(item['commit_message_findings'])} license={item['license']} ci={len(item['ci_workflows'])}", flush=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return 1 if any(r["secret_findings"] or r["commit_message_findings"] for r in report["repositories"].values()) else 0


if __name__ == "__main__":
    sys.exit(main())
