#!/usr/bin/env python3
"""Generate design-choice and comparison schematics (EN + VI) for the summary report."""

from __future__ import annotations

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
GREEN = "#2f6b45"
RED = "#9b2c2c"
BLUE = "#1f4e79"
ORANGE = "#b45309"


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def text(x, y, s, *, size=12, weight=400, fill=INK, anchor="start"):
    w = f' font-weight="{weight}"' if weight != 400 else ""
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}"'
        f'{w} fill="{fill}" font-family="{FONT}">{esc(s)}</text>'
    )


def rect(x, y, w, h, fill, stroke=None, sw=1, rx=0):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    r = f' rx="{rx}"' if rx else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{st}{r}/>'


def circle(cx, cy, r, fill, stroke=None, sw=1):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{st}/>'


def line(x1, y1, x2, y2, stroke=ACCENT, sw=1.5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"'
        f' stroke="{stroke}" stroke-width="{sw}"{d}/>'
    )


def write(path: Path, svg: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")
    print("wrote", path)


# ---------------------------------------------------------------------------
# S14: N and D grids
# ---------------------------------------------------------------------------

def nd_grids(lang: str) -> str:
    if lang == "en":
        title = "Design: N and D grids (why denser where frontiers sit)"
        n_h = "N grid (10 sizes)"
        d_h = "D grid (10 dog counts)"
        n_note = "Tighter around 100 (draft change point). Floor 5. Skip 250, 350."
        d_note = "Step 1 near D_min (1 to 4); wider after. Cap 35."
        foot = "Dense where the answer usually lives; sparse where only large jumps matter."
        aria = "N and D design grids"
    else:
        title = "Thiết kế: lưới N và D (dày ở nơi biên thường nằm)"
        n_h = "Lưới N (10 kích thước)"
        d_h = "Lưới D (10 số chó)"
        n_note = "Dày quanh 100 (điểm đổi của bản thảo). Sàn 5. Bỏ 250, 350."
        d_note = "Bước 1 gần D_min (1 đến 4); thưa sau đó. Trần 35."
        foot = "Dày nơi câu trả lời thường nằm; thưa nơi chỉ bước lớn mới quan trọng."
        aria = "luoi N va D"

    n_vals = [5, 10, 25, 50, 75, 100, 150, 200, 300, 400]
    d_vals = [1, 2, 3, 4, 6, 10, 15, 20, 25, 35]
    # highlight around 100 for N and 1-4 for D
    w, h = 720, 260
    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">',
        rect(0, 0, w, h, BG),
        text(16, 24, title, size=14, weight=700),
        text(16, 52, n_h, size=12, weight=700, fill=DOG),
        text(16, 70, n_note, size=11, fill=MUTED),
    ]
    x0, y0 = 30, 88
    for i, n in enumerate(n_vals):
        x = x0 + i * 68
        hot = n in (75, 100, 150)
        fill = "#dbeafe" if hot else "#fff"
        stroke = DOG if hot else STROKE
        parts.append(rect(x, y0, 58, 36, fill, stroke, 1.5 if hot else 1, rx=6))
        parts.append(text(x + 29, y0 + 23, str(n), size=13, weight=700, fill=DOG, anchor="middle"))

    parts.append(text(16, 152, d_h, size=12, weight=700, fill=GREEN))
    parts.append(text(16, 170, d_note, size=11, fill=MUTED))
    for i, d in enumerate(d_vals):
        x = x0 + i * 68
        hot = d <= 4
        fill = "#dcfce7" if hot else "#fff"
        stroke = GREEN if hot else STROKE
        parts.append(rect(x, 188, 58, 36, fill, stroke, 1.5 if hot else 1, rx=6))
        parts.append(text(x + 29, 211, str(d), size=13, weight=700, fill=GREEN, anchor="middle"))

    parts.append(text(16, h - 12, foot, size=11, fill=MUTED))
    parts.append("</svg>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# S15: frontier definitions on an R(D) sketch
# ---------------------------------------------------------------------------

def frontier_defs(lang: str) -> str:
    if lang == "en":
        title = "Design: how HerdSim reads D_min, D_overcrowd, D_max, B*"
        theta = "theta = 0.90"
        dmin = "D_min"
        dover = "D_overcrowd"
        dmax = "D_max"
        bstar = "B* = cheapest reliable D"
        foot = "Sketch only. Overcrowding needs two consecutive D below theta after D_min."
        aria = "frontier definitions"
        ylab, xlab = "R", "D"
    else:
        title = "Thiết kế: HerdSim đọc D_min, D_overcrowd, D_max, B* thế nào"
        theta = "theta = 0.90"
        dmin = "D_min"
        dover = "D_overcrowd"
        dmax = "D_max"
        bstar = "B* = D đáng tin rẻ nhất"
        foot = "Phác thảo. Quá tải cần hai D liên tiếp dưới theta sau D_min."
        aria = "dinh nghia bien"
        ylab, xlab = "R", "D"

    w, h = 720, 300
    ax, ay, aw, ah = 70, 50, 520, 180
    xs = [0.05, 0.15, 0.25, 0.35, 0.48, 0.60, 0.72, 0.84, 0.92]
    rs = [0.55, 0.78, 0.92, 0.95, 0.93, 0.88, 0.82, 0.78, 0.75]
    y_th = ay + ah * (1 - 0.90)

    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">',
        rect(0, 0, w, h, BG),
        text(16, 24, title, size=14, weight=700),
        rect(ax, ay, aw, ah, "#fff", STROKE),
        line(ax, y_th, ax + aw, y_th, stroke=ORANGE, sw=1.2, dash="4 3"),
        text(ax + aw + 8, y_th + 4, theta, size=10, fill=ORANGE),
    ]

    pts = []
    for fx, fr in zip(xs, rs):
        px = ax + fx * aw
        py = ay + ah * (1 - fr)
        pts.append(f"{px:.1f},{py:.1f}")
        parts.append(circle(px, py, 3.5, DOG))
    parts.append(
        f'<polyline points="{" ".join(pts)}" fill="none" stroke="{DOG}" stroke-width="2"/>'
    )

    def x_at(i):
        return ax + xs[i] * aw

    parts.append(line(x_at(2), ay, x_at(2), ay + ah, stroke=GREEN, sw=1.5, dash="2 2"))
    parts.append(text(x_at(2), ay + ah + 16, dmin, size=11, weight=700, fill=GREEN, anchor="middle"))
    parts.append(circle(x_at(2), ay + ah * (1 - rs[2]), 6, "#fff", GREEN, 2))
    parts.append(text(x_at(2) + 8, ay + ah * (1 - rs[2]) - 8, bstar, size=10, fill=GREEN))
    parts.append(line(x_at(5), ay, x_at(5), ay + ah, stroke=RED, sw=1.5, dash="2 2"))
    parts.append(text(x_at(5), ay + ah + 16, dover, size=11, weight=700, fill=RED, anchor="middle"))
    parts.append(line(x_at(4), ay, x_at(4), ay + ah, stroke=PURPLE, sw=1.2, dash="2 2"))
    parts.append(text(x_at(4), ay - 8, dmax, size=11, weight=700, fill=PURPLE, anchor="middle"))

    parts.append(text(ax - 28, ay + ah / 2, ylab, size=12, fill=MUTED, anchor="middle"))
    parts.append(text(ax + aw / 2, ay + ah + 36, xlab, size=12, fill=MUTED, anchor="middle"))
    parts.append(text(16, h - 12, foot, size=11, fill=MUTED))
    parts.append("</svg>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# S16: timeout / drive geometry
# ---------------------------------------------------------------------------

def timeout_drive(lang: str) -> str:
    if lang == "en":
        title = "Design: field, drive length, and timeout budget"
        field = "field 500 x 500"
        drive = "drive ~120"
        t0 = "T0 = 10,000 ticks"
        note = "~80 straight crossings at speed 1: timeout means loss of control, not a short race"
        t1 = "T1 = 20,000 only if overcrowding cells exist (none on baseline)"
        aria = "timeout and drive"
    else:
        title = "Thiết kế: sân, quãng đường lùa, và ngân sách thời gian"
        field = "sân 500 x 500"
        drive = "lùa ~120"
        t0 = "T0 = 10,000 bước"
        note = "~80 lần đi thẳng ở tốc độ 1: hết giờ = mất kiểm soát, không phải cuộc đua ngắn"
        t1 = "T1 = 20,000 chỉ khi có ô quá tải (không có ở mức cơ sở)"
        aria = "het gio va lua"

    w, h = 720, 260
    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">',
        rect(0, 0, w, h, BG),
        text(16, 24, title, size=14, weight=700),
        rect(40, 50, 280, 160, PANEL, STROKE),
        text(180, 70, field, size=11, fill=MUTED, anchor="middle"),
        # flock and goal
        circle(120, 140, 8, SHEEP),
        circle(300, 140, 14, GOAL_FILL, DOG, 1.5),
        text(120, 165, "N", size=10, fill=SHEEP, anchor="middle"),
        text(300, 120, "goal", size=10, fill=DOG, anchor="middle") if lang == "en"
        else text(300, 120, "đích", size=10, fill=DOG, anchor="middle"),
        line(132, 140, 282, 140, stroke=ACCENT, sw=2, dash="5 3"),
        text(207, 132, drive, size=11, weight=700, fill=ACCENT, anchor="middle"),
        # callouts
        rect(360, 60, 330, 140, "#fff", STROKE, rx=8),
        text(375, 90, t0, size=13, weight=700, fill=DOG),
        text(375, 118, note, size=11, fill=MUTED),
        # wrap note manually - if long may overflow; keep short
        text(375, 150, t1, size=11, fill=MUTED),
        text(16, h - 14, "", size=11),
    ]
    # fix Vietnamese goal label without ternary mess
    if lang != "en":
        # replace the goal text already added - easier rebuild that part
        pass
    parts.append("</svg>")
    # Rebuild goal label cleanly
    svg = "\n".join(parts)
    if lang != "en":
        svg = svg.replace(">goal<", ">đích<")
    return svg


# ---------------------------------------------------------------------------
# S17: failure labels
# ---------------------------------------------------------------------------

def failure_labels(lang: str) -> str:
    """Priority cards plus mini metric sketches of what each failure looks like."""
    if lang == "en":
        title = "Failure labels: what they mean, and what the metric curves look like"
        items = [
            ("1. stacking", "dogs pile on one point", DOG),
            ("2. split", "flock stays in pieces", PURPLE),
            ("3. scatter", "cohesion distances high", ORANGE),
            ("4. oscillation", "GCM flips, little progress", RED),
            ("5. stuck", "GCM barely moves to goal", ACCENT),
            ("6. timeout", "still unfinished at T0", MUTED),
        ]
        sketch_title = "How a failed trial looks on its metric graph (schematic)"
        sketches = [
            ("success", "gcm_goal falls to goal", GREEN, "fall"),
            ("oscillation", "gcm_goal zigzags, stays high", RED, "zigzag"),
            ("stuck", "gcm_goal flat / tiny drop", ACCENT, "flat"),
            ("timeout", "gcm_goal still high at T0", MUTED, "slow"),
            ("scatter", "cohesion stays high", ORANGE, "high"),
            ("split", "fragmentation stays low", PURPLE, "low"),
        ]
        foot = (
            "Labels are analysis heuristics after a failed trial (not the stop reason). "
            "First match in priority order wins. stacking needs dog-separation history "
            "(rare in these runs)."
        )
        seen = "Seen in claim data: oscillation, stuck, timeout, scatter, split. Not seen: stacking."
        aria = "failure labels"
    else:
        title = "Nhãn thất bại: ý nghĩa, và đường cong chỉ số nhìn ra sao"
        items = [
            ("1. chồng chất", "chó chồng lên một điểm", DOG),
            ("2. tách", "đàn còn nhiều cụm", PURPLE),
            ("3. tán", "khoảng cách kết đàn cao", ORANGE),
            ("4. dao động", "GCM đổi dấu, tiến ít", RED),
            ("5. kẹt", "GCM gần như không tiến về đích", ACCENT),
            ("6. hết giờ", "chưa xong tại T0", MUTED),
        ]
        sketch_title = "Lượt thất bại nhìn trên đồ thị chỉ số (phác thảo)"
        sketches = [
            ("thành công", "gcm_goal hạ về đích", GREEN, "fall"),
            ("dao động", "gcm_goal zigzag, vẫn cao", RED, "zigzag"),
            ("kẹt", "gcm_goal phẳng / hạ rất ít", ACCENT, "flat"),
            ("hết giờ", "gcm_goal vẫn cao tại T0", MUTED, "slow"),
            ("tán", "cohesion giữ cao", ORANGE, "high"),
            ("tách", "fragmentation giữ thấp", PURPLE, "low"),
        ]
        foot = (
            "Nhãn là heuristic phân tích sau khi lượt thất bại (không phải lý do dừng). "
            "Nhãn khớp đầu tiên theo thứ tự ưu tiên thắng. chồng chất cần lịch sử khoảng cách chó "
            "(hiếm trong các lần chạy này)."
        )
        seen = "Có trong dữ liệu xác nhận: dao động, kẹt, hết giờ, tán, tách. Không thấy: chồng chất."
        aria = "nhan that bai"

    def mini_curve(x0: float, y0: float, kind: str, col: str) -> list[str]:
        # small 90x42 plot frame
        w, h = 90, 42
        out = [
            rect(x0, y0, w, h, "#fff", STROKE, 1, rx=3),
            line(x0 + 6, y0 + h - 6, x0 + w - 6, y0 + h - 6, stroke=STROKE, sw=1),
            line(x0 + 6, y0 + 6, x0 + 6, y0 + h - 6, stroke=STROKE, sw=1),
        ]
        # polyline paths inside frame
        if kind == "fall":
            pts = [(8, 10), (28, 14), (50, 22), (70, 32), (84, 36)]
        elif kind == "zigzag":
            pts = [(8, 12), (20, 28), (32, 10), (44, 30), (56, 12), (68, 28), (84, 14)]
        elif kind == "flat":
            pts = [(8, 14), (30, 15), (55, 16), (84, 17)]
        elif kind == "slow":
            pts = [(8, 12), (35, 16), (60, 22), (84, 26)]
        elif kind == "high":
            pts = [(8, 12), (30, 11), (55, 13), (84, 12)]
        else:  # low fragmentation stays near bottom
            pts = [(8, 34), (30, 33), (55, 35), (84, 34)]
        path = " ".join(f"{x0 + px},{y0 + py}" for px, py in pts)
        # use polyline via multiple short lines
        for (a, b) in zip(pts, pts[1:]):
            out.append(
                line(x0 + a[0], y0 + a[1], x0 + b[0], y0 + b[1], stroke=col, sw=2)
            )
        return out

    w, h = 740, 360
    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">',
        rect(0, 0, w, h, BG),
        text(16, 24, title, size=14, weight=700),
    ]
    for i, (name, desc, col) in enumerate(items):
        x = 16 + (i % 3) * 240
        y = 40 + (i // 3) * 58
        parts.append(rect(x, y, 228, 50, "#fff", col, 2, rx=8))
        parts.append(text(x + 12, y + 22, name, size=12, weight=700, fill=col))
        parts.append(text(x + 12, y + 40, desc, size=11, fill=MUTED))

    parts.append(text(16, 172, sketch_title, size=12, weight=700, fill=INK))
    for i, (name, desc, col, kind) in enumerate(sketches):
        x = 16 + (i % 6) * 120
        y = 188
        parts.extend(mini_curve(x, y, kind, col))
        parts.append(text(x + 45, y + 56, name, size=10, weight=700, fill=col, anchor="middle"))
        # wrap desc under in two short lines if needed
        parts.append(text(x + 45, y + 70, desc, size=9, fill=MUTED, anchor="middle"))

    parts.append(text(16, h - 28, seen, size=11, weight=700, fill=BLUE))
    parts.append(text(16, h - 10, foot, size=10, fill=MUTED))
    parts.append("</svg>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# S18: draft task vs HerdSim task
# ---------------------------------------------------------------------------

def draft_vs_herdsim(lang: str) -> str:
    if lang == "en":
        title = "Draft task vs HerdSim task (why outcomes can diverge)"
        left_h = "2025 draft (NetLogo)"
        right_h = "HerdSim (this study)"
        left = ["1. Collect", "2. Hold 800 ticks", "3. Exit gate", "Start: random scatter", "Dogs: top-left corner"]
        right = ["1. Drive into goal disk", "(no hold / no gate)", "", "Start: controlled layouts", "Dogs: behind flock"]
        foot = "Same science family (D vs N, SR >= 90%), different task and starts."
        aria = "draft vs HerdSim task"
    else:
        title = "Nhiệm vụ bản thảo so với HerdSim (vì sao kết quả có thể lệch)"
        left_h = "Bản thảo 2025 (NetLogo)"
        right_h = "HerdSim (nghiên cứu này)"
        left = ["1. Gom", "2. Giữ 800 bước", "3. Thoát cổng", "Xuất phát: rải ngẫu nhiên", "Chó: góc trên trái"]
        right = ["1. Lùa vào đĩa đích", "(không giữ / không cổng)", "", "Xuất phát: bố cục kiểm soát", "Chó: sau đàn"]
        foot = "Cùng họ câu hỏi (D theo N, SR >= 90%), khác nhiệm vụ và xuất phát."
        aria = "ban thao vs HerdSim"

    w, h = 720, 280
    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">',
        rect(0, 0, w, h, BG),
        text(16, 24, title, size=14, weight=700),
        rect(30, 44, 300, 190, "#fff", ORANGE, 2, rx=10),
        rect(390, 44, 300, 190, "#fff", DOG, 2, rx=10),
        text(180, 72, left_h, size=13, weight=700, fill=ORANGE, anchor="middle"),
        text(540, 72, right_h, size=13, weight=700, fill=DOG, anchor="middle"),
    ]
    for i, s in enumerate(left):
        if s:
            parts.append(text(50, 105 + i * 24, s, size=12, fill=INK))
    for i, s in enumerate(right):
        if s:
            parts.append(text(410, 105 + i * 24, s, size=12, fill=INK))
    parts.append(text(360, 140, "vs", size=16, weight=700, fill=MUTED, anchor="middle"))
    parts.append(text(16, h - 14, foot, size=11, fill=MUTED))
    parts.append("</svg>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# S19: theta reliability bar
# ---------------------------------------------------------------------------

def theta_bar(lang: str) -> str:
    if lang == "en":
        title = "Design: theta = 0.90 decides D_min"
        sub = "0.50 and 0.70 are reported for diagnostics, not for the claim frontier"
        fail = "fail band"
        pass_ = "pass band"
        foot = "Same reliable band as the 2025 draft."
        aria = "theta reliability"
    else:
        title = "Thiết kế: theta = 0.90 quyết định D_min"
        sub = "0.50 và 0.70 được báo cáo để chẩn đoán, không dùng cho biên kết luận"
        fail = "dải thất bại"
        pass_ = "dải đạt"
        foot = "Cùng dải tin cậy với bản thảo 2025."
        aria = "nguong theta"

    w, h = 720, 180
    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">',
        rect(0, 0, w, h, BG),
        text(16, 24, title, size=14, weight=700),
        text(16, 44, sub, size=11, fill=MUTED),
        # bar
        rect(60, 80, 540, 28, "#fecaca", None, 0, rx=6),
        rect(60 + 0.90 * 540, 80, 0.10 * 540, 28, "#bbf7d0", None, 0, rx=0),
        # fix right end radius with overlay
        rect(60, 80, 540, 28, "none", STROKE, 1, rx=6),
        line(60 + 0.90 * 540, 70, 60 + 0.90 * 540, 120, stroke=GREEN, sw=2),
        text(60 + 0.90 * 540, 64, "0.90", size=12, weight=700, fill=GREEN, anchor="middle"),
        text(60 + 0.45 * 540, 100, fail, size=12, fill=RED, anchor="middle"),
        text(60 + 0.95 * 540, 100, pass_, size=11, fill=GREEN, anchor="middle"),
        text(60, 140, "0", size=10, fill=MUTED, anchor="middle"),
        text(60 + 540, 140, "1", size=10, fill=MUTED, anchor="middle"),
        text(16, h - 12, foot, size=11, fill=MUTED),
        "</svg>",
    ]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# S20: bootstrap on D_min
# ---------------------------------------------------------------------------

def bootstrap_dmin(lang: str) -> str:
    if lang == "en":
        title = "Bootstrap on D_min: resample seeds, not new simulations"
        p1 = "1. Observed seeds per D"
        p2 = "2. Resample within each D"
        p3 = "3. Interval from percentiles"
        r_labels = [("D=1", "R=0.50", ORANGE), ("D=2", "R=0.88", ORANGE), ("D=3", "R=1.00", BLUE)]
        ok, fail = "success", "fail"
        resample_note = "... x 1,000"
        resample_foot = "1,000 resamples -> 1,000 D_min*"
        hist_sub = "count of D_min*"
        interval = "2.5% to 97.5%"
        foot = "Why: finite seeds make D_min noisy. Width zero means every resample gave the same D_min."
        aria = "bootstrap D_min"
    else:
        title = "Bootstrap trên D_min: lấy mẫu lại hạt giống, không chạy mô phỏng mới"
        p1 = "1. Hạt giống quan sát theo D"
        p2 = "2. Lấy mẫu lại trong mỗi D"
        p3 = "3. Khoảng từ phân vị"
        r_labels = [("D=1", "R=0.50", ORANGE), ("D=2", "R=0.88", ORANGE), ("D=3", "R=1.00", BLUE)]
        ok, fail = "thành công", "thất bại"
        resample_note = "... x 1,000"
        resample_foot = "1,000 lần -> 1,000 D_min*"
        hist_sub = "số lần ra D_min*"
        interval = "2.5% đến 97.5%"
        foot = "Vì sao: mẫu hữu hạn làm D_min nhiễu. Độ rộng 0: mọi lần lấy mẫu cho cùng D_min."
        aria = "bootstrap D_min"

    w, h = 740, 310
    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">',
        rect(0, 0, w, h, BG),
        text(16, 22, title, size=14, weight=700),
        # panel 1
        rect(16, 40, 220, 220, "#fff", STROKE, 1, rx=8),
        text(28, 62, p1, size=12, weight=700, fill=BLUE),
    ]

    cols = [
        (50, [GREEN, RED, GREEN, RED, RED, GREEN, RED, GREEN]),
        (110, [GREEN, GREEN, GREEN, GREEN, RED, GREEN, GREEN, GREEN]),
        (170, [GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN]),
    ]
    for (cx, colors), (dlab, rlab, rcol) in zip(cols, r_labels):
        parts.append(text(cx, 84, dlab, size=11, weight=700, fill=MUTED, anchor="middle"))
        for i, c in enumerate(colors):
            parts.append(circle(cx, 100 + i * 13, 4.2, c))
        parts.append(text(cx, 215, rlab, size=10, fill=rcol, anchor="middle"))

    parts += [
        circle(40, 240, 4, GREEN),
        text(50, 244, ok, size=10, fill=MUTED),
        circle(115, 240, 4, RED),
        text(125, 244, fail, size=10, fill=MUTED),
        text(248, 150, "→", size=24, fill=MUTED, anchor="middle"),
        # panel 2
        rect(268, 40, 210, 220, "#fff", STROKE, 1, rx=8),
        text(280, 62, p2, size=12, weight=700, fill=PURPLE),
    ]

    rows = [
        [GREEN, RED, GREEN, GREEN, RED, GREEN, GREEN, GREEN],
        [RED, GREEN, GREEN, RED, GREEN, GREEN, GREEN, RED],
        [GREEN, GREEN, RED, GREEN, GREEN, GREEN, RED, GREEN],
        [GREEN, RED, GREEN, GREEN, GREEN, RED, GREEN, GREEN],
        [GREEN, RED, GREEN, GREEN, RED, GREEN, GREEN, GREEN],
    ]
    for i, row in enumerate(rows):
        y = 80 + i * 24
        fill = "#f3e8ff" if i % 2 == 0 else "#ede9fe"
        parts.append(rect(285, y, 175, 18, fill, PURPLE, 1, rx=3))
        for j, c in enumerate(row):
            parts.append(circle(300 + j * 18, y + 9, 3.2, c))
        parts.append(text(450, y + 13, f"#{i+1}", size=9, fill=PURPLE, anchor="end"))

    parts += [
        text(373, 215, resample_note, size=12, weight=700, fill=PURPLE, anchor="middle"),
        text(373, 240, resample_foot, size=10, fill=MUTED, anchor="middle"),
        text(492, 150, "→", size=24, fill=MUTED, anchor="middle"),
        # panel 3: histogram with interval BELOW bars (no overlap with top labels)
        rect(510, 40, 214, 220, "#fff", STROKE, 1, rx=8),
        text(522, 62, p3, size=12, weight=700, fill=GREEN),
        text(617, 82, hist_sub, size=10, fill=MUTED, anchor="middle"),
        # bars sit on a baseline; leave clear space above for subtitle only
        rect(545, 160, 30, 40, "#bbf7d0", GREEN, 1, rx=2),
        rect(600, 95, 30, 105, "#bbf7d0", GREEN, 1, rx=2),
        rect(655, 145, 30, 55, "#bbf7d0", GREEN, 1, rx=2),
        text(560, 216, "1", size=11, fill=MUTED, anchor="middle"),
        text(615, 216, "2", size=11, fill=MUTED, anchor="middle"),
        text(670, 216, "3", size=11, fill=MUTED, anchor="middle"),
        # percentile bracket under the axis labels
        line(545, 230, 685, 230, stroke=ORANGE, sw=2.5),
        line(545, 222, 545, 230, stroke=ORANGE, sw=2),
        line(685, 222, 685, 230, stroke=ORANGE, sw=2),
        text(617, 248, interval, size=11, weight=700, fill=ORANGE, anchor="middle"),
        text(16, h - 12, foot, size=11, fill=MUTED),
        "</svg>",
    ]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# S21: field map (literature themes vs this study)
