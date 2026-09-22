"""Diagnostic plots for scaling protocols."""

from __future__ import annotations

from pathlib import Path

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
    sheep_col: str = "n_sheep",
    dog_col: str = "n_shepherds",
    value_col: str = "reliability",
) -> Path | None:
    """Save a reliability heatmap if matplotlib is available."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None
    if rates.empty or sheep_col not in rates.columns or dog_col not in rates.columns:
        return None
    mat = reliability_heatmap_data(
        rates,
        sheep_col=sheep_col,
        dog_col=dog_col,
        value_col=value_col,
    )
    if mat.empty:
        return None
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    im = ax.imshow(
        mat.to_numpy(dtype=float),
        aspect="auto",
        origin="lower",
        vmin=0,
        vmax=1,
        cmap="viridis",
    )
    ax.set_xticks(range(len(mat.columns)))
    ax.set_xticklabels([str(c) for c in mat.columns])
    ax.set_yticks(range(len(mat.index)))
    ax.set_yticklabels([str(i) for i in mat.index])
    ax.set_xlabel("D (shepherds)")
    ax.set_ylabel("N (sheep)")
    ax.set_title(title)
    fig.colorbar(im, ax=ax, label="R")
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def save_frontier_curve(
    frontier: pd.DataFrame,
    path: Path | str,
    *,
    title: str = "Frontier D_min(N)",
    group_col: str | None = None,
) -> Path | None:
    """Save D_min / D_overcrowd / D_max vs N. Optional group_col (e.g. layout)."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None
    if frontier.empty or "n_sheep" not in frontier.columns:
        return None
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))

    def _plot_group(df: pd.DataFrame, label_prefix: str = "") -> None:
        ordered = df.sort_values("n_sheep")
        n = ordered["n_sheep"].to_numpy()
        if "d_min" in ordered.columns:
            ax.plot(n, ordered["d_min"], marker="o", label=f"{label_prefix}D_min".strip())
        if "d_overcrowd" in ordered.columns:
            y = ordered["d_overcrowd"]
            if bool(y.notna().to_numpy().any()):
                ax.plot(
                    n,
                    y,
                    marker="s",
                    linestyle="--",
                    label=f"{label_prefix}D_overcrowd".strip(),
                )
        if "d_max" in ordered.columns:
            y = ordered["d_max"]
            if bool(y.notna().to_numpy().any()):
                ax.plot(
                    n,
                    y,
                    marker="^",
                    linestyle=":",
                    label=f"{label_prefix}D_max".strip(),
                )

    if group_col and group_col in frontier.columns:
        for g, sub in frontier.groupby(group_col, dropna=False):
            _plot_group(sub, label_prefix=f"{g}: ")
    else:
        _plot_group(frontier)

    ax.set_xlabel("N (sheep)")
    ax.set_ylabel("D (shepherds)")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def save_regime_counts(
    regimes: pd.DataFrame,
    path: Path | str,
    *,
    title: str = "Regime counts",
    regime_col: str = "regime",
) -> Path | None:
    """Bar chart of regime label frequencies."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return None
    if regimes.empty or regime_col not in regimes.columns:
        return None
    counts = regimes[regime_col].value_counts().sort_index()
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(counts.index.astype(str), counts.to_numpy())
    ax.set_ylabel("Cells")
    ax.set_title(title)
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out
