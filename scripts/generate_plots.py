#!/usr/bin/env python3
"""Generate scientific plots from HerdSim batch CSV output."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_success_rate(df: pd.DataFrame, out_dir: Path) -> None:
    """Plot success rate by algorithm."""
    plt.figure(figsize=(10, 6))
    if "success" in df.columns:
        sns.barplot(data=df, x="algorithm", y="success", errorbar=None)
        plt.title("Average Success Rate by Algorithm")
        plt.ylabel("Success Rate")
        plt.ylim(0, 1)
        plt.tight_layout()
        plt.savefig(out_dir / "success_rate.png")
        plt.close()


def plot_convergence(df: pd.DataFrame, out_dir: Path) -> None:
    """Plot time to goal (ticks) distribution by algorithm."""
    plt.figure(figsize=(10, 6))
    if "total_ticks" in df.columns and "success" in df.columns:
        # Only plot convergence for successful runs
        success_df = df[df["success"] == True]
        if not success_df.empty:
            sns.boxplot(data=success_df, x="algorithm", y="total_ticks")
            plt.title("Convergence Time (Ticks) for Successful Runs")
            plt.ylabel("Total Ticks to Success")
            plt.tight_layout()
            plt.savefig(out_dir / "convergence.png")
            plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="HerdSim scientific plot generator")
    parser.add_argument("--input", required=True, help="Batch CSV from run_batch.py")
    parser.add_argument("--outdir", default="results/plots", help="Output directory for plots")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    out_dir = Path(args.outdir)
    out_dir.mkdir(parents=True, exist_ok=True)

    sns.set_theme(style="whitegrid")

    print(f"Generating plots in {out_dir}...")
    plot_success_rate(df, out_dir)
    plot_convergence(df, out_dir)
    print("Done.")


if __name__ == "__main__":
    main()
