"""Flock Cohesion metric: mean distance of sheep to flock centroid (GCM radius)."""

from core.simulation_state import SimulationState

from .base import BaseMetric


class CohesionMetric(BaseMetric):
    """Mean Euclidean distance of all sheep to the flock centroid (GCM), in world units."""

    @property
    def id(self) -> str:
        return "cohesion"

    def compute(self, state: SimulationState) -> float:
        if state.n_sheep == 0:
            return 0.0
        return float(state.distances_to_centroid().mean())
