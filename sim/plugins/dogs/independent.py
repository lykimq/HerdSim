"""Independent single-dog controllers without team coordination.

Each dog evaluates the global Strömböm heuristic independently. Without inter-dog
coordination or task assignment, all dogs compute identical targets.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from sim.core.simulation_state import SimulationState
from sim.methods.strombom.heuristics import decide, step_toward

from .helpers import move_dogs, noise_angles


def targets(state: SimulationState, config: dict[str, Any]) -> np.ndarray:
    """Target position for each dog, shape (D, 2), broadcast from the global heuristic."""
    target = decide(state.sheep_positions, state.world.goal.center, config).target
    return np.tile(target, (state.n_shepherds, 1))


def step(state: SimulationState, config: dict[str, Any]) -> SimulationState:
    velocities = np.zeros((state.n_shepherds, 2))
    angles = noise_angles(state)
    if state.n_shepherds:
        aims = targets(state, config)
        for i in range(state.n_shepherds):
            velocities[i] = step_toward(
                state.shepherd_positions[i], aims[i], state.sheep_positions, config, angles[i]
            )
    return move_dogs(state, velocities, float(config["dt"]), config)
