"""Flock density metric: sheep count per unit convex-hull area."""

from __future__ import annotations

from core.simulation_state import SimulationState

from .base import BaseMetric
from .hull_geometry import flock_density, hull_geometry


class FlockDensityMetric(BaseMetric):
    """N / hull_area. Zero when the hull area is degenerate."""

    @property
    def id(self) -> str:
        return "flock_density"

    def compute(self, state: SimulationState) -> float:
        area = hull_geometry(state.sheep_positions).area
        return flock_density(state.n_sheep, area)
