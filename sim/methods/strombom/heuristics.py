"""Strombom 2014 shepherd heuristics used by the multi-dog and FAT controllers.

Paper rules:
- Collect: Pc = r_a behind the furthest sheep relative to GCM
- Drive: Pd = r_a * sqrt(N) behind the flock relative to the goal
- If within 3*r_a of any sheep, shepherd speed is zero
- Shepherd heading includes the same angular noise as agents
"""

from __future__ import annotations

from typing import Any

import numpy as np
from core.simulation_state import SimulationState
from plugins.sheep.helpers import compute_noise, unit_vector


def move_toward(current_pos: np.ndarray, target_pos: np.ndarray, speed: float) -> np.ndarray:
    """Velocity from current toward target at most `speed` (zeros if at target)."""
    diff = target_pos - current_pos
    dist = np.linalg.norm(diff)
    if dist < 1e-10:
        return np.zeros(2)
    return (diff / dist) * min(speed, dist)


def compute_threshold(n_sheep: int, r_a: float) -> float:
    """Switching threshold f(N) = r_a * N^(2/3)."""
    return r_a * (n_sheep ** (2.0 / 3.0))


def collect_offset(config: dict[str, Any]) -> float:
    """Collect stand-off Pc: r_a behind the furthest agent (paper Table 1)."""
    return float(config["r_a"])


def drive_offset(state: SimulationState, config: dict[str, Any]) -> float:
    """Drive stand-off Pd: r_a * sqrt(N) behind the flock (paper Table 1)."""
    return float(config["r_a"]) * (state.n_sheep**0.5)


def shepherd_step_toward(
    state: SimulationState,
    config: dict[str, Any],
    shepherd_idx: int,
    target: np.ndarray,
    *,
    proximity_sheep: np.ndarray | None = None,
) -> np.ndarray:
    """Velocity toward target with paper 3*r_a stop and angular noise.

    Planning may use an observation-limited view as `state`. The stop radius is a
    body-proximity rule: pass true world sheep as `proximity_sheep` when `state`
    holds observed or bearing-proxy positions.
    """
    speed = float(config["shepherd_speed"])
    shepherd_pos = state.shepherd_positions[shepherd_idx]
    sheep = state.sheep_positions if proximity_sheep is None else proximity_sheep
    stop_radius = float(config["shepherd_stop_multiple"]) * float(config["r_a"])
    if sheep.shape[0] > 0:
        min_sheep_dist = float(np.min(np.linalg.norm(sheep - shepherd_pos, axis=1)))
        if min_sheep_dist < stop_radius:
            return np.zeros(2)

    base = move_toward(shepherd_pos, target, speed)
    noise = compute_noise(state.rng, float(config["noise_strength"]))
    direction = unit_vector(base + noise)
    step = min(speed, float(np.linalg.norm(target - shepherd_pos)))
    return direction * step
