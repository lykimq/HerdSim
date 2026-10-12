"""Scaling-related metrics, X0 layouts, and multi-dog observation behaviour."""

from __future__ import annotations

import numpy as np
import pytest
from core.world.layouts import generate_initial_positions, normalize_layout
from plugins.metrics.cohesion import CohesionMetric
from plugins.metrics.extent import ExtentMetric
from plugins.metrics.fragmentation import FragmentationMetric
from plugins.metrics.mean_spread import MeanSpreadMetric
from plugins.metrics.outlier_count import OutlierCountMetric
from plugins.metrics.registry import metric_registry
from plugins.metrics.shepherd_coverage import ShepherdCoverageMetric
from plugins.metrics.shepherd_interference import ShepherdInterferenceMetric

from tests.helpers import make_state, make_world


def test_scaling_metrics_registered():
    ids = {m["id"] for m in metric_registry.list_all()}
    for needed in (
        "mean_spread",
        "extent",
        "perimeter",
        "hull_area",
        "flock_density",
        "aspect_ratio",
        "i_dir",
        "coverage",
    ):
        assert needed in ids


def test_mean_spread_and_extent_formulas():
    sheep = [[0.0, 0.0], [2.0, 0.0], [0.0, 2.0], [2.0, 2.0]]
    state = make_state(sheep, [[10.0, 10.0]])
    distances = np.full(4, np.sqrt(2.0))
    assert MeanSpreadMetric().compute(state) == pytest.approx(float(np.var(distances)))
    assert ExtentMetric().compute(state) == pytest.approx(np.sqrt(2.0))


def test_hull_shape_metrics_on_unit_square():
    from plugins.metrics.aspect_ratio import AspectRatioMetric
    from plugins.metrics.flock_density import FlockDensityMetric
    from plugins.metrics.hull_area import HullAreaMetric
    from plugins.metrics.perimeter import PerimeterMetric

    # Axis-aligned unit square: perimeter 4, area 1, aspect ~1.
    sheep = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]
    state = make_state(sheep, [[10.0, 10.0]])
    assert PerimeterMetric().compute(state) == pytest.approx(4.0)
    assert HullAreaMetric().compute(state) == pytest.approx(1.0)
    assert FlockDensityMetric().compute(state) == pytest.approx(4.0)
    assert AspectRatioMetric().compute(state) == pytest.approx(1.0, abs=1e-6)

    # Collinear: no area, positive perimeter, elongated aspect.
    line = make_state([[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]], [[0.0, 0.0]])
    assert HullAreaMetric().compute(line) == pytest.approx(0.0)
    assert FlockDensityMetric().compute(line) == pytest.approx(0.0)
    assert PerimeterMetric().compute(line) == pytest.approx(4.0)
    assert AspectRatioMetric().compute(line) > 10.0


def test_interference_zero_when_aligned_or_stationary():
    state = make_state([[0.0, 0.0], [1.0, 0.0]], [[0.0, 0.0], [5.0, 0.0]])
    state.shepherd_velocities[:] = [[1.0, 0.0], [2.0, 0.0]]
    assert ShepherdInterferenceMetric().compute(state) == pytest.approx(0.0)

    state.shepherd_velocities[:] = [[0.0, 0.0], [0.0, 0.0]]
    assert ShepherdInterferenceMetric().compute(state) == pytest.approx(0.0)

    state.shepherd_velocities[:] = [[1.0, 0.0], [-1.0, 0.0]]
    assert ShepherdInterferenceMetric().compute(state) == pytest.approx(1.0)


def test_coverage_uses_influence_radius():
    sheep = [[0.0, 0.0], [0.1, 0.0], [10.0, 0.0]]
    shepherds = [[10.0, 0.0]]
    missing = make_state(sheep, shepherds, metadata={"r_a": 2.0, "r_s": 2.0})
    assert np.isnan(ShepherdCoverageMetric().compute(missing))
    covered = make_state(sheep, shepherds, metadata={"influence_radius": 2.0, "r_a": 2.0})
    assert ShepherdCoverageMetric().compute(covered) == pytest.approx(1.0)


def test_normalize_layout():
    assert normalize_layout(" Wide ") == "wide"
    assert normalize_layout("compact") == "compact"


