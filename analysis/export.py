"""Write auto-generated package dossiers under ``results/.../packages/``.

This module is the exporter for analysis Packages A and D-G (Cap I13). It does
not run simulations. Given trial tables and (for Package A) derived
frontiers/regimes, it writes machine-owned files into a package folder under
``results/`` only, for example:

- ``README.md``: auto-generated dossier (first line is the AUTO-GENERATED notice)
- ``artefacts.json``: path index of what was written
- ``provenance.json``: run stamp for the export
- Package A also: ``trials.csv``, ``reliability.csv``, ``frontier.csv``,
  ``regimes.csv``, ``dmin_bootstrap.csv``

Entry points:
- ``export_package_a``: full Package A herdability map dossier
- ``export_package_dossier``: generic CSV + README writer for Packages B-G

Paths under the repo but outside ``results/`` (including ``docs/report/``) are
refused. Hand-written protocol-folder READMEs (phase/stage notes) are separate
and must not be overwritten by these exporters.
"""

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
from analysis.regimes import REGIME_OVERCROWD, label_regimes
from protocols.packaging.generated_notice import markdown_banner_line, with_json_notice
from protocols.packaging.provenance import build_provenance_stamp, write_provenance
from services.layout import ensure_under_results


def _write_df(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def _unique_sorted(df: pd.DataFrame, col: str) -> list[Any]:
    if col not in df.columns:
        return []
    return sorted(set(df[col].dropna().tolist()))


def _fmt_cell(value: object) -> str:
    """Format one table cell for a hand-written-looking markdown table."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, int):
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


def _fmt_list(values: list[Any]) -> str:
    if not values:
        return "(none)"
    return ", ".join(str(v) for v in values)


def _finish_dossier(
    out: Path,
    paths: dict[str, Path],
    *,
    stamp: dict[str, Any],
    readme_lines: list[str],
) -> dict[str, Path]:
    """Write provenance.json, README.md, and artefacts.json; return the full path index."""
    paths["provenance"] = out / "provenance.json"
    write_provenance(paths["provenance"], stamp)
    paths["report"] = out / "README.md"
    _ = paths["report"].write_text("\n".join(readme_lines) + "\n")
    paths["artefacts"] = out / "artefacts.json"
    _ = paths["artefacts"].write_text(
        json.dumps(with_json_notice({k: str(v) for k, v in paths.items()}), indent=2) + "\n"
    )
    return paths


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
        has_overcrowd = bool((regimes["regime"] == REGIME_OVERCROWD).to_numpy().any())
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
        "- C2b (hard ceiling at extended time): not evaluated here "
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
        has_over = "d_overcrowd" in frontier.columns and bool(
            frontier["d_overcrowd"].notna().to_numpy().any()
        )
        over_bit = "; overcrowding present" if has_over else "; no D_overcrowd"
        if d_vals.empty:
            lines.append(
                "Frontier: " + ("with overcrowding marks" if has_over else "no D_min values") + "."
            )
        elif d_vals.nunique() <= 1:
            lines.append(f"Frontier: D_min = {d_vals.iloc[0]} everywhere{over_bit}.")
        else:
            lines.append("Frontier: D_min varies with N" + over_bit + " (table below).")
    lines.append("")
    return lines


def export_package_a(
    trials: pd.DataFrame,
    output_dir: Path | str,
    *,
    protocol: dict[str, Any],
    protocol_id: str = "package_a",
    theta: float = 0.90,
    group_cols: list[str] | None = None,
) -> dict[str, Path]:
    """Export Package A: tables, provenance, and markdown summary.

    Writes only under ``results/...`` (or a temp path outside the repo for tests).
    """
    out = ensure_under_results(output_dir, label="package A export")
    out.mkdir(parents=True, exist_ok=True)
    groups = list(group_cols or [])

    tables = {
        "trials": trials,
        "reliability": reliability_table(trials, group_cols=groups),
        "frontier": extract_frontier(trials, theta=theta, group_cols=groups),
        "regimes": label_regimes(trials, theta=theta, group_cols=groups),
        "dmin_bootstrap": bootstrap_d_min_ci(trials, theta=theta, group_cols=groups),
    }
    paths: dict[str, Path] = {}
    for name, df in tables.items():
        paths[name] = out / f"{name}.csv"
        _write_df(df, paths[name])
    frontier = tables["frontier"]
    regimes = tables["regimes"]

    seeds = sorted(int(s) for s in trials["seed"].unique()) if "seed" in trials.columns else []
    methods = _unique_sorted(trials, "method")
    layouts = _unique_sorted(trials, "initial_layout")
    n_values = _unique_sorted(trials, "n_sheep")
    d_values = _unique_sorted(trials, "n_shepherds")

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
            "methods": methods,
            "layouts": layouts,
            "n_values": n_values,
            "d_values": d_values,
        },
    )
    regime_counts = "_(none)_"
    if not regimes.empty and "regime" in regimes.columns:
        counts = regimes["regime"].value_counts().rename("count").reset_index()
        counts.columns = ["regime", "count"]
        regime_counts = _df_to_markdown_table(counts)

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
        *_package_a_results_prose(trials, frontier),
        "### Frontier table",
        "",
        _df_to_markdown_table(frontier),
        "",
        "### Regime counts",
        "",
        regime_counts,
        "",
        "## Claim stubs (auto, not final)",
        "",
        "These are automatic hints only. They are not final claim verdicts.",
        "",
        *_package_a_claim_stubs(frontier=frontier, regimes=regimes, theta=theta),
        "",
        "## Files from this export",
        "",
        *[f"- {p.name}" for p in paths.values()],
        "- provenance.json",
        "",
    ]
    return _finish_dossier(out, paths, stamp=stamp, readme_lines=lines)


def export_package_dossier(
    package: str,
    artefacts: dict[str, pd.DataFrame],
    output_dir: Path | str,
    *,
    protocol: dict[str, Any],
    protocol_id: str,
    notes: list[str] | None = None,
) -> dict[str, Path]:
    """Generic dossier writer for packages B-G.

    Writes only under ``results/...`` (or a temp path outside the repo for tests).
    """
    out = ensure_under_results(output_dir, label=f"package {package} export")
    out.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}
    for name, df in artefacts.items():
        paths[name] = out / f"{name}.csv"
        _write_df(df, paths[name])
    stamp = build_provenance_stamp(
        protocol=protocol,
        seed_list=[],
        extra={"package": package, "notes": notes or []},
    )
    lines = [
        markdown_banner_line(),
        "",
        f"# Package {package}: {protocol_id}",
        "",
        "Tables for this analysis package. Read the protocol-folder `README.md` "
        + "for interpretation and claim verdicts. This file is only the export dossier.",
        "",
    ]
    if notes:
        lines.extend(["## Notes", "", *notes, ""])
    lines.extend(
        [
            "## Files from this export",
            "",
            *[f"- {k}: `{v.name}`" for k, v in paths.items()],
            "- provenance.json",
            "",
        ]
    )
    return _finish_dossier(out, paths, stamp=stamp, readme_lines=lines)
