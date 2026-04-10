import unittest

from coverage_types import satisfies_racc
from .test_helpers import make_predicate


class RACCTests(unittest.TestCase):
    def test_satisfies_racc_true_for_strong_witnesses(self):
        predicate = make_predicate(
            "p3",
            [
                (("T", "T"), True),
                (("T", "F"), False),
                (("F", "T"), False),
                (("F", "F"), False),
            ],
        )

        self.assertTrue(satisfies_racc(predicate))

    def test_satisfies_racc_false_when_minors_change(self):
        predicate = make_predicate(
            "p4",
            [
                (("T", "T"), True),
                (("F", "T"), False),
                (("F", "F"), False),
            ],
        )

        self.assertFalse(satisfies_racc(predicate))


if __name__ == "__main__":
    unittest.main()
