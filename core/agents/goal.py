"""Shared goal resolution for herding algorithms."""

from __future__ import annotations

from typing import Any

import numpy as np

from core.simulation_state import SimulationState

_DEFAULT_GOAL = [15.0, 15.0]


def resolve_goal_center(
    state: SimulationState, config: dict[str, Any] | None = None
) -> np.ndarray:
    """Return the active goal centre from world, else config, else default."""
    if state.world.goal is not None:
        return state.world.goal.center.astype(float)
    cfg = config or {}
    return np.array(cfg.get("goal_center", _DEFAULT_GOAL), dtype=float)
