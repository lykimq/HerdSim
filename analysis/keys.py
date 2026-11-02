"""Build and split the text keys for groups, cells and trials."""

from __future__ import annotations

from typing import Any

SEP = "|"


def group_key(method: str, layout: str, n: int) -> str:
    """The key of one D curve."""
    return SEP.join([method, layout, f"N={n}"])


def cell_key(group: str, d: int) -> str:
    return f"{group}{SEP}D={d}"


def trial_key(cell: str, seed_index: int) -> str:
    return f"{cell}{SEP}seed={seed_index}"


def group_of_cell(cell: str) -> str:
    return cell.rsplit(f"{SEP}D=", 1)[0]


def cell_of_trial(trial: str) -> str:
    return trial.rsplit(f"{SEP}seed=", 1)[0]


def split_group(key: str) -> dict[str, Any]:
    """'strombom_multi|wide|N=200' -> method, layout, n."""
    method, layout, n = key.split(SEP)
    return {"method": method, "layout": layout, "n": int(n.removeprefix("N="))}
