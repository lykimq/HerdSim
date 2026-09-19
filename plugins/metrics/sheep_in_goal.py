"""Sheep in Goal metric: count of sheep inside the goal zone."""

import numpy as np

from core.base_metric import BaseMetric
from core.simulation_state import SimulationState


class SheepInGoalMetric(BaseMetric):
    @property
    def id(self) -> str:
        return "sheep_in_goal"

    @property
    def name(self) -> str:
        return "Sheep in Goal"

    @property
    def description(self) -> str:
        return (
            "Number of sheep whose center is inside the goal circle "
            "(same rule as success; not outlier_count)."
        )

    @property
    def unit(self) -> str:
        return "sheep"

    def compute(self, state: SimulationState) -> float:
        goal = state.world.goal
        if goal is None or state.n_sheep == 0:
            return 0.0
        return float(np.sum(goal.contains(state.sheep_positions)))
