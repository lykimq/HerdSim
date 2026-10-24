"""Strombom 2014 rules: the shepherd decision, the multi-dog layer on top, and the sheep heading."""

from __future__ import annotations

import numpy as np
import pytest

from sim.core.simulation_runner import initial_state, run_trial
from sim.core.vectors import behind, unit
from sim.methods.strombom import sheep
from sim.methods.strombom.config import resolve_n_neighbors
from sim.methods.strombom.heuristics import (
    COLLECT,
    DRIVE,
    decide,
    drive_point,
    radius_of,
    step_toward,
)
from sim.plugins.dogs import independent
from sim.plugins.dogs.collect_drive_multi import drive_front, team_targets
from tests.helpers import config_for

CONFIG = config_for("strombom_multi", n=10, d=1)
R_A = CONFIG["r_a"]
GOAL = np.array([200.0, 0.0])


def _cfg(n_sheep: int, **overrides) -> dict:
    """CONFIG for a flock of ``n_sheep``: the rule uses the true N, not the sheep passed in."""
    return {**CONFIG, "n_sheep": n_sheep, **overrides}


def _tight_flock(n: int, center=(0.0, 0.0)) -> np.ndarray:
    rng = np.random.default_rng(1)
    return np.asarray(center) + rng.normal(0.0, 0.5, size=(n, 2))


def test_drive_target_is_paper_pd_behind_flock():
    flock = _tight_flock(25)
    d = decide(flock, GOAL, _cfg(25))
    assert d.mode == DRIVE
    centroid = flock.mean(axis=0)
    expected = centroid + unit(centroid - GOAL) * R_A * np.sqrt(25)
    np.testing.assert_allclose(d.target, expected)


def test_collect_target_is_paper_pc_behind_furthest():
    flock = np.vstack([_tight_flock(9), [[30.0, 0.0]]])
    d = decide(flock, GOAL, _cfg(10))
    assert d.mode == COLLECT
    centroid = flock.mean(axis=0)
    np.testing.assert_allclose(d.target, flock[-1] + unit(flock[-1] - centroid) * R_A)


def test_local_dog_uses_the_true_flock_size():
    """Seeing 10 of 400 sheep: f(N) and Pd use N = 400, the GCM the 10 seen sheep."""
    seen = _tight_flock(10)
    d = decide(seen, GOAL, _cfg(400))
    assert d.mode == DRIVE
    centroid = seen.mean(axis=0)
    assert np.linalg.norm(d.target - centroid) == pytest.approx(R_A * np.sqrt(400))


def test_decision_mirrors_with_the_goal():
    flock = _tight_flock(25)
    mirror = np.array([-1.0, 1.0])
    a = decide(flock, GOAL, _cfg(25))
    b = decide(flock * mirror, GOAL * mirror, _cfg(25))
    np.testing.assert_allclose(b.target, a.target * mirror)


def _behind(n_dogs: int, flock: np.ndarray) -> np.ndarray:
    """Dogs on a line behind the flock (away from the goal), spread sideways."""
    centroid = flock.mean(axis=0)
    return centroid + np.column_stack([np.full(n_dogs, -40.0), np.linspace(-20, 20, n_dogs)])


def _angle(points: np.ndarray, centroid: np.ndarray, arm: np.ndarray) -> np.ndarray:
    rel = points - centroid
    return np.arctan2(arm[0] * rel[:, 1] - arm[1] * rel[:, 0], rel @ arm)


@pytest.mark.parametrize("flock", [_tight_flock(25), np.vstack([_tight_flock(9), [[30.0, 0.0]]])])
def test_one_dog_takes_the_paper_target(flock):
    cfg = _cfg(flock.shape[0])
    d = decide(flock, GOAL, cfg)
    np.testing.assert_allclose(team_targets(flock, GOAL, _behind(1, flock), cfg)[0], d.target)


def test_driving_point_dogs_cover_the_flock_width_not_one_point():
    """Each added dog takes its own stretch of the flock's back edge; the middle is Pd."""
    flock = _tight_flock(25) * 6.0  # radius about 4
    cfg = _cfg(25)
    d = decide(flock, GOAL, cfg)
    slots = team_targets(flock, GOAL, _behind(5, flock), cfg)
    radius = np.linalg.norm(d.target - d.centroid)
    np.testing.assert_allclose(np.linalg.norm(slots - d.centroid, axis=1), radius)
    half = np.arcsin(radius_of(flock, d.centroid) / radius)
    angles = np.sort(_angle(slots, d.centroid, d.target - d.centroid))
    np.testing.assert_allclose(angles, np.linspace(-half, half, 5), atol=1e-12)
    assert len(np.unique(np.round(slots, 9), axis=0)) == 5  # five distinct jobs


