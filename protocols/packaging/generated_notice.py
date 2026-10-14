"""Shared AUTO-GENERATED notice for machine-written files.

Every file the campaign or analysis code writes carries the notice at the top:

- YAML, CSV, JSONL: a first comment line ``# AUTO-GENERATED: ...``
- JSON: a first field ``_auto_generated_notice``
- Parquet timeseries: binary, no notice

CSV files must be read with ``read_csv`` here (or ``pd.read_csv(path, skiprows=1)``)
so the notice line is not parsed as the header. ``read_csv`` also accepts older
files written before the notice existed.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

AUTO_GENERATED_NOTICE = (
    "AUTO-GENERATED: do not modify. Re-run the producing command to refresh this file."
)

# First line for YAML / CSV / JSONL files.
NOTICE_LINE = f"# {AUTO_GENERATED_NOTICE}"

# Stable JSON key so tools can skip or display the notice.
JSON_NOTICE_KEY = "_auto_generated_notice"


def with_json_notice(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a new dict with the auto-generated notice as the first key."""
    return {JSON_NOTICE_KEY: AUTO_GENERATED_NOTICE, **payload}


def write_csv(df: pd.DataFrame, path: Path | str) -> None:
    """Write ``df`` as CSV with the notice as the first line."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        f.write(NOTICE_LINE + "\n")
        df.to_csv(f, index=False)


def read_csv(path: Path | str) -> pd.DataFrame:
    """Read a CSV written by ``write_csv``; older files without the notice also work."""
    with Path(path).open() as f:
        has_notice = f.readline().startswith("#")
    return pd.read_csv(path, skiprows=1 if has_notice else 0)
