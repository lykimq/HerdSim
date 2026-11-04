"""Strombom et al. 2014 sheep heading (vectorised).

Beyond r_s: graze (stay or one random step of length delta). Inside r_s: eq. 4.2
heading, then move at sheep_speed. Multi-dog R_s is ``dog_push``. Where the paper is
silent: H is the last velocity (zero after a still tick). The paper repels sheep from each
other at any distance from the dog (section 2); with ``graze_repulsion`` a grazing sheep
closer than r_a to another takes a step along the inertia, repulsion and noise terms of
eq. 4.2. Off by default, which is how every study protocol ran.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

import numpy as np
from scipy.spatial import cKDTree

from sim.state import SimulationState
from sim.vectors import EPS, angle_vectors, unit_rows

from .params import resolve_n_neighbors


@dataclass(frozen=True)
class SheepDraws:
    """Random numbers for one tick, drawn in a fixed order for every sheep."""

    graze_move: np.ndarray  # (N,) uniform in [0, 1)
    graze_angle: np.ndarray  # (N,) radians
    noise_angle: np.ndarray  # (N,) radians


def draw(rng: np.random.Generator, n: int) -> SheepDraws:
    return SheepDraws(
        graze_move=rng.random(n),
        graze_angle=rng.uniform(0.0, 2.0 * np.pi, n),
        noise_angle=rng.uniform(0.0, 2.0 * np.pi, n),
    )


def neighbour_centres(positions: np.ndarray, idx: np.ndarray, k: int) -> np.ndarray:
    """Centre of the k nearest other sheep for each sheep in ``idx``."""
    n = positions.shape[0]
    if n == 1:
        return positions[idx].copy()
    if k == n - 1:
        return (positions.sum(axis=0) - positions[idx]) / (n - 1)
    dist = np.linalg.norm(positions[idx][:, None, :] - positions[None, :, :], axis=2)
    dist[np.arange(idx.size), idx] = np.inf
    nearest = np.argpartition(dist, k - 1, axis=1)[:, :k]
    return positions[nearest].mean(axis=1)


def sheep_repulsion(positions: np.ndarray, idx: np.ndarray, r_a: float) -> np.ndarray:
    """Eq. 4.1: unit repulsion from neighbours closer than r_a (KD-tree pairs)."""
    pairs = cKDTree(positions).query_pairs(r_a, output_type="ndarray")
    total = np.zeros_like(positions, dtype=float)
    if pairs.size:
        diff = positions[pairs[:, 0]] - positions[pairs[:, 1]]
        dist = np.linalg.norm(diff, axis=1)
        keep = (dist < r_a) & (dist > 0.0)
        units = diff[keep] / dist[keep, None]
        np.add.at(total, pairs[keep, 0], units)
        np.add.at(total, pairs[keep, 1], -units)
    return total[idx]


def dog_push(to_dogs: np.ndarray, dist: np.ndarray, r_s: float) -> np.ndarray:
    """Multi-dog R_s: unit of the summed unit pushes from dogs within r_s.

    Normalised so several dogs cannot outweigh cohesion (rho_s stays 1).
    """
    near = dist < r_s
    units = to_dogs / np.maximum(dist, EPS)[:, :, None]
    return unit_rows((units * near[:, :, None]).sum(axis=1))


def velocities(
    positions: np.ndarray,
    prev_velocities: np.ndarray,
    dogs: np.ndarray,
    draws: SheepDraws,
    config: dict[str, Any],
    k_neighbors: int,
) -> np.ndarray:
    """New velocity of every sheep for one tick."""
    n = positions.shape[0]
    out = np.zeros((n, 2))
    r_a, r_s, speed = float(config["r_a"]), float(config["r_s"]), float(config["sheep_speed"])

    to_dogs = positions[:, None, :] - dogs[None, :, :]
    dist = np.linalg.norm(to_dogs, axis=2)
    active = (dist < r_s).any(axis=1)

    grazing_step = ~active & (draws.graze_move < float(config["graze_move_prob"]))
    out[grazing_step] = angle_vectors(draws.graze_angle[grazing_step]) * speed

    idx = np.flatnonzero(active)
    if idx.size == 0 and not config["graze_repulsion"]:
        return out  # no sheep reacts or steps apart: skip the neighbour search
    push_apart = sheep_repulsion(positions, np.arange(n), r_a)
    if config["graze_repulsion"]:
        crowded = np.flatnonzero(~active & (np.linalg.norm(push_apart, axis=1) > 0.0))
        heading = (
            float(config["inertia"]) * unit_rows(prev_velocities[crowded])
            + float(config["rho_a"]) * unit_rows(push_apart[crowded])
            + float(config["noise_strength"]) * angle_vectors(draws.noise_angle[crowded])
        )
        out[crowded] = unit_rows(heading) * speed
    if idx.size == 0:
        return out
    pos = positions[idx]
    attraction = unit_rows(neighbour_centres(positions, idx, k_neighbors) - pos)
    repulsion = unit_rows(push_apart[idx])
    push = dog_push(to_dogs[idx], dist[idx], r_s)
    heading = (
        float(config["inertia"]) * unit_rows(prev_velocities[idx])
        + float(config["c"]) * attraction
        + float(config["rho_a"]) * repulsion
        + float(config["rs_weight"]) * push
        + float(config["noise_strength"]) * angle_vectors(draws.noise_angle[idx])
    )
    # A reacting sheep always moves at sheep_speed: the dogs change its heading, never its
    # speed, so more dogs cannot drive a flock faster than one sheep walks.
    out[idx] = unit_rows(heading) * speed
    return out


def prepare(config: dict[str, Any]) -> dict[str, Any]:
    """The keys the sheep derive from the config: the neighbour count k."""
    return {"k_neighbors": resolve_n_neighbors(config["n_neighbors"], int(config["n_sheep"]))}


def top_speed(config: dict[str, Any]) -> float:
    """Units per second: one heading of length ``sheep_speed`` is walked per tick at dt = 1."""
    return float(config["sheep_speed"])


def step(state: SimulationState, config: dict[str, Any]) -> SimulationState:
    """Advance every sheep by ``dt * velocity`` (dt = 1 is the paper's one step per tick)."""
    moved = velocities(
        state.sheep_positions,
        state.sheep_velocities,
        state.shepherd_positions,
        draw(state.rng, state.n_sheep),
        config,
        int(config["k_neighbors"]),
    )
    return replace(
        state,
        sheep_positions=state.sheep_positions + float(config["dt"]) * moved,
        sheep_velocities=moved,
    )
