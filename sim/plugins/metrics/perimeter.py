"""Perimeter metric: convex-hull perimeter of the sheep flock."""

from __future__ import annotations

from core.simulation_state import SimulationState

from .base import BaseMetric
from .hull_geometry import hull_geometry


class PerimeterMetric(BaseMetric):
    """Length of the sheep convex hull boundary (world units).

    Complements mean-spread and extent: two flocks can share a similar radius
    while one has a longer edge (more elongated or irregular outline).
    """

    @property
    def id(self) -> str:
        return "perimeter"

    def compute(self, state: SimulationState) -> float:
        return hull_geometry(state.sheep_positions).perimeter
