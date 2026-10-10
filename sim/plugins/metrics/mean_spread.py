"""Mean-spread metric: variance of sheep distances to the flock centroid."""

from __future__ import annotations

import numpy as np

from core.base_metric import BaseMetric
from core.simulation_state import SimulationState


class MeanSpreadMetric(BaseMetric):
    """Variance of Euclidean distances from sheep to the flock centroid (GCM).

    Matches the draft sheep-scaling mean-spread idea: lower values are tighter
    flocks; higher values mean sheep are more widely distributed around the GCM.
    """

    @property
    def id(self) -> str:
        return "mean_spread"

    @property
    def name(self) -> str:
        return "Mean Spread"

    @property
    def description(self) -> str:
        return (
            "Variance of sheep Euclidean distances to the flock centroid (GCM), "
            "in world-units squared. Lower is more compact."
        )

    @property
    def unit(self) -> str:
        return "world units^2"

    def compute(self, state: SimulationState) -> float:
        if state.n_sheep == 0:
            return 0.0
        distances = state.distances_to_centroid()
        if state.n_sheep == 1:
            return 0.0
        return float(np.var(distances))
