"""Report tabulation helpers for frontier metrics, growth rates, and operational regimes.

Transforms simulation outputs (frontier_groups.csv, frontier_cells.csv, trials.csv,
and queue_log.jsonl) into structured summary DataFrames for Markdown reports and CLI tools:
- D_min and D_sat scaling grids across initial layouts and flock sizes.
- Power-law log-log slope ranges accounting for interval censoring.
- Efficiency and overhead metrics for dog teams beyond saturation.
- Identification of non-monotonic dips, operational drag, and collapse zones.
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from .dmin import arrival_groups
from .results import read_groups


def parse_group_key(key: str) -> dict[str, Any]:
    """Parses a serialized group key string into method, layout, factors, and n components."""
    parts = key.split("|")
    return {
        "method": parts[0],
        "layout": parts[1],
        "factors": "|".join(parts[2:-1]),
        "n": int(parts[-1].removeprefix("N=")),
    }


def split_group_key(frame: pd.DataFrame) -> pd.DataFrame:
    """Expands the group_key column of a DataFrame into individual metadata columns."""
    keys = pd.DataFrame([parse_group_key(k) for k in frame["group_key"]], index=frame.index)
    return pd.concat([keys, frame.drop(columns=["group_key"])], axis=1)


def groups_table(folder: Path) -> pd.DataFrame:
    """Loads frontier_groups.csv with expanded metadata columns for each D curve."""
    return split_group_key(read_groups(folder))


def dmin_text(row: pd.Series) -> str:
    """Formats the estimated D_min value or bracket as a display string (e.g. '4', '2-4', '[2]')."""
    if pd.notna(row["d_min"]):
        high = int(row["d_min"])
        low = int(row["d_min_low"]) if pd.notna(row["d_min_low"]) else high
        return str(high) if low >= high else f"{low}-{high}"
    if bool(row.get("d_min_above_grid", False)):
        return "none on grid"
    if pd.notna(row["d_min_low"]):
        return f"[{int(row['d_min_low'])}]"
    return "-"


def one_level(table: pd.DataFrame) -> pd.DataFrame:
    """Validates that a DataFrame contains at most one factor level before layout-by-N pivoting."""
    if "factors" in table and table["factors"].nunique() > 1:
        levels = sorted(table["factors"].unique())
        raise ValueError(f"several factor levels {levels}; use compare, which keeps them apart")
    return table


def layout_by_n(table: pd.DataFrame, layouts: tuple[str, ...] | None = None) -> pd.DataFrame:
    """Pivots D_min into a 2D grid with layouts as rows and flock sizes N as columns."""
    table = one_level(table)
    shown = table.assign(text=table.apply(dmin_text, axis=1))
    wide = shown.pivot_table(index="layout", columns="n", values="text", aggfunc="first")
    if layouts is not None:
        wide = wide.reindex([layout for layout in layouts if layout in wide.index])
    return wide.fillna("-")


def bracket(row: pd.Series) -> tuple[float, float] | None:
    """Extracts the [low, high] bounds of the true D_min, or None if no reliable D exists."""
    if pd.isna(row["d_min"]) or pd.isna(row["d_min_low"]):
        return None
    return float(row["d_min_low"]), float(row["d_min"])


def slope_range(points: list[tuple[int, float, float]]) -> tuple[float, float] | None:
    """Computes min and max OLS slopes of log2(D) vs log2(N) over bracket combinations."""
    if len(points) < 2:
        return None
    x = np.log2([p[0] for p in points])
    x = x - x.mean()
    ends = [(math.log2(p[1]), math.log2(p[2])) for p in points]
    slopes = []
    for pick in itertools.product((0, 1), repeat=len(points)):
        y = np.array([ends[i][pick[i]] for i in range(len(points))])
        slopes.append(float((x * (y - y.mean())).sum() / (x * x).sum()))
    return min(slopes), max(slopes)


def growth_table(table: pd.DataFrame) -> pd.DataFrame:
    """Summarizes log-log scaling slope ranges and inclusion notes per layout."""
    rows = []
    for layout, part in one_level(table).groupby("layout", sort=False):
        used, above, open_ = [], [], []
        for _, row in part.sort_values("n").iterrows():
            b = bracket(row)
            if b:
                used.append((int(row["n"]), b))
            elif bool(row.get("d_min_above_grid", False)):
                above.append(int(row["n"]))
            else:
                open_.append(int(row["n"]))
        points = [(n, b[0], b[1]) for n, b in used]
        result = slope_range(points)
        flat = bool(points) and all(p[1] == 1.0 and p[2] == 1.0 for p in points)
        notes = []
        if flat and not above and not open_:
            notes.append("D_min = 1 throughout")
        elif flat:
            notes.append("D_min = 1 where decided")
        if above:
            notes.append("no reliable D on the grid at N = " + " ".join(map(str, above)))
        if open_:
            notes.append("still open on reliability at N = " + " ".join(map(str, open_)))
        if flat:
            slope = "0 (flat, decided sizes only)" if above or open_ else "0 (flat)"
        elif result is None:
            slope = "-"
            notes.append("fewer than two decided flock sizes")
        else:
            slope = f"{result[0]:.2f} to {result[1]:.2f}"
        rows.append(
            {
                "layout": layout,
                "slope_range": slope,
                "n_used": " ".join(str(n) for n, _ in used) or "-",
                "note": "; ".join(notes),
            }
        )
    return pd.DataFrame(rows)


def dsat_bracket(row: pd.Series) -> tuple[float, float] | None:
    """Extracts the [low, high] bounds for D_sat, accounting for undecided faster comparisons."""
    if pd.isna(row["d_sat"]) or bool(row.get("still_improving_at_top", False)):
        return None
    low = float(row["d_sat"])
    if bool(row.get("d_sat_undecided", False)) and pd.notna(row["d_max"]):
        return low, max(low, float(row["d_max"]))
    return low, low


def dsat_text(row: pd.Series) -> str:
    """Formats D_sat or its bracket as a display string (e.g. '5', '5-24', '[24]')."""
    if pd.isna(row["d_sat"]):
        return "-"
    if bool(row.get("still_improving_at_top", False)):
        return f"[{int(row['d_sat'])}]"
    low, high = dsat_bracket(row) or (row["d_sat"], row["d_sat"])
    return str(int(low)) if low >= high else f"{int(low)}-{int(high)}"


def dsat_by_n(table: pd.DataFrame, layouts: tuple[str, ...] | None = None) -> pd.DataFrame:
    """Pivots D_sat values into a 2D grid with layouts as rows and flock sizes N as columns."""
    table = one_level(table)
    shown = table.assign(text=table.apply(dsat_text, axis=1))
    wide = shown.pivot_table(index="layout", columns="n", values="text", aggfunc="first")
    if layouts is not None:
        wide = wide.reindex([layout for layout in layouts if layout in wide.index])
    return wide.fillna("-")


def dsat_growth(table: pd.DataFrame) -> pd.DataFrame:
    """Computes log-log scaling slope ranges for D_sat vs N across layouts."""
    rows = []
    for layout, part in one_level(table).groupby("layout", sort=False):
        points, left_out = [], []
        for _, row in part.sort_values("n").iterrows():
            b = dsat_bracket(row)
            if b:
                points.append((int(row["n"]), b[0], b[1]))
            else:
                left_out.append(int(row["n"]))
        result = slope_range(points)
        if points and all(p[1] == p[2] == 1.0 for p in points):
            slope = "0 (flat)"
        else:
            slope = "-" if result is None else f"{result[0]:.2f} to {result[1]:.2f}"
        rows.append(
            {
                "layout": layout,
                "slope_range": slope,
                "n_used": " ".join(str(p[0]) for p in points) or "-",
                "n_left_out": " ".join(map(str, left_out)) or "-",
            }
        )
    return pd.DataFrame(rows)


def effort_table(cells: pd.DataFrame, table: pd.DataFrame) -> pd.DataFrame:
    """Evaluates completion time, dog-time, and trajectory length ratios beyond D_sat."""
    rows = []
    for _, curve in one_level(table).iterrows():
        if pd.isna(curve["d_sat"]) or pd.isna(curve["d_max"]):
            continue
        sat, top = int(curve["d_sat"]), int(curve["d_max"])
        if top <= sat:
            continue
        factors = [str(curve["factors"])] if curve.get("factors") else []
        key = "|".join([str(curve["method"]), str(curve["layout"]), *factors, f"N={curve['n']}"])
        mine = cells[(cells["group_key"] == key) & (cells["reliability"] == "reliable")]
        medians = {
            int(c["n_shepherds"]): (
                float(c["median_finish"]),
                float(c["median_dog_ticks"]),
                int(c["n_shepherds"]) * float(c["median_path_per_dog"]),
            )
            for _, c in mine.iterrows()
        }
        if sat not in medians:
            continue
        working = [d for d in medians if sat <= d <= top]
        base = medians[sat]

        def ratios(d: int) -> dict[str, float]:
            return dict(
                zip(("time", "dog_time", "path"), (v / b for v, b in zip(medians[d], base)))
            )

        double = next((d for d in sorted(working) if d >= 2 * sat), None)
        row: dict[str, Any] = {
            "layout": curve["layout"],
            "n": int(curve["n"]),
            "d_sat": dsat_text(curve),
            "d_double": double if double is not None else "-",
        }
        for label, d in (("double", double), ("top", top)):
            r = ratios(d) if d is not None else {}
            for name in ("time", "dog_time", "path"):
                row[f"{name}_{label}"] = round(r[name], 2) if name in r else "-"
        row["d_top"] = top
        rows.append(row)
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).sort_values(["layout", "n"], ignore_index=True)


def unusual_zones(cells: pd.DataFrame) -> pd.DataFrame:
    """Identifies cells exhibiting performance degradation (crowded, dip, collapse, or recovery)."""
    flagged = cells[cells["zone"].isin(["crowded", "unreliable_dip", "collapse", "recovered"])]
    rows = []
    for key, part in flagged.groupby("group_key", sort=True):
        curve = cells[cells["group_key"] == key]
        reliable = curve[curve["reliability"] == "reliable"].sort_values("median_finish")
        fastest = reliable.iloc[0] if len(reliable) else None
        for _, cell in part.iterrows():
            rows.append(
                {
                    **{k: v for k, v in parse_group_key(str(key)).items() if k != "factors"},
                    "d": int(cell["n_shepherds"]),
                    "zone": cell["zone"],
                    "success_rate": round(float(cell["success_rate"]), 2),
                    "median_finish": cell["median_finish"],
                    "fastest_d": int(fastest["n_shepherds"]) if fastest is not None else "-",
                    "fastest_finish": fastest["median_finish"] if fastest is not None else "-",
                }
            )
    return pd.DataFrame(rows)


def frontier_values(table: pd.DataFrame) -> pd.DataFrame:
    """Compiles D_min, D_sat, D_crowd, and D_max values across methods into a comparison table."""
    rows = []
    for _, curve in table.iterrows():
        rows.append(
            {
                "method": curve["method"],
                "layout": curve["layout"],
                "n": int(curve["n"]),
                "d_min": dmin_text(curve),
                "d_sat": dsat_text(curve),
                "d_crowd": "-" if pd.isna(curve["d_crowd"]) else int(curve["d_crowd"]),
                "d_max": "-" if pd.isna(curve["d_max"]) else int(curve["d_max"]),
            }
        )
    return pd.DataFrame(rows).sort_values(["method", "layout", "n"], ignore_index=True)


def extent_check(trials: pd.DataFrame, radii: dict[str, dict[str, float]]) -> pd.DataFrame:
    """Compares empirical flock RMS extent against calibrated reference radius R_f."""
    rows = []
    for _, part in trials.groupby(["group_key", "n_shepherds"], sort=True):
        info = parse_group_key(str(part["group_key"].iloc[0]))
        d = part["n_shepherds"].iloc[0]
        radius = radii[info["method"]][str(info["n"])]
        ratio = np.sqrt(2.0) * part["mean_extent"].astype(float) / radius
        rows.append(
            {
                "layout": info["layout"],
                "n": info["n"],
                "d": int(d),
                "r_f": round(radius, 2),
                "extent_over_r_f": round(float(ratio.median()), 2),
            }
        )
    return pd.DataFrame(rows).sort_values(["layout", "n", "d"], ignore_index=True)


def midpoint(row: pd.Series) -> float | None:
    """Calculates the geometric mean of a D_min bracket or lower bound."""
    b = bracket(row)
    if b:
        return math.sqrt(b[0] * b[1])
    if pd.notna(row["d_min_low"]):
        return float(row["d_min_low"])
    return None


def layout_against_n(table: pd.DataFrame) -> dict[str, float]:
    """Compares the average dynamic range of D_min across layouts vs across flock sizes N."""
    rows = one_level(table).iterrows()
    mid = {(str(r["layout"]), int(r["n"])): midpoint(r) for _, r in rows}
    mid = {k: v for k, v in mid.items() if v is not None}

    def spread(values: list[float]) -> float | None:
        return math.log2(max(values) / min(values)) if len(values) >= 2 else None

    by_n = [
        spread([v for (_, n2), v in mid.items() if n2 == n]) for n in sorted({n for _, n in mid})
    ]
    by_layout = [
        spread([v for (lay2, _), v in mid.items() if lay2 == lay])
        for lay in sorted({lay for lay, _ in mid})
    ]
    by_n = [s for s in by_n if s is not None]
    by_layout = [s for s in by_layout if s is not None]
    return {
        "layout_spread_at_fixed_n": float(np.mean(by_n)) if by_n else float("nan"),
        "n_spread_at_fixed_layout": float(np.mean(by_layout)) if by_layout else float("nan"),
    }


def compare(base: pd.DataFrame, variant: pd.DataFrame) -> pd.DataFrame:
    """Constructs a side-by-side comparison matrix ('base / variant') across layouts and N."""
    keys = ["layout", "n"]
    b = base.assign(text=base.apply(dmin_text, axis=1))[keys + ["text"]]
    v = variant.assign(text=variant.apply(dmin_text, axis=1))[keys + ["factors", "text"]]
    merged = v.merge(b, on=keys, how="left", suffixes=("_variant", "_base"))
    merged["pair"] = merged["text_base"].fillna("-") + " / " + merged["text_variant"]
    merged["row"] = merged["factors"].where(merged["factors"] != "", "")
    merged["col"] = merged["layout"] + " N=" + merged["n"].astype(str)
    out = merged.pivot_table(index="row", columns="col", values="pair", aggfunc="first")
    return out.fillna("-")


def dips(cells: pd.DataFrame, groups: pd.DataFrame) -> pd.DataFrame:
    """Identifies cells where success fell below theta despite exceeding D_min."""
    d_min = {r["group_key"]: r["d_min"] for _, r in groups.iterrows()}
    rows = []
    for _, cell in cells.iterrows():
        floor = d_min.get(cell["group_key"])
        if floor is None or pd.isna(floor):
            continue
        if cell["n_shepherds"] > floor and cell["reliability"] == "unreliable":
            key = parse_group_key(cell["group_key"])
            rows.append(
                {
                    "layout": key["layout"],
                    "n": key["n"],
                    "d": int(cell["n_shepherds"]),
                    "d_min": int(floor),
                    "success_rate": round(float(cell["success_rate"]), 2),
                    "seeds": int(cell["n_seeds"]),
                    "zone": cell["zone"],
                }
            )
    return pd.DataFrame(rows)


def run_record(queue_log: Path, results_root: Path | None = None) -> pd.DataFrame:
    """Extracts the latest status and execution metrics for each protocol from queue logs."""
    if not queue_log.exists():
        return pd.DataFrame()
    entries = [json.loads(line) for line in queue_log.read_text().splitlines() if line.strip()]
    last: dict[str, dict[str, Any]] = {}
    for entry in entries:
        last[entry["protocol"]] = entry
    current = {
        "trials": "trials_done",
        "cells": "cells",
        "cells_needing_seeds": "cells_needing_seeds",
        "cells_at_max_seeds_undecided": "cells_at_max_seeds_undecided",
        "trial_errors": "trial_errors",
    }
    for protocol, entry in last.items():
        status = results_root / protocol / "status.json" if results_root else None
        if status is not None and status.exists():
            found = json.loads(status.read_text())
            last[protocol] = {**entry, **{k: found[v] for k, v in current.items() if v in found}}
    cols = [
        "protocol",
        "finished",
        "trials",
        "cells",
        "cells_needing_seeds",
        "cells_at_max_seeds_undecided",
        "trial_errors",
        "hours",
        "workers",
        "outcome",
    ]
    return pd.DataFrame([{c: e.get(c, "") for c in cols} for e in last.values()])


__all__ = [
    "arrival_groups",
    "bracket",
    "compare",
    "dips",
    "dmin_text",
    "dsat_bracket",
    "dsat_by_n",
    "dsat_growth",
    "dsat_text",
    "effort_table",
    "extent_check",
    "frontier_values",
    "groups_table",
    "growth_table",
    "layout_against_n",
    "layout_by_n",
    "midpoint",
    "one_level",
    "parse_group_key",
    "run_record",
    "slope_range",
    "split_group_key",
    "unusual_zones",
]
