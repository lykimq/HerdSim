"""Built-in observation models for shepherd sensing factors."""

from __future__ import annotations

from typing import Any

import numpy as np

from core.agents.goal import resolve_goal_center
from core.observation import BaseObservationModel, ShepherdObservation
from core.simulation_state import SimulationState


def _goal_array(state: SimulationState, config: dict[str, Any]) -> np.ndarray | None:
    try:
        return resolve_goal_center(state, config)
    except Exception:
        return None


def _base_observation(
    state: SimulationState,
    shepherd_index: int,
    *,
    sheep_mask: np.ndarray,
    other_mask: np.ndarray,
    mode: str,
    bearings: np.ndarray | None = None,
    distances: np.ndarray | None = None,
    config: dict[str, Any],
) -> ShepherdObservation:
    sheep_idx = np.where(sheep_mask)[0]
    other_idx = np.where(other_mask)[0]
    return ShepherdObservation(
        shepherd_index=shepherd_index,
        self_position=state.shepherd_positions[shepherd_index].copy(),
        self_velocity=state.shepherd_velocities[shepherd_index].copy(),
        goal_center=_goal_array(state, config),
        sheep_positions=state.sheep_positions[sheep_idx].copy(),
        sheep_velocities=state.sheep_velocities[sheep_idx].copy(),
        sheep_indices=sheep_idx.astype(int),
        other_shepherd_positions=state.shepherd_positions[other_idx].copy(),
        other_shepherd_indices=other_idx.astype(int),
        bearings_to_sheep=None if bearings is None else bearings.copy(),
        distances_to_sheep=None if distances is None else distances.copy(),
        mode=mode,
    )


def _sensing_range(state: SimulationState, shepherd_index: int, config: dict[str, Any]) -> float:
    base = config.get("sensing_range")
    if base is None:
        base = config.get("r_s", config.get("radius", 65.0))
    scale = float(state.shepherd_sensing_scale[shepherd_index])
    return float(base) * scale


class GlobalObservation(BaseObservationModel):
    @property
    def id(self) -> str:
        return "global"

    def observe(
        self, state: SimulationState, shepherd_index: int, config: dict[str, Any]
    ) -> ShepherdObservation:
        sheep_mask = np.ones(state.n_sheep, dtype=bool)
        other_mask = np.ones(state.n_shepherds, dtype=bool)
        other_mask[shepherd_index] = False
        diffs = state.sheep_positions - state.shepherd_positions[shepherd_index]
        distances = np.linalg.norm(diffs, axis=1)
        bearings = np.arctan2(diffs[:, 1], diffs[:, 0])
        return _base_observation(
            state,
            shepherd_index,
            sheep_mask=sheep_mask,
            other_mask=other_mask,
            mode="global",
            bearings=bearings,
            distances=distances,
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
        radius = _sensing_range(state, shepherd_index, config)
        sheep_dist = np.linalg.norm(state.sheep_positions - origin, axis=1)
        sheep_mask = sheep_dist <= radius
        other_dist = np.linalg.norm(state.shepherd_positions - origin, axis=1)
        other_mask = (other_dist <= radius) & (np.arange(state.n_shepherds) != shepherd_index)
        diffs = state.sheep_positions[sheep_mask] - origin
        distances = np.linalg.norm(diffs, axis=1) if diffs.size else np.zeros(0)
        bearings = np.arctan2(diffs[:, 1], diffs[:, 0]) if diffs.size else np.zeros(0)
        return _base_observation(
            state,
            shepherd_index,
            sheep_mask=sheep_mask,
            other_mask=other_mask,
            mode="local_positions",
            bearings=bearings,
            distances=distances,
            config=config,
        )


def _bearing_proxy_distance(state: SimulationState, shepherd_index: int, config: dict[str, Any]) -> float:
    """Cartesian depth for direction-only sheep proxies.

    Controllers (Collect/Drive stop, FAT, etc.) treat sheep_positions as metric
    points. Placing proxies on the unit circle makes every sheep look closer than
    the Strombom stop radius (3*r_a), so dogs never move. Use the sensing range,
    and never place proxies inside the stop radius.
    """
    radius = _sensing_range(state, shepherd_index, config)
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
        # Drop metric distances; keep bearings. Controllers that need Cartesian
        # points get fixed-depth proxies along those bearings (not unit depth).
        if local.n_sheep_seen and local.bearings_to_sheep is not None:
            proxy = _bearing_proxy_distance(state, shepherd_index, config)
            local.sheep_positions = _positions_from_bearings(
                local.self_position, local.bearings_to_sheep, proxy
            )
            local.distances_to_sheep = None
        local.mode = "bearing_only"
        return local


class NoisyBearingObservation(BaseObservationModel):
    @property
    def id(self) -> str:
        return "noisy_bearing"

    def observe(
        self, state: SimulationState, shepherd_index: int, config: dict[str, Any]
    ) -> ShepherdObservation:
        obs = BearingOnlyObservation().observe(state, shepherd_index, config)
        sigma = float(config.get("noise_sigma", 0.0))
        if sigma > 0.0 and obs.n_sheep_seen and obs.bearings_to_sheep is not None:
            noise = state.rng.normal(0.0, sigma, size=obs.bearings_to_sheep.shape)
            bearings = obs.bearings_to_sheep + noise
            obs.bearings_to_sheep = bearings
            proxy = _bearing_proxy_distance(state, shepherd_index, config)
            obs.sheep_positions = _positions_from_bearings(
                obs.self_position, bearings, proxy
            )
        obs.mode = "noisy_bearing"
        return obs


class IntermittentObservation(BaseObservationModel):
    """Cache observations and refresh every observation_frequency ticks."""

    def __init__(self, inner: BaseObservationModel | None = None) -> None:
        self._inner = inner or GlobalObservation()
        self._cache: dict[int, ShepherdObservation] = {}
        self._last_tick: dict[int, int] = {}

    @property
    def id(self) -> str:
        return "intermittent"

    def observe(
        self, state: SimulationState, shepherd_index: int, config: dict[str, Any]
    ) -> ShepherdObservation:
        freq = max(1, int(config.get("observation_frequency", 1)))
        last = self._last_tick.get(shepherd_index, -(10**9))
        if shepherd_index not in self._cache or state.tick - last >= freq:
            obs = self._inner.observe(state, shepherd_index, config)
            obs.mode = "intermittent"
            self._cache[shepherd_index] = obs
            self._last_tick[shepherd_index] = state.tick
        return self._cache[shepherd_index]
