"""API and WebSocket smoke tests for the simulation baseline."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from starlette.testclient import TestClient as StarletteTestClient

from api.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_list_algorithms(client):
    res = client.get("/api/algorithms")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert any(item["id"] == "strombom" for item in data)


def test_list_scenarios(client):
    res = client.get("/api/scenarios")
    assert res.status_code == 200
    data = res.json()
    assert any(item["id"] == "drive_to_goal" for item in data)


def test_list_metrics(client):
    res = client.get("/api/metrics")
    assert res.status_code == 200
    ids = {item["id"] for item in res.json()}
    assert "cohesion" in ids
    assert "shepherd_path" in ids


def test_create_session(client):
    res = client.post(
        "/api/simulations",
        json={
            "algorithm_id": "strombom",
            "scenario_id": "drive_to_goal",
            "num_sheep": 12,
            "num_shepherds": 1,
            "seed": 7,
        },
    )
    assert res.status_code == 200
    payload = res.json()
    assert "session_id" in payload
    assert payload["tick"] == 0
    assert len(payload["sheep_positions"]) == 12
    assert payload["world"]["goal_center"] is not None


def test_websocket_tick_and_reset(client):
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
        initial = ws.receive_json()
        assert initial["type"] == "reset"
        assert initial["tick"] == 0
        assert "world" in initial
        assert len(initial["sheep_positions"]) == 8

        ws.send_json({"action": "step"})
        tick = ws.receive_json()
        assert tick["type"] == "tick"
        assert tick["tick"] == 1
        assert "cohesion" in tick["metrics"]

        ws.send_json({"action": "reset"})
        reset = ws.receive_json()
        assert reset["type"] == "reset"
        assert reset["tick"] == 0


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
