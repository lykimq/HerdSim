"""Lama & di Bernardo 2024 dynamics vectorised over targets and herders.

All coordinates are defined relative to the goal centre at the origin.
- Targets: Integrate stochastic Brownian motion and linear distance-dependent repulsion
  from all herders within repulsion radius lambda.
- Herders: Chase assigned targets with gain alpha toward offset points, bounded by speed v_H;
  or return toward the origin if unassigned until reaching the goal perimeter.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from scipy.spatial.distance import cdist

from sim.core.vectors import EPS, unit_rows

# Metadata key storing target coordinates at tick start for synchronous controller updates.
TARGETS_AT_TICK_START = "targets_at_tick_start"


def target_velocities(
    targets: np.ndarray, herders: np.ndarray, config: dict[str, Any]
) -> np.ndarray:
    """Compute net repulsive velocity on targets exerted by herders within repulsion_radius."""
    if herders.shape[0] == 0:
        return np.zeros_like(targets, dtype=float)
    away = targets[:, None, :] - herders[None, :, :]  # (N, D, 2), herder to target
    dist = np.linalg.norm(away, axis=2)
    reach = float(config["repulsion_radius"])
    weight = np.where(dist <= reach, reach - dist, 0.0) / np.maximum(dist, EPS)
    return float(config["repulsion_strength"]) * (away * weight[:, :, None]).sum(axis=1)


def noise_step(rng: np.random.Generator, n: int, config: dict[str, Any]) -> np.ndarray:
    """Generate Brownian displacement for `n` targets over one timestep."""
    scale = np.sqrt(2.0 * float(config["target_diffusion"]) * float(config["dt"]))
    return scale * rng.standard_normal((n, 2))


@dataclass(frozen=True)
class Choice:
    """Target assignment per herder: index of assigned target, or -1 if unassigned."""
    target: np.ndarray  # (D,) int


def choose_targets(targets: np.ndarray, herders: np.ndarray, config: dict[str, Any]) -> Choice:
    """Assign targets to herders based on local sensing radius and proximity arbitration."""
    n_herders = herders.shape[0]
    if n_herders == 0 or targets.shape[0] == 0:
        return Choice(np.full(n_herders, -1, dtype=int))
    reach = float(config["sensing_radius"])
    to_targets = cdist(herders, targets)  # (D, N)
    sees = to_targets <= reach
    near = cdist(herders, herders) <= reach
    np.fill_diagonal(near, False)
    # Target a is eligible for herder i if i is as close to a as any neighboring herder j
    closer = ~near[:, :, None] | (to_targets[:, None, :] <= to_targets[None, :, :])
    eligible = sees & closer.all(axis=1)
    radius = np.linalg.norm(targets, axis=1)
    score = np.where(eligible, radius[None, :], -np.inf)
    chosen = np.argmax(score, axis=1)
    chosen[~eligible.any(axis=1)] = -1
    return Choice(chosen)


def saturate(velocities: np.ndarray, top: float) -> np.ndarray:
    """Clamp 2D velocity vectors to maximum magnitude `top`."""
    speed = np.linalg.norm(velocities, axis=1, keepdims=True)
    return velocities * np.minimum(1.0, top / np.maximum(speed, EPS))


def herder_velocities(
    targets: np.ndarray, herders: np.ndarray, goal_radius: float, config: dict[str, Any]
) -> tuple[np.ndarray, Choice]:
    """Compute herder velocities toward assigned targets or returning toward the goal."""
    choice = choose_targets(targets, herders, config)
    top = float(config["herder_speed"])
    out = np.zeros_like(herders, dtype=float)
    chasing = choice.target >= 0
    if chasing.any():
        aim = targets[choice.target[chasing]]
        point = aim + float(config["chase_offset"]) * unit_rows(aim)
        out[chasing] = saturate(float(config["herder_gain"]) * (point - herders[chasing]), top)
    idle = ~chasing
    if idle.any():
        outside = np.linalg.norm(herders[idle], axis=1) >= goal_radius
        home = -top * unit_rows(herders[idle])
        out[idle] = np.where(outside[:, None], home, 0.0)
    return out, choice


def reaction_radius(config: dict[str, Any]) -> float:
    """Return target reaction threshold (herder repulsion radius lambda)."""
    return float(config["repulsion_radius"])
