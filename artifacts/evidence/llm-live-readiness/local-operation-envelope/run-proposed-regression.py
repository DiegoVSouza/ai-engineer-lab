import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[4]
evidence = Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix="proposed-policy-regression-") as directory:
    fixture = Path(directory)
    shutil.copytree(root / "scripts/harness", fixture / "scripts/harness")
    (fixture / "shared/policies").mkdir(parents=True)
    shutil.copyfile(evidence / "policy-after.json", fixture / "shared/policies/groq-free-campaign.json")
    command = [sys.executable, "-m", "unittest", "discover", "-s", str(fixture / "scripts/harness"), "-p", "test_live*.py"]
    result = subprocess.run(command, cwd=fixture, capture_output=True, text=True, timeout=180)
    report = {"command": "python -m unittest discover -s scripts/harness -p test_live*.py (isolated proposed-policy fixture)", "cwd": "temporary isolated fixture", "exit_code": result.returncode, "output": result.stdout + result.stderr}
    (evidence / "root-proposed-attempt3.json").write_text(json.dumps(report, indent=2) + "\n")
    print(report["output"])
    sys.exit(result.returncode)
