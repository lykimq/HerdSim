"""Notice marking machine-written files.

- YAML, CSV, JSONL: first line ``# AUTO-GENERATED: ...``
- JSON: first field ``_auto_generated_notice``
- Parquet: binary, no notice

Read CSVs written here with ``pd.read_csv(path, skiprows=1)`` so the notice
line is skipped.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

AUTO_GENERATED_NOTICE = (
    "AUTO-GENERATED: do not modify. Re-run the producing command to refresh this file."
)
NOTICE_LINE = f"# {AUTO_GENERATED_NOTICE}"
JSON_NOTICE_KEY = "_auto_generated_notice"


def with_json_notice(payload: dict[str, Any]) -> dict[str, Any]:
    """New dict with the notice as its first key."""
    return {JSON_NOTICE_KEY: AUTO_GENERATED_NOTICE, **payload}


def write_csv(df: pd.DataFrame, path: Path) -> None:
    """Write ``df`` with the notice as the first line, atomically (temp file, then rename)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", newline="") as f:
        f.write(NOTICE_LINE + "\n")
        df.to_csv(f, index=False)
    tmp.replace(path)
