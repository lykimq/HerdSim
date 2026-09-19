"""Helpers shared by dog controllers."""

from __future__ import annotations

from typing import Any

import numpy as np

from core.observation import ShepherdObservation
from core.simulation_state import SimulationState


def view_from_observation(
    state: SimulationState, obs: ShepherdObservation
) -> SimulationState:
    """Build a controller-local state view from one shepherd observation."""
    if obs.n_sheep_seen == 0:
        sheep_pos = np.zeros((0, 2))
        sheep_vel = np.zeros((0, 2))
    else:
        sheep_pos = obs.sheep_positions
        sheep_velocities = obs.sheep_velocities
        sheep_vel = sheep_velocities
    return state.copy_with(
        sheep_positions=sheep_pos,
        sheep_velocities=sheep_vel,
        shepherd_positions=state.shepherd_positions.copy(),
        shepherd_velocities=state.shepherd_velocities.copy(),
    )


def apply_dog_speeds(
    velocities: np.ndarray,
    state: SimulationState,
    config: dict[str, Any],
) -> np.ndarray:
    """Scale dog velocities by per-dog speed factors and active mask."""
    out = velocities.copy()
    scale = state.shepherd_speed_scale * float(config.get("speed_scale", 1.0))
    out = out * scale[:, np.newaxis]
    out[~state.shepherd_active] = 0.0
    return out


def empty_dog_velocities(state: SimulationState) -> np.ndarray:
    return np.zeros_like(state.shepherd_positions)
