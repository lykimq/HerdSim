"""Shepherd sensing: observation payload and concrete obs_mode implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import numpy as np

from core.simulation_state import SimulationState
from core.world.goal import resolve_goal_center


@dataclass
class ShepherdObservation:
    """What one shepherd can see on this tick."""

    shepherd_index: int
    self_position: np.ndarray
    goal_center: np.ndarray | None
    sheep_positions: np.ndarray
    sheep_velocities: np.ndarray
    sheep_indices: np.ndarray
    bearings_to_sheep: np.ndarray | None = None
    mode: str = "global"

    @property
    def n_sheep_seen(self) -> int:
        return int(self.sheep_positions.shape[0])


class BaseObservationModel(ABC):
    """Build per-shepherd observations from world state."""

    @property
    @abstractmethod
    def id(self) -> str:
        """Observation mode id (matches the obs_mode factor)."""

    @abstractmethod
    def observe(
        self,
        state: SimulationState,
        shepherd_index: int,
        config: dict[str, Any],
    ) -> ShepherdObservation:
        """Return the observation available to one shepherd."""

    def observe_all(
        self, state: SimulationState, config: dict[str, Any]
    ) -> list[ShepherdObservation]:
        return [self.observe(state, i, config) for i in range(state.n_shepherds)]


def _goal_array(state: SimulationState, config: dict[str, Any]) -> np.ndarray | None:
    try:
        return resolve_goal_center(state, config)
    except Exception:
        return None


def _build_observation(
    state: SimulationState,
    shepherd_index: int,
    *,
    sheep_mask: np.ndarray,
    mode: str,
    bearings: np.ndarray,
    config: dict[str, Any],
) -> ShepherdObservation:
    sheep_idx = np.where(sheep_mask)[0]
    return ShepherdObservation(
        shepherd_index=shepherd_index,
        self_position=state.shepherd_positions[shepherd_index].copy(),
        goal_center=_goal_array(state, config),
        sheep_positions=state.sheep_positions[sheep_idx].copy(),
        sheep_velocities=state.sheep_velocities[sheep_idx].copy(),
        sheep_indices=sheep_idx.astype(int),
        bearings_to_sheep=bearings,
        mode=mode,
    )


def sensing_range(config: dict[str, Any]) -> float:
    """Absolute dog sensing radius: ``sensing_range`` factor, else the method r_s / radius."""
    base = config.get("sensing_range")
    if base is None:
        base = config.get("r_s", config.get("radius", 65.0))
    return float(base)


class GlobalObservation(BaseObservationModel):
    @property
    def id(self) -> str:
        return "global"

    def observe(
        self, state: SimulationState, shepherd_index: int, config: dict[str, Any]
    ) -> ShepherdObservation:
        diffs = state.sheep_positions - state.shepherd_positions[shepherd_index]
        return _build_observation(
            state,
            shepherd_index,
            sheep_mask=np.ones(state.n_sheep, dtype=bool),
            mode="global",
            bearings=np.arctan2(diffs[:, 1], diffs[:, 0]),
            config=config,
        )


class LocalPositionsObservation(BaseObservationModel):
    @property
    def id(self) -> str:
        return "local_positions"

    def observe(
        self, state: SimulationState, shepherd_index: int, config: dict[str, Any]
    ) -> ShepherdObservation:
        origin = state.shepherd_positions[shepherd_index]
        radius = sensing_range(config)
        sheep_dist = np.linalg.norm(state.sheep_positions - origin, axis=1)
        sheep_mask = sheep_dist <= radius
        diffs = state.sheep_positions[sheep_mask] - origin
        bearings = np.arctan2(diffs[:, 1], diffs[:, 0]) if diffs.size else np.zeros(0)
        return _build_observation(
            state,
            shepherd_index,
            sheep_mask=sheep_mask,
            mode="local_positions",
            bearings=bearings,
            config=config,
        )


def _bearing_proxy_distance(config: dict[str, Any]) -> float:
    """Cartesian depth for direction-only sheep proxies.

    Controllers treat sheep_positions as metric points. Proxies on the unit
    circle look closer than the Strombom stop radius, so dogs never move.
    Use sensing range and stay outside the stop radius.
    """
    radius = sensing_range(config)
    stop_multiple = float(config.get("shepherd_stop_multiple", 3.0))
    r_a = float(config.get("r_a", 2.0))
    return max(float(radius), stop_multiple * r_a + r_a)


def _positions_from_bearings(
    origin: np.ndarray,
    bearings: np.ndarray,
    proxy_distance: float,
) -> np.ndarray:
    unit = np.stack([np.cos(bearings), np.sin(bearings)], axis=1)
    return origin + unit * float(proxy_distance)


class BearingOnlyObservation(BaseObservationModel):
    @property
    def id(self) -> str:
        return "bearing_only"

    def observe(
        self, state: SimulationState, shepherd_index: int, config: dict[str, Any]
    ) -> ShepherdObservation:
        local = LocalPositionsObservation().observe(state, shepherd_index, config)
        if local.n_sheep_seen and local.bearings_to_sheep is not None:
            proxy = _bearing_proxy_distance(config)
            local.sheep_positions = _positions_from_bearings(
                local.self_position, local.bearings_to_sheep, proxy
            )
        local.mode = "bearing_only"
        return local


__all__ = [
    "BaseObservationModel",
    "BearingOnlyObservation",
    "GlobalObservation",
    "LocalPositionsObservation",
    "ShepherdObservation",
    "sensing_range",
]
