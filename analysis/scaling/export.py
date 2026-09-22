"""Package dossier export for scaling protocols (Cap I13)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from analysis.scaling.frontier import (
    bootstrap_d_min_ci,
    extract_frontier,
    reliability_table,
)
from analysis.scaling.plots import (
    save_frontier_curve,
    save_regime_counts,
    save_reliability_heatmap,
)
from analysis.scaling.provenance import build_provenance_stamp, write_provenance
from analysis.scaling.regimes import label_regimes


def _write_df(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def _unique_sorted(series: pd.Series) -> list[Any]:
    vals = sorted({v for v in series.dropna().tolist()})
    return vals


def _package_a_claim_stubs(
    *,
    frontier: pd.DataFrame,
    regimes: pd.DataFrame,
    theta: float,
) -> list[str]:
    """Auto, non-final claim hints for Package A (C2 / C6 path)."""
    lines: list[str] = []
    has_overcrowd = False
    if not regimes.empty and "regime" in regimes.columns:
        has_overcrowd = bool((regimes["regime"] == "overcrowding_collapse").to_numpy().any())
    if "d_overcrowd" in frontier.columns:
        has_overcrowd = has_overcrowd or bool(frontier["d_overcrowd"].notna().to_numpy().any())

    if has_overcrowd:
        lines.append(
            f"- C2a (overcrowding at theta={theta}): candidate signal present "
            "(overcrowding cells or D_overcrowd). Needs claim-grade seeds / multi-method."
        )
    else:
        lines.append(
            f"- C2a (overcrowding at theta={theta}): UNEVALUABLE on this export "
            "(no overcrowding regime / D_overcrowd)."
        )

    lines.append(
        "- C2b (hard ceiling at T1): not evaluated here (requires extended-time campaign)."
    )

    if frontier.empty or "d_min" not in frontier.columns:
        lines.append("- C6 (scaling): UNEVALUABLE (empty frontier).")
    else:
        d_vals = frontier["d_min"].dropna()
        if d_vals.empty:
            lines.append("- C6 (scaling): UNEVALUABLE (no D_min values).")
        elif d_vals.nunique() <= 1:
            lines.append(
                f"- C6 (scaling): DEGENERATE on this domain "
                f"(constant D_min={d_vals.iloc[0]}). Prefer harder X0 / larger N."
            )
        else:
            lines.append(
                "- C6 (scaling): frontier varies with N; run Package F fits before deciding C6a/C6b."
            )
    return lines


def _package_a_diagnostics(trials: pd.DataFrame, regimes: pd.DataFrame) -> list[str]:
    lines: list[str] = []
    lines.append(f"- Trial rows: {len(trials)}")
    if "success" in trials.columns and len(trials):
        rate = float(pd.Series(trials["success"]).mean())
        lines.append(f"- Overall success rate: {rate:.3f}")
    if "failure_mode" in trials.columns:
        top = trials["failure_mode"].value_counts().head(5)
        if not top.empty:
            lines.append("- Top failure_mode counts:")
            for mode, count in top.items():
                lines.append(f"  - {mode}: {count}")
    if "total_ticks" in trials.columns and len(trials):
        ticks = trials["total_ticks"]
        lines.append(
            f"- Ticks: median={ticks.median():.0f}, "
            f"p90={ticks.quantile(0.9):.0f}, max={ticks.max():.0f}"
        )
    if not regimes.empty and "regime" in regimes.columns:
        lines.append("- Regime counts:")
        for regime, count in regimes["regime"].value_counts().items():
            lines.append(f"  - {regime}: {count}")
    return lines


def _write_package_a_figures(
    *,
    rates: pd.DataFrame,
    frontier: pd.DataFrame,
    regimes: pd.DataFrame,
    figures_dir: Path,
    protocol_id: str,
) -> dict[str, Path]:
    """Write Package A figures; skip gracefully if matplotlib missing or data empty."""
    figures_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}

    if "initial_layout" in rates.columns and rates["initial_layout"].nunique() > 1:
        for layout, sub in rates.groupby("initial_layout", dropna=False):
            path = figures_dir / f"reliability_heatmap_{layout}.png"
            saved = save_reliability_heatmap(
                sub.drop(columns=["initial_layout"], errors="ignore"),
                path,
                title=f"R(N, D) -- {protocol_id} / {layout}",
            )
            if saved is not None:
                written[f"heatmap_{layout}"] = saved
    else:
        plot_rates = rates.drop(columns=["initial_layout"], errors="ignore")
        path = figures_dir / "reliability_heatmap.png"
        saved = save_reliability_heatmap(
            plot_rates,
            path,
            title=f"R(N, D) -- {protocol_id}",
        )
        if saved is not None:
            written["heatmap"] = saved

    group_col = (
        "initial_layout"
        if "initial_layout" in frontier.columns and frontier["initial_layout"].nunique() > 1
        else None
    )
    frontier_path = figures_dir / "frontier_dmin.png"
    saved = save_frontier_curve(
        frontier.drop(columns=["rates"], errors="ignore"),
        frontier_path,
        title=f"Frontier -- {protocol_id}",
        group_col=group_col,
    )
    if saved is not None:
        written["frontier"] = saved

    regimes_path = figures_dir / "regime_counts.png"
    saved = save_regime_counts(
        regimes,
        regimes_path,
        title=f"Regimes -- {protocol_id}",
    )
    if saved is not None:
        written["regimes"] = saved

    return written


def export_package_a(
    trials: pd.DataFrame,
    output_dir: Path | str,
    *,
    protocol: dict[str, Any],
    protocol_id: str = "package_a",
    theta: float = 0.90,
    seed_list: list[int] | None = None,
    group_cols: list[str] | None = None,
) -> dict[str, Path]:
    """Export Package A: tables, figures, provenance, and markdown summary."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    figures_dir = out / "figures"
    groups = list(group_cols or [])

    rates = reliability_table(trials, group_cols=groups)
    frontier = extract_frontier(trials, theta=theta, group_cols=groups)
    regimes = label_regimes(trials, theta=theta, group_cols=groups)
    bootstrap = bootstrap_d_min_ci(trials, theta=theta, group_cols=groups)

    paths: dict[str, Path] = {
        "trials": out / "trials.csv",
        "reliability": out / "reliability.csv",
        "frontier": out / "frontier.csv",
        "regimes": out / "regimes.csv",
        "dmin_bootstrap": out / "dmin_bootstrap.csv",
        "provenance": out / "provenance.json",
        "report": out / "package_a.md",
        "artefacts": out / "artefacts.json",
    }
    _write_df(trials, paths["trials"])
    _write_df(rates, paths["reliability"])
    front_csv = frontier.drop(columns=["rates"], errors="ignore")
    _write_df(front_csv, paths["frontier"])
    _write_df(regimes, paths["regimes"])
    _write_df(bootstrap, paths["dmin_bootstrap"])

    figure_paths = _write_package_a_figures(
        rates=rates,
        frontier=frontier,
        regimes=regimes,
        figures_dir=figures_dir,
        protocol_id=protocol_id,
    )
    for key, path in figure_paths.items():
        paths[f"fig_{key}"] = path

    if seed_list is not None:
        seeds = list(seed_list)
    elif "seed" in trials.columns:
        seeds = sorted(int(s) for s in trials["seed"].unique().tolist())
    else:
        seeds = []

    methods = _unique_sorted(pd.Series(trials["method"])) if "method" in trials.columns else []
    layouts = (
        _unique_sorted(pd.Series(trials["initial_layout"]))
        if "initial_layout" in trials.columns
        else []
    )
    n_values = _unique_sorted(pd.Series(trials["n_sheep"])) if "n_sheep" in trials.columns else []
    d_values = (
        _unique_sorted(pd.Series(trials["n_shepherds"]))
        if "n_shepherds" in trials.columns
        else []
    )

    stamp = build_provenance_stamp(
        protocol_id=protocol_id,
        protocol=protocol,
        seed_list=seeds,
        metric_ids=["success", "mean_spread", "extent", "cohesion", "fragmentation"],
        extra={
            "package": "A",
            "theta": theta,
            "n_figures": len(figure_paths),
            "methods": methods,
            "layouts": layouts,
        },
    )
    write_provenance(paths["provenance"], stamp)

    lines = [
        f"# Package A -- Herdability map ({protocol_id})",
        "",
        "Auto-generated evidence package. Interpretation belongs in the protocol `REPORT.md`.",
        "",
        "## Setup",
        "",
        f"- Protocol id: `{protocol.get('protocol_id', 'unknown')}`",
        f"- Reliability theta: {theta}",
        f"- Methods: {methods or ['(not in trials.csv)']}",
        f"- Layouts: {layouts or ['(not in trials.csv)']}",
        f"- N grid: {n_values}",
        f"- D grid: {d_values}",
        f"- Seeds in export: {len(seeds)} unique",
        f"- Trial rows: {len(trials)}",
        f"- Frontier rows: {len(frontier)}",
        "",
        "## Diagnostics",
        "",
        *_package_a_diagnostics(trials, regimes),
        "",
        "## Claim stubs (auto, not final)",
        "",
        *_package_a_claim_stubs(frontier=frontier, regimes=regimes, theta=theta),
        "",
        "## Frontier summary",
        "",
        front_csv.to_string(index=False) if not front_csv.empty else "(empty)",
        "",
        "## Regime counts",
        "",
        regimes["regime"].value_counts().to_string()
        if not regimes.empty and "regime" in regimes.columns
        else "(none)",
        "",
        "## Figures",
        "",
    ]
    if figure_paths:
        for key, path in figure_paths.items():
            rel = path.name
            lines.append(f"- {key}: `figures/{rel}`")
            lines.append(f"  ![{key}](figures/{rel})")
            lines.append("")
    else:
        lines.append("- (no figures written; check matplotlib / empty tables)")
        lines.append("")

    lines.extend(
        [
            "## Artefacts",
            "",
            "- trials.csv",
            "- reliability.csv",
            "- frontier.csv",
            "- regimes.csv",
            "- dmin_bootstrap.csv",
            "- provenance.json",
            "- figures/",
            "",
        ]
    )
    paths["report"].write_text("\n".join(lines) + "\n")
    paths["artefacts"].write_text(
        json.dumps({k: str(v) for k, v in paths.items()}, indent=2) + "\n"
    )
    return paths


