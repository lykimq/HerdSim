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
from functools import cache
from pathlib import Path
from typing import Any

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle, Rectangle
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
    style_map,
)
from docs.generate_docs.runs import F99_RUNS, FAT_RUNS  # noqa: E402
from paper_check.settings import DONE_DISTANCE, FIELD_SIDE  # noqa: E402
from paper_check.sweep import fig3_replay_job  # noqa: E402
from paper_check.trials import seed_of  # noqa: E402
from services.replay import ReplayJob, StoredRun, open_run, replay_trial  # noqa: E402
from sim.state import SimulationState  # noqa: E402
from sim.strombom.params import FAT, INDEPENDENT, METHOD  # noqa: E402
from sim.strombom.shepherd import COLLECT, collect_threshold, decide  # noqa: E402
from sim.strombom.team import team_targets  # noqa: E402
from sim.trial import RunResult, initial_state  # noqa: E402

# ----- settings -----
FPS = 12
FRAMES = 200  # about 17 s of animation, whatever the trial's length
HOLD_SECONDS = 2.0  # the last frame stays on screen this long before the loop restarts
DPI = 100  # readable text; every GIF stays under 1.5 MB, within the 2 MB page budget
MARGIN = 12.0  # length units around everything that moves, so no agent touches the frame
NOTE_CHARS = 72  # note characters per panel width before it wraps
NOTE_LINE = 0.16  # inches per extra note line
PANEL_WIDTH = 4.6  # inches per panel; the height follows the view, so no space is wasted
# Every GIF replays the 99 percent run at 6 drive times.
RUN = F99_RUNS[6]

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
    run: str = RUN
    method: str = METHOD


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
    paper: bool = False  # the paper's task: time steps, and the flock centre ends the trial

    @property
    def ending(self) -> str:
        if self.paper:
            return "finished" if self.success else "not finished, time is up"
        return "succeeded" if self.success else "failed, time is up"

    def at(self, tick: int) -> int:
        """Index of the last kept frame at or before ``tick``."""
        return max(0, int(np.searchsorted(self.ticks, tick, side="right")) - 1)

    def outside(self, i: int) -> int:
        d = np.linalg.norm(self.herd[i] - self.goal, axis=1)
        return int((d > self.goal_radius).sum())


@cache
def _run(name: str = RUN) -> StoredRun:
    """A stored run the animations replay, opened once."""
    return open_run(name)


def shown_ticks(shot: Shot) -> int:
    """Stored trial length, or ``until`` if shorter."""
    stored = _run(shot.run).job(shot.method, shot.layout, shot.n, shot.d, shot.seed_index).stored[1]
    return stored if shot.until is None else min(stored, shot.until)


def _record(
    job: ReplayJob, every: int = 1, end: float = math.inf
) -> tuple[tuple[np.ndarray, np.ndarray, np.ndarray], RunResult]:
    """Replay ``job`` (checked against its stored outcome) and keep (ticks, sheep, dogs) at
    tick 0, every ``every``-th tick up to ``end``, and the last tick up to ``end``."""
    # on_tick sees only the state after each tick, so the start is taken from the seed.
    start = initial_state(job.config, job.seed)
    kept = [(0, start.sheep_positions.copy(), start.shepherd_positions.copy())]
    last = kept[:]

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
    ticks, herd, herders = zip(*kept, strict=True)
    return (np.array(ticks), np.array(herd), np.array(herders)), result


def replay(shot: Shot, every: int) -> Replayed:
    """Replay one stored trial, keeping every ``every``-th tick.

    The full trial is always replayed (and checked against the stored outcome) even when
    ``until`` cuts what is shown.
    """
    job = _run(shot.run).job(shot.method, shot.layout, shot.n, shot.d, shot.seed_index)
    end = shot.until if shot.until is not None else math.inf
    (ticks, herd, herders), result = _record(job, every, end)
    return Replayed(
        ticks=ticks,
        herd=herd,
        herders=herders,
        goal=np.asarray(job.config["goal_center"], dtype=float),
        goal_radius=float(job.config["goal_radius"]),
        dt=float(job.config["dt"]),
        success=bool(result.success),
        config=job.config,
        cut=shot.until is not None and shot.until < int(result.total_ticks),
    )


def shared_view(trials: list[Replayed]) -> View:
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
    style_map(ax, title)
    ax.set_xlim(*view[0])
    ax.set_ylim(*view[1])
    centre = (float(trial.goal[0]), float(trial.goal[1]))
    ax.add_patch(Circle(centre, trial.goal_radius, fc="none", ec=AQUA, lw=1.5))
    herd = ax.scatter(*trial.herd[0].T, s=dot, color=BLUE, alpha=0.85, lw=0)
    herders = ax.scatter(
        *trial.herders[0].T, s=60, marker="^", color=ORANGE, ec=SURFACE, lw=0.8, zorder=3
    )
    # A light backing keeps the status readable when a dog walks under it.
    status = ax.text(
        0.02,
        0.03,
        "",
        transform=ax.transAxes,
        fontsize=9,
        color=INK,
        zorder=4,
        bbox={"fc": SURFACE, "ec": "none", "alpha": 0.8, "pad": 1.5},
    )
    return Panel(trial, herd, herders, status)


