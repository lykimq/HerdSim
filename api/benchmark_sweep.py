"""Parameter-grid helpers for Analytics benchmarks."""

from __future__ import annotations

from itertools import product
from typing import Any


def parse_sweep_specs(sweep: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    """Normalize sweep specs to [{key, values}, ...] (at most two params)."""
    if not sweep:
        return []
    specs: list[dict[str, Any]] = []
    for item in sweep:
        key = str(item.get("key") or "").strip()
        values = item.get("values")
        if not key:
            raise ValueError("Each sweep entry needs a non-empty key")
        if not isinstance(values, list) or not values:
            raise ValueError(f"Sweep '{key}' needs a non-empty values list")
        parsed: list[float | int] = []
        for raw in values:
            num = float(raw)
            parsed.append(int(num) if num.is_integer() else num)
        specs.append({"key": key, "values": parsed})
    if len(specs) > 2:
        raise ValueError("Param sweep supports at most 2 parameters")
    return specs


def expand_param_grid(specs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Cartesian product of sweep specs into algorithm_params dicts."""
    if not specs:
        return [{}]
    keys = [s["key"] for s in specs]
    value_lists = [s["values"] for s in specs]
    return [dict(zip(keys, combo)) for combo in product(*value_lists)]


def sweep_label(params: dict[str, Any]) -> str:
    if not params:
        return ""
    return ", ".join(f"{k}={params[k]}" for k in sorted(params))
