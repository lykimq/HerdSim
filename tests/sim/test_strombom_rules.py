"""Strombom et al. (2014) rules of the single dog and the sheep, as the engine runs them."""

from __future__ import annotations

from typing import Any

import numpy as np
import pytest

from sim.strombom import sheep
from sim.strombom.shepherd import COLLECT, DRIVE, decide, step_toward
from sim.vectors import unit
from tests.helpers import (
    ANGLE_TOL,
    GOAL,
    flock_with_outlier,
    tight_flock,
)
from tests.helpers import (
    STROMBOM_BASE as BASE,
)
from tests.helpers import (
    strombom_cfg as cfg,
)

R_A = BASE["r_a"]


# --- single-dog collect / drive ----------------------------------------------


def test_drive_target_is_paper_pd_behind_flock() -> None:
    flock = tight_flock(25)
    decision = decide(flock, GOAL, cfg(25))
    assert decision.mode == DRIVE
    centroid = flock.mean(axis=0)
    expected = centroid + unit(centroid - GOAL) * R_A * np.sqrt(25)
    np.testing.assert_allclose(decision.target, expected)


def test_collect_target_is_paper_pc_behind_furthest() -> None:
    flock = flock_with_outlier()
    decision = decide(flock, GOAL, cfg(10))
    assert decision.mode == COLLECT
    centroid = flock.mean(axis=0)
    np.testing.assert_allclose(decision.target, flock[-1] + unit(flock[-1] - centroid) * R_A)


def test_decision_mirrors_with_the_goal() -> None:
    flock = tight_flock(25)
    mirror = np.array([-1.0, 1.0])
    a = decide(flock, GOAL, cfg(25))
    b = decide(flock * mirror, GOAL * mirror, cfg(25))
    np.testing.assert_allclose(b.target, a.target * mirror)


def test_dog_stops_near_sheep_and_always_walks_delta_s() -> None:
    sheep_at = np.array([[0.0, 0.0]])
    stop_distance = 3.0 * R_A  # dog halts inside this distance of any sheep
    noise_angle = 0.3
    far_target = np.array([50.0, 0.0])

    halted = step_toward(
        np.array([stop_distance - 0.1, 0.0]), far_target, sheep_at, BASE, noise_angle
    )
    assert np.all(halted == 0.0)

    walking = step_toward(np.array([20.0, 0.0]), far_target, sheep_at, BASE, noise_angle)
    assert np.linalg.norm(walking) == pytest.approx(BASE["shepherd_speed"])

    # Even a tiny remaining gap still takes a full shepherd_speed step (paper delta_s).
    last_step = step_toward(
        np.array([20.0, 0.0]), np.array([20.1, 0.0]), sheep_at, BASE, noise_angle
    )
    assert np.linalg.norm(last_step) == pytest.approx(BASE["shepherd_speed"])


# --- sheep heading -----------------------------------------------------------
# Slow per-sheep oracle of the paper rule; used only to check the vectorised path.


def _angle_vec(angle: float) -> np.ndarray:
    return np.array([np.cos(angle), np.sin(angle)])


def _dog_is_near(sheep_xy: np.ndarray, dogs: np.ndarray, r_s: float) -> bool:
    return bool(np.any(np.linalg.norm(sheep_xy - dogs, axis=1) < r_s))


def _graze_step(angle: float, speed: float) -> np.ndarray:
    return _angle_vec(angle) * speed


def _local_centre(positions: np.ndarray, index: int, k: int) -> np.ndarray:
    """Mean of the k nearest other sheep (LCM); the sheep itself if k is 0."""
    sheep_xy = positions[index]
    others = np.delete(np.arange(len(positions)), index)
    if k <= 0 or len(others) == 0:
        return sheep_xy
    order = others[np.argsort(np.linalg.norm(positions[others] - sheep_xy, axis=1))]
    return positions[order[:k]].mean(axis=0)


def _sheep_repulsion(positions: np.ndarray, index: int, r_a: float) -> np.ndarray:
    """Sum of unit vectors away from other sheep inside r_a."""
    sheep_xy = positions[index]
    total = np.zeros(2)
    for j, other in enumerate(positions):
        if j == index:
            continue
        gap = np.linalg.norm(sheep_xy - other)
        if 0.0 < gap < r_a:
            total = total + unit(sheep_xy - other)
    return total


def _dog_repulsion(sheep_xy: np.ndarray, dogs: np.ndarray, r_s: float) -> np.ndarray:
    """Unit vector of the summed unit pushes from dogs inside r_s."""
    total = np.zeros(2)
    for dog in dogs:
        if np.linalg.norm(sheep_xy - dog) < r_s:
            total = total + unit(sheep_xy - dog)
    return unit(total)


