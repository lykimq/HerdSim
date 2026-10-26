"""Circular goal zone setup, spatial metrics, and arrival time tracking."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from sim.core.world.arena import GoalZone, World
from sim.plugins.metrics.view import TickView

# Flock arrival fractions for which time-to-arrival metrics (seconds_to_<pct>pct_in_goal)
# are logged in trial results to enable post-hoc analysis under relaxed success thresholds.
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
    """Return 1.0 if the flock centroid is inside the goal zone, else 0.0."""
    return float(view.state.world.goal.contains(view.centroid[None, :])[0])


def sheep_in_goal(view: TickView) -> float:
    """Number of sheep inside the goal."""
    state = view.state
    return float(np.sum(state.world.goal.contains(state.sheep_positions)))


def dogs_goal_side(view: TickView) -> float:
    """Fraction of dogs positioned between flock centroid and goal (NaN if no dogs)."""
    state = view.state
    if state.n_shepherds == 0:
        return float("nan")
    to_goal = state.world.goal.center - view.centroid
    to_dogs = state.shepherd_positions - view.centroid
    return float(np.mean(to_dogs @ to_goal > 0.0))


def arrival_columns(config: dict[str, Any], history: pd.DataFrame) -> dict[str, float]:
    """Compute elapsed seconds to reach flock arrival thresholds (unheld first arrivals)."""
    dt = float(config["dt"])
    n = int(config["n_sheep"])
    inside = history["sheep_in_goal"].to_numpy(dtype=float)
    out: dict[str, float] = {}
    for fraction in ARRIVAL_FRACTIONS:
        hit = np.flatnonzero(inside >= fraction * n)
        ticks = float(history["tick"].to_numpy()[hit[0]]) if hit.size else float("nan")
        out[f"seconds_to_{round(fraction * 100)}pct_in_goal"] = ticks * dt
    return out
