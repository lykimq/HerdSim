"""Pytest fixtures and marker registration for backend tests."""

from __future__ import annotations

import pytest

from tests.backend.helpers import make_state, make_world


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "stress: heavy / long runs; use make test-stress",
    )


@pytest.fixture
def sample_world():
    return make_world()


@pytest.fixture
def sample_state(sample_world):
    sheep = [[50.0 + i, 50.0] for i in range(10)]
    return make_state(sheep, [[10.0, 10.0]], world=sample_world, seed=42)
