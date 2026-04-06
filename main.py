import ast
import sys
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

    # Print observed predicate combinations
    report.print_predicate_combinations_report()

if __name__ == "__main__":
    main()