def export_package_dossier(
    package: str,
    artefacts: dict[str, pd.DataFrame],
    output_dir: Path | str,
    *,
    protocol: dict[str, Any],
    protocol_id: str,
    notes: list[str] | None = None,
) -> dict[str, Path]:
    """Generic dossier writer for packages B-G."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}
    for name, df in artefacts.items():
        path = out / f"{name}.csv"
        _write_df(df, path)
        paths[name] = path
    stamp = build_provenance_stamp(
        protocol_id=protocol_id,
        protocol=protocol,
        seed_list=[],
        extra={"package": package, "notes": notes or []},
    )
    prov = out / "provenance.json"
    write_provenance(prov, stamp)
    paths["provenance"] = prov
    report = out / f"package_{package.lower()}.md"
    body = [
        f"# Package {package} -- {protocol_id}",
        "",
        "Auto-generated evidence package. Interpretation belongs in the protocol `REPORT.md`.",
        "",
        *(notes or []),
        "",
        "Artefacts:",
        *[f"- {k}: {v.name}" for k, v in paths.items() if k != "provenance"],
        "",
    ]
    report.write_text("\n".join(body) + "\n")
    paths["report"] = report
    (out / "artefacts.json").write_text(
        json.dumps({k: str(v) for k, v in paths.items()}, indent=2) + "\n"
    )
    return paths
