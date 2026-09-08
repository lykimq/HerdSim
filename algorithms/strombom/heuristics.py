"""Strombom 2014 shepherd heuristics: Collect and Drive positioning.

Paper rules:
- Collect: Pc = r_a behind the furthest sheep relative to GCM
- Drive: Pd = r_a * sqrt(N) behind the flock relative to the goal
- If within 3*r_a of any sheep, shepherd speed is zero
- Shepherd heading includes the same angular noise as agents
"""

from __future__ import annotations

import numpy as np

from core.agents.goal import resolve_goal_center
from core.agents.sheep import compute_noise, unit_vector
from core.agents.shepherd import move_toward, position_behind_target
from core.simulation_state import SimulationState


def compute_threshold(n_sheep: int, r_a: float) -> float:
    """Switching threshold f(N) = r_a * N^(2/3)."""
    return r_a * (n_sheep ** (2.0 / 3.0))


def should_collect(state: SimulationState, config: dict) -> bool:
    """True if any sheep is farther than f(N) from the GCM (Collect mode)."""
    scale = float(config.get("collect_threshold_scale", 1.0))
    threshold = compute_threshold(state.n_sheep, config["r_a"]) * scale
    max_dist = np.max(state.distances_to_centroid())
    return bool(max_dist > threshold)


def collect_offset(config: dict) -> float:
    """Collect stand-off Pc: r_a behind the furthest agent (paper Table 1)."""
    if "collect_offset" in config:
        return float(config["collect_offset"])
    # Compatibility alias used by some older configs / UI overrides.
    if "collect_drive_offset" in config:
        return float(config["collect_drive_offset"])
    return float(config.get("r_a", 2.0))


def drive_offset(state: SimulationState, config: dict) -> float:
    """Drive stand-off Pd: r_a * sqrt(N) behind the flock (paper Table 1)."""
    if "drive_offset" in config:
        return float(config["drive_offset"])
    return float(config["r_a"]) * (state.n_sheep ** 0.5)


def collect_target(state: SimulationState, config: dict) -> np.ndarray:
    """Shepherd target for Collect: behind furthest sheep relative to GCM."""
    centroid = state.sheep_centroid
    furthest_idx = state.furthest_sheep_index()
    furthest_pos = state.sheep_positions[furthest_idx]
    return position_behind_target(furthest_pos, centroid, collect_offset(config))


def drive_target(state: SimulationState, config: dict) -> np.ndarray:
    """Shepherd target for Drive: behind GCM relative to goal."""
    centroid = state.sheep_centroid
    goal_center = resolve_goal_center(state, config)
    return position_behind_target(centroid, goal_center, drive_offset(state, config))


def shepherd_step_toward(
    state: SimulationState, config: dict, shepherd_idx: int, target: np.ndarray
) -> np.ndarray:
    """Velocity toward target with paper 3*r_a stop and angular noise."""
    speed = float(config.get("shepherd_speed", 1.5))
    shepherd_pos = state.shepherd_positions[shepherd_idx]
    min_sheep_dist = float(
        np.min(np.linalg.norm(state.sheep_positions - shepherd_pos, axis=1))
    )
    stop_multiple = float(config.get("shepherd_stop_multiple", 3.0))
    stop_radius = stop_multiple * float(config.get("r_a", 2.0))

    if min_sheep_dist < stop_radius:
        return np.zeros(2)

    base = move_toward(shepherd_pos, target, speed)
    noise = compute_noise(state.rng, float(config.get("noise_strength", 0.3)))
    direction = unit_vector(base + noise)
    step = min(speed, float(np.linalg.norm(target - shepherd_pos)))
    return direction * step


def compute_shepherd_velocity(
    state: SimulationState, config: dict, shepherd_idx: int = 0
) -> np.ndarray:
    """Collect/Drive velocity with 3*r_a stop and paper angular noise."""
    if should_collect(state, config):
        target = collect_target(state, config)
    else:
        target = drive_target(state, config)
    return shepherd_step_toward(state, config, shepherd_idx, target)


def strombom_assignment_line(
    state: SimulationState, config: dict, shepherd_idx: int = 0
) -> dict:
    """Overlay line from herder to Collect sheep or Drive stand-off point."""
    shepherd_pos = state.shepherd_positions[shepherd_idx]
    if should_collect(state, config):
        sheep_idx = int(state.furthest_sheep_index())
        return {
            "from": shepherd_pos.tolist(),
            "to": state.sheep_positions[sheep_idx].tolist(),
            "mode": "collect",
            "sheep_index": sheep_idx,
        }
    target = drive_target(state, config)
    return {
        "from": shepherd_pos.tolist(),
        "to": target.tolist(),
        "mode": "drive",
    }


def strombom_assignment_lines(
    state: SimulationState, config: dict
) -> list[dict]:
    """One assignment line per shepherd using Strombom Collect/Drive targets."""
    return [
        strombom_assignment_line(state, config, i)
        for i in range(state.n_shepherds)
    ]
