"""The start spread of the flock times N, and how the failed drives failed.

    uv run cli/dmin_tables.py dispersion

Two readings of the finished main drive runs, both from trials.csv:

- S0 x N, the dispersion burden of a layout at one flock size: S0 is the flock's extent (RMS
  radius) at the start, read from the ``max_extent`` column as the start extent. That holds
  where the dogs only gather the flock; on compact the flock first spreads, so the maximum
  is above the start (1.08 times on average, up to 1.26, over the 135 stored dmin_m6 compact
  histories; at N = 400 the start is 7.92 m and the maximum 8.30 m). The burden grows with N
  on the scattered layouts and barely on the compact one
- which of two regimes a failed trial belongs to, by where the flock ended only: boundary or
  temporal when it ended within ``NEAR_GOAL_RADII`` goal radii of the goal centre, structural
  when it ended farther away. The rule does not say whether the flock was ever gathered: in
  dmin_f99_m6, 881 of 1067 far failures had 90% or more of the flock in the goal at some tick
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any, cast

import pandas as pd

from .results import read_trials

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
NEAR_GOAL_RADII = 2.0

# The runs read, with the rule each ran under.
CAMPAIGNS: Mapping[str, str] = {
    "dmin_m12": "100% containment, 12x drive time",
    "dmin_m6": "100% containment, 6x drive time",
    "dmin_m3": "100% containment, 3x drive time",
    "dmin_f99_m12": "99% arrival, 12x drive time",
    "dmin_f99_m6": "99% arrival, 6x drive time",
    "dmin_f99_m3": "99% arrival, 3x drive time",
}
# The run whose start spreads are tabulated; the layouts are the same in every run.
BURDEN_CAMPAIGN = "dmin_m6"


def load_campaign_trials(campaign: str, results_dir: Path = RESULTS_DIR) -> pd.DataFrame:
    folder = results_dir / campaign
    if not (folder / "trials.csv").exists():
        raise FileNotFoundError(f"Missing results file: {folder / 'trials.csv'}")
    return read_trials(folder)


def analyze_failure_regimes(df: pd.DataFrame) -> dict[str, Any]:
    """Counts of the failed trials in each regime, and their shares in percent."""
    failed = df[~df["success"]]
    if failed.empty:
        return {"total_failed": 0, "structural": 0, "boundary": 0, "pct_structural": 0.0}
    near = failed["final_gcm_goal"] <= NEAR_GOAL_RADII * failed["goal_radius"]
    boundary, structural = int(near.sum()), int((~near).sum())
    return {
        "total_failed": len(failed),
        "structural": structural,
        "boundary": boundary,
        "pct_structural": 100.0 * structural / len(failed),
        "pct_boundary": 100.0 * boundary / len(failed),
    }


def compute_dispersion_burdens(df: pd.DataFrame) -> pd.DataFrame:
    """Per (layout, N): the start extent S0, the burden S0 x N and the success rate over
    every D and seed."""
    records: list[dict[str, Any]] = []
    for (layout, n), group in df.groupby(["initial_layout", "n_sheep"], sort=True):
        s0 = float(group["max_extent"].mean())
        n_int = cast(int, n)
        records.append(
            {
                "layout": str(layout),
                "n": n_int,
                "s0": s0,
                "dispersion_burden": s0 * n_int,
                "overall_sr": float(group["success"].mean()),
            }
        )
    return pd.DataFrame(records)


def run_full_dispersion_analysis(
    results_dir: Path = RESULTS_DIR,
    campaigns: Mapping[str, str] = CAMPAIGNS,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(failure regimes per run, dispersion burdens of BURDEN_CAMPAIGN); runs whose folder
    is missing are skipped."""
    failure_rows: list[dict[str, Any]] = []
    burdens = pd.DataFrame()
    for campaign, description in campaigns.items():
        try:
            df = load_campaign_trials(campaign, results_dir)
        except FileNotFoundError:
            continue
        stats = analyze_failure_regimes(df)
        failure_rows.append(
            {"campaign": campaign, "description": description, "total_trials": len(df), **stats}
        )
        if campaign == BURDEN_CAMPAIGN:
            burdens = compute_dispersion_burdens(df)
    return pd.DataFrame(failure_rows), burdens
