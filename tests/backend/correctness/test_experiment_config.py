"""Correctness: experiment preset resolution."""

from __future__ import annotations

from algorithms.kubo.algorithm import KuboAlgorithm
from algorithms.strombom.algorithm import StrombomAlgorithm
from core.experiment_config import resolve_experiment_config
from scenarios.drive_to_goal import DriveToGoalScenario
from scenarios.obstacle_course import ObstacleCourseScenario


def test_paper_preset_keeps_algorithm_agent_counts():
    alg = StrombomAlgorithm()
    config = resolve_experiment_config(alg, DriveToGoalScenario(), preset="paper")
    assert config["n_sheep"] == alg.default_config["n_sheep"]
    assert config["n_shepherds"] == alg.default_config["n_shepherds"]


def test_paper_preset_uses_scenario_world_layout():
    alg = StrombomAlgorithm()
    scen = ObstacleCourseScenario()
    config = resolve_experiment_config(alg, scen, preset="paper")
    assert config["n_sheep"] == alg.default_config["n_sheep"]
    assert config["goal_center"] == scen.default_config["goal_center"]
    assert config["obstacles"] == scen.default_config["obstacles"]
    assert len(config["obstacles"]) == 3


def test_scenario_preset_overlays_world_and_counts():
    alg = KuboAlgorithm()
    scen = ObstacleCourseScenario()
    config = resolve_experiment_config(alg, scen, preset="scenario")
    assert config["n_sheep"] == scen.default_config["n_sheep"]
    assert config["goal_center"] == scen.default_config["goal_center"]
    assert "obstacles" in config


def test_custom_overrides_win():
    config = resolve_experiment_config(
        StrombomAlgorithm(),
        DriveToGoalScenario(),
        preset="custom",
        num_sheep=12,
        num_shepherds=2,
        world_overrides={"world_width": 200.0, "max_ticks": 500},
    )
    assert config["n_sheep"] == 12
    assert config["n_shepherds"] == 2
    assert config["world_width"] == 200.0
    assert config["max_ticks"] == 500
