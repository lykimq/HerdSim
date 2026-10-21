"""Start layouts, dog start arcs and the task geometry."""

from __future__ import annotations

from dataclasses import replace

import numpy as np
import pytest

from services.cells import Cell, Group, cell_config
from sim.core.world.layouts import (
    layout_extent,
    place_dogs,
    place_flock,
    split_centres,
)
from sim.plugins.metrics.flock import fragmentation
from sim.plugins.metrics.view import TickView
from tests.helpers import config_for, make_state, protocol_with


@pytest.mark.parametrize("n", [5, 50, 200, 400])
def test_split_clusters_start_apart(n):
    cfg = config_for(n=n, layout="split", flock_radius=8.0)
    sheep = place_flock(cfg, np.random.default_rng(1))
    k = 2 if n < 12 else 3
    view = TickView(make_state(sheep, [[0.0, 0.0]]), cfg)
    assert fragmentation(view) <= (np.ceil(n / k) / n) + 1e-9


def test_compact_start_is_inside_the_field_and_outside_the_goal():
    cfg = config_for(n=400, flock_radius=12.0)
    sheep = place_flock(cfg, np.random.default_rng(2))
    assert sheep.shape == (400, 2)
    assert np.all(sheep > 0.0)
    assert np.all(sheep[:, 0] < cfg["world_width"]) and np.all(sheep[:, 1] < cfg["world_height"])
    assert np.all(np.linalg.norm(sheep - cfg["goal_center"], axis=1) > cfg["goal_radius"])


def test_outliers_start_beyond_the_lost_radius():
    cfg = config_for(n=100, layout="outlier_rich", flock_radius=9.0)
    sheep = place_flock(cfg, np.random.default_rng(3))
    center = np.asarray(cfg["flock_center"])
    beyond = np.linalg.norm(sheep - center, axis=1) > cfg["lost_radius"]
    assert beyond.sum() >= round(cfg["outlier_fraction"] * 100)


def test_dogs_start_on_arcs_behind_the_flock():
    cfg = config_for(d=128, flock_radius=9.0, settings={"dog_start_spacing": 5.0})
    center = np.asarray(cfg["flock_center"])
    back = center - np.asarray(cfg["goal_center"])
    back /= np.linalg.norm(back)
    dogs = place_dogs(cfg)
    assert dogs.shape == (128, 2)
    offsets = dogs - center
    assert np.all(offsets @ back >= -1e-9)  # on the side away from the goal
    reach = np.linalg.norm(offsets, axis=1)
    assert reach.min() == pytest.approx(layout_extent(cfg) + cfg["dog_start_gap"])
    assert reach.max() < layout_extent(cfg) + 65.0  # within the sheep reaction distance
    gaps = np.linalg.norm(dogs[:, None] - dogs[None], axis=2)[np.triu_indices(128, k=1)]
    # Full arcs: neighbours at least one spacing apart along the arc (the chord is shorter
    # by under 0.01).
    assert gaps.min() >= 0.99 * cfg["dog_start_spacing"]


@pytest.mark.parametrize("d", [2, 3, 4, 8])
def test_a_few_dogs_spread_over_the_whole_half_circle(d):
    """Each added dog starts at its own station: the centres of d equal sectors of the half
    circle behind the flock, not a short arc of neighbours."""
    cfg = config_for(d=d, flock_radius=9.0)
    center = np.asarray(cfg["flock_center"])
    back = center - np.asarray(cfg["goal_center"])
    rel = place_dogs(cfg) - center
    angles = np.sort(np.arctan2(back[0] * rel[:, 1] - back[1] * rel[:, 0], rel @ back))
    np.testing.assert_allclose(angles, -np.pi / 2 + np.pi * (np.arange(d) + 0.5) / d)


@pytest.mark.parametrize("start", ["arcs", "ring", "handler"])
def test_every_start_puts_one_dog_straight_behind_the_flock(start):
    cfg = config_for(d=1, flock_radius=9.0, settings={"dog_start": start})
    dog = place_dogs(cfg)[0]
    assert dog[1] == pytest.approx(cfg["flock_center"][1])
    assert dog[0] < cfg["flock_center"][0]  # the goal lies at +x


