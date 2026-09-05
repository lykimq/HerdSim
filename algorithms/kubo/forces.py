"""Force components for Kubo 2022 multi-dog herding.

Faithful Python port of the MATLAB force terms in
matlab/Force-Based-Sheep-Herding-Algorithm/src/main.m.
"""

from __future__ import annotations

import numpy as np

EPS = 1e-6


def agents_in_range(
    pos_i: np.ndarray, positions: np.ndarray, radius: float, exclude_self: bool = True
) -> tuple[np.ndarray, np.ndarray]:
    """Return (positions_in_range, boolean_mask)."""
    diffs = pos_i - positions
    dists = np.linalg.norm(diffs, axis=1)
    mask = dists < radius
    if exclude_self:
        mask &= dists > 0
    return positions[mask], mask


def sheep_force_components(
    index: int,
    sheep_pos: np.ndarray,
    sheep_vel: np.ndarray,
    dog_pos: np.ndarray,
    radius: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Compute sheep force terms a,b,c,d for sheep `index`.

    a: sheep-sheep repulsion (1/r^2)
    b: velocity alignment
    c: cohesion toward neighbours
    d: dog repulsion (1/r^3)
    """
    pos_i = sheep_pos[index]
    neighbours, _ = agents_in_range(pos_i, sheep_pos, radius)
    n_s = neighbours.shape[0]

    if n_s == 0:
        a_i = np.zeros(2)
        b_i = np.zeros(2)
        c_i = np.zeros(2)
    else:
        diff = pos_i - neighbours
        dist = np.linalg.norm(diff, axis=1)
        dist_safe = np.maximum(dist, EPS)
        a_i = np.mean(diff / (dist_safe**2)[:, None], axis=0)
        c_i = -np.mean(diff / dist_safe[:, None], axis=0)

        # Alignment uses neighbour velocities matching neighbour positions.
        neigh_mask = (np.linalg.norm(sheep_pos - pos_i, axis=1) < radius) & (
            np.linalg.norm(sheep_pos - pos_i, axis=1) > 0
        )
        vel_in_range = sheep_vel[neigh_mask]
        speeds = np.linalg.norm(vel_in_range, axis=1)
        valid = speeds > 0
        if np.any(valid):
            b_i = np.mean(vel_in_range[valid] / speeds[valid, None], axis=0)
        else:
            b_i = np.zeros(2)

    dogs, _ = agents_in_range(pos_i, dog_pos, radius, exclude_self=False)
    if dogs.shape[0] == 0:
        d_i = np.zeros(2)
    else:
        diff = pos_i - dogs
        dist = np.maximum(np.linalg.norm(diff, axis=1), EPS)
        d_i = np.mean(diff / (dist**3)[:, None], axis=0)

    return a_i, b_i, c_i, d_i


def target_sheep_farthest_from_goal(
    goal_pos: np.ndarray, sheep_in_range: np.ndarray
) -> np.ndarray:
    """Return the sheep position farthest from the goal."""
    dists = np.linalg.norm(sheep_in_range - goal_pos, axis=1)
    return sheep_in_range[int(np.argmax(dists))]


def dog_force_components(
    index: int,
    dog_pos: np.ndarray,
    sheep_pos: np.ndarray,
    goal_pos: np.ndarray,
    radius: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Compute dog force terms A,B,C,D for dog `index`.

    A: attraction toward farthest-from-goal sheep in range
    B: inverse-cube repulsion from that target sheep
    C: repulsion from goal (or weak attraction if no sheep in range)
    D: inverse-cube repulsion from other dogs
    """
    dog_i = dog_pos[index]
    sheep_in_range, _ = agents_in_range(dog_i, sheep_pos, radius, exclude_self=False)

    if sheep_in_range.shape[0] == 0:
        a_i = np.zeros(2)
        b_i = np.zeros(2)
        diff_goal = goal_pos - dog_i
        dist_goal = np.linalg.norm(diff_goal)
        c_i = 0.1 * diff_goal / (dist_goal + EPS)
        d_i = np.zeros(2)
        return a_i, b_i, c_i, d_i

    target = target_sheep_farthest_from_goal(goal_pos, sheep_in_range)
    diff = dog_i - target
    dist = np.linalg.norm(diff)
    a_i = -diff / (dist + EPS)
    b_i = diff / ((dist + EPS) ** 3)

    diff_goal = dog_i - goal_pos
    dist_goal = np.linalg.norm(diff_goal)
    c_i = diff_goal / (dist_goal + EPS)

    other_dogs = np.delete(dog_pos, index, axis=0)
    dogs_in_range, _ = agents_in_range(dog_i, other_dogs, radius, exclude_self=False)
    if dogs_in_range.shape[0] == 0:
        d_i = np.zeros(2)
    else:
        diff = dog_i - dogs_in_range
        dist = np.maximum(np.linalg.norm(diff, axis=1), EPS)
        d_i = np.mean(diff / (dist**3)[:, None], axis=0)

    return a_i, b_i, c_i, d_i


def clamp_speed(velocities: np.ndarray, max_speed: float) -> np.ndarray:
    """Limit each velocity vector to max_speed."""
    speeds = np.linalg.norm(velocities, axis=1)
    out = velocities.copy()
    exceed = speeds > max_speed
    if np.any(exceed):
        out[exceed] = out[exceed] / speeds[exceed, None] * max_speed
    return out
