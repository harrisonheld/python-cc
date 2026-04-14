import argparse
import ast
from coverage_types import evaluate_predicates
from instrumentor import ClauseInstrumentor
from report import Report


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Reports clause coverage of the given python file.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("target_file", help="Python file to instrument and execute")
    coverage_modes = parser.add_argument_group("coverage modes")
    coverage_modes.add_argument(
        "--all",
        action="store_true",
        help="(Default) Report all of CC, CACC, and RACC.",
    )
    coverage_modes.add_argument(
        "--cc",
        action="store_true",
        help="Report will include Total Clause Coverage (CC)",
    )
    coverage_modes.add_argument(
        "--cacc",
        action="store_true",
        help="Report will include Correlated Active Clause Coverage (CACC)",
    )
    coverage_modes.add_argument(
        "--racc",
        action="store_true",
        help="Report will include Restricted Active Clause Coverage (RACC)",
    )
    parser.add_argument(
        "--ast",
        action="store_true",
        help="Print the parsed AST for the target file and exit.",
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

    if not modes or args.all:
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

    if args.ast:
        print(ast.dump(tree, indent=2, include_attributes=False))
        return

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
    predicates = report.get_predicates()
    assessments = evaluate_predicates(predicates)

    for predicate, assessment in zip(predicates, assessments):
        print(f"Predicate ID: {predicate.predicate_id}")
        print(f"Expression: {predicate.expression_text}")
        clause_texts = [report.get_clause_text(clause_id) for clause_id in predicate.clause_ids]
        quoted_clause_texts = [f"'{text}'" for text in clause_texts]
        print(f"Clauses: [{', '.join(quoted_clause_texts)}]")
        print("Observed executions (clause values -> predicate result):")
        for index, (combination, result) in enumerate(sorted(predicate.observed_executions), start=1):
            print(f"  {index}. [{', '.join(combination)}] -> {'True' if result else 'False'}")
        print("Coverage summary:")
        coverage_parts = []
        if "CC" in modes:
            coverage_parts.append(f"CC={'Yes' if assessment.cc else 'No'}")
        if "CACC" in modes:
            coverage_parts.append(f"CACC={'Yes' if assessment.cacc else 'No'}")
        if "RACC" in modes:
            coverage_parts.append(f"RACC={'Yes' if assessment.racc else 'No'}")

        print(f"  {assessment.predicate_id}: {', '.join(coverage_parts)}")
        print()

if __name__ == "__main__":
    main()