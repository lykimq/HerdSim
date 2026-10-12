"""Pytest fixtures and marker registration for HerdSim tests."""

from __future__ import annotations


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "stress: heavier / longer runs (included in make test)",
    )
