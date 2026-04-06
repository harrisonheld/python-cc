from typing import Dict

coverage: Dict[str, Dict[str, object]] = {}

def initialize(clause_dict: Dict[str, str]) -> None:
    for clause_id, expr_text in clause_dict.items():
        coverage[clause_id] = {
            "true": False,
            "false": False,
            "expr": expr_text
        }


def record(clause_id, value):
    assert(clause_id in coverage)

    if value:
        coverage[clause_id]["true"] = True
    else:
        coverage[clause_id]["false"] = True
    return value


def print_tcc_report():
    if not coverage:
        print("No clauses recorded.")
        return

    for clause, result in coverage.items():
        print(clause)
        print(f"Expression: {result.get('expr', '<unknown>')}")
        print(f"True seen : {'Yes' if result['true'] else 'No'}")
        print(f"False seen: {'Yes' if result['false'] else 'No'}")
        print()