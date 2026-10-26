"""Lama and di Bernardo 2024 dynamics, vectorised over targets and herders.

Positions are relative to the goal centre, which is the paper's origin: every |T| and |H| below
is a distance from it.

Targets (eq. 1), one Euler-Maruyama step per target a:

    T_a += dt x beta sum_{i: |H_i - T_a| <= lambda} (lambda - |H_i - T_a|) u_ia
           + sqrt(2 D dt) x standard normal (per coordinate)

with u_ia the unit vector from herder i to target a. The paper prints the unit vector as d-hat
with d = H - T, pointing from the target to the herder; the text ("targets are repelled by
nearby herders", "maximum escaping speed") needs the push away from the herder, which is what
``target_velocities`` computes. The push is linear in distance (beta lambda at contact, 0 at
lambda) and the pushes of several herders add. There is no cohesion and no speed cap.

Herders (eqs. 2 to 4), forward Euler, no noise:

    dH_i/dt = (1 - eta_i) F_i + eta_i I_i
    F_i = -v_H unit(H_i) if |H_i| >= r*, else 0
    I_i = saturate_{v_H}( alpha (P_i - H_i) ),   P_i = T*_i + delta unit(T*_i)

T*_i is the target farthest from the origin among those within xi of herder i, leaving out any
target that is closer to another herder j within xi of i than to i (|T - H_i| <= |T - H_j| is
required, p. 2). eta_i is 1 when such a target exists. Targets inside the goal are not excluded.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from scipy.spatial.distance import cdist

from sim.core.vectors import EPS, unit_rows

# State metadata key: the targets' positions at the start of the tick. The target step writes
# it and the herders read it, so both integrate from the state at time t (paper p. 5).
TARGETS_AT_TICK_START = "targets_at_tick_start"


def target_velocities(
    targets: np.ndarray, herders: np.ndarray, config: dict[str, Any]
) -> np.ndarray:
    """Deterministic part of eq. 1 for every target: the summed pushes of the herders within
    ``repulsion_radius``, shape (N, 2). Zero without herders."""
    if herders.shape[0] == 0:
        return np.zeros_like(targets, dtype=float)
    away = targets[:, None, :] - herders[None, :, :]  # (N, D, 2), herder to target
    dist = np.linalg.norm(away, axis=2)
    reach = float(config["repulsion_radius"])
    weight = np.where(dist <= reach, reach - dist, 0.0) / np.maximum(dist, EPS)
    return float(config["repulsion_strength"]) * (away * weight[:, :, None]).sum(axis=1)


def noise_step(rng: np.random.Generator, n: int, config: dict[str, Any]) -> np.ndarray:
    """The Brownian displacement of one step for ``n`` targets: sqrt(2 D dt) x standard normal."""
    scale = np.sqrt(2.0 * float(config["target_diffusion"]) * float(config["dt"]))
    return scale * rng.standard_normal((n, 2))


@dataclass(frozen=True)
class Choice:
    """What each herder chases this tick: the index of its target, or -1 when it has none."""

    target: np.ndarray  # (D,) int


def choose_targets(targets: np.ndarray, herders: np.ndarray, config: dict[str, Any]) -> Choice:
    """The paper's target choice for every herder (p. 2).

    Herder i considers the targets within ``sensing_radius`` of it, minus those closer to a herder
    j within that radius of i than to i, and takes the one farthest from the origin. Ties (two
    targets at the same distance) go to the lower index. A herder with no eligible target gets -1.
    """
    n_herders = herders.shape[0]
    if n_herders == 0 or targets.shape[0] == 0:
        return Choice(np.full(n_herders, -1, dtype=int))
    reach = float(config["sensing_radius"])
    to_targets = cdist(herders, targets)  # (D, N)
    sees = to_targets <= reach
    near = cdist(herders, herders) <= reach
    np.fill_diagonal(near, False)
    # closer[i, j, a]: target a is at least as close to herder i as to herder j, or j is not
    # a neighbour of i and does not count.
    closer = ~near[:, :, None] | (to_targets[:, None, :] <= to_targets[None, :, :])
    eligible = sees & closer.all(axis=1)
    radius = np.linalg.norm(targets, axis=1)
    score = np.where(eligible, radius[None, :], -np.inf)
    chosen = np.argmax(score, axis=1)
    chosen[~eligible.any(axis=1)] = -1
    return Choice(chosen)


def saturate(velocities: np.ndarray, top: float) -> np.ndarray:
    """Each row limited to length ``top`` (the paper's [.]_{v_H})."""
    speed = np.linalg.norm(velocities, axis=1, keepdims=True)
    return velocities * np.minimum(1.0, top / np.maximum(speed, EPS))


def herder_velocities(
    targets: np.ndarray, herders: np.ndarray, goal_radius: float, config: dict[str, Any]
) -> tuple[np.ndarray, Choice]:
    """Velocity of every herder (eqs. 2 to 4), shape (D, 2), and the choice it rests on.

    A herder with a target walks toward the point ``chase_offset`` beyond it on the ray from the
    origin, with gain ``herder_gain``, at most ``herder_speed``. One without a target walks
    straight to the origin at ``herder_speed`` while outside the goal disc of ``goal_radius``,
    and stands still inside it.
    """
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
    """Distance at which a target reacts to a herder: the repulsion radius lambda."""
    return float(config["repulsion_radius"])
