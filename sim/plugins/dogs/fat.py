"""Farthest-agent targeting (dog_controller=fat).

Each dog pushes the sheep farthest from the goal: it aims r_a behind that sheep, seen from
the goal, and moves with the Strombom shepherd step (noise and stop rule). The dogs do not
coordinate, and every dog sees every sheep, so they all choose the same sheep and become
copies of each other once they meet (the ``dog_overlap`` metric shows it).

A HerdSim construction: it borrows the target choice of Kubo 2022's farthest-individual
rule but not its forces or speeds.
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
