import json
import re
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[4]
base = root / ".planning/llm-live-readiness"
plan = (base / "CONTINUATION-PLAN.md").read_text(encoding="utf-8")
prompt = (base / "NEXT-EXECUTOR-PROMPT.pt-BR.md").read_text(encoding="utf-8")
checks = {}
checks["finite_queue"] = all(f"| T{number} |" in plan for number in range(8))
checks["repair_protocol"] = all(value in plan for value in ("max_tries: 3", "initial attempt plus two", "failure ID", "same turn"))
checks["authority_and_reserves"] = all(value in plan for value in ("Paid authorization is USD 0", "84 holdout", "60 confirmation", "68 attempts", "incomplete", "unknown"))
checks["host_limit_explicit"] = "cannot guarantee" in plan and "não garante" in prompt
checks["prompt_actionable"] = all(value in prompt for value in ("CONTINUATION-PLAN.md", "LOOP:", "T0–T7", "mesmo turno", "max_tries: 3"))
references = [
    "projects/p00/.planning/phases/033-p01-envelope-reconciliation/VERIFY.md",
    "projects/p01/.planning/phases/019-accounted-local-live/VERIFY.md",
    "projects/p01/artifacts/evidence/accounted-local-live-019/reconciliation-verified.json",
    "projects/p02/.planning/phases/014-grounded-fixture-boundary/VERIFY.md",
    "projects/p03/.planning/phases/023-service-availability-recheck/VERIFY.md",
    "projects/p03/artifacts/evidence/service-availability-recheck-023/service-result.json",
    "projects/p04/.planning/phases/028-disable-unaccounted-live/VERIFY.md",
    "projects/p05/.planning/phases/026-disable-unaccounted-live/VERIFY.md",
]
checks["owner_references_exist"] = all((root / name).is_file() for name in references)
for name in ("EXECUTOR-HANDOFF.md", "WORK.md"):
    source = (base / name).read_text(encoding="utf-8")
    checks[name + "_links"] = all((base / target).is_file() for target in re.findall(r"\]\(([^)]+)\)", source) if target in {"CONTINUATION-PLAN.md", "NEXT-EXECUTOR-PROMPT.pt-BR.md"})
reconciliation = json.loads((root / references[2]).read_text())
checks["p01_reservation_preserved"] = reconciliation["totals"]["requests"] == "4" and reconciliation["events"][-1]["outcome"] == "incomplete"
service = json.loads((root / references[5]).read_text())
checks["p03_service_pass"] = service["gate_exit_code"] == 0 and service["cleanup_exit_code"] == 0 and service["prior_resources_preserved"] and not service["phase_containers_remaining"]
git = []
for owner in [root] + [root / "projects" / f"p{number:02d}" for number in range(6)]:
    result = subprocess.run(["git", "log", "-1", "--format=%H"], cwd=owner, capture_output=True, text=True, timeout=20)
    git.append({"owner": str(owner), "command": "git log -1 --format=%H", "exit_code": result.returncode, "output": result.stdout.strip() + result.stderr.strip()})
checks["git_owners_verified"] = all(item["exit_code"] == 0 for item in git)
report = {"command": "uv run --locked --project projects/p01 python artifacts/evidence/llm-live-readiness/executor-continuation-030/validate.py", "cwd": str(root), "exit_code": 0 if all(checks.values()) else 1, "checks": checks, "git": git, "references": references, "provider_accessed": False, "credentials_read": False, "product_files_modified": False}
(Path(__file__).resolve().parent / "validation-attempt2.json").write_text(json.dumps(report, indent=2) + "\n", newline="\n")
print(json.dumps(report, indent=2))
sys.exit(report["exit_code"])