def test_x0_families_differ_on_target_metrics():
    rng = np.random.default_rng(0)
    center = np.array([75.0, 75.0])
    compact = generate_initial_positions(40, "compact", center, rng, spread=20.0)
    wide = generate_initial_positions(40, "wide", center, rng, spread=20.0)
    split = generate_initial_positions(
        40, "split", center, rng, spread=20.0, interaction_radius=5.0
    )
    outliers = generate_initial_positions(
        40, "outlier_rich", center, rng, spread=20.0, lost_threshold=15.0
    )

    def cohesion(pos):
        state = make_state(pos, [[0.0, 0.0]])
        return CohesionMetric().compute(state)

    def frag(pos):
        state = make_state(pos, [[0.0, 0.0]], metadata={"measurement_radius": 5.0})
        return FragmentationMetric().compute(state)

    def outliers_n(pos):
        state = make_state(pos, [[0.0, 0.0]], metadata={"r_a": 2.0})
        return OutlierCountMetric().compute(state)

    assert cohesion(wide) > cohesion(compact)
    assert frag(split) < frag(compact)
    assert outliers_n(outliers) > outliers_n(compact)


def test_drive_to_goal_uses_initial_layout():
    from plugins.scenarios.drive_to_goal import DriveToGoalScenario

    scenario = DriveToGoalScenario()
    rng = np.random.default_rng(1)
    cfg = {
        "n_sheep": 30,
        "n_shepherds": 1,
        "world_width": 150.0,
        "world_height": 150.0,
        "initial_spread": 20.0,
        "initial_layout": "split",
        "measurement_radius": 5.0,
        "r_a": 2.0,
    }
    sheep, dogs = scenario.initial_positions(cfg, rng)
    assert sheep.shape == (30, 2)
    assert dogs.shape == (1, 2)
    # Split should produce lower fragmentation than compact under same radius.
    frag_split = FragmentationMetric().compute(
        make_state(sheep, dogs, metadata={"measurement_radius": 5.0})
    )
    cfg["initial_layout"] = "compact"
    sheep_c, dogs_c = scenario.initial_positions(cfg, np.random.default_rng(1))
    frag_compact = FragmentationMetric().compute(
        make_state(sheep_c, dogs_c, metadata={"measurement_radius": 5.0})
    )
    assert frag_split < frag_compact


def test_x0_families_on_scaling_arena():
    center = np.array([250.0, 250.0])
    goal = np.array([370.0, 250.0])
    spread = 30.0
    world_width = 500.0
    world_height = 500.0
    goal_radius = 15.0
    rng = np.random.default_rng(0)
    compact = generate_initial_positions(
        50,
        "compact",
        center,
        rng,
        spread=spread,
        world_width=world_width,
        world_height=world_height,
        goal_center=goal,
        goal_radius=goal_radius,
    )
    wide = generate_initial_positions(
        50,
        "wide",
        center,
        rng,
        spread=spread,
        world_width=world_width,
        world_height=world_height,
        goal_center=goal,
        goal_radius=goal_radius,
    )
    split = generate_initial_positions(
        50,
        "split",
        center,
        rng,
        spread=spread,
        interaction_radius=5.0,
        world_width=world_width,
        world_height=world_height,
        goal_center=goal,
        goal_radius=goal_radius,
    )
    outliers = generate_initial_positions(
        50,
        "outlier_rich",
        center,
        rng,
        spread=spread,
        lost_threshold=2.0 * (50 ** (2.0 / 3.0)),
        world_width=world_width,
        world_height=world_height,
        goal_center=goal,
        goal_radius=goal_radius,
    )

    def _inside(pos: np.ndarray) -> None:
        assert np.all((pos[:, 0] >= 1.0) & (pos[:, 0] <= 499.0))
        assert np.all((pos[:, 1] >= 1.0) & (pos[:, 1] <= 499.0))
        assert np.all(np.linalg.norm(pos - goal, axis=1) > 15.0)

    for pos in (compact, wide, split, outliers):
        _inside(pos)

    def cohesion(pos):
        return CohesionMetric().compute(make_state(pos, [[250.0, 250.0]]))

    def frag(pos):
        return FragmentationMetric().compute(
            make_state(pos, [[250.0, 250.0]], metadata={"measurement_radius": 5.0})
        )

    def outliers_n(pos):
        return OutlierCountMetric().compute(
            make_state(pos, [[250.0, 250.0]], metadata={"r_a": 2.0})
        )

    assert cohesion(wide) > cohesion(compact)
    assert frag(split) < frag(compact)
    assert outliers_n(outliers) > outliers_n(compact)


