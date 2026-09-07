#!/usr/bin/env python3
"""Build a markdown comparison report from batch CSV output."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="HerdSim markdown report exporter")
    parser.add_argument("--input", required=True, help="Batch CSV from run_batch.py")
    parser.add_argument("--out", default="results/report.md")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    lines = [
        "# HerdSim Batch Report",
        "",
        f"- rows: {len(df)}",
        f"- algorithms: {', '.join(sorted(df['algorithm'].astype(str).unique()))}",
        f"- scenarios: {', '.join(sorted(df['scenario'].astype(str).unique()))}",
        "",
        "## Summary by Algorithm",
        "",
    ]

    if "success" in df.columns:
        grouped = df.groupby("algorithm")["success"].mean()
        for alg, rate in grouped.items():
            lines.append(f"- {alg}: success_rate={rate:.2f}")

    lines.extend([
        "", 
        "## Scientific Analysis",
        "![Success Rate](plots/success_rate.png)",
        "",
        "![Convergence Time](plots/convergence.png)",
        "",
        "## Raw Table", 
        "", 
        "```", 
        df.to_string(index=False), 
        "```", 
        ""
    ])

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
