#!/usr/bin/env python3
"""CLI: run shepherding-budget N x D campaigns (Cap I1)."""

from __future__ import annotations

import argparse
from pathlib import Path

from api.budget_runner import (
    expand_budget_grid,
    load_canonical_protocol,
    run_budget_grid,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a shepherding budget grid")
    parser.add_argument(
        "--protocol",
        type=Path,
        default=None,
        help="Path to canonical_grid.yaml (default: configs/budget/canonical_grid.yaml)",
    )
    parser.add_argument("--output", type=Path, required=True, help="Output directory")
    parser.add_argument(
        "--instruments",
        nargs="+",
        default=None,
        help="Instruments to run (default: baseline_method from protocol)",
    )
    parser.add_argument(
        "--layouts",
        nargs="+",
        default=None,
        help="X0 families (default: protocol x0_families)",
    )
    parser.add_argument("--n", nargs="+", type=int, default=None, help="Flock sizes")
    parser.add_argument("--d", nargs="+", type=int, default=None, help="Shepherd counts")
    parser.add_argument(
        "--seeds",
        type=int,
        default=None,
        help="Override number of seeds",
    )
    parser.add_argument(
        "--seed-mode",
        choices=("scout", "claim"),
        default="scout",
        help="Use scout_seeds or claim_grade_seeds from protocol",
    )
    parser.add_argument("--workers", type=int, default=1, help="Process pool size")
    parser.add_argument(
        "--max-ticks",
        type=int,
        default=None,
        help="Override protocol time_limit_t0 per cell",
    )
    parser.add_argument(
        "--no-timeseries",
        action="store_true",
        help="Skip per-trial Parquet timeseries writes",
    )
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Ignore existing manifest and rerun all cells",
    )
    parser.add_argument("--campaign-id", default="budget_grid")
    args = parser.parse_args()

    protocol = load_canonical_protocol(args.protocol)
    cells = expand_budget_grid(
        protocol,
        instruments=args.instruments,
        layouts=args.layouts,
        n_values=args.n,
        d_values=args.d,
        n_seeds=args.seeds,
        seed_mode=args.seed_mode,
        max_ticks=args.max_ticks,
    )
    trials = run_budget_grid(
        cells,
        args.output,
        protocol=protocol,
        campaign_id=args.campaign_id,
        max_workers=args.workers,
        store_timeseries=not args.no_timeseries,
        resume=not args.no_resume,
    )
    print(f"Wrote {len(trials)} trial rows to {args.output / 'trials.csv'}")


if __name__ == "__main__":
    main()
