"""Schematics for research_design.md: drawings of the design, not simulation output.

    cd /home/gwen/HerdSim && uv run --with matplotlib python docs/science/figures/make_schematics.py

Positions are drawn by hand to illustrate the text. Where a figure is to scale it says so; the rest are
marked "not to scale".
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle  # noqa: E402

OUT = Path(__file__).resolve().parent
SHEEP, DOG, GOAL, GREY, RED, FENCE = "#3b6fb6", "#d9731f", "#2e8b57", "#8a8a8a", "#c0392b", "#5b4636"
RNG = np.random.default_rng(7)


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=130, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", name)


def dogs(ax, pts, s=90):
    pts = np.atleast_2d(pts)
    ax.scatter(pts[:, 0], pts[:, 1], s=s, marker="^", c=DOG, ec="black", lw=0.6, zorder=5)


def sheep(ax, pts, s=18, c=SHEEP):
    pts = np.atleast_2d(pts)
    ax.scatter(pts[:, 0], pts[:, 1], s=s, c=c, zorder=4)


def blob(centre, sigma, n):
    return np.asarray(centre) + RNG.normal(0, sigma, size=(n, 2))


def arrow(ax, a, b, color="black", lw=1.4, style="->"):
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle=style, color=color, lw=lw))


def clean(ax, title):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=10)


# --- gathering, as in Lama and di Bernardo -------------------------------------------------
def gathering():
    fig, ax = plt.subplots(figsize=(6, 6))
    R = 50.0
    ax.add_patch(Circle((0, 0), R, fill=False, ec=GREY, ls="--"))
    ax.add_patch(Circle((0, 0), R / 5, fc=GOAL, alpha=0.2, ec=GOAL))
    ang = RNG.uniform(0, 2 * np.pi, 120)
    rad = R * np.sqrt(RNG.uniform(0, 1, 120))
    sheep(ax, np.c_[rad * np.cos(ang), rad * np.sin(ang)], s=10)
    ang = RNG.uniform(0, 2 * np.pi, 6)
    rad = R * np.sqrt(RNG.uniform(0.2, 1, 6))
    dogs(ax, np.c_[rad * np.cos(ang), rad * np.sin(ang)], s=70)
    ax.annotate("start area, radius R", (R * 0.71, R * 0.71), (R * 0.55, R * 1.08), fontsize=9,
                arrowprops=dict(arrowstyle="-", color=GREY))
    ax.annotate("goal, radius R/5", (R / 5 * 0.7, -R / 5 * 0.7), (R * 0.35, -R * 0.5), fontsize=9, color=GOAL,
                arrowprops=dict(arrowstyle="-", color=GOAL))
    ax.set_xlim(-R * 1.15, R * 1.15)
    ax.set_ylim(-R * 1.15, R * 1.2)
    clean(ax, "Gathering in the setting of Lama and di Bernardo (to scale, R = 50)")
    save(fig, "sch01_gathering")


# --- gate task -----------------------------------------------------------------------------
def gate():
    fig, ax = plt.subplots(figsize=(9, 5))
    x_f, w = 0.0, 8.0
    ax.plot([x_f, x_f], [-60, -w / 2], c=FENCE, lw=4)
    ax.plot([x_f, x_f], [w / 2, 60], c=FENCE, lw=4)
    ax.text(x_f + 2, 50, "fence", color=FENCE, fontsize=9)
    ax.annotate("", xy=(x_f - 3, w / 2), xytext=(x_f - 3, -w / 2), arrowprops=dict(arrowstyle="<->"))
    ax.annotate("gate, width w", (x_f - 3, w / 2), (x_f - 30, 22), fontsize=9,
                arrowprops=dict(arrowstyle="-", color=GREY))
    flock = blob((-40, 0), 6, 60)
    sheep(ax, flock)
    gcm = flock.mean(axis=0)
    ax.scatter(*gcm, marker="x", c="black", s=40, zorder=6)
    g = np.array([x_f + 30.0, 0.0])
    ax.scatter(*g, marker="P", s=90, c=GOAL, ec="black", zorder=6)
    ax.text(g[0], g[1] + 5, "G", color=GOAL, fontsize=10, ha="center")
    u_d = (gcm - g) / np.linalg.norm(gcm - g)
    u_perp = np.array([-u_d[1], u_d[0]])
    r = 2 * np.sqrt(60)
    drive = gcm + r * u_d
    ax.scatter(*drive, marker="*", s=160, c=DOG, ec="black", zorder=6)
    t = np.radians(np.linspace(-90, 90, 60))
    ring = gcm + r * (np.cos(t)[:, None] * u_d + np.sin(t)[:, None] * u_perp)
    ax.plot(ring[:, 0], ring[:, 1], c=GREY, ls=":", lw=1)
    phis = np.radians([-45.0, 45.0])
    dogs(ax, [gcm + r * (np.cos(p) * u_d + np.sin(p) * u_perp) for p in phis])
    ax.plot([drive[0], g[0]], [drive[1], g[1]], c=GREY, ls=":", lw=1)
    arrow(ax, gcm + [8, 0], gcm + [28, 0], color=GOAL, lw=2)
    ax.axvspan(x_f, 55, color=GOAL, alpha=0.07)
    ax.text(27, -50, "success area:\nbeyond the fence line", color=GOAL, fontsize=9, ha="center")
    ax.annotate("P_d, on the line from G through\nthe flock centre; the two dogs\nstand at +-45 degrees on the ring",
                drive, (-79, -45), fontsize=8, arrowprops=dict(arrowstyle="-", color=GREY))
    ax.set_xlim(-80, 55)
    ax.set_ylim(-60, 60)
    clean(ax, "Passing a gate (not to scale)")
    save(fig, "sch02_gate")


# --- holding task --------------------------------------------------------------------------
def holding():
    fig, ax = plt.subplots(figsize=(6.5, 6))
    A = 30.0
    ax.add_patch(Circle((0, 0), A, fc=GOAL, alpha=0.12, ec=GOAL, lw=1.5))
    inside = blob((0, 0), 9, 50)
    inside = inside[np.linalg.norm(inside, axis=1) < A * 0.9]
    sheep(ax, inside)
    out = np.array([[38.0, 14.0], [-20.0, -36.0]])
    sheep(ax, out, c=RED)
    edge = np.array([[A * np.cos(t), A * np.sin(t)] for t in (2.2, 3.9, 5.5)])
    dogs(ax, edge, s=80)
    chaser = out[0] + np.array([6.0, 4.0])
    dogs(ax, chaser, s=80)
    arrow(ax, out[0], out[0] - out[0] / np.linalg.norm(out[0]) * 10, color=RED)
    ax.annotate("dog chasing a sheep\nthat left the area", chaser, chaser + [2, 14], fontsize=8,
                arrowprops=dict(arrowstyle="-", color=GREY))
    ax.annotate("dogs waiting\nat the edge", edge[1], edge[1] + [-22, -10], fontsize=8,
                arrowprops=dict(arrowstyle="-", color=GREY))
    ax.text(0, A + 3, "holding area", ha="center", color=GOAL, fontsize=9)
    ax.set_xlim(-55, 60)
    ax.set_ylim(-50, 50)
    clean(ax, "Holding: keep the flock inside the area for a set time (not to scale)")
    save(fig, "sch03_holding")


# --- bodies and contact --------------------------------------------------------------------
def bodies():
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    # (a) two discs overlapping, pushed apart
    ax = axes[0]
    r = 0.4
    ax.add_patch(Circle((0, 0), r, fc=SHEEP, alpha=0.5, ec=SHEEP))
    ax.add_patch(Circle((0.55, 0), r, fc=SHEEP, alpha=0.5, ec=SHEEP))
    arrow(ax, (0, 0), (-0.35, 0), lw=1.6)
    arrow(ax, (0.55, 0), (0.9, 0), lw=1.6)
    ax.text(0.27, 0.6, "overlap: pushed apart along\nthe line between the centres", ha="center", fontsize=9)
    ax.set_xlim(-0.9, 1.4)
    ax.set_ylim(-0.9, 1.0)
    clean(ax, "(a) contact")
    # (b) hexagonal packing with numbers
    ax = axes[1]
    r = 0.4
    for i in range(6):
        for j in range(5):
            x = 2 * r * i + (r if j % 2 else 0)
            y = np.sqrt(3) * r * j
            ax.add_patch(Circle((x, y), r, fc=SHEEP, alpha=0.4, ec=SHEEP))
    ax.text(2.2 * r * 3, -1.3, "densest packing: 1 / (2 sqrt(3) r^2) per m^2\n"
            "r = 0.5 m: 1.15 per m^2    r = 0.4 m: 1.80 per m^2\n"
            "real flock of 14 (Jadhav et al. 2024): about 1.35 per m^2", ha="center", va="top", fontsize=8.5)
    ax.set_xlim(-0.8, 5.2)
    ax.set_ylim(-2.6, 3.6)
    clean(ax, "(b) how tightly discs of radius r can pack (to scale, r = 0.4 m)")
    # (c) jam at a gate
    ax = axes[2]
    w = 3.0
    ax.plot([0, 0], [-6, -w / 2], c=FENCE, lw=4)
    ax.plot([0, 0], [w / 2, 6], c=FENCE, lw=4)
    pts = []
    for i in range(1, 6):
        for j in range(-5, 6):
            p = np.array([-0.85 * i, 0.85 * j + (0.42 if i % 2 else 0)])
            if abs(p[1]) < 5.5:
                pts.append(p)
    for p in pts:
        ax.add_patch(Circle(p, 0.4, fc=SHEEP, alpha=0.5, ec=SHEEP))
    dogs(ax, [[-6.5, 1.5], [-6.5, -1.5], [-7.0, 0.0]], s=60)
    ax.text(-3, -6.8, "sheep pressed against the fence\nand into the gap; dogs behind add pressure", ha="center",
            fontsize=9)
    ax.set_xlim(-8, 3)
    ax.set_ylim(-7.5, 6.5)
    clean(ax, "(c) a jam at a gate (not to scale)")
    save(fig, "sch04_bodies")


# --- the five parts of a sheep's heading ---------------------------------------------------
def heading():
    fig, ax = plt.subplots(figsize=(8, 6.5))
    me = np.array([0.0, 0.0])
    neigh = np.array([[1.2, 0.5], [2.6, 1.8], [3.5, -0.6], [2.2, 3.0], [4.2, 1.5], [0.8, -2.6]])
    sheep(ax, me, s=80, c="black")
    sheep(ax, neigh, s=40)
    ax.add_patch(Circle(me, 2.0, fill=False, ec=SHEEP, ls="--"))
    ax.text(1.7, -1.7, "r_a = 2 m", color=SHEEP, fontsize=8, va="top")
    lcm = neigh[:5].mean(axis=0)
    ax.scatter(*lcm, marker="+", c="black", s=60)
    ax.text(lcm[0] + 0.25, lcm[1] - 0.5, "centre of the n nearest", fontsize=8)
    dog = np.array([-5.0, -3.5])
    dogs(ax, dog)
    ax.text(dog[0] - 0.2, dog[1] - 0.8, "dog (within r_s = 65 m)", fontsize=8, ha="center")
    parts = {
        "h H  previous heading": (np.array([0.0, 1.0]), "#7f7f7f"),
        "c C  toward the neighbours": ((lcm - me) / np.linalg.norm(lcm - me), "#2e8b57"),
        "rho_a R_a  away from the close one": (-(neigh[0] - me) / np.linalg.norm(neigh[0] - me), SHEEP),
        "rho_s R_s  away from the dog": ((me - dog) / np.linalg.norm(me - dog), DOG),
        "e eps  noise": (np.array([np.cos(4.0), np.sin(4.0)]), "#9467bd"),
    }
    weights = {"h H  previous heading": 0.5, "c C  toward the neighbours": 1.05,
               "rho_a R_a  away from the close one": 2.0, "rho_s R_s  away from the dog": 1.0, "e eps  noise": 0.3}
    total = np.zeros(2)
    for i, (label, (v, col)) in enumerate(parts.items()):
        wv = weights[label] * v
        total += wv
        arrow(ax, me, me + 1.4 * wv, color=col, lw=2)
        ax.text(-7.8, 4.6 - 0.55 * i, f"{label}  (weight {weights[label]})", color=col, fontsize=8.5)
    new = total / np.linalg.norm(total)
    arrow(ax, me, me + 2.8 * new, color="black", lw=2.6)
    ax.text(*(me + 3.0 * new), "new heading H'", fontsize=9, fontweight="bold")
    ax.set_xlim(-8, 6)
    ax.set_ylim(-5, 5.2)
    clean(ax, "The parts of a sheep's new heading (Strombom et al. 2014; not to scale)")
    save(fig, "sch05_heading")


# --- reaction to several dogs --------------------------------------------------------------
def several_dogs():
    fig, axes = plt.subplots(1, 2, figsize=(12, 3.6))
    me = np.array([0.0, 0.0])
    ds = np.array([[-6.0, 1.0], [-5.0, -3.0], [-15.0, 0.0]])
    for ax, mode in zip(axes, ("averaged", "added")):
        sheep(ax, me, s=80, c="black")
        dogs(ax, ds)
        units = [(me - d) / np.linalg.norm(me - d) for d in ds]
        for d, u in zip(ds, units):
            ax.plot([d[0], me[0]], [d[1], me[1]], c=GREY, ls=":", lw=1)
        s = np.sum(units, axis=0)
        if mode == "averaged":
            push = s / np.linalg.norm(s)
            text = "pushes added, then rescaled to the\nlength of one push: three dogs push\nlike one, from the average direction"
        else:
            push = s
            text = "unit pushes added, not rescaled:\nthree dogs from one side push about\nthree times as hard; distance inside\nr_s does not matter"
            for u in units:
                arrow(ax, me, me + 2.5 * u, color=DOG, lw=1)
        arrow(ax, me, me + 2.5 * push, color="black", lw=2.5)
        ax.text(-16, -8.6, text, fontsize=8.5)
        ax.set_xlim(-17, 9)
        ax.set_ylim(-9, 5)
        clean(ax, f"{mode} push (not to scale)")
    fig.suptitle("How a sheep can react to several dogs within r_s (equations S5 and S6)", fontsize=11)
    save(fig, "sch06_several_dogs")


# --- ways of sharing the work --------------------------------------------------------------
def sharing():
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.0))
    core = blob((0, 0), 4, 40)
    strays = np.array([[-30.0, 18.0], [-26.0, -22.0], [6.0, 30.0], [10.0, -28.0]])
    goal = np.array([60.0, 0.0])
    d0 = np.array([[-45.0, 6.0], [-45.0, -6.0], [-45.0, 0.0]])
    gcm = np.vstack([core, strays]).mean(axis=0)
    far_c = strays[np.argmax(np.linalg.norm(strays - gcm, axis=1))]
    by_goal = strays[np.argsort(-np.linalg.norm(strays - goal, axis=1))]
    by_centre = strays[np.argsort(-np.linalg.norm(strays - gcm, axis=1))]
    del by_goal
    d0 = np.array([[-45.0, 28.0], [-45.0, -28.0], [25.0, -36.0]])
    # coordinated: each dog keeps the sheep closer to it than to any other dog, then takes the one
    # farthest from the goal among those (Lama and di Bernardo 2024; Auletta et al. 2021)
    owner = np.argmin(np.linalg.norm(strays[:, None, :] - d0[None, :, :], axis=2), axis=1)
    coordinated = []
    for i in range(3):
        mine = strays[owner == i]
        coordinated.append(mine[np.argmax(np.linalg.norm(mine - goal, axis=1))] if len(mine) else d0[i])
    titles = ("independent: all dogs pick the same sheep",
              "split the stragglers: dog i takes straggler i mod k",
              "coordinated: each dog takes its own sheep")
    targets = ([far_c] * 3, [by_centre[i % 4] for i in range(3)], coordinated)
    for ax, title, tg in zip(axes, titles, targets):
        sheep(ax, core, s=10)
        sheep(ax, strays, s=26, c=RED)
        dogs(ax, d0, s=70)
        for d, t in zip(d0, tg):
            arrow(ax, d, t, color=DOG, lw=1.2)
        ax.add_patch(Circle(goal, 8, fc=GOAL, alpha=0.2, ec=GOAL))
        ax.text(goal[0], goal[1] - 12, "goal", ha="center", color=GOAL, fontsize=8)
        ax.set_xlim(-55, 72)
        ax.set_ylim(-40, 40)
        clean(ax, title)
    fig.suptitle("Three ways for three dogs to share the work while collecting (red: stragglers; not to scale)",
                 fontsize=11)
    save(fig, "sch07_sharing")


# --- one tick ------------------------------------------------------------------------------
def one_tick():
    fig, ax = plt.subplots(figsize=(13, 2.6))
    steps = ["sheep move", "dogs observe,\ndecide, move", "overlapping\nbodies pushed\napart", "fences and walls\nstop crossing",
             "measurements\nrecorded", "stop checks:\nsuccess or\ntime limit"]
    for i, s in enumerate(steps):
        x = i * 2.2
        ax.add_patch(FancyBboxPatch((x, 0), 1.8, 1.2, boxstyle="round,pad=0.05", fc="#eef3fa", ec=SHEEP))
        ax.text(x + 0.9, 0.6, s, ha="center", va="center", fontsize=9)
        if i < len(steps) - 1:
            arrow(ax, (x + 1.85, 0.6), (x + 2.15, 0.6))
    x_last = (len(steps) - 1) * 2.2 + 0.9
    ax.plot([x_last, x_last, 0.9], [-0.06, -0.3, -0.3], c=GREY, lw=1.4)
    arrow(ax, (0.9, -0.3), (0.9, -0.06), color=GREY)
    ax.text(len(steps) * 1.1, -0.48, "next tick", ha="center", color=GREY, fontsize=8)
    ax.set_xlim(-0.3, len(steps) * 2.2)
    ax.set_ylim(-0.65, 1.4)
    ax.axis("off")
    ax.set_title("One tick (the order is a convention; section 9.7)", fontsize=10)
    save(fig, "sch08_one_tick")


# --- where the sheep start -----------------------------------------------------------------
def sheep_starts():
    fig, axes = plt.subplots(1, 5, figsize=(17, 3.5))
    F = 10.0
    lay = {
        "compact": blob((0, 0), 2.2, 40),
        "spread": None,
        "groups": np.vstack([blob(c, 1.6, 14) for c in ((-11, 6), (9, 9), (2, -12))]),
        "stragglers": np.vstack([blob((0, 0), 2.0, 32),
                                 np.array([[15.0, 4.0], [-14.0, 9.0], [-6.0, -15.0], [11.0, -12.0]])]),
        "against a fence": None,
    }
    ang = RNG.uniform(0, 2 * np.pi, 40)
    lay["spread"] = np.c_[np.cos(ang), np.sin(ang)] * (17 * np.sqrt(RNG.uniform(0, 1, 40)))[:, None]
    fence = np.c_[RNG.uniform(7.2, 9.5, 40), RNG.uniform(-11, 11, 40)]
    lay["against a fence"] = fence
    for ax, (name, pts) in zip(axes, lay.items()):
        sheep(ax, pts, s=12)
        gcm = pts.mean(axis=0)
        ax.scatter(*gcm, marker="x", c="black", s=30, zorder=6)
        ax.add_patch(Circle(gcm, F, fill=False, ec=RED, ls="--"))
        if name == "against a fence":
            ax.plot([10, 10], [-19, 19], c=FENCE, lw=4)
        ax.set_xlim(-20, 20)
        ax.set_ylim(-20, 20)
        clean(ax, name)
    axes[0].annotate("f(N) around the\nflock centre", (F * 0.7, F * 0.7), (6, 15), fontsize=8, color=RED,
                     arrowprops=dict(arrowstyle="-", color=RED))
    fig.suptitle("Where the sheep start (not to scale; red dashed circle: collect distance f(N))", fontsize=11)
    save(fig, "sch09_sheep_starts")


# --- where the dogs start ------------------------------------------------------------------
def dog_starts():
    fig, axes = plt.subplots(1, 2, figsize=(12, 3.7))
    flock = blob((0, 0), 4, 40)
    goal = np.array([60.0, 0.0])
    far = np.max(np.linalg.norm(flock, axis=1))
    for ax, name in zip(axes, ("behind the flock", "at a handler point")):
        sheep(ax, flock, s=10)
        ax.add_patch(Circle(goal, 8, fc=GOAL, alpha=0.2, ec=GOAL))
        ax.text(goal[0], goal[1] - 12, "goal", ha="center", color=GOAL, fontsize=8)
        if name == "behind the flock":
            r = far + 8
            t = np.pi + np.array([-0.45, -0.15, 0.15, 0.45])
            dogs(ax, np.c_[r * np.cos(t), r * np.sin(t)], s=60)
            ax.add_patch(Circle((0, 0), far, fill=False, ec=GREY, ls=":"))
            ax.annotate("dogs on an arc behind the farthest\nsheep, away from the goal, a gap apart",
                        (r * np.cos(t[-1]), r * np.sin(t[-1])), (-48, -30), fontsize=8,
                        arrowprops=dict(arrowstyle="-", color=GREY))
        else:
            h = np.array([10.0, -34.0])
            dogs(ax, h + np.array([[-1.5, 0], [1.5, 0], [0, 1.6], [0, -1.6]]), s=40)
            ax.annotate("all dogs at one point; each runs out\nto the flock first (the outrun)", h, (-48, -30),
                        fontsize=8, arrowprops=dict(arrowstyle="-", color=GREY))
        ax.set_xlim(-50, 72)
        ax.set_ylim(-40, 30)
        clean(ax, name)
    fig.suptitle("Where the dogs start in the core (not to scale)", fontsize=11)
    save(fig, "sch10_dog_starts")


# --- the world -----------------------------------------------------------------------------
def world():
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.add_patch(Rectangle((0, 0), 300, 200, fill=False, ec="black", lw=2.5))
    ax.add_patch(Rectangle((40, 40), 220, 120, fill=False, ec=GREY, ls="--"))
    arrow(ax, (0, 100), (40, 100), color=GREY, style="<->")
    ax.text(20, 104, "clearance\n>= r_s", ha="center", va="bottom", fontsize=8, color=GREY)
    ax.text(150, 192, "field: walls on all sides", ha="center", va="top", fontsize=9)
    ax.text(45, 152, "task area", fontsize=8, color=GREY, va="top")
    sheep(ax, blob((85, 95), 6, 40), s=8)
    ax.plot([170, 170], [45, 92], c=FENCE, lw=3)
    ax.plot([170, 170], [108, 155], c=FENCE, lw=3)
    ax.annotate("fence with a gate", (170, 100), (120, 60), fontsize=8,
                arrowprops=dict(arrowstyle="-", color=GREY))
    px, py, pw = 215, 110, 30
    ax.plot([px, px + pw, px + pw, px, px], [py, py, py + pw, py + pw, py], c=FENCE, lw=3)
    ax.plot([px, px], [py + 10, py + 20], c="white", lw=4)
    ax.annotate("pen with one gate", (px + pw / 2, py + pw), (200, 150), fontsize=8,
                arrowprops=dict(arrowstyle="-", color=GREY))
    ax.add_patch(Circle((225, 70), 12, fc=GOAL, alpha=0.2, ec=GOAL))
    ax.text(225, 52, "goal area", ha="center", color=GOAL, fontsize=8)
    ax.set_xlim(-5, 305)
    ax.set_ylim(-5, 205)
    clean(ax, "The world: field, task area and the parts a task can use (not to scale)")
    save(fig, "sch11_world")


# --- the one-dog rule ----------------------------------------------------------------------
def one_dog():
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.4))
    goal = np.array([45.0, -20.0])
    base = blob((0, 0), 2.5, 30)
    for ax, mode in zip(axes, ("drive", "collect")):
        pts = base if mode == "drive" else np.vstack([base, [[-6.0, 13.0]]])
        gcm = pts.mean(axis=0)
        F = 10.0
        sheep(ax, pts, s=12)
        ax.scatter(*gcm, marker="x", c="black", s=40, zorder=6)
        ax.add_patch(Circle(gcm, F, fill=False, ec=RED, ls="--"))
        ax.add_patch(Circle(goal, 5, fc=GOAL, alpha=0.2, ec=GOAL))
        ax.text(goal[0], goal[1] - 8, "goal G", ha="center", color=GOAL, fontsize=8)
        if mode == "drive":
            u = (gcm - goal) / np.linalg.norm(gcm - goal)
            target = gcm + 13 * u
            ax.plot([goal[0], target[0]], [goal[1], target[1]], c=GREY, ls=":", lw=1)
            ax.annotate("P_d: r_a sqrt(N) behind the centre,\non the line from G through the centre",
                        target, (-38, 22), fontsize=8, arrowprops=dict(arrowstyle="-", color=GREY))
            ax.annotate("all sheep within f(N):\nthe dog drives", (gcm[0] + F * 0.7, gcm[1] - F * 0.7),
                        (14, -26), fontsize=8, arrowprops=dict(arrowstyle="-", color=GREY))
        else:
            far = pts[-1]
            u = (far - gcm) / np.linalg.norm(far - gcm)
            target = far + 3 * u
            ax.plot([gcm[0], target[0]], [gcm[1], target[1]], c=GREY, ls=":", lw=1)
            sheep(ax, far, s=26, c=RED)
            ax.annotate("P_c: r_a behind the sheep farthest\nfrom the centre, on the line from the centre",
                        target, (-38, 24), fontsize=8, arrowprops=dict(arrowstyle="-", color=GREY))
            ax.annotate("a sheep beyond f(N):\nthe dog collects", far, (14, 18), fontsize=8,
                        arrowprops=dict(arrowstyle="-", color=GREY))
        ax.scatter(*target, marker="*", s=160, c=DOG, ec="black", zorder=6)
        dog = target + np.array([-14.0, -12.0]) if mode == "drive" else target + np.array([-16.0, -2.0])
        dogs(ax, dog, s=70)
        arrow(ax, dog, dog + 0.6 * (target - dog), color=DOG, lw=1.4)
        ax.add_patch(Circle(dog, 4.5, fill=False, ec=DOG, ls=":"))
        ax.text(dog[0], dog[1] - 6.5, "stops if a sheep is\nwithin 3 r_a", va="top", ha="center", fontsize=7, color=DOG)
        ax.set_xlim(-40, 55)
        ax.set_ylim(-32, 32)
        clean(ax, f"{mode} (not to scale)")
    fig.suptitle("The one-dog rule of Strombom et al. 2014 (equations S7 to S10); cross: flock centre, "
                 "red dashed circle: f(N), star: the dog's point", fontsize=10)
    save(fig, "sch12_one_dog")


# --- limited sensing -----------------------------------------------------------------------
def sensing():
    fig, ax = plt.subplots(figsize=(7, 6))
    ang = RNG.uniform(0, 2 * np.pi, 80)
    pts = np.c_[np.cos(ang), np.sin(ang)] * (30 * np.sqrt(RNG.uniform(0, 1, 80)))[:, None]
    dog = np.array([-38.0, -6.0])
    xi = 22.0
    seen = np.linalg.norm(pts - dog, axis=1) <= xi
    sheep(ax, pts[~seen], s=14, c="#bdbdbd")
    sheep(ax, pts[seen], s=14)
    dogs(ax, dog, s=80)
    ax.add_patch(Circle(dog, xi, fill=False, ec=DOG, ls="--"))
    ax.text(dog[0], dog[1] - xi - 3, "sensing range xi", ha="center", fontsize=8, color=DOG)
    true_c = pts.mean(axis=0)
    seen_c = pts[seen].mean(axis=0)
    ax.scatter(*true_c, marker="x", c="black", s=60, zorder=6)
    ax.scatter(*seen_c, marker="x", c=DOG, s=60, zorder=6)
    ax.annotate("centre of all sheep", true_c, (true_c[0] + 6, true_c[1] + 30), fontsize=8,
                arrowprops=dict(arrowstyle="-", color=GREY))
    ax.annotate("centre of the sheep\nthis dog senses", seen_c, (seen_c[0] - 25, seen_c[1] + 34), fontsize=8,
                color=DOG, arrowprops=dict(arrowstyle="-", color=DOG))
    ax.set_xlim(-65, 35)
    ax.set_ylim(-35, 40)
    clean(ax, "Limited sensing (not to scale): blue sensed, grey not sensed")
    save(fig, "sch13_sensing")


# --- 4.1: phases of a sheepdog trial course -------------------------------------------------
def trial_phases():
    fig, ax = plt.subplots(figsize=(8, 9))
    post = np.array([0.0, 0.0])
    sheep0 = np.array([1.5, 7.0])
    fetch_gate = np.array([0.0, 2.0])
    drive_gate1 = np.array([4.0, -1.0])
    drive_gate2 = np.array([-4.0, -1.0])
    pen = np.array([0.0, -4.0])
    shed_ring = np.array([2.6, -3.3])

    # 1 outrun: wide pear-shaped arc from the post to behind the sheep
    t = np.linspace(0, 1, 100)
    arc = post[None, :] + np.c_[6 * np.sin(np.pi * t), 1 - np.cos(np.pi * t)] * np.array([1, 3.3])
    arc[:, 0] *= -1
    ax.plot(arc[:, 0], arc[:, 1], c=DOG, lw=1.6, ls="--")
    ax.annotate("1 outrun", arc[70], arc[70] + [-2.2, 0.3], fontsize=9, color=DOG,
                arrowprops=dict(arrowstyle="-", color=DOG))

    sheep(ax, blob(sheep0, 0.35, 8), s=16)
    dogs(ax, arc[-1] + [0.9, -0.5])
    ax.annotate("2 lift", arc[-1] + [0.9, -0.5], arc[-1] + [2.3, -1.1], fontsize=9,
                arrowprops=dict(arrowstyle="-", color=GREY))

    # 3 fetch: straight line from the sheep through the fetch gate, past the post
    ax.plot([sheep0[0], fetch_gate[0]], [sheep0[1], fetch_gate[1]], c=GREY, ls=":", lw=1.2)
    ax.plot([fetch_gate[0], post[0]], [fetch_gate[1], post[1] - 1.4], c=GREY, ls=":", lw=1.2)
    ax.plot([fetch_gate[0] - 0.7, fetch_gate[0] - 0.3], [fetch_gate[1], fetch_gate[1]], c=FENCE, lw=4)
    ax.plot([fetch_gate[0] + 0.3, fetch_gate[0] + 0.7], [fetch_gate[1], fetch_gate[1]], c=FENCE, lw=4)
    ax.annotate("3 fetch, through the\nfetch gate, past the post", fetch_gate, fetch_gate + [1.9, 0.9],
                fontsize=9, arrowprops=dict(arrowstyle="-", color=GREY))

    handler = post + [0.0, -1.4]
    ax.scatter(*handler, marker="s", s=60, c="black", zorder=6)
    ax.annotate("handler's post", handler, handler + [-3.0, -0.2], fontsize=8.5, color="black",
                arrowprops=dict(arrowstyle="-", color="black"))

    # 4 drive to the first gate, 5 cross-drive to the second
    ax.plot([handler[0], drive_gate1[0]], [handler[1], drive_gate1[1]], c=SHEEP, ls="-.", lw=1.2)
    ax.plot([drive_gate1[0], drive_gate2[0]], [drive_gate1[1], drive_gate2[1]], c=SHEEP, ls="-.", lw=1.2)
    for g in (drive_gate1, drive_gate2):
        ax.plot([g[0] - 0.7, g[0] - 0.3], [g[1], g[1]], c=FENCE, lw=4)
        ax.plot([g[0] + 0.3, g[0] + 0.7], [g[1], g[1]], c=FENCE, lw=4)
    ax.annotate("4 drive, to the\nfirst drive gate", drive_gate1, drive_gate1 + [1.1, 1.0], fontsize=9,
                color=SHEEP, arrowprops=dict(arrowstyle="-", color=SHEEP))
    ax.annotate("5 cross-drive, turn\nto the second gate", drive_gate2, drive_gate2 + [-3.4, 0.8], fontsize=9,
                color=SHEEP, arrowprops=dict(arrowstyle="-", color=SHEEP))

    # 6 pen
    pw = 1.0
    ax.plot([pen[0] - pw, pen[0] + pw, pen[0] + pw, pen[0] - pw, pen[0] - pw],
             [pen[1] - pw, pen[1] - pw, pen[1] + pw, pen[1] + pw, pen[1] - pw], c=FENCE, lw=2.5)
    ax.plot([pen[0] - 0.25, pen[0] + 0.25], [pen[1] + pw, pen[1] + pw], c="white", lw=3, zorder=5)
    ax.annotate("6 pen", pen, pen + [1.6, -0.6], fontsize=9, arrowprops=dict(arrowstyle="-", color=GREY))

    # 7 shed or single
    ax.add_patch(Circle(shed_ring, 1.1, fill=False, ec=GOAL, ls=":"))
    ax.annotate("7 shed or single,\nin a marked ring", shed_ring, shed_ring + [1.5, 1.6], fontsize=9,
                color=GOAL, arrowprops=dict(arrowstyle="-", color=GOAL))

    ax.set_xlim(-8, 7.5)
    ax.set_ylim(-6.5, 9)
    clean(ax, "Phases of a sheepdog trial course (section 4.1; not to scale, no distances shown)")
    save(fig, "sch14_trial_phases")

# --- placement as D grows (section 9.5, S11) ------------------------------------------------
def dog_placement():
    fig, axes = plt.subplots(1, 4, figsize=(15, 4.4))
    goal = np.array([40.0, 0.0])
    gcm = np.array([0.0, 0.0])
    R = 20.0
    u_d = (gcm - goal) / np.linalg.norm(gcm - goal)
    u_perp = np.array([-u_d[1], u_d[0]])
    flock = blob(gcm, 3.5, 25)
    t = np.linspace(-90, 90, 100)
    arc = gcm + R * (np.cos(np.radians(t))[:, None] * u_d + np.sin(np.radians(t))[:, None] * u_perp)
    for D, ax in zip((1, 2, 3, 4), axes):
        ax.plot(arc[:, 0], arc[:, 1], c=GREY, ls=":", lw=1)
        ax.add_patch(Circle(goal, 6, fc=GOAL, alpha=0.2, ec=GOAL))
        ax.text(goal[0], goal[1] - 9, "goal", ha="center", color=GOAL, fontsize=8)
        sheep(ax, flock, s=8)
        ax.scatter(*gcm, marker="x", c="black", s=40, zorder=6)
        phis = [-90 + 180 * (i - 0.5) / D for i in range(1, D + 1)]
        push = np.zeros(2)
        for phi in phis:
            p = gcm + R * (np.cos(np.radians(phi)) * u_d + np.sin(np.radians(phi)) * u_perp)
            dogs(ax, p, s=60)
            ax.annotate(f"{phi:g}", p, p + 6.5 * (p - gcm) / R, fontsize=8, color=DOG, ha="center", va="center")
            push += (gcm - p) / R
        arrow(ax, gcm, gcm + 12 * push / np.linalg.norm(push), color=GOAL, lw=2)
        ax.set_xlim(-30, 48)
        ax.set_ylim(-30, 30)
        clean(ax, f"D = {D}")
    fig.suptitle("Driving positions on the half-ring away from the goal, phi_i = -90 + 180 (i - 0.5) / D degrees (S11)\n"
                 "green: direction of the averaged push on a sheep at the flock centre; not simulation output",
                 fontsize=10, y=0.98)
    save(fig, "sch15_dog_placement")


if __name__ == "__main__":
    for fn in (gathering, gate, holding, bodies, heading, several_dogs, sharing, one_tick, sheep_starts, dog_starts,
               world, one_dog, sensing, trial_phases, dog_placement):
        fn()