def test_ring_spreads_dogs_evenly_round_the_flock_goal_side_included():
    cfg = config_for(d=8, flock_radius=9.0, settings={"dog_start": "ring"})
    centre = np.asarray(cfg["flock_center"])
    rel = place_dogs(cfg) - centre
    np.testing.assert_allclose(np.linalg.norm(rel, axis=1), np.linalg.norm(rel[0]))
    assert (rel[:, 0] > 0).any()  # some dogs start on the goal side
    angles = np.sort(
        np.mod(np.arctan2(rel[:, 1], rel[:, 0]) - np.arctan2(rel[0, 1], rel[0, 0]), 2 * np.pi)
    )
    np.testing.assert_allclose(angles, 2 * np.pi * np.arange(8) / 8, atol=1e-9)


def test_ring_opens_a_second_circle_only_when_the_first_is_full():
    cfg = config_for(d=60, flock_radius=9.0, settings={"dog_start": "ring"})
    reach = np.linalg.norm(place_dogs(cfg) - np.asarray(cfg["flock_center"]), axis=1)
    first = int(2 * np.pi * reach.min() / cfg["dog_start_spacing"])
    assert (np.isclose(reach, reach.min())).sum() == min(60, first)


def test_handler_puts_every_dog_at_one_point_at_the_first_arc_radius():
    arcs = config_for(d=12, flock_radius=9.0)
    handler = config_for(d=12, flock_radius=9.0, settings={"dog_start": "handler"})
    dogs = place_dogs(handler)
    assert dogs.shape == (12, 2)
    np.testing.assert_allclose(dogs, np.tile(dogs[0], (12, 1)))
    centre = np.asarray(handler["flock_center"])
    radius = np.linalg.norm(place_dogs(arcs) - centre, axis=1).min()
    assert np.linalg.norm(dogs[0] - centre) == pytest.approx(radius)


def test_an_unknown_dog_start_is_refused():
    with pytest.raises(ValueError, match="dog_start"):
        config_for(settings={"dog_start": "line"})


def test_a_single_dog_starts_on_the_drive_axis():
    cfg = config_for(d=1, flock_radius=9.0)
    dog = place_dogs(cfg)[0]
    assert dog[1] == pytest.approx(cfg["flock_center"][1])
    farthest_sheep = 3.0 * cfg["compact_spread"] * 9.0  # the 3 sigma cut
    assert dog[0] == pytest.approx(cfg["flock_center"][0] - farthest_sheep - cfg["dog_start_gap"])


def test_drive_distance_scales_with_the_flock_radius():
    for radius in (9.0, 15.0, 18.0):
        cfg = config_for(n=100, flock_radius=radius)
        drive = cfg["goal_center"][0] - cfg["flock_center"][0]
        assert drive == pytest.approx(13.0 * radius)
        assert cfg["goal_radius"] == pytest.approx(1.9 * radius)


def test_tiny_flocks_still_drive_the_minimum_distance():
    cfg = config_for(n=5, flock_radius=3.0)
    assert cfg["goal_center"][0] - cfg["flock_center"][0] == pytest.approx(80.0)


def test_a_zero_drive_multiple_is_refused():
    """Its sign is the drive direction, and 0 has none (it once put the goal outside the field)."""
    with pytest.raises(ValueError, match="must not be 0"):
        config_for(settings={"drive_distance_multiple": 0.0})


def test_a_nonpositive_start_spacing_is_refused():
    with pytest.raises(ValueError, match="dog_start_spacing"):
        config_for(settings={"dog_start_spacing": 0.0})


def test_mirrored_drive_is_the_field_reflected():
    right = config_for(n=100, flock_radius=9.0)
    left = config_for(n=100, flock_radius=9.0, settings={"drive_distance_multiple": -13.0})
    assert left["world_width"] == right["world_width"]
    assert left["flock_center"][0] == pytest.approx(right["world_width"] - right["flock_center"][0])
    assert left["goal_center"][0] == pytest.approx(right["world_width"] - right["goal_center"][0])


