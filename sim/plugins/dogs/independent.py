"""Independent paper shepherds (dog_controller=independent).

Each dog runs the single-dog rule of Strombom 2014 on its own: the decision (collect from behind
the farthest outlier, or drive from Pd) is taken on the whole flock, and the dog walks to that
target with the paper step, noise and stop rule. There is no team layer and no assignment, and
every dog sees every sheep, so all dogs choose the same target. With one dog this is the paper
shepherd, the same trial as collect_drive_multi with one dog.

It is the control that separates the two parts FAT lacks: FAT has neither the team layer nor
the collect/drive switch, this rule has the switch and no team layer.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from sim.core.simulation_state import SimulationState
from sim.methods.strombom.heuristics import decide, step_toward

from .helpers import move_dogs, noise_angles


def targets(state: SimulationState, config: dict[str, Any]) -> np.ndarray:
    """Target of every dog, shape (D, 2): the one paper target, repeated."""
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
