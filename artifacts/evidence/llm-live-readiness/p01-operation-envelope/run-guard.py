import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[4]
command = [sys.executable, "-m", "unittest", "discover", "-s", "scripts/harness", "-p", "test_live_free_account.py"]
result = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=120)
report = {"command": " ".join(command), "cwd": str(root), "exit_code": result.returncode, "output": result.stdout + result.stderr}
(Path(__file__).resolve().parent / "guard-attempt2.json").write_text(json.dumps(report, indent=2) + "\n", newline="\n")
print(report["output"])
sys.exit(result.returncode)
