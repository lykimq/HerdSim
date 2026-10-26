"""Farthest-agent targeting controller (FAT).

Each dog targets a position distance r_a behind the sheep farthest from the goal,
stepping via Strömböm shepherd dynamics without inter-dog coordination.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from sim.core.simulation_state import SimulationState
from sim.core.vectors import behind, farthest_from
from sim.methods.strombom.heuristics import step_toward

from .helpers import move_dogs, noise_angles


def step(state: SimulationState, config: dict[str, Any]) -> SimulationState:
    velocities = np.zeros((state.n_shepherds, 2))
    angles = noise_angles(state)
    goal = state.world.goal.center
    target = behind(farthest_from(state.sheep_positions, goal), goal, float(config["r_a"]))
    for i in range(state.n_shepherds):
        velocities[i] = step_toward(
            state.shepherd_positions[i], target, state.sheep_positions, config, angles[i]
        )
    return move_dogs(state, velocities, float(config["dt"]), config)
