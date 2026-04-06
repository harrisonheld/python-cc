from typing import Any, Dict, List, Set, Tuple

clause_text_by_id: Dict[str, str] = {}
predicate_text_by_id: Dict[str, str] = {}
predicate_clause_ids: Dict[str, List[str]] = {}
predicate_combinations: Dict[str, Set[Tuple[str, ...]]] = {}
active_predicates: List[Dict[str, Any]] = []


def initialize(
    clause_dict: Dict[str, str],
    predicate_clause_dict: Dict[str, List[str]],
    predicate_expr_dict: Dict[str, str]
) -> None:
    clause_text_by_id.update(clause_dict)
    predicate_clause_ids.update(predicate_clause_dict)
    predicate_text_by_id.update(predicate_expr_dict)
    for predicate_id in predicate_clause_ids:
        predicate_combinations[predicate_id] = set()


def record_clause(predicate_id: str, clause_id: str, value):
    assert clause_id in clause_text_by_id

    bool_value = bool(value)

    if active_predicates and active_predicates[-1]["predicate_id"] == predicate_id:
        active_predicates[-1]["clause_values"][clause_id] = "T" if bool_value else "F"

    return value


def record_predicate(predicate_id: str, evaluate_predicate):
    # we will add the predicate to the top of the stack of predicates
    # that way, when record_clause gets called, it can pull from the top of the stack
    # and know what predicate it is a part of
    active_predicates.append(
        {
            "predicate_id": predicate_id,
            "clause_values": {}
        }
    )
    try:
        return evaluate_predicate()
    finally:
        completed = active_predicates.pop()
        ordered_clause_ids = predicate_clause_ids[predicate_id]
        observed_values = completed["clause_values"]
        combination = tuple(observed_values.get(clause_id, "-") for clause_id in ordered_clause_ids)
        predicate_combinations[predicate_id].add(combination)


def print_predicate_combinations_report() -> None:
    if not predicate_clause_ids:
        print("No predicates recorded.")
        return

    for predicate_id, clause_ids in predicate_clause_ids.items():
        print(predicate_id)
        print(f"Predicate: {predicate_text_by_id[predicate_id]}")
        print("Clauses:")
        for clause_id in clause_ids:
            print(f"  {clause_id}: {clause_text_by_id[clause_id]}")

        combinations = predicate_combinations[predicate_id]
        print("Observed combinations (T/F/-):")
        if not combinations:
            print("  None")
        else:
            for combination in sorted(combinations):
                print(f"  {', '.join(combination)}")
        print()