"""Outlier Count metric: number of sheep beyond threshold from centroid."""

import numpy as np

from core.base_metric import BaseMetric
from core.simulation_state import SimulationState


class OutlierCountMetric(BaseMetric):
    """Counts sheep exceeding distance f(N) = r_a * N^(2/3) from the GCM.

    This directly corresponds to the Strömbom switching condition,
    but is useful as a generic straggler measure for any algorithm.
    """

    @property
    def id(self) -> str:
        return "outlier_count"

    @property
    def name(self) -> str:
        return "Outlier Count"

    @property
    def description(self) -> str:
        return "Number of sheep beyond f(N) = r_a × N^(2/3) from the flock centroid."

    def compute(self, state: SimulationState) -> float:
        if state.n_sheep == 0:
            return 0.0
        r_a = state.metadata.get("r_a", 2.0)
        threshold = r_a * (state.n_sheep ** (2.0 / 3.0))
        distances = state.distances_to_centroid()
        return float(np.sum(distances > threshold))
