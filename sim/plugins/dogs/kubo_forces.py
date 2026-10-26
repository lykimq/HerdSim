"""Kubo force dogs (dog_controller=kubo_forces): eqs. 8 to 12 of Kubo et al. 2022.

Every dog chases the sheep farthest from the goal, pushed by the paper's four force terms
(sim/methods/kubo/forces.py), and its speed is clamped to ``dog_speed_max``.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from sim.core.simulation_state import SimulationState
from sim.core.vectors import farthest_from
from sim.methods.kubo.forces import clamp_speed, dog_velocity

from .helpers import move_dogs


def step(state: SimulationState, config: dict[str, Any]) -> SimulationState:
    dogs = state.shepherd_positions
    goal = state.world.goal.center
    target = farthest_from(state.sheep_positions, goal)
    velocities = np.zeros_like(dogs)
    for i in range(state.n_shepherds):
        velocities[i] = dog_velocity(dogs[i], target, goal, np.delete(dogs, i, axis=0), config)
    velocities = clamp_speed(velocities, float(config["dog_speed_max"]))
    return move_dogs(state, velocities, float(config["dt"]))
