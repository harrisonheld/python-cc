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
    report.initialize(instrumentor.clause_ids, instrumentor.clause_text_by_id)

    # Compile and execute instrumented code
    exec_globals = {"record": report.record}  # give the AST access to the "record" function
    code = compile(tree, filename="<ast>", mode="exec")
    exec(code, exec_globals)

    # Print the clause coverage report
    report.print_tcc_report()

if __name__ == "__main__":
    main()