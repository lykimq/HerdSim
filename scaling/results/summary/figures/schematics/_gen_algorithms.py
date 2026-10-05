#!/usr/bin/env python3
"""Generate algorithm schematics (EN + VI) for the summary report."""

from __future__ import annotations

import math
from pathlib import Path

OUT = Path(__file__).resolve().parent
FONT = "Segoe UI,Noto Sans,sans-serif"
BG = "#f7f6f2"
SHEEP = "#3d6b3a"
OUTLIER = "#9b2c2c"
DOG = "#1f4e79"
GOAL_FILL = "#cfe0f0"
MUTED = "#5c5852"
INK = "#1c1b19"
PANEL = "#efece5"
STROKE = "#bbb3a5"
ACCENT = "#5b4a2f"
PURPLE = "#7b1fa2"


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def text(x, y, s, *, size=12, weight=400, fill=INK, anchor="start", family=FONT):
    w = f' font-weight="{weight}"' if weight != 400 else ""
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}"'
        f'{w} fill="{fill}" font-family="{family}">{esc(s)}</text>'
    )


def circle(cx, cy, r, fill, stroke=None, sw=1):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{st}/>'


def rect(x, y, w, h, fill, stroke=None, sw=1, rx=0):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    r = f' rx="{rx}"' if rx else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{st}{r}/>'


def dog(x, y, size=7):
    return f'<rect x="{x - size/2}" y="{y - size/2}" width="{size}" height="{size}" rx="1" fill="{DOG}"/>'


def arrow_defs(uid="arr"):
    return f"""<defs>
  <marker id="{uid}" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L6,3 L0,6 Z" fill="{ACCENT}"/>
  </marker>
  <marker id="{uid}p" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L6,3 L0,6 Z" fill="{PURPLE}"/>
  </marker>
  <marker id="{uid}d" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L6,3 L0,6 Z" fill="{DOG}"/>
  </marker>
  <marker id="{uid}r" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L6,3 L0,6 Z" fill="{OUTLIER}"/>
  </marker>
</defs>"""


def line(x1, y1, x2, y2, stroke=ACCENT, sw=1.5, dash=None, marker=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#{marker})"' if marker else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"'
        f' stroke="{stroke}" stroke-width="{sw}"{d}{m}/>'
    )


def flock_blob(cx, cy, n=18, spread=18, seed=3):
    """Deterministic pseudo-random sheep around a center."""
    pts = []
    for i in range(n):
        a = (i * 2.399 + seed) % (2 * math.pi)
        r = spread * (0.25 + ((i * 7 + seed * 3) % 10) / 12.0)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a) * 0.85))
    return pts


