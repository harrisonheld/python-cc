import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MAIN_FILE = PROJECT_ROOT / "main.py"


class IntegrationTargetsTests(unittest.TestCase):
    def run_target(self, target_filename: str, extra_args=None) -> str:
        if extra_args is None:
            extra_args = []

        completed = subprocess.run(
            [sys.executable, str(MAIN_FILE), target_filename, *extra_args],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            0,
            completed.returncode,
            msg=f"main.py failed for {target_filename}:\nSTDOUT:\n{completed.stdout}\nSTDERR:\n{completed.stderr}",
        )
        self.assertIn("Coverage summary:", completed.stdout)
        self.assertIn("Predicate ID: predicate1", completed.stdout)
        self.assertIn("Observed executions (clause values -> predicate result):", completed.stdout)
        return completed.stdout

    def test_targets_1_through_6(self):
        expected = {
            "target1.py": {
                "expression": "Expression: a",
                "summary": "predicate1: CC=Yes, CACC=Yes, RACC=Yes",
                "execution": "1. [F] -> False",
            },
            "target2.py": {
                "expression": "Expression: a != 0 and b != 0",
                "summary": "predicate1: CC=No, CACC=Yes, RACC=No",
                "execution": "1. [F, -] -> False",
            },
            "target3.py": {
                "expression": "Expression: a and b and c",
                "summary": "predicate1: CC=No, CACC=No, RACC=No",
                "execution": "1. [F, -, -] -> False",
            },
            "target4.py": {
                "expression": "Expression: a or b",
                "summary": "predicate1: CC=No, CACC=Yes, RACC=No",
                "execution": "3. [T, -] -> True",
            },
            "target5.py": {
                "expression": "Expression: not x",
                "summary": "predicate1: CC=Yes, CACC=Yes, RACC=Yes",
                "execution": "2. [T] -> False",
            },
            "target6.py": {
                "expression": "Expression: a and b or c",
                "summary": "predicate1: CC=No, CACC=Yes, RACC=No",
                "execution": "4. [T, T, -] -> True",
            },
        }

        for target_filename, checks in expected.items():
            with self.subTest(target=target_filename):
                output = self.run_target(target_filename)
                self.assertIn(checks["expression"], output)
                self.assertIn(checks["summary"], output)
                self.assertIn(checks["execution"], output)

    def test_coverage_mode_flags_filter_summary_fields(self):
        flag_expectations = [
            ("--cc", "CC", "CC=No"),
            ("--cacc", "CACC", "CACC=Yes"),
            ("--racc", "RACC", "RACC=No"),
        ]

        for flag, expected_mode, expected_present in flag_expectations:
            with self.subTest(flag=flag):
                output = self.run_target("target2.py", [flag])
                self.assertIn(expected_present, output)

                summary_line = next(
                    line.strip() for line in output.splitlines() if line.strip().startswith("predicate1:")
                )
                summary_values = summary_line.split(": ", 1)[1]
                reported_modes = {part.split("=", 1)[0] for part in summary_values.split(", ")}
                self.assertEqual({expected_mode}, reported_modes)


if __name__ == "__main__":
    unittest.main()
