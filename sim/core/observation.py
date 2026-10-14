"""Shepherd sensing: what each dog can see, one function per obs_mode."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import numpy as np

from core.simulation_state import SimulationState


@dataclass
class ShepherdObservation:
    """What one shepherd can see on this tick."""

    shepherd_index: int
    self_position: np.ndarray
    goal_center: np.ndarray
    sheep_positions: np.ndarray
    sheep_velocities: np.ndarray
    sheep_indices: np.ndarray

    @property
    def n_sheep_seen(self) -> int:
        return int(self.sheep_positions.shape[0])


def _build_observation(
    state: SimulationState, shepherd_index: int, sheep_mask: np.ndarray
) -> ShepherdObservation:
    sheep_idx = np.where(sheep_mask)[0]
    return ShepherdObservation(
        shepherd_index=shepherd_index,
        self_position=state.shepherd_positions[shepherd_index].copy(),
        goal_center=state.world.goal.center.copy(),
        sheep_positions=state.sheep_positions[sheep_idx].copy(),
        sheep_velocities=state.sheep_velocities[sheep_idx].copy(),
        sheep_indices=sheep_idx.astype(int),
    )


def sensing_range(config: dict[str, Any]) -> float:
    """Absolute dog sensing radius: ``sensing_range`` factor, else the method r_s / radius."""
    base = config.get("sensing_range")
    if base is None:
        # The method's own sensing distance: Strombom r_s, Kubo radius.
        base = config["r_s"] if "r_s" in config else config["radius"]
    return float(base)


def observe_global(
    state: SimulationState, shepherd_index: int, _config: dict[str, Any]
) -> ShepherdObservation:
    """Every sheep, true positions."""
    return _build_observation(state, shepherd_index, np.ones(state.n_sheep, dtype=bool))


def observe_local_positions(
    state: SimulationState, shepherd_index: int, config: dict[str, Any]
) -> ShepherdObservation:
    """Sheep within the sensing range, true positions."""
    origin = state.shepherd_positions[shepherd_index]
    sheep_dist = np.linalg.norm(state.sheep_positions - origin, axis=1)
    return _build_observation(state, shepherd_index, sheep_dist <= sensing_range(config))


def _bearing_proxy_distance(config: dict[str, Any]) -> float:
    """Cartesian depth for direction-only sheep proxies.

    Controllers treat sheep_positions as metric points. Proxies on the unit
    circle look closer than the Strombom stop radius, so dogs never move.
    Use sensing range and stay outside the stop radius.
    """
    radius = sensing_range(config)
    if "shepherd_stop_multiple" not in config:
        # Kubo dogs have no stop radius to stay outside of.
        return radius
    r_a = float(config["r_a"])
    return max(radius, float(config["shepherd_stop_multiple"]) * r_a + r_a)


def observe_bearing_only(
    state: SimulationState, shepherd_index: int, config: dict[str, Any]
) -> ShepherdObservation:
    """Sheep within the sensing range, direction only: each one is placed at a
    fixed proxy depth along its bearing from the dog."""
    obs = observe_local_positions(state, shepherd_index, config)
    if obs.n_sheep_seen:
        diffs = obs.sheep_positions - obs.self_position
        bearings = np.arctan2(diffs[:, 1], diffs[:, 0])
        unit = np.stack([np.cos(bearings), np.sin(bearings)], axis=1)
        obs.sheep_positions = obs.self_position + unit * _bearing_proxy_distance(config)
    return obs


Observe = Callable[[SimulationState, int, dict[str, Any]], ShepherdObservation]

OBS_MODES: dict[str, Observe] = {
    "global": observe_global,
    "local_positions": observe_local_positions,
    "bearing_only": observe_bearing_only,
}
