#!/usr/bin/env python3
"""CLI: analyse completed budget campaigns into packages A-G."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from analysis.budget.early_warning import evaluate_early_warning, summarise_early_warning
from analysis.budget.export import export_package_a, export_package_dossier
from analysis.budget.frontier import extract_frontier
from analysis.budget.mechanism import evaluate_overcrowding_mechanisms
from analysis.budget.predictors import compare_state_vs_nd_predictors
from analysis.budget.regimes import label_regimes
from analysis.budget.scaling import fit_scaling_models
from analysis.budget.substitution import substitution_curves, summarize_substitution
from analysis.budget.transfer import build_transfer_table
from api.budget_runner import load_canonical_protocol


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyse budget campaign outputs")
    parser.add_argument("--trials", type=Path, required=True, help="trials.csv path")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--protocol", type=Path, default=None)
    parser.add_argument(
        "--package",
        choices=list("ABCDEFG"),
        default="A",
        help="Evidence package to export",
    )
    parser.add_argument("--theta", type=float, default=0.90)
    parser.add_argument("--baseline", default="strombom_multi")
    parser.add_argument(
        "--trials-by-method",
        nargs="*",
        default=None,
        help="Optional method=path pairs for Package D transfer",
    )
    args = parser.parse_args()

    protocol = load_canonical_protocol(args.protocol)
    trials = pd.read_csv(args.trials)
    args.output.mkdir(parents=True, exist_ok=True)

    if args.package == "A":
        export_package_a(
            trials,
            args.output,
            protocol=protocol,
            theta=args.theta,
            group_cols=["initial_layout"] if "initial_layout" in trials.columns else None,
        )
    elif args.package == "B":
        frontier = extract_frontier(
            trials,
            theta=args.theta,
            group_cols=["initial_layout"] if "initial_layout" in trials.columns else None,
        )
        pred = compare_state_vs_nd_predictors(trials)
        export_package_dossier(
            "B",
            {
                "frontier_by_layout": frontier,
                "predictor_comparison": pd.DataFrame([pred]),
            },
            args.output,
            protocol=protocol,
            campaign_id="package_b",
            notes=[
                "RQ1 state vs size: compare d_min across initial_layout.",
                f"Predictor prefers_state={pred.get('prefers_state')} "
                f"delta_aic={pred.get('delta_aic')}",
            ],
        )
    elif args.package == "C":
        regimes = label_regimes(trials, theta=args.theta)
        mech = evaluate_overcrowding_mechanisms(trials, regimes)
        mech_rows = []
        for hyp, payload in mech.get("overall", {}).items():
            row = {"hypothesis": hyp}
            if isinstance(payload, dict):
                row.update(payload)
            mech_rows.append(row)
        export_package_dossier(
            "C",
            {
                "regimes": regimes,
                "mechanism_summary": pd.DataFrame(mech_rows),
                "mechanism_by_n": pd.DataFrame(mech.get("by_n") or []),
            },
            args.output,
            protocol=protocol,
            campaign_id="package_c",
            notes=[json.dumps(mech, default=str)],
        )
    elif args.package == "D":
        by_method: dict[str, pd.DataFrame] = {}
        if args.trials_by_method:
            for item in args.trials_by_method:
                method, path = item.split("=", 1)
                by_method[method] = pd.read_csv(path)
        else:
            if "instrument" not in trials.columns:
                raise SystemExit("Package D needs instrument column or --trials-by-method")
            for method, g in trials.groupby("instrument"):
                by_method[str(method)] = g
        table = build_transfer_table(by_method, baseline=args.baseline, theta=args.theta)
        export_package_dossier(
            "D",
            {"transfer_table": table},
            args.output,
            protocol=protocol,
            campaign_id="package_d",
        )
    elif args.package == "E":
        curves = substitution_curves(trials, theta=args.theta)
        summary = summarize_substitution(curves)
        export_package_dossier(
            "E",
            {
                "substitution_curves": curves,
                "substitution_summary": pd.DataFrame([summary]),
            },
            args.output,
            protocol=protocol,
            campaign_id="package_e",
        )
    elif args.package == "F":
        frontier = extract_frontier(trials, theta=args.theta)
        fits = fit_scaling_models(frontier)
        export_package_dossier(
            "F",
            {
                "frontier": frontier.drop(columns=["rates"], errors="ignore"),
                "scaling_fits": pd.DataFrame(
                    [
                        {"model": name, **vals}
                        for name, vals in fits.get("models", {}).items()
                    ]
                ),
            },
            args.output,
            protocol=protocol,
            campaign_id="package_f",
            notes=[f"best_model={fits.get('best')}"],
        )
    elif args.package == "G":
        ts_dir = args.trials.parent / "timeseries"
        results = []
        if ts_dir.exists():
            for path in sorted(ts_dir.glob("*.parquet")) + sorted(ts_dir.glob("*.csv")):
                ts = pd.read_parquet(path) if path.suffix == ".parquet" else pd.read_csv(path)
                # Infer success from matching trial row when possible.
                success = False
                results.append(evaluate_early_warning(ts, success=success))
        summary = summarise_early_warning(results)
        export_package_dossier(
            "G",
            {"early_warning_summary": pd.DataFrame([summary])},
            args.output,
            protocol=protocol,
            campaign_id="package_g",
            notes=[json.dumps(summary)],
        )
    print(f"Package {args.package} written to {args.output}")


if __name__ == "__main__":
    main()
