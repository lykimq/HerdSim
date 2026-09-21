#!/usr/bin/env python3
"""CLI: analyse completed scaling protocols into packages A-G."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd

from analysis.scaling.early_warning import (
    default_eval_ticks,
    evaluate_early_warning,
    evaluate_early_warning_campaign,
    summarise_early_warning,
)
from analysis.scaling.export import export_package_a, export_package_dossier
from analysis.scaling.frontier import extract_frontier
from analysis.scaling.mechanism import (
    evaluate_overcrowding_mechanisms,
    evaluate_temporal_order,
)
from analysis.scaling.predictors import compare_state_vs_nd_predictors
from analysis.scaling.regimes import label_regimes
from analysis.scaling.fits import fit_scaling_models
from analysis.scaling.substitution import (
    substitution_curves,
    substitution_curves_communication,
    substitution_curves_range,
    summarize_substitution,
)
from analysis.scaling.transfer import build_transfer_table, transfer_summary
from services.scaling.layout import protocol_id_from_dir, package_output_dir
from services.scaling.runner import load_canonical_protocol

_CELL_BASE = re.compile(
    r"^N(?P<N>\d+)_D(?P<D>\d+)_L(?P<L>[^_]+)_S(?P<S>\d+)_M(?P<rest>.+)$"
)


def _parse_timeseries_stem(stem: str) -> dict[str, object] | None:
    m = _CELL_BASE.match(stem)
    if m is None:
        return None
    rest = m.group("rest")
    method = rest
    obs_mode = None
    sensing_range = None
    communication = None
    if "_O" in rest:
        method, after = rest.split("_O", 1)
        parts = after.split("_")
        obs_mode = parts[0] if parts else after
        rem = after[len(obs_mode) :]
        if rem.startswith("_R"):
            rem = rem[2:]
            sensing_range = rem.split("_C", 1)[0]
            rem = rem[len(str(sensing_range)) :]
        if "_C" in (rem if rem else after):
            communication = (rem if rem.startswith("_C") else after).split("_C", 1)[-1]
    return {
        "n_sheep": int(m.group("N")),
        "n_shepherds": int(m.group("D")),
        "initial_layout": m.group("L"),
        "seed": int(m.group("S")),
        "method": method,
        "obs_mode": obs_mode,
        "sensing_range": float(sensing_range) if sensing_range else None,
        "communication": communication,
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


def _load_timeseries_trials(
    trials: pd.DataFrame,
    ts_dir: Path,
    regimes: pd.DataFrame | None = None,
) -> list[dict]:
    rows: list[dict] = []
    if not ts_dir.exists():
        return rows
    regime_map = {}
    if regimes is not None and not regimes.empty:
        for _, r in regimes.iterrows():
            regime_map[(int(r["n_sheep"]), int(r["n_shepherds"]))] = r.get("regime")
    paths = sorted(ts_dir.glob("*.parquet")) + sorted(ts_dir.glob("*.csv"))
    for path in paths:
        ts = pd.read_parquet(path) if path.suffix == ".parquet" else pd.read_csv(path)
        parsed = _parse_timeseries_stem(path.stem) or {}
        success = _success_for_timeseries(path.stem, trials)
        n = parsed.get("n_sheep")
        d = parsed.get("n_shepherds")
        regime = regime_map.get((int(n), int(d))) if n is not None and d is not None else None
        rows.append(
            {
                "timeseries": ts,
                "success": success,
                "n_sheep": n,
                "n_shepherds": d,
                "regime": regime,
                "stem": path.stem,
            }
        )
    return rows


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
                "frontier_by_layout": frontier.drop(columns=["rates"], errors="ignore"),
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
        ts_rows = _load_timeseries_trials(
            trials, args.trials.parent / "timeseries", regimes=regimes
        )
        temporal = evaluate_temporal_order(ts_rows)
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
                "temporal_order": pd.DataFrame([temporal]),
            },
            output,
            protocol=protocol,
            protocol_id=protocol_id,
            notes=[json.dumps({"mechanism": mech, "temporal": temporal}, default=str)],
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
        summary = transfer_summary(table)
        export_package_dossier(
            "D",
            {
                "transfer_table": table,
                "transfer_summary": pd.DataFrame([summary]),
            },
            output,
            protocol=protocol,
            protocol_id=protocol_id,
            notes=[json.dumps(summary)],
        )
    elif args.package == "E":
        artefacts: dict[str, pd.DataFrame] = {}
        notes = []
        if "obs_mode" in trials.columns:
            curves = substitution_curves(trials, theta=args.theta)
            summary = summarize_substitution(curves)
            artefacts["substitution_curves_obs"] = curves
            artefacts["substitution_summary_obs"] = pd.DataFrame([summary])
            notes.append(f"obs: {summary}")
        if "sensing_range" in trials.columns:
            base_range = float(protocol.get("rq5_base_sensing_range", 50.0))
            curves_r = substitution_curves_range(
                trials, theta=args.theta, base_range=base_range
            )
            summary_r = summarize_substitution(curves_r)
            artefacts["substitution_curves_range"] = curves_r
            artefacts["substitution_summary_range"] = pd.DataFrame([summary_r])
            notes.append(f"range: {summary_r}")
        if "communication" in trials.columns:
            curves_c = substitution_curves_communication(trials, theta=args.theta)
            summary_c = summarize_substitution(curves_c)
            artefacts["substitution_curves_comm"] = curves_c
            artefacts["substitution_summary_comm"] = pd.DataFrame([summary_c])
            notes.append(f"comm: {summary_c}")
        if not artefacts:
            curves = substitution_curves(trials, theta=args.theta)
            summary = summarize_substitution(curves)
            artefacts = {
                "substitution_curves": curves,
                "substitution_summary": pd.DataFrame([summary]),
            }
            notes = [str(summary)]
        export_package_dossier(
            "E",
            artefacts,
            output,
            protocol=protocol,
            protocol_id=protocol_id,
            notes=notes,
        )
    elif args.package == "F":
        group_cols = (
            ["initial_layout"] if "initial_layout" in trials.columns else None
        )
        frontier = extract_frontier(trials, theta=args.theta, group_cols=group_cols)
        fits = fit_scaling_models(frontier)
        model_rows = []
        for name, vals in fits.get("models", {}).items():
            row = {"model": name}
            for k, v in vals.items():
                if k == "params":
                    row["params"] = json.dumps(v)
                else:
                    row[k] = v
            model_rows.append(row)
        export_package_dossier(
            "F",
            {
                "frontier": frontier.drop(columns=["rates"], errors="ignore"),
                "scaling_fits": pd.DataFrame(model_rows),
                "scaling_cv": pd.DataFrame([fits.get("cv") or {}]),
                "delta_aic_vs_power": pd.DataFrame(
                    [fits.get("delta_aic_vs_power") or {}]
                ),
            },
            output,
            protocol=protocol,
            protocol_id=protocol_id,
            notes=[
                f"best_model={fits.get('best')}",
                f"state_models={list((fits.get('state_models') or {}).keys())}",
            ],
        )
    elif args.package == "G":
        regimes = label_regimes(trials, theta=args.theta)
        ts_rows = _load_timeseries_trials(
            trials, args.trials.parent / "timeseries", regimes=regimes
        )
        k = int(protocol.get("rq7_prediction_horizon_k", 500))
        w = int(protocol.get("rq7_feature_window_w", 200))
        campaign = evaluate_early_warning_campaign(
            [
                r
                for r in ts_rows
                if r.get("n_sheep") is not None and r.get("n_shepherds") is not None
            ],
            horizon_k=k,
            window_w=w,
            eval_ticks=default_eval_ticks(),
        )
        # Also keep per-trial summaries for lead-time claims (C7b).
        per_trial = [
            evaluate_early_warning(
                r["timeseries"],
                success=bool(r["success"]),
                horizon_k=k,
                window_w=w,
                eval_ticks=default_eval_ticks(),
            )
            for r in ts_rows
        ]
        summary = summarise_early_warning(per_trial)
        export_package_dossier(
            "G",
            {
                "early_warning_summary": pd.DataFrame([summary]),
                "early_warning_campaign": pd.DataFrame(
                    [{k: v for k, v in campaign.items() if k != "folds"}]
                ),
                "early_warning_folds": pd.DataFrame(campaign.get("folds") or []),
            },
            output,
            protocol=protocol,
            protocol_id=protocol_id,
            notes=[json.dumps({"summary": summary, "campaign": campaign}, default=str)],
        )
    print(f"Package {args.package} written to {output}")


if __name__ == "__main__":
    main()