def write(path: Path, svg: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")
    print("wrote", path)


# ---------------------------------------------------------------------------
# S10 strombom_multi: Collect | Drive
# ---------------------------------------------------------------------------

def strombom_multi(lang: str) -> str:
    if lang == "en":
        title = "strombom_multi: Collect then Drive (coordinated multi-dog)"
        left_h = "Collect: dogs assigned to distinct outliers"
        right_h = "Drive: dogs spaced on a circle behind the flock"
        gcm = "GCM"
        fN = "f(N) cohesion ring"
        goal = "goal"
        assign = "assign"
        drive = "drive"
        foot = (
            "Green = sheep · red = outliers · blue squares = dogs · "
            "Collect if any sheep beyond f(N) from GCM; else Drive"
        )
        aria = "strombom_multi Collect and Drive"
    else:
        title = "strombom_multi: Gom rồi Lùa (nhiều chó phối hợp)"
        left_h = "Gom: gán chó cho các cá thể lạc khác nhau"
        right_h = "Lùa: chó xoè trên vòng sau đàn"
        gcm = "GCM"
        fN = "vòng kết đàn f(N)"
        goal = "đích"
        assign = "gán"
        drive = "lùa"
        foot = (
            "Xanh lá = cừu · đỏ = cá thể lạc · ô xanh = chó · "
            "Gom nếu có cừu ngoài f(N) so với GCM; không thì Lùa"
        )
        aria = "strombom_multi Gom va Lua"

    w, h = 720, 340
    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">',
        rect(0, 0, w, h, BG),
        text(16, 24, title, size=14, weight=700),
        arrow_defs("s10"),
    ]

    # Left panel: Collect
    px, py, pw, ph = 20, 44, 330, 250
    parts.append(rect(px, py, pw, ph, PANEL, STROKE))
    parts.append(text(px + 10, py + 20, left_h, size=12, weight=700, fill=DOG))

    # flock + outliers
    cx, cy = px + 160, py + 140
    core = flock_blob(cx, cy, 16, 22, seed=1)
    for x, y in core:
        parts.append(circle(x, y, 2.2, SHEEP))
    outliers = [(cx - 70, cy - 55), (cx + 55, cy + 70), (cx - 40, cy + 75)]
    for x, y in outliers:
        parts.append(circle(x, y, 3.0, OUTLIER))
    parts.append(circle(cx, cy, 3.5, "#fff", DOG, 1.5))
    parts.append(text(cx + 6, cy - 6, gcm, size=10, fill=DOG))
    # f(N) ring
    parts.append(
        f'<circle cx="{cx}" cy="{cy}" r="58" fill="none" stroke="{DOG}" '
        f'stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>'
    )
    parts.append(text(cx + 42, cy - 48, fN, size=9, fill=DOG))

    dogs = [(cx - 95, cy - 40), (cx + 90, cy + 45), (cx - 70, cy + 95)]
    for (dx, dy), (ox, oy) in zip(dogs, outliers):
        parts.append(dog(dx, dy))
        parts.append(line(dx, dy, ox, oy, stroke=PURPLE, sw=1.2, dash="3 2", marker="s10p"))
    parts.append(text(px + 10, py + ph - 12, assign, size=10, fill=PURPLE))

    # Right panel: Drive
    px2 = 370
    parts.append(rect(px2, py, pw, ph, PANEL, STROKE))
    parts.append(text(px2 + 10, py + 20, right_h, size=12, weight=700, fill=DOG))

    cx2, cy2 = px2 + 140, py + 140
    core2 = flock_blob(cx2, cy2, 20, 20, seed=2)
    for x, y in core2:
        parts.append(circle(x, y, 2.2, SHEEP))
    parts.append(circle(cx2, cy2, 3.5, "#fff", DOG, 1.5))
    parts.append(text(cx2 + 6, cy2 - 6, gcm, size=10, fill=DOG))

    # goal to the right
    gx, gy = px2 + 280, cy2
    parts.append(circle(gx, gy, 10, GOAL_FILL, DOG, 1.5))
    parts.append(text(gx, gy - 16, goal, size=10, fill=DOG, anchor="middle"))
    parts.append(line(cx2 + 25, cy2, gx - 14, gy, stroke=ACCENT, sw=1.5, dash="4 3", marker="s10"))
    parts.append(text((cx2 + gx) / 2, cy2 - 12, drive, size=10, fill=ACCENT, anchor="middle"))

    # drive circle behind flock (opposite goal)
    r_drive = 36
    # behind = left of GCM
    angles = [math.pi * 0.85, math.pi, math.pi * 1.15]
    for a in angles:
        dx = cx2 + r_drive * math.cos(a)
        dy = cy2 + r_drive * math.sin(a)
        parts.append(dog(dx, dy))
    parts.append(
        f'<circle cx="{cx2}" cy="{cy2}" r="{r_drive}" fill="none" stroke="{PURPLE}" '
        f'stroke-width="1" stroke-dasharray="2 2" opacity="0.8"/>'
    )
    parts.append(text(cx2 - r_drive - 4, cy2 + r_drive + 14, "4*r_a", size=9, fill=PURPLE, anchor="end"))

    parts.append(text(16, h - 14, foot, size=11, fill=MUTED))
    parts.append("</svg>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# S11 kubo: force-based, farthest from goal
# ---------------------------------------------------------------------------

def kubo(lang: str) -> str:
    if lang == "en":
        title = "kubo: continuous forces (no Collect / Drive switch)"
        sub = "Each dog targets the in-range sheep farthest from the goal; dog-dog repulsion fans the arc"
        goal = "goal"
        sense = "sensing radius"
        tgt = "farthest from goal"
        repel = "dog-dog repel"
        force = "force sum"
        foot = (
            "Sheep and dogs use Kubo force fields (not Strombom sheep). "
            "Integration p <- p + dt * v"
        )
        aria = "kubo force-based herding"
    else:
        title = "kubo: lực liên tục (không chuyển Gom / Lùa)"
        sub = "Mỗi chó nhắm cừu trong tầm xa nhất so với đích; đẩy chó-chó xoè thành cung"
        goal = "đích"
        sense = "bán kính cảm"
        tgt = "xa nhất so với đích"
        repel = "đẩy chó-chó"
        force = "tổng lực"
        foot = (
            "Cừu và chó dùng trường lực Kubo (không phải cừu Strombom). "
            "Tích phân p <- p + dt * v"
        )
        aria = "kubo theo luc"

    w, h = 720, 320
    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">',
        rect(0, 0, w, h, BG),
        text(16, 24, title, size=14, weight=700),
        text(16, 44, sub, size=11, fill=MUTED),
        arrow_defs("s11"),
        rect(20, 58, 680, 220, PANEL, STROKE),
    ]

    # flock
    cx, cy = 280, 170
    core = flock_blob(cx, cy, 22, 28, seed=5)
    # add one sheep farthest from goal (leftmost)
    far = (cx - 55, cy + 8)
    for x, y in core:
        parts.append(circle(x, y, 2.2, SHEEP))
    parts.append(circle(far[0], far[1], 3.2, OUTLIER))
    parts.append(text(far[0] - 4, far[1] - 10, tgt, size=9, fill=OUTLIER, anchor="end"))

    gx, gy = 620, 170
    parts.append(circle(gx, gy, 12, GOAL_FILL, DOG, 1.5))
    parts.append(text(gx, gy - 18, goal, size=10, fill=DOG, anchor="middle"))
    parts.append(line(cx + 30, cy, gx - 16, gy, stroke=ACCENT, sw=1.4, dash="4 3", marker="s11"))

    # dogs in an arc behind flock
    dogs = [(cx - 70, cy - 45), (cx - 85, cy), (cx - 70, cy + 45)]
    for i, (dx, dy) in enumerate(dogs):
        parts.append(dog(dx, dy, size=8))
        # sensing radius
        parts.append(
            f'<circle cx="{dx}" cy="{dy}" r="48" fill="none" stroke="{DOG}" '
            f'stroke-width="0.8" stroke-dasharray="2 3" opacity="0.45"/>'
        )
        # attract toward farthest-from-goal sheep
        parts.append(line(dx, dy, far[0], far[1], stroke=DOG, sw=1.1, dash="3 2", marker="s11d"))
    parts.append(text(dogs[0][0] - 10, dogs[0][1] - 55, sense, size=9, fill=DOG))

    # dog-dog repulsion between adjacent
    parts.append(line(dogs[0][0], dogs[0][1] + 6, dogs[1][0], dogs[1][1] - 6,
                      stroke=PURPLE, sw=1.2, marker="s11p"))
    parts.append(line(dogs[1][0], dogs[1][1] + 6, dogs[2][0], dogs[2][1] - 6,
                      stroke=PURPLE, sw=1.2, marker="s11p"))
    parts.append(text(cx - 130, cy + 5, repel, size=9, fill=PURPLE))

    # force sum callout
    parts.append(rect(480, 80, 190, 70, "#fff", STROKE, rx=6))
    parts.append(text(575, 105, force, size=11, weight=700, fill=DOG, anchor="middle"))
    parts.append(text(575, 125, "attract + repel + align", size=10, fill=MUTED, anchor="middle"))
    parts.append(text(575, 142, "+ dog repulsion", size=10, fill=MUTED, anchor="middle"))

    parts.append(text(16, h - 14, foot, size=11, fill=MUTED))
    parts.append("</svg>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# S12 fat: farthest from the dog itself
# ---------------------------------------------------------------------------

def fat(lang: str) -> str:
    if lang == "en":
        title = "fat: each dog presses the sheep farthest from itself"
        sub = "No Collect / Drive. Stand off r_a behind the chosen sheep toward the goal"
        goal = "goal"
        far_lbl = "farthest from me"
        standoff = "stand-off r_a"
        indep = "independent (no shared target)"
        foot = (
            "Sheep are Strombom 2014. In Phases 1/2/4, obs_mode=global "
            "(each dog sees the full flock)"
        )
        aria = "FAT farthest-agent targeting"
    else:
        title = "fat: mỗi chó ép cừu xa nhất so với chính nó"
        sub = "Không Gom / Lùa. Đứng lệch r_a sau cừu đã chọn về phía đích"
        goal = "đích"
        far_lbl = "xa nhất so với tôi"
        standoff = "lệch r_a"
        indep = "độc lập (không đích chung)"
        foot = (
            "Cừu là Strombom 2014. Ở Giai đoạn 1/2/4, obs_mode=global "
            "(mỗi chó thấy cả đàn)"
        )
        aria = "FAT nham ca the xa nhat"

    w, h = 720, 320
    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">',
        rect(0, 0, w, h, BG),
        text(16, 24, title, size=14, weight=700),
        text(16, 44, sub, size=11, fill=MUTED),
        arrow_defs("s12"),
        rect(20, 58, 680, 220, PANEL, STROKE),
    ]

    cx, cy = 300, 170
    core = flock_blob(cx, cy, 18, 24, seed=8)
    for x, y in core:
        parts.append(circle(x, y, 2.2, SHEEP))

    # three dogs, each with its own farthest sheep
    dogs = [(cx - 90, cy - 70), (cx - 100, cy + 10), (cx - 80, cy + 80)]
    targets = [(cx + 40, cy - 55), (cx - 35, cy + 5), (cx + 35, cy + 60)]
    gx, gy = 640, 170
    parts.append(circle(gx, gy, 12, GOAL_FILL, DOG, 1.5))
    parts.append(text(gx, gy - 18, goal, size=10, fill=DOG, anchor="middle"))

    colors = [DOG, PURPLE, OUTLIER]
    markers = ["s12d", "s12p", "s12r"]
    for i, ((dx, dy), (tx, ty), col, mk) in enumerate(zip(dogs, targets, colors, markers)):
        parts.append(dog(dx, dy, size=8))
        parts.append(circle(tx, ty, 3.4, col if col != DOG else OUTLIER))
        # dashed range from dog to target
        parts.append(line(dx, dy, tx, ty, stroke=col, sw=1.2, dash="3 2"))
        # stand-off point behind target away from goal
        vx, vy = tx - gx, ty - gy
        norm = math.hypot(vx, vy) or 1.0
        sx = tx + 18 * vx / norm
        sy = ty + 18 * vy / norm
        parts.append(circle(sx, sy, 3, "#fff", col, 1.5))
        parts.append(line(dx, dy, sx, sy, stroke=col, sw=1.3, marker=mk))
        if i == 0:
            parts.append(text(tx + 8, ty - 10, far_lbl, size=9, fill=OUTLIER))
            parts.append(text(sx + 6, sy + 4, standoff, size=9, fill=col))

    parts.append(text(cx + 120, cy + 95, indep, size=10, fill=PURPLE))

    parts.append(text(16, h - 14, foot, size=11, fill=MUTED))
    parts.append("</svg>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# S13 side-by-side "what farthest means"
# ---------------------------------------------------------------------------

def farthest_compare(lang: str) -> str:
    if lang == "en":
        title = 'What "farthest" means in each controller'
        cards = [
            ("strombom_multi Collect", "farthest from GCM\n(outlier vs flock centre)", DOG),
            ("kubo", "farthest from the goal\n(among sheep in range)", PURPLE),
            ("fat", "farthest from the dog\n(among observed sheep)", OUTLIER),
        ]
        foot = "Same word, three different targets. That is why transfer results can diverge."
        aria = "farthest meaning comparison"
        gcm, goal, me = "GCM", "goal", "dog"
    else:
        title = 'Ý nghĩa "xa nhất" ở mỗi bộ điều khiển'
        cards = [
            ("strombom_multi Gom", "xa nhất so với GCM\n(cá thể lạc vs tâm đàn)", DOG),
            ("kubo", "xa nhất so với đích\n(trong tầm cảm)", PURPLE),
            ("fat", "xa nhất so với chó\n(trong tập quan sát)", OUTLIER),
        ]
        foot = "Cùng chữ, ba đích khác nhau. Đó là lý do kết quả chuyển giao có thể lệch."
        aria = "so sanh y nghia xa nhat"
        gcm, goal, me = "GCM", "đích", "chó"

    w, h = 720, 280
    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">',
        rect(0, 0, w, h, BG),
        text(16, 24, title, size=14, weight=700),
        arrow_defs("s13"),
    ]

    card_w, card_h = 210, 190
    gap = 20
    x0 = 30
    y0 = 44
    for i, (head, body, col) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        parts.append(rect(x, y0, card_w, card_h, "#fff", col, 2, rx=8))
        parts.append(text(x + card_w / 2, y0 + 24, head, size=12, weight=700, fill=col, anchor="middle"))
        # mini scene
        cx, cy = x + 90, y0 + 100
        for sx, sy in flock_blob(cx, cy, 10, 16, seed=i + 2):
            parts.append(circle(sx, sy, 2.0, SHEEP))
        if i == 0:
            parts.append(circle(cx, cy, 3, "#fff", DOG, 1.2))
            parts.append(text(cx + 5, cy - 5, gcm, size=8, fill=DOG))
            ox, oy = cx + 28, cy - 28
            parts.append(circle(ox, oy, 3, OUTLIER))
            parts.append(dog(cx - 35, cy + 25, 6))
            parts.append(line(cx - 35, cy + 25, ox, oy, stroke=col, sw=1.1, marker="s13d" if i == 0 else "s13p"))
        elif i == 1:
            gx, gy = x + card_w - 28, cy
            parts.append(circle(gx, gy, 7, GOAL_FILL, DOG, 1.2))
            parts.append(text(gx, gy - 12, goal, size=8, fill=DOG, anchor="middle"))
            ox, oy = cx - 30, cy + 5
            parts.append(circle(ox, oy, 3, OUTLIER))
            parts.append(dog(cx - 40, cy - 20, 6))
            parts.append(line(cx - 40, cy - 20, ox, oy, stroke=col, sw=1.1, marker="s13p"))
        else:
            gx, gy = x + card_w - 28, cy
            parts.append(circle(gx, gy, 7, GOAL_FILL, DOG, 1.2))
            parts.append(text(gx, gy - 12, goal, size=8, fill=DOG, anchor="middle"))
            dx, dy = cx - 40, cy + 20
            ox, oy = cx + 25, cy - 25
            parts.append(dog(dx, dy, 6))
            parts.append(circle(ox, oy, 3, OUTLIER))
            parts.append(line(dx, dy, ox, oy, stroke=col, sw=1.1, marker="s13r"))
            parts.append(text(dx - 4, dy + 18, me, size=8, fill=col))

        for j, line_s in enumerate(body.split("\n")):
            parts.append(text(x + card_w / 2, y0 + 158 + j * 14, line_s, size=10, fill=MUTED, anchor="middle"))

    parts.append(text(16, h - 12, foot, size=11, fill=MUTED))
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    for lang in ("en", "vi"):
        d = OUT / lang
        write(d / "alg_strombom_multi.svg", strombom_multi(lang))
        write(d / "alg_kubo.svg", kubo(lang))
        write(d / "alg_fat.svg", fat(lang))
        write(d / "alg_farthest_compare.svg", farthest_compare(lang))


if __name__ == "__main__":
    main()
