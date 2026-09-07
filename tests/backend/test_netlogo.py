"""Tests for NetLogo path helpers and model files (desktop launcher support)."""

from __future__ import annotations

from pathlib import Path

import pytest

from algorithms.netlogo.bridge import (
    find_netlogo_gui_launcher,
    find_netlogo_home,
    resolve_model_path,
)
from algorithms.registry import algorithm_registry


def test_netlogo_not_registered_as_herdsim_algorithm():
    assert "netlogo" not in algorithm_registry.names()


def test_example_model_exists():
    path = resolve_model_path("netlogo/models/example.nlogo")
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "to setup" in text
    assert "to go" in text


def test_resolve_model_path_prefers_repo_root():
    path = resolve_model_path("netlogo/models/example.nlogo")
    assert path.name == "example.nlogo"
    assert path.is_file()


def test_find_netlogo_home_detects_local_install():
    home = find_netlogo_home()
    if home is None:
        pytest.skip("NetLogo is not installed on this machine")
    assert Path(home).is_dir()
    launcher = find_netlogo_gui_launcher(home)
    assert launcher is not None
    assert launcher.is_file()
