"""Animated GIFs of stored trials, for the dynamics a still figure cannot show.

    uv run python docs/generate_docs/make_gifs.py              # every GIF
    uv run python docs/generate_docs/make_gifs.py last_sheep   # one, by name

Every animation replays trials that a study protocol stored (services/replay.py), and each
replay is checked against its stored outcome, so what moves on screen is the trial behind
the reported numbers. The GIFs are written to docs/gifs.

The file has three parts:

- settings: the frame rate, the number of frames, the size of a panel
- helpers: a ``Shot`` names one stored trial, ``replay`` records it at the ticks a frame
  shows, ``animate`` draws shots side by side on one view and writes the GIF
- overlays: what a GIF draws on top of the agents (which sheep react, each dog's target,
  each herder's sensing range), computed with the model's own functions
- one function per GIF, which lists its shots, its overlay and the note under the panels

Colours and matplotlib defaults come from figstyle.py, so the animations look
like the still figures. Agents being herded are dots and herders are triangles, so the two
differ by shape as well as colour. Captions are in the documents that show the GIFs.
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
from sim.plugins.dogs.collect_drive_multi import known_sheep, team_targets  # noqa: E402

# ------------------------------------------------------------------------------------ settings

FPS = 12
FRAMES = 200  # about 17 s of animation, whatever the trial's length
HOLD_SECONDS = 2.0  # the last frame stays on screen this long before the loop restarts
DPI = 80
MARGIN = 12.0  # length units around everything that moves, so no agent touches the frame
NOTE_CHARS = 72  # note characters per panel width before it wraps
NOTE_LINE = 0.16  # inches per extra note line
PANEL_WIDTH = 4.6  # inches per panel; the height follows the view, so no space is wasted

View = tuple[tuple[float, float], tuple[float, float]]  # x limits and y limits of a panel

# ------------------------------------------------------------------------------------- helpers


@dataclass(frozen=True)
class Shot:
    """One stored trial to show, and the title of its panel."""

    run: str
    method: str
    layout: str
    n: int
    d: int
    seed_index: int
    title: str
    factors: tuple[tuple[str, Any], ...] = ()
    until: int | None = None  # show only the first ticks, for the start of a trial


@dataclass
class Replayed:
    """A replayed trial, kept at the ticks the frames show."""

    ticks: np.ndarray  # tick number of each kept frame, ascending
    herd: np.ndarray  # (frames, N, 2) positions of the sheep or targets
    herders: np.ndarray  # (frames, D, 2)
    goal: np.ndarray
    goal_radius: float
    dt: float
    success: bool
    timed_out: bool  # False when the task ended the trial itself (gather: herders home)
    config: dict[str, Any]
    extra: list[Any]  # what ``capture`` read from the state at each kept frame
    cut: bool  # shown only up to Shot.until, so the last frame is not the trial's end

    @property
    def ending(self) -> str:
        if self.success:
            return "succeeded"
        return "failed, time is up" if self.timed_out else "failed, the task ended"

    def at(self, tick: int) -> int:
        """Index of the last kept frame at or before ``tick``."""
        return max(0, int(np.searchsorted(self.ticks, tick, side="right")) - 1)

    def outside(self, i: int) -> int:
        d = np.linalg.norm(self.herd[i] - self.goal, axis=1)
        return int((d > self.goal_radius).sum())


Capture = Callable[[Any], Any]


def shown_ticks(shot: Shot) -> int:
    """The ticks the GIF shows: the stored trial's length, read from its row before anything
    is replayed, or ``until`` when that is shorter."""
    run = open_run(shot.run)
    outcome = run.outcomes(shot.method, shot.layout, shot.n, shot.d, shot.factors)
    stored = outcome[shot.seed_index][1]
    return stored if shot.until is None else min(stored, shot.until)


def replay(shot: Shot, every: int, capture: Capture | None) -> Replayed:
    """Replay one stored trial, keeping every ``every``-th tick up to the last tick shown, so a
    long trial (the gather task runs about 15,000 ticks) needs no more memory than a short
    one. The whole trial is replayed even when only its start is shown, so it is still
    checked against the stored outcome; it raises when the two differ."""
    run = open_run(shot.run)
    jobs = run.jobs(shot.method, shot.layout, shot.n, shot.d, shot.seed_index + 1, shot.factors)
    job = next(j for j in jobs if j.label["seed_index"] == shot.seed_index)
    end = shot.until if shot.until is not None else math.inf
    kept: list[tuple[int, np.ndarray, np.ndarray, Any]] = []
    last: list[tuple[int, np.ndarray, np.ndarray, Any]] = []

    def keep(state: SimulationState) -> None:
        if state.tick > end:
            return
        extra = capture(state) if capture is not None else None
        snapshot = (
            state.tick,
            state.sheep_positions.copy(),
            state.shepherd_positions.copy(),
            extra,
        )
        if state.tick % every == 0:
            kept.append(snapshot)
        last[:] = [snapshot]

    result = replay_trial(job, on_tick=keep)
    if kept[-1][0] != last[0][0]:
        kept.append(last[0])
    ticks, herd, herders, extra = zip(*kept)
    return Replayed(
        np.array(ticks),
        np.array(herd),
        np.array(herders),
        np.asarray(job.config["goal_center"], dtype=float),
        float(job.config["goal_radius"]),
        float(job.config["dt"]),
        bool(result.success),
        int(result.total_ticks) >= int(job.config["max_ticks"]),
        job.config,
        list(extra),
        shot.until is not None and shot.until < int(result.total_ticks),
    )


def window(trials: list[Replayed]) -> View:
    """One view for every panel: everything that moves in any trial, and the goals."""
    points = np.vstack(
        [np.vstack([t.herd.reshape(-1, 2), t.herders.reshape(-1, 2)]) for t in trials]
    )
    goals = np.array([t.goal for t in trials])
    radius = max(t.goal_radius for t in trials)
    lo = np.minimum(points.min(axis=0), goals.min(axis=0) - radius)
    hi = np.maximum(points.max(axis=0), goals.max(axis=0) + radius)
    margin = max(MARGIN, 0.04 * float((hi - lo).max()))  # a few percent on wide views
    return (float(lo[0] - margin), float(hi[0] + margin)), (
        float(lo[1] - margin),
        float(hi[1] + margin),
    )


@dataclass
class Panel:
    """The artists of one trial's panel, updated frame by frame."""

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


