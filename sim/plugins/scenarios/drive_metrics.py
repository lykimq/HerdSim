"""Metrics of the drive task: progress toward the circular goal. Each takes a TickView
and returns one float; the task records them next to the generic metrics."""

from __future__ import annotations

import numpy as np

from sim.plugins.metrics.view import TickView


def gcm_goal(view: TickView) -> float:
    """Distance from the flock centroid to the goal centre."""
    return float(np.linalg.norm(view.centroid - view.state.world.goal.center))


def gcm_in_goal(view: TickView) -> float:
    """1.0 if the flock centroid is inside the goal, else 0.0.

    Lets Strombom's GCM criterion be read from the history; success itself
    stays the all-sheep rule.
    """
    return float(view.state.world.goal.contains(view.centroid[None, :])[0])


def sheep_in_goal(view: TickView) -> float:
    """Number of sheep inside the goal."""
    state = view.state
    return float(np.sum(state.world.goal.contains(state.sheep_positions)))


def dogs_goal_side(view: TickView) -> float:
    """Fraction of dogs on the goal side of the flock, where they push it backwards.

    NaN without dogs. Noise once the centroid is at the goal centre, where the
    direction to the goal is undefined.
    """
    state = view.state
    if state.n_shepherds == 0:
        return float("nan")
    to_goal = state.world.goal.center - view.centroid
    to_dogs = state.shepherd_positions - view.centroid
    return float(np.mean(to_dogs @ to_goal > 0.0))
