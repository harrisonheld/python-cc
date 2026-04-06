coverage = {}

def initialize(clause_ids, clause_dict=None):
    if not clause_dict:
        clause_dict = {}
        
    for clause_id in clause_ids:
        if clause_id not in coverage:
            coverage[clause_id] = {
                "true": False,
                "false": False,
                "expr": clause_dict.get(clause_id, "<unknown>")
            }
        elif "expr" not in coverage[clause_id]:
            coverage[clause_id]["expr"] = clause_dict.get(clause_id, "<unknown>")


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