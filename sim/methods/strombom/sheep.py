"""Strombom et al. 2014 sheep heading, vectorised over the flock.

A sheep farther than r_s from every dog grazes: it stays put, or with probability p takes
one step in a random direction. A sheep closer than r_s to a dog takes the heading of
eq. 4.2,

    H' = h H + c C + rho_a R_a + rho_s R_s + e eps

with every term a unit vector: H the previous heading, C toward the centre of its n nearest
neighbours, R_a away from neighbours closer than r_a (eq. 4.1), R_s away from the dogs,
eps random. It then moves sheep_speed along H' (eq. 4.3). Only the dog term is extended
for several dogs, see ``dog_push``.

Three readings of the paper, which gives no rule for any of them:

- A grazing sheep gets no repulsion from its neighbours: the paper introduces R_a inside
  the reacting heading and says of grazing only that agents "exhibit small random
  movements". A flock that is not being herded therefore does not spread out.
- A grazing step has length delta (Table 1 defines delta as the displacement per time
  step without restricting it to the reacting case) in a direction uniform on [0, 2 pi).
- The previous heading H is the last stored velocity, so it is zero after a tick in which
  the sheep did not move; the paper is silent on a stationary agent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from scipy.spatial import cKDTree

from sim.core.vectors import EPS, angle_vectors, unit_rows


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
    """Eq. 4.1: sum of unit vectors away from every sheep closer than r_a.

    Close pairs come from a KD-tree, so the cost grows with their number, not with N^2.
    """
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
    """R_s for several dogs: the unit vector of the summed unit vectors away from the dogs
    within r_s.

    Summing without normalising would let two dogs overpower the cohesion c = 1.05 (two
    dogs less than 116 degrees apart push with more than 2 cos(58) = 1.05) and tear the
    flock apart from D = 2 on. Normalising keeps the paper's weight rho_s = 1 per sheep.
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
    if idx.size == 0:
        return out
    pos = positions[idx]
    attraction = unit_rows(neighbour_centres(positions, idx, k_neighbors) - pos)
    repulsion = unit_rows(sheep_repulsion(positions, idx, r_a))
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


def reaction_radius(config: dict[str, Any]) -> float:
    """Distance at which a sheep reacts to a dog."""
    return float(config["r_s"])
