"""Multi-dog collect/drive (dog_controller=collect_drive_multi).

The dogs take the Strombom 2014 decision (``heuristics.decide``) on the whole flock. With one
dog that is the whole rule: the dog goes to the paper's collect point Pc or drive point Pd.
With more dogs a team layer gives every dog its own target, so an added dog does not repeat
the target of one that is already there (at large D dogs can still stand next to each other):

- collect: the D farthest outliers each get one dog, matched to the dogs by distance (the
  assignment with the least total walk to the collect points, ``linear_sum_assignment``).
  With one dog this is the paper's farthest outlier. When there are more dogs than outliers,
  the dogs left over drive the core of the flock (the sheep within f(N)) from behind, so they
  push the part of the flock no collecting dog works on;
- drive: the dogs stand on an arc behind the flock at the paper drive distance R, spread
  evenly over the angle that covers the flock's width (half-angle asin(R_flock / R)), so each
  dog works its own stretch of the flock's back edge. The middle of the arc is the paper
  point Pd. No dog is ever placed on the goal side.

Dogs are matched to drive slots by their angle around the flock centre, so neighbours stay
neighbours and no two dogs cross to swap places. Every dog knows every sheep and every other
dog, so the team is planned once per tick from the true state.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist

from sim.core.simulation_state import SimulationState
from sim.core.vectors import behind, rotate
from sim.methods.strombom.heuristics import (
    COLLECT,
    collect_threshold,
    decide,
    drive_point,
    radius_of,
    step_toward,
)

from .helpers import move_dogs, noise_angles


def _angles(points: np.ndarray, centroid: np.ndarray, arm: np.ndarray) -> np.ndarray:
    """Signed angle of each point around ``centroid``, measured from ``arm``."""
    rel = points - centroid
    cross = arm[0] * rel[:, 1] - arm[1] * rel[:, 0]
    return np.arctan2(cross, rel @ arm)


def drive_front(
    centroid: np.ndarray, target: np.ndarray, flock_radius: float, n: int
) -> np.ndarray:
    """``n`` drive slots behind the flock, in increasing angle; the middle one is ``target``.

    Spread over the half-angle asin(flock_radius / R) that covers the flock's width, where R is
    the distance from the centroid to ``target``.
    """
    arm = target - centroid
    radius = float(np.linalg.norm(arm))
    if n == 1 or radius == 0.0:
        return np.tile(target, (n, 1))
    half = math.asin(min(1.0, flock_radius / radius))
    return np.array([centroid + rotate(arm, a) for a in np.linspace(-half, half, n)])


def _to_slots(dogs: np.ndarray, slots: np.ndarray, centroid: np.ndarray, arm: np.ndarray):
    """Slot of each dog: dogs in order of their angle around the flock take the slots in order."""
    order = np.argsort(_angles(dogs, centroid, arm), kind="stable")
    slot_order = np.argsort(_angles(slots, centroid, arm), kind="stable")
    out = np.empty_like(dogs)
    out[order] = slots[slot_order]
    return out


def _drive(
    flock: np.ndarray, goal: np.ndarray, dogs: np.ndarray, config: dict[str, Any]
) -> np.ndarray:
    """Targets of ``dogs`` driving ``flock``: one slot each on its drive front."""
    centroid = flock.mean(axis=0)
    target = drive_point(flock, goal, config)
    slots = drive_front(centroid, target, radius_of(flock, centroid), len(dogs))
    return _to_slots(dogs, slots, centroid, target - centroid)


def team_targets(
    flock: np.ndarray, goal: np.ndarray, dogs: np.ndarray, config: dict[str, Any]
) -> np.ndarray:
    """Target of every dog; shape (D, 2)."""
    decision = decide(flock, goal, config)
    if len(dogs) == 1:
        return decision.target[None, :]
    if decision.mode != COLLECT:
        return _drive(flock, goal, dogs, config)
    r_a = float(config["r_a"])
    jobs = decision.outliers[: len(dogs)]
    points = np.array([behind(flock[o], decision.centroid, r_a) for o in jobs])
    rows, cols = linear_sum_assignment(cdist(dogs, points))
    targets = np.empty_like(dogs)
    targets[rows] = points[cols]
    rest = np.setdiff1d(np.arange(len(dogs)), rows)
    if rest.size:
        dists = np.linalg.norm(flock - decision.centroid, axis=1)
        core = flock[dists <= collect_threshold(int(config["n_sheep"]), r_a)]
        targets[rest] = _drive(core if core.size else flock, goal, dogs[rest], config)
    return targets


def step(state: SimulationState, config: dict[str, Any]) -> SimulationState:
    dogs = state.shepherd_positions
    velocities = np.zeros((state.n_shepherds, 2))
    angles = noise_angles(state)
    if state.n_shepherds:
        targets = team_targets(state.sheep_positions, state.world.goal.center, dogs, config)
        for i in range(state.n_shepherds):
            velocities[i] = step_toward(
                dogs[i], targets[i], state.sheep_positions, config, angles[i]
            )
    return move_dogs(state, velocities, float(config["dt"]))
