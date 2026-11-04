"""Tables and figures of the Strombom et al. (2014) check (docs/methods/strombom_check.md).

Tables come out through the `paper` verb of page.py; figures through make_figures.py (the
layout) and make_result_figures.py (the results). The paper's own figures are cropped from
its PDF with pdftoppm and set beside HerdSim's for a comparison by eye.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle, Rectangle

from docs.generate_docs.figstyle import (
    AQUA,
    BLUE,
    GRID,
    INK,
    MUTED,
    ORANGE,
    REPO,
    SURFACE,
    grid,
    save,
)
from docs.generate_docs.figures import dogs_at, style_map, window
from paper_check import settings as paper
from paper_check.sweep import EXPERIMENTS, neighbour_count, read
from paper_check.trials import dog_box, paper_config, seed_of
from sim.trial import initial_state

PAPER_PDF = REPO / "docs" / "papers" / "Strombom_et_al.pdf"
# A figure of the paper: (page, box as shares of the page: left, right, top, bottom).
PAPER_FIG3 = (3, (0.19, 0.83, 0.395, 0.645))
PAPER_DPI = 200
# The paper's edge of the always-successful region, n = 0.53 N, stated in its text. Its lower
# curve, n about 3 log N, has no stated base and is not drawn.
SHARE_LINE = 0.53
LAYOUT_N = 100  # flock size of the layout figure


# ----- tables -----
def fig3_table(trials: pd.DataFrame) -> pd.DataFrame:
    """Trials finished per Fig. 3 point: N rows, one column per share of N, the last the
    global case; '-' marks a point not run yet."""
    counts = trials.groupby(["n_sheep", "n_neighbors"])["success"].sum().to_dict()
    labels = [f"n = {s}N" for s in paper.NEIGHBOUR_SHARES] + ["n = N-1"]
    rows = []
    for n_sheep in paper.FLOCK_SIZES:
        row: dict[str, int | str] = {"N": n_sheep}
        for label, share in zip(labels, [*paper.NEIGHBOUR_SHARES, None], strict=True):
            n = n_sheep - 1 if share is None else neighbour_count(n_sheep, share)
            row[label] = int(counts[(n_sheep, n)]) if (n_sheep, n) in counts else "-"
        rows.append(row)
    return pd.DataFrame(rows)


def distance_table(trials: pd.DataFrame) -> pd.DataFrame:
    """Per l: runs that finished and the mean (min-max) time steps of those."""
    done = trials[trials["success"]].groupby("distance")["steps"]
    table = pd.DataFrame(
        {
            "finished": trials.groupby("distance")["success"].sum(),
            "steps": done.mean().round(0).astype(int).astype(str)
            + " ("
            + done.min().astype(str)
            + "-"
            + done.max().astype(str)
            + ")",
        }
    )
    return table.reset_index().rename(columns={"distance": "l"})


def distance_fit(trials: pd.DataFrame) -> tuple[float, float, float]:
    """(intercept, slope, R^2) of the least-squares line of mean steps (finished runs) on l."""
    means = trials[trials["success"]].groupby("distance")["steps"].mean()
    slope, intercept = np.polyfit(means.index, means.to_numpy(), 1)
    residual = means - (slope * means.index + intercept)
    r2 = 1.0 - float((residual**2).sum() / ((means - means.mean()) ** 2).sum())
    return float(intercept), float(slope), r2


def tables() -> list[tuple[str | None, pd.DataFrame | str]]:
    """Every table of the check that has stored trials, with its heading."""
    fig3 = read("fig3")
    out: list[tuple[str | None, pd.DataFrame | str]] = [
        ("Fig. 3", fig3_table(fig3)),
    ]
    if EXPERIMENTS["distance"].path.exists():
        distance = read("distance")
        intercept, slope, r2 = distance_fit(distance)
        line = f"Mean steps = {intercept:.0f} + {slope:.2f} l, R^2 = {r2:.4f} (finished runs)."
        out += [("Distance study", distance_table(distance)), (None, line)]
    return out


# ----- figures -----
def paper_figure(page_and_box: tuple[int, tuple[float, float, float, float]]) -> np.ndarray:
    """A figure of the paper as an image, cropped from its PDF page."""
    number, (left, right, top, bottom) = page_and_box
    command = ["pdftoppm", "-f", str(number), "-l", str(number), "-r", str(PAPER_DPI), "-png"]
    with tempfile.TemporaryDirectory() as tmp:
        try:
            subprocess.run([*command, str(PAPER_PDF), str(Path(tmp) / "page")], check=True)
        except FileNotFoundError as err:
            raise RuntimeError("pdftoppm (poppler-utils) is needed to crop the paper") from err
        image = plt.imread(next(Path(tmp).glob("page*.png")))
    height, width = image.shape[:2]
    return image[int(top * height) : int(bottom * height), int(left * width) : int(right * width)]


def _paper_panel(ax: Axes, page_and_box: tuple[int, Any], title: str) -> None:
    ax.imshow(paper_figure(page_and_box))
    ax.axis("off")
    ax.set_title(title)


def _missing(name: str) -> bool:
    path = EXPERIMENTS[name].path
    if not path.exists():
        print("missing", path, ": figure skipped")
    return not path.exists()


def _fig3_panel(ax: Axes, trials: pd.DataFrame, title: str) -> Any:
    rate = trials.groupby(["n_sheep", "n_neighbors"])["success"].mean().reset_index()
    colors = LinearSegmentedColormap.from_list("success", [BLUE, SURFACE])
    points = ax.scatter(
        rate["n_sheep"], rate["n_neighbors"], c=rate["success"], cmap=colors, vmin=0, vmax=1,
        marker="s", s=40, edgecolor=MUTED, linewidth=0.4,
    )  # fmt: skip
    sizes = np.linspace(2, 150, 100)
    ax.plot(sizes, SHARE_LINE * sizes, color=INK, lw=0.9)
    ax.set(xlim=(0, 156), ylim=(0, 156), xlabel="no. agents (N)", ylabel="no. neighbours (n)")
    ax.set_title(title)
    return points


def fig_paper_check() -> None:
    """Fig. 3 of the paper beside HerdSim's run of the same task."""
    if _missing("fig3"):
        return
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4), gridspec_kw={"width_ratios": (1.3, 1)})
    _paper_panel(axes[0], PAPER_FIG3, "Strombom et al. (2014), Fig. 3")
    points = _fig3_panel(axes[1], read("fig3"), "HerdSim, same task")
    fig.colorbar(points, ax=axes[1], label=f"share of {paper.FIG3_TRIALS} trials that finish")
    save(fig, "fig_paper_check.png", layout=False)


