"""API coverage for NetLogo model library and uploads."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_list_twins_includes_all_algorithms():
    res = client.get("/api/netlogo/twins")
    assert res.status_code == 200
    twins = res.json()["twins"]
    by_id = {t["algorithm_id"]: t for t in twins}
    expected = {
        "strombom": "strombom.nlogo",
        "strombom_noise": "strombom_noise.nlogo",
        "strombom_multi": "strombom_multi.nlogo",
        "kubo": "kubo.nlogo",
        "flocking_dog": "flocking_dog.nlogo",
    }
    for alg_id, filename in expected.items():
        assert alg_id in by_id
        assert by_id[alg_id]["model_file"].endswith(filename)


def test_list_netlogo_models_includes_example():
    res = client.get("/api/netlogo/models")
    assert res.status_code == 200
    payload = res.json()
    paths = [m["path"] for m in payload["models"]]
    assert "netlogo/models/example.nlogo" in paths
    example = next(m for m in payload["models"] if m["name"] == "example.nlogo")
    assert example["source"] == "bundled"


def test_netlogo_status_shape():
    res = client.get("/api/netlogo/status")
    assert res.status_code == 200
    body = res.json()
    assert "detected" in body
    assert "netlogo_home" in body
    assert "gui_available" in body
    assert "models_dir" in body


def test_open_in_desktop_launches_gui(monkeypatch):
    from api.routers import netlogo as netlogo_router

    calls = []

    def fake_popen(cmd, **kwargs):
        calls.append((cmd, kwargs))
        return object()

    monkeypatch.setattr(netlogo_router.subprocess, "Popen", fake_popen)
    monkeypatch.setattr(
        netlogo_router,
        "find_netlogo_home",
        lambda: "/fake/NetLogo",
    )
    monkeypatch.setattr(
        netlogo_router,
        "find_netlogo_gui_launcher",
        lambda home=None: Path("/fake/NetLogo/NetLogo"),
    )

    res = client.post(
        "/api/netlogo/open",
        json={"model_file": "netlogo/models/example.nlogo"},
    )
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["opened"] is True
    assert body["model_file"].endswith("example.nlogo")
    assert calls
    assert str(calls[0][0][0]).endswith("NetLogo")
    assert str(calls[0][0][1]).endswith("example.nlogo")


def test_open_rejects_outside_models_dir():
    res = client.post(
        "/api/netlogo/open",
        json={"model_file": "/etc/passwd"},
    )
    assert res.status_code in {400, 404}


def test_upload_netlogo_model(tmp_path: Path, monkeypatch):
    from api.routers import netlogo as netlogo_router

    uploads = tmp_path / "uploads"
    uploads.mkdir()
    monkeypatch.setattr(netlogo_router, "_MODELS_ROOT", tmp_path)
    monkeypatch.setattr(netlogo_router, "_UPLOADS_ROOT", uploads)
    monkeypatch.setattr(netlogo_router, "_REPO_ROOT", tmp_path.parent)

    # Create a tiny valid-looking upload relative to the patched roots.
    content = b"globals []\nto setup\nend\nto go\nend\n"
    res = client.post(
        "/api/netlogo/upload",
        files={"file": ("demo_model.nlogo", content, "application/octet-stream")},
    )
    assert res.status_code == 200, res.text
    model = res.json()["model"]
    assert model["name"] == "demo_model.nlogo"
    assert model["source"] == "upload"
    assert (uploads / "demo_model.nlogo").is_file()


def test_upload_rejects_bad_extension():
    res = client.post(
        "/api/netlogo/upload",
        files={"file": ("evil.txt", b"nope", "text/plain")},
    )
    assert res.status_code == 400
