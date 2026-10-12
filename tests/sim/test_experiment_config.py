"""Correctness: experiment preset resolution."""

from __future__ import annotations

from core.config import resolve_experiment_config
from core.methods import get_method, list_methods
from core.world.defaults import WORLD_DEFAULTS, WORLD_KEYS
from methods.kubo.config import KUBO_DEFAULTS
from methods.strombom.config import STROMBOM_DEFAULTS
from plugins.scenarios.drive_to_goal import DriveToGoalScenario

_LAYOUT_ONLY_KEYS = set(WORLD_KEYS) - {"collect_threshold_scale"}


def test_paper_preset_keeps_algorithm_agent_counts():
    preset = get_method("strombom")
    config = resolve_experiment_config(
        scenario=DriveToGoalScenario(),
        method="strombom",
        preset="paper",
    )
    assert config["n_sheep"] == preset["default_config"]["n_sheep"]
    assert config["n_shepherds"] == preset["default_config"]["n_shepherds"]


def test_paper_preset_uses_scenario_world_layout():
    preset = get_method("strombom")
    scen = DriveToGoalScenario()
    config = resolve_experiment_config(scenario=scen, method="strombom", preset="paper")
    assert config["n_sheep"] == preset["default_config"]["n_sheep"]
    assert config["goal_center"] == scen.default_config["goal_center"]
    assert config["goal_radius"] == scen.default_config["goal_radius"]
    assert config["world_width"] == scen.default_config["world_width"]


def test_scenario_preset_overlays_world_and_counts():
    scen = DriveToGoalScenario()
    config = resolve_experiment_config(scenario=scen, method="kubo", preset="scenario")
    assert config["n_sheep"] == scen.default_config["n_sheep"]
    assert config["n_shepherds"] == scen.default_config["n_shepherds"]
    assert config["goal_center"] == scen.default_config["goal_center"]


def test_custom_overrides_win():
    config = resolve_experiment_config(
        scenario=DriveToGoalScenario(),
        method="strombom",
        preset="custom",
        num_sheep=12,
        num_shepherds=2,
        world_overrides={"world_width": 200.0, "max_ticks": 500},
    )
    assert config["n_sheep"] == 12
    assert config["n_shepherds"] == 2
    assert config["world_width"] == 200.0
    assert config["max_ticks"] == 500


def test_resolve_includes_world_fallbacks():
    config = resolve_experiment_config(
        scenario=DriveToGoalScenario(), method="kubo", preset="paper"
    )
    for key, value in WORLD_DEFAULTS.items():
        assert key in config
        assert config[key] == DriveToGoalScenario().default_config.get(key, value)


def test_algorithm_configs_omit_layout_world_keys():
    for defaults in (STROMBOM_DEFAULTS, KUBO_DEFAULTS):
        overlap = _LAYOUT_ONLY_KEYS.intersection(defaults)
        assert not overlap, f"layout keys in algorithm defaults: {overlap}"

    for entry in list_methods():
        overlap = _LAYOUT_ONLY_KEYS.intersection(entry["default_config"])
        assert not overlap, f"{entry['id']} default_config has layout keys: {overlap}"


def test_kubo_paper_keeps_force_params_under_drive_to_goal_world():
    preset = get_method("kubo")
    scen = DriveToGoalScenario()
    config = resolve_experiment_config(scenario=scen, method="kubo", preset="paper")
    assert config["K_f4"] == preset["default_config"]["K_f4"]
    assert config["dog_speed_max"] == preset["default_config"]["dog_speed_max"]
    assert config["n_shepherds"] == preset["default_config"]["n_shepherds"]
    assert config["goal_center"] == scen.default_config["goal_center"]
    assert config["world_width"] == scen.default_config["world_width"]