@pytest.mark.parametrize("n", [5, 100])
def test_mirrored_drive_mirrors_the_split_clusters(n):
    """The cluster centres of the mirrored run are the x-reflection of the normal ones."""
    right = config_for(n=n, layout="split", flock_radius=9.0)
    left = config_for(
        n=n, layout="split", flock_radius=9.0, settings={"drive_distance_multiple": -13.0}
    )
    reflected = split_centres(right) * [-1.0, 1.0] + [right["world_width"], 0.0]
    order = np.lexsort((reflected[:, 1], reflected[:, 0]))
    mirrored = split_centres(left)
    np.testing.assert_allclose(
        mirrored[np.lexsort((mirrored[:, 1], mirrored[:, 0]))], reflected[order]
    )
    # Centres are symmetric about the drive axis, with one straight behind the
    # flock (three clusters) or none on the axis (two).
    offsets = split_centres(right) - np.asarray(right["flock_center"])
    assert sorted(np.round(offsets[:, 1], 9)) == sorted(np.round(-offsets[:, 1], 9))
    assert np.sum(np.abs(offsets[:, 1]) < 1e-9) == (1 if n >= 12 else 0)
    if n >= 12:
        assert offsets[np.abs(offsets[:, 1]) < 1e-9][0, 0] < 0.0  # behind, away from the goal


@pytest.mark.parametrize(
    ("layout", "n", "d", "radius"),
    [
        ("compact", 5, 1, 3.0),
        ("wide", 100, 35, 9.0),
        ("split", 400, 35, 11.6),
        ("outlier_rich", 400, 128, 11.6),
        ("wide", 1600, 128, 27.0),
        ("wide", 3200, 128, 49.0),
        ("compact", 3200, 400, 49.0),
    ],
)
def test_field_holds_flock_dogs_and_goal_with_clearance(layout, n, d, radius):
    cfg = config_for(n=n, d=d, layout=layout, flock_radius=radius)
    w, h, clearance = cfg["world_width"], cfg["world_height"], cfg["field_clearance"]
    goal, goal_radius = np.asarray(cfg["goal_center"]), cfg["goal_radius"]
    dogs = place_dogs(cfg)
    sheep = place_flock(cfg, np.random.default_rng(4))
    for points, slack in ((dogs, clearance), (sheep, 1.0)):
        assert points[:, 0].min() >= slack - 1e-9 and points[:, 0].max() <= w - slack + 1e-9
        assert points[:, 1].min() >= slack - 1e-9 and points[:, 1].max() <= h - slack + 1e-9
    assert goal[0] + goal_radius <= w - clearance + 1e-9
    assert clearance - 1e-9 <= goal[1] - goal_radius
    assert goal[1] + goal_radius <= h - clearance + 1e-9


def test_all_cells_of_a_protocol_at_one_n_share_the_field():
    protocol = protocol_with(settings={})
    protocol = replace(protocol, layouts=("compact", "wide"), shepherd_counts=(1, 8, 35))
    sizes = {
        (cfg["world_width"], cfg["world_height"], cfg["flock_center"][0])
        for layout in protocol.layouts
        for d in protocol.shepherd_counts
        for cfg in [cell_config(protocol, Cell(Group("strombom_multi", layout, (), 100), d), 9.0)]
    }
    assert len(sizes) == 1


def test_field_grows_with_n_and_dog_count():
    small = config_for(n=100, d=8, flock_radius=9.0)
    larger_n = config_for(n=1600, d=8, flock_radius=15.0)
    more_dogs = config_for(n=100, d=128, flock_radius=9.0)
    assert larger_n["world_width"] > small["world_width"]
    assert more_dogs["world_height"] >= small["world_height"]


def test_no_dogs_means_no_start_positions():
    cfg = config_for(d=0, flock_radius=9.0)
    assert place_dogs(cfg).shape == (0, 2)


@pytest.mark.parametrize(("n", "radius"), [(25, 7.0), (100, 9.0), (400, 11.6), (1600, 23.0)])
def test_scattered_layouts_make_strombom_collect_and_compact_does_not(n, radius):
    """The point of the layouts: a sheep beyond r_a N^(2/3) from the flock centre means collect."""
    threshold = 2.0 * n ** (2.0 / 3.0)

    def collecting(layout):
        hits = 0
        for seed in range(30):
            cfg = config_for(n=n, d=1, layout=layout, flock_radius=radius)
            sheep = place_flock(cfg, np.random.default_rng(seed))
            hits += np.linalg.norm(sheep - sheep.mean(axis=0), axis=1).max() > threshold
        return hits / 30

    assert collecting("compact") == 0.0
    for layout in ("wide", "split", "outlier_rich"):
        assert collecting(layout) >= 0.95, layout