def update_panel(panel: Panel, tick: int, noun: str) -> None:
    """Show the panel at ``tick``, or at the trial's end once it has ended."""
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
        panel.status.set_text(f"t = {seconds:.0f} s, {outside} {noun} outside the goal")
        panel.status.set_color(INK)


Overlay = Callable[[Any, Panel], Callable[[int], None]]


def animate(
    shots: list[Shot],
    file: str,
    note: str,
    noun: str = "sheep",
    dot: float = 9,
    capture: Capture | None = None,
    overlay: Overlay | None = None,
    frames: int = FRAMES,
) -> None:
    """Replay ``shots`` and draw them side by side on one view, as a looping GIF.

    All panels share one clock: each frame is the same tick in every panel, and a trial that
    has ended stays on its last state, so the panels can be compared moment by moment.
    ``capture`` reads extra values from the state at each kept tick; ``overlay`` sets up
    artists on a panel and returns the function that updates them for a kept frame."""
    longest = max(shown_ticks(s) for s in shots)
    every = max(1, math.ceil(longest / frames))
    trials = [replay(s, every, capture) for s in shots]
    view = window(trials)
    aspect = (view[1][1] - view[1][0]) / (view[0][1] - view[0][0])
    lines = textwrap.wrap(note, NOTE_CHARS * len(shots), break_on_hyphens=False)
    extra_height = NOTE_LINE * (len(lines) - 1)
    size = (PANEL_WIDTH * len(shots), PANEL_WIDTH * aspect + 0.9 + extra_height)  # titles, note
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
            update_panel(panel, ticks[k], noun)
        for panel, update in zip(panels, extras):
            update(panel.trial.at(ticks[k]))
        return []

    animation = FuncAnimation(fig, draw, frames=len(ticks))
    animation.save(GIF_OUT / file, writer=PillowWriter(fps=FPS), dpi=DPI)
    plt.close(fig)
    print(file, f"{(GIF_OUT / file).stat().st_size / 1e6:.1f} MB")


