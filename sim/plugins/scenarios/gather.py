"""Gather task: bring targets scattered over a disc into a goal at its centre.

The task of Lama and di Bernardo 2024 (Fig. 1): sheep and dogs start uniform over a disc of
radius R (``gather_start_radius``) centred on the goal, the goal is a disc of radius
``gather_goal_fraction`` x R (the paper's r* = R / 5), and the dogs have to bring the share
``success_fraction`` of the sheep inside it (the paper's chi*). No calibration: R sizes the
task, and ``flock_radius`` holds R (sqrt(2) x the RMS radius of a uniform disc is R).

Success (``is_success``): the share is inside the goal and every dog is inside it too, the
paper's own stop ("the simulation is stopped ... when all the herders are inside Omega_G").
A trial in which the share is reached while the dogs are still outside runs on until they
are in, as the paper's does.

End (``is_over``): a failing trial ends before the time limit when every dog is inside the
goal and no dog senses a sheep outside it. The second clause is added to the paper's stop:
read literally, a one-herder trial whose herder starts inside the goal would end at the
first step. The success rule keeps the literal stop, because there the degenerate start
cannot occur. The paper also stops some failing runs early on an unstated stationarity
test; HerdSim runs them to the limit, which can only help the dogs. A trial that reaches
the limit with the share inside but a dog still outside is a failure here;
``final_in_goal_fraction`` keeps chi at the end for the paper's reading.

What a dog senses is its ``sensing_radius`` when the controller has one (the Lama
herders), else everything.

Failure labels: ``targets_lost``, sheep beyond every dog's sensing at the end (the paper's
condition (i)); ``outnumbered``, every sheep sensed but the share not reached at the time
limit (condition (ii)).
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

from sim.core.simulation_state import SimulationState
from sim.core.world.layouts import UNIFORM, place_uniform_disc
from sim.plugins.metrics.view import TickView

from .failures import NONE, TIMEOUT, Failure
from .goal import arrival_columns
from .team_settings import KEYS as TEAM_KEYS
from .team_settings import check as check_team
from .team_settings import setup as team_setup

LAYOUTS = (UNIFORM,)

REQUIRED_KEYS = (
    "world_width",
    "world_height",
    "flock_center",
    "goal_center",
    "goal_radius",
    "success_fraction",
    "flock_radius",
    "start_radius",
    "field_clearance",
    "hold_ticks",
    *TEAM_KEYS,
)

# Canonical settings only this task reads.
OWN_SETTINGS = ("gather_start_radius", "gather_goal_fraction")

TARGETS_LOST = "targets_lost"
OUTNUMBERED = "outnumbered"


def check(config: dict[str, Any]) -> None:
    if config["initial_layout"] not in LAYOUTS:
        raise ValueError(f"initial_layout {config['initial_layout']!r} not in {LAYOUTS}")
    if int(config["hold_ticks"]) < 0:
        raise ValueError("hold_ticks must not be negative")
    if not 0.0 < float(config["goal_radius"]) < float(config["start_radius"]):
        raise ValueError("the goal must be smaller than the start disc")
    if float(config["sensing_range"]) > 0.0:
        # The end rule and unseen_targets read the Lama herders' sensing_radius and treat
        # every other dog as all-seeing; a team with a local view needs its own reading first.
        raise ValueError("sensing_range is not read by the gather task's end rule; leave it 0")
    check_team(config)


def build_setup(
    settings: Mapping[str, Any],
    *,
    flock_radius: float,
    n_sheep: int,
    layouts: tuple[str, ...],
    max_dogs: int,
) -> dict[str, Any]:
    """Setup keys from the protocol settings: the start disc, the goal and a field that holds
    the disc with ``field_clearance`` around it.

    The task sizes itself from R and does not calibrate, so ``flock_radius`` and the other
    sizing arguments of the drive task are ignored. The field only places the start.
    """
    _ = (flock_radius, n_sheep, layouts, max_dogs)
    s = settings
    radius = float(s["gather_start_radius"])
    fraction = float(s["gather_goal_fraction"])
    if radius <= 0.0:
        raise ValueError("gather_start_radius must be positive")
    if not 0.0 < fraction < 1.0:
        raise ValueError("gather_goal_fraction must lie between 0 and 1")
    if not 0.0 < float(s["success_fraction"]) <= 1.0:
        raise ValueError("success_fraction must be in (0, 1]")
    clearance = float(s["field_clearance"])
    side = 2.0 * (radius + clearance)
    centre = [side / 2.0, side / 2.0]
    return {
        "world_width": side,
        "world_height": side,
        "flock_center": centre,
        "goal_center": centre,
        "goal_radius": fraction * radius,
        "success_fraction": float(s["success_fraction"]),
        "flock_radius": radius,
        "start_radius": radius,
        "lost_radius": float(s["lost_radius_multiple"]) * radius,
        "field_clearance": clearance,
        **team_setup(s),
    }


def drive_length(setup: Mapping[str, Any]) -> float:
    """The task length: from the edge of the start disc to the edge of the goal."""
    return float(setup["start_radius"]) - float(setup["goal_radius"])


def initial_positions(
    config: dict[str, Any], rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    """Sheep, then dogs, uniform over the start disc (the goal is not excluded, as in the
    paper). The sheep are drawn first, so their start does not depend on the dog count."""
    centre = np.asarray(config["flock_center"], dtype=float)
    radius = float(config["start_radius"])
    sheep = place_uniform_disc(centre, radius, int(config["n_sheep"]), rng)
    dogs = place_uniform_disc(centre, radius, int(config["n_shepherds"]), rng)
    return sheep, dogs


def sensing(config: Mapping[str, Any]) -> float:
    """How far a dog senses: the controller's ``sensing_radius`` if it has one, else everything."""
    return float(config.get("sensing_radius", math.inf))


