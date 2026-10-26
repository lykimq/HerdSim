"""Multi-dog collect/drive controller.

Coordinates D dogs using Strömböm collect/drive heuristics:
- Collect: Matches dogs to outliers via minimum-distance bipartite matching. Surplus dogs
  drive the flock core from behind.
- Drive: Spreads dogs along an arc behind the flock covering its width. Dogs are assigned
  slots by angle around the flock center to prevent trajectory crossing.
- Goal withdrawal (`hold_withdraw`): Standoff at distance r_s + r_a once the flock is inside
  the goal zone to let sheep settle.
- Partial observability (`sensing_range`, `communication`): Plans targets from individual,
  shared, or pooled views; dogs with no visible targets recall the last known flock center.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist

from sim.core.simulation_state import SimulationState
from sim.core.vectors import behind, rotate, unit
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
    # Match dogs to arc slots by angular order around flock center to avoid crossing paths.
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


def spread_jobs(flock: np.ndarray, outliers: np.ndarray, count: int, gap: float) -> np.ndarray:
    """Select outlier sheep positions for collecting dogs.

    When gap > 0, enforces minimum spacing between selected outliers to prevent
    dogs from converging on the same sub-cluster.
    """
    if gap <= 0.0:
        return outliers[:count]
    taken: list[int] = []
    for o in outliers:
        if len(taken) == count:
            break
        if all(np.linalg.norm(flock[o] - flock[t]) >= gap for t in taken):
            taken.append(int(o))
    for o in outliers:
        if len(taken) == count:
            break
        if int(o) not in taken:
            taken.append(int(o))
    return np.array(taken, dtype=int)


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
    gap = float(config.get("collect_min_gap", 0.0))
    jobs = spread_jobs(flock, decision.outliers, len(dogs), gap)
    points = np.array([behind(flock[o], decision.centroid, r_a) for o in jobs])

    # Assign dogs to outlier targets minimizing total travel distance.
    rows, cols = linear_sum_assignment(cdist(dogs, points))
    targets = np.empty_like(dogs)
    targets[rows] = points[cols]

    # Dogs not assigned to outliers drive the core flock toward the goal.
    rest = np.setdiff1d(np.arange(len(dogs)), rows)
    if rest.size:
        dists = np.linalg.norm(flock - decision.centroid, axis=1)
        core = flock[dists <= collect_threshold(int(config["n_sheep"]), r_a)]
        targets[rest] = _drive(core if core.size else flock, goal, dogs[rest], config)
    return targets


def withdraw_targets(flock: np.ndarray, dogs: np.ndarray, config: dict[str, Any]) -> np.ndarray:
    """Position dogs beyond sheep reaction distance (r_s + r_a) when goal is reached."""
    centroid = flock.mean(axis=0)
    farthest = float(np.max(np.linalg.norm(flock - centroid, axis=1)))
    reach = farthest + float(config["reaction_radius"]) + float(config["r_a"])
    out = np.empty_like(dogs)
    for i, dog in enumerate(dogs):
        bearing = dog - centroid
        bearing = unit(bearing) if np.linalg.norm(bearing) > 0.0 else np.array([1.0, 0.0])
        out[i] = centroid + reach * bearing
    return out


def known_sheep(sheep: np.ndarray, dogs: np.ndarray, config: dict[str, Any]) -> np.ndarray:
    """Determine visible sheep per dog based on sensing range and communication mode."""
    reach = float(config["sensing_range"])
    sees = cdist(dogs, sheep) < reach
    mode = str(config["communication"])
    if mode == "shared":
        return np.tile(sees.any(axis=0), (len(dogs), 1))
    if mode == "neighbour":
        hears = cdist(dogs, dogs) < reach  # includes the dog itself
        return (hears.astype(int) @ sees.astype(int)) > 0
    return sees


def local_targets(state: SimulationState, config: dict[str, Any]) -> np.ndarray:
    """Targets when each dog knows only part of the flock (``known_sheep``)."""
    sheep, dogs, goal = state.sheep_positions, state.shepherd_positions, state.world.goal.center
    last = state.metadata.setdefault(
        "last_flock_centre",
        np.tile(np.asarray(config["flock_center"], dtype=float), (len(dogs), 1)),
    )
    knows = known_sheep(sheep, dogs, config)
    targets = np.empty_like(dogs)
    if str(config["communication"]) == "shared":
        if knows[0].any():
            targets[:] = team_targets(sheep[knows[0]], goal, dogs, config)
            last[:] = sheep[knows[0]].mean(axis=0)
        else:
            targets[:] = last
        return targets
    for i in range(len(dogs)):
        if knows[i].any():
            targets[i] = team_targets(sheep[knows[i]], goal, dogs, config)[i]
            last[i] = sheep[knows[i]].mean(axis=0)
        else:
            targets[i] = last[i]
    return targets


def step(state: SimulationState, config: dict[str, Any]) -> SimulationState:
    dogs = state.shepherd_positions
    velocities = np.zeros((state.n_shepherds, 2))
    angles = noise_angles(state)
    if state.n_shepherds:
        holding = bool(config["hold_withdraw"]) and state.world.goal.reached(state.sheep_positions)
        if holding:
            targets = withdraw_targets(state.sheep_positions, dogs, config)
        elif float(config["sensing_range"]) > 0.0:
            targets = local_targets(state, config)
        else:
            targets = team_targets(state.sheep_positions, state.world.goal.center, dogs, config)
        for i in range(state.n_shepherds):
            velocities[i] = step_toward(
                dogs[i], targets[i], state.sheep_positions, config, angles[i]
            )
    return move_dogs(state, velocities, float(config["dt"]), config)
