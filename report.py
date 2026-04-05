# report.py
from tracker import coverage

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