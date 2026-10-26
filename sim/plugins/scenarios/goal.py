"""What tasks with a circular goal share: the world, the goal metrics, the arrival columns.

Each metric takes a TickView and returns one float; a task records the ones that mean
something for it next to the generic metrics. ``arrival_columns`` reads the first arrival of
a share of the flock from a history.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from sim.core.world.arena import GoalZone, World
from sim.plugins.metrics.view import TickView

# Fractions of the flock whose first arrival is recorded in every trial row, so a weaker
# success rule than the task's own can be read afterwards (analysis/dmin.py).
ARRIVAL_FRACTIONS = (0.90, 0.95, 0.99)


def create_world(config: dict[str, Any]) -> World:
    """The field rectangle and the goal disc, with the task's success share and hold time."""
    return World(
        width=float(config["world_width"]),
        height=float(config["world_height"]),
        goal=GoalZone(
            center=np.asarray(config["goal_center"], dtype=float),
            radius=float(config["goal_radius"]),
            required_fraction=float(config["success_fraction"]),
            hold_ticks=int(config["hold_ticks"]),
        ),
    )


def gcm_goal(view: TickView) -> float:
    """Distance from the flock centroid to the goal centre."""
    return float(np.linalg.norm(view.centroid - view.state.world.goal.center))


def gcm_in_goal(view: TickView) -> float:
    """1.0 if the flock centroid is inside the goal, else 0.0: lets Strombom's own end rule
    (centre of mass at the target) be read from the history."""
    return float(view.state.world.goal.contains(view.centroid[None, :])[0])


def sheep_in_goal(view: TickView) -> float:
    """Number of sheep inside the goal."""
    state = view.state
    return float(np.sum(state.world.goal.contains(state.sheep_positions)))


def dogs_goal_side(view: TickView) -> float:
    """Fraction of dogs on the goal side of the flock, where they push it backwards.

    NaN without dogs. Noise once the centroid is at the goal centre, where the direction to
    the goal is undefined.
    """
    state = view.state
    if state.n_shepherds == 0:
        return float("nan")
    to_goal = state.world.goal.center - view.centroid
    to_dogs = state.shepherd_positions - view.centroid
    return float(np.mean(to_dogs @ to_goal > 0.0))


def arrival_columns(config: dict[str, Any], history: pd.DataFrame) -> dict[str, float]:
    """Model seconds until a fraction of the sheep first stood in the goal (NaN if never).

    First arrivals, not held ones: a sheep may leave again before the trial ends.
    """
    dt = float(config["dt"])
    n = int(config["n_sheep"])
    inside = history["sheep_in_goal"].to_numpy(dtype=float)
    out: dict[str, float] = {}
    for fraction in ARRIVAL_FRACTIONS:
        hit = np.flatnonzero(inside >= fraction * n)
        ticks = float(history["tick"].to_numpy()[hit[0]]) if hit.size else float("nan")
        out[f"seconds_to_{round(fraction * 100)}pct_in_goal"] = ticks * dt
    return out
