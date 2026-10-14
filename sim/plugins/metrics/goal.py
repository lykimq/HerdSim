"""Goal-progress metrics. Each takes a state and returns one float."""

from __future__ import annotations

import numpy as np
from core.simulation_state import SimulationState


def gcm_goal(state: SimulationState) -> float:
    """Distance from the flock centroid (GCM) to the goal centre."""
    if state.n_sheep == 0:
        return 0.0
    return float(np.linalg.norm(state.sheep_centroid - state.world.goal.center))


def time_to_goal(state: SimulationState) -> float:
    """Current tick when all sheep are in the goal disk, else -1.

    For collect_hold_gate the goal disk is the hold disk, not task success;
    trials.csv first_success_tick records success.
    """
    if np.all(state.world.goal.contains(state.sheep_positions)):
        return float(state.tick)
    return -1.0


def success_rate(state: SimulationState) -> float:
    """Fraction of sheep inside the goal disk."""
    if state.n_sheep == 0:
        return 0.0
    return float(np.mean(state.world.goal.contains(state.sheep_positions)))


def sheep_in_goal(state: SimulationState) -> float:
    """Number of sheep whose centre is inside the goal disk."""
    if state.n_sheep == 0:
        return 0.0
    return float(np.sum(state.world.goal.contains(state.sheep_positions)))
