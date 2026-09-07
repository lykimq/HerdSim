"""Thin API smoke: wiring only (not scientific coverage)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from api.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_lists_core_catalog(client):
    algs = client.get("/api/algorithms").json()
    by_id = {item["id"]: item for item in algs}
    assert by_id["strombom"]["herder_kind"] == "human"
    assert by_id["kubo"]["herder_kind"] == "dog"
    assert "netlogo" not in by_id

    scenarios = client.get("/api/scenarios").json()
    assert any(item["id"] == "drive_to_goal" for item in scenarios)

    metrics = {item["id"]: item for item in client.get("/api/metrics").json()}
    assert {"cohesion", "shepherd_path"} <= set(metrics)
    assert metrics["time_to_goal"]["unit"] == "ticks"
    assert "world" in metrics["cohesion"]["unit"]


def test_create_session_paper_strombom(client):
    res = client.post(
        "/api/simulations",
        json={
            "algorithm_id": "strombom",
            "scenario_id": "drive_to_goal",
            "preset": "paper",
            "seed": 7,
        },
    )
    assert res.status_code == 200
    payload = res.json()
    assert payload["tick"] == 0
    assert payload["num_sheep"] == 50
    assert len(payload["sheep_positions"]) == 50


def test_create_session_scenario_preset_kubo(client):
    res = client.post(
        "/api/simulations",
        json={
            "algorithm_id": "kubo",
            "scenario_id": "obstacle_course",
            "preset": "scenario",
            "seed": 1,
        },
    )
    assert res.status_code == 200
    payload = res.json()
    assert payload["num_sheep"] == 30
    assert payload["num_shepherds"] == 2


def test_websocket_step_and_reset(client):
    create = client.post(
        "/api/simulations",
        json={
            "algorithm_id": "strombom",
            "scenario_id": "drive_to_goal",
            "num_sheep": 8,
            "num_shepherds": 1,
            "seed": 3,
        },
    )
    session_id = create.json()["session_id"]
    with client.websocket_connect(f"/ws/simulation/{session_id}") as ws:
        assert ws.receive_json()["type"] == "reset"
        ws.send_json({"action": "step"})
        tick = ws.receive_json()
        assert tick["type"] == "tick"
        assert tick["tick"] == 1
        assert tick["status"] == "paused"
        assert "cohesion" in tick["metrics"]
        # Repeated step must stay available without an explicit Pause.
        ws.send_json({"action": "step"})
        tick2 = ws.receive_json()
        assert tick2["tick"] == 2
        assert tick2["status"] == "paused"
        ws.send_json({"action": "reset"})
        assert ws.receive_json()["tick"] == 0


def test_benchmark_run_and_export(client):
    res = client.post(
        "/api/benchmarks/run",
        json={
            "algorithm_ids": ["strombom"],
            "scenario_id": "drive_to_goal",
            "seeds": [1],
            "preset": "paper",
            "num_sheep": 8,
            "num_shepherds": 1,
        },
    )
    assert res.status_code == 200
    payload = res.json()
    assert len(payload["rows"]) == 1
    assert len(payload["summary"]) == 1
    csv_res = client.get("/api/benchmarks/export?format=csv")
    assert csv_res.status_code == 200
    assert csv_res.text.startswith("# HerdSim benchmark CSV column definitions")
    assert "algorithm" in csv_res.text
    defs = client.get("/api/benchmarks/definitions")
    assert defs.status_code == 200
    body = defs.json()
    assert any(d["id"] == "success_rate" for d in body["summary"])
    assert any(d["id"] == "cohesion" for d in body["csv"])


@pytest.mark.asyncio
async def test_async_create_session():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/api/simulations",
            json={
                "algorithm_id": "strombom",
                "scenario_id": "drive_to_goal",
                "num_sheep": 5,
                "num_shepherds": 1,
                "seed": 1,
            },
        )
    assert res.status_code == 200
    assert res.json()["session_id"]
