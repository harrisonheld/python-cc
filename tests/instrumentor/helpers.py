import ast
from instrumentor import ClauseInstrumentor
from report import Report, PredicateRecording
from typing import List

def run_source(source: str) -> List[PredicateRecording]:
    tree = ast.parse(source)
    instrumentor = ClauseInstrumentor()
    tree = instrumentor.visit(tree)
    ast.fix_missing_locations(tree)
    report = Report()
    report.initialize(
        instrumentor.clause_text_by_id,
        instrumentor.predicate_clause_ids,
        instrumentor.predicate_text_by_id,
    )
    exec(compile(tree, "<ast>", "exec"), {
        "record_clause": report.record_clause,
        "record_predicate": report.record_predicate,
    })
    return report.get_predicates()

def run_file(path: str) -> List[PredicateRecording]:
    with open(path) as f:
        return run_source(f.read())