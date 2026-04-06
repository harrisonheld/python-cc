from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple


# This will be used to represent a predicate and record all the seen combinations of its clauses
@dataclass
class Predicate:
    predicate_id: str
    expression_text: str
    clause_ids: List[str]
    observed_combinations: Set[Tuple[str, ...]] = field(default_factory=set)

    def add_combination(self, clause_values: Dict[str, str]) -> None:
        combination = tuple(clause_values.get(clause_id, "-") for clause_id in self.clause_ids)
        self.observed_combinations.add(combination)


# This represents a Predicate that is ACTIVELY being evaluated
# These will go in a stack, with the currently active one on the top
# Then when record_clause gets called, it can read from the top of the stack
# When it is done, we will make a Predicate class
@dataclass
class ActivePredicateExecution:
    predicate_id: str
    clause_values: Dict[str, str] = field(default_factory=dict)


clause_text_by_id: Dict[str, str] = {}
predicates_by_id: Dict[str, Predicate] = {}
active_predicates: List[ActivePredicateExecution] = []


def initialize(
    clause_dict: Dict[str, str],
    predicate_clause_dict: Dict[str, List[str]],
    predicate_expr_dict: Dict[str, str]
) -> None:
    clause_text_by_id.clear()
    predicates_by_id.clear()
    active_predicates.clear()

    clause_text_by_id.update(clause_dict)

    for predicate_id, clause_ids in predicate_clause_dict.items():
        predicates_by_id[predicate_id] = Predicate(
            predicate_id=predicate_id,
            expression_text=predicate_expr_dict[predicate_id],
            clause_ids=clause_ids
        )


def record_clause(predicate_id: str, clause_id: str, value):
    assert clause_id in clause_text_by_id

    bool_value = bool(value)

    if active_predicates and active_predicates[-1].predicate_id == predicate_id:
        active_predicates[-1].clause_values[clause_id] = "T" if bool_value else "F"

    return value


def record_predicate(predicate_id: str, evaluate_predicate):
    active_predicates.append(ActivePredicateExecution(predicate_id=predicate_id))
    try:
        return evaluate_predicate()
    finally:
        completed = active_predicates.pop()
        predicates_by_id[completed.predicate_id].add_combination(completed.clause_values)


def get_predicates() -> List[Predicate]:
    return [predicates_by_id[predicate_id] for predicate_id in sorted(predicates_by_id.keys())]


def get_clause_text(clause_id: str) -> str:
    return clause_text_by_id[clause_id]