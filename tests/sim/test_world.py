"""Start layouts, dog starts and the task geometry that size every trial."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

import numpy as np
import pytest

from services.cells import Cell, Group, cell_config
from services.protocol import Protocol
from sim.drive_task.layouts import (
    goal_half_angle,
    layout_extent,
    place_boxes,
    place_dogs,
    place_flock,
)
from sim.drive_task.world import GoalZone
from sim.metrics.flock import fragmentation
from sim.metrics.view import TickView
from sim.trial import run_trial
from tests.helpers import config_for, make_state, protocol_with

METHOD = "strombom_multi"
LAYOUTS = ("compact", "wide", "split", "outlier_rich")
SCATTERED = ("wide", "split", "outlier_rich")

# Calibrated R_f used in a few placement checks (same values as the study table).
RF = {100: 9.0, 200: 10.47, 400: 11.4}

DRIVE_MULTIPLE = 13.0
GOAL_RADIUS_MULTIPLE = 1.9
MIN_DRIVE = 80.0
SHEEP_REACTION = 65.0  # r_s: first-arc dogs stay inside this of the flock edge
COLLECT_SEEDS = 30
EPS = 1e-9
SEED = 2026


# --- helpers -----------------------------------------------------------------


def behind_unit(cfg: dict[str, Any]) -> np.ndarray:
    """Unit vector from the goal through the flock centre (straight behind the flock)."""
    back = np.asarray(cfg["flock_center"]) - np.asarray(cfg["goal_center"])
    return back / np.linalg.norm(back)


def toward_goal_unit(cfg: dict[str, Any]) -> np.ndarray:
    return -behind_unit(cfg)


def flock_centre(cfg: dict[str, Any]) -> np.ndarray:
    return np.asarray(cfg["flock_center"])


def goal_centre(cfg: dict[str, Any]) -> np.ndarray:
    return np.asarray(cfg["goal_center"])


def signed_angles_from_behind(cfg: dict[str, Any], points: np.ndarray) -> np.ndarray:
    centre = flock_centre(cfg)
    back = behind_unit(cfg)
    rel = points - centre
    return np.arctan2(back[0] * rel[:, 1] - back[1] * rel[:, 0], rel @ back)


def sheep_at(cfg: dict[str, Any], seed: int) -> np.ndarray:
    return place_flock(cfg, np.random.default_rng(seed))


def drive_length(cfg: dict[str, Any]) -> float:
    return float(cfg["goal_center"][0] - cfg["flock_center"][0])


def collect_threshold(n_sheep: int) -> float:
    """Strombom collect radius: a sheep farther than this from the GCM triggers collect."""
    return 2.0 * n_sheep ** (2.0 / 3.0)


def farthest_from_gcm(sheep: np.ndarray) -> float:
    return float(np.linalg.norm(sheep - sheep.mean(axis=0), axis=1).max())


def fraction_that_collect(
    n: int, radius: float, layout: str, n_seeds: int = COLLECT_SEEDS
) -> float:
    threshold = collect_threshold(n)
    hits = 0
    for seed in range(n_seeds):
        sheep = sheep_at(config_for(n=n, d=1, layout=layout, flock_radius=radius), seed)
        hits += farthest_from_gcm(sheep) > threshold
    return hits / n_seeds


def n_beyond_lost_radius(cfg: dict[str, Any], seed: int = 3) -> int:
    sheep = sheep_at(cfg, seed)
    return int(np.sum(np.linalg.norm(sheep - flock_centre(cfg), axis=1) > cfg["lost_radius"]))


def split_fragmentation(n: int, seed: int = 6) -> float:
    cfg = config_for(n=n, layout="split", flock_radius=9.0)
    view = TickView(make_state(sheep_at(cfg, seed), [[0.0, 0.0]]), cfg)
    return float(fragmentation(view))


def max_sheep_reach(cfg: dict[str, Any], seed: int = 7) -> float:
    sheep = sheep_at(cfg, seed)
    return float(np.linalg.norm(sheep - flock_centre(cfg), axis=1).max())


def pairwise_min_gap(points: np.ndarray) -> float:
    n = points.shape[0]
    if n < 2:
        return float("inf")
    gaps = np.linalg.norm(points[:, None] - points[None], axis=2)[np.triu_indices(n, k=1)]
    return float(gaps.min())


def dog_offsets_from_flock(cfg: dict[str, Any]) -> np.ndarray:
    return place_dogs(cfg) - flock_centre(cfg)


def first_arc_radius(cfg: dict[str, Any]) -> float:
    return layout_extent(cfg) + cfg["dog_start_gap"]


def dog_reaches(cfg: dict[str, Any]) -> np.ndarray:
    return np.linalg.norm(dog_offsets_from_flock(cfg), axis=1)


def behind_flock_dot(cfg: dict[str, Any]) -> np.ndarray:
    """Projection of each dog offset onto the behind-flock axis (positive = behind)."""
    return dog_offsets_from_flock(cfg) @ behind_unit(cfg)


def goal_half(cfg: dict[str, Any]) -> float:
    centre = flock_centre(cfg)
    return goal_half_angle(cfg, float(np.linalg.norm(centre - goal_centre(cfg))))


def dog_angles_from_behind(cfg: dict[str, Any]) -> np.ndarray:
    return signed_angles_from_behind(cfg, place_dogs(cfg))


def dog_distances_to_goal(cfg: dict[str, Any]) -> np.ndarray:
    return np.linalg.norm(place_dogs(cfg) - goal_centre(cfg), axis=1)


def min_sheep_dog_gap(cfg: dict[str, Any], seed: int = 8) -> float:
    sheep = sheep_at(cfg, seed)
    dogs = place_dogs(cfg)
    return float(np.linalg.norm(sheep[:, None] - dogs[None], axis=2).min())


def dog_goal_side_dots(cfg: dict[str, Any]) -> np.ndarray:
    """Projection of each dog onto the toward-goal axis (positive = goal side)."""
    return (place_dogs(cfg) - flock_centre(cfg)) @ toward_goal_unit(cfg)


def in_field(points: np.ndarray, cfg: dict[str, Any], slack: float) -> bool:
    w, h = cfg["world_width"], cfg["world_height"]
    return bool(
        points[:, 0].min() >= slack - EPS
        and points[:, 0].max() <= w - slack + EPS
        and points[:, 1].min() >= slack - EPS
        and points[:, 1].max() <= h - slack + EPS
    )


def goal_clear_of_edges(cfg: dict[str, Any]) -> bool:
    clearance = cfg["field_clearance"]
    goal = goal_centre(cfg)
    radius = cfg["goal_radius"]
    return bool(
        goal[0] + radius <= cfg["world_width"] - clearance + EPS
        and clearance - EPS <= goal[1] - radius
        and goal[1] + radius <= cfg["world_height"] - clearance + EPS
    )


def field_keys(protocol: Protocol, n: int, radius: float) -> set[tuple[float, float, float]]:
    """(width, height, flock_x) for every (layout, D) cell at one N."""
    return {
        (cfg["world_width"], cfg["world_height"], cfg["flock_center"][0])
        for layout in protocol.layouts
        for d in protocol.shepherd_counts
        for cfg in [cell_config(protocol, Cell(Group(METHOD, layout, n), d), radius)]
    }


# --- why the layouts exist ---------------------------------------------------


@pytest.mark.parametrize(("n", "radius"), [(25, 7.0), (100, 9.0), (400, 11.6)])
def test_scattered_layouts_make_strombom_collect_and_compact_does_not(
    n: int, radius: float
) -> None:
    """A sheep beyond r_a N^(2/3) from the flock centre triggers collect; compact never does."""
    assert fraction_that_collect(n, radius, "compact") == 0.0
    for layout in SCATTERED:
        assert fraction_that_collect(n, radius, layout) >= 0.95, layout


def test_outliers_start_beyond_the_lost_radius() -> None:
    n = 100
    cfg = config_for(n=n, layout="outlier_rich", flock_radius=RF[100])
    assert n_beyond_lost_radius(cfg) >= round(cfg["outlier_fraction"] * n)


@pytest.mark.parametrize("n", [25, 100, 400])
def test_split_clusters_start_as_separate_groups(n: int) -> None:
    assert split_fragmentation(n) <= 0.4  # three clusters; none holds more than 40%


@pytest.mark.parametrize("layout", LAYOUTS)
def test_no_sheep_starts_beyond_the_layout_extent(layout: str) -> None:
    """layout_extent is exact: every Gaussian is cut at 3 sigma, the outlier ring ends at far."""
    cfg = config_for(n=400, layout=layout, flock_radius=RF[400])
    assert max_sheep_reach(cfg) <= layout_extent(cfg)


# --- dog starts --------------------------------------------------------------


def test_dogs_start_on_arcs_behind_the_flock() -> None:
    # 128 is well above the study max (24): enough to fill several start arcs so the
    # neighbour-spacing check is meaningful; campaigns never run this many dogs.
    n_dogs = 128
    spacing = 5.0
    cfg = config_for(d=n_dogs, flock_radius=RF[100], settings={"dog_start_spacing": spacing})
    reaches = dog_reaches(cfg)

    assert place_dogs(cfg).shape == (n_dogs, 2)
    assert np.all(behind_flock_dot(cfg) >= -EPS)
    assert reaches.min() == pytest.approx(first_arc_radius(cfg))
    assert reaches.max() < layout_extent(cfg) + SHEEP_REACTION
    assert pairwise_min_gap(place_dogs(cfg)) >= 0.99 * spacing


@pytest.mark.parametrize("start", ["arcs", "ring", "handler"])
def test_every_start_puts_one_dog_straight_behind_the_flock(start: str) -> None:
    cfg = config_for(d=1, flock_radius=RF[100], settings={"dog_start": start})
    dog = place_dogs(cfg)[0]
    centre = flock_centre(cfg)
    assert dog[1] == pytest.approx(centre[1])
    assert dog[0] < centre[0]


@pytest.mark.parametrize("layout", ["wide", "outlier_rich"])
@pytest.mark.parametrize("n, r_f", [(200, RF[200]), (400, RF[400])])
def test_no_ring_dog_starts_in_the_goal_or_its_cone(layout: str, n: int, r_f: float) -> None:
    """A closed ring once put a dog on the drive axis inside the goal; the open ring must not."""
    cfg = config_for(n=n, d=16, layout=layout, flock_radius=r_f, settings={"dog_start": "ring"})
    half = goal_half(cfg)
    angles = dog_angles_from_behind(cfg)

    assert np.all(np.pi - np.abs(angles) >= half - EPS)
    assert np.all(dog_distances_to_goal(cfg) > cfg["goal_radius"])


@pytest.mark.parametrize("layout", LAYOUTS)
@pytest.mark.parametrize(("n", "d"), [(100, 4), (400, 128)])
def test_dogs_start_behind_every_sheep(layout: str, n: int, d: int) -> None:
    """The first arc is dog_start_gap beyond the farthest sheep; no dog starts goal-side."""
    cfg = config_for(n=n, d=d, layout=layout, flock_radius=RF[n])
    assert min_sheep_dog_gap(cfg) >= cfg["dog_start_gap"] - EPS
    assert np.all(dog_goal_side_dots(cfg) <= EPS)


def test_a_zero_drive_multiple_is_refused() -> None:
    """Its sign is the drive direction, and 0 has none (it once put the goal outside the field)."""
    with pytest.raises(ValueError, match="must not be 0"):
        config_for(settings={"drive_distance_multiple": 0.0})


# --- field and drive geometry ------------------------------------------------


def test_drive_distance_scales_with_the_flock_radius() -> None:
    for radius in (9.0, 15.0, 18.0):
        cfg = config_for(n=100, flock_radius=radius)
        assert drive_length(cfg) == pytest.approx(DRIVE_MULTIPLE * radius)
        assert cfg["goal_radius"] == pytest.approx(GOAL_RADIUS_MULTIPLE * radius)


def test_tiny_flocks_still_drive_the_minimum_distance() -> None:
    cfg = config_for(n=5, flock_radius=3.0)
    assert drive_length(cfg) == pytest.approx(MIN_DRIVE)


@pytest.mark.parametrize(
    ("layout", "n", "d", "radius"),
    [
        ("compact", 25, 1, 7.0),
        ("wide", 100, 8, RF[100]),
        ("split", 400, 8, RF[400]),
        ("outlier_rich", 400, 24, RF[400]),
    ],
)
def test_field_holds_flock_dogs_and_goal_with_clearance(
    layout: str, n: int, d: int, radius: float
) -> None:
    cfg = config_for(n=n, d=d, layout=layout, flock_radius=radius)
    assert in_field(place_dogs(cfg), cfg, slack=cfg["field_clearance"])
    assert in_field(sheep_at(cfg, seed=4), cfg, slack=1.0)
    assert goal_clear_of_edges(cfg)


def test_all_cells_of_a_protocol_at_one_n_share_the_field() -> None:
    """Every (layout, D) cell at one N uses the same field, so finishes are comparable."""
    n = 100
    protocol = replace(
        protocol_with(settings={}),
        layouts=("compact", "wide"),
        shepherd_counts=(1, 8, 24),
    )
    assert len(field_keys(protocol, n, RF[100])) == 1


# --- success rule ------------------------------------------------------------


def test_success_fraction_counts_the_share_of_sheep_inside() -> None:
    goal_radius = 5.0
    inside = np.zeros((99, 2))
    outside = np.array([[50.0, 0.0]])
    strict = GoalZone(np.zeros(2), goal_radius)
    relaxed = GoalZone(np.zeros(2), goal_radius, required_fraction=0.99)

    assert not strict.reached(np.vstack([inside, outside]))
    assert relaxed.reached(np.vstack([inside, outside]))  # 99 of 100
    assert not relaxed.reached(np.vstack([inside[:98], outside, outside]))  # 98 of 100
    assert strict.reached(inside)


def test_the_centroid_rule_ends_on_the_flock_centre_not_the_sheep_count() -> None:
    """Strombom et al. (2014): the task ends when the flock centre is in the goal."""
    goal = GoalZone(np.zeros(2), 10.0, by_centroid=True)
    straddling = np.array([[-30.0, 0.0], [30.0, 0.0]])  # no sheep inside, centre at the goal

    assert goal.reached(straddling)
    assert not goal.reached(straddling + [25.0, 0.0])


def test_the_box_start_puts_the_sheep_and_the_dog_in_their_boxes() -> None:
    side = 150.0
    config = {
        "sheep_box": (side / 2, side),
        "dog_box": (0.0, side / 2),
        "n_sheep": 200,
        "n_shepherds": 1,
    }
    sheep, dogs = place_boxes(config, np.random.default_rng(SEED))

    assert sheep.shape == (200, 2) and dogs.shape == (1, 2)
    assert np.all((sheep >= side / 2) & (sheep <= side))
    assert np.all((dogs >= 0.0) & (dogs <= side / 2))


def test_a_relaxed_success_rule_never_finishes_later_than_the_strict_one() -> None:
    ticks = 900
    common: dict[str, Any] = {
        "n": 100,
        "d": 3,
        "layout": "wide",
        "ticks": ticks,
        "flock_radius": 9.08,
    }
    strict = run_trial(config_for(**common), SEED)
    relaxed = run_trial(config_for(**common, settings={"success_fraction": 0.99}), SEED)
    strict_limit = strict.total_ticks if strict.success else ticks
    assert relaxed.success
    assert relaxed.total_ticks <= strict_limit
