"""Tests for Analytics param-grid sweep helpers and runner."""

from __future__ import annotations

import pandas as pd
import pytest

from api.benchmark_runner import run_benchmark
from api.benchmark_summary import summarize_rows
from api.benchmark_sweep import expand_param_grid, parse_sweep_specs, sweep_label


def test_parse_and_expand_param_grid():
    specs = parse_sweep_specs(
        [
            {"key": "n_neighbors", "values": [1, 5]},
            {"key": "rs_weight", "values": [1.0]},
        ]
    )
    grid = expand_param_grid(specs)
    assert grid == [
        {"n_neighbors": 1, "rs_weight": 1.0},
        {"n_neighbors": 5, "rs_weight": 1.0},
    ]
    assert sweep_label(grid[0]) == "n_neighbors=1, rs_weight=1"


def test_parse_sweep_rejects_more_than_two_params():
    with pytest.raises(ValueError, match="at most 2"):
        parse_sweep_specs(
            [
                {"key": "a", "values": [1]},
                {"key": "b", "values": [2]},
                {"key": "c", "values": [3]},
            ]
        )


def test_run_benchmark_param_sweep_labels_rows():
    payload = run_benchmark(
        algorithm_ids=["strombom"],
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
    assert all("[" in row["algorithm"] for row in summary)
