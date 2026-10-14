"""Farthest-agent targeting (FAT) under local observations."""

from __future__ import annotations

from typing import Any

import numpy as np
from core.observation import ShepherdObservation
from core.simulation_state import SimulationState
from methods.strombom.heuristics import shepherd_step_toward

from .helpers import (
    empty_dog_velocities,
    finalize_dog_step,
    position_behind_target,
    view_from_observation,
)


def step(
    state: SimulationState,
    observations: list[ShepherdObservation],
    config: dict[str, Any],
) -> SimulationState:
    """Drive the locally farthest observed sheep toward the goal."""
    velocities = empty_dog_velocities(state)
    goal = state.world.goal.center
    offset = float(config["r_a"])

    for obs in observations:
        if obs.n_sheep_seen == 0:
            continue
        i = obs.shepherd_index
        local = view_from_observation(state, obs)
        # Farthest from dog among observed sheep. Bearing-only proxies sit at
        # equal depth, so fall back to farthest from the goal among proxies.
        dists = np.linalg.norm(obs.sheep_positions - obs.self_position, axis=1)
        if float(np.ptp(dists)) < 1e-9:
            far_idx = int(np.argmax(np.linalg.norm(obs.sheep_positions - goal, axis=1)))
        else:
            far_idx = int(np.argmax(dists))
        sheep_pos = obs.sheep_positions[far_idx]
        target = position_behind_target(sheep_pos, goal, offset)
        velocities[i] = shepherd_step_toward(
            local, config, i, target, proximity_sheep=state.sheep_positions
        )

    return finalize_dog_step(state, velocities, metadata_updates={"herding_mode": "fat"})