def _reacting_step(
    positions: np.ndarray,
    prev: np.ndarray,
    dogs: np.ndarray,
    draws: sheep.SheepDraws,
    settings: dict[str, Any],
    index: int,
    k: int,
) -> np.ndarray:
    """One reacting sheep: inertia + LCM + sheep repulsion + dog push + noise."""
    sheep_xy = positions[index]
    heading = (
        settings["inertia"] * unit(prev[index])
        + settings["c"] * unit(_local_centre(positions, index, k) - sheep_xy)
        + settings["rho_a"] * unit(_sheep_repulsion(positions, index, settings["r_a"]))
        + settings["rs_weight"] * _dog_repulsion(sheep_xy, dogs, settings["r_s"])
        + settings["noise_strength"] * _angle_vec(draws.noise_angle[index])
    )
    return unit(heading) * settings["sheep_speed"]


def sheep_reference(
    positions: np.ndarray,
    prev: np.ndarray,
    dogs: np.ndarray,
    draws: sheep.SheepDraws,
    settings: dict[str, Any],
    k: int,
) -> np.ndarray:
    """Per-sheep loop written from the paper terms, on the same random draws."""
    out = np.zeros_like(positions)
    for i, sheep_xy in enumerate(positions):
        if not _dog_is_near(sheep_xy, dogs, settings["r_s"]):
            if draws.graze_move[i] < settings["graze_move_prob"]:
                out[i] = _graze_step(draws.graze_angle[i], settings["sheep_speed"])
            continue
        out[i] = _reacting_step(positions, prev, dogs, draws, settings, i, k)
    return out


def _still_draws(n: int) -> sheep.SheepDraws:
    """Draws that never graze-step and add no heading noise."""
    return sheep.SheepDraws(
        graze_move=np.ones(n),
        graze_angle=np.zeros(n),
        noise_angle=np.zeros(n),
    )


@pytest.mark.parametrize("r_a", [2.0, 1.0])
@pytest.mark.parametrize("k", [29, 7])
@pytest.mark.parametrize("n_dogs", [1, 3])
def test_vectorised_sheep_match_reference(k: int, n_dogs: int, r_a: float) -> None:
    n_sheep = 30
    pos_rng = np.random.default_rng(3)
    positions = pos_rng.normal(0.0, 3.0, size=(n_sheep, 2))
    positions[-1] = [200.0, 200.0]  # far from every dog: must take the graze branch
    prev = pos_rng.normal(0.0, 1.0, size=(n_sheep, 2))
    dogs = pos_rng.normal(0.0, 1.0, size=(n_dogs, 2)) + [8.0, 0.0]
    settings = {**BASE, "r_a": r_a}
    draws = sheep.draw(np.random.default_rng(4), n_sheep)

    got = sheep.velocities(positions, prev, dogs, draws, settings, k)
    expected = sheep_reference(positions, prev, dogs, draws, settings, k)
    np.testing.assert_allclose(got, expected, atol=ANGLE_TOL)


def test_sheep_at_exactly_r_s_grazes() -> None:
    """Reaction is strict < r_s: on the boundary the sheep grazes (stays still here)."""
    flock = np.array([[0.0, 0.0], [0.0, 1.0]])
    prev = np.zeros_like(flock)
    draws = _still_draws(len(flock))
    r_s = BASE["r_s"]

    on_boundary = np.array([[r_s, 0.0]])
    assert np.all(sheep.velocities(flock, prev, on_boundary, draws, BASE, k_neighbors=1) == 0.0)

    just_inside = on_boundary - [1e-9, 0.0]
    assert np.any(sheep.velocities(flock, prev, just_inside, draws, BASE, k_neighbors=1) != 0.0)


def test_graze_repulsion_pushes_apart_sheep_that_no_dog_reaches() -> None:
    """The paper repels sheep closer than r_a at any distance from the dog; off, they stay."""
    flock = np.array([[0.0, 0.0], [1.0, 0.0]])
    far_dog = np.array([[1000.0, 0.0]])
    prev = np.zeros_like(flock)
    draws = _still_draws(len(flock))

    off = sheep.velocities(flock, prev, far_dog, draws, {**BASE, "graze_repulsion": False}, 1)
    on = sheep.velocities(flock, prev, far_dog, draws, {**BASE, "graze_repulsion": True}, 1)

    assert np.all(off == 0.0)
    np.testing.assert_allclose(on, [[-BASE["sheep_speed"], 0.0], [BASE["sheep_speed"], 0.0]])


def test_one_dog_push_is_the_paper_unit_vector() -> None:
    # One sheep, one dog offset by the 3-4-5 triangle -> unit push (0.6, 0.8).
    offset = np.array([3.0, 4.0])
    to_dogs = offset.reshape(1, 1, 2)
    dist = np.linalg.norm(to_dogs, axis=2)
    r_s = 65.0  # well beyond the 5 m gap, so the dog counts
    np.testing.assert_allclose(sheep.dog_push(to_dogs, dist, r_s), [[0.6, 0.8]])
