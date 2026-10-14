"""Aspect-ratio metric: PCA elongation of sheep positions."""

from __future__ import annotations

from core.simulation_state import SimulationState

from .base import BaseMetric
from .hull_geometry import aspect_ratio_of_points


class AspectRatioMetric(BaseMetric):
    """Largest / smallest PCA axis length of the sheep cloud.

    1.0 is isotropic; larger values mean a more elongated flock.
    """

    @property
    def id(self) -> str:
        return "aspect_ratio"

    def compute(self, state: SimulationState) -> float:
        return aspect_ratio_of_points(state.sheep_positions)
