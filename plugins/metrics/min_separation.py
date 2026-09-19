"""Minimum Separation metric: closest pair of sheep distance (safety)."""

import numpy as np
from scipy.spatial.distance import pdist

from core.base_metric import BaseMetric
from core.simulation_state import SimulationState


class MinSeparationMetric(BaseMetric):
    @property
    def id(self) -> str:
        return "min_separation"

    @property
    def name(self) -> str:
        return "Min Separation"

    @property
    def description(self) -> str:
        return (
            "Minimum pairwise distance between any two sheep (collision risk), "
            "in world units."
        )

    @property
    def unit(self) -> str:
        return "world units"

    def compute(self, state: SimulationState) -> float:
        if state.n_sheep < 2:
            return 0.0
        pairwise = pdist(state.sheep_positions)
        return float(np.min(pairwise))
