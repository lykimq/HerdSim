"""Animated GIFs of stored trials, for dynamics a still figure cannot show.

    uv run python docs/generate_docs/make_gifs.py              # every GIF
    uv run python docs/generate_docs/make_gifs.py one_trial    # one, by name

Replays study trials via services/replay.py (checked against stored outcomes) into docs/gifs/.
Layout: settings, helpers, overlays, then one function per GIF. Style from figstyle.py.
"""

from __future__ import annotations

import math
import sys
import textwrap
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle
from scipy.spatial.distance import cdist

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from docs.generate_docs.figstyle import (  # noqa: E402
    AQUA,
    BLUE,
    GIF_OUT,
    INK,
    MUTED,
    ORANGE,
    SURFACE,
)
from services.replay import open_run, replay_trial  # noqa: E402
from sim.core.simulation_state import SimulationState  # noqa: E402
from sim.methods.strombom.heuristics import COLLECT, collect_threshold, decide  # noqa: E402
from sim.plugins.dogs.collect_drive_multi import team_targets  # noqa: E402

# ----- settings -----
FPS = 12
FRAMES = 200  # about 17 s of animation, whatever the trial's length
HOLD_SECONDS = 2.0  # the last frame stays on screen this long before the loop restarts
DPI = 80
MARGIN = 12.0  # length units around everything that moves, so no agent touches the frame
NOTE_CHARS = 72  # note characters per panel width before it wraps
NOTE_LINE = 0.16  # inches per extra note line
PANEL_WIDTH = 4.6  # inches per panel; the height follows the view, so no space is wasted
# Every GIF replays the 99 percent run at 6 drive times.
RUN = "dmin_f99_m6"
METHOD = "strombom_multi"

View = tuple[tuple[float, float], tuple[float, float]]  # x limits and y limits of a panel

# ----- helpers -----
@dataclass(frozen=True)
class Shot:
    """One stored trial and its panel title."""

    layout: str
    n: int
    d: int
    seed_index: int
    title: str
    until: int | None = None  # first ticks only (trial start)


@dataclass
class Replayed:
    """Replayed trial at the ticks the frames show."""

    ticks: np.ndarray  # tick number of each kept frame, ascending
    herd: np.ndarray  # (frames, N, 2) positions of the sheep
    herders: np.ndarray  # (frames, D, 2)
    goal: np.ndarray
    goal_radius: float
    dt: float
    success: bool
    config: dict[str, Any]
    cut: bool  # True when shown only up to Shot.until

    @property
    def ending(self) -> str:
        return "succeeded" if self.success else "failed, time is up"

    def at(self, tick: int) -> int:
        """Index of the last kept frame at or before ``tick``."""
        return max(0, int(np.searchsorted(self.ticks, tick, side="right")) - 1)

    def outside(self, i: int) -> int:
        d = np.linalg.norm(self.herd[i] - self.goal, axis=1)
        return int((d > self.goal_radius).sum())


def shown_ticks(shot: Shot) -> int:
    """Stored trial length, or ``until`` if shorter."""
    outcome = open_run(RUN).outcomes(METHOD, shot.layout, shot.n, shot.d)
    stored = outcome[shot.seed_index][1]
    return stored if shot.until is None else min(stored, shot.until)


def replay(shot: Shot, every: int) -> Replayed:
    """Replay one stored trial, keeping every ``every``-th tick.

    The full trial is always replayed (and checked against the stored outcome) even when
    ``until`` cuts what is shown.
    """
    jobs = open_run(RUN).jobs(METHOD, shot.layout, shot.n, shot.d, shot.seed_index + 1)
    job = next(j for j in jobs if j.label["seed_index"] == shot.seed_index)
    end = shot.until if shot.until is not None else math.inf
    kept: list[tuple[int, np.ndarray, np.ndarray]] = []
    last: list[tuple[int, np.ndarray, np.ndarray]] = []

    def keep(state: SimulationState) -> None:
        if state.tick > end:
            return
        snapshot = (state.tick, state.sheep_positions.copy(), state.shepherd_positions.copy())
        if state.tick % every == 0:
            kept.append(snapshot)
        last[:] = [snapshot]

    result = replay_trial(job, on_tick=keep)
    if kept[-1][0] != last[0][0]:
        kept.append(last[0])
    ticks, herd, herders = zip(*kept)
    return Replayed(
        np.array(ticks),
        np.array(herd),
        np.array(herders),
        np.asarray(job.config["goal_center"], dtype=float),
        float(job.config["goal_radius"]),
        float(job.config["dt"]),
        bool(result.success),
        job.config,
        shot.until is not None and shot.until < int(result.total_ticks),
    )


