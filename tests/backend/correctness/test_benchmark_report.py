"""Tests for Analytics research report packages (CSV / JSON)."""

from __future__ import annotations

import pandas as pd
import pytest

from api.benchmark_aggregates import build_trial_metric_fields, control_efficiency
from api.benchmark_report import (
    HERDSIM_VERSION,
    build_report_package,
    report_to_csv,
    report_to_markdown,
)
from api.benchmark_runner import run_benchmark


def test_report_package_includes_provenance():
    payload = run_benchmark(
        algorithm_ids=["strombom"],
        scenario_id="drive_to_goal",
        seeds=[1],
        preset="paper",
        num_sheep=8,
        num_shepherds=1,
    )
    request = {
        "algorithm_ids": ["strombom"],
        "scenario_id": "drive_to_goal",
        "preset": "paper",
        "seeds": [1],
        "num_sheep": 8,
        "num_shepherds": 1,
    }
    package = build_report_package(payload, request=request)
    assert package["herdsim_version"] == HERDSIM_VERSION
    assert "git_commit" in package
    assert package["python_version"]
    assert package["experiment"]["scenario_id"] == "drive_to_goal"
    assert package["experiment"]["seeds"] == [1]
    assert package["experiment"]["resolved_config"] is not None
    assert "measurement_radius" in package["experiment"]["resolved_config"]
    assert package["metric_definitions"]
    assert package["caveats"]
    assert package["rows"]
    assert package["summary"]
    row = package["rows"][0]
    assert "auc_cohesion" in row
    assert "control_efficiency" in row
    assert "cohesion" not in row
    assert "failure_rate" in package["summary"][0]


def test_csv_export_includes_caveats_and_columns():
    payload = {
        "rows": [
            {
                "algorithm": "strombom",
                "scenario": "drive_to_goal",
                "preset": "paper",
                "seed": 1,
                "n_sheep": 8,
                "n_shepherds": 1,
                "success": True,
                "total_ticks": 10,
                "first_success_tick": 10.0,
                "auc_cohesion": 1.0,
                "shepherd_path": 5.0,
                "resolved_config": {"n_sheep": 8},
            }
        ],
        "summary": [],
    }
    text = report_to_csv(payload, request={"scenario_id": "drive_to_goal", "preset": "paper"})
    assert text.startswith(f"# HerdSim benchmark CSV (version {HERDSIM_VERSION})")
    assert "# git_commit:" in text
    assert "# caveat:" in text
    assert "algorithm" in text
    assert "first_success_tick" in text
    assert "resolved_config" not in text.split("\n")[-1]


def test_markdown_export_shares_caveats():
    payload = {
        "rows": [{"algorithm": "strombom", "scenario": "drive_to_goal", "seed": 1}],
        "summary": [
            {
                "algorithm": "strombom",
                "trials": 1,
                "success_rate": 1.0,
                "failure_rate": 0.0,
                "mean_ticks_success": 10,
                "median_ticks_success": 10,
                "iqr_ticks_success": 0.0,
                "mean_auc_cohesion": 1.0,
                "mean_auc_fragmentation": 1.0,
                "mean_shepherd_path": 5.0,
                "mean_control_efficiency": 0.1,
                "mean_final_gcm_goal": 2.0,
            }
        ],
    }
    md = report_to_markdown(payload)
    assert "HerdSim benchmark report" in md
    assert "Caveats" in md
    assert "strombom" in md


def test_first_success_tick_matches_scenario_success_not_time_to_goal():
    """Successful trials set first_success_tick from scenario stop, not all-in-goal."""
    payload = run_benchmark(
        algorithm_ids=["strombom"],
        scenario_id="drive_to_goal",
        seeds=[1],
        preset="paper",
        num_sheep=8,
        num_shepherds=1,
    )
    row = payload["rows"][0]
    assert "first_success_tick" in row
    if row["success"]:
        assert row["first_success_tick"] == float(row["total_ticks"])
    else:
        assert row["first_success_tick"] == -1.0


def test_trial_aggregates_from_history():
    history = pd.DataFrame(
        {
            "tick": [0, 1, 2],
            "cohesion": [3.0, 2.0, 1.0],
            "gcm_goal": [10.0, 6.0, 4.0],
            "polarization": [0.2, 0.4, 0.6],
            "fragmentation": [1.0, 0.5, 1.0],
            "outlier_count": [2.0, 1.0, 0.0],
            "shepherd_path": [0.0, 5.0, 10.0],
            "success_rate": [0.0, 0.5, 1.0],
            "sheep_in_goal": [0.0, 2.0, 4.0],
            "time_to_goal": [-1.0, -1.0, 2.0],
            "min_separation": [1.0, 1.0, 1.0],
        }
    )
    fields = build_trial_metric_fields(history)
    assert fields["mean_cohesion"] == pytest.approx(2.0)
    assert fields["auc_cohesion"] == pytest.approx(2.0)
    assert fields["final_gcm_goal"] == pytest.approx(4.0)
    assert fields["control_efficiency"] == pytest.approx(
        control_efficiency(10.0, 4.0, 10.0)
    )
    assert "cohesion" not in fields
