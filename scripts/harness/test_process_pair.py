"""Pin the supervisor that shares a Fly machine between a worker and an API."""
import shutil
import subprocess
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAIR = ROOT/'projects/p05/infra/logging/pair.py'
LONG = [sys.executable, '-c', 'import time; time.sleep(60)']


class ProcessPair(unittest.TestCase):
    def test_copies_are_identical(self):
        self.assertEqual(PAIR.read_bytes(), (ROOT/'projects/p04/infra/logging/pair.py').read_bytes())

    def test_a_crash_stops_the_partner_and_fails_the_machine(self):
        started = time.monotonic()
        code = subprocess.run([sys.executable, str(PAIR), sys.executable, '-c', 'raise SystemExit(3)', '::', *LONG],
                              timeout=40).returncode
        self.assertEqual(code, 3)
        self.assertLess(time.monotonic() - started, 30)

    def test_bad_usage_is_rejected(self):
        self.assertEqual(subprocess.run([sys.executable, str(PAIR), 'only-one'], capture_output=True).returncode, 2)

    def test_toml_runs_worker_and_api_in_one_group(self):
        for app, worker in (('p05', 'supportops_platform.service_runtime'), ('p04', 'supportops_async.worker.cli')):
            text = (ROOT/'fly'/app/'fly.toml').read_text(encoding='utf-8')
            self.assertIn('/app/logcfg/pair.py', text)
            self.assertIn(worker, text)
            self.assertNotIn('worker = "', text)
            self.assertNotIn('processes = ["worker"]', text)


if __name__ == '__main__':
    unittest.main()
