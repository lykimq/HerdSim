"""Minimum Separation metric: closest pair of shepherd distance (stacking)."""

from __future__ import annotations

import numpy as np
from core.simulation_state import SimulationState
from scipy.spatial.distance import pdist

from .base import BaseMetric


class MinDogSeparationMetric(BaseMetric):
    """Minimum pairwise distance between active shepherds."""

    @property
    def id(self) -> str:
        return "min_dog_separation"

    @property
    def name(self) -> str:
        return "Min Dog Separation"

    @property
    def description(self) -> str:
        return (
            "Minimum pairwise distance between active shepherds in world units. "
            "Used by the stacking failure heuristic."
        )

    @property
    def unit(self) -> str:
        return "world units"

    def compute(self, state: SimulationState) -> float:
        active = np.asarray(state.shepherd_active, dtype=bool)
        if int(active.sum()) < 2:
            return float("inf")
        positions = state.shepherd_positions[active]
        return float(np.min(pdist(positions)))
