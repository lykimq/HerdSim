"""API docs whitelist serves Guide markdown."""

from pathlib import Path

from fastapi.testclient import TestClient

from api.main import app
from api.routers.docs import DOC_SLUGS

client = TestClient(app)


def test_docs_list_and_fetch_algorithms_overview():
    listed = client.get("/api/docs")
    assert listed.status_code == 200
    slugs = {d["slug"] for d in listed.json()["docs"]}
    assert "research/algorithms" in slugs
    assert "guide" not in slugs
    res = client.get("/api/docs/research/algorithms")
    assert res.status_code == 200
    assert "Algorithms" in res.text
    assert "text/markdown" in res.headers.get("content-type", "")


def test_docs_unknown_slug_404():
    res = client.get("/api/docs/developer/architecture")
    assert res.status_code == 404


def test_whitelisted_paths_exist_or_are_known():
    # Core pages must exist; new algorithm pages may be added with the plugin.
    for slug in ("research/algorithms", "research/scenarios", "research/algorithms/strombom_2014"):
        path = DOC_SLUGS[slug]
        assert path.is_file(), path
