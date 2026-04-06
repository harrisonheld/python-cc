from dataclasses import dataclass
from itertools import product
from typing import Iterable, List

from report import PredicateRecording


@dataclass
class CoverageAssessment:
	predicate_id: str
	cc: bool
	cacc: bool
	racc: bool


def _all_full_combinations(clause_count: int) -> set[tuple[str, ...]]:
	return set(product(("T", "F"), repeat=clause_count))


def satisfies_cc(predicate: PredicateRecording) -> bool:
	expected = _all_full_combinations(len(predicate.clause_ids))
	seen = {combination for combination in predicate.observed_combinations if "-" not in combination}
	return expected.issubset(seen)


def _has_cacc_pair(predicate: PredicateRecording, major_clause_index: int) -> bool:
	for combination_a, result_a in predicate.observed_executions:
		value_a = combination_a[major_clause_index]
		if value_a not in {"T", "F"}:
			continue

		for combination_b, result_b in predicate.observed_executions:
			value_b = combination_b[major_clause_index]
			if value_b not in {"T", "F"}:
				continue

			if value_a == value_b:
				continue

			if result_a != result_b:
				return True

	return False


def _has_racc_pair(predicate: PredicateRecording, major_clause_index: int) -> bool:
	for combination_a, result_a in predicate.observed_executions:
		value_a = combination_a[major_clause_index]
		if value_a not in {"T", "F"}:
			continue

		for combination_b, result_b in predicate.observed_executions:
			value_b = combination_b[major_clause_index]
			if value_b not in {"T", "F"}:
				continue

			if value_a == value_b:
				continue

			if result_a == result_b:
				continue

			minors_match = True
			for i, (minor_a, minor_b) in enumerate(zip(combination_a, combination_b)):
				if i == major_clause_index:
					continue
				if minor_a != minor_b or minor_a == "-":
					minors_match = False
					break

			if minors_match:
				return True

	return False


def satisfies_cacc(predicate: PredicateRecording) -> bool:
	return all(_has_cacc_pair(predicate, i) for i in range(len(predicate.clause_ids)))


def satisfies_racc(predicate: PredicateRecording) -> bool:
	return all(_has_racc_pair(predicate, i) for i in range(len(predicate.clause_ids)))


def evaluate_predicate(predicate: PredicateRecording) -> CoverageAssessment:
	return CoverageAssessment(
		predicate_id=predicate.predicate_id,
		cc=satisfies_cc(predicate),
		cacc=satisfies_cacc(predicate),
		racc=satisfies_racc(predicate),
	)


def evaluate_predicates(predicates: Iterable[PredicateRecording]) -> List[CoverageAssessment]:
	return [evaluate_predicate(predicate) for predicate in predicates]