def window(trials: list[Replayed]) -> View:
    """Shared view covering every trial's agents and goals."""
    points = np.vstack(
        [np.vstack([t.herd.reshape(-1, 2), t.herders.reshape(-1, 2)]) for t in trials]
    )
    goals = np.array([t.goal for t in trials])
    radius = max(t.goal_radius for t in trials)
    lo = np.minimum(points.min(axis=0), goals.min(axis=0) - radius)
    hi = np.maximum(points.max(axis=0), goals.max(axis=0) + radius)
    margin = max(MARGIN, 0.04 * float((hi - lo).max()))
    return (float(lo[0] - margin), float(hi[0] + margin)), (
        float(lo[1] - margin),
        float(hi[1] + margin),
    )


@dataclass
class Panel:
    """Artists for one trial panel."""

    trial: Replayed
    herd: Any
    herders: Any
    status: Any


def draw_panel(ax: Axes, trial: Replayed, title: str, view: View, dot: float) -> Panel:
    ax.set_aspect("equal")
    ax.set_xlim(*view[0])
    ax.set_ylim(*view[1])
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)
    ax.set_title(title, fontsize=10)
    centre = (float(trial.goal[0]), float(trial.goal[1]))
    ax.add_patch(Circle(centre, trial.goal_radius, fc="none", ec=AQUA, lw=1.5))
    herd = ax.scatter(*trial.herd[0].T, s=dot, color=BLUE, alpha=0.85, lw=0)
    herders = ax.scatter(
        *trial.herders[0].T, s=60, marker="^", color=ORANGE, ec=SURFACE, lw=0.8, zorder=3
    )
    status = ax.text(0.02, 0.03, "", transform=ax.transAxes, fontsize=9, color=INK)
    return Panel(trial, herd, herders, status)


def update_panel(panel: Panel, tick: int) -> None:
    """Show the panel at ``tick`` (or the last frame after the trial ends)."""
    trial = panel.trial
    i = trial.at(tick)
    panel.herd.set_offsets(trial.herd[i])
    panel.herders.set_offsets(trial.herders[i])
    seconds = trial.ticks[i] * trial.dt
    outside = trial.outside(i)
    if i == len(trial.ticks) - 1 and not trial.cut:
        panel.status.set_text(f"t = {seconds:.0f} s, {outside} outside: {trial.ending}")
        panel.status.set_color(INK if trial.success else ORANGE)
    else:
        panel.status.set_text(f"t = {seconds:.0f} s, {outside} sheep outside the goal")
        panel.status.set_color(INK)


Overlay = Callable[[Any, Panel], Callable[[int], None]]


def animate(
    shots: list[Shot],
    file: str,
    note: str,
    dot: float = 9,
    overlay: Overlay | None = None,
    frames: int = FRAMES,
) -> None:
    """Replay ``shots`` side by side on one shared clock as a looping GIF.

    ``overlay`` adds artists and returns their per-frame updater.
    """
    longest = max(shown_ticks(s) for s in shots)
    every = max(1, math.ceil(longest / frames))
    trials = [replay(s, every) for s in shots]
    view = window(trials)
    aspect = (view[1][1] - view[1][0]) / (view[0][1] - view[0][0])
    lines = textwrap.wrap(note, NOTE_CHARS * len(shots), break_on_hyphens=False)
    extra_height = NOTE_LINE * (len(lines) - 1)
    size = (PANEL_WIDTH * len(shots), PANEL_WIDTH * aspect + 0.9 + extra_height)
    fig, axes = plt.subplots(1, len(shots), figsize=size)
    panels = [
        draw_panel(ax, t, s.title, view, dot)
        for ax, t, s in zip(np.atleast_1d(axes), trials, shots)
    ]
    extras = [overlay(ax, p) for ax, p in zip(np.atleast_1d(axes), panels)] if overlay else []
    fig.text(0.5, 0.02, "\n".join(lines), ha="center", fontsize=8.5, color=MUTED)
    fig.tight_layout(rect=(0, (0.35 + extra_height) / size[1], 1, 1))
    ticks = list(range(0, longest, every)) + [longest] * (1 + round(HOLD_SECONDS * FPS))

    def draw(k: int) -> list[Any]:
        for panel in panels:
            update_panel(panel, ticks[k])
        for panel, update in zip(panels, extras):
            update(panel.trial.at(ticks[k]))
        return []

    animation = FuncAnimation(fig, draw, frames=len(ticks))
    animation.save(GIF_OUT / file, writer=PillowWriter(fps=FPS), dpi=DPI)
    plt.close(fig)
    print(file, f"{(GIF_OUT / file).stat().st_size / 1e6:.1f} MB")


