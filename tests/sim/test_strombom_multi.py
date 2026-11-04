"""strombom_multi: the multi-dog layer on top of the Strombom 2014 rules."""

from __future__ import annotations

import numpy as np
import pytest

from sim.strombom import sheep
from sim.strombom.params import resolve_n_neighbors
from sim.strombom.shepherd import DRIVE, decide, drive_point, radius_of
from sim.strombom.team import drive_front, team_targets
from sim.vectors import behind, unit
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
DOG_BEHIND_X = -40.0  # dogs start this far left of the flock centre
DOG_SPREAD_Y = 20.0  # half-width of the dog line along y
WIDE_SCALE = 6.0  # stretch a tight flock so drive slots have room to fan out


# --- helpers -----------------------------------------------------------------


def wide_flock(n: int = 25) -> np.ndarray:
    """Tight flock scaled up so the back-edge drive arc is wide enough to check."""
    return tight_flock(n) * WIDE_SCALE


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


# --- local view and settings -------------------------------------------------


def test_local_dog_uses_the_true_flock_size() -> None:
    """Seeing 10 of 400 sheep: f(N) and Pd use N = 400, the GCM the 10 seen sheep."""
    seen = tight_flock(10)
    decision = decide(seen, GOAL, cfg(400))
    assert decision.mode == DRIVE
    centroid = seen.mean(axis=0)
    assert np.linalg.norm(decision.target - centroid) == pytest.approx(R_A * np.sqrt(400))


def test_n_neighbors_forms() -> None:
    n_sheep = 50
    assert resolve_n_neighbors(-1, n_sheep) == n_sheep - 1  # "all others"
    assert resolve_n_neighbors(7, n_sheep) == 7
    assert resolve_n_neighbors("0.25N", n_sheep) == 13  # round(0.25 * 50)
    with pytest.raises(ValueError):
        resolve_n_neighbors(7, 5)  # k must be < N
    with pytest.raises(ValueError):
        resolve_n_neighbors("0.25", n_sheep)  # fraction form needs the N suffix


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


def test_collecting_dogs_take_distinct_outliers_by_least_walk_and_the_rest_drive_the_core() -> None:
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

    # Least total walk: dog at y=-50 takes the lower outlier, dog at y=50 the upper.
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


def test_several_dogs_push_as_one_unit_vector_from_their_mean_direction() -> None:
    # Two equal pushes above/below +x cancel the y parts; a third dog is out of range.
    near_a = np.array([3.0, 4.0])
    near_b = np.array([3.0, -4.0])
    far = np.array([-500.0, 0.0])
    to_dogs = np.stack([near_a, near_b, far])[None, :, :]  # shape (1 sheep, 3 dogs, 2)
    dist = np.linalg.norm(to_dogs, axis=2)
    r_s = 65.0
    np.testing.assert_allclose(sheep.dog_push(to_dogs, dist, r_s), [[1.0, 0.0]], atol=ANGLE_TOL)
