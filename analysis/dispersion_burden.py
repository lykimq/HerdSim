"""Analyzes Total Dispersion Burden (S0 x N) and classifies failure regimes.

Extracts empirical data from existing HerdSim campaign results without re-running simulations.
1. Computes initial spreadness S0 (mean flock extent at start) for each layout and flock size N.
2. Evaluates the composite metric B_disp = S0 x N.
3. Classifies all failed trials into:
   - Structural Gather Failures (final_gcm_goal > 2 * goal_radius): pack stalled during gathering.
   - Boundary / Temporal Failures (final_gcm_goal <= 2 * goal_radius): flock reached pen vicinity
     but timed out due to marginal boundary stragglers.
4. Tabulates failure breakdowns across deadlines (3x, 6x, 12x) and success criteria (100% vs 99%).
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"

CAMPAIGNS = {
    "dmin_m12": "100% Containment, 12x Drive Time",
    "dmin_m6": "100% Containment, 6x Drive Time",
    "dmin_m3": "100% Containment, 3x Drive Time",
    "dmin_f99_m12": "99% Arrival, 12x Drive Time",
    "dmin_f99_m6": "99% Arrival, 6x Drive Time",
    "dmin_f99_m3": "99% Arrival, 3x Drive Time",
}


def load_campaign_trials(campaign: str) -> pd.DataFrame:
    """Loads trials.csv for a campaign, returning a cleaned DataFrame."""
    path = RESULTS_DIR / campaign / "trials.csv"
    if not path.exists():
        raise FileNotFoundError(f"Missing results file: {path}")
    return pd.read_csv(path, comment="#", low_memory=False)



def analyze_failure_regimes(df: pd.DataFrame) -> dict[str, Any]:
    """Computes failure breakdown into Structural Gather vs Boundary/Temporal."""
    failed = df[~df["success"]].copy()
    if failed.empty:
        return {"total_failed": 0, "structural": 0, "boundary": 0, "pct_structural": 0.0}

    is_boundary = failed["final_gcm_goal"] <= (2.0 * failed["goal_radius"])
    boundary_count = int(is_boundary.sum())
    structural_count = int((~is_boundary).sum())
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
        # Initial extent is closely mirrored by min_extent or flock_radius
        # We compute mean flock_radius or min_extent as proxy for initial spreadness S0
        s0 = float(group["min_extent"].mean())
        n_int = int(str(n))
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


def run_full_dispersion_analysis() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Runs complete analysis across all primary campaigns."""
    failure_rows: list[dict[str, Any]] = []
    dispersion_frames: list[pd.DataFrame] = []

    for camp_id, desc in CAMPAIGNS.items():
        try:
            df = load_campaign_trials(camp_id)
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze Dispersion Burden and Failure Regimes.")
    parser.parse_args()

    print("=" * 80)
    print("HerdSim Macro-Analysis: Dispersion Burden (S0 x N) and Failure Taxonomy")
    print("=" * 80)

    failure_df, disp_df = run_full_dispersion_analysis()

    print("\n### 1. Phân loại Cơ cấu Thất bại (Failure Regime Breakdown across Campaigns)")
    print("-" * 80)
    fmt = "{:<14} | {:<32} | {:>7} | {:>10} | {:>10} | {:>10}"
    print(fmt.format("Protocol", "Mô tả", "Thất bại", "Cấu trúc", "Ranh giới", "% Cấu trúc"))
    print("-" * 95)
    for _, r in failure_df.iterrows():
        line = (
            f"{r['campaign']:<14} | {r['description']:<32} | {r['total_failed']:7d} | "
            + f"{r['structural']:10d} | {r['boundary']:10d} | {r['pct_structural']:9.1f}%"
        )
        print(line)

    if not disp_df.empty:
        print("\n### 2. Tải trọng Tản mác S0 x N theo Bố cục và Quy mô đàn (dmin_m6)")
        print("-" * 80)
        fmt2 = "{:<12} | {:>5} | {:>12} | {:>18} | {:>12}"
        print(fmt2.format("Bố cục", "N", "S0 (m)", "Tải trọng S0 x N", "Tỷ lệ Thắng"))
        print("-" * 70)
        for _, r in disp_df.iterrows():
            line2 = (
                f"{r['layout']:<12} | {int(str(r['n'])):5d} | {r['s0']:10.2f} m | "
                + f"{r['dispersion_burden']:16.1f} | {r['overall_sr'] * 100:10.1f}%"
            )
            print(line2)



if __name__ == "__main__":
    main()
