"""Success Rate metric: fraction of sheep inside the goal zone."""

import numpy as np

from core.base_metric import BaseMetric
from core.simulation_state import SimulationState


class SuccessRateMetric(BaseMetric):
    @property
    def id(self) -> str:
        return "success_rate"

    @property
    def name(self) -> str:
        return "Success Rate"

    @property
    def description(self) -> str:
        return (
            "Fraction of sheep currently inside the goal zone (0.0 to 1.0). "
            "See sheep_in_goal for the integer count."
        )
    @property
    def unit(self) -> str:
        return "fraction"

    def compute(self, state: SimulationState) -> float:
        goal = state.world.goal
        if goal is None or state.n_sheep == 0:
            return 0.0
        inside = goal.contains(state.sheep_positions)
        return float(np.mean(inside))
