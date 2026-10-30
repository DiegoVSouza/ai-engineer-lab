"""Pin how scripts/stack.py forwards operator flags without starting anything."""
import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("lab_stack_cli", ROOT / "scripts/stack.py")
stack = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(stack)


class Completed:
    returncode = 3


class StackCli(unittest.TestCase):
    def invoke(self, *arguments):
        with patch("sys.argv", ["stack.py", *arguments]), patch.object(stack.subprocess, "run", return_value=Completed()) as run:
            code = stack.main()
        return code, run.call_args.args[0]

    def test_down_keeps_volumes_by_default(self):
        code, command = self.invoke("down")
        self.assertEqual(code, 3)
        self.assertEqual(command[-2:], ["down", "--remove-orphans"])

    def test_down_forwards_the_explicit_volume_flag(self):
        _, command = self.invoke("down", "--volumes")
        self.assertEqual(command[-3:], ["down", "--remove-orphans", "--volumes"])

    def test_logs_forward_flags(self):
        _, command = self.invoke("logs", "--follow", "api")
        self.assertEqual(command[-2:], ["--follow", "api"])

    def test_unknown_flag_on_up_is_still_rejected(self):
        with patch("sys.argv", ["stack.py", "up", "--volumes"]), self.assertRaises(SystemExit):
            stack.main()

    def test_fly_actions_invoke_the_operator_script(self):
        for action, expected in (("fly-up", "Up"), ("fly-down", "Down"), ("fly-status", "Status")):
            code, command = self.invoke(action, "-DryRun")
            self.assertEqual(code, 3)
            self.assertEqual(command[0], "pwsh")
            self.assertEqual(Path(command[command.index("-File") + 1]), ROOT / "ops/fly/deploy.ps1")
            self.assertEqual(command[command.index("-Action") + 1], expected)
            self.assertEqual(command[-1], "-DryRun")


if __name__ == "__main__":
    unittest.main()
