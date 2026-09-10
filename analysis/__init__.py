"""Analysis package for herdability and validation studies."""

from analysis.behavioural import detect_events, matrix_distance, transition_matrix
from analysis.herdability import (
    attach_dimensionless,
    degradation_slope,
    dimensionless_features,
    required_shepherds,
)
from analysis.propagation import velocity_correlation_delay

__all__ = [
    "required_shepherds",
    "degradation_slope",
    "dimensionless_features",
    "attach_dimensionless",
    "detect_events",
    "transition_matrix",
    "matrix_distance",
    "velocity_correlation_delay",
]
