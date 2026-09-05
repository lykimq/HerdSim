"""Unit test for SimulationRunner integration."""

from algorithms.strombom.algorithm import StrombomAlgorithm
from core.simulation_runner import SimulationRunner
from metrics.registry import metric_registry
from scenarios.drive_to_goal import DriveToGoalScenario


def test_simulation_runner_initialization():
    alg = StrombomAlgorithm()
    scen = DriveToGoalScenario()
    metrics = metric_registry.get_all()
    config = alg.default_config
    config["n_sheep"] = 15
    config["n_shepherds"] = 1

    runner = SimulationRunner(
        algorithm=alg,
        scenario=scen,
        metrics=metrics,
        config=config,
        seed=123,
    )
    state = runner.initialize()
    assert state.n_sheep == 15
    assert state.n_shepherds == 1
    assert state.tick == 0


def test_simulation_runner_step():
    alg = StrombomAlgorithm()
    scen = DriveToGoalScenario()
    metrics = metric_registry.get_all()
    config = alg.default_config
    config["n_sheep"] = 10
    config["n_shepherds"] = 1

    runner = SimulationRunner(
        algorithm=alg,
        scenario=scen,
        metrics=metrics,
        config=config,
        seed=42,
    )
    runner.initialize()
    state, metrics_snapshot, status = runner.step()
    assert state.tick == 1
    assert "cohesion" in metrics_snapshot
    assert status in ("running", "success", "timeout")
