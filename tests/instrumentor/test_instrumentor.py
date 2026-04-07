import unittest
from pathlib import Path
from .helpers import run_file

PROJECT_ROOT = Path(__file__).resolve().parents[2]

class InstrumentorTests(unittest.TestCase):

    def test_target1_single_clause(self):
        predicates = run_file(PROJECT_ROOT / "target1.py")
        self.assertEqual(1, len(predicates))
        self.assertEqual("a", predicates[0].expression_text)
        self.assertIn((("T",), True),  predicates[0].observed_executions)
        self.assertIn((("F",), False), predicates[0].observed_executions)

    def test_target2_and_short_circuit(self):
        predicates = run_file(PROJECT_ROOT / "target2.py")
        self.assertEqual(1, len(predicates))
        executions = predicates[0].observed_executions
        self.assertIn((("F", "-"), False), executions)
        self.assertIn((("T", "T"), True),  executions)
        self.assertIn((("T", "F"), False), executions)

    def test_target3_and_short_circuit(self):
        predicates = run_file(PROJECT_ROOT / "target3.py")
        self.assertEqual(1, len(predicates))
        executions = predicates[0].observed_executions
        self.assertIn((("T", "T", "T"), True),  executions)
        self.assertIn((("F", "-", "-"), False), executions)

    def test_target4_or_short_circuit(self):
        predicates = run_file(PROJECT_ROOT / "target4.py")
        self.assertEqual(1, len(predicates))
        executions = predicates[0].observed_executions
        self.assertIn((("T", "-"), True),  executions)
        self.assertIn((("F", "T"), True),  executions)
        self.assertIn((("F", "F"), False), executions)

    def test_target5_single_clause(self):
        predicates = run_file(PROJECT_ROOT / "target5.py")
        self.assertEqual(1, len(predicates))
        executions = predicates[0].observed_executions
        self.assertIn((("T",), False), executions)
        self.assertIn((("F",), True),  executions)

    def test_target6_and_or_short_circuit(self):
        predicates = run_file(PROJECT_ROOT / "target6.py")
        self.assertEqual(1, len(predicates))
        executions = predicates[0].observed_executions
        self.assertIn((("T", "T", "-"), True),  executions)
        self.assertIn((("T", "F", "F"), False), executions)
        self.assertIn((("F", "-", "T"), True),  executions)
        self.assertIn((("F", "-", "F"), False), executions)

    def test_target7_while_loop(self):
        predicates = run_file(PROJECT_ROOT / "target7.py")
        self.assertEqual(1, len(predicates))
        self.assertEqual("x", predicates[0].expression_text)
        executions = predicates[0].observed_executions
        self.assertIn((("T",), True),  executions)
        self.assertIn((("F",), False), executions)

    def test_target8_nested_if_two_predicates(self):
        predicates = run_file(PROJECT_ROOT / "target8.py")
        self.assertEqual(2, len(predicates))
        # predicate1 = outer `if a`, fires all 3 calls
        self.assertEqual("a", predicates[0].expression_text)
        self.assertIn((("T",), True),  predicates[0].observed_executions)
        self.assertIn((("F",), False), predicates[0].observed_executions)
        # predicate2 = inner `if b`, only fires when a is True (2 calls)
        self.assertEqual("b", predicates[1].expression_text)
        self.assertIn((("T",), True),  predicates[1].observed_executions)
        self.assertIn((("F",), False), predicates[1].observed_executions)

    def test_target9_and_not(self):
        predicates = run_file(PROJECT_ROOT / "target9.py")
        self.assertEqual(1, len(predicates))
        executions = predicates[0].observed_executions
        # clause values are the RAW values of a and b, before `not` is applied
        self.assertIn((("T", "T"), False), executions)  # a=T, b=T → a and not T = False
        self.assertIn((("T", "F"), True),  executions)  # a=T, b=F → a and not F = True
        self.assertIn((("F", "-"), False), executions)  # a=F → short-circuit