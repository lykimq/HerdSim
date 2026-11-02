"""Strombom 2014 rules: shepherd decision, multi-dog layer, and sheep heading."""

from __future__ import annotations

from typing import Any

import numpy as np
import pytest

from sim.strombom import sheep
from sim.strombom.params import resolve_n_neighbors
from sim.strombom.shepherd import (
    COLLECT,
    DRIVE,
    decide,
    drive_point,
    radius_of,
    step_toward,
)
from sim.strombom.team import drive_front, team_targets
from sim.vectors import behind, unit
from tests.helpers import config_for

BASE = config_for("strombom_multi", n=10, d=1)
R_A = BASE["r_a"]
GOAL = np.array([200.0, 0.0])  # goal lies to the right; dogs approach from -x
DOG_BEHIND_X = -40.0  # dogs start this far left of the flock centre
DOG_SPREAD_Y = 20.0  # half-width of the dog line along y
WIDE_SCALE = 6.0  # stretch a tight flock so drive slots have room to fan out
ANGLE_TOL = 1e-12


# --- helpers -----------------------------------------------------------------


def cfg(n_sheep: int, **overrides: Any) -> dict[str, Any]:
    """Run config for a flock of ``n_sheep``: the rule uses true N, not the sheep passed in."""
    return {**BASE, "n_sheep": n_sheep, **overrides}


def tight_flock(n: int, center: tuple[float, float] = (0.0, 0.0)) -> np.ndarray:
    rng = np.random.default_rng(1)
    return np.asarray(center) + rng.normal(0.0, 0.5, size=(n, 2))


def wide_flock(n: int = 25) -> np.ndarray:
    """Tight flock scaled up so the back-edge drive arc is wide enough to check."""
    return tight_flock(n) * WIDE_SCALE


def flock_with_outlier(core: int = 9, outlier: tuple[float, float] = (30.0, 0.0)) -> np.ndarray:
    return np.vstack([tight_flock(core), [list(outlier)]])


def dogs_behind(n_dogs: int, flock: np.ndarray) -> np.ndarray:
    """Dogs on a line behind the flock (away from the goal), spread sideways."""
    centroid = flock.mean(axis=0)
    xs = np.full(n_dogs, DOG_BEHIND_X)
    ys = np.linspace(-DOG_SPREAD_Y, DOG_SPREAD_Y, n_dogs)
    return centroid + np.column_stack([xs, ys])


def signed_angles(points: np.ndarray, centroid: np.ndarray, arm: np.ndarray) -> np.ndarray:
    """Signed angle of each point around ``centroid``, measured from ``arm``."""
    rel = points - centroid
    return np.arctan2(arm[0] * rel[:, 1] - arm[1] * rel[:, 0], rel @ arm)


def evenly_spaced_angles(half_span: float, count: int) -> np.ndarray:
    return np.linspace(-half_span, half_span, count)


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


def test_local_dog_uses_the_true_flock_size() -> None:
    """Seeing 10 of 400 sheep: f(N) and Pd use N = 400, the GCM the 10 seen sheep."""
    seen = tight_flock(10)
    decision = decide(seen, GOAL, cfg(400))
    assert decision.mode == DRIVE
    centroid = seen.mean(axis=0)
    assert np.linalg.norm(decision.target - centroid) == pytest.approx(R_A * np.sqrt(400))


def test_decision_mirrors_with_the_goal() -> None:
    flock = tight_flock(25)
    mirror = np.array([-1.0, 1.0])
    a = decide(flock, GOAL, cfg(25))
    b = decide(flock * mirror, GOAL * mirror, cfg(25))
    np.testing.assert_allclose(b.target, a.target * mirror)


# --- multi-dog layer ---------------------------------------------------------


@pytest.mark.parametrize(
    "flock",
    [tight_flock(25), flock_with_outlier()],
    ids=["drive_flock", "collect_flock"],
)
def test_one_dog_takes_the_paper_target(flock: np.ndarray) -> None:
    n = flock.shape[0]
    paper = decide(flock, GOAL, cfg(n)).target
    team = team_targets(flock, GOAL, dogs_behind(1, flock), cfg(n))
    np.testing.assert_allclose(team[0], paper)


def test_driving_point_dogs_cover_the_flock_width_not_one_point() -> None:
    """Each added dog takes its own stretch of the flock's back edge; the middle is Pd."""
    n_dogs = 5
    flock = wide_flock(25)
    decision = decide(flock, GOAL, cfg(25))
    slots = team_targets(flock, GOAL, dogs_behind(n_dogs, flock), cfg(25))

    drive_radius = np.linalg.norm(decision.target - decision.centroid)
    distances = np.linalg.norm(slots - decision.centroid, axis=1)
    np.testing.assert_allclose(distances, drive_radius)

    flock_radius = radius_of(flock, decision.centroid)
    half_span = np.arcsin(flock_radius / drive_radius)
    arm = decision.target - decision.centroid
    angles = np.sort(signed_angles(slots, decision.centroid, arm))
    np.testing.assert_allclose(angles, evenly_spaced_angles(half_span, n_dogs), atol=ANGLE_TOL)
    assert len(np.unique(np.round(slots, 9), axis=0)) == n_dogs


