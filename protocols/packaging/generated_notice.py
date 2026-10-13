"""Shared banner for machine-written artefacts.

Use this whenever code writes a file that should not be edited by hand.
Markdown and YAML get a literal first line. JSON gets a notice field that
callers should place first in the object when practical.
"""

from __future__ import annotations

from typing import Any

AUTO_GENERATED_NOTICE = (
    "AUTO-GENERATED: do not modify. Re-run the producing command to refresh this file."
)

# Stable JSON key so tools can skip or display the notice.
JSON_NOTICE_KEY = "_auto_generated_notice"


def markdown_banner_line() -> str:
    """First line for auto-generated Markdown files."""
    return AUTO_GENERATED_NOTICE


def yaml_banner_line() -> str:
    """First line for auto-generated YAML files."""
    return f"# {AUTO_GENERATED_NOTICE}"


def with_json_notice(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a new dict with the auto-generated notice as the first key."""
    return {JSON_NOTICE_KEY: AUTO_GENERATED_NOTICE, **payload}
