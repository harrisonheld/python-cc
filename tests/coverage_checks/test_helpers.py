from report import PredicateRecording


def make_predicate(predicate_id: str, executions) -> PredicateRecording:
    predicate = PredicateRecording(
        predicate_id=predicate_id,
        expression_text="dummy",
        clause_ids=["c1", "c2"],
    )
    predicate.observed_executions = list(executions)
    predicate.observed_combinations = {combination for combination, _ in executions}
    return predicate
