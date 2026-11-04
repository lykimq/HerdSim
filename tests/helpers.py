"""Builders shared by the tests: hand-made states and real trial configs."""

from __future__ import annotations

import tempfile
from dataclasses import replace
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt

from services.cells import Cell, Group, cell_config
from services.protocol import Protocol, load_protocol
from sim.drive_task.world import GoalZone, World
from sim.state import SimulationState

PROTOCOLS = Path(__file__).parent / "protocols"
TEST_OUTPUT = Path(tempfile.gettempdir()) / "herdsim-tests"

# Loaded once from tests/protocols/unit.yaml; campaigns never write here.
BASE_PROTOCOL = load_protocol(str(PROTOCOLS / "unit.yaml"), output=TEST_OUTPUT)


def protocol_with(
    *,
    method: str = "strombom_multi",
    ticks: int = 300,
    settings: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
    base: Protocol = BASE_PROTOCOL,
) -> Protocol:
    """Copy of ``base`` with one method's time limit and parameters, and settings, replaced."""
    methods = tuple(
        replace(m, time_limit_ticks=ticks, params={**m.params, **(params or {})})
        if m.name == method
        else m
        for m in base.methods
    )
    return replace(base, settings={**base.settings, **(settings or {})}, methods=methods)


def config_for(
    method: str = "strombom_multi",
    *,
    n: int = 25,
    d: int = 2,
    layout: str = "compact",
    ticks: int = 300,
    flock_radius: float = 7.0,
    settings: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run config of one cell, built the way a campaign builds it (fixed R_f, no calibration).

    The field is sized for this single cell only, so finish times can be shorter than in a
    full protocol that also sizes for scattered layouts or larger teams.
    """
    protocol = replace(
        protocol_with(method=method, ticks=ticks, settings=settings, params=params),
        layouts=(layout,),
        shepherd_counts=(d,),
    )
    group = Group(method, layout, n)
    return cell_config(protocol, Cell(group, d), flock_radius)


STROMBOM_BASE = config_for("strombom_multi", n=10, d=1)
GOAL = np.array([200.0, 0.0])  # goal lies to the right; dogs approach from -x
ANGLE_TOL = 1e-12


def strombom_cfg(n_sheep: int, **overrides: Any) -> dict[str, Any]:
    """Run config for a flock of ``n_sheep``: the rule uses true N, not the sheep passed in."""
    return {**STROMBOM_BASE, "n_sheep": n_sheep, **overrides}


def tight_flock(n: int, center: tuple[float, float] = (0.0, 0.0)) -> np.ndarray:
    rng = np.random.default_rng(1)
    return np.asarray(center) + rng.normal(0.0, 0.5, size=(n, 2))


def flock_with_outlier(core: int = 9, outlier: tuple[float, float] = (30.0, 0.0)) -> np.ndarray:
    return np.vstack([tight_flock(core), [list(outlier)]])


def make_world(
    *,
    width: float = 150.0,
    height: float = 150.0,
    goal_center: tuple[float, float] = (15.0, 15.0),
    goal_radius: float = 15.0,
) -> World:
    """Small fixed arena for hand-placed agents. Not the campaign field sizing."""
    return World(width, height, GoalZone(np.array(goal_center, dtype=float), goal_radius))


def make_state(
    sheep: npt.ArrayLike,
    shepherds: npt.ArrayLike,
    *,
    world: World | None = None,
    velocities: npt.ArrayLike | None = None,
    metadata: dict[str, Any] | None = None,
) -> SimulationState:
    sheep_arr = np.asarray(sheep, dtype=float)
    dogs = np.asarray(shepherds, dtype=float).reshape(-1, 2)
    return SimulationState(
        tick=0,
        sheep_positions=sheep_arr,
        sheep_velocities=np.zeros_like(sheep_arr),
        shepherd_positions=dogs,
        shepherd_velocities=np.zeros_like(dogs)
        if velocities is None
        else np.asarray(velocities, dtype=float),
        world=world or make_world(),
        rng=np.random.default_rng(0),
        dog_rng=np.random.default_rng(1),
        metadata=metadata or {},
    )