# ------------------------------------------------------------------------------------ overlays


def corner_text(ax: Axes) -> Any:
    """A second status line, top right, for what an overlay counts; the time and outcome
    line takes the bottom left."""
    return ax.text(
        0.98, 0.97, "", transform=ax.transAxes, ha="right", va="top", fontsize=9, color=INK
    )


def fill_herd(panel: Panel, filled: np.ndarray) -> None:
    """Sheep drawn filled where ``filled`` holds and hollow elsewhere, so two groups differ by
    fill and not by colour alone."""
    panel.herd.set_linewidths(0.8)
    panel.herd.set_facecolors([BLUE if f else SURFACE for f in filled])
    panel.herd.set_edgecolors([BLUE] * len(filled))


def dashed_rings(ax: Axes, count: int, radius: float) -> list[Circle]:
    """One dashed circle per agent, for a sensing range; ``move_rings`` places them."""
    rings = [Circle((0.0, 0.0), radius, fc="none", ec=MUTED, lw=0.5, ls="--") for _ in range(count)]
    for ring in rings:
        ax.add_patch(ring)
    return rings


def move_rings(rings: list[Circle], centres: np.ndarray) -> None:
    for ring, centre in zip(rings, centres):
        ring.set_center(tuple(centre))


def reacting(ax: Axes, panel: Panel) -> Callable[[int], None]:
    """Sheep within r_s of a dog react (filled); the others graze (hollow)."""
    trial = panel.trial
    r_s = float(trial.config["r_s"])
    label = corner_text(ax)

    def update(i: int) -> None:
        near = cdist(trial.herd[i], trial.herders[i]).min(axis=1) < r_s
        fill_herd(panel, near)
        label.set_text(f"{int(near.sum())} reacting, {int((~near).sum())} grazing")

    return update


def sight(ax: Axes, panel: Panel) -> Callable[[int], None]:
    """Each dog's sensing range (dashed) and the sheep no dog sees (hollow), from the
    controller's own ``known_sheep``. The team plans only on the sheep it sees; how it shares
    them (none or shared) is what differs between panels."""
    trial = panel.trial
    rings = dashed_rings(ax, len(trial.herders[0]), float(trial.config["sensing_range"]))
    label = corner_text(ax)

    def update(i: int) -> None:
        move_rings(rings, trial.herders[i])
        seen = known_sheep(trial.herd[i], trial.herders[i], trial.config).any(axis=0)
        fill_herd(panel, seen)
        label.set_text(f"{int((~seen).sum())} seen by no dog")

    return update


def team_rule(ax: Axes, panel: Panel) -> Callable[[int], None]:
    """What the team rule decides at each frame, from the positions shown: the mode, the
    collect distance f(N) round the flock centre, and each dog's target (cross) with a line
    from the dog to it. Computed with the controller's own ``team_targets``."""
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


def herder_view(ax: Axes, panel: Panel) -> Callable[[int], None]:
    """Each herder's sensing circle and a ring round the target it chases (none when it
    senses nothing and walks home), from the choice the model stored in the state. A herder
    stands only 1.25 beyond its target, so a line to it would be too short to see."""
    trial = panel.trial
    rings = dashed_rings(ax, len(trial.herders[0]), float(trial.config["sensing_radius"]))
    chased = ax.scatter([], [], s=70, fc="none", ec=ORANGE, lw=1.3, zorder=4)
    label = corner_text(ax)

    def update(i: int) -> None:
        herders, chosen = trial.herders[i], trial.extra[i]
        move_rings(rings, herders)
        chasing = chosen[chosen >= 0]
        chased.set_offsets(trial.herd[i][chasing].reshape(-1, 2))
        label.set_text(f"{len(chasing)} chasing, {len(herders) - len(chasing)} heading home")

    return update


