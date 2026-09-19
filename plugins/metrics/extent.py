"""Extent metric: radius of gyration (RMS distance to flock centroid)."""

from __future__ import annotations

import numpy as np

from core.base_metric import BaseMetric
from core.simulation_state import SimulationState


class ExtentMetric(BaseMetric):
    """Root-mean-square distance of sheep to the flock centroid.

    Complements mean-spread (variance): extent is an RMS length scale of the
    flock around its GCM.
    """

    @property
    def id(self) -> str:
        return "extent"

    @property
    def name(self) -> str:
        return "Flock Extent"

    @property
    def description(self) -> str:
        return (
            "Radius of gyration: RMS Euclidean distance of sheep to the flock "
            "centroid (GCM), in world units."
        )

    @property
    def unit(self) -> str:
        return "world units"

    def compute(self, state: SimulationState) -> float:
        if state.n_sheep == 0:
            return 0.0
        distances = state.distances_to_centroid()
        return float(np.sqrt(np.mean(distances ** 2)))
