"""Vectorized Strömböm et al. 2014 sheep heading and flock dynamics.

Sheep state machine:
- Grazing (no dog within r_s): Sheep remains stationary, or steps with probability p
  in a uniform random direction. No neighbor repulsion applies during grazing.
- Reacting (dog within r_s): Computes normalized heading vector:
    H' = h H + c C + rho_a R_a + rho_s R_s + e eps
  combining inertia (H), neighbor attraction (C), neighbor repulsion (R_a),
  dog repulsion (R_s), and angular noise (eps).
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
    """Compute unit repulsion vectors from all neighbors within distance r_a using KD-tree."""
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
    # Normalize combined dog push to unit length.
    # Linear addition would overpower sheep cohesion (c = 1.05): two dogs flanking
    # at theta < 116 deg produce 2*cos(theta/2) > 1.05, tearing the herd apart at D >= 2.
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
    # Sheep speed is fixed at 1.0 m/s.
    # Unlike continuous models (e.g. Kubo), adding more dogs cannot push sheep
    # faster than 1 m/s, which creates the flat completion time plateau at D_sat.

    out[idx] = unit_rows(heading) * speed
    return out


def reaction_radius(config: dict[str, Any]) -> float:
    """Distance at which a sheep reacts to a dog."""
    return float(config["r_s"])
