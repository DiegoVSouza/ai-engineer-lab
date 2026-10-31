"""The audit must find real secrets, ignore public settings, read archives and never echo a value."""
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("public_readiness", ROOT / "scripts/harness/public_readiness.py")
audit = importlib.util.module_from_spec(spec)
sys.modules["public_readiness"] = audit
spec.loader.exec_module(audit)

SECRET = "zQ7" + "x9LmP2vK4rT8bN1cW6yH"


def repo_with(directory: Path, files: dict[str, bytes]) -> Path:
    subprocess.run(["git", "init", "-q", str(directory)], check=True)
    for name, data in files.items():
        (directory / name).write_bytes(data)
    subprocess.run(["git", "-C", str(directory), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(directory), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "x"], check=True)
    return directory


class Audit(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)

    def test_only_credential_names_count_as_known_values(self):
        env = self.base / ".env"
        env.write_text(f"GROQ_API_KEY={SECRET}\nGROQ_MODEL=openai/gpt-oss-20b-long-name\n", encoding="utf-8")
        self.assertEqual(audit.known_values([env]), [SECRET.encode()])

    def test_finds_a_known_value_in_a_deleted_file_and_inside_a_wheel(self):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as archive:
            archive.writestr("pkg/settings.py", f"value = '{SECRET}'")
        repo = repo_with(self.base / "r", {"a.txt": SECRET.encode(), "p-1.0-py3-none-any.whl": buffer.getvalue()})
        subprocess.run(["git", "-C", str(repo), "rm", "-q", "a.txt"], check=True)
        subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "rm"], check=True)
        result = audit.scan(repo, [SECRET.encode()])
        paths = {finding["path"] for finding in result["secret_findings"]}
        self.assertIn("a.txt", paths)
        self.assertIn("p-1.0-py3-none-any.whl!pkg/settings.py", paths)

    def test_report_never_contains_the_value(self):
        repo = repo_with(self.base / "r", {"a.txt": SECRET.encode()})
        self.assertNotIn(SECRET, json.dumps(audit.scan(repo, [SECRET.encode()])))

    def test_many_blobs_do_not_deadlock_the_pipe(self):
        repo = repo_with(self.base / "r", {f"f{n}.txt": bytes([n % 250 + 1]) * 200_000 for n in range(12)})
        self.assertEqual(audit.scan(repo, [])["blobs_scanned"], 12)


if __name__ == "__main__":
    unittest.main()
