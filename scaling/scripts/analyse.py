#!/usr/bin/env python3
"""CLI: analyse completed scaling protocols into packages A-G."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd

from analysis.scaling.early_warning import evaluate_early_warning, summarise_early_warning
from analysis.scaling.export import export_package_a, export_package_dossier
from analysis.scaling.frontier import extract_frontier
from analysis.scaling.mechanism import evaluate_overcrowding_mechanisms
from analysis.scaling.predictors import compare_state_vs_nd_predictors
from analysis.scaling.regimes import label_regimes
from analysis.scaling.fits import fit_scaling_models
from analysis.scaling.substitution import substitution_curves, summarize_substitution
from analysis.scaling.transfer import build_transfer_table
from services.scaling.layout import protocol_id_from_dir, package_output_dir
from services.scaling.runner import load_canonical_protocol

_CELL_BASE = re.compile(
    r"^N(?P<N>\d+)_D(?P<D>\d+)_L(?P<L>[^_]+)_S(?P<S>\d+)_I(?P<rest>.+)$"
)


def _parse_timeseries_stem(stem: str) -> dict[str, object] | None:
    m = _CELL_BASE.match(stem)
    if m is None:
        return None
    rest = m.group("rest")
    obs_mode = None
    method = rest
    if "_O" in rest:
        method, after = rest.split("_O", 1)
        obs_mode = after.split("_R", 1)[0].split("_C", 1)[0]
    return {
        "n_sheep": int(m.group("N")),
        "n_shepherds": int(m.group("D")),
        "initial_layout": m.group("L"),
        "seed": int(m.group("S")),
        "method": method,
        "obs_mode": obs_mode,
    }


def _resolve_protocol_id(trials_path: Path, override: str | None) -> str:
    if override:
        return override
    protocol_yaml = trials_path.parent / "protocol.yaml"
    if protocol_yaml.exists():
        try:
            import yaml

            spec = yaml.safe_load(protocol_yaml.read_text()) or {}
            if isinstance(spec, dict) and spec.get("protocol_id"):
                return str(spec["protocol_id"])
        except Exception:
            pass
    return protocol_id_from_dir(trials_path.parent)


def _success_for_timeseries(stem: str, trials: pd.DataFrame) -> bool:
    """Match a timeseries stem to a trials.csv row when possible."""
    parsed = _parse_timeseries_stem(stem)
    if parsed is None or trials.empty:
        return False
    q = trials
    for col in ("n_sheep", "n_shepherds", "seed", "initial_layout", "method"):
        if col in q.columns:
            q = q[q[col] == parsed[col]]
    if parsed.get("obs_mode") is not None and "obs_mode" in q.columns:
        q = q[q["obs_mode"] == parsed["obs_mode"]]
    if q.empty or "success" not in q.columns:
        return False
    return bool(q.iloc[0]["success"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyse scaling protocol outputs")
    parser.add_argument("--trials", type=Path, required=True, help="trials.csv path")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Package output dir (default: <protocol>/packages/<letter>)",
    )
    parser.add_argument("--protocol", type=Path, default=None)
    parser.add_argument(
        "--package",
        choices=list("ABCDEFG"),
        default="A",
        help="Evidence package to export",
    )
    parser.add_argument("--theta", type=float, default=0.90)
    parser.add_argument("--baseline", default="strombom_multi")
    parser.add_argument("--protocol-id", default=None)
    parser.add_argument(
        "--trials-by-method",
        nargs="*",
        default=None,
        help="Optional method=path pairs for Package D transfer",
    )
    args = parser.parse_args()

    protocol = load_canonical_protocol(args.protocol)
    trials = pd.read_csv(args.trials)
    protocol_id = _resolve_protocol_id(args.trials, args.protocol_id)
    output = args.output
    if output is None:
        output = package_output_dir(args.trials.parent, args.package)
    output.mkdir(parents=True, exist_ok=True)

    if args.package == "A":
        export_package_a(
            trials,
            output,
            protocol=protocol,
            protocol_id=protocol_id,
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
            output,
            protocol=protocol,
            protocol_id=protocol_id,
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
            output,
            protocol=protocol,
            protocol_id=protocol_id,
            notes=[json.dumps(mech, default=str)],
        )
    elif args.package == "D":
        by_method: dict[str, pd.DataFrame] = {}
        if args.trials_by_method:
            for item in args.trials_by_method:
                method, path = item.split("=", 1)
                by_method[method] = pd.read_csv(path)
        else:
            if "method" not in trials.columns:
                raise SystemExit("Package D needs method column or --trials-by-method")
            for method, g in trials.groupby("method"):
                by_method[str(method)] = g
        table = build_transfer_table(by_method, baseline=args.baseline, theta=args.theta)
        export_package_dossier(
            "D",
            {"transfer_table": table},
            output,
            protocol=protocol,
            protocol_id=protocol_id,
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
            output,
            protocol=protocol,
            protocol_id=protocol_id,
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
            output,
            protocol=protocol,
            protocol_id=protocol_id,
            notes=[f"best_model={fits.get('best')}"],
        )
    elif args.package == "G":
        ts_dir = args.trials.parent / "timeseries"
        results = []
        if ts_dir.exists():
            paths = sorted(ts_dir.glob("*.parquet")) + sorted(ts_dir.glob("*.csv"))
            for path in paths:
                ts = (
                    pd.read_parquet(path)
                    if path.suffix == ".parquet"
                    else pd.read_csv(path)
                )
                success = _success_for_timeseries(path.stem, trials)
                results.append(evaluate_early_warning(ts, success=success))
        summary = summarise_early_warning(results)
        export_package_dossier(
            "G",
            {"early_warning_summary": pd.DataFrame([summary])},
            output,
            protocol=protocol,
            protocol_id=protocol_id,
            notes=[json.dumps(summary)],
        )
    print(f"Package {args.package} written to {output}")


if __name__ == "__main__":
    main()
