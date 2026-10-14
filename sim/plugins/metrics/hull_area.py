"""Hull-area metric: convex-hull area of the sheep flock."""

from __future__ import annotations

from core.simulation_state import SimulationState

from .base import BaseMetric
from .hull_geometry import hull_geometry


class HullAreaMetric(BaseMetric):
    """Area enclosed by the sheep convex hull (world units squared)."""

    @property
    def id(self) -> str:
        return "hull_area"

    def compute(self, state: SimulationState) -> float:
        return hull_geometry(state.sheep_positions).area
