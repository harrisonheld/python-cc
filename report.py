from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple


# This will be used to represent a predicate and record all the seen combinations of its clauses
@dataclass
class PredicateRecording:
    predicate_id: str
    expression_text: str
    clause_ids: List[str]
    observed_combinations: Set[Tuple[str, ...]] = field(default_factory=set)
    observed_executions: List[Tuple[Tuple[str, ...], bool]] = field(default_factory=list)

    def add_combination(self, clause_values: Dict[str, str], result: bool) -> None:
        combination = tuple(clause_values.get(clause_id, "-") for clause_id in self.clause_ids)
        self.observed_combinations.add(combination)
        self.observed_executions.append((combination, result))


# This represents a Predicate that is ACTIVELY being evaluated
# These will go in a stack, with the currently active one on the top
# Then when record_clause gets called, it can read from the top of the stack
# When it is done, we will make a Predicate class
@dataclass
class ActivePredicateExecution:
    predicate_id: str
    clause_values: Dict[str, str] = field(default_factory=dict)


class Report:
    def __init__(self) -> None:
        self.clause_text_by_id: Dict[str, str] = {}
        self.predicates_by_id: Dict[str, PredicateRecording] = {}
        self.active_predicates: List[ActivePredicateExecution] = []

    def initialize(
        self,
        clause_dict: Dict[str, str],
        predicate_clause_dict: Dict[str, List[str]],
        predicate_expr_dict: Dict[str, str]
    ) -> None:
        self.clause_text_by_id.clear()
        self.predicates_by_id.clear()
        self.active_predicates.clear()

        self.clause_text_by_id.update(clause_dict)

        for predicate_id, clause_ids in predicate_clause_dict.items():
            self.predicates_by_id[predicate_id] = PredicateRecording(
                predicate_id=predicate_id,
                expression_text=predicate_expr_dict[predicate_id],
                clause_ids=clause_ids
            )

    def record_clause(self, predicate_id: str, clause_id: str, value):
        assert clause_id in self.clause_text_by_id

        bool_value = bool(value)

        if self.active_predicates and self.active_predicates[-1].predicate_id == predicate_id:
            self.active_predicates[-1].clause_values[clause_id] = "T" if bool_value else "F"

        return value

    def record_predicate(self, predicate_id: str, evaluate_predicate):
        self.active_predicates.append(ActivePredicateExecution(predicate_id=predicate_id))
        result = None
        try:
            result = evaluate_predicate()
            return result
        finally:
            completed = self.active_predicates.pop()
            if result is not None:
                self.predicates_by_id[completed.predicate_id].add_combination(completed.clause_values, result)

    def get_predicates(self) -> List[PredicateRecording]:
        return [self.predicates_by_id[predicate_id] for predicate_id in sorted(self.predicates_by_id.keys())]

    def get_clause_text(self, clause_id: str) -> str:
        return self.clause_text_by_id[clause_id]