def update_panel(panel: Panel, tick: int) -> None:
    """Show the panel at ``tick`` (or the last frame after the trial ends)."""
    trial = panel.trial
    i = trial.at(tick)
    panel.herd.set_offsets(trial.herd[i])
    panel.herders.set_offsets(trial.herders[i])
    last = i == len(trial.ticks) - 1 and not trial.cut
    if trial.paper:
        gcm = float(np.linalg.norm(trial.herd[i].mean(axis=0) - trial.goal))
        text = f"step {trial.ticks[i]}, flock centre {gcm:.0f} m from the goal"
        text += f": {trial.ending}" if last else ""
    else:
        seconds = trial.ticks[i] * trial.dt
        outside = trial.outside(i)
        if last:
            text = f"t = {seconds:.0f} s, {outside} outside: {trial.ending}"
        else:
            text = f"t = {seconds:.0f} s, {outside} sheep outside the goal"
    panel.status.set_text(text)
    panel.status.set_color(ORANGE if last and not trial.success else INK)


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
    render(trials, [s.title for s in shots], (longest, every), file, note, dot, overlay)


def render(
    trials: list[Replayed],
    titles: list[str],
    clock: tuple[int, int],
    file: str,
    note: str,
    dot: float,
    overlay: Overlay | None,
) -> None:
    """Draw ``trials`` side by side on one clock, ``clock`` = (last tick, ticks per frame), and
    save a GIF."""
    longest, every = clock
    view = shared_view(trials)
    aspect = (view[1][1] - view[1][0]) / (view[0][1] - view[0][0])
    lines = textwrap.wrap(note, NOTE_CHARS * len(trials), break_on_hyphens=False)
    extra_height = NOTE_LINE * (len(lines) - 1)
    size = (PANEL_WIDTH * len(trials), PANEL_WIDTH * aspect + 0.9 + extra_height)
    fig, axes = plt.subplots(1, len(trials), figsize=size)
    panels = [
        draw_panel(ax, t, title, view, dot)
        for ax, t, title in zip(np.atleast_1d(axes), trials, titles, strict=True)
    ]
    extras = (
        [(p, overlay(ax, p)) for ax, p in zip(np.atleast_1d(axes), panels, strict=True)]
        if overlay
        else []
    )
    fig.text(0.5, 0.02, "\n".join(lines), ha="center", fontsize=8.5, color=MUTED)
    fig.tight_layout(rect=(0, (0.35 + extra_height) / size[1], 1, 1))
    ticks = list(range(0, longest, every)) + [longest] * (1 + round(HOLD_SECONDS * FPS))

    def draw(k: int) -> list[Any]:
        for panel in panels:
            update_panel(panel, ticks[k])
        for panel, update in extras:
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
        lines.set_segments([[tuple(a), tuple(b)] for a, b in zip(dogs, targets, strict=True)])
        crosses.set_offsets(targets)
        label.set_text("collecting" if mode == COLLECT else "driving")

    return update


def paper_field(ax: Axes, _: Panel) -> Callable[[int], None]:
    """The paper's field and its two start quarters, behind the agents."""
    half = FIELD_SIDE / 2
    ax.add_patch(Rectangle((0, 0), FIELD_SIDE, FIELD_SIDE, fc="none", ec=MUTED, lw=0.8))
    ax.add_patch(Rectangle((half, half), half, half, fc=BLUE, ec="none", alpha=0.08, zorder=0))
    ax.add_patch(Rectangle((0, 0), half, half, fc=ORANGE, ec="none", alpha=0.08, zorder=0))
    return lambda _: None


def paper_replay(n_sheep: int, n_neighbors: int, seed: int) -> Replayed:
    """Replay one stored trial of the paper's task, checked against its stored outcome, and
    keep every tick for the animation."""
    job = fig3_replay_job(n_sheep, n_neighbors, seed)
    (ticks, herd, herders), result = _record(job)
    return Replayed(
        ticks=ticks,
        herd=herd,
        herders=herders,
        goal=np.zeros(2),
        goal_radius=DONE_DISTANCE,
        dt=1.0,
        success=bool(result.success),
        config=job.config,
        cut=False,
        paper=True,
    )


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


def controllers() -> None:
    """Same start flock: team rule vs independent shepherds vs uncoordinated FAT."""
    shots = [
        Shot("wide", 400, 4, 0, "the team rule (strombom_multi)"),
        Shot(
            "wide",
            400,
            4,
            0,
            "independent shepherds (independent)",
            run="dmin_f99_indep",
            method=INDEPENDENT,
        ),
        Shot("wide", 400, 4, 0, "FAT baseline (fat)", run=FAT_RUNS[1], method=FAT),
    ]
    animate(
        shots, "controllers.gif", "wide, N = 400, D = 4, seed 0, 99 percent rule, 6 drive times"
    )


def paper_task() -> None:
    """One trial of the paper's task: N = 100, the global case."""
    n_sheep = 100
    trial = paper_replay(n_sheep, n_sheep - 1, seed_of(n_sheep, 0))
    every = max(1, math.ceil(int(trial.ticks[-1]) / FRAMES))
    keep = np.flatnonzero((trial.ticks % every == 0) | (trial.ticks == trial.ticks[-1]))
    trial.ticks, trial.herd, trial.herders = (
        trial.ticks[keep],
        trial.herd[keep],
        trial.herders[keep],
    )
    render(
        [trial],
        ["HerdSim on the paper's task"],
        (int(trial.ticks[-1]), every),
        "paper_task.gif",
        (
            f"N = {n_sheep}, n = {n_sheep - 1}, seed {seed_of(n_sheep, 0)}; "
            "blue: sheep, orange: the dog, green: the 10 m goal circle at the origin"
        ),
        dot=9,
        overlay=paper_field,
    )


GIFS = {
    g.__name__: g
    for g in (
        one_trial,
        sheep_reaction,
        push_blending,
        team_rule_at_work,
        start_layouts,
        controllers,
        paper_task,
    )
}


def main() -> None:
    names = sys.argv[1:] or list(GIFS)
    unknown = [name for name in names if name not in GIFS]
    if unknown:
        sys.exit(f"unknown animations {unknown}; choose from {list(GIFS)}")
    for name in names:
        GIFS[name]()


if __name__ == "__main__":
    main()
