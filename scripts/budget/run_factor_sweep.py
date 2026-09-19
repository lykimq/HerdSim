#!/usr/bin/env python3
"""CLI: information-factor sweeps for RQ5 (Cap I10)."""

from __future__ import annotations

import argparse
from pathlib import Path

from services.budget.layout import (
    CAMPAIGNS_DIR,
    copy_campaign_spec,
    load_campaign_spec,
    protocol_path_for_spec,
    resolve_campaign_output,
)
from services.budget.runner import BudgetCell, load_canonical_protocol, run_budget_grid


def main() -> None:
    parser = argparse.ArgumentParser(description="Run RQ5 information factor sweep")
    parser.add_argument(
        "--campaign",
        type=Path,
        default=None,
        help="Default: configs/budget/campaigns/phase5_factor_sweep.yaml",
    )
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--protocol", type=Path, default=None)
    parser.add_argument("--n", nargs="+", type=int, default=None)
    parser.add_argument("--d", nargs="+", type=int, default=None)
    parser.add_argument("--obs-modes", nargs="+", default=None)
    parser.add_argument("--seeds", type=int, default=None)
    parser.add_argument("--instrument", default=None)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--campaign-id", default=None)
    parser.add_argument("--no-resume", action="store_true")
    args = parser.parse_args()

    spec_path = args.campaign
    if spec_path is None:
        spec_path = CAMPAIGNS_DIR / "phase5_factor_sweep.yaml"
    elif not spec_path.is_absolute() and not spec_path.exists():
        candidate = CAMPAIGNS_DIR / spec_path.name
        if candidate.exists():
            spec_path = candidate
    spec = load_campaign_spec(spec_path) if spec_path.exists() else {}

    protocol_path = args.protocol
    if protocol_path is None and spec:
        protocol_path = protocol_path_for_spec(spec)
    protocol = load_canonical_protocol(protocol_path)

    output = args.output
    if output is None and spec:
        output = resolve_campaign_output(spec)
    if output is None:
        raise SystemExit("Provide --output or a campaign YAML with output")

    campaign_id = args.campaign_id or str(spec.get("campaign_id", "phase5_factor_sweep"))
    instrument = args.instrument or str(spec.get("instrument", "strombom_multi"))
    n_values = args.n or list(spec.get("flock_sizes") or [50, 100])
    d_values = args.d or list(spec.get("shepherd_counts") or [1, 2, 3, 4, 6, 10])
    obs_modes = args.obs_modes or list(
        spec.get("obs_modes") or ["bearing_only", "local_positions", "global"]
    )
    n_seeds = args.seeds if args.seeds is not None else int(spec.get("seeds", 10))
    layout = (list(spec.get("layouts") or ["compact"]) or ["compact"])[0]

    master = int(protocol.get("master_seed", 2026))
    max_ticks = int(protocol.get("time_limit_t0", 10000))
    seeds = [master + i for i in range(int(n_seeds))]
    cells: list[BudgetCell] = []
    for obs in obs_modes:
        for n in n_values:
            for d in d_values:
                for seed in seeds:
                    cells.append(
                        BudgetCell(
                            n_sheep=int(n),
                            n_shepherds=int(d),
                            seed=int(seed),
                            initial_layout=str(layout),
                            instrument=instrument,
                            obs_mode=str(obs),
                            max_ticks=max_ticks,
                        )
                    )

    if spec_path.exists():
        copy_campaign_spec(spec_path, output)

    store_ts = bool(spec.get("store_timeseries", False))
    trials = run_budget_grid(
        cells,
        output,
        protocol=protocol,
        campaign_id=campaign_id,
        max_workers=args.workers,
        store_timeseries=store_ts,
        resume=not args.no_resume,
    )
    print(f"Wrote {len(trials)} trial rows to {output / 'trials.csv'}")


if __name__ == "__main__":
    main()
