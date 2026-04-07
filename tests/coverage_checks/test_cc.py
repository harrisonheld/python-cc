import unittest

from coverage_types import satisfies_cc
from .test_helpers import make_predicate


class CCTests(unittest.TestCase):
    def test_satisfies_cc_true_when_all_full_combinations_seen(self):
        predicate = make_predicate(
            "p1",
            [
                (("T", "T"), True),
                (("T", "F"), False),
                (("F", "T"), False),
                (("F", "F"), False),
            ],
        )

        self.assertTrue(satisfies_cc(predicate))

    def test_satisfies_cc_false_with_short_circuit_only(self):
        predicate = make_predicate(
            "p2",
            [
                (("T", "-"), True),
                (("F", "-"), False),
            ],
        )

        self.assertFalse(satisfies_cc(predicate))


if __name__ == "__main__":
    unittest.main()
