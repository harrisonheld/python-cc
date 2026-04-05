coverage = {}

def initialize_clauses(clause_ids, clause_dict=None):
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
    if clause_id not in coverage:
        coverage[clause_id] = {"true": False, "false": False, "expr": "<unknown>"}
    if value:
        coverage[clause_id]["true"] = True
    else:
        coverage[clause_id]["false"] = True
    return value