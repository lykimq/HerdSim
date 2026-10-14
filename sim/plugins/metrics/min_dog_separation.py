"""Minimum Separation metric: closest pair of shepherd distance (stacking)."""

from __future__ import annotations

import numpy as np
from core.simulation_state import SimulationState
from scipy.spatial.distance import pdist

from .base import BaseMetric


class MinDogSeparationMetric(BaseMetric):
    """Minimum pairwise distance between shepherds."""

    @property
    def id(self) -> str:
        return "min_dog_separation"

    def compute(self, state: SimulationState) -> float:
        if state.n_shepherds < 2:
            return float("inf")
        return float(np.min(pdist(state.shepherd_positions)))
