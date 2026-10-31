"""Drive ops/pages/deploy.ps1 against a fake wrangler; nothing reaches Cloudflare."""
import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[2]
DEPLOY = ROOT / "ops/pages/deploy.ps1"
PWSH = shutil.which("pwsh")
FAKE = '''
import json, os, sys
with open(os.environ["FAKE_WRANGLER_LOG"], "a", encoding="utf-8") as log:
    log.write(json.dumps(sys.argv[1:]) + "\\n")
'''


@unittest.skipUnless(PWSH, "pwsh is required")
class PagesDeploy(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        base = Path(self.directory.name)
        script = base / "fake_wrangler.py"
        script.write_text(FAKE, encoding="utf-8")
        wrapper = base / "wrangler.cmd"
        wrapper.write_text(f'@"{sys.executable}" "{script}" %*\r\n', encoding="utf-8")
        self.log = base / "calls.jsonl"
        self.log.touch()
        self.env = {**os.environ, "WRANGLER_BIN": str(wrapper), "FAKE_WRANGLER_LOG": str(self.log),
                    "PAGES_SKIP_BUILD": "1", "PAGES_EVIDENCE_DIR": str(base / "evidence")}

    def run_script(self, *arguments, **overrides):
        return subprocess.run([PWSH, "-NoProfile", "-File", str(DEPLOY), *arguments], cwd=ROOT,
                              env={**self.env, **overrides}, capture_output=True, text=True, timeout=120)

    def calls(self):
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]

    def test_default_is_a_dry_run_that_calls_nothing(self):
        result = self.run_script("-Site", "console")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("DRY-RUN", result.stdout)
        self.assertIn("supportops-console", result.stdout)
        self.assertEqual(self.calls(), [])

    def test_unknown_site_is_refused(self):
        result = self.run_script("-Site", "someone-elses-site")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.calls(), [])

    def test_project_name_cannot_be_overridden(self):
        result = self.run_script("-Site", "portfolio", PAGES_PROJECT_OVERRIDE="other")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.calls(), [])

    def test_apply_deploys_dist_to_the_inventory_project_on_main(self):
        result = self.run_script("-Site", "portfolio", "-Apply", "-AllowDirty")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        deploys = [c for c in self.calls() if c[:2] == ["pages", "deploy"]]
        self.assertEqual(len(deploys), 1)
        call = deploys[0]
        self.assertEqual(call[call.index("--project-name") + 1], "diego-portfolio-ai")
        self.assertEqual(call[call.index("--branch") + 1], "main")
        self.assertIn("dist", call)
        self.assertIn("DEPLOYED diego-portfolio-ai", result.stdout)
        self.assertTrue(list((Path(self.directory.name) / "evidence").glob("portfolio-*.json")))

    def test_create_project_is_explicit(self):
        self.run_script("-Site", "console", "-Apply", "-AllowDirty")
        self.assertFalse(any(c[:3] == ["pages", "project", "create"] for c in self.calls()))
        self.run_script("-Site", "console", "-Apply", "-AllowDirty", "-CreateProject")
        self.assertTrue(any(c[:3] == ["pages", "project", "create"] for c in self.calls()))


if __name__ == "__main__":
    unittest.main()
