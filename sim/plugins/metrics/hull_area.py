"""Hull-area metric: convex-hull area of the sheep flock."""

from __future__ import annotations

from core.base_metric import BaseMetric
from core.simulation_state import SimulationState
from plugins.metrics.hull_geometry import hull_geometry


class HullAreaMetric(BaseMetric):
    """Area enclosed by the sheep convex hull (world units squared)."""

    @property
    def id(self) -> str:
        return "hull_area"

    @property
    def name(self) -> str:
        return "Flock Hull Area"

    @property
    def description(self) -> str:
        return (
            "Area of the sheep convex hull in world-units squared. "
            "Zero when fewer than three non-collinear sheep."
        )

    @property
    def unit(self) -> str:
        return "world units^2"

    def compute(self, state: SimulationState) -> float:
        return hull_geometry(state.sheep_positions).area
