import unittest

from report import Report


class ReportTests(unittest.TestCase):
	def test_initialize_creates_predicate_recordings(self):
		report = Report()
		report.initialize(
			clause_dict={"c1": "a", "c2": "b"},
			predicate_clause_dict={"p1": ["c1", "c2"]},
			predicate_expr_dict={"p1": "a and b"},
		)

		predicates = report.get_predicates()
		self.assertEqual(1, len(predicates))
		self.assertEqual("p1", predicates[0].predicate_id)
		self.assertEqual(["c1", "c2"], predicates[0].clause_ids)

	def test_record_predicate_records_combination_and_result(self):
		report = Report()
		report.initialize(
			clause_dict={"c1": "a", "c2": "b"},
			predicate_clause_dict={"p1": ["c1", "c2"]},
			predicate_expr_dict={"p1": "a and b"},
		)

		def evaluate_predicate():
			left = report.record_clause("p1", "c1", True)
			right = report.record_clause("p1", "c2", False)
			return left and right

		result = report.record_predicate("p1", evaluate_predicate)
		self.assertFalse(result)

		predicate = report.get_predicates()[0]
		self.assertIn(("T", "F"), predicate.observed_combinations)
		self.assertIn((("T", "F"), False), predicate.observed_executions)

	def test_record_predicate_keeps_short_circuited_clause_as_dash(self):
		report = Report()
		report.initialize(
			clause_dict={"c1": "a", "c2": "b"},
			predicate_clause_dict={"p1": ["c1", "c2"]},
			predicate_expr_dict={"p1": "a and b"},
		)

		def evaluate_predicate():
			left = report.record_clause("p1", "c1", False)
			if not left:
				return False

			right = report.record_clause("p1", "c2", True)
			return left and right

		report.record_predicate("p1", evaluate_predicate)

		predicate = report.get_predicates()[0]
		self.assertIn(("F", "-"), predicate.observed_combinations)
		self.assertIn((("F", "-"), False), predicate.observed_executions)

	def test_get_clause_text_returns_expression(self):
		report = Report()
		report.initialize(
			clause_dict={"c1": "a", "c2": "b"},
			predicate_clause_dict={"p1": ["c1", "c2"]},
			predicate_expr_dict={"p1": "a and b"},
		)

		self.assertEqual("a", report.get_clause_text("c1"))


if __name__ == "__main__":
	unittest.main()