def chosen_targets(state: SimulationState) -> np.ndarray:
    """The target index each Lama herder chases this tick (-1 for none)."""
    return np.asarray(state.metadata.get("herder_target", []), dtype=int).copy()


# ---------------------------------------------------------------------------------------- GIFs


def last_sheep() -> None:
    """The same start flock of 400 on `wide`, 16 dogs, strict rule: fast dogs bring the flock
    in with a sheep or two missing and drive it out again; slower dogs finish in one pass."""
    cell = ("strombom_multi", "wide", 400, 16, 2)
    animate(
        [
            Shot("dmin_s_base", *cell, "dogs at 1.5 m/s"),
            Shot("dmin_s_dogspeed", *cell, "dogs at 1.15 m/s"),
        ],
        "last_sheep.gif",
        "wide, N = 400, D = 16, seed 2, strict rule, 6 drive times (dmin_s_base, dmin_s_dogspeed)",
    )


def controllers() -> None:
    """Three dog rules on the same start flock of 400 on `wide`, 4 dogs: the team rule
    finishes, the independent dogs move as one, FAT spreads the flock."""
    cell = ("wide", 400, 4, 0)
    animate(
        [
            Shot("dmin_f99_m6", "strombom_multi", *cell, "team rule"),
            Shot("dmin_f99_indep", "independent", *cell, "independent dogs"),
            Shot("dmin_f99_fat", "fat", *cell, "FAT"),
        ],
        "controllers.gif",
        (
            "wide, N = 400, D = 4, seed 0, 99 percent rule, 6 drive times "
            "(dmin_f99_m6, dmin_f99_indep, dmin_f99_fat)"
        ),
    )


def one_trial() -> None:
    """One trial from start to goal: the dogs collect the outliers of a scattered start, then
    drive the gathered flock."""
    animate(
        [Shot("dmin_f99_m6", "strombom_multi", "wide", 200, 4, 0, "the team rule, 4 dogs")],
        "one_trial.gif",
        "wide, N = 200, D = 4, seed 0, 99 percent rule, 6 drive times (dmin_f99_m6)",
    )


def split_layout() -> None:
    """Two seeds of one `split` cell with 16 dogs: one brings the clusters together quickly, the
    other runs out of time with the flock short of the goal."""
    cell = ("strombom_multi", "split", 200, 16)
    animate(
        [Shot("dmin_f99_m6", *cell, 4, "seed 4"), Shot("dmin_f99_m6", *cell, 8, "seed 8")],
        "split.gif",
        "split, N = 200, D = 16, 99 percent rule, 6 drive times (dmin_f99_m6)",
    )


def holding() -> None:
    """Holding a flock of 25 with one dog, from the same start: the flock keeps walking while
    the dog withdraws, out of a goal of 1.9 R_f but not out of one of 3.0 R_f."""
    cell = ("strombom_multi", "compact", 25, 1, 0)
    three = (("goal_radius_multiple", 3.0),)
    animate(
        [
            Shot("dmin_f99_hold", *cell, "goal 1.9 R_f (11.8 m)"),
            Shot("dmin_f99_hold_goal", *cell, "goal 3.0 R_f (18.6 m)", three),
        ],
        "holding.gif",
        (
            "compact, N = 25, D = 1, seed 0, 99 percent held for one drive time, 6 drive times "
            "(dmin_f99_hold, dmin_f99_hold_goal)"
        ),
    )


def gather() -> None:
    """The Lama and di Bernardo model at 144 targets and 11 herders that sense within 10:
    one run gathers all but one target; in the other the herders go home with two targets
    out of sight, and the run fails the 99 percent rule."""
    cell = ("lama", "uniform", 144, 11)
    animate(
        [Shot("lama_r50", *cell, 0, "seed 0"), Shot("lama_r50", *cell, 1, "seed 1")],
        "gather.gif",
        "gather task, 144 targets, 11 herders, sensing radius 10, 99 percent rule (lama_r50)",
        noun="targets",
        dot=12,
    )


