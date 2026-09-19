"""Pytest fixtures and marker registration for backend tests."""

from __future__ import annotations


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "stress: heavy / long runs; use make test-stress",
    )
