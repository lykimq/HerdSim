"""Package dossier export for scaling protocols (Cap I13)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from analysis.frontier import (
    bootstrap_d_min_ci,
    extract_frontier,
    reliability_table,
)
from analysis.plots import (
    save_frontier_curve,
    save_regime_counts,
    save_reliability_heatmap,
)
from analysis.regimes import label_regimes
from protocols.packaging.generated_notice import markdown_banner_line, with_json_notice
from protocols.packaging.provenance import build_provenance_stamp, write_provenance


def _write_df(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def _unique_sorted(series: pd.Series) -> list[Any]:
    vals = sorted({v for v in series.dropna().tolist()})
    return vals


def _fmt_cell(value: object) -> str:
    """Format one table cell for a hand-written-looking markdown table."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, float):
        if float(value).is_integer():
            return str(int(value))
        return f"{value:.3f}".rstrip("0").rstrip(".")
    text = str(value)
    if text in {"None", "nan", "NaN", "<NA>"}:
        return ""
    if text == "True":
        return "yes"
    if text == "False":
        return "no"
    return text


def _df_to_markdown_table(df: pd.DataFrame) -> str:
    """Render a small dataframe as a GitHub-flavored markdown table."""
    if df.empty:
        return "_(empty)_"
    cols = [str(c) for c in df.columns]
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    rows: list[str] = []
    for _, row in df.iterrows():
        cells = [_fmt_cell(row[c]) for c in df.columns]
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, sep, *rows])


def _series_counts_to_markdown(counts: pd.Series, *, key_name: str = "regime") -> str:
    if counts.empty:
        return "_(none)_"
    frame = counts.rename("count").reset_index()
    frame.columns = [key_name, "count"]
    return _df_to_markdown_table(frame)


def _fmt_list(values: list[Any]) -> str:
    if not values:
        return "(none)"
    return ", ".join(str(v) for v in values)


def _package_a_claim_stubs(
    *,
    frontier: pd.DataFrame,
    regimes: pd.DataFrame,
    theta: float,
) -> list[str]:
    """Automatic, non-final claim hints for Package A (C2 / C6 path)."""
    lines: list[str] = []
    has_overcrowd = False
    if not regimes.empty and "regime" in regimes.columns:
        has_overcrowd = bool((regimes["regime"] == "overcrowding_collapse").to_numpy().any())
    if "d_overcrowd" in frontier.columns:
        has_overcrowd = has_overcrowd or bool(frontier["d_overcrowd"].notna().to_numpy().any())

    if has_overcrowd:
        lines.append(
            f"- C2a (overcrowding at theta={theta}): there is a candidate signal "
            + "(overcrowding cells or D_overcrowd). Confirm with claim-grade seeds "
            + "and, if needed, more than one method."
        )
    else:
        lines.append(
            f"- C2a (overcrowding at theta={theta}): not evaluable on this export "
            + "(no overcrowding regime / D_overcrowd)."
        )

    lines.append(
        "- C2b (hard ceiling at T1): not evaluated here "
        + "(needs an extended-time campaign)."
    )

    if frontier.empty or "d_min" not in frontier.columns:
        lines.append("- C6 (scaling): not evaluable (empty frontier).")
    else:
        d_vals = frontier["d_min"].dropna()
        if d_vals.empty:
            lines.append("- C6 (scaling): not evaluable (no D_min values).")
        elif d_vals.nunique() <= 1:
            lines.append(
                "- C6 (scaling): flat on this domain "
                + f"(constant D_min={d_vals.iloc[0]}). A harder start or larger N "
                + "would give the fits more to work with."
            )
        else:
            lines.append(
                "- C6 (scaling): frontier changes with N; "
                + "run Package F fits before deciding C6a/C6b."
            )
    return lines


