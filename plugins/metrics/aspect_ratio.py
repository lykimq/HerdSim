"""Aspect-ratio metric: PCA elongation of sheep positions."""

from __future__ import annotations

from core.base_metric import BaseMetric
from core.simulation_state import SimulationState
from plugins.metrics.hull_geometry import aspect_ratio_of_points


class AspectRatioMetric(BaseMetric):
    """Largest / smallest PCA axis length of the sheep cloud.

    1.0 is isotropic; larger values mean a more elongated flock.
    """

    @property
    def id(self) -> str:
        return "aspect_ratio"

    @property
    def name(self) -> str:
        return "Flock Aspect Ratio"

    @property
    def description(self) -> str:
        return (
            "Ratio of the largest to smallest PCA axis of sheep positions. "
            "1.0 is round; higher values mean elongation."
        )

    @property
    def unit(self) -> str:
        return "ratio"

    def compute(self, state: SimulationState) -> float:
        return aspect_ratio_of_points(state.sheep_positions)
