"""Write analysis package tables under ``results/.../packages/<letter>/``.

This module is the exporter for analysis Packages A and D-G (Cap I13). It does
not run simulations and is not called by the campaign runner. Each export writes
CSV tables plus ``provenance.json``; every file carries the AUTO-GENERATED
notice. Interpretation and claim verdicts belong in the hand-written
protocol-folder ``README.md``, not here.

Entry points:
- ``export_package_a``: Package A size / structure map (trials, reliability,
  frontier, regimes, D_min bootstrap)
- ``export_package_dossier``: any named tables for Packages D-G

Paths under the repo but outside ``results/`` (including ``docs/``) are refused.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from analysis.frontier import bootstrap_d_min_ci, extract_frontier, reliability_table
from analysis.regimes import label_regimes
from protocols.packaging.generated_notice import write_csv
from protocols.packaging.provenance import build_provenance_stamp, write_provenance
from services.layout import ensure_under_results


def _write_package(
    out: Path,
    tables: dict[str, pd.DataFrame],
    stamp: dict[str, Any],
) -> dict[str, Path]:
    """Write ``<name>.csv`` per table plus provenance.json; return the paths."""
    paths: dict[str, Path] = {}
    for name, df in tables.items():
        paths[name] = out / f"{name}.csv"
        write_csv(df, paths[name])
    paths["provenance"] = out / "provenance.json"
    write_provenance(paths["provenance"], stamp)
    return paths


def export_package_a(
    trials: pd.DataFrame,
    output_dir: Path | str,
    *,
    protocol: dict[str, Any],
    theta: float = 0.90,
    group_cols: list[str] | None = None,
) -> dict[str, Path]:
    """Export Package A tables and provenance for one trials table.

    Writes only under ``results/...`` (or a temp path outside the repo for tests).
    """
    out = ensure_under_results(output_dir, label="package A export")
    groups = list(group_cols or [])
    tables = {
        "trials": trials,
        "reliability": reliability_table(trials, group_cols=groups),
        "frontier": extract_frontier(trials, theta=theta, group_cols=groups),
        "regimes": label_regimes(trials, theta=theta, group_cols=groups),
        "dmin_bootstrap": bootstrap_d_min_ci(trials, theta=theta, group_cols=groups),
    }
    seeds = sorted(int(s) for s in trials["seed"].unique()) if "seed" in trials.columns else []
    stamp = build_provenance_stamp(
        protocol=protocol,
        seed_list=seeds,
        extra={"package": "A", "theta": theta, "group_cols": groups},
    )
    return _write_package(out, tables, stamp)


def export_package_dossier(
    package: str,
    tables: dict[str, pd.DataFrame],
    output_dir: Path | str,
    *,
    protocol: dict[str, Any],
    notes: list[str] | None = None,
) -> dict[str, Path]:
    """Export named tables for Packages D-G plus provenance (``notes`` go in it).

    Writes only under ``results/...`` (or a temp path outside the repo for tests).
    """
    out = ensure_under_results(output_dir, label=f"package {package} export")
    stamp = build_provenance_stamp(
        protocol=protocol,
        seed_list=[],
        extra={"package": package, "notes": notes or []},
    )
    return _write_package(out, tables, stamp)