@pytest.mark.parametrize("layout", ["wide", "split", "outlier_rich"])
def test_goal_lies_beyond_every_start_sheep(layout):
    cfg = config_for(n=400, layout=layout, flock_radius=11.6)
    sheep = place_flock(cfg, np.random.default_rng(5))
    to_goal = np.linalg.norm(sheep - np.asarray(cfg["goal_center"]), axis=1)
    assert to_goal.min() > cfg["goal_radius"]


def test_split_clusters_start_as_separate_groups_at_every_size():
    for n in (25, 100, 400, 1600):
        cfg = config_for(n=n, layout="split", flock_radius=9.0)
        sheep = place_flock(cfg, np.random.default_rng(6))
        view = TickView(make_state(sheep, [[0.0, 0.0]]), cfg)
        assert fragmentation(view) <= 0.4, n  # three clusters, none holds more than 40%


@pytest.mark.parametrize("layout", ["compact", "wide", "split", "outlier_rich"])
def test_no_sheep_starts_beyond_the_layout_extent(layout):
    """layout_extent is exact: every Gaussian is cut at 3 sigma, the outlier ring ends at far."""
    cfg = config_for(n=1600, layout=layout, flock_radius=23.0)
    sheep = place_flock(cfg, np.random.default_rng(7))
    reach = np.linalg.norm(sheep - np.asarray(cfg["flock_center"]), axis=1).max()
    assert reach <= layout_extent(cfg)


@pytest.mark.parametrize("layout", ["compact", "wide", "split", "outlier_rich"])
@pytest.mark.parametrize(("n", "d"), [(100, 4), (400, 4), (400, 128)])
def test_dogs_start_behind_every_sheep(layout, n, d):
    """The first arc is dog_start_gap beyond the farthest possible sheep on every layout."""
    cfg = config_for(n=n, d=d, layout=layout, flock_radius={100: 9.0, 400: 11.4}[n])
    sheep = place_flock(cfg, np.random.default_rng(8))
    dogs = place_dogs(cfg)
    gaps = np.linalg.norm(sheep[:, None] - dogs[None], axis=2)
    assert gaps.min() >= cfg["dog_start_gap"] - 1e-9
    center = np.asarray(cfg["flock_center"])
    toward = np.asarray(cfg["goal_center"]) - center
    assert np.all((dogs - center) @ toward <= 1e-9)  # no dog starts on the goal side


def test_success_fraction_counts_the_share_of_sheep_inside():
    from sim.core.world.arena import GoalZone

    inside, outside = np.zeros((99, 2)), np.array([[50.0, 0.0]])
    strict = GoalZone(np.zeros(2), 5.0)
    relaxed = GoalZone(np.zeros(2), 5.0, required_fraction=0.99)
    assert not strict.reached(np.vstack([inside, outside]))
    assert relaxed.reached(np.vstack([inside, outside]))  # 99 of 100
    assert not relaxed.reached(np.vstack([inside[:98], outside, outside]))  # 98 of 100
    assert strict.reached(inside)


def test_a_relaxed_success_rule_never_finishes_later_than_the_strict_one():
    from sim.core.simulation_runner import run_trial

    common = {"n": 100, "d": 3, "layout": "wide", "ticks": 900, "flock_radius": 9.08}
    strict = run_trial(config_for(**common), 2026)
    relaxed = run_trial(config_for(**common, settings={"success_fraction": 0.99}), 2026)
    assert relaxed.success and relaxed.total_ticks <= (
        strict.total_ticks if strict.success else 900
    )


def test_success_fraction_outside_zero_to_one_is_refused():
    for bad in (0.0, 1.5):
        with pytest.raises(ValueError, match="success_fraction"):
            config_for(settings={"success_fraction": bad})
