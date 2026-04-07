import unittest

from coverage_types import satisfies_cacc
from .test_helpers import make_predicate


class CACCTests(unittest.TestCase):
    def test_satisfies_cacc_true_for_strong_witnesses(self):
        predicate = make_predicate(
            "p3",
            [
                (("T", "T"), True),
                (("T", "F"), False),
                (("F", "T"), False),
                (("F", "F"), False),
            ],
        )

        self.assertTrue(satisfies_cacc(predicate))

    def test_satisfies_cacc_true_when_minors_change(self):
        predicate = make_predicate(
            "p4",
            [
                (("T", "T"), True),
                (("F", "T"), False),
                (("F", "F"), False),
            ],
        )

        self.assertTrue(satisfies_cacc(predicate))

    def test_satisfies_cacc_false_when_predicate_result_never_changes(self):
        predicate = make_predicate(
            "p5",
            [
                (("T", "T"), False),
                (("T", "F"), False),
                (("F", "T"), False),
                (("F", "F"), False),
            ],
        )

        self.assertFalse(satisfies_cacc(predicate))


if __name__ == "__main__":
    unittest.main()
