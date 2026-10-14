"""Shared state builders for HerdSim tests."""

from __future__ import annotations

from typing import Any

import numpy as np
import numpy.typing as npt
from core.simulation_state import SimulationState
from core.world import GoalZone, World


def make_world(
    *,
    width: float = 150.0,
    height: float = 150.0,
    goal_center: tuple[float, float] = (15.0, 15.0),
    goal_radius: float = 15.0,
) -> World:
    return World(
        width=width,
        height=height,
        goal=GoalZone(center=np.array(goal_center, dtype=float), radius=goal_radius),
    )


def make_state(
    sheep: npt.ArrayLike,
    shepherds: npt.ArrayLike,
    *,
    world: World | None = None,
    seed: int = 0,
    tick: int = 0,
    metadata: dict[str, Any] | None = None,
) -> SimulationState:
    sheep_arr = np.asarray(sheep, dtype=float)
    shepherds_arr = np.asarray(shepherds, dtype=float)
    return SimulationState(
        tick=tick,
        sheep_positions=sheep_arr,
        sheep_velocities=np.zeros_like(sheep_arr),
        shepherd_positions=shepherds_arr,
        shepherd_velocities=np.zeros_like(shepherds_arr),
        world=world or make_world(),
        rng=np.random.default_rng(seed),
        metadata=metadata or {"r_a": 2.0},
    )
