"""Extent metric: radius of gyration (RMS distance to flock centroid)."""

from __future__ import annotations

import numpy as np
from core.simulation_state import SimulationState

from .base import BaseMetric


class ExtentMetric(BaseMetric):
    """Root-mean-square distance of sheep to the flock centroid.

    Complements mean-spread (variance): extent is an RMS length scale of the
    flock around its GCM.
    """

    @property
    def id(self) -> str:
        return "extent"

    def compute(self, state: SimulationState) -> float:
        if state.n_sheep == 0:
            return 0.0
        distances = state.distances_to_centroid()
        return float(np.sqrt(np.mean(distances**2)))
