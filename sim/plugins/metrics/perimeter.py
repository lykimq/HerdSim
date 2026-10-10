"""Perimeter metric: convex-hull perimeter of the sheep flock."""

from __future__ import annotations

from core.base_metric import BaseMetric
from core.simulation_state import SimulationState
from plugins.metrics.hull_geometry import hull_geometry


class PerimeterMetric(BaseMetric):
    """Length of the sheep convex hull boundary (world units).

    Complements mean-spread and extent: two flocks can share a similar radius
    while one has a longer edge (more elongated or irregular outline).
    """

    @property
    def id(self) -> str:
        return "perimeter"

    @property
    def name(self) -> str:
        return "Flock Perimeter"

    @property
    def description(self) -> str:
        return (
            "Convex-hull perimeter of sheep positions in world units. "
            "Collinear or two-point flocks use twice the projected span."
        )

    @property
    def unit(self) -> str:
        return "world units"

    def compute(self, state: SimulationState) -> float:
        return hull_geometry(state.sheep_positions).perimeter
