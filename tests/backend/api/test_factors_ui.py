"""API and helper coverage for UI-exposed experimental factors."""

from __future__ import annotations

import numpy as np
import pytest
from fastapi.testclient import TestClient

from api.benchmark_sweep import expand_factor_grid, parse_factor_specs, sweep_label
from api.main import app
from core.agent_attributes import apply_robot_constraints
from core.experiment_config import resolve_experiment_config
from core.presets import get_preset
from core.simulation_runner import SimulationRunner
from metrics.registry import metric_registry
from scenarios.drive_to_goal import DriveToGoalScenario


@pytest.fixture
def client():
    return TestClient(app)


def test_meta_models_lists_plugins(client):
    res = client.get("/api/algorithms/meta/models")
    assert res.status_code == 200
    payload = res.json()
    sheep_ids = {
        item if isinstance(item, str) else item["id"] for item in payload["sheep_models"]
    }
    dog_ids = {
        item if isinstance(item, str) else item["id"]
        for item in payload["dog_controllers"]
    }
    assert "strombom" in sheep_ids
    assert "collect_drive" in dog_ids
    assert "fat" in dog_ids
    assert "adaptive" in dog_ids
    factors = payload["factors"]
    assert factors["max_grid_cells"] >= 1
    assert "n_sheep" in factors["grid_keys"]
    assert any(item["id"] == "global" for item in factors["enums"]["obs_mode"])
    assert "sensing_range" in factors["dependencies"]


def test_create_session_echoes_obs_mode_and_factors(client):
    res = client.post(
        "/api/simulations",
        json={
            "instrument": "strombom",
            "scenario_id": "drive_to_goal",
            "preset": "custom",
            "num_sheep": 12,
            "num_shepherds": 1,
            "seed": 11,
            "obs_mode": "local_positions",
            "algorithm_params": {
                "sensing_range": 28.0,
                "stubborn_fraction": 0.35,
                "failure_mode": "none",
            },
        },
    )
    assert res.status_code == 200
    payload = res.json()
    assert payload["obs_mode"] == "local_positions"
    assert payload["sheep_model"] == "strombom"
    assert payload["dog_controller"] == "collect_drive"
    assert payload["config"]["sensing_range"] == 28.0
    assert payload["config"]["stubborn_fraction"] == 0.35


@pytest.mark.parametrize(
    "instrument,obs_mode",
    [
        ("fat", "local_positions"),
        ("adaptive", "bearing_only"),
        ("communication_free", "global"),
    ],
)
def test_instrument_session_steps_with_local_obs(client, instrument, obs_mode):
    create = client.post(
        "/api/simulations",
        json={
            "instrument": instrument,
            "scenario_id": "drive_to_goal",
            "preset": "custom",
            "num_sheep": 10,
            "num_shepherds": 2,
            "seed": 4,
            "obs_mode": obs_mode,
        },
    )
    assert create.status_code == 200, create.text
    session_id = create.json()["session_id"]
    with client.websocket_connect(f"/ws/simulation/{session_id}") as ws:
        assert ws.receive_json()["type"] == "reset"
        ws.send_json({"action": "step"})
        tick = ws.receive_json()
        assert tick["type"] == "tick"
        assert tick["tick"] == 1
        assert tick["status"] in {"paused", "running", "success", "failed"}


def test_robot_constraints_clamp_vmax():
    desired = np.array([[10.0, 0.0], [0.0, 10.0]], dtype=float)
    prev = np.zeros_like(desired)
    out = apply_robot_constraints(
        state=None,
        desired_velocities=desired,
        config={"v_max": 2.0},
        prev_velocities=prev,
    )
    norms = np.linalg.norm(out, axis=1)
    assert np.all(norms <= 2.0 + 1e-9)


def test_factor_grid_helpers_parse_and_label():
    specs = parse_factor_specs(
        [
            {"key": "n_sheep", "values": [20, 40]},
            {"key": "obs_mode", "values": ["global", "bearing_only"]},
        ]
    )
    combos = expand_factor_grid(specs)
    assert len(combos) == 4
    assert sweep_label(combos[0]).startswith("n_sheep=")


def test_resolve_failure_and_blind_masks():
    config = resolve_experiment_config(
        scenario=DriveToGoalScenario(),
        instrument="strombom",
        preset="custom",
        num_sheep=8,
        num_shepherds=2,
        algorithm_params={
            "failure_mode": "blind_after_tick",
            "failure_tick": 0,
            "speed_scale": 0.8,
        },
    )
    assert config["failure_mode"] == "blind_after_tick"
    assert config["speed_scale"] == 0.8
    runner = SimulationRunner(
        scenario=DriveToGoalScenario(),
        metrics=metric_registry.get_all(),
        config=config,
        seed=2,
        instrument="strombom",
    )
    runner.initialize()
    assert runner.state is not None
    runner.step()
    assert float(runner.state.shepherd_sensing_scale[1]) == 0.0


def test_presets_expose_model_pair():
    fat = get_preset("fat")
    assert fat["sheep_model"]
    assert fat["dog_controller"] == "fat"
