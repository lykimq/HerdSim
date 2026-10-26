"""Formatting and header notices for machine-generated files.

Marks output files (YAML, CSV, JSON, JSONL) with non-editable provenance notices:
- Text formats (YAML, CSV, JSONL): Prefixed with `# AUTO-GENERATED: ...`
- Structured JSON: Includes `_auto_generated_notice` as the leading key.
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
    """Prepend auto-generated notice metadata to a dictionary before JSON serialization."""
    return {JSON_NOTICE_KEY: AUTO_GENERATED_NOTICE, **payload}


def write_csv(df: pd.DataFrame, path: Path) -> None:
    """Atomically write DataFrame to CSV with an auto-generated header notice."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", newline="") as f:
        f.write(NOTICE_LINE + "\n")
        df.to_csv(f, index=False)
    tmp.replace(path)
