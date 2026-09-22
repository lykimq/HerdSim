"""Tests for factor-grid helpers and runner."""

from __future__ import annotations

import pandas as pd
import pytest
from services.experiments.runner import run_benchmark
from services.experiments.summary import summarize_rows
from services.experiments.sweep import expand_factor_grid, parse_factor_specs, sweep_label

from core.experimental_factors import MAX_FACTOR_GRID_CELLS


def test_parse_and_expand_param_grid():
    specs = parse_factor_specs(
        [
            {"key": "n_neighbors", "values": [1, 5]},
            {"key": "rs_weight", "values": [1.0]},
        ]
    )
    grid = expand_factor_grid(specs)
    assert grid == [
        {"n_neighbors": 1, "rs_weight": 1.0},
        {"n_neighbors": 5, "rs_weight": 1.0},
    ]
    assert sweep_label(grid[0]) == "n_neighbors=1, rs_weight=1"


def test_parse_sweep_rejects_oversized_grid():
    with pytest.raises(ValueError, match="max is"):
        expand_factor_grid(
            [
                {"key": "n_sheep", "values": list(range(MAX_FACTOR_GRID_CELLS + 1))},
            ]
        )


def test_run_benchmark_param_sweep_labels_rows():
    payload = run_benchmark(
        methods=["strombom"],
        scenario_id="drive_to_goal",
        seeds=[1],
        preset="paper",
        sweep=[{"key": "n_neighbors", "values": [-1, 2]}],
        num_sheep=8,
        num_shepherds=1,
    )
    assert len(payload["rows"]) == 2
    labels = {row["sweep_label"] for row in payload["rows"]}
    assert labels == {"n_neighbors=-1", "n_neighbors=2"}
    summary = summarize_rows(pd.DataFrame(payload["rows"]))
    assert len(summary) == 2
    assert all("[" in row["method"] for row in summary)


def test_find_preset_for_models_prefers_canonical():
    from core.methods import find_method_for_models

    assert find_method_for_models("strombom", "collect_drive") == "strombom"
    assert find_method_for_models("kubo", "kubo_forces") == "kubo"
    assert find_method_for_models("jadhav", "fat") is None


def test_run_benchmark_factor_grid_without_method_uses_param_bundle():
    payload = run_benchmark(
        methods=[],
        scenario_id="drive_to_goal",
        seeds=[1],
        preset="custom",
        sweep=[
            {"key": "sheep_model", "values": ["strombom"]},
            {"key": "dog_controller", "values": ["collect_drive"]},
            {"key": "n_sheep", "values": [8]},
            {"key": "n_shepherds", "values": [1]},
        ],
    )
    assert len(payload["rows"]) == 1
    row = payload["rows"][0]
    assert row["sheep_model"] == "strombom"
    assert row["dog_controller"] == "collect_drive"
    assert row["method"] == "strombom"
    assert row["sweep_label"]
    assert "n_sheep=8" in row["sweep_label"]


def test_run_benchmark_factor_grid_without_models_rejected():
    with pytest.raises(ValueError, match="sheep_model"):
        run_benchmark(
            methods=[],
            scenario_id="drive_to_goal",
            seeds=[1],
            preset="custom",
            sweep=[{"key": "n_sheep", "values": [8, 16]}],
        )
