"""Drive the Fly operator scripts against a fake flyctl; nothing reaches Fly."""
import json
import os
import shutil
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[2]
DEPLOY = ROOT / "ops/fly/deploy.ps1"
POWER = ROOT / "ops/fly/power.ps1"
PWSH = shutil.which("pwsh")
FAKE = '''
import json, os, sys
args = sys.argv[1:]
with open(os.environ["FAKE_FLY_LOG"], "a", encoding="utf-8") as log:
    log.write(json.dumps(args) + "\\n")
fail = os.environ.get("FAKE_FLY_FAIL")
if fail and fail in " ".join(args):
    print("fake failure", file=sys.stderr)
    raise SystemExit(7)
if args[:2] == ["apps", "list"]:
    print(json.dumps([{"Name": "supportops-lab-db"}, {"Name": "someone-elses-app"}]))
elif args[:2] == ["machine", "list"]:
    state = os.environ.get("FAKE_FLY_MACHINE_STATE", "started")
    print(json.dumps([{"id": "m1", "state": state, "checks": [{"status": "passing"}],
                       "config": {"metadata": {"fly_process_group": "app"},
                                  "services": [{"autostart": True}]}}]))
elif args[:2] == ["volumes", "list"]:
    print(json.dumps([{"name": "pg_data", "size_gb": 10, "state": "created"}]))
'''


@unittest.skipUnless(PWSH, "pwsh is required")
class FlyOperatorScripts(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        base = Path(self.directory.name)
        script = base / "fake_fly.py"
        script.write_text(FAKE, encoding="utf-8")
        wrapper = base / "fly.cmd"
        wrapper.write_text(f'@"{sys.executable}" "{script}" %*\r\n', encoding="utf-8")
        self.log = base / "calls.jsonl"
        self.log.touch()
        self.env = {**os.environ, "FLY_BIN": str(wrapper), "FAKE_FLY_LOG": str(self.log),
                    "FLY_SECRETS_DIR": str(base / "private"), "FLY_EVIDENCE_DIR": str(base / "evidence")}

    def run_script(self, script, *arguments, **overrides):
        return subprocess.run([PWSH, "-NoProfile", "-File", str(script), *arguments], cwd=ROOT,
                              env={**self.env, **overrides}, capture_output=True, text=True, timeout=180)

    def calls(self):
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]

    def named_apps(self):
        found = set()
        for call in self.calls():
            if "--app" in call:
                found.add(call[call.index("--app") + 1])
            if call[:2] in (["apps", "create"], ["apps", "destroy"]):
                found.add(call[2])
        return found

    def assert_no_mutation(self):
        mutating = (("apps", "create"), ("apps", "destroy"), ("volumes", "create"), ("volumes", "destroy"),
                    ("machine", "start"), ("machine", "stop"), ("machine", "update"), ("machine", "destroy"),
                    ("scale", "count"), ("secrets", "import"))
        for call in self.calls():
            self.assertNotIn(tuple(call[:2]), mutating)
            self.assertNotEqual(call[:1], ["deploy"])

    def test_down_stops_every_stack_app_and_keeps_volumes(self):
        result = self.run_script(DEPLOY, "-Action", "Down")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(all(name.startswith("supportops-lab-") for name in self.named_apps()))
        self.assertIn("supportops-lab-db", self.named_apps())
        self.assertTrue(any(call[:2] == ["machine", "stop"] for call in self.calls()))
        self.assertFalse(any(call[:2] == ["apps", "destroy"] or call[:2] == ["volumes", "destroy"]
                             for call in self.calls()))
        self.assertIn("preserved", result.stdout)
        self.assertIn("pg_data", result.stdout)

    def test_stop_order_finishes_with_the_database(self):
        self.run_script(POWER, "-Action", "Stop")
        stopped = [call[call.index("--app") + 1] for call in self.calls() if call[:2] == ["machine", "stop"]]
        self.assertEqual(stopped[-1], "supportops-lab-db")

    def test_destroy_requires_the_exact_confirmation(self):
        result = self.run_script(DEPLOY, "-Action", "Down", "-DestroyData")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.calls(), [])
        result = self.run_script(DEPLOY, "-Action", "Down", "-DestroyData", "-ConfirmDestroy", "wrong")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.calls(), [])

    def test_confirmed_destroy_never_leaves_the_allowlist(self):
        result = self.run_script(DEPLOY, "-Action", "Down", "-DestroyData", "-ConfirmDestroy", "supportops-lab")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        destroyed = {call[2] for call in self.calls() if call[:2] == ["apps", "destroy"]}
        self.assertIn("supportops-lab-db", destroyed)
        self.assertNotIn("someone-elses-app", destroyed)
        self.assertTrue(all(name.startswith("supportops-lab-") for name in destroyed))

    def test_only_rejects_apps_outside_the_inventory(self):
        result = self.run_script(DEPLOY, "-Action", "Down", "-Only", "someone-elses-app")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.calls(), [])

    def test_dry_run_plans_up_and_down_without_mutation(self):
        for action in ("Up", "Down"):
            result = self.run_script(DEPLOY, "-Action", action, "-DryRun")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("DRY-RUN", result.stdout)
        self.assert_no_mutation()

    def test_up_deploys_infrastructure_before_products(self):
        result = self.run_script(DEPLOY, "-Action", "Up", "-SkipSecrets")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        deployed = [call[call.index("--app") + 1] for call in self.calls() if call[0] == "deploy"]
        self.assertLess(deployed.index("supportops-lab-db"), deployed.index("supportops-lab-p05"))
        self.assertLess(deployed.index("supportops-lab-idp"), deployed.index("supportops-lab-p05"))

    def test_console_is_in_the_inventory_and_stops_first(self):
        self.run_script(POWER, "-Action", "Stop")
        stopped = [call[call.index("--app") + 1] for call in self.calls() if call[:2] == ["machine", "stop"]]
        self.assertEqual(stopped[0], "supportops-lab-web")
        result = self.run_script(DEPLOY, "-Action", "Up", "-DryRun")
        self.assertIn("idp_clients.py", result.stdout)

    def test_failed_fly_call_returns_non_zero_and_stops(self):
        result = self.run_script(DEPLOY, "-Action", "Up", "-SkipSecrets", FAKE_FLY_FAIL="deploy")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(sum(call[0] == "deploy" for call in self.calls()), 1)
        result = self.run_script(POWER, "-Action", "Stop", FAKE_FLY_FAIL="machine stop")
        self.assertNotEqual(result.returncode, 0)

    def test_status_reports_machines_and_volumes_without_mutation(self):
        result = self.run_script(DEPLOY, "-Action", "Status")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("supportops-lab-db", result.stdout)
        self.assertIn("pg_data", result.stdout)
        self.assert_no_mutation()

    def test_status_treats_a_missing_app_as_not_deployed(self):
        result = self.run_script(POWER, "-Action", "Status", FAKE_FLY_FAIL="machine list")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("not deployed", result.stdout)

    def test_help_documents_each_action(self):
        result = subprocess.run([PWSH, "-NoProfile", "-Command", f"Get-Help '{DEPLOY}' -Full | Out-String -Width 200"],
                                capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0)
        for word in ("Up", "Down", "Status", "DestroyData", "DryRun"):
            self.assertIn(word, result.stdout)

    def test_secret_import_is_scoped_to_the_inventory(self):
        text = textwrap.dedent((ROOT / "ops/fly/prepare-secrets.ps1").read_text(encoding="utf-8"))
        self.assertIn("Assert-StackApp", text)


if __name__ == "__main__":
    unittest.main()