def test_drive_front_stays_behind_the_flock_at_the_drive_distance():
    centroid, target = np.zeros(2), np.array([-10.0, 0.0])  # goal at +x
    many = drive_front(centroid, target, 2.0, 40)
    rel = many - centroid
    np.testing.assert_allclose(np.linalg.norm(rel, axis=1), 10.0)
    assert np.all(rel @ unit(target - centroid) > -1e-9)  # never on the goal side
    half = np.arcsin(2.0 / 10.0)
    angles = np.sort(_angle(many, centroid, target))
    np.testing.assert_allclose(angles, np.linspace(-half, half, 40), atol=1e-12)


def test_collecting_dogs_take_distinct_outliers_nearest_first_and_the_rest_drive_the_core():
    core = _tight_flock(20)
    flock = np.vstack([core, [[0.0, 60.0], [0.0, -60.0]]])  # two outliers, above and below
    cfg = _cfg(22)
    dogs = np.array([[-40.0, -50.0], [-40.0, 50.0], [-40.0, 0.0], [-40.0, 5.0]])
    targets = team_targets(flock, GOAL, dogs, cfg)
    centroid = flock.mean(axis=0)
    np.testing.assert_allclose(targets[0], behind(flock[-1], centroid, R_A))  # lower dog: lower
    np.testing.assert_allclose(targets[1], behind(flock[-2], centroid, R_A))  # upper dog: upper
    core_centroid = core.mean(axis=0)
    drive_radius = np.linalg.norm(drive_point(core, GOAL, cfg) - core_centroid)
    for t in targets[2:]:  # the two dogs without an outlier drive the core from behind
        assert np.linalg.norm(t - core_centroid) == pytest.approx(drive_radius)
        assert t[0] < core_centroid[0]
    assert not np.allclose(targets[2], targets[3])


def test_dogs_keep_their_side_when_matched_to_drive_slots():
    flock = _tight_flock(25) * 6.0
    cfg = _cfg(25)
    dogs = _behind(4, flock)[::-1]  # dog 0 is the topmost
    targets = team_targets(flock, GOAL, dogs, cfg)
    assert np.all(np.diff(targets[:, 1]) < 0)  # top dog takes the top slot, and so on


def test_dog_stops_near_sheep_and_always_walks_delta_s():
    sheep_pos = np.array([[0.0, 0.0]])
    near = step_toward(
        np.array([3.0 * R_A - 0.1, 0.0]), np.array([50.0, 0.0]), sheep_pos, CONFIG, 0.3
    )
    assert np.all(near == 0.0)
    far = step_toward(np.array([20.0, 0.0]), np.array([50.0, 0.0]), sheep_pos, CONFIG, 0.3)
    assert np.linalg.norm(far) == pytest.approx(CONFIG["shepherd_speed"])
    close = step_toward(np.array([20.0, 0.0]), np.array([20.1, 0.0]), sheep_pos, CONFIG, 0.3)
    assert np.linalg.norm(close) == pytest.approx(CONFIG["shepherd_speed"])  # no overshoot cap


def test_n_neighbors_forms():
    assert resolve_n_neighbors(-1, 50) == 49
    assert resolve_n_neighbors(7, 50) == 7
    assert resolve_n_neighbors("0.25N", 50) == 13
    with pytest.raises(ValueError):
        resolve_n_neighbors(7, 5)  # more neighbours than the flock has: an error, not a clip
    with pytest.raises(ValueError):
        resolve_n_neighbors("0.25", 50)


# --- sheep heading: vectorised step against a per-sheep reading of eq. 4.1 to 4.3


def _reference(positions, prev, dogs, draws, cfg, k):
    """Per-sheep loop written straight from the paper, on the same random draws."""
    out = np.zeros_like(positions)
    for i, x in enumerate(positions):
        dist = np.linalg.norm(x - dogs, axis=1)
        if not np.any(dist < cfg["r_s"]):
            if draws.graze_move[i] < cfg["graze_move_prob"]:
                a = draws.graze_angle[i]
                out[i] = np.array([np.cos(a), np.sin(a)]) * cfg["sheep_speed"]
            continue
        others = np.delete(np.arange(len(positions)), i)
        order = others[np.argsort(np.linalg.norm(positions[others] - x, axis=1))]
        lcm = positions[order[:k]].mean(axis=0) if k > 0 else x
        rep = sum(
            (
                unit(x - positions[j])
                for j in others
                if 0 < np.linalg.norm(x - positions[j]) < cfg["r_a"]
            ),
            np.zeros(2),
        )
        push = sum(
            (unit(x - dog) for dog in dogs if np.linalg.norm(x - dog) < cfg["r_s"]), np.zeros(2)
        )
        push = unit(push)
        a = draws.noise_angle[i]
        heading = (
            cfg["inertia"] * unit(prev[i])
            + cfg["c"] * unit(lcm - x)
            + cfg["rho_a"] * unit(rep)
            + cfg["rs_weight"] * push
            + cfg["noise_strength"] * np.array([np.cos(a), np.sin(a)])
        )
        out[i] = unit(heading) * cfg["sheep_speed"]
    return out


