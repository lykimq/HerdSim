#!/usr/bin/env python3
"""CLI: information-factor sweeps for RQ5 (Cap I10)."""

from __future__ import annotations

import argparse
from pathlib import Path

from api.budget_runner import BudgetCell, load_canonical_protocol, run_budget_grid


def main() -> None:
    parser = argparse.ArgumentParser(description="Run RQ5 information factor sweep")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--protocol", type=Path, default=None)
    parser.add_argument("--n", nargs="+", type=int, default=[50, 100])
    parser.add_argument("--d", nargs="+", type=int, default=[1, 2, 3, 4, 6, 10])
    parser.add_argument(
        "--obs-modes",
        nargs="+",
        default=["bearing_only", "local_positions", "global"],
    )
    parser.add_argument("--seeds", type=int, default=10)
    parser.add_argument("--instrument", default="strombom_multi")
    parser.add_argument("--workers", type=int, default=1)
    args = parser.parse_args()

    protocol = load_canonical_protocol(args.protocol)
    master = int(protocol.get("master_seed", 2026))
    max_ticks = int(protocol.get("time_limit_t0", 10000))
    seeds = [master + i for i in range(args.seeds)]
    cells: list[BudgetCell] = []
    for obs in args.obs_modes:
        for n in args.n:
            for d in args.d:
                for seed in seeds:
                    cells.append(
                        BudgetCell(
                            n_sheep=int(n),
                            n_shepherds=int(d),
                            seed=int(seed),
                            instrument=args.instrument,
                            obs_mode=str(obs),
                            max_ticks=max_ticks,
                        )
                    )
    trials = run_budget_grid(
        cells,
        args.output,
        protocol=protocol,
        campaign_id="rq5_factor_sweep",
        max_workers=args.workers,
        store_timeseries=False,
    )
    print(f"Wrote {len(trials)} trial rows to {args.output / 'trials.csv'}")


if __name__ == "__main__":
    main()
