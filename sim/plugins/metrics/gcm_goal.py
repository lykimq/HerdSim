"""GCM-to-goal distance: Euclidean distance from flock centroid to goal centre."""

from __future__ import annotations

import numpy as np
from core.simulation_state import SimulationState
from core.world.goal import resolve_goal_center

from .base import BaseMetric


class GcmGoalMetric(BaseMetric):
    """Euclidean distance from the flock centroid (GCM) to the goal centre, in world units."""

    @property
    def id(self) -> str:
        return "gcm_goal"

    def compute(self, state: SimulationState) -> float:
        if state.n_sheep == 0:
            return 0.0
        goal = resolve_goal_center(state)
        return float(np.linalg.norm(state.sheep_centroid - goal))
