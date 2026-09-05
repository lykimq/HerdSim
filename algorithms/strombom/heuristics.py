"""Strömbom 2014 shepherd heuristics: Collect and Drive positioning.

These are the two core behaviours from the paper:
- Collect: move behind the furthest sheep to push it toward the flock centroid
- Drive: move behind the flock centroid to push the whole flock toward the goal
"""

from __future__ import annotations

import numpy as np

from core.agents.shepherd import move_toward, position_behind_target
from core.simulation_state import SimulationState


def compute_threshold(n_sheep: int, r_a: float) -> float:
    """Switching threshold f(N) = r_a * N^(2/3).

    If the furthest sheep exceeds this distance from the GCM,
    the shepherd switches to Collect mode.
    """
    return r_a * (n_sheep ** (2.0 / 3.0))


def should_collect(state: SimulationState, config: dict) -> bool:
    """Determine if the shepherd should be in Collect mode.

    Returns True if any sheep is further than f(N) from the flock centroid.
    """
    threshold = compute_threshold(state.n_sheep, config["r_a"])
    max_dist = np.max(state.distances_to_centroid())
    return max_dist > threshold


def _offset_distance(config: dict) -> float:
    """Paper uses r_a as the collect/drive stand-off distance."""
    if "collect_drive_offset" in config:
        return float(config["collect_drive_offset"])
    return float(config.get("r_a", 2.0))


def collect_target(state: SimulationState, config: dict) -> np.ndarray:
    """Compute the shepherd's target position for Collect behaviour.

    The shepherd aims for a point behind the furthest sheep,
    on the line from the centroid through that sheep.
    """
    centroid = state.sheep_centroid
    furthest_idx = state.furthest_sheep_index()
    furthest_pos = state.sheep_positions[furthest_idx]
    return position_behind_target(furthest_pos, centroid, _offset_distance(config))


def drive_target(state: SimulationState, config: dict) -> np.ndarray:
    """Compute the shepherd's target position for Drive behaviour.

    The shepherd aims for a point behind the flock centroid,
    on the line from the goal through the centroid.
    """
    centroid = state.sheep_centroid
    if state.world.goal is not None:
        goal_center = state.world.goal.center
    else:
        goal_center = np.array(config.get("goal_center", [15.0, 15.0]), dtype=float)
    return position_behind_target(centroid, goal_center, _offset_distance(config))


def compute_shepherd_velocity(
    state: SimulationState, config: dict, shepherd_idx: int = 0
) -> np.ndarray:
    """Compute the shepherd's velocity for this tick.

    Selects Collect or Drive based on flock cohesion,
    then moves toward the appropriate target position.
    """
    if should_collect(state, config):
        target = collect_target(state, config)
    else:
        target = drive_target(state, config)

    speed = config.get("shepherd_speed", 1.5)
    return move_toward(state.shepherd_positions[shepherd_idx], target, speed)
