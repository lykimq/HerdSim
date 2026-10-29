"""How a value of the analysis is written in a table: D_min and D_sat as text, the success rule,
the label of a factor level, and a table as Markdown.

Every table the docs show writes its values through these functions, so '2-4', '[5]' and
'none on grid' mean one thing everywhere.
"""

from __future__ import annotations

import pandas as pd

from analysis.curves import dsat_bracket

# Short labels of the factors a protocol sweeps, as the overview tables show them.
FACTOR_LABELS = {
    "goal_radius_multiple": "goal {} R_f",
    "dog_start_gap": "gap {} m",
    "sensing_range": "range {} m",
    "communication": "{}",
}


def markdown(frame: pd.DataFrame, index: bool = False) -> str:
    """A Markdown table; no extra dependency. A "|" inside a cell is escaped, because a row of
    several factors is labelled "a=1|b=2" and would otherwise split into two cells."""
    if frame.empty:
        return "(no rows)"
    frame = frame.reset_index() if index else frame

    def text(v: object) -> str:
        return "" if isinstance(v, float) and pd.isna(v) else str(v).replace("|", "\\|")

    columns = [text(c) for c in frame.columns]
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    for row in frame.itertuples(index=False):
        lines.append("| " + " | ".join(text(v) for v in row) + " |")
    return "\n".join(lines)


def int_or_dash(value: float) -> int | str:
    """A D value as an integer, '-' when the curve has none."""
    return "-" if pd.isna(value) else int(value)


def numbers_text(values: list[int]) -> str:
    """'25 50 100', or '-' for none."""
    return " ".join(map(str, values)) or "-"


def _range_text(low: float, high: float) -> str:
    """'4' when the bracket is closed, '2-4' when it is open."""
    low, high = int(low), int(high)
    return str(high) if low >= high else f"{low}-{high}"


def dmin_text(row: pd.Series) -> str:
    """The true D_min as far as the curve decides it.

    '4' when D_min is decided (every smaller D is unreliable), '2-4' when D = 4 is the
    smallest reliable D but a D from 2 up is still undecided, '[2]' when no D is reliable
    yet and D_min is 2 or more, 'none on grid' when every D is unreliable, '-' with no data.
    """
    if pd.notna(row["d_min"]):
        high = row["d_min"]
        return _range_text(row["d_min_low"] if pd.notna(row["d_min_low"]) else high, high)
    if bool(row.get("d_min_above_grid", False)):
        return "none on grid"
    if pd.notna(row["d_min_low"]):
        return f"[{int(row['d_min_low'])}]"
    return "-"


def dsat_text(row: pd.Series) -> str:
    """'5' decided, '5-24' when a larger D may still turn out faster, '[24]' when the curve
    is still improving at the top of the grid, '-' without a reliable D."""
    if pd.isna(row["d_sat"]):
        return "-"
    found = dsat_bracket(row)
    if found is None:  # still improving at the top of the grid
        return f"[{int(row['d_sat'])}]"
    return _range_text(*found)


def slope_text(result: tuple[float, float] | None) -> str:
    return "-" if result is None else f"{result[0]:.2f} to {result[1]:.2f}"


def rule_text(fraction: float) -> str:
    """'strict' when every sheep must be in the goal, else the share, as '99 percent'."""
    return "strict" if fraction == 1.0 else f"{round(fraction * 100)} percent"


def number_or_text(value: str) -> float | str:
    """A factor level as a number when it reads as one ('15.0' -> 15.0), else the text."""
    try:
        return float(value)
    except ValueError:
        return value


def _number_text(value: str) -> str:
    """'15.0' -> '15', '2.5' -> '2.5'; text stays as it is."""
    level = number_or_text(value)
    return level if isinstance(level, str) else f"{level:g}"


def variant_label(factors: list[tuple[str, str]]) -> str:
    """[('goal_radius_multiple', '2.1')] -> 'goal 2.1 R_f'; empty without factors."""
    labels = []
    for name, value in factors:
        if name not in FACTOR_LABELS:
            raise ValueError(f"no overview label for factor {name!r}; add one to FACTOR_LABELS")
        labels.append(FACTOR_LABELS[name].format(_number_text(value)))
    return ", ".join(labels)
