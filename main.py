import ast
import sys
from coverage_types import evaluate_predicates
from instrumentor import ClauseInstrumentor
import report

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 clause_cover.py target.py")
        sys.exit(1)

    target_file = sys.argv[1]

    with open(target_file, "r") as f:
        source_code = f.read()

    # get Abstract Syntax Tree from source code as string
    tree = ast.parse(source_code)

    # Instrument the AST
    instrumentor = ClauseInstrumentor()
    tree = instrumentor.visit(tree)
    ast.fix_missing_locations(tree)
    report.initialize(
        instrumentor.clause_text_by_id,
        instrumentor.predicate_clause_ids,
        instrumentor.predicate_text_by_id
    )

    # Compile and execute instrumented code
    # Setting exec_globals gives the AST access to these functions
    exec_globals = {
        "record_clause": report.record_clause,
        "record_predicate": report.record_predicate
    }
    code = compile(tree, filename="<ast>", mode="exec")
    exec(code, exec_globals)

    # print nicely formatted report
    for predicate in report.get_predicates():
        print(f"Predicate ID: {predicate.predicate_id}")
        print(f"Expression: {predicate.expression_text}")
        clause_texts = [report.get_clause_text(clause_id) for clause_id in predicate.clause_ids]
        print(f"Clauses: {', '.join(f"'{text}'" for text in clause_texts)}")
        print("Observed executions:")
        for combination, result in sorted(predicate.observed_executions):
            print(f"* {', '.join(combination)} => {'True' if result else 'False'}")
        print()

    print("Coverage summary:")
    for assessment in evaluate_predicates(report.get_predicates()):
        print(
            f"{assessment.predicate_id}: "
            f"CC={'Yes' if assessment.cc else 'No'}, "
            f"CACC={'Yes' if assessment.cacc else 'No'}, "
            f"RACC={'Yes' if assessment.racc else 'No'}"
        )

if __name__ == "__main__":
    main()