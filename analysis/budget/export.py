"""Package dossier export for budget campaigns (Cap I13)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from analysis.budget.frontier import extract_frontier, reliability_table
from analysis.budget.provenance import build_provenance_stamp, write_provenance
from analysis.budget.regimes import label_regimes


def _write_df(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def export_package_a(
    trials: pd.DataFrame,
    output_dir: Path | str,
    *,
    protocol: dict[str, Any],
    campaign_id: str = "package_a",
    theta: float = 0.90,
    seed_list: list[int] | None = None,
    group_cols: list[str] | None = None,
) -> dict[str, Path]:
    """Export Package A: reliability map, frontier, regimes, provenance, markdown."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    groups = list(group_cols or [])

    rates = reliability_table(trials, group_cols=groups)
    frontier = extract_frontier(trials, theta=theta, group_cols=groups)
    regimes = label_regimes(trials, theta=theta, group_cols=groups)

    paths = {
        "trials": out / "trials.csv",
        "reliability": out / "reliability.csv",
        "frontier": out / "frontier.csv",
        "regimes": out / "regimes.csv",
        "provenance": out / "provenance.json",
        "report": out / "package_a.md",
    }
    _write_df(trials, paths["trials"])
    _write_df(rates, paths["reliability"])
    # Drop nested dict column for CSV friendliness.
    front_csv = frontier.drop(columns=["rates"], errors="ignore")
    _write_df(front_csv, paths["frontier"])
    _write_df(regimes, paths["regimes"])

    if seed_list is not None:
        seeds = list(seed_list)
    elif "seed" in trials.columns:
        seeds = sorted(int(s) for s in trials["seed"].unique().tolist())
    else:
        seeds = []
    stamp = build_provenance_stamp(
        campaign_id=campaign_id,
        protocol=protocol,
        seed_list=seeds,
        metric_ids=["success", "mean_spread", "extent", "cohesion", "fragmentation"],
        extra={"package": "A", "theta": theta},
    )
    write_provenance(paths["provenance"], stamp)

    lines = [
        f"# Package A -- Herdability map ({campaign_id})",
        "",
        f"Reliability threshold theta = {theta}",
        f"Trials: {len(trials)}",
        f"Frontier rows: {len(frontier)}",
        "",
        "## Frontier summary",
        "",
        front_csv.to_string(index=False),
        "",
        "## Regime counts",
        "",
        regimes["regime"].value_counts().to_string()
        if not regimes.empty
        else "(none)",
        "",
    ]
    paths["report"].write_text("\n".join(lines) + "\n")
    return paths


def export_package_dossier(
    package: str,
    artefacts: dict[str, pd.DataFrame],
    output_dir: Path | str,
    *,
    protocol: dict[str, Any],
    campaign_id: str,
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
        campaign_id=campaign_id,
        protocol=protocol,
        seed_list=[],
        extra={"package": package, "notes": notes or []},
    )
    prov = out / "provenance.json"
    write_provenance(prov, stamp)
    paths["provenance"] = prov
    report = out / f"package_{package.lower()}.md"
    body = [
        f"# Package {package} -- {campaign_id}",
        "",
        *(notes or []),
        "",
        "Artefacts:",
        *[f"- {k}: {v.name}" for k, v in paths.items() if k != "provenance"],
        "",
    ]
    report.write_text("\n".join(body) + "\n")
    paths["report"] = report
    (out / "manifest.json").write_text(
        json.dumps({k: str(v) for k, v in paths.items()}, indent=2) + "\n"
    )
    return paths
