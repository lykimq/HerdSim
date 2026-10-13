"""Cross-method transfer tables for RQ4 (Cap I9 / Package D).

Compares frontiers (and related features) between baseline ``strombom_multi`` and
transfer methods (Kubo, FAT, ...). Labels each feature/N cell as shared, shifted,
or absent. Outputs feed ``package_d`` size/structure summaries and claim C4.
Pure table building; CSV/README writing is done by callers / export helpers.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from analysis.coerce import as_int
from analysis.frontier import extract_frontier


def _missing_grid_value(value: float | None) -> bool:
    if value is None:
        return True
    try:
        number = float(value)
    except (TypeError, ValueError):
        return True
    return number != number


def _classify_d_min_transfer(
    base_dmin: float | None,
    other_dmin: float | None,
) -> str:
    """Shared only when both sides have the same grid D_min."""
    if _missing_grid_value(base_dmin) or _missing_grid_value(other_dmin):
        return "absent"
    assert base_dmin is not None and other_dmin is not None
    if int(base_dmin) == int(other_dmin):
        return "shared"
    return "shifted"


def _classify_overcrowd_transfer(
    base_d: float | None,
    other_d: float | None,
    base_n: float,
) -> str:
    if base_d is None and other_d is None:
        return "absent"
    if base_d is None or other_d is None:
        return "absent" if base_d is None and other_d is None else "shifted"
    br = float(base_d) / max(float(base_n), 1.0)
    or_ = float(other_d) / max(float(base_n), 1.0)
    ratio = max(br, or_) / max(min(br, or_), 1e-9)
    if ratio <= 1.5:
        return "shared"
    return "shifted"


def _idir_correlation(trials: pd.DataFrame) -> float | None:
    """Pearson r(mean_i_dir, success) when both columns exist; else None."""
    if "mean_i_dir" not in trials.columns or "success" not in trials.columns:
        return None
    sub = trials[["mean_i_dir", "success"]].dropna()
    if len(sub) < 3:
        return None
    r = float(np.corrcoef(sub["mean_i_dir"].astype(float), sub["success"].astype(float))[0, 1])
    if r != r:
        return None
    return r


def _classify_idir_transfer(base_r: float | None, other_r: float | None) -> str:
    """Plan: shared when r(I_dir, R) < -0.3 in both; shifted if present but weaker."""
    if base_r is None or other_r is None:
        return "absent"
    base_sig = base_r < -0.3
    other_sig = other_r < -0.3
    if base_sig and other_sig:
        return "shared"
    if base_sig or other_sig:
        return "shifted"
    return "absent"


def _coverage_saturation_flag(trials: pd.DataFrame, theta: float) -> bool | None:
    """True when reliable cells show flat coverage while effort rises with D."""
    need = {"n_shepherds", "success", "mean_coverage", "shepherd_path"}
    if not need.issubset(trials.columns):
        return None
    rates = (
        trials.groupby("n_shepherds")
        .agg(
            reliability=("success", "mean"),
            coverage=("mean_coverage", "median"),
            effort=("shepherd_path", "median"),
        )
        .sort_index()
    )
    reliable = rates.loc[rates["reliability"] >= theta].copy()
    if len(reliable) < 2:
        return None
    coverage = pd.Series(reliable.loc[:, "coverage"])
    effort = pd.Series(reliable.loc[:, "effort"])
    cov_range = float(coverage.max() - coverage.min())
    effort_up = float(effort.iloc[-1] - effort.iloc[0])
    high = float(np.median(coverage)) > 0.5
    return bool(high and cov_range < 0.1 and effort_up > 0)


def _classify_flag_transfer(base: bool | None, other: bool | None) -> str:
    if base is None and other is None:
        return "absent"
    if base and other:
        return "shared"
    if base or other:
        return "shifted"
    return "absent"


def _default_group_cols(trials_by_method: dict[str, pd.DataFrame]) -> list[str]:
    for df in trials_by_method.values():
        if "initial_layout" in df.columns and int(df["initial_layout"].nunique(dropna=True)) > 1:
            return ["initial_layout"]
    return []


def _frontier_lookup(
    front: pd.DataFrame,
    *,
    group_cols: list[str],
    sheep_col: str,
) -> dict[tuple[Any, ...], pd.Series]:
    """Map (group..., n_sheep) -> frontier row."""
    out: dict[tuple[Any, ...], pd.Series] = {}
    if front.empty:
        return out
    for _, row in front.iterrows():
        key = tuple(row[c] for c in group_cols) + (as_int(row[sheep_col]),)
        out[key] = row
    return out


def build_transfer_table(
    trials_by_method: dict[str, pd.DataFrame],
    *,
    baseline: str,
    theta: float = 0.90,
    feature: str | None = None,
    group_cols: list[str] | None = None,
    sheep_col: str = "n_sheep",
) -> pd.DataFrame:
    """Build a transfer table comparing frontier / mechanism features across methods.

    Labels follow the plan: shared / shifted / absent. When ``feature`` is None,
    emits rows for d_min, overcrowd, i_dir_signature, and coverage_saturation.
    Multi-layout trials are compared within each layout when ``group_cols`` is
    set (default: ``initial_layout`` when it has more than one level).
    """
    if baseline not in trials_by_method:
        raise KeyError(f"baseline method '{baseline}' missing from trials_by_method")

    groups = list(group_cols) if group_cols is not None else _default_group_cols(trials_by_method)
    features = (
        [feature]
        if feature
        else [
            "d_min",
            "overcrowd",
            "i_dir_signature",
            "coverage_saturation",
        ]
    )

    fronts = {
        m: extract_frontier(df, theta=theta, sheep_col=sheep_col, group_cols=groups)
        for m, df in trials_by_method.items()
    }
    lookups = {
        m: _frontier_lookup(front, group_cols=groups, sheep_col=sheep_col)
        for m, front in fronts.items()
    }
    idir_r = {m: _idir_correlation(df) for m, df in trials_by_method.items()}
    cov_flags = {m: _coverage_saturation_flag(df, theta) for m, df in trials_by_method.items()}

    base_keys = set(lookups[baseline])
    rows: list[dict[str, Any]] = []
    for method in trials_by_method:
        if method == baseline:
            continue
        for feat in features:
            if feat == "i_dir_signature":
                label = _classify_idir_transfer(idir_r[baseline], idir_r[method])
                rows.append(
                    {
                        "feature": feat,
                        "n_sheep": None,
                        **{c: None for c in groups},
                        "baseline": baseline,
                        "method": method,
                        "baseline_value": idir_r[baseline],
                        "method_value": idir_r[method],
                        "transfer_label": label,
                    }
                )
                continue
            if feat == "coverage_saturation":
                label = _classify_flag_transfer(cov_flags[baseline], cov_flags[method])
                rows.append(
                    {
                        "feature": feat,
                        "n_sheep": None,
                        **{c: None for c in groups},
                        "baseline": baseline,
                        "method": method,
                        "baseline_value": cov_flags[baseline],
                        "method_value": cov_flags[method],
                        "transfer_label": label,
                    }
                )
                continue

            shared_keys = sorted(base_keys.intersection(lookups[method]))
            for key in shared_keys:
                b = lookups[baseline][key]
                o = lookups[method][key]
                n = key[-1]
                group_meta = {c: key[i] for i, c in enumerate(groups)}
                if feat == "d_min":
                    label = _classify_d_min_transfer(b.get("d_min"), o.get("d_min"))
                    bval, oval = b.get("d_min"), o.get("d_min")
                elif feat == "overcrowd":
                    label = _classify_overcrowd_transfer(
                        b.get("d_overcrowd"), o.get("d_overcrowd"), float(n)
                    )
                    bval, oval = b.get("d_overcrowd"), o.get("d_overcrowd")
                else:
                    label = "absent"
                    bval = oval = None
                rows.append(
                    {
                        "feature": feat,
                        "n_sheep": int(n),
                        **group_meta,
                        "baseline": baseline,
                        "method": method,
                        "baseline_value": bval,
                        "method_value": oval,
                        "transfer_label": label,
                    }
                )
    return pd.DataFrame(rows)


def transfer_summary(table: pd.DataFrame) -> dict[str, Any]:
    """Count shared / shifted / absent labels for C4-style reporting."""
    if table.empty or "transfer_label" not in table.columns:
        return {"n_rows": 0, "n_shared": 0, "n_shifted": 0, "n_absent": 0}
    counts = table["transfer_label"].value_counts().to_dict()
    return {
        "n_rows": int(len(table)),
        "n_shared": int(counts.get("shared", 0)),
        "n_shifted": int(counts.get("shifted", 0)),
        "n_absent": int(counts.get("absent", 0)),
    }
