"""Value text and Markdown tables for the docs."""

from __future__ import annotations

import re
from collections.abc import Sequence

import pandas as pd

# Matches a cell that should be centred as a number in Markdown tables.
NUMBER_CELL = re.compile(r"^(-|none( on grid)?|[\[(]?[-+]?\d[\d.,%\- ]*[\])]?)$")


# Notation key for the D_min tables on the results page.
DMIN_KEY = (
    "An entry of a $D_{\\min}$ table is the smallest number of dogs whose success rate is at "
    "least 0.90 with 99% confidence "
    "([decision rules](d_min_report.md#23-when-a-team-is-reliable)). `3` is decided: every "
    "smaller team is unreliable. `3-8` means 8 dogs are reliable and teams below 3 are "
    "unreliable, while 3 to 7 are not known to be reliable at the seed limit of 200 trials per "
    "cell. `[5]` means no team is reliable yet and teams below 5 are unreliable. `none` or "
    "`none on grid` means every team tested is unreliable."
)


def markdown(frame: pd.DataFrame, index: bool = False) -> str:
    """Render a DataFrame as a Markdown table (escape `|`; centre number-like columns)."""
    if frame.empty:
        return "None."
    frame = frame.reset_index() if index else frame

    def text(v: object) -> str:
        return "" if isinstance(v, float) and pd.isna(v) else str(v).replace("|", "\\|")

    columns = [text(c) for c in frame.columns]
    rows = [[text(v) for v in row] for row in frame.itertuples(index=False)]

    def is_number_column(cells: Sequence[str]) -> bool:
        filled = [c for c in cells if c]
        return bool(filled) and all(NUMBER_CELL.match(c) for c in filled)

    align = [":---:" if is_number_column(col) else ":---" for col in zip(*rows, strict=True)]
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(align) + " |"]
    lines += ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join(lines)


def numbers_text(values: list[int]) -> str:
    """Space-separated integers, or '-' if empty."""
    return " ".join(map(str, values)) or "-"


def _range_text(low: float, high: float) -> str:
    """Closed bracket as '4', open as '2-4'."""
    low, high = int(low), int(high)
    return str(high) if low >= high else f"{low}-{high}"


def dmin_text(row: pd.Series) -> str:
    """D_min as decided by the curve: '4', '2-4', '[2]', 'none on grid', or '-'."""
    if pd.notna(row["d_min"]):
        high = row["d_min"]
        return _range_text(row["d_min_low"] if pd.notna(row["d_min_low"]) else high, high)
    if bool(row.get("d_min_above_grid", False)):
        return "none on grid"
    if pd.notna(row["d_min_low"]):
        return f"[{int(row['d_min_low'])}]"
    return "-"


def slope_text(result: tuple[float, float] | None) -> str:
    return "-" if result is None else f"{result[0]:.2f} to {result[1]:.2f}"


def rule_text(fraction: float) -> str:
    """'strict' for fraction 1.0, else e.g. '99 percent'."""
    return "strict" if fraction == 1.0 else f"{round(fraction * 100)} percent"
