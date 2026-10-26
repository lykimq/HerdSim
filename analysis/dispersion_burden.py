"""Analyzes Total Dispersion Burden (S0 x N) and classifies failure regimes.

Extracts empirical data from existing HerdSim campaign results without re-running simulations:
1. Computes initial spreadness S0 (mean flock extent at start) for each layout and flock size N.
2. Evaluates the composite metric B_disp = S0 x N.
3. Classifies failed trials into:
   - Structural Gather Failures (final_gcm_goal > 2 * goal_radius): pack stalled during gathering.
   - Boundary / Temporal Failures (final_gcm_goal <= 2 * goal_radius): flock reached pen vicinity
     but timed out due to marginal boundary stragglers.
4. Tabulates failure breakdowns across deadlines and success criteria.
"""

from __future__ import annotations

import argparse
from collections.abc import Mapping
from pathlib import Path
from typing import Any, cast

import pandas as pd

from .results import markdown, read_trials

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"

CAMPAIGNS: Mapping[str, str] = {
    "dmin_m12": "100% Containment, 12x Drive Time",
    "dmin_m6": "100% Containment, 6x Drive Time",
    "dmin_m3": "100% Containment, 3x Drive Time",
    "dmin_f99_m12": "99% Arrival, 12x Drive Time",
    "dmin_f99_m6": "99% Arrival, 6x Drive Time",
    "dmin_f99_m3": "99% Arrival, 3x Drive Time",
}


def load_campaign_trials(campaign: str, results_dir: Path = RESULTS_DIR) -> pd.DataFrame:
    """Loads trials.csv for a campaign, returning a cleaned DataFrame."""
    folder = results_dir / campaign
    if not (folder / "trials.csv").exists():
        raise FileNotFoundError(f"Missing results file: {folder / 'trials.csv'}")
    return read_trials(folder)


def analyze_failure_regimes(df: pd.DataFrame) -> dict[str, Any]:
    """Computes failure breakdown into Structural Gather vs Boundary/Temporal."""
    failed = df[~df["success"]].copy()
    if failed.empty:
        return {"total_failed": 0, "structural": 0, "boundary": 0, "pct_structural": 0.0}

    is_boundary = failed["final_gcm_goal"] <= (2.0 * failed["goal_radius"])
    boundary_count = is_boundary.sum()
    structural_count = (~is_boundary).sum()
    total_failed = len(failed)

    return {
        "total_failed": total_failed,
        "structural": structural_count,
        "boundary": boundary_count,
        "pct_structural": 100.0 * structural_count / total_failed,
        "pct_boundary": 100.0 * boundary_count / total_failed,
    }


def compute_dispersion_burdens(df: pd.DataFrame) -> pd.DataFrame:
    """Computes characteristic S0 and dispersion burden B_disp = S0 x N per (layout, N)."""
    records: list[dict[str, Any]] = []
    for (layout, n), group in df.groupby(["initial_layout", "n_sheep"], sort=True):
        s0 = float(group["min_extent"].mean())
        n_int = cast(int, n)
        burden = s0 * n_int
        sr = float(group["success"].mean())

        records.append({
            "layout": str(layout),
            "n": n_int,
            "s0": s0,
            "dispersion_burden": burden,
            "overall_sr": sr,
        })
    return pd.DataFrame(records)


def run_full_dispersion_analysis(
    results_dir: Path = RESULTS_DIR,
    campaigns: Mapping[str, str] = CAMPAIGNS,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Runs complete analysis across all primary campaigns."""
    failure_rows: list[dict[str, Any]] = []
    dispersion_frames: list[pd.DataFrame] = []

    for camp_id, desc in campaigns.items():
        try:
            df = load_campaign_trials(camp_id, results_dir)
        except FileNotFoundError:
            continue

        stats = analyze_failure_regimes(df)
        failure_rows.append({
            "campaign": camp_id,
            "description": desc,
            "total_trials": len(df),
            **stats,
        })

        if camp_id == "dmin_m6":
            dispersion_frames.append(compute_dispersion_burdens(df))

    failure_df = pd.DataFrame(failure_rows)
    disp_df = dispersion_frames[0] if dispersion_frames else pd.DataFrame()
    return failure_df, disp_df


def format_failure_table(failure_df: pd.DataFrame) -> pd.DataFrame:
    """Formats raw failure regime metrics into a Markdown-ready table."""
    if failure_df.empty:
        return pd.DataFrame()
    return pd.DataFrame({
        "Protocol": failure_df["campaign"],
        "Description": failure_df["description"],
        "Failed": failure_df["total_failed"],
        "Structural": failure_df["structural"],
        "Boundary": failure_df["boundary"],
        "% Structural": failure_df["pct_structural"].map(lambda v: f"{v:.1f}%"),
    })


def format_dispersion_table(disp_df: pd.DataFrame) -> pd.DataFrame:
    """Formats raw dispersion burdens into a Markdown-ready table."""
    if disp_df.empty:
        return pd.DataFrame()
    return pd.DataFrame({
        "Layout": disp_df["layout"],
        "N": disp_df["n"],
        "S0 (m)": disp_df["s0"].map(lambda v: f"{v:.2f}"),
        "Burden S0 x N": disp_df["dispersion_burden"].map(lambda v: f"{v:.1f}"),
        "Success Rate": disp_df["overall_sr"].map(lambda v: f"{v * 100:.1f}%"),
    })


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze Dispersion Burden and Failure Regimes.")
    parser.parse_args()

    failure_df, disp_df = run_full_dispersion_analysis()

    print("### Failure Regime Breakdown across Campaigns\n")
    print(markdown(format_failure_table(failure_df)), "\n")

    if not disp_df.empty:
        print("### Dispersion Burden (S0 x N) by Layout and Flock Size (dmin_m6)\n")
        print(markdown(format_dispersion_table(disp_df)), "\n")


if __name__ == "__main__":
    main()
