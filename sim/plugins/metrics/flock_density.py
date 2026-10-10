"""Flock density metric: sheep count per unit convex-hull area."""

from __future__ import annotations

from core.base_metric import BaseMetric
from core.simulation_state import SimulationState
from plugins.metrics.hull_geometry import flock_density, hull_geometry


class FlockDensityMetric(BaseMetric):
    """N / hull_area. Zero when the hull area is degenerate."""

    @property
    def id(self) -> str:
        return "flock_density"

    @property
    def name(self) -> str:
        return "Flock Density"

    @property
    def description(self) -> str:
        return (
            "Sheep count divided by convex-hull area (1 / world-units squared). "
            "Zero when the hull has no area."
        )

    @property
    def unit(self) -> str:
        return "1 / world units^2"

    def compute(self, state: SimulationState) -> float:
        area = hull_geometry(state.sheep_positions).area
        return flock_density(state.n_sheep, area)
