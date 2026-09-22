"""Cross-method transfer table builder (Cap I9)."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from analysis.scaling.frontier import extract_frontier


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


def build_transfer_table(
    trials_by_method: dict[str, pd.DataFrame],
    *,
    baseline: str,
    theta: float = 0.90,
    feature: str | None = None,
) -> pd.DataFrame:
    """Build a transfer table comparing frontier / mechanism features across methods.

    Labels follow the plan: shared / shifted / absent. When ``feature`` is None,
    emits rows for d_min, overcrowd, i_dir_signature, and coverage_saturation.
    """
    if baseline not in trials_by_method:
        raise KeyError(f"baseline method '{baseline}' missing from trials_by_method")

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
        m: extract_frontier(df, theta=theta).set_index("n_sheep")
        for m, df in trials_by_method.items()
    }
    idir_r = {m: _idir_correlation(df) for m, df in trials_by_method.items()}
    cov_flags = {m: _coverage_saturation_flag(df, theta) for m, df in trials_by_method.items()}

    base = fronts[baseline]
    rows: list[dict[str, Any]] = []
    for method, front in fronts.items():
        if method == baseline:
            continue
        for feat in features:
            if feat == "i_dir_signature":
                label = _classify_idir_transfer(idir_r[baseline], idir_r[method])
                rows.append(
                    {
                        "feature": feat,
                        "n_sheep": None,
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
                        "baseline": baseline,
                        "method": method,
                        "baseline_value": cov_flags[baseline],
                        "method_value": cov_flags[method],
                        "transfer_label": label,
                    }
                )
                continue

            for n in sorted(set(base.index).intersection(set(front.index))):
                b = base.loc[n]
                o = front.loc[n]
                if isinstance(b, pd.DataFrame):
                    b = b.iloc[0]
                if isinstance(o, pd.DataFrame):
                    o = o.iloc[0]
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
