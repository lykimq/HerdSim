"""Correctness: runner status transitions and termination."""

from __future__ import annotations

from scenarios.drive_to_goal import DriveToGoalScenario
from tests.backend.helpers import build_runner, make_state


def test_step_advances_tick_and_reports_status():
    runner = build_runner(
        "strombom",
        seed=42,
        num_sheep=8,
        num_shepherds=1,
        config_overrides={"max_ticks": 50},
    )
    runner.initialize()
    state, metrics, status = runner.step()
    assert state.tick == 1
    assert "cohesion" in metrics
    assert status in {"running", "success", "timeout"}


def test_drive_to_goal_success_requires_fraction_in_goal():
    runner = build_runner(
        "strombom",
        seed=1,
        num_sheep=4,
        num_shepherds=1,
    )
    state = runner.initialize()
    scen = DriveToGoalScenario()
    inside = make_state(
        [state.world.goal.center] * 4,
        [[50.0, 50.0]],
        world=state.world,
    )
    outside = make_state(
        [[80.0, 80.0]] * 4,
        [[50.0, 50.0]],
        world=state.world,
    )
    assert scen.is_success(inside, runner.config)
    assert not scen.is_success(outside, runner.config)


def test_timeout_when_max_ticks_exhausted():
    runner = build_runner(
        "strombom",
        seed=3,
        num_sheep=6,
        num_shepherds=1,
        config_overrides={
            "max_ticks": 3,
            "goal_radius": 1.0,
            "goal_center": [0.0, 0.0],
        },
    )
    result = runner.run()
    assert result.success is False
    assert result.total_ticks == 3
