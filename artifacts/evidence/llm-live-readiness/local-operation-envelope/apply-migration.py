import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[4]
command = [sys.executable, "scripts/harness/migrate_local_operation.py", "--apply"]
result = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=60)
report = {"command": " ".join(command), "cwd": str(root), "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
(Path(__file__).resolve().parent / "migration-apply.json").write_text(json.dumps(report, indent=2) + "\n", newline="\n")
print(json.dumps(report, indent=2))
sys.exit(result.returncode)