def sheep_reaction() -> None:
    """The first two minutes of a trial on `wide`: sheep react only once a dog is within r_s,
    so a front of reacting sheep spreads from the dogs through a grazing flock."""
    animate(
        [
            Shot(
                "dmin_f99_m6",
                "strombom_multi",
                "wide",
                200,
                4,
                0,
                "sheep react within r_s",
                until=120,
            )
        ],
        "sheep_reaction.gif",
        (
            "wide, N = 200, D = 4, seed 0, first 120 s (dmin_f99_m6); "
            "filled: within r_s of a dog, hollow: grazing"
        ),
        overlay=reacting,
    )


def push_blending() -> None:
    """One dog against eight on the same compact flock: the push of several dogs is
    normalised to that of one, so the flock walks at the same speed and arrives together."""
    cell = ("strombom_multi", "compact", 100)
    animate(
        [Shot("dmin_f99_m6", *cell, 1, 0, "1 dog"), Shot("dmin_f99_m6", *cell, 8, 0, "8 dogs")],
        "push_blending.gif",
        "compact, N = 100, seed 0, 99 percent rule, 6 drive times (dmin_f99_m6)",
    )


def kubo_ring() -> None:
    """The Kubo model with 4 dogs: their mutual repulsion spreads them round the flock while
    each chases the sheep farthest from the goal."""
    animate(
        [Shot("dmin_kubo", "kubo", "compact", 50, 4, 0, "Kubo sheep and dogs, 4 dogs")],
        "kubo_ring.gif",
        "compact, N = 50, D = 4, seed 0, strict rule, 500 s (dmin_kubo)",
        dot=12,
    )


def kubo_speed() -> None:
    """One Kubo dog against ten on the same flock: a Kubo sheep speeds up under a stronger
    push, so more dogs finish sooner, where Strömbom's sheep keep 1 m/s."""
    cell = ("kubo", "compact", 100)
    animate(
        [Shot("dmin_kubo", *cell, 1, 0, "1 dog"), Shot("dmin_kubo", *cell, 10, 0, "10 dogs")],
        "kubo_speed.gif",
        "Kubo, compact, N = 100, seed 0, strict rule, 500 s (dmin_kubo)",
    )


def drive_cap() -> None:
    """One dog driving 1131 sheep, from the paper's drive point and from the capped one: at
    r_a sqrt(N) = 67 m behind the centre the dog reaches only the rear of the flock."""
    cell = ("strombom_multi", "compact", 1131, 1, 0)
    animate(
        [
            Shot("dmin_f99_big", *cell, "drive point r_a sqrt(N) = 67 m"),
            Shot("dmin_f99_big_cap", *cell, "drive point capped at 63 m"),
        ],
        "drive_cap.gif",
        (
            "compact, N = 1131, D = 1, seed 0, 99 percent rule, 12 drive times "
            "(dmin_f99_big, dmin_f99_big_cap); filled: within r_s of the dog, hollow: grazing"
        ),
        dot=3,
        overlay=reacting,
    )


def flock_pressure() -> None:
    """3 dogs against 12 on the same `wide` flock of 400: more dogs spread over a wider arc, so
    more of the flock flees at once, but the drive ends sooner."""
    cell = ("strombom_multi", "wide", 400)
    animate(
        [Shot("dmin_f99_m6", *cell, 3, 0, "3 dogs"), Shot("dmin_f99_m6", *cell, 12, 0, "12 dogs")],
        "flock_pressure.gif",
        (
            "wide, N = 400, seed 0, 99 percent rule, 6 drive times (dmin_f99_m6); "
            "filled: within r_s of a dog, hollow: grazing"
        ),
        dot=6,
        overlay=reacting,
    )


def sight_sharing() -> None:
    """Two dogs that see 65 m, without and with sharing: without it each dog plans on its own
    view; shared, the team plans once on everything any dog sees."""
    cell = ("strombom_multi", "wide", 200, 2, 0)
    animate(
        [
            Shot(
                "dmin_f99_view_range", *cell, "range 65 m, no sharing", (("sensing_range", 65.0),)
            ),
            Shot("dmin_f99_view_comm", *cell, "range 65 m, shared", (("communication", "shared"),)),
        ],
        "sight_sharing.gif",
        (
            "wide, N = 200, D = 2, seed 0, 99 percent rule, 6 drive times "
            "(dmin_f99_view_range, dmin_f99_view_comm); dashed: sensing range, hollow: seen by no "
            "dog"
        ),
        overlay=sight,
        frames=130,  # two 200-sheep panels whose fill changes every frame; 200 frames pass 2 MB
    )


