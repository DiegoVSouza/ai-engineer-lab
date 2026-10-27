"""Validate the P00 handoff without importing product source or using a provider."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
status = ROOT / ".planning/llm-live-readiness/STATUS.md"
text = status.read_text(encoding="utf-8")
for target in re.findall(r"\]\(([^)]+)\)", text):
    if "://" not in target and not target.startswith("#"):
        assert (status.parent / target.split("#", 1)[0]).exists(), target
accounting = json.loads((ROOT / "projects/p00/artifacts/evidence/candidate-continuity-allocation/accounting.json").read_text())
provenance = json.loads((ROOT / "projects/p00/artifacts/evidence/candidate-continuity-allocation/provenance.json").read_text())
probe = json.loads((ROOT / "projects/p00/artifacts/evidence/private-review-ui/local-probe.json").read_text())
assert accounting["minimum_deficit"]["calls"] == 10
assert accounting["minimum_deficit"]["output_tokens"] == 370
assert accounting["confirmation_protected"]["calls"] == 60
assert provenance["reason"] == "immutable_campaign_provenance_mismatch"
assert provenance["provider_initializations"] == 0
assert provenance["immutable_files_and_ledgers_unchanged"] is True
assert probe["items"] == 16 and sum(probe["response_counts"].values()) == 15
assert probe["annotations_written"] == 0 and probe["provider_accessed"] is False
print(json.dumps({"status": "PASS", "links_resolve": True, "provider_accessed": False, "credentials_read": False, "human_review": "PENDING", "live_allocation": "INCOMPLETE", "project_sources_imported": False}, indent=2))
