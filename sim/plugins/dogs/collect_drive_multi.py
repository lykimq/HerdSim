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

With ``hold_withdraw`` (a HerdSim holding step, not from the papers), while the goal is
reached every dog walks to the point r_s + r_a beyond the farthest sheep on its own bearing
from the flock centre, so no dog is within r_s of a sheep and the flock grazes. When the goal is
no longer reached the team rule above takes over again.

With ``sensing_range`` above 0 (report section 3.12) a dog knows only the sheep within
that range, plus what other dogs see under ``communication``: with shared, the team is planned
once from the pooled view; with none or neighbour, each dog plans the team from its own view
and takes its own target from that plan. f(N) and the drive offset use the true N. A dog that
knows no sheep walks to the flock centre it last knew, kept per dog in ``state.metadata``.
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
    # Preserves cyclic angular topology around the herd centroid: dogs sorted by polar angle
    # are assigned to drive arc slots sorted in the same angular order. This invariant strictly
    # eliminates intersecting trajectories, preventing shepherds from colliding or cutting
    # across each other's driving lanes.
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
    """The outliers the collecting dogs take: the ``count`` farthest (the team rule), or with
    ``gap`` > 0 the farthest first but none closer than ``gap`` to one already taken, so the dogs
    do not all go to one cluster; the rest are filled in farthest first if too few are that far
    apart. ``gap`` is a diagnostic hook (``collect_min_gap`` in a config, not a protocol
    setting; cli/diagnostics/split_diagnostic.py), 0 in every campaign."""
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

    # Hungarian assignment (linear_sum_assignment) globally minimizes total Euclidean distance
    # traveled by all dogs.
    # Algorithmic pathology on 'split' pastures: Euclidean minimization is topologically cluster-blind.
    # If the herd ruptures into separate clusters, a cluster marginally closer or with more strays
    # captures all dogs. The entire pack swarms one sub-cluster while the abandoned cluster drifts.
    # Enforcing target dispersion via `spread_jobs(gap=f(N))` restores parallel collection.
    rows, cols = linear_sum_assignment(cdist(dogs, points))
    targets = np.empty_like(dogs)
    targets[rows] = points[cols]

    # Surplus dogs beyond the number of active strays do not idle: they form a driving arc behind
    # the cohesive herd core to maintain forward pressure toward the goal while perimeter dogs collect.
    rest = np.setdiff1d(np.arange(len(dogs)), rows)
    if rest.size:
        dists = np.linalg.norm(flock - decision.centroid, axis=1)
        core = flock[dists <= collect_threshold(int(config["n_sheep"]), r_a)]
        targets[rest] = _drive(core if core.size else flock, goal, dogs[rest], config)
    return targets


def withdraw_targets(flock: np.ndarray, dogs: np.ndarray, config: dict[str, Any]) -> np.ndarray:
    # Holding task withdrawal policy:
    # Positions shepherds r_s + r_a = 67 m beyond the farthest sheep along each dog's outward ray
    # from the flock center. This removes canine fear vectors, allowing sheep to enter calm grazing.
    #
    # Geometric failure mode at small N (N <= 50):
    # Small flock goal pens are only 12-14 m across. Forcing dogs to retreat 67 m into open pasture
    # removes all containment barriers; sheep randomly diffuse out of the small pen opening before
    # the holding timer expires, causing timeout failures unrelated to multi-agent herding capacity.
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
    """Which sheep each dog knows, shape (D, N): within ``sensing_range`` of it, and under
    ``communication`` also what the dogs it hears see (neighbour: dogs within the range;
    shared: every dog)."""
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