def team_rule_at_work() -> None:
    """The team rule on an outlier-rich start: each dog's target as the rule computes it, the
    collect distance f(N), and the switch from collecting to driving."""
    animate(
        [Shot("dmin_f99_m6", "strombom_multi", "outlier_rich", 200, 4, 0, "the team rule, 4 dogs")],
        "team_rule.gif",
        (
            "outlier_rich, N = 200, D = 4, seed 0 (dmin_f99_m6); "
            "crosses: each dog's target, dashed: f(N)"
        ),
        overlay=team_rule,
    )


def lama_herders() -> None:
    """The Lama herders at 144 targets: each senses within 10, chases the farthest target it
    senses that no closer herder takes, and walks home when it senses none."""
    animate(
        [Shot("lama_r50", "lama", "uniform", 144, 11, 0, "11 herders, sensing radius 10")],
        "lama_herders.gif",
        (
            "gather task, 144 targets, seed 0 (lama_r50); "
            "dashed: sensing range, orange rings: the targets being chased"
        ),
        noun="targets",
        dot=12,
        capture=chosen_targets,
        overlay=herder_view,
        frames=140,  # 11 sensing rings move every frame; 200 frames pass 2 MB
    )


def start_layouts() -> None:
    """The same team on the four start layouts: compact is driven at once, the scattered
    layouts are collected first, and split takes longest because its clusters lie apart."""
    shots = [
        Shot("dmin_f99_m6", "strombom_multi", layout, 200, 4, 0, layout)
        for layout in ("compact", "wide", "split", "outlier_rich")
    ]
    animate(
        shots, "layouts.gif", "N = 200, D = 4, seed 0, 99 percent rule, 6 drive times (dmin_f99_m6)"
    )


def dog_starts() -> None:
    """Eight dogs released from arcs, a ring and a handler's post onto the same flock: the
    team rule sorts them onto their targets within the first minutes whatever the start."""
    cell = ("strombom_multi", "wide", 200, 8, 0)
    animate(
        [
            Shot("dmin_s_base", *cell, "arcs (default)"),
            Shot("dmin_s_ring", *cell, "ring"),
            Shot("dmin_s_handler", *cell, "handler"),
        ],
        "dog_starts.gif",
        (
            "wide, N = 200, D = 8, seed 0, strict rule, 6 drive times "
            "(dmin_s_base, dmin_s_ring, dmin_s_handler)"
        ),
    )


def crowding() -> None:
    """Twelve point dogs against twelve that keep 2 m apart, holding the same outlier-rich
    flock of 400: the spaced team runs out of time where the point team holds the flock."""
    cell = ("strombom_multi", "outlier_rich", 400, 12, 0)
    animate(
        [
            Shot("dmin_f99_hold", *cell, "point dogs"),
            Shot("dmin_f99_hold_spacing", *cell, "dogs 2 m apart"),
        ],
        "crowding.gif",
        (
            "outlier_rich, N = 400, D = 12, seed 0, 99 percent held for one drive time, "
            "6 drive times (dmin_f99_hold, dmin_f99_hold_spacing)"
        ),
        dot=6,
    )


GIFS = {
    g.__name__: g
    for g in (
        last_sheep,
        controllers,
        one_trial,
        split_layout,
        holding,
        gather,
        sheep_reaction,
        push_blending,
        kubo_ring,
        kubo_speed,
        team_rule_at_work,
        drive_cap,
        flock_pressure,
        sight_sharing,
        lama_herders,
        start_layouts,
        dog_starts,
        crowding,
    )
}


def main() -> None:
    for name in sys.argv[1:] or list(GIFS):
        GIFS[name]()


if __name__ == "__main__":
    main()
