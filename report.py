from typing import Dict

class Clause:
    def __init__(self, expr: str):
        self.expr = expr
        self.true: bool = False
        self.false: bool = False

    def record(self, value: bool) -> bool:
        if value:
            self.true = True
        else:
            self.false = True
        return value


coverage: Dict[str, Clause] = {}


def initialize(clause_dict: Dict[str, str]) -> None:
    for clause_id, expr_text in clause_dict.items():
        coverage[clause_id] = Clause(expr_text)


def record(clause_id: str, value: bool) -> bool:
    assert clause_id in coverage

    return coverage[clause_id].record(value)


def print_tcc_report() -> None:
    if not coverage:
        print("No clauses recorded.")
        return

    for clause_id, clause in coverage.items():
        print(clause_id)
        print(f"Expression: {clause.expr}")
        print(f"True seen : {'Yes' if clause.true else 'No'}")
        print(f"False seen: {'Yes' if clause.false else 'No'}")
        print()