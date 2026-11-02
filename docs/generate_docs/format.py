"""Value text, Markdown tables, and replay CSV summaries for the docs."""


from __future__ import annotations

import re
from collections.abc import Sequence

import pandas as pd

from analysis.curves import dsat_bracket

# Short labels for factors shown in overview tables.
FACTOR_LABELS = {
    "goal_radius_multiple": "goal {} R_f",
    "dog_start_gap": "gap {} m",
    "sensing_range": "range {} m",
    "communication": "{}",
}


# Matches a cell that should be centred as a number in Markdown tables.
NUMBER_CELL = re.compile(
    r"^(-|none( on grid)?|[\[(]?[-+]?\d[\d.,%\- ]*[\])]?( \((max|over) \d+(, (max|over) \d+)*\))*)$"
)


# Shared notation key for D_min / D_sat tables on the summary and results pages.
DMIN_KEY = (
    "An entry of a $D_{\\min}$ table is the smallest number of dogs whose success rate is at "
    "least 0.90 with 99% confidence "
    "([decision rules](d_min_report.md#21-when-a-team-is-reliable)):\n\n"
    "- `3`: decided; every smaller team is unreliable.\n"
    "- `3-8`: 8 dogs are reliable and teams below 3 are unreliable; 3 to 7 are not known to be "
    "reliable at the seed limit of 200 trials per cell.\n"
    "- `[5]`: no team is reliable yet and teams below 5 are unreliable.\n"
    "- `none` or `none on grid`: every team tested is unreliable."
)
DSAT_KEY = (
    "An entry of a $D_{\\mathrm{sat}}$ table is the smallest working team that no larger working "
    "team beats on finish time by more than 5% with 99% confidence:\n\n"
    "- `5`: decided.\n"
    "- `5-24`: a larger team may still turn out faster.\n"
    "- `[24]`: the finish time is still falling at the largest team tested.\n"
    "- `-`: no team is reliable."
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


# Grid identifiers shown beside the layout, not as value columns.
IDENTIFIER_HEADERS = ("n", "d")
# Column header that is only a flock size ('25' or 'N=25').
SIZE_HEADER = re.compile(r"(N=)?\d+")
# Prefer one field per line when a row has this many value fields or more.
NESTED_FIELDS = 9


def _cells(line: str) -> list[str]:
    """Split one Markdown table row into cells, keeping escaped pipes."""
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip()[1:-1])]


def _label(header: str, cell: str) -> str:
    """Format a label cell: N=100 / D=3 for size columns, else header=value or the name."""
    if header in IDENTIFIER_HEADERS:
        return f"{header.upper()}={cell}"
    return f"{header}={cell}" if NUMBER_CELL.match(cell) else cell


def _entry(header: Sequence[str], row: Sequence[str], labels: int) -> str:
    """One list entry: labels, then each filled value with its header."""
    name = ", ".join(_label(h, c) for h, c in zip(header[:labels], row[:labels], strict=True) if c)
    values = ", ".join(
        f"{f'N={h}' if h.isdigit() else h} {v}"
        for h, v in zip(header[labels:], row[labels:], strict=True)
        if v
    )
    return f"- {name}: {values}" if name and values else f"- {name or values}"


def _names(header: Sequence[str], row: Sequence[str]) -> str:
    return ", ".join(_label(h, c) for h, c in zip(header, row, strict=True) if c)


def _nested(
    header: Sequence[str], rows: Sequence[Sequence[str]], labels: int, named: int
) -> list[str]:
    """Many-field rows as a nested list under layout, then N/D, then fields."""
    out: list[str] = []
    last = None
    for row in rows:
        group = _names(header[:named], row[:named])
        ident = _names(header[named:labels], row[named:labels])
        if group and ident:
            if group != last:
                out.append(f"- {group}")
            head, depth = ident, 1
        else:
            head, depth = group or ident, 0
        last = group
        if head:
            out.append(f"{'  ' * depth}- {head}")
        indent = "  " * (depth + bool(head))
        out.extend(
            f"{indent}- {h}: {v}" for h, v in zip(header[labels:], row[labels:], strict=True) if v
        )
    return out


def _grouped(header: Sequence[str], rows: Sequence[Sequence[str]], labels: int) -> list[str]:
    """One line per row, grouped under a shared first label when it repeats."""
    out: list[str] = []
    last = None
    repeats = len({row[0] for row in rows}) < len(rows)
    for row in rows:
        if labels < 2 or not row[0] or not repeats:
            out.append(_entry(header, row, labels))
            last = None
            continue
        if row[0] != last:
            out.append(f"- {_label(header[0], row[0])}")
        last = row[0]
        out.append("  " + _entry(header[1:], row[1:], labels - 1))
    return out


def as_entries(page: str) -> str:
    """Rewrite every Markdown table on a page as a bullet list."""
    out: list[str] = []
    table: list[str] = []

    def flush() -> None:
        if table:
            header, align, *rows = (_cells(line) for line in table)
            labels = max(next((i for i, a in enumerate(align) if a == ":---:"), 1), 1)
            named = labels
            while labels < len(header) and header[labels] in IDENTIFIER_HEADERS:
                labels += 1
            values = header[labels:]
            if len(values) >= NESTED_FIELDS and not all(SIZE_HEADER.fullmatch(h) for h in values):
                out.extend(_nested(header, rows, labels, named))
            else:
                out.extend(_grouped(header, rows, labels))
            table.clear()

    for line in page.splitlines():
        if line.startswith("|"):
            table.append(line)
        else:
            flush()
            out.append(line)
    flush()
    return "\n".join(out) + "\n"


def int_or_dash(value: float) -> int | str:
    """Integer D value, or '-' when missing."""
    return "-" if pd.isna(value) else int(value)


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


def dsat_text(row: pd.Series) -> str:
    """D_sat as text: '5', '5-24', '[24]', or '-'."""
    if pd.isna(row["d_sat"]):
        return "-"
    found = dsat_bracket(row)
    if found is None:  # still improving at the top of the grid
        return f"[{int(row['d_sat'])}]"
    return _range_text(*found)


def slope_text(result: tuple[float, float] | None) -> str:
    return "-" if result is None else f"{result[0]:.2f} to {result[1]:.2f}"


def rule_text(fraction: float) -> str:
    """'strict' for fraction 1.0, else e.g. '99 percent'."""
    return "strict" if fraction == 1.0 else f"{round(fraction * 100)} percent"


def number_or_text(value: str) -> float | str:
    """Parse a factor level as float when possible, else leave as text."""
    try:
        return float(value)
    except ValueError:
        return value


def _number_text(value: str) -> str:
    """Trim trailing .0 from numeric levels; leave other text alone."""
    level = number_or_text(value)
    return level if isinstance(level, str) else f"{level:g}"


def variant_label(factors: list[tuple[str, str]]) -> str:
    """Human label for factor levels, e.g. 'goal 2.1 R_f'. Empty if no factors."""
    labels = []
    for name, value in factors:
        if name not in FACTOR_LABELS:
            raise ValueError(f"no overview label for factor {name!r}; add one to FACTOR_LABELS")
        labels.append(FACTOR_LABELS[name].format(_number_text(value)))
    return ", ".join(labels)

# --- Replay CSV summaries -------------------------------------------------------

# Decimal places used in printed summaries.
SUMMARY_DECIMALS_SPLIT = 2
SUMMARY_DECIMALS_WALK = 1


def split_summary(table: pd.DataFrame) -> pd.DataFrame:
    """Per deadline, N, D and version: success share, median finish, mean dogs stopped."""
    return (
        table.groupby(["deadline", "n", "d", "version"], sort=True)
        .agg(
            success=("success", "mean"),
            median_finish=("finish_seconds", "median"),
            stopped=("dogs_stopped", "mean"),
        )
        .round(SUMMARY_DECIMALS_SPLIT)
        .reset_index()
    )


def walk_summary(table: pd.DataFrame, by: list[str]) -> pd.DataFrame:
    """Medians per group over replays whose dogs cleared r_s."""
    cleared = table.dropna(subset=["walk"]).assign(
        goal_needed=lambda t: t["walk"] / 2 + t["farthest"]
    )
    out = cleared.groupby(by)[["walk", "seconds", "farthest", "goal_needed"]].median()
    out.insert(0, "cleared", cleared.groupby(by).size())
    out.insert(0, "replays", table.groupby(by).size())
    return out.round(SUMMARY_DECIMALS_WALK).reset_index()
