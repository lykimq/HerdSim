"""Diagnostic plots for budget campaigns."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def reliability_heatmap_data(
    rates: pd.DataFrame,
    *,
    sheep_col: str = "n_sheep",
    dog_col: str = "n_shepherds",
    value_col: str = "reliability",
) -> pd.DataFrame:
    """Pivot reliability into an N x D matrix for heatmap plotting."""
    return rates.pivot(index=sheep_col, columns=dog_col, values=value_col)


def save_reliability_heatmap(
    rates: pd.DataFrame,
    path: Path | str,
    *,
    title: str = "Reliability R(N, D)",
) -> Path | None:
    """Save a reliability heatmap if matplotlib is available."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None
    mat = reliability_heatmap_data(rates)
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    im = ax.imshow(mat.to_numpy(dtype=float), aspect="auto", origin="lower", vmin=0, vmax=1)
    ax.set_xticks(range(len(mat.columns)))
    ax.set_xticklabels([str(c) for c in mat.columns])
    ax.set_yticks(range(len(mat.index)))
    ax.set_yticklabels([str(i) for i in mat.index])
    ax.set_xlabel("D (shepherds)")
    ax.set_ylabel("N (sheep)")
    ax.set_title(title)
    fig.colorbar(im, ax=ax, label="R")
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return out


def frontier_overlay_data(frontier: pd.DataFrame) -> dict[str, Any]:
    """Extract series useful for D_min(N) overlay plots."""
    cols = [c for c in ("n_sheep", "d_min", "d_overcrowd", "d_max") if c in frontier.columns]
    return frontier[cols].to_dict(orient="list")
