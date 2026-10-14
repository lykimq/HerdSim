"""Outlier Count metric: number of sheep beyond threshold from centroid."""

import numpy as np
from core.simulation_state import SimulationState

from .base import BaseMetric


class OutlierCountMetric(BaseMetric):
    """Counts sheep exceeding the shared collect-style threshold from the GCM.

    Threshold is f(N) = r_a * N^(2/3) times optional collect_threshold_scale.
    Same formula for every algorithm so spread stays comparable. For Collect /
    Drive controllers this matches the mode switch; for others (e.g. Kubo) it
    is only a report score. Not sheep outside the goal.
    """

    @property
    def id(self) -> str:
        return "outlier_count"

    def compute(self, state: SimulationState) -> float:
        if state.n_sheep == 0:
            return 0.0
        r_a = state.metadata.get("r_a", 2.0)
        scale = float(state.metadata.get("collect_threshold_scale", 1.0))
        threshold = r_a * (state.n_sheep ** (2.0 / 3.0)) * scale
        distances = state.distances_to_centroid()
        return float(np.sum(distances > threshold))
