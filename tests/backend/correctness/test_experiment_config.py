"""Correctness: experiment preset resolution."""

from __future__ import annotations

from algorithms.flocking_dog.config import FLOCKING_DOG_DEFAULTS
from algorithms.kubo.algorithm import KuboAlgorithm
from algorithms.kubo.config import KUBO_DEFAULTS
from algorithms.registry import algorithm_registry
from algorithms.strombom.algorithm import StrombomAlgorithm
from algorithms.strombom.config import STROMBOM_DEFAULTS
from core.experiment_config import resolve_experiment_config
from core.shared_defaults import SHARED_WORLD_DEFAULTS, WORLD_KEYS
from scenarios.drive_to_goal import DriveToGoalScenario
from scenarios.obstacle_course import ObstacleCourseScenario

# Algorithm modules may declare collect_threshold_scale; scenarios can override it.
_LAYOUT_ONLY_KEYS = set(WORLD_KEYS) - {"collect_threshold_scale"}


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


def test_resolve_includes_shared_world_fallbacks():
    config = resolve_experiment_config(
        KuboAlgorithm(), DriveToGoalScenario(), preset="paper"
    )
    for key, value in SHARED_WORLD_DEFAULTS.items():
        assert key in config
        # Drive-to-goal scenario supplies the same layout defaults as shared.
        assert config[key] == DriveToGoalScenario().default_config.get(key, value)


def test_algorithm_configs_omit_layout_world_keys():
    for defaults in (STROMBOM_DEFAULTS, KUBO_DEFAULTS, FLOCKING_DOG_DEFAULTS):
        overlap = _LAYOUT_ONLY_KEYS.intersection(defaults)
        assert not overlap, f"layout keys in algorithm defaults: {overlap}"

    for entry in algorithm_registry.list_all():
        overlap = _LAYOUT_ONLY_KEYS.intersection(entry["default_config"])
        assert not overlap, f"{entry['id']} default_config has layout keys: {overlap}"


def test_kubo_paper_keeps_force_params_under_narrow_gate_world():
    from scenarios.narrow_gate import NarrowGateScenario

    alg = KuboAlgorithm()
    scen = NarrowGateScenario()
    config = resolve_experiment_config(alg, scen, preset="paper")
    assert config["K_f4"] == alg.default_config["K_f4"]
    assert config["dog_speed_max"] == alg.default_config["dog_speed_max"]
    assert config["n_shepherds"] == 4
    assert config["gate_width"] == scen.default_config["gate_width"]
    assert config["goal_center"] == scen.default_config["goal_center"]
