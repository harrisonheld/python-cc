import argparse
import ast
from coverage_types import evaluate_predicates
from instrumentor import ClauseInstrumentor
from report import Report


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Instrument predicates and report logic coverage.",
        epilog=(
            "Coverage modes:\n"
            "  --cc    Total Clause Coverage (CC): all full T/F clause combinations are observed.\n"
            "  --cacc  Correlated Active Clause Coverage (CACC): for each major clause,\n"
            "          toggling it can change predicate outcome (minor clauses may differ).\n"
            "  --racc  Restricted Active Clause Coverage (RACC): like CACC, but minor\n"
            "          clauses must remain the same between the witness pair.\n\n"
            "If no coverage mode flag is provided, all three (CC, CACC, RACC) are reported."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("target_file", help="Python file to instrument and execute")
    parser.add_argument(
        "--cc",
        action="store_true",
        help="Report only Total Clause Coverage (CC)",
    )
    parser.add_argument(
        "--cacc",
        action="store_true",
        help="Report only Correlated Active Clause Coverage (CACC)",
    )
    parser.add_argument(
        "--racc",
        action="store_true",
        help="Report only Restricted Active Clause Coverage (RACC)",
    )
    return parser.parse_args(argv)


def selected_modes(args) -> list[str]:
    modes = []
    if args.cc:
        modes.append("CC")
    if args.cacc:
        modes.append("CACC")
    if args.racc:
        modes.append("RACC")

    if not modes:
        return ["CC", "CACC", "RACC"]
    return modes


def main(argv=None):
    args = parse_args(argv)
    target_file = args.target_file
    modes = selected_modes(args)

    with open(target_file, "r") as f:
        source_code = f.read()

    # get Abstract Syntax Tree from source code as string
    tree = ast.parse(source_code)

    # Instrument the AST
    instrumentor = ClauseInstrumentor()
    report = Report()
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
        quoted_clause_texts = [f"'{text}'" for text in clause_texts]
        print(f"Clauses: {', '.join(quoted_clause_texts)}")
        print("Observed executions:")
        for combination, result in sorted(predicate.observed_executions):
            print(f"* {', '.join(combination)} => {'True' if result else 'False'}")
        print()

    print("Coverage summary:")
    for assessment in evaluate_predicates(report.get_predicates()):
        coverage_parts = []
        if "CC" in modes:
            coverage_parts.append(f"CC={'Yes' if assessment.cc else 'No'}")
        if "CACC" in modes:
            coverage_parts.append(f"CACC={'Yes' if assessment.cacc else 'No'}")
        if "RACC" in modes:
            coverage_parts.append(f"RACC={'Yes' if assessment.racc else 'No'}")

        print(
            f"{assessment.predicate_id}: "
            f"{', '.join(coverage_parts)}"
        )

if __name__ == "__main__":
    main()