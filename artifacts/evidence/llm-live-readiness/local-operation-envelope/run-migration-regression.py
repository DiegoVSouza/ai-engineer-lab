import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[4]
evidence = Path(__file__).resolve().parent
reports = []
for pattern in ("test_migrate_free_envelope_plus13.py", "test_migrate_local_operation.py"):
    command = [sys.executable, "-m", "unittest", "discover", "-s", "scripts/harness", "-p", pattern]
    result = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=180)
    reports.append({"command": " ".join(command), "cwd": str(root), "exit_code": result.returncode, "output": result.stdout + result.stderr})
    print(pattern, result.returncode, result.stdout + result.stderr)
(evidence / "migration-regression.json").write_text(json.dumps(reports, indent=2) + "\n")
sys.exit(any(report["exit_code"] for report in reports))