# ---------------------------------------------------------------------------

def field_map(lang: str) -> str:
    if lang == "en":
        title = "Where this study sits in the shepherding field"
        headers = ("Theme / paper", "Classic focus", "HerdSim finding here")
        rows = [
            ("Strombom 2014", "Collect/Drive; one dog, moderate N", "1 dog to N=400 on drive_to_goal; N=5,10 need 2"),
            ("Kubo 2022", "Multi-dog repulsion aids guidance", "Matches compact size map; fails on wide starts"),
            ("Tsunoda / FAT", "Local farthest-sheep targeting", "Under global obs: R>=0.90 only for N<=10"),
            ("2025 draft", "Steep D_min(N); overcrowding", "Not reproduced (task and starts differ)"),
            ("Structure / herdability", "Start state and controllability", "Cost shifts huge; D_min floor on baseline"),
        ]
        foot = "Mapping themes, not a claim that published numbers were re-run bit-for-bit."
        aria = "field map"
    else:
        title = "Nghiên cứu này nằm đâu trong lĩnh vực chăn đàn"
        headers = ("Chủ đề / bài báo", "Trọng tâm cổ điển", "Phát hiện HerdSim ở đây")
        rows = [
            ("Strombom 2014", "Gom/Lùa; một chó, N vừa", "1 chó đến N=400 trên drive_to_goal; N=5,10 cần 2"),
            ("Kubo 2022", "Đẩy giữa chó hỗ trợ dẫn đàn", "Khớp bản đồ tập trung; thất bại ở phân tán"),
            ("Tsunoda / FAT", "Nhắm cừu xa nhất (cục bộ)", "Quan sát toàn cục: R>=0.90 chỉ khi N<=10"),
            ("Bản thảo 2025", "D_min(N) dốc; quá tải", "Không tái hiện (nhiệm vụ và xuất phát khác)"),
            ("Cấu trúc / herdability", "Trạng thái đầu và điều khiển được", "Chi phí lệch lớn; D_min chạm sàn ở cơ sở"),
        ]
        foot = "Ghép chủ đề, không khẳng định đã chạy lại số liệu bài báo từng bit."
        aria = "ban do linh vuc"

    w, h = 760, 300
    col_w = (220, 240, 260)
    x0 = 16
    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">',
        rect(0, 0, w, h, BG),
        text(16, 24, title, size=14, weight=700),
    ]
    x = x0
    fills = (DOG, PURPLE, GREEN)
    for hdr, cw, fill in zip(headers, col_w, fills):
        parts.append(rect(x, 40, cw - 8, 36, fill, None, 0, rx=6))
        parts.append(text(x + 10, 62, hdr, size=11, weight=700, fill="#fff"))
        x += cw
    for r_i, row in enumerate(rows):
        y = 86 + r_i * 36
        x = x0
        bg = "#fff" if r_i % 2 == 0 else "#efece5"
        for cell, cw in zip(row, col_w):
            parts.append(rect(x, y, cw - 8, 32, bg, STROKE, 1, rx=4))
            parts.append(text(x + 8, y + 21, cell, size=10, fill=INK))
            x += cw
    parts.append(text(16, h - 12, foot, size=11, fill=MUTED))
    parts.append("</svg>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# S22: NetLogo platform vs HerdSim system (design nature)
# ---------------------------------------------------------------------------

def netlogo_vs_herdsim(lang: str) -> str:
    if lang == "en":
        title = "NetLogo the platform versus HerdSim the system"
        left_h = "NetLogo (ABM platform)"
        right_h = "HerdSim (shepherding stack)"
        left = [
            "General agent-based modeling language",
            "Patch / turtle world (discrete space)",
            "Desktop IDE: setup, go, monitors",
            "BehaviorSpace for batch sweeps",
            "Any .nlogo model (education + research)",
        ]
        right = [
            "Domain stack for sheep herding methods",
            "Continuous space, elastic walls, discrete ticks",
            "Simulate / Compare / Experiments apps",
            "Scout-claim staging, seeds, CSV provenance",
            "Shared scenarios + metrics across methods",
        ]
        mid = "related, not the same binary"
        mid2 = "twins bridge shared methods"
        foot = (
            "Twins exist for some methods (behaviour check, not bit-identical). "
            "The 2025 draft is one NetLogo model with its own task; not NetLogo itself."
        )
        aria = "netlogo platform vs herdsim system"
        row_h = "Design axis"
        rows = [
            ("Purpose", "General ABM toolkit", "Controlled herding experiments"),
            ("Space", "Patches / turtles", "Continuous positions"),
            ("Batch", "BehaviorSpace / manual", "Experiments + claim pipeline"),
            ("Compare", "Separate windows", "Compare tab + shared metrics"),
        ]
    else:
        title = "NetLogo như nền tảng so với HerdSim như hệ thống"
        left_h = "NetLogo (nền tảng ABM)"
        right_h = "HerdSim (chồng chăn đàn)"
        left = [
            "Ngôn ngữ mô phỏng đa tác nhân tổng quát",
            "Thế giới ô / rùa (không gian rời rạc)",
            "IDE máy tính: setup, go, monitor",
            "BehaviorSpace cho quét hàng loạt",
            "Mọi mô hình .nlogo (học + nghiên cứu)",
        ]
        right = [
            "Chồng chuyên cho phương pháp chăn đàn",
            "Không gian liên tục, tường đàn hồi, bước rời",
            "Ứng dụng Simulate / Compare / Experiments",
            "Phân tầng dò đường-xác nhận, hạt giống, CSV",
            "Kịch bản + chỉ số chung giữa các phương pháp",
        ]
        mid = "liên quan, không cùng nhị phân"
        mid2 = "twin nối phương pháp dùng chung"
        foot = (
            "Có twin cho một số phương pháp (kiểm hành vi, không trùng bit). "
            "Bản thảo 2025 là một mô hình NetLogo với nhiệm vụ riêng; không phải bản thân NetLogo."
        )
        aria = "netlogo nen tang vs herdsim he thong"
        row_h = "Trục thiết kế"
        rows = [
            ("Mục đích", "Bộ công cụ ABM tổng quát", "Thí nghiệm chăn đàn kiểm soát"),
            ("Không gian", "Ô / rùa", "Vị trí liên tục"),
            ("Hàng loạt", "BehaviorSpace / tay", "Experiments + đường ống xác nhận"),
            ("So sánh", "Cửa sổ riêng", "Tab Compare + chỉ số chung"),
        ]

    w, h = 780, 420
    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">',
        rect(0, 0, w, h, BG),
        text(16, 24, title, size=14, weight=700),
        rect(16, 40, 340, 190, "#fff", ORANGE, 2, rx=10),
        rect(424, 40, 340, 190, "#fff", DOG, 2, rx=10),
        text(186, 66, left_h, size=13, weight=700, fill=ORANGE, anchor="middle"),
        text(594, 66, right_h, size=13, weight=700, fill=DOG, anchor="middle"),
    ]
    for i, s in enumerate(left):
        parts.append(text(32, 96 + i * 24, f"- {s}", size=11, fill=INK))
    for i, s in enumerate(right):
        parts.append(text(440, 96 + i * 24, f"- {s}", size=11, fill=INK))
    parts.append(text(390, 120, "<->", size=18, weight=700, fill=MUTED, anchor="middle"))
    parts.append(text(390, 145, mid, size=9, fill=MUTED, anchor="middle"))
    parts.append(text(390, 162, mid2, size=9, fill=MUTED, anchor="middle"))

    # design axes table
    col_w = (130, 280, 300)
    x = 16
    parts.append(rect(x, 250, col_w[0] - 6, 26, DOG, None, 0, rx=4))
    parts.append(text(x + 8, 267, row_h, size=11, weight=700, fill="#fff"))
    x += col_w[0]
    parts.append(rect(x, 250, col_w[1] - 6, 26, ORANGE, None, 0, rx=4))
    parts.append(text(x + 8, 267, left_h if lang == "en" else "NetLogo", size=11, weight=700, fill="#fff"))
    x += col_w[1]
    parts.append(rect(x, 250, col_w[2] - 6, 26, DOG, None, 0, rx=4))
    parts.append(text(x + 8, 267, "HerdSim", size=11, weight=700, fill="#fff"))

    for r_i, row in enumerate(rows):
        y = 282 + r_i * 24
        x = 16
        bg = "#fff" if r_i % 2 == 0 else PANEL
        for cell, cw in zip(row, col_w):
            parts.append(rect(x, y, cw - 6, 22, bg, STROKE, 1, rx=3))
            parts.append(text(x + 6, y + 15, cell, size=10, fill=INK))
            x += cw

    parts.append(text(16, h - 14, foot, size=11, fill=MUTED))
    parts.append("</svg>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# S25: phase roadmap (claim done vs remaining; no invented results)
# ---------------------------------------------------------------------------

def phase_roadmap(lang: str) -> str:
    if lang == "en":
        title = "Phase roadmap: claim-grade done vs remaining"
        legend = [
            (GREEN, "Claim done"),
            (ORANGE, "Skipped"),
            (PURPLE, "Analysed (weak)"),
            (MUTED, "Not run"),
        ]
        phases = [
            ("1", "Size", "Claim", GREEN),
            ("2", "Structure", "Claim", GREEN),
            ("3", "Mechanism", "Skipped", ORANGE),
            ("4", "Transfer", "Claim", GREEN),
            ("5", "Information", "Not run", MUTED),
            ("6", "Fits", "Weak", PURPLE),
            ("7", "Early warn", "Not run", MUTED),
        ]
        rem_h = "Remaining phases (planned question only; no invented numbers)"
        rem_rows = [
            ("3", "SKIPPED", "Efficient vs overcrowding on I_dir / fragmentation", "No result: 0 overcrowding cells"),
            ("5", "NOT RUN", "Obs / range / comm: does one step lower D_min?", "No scout/claim folder yet"),
            ("6", "WEAK", "Leave-one-N-out fits; C6b slope band open", "Package F / Fig 8 here; not a real law"),
            ("7", "NOT RUN", "Held-out state AUROC and lead time on failures", "Package G not run"),
        ]
        cols = ("Phase", "Status", "Planned question", "Result here?")
        foot = "Green boxes are claim-grade in this report. Grey and amber show status only; they do not invent R or D_min."
        aria = "phase roadmap"
    else:
        title = "Lộ trình giai đoạn: đã xác nhận so với còn lại"
        legend = [
            (GREEN, "Đã xác nhận"),
            (ORANGE, "Bỏ qua"),
            (PURPLE, "Đã phân tích (yếu)"),
            (MUTED, "Chưa chạy"),
        ]
        phases = [
            ("1", "Kích thước", "Xác nhận", GREEN),
            ("2", "Cấu trúc", "Xác nhận", GREEN),
            ("3", "Cơ chế", "Bỏ qua", ORANGE),
            ("4", "Chuyển giao", "Xác nhận", GREEN),
            ("5", "Thông tin", "Chưa chạy", MUTED),
            ("6", "Khớp tỷ lệ", "Yếu", PURPLE),
            ("7", "Cảnh báo sớm", "Chưa chạy", MUTED),
        ]
        rem_h = "Giai đoạn còn lại (chỉ câu hỏi dự kiến; không bịa số)"
        rem_rows = [
            ("3", "BỎ QUA", "Ô hiệu quả vs quá tải trên I_dir / phân mảnh", "Không kết quả: 0 ô quá tải cơ sở"),
            ("5", "CHƯA CHẠY", "Obs / tầm / giao tiếp: một bước có hạ D_min?", "Chưa có thư mục dò đường/xác nhận"),
            ("6", "YẾU", "Khớp leave-one-N-out; C6b dải độ dốc còn mở", "Gói F / Hình 8 đã có; không phải luật thật"),
            ("7", "CHƯA CHẠY", "AUROC trạng thái và thời gian báo trước khi thất bại", "Gói G chưa chạy"),
        ]
        cols = ("Giai đoạn", "Trạng thái", "Câu hỏi dự kiến", "Có kết quả ở đây?")
        foot = "Ô xanh là mức xác nhận trong báo cáo này. Xám và cam chỉ trạng thái; không bịa R hay D_min."
        aria = "lo trinh giai doan"

    w, h = 780, 430
    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">',
        rect(0, 0, w, h, BG),
        text(16, 24, title, size=14, weight=700),
    ]
    # legend
    lx = 16
    for fill, lab in legend:
        parts.append(rect(lx, 36, 14, 14, fill if fill != MUTED else "#fff", fill, 2, rx=2))
        parts.append(text(lx + 20, 48, lab, size=11, fill=MUTED))
        lx += 150

    # phase strip
    box_w, box_h = 100, 88
    gap = 8
    x0 = 16
    y0 = 64
    for i, (num, name, status, color) in enumerate(phases):
        x = x0 + i * (box_w + gap)
        parts.append(rect(x, y0, box_w, box_h, "#fff", color, 2, rx=8))
        parts.append(rect(x + 6, y0 + 6, box_w - 12, 4, color, None, 0, rx=2))
        parts.append(text(x + box_w / 2, y0 + 32, num, size=20, weight=800, fill=color, anchor="middle"))
        parts.append(text(x + box_w / 2, y0 + 50, name, size=11, weight=700, fill=INK, anchor="middle"))
        parts.append(text(x + box_w / 2, y0 + 68, status, size=10, fill=MUTED, anchor="middle"))

    # remaining detail table
    parts.append(text(16, 174, rem_h, size=12, weight=700, fill=DOG))
    col_w = (50, 120, 340, 230)
    x = 16
    for hdr, cw in zip(cols, col_w):
        parts.append(rect(x, 188, cw - 6, 28, DOG, None, 0, rx=4))
        parts.append(text(x + 8, 206, hdr, size=11, weight=700, fill="#fff"))
        x += cw
    for r_i, row in enumerate(rem_rows):
        y = 222 + r_i * 36
        x = 16
        bg = "#fff" if r_i % 2 == 0 else PANEL
        for cell, cw in zip(row, col_w):
            parts.append(rect(x, y, cw - 6, 32, bg, STROKE, 1, rx=4))
            parts.append(text(x + 8, y + 21, cell, size=10, fill=INK))
            x += cw

    parts.append(text(16, h - 14, foot, size=11, fill=MUTED))
    parts.append("</svg>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# S26: draft experiment design (grid + budget + vs HerdSim)
# ---------------------------------------------------------------------------

def draft_experiment_design(lang: str) -> str:
    draft_n = [5, 10, 25, 50, 100, 150, 200, 250, 300, 350, 400]
    draft_d = [1, 2, 3, 4, 6, 10, 15, 20, 25, 35]
    draft_only_n = {250, 350}

    if lang == "en":
        title = "2025 draft experiment design: flat N x D grid"
        n_h = "N grid (11 sizes; has 250, 350; no 75)"
        d_h = "D grid (10 counts; same as HerdSim)"
        n_note = "Amber chips are draft-only (250, 350). HerdSim-only 75 is not on this row."
        grid_note = "10 D x 11 N = 110 conditions  |  D shared with HerdSim"
        cards = [
            (ORANGE, "100", "runs / cell", "Flat: no scout / claim split"),
            (DOG, "11,000", "simulations", "110 x 100"),
            (GREEN, "SR >= 90%", "reliability bar", "Defines [Dmin, Dmax]"),
            (PURPLE, "No", "bootstrap on Dmin", "Spearman on 110 aggregates"),
        ]
        cmp_h = "Design contrast (not results)"
        cmp_cols = ("Piece", "Draft 2025", "HerdSim here")
        cmp_rows = [
            ("Sampling", "100 flat every cell", "Scout 30; claim 100 on window"),
            ("D_min uncertainty", "None", "Bootstrap (1,000 resamples)"),
            ("N grid", "Has 250, 350; no 75", "Has 75; no 250, 350"),
            ("D grid", "Same 10 levels", "Same 10 levels"),
            ("Statistics", "Spearman; no binomial CI", "Frontiers + regimes + packages"),
        ]
        foot = "Draft numbers only describe its protocol. HerdSim claim counts are separate (Table 2)."
        aria = "draft experiment design"
    else:
        title = "Thiết kế thí nghiệm bản thảo 2025: lưới N x D đều"
        n_h = "Lưới N (11 kích thước; có 250, 350; không 75)"
        d_h = "Lưới D (10 mức; giống HerdSim)"
        n_note = "Chip cam chỉ bản thảo (250, 350). HerdSim-only 75 không có trên hàng này."
        grid_note = "10 D x 11 N = 110 điều kiện  |  D chung với HerdSim"
        cards = [
            (ORANGE, "100", "lượt / ô", "Đều: không dò đường / xác nhận"),
            (DOG, "11,000", "mô phỏng", "110 x 100"),
            (GREEN, "SR >= 90%", "ngưỡng tin cậy", "Định nghĩa [Dmin, Dmax]"),
            (PURPLE, "Không", "bootstrap Dmin", "Spearman trên 110 ô tổng hợp"),
        ]
        cmp_h = "Đối chiếu thiết kế (không phải kết quả)"
        cmp_cols = ("Phần", "Bản thảo 2025", "HerdSim ở đây")
        cmp_rows = [
            ("Mẫu thử", "100 đều mọi ô", "Dò đường 30; xác nhận 100 cửa sổ"),
            ("Độ bất định D_min", "Không có", "Bootstrap (1,000 lần lấy mẫu)"),
            ("Lưới N", "Có 250, 350; không 75", "Có 75; không 250, 350"),
            ("Lưới D", "Cùng 10 mức", "Cùng 10 mức"),
            ("Thống kê", "Spearman; không CI nhị thức", "Biên + trạng thái + gói"),
        ]
        foot = "Số bản thảo chỉ mô tả giao thức của nó. Số xác nhận HerdSim riêng (Bảng 2)."
        aria = "thiet ke thi nghiem ban thao"

    w, h = 780, 470
    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">',
        rect(0, 0, w, h, BG),
        text(16, 24, title, size=14, weight=700),
        text(16, 48, n_h, size=12, weight=700, fill=DOG),
    ]

    chip_w, chip_h = 62, 32
    x0, y0 = 16, 58
    for i, n in enumerate(draft_n):
        x = x0 + i * (chip_w + 4)
        hot = n in draft_only_n
        fill = "#fde68a" if hot else "#fff"
        stroke = ORANGE if hot else DOG
        parts.append(rect(x, y0, chip_w, chip_h, fill, stroke, 1.5 if hot else 1, rx=6))
        parts.append(text(x + chip_w / 2, y0 + 21, str(n), size=12, weight=700, fill=DOG, anchor="middle"))
    parts.append(text(16, 108, n_note, size=10, fill=MUTED))

    parts.append(text(16, 132, d_h, size=12, weight=700, fill=GREEN))
    for i, d in enumerate(draft_d):
        x = x0 + i * (chip_w + 4)
        parts.append(rect(x, 142, chip_w, chip_h, "#fff", GREEN, 1, rx=6))
        parts.append(text(x + chip_w / 2, 163, str(d), size=12, weight=700, fill=GREEN, anchor="middle"))
    parts.append(text(16, 192, grid_note, size=11, weight=700, fill=INK))

    card_w = 180
    for i, (color, big, mid, small) in enumerate(cards):
        x = 16 + i * (card_w + 10)
        parts.append(rect(x, 208, card_w, 78, "#fff", color, 2, rx=8))
        parts.append(text(x + 12, 232, big, size=18, weight=800, fill=color))
        parts.append(text(x + 12, 252, mid, size=12, weight=700, fill=INK))
        parts.append(text(x + 12, 272, small, size=10, fill=MUTED))

    parts.append(text(16, 310, cmp_h, size=12, weight=700, fill=DOG))
    col_w = (140, 280, 300)
    x = 16
    for hdr, cw in zip(cmp_cols, col_w):
        parts.append(rect(x, 320, cw - 6, 26, DOG, None, 0, rx=4))
        parts.append(text(x + 8, 337, hdr, size=11, weight=700, fill="#fff"))
        x += cw
    for r_i, row in enumerate(cmp_rows):
        y = 352 + r_i * 20
        x = 16
        bg = "#fff" if r_i % 2 == 0 else PANEL
        for cell, cw in zip(row, col_w):
            parts.append(rect(x, y, cw - 6, 18, bg, STROKE, 1, rx=2))
            parts.append(text(x + 6, y + 13, cell, size=10, fill=INK))
            x += cw

    parts.append(text(16, h - 12, foot, size=11, fill=MUTED))
    parts.append("</svg>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# S27: draft main results (from paper note / Table A3)
# ---------------------------------------------------------------------------

def draft_main_results(lang: str) -> str:
    # Dmin from draft Table A3 (documented in sheep-scaling_paper2025.md)
    dmin_pairs = [
        (5, 1), (10, 1), (25, 1), (50, 1), (100, 1),
        (150, 3), (200, 20), (250, 25), (300, 20), (350, 35), (400, 35),
    ]
    if lang == "en":
        title = "2025 draft main results (from the paper; not re-run here)"
        cards = [
            (GREEN, "D=1 OK", "to N = 100", "Then collapse at N=150 (SR ~1%)"),
            (ORANGE, "Dmin rises", "with N", "3 / ~20 / 35 at N=150 / 200 / 400"),
            (RED, "Overcrowd", "e.g. N=10", "D >= 20 worse than fewer dogs"),
            (PURPLE, "3,089", "failures", "90% stall in Collect phase"),
        ]
        chart_h = "Dmin(N) at SR >= 90% (draft Table A3)"
        cost_h = "Cost trends (successful runs)"
        cost_lines = [
            "Mean ticks to success rise with N, fall with D",
            "Total dog path rises with D; saturates near breakpoints",
        ]
        foot = "Numbers are draft-reported. Full [Dmin, Dmax] also in Table 3 later for side-by-side with HerdSim."
        aria = "draft main results"
        y_lab = "Dmin"
    else:
        title = "Kết quả chính bản thảo 2025 (từ bài; không chạy lại ở đây)"
        cards = [
            (GREEN, "D=1 ổn", "đến N = 100", "Rồi sụp ở N=150 (SR ~1%)"),
            (ORANGE, "Dmin tăng", "theo N", "3 / ~20 / 35 tại N=150 / 200 / 400"),
            (RED, "Quá tải", "vd N=10", "D >= 20 tệ hơn ít chó"),
            (PURPLE, "3,089", "thất bại", "90% dừng ở pha Gom"),
        ]
        chart_h = "Dmin(N) tại SR >= 90% (Bảng A3 bản thảo)"
        cost_h = "Xu hướng chi phí (lượt thành công)"
        cost_lines = [
            "Thời gian trung bình tăng theo N, giảm theo D",
            "Tổng quãng đường chó tăng theo D; bão hòa gần điểm gãy",
        ]
        foot = "Số liệu theo bản thảo. [Dmin, Dmax] đầy đủ cũng ở Bảng 3 sau để so cạnh HerdSim."
        aria = "ket qua chinh ban thao"
        y_lab = "Dmin"

    w, h = 780, 400
    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">',
        rect(0, 0, w, h, BG),
        text(16, 24, title, size=14, weight=700),
    ]
    card_w = 180
    for i, (color, big, mid, small) in enumerate(cards):
        x = 16 + i * (card_w + 10)
        parts.append(rect(x, 40, card_w, 78, "#fff", color, 2, rx=8))
        parts.append(text(x + 12, 64, big, size=16, weight=800, fill=color))
        parts.append(text(x + 12, 84, mid, size=12, weight=700, fill=INK))
        parts.append(text(x + 12, 104, small, size=10, fill=MUTED))

    parts.append(text(16, 144, chart_h, size=12, weight=700, fill=DOG))
    # bar chart: max Dmin 35
    chart_x, chart_y, chart_w, chart_hh = 50, 160, 700, 140
    parts.append(rect(chart_x, chart_y, chart_w, chart_hh, "#fff", STROKE, 1, rx=6))
    parts.append(text(28, chart_y + 70, y_lab, size=10, fill=MUTED, anchor="middle"))
    max_d = 35.0
    bar_gap = 8
    bar_w = (chart_w - 40) / len(dmin_pairs) - bar_gap
    base = chart_y + chart_hh - 24
    for i, (n, dmin) in enumerate(dmin_pairs):
        x = chart_x + 20 + i * (bar_w + bar_gap)
        bh = (dmin / max_d) * (chart_hh - 50)
        y = base - bh
        hot = dmin >= 20
        fill = ORANGE if hot else "#93c5fd"
        stroke = RED if dmin >= 35 else (ORANGE if hot else DOG)
        parts.append(rect(x, y, bar_w, bh, fill, stroke, 1, rx=3))
        parts.append(text(x + bar_w / 2, y - 6, str(dmin), size=10, weight=700, fill=INK, anchor="middle"))
        parts.append(text(x + bar_w / 2, base + 14, str(n), size=10, fill=MUTED, anchor="middle"))
    parts.append(text(chart_x + chart_w / 2, chart_y + chart_hh - 4, "N", size=10, fill=MUTED, anchor="middle"))

    parts.append(text(16, 330, cost_h, size=12, weight=700, fill=GREEN))
    for i, line in enumerate(cost_lines):
        parts.append(text(16, 352 + i * 18, f"- {line}", size=12, fill=INK))
    parts.append(text(16, h - 12, foot, size=11, fill=MUTED))
    parts.append("</svg>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# S28: draft extra analyses
# ---------------------------------------------------------------------------

def draft_extra_analyses(lang: str) -> str:
    if lang == "en":
        title = "2025 draft extra analyses (paper Tables VIII to X)"
        rho_h = "Spread vs success (Spearman over 110 cells)"
        rho_rows = [
            ("S_bar vs SR", -0.701, "Strong negative"),
            ("S_bar * N vs SR", -0.828, "Best composite"),
            ("S_bar * sqrt(N)", -0.819, "Close second"),
        ]
        fail_h = "Failures by control (Table VIII idea)"
        fail_rows = [
            ("S_bar > 25 (no control)", "2,161", "Collect 97%"),
            ("S_bar <= 25 (some control)", "928", "Collect 74%; hold 9%; exit 18%"),
            ("All failures", "3,089", "Collect 90%"),
        ]
        sens_h = "Sensitivity: lower sheep Rrep 3.0 to 2.5 (Table IX)"
        sens = [
            ("D=6, N=400", "0%", "92%"),
            ("D=3, N=250", "5%", "100%"),
        ]
        grad_h = "Density gradient vs true GCM (RQ3; ~80M obs; Table X)"
        grad = [
            "N >= 100: mean angular error ~18 to 22 deg",
            "Correct sector often >= 65%; correct or adjacent >= 87%",
            "Worse at very small or very large N (sparse / vision limits)",
        ]
        foot = "These are draft findings. HerdSim did not re-run these NetLogo analyses."
        aria = "draft extra analyses"
        before = "Before"
        after = "After"
    else:
        title = "Phân tích thêm bản thảo 2025 (Bảng VIII đến X)"
        rho_h = "Độ trải so với thành công (Spearman trên 110 ô)"
        rho_rows = [
            ("S_bar vs SR", -0.701, "Âm mạnh"),
            ("S_bar * N vs SR", -0.828, "Tổ hợp tốt nhất"),
            ("S_bar * sqrt(N)", -0.819, "Gần nhất nhì"),
        ]
        fail_h = "Thất bại theo mức kiểm soát (ý Bảng VIII)"
        fail_rows = [
            ("S_bar > 25 (mất kiểm soát)", "2,161", "Gom 97%"),
            ("S_bar <= 25 (còn kiểm soát)", "928", "Gom 74%; giữ 9%; thoát 18%"),
            ("Mọi thất bại", "3,089", "Gom 90%"),
        ]
        sens_h = "Độ nhạy: giảm Rrep cừu 3.0 xuống 2.5 (Bảng IX)"
        sens = [
            ("D=6, N=400", "0%", "92%"),
            ("D=3, N=250", "5%", "100%"),
        ]
        grad_h = "Gradient mật độ so với GCM thật (RQ3; ~80 triệu qs; Bảng X)"
        grad = [
            "N >= 100: sai góc trung bình ~18 đến 22 độ",
            "Đúng sector thường >= 65%; đúng hoặc kề >= 87%",
            "Tệ hơn ở N rất nhỏ hoặc rất lớn (thưa / giới hạn tầm nhìn)",
        ]
        foot = "Đây là phát hiện bản thảo. HerdSim không chạy lại các phân tích NetLogo này."
        aria = "phan tich them ban thao"
        before = "Trước"
        after = "Sau"

    w, h = 780, 430
    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">',
        rect(0, 0, w, h, BG),
        text(16, 24, title, size=14, weight=700),
        text(16, 48, rho_h, size=12, weight=700, fill=DOG),
    ]
    # rho bars (magnitude)
    for i, (name, rho, gloss) in enumerate(rho_rows):
        y = 58 + i * 36
        mag = abs(rho)
        bw = mag * 280
        parts.append(text(16, y + 16, name, size=11, fill=INK))
        parts.append(rect(200, y + 4, 280, 20, PANEL, STROKE, 1, rx=4))
        parts.append(rect(200 + (280 - bw), y + 4, bw, 20, "#fca5a5", RED, 1, rx=4))
        parts.append(text(500, y + 18, f"rho = {rho}", size=11, weight=700, fill=RED))
        parts.append(text(600, y + 18, gloss, size=11, fill=MUTED))

    parts.append(text(16, 175, fail_h, size=12, weight=700, fill=PURPLE))
    col_w = (260, 90, 280)
    x = 16
    headers = (
        ("Slice", "Count", "Mostly stall in")
        if lang == "en"
        else ("Lát cắt", "Số", "Phần lớn dừng ở")
    )
    for hdr, cw in zip(headers, col_w):
        parts.append(rect(x, 186, cw - 6, 24, PURPLE, None, 0, rx=4))
        parts.append(text(x + 8, 202, hdr, size=11, weight=700, fill="#fff"))
        x += cw
    for r_i, row in enumerate(fail_rows):
        y = 214 + r_i * 24
        x = 16
        bg = "#fff" if r_i % 2 == 0 else PANEL
        for cell, cw in zip(row, col_w):
            parts.append(rect(x, y, cw - 6, 22, bg, STROKE, 1, rx=3))
            parts.append(text(x + 6, y + 15, cell, size=10, fill=INK))
            x += cw

    parts.append(text(16, 300, sens_h, size=12, weight=700, fill=ORANGE))
    parts.append(text(16, 322, f"Cell          {before}     {after}", size=11, weight=700, fill=MUTED))
    for i, (cell, b, a) in enumerate(sens):
        y = 340 + i * 22
        parts.append(text(16, y, cell, size=12, fill=INK))
        parts.append(text(160, y, b, size=12, weight=700, fill=RED))
        parts.append(text(230, y, "->", size=12, fill=MUTED))
        parts.append(text(260, y, a, size=12, weight=700, fill=GREEN))

    parts.append(text(400, 300, grad_h, size=12, weight=700, fill=GREEN))
    for i, line in enumerate(grad):
        parts.append(text(400, 322 + i * 20, f"- {line}", size=11, fill=INK))

    parts.append(text(16, h - 12, foot, size=11, fill=MUTED))
    parts.append("</svg>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# S29: five claim-grade discoveries from HerdSim runs
# ---------------------------------------------------------------------------

def herdsim_discoveries(lang: str) -> str:
    if lang == "en":
        title = "What the HerdSim claim runs add (beyond one-controller demos)"
        foot = "Numbers from Phases 1, 2, and 4 only. Full write-ups: sections 8 to 10."
        aria = "herdsim discoveries"
        cards = [
            # (color, phase, big, title, gloss1, gloss2, evidence)
            (ORANGE, "Phase 1", "88%", "Extra dogs mostly waste",
             "Time flat ~183 ticks", "~146 path / dog on compact",
             "Fig 2; regimes 88/10/2"),
            (PURPLE, "Phase 2", "Cost", "Structure hits cost first",
             "Wide / outlier_rich inflate", "ticks and path; D_min still 1",
             "Phase 2 cost tables"),
            (GREEN, "Phase 4", "Mixed", "Transfer is method-specific",
             "Kubo shares compact D_min", "FAT does not scale",
             "Phase 4 transfer counts"),
            (RED, "Phase 1", "N=5,10", "Tiny flocks fail differently",
             "Oscillation / stuck at D=1", "Fixed when D=2 (R to 1.00)",
             "Phase 1 failure labels"),
            (DOG, "Phase 1", "Width 0", "D_min can be certain",
             "Bootstrap interval width 0", "on every baseline D_min",
             "dmin_bootstrap.csv"),
        ]
    else:
        title = "HerdSim đo thêm gì (so với demo một bộ điều khiển)"
        foot = "Số liệu chỉ từ Giai đoạn 1, 2 và 4. Viết đủ: mục 8 đến 10."
        aria = "phat hien herdsim"
        cards = [
            (ORANGE, "Giai đoạn 1", "88%", "Thêm chó phần lớn lãng phí",
             "Thời gian phẳng ~183 bước", "~146 đường / chó (tập trung)",
             "Hình 2; trạng thái 88/10/2"),
            (PURPLE, "Giai đoạn 2", "Chi phí", "Cấu trúc đánh chi phí trước",
             "Phân tán / cá thể lạc phình", "thời gian và đường; D_min vẫn 1",
             "Bảng chi phí Giai đoạn 2"),
            (GREEN, "Giai đoạn 4", "Lẫn", "Chuyển giao phụ thuộc phương pháp",
             "Kubo chia sẻ D_min tập trung", "FAT không tỷ lệ",
             "Số chuyển giao Giai đoạn 4"),
            (RED, "Giai đoạn 1", "N=5,10", "Đàn rất nhỏ thất bại khác",
             "Dao động / kẹt tại D=1", "Hết khi D=2 (R lên 1.00)",
             "Nhãn thất bại Giai đoạn 1"),
            (DOG, "Giai đoạn 1", "Rộng 0", "D_min có thể chắc chắn",
             "Khoảng bootstrap độ rộng 0", "mọi D_min cơ sở",
             "dmin_bootstrap.csv"),
        ]

    w, h = 780, 430
    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">',
        rect(0, 0, w, h, BG),
        text(16, 26, title, size=14, weight=700),
    ]

    # row 1: three cards; row 2: two cards centered
    positions = [
        (16, 44), (270, 44), (524, 44),
        (140, 220), (400, 220),
    ]
    cw, ch = 240, 160
    for (x, y), (color, phase, big, title_c, g1, g2, ev) in zip(positions, cards):
        parts.append(rect(x, y, cw, ch, "#fff", color, 2, rx=10))
        badge_w = 98 if lang == "vi" else 72
        parts.append(rect(x + 12, y + 12, badge_w, 20, color, None, 0, rx=4))
        parts.append(text(x + 18, y + 26, phase, size=10, weight=700, fill="#fff"))
        parts.append(text(x + 14, y + 62, big, size=28, weight=800, fill=INK))
        title_size = 11 if len(title_c) > 28 else 12
        parts.append(text(x + 14, y + 88, title_c, size=title_size, weight=700, fill=color))
        parts.append(text(x + 14, y + 110, g1, size=11, fill=MUTED))
        parts.append(text(x + 14, y + 128, g2, size=11, fill=MUTED))
        parts.append(text(x + 14, y + 148, ev, size=10, weight=700, fill=DOG))

    parts.append(text(16, h - 12, foot, size=11, fill=MUTED))
    parts.append("</svg>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# S30: why trust HerdSim vs NetLogo / similar tools
# ---------------------------------------------------------------------------

def trust_herdsim(lang: str) -> str:
    if lang == "en":
        title = "Why HerdSim results can be trusted (without being NetLogo)"
        foot = (
            "Trust is layered evidence, not 'same IDE as everyone else'. "
            "All claim numbers still come from HerdSim CSVs."
        )
        aria = "trust herdsim"
        rungs = [
            (DOG, "1", "Published lineage",
             "Controllers reuse Strombom /",
             "Kubo ideas with fidelity notes",
             "Not invented from scratch"),
            (GREEN, "2", "NetLogo twins",
             "Desktop twins for shared",
             "methods: behaviour check",
             "Not tick-for-tick replay"),
            (ORANGE, "3", "Frozen protocol",
             "scaling_v2, seeds, scout/claim,",
             "bootstrap, open claim CSVs",
             "Reproducible claim path"),
            (RED, "4", "Honest limits",
             "No quantitative twin parity",
             "table yet; FAT has no twin;",
             "draft model is not a twin"),
        ]
    else:
        title = "Tại sao tin kết quả HerdSim (mà không cần là NetLogo)"
        foot = (
            "Tin cậy là bằng chứng xếp lớp, không phải 'cùng IDE với mọi người'. "
            "Mọi số kết luận vẫn từ CSV HerdSim."
        )
        aria = "tin cay herdsim"
        rungs = [
            (DOG, "1", "Thuật toán công bố",
             "Bộ điều khiển tái dùng ý",
             "Strombom / Kubo + ghi chú fidelity",
             "Không invent từ đầu"),
            (GREEN, "2", "Twin NetLogo",
             "Twin máy tính cho phương pháp",
             "chung: kiểm hành vi",
             "Không phát lại từng bước"),
            (ORANGE, "3", "Giao thức đóng băng",
             "scaling_v2, hạt giống, dò/xác nhận,",
             "bootstrap, CSV mở",
             "Đường kết luận tái lập được"),
            (RED, "4", "Giới hạn nói thẳng",
             "Chưa bảng parity định lượng;",
             "FAT không twin; bản thảo",
             "không phải twin"),
        ]

    w, h = 780, 280
    parts = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(aria)}">',
        rect(0, 0, w, h, BG),
        text(16, 26, title, size=14, weight=700),
    ]

    cw, ch = 176, 188
    gap = 12
    x0 = 16
    for i, (color, num, head, l1, l2, l3) in enumerate(rungs):
        x = x0 + i * (cw + gap)
        y = 44
        parts.append(rect(x, y, cw, ch, "#fff", color, 2, rx=10))
        parts.append(circle(x + 22, y + 24, 14, color))
        parts.append(text(x + 22, y + 29, num, size=13, weight=800, fill="#fff", anchor="middle"))
        parts.append(text(x + 44, y + 30, head, size=11, weight=700, fill=color))
        parts.append(text(x + 14, y + 70, l1, size=11, fill=INK))
        parts.append(text(x + 14, y + 90, l2, size=11, fill=INK))
        parts.append(text(x + 14, y + 118, l3, size=11, weight=700, fill=MUTED))
        if i < 3:
            ax = x + cw + 2
            parts.append(line(ax, y + ch / 2, ax + gap - 4, y + ch / 2, stroke=STROKE, sw=2))

    parts.append(text(16, h - 14, foot, size=11, fill=MUTED))
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    for lang in ("en", "vi"):
        d = OUT / lang
        write(d / "design_nd_grids.svg", nd_grids(lang))
        write(d / "design_frontier.svg", frontier_defs(lang))
        write(d / "design_timeout.svg", timeout_drive(lang))
        write(d / "design_failures.svg", failure_labels(lang))
        write(d / "draft_vs_herdsim.svg", draft_vs_herdsim(lang))
        write(d / "design_theta.svg", theta_bar(lang))
        write(d / "design_bootstrap.svg", bootstrap_dmin(lang))
        write(d / "field_map.svg", field_map(lang))
        write(d / "netlogo_vs_herdsim.svg", netlogo_vs_herdsim(lang))
        write(d / "phase_roadmap.svg", phase_roadmap(lang))
        write(d / "draft_experiment_design.svg", draft_experiment_design(lang))
        write(d / "draft_main_results.svg", draft_main_results(lang))
        write(d / "draft_extra_analyses.svg", draft_extra_analyses(lang))
        write(d / "herdsim_discoveries.svg", herdsim_discoveries(lang))
        write(d / "trust_herdsim.svg", trust_herdsim(lang))


if __name__ == "__main__":
    main()
