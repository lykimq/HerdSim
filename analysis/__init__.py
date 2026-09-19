"""Analysis package for validation studies and budget campaigns."""

from analysis.failure_taxonomy import FAILURE_LABELS, classify_failure

__all__ = [
    "classify_failure",
    "FAILURE_LABELS",
]
