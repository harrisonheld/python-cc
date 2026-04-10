import importlib.util
from pathlib import Path


_ROOT_COVERAGE_TYPES = Path(__file__).resolve().parents[2] / "coverage_types.py"
_SPEC = importlib.util.spec_from_file_location("_project_coverage_types", _ROOT_COVERAGE_TYPES)
_MODULE = importlib.util.module_from_spec(_SPEC)
assert _SPEC is not None and _SPEC.loader is not None
_SPEC.loader.exec_module(_MODULE)

CoverageAssessment = _MODULE.CoverageAssessment
evaluate_predicate = _MODULE.evaluate_predicate
evaluate_predicates = _MODULE.evaluate_predicates
satisfies_cc = _MODULE.satisfies_cc
satisfies_cacc = _MODULE.satisfies_cacc
satisfies_racc = _MODULE.satisfies_racc

__all__ = [
	"CoverageAssessment",
	"evaluate_predicate",
	"evaluate_predicates",
	"satisfies_cc",
	"satisfies_cacc",
	"satisfies_racc",
]