def test_collect_drive_multi_uses_each_dogs_observation():
    from core.observation import ShepherdObservation
    from plugins.dogs.collect_drive_multi import CollectDriveMultiController

    seen = np.array([[50.0, 50.0], [51.0, 50.0], [50.0, 51.0], [51.0, 51.0]], dtype=float)
    hidden = np.array([[50.0, 130.0]], dtype=float)
    sheep = np.vstack([seen, hidden])
    dogs = np.array([[90.0, 50.0], [90.0, 80.0]], dtype=float)
    state = make_state(sheep, dogs, world=make_world(), seed=1)

    def _obs(index: int, positions: np.ndarray) -> ShepherdObservation:
        positions = np.asarray(positions, dtype=float).reshape(-1, 2)
        other = 1 - index
        return ShepherdObservation(
            shepherd_index=index,
            self_position=dogs[index],
            self_velocity=np.zeros(2),
            goal_center=np.array([15.0, 15.0]),
            sheep_positions=positions,
            sheep_velocities=np.zeros_like(positions),
            sheep_indices=np.arange(len(positions)),
            other_shepherd_positions=dogs[other : other + 1],
            other_shepherd_indices=np.array([other]),
        )

    ctrl = CollectDriveMultiController()
    cfg = {
        **ctrl.default_config,
        "noise_strength": 0.0,
        "n_shepherds": 2,
        "communication": "none",
    }
    none_obs = [_obs(0, seen), _obs(1, np.zeros((0, 2)))]
    none_state = ctrl.step(state, none_obs, cfg)
    assert np.linalg.norm(none_state.shepherd_velocities[0]) > 0
    assert np.allclose(none_state.shepherd_velocities[1], 0.0)
    assert none_state.metadata["herding_mode"] == "drive"

    cfg["communication"] = "global_shared"
    shared_state = ctrl.step(state, none_obs, cfg)
    assert np.linalg.norm(shared_state.shepherd_velocities[1]) > 0
    assert shared_state.metadata["herding_mode"] == "drive"


def test_collect_drive_multi_global_shared_unions_by_index():
    from core.observation import ShepherdObservation
    from plugins.dogs.collect_drive_multi import _sheep_for_dog, _union_sheep_positions

    dogs = np.array([[0.0, 0.0], [10.0, 0.0]], dtype=float)
    sheep_a = np.array([[1.0, 0.0], [2.0, 0.0]], dtype=float)
    sheep_b = np.array([[2.0, 0.0], [3.0, 0.0]], dtype=float)
    state = make_state(
        np.array([[1.0, 0.0], [2.0, 0.0], [3.0, 0.0]], dtype=float),
        dogs,
        world=make_world(),
        seed=0,
    )

    def _obs(index: int, positions: np.ndarray, indices: np.ndarray) -> ShepherdObservation:
        positions = np.asarray(positions, dtype=float).reshape(-1, 2)
        other = 1 - index
        return ShepherdObservation(
            shepherd_index=index,
            self_position=dogs[index],
            self_velocity=np.zeros(2),
            goal_center=np.array([15.0, 15.0]),
            sheep_positions=positions,
            sheep_velocities=np.zeros_like(positions),
            sheep_indices=np.asarray(indices, dtype=int),
            other_shepherd_positions=dogs[other : other + 1],
            other_shepherd_indices=np.array([other]),
        )

    observations = [
        _obs(0, sheep_a, np.array([0, 1])),
        _obs(1, sheep_b, np.array([1, 2])),
    ]
    unioned = _union_sheep_positions(observations)
    assert unioned.shape == (3, 2)

    shared = _sheep_for_dog(
        0, observations, state, {"communication": "global_shared", "sensing_range": 65.0}
    )
    assert shared.shape == (3, 2)

    # Overlapping full views must not inflate N to D*N.
    both_full = [
        _obs(0, sheep_a, np.array([0, 1])),
        _obs(1, sheep_a, np.array([0, 1])),
    ]
    assert _union_sheep_positions(both_full).shape == (2, 2)
