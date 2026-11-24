"""Capture root guard tests; all accounts and ledgers are test fixtures."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
out = Path(__file__).resolve().parent
command = [sys.executable, "scripts/harness/test_live_free_account.py"]
result = subprocess.run(command, cwd=root, text=True, encoding="utf-8", errors="replace", capture_output=True)
report = f"command={' '.join(command)}\nworking_directory=lab\nexit_code={result.returncode}\n{result.stdout}{result.stderr}"
(out / "guard-tests.txt").write_bytes(report.rstrip().encode("utf-8") + b"\n")
print("root guard tests exit", result.returncode, flush=True)
sys.exit(result.returncode)
