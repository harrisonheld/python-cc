import unittest

from coverage_types import evaluate_predicate, evaluate_predicates
from .test_helpers import make_predicate


class EvaluateTests(unittest.TestCase):
    def test_evaluate_helpers(self):
        predicate = make_predicate(
            "p6",
            [
                (("T", "T"), True),
                (("T", "F"), False),
                (("F", "T"), False),
                (("F", "F"), False),
            ],
        )

        assessment = evaluate_predicate(predicate)
        self.assertEqual("p6", assessment.predicate_id)
        self.assertTrue(assessment.cc)
        self.assertTrue(assessment.cacc)
        self.assertTrue(assessment.racc)

        assessments = evaluate_predicates([predicate])
        self.assertEqual(1, len(assessments))
        self.assertEqual("p6", assessments[0].predicate_id)


if __name__ == "__main__":
    unittest.main()
