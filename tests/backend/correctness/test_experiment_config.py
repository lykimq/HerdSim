"""Correctness: experiment preset resolution."""

from __future__ import annotations

from algorithms.flocking_dog.config import FLOCKING_DOG_DEFAULTS
from algorithms.kubo.config import KUBO_DEFAULTS
from algorithms.registry import algorithm_registry
from algorithms.strombom.config import STROMBOM_DEFAULTS
from core.experiment_config import resolve_experiment_config
from core.presets import get_preset
from core.shared_defaults import SHARED_WORLD_DEFAULTS, WORLD_KEYS
from scenarios.drive_to_goal import DriveToGoalScenario
from scenarios.obstacle_course import ObstacleCourseScenario

_LAYOUT_ONLY_KEYS = set(WORLD_KEYS) - {"collect_threshold_scale"}


def test_paper_preset_keeps_algorithm_agent_counts():
    preset = get_preset("strombom")
    config = resolve_experiment_config(
        scenario=DriveToGoalScenario(),
        instrument="strombom",
        preset="paper",
    )
    assert config["n_sheep"] == preset["default_config"]["n_sheep"]
    assert config["n_shepherds"] == preset["default_config"]["n_shepherds"]


def test_paper_preset_uses_scenario_world_layout():
    preset = get_preset("strombom")
    scen = ObstacleCourseScenario()
    config = resolve_experiment_config(
        scenario=scen, instrument="strombom", preset="paper"
    )
    assert config["n_sheep"] == preset["default_config"]["n_sheep"]
    assert config["goal_center"] == scen.default_config["goal_center"]
    assert config["obstacles"] == scen.default_config["obstacles"]
    assert len(config["obstacles"]) == 3


def test_scenario_preset_overlays_world_and_counts():
    scen = ObstacleCourseScenario()
    config = resolve_experiment_config(
        scenario=scen, instrument="kubo", preset="scenario"
    )
    assert config["n_sheep"] == scen.default_config["n_sheep"]
    assert config["goal_center"] == scen.default_config["goal_center"]
    assert "obstacles" in config


def test_custom_overrides_win():
    config = resolve_experiment_config(
        scenario=DriveToGoalScenario(),
        instrument="strombom",
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
        scenario=DriveToGoalScenario(), instrument="kubo", preset="paper"
    )
    for key, value in SHARED_WORLD_DEFAULTS.items():
        assert key in config
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

    preset = get_preset("kubo")
    scen = NarrowGateScenario()
    config = resolve_experiment_config(
        scenario=scen, instrument="kubo", preset="paper"
    )
    assert config["K_f4"] == preset["default_config"]["K_f4"]
    assert config["dog_speed_max"] == preset["default_config"]["dog_speed_max"]
    assert config["n_shepherds"] == 4
    assert config["gate_width"] == scen.default_config["gate_width"]
    assert config["gate_x"] == scen.default_config["gate_x"]
    assert config["wall_thickness"] == scen.default_config["wall_thickness"]
    assert config["goal_center"] == scen.default_config["goal_center"]


def test_paper_preset_includes_containment_scenario_keys():
    from scenarios.containment import ContainmentScenario

    config = resolve_experiment_config(
        scenario=ContainmentScenario(), instrument="strombom", preset="paper"
    )
    assert config["containment_fraction"] == 0.95
    assert config["containment_min_ticks"] == 200
    assert config["pen_center"] == ContainmentScenario().default_config["pen_center"]
    assert config["pen_radius"] == ContainmentScenario().default_config["pen_radius"]