def _package_a_results_prose(
    trials: pd.DataFrame,
    regimes: pd.DataFrame,
    frontier: pd.DataFrame,
) -> list[str]:
    """Short plain-language results block for the Package A README."""
    parts: list[str] = [f"{len(trials)} trials."]
    if "success" in trials.columns and len(trials):
        rate = float(pd.Series(trials["success"]).mean())
        n_ok = int(pd.Series(trials["success"]).sum())
        parts.append(f"Overall success {rate:.3f} ({n_ok} succeed).")
    if "failure_mode" in trials.columns and len(trials):
        failed = trials.loc[~trials["success"].astype(bool), "failure_mode"]
        if len(failed):
            top = failed.value_counts().head(4)
            bits = [f"{mode} {int(count)}" for mode, count in top.items()]
            parts.append("Failures: " + ", ".join(bits) + ".")
    if "total_ticks" in trials.columns and len(trials):
        ticks = trials["total_ticks"]
        parts.append(
            f"Ticks: median {ticks.median():.0f}, "
            + f"p90 {ticks.quantile(0.9):.0f}, max {ticks.max():.0f}."
        )

    lines = [" ".join(parts), ""]

    if frontier.empty or "d_min" not in frontier.columns:
        lines.append("Frontier: (empty).")
    else:
        d_vals = frontier["d_min"].dropna()
        has_over = (
            "d_overcrowd" in frontier.columns
            and bool(frontier["d_overcrowd"].notna().to_numpy().any())
        )
        if d_vals.empty:
            over_bit = "with overcrowding marks" if has_over else "no D_min values"
            lines.append(f"Frontier: {over_bit}.")
        elif d_vals.nunique() <= 1:
            over_bit = "; overcrowding present" if has_over else "; no D_overcrowd"
            lines.append(f"Frontier: D_min = {d_vals.iloc[0]} everywhere{over_bit}.")
        else:
            over_bit = "; overcrowding present" if has_over else "; no D_overcrowd"
            lines.append(
                "Frontier: D_min varies with N"
                + over_bit
                + " (table below)."
            )
    lines.append("")
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
        "report": out / "README.md",
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
        _unique_sorted(pd.Series(trials["n_shepherds"])) if "n_shepherds" in trials.columns else []
    )

    stamp = build_provenance_stamp(
        protocol=protocol,
        seed_list=seeds,
        metric_ids=[
            "success",
            "mean_spread",
            "extent",
            "perimeter",
            "hull_area",
            "flock_density",
            "aspect_ratio",
            "cohesion",
            "fragmentation",
        ],
        extra={
            "package": "A",
            "theta": theta,
            "n_figures": len(figure_paths),
            "methods": methods,
            "layouts": layouts,
            "n_values": n_values,
            "d_values": d_values,
        },
    )
    write_provenance(paths["provenance"], stamp)

    lines = [
        markdown_banner_line(),
        "",
        f"# Package A: Herdability map ({protocol_id})",
        "",
        "Package A is the herdability (size) map for this run: success rate R by "
        + "(N, D), the fewest-dogs frontier (`D_min`, and overcrowding "
        + "`D_overcrowd` if any), and regime labels (under-resourced / efficient / "
        + "wasteful / overcrowding).",
        "",
        "Read the protocol-folder `README.md` for interpretation and claim "
        + "verdicts. This file is only the export dossier.",
        "",
        "## Setup",
        "",
        f"- Protocol id: `{protocol.get('protocol_id', 'unknown')}`",
        f"- Reliability theta: {theta}",
        f"- Methods: {_fmt_list(methods) if methods else '(not in trials.csv)'}",
        f"- Layouts: {_fmt_list(layouts) if layouts else '(not in trials.csv)'}",
        f"- N grid: {_fmt_list(n_values)}",
        f"- D grid: {_fmt_list(d_values)}",
        f"- Seeds in export: {len(seeds)} unique",
        f"- Trial rows: {len(trials)}",
        f"- Frontier rows: {len(frontier)}",
        "",
        "## Results",
        "",
        *_package_a_results_prose(trials, regimes, frontier),
        "### Frontier table",
        "",
        _df_to_markdown_table(front_csv),
        "",
        "### Regime counts",
        "",
        (
            _series_counts_to_markdown(regimes["regime"].value_counts())
            if not regimes.empty and "regime" in regimes.columns
            else "_(none)_"
        ),
        "",
        "## Claim stubs (auto, not final)",
        "",
        "These are automatic hints only. They are not final claim verdicts.",
        "",
        *_package_a_claim_stubs(frontier=frontier, regimes=regimes, theta=theta),
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
            "## Files from this export",
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
    _ = paths["report"].write_text("\n".join(lines) + "\n")
    _ = paths["artefacts"].write_text(
        json.dumps(
            with_json_notice({k: str(v) for k, v in paths.items()}),
            indent=2,
        )
        + "\n"
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
        protocol=protocol,
        seed_list=[],
        extra={"package": package, "notes": notes or []},
    )
    prov = out / "provenance.json"
    write_provenance(prov, stamp)
    paths["provenance"] = prov
    report = out / "README.md"
    note_lines = list(notes or [])
    body = [
        markdown_banner_line(),
        "",
        f"# Package {package}: {protocol_id}",
        "",
        "Tables for this analysis package. Read the protocol-folder `README.md` "
        + "for interpretation and claim verdicts. This file is only the export dossier.",
        "",
    ]
    if note_lines:
        body.extend(["## Notes", "", *note_lines, ""])
    body.extend(
        [
            "## Files from this export",
            "",
            *[f"- {k}: `{v.name}`" for k, v in paths.items() if k != "provenance"],
            "- provenance.json",
            "",
        ]
    )
    _ = report.write_text("\n".join(body) + "\n")
    paths["report"] = report
    _ = (out / "artefacts.json").write_text(
        json.dumps(
            with_json_notice({k: str(v) for k, v in paths.items()}),
            indent=2,
        )
        + "\n"
    )
    return paths