def fig_paper_distance() -> None:
    """Time to finish against the distance to the goal, with the least-squares line."""
    if _missing("distance"):
        return
    trials = read("distance")
    stats = trials[trials["success"]].groupby("distance")["steps"].agg(["mean", "min", "max"])
    intercept, slope, _ = distance_fit(trials)
    fig, ax = plt.subplots(figsize=(6, 4.0))
    ax.fill_between(stats.index, stats["min"], stats["max"], color=BLUE, alpha=0.15, lw=0)
    ax.plot(stats.index, stats["mean"], color=BLUE, marker="o", ms=4, lw=0, label="mean")
    ax.plot(stats.index, intercept + slope * stats.index, color=INK, lw=0.9, label="fitted line")
    ax.set(xlabel="distance to target l", ylabel="time steps to finish")
    ax.set_title("HerdSim, the paper's distance study")
    ax.legend(frameon=False, fontsize=8)
    grid(ax)
    save(fig, "fig_paper_distance.png")


def _paper_layout_panel(ax: Axes) -> None:
    """The start of the paper's task: field, the two start squares and the goal."""
    n, side = LAYOUT_N, paper.FIELD_SIDE
    state = initial_state(paper_config(n, n - 1), seed_of(n, 0))
    for (low, high), color in ((paper.SHEEP_BOX, BLUE), (dog_box(paper.SHEEP_BOX), ORANGE)):
        ax.add_patch(Rectangle((low, low), high - low, high - low, fc=color, ec="none", alpha=0.1))
    ax.add_patch(Rectangle((0, 0), side, side, fc="none", ec=GRID, lw=1.0))
    ax.add_patch(Circle((0, 0), paper.DONE_DISTANCE, fc="none", ec=AQUA, lw=1.5))
    ax.scatter(*state.sheep_positions.T, s=7, color=BLUE, alpha=0.85, lw=0)
    dogs_at(ax, state.shepherd_positions)
    ax.text(side - 3, side + 5, "sheep start here", ha="right", color=BLUE)
    ax.text(side / 2 - 3, side / 2 + 5, "dog starts here", ha="right", color=ORANGE)
    ax.text(paper.DONE_DISTANCE + 4, -14, f"goal, {paper.DONE_DISTANCE:.0f} m", color=AQUA)
    ax.text(side, -14, f"field {side:.0f} m", ha="right", color=MUTED)
    window(ax, (side / 2, side / 2), 130, 130, 100, 100)
    style_map(ax, f"the paper's start as the check runs it, N = {n}")


def fig_paper_layout() -> None:
    """Start of one trial of the paper's task, as the check runs it."""
    fig, ax = plt.subplots(figsize=(5.8, 4.6))
    _paper_layout_panel(ax)
    save(fig, "fig_paper_layout.png")


FIGURES = (fig_paper_check, fig_paper_distance)
