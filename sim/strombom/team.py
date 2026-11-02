"""Multi-dog collect/drive on the Strombom decide rule.

One dog: paper Pc or Pd. More dogs: collect assigns the farthest outliers
(Hungarian); spare dogs drive the core. Drive spreads dogs on an arc behind the
flock (middle = Pd), matched by angle so neighbours do not cross.
"""

from __future__ import annotations

import math
from dataclasses import replace
from typing import Any

import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist

from sim.state import SimulationState
from sim.strombom.shepherd import (
    COLLECT,
    collect_threshold,
    decide,
    drive_point,
    radius_of,
    step_toward,
)
from sim.vectors import behind, rotate


def _angles(points: np.ndarray, centroid: np.ndarray, arm: np.ndarray) -> np.ndarray:
    """Signed angle of each point around ``centroid``, measured from ``arm``."""
    rel = points - centroid
    cross = arm[0] * rel[:, 1] - arm[1] * rel[:, 0]
    return np.arctan2(cross, rel @ arm)


def drive_front(
    centroid: np.ndarray, target: np.ndarray, flock_radius: float, n: int
) -> np.ndarray:
    """``n`` drive slots on the back arc (middle = ``target``), span asin(R_flock / R)."""
    arm = target - centroid
    radius = float(np.linalg.norm(arm))
    if n == 1 or radius == 0.0:
        return np.tile(target, (n, 1))
    half = math.asin(min(1.0, flock_radius / radius))
    return np.array([centroid + rotate(arm, a) for a in np.linspace(-half, half, n)])


def _to_slots(dogs: np.ndarray, slots: np.ndarray, centroid: np.ndarray, arm: np.ndarray):
    """Each dog's slot: dogs and slots sorted by angle round the centroid are paired in order,
    so no two dogs cross on their way."""
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

    # One dog per collect point, with the least total walk.
    rows, cols = linear_sum_assignment(cdist(dogs, points))
    targets = np.empty_like(dogs)
    targets[rows] = points[cols]

    # Dogs left without an outlier drive the core from behind.
    rest = np.setdiff1d(np.arange(len(dogs)), rows)
    if rest.size:
        dists = np.linalg.norm(flock - decision.centroid, axis=1)
        core = flock[dists <= collect_threshold(int(config["n_sheep"]), r_a)]
        targets[rest] = _drive(core if core.size else flock, goal, dogs[rest], config)
    return targets


def step(state: SimulationState, config: dict[str, Any]) -> SimulationState:
    """Advance every dog by ``dt * velocity`` toward its target and store the velocities."""
    dogs = state.shepherd_positions
    velocities = np.zeros((state.n_shepherds, 2))
    # One heading-noise angle per dog, drawn every tick in dog order from the dogs' stream.
    angles = state.dog_rng.uniform(0.0, 2.0 * np.pi, state.n_shepherds)
    if state.n_shepherds:
        targets = team_targets(state.sheep_positions, state.world.goal.center, dogs, config)
        for i in range(state.n_shepherds):
            velocities[i] = step_toward(
                dogs[i], targets[i], state.sheep_positions, config, angles[i]
            )
    return replace(
        state,
        shepherd_positions=dogs + float(config["dt"]) * velocities,
        shepherd_velocities=velocities,
    )
