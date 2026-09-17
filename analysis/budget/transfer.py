"""Cross-method transfer table builder (Cap I9)."""

from __future__ import annotations

from typing import Any

import pandas as pd

from analysis.budget.frontier import extract_frontier


def _classify_d_min_transfer(
    base_dmin: float | None,
    other_dmin: float | None,
) -> str:
    if base_dmin is None or other_dmin is None:
        return "absent"
    delta = abs(float(other_dmin) - float(base_dmin))
    if delta <= 2:
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
    # Comparable D/N ratio within 1.5x.
    br = float(base_d) / max(float(base_n), 1.0)
    or_ = float(other_d) / max(float(base_n), 1.0)
    ratio = max(br, or_) / max(min(br, or_), 1e-9)
    if ratio <= 1.5:
        return "shared"
    return "shifted"


def build_transfer_table(
    trials_by_method: dict[str, pd.DataFrame],
    *,
    baseline: str,
    theta: float = 0.90,
    feature: str = "d_min",
) -> pd.DataFrame:
    """Build a transfer table comparing frontier features across methods.

    Labels follow the plan: shared / shifted / absent.
    """
    if baseline not in trials_by_method:
        raise KeyError(f"baseline method '{baseline}' missing from trials_by_method")

    fronts = {
        m: extract_frontier(df, theta=theta).set_index("n_sheep")
        for m, df in trials_by_method.items()
    }
    base = fronts[baseline]
    rows: list[dict[str, Any]] = []
    for method, front in fronts.items():
        if method == baseline:
            continue
        for n in sorted(set(base.index).intersection(set(front.index))):
            b = base.loc[n]
            o = front.loc[n]
            if isinstance(b, pd.DataFrame):
                b = b.iloc[0]
            if isinstance(o, pd.DataFrame):
                o = o.iloc[0]
            if feature == "d_min":
                label = _classify_d_min_transfer(b.get("d_min"), o.get("d_min"))
            elif feature == "overcrowd":
                label = _classify_overcrowd_transfer(
                    b.get("d_overcrowd"), o.get("d_overcrowd"), float(n)
                )
            else:
                label = "absent"
            rows.append(
                {
                    "feature": feature,
                    "n_sheep": int(n),
                    "baseline": baseline,
                    "method": method,
                    "baseline_value": b.get("d_min" if feature == "d_min" else "d_overcrowd"),
                    "method_value": o.get("d_min" if feature == "d_min" else "d_overcrowd"),
                    "transfer_label": label,
                }
            )
    return pd.DataFrame(rows)
