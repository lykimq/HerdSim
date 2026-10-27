"""The gather task: its geometry, start, success and end rules, labels, and a real trial."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
import yaml

from records.trial_row import build_row
from services.protocol import load_protocol
from sim.core.simulation_runner import STOP_ENDED, STOP_SUCCESS, run_trial
from sim.core.world.arena import GoalZone, World
from sim.plugins.scenarios import SCENARIOS, gather
from sim.plugins.scenarios.failures import NONE, TIMEOUT
from tests.helpers import GATHER_PROTOCOL, gather_config, make_state

CONFIG = gather_config(n=40, d=3)
R, GOAL = CONFIG["start_radius"], CONFIG["goal_radius"]
XI = CONFIG["sensing_radius"]


def _world(goal_radius: float = GOAL) -> World:
    return World(100.0, 100.0, GoalZone(np.zeros(2), goal_radius, required_fraction=0.99))


def test_geometry_follows_the_start_radius_not_a_flock_radius():
    assert CONFIG["start_radius"] == 20.0 and CONFIG["flock_radius"] == 20.0
    assert CONFIG["goal_radius"] == pytest.approx(0.2 * 20.0)
    assert CONFIG["goal_center"] == CONFIG["flock_center"]
    assert CONFIG["world_width"] == pytest.approx(2.0 * (20.0 + CONFIG["field_clearance"]))
    assert SCENARIOS["gather"].drive_length(CONFIG) == pytest.approx(16.0)
    other = gather_config(n=40, d=3, settings={"gather_start_radius": 50.0})
    assert other["goal_radius"] == pytest.approx(10.0) and other["max_ticks"] == 2000


def test_everyone_starts_inside_the_disc_and_sheep_do_not_depend_on_the_dog_count():
    scenario = SCENARIOS["gather"]
    sheep, dogs = scenario.initial_positions(CONFIG, np.random.default_rng(5))
    centre = np.asarray(CONFIG["flock_center"])
    assert sheep.shape == (40, 2) and dogs.shape == (3, 2)
    assert np.linalg.norm(sheep - centre, axis=1).max() <= R
    assert np.linalg.norm(dogs - centre, axis=1).max() <= R
    more, _ = scenario.initial_positions({**CONFIG, "n_shepherds": 7}, np.random.default_rng(5))
    np.testing.assert_array_equal(more, sheep)


def test_uniform_start_fills_the_disc_evenly():
    """Half the points lie within R / sqrt(2): the density is uniform in area, not in radius."""
    sheep, _ = SCENARIOS["gather"].initial_positions(
        {**CONFIG, "n_sheep": 20000}, np.random.default_rng(1)
    )
    r = np.linalg.norm(sheep - np.asarray(CONFIG["flock_center"]), axis=1)
    assert np.mean(r <= R / np.sqrt(2.0)) == pytest.approx(0.5, abs=0.02)


def test_success_needs_the_share_inside_and_every_dog_inside():
    inside = np.zeros((99, 2))
    out = np.array([[R, 0.0]])
    sheep = np.vstack([inside, out])  # 99 of 100
    home = [[1.0, 0.0]]
    assert gather.is_success(make_state(sheep, home, world=_world()))
    assert not gather.is_success(make_state(sheep, [[GOAL + 1.0, 0.0]], world=_world()))
    two_out = np.vstack([inside[:98], out, out])
    assert not gather.is_success(make_state(two_out, home, world=_world()))


def test_the_trial_ends_when_the_dogs_are_home_and_see_nothing_outside():
    inside = np.zeros((10, 2))
    home = [[0.5, 0.0]]
    lost = np.array([[GOAL + XI + 1.0, 0.0]])  # outside the goal, beyond the dog's sensing
    seen = np.array([[0.5 + XI - 1.0, 0.0]])  # outside the goal (4), within the dog's sensing
    assert gather.is_over(make_state(np.vstack([inside, lost]), home, world=_world()), CONFIG)
    assert not gather.is_over(make_state(np.vstack([inside, seen]), home, world=_world()), CONFIG)
    away = [[GOAL + 1.0, 0.0]]
    assert not gather.is_over(make_state(np.vstack([inside, lost]), away, world=_world()), CONFIG)
    # A dog that sees everything ends the trial only when every sheep is inside.
    sees_all = {**CONFIG, "sensing_radius": float("inf")}
    assert not gather.is_over(make_state(np.vstack([inside, lost]), home, world=_world()), sees_all)
    assert gather.is_over(make_state(inside, home, world=_world()), sees_all)


def test_failure_labels_lost_targets_and_outnumbered():
    cfg = {**CONFIG, "max_ticks": 100}

    def label(unseen, last_tick, success=False):
        ticks = np.linspace(0, last_tick, len(unseen)).round()
        frame = pd.DataFrame({"tick": ticks, "unseen_targets": unseen})
        return gather.classify_failure(frame, success=success, config=cfg).mode

    assert label([0.0, 1.0], 40) == gather.TARGETS_LOST
    assert label(np.zeros(11), 100) == gather.OUTNUMBERED  # every target seen, ran to the limit
    assert label(np.zeros(6), 50) == TIMEOUT  # ended early with every target seen: no rule
    assert label([0.0, 1.0], 40, success=True) == NONE


def test_a_real_trial_runs_to_an_end_and_its_row_reads_the_paper_quantities():
    """Five herders that see everything gather 20 targets from a disc of radius 20 (measured:
    seed 2026 succeeds at tick 1823, 55 model seconds); the row keeps chi at the end and the
    unseen count. The tick count assumes the herders read the targets at the start of the
    tick; a same-machine replay is exact."""
    cfg = gather_config(n=20, d=5, ticks=8000, params={"sensing_radius": float("inf")})
    result = run_trial(cfg, 2026)
    assert result.success and result.stop_reason == STOP_SUCCESS
    assert result.total_ticks == pytest.approx(1823, rel=0.05)
    row = build_row({}, result, cfg)
    assert row["final_in_goal_fraction"] >= 0.99 and row["final_unseen_targets"] == 0.0
    assert row["failure_mode"] == NONE
    assert row["drive_distance"] == pytest.approx(16.0)
    assert row["seconds_to_99pct_in_goal"] <= row["finish_seconds"]
    again = build_row({}, run_trial(cfg, 2026), cfg)
    assert pd.Series(again).equals(pd.Series(row))


def test_a_recording_stride_changes_the_rows_but_not_the_trial():
    """With a stride the stop checks still run every tick, the last tick is recorded, and a
    first arrival is read from the recorded ticks, so it is never earlier than the exact one
    (a touch between two records is missed)."""
    every = gather_config(n=20, d=5, ticks=8000, params={"sensing_radius": float("inf")})
    strided = {**every, "metrics_stride": 10}
    a, b = run_trial(every, 2026), run_trial(strided, 2026)
    assert (a.success, a.total_ticks) == (b.success, b.total_ticks)
    assert b.history["tick"].iloc[-1] == b.total_ticks
    ticks = b.history["tick"].to_numpy()
    assert (ticks[:-1] % 10 == 0).all() and len(b.history) < len(a.history) / 8
    ra, rb = build_row({}, a, every), build_row({}, b, strided)
    assert rb["seconds_to_90pct_in_goal"] >= ra["seconds_to_90pct_in_goal"]
    assert rb["finish_seconds"] == ra["finish_seconds"]


def test_a_dog_that_sees_nothing_outside_ends_the_trial_early_as_a_failure():
    """One herder with a short sight and many targets on a disc wide against it: it brings in
    what it sees and goes home while targets are lost beyond its reach."""
    cfg = gather_config(n=10, d=1, ticks=2000, params={"sensing_radius": 3.0})
    result = run_trial(cfg, 11)
    assert not result.success and result.stop_reason == STOP_ENDED
    assert result.total_ticks < cfg["max_ticks"]
    row = build_row({}, result, cfg)
    assert row["failure_mode"] == gather.TARGETS_LOST and row["final_unseen_targets"] > 0.0


def test_a_layout_of_the_other_task_is_refused_at_load(tmp_path):
    spec = {k: v for k, v in GATHER_PROTOCOL.resolved.items() if k != "canonical_values"}
    path = tmp_path / "bad_gather.yaml"
    path.write_text(yaml.safe_dump({**spec, "layouts": ["compact"]}))
    with pytest.raises(ValueError, match="unknown layouts .* for task 'gather'"):
        load_protocol(str(path), output=tmp_path / "out")
    with pytest.raises(ValueError, match="unknown task"):
        path.write_text(yaml.safe_dump({**spec, "task": "fetch"}))
        load_protocol(str(path), output=tmp_path / "out")