def test_drive_front_stays_behind_the_flock_at_the_drive_distance() -> None:
    n_dogs = 40
    flock_radius = 2.0
    drive_distance = 10.0
    centroid = np.zeros(2)
    # Pd sits drive_distance behind the centroid; goal is the opposite way (+x).
    drive_point_xy = np.array([-drive_distance, 0.0])

    slots = drive_front(centroid, drive_point_xy, flock_radius, n_dogs)
    offset = slots - centroid
    np.testing.assert_allclose(np.linalg.norm(offset, axis=1), drive_distance)
    assert np.all(offset @ unit(drive_point_xy - centroid) > -1e-9)  # never goal-side

    half_span = np.arcsin(flock_radius / drive_distance)
    angles = np.sort(signed_angles(slots, centroid, drive_point_xy))
    np.testing.assert_allclose(angles, evenly_spaced_angles(half_span, n_dogs), atol=ANGLE_TOL)


def test_collecting_dogs_take_distinct_outliers_nearest_first_and_the_rest_drive_the_core() -> None:
    core = tight_flock(20)
    outliers = np.array([[0.0, 60.0], [0.0, -60.0]])  # above and below the core
    flock = np.vstack([core, outliers])
    # Two dogs near the outliers (matched first), two spare dogs for the drive arc.
    dogs = np.array(
        [
            [DOG_BEHIND_X, -50.0],  # nearest the lower outlier
            [DOG_BEHIND_X, 50.0],  # nearest the upper outlier
            [DOG_BEHIND_X, 0.0],
            [DOG_BEHIND_X, 5.0],
        ]
    )
    n = flock.shape[0]
    targets = team_targets(flock, GOAL, dogs, cfg(n))
    centroid = flock.mean(axis=0)

    # Nearest-first: dog at y=-50 takes the lower outlier, dog at y=50 the upper.
    np.testing.assert_allclose(targets[0], behind(outliers[1], centroid, R_A))
    np.testing.assert_allclose(targets[1], behind(outliers[0], centroid, R_A))

    core_centroid = core.mean(axis=0)
    drive_radius = np.linalg.norm(drive_point(core, GOAL, cfg(n)) - core_centroid)
    drive_slots = targets[2:]
    for slot in drive_slots:
        assert np.linalg.norm(slot - core_centroid) == pytest.approx(drive_radius)
        assert slot[0] < core_centroid[0]  # still behind the core
    assert not np.allclose(drive_slots[0], drive_slots[1])


def test_dogs_keep_their_side_when_matched_to_drive_slots() -> None:
    flock = wide_flock(25)
    dogs = dogs_behind(4, flock)[::-1]  # reverse order: dog 0 is topmost in y
    targets = team_targets(flock, GOAL, dogs, cfg(25))
    assert np.all(np.diff(targets[:, 1]) < 0)  # matched slots keep top-to-bottom order


def test_dog_stops_near_sheep_and_always_walks_delta_s() -> None:
    sheep_at = np.array([[0.0, 0.0]])
    stop_distance = 3.0 * R_A  # dog halts inside this distance of any sheep
    dt = 0.3
    far_target = np.array([50.0, 0.0])

    halted = step_toward(np.array([stop_distance - 0.1, 0.0]), far_target, sheep_at, BASE, dt)
    assert np.all(halted == 0.0)

    walking = step_toward(np.array([20.0, 0.0]), far_target, sheep_at, BASE, dt)
    assert np.linalg.norm(walking) == pytest.approx(BASE["shepherd_speed"])

    # Even a tiny remaining gap still takes a full shepherd_speed step (paper delta_s).
    last_step = step_toward(np.array([20.0, 0.0]), np.array([20.1, 0.0]), sheep_at, BASE, dt)
    assert np.linalg.norm(last_step) == pytest.approx(BASE["shepherd_speed"])


def test_n_neighbors_forms() -> None:
    n_sheep = 50
    assert resolve_n_neighbors(-1, n_sheep) == n_sheep - 1  # "all others"
    assert resolve_n_neighbors(7, n_sheep) == 7
    assert resolve_n_neighbors("0.25N", n_sheep) == 13  # round(0.25 * 50)
    with pytest.raises(ValueError):
        resolve_n_neighbors(7, 5)  # k must be < N
    with pytest.raises(ValueError):
        resolve_n_neighbors("0.25", n_sheep)  # fraction form needs the N suffix


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


def test_one_dog_push_is_the_paper_unit_vector() -> None:
    # One sheep, one dog offset by the 3-4-5 triangle -> unit push (0.6, 0.8).
    offset = np.array([3.0, 4.0])
    to_dogs = offset.reshape(1, 1, 2)
    dist = np.linalg.norm(to_dogs, axis=2)
    r_s = 65.0  # well beyond the 5 m gap, so the dog counts
    np.testing.assert_allclose(sheep.dog_push(to_dogs, dist, r_s), [[0.6, 0.8]])


def test_several_dogs_push_as_one_unit_vector_from_their_mean_direction() -> None:
    # Two equal pushes above/below +x cancel the y parts; a third dog is out of range.
    near_a = np.array([3.0, 4.0])
    near_b = np.array([3.0, -4.0])
    far = np.array([-500.0, 0.0])
    to_dogs = np.stack([near_a, near_b, far])[None, :, :]  # shape (1 sheep, 3 dogs, 2)
    dist = np.linalg.norm(to_dogs, axis=2)
    r_s = 65.0
    np.testing.assert_allclose(sheep.dog_push(to_dogs, dist, r_s), [[1.0, 0.0]], atol=ANGLE_TOL)
