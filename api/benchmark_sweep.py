"""Factor-grid helpers for Analytics and CLI experiments."""

from __future__ import annotations

from itertools import product
from typing import Any

from core.experimental_factors import FACTOR_GRID_KEYS, MAX_FACTOR_GRID_CELLS


def parse_factor_specs(sweep: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    """Normalize factor specs to [{key, values}, ...]."""
    if not sweep:
        return []
    specs: list[dict[str, Any]] = []
    for item in sweep:
        key = str(item.get("key") or "").strip()
        values = item.get("values")
        if not key:
            raise ValueError("Each factor-grid entry needs a non-empty key")
        if not isinstance(values, list) or not values:
            raise ValueError(f"Factor '{key}' needs a non-empty values list")
        parsed: list[Any] = []
        for raw in values:
            if isinstance(raw, str):
                parsed.append(raw)
                continue
            num = float(raw)
            parsed.append(int(num) if num.is_integer() else num)
        specs.append({"key": key, "values": parsed})
    return specs


def expand_factor_grid(specs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Cartesian product of factor specs into flat override dicts."""
    if not specs:
        return [{}]
    keys = [s["key"] for s in specs]
    value_lists = [s["values"] for s in specs]
    combos = [dict(zip(keys, combo)) for combo in product(*value_lists)]
    if len(combos) > MAX_FACTOR_GRID_CELLS:
        raise ValueError(
            f"Factor grid has {len(combos)} cells; max is {MAX_FACTOR_GRID_CELLS}"
        )
    return combos


def sweep_label(params: dict[str, Any]) -> str:
    if not params:
        return ""
    return ", ".join(f"{k}={params[k]}" for k in sorted(params))


# Backward names used by older imports inside this repo during migration.
parse_sweep_specs = parse_factor_specs
expand_param_grid = expand_factor_grid
