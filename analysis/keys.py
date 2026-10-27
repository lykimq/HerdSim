"""The text keys that name groups, cells and trials in rows, logs and tables.

    group  method|layout|name=value|...|N=n
    cell   <group>|D=d
    trial  <cell>|seed=i

Every results folder stores these keys, so the format is fixed. This module is its one
definition: the campaign builds keys here and the analysis splits them here. It sits in the
analysis layer, which imports nothing else of the project, so both sides can use it.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

SEP = "|"


def value_text(value: Any) -> str:
    """A factor value as written in keys: numbers as floats, so 1 and 1.0 name one cell, as
    they run one physics (provenance.normalise_numbers)."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return repr(float(value))
    return str(value)


def group_key(method: str, layout: str, factors: Iterable[tuple[str, Any]], n: int) -> str:
    """The key of one D curve; ``factors`` are sorted (name, value) pairs."""
    parts = [method, layout, *(f"{k}={value_text(v)}" for k, v in factors)]
    return SEP.join([*parts, f"N={n}"])


def cell_key(group: str, d: int) -> str:
    return f"{group}{SEP}D={d}"


def trial_key(cell: str, seed_index: int) -> str:
    return f"{cell}{SEP}seed={seed_index}"


def group_of_cell(cell: str) -> str:
    return cell.rsplit(f"{SEP}D=", 1)[0]


def cell_of_trial(trial: str) -> str:
    return trial.rsplit(f"{SEP}seed=", 1)[0]


def split_group(key: str) -> dict[str, Any]:
    """'strombom_multi|wide|dog_start_gap=15.0|N=200' -> method, layout, factors, n, with the
    factor parts kept as one text ('dog_start_gap=15.0'), as the tables show them."""
    parts = key.split(SEP)
    return {
        "method": parts[0],
        "layout": parts[1],
        "factors": SEP.join(parts[2:-1]),
        "n": int(parts[-1].removeprefix("N=")),
    }


def join_group(method: str, layout: str, factors: str, n: int) -> str:
    """The inverse of ``split_group``: a group key from its parts, factors as one text."""
    return SEP.join([method, layout, *([factors] if factors else []), f"N={n}"])
