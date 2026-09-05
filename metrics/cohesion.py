"""Flock Cohesion metric: mean distance of sheep to flock centroid (GCM radius)."""

from core.base_metric import BaseMetric
from core.simulation_state import SimulationState


class CohesionMetric(BaseMetric):
    @property
    def id(self) -> str:
        return "cohesion"

    @property
    def name(self) -> str:
        return "Flock Cohesion"

    @property
    def description(self) -> str:
        return "Mean Euclidean distance of all sheep to the flock centroid (GCM)."

    def compute(self, state: SimulationState) -> float:
        if state.n_sheep == 0:
            return 0.0
        return float(state.distances_to_centroid().mean())
