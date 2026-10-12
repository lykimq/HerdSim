"""Helpers shared by dog controllers."""

from __future__ import annotations

from typing import Any

import numpy as np
from core.observation import ShepherdObservation
from core.simulation_state import SimulationState


def move_toward(current_pos: np.ndarray, target_pos: np.ndarray, speed: float) -> np.ndarray:
    """Velocity from current toward target at most `speed` (zeros if at target)."""
    diff = target_pos - current_pos
    dist = np.linalg.norm(diff)
    if dist < 1e-10:
        return np.zeros(2)
    return (diff / dist) * min(speed, dist)


def position_behind_target(
    target_pos: np.ndarray, reference_pos: np.ndarray, offset_distance: float
) -> np.ndarray:
    """Point beyond `target_pos` on the ray from `reference_pos` through target.

    Collect: behind furthest sheep relative to centroid.
    Drive: behind centroid relative to goal.
    """
    direction = target_pos - reference_pos
    norm = np.linalg.norm(direction)
    if norm < 1e-10:
        return target_pos.copy()
    unit = direction / norm
    return target_pos + unit * offset_distance


def view_from_observation(state: SimulationState, obs: ShepherdObservation) -> SimulationState:
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


def iter_active_observations(
    state: SimulationState,
    observations: list[ShepherdObservation],
) -> list[tuple[int, ShepherdObservation]]:
    """Active shepherds that received an observation this tick."""
    by_idx = {o.shepherd_index: o for o in observations}
    out: list[tuple[int, ShepherdObservation]] = []
    for i in range(state.n_shepherds):
        if not state.shepherd_active[i] or i not in by_idx:
            continue
        out.append((i, by_idx[i]))
    return out


def finalize_dog_step(
    state: SimulationState,
    velocities: np.ndarray,
    config: dict[str, Any],
    *,
    metadata_updates: dict[str, Any] | None = None,
    dt: float = 1.0,
) -> SimulationState:
    """Apply speed scales and write shepherd positions/velocities/metadata."""
    scaled = apply_dog_speeds(velocities, state, config)
    metadata = dict(state.metadata)
    if metadata_updates:
        metadata.update(metadata_updates)
    if "r_a" not in metadata:
        metadata["r_a"] = float(config.get("r_a", 2.0))
    return state.copy_with(
        shepherd_positions=state.shepherd_positions + float(dt) * scaled,
        shepherd_velocities=scaled,
        metadata=metadata,
    )