@pytest.mark.parametrize("r_a", [2.0, 1.0])  # figure 5 of the paper uses r_a = 1 with rho_a = 2
@pytest.mark.parametrize("k", [29, 7])
@pytest.mark.parametrize("n_dogs", [1, 3])
def test_vectorised_sheep_match_reference(k, n_dogs, r_a):
    rng = np.random.default_rng(3)
    positions = rng.normal(0.0, 3.0, size=(30, 2))
    positions[-1] = [200.0, 200.0]  # one grazer, far from every dog
    prev = rng.normal(0.0, 1.0, size=(30, 2))
    dogs = rng.normal(0.0, 1.0, size=(n_dogs, 2)) + [8.0, 0.0]
    cfg = {**CONFIG, "r_a": r_a}
    draws = sheep.draw(np.random.default_rng(4), 30)
    np.testing.assert_allclose(
        sheep.velocities(positions, prev, dogs, draws, cfg, k),
        _reference(positions, prev, dogs, draws, cfg, k),
        atol=1e-12,
    )


def test_sheep_at_exactly_r_s_grazes():
    positions = np.array([[0.0, 0.0], [0.0, 1.0]])  # the second sheep is beyond r_s either way
    draws = sheep.SheepDraws(
        graze_move=np.ones(2), graze_angle=np.zeros(2), noise_angle=np.zeros(2)
    )
    still = np.zeros((2, 2))
    at_edge = np.array([[CONFIG["r_s"], 0.0]])
    assert np.all(sheep.velocities(positions, still, at_edge, draws, CONFIG, 1) == 0.0)
    inside = at_edge - [1e-9, 0.0]
    assert np.any(sheep.velocities(positions, still, inside, draws, CONFIG, 1) != 0.0)


def test_one_dog_push_is_the_paper_unit_vector():
    to_dog = np.array([[[3.0, 4.0]]])
    dist = np.linalg.norm(to_dog, axis=2)
    np.testing.assert_allclose(sheep.dog_push(to_dog, dist, 65.0), [[0.6, 0.8]])


def test_several_dogs_push_as_one_unit_vector_from_their_mean_direction():
    to_dogs = np.array([[[3.0, 4.0], [3.0, -4.0], [-500.0, 0.0]]])  # the third is out of reach
    dist = np.linalg.norm(to_dogs, axis=2)
    np.testing.assert_allclose(sheep.dog_push(to_dogs, dist, 65.0), [[1.0, 0.0]], atol=1e-12)


def test_one_independent_dog_is_the_paper_shepherd_trial():
    multi = run_trial(config_for(n=60, d=1, layout="wide", ticks=200), 2026)
    alone = run_trial(config_for("independent", n=60, d=1, layout="wide", ticks=200), 2026)
    assert alone.total_ticks == multi.total_ticks
    np.testing.assert_array_equal(alone.history.to_numpy(), multi.history.to_numpy())


def test_independent_dogs_all_take_the_one_paper_target():
    config = config_for("independent", n=60, d=4, layout="wide")
    state = initial_state(config, 2026)
    aims = independent.targets(state, config)
    paper = decide(state.sheep_positions, state.world.goal.center, config).target
    assert aims.shape == (4, 2)
    np.testing.assert_array_equal(aims, np.tile(paper, (4, 1)))


def test_capped_drive_offset_stays_within_reach_and_is_off_by_default():
    flock = np.array([[0.0, 0.0], [2.0, 0.0], [0.0, 2.0]])
    goal = np.array([100.0, 0.0])
    paper = config_for(n=1600, d=1)  # r_a sqrt(N) = 80, beyond r_s = 65
    capped = {**paper, "drive_offset_cap": 63.0}
    centre = flock.mean(axis=0)
    assert np.linalg.norm(drive_point(flock, goal, paper) - centre) == pytest.approx(80.0)
    assert np.linalg.norm(drive_point(flock, goal, capped) - centre) == pytest.approx(63.0)


def test_spread_jobs_skip_outliers_near_one_already_taken():
    from sim.plugins.dogs.collect_drive_multi import spread_jobs

    flock = np.array([[100.0, 0.0], [99.0, 1.0], [-90.0, 0.0], [0.0, 80.0]])
    outliers = np.array([0, 1, 2, 3])  # farthest first
    assert spread_jobs(flock, outliers, 2, 0.0).tolist() == [0, 1]  # the team rule
    assert spread_jobs(flock, outliers, 2, 50.0).tolist() == [0, 2]  # 1 is next to 0
    assert spread_jobs(flock, outliers, 4, 50.0).tolist() == [0, 2, 3, 1]  # filled in at the end
