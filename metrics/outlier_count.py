"""Outlier Count metric: number of sheep beyond threshold from centroid."""

import numpy as np

from core.base_metric import BaseMetric
from core.simulation_state import SimulationState


class OutlierCountMetric(BaseMetric):
    """Counts sheep exceeding the effective collect threshold from the GCM.

    Base threshold is f(N) = r_a * N^(2/3) (Strombom 2014).  An optional
    'collect_threshold_scale' stored in state metadata (not in the paper;
    default 1.0) widens the tolerance for scenarios where oscillation is a
    concern.  The count always matches the algorithm's switching condition.
    """

    @property
    def id(self) -> str:
        return "outlier_count"

    @property
    def name(self) -> str:
        return "Outlier Count"

    @property
    def description(self) -> str:
        return (
            "Number of sheep beyond the effective collect threshold from the flock "
            "centroid (stragglers).  Base formula: f(N) = r_a * N^(2/3) (Strombom "
            "2014).  A scenario may supply collect_threshold_scale != 1.0 (not in "
            "the paper) to widen tolerance; the displayed count always matches the "
            "algorithm's switching condition.  This is not sheep outside the goal."
        )

    @property
    def unit(self) -> str:
        return "sheep"

    def compute(self, state: SimulationState) -> float:
        if state.n_sheep == 0:
            return 0.0
        r_a = state.metadata.get("r_a", 2.0)
        scale = float(state.metadata.get("collect_threshold_scale", 1.0))
        threshold = r_a * (state.n_sheep ** (2.0 / 3.0)) * scale
        distances = state.distances_to_centroid()
        return float(np.sum(distances > threshold))
