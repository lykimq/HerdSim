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
from sim.core.simulation_state import SimulationState
from sim.core.world.arena import GoalZone, World

UNIT_YAML = (
    Path(__file__).parent / "protocols" / "unit.yaml"
)  # canonical setup and every method
BASE_PROTOCOL = load_protocol(str(UNIT_YAML), output=Path(tempfile.gettempdir()) / "herdsim-tests")


def protocol_with(
    *,
    method: str = "strombom_multi",
    ticks: int = 300,
    settings: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
) -> Protocol:
    """The unit protocol with one method's time limit and parameters, and settings, replaced."""
    methods = tuple(
        replace(m, time_limit_ticks=ticks, params={**m.params, **(params or {})})
        if m.name == method
        else m
        for m in BASE_PROTOCOL.methods
    )
    return replace(
        BASE_PROTOCOL, settings={**BASE_PROTOCOL.settings, **(settings or {})}, methods=methods
    )


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
    factors: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run config of one cell, built the way a campaign builds it (fixed R_f, no calibration).

    The field is sized for this single cell (layouts=(layout,), shepherd_counts=(d,)), not for a
    whole protocol, so finish times measured with it are shorter than a campaign's for protocols
    with scattered layouts or many dogs.
    """
    protocol = replace(
        protocol_with(method=method, ticks=ticks, settings=settings, params=params),
        layouts=(layout,),
        shepherd_counts=(d,),
    )
    group = Group(method, layout, tuple(sorted((factors or {}).items())), n)
    return cell_config(protocol, Cell(group, d), flock_radius)


def make_world(
    *,
    width: float = 150.0,
    height: float = 150.0,
    goal_center: tuple[float, float] = (15.0, 15.0),
    goal_radius: float = 15.0,
) -> World:
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