# ----- overlays -----
def corner_text(ax: Axes) -> Any:
    """Top-right status line for overlay counts (time stays bottom left)."""
    return ax.text(
        0.98, 0.97, "", transform=ax.transAxes, ha="right", va="top", fontsize=9, color=INK
    )


def fill_herd(panel: Panel, filled: np.ndarray) -> None:
    """Fill sheep where ``filled`` is true; hollow elsewhere."""
    panel.herd.set_linewidths(0.8)
    panel.herd.set_facecolors([BLUE if f else SURFACE for f in filled])
    panel.herd.set_edgecolors([BLUE] * len(filled))


def reacting(ax: Axes, panel: Panel) -> Callable[[int], None]:
    """Fill sheep within r_s of a dog; hollow sheep are grazing."""
    trial = panel.trial
    r_s = float(trial.config["r_s"])
    label = corner_text(ax)

    def update(i: int) -> None:
        near = cdist(trial.herd[i], trial.herders[i]).min(axis=1) < r_s
        fill_herd(panel, near)
        label.set_text(f"{int(near.sum())} reacting, {int((~near).sum())} grazing")

    return update


def team_rule(ax: Axes, panel: Panel) -> Callable[[int], None]:
    """Mode, f(N) ring, and each dog's target from ``team_targets``."""
    trial = panel.trial
    config = trial.config
    f_n = collect_threshold(int(config["n_sheep"]), float(config["r_a"]))
    ring = Circle((0.0, 0.0), f_n, fc="none", ec=MUTED, lw=0.9, ls="--")
    ax.add_patch(ring)
    lines = LineCollection([], colors=ORANGE, linewidths=0.9, zorder=2)
    ax.add_collection(lines)
    crosses = ax.scatter([], [], s=40, marker="x", color=INK, lw=1.4, zorder=4)
    label = corner_text(ax)

    def update(i: int) -> None:
        sheep, dogs = trial.herd[i], trial.herders[i]
        mode = decide(sheep, trial.goal, config).mode
        targets = team_targets(sheep, trial.goal, dogs, config)
        ring.set_center(tuple(sheep.mean(axis=0)))
        lines.set_segments([[tuple(a), tuple(b)] for a, b in zip(dogs, targets)])
        crosses.set_offsets(targets)
        label.set_text("collecting" if mode == COLLECT else "driving")

    return update


# ----- GIFs -----
def one_trial() -> None:
    """One wide trial: collect outliers, then drive to the goal."""
    animate(
        [Shot("wide", 200, 4, 0, "the team rule, 4 dogs")],
        "one_trial.gif",
        f"wide, N = 200, D = 4, seed 0, 99 percent rule, 6 drive times ({RUN})",
    )


def sheep_reaction() -> None:
    """Wide start, first 120 s: reacting front spreads through a grazing flock."""
    animate(
        [Shot("wide", 200, 4, 0, "sheep react within r_s", until=120)],
        "sheep_reaction.gif",
        (
            f"wide, N = 200, D = 4, seed 0, first 120 s ({RUN}); "
            "filled: within r_s of a dog, hollow: grazing"
        ),
        overlay=reacting,
    )


def push_blending() -> None:
    """Compact N=100: 1 vs 8 dogs; normalised push keeps the same walk speed."""
    animate(
        [Shot("compact", 100, 1, 0, "1 dog"), Shot("compact", 100, 8, 0, "8 dogs")],
        "push_blending.gif",
        f"compact, N = 100, seed 0, 99 percent rule, 6 drive times ({RUN})",
    )


def team_rule_at_work() -> None:
    """Outlier-rich N=200, D=4: targets, f(N), and collect-to-drive."""
    animate(
        [Shot("outlier_rich", 200, 4, 0, "the team rule, 4 dogs")],
        "team_rule.gif",
        f"outlier_rich, N = 200, D = 4, seed 0 ({RUN}); crosses: each dog's target, dashed: f(N)",
        overlay=team_rule,
    )


def start_layouts() -> None:
    """Same team on compact, wide, split, and outlier_rich starts."""
    shots = [
        Shot(layout, 200, 4, 0, layout) for layout in ("compact", "wide", "split", "outlier_rich")
    ]
    animate(shots, "layouts.gif", f"N = 200, D = 4, seed 0, 99 percent rule, 6 drive times ({RUN})")


GIFS = {
    g.__name__: g
    for g in (one_trial, sheep_reaction, push_blending, team_rule_at_work, start_layouts)
}


def main() -> None:
    for name in sys.argv[1:] or list(GIFS):
        GIFS[name]()


if __name__ == "__main__":
    main()
