"""GCM-to-goal distance: Euclidean distance from flock centroid to goal centre."""

from __future__ import annotations

import numpy as np

from core.agents.goal import resolve_goal_center
from core.base_metric import BaseMetric
from core.simulation_state import SimulationState


class GcmGoalMetric(BaseMetric):
    @property
    def id(self) -> str:
        return "gcm_goal"

    @property
    def name(self) -> str:
        return "GCM to Goal"

    @property
    def description(self) -> str:
        return (
            "Euclidean distance from the flock centroid (GCM) to the goal centre, "
            "in world units."
        )

    @property
    def unit(self) -> str:
        return "world units"

    def compute(self, state: SimulationState) -> float:
        if state.n_sheep == 0:
            return 0.0
        goal = resolve_goal_center(state)
        return float(np.linalg.norm(state.sheep_centroid - goal))