def _dogs_home(state: SimulationState) -> bool:
    """Every dog inside the goal disc (the paper's stop: all herders inside Omega_G)."""
    goal = state.world.goal
    inside = np.linalg.norm(state.shepherd_positions - goal.center, axis=1) < goal.radius
    return bool(inside.all())


def _unseen(sheep: np.ndarray, dogs: np.ndarray, reach: float) -> np.ndarray:
    """Which sheep no dog senses, shape (N,)."""
    if dogs.shape[0] == 0:
        return np.ones(sheep.shape[0], dtype=bool)
    if math.isinf(reach):
        return np.zeros(sheep.shape[0], dtype=bool)
    return ~(cdist(sheep, dogs) <= reach).any(axis=1)


def _sensed_outside(state: SimulationState, reach: float) -> bool:
    """Some dog senses a sheep that is outside the goal."""
    outside = ~state.world.goal.contains(state.sheep_positions)
    if not outside.any():
        return False
    return not _unseen(state.sheep_positions[outside], state.shepherd_positions, reach).all()


def is_over(state: SimulationState, config: dict[str, Any]) -> bool:
    """The dogs are all inside the goal and none senses a sheep outside it (module docstring)."""
    return _dogs_home(state) and not _sensed_outside(state, sensing(config))


def is_success(state: SimulationState) -> bool:
    """The share ``success_fraction`` is inside the goal, held for ``hold_ticks``, and every dog
    is inside it (module docstring)."""
    goal = state.world.goal
    if not (goal.reached(state.sheep_positions) and _dogs_home(state)):
        state.metadata.pop("reached_since", None)
        return False
    since = state.metadata.setdefault("reached_since", state.tick)
    return state.tick - since >= goal.hold_ticks


def unseen_targets(view: TickView) -> float:
    """Number of sheep beyond every dog's sensing (the paper's condition (i))."""
    state = view.state
    unseen = _unseen(state.sheep_positions, state.shepherd_positions, sensing(view.config))
    return float(unseen.sum())


def dog_radius(view: TickView) -> float:
    """Mean distance of the dogs from the goal centre (the paper's <|H|>). NaN without dogs."""
    state = view.state
    if state.n_shepherds == 0:
        return float("nan")
    distance = np.linalg.norm(state.shepherd_positions - state.world.goal.center, axis=1)
    return float(distance.mean())


def row_columns(config: dict[str, Any], history: pd.DataFrame) -> dict[str, Any]:
    """The task's columns of a trial row: the geometry it ran in and where it ended."""
    final = history.iloc[-1]
    n = int(config["n_sheep"])
    return {
        **arrival_columns(config, history),
        "start_radius": float(config["start_radius"]),
        "goal_radius": float(config["goal_radius"]),
        "success_fraction": float(config["success_fraction"]),
        "drive_distance": drive_length(config),
        "world_width": float(config["world_width"]),
        "world_height": float(config["world_height"]),
        "final_gcm_goal": float(final["gcm_goal"]),
        "final_sheep_in_goal": float(final["sheep_in_goal"]),
        "final_in_goal_fraction": float(final["sheep_in_goal"]) / n,
        "final_unseen_targets": float(final["unseen_targets"]),
    }


def classify_failure(history: pd.DataFrame, *, success: bool, config: dict[str, Any]) -> Failure:
    """Lost targets when some sheep was out of every dog's sensing at the end (whether the
    trial ended early or at the limit); outnumbered when every sheep was sensed and the
    share was still not reached."""
    if success:
        return Failure(NONE, ())
    final = history.iloc[-1]
    matched: list[str] = []
    if float(final["unseen_targets"]) > 0.0:
        matched.append(TARGETS_LOST)
    elif int(final["tick"]) >= int(config["max_ticks"]):
        matched.append(OUTNUMBERED)
    return Failure(matched[0] if matched else TIMEOUT, tuple(matched))
