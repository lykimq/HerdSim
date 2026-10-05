#!/usr/bin/env python3
"""Rebuild SUMMARY_REPORT.html and SUMMARY_REPORT_vi.html from markdown with embedded figures."""

from __future__ import annotations

import base64
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MIME = {".png": "image/png", ".svg": "image/svg+xml", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}

CSS = """
:root{--ink:#111827;--mut:#6b7280;--line:#e5e7eb;--acc:#2563eb;--bg:#f9fafb}
*{box-sizing:border-box}body{margin:0;font:16px/1.65 -apple-system,'Segoe UI',Inter,Roboto,sans-serif;color:var(--ink);background:var(--bg)}
header{background:linear-gradient(120deg,#1e3a8a,#0f766e);color:#fff;padding:48px 24px}
header .in,main{max-width:1000px;margin:auto}header h1{margin:0 0 8px;font-size:2rem}header p{margin:0;opacity:.9;max-width:46rem}
.layout{display:grid;grid-template-columns:230px 1fr;gap:32px;max-width:1280px;margin:0 auto;padding:24px}
nav{position:sticky;top:16px;align-self:start;font-size:.88rem;max-height:calc(100vh - 32px);overflow:auto}
nav a{display:block;padding:5px 10px;color:var(--mut);text-decoration:none;border-left:2px solid var(--line)}
nav a:hover,nav a:focus{color:var(--acc);border-color:var(--acc)}
main{background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px 40px 40px;min-width:0}
h2{margin-top:2.2em;padding-bottom:6px;border-bottom:2px solid var(--line);scroll-margin-top:16px}
h2:first-child{margin-top:1.2em}
h3{margin-top:1.6em;color:#1e3a8a}
code{background:#eef2ff;border-radius:4px;padding:1px 5px;font-size:.88em;word-break:break-word}
a{color:var(--acc)}
figure{margin:24px 0;text-align:center}figure img{max-width:100%;border:1px solid var(--line);border-radius:8px;background:#fff}
figcaption{font-size:.88rem;color:var(--mut);margin-top:6px;text-align:left}
table{border-collapse:collapse;width:100%;font-size:.9rem;margin:8px 0}
.table-wrap{overflow-x:auto;margin:8px 0}
th,td{border:1px solid var(--line);padding:6px 10px;text-align:left;vertical-align:top}
th{background:#f3f4f6}caption{caption-side:bottom;font-size:.85rem;color:var(--mut);padding:6px;text-align:left}
.badge{display:inline-block;padding:2px 9px;border-radius:99px;font-size:.78rem;font-weight:600}
.REJECTED,.BI_BAC_BO,.NOT_REPRODUCED,.KHONG_TAI_HIEN{background:#fee2e2;color:#991b1b}
.SUPPORTED,.DUOC_UNG_HO,.OK,.DUNG,.READY,.SAN_DUNG,.D_MIN_1{background:#dcfce7;color:#166534}
.INCONCLUSIVE,.EVALUATED,.KHONG_RO_RANG,.DA_DANH_GIA,.WEAK,.YEU,.UNVERIFIED,.CHUA_XAC_NHAN,.PARTIAL,.MOT_PHAN,.COST_ONLY,.CHI_CHI_PHI{background:#fef3c7;color:#92400e}
.SKIPPED,.UNEVALUATED,.BO_QUA,.CHUA_DANH_GIA,.NOT_RUN,.CHUA_CHAY,.WASTE,.LANG_PHI{background:#ffedd5;color:#9a3412}
.NEEDS_RUN,.CAN_CHAY,.STALE,.LOI_THOI{background:#ffedd5;color:#9a3412}
.kpi-note{background:#eff6ff;border-left:4px solid #2563eb;padding:10px 14px;margin:12px 0;border-radius:0 8px 8px 0;font-size:.95rem}
ul{padding-left:1.2em}li{margin:6px 0}
footer{max-width:1280px;margin:0 auto 32px;padding:0 24px;color:var(--mut);font-size:.85rem}
@media(max-width:900px){.layout{grid-template-columns:1fr}nav{display:none}main{padding:8px 18px 30px}header{padding:32px 18px}header h1{font-size:1.55rem}}
""".strip()

BADGE_WORDS = {
    "REJECTED", "SUPPORTED", "INCONCLUSIVE", "EVALUATED", "SKIPPED", "UNEVALUATED",
    "OK", "READY", "WEAK", "UNVERIFIED", "NEEDS RUN", "NOT RUN", "STALE",
    "D_min = 1", "Waste", "Not reproduced", "Cost only", "Partial",
    "BỊ BÁC BỎ", "ĐƯỢC ỦNG HỘ", "KHÔNG RÕ RÀNG", "ĐÃ ĐÁNH GIÁ", "BỎ QUA", "CHƯA ĐÁNH GIÁ",
    "ĐÚNG", "SẴN DÙNG", "YẾU", "CHƯA XÁC NHẬN", "CẦN CHẠY", "CHƯA CHẠY", "LỖI THỜI",
    "Lãng phí", "Không tái hiện", "Chỉ chi phí", "Một phần",
}


def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[`*_]", "", s)
    s = re.sub(r"[^a-z0-9àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    # ASCII fold for anchors matching prior HTML somewhat
    trans = str.maketrans(
        "àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ",
        "aaaaaaaaaaaaaaaaaeeeeeeeeeeeiiiiiooooooooooooooooouuuuuuuuuuuyyyyyd",
    )
    return s.translate(trans)


def inline(text: str) -> str:
    """Render a limited Markdown inline subset to HTML."""
    codes: list[str] = []

    def save_code(m: re.Match) -> str:
        codes.append(html.escape(m.group(1)))
        return f"@@CODE{len(codes)-1}@@"

    text = re.sub(r"`([^`]+)`", save_code, text)

    imgs: list[str] = []

    def save_img(m: re.Match) -> str:
        imgs.append(embed_img(m.group(1), m.group(2)))
        return f"@@IMG{len(imgs)-1}@@"

    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", save_img, text)

    links: list[tuple[str, str]] = []

    def save_link(m: re.Match) -> str:
        links.append((m.group(1), m.group(2)))
        return f"@@LINK{len(links)-1}@@"

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", save_link, text)

    bolds: list[str] = []

    def save_bold(m: re.Match) -> str:
        bolds.append(m.group(1))
        return f"@@BOLD{len(bolds)-1}@@"

    text = re.sub(r"\*\*([^*]+)\*\*", save_bold, text)

    italics: list[str] = []

    def save_italic(m: re.Match) -> str:
        italics.append(m.group(1))
        return f"@@ITAL{len(italics)-1}@@"

    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", save_italic, text)

    text = html.escape(text)

    def with_codes(s: str) -> str:
        for i, c in enumerate(codes):
            s = s.replace(f"@@CODE{i}@@", f"<code>{c}</code>")
        return s

    for i, (label, href) in enumerate(links):
        text = text.replace(
            f"@@LINK{i}@@",
            f'<a href="{html.escape(href, quote=True)}">{with_codes(html.escape(label))}</a>',
        )
    for i, b in enumerate(bolds):
        text = text.replace(f"@@BOLD{i}@@", f"<strong>{with_codes(html.escape(b))}</strong>")
    for i, it in enumerate(italics):
        text = text.replace(f"@@ITAL{i}@@", f"<em>{with_codes(html.escape(it))}</em>")
    text = with_codes(text)
    for i, im in enumerate(imgs):
        text = text.replace(f"@@IMG{i}@@", im)
    return text


def embed_img(alt: str, rel: str) -> str:
    path = (ROOT / rel).resolve()
    if not path.exists():
        return f'<p class="missing">[missing figure: {html.escape(rel)}]</p>'
    mime = MIME.get(path.suffix.lower(), "application/octet-stream")
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return (
        f'<figure><img alt="{html.escape(alt)}" src="data:{mime};base64,{data}"/>'
        f"</figure>"
    )


def badgeify(cell: str) -> str:
    raw = cell.strip()
    bare = re.sub(r"^\*\*(.+)\*\*$", r"\1", raw)
    if bare in BADGE_WORDS:
        slug = slugify(bare).replace("-", "_").upper()
        en_exact = {
            "REJECTED", "SUPPORTED", "INCONCLUSIVE", "EVALUATED", "SKIPPED", "UNEVALUATED",
            "OK", "READY", "WEAK", "UNVERIFIED", "STALE",
        }
        if bare in en_exact:
            cls = bare
        elif bare == "NEEDS RUN":
            cls = "NEEDS_RUN"
        elif bare == "NOT RUN":
            cls = "NOT_RUN"
        elif bare == "ĐÚNG":
            cls = "DUNG"
        elif bare == "SẴN DÙNG":
            cls = "SAN_DUNG"
        elif bare == "YẾU":
            cls = "YEU"
        elif bare == "CHƯA XÁC NHẬN":
            cls = "CHUA_XAC_NHAN"
        elif bare == "CẦN CHẠY":
            cls = "CAN_CHAY"
        elif bare == "CHƯA CHẠY":
            cls = "CHUA_CHAY"
        elif bare == "LỖI THỜI":
            cls = "LOI_THOI"
        elif bare == "D_min = 1":
            cls = "D_MIN_1"
        elif bare == "Waste":
            cls = "WASTE"
        elif bare == "Not reproduced":
            cls = "NOT_REPRODUCED"
        elif bare == "Cost only":
            cls = "COST_ONLY"
        elif bare == "Partial":
            cls = "PARTIAL"
        elif bare == "Lãng phí":
            cls = "LANG_PHI"
        elif bare == "Không tái hiện":
            cls = "KHONG_TAI_HIEN"
        elif bare == "Chỉ chi phí":
            cls = "CHI_CHI_PHI"
        elif bare == "Một phần":
            cls = "MOT_PHAN"
        elif "bac_bo" in slug or bare == "BỊ BÁC BỎ":
            cls = "BI_BAC_BO"
        elif "ung_ho" in slug or bare.startswith("ĐƯỢC"):
            cls = "DUOC_UNG_HO"
        elif "ro_rang" in slug or "KHÔNG RÕ" in bare:
            cls = "KHONG_RO_RANG"
        elif "danh_gia" in slug and "CHƯA" in bare:
            cls = "CHUA_DANH_GIA"
        elif "danh_gia" in slug:
            cls = "DA_DANH_GIA"
        elif "bo_qua" in slug:
            cls = "BO_QUA"
        else:
            cls = slug
        return f'<span class="badge {cls}">{html.escape(bare)}</span>'
    return inline(raw)


def parse_table(lines: list[str]) -> str:
    rows = []
    for ln in lines:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 2:
        return ""
    # skip separator
    body_start = 2 if re.match(r"^:?-+:?$", rows[1][0].replace(" ", "")) or set(rows[1][0]) <= set("-: ") else 1
    # better: any cell of row1 is --- pattern
    if all(re.match(r"^:?-+:?$", c.replace(" ", "")) for c in rows[1]):
        body_start = 2
    else:
        body_start = 1

    head = rows[0]
    out = ['<div class="table-wrap"><table>', "<thead><tr>"]
    for c in head:
        out.append(f"<th>{inline(c)}</th>")
    out.append("</tr></thead><tbody>")
    for row in rows[body_start:]:
        out.append("<tr>")
        for i, c in enumerate(row):
            # badge on verdict-like first columns often
            out.append(f"<td>{badgeify(c)}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


def md_to_html(md: str) -> tuple[str, list[tuple[str, str]], str]:
    """Return (body_html, nav_items, title)."""
    lines = md.splitlines()
    title = "HerdSim summary"
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        lines = lines[1:]

    nav: list[tuple[str, str]] = []
    out: list[str] = []
    i = 0
    n = len(lines)
    pending_caption: str | None = None

    def flush_caption():
        nonlocal pending_caption
        if pending_caption is not None and out and out[-1].endswith("</figure>"):
            cap = pending_caption
            # strip leading * and trailing *
            cap = re.sub(r"^\*(.*)\*$", r"\1", cap.strip())
            out[-1] = out[-1][:-len("</figure>")] + f"<figcaption>{inline(cap)}</figcaption></figure>"
            pending_caption = None

    while i < n:
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue

        # ATX headers
        hm = re.match(r"^(#{2,3})\s+(.*)$", ln)
        if hm:
            flush_caption()
            level = len(hm.group(1))
            text = hm.group(2).strip()
            sid = slugify(text)
            if level == 2:
                nav.append((sid, text))
            out.append(f'<h{level} id="{sid}">{inline(text)}</h{level}>')
            i += 1
            continue

        # skip H1 if any remaining
        if ln.startswith("# "):
            i += 1
            continue

        # table
        if "|" in ln and i + 1 < n and re.search(r"\|?\s*:?-{3,}", lines[i + 1]):
            flush_caption()
            block = [ln]
            i += 1
            while i < n and "|" in lines[i] and lines[i].strip():
                block.append(lines[i])
                i += 1
            out.append(parse_table(block))
            continue

        # image alone
        im = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", ln.strip())
        if im:
            flush_caption()
            out.append(embed_img(im.group(1), im.group(2)))
            # peek caption italic line
            if i + 1 < n and re.match(r"^\*.*\*\s*$", lines[i + 1].strip()):
                pending_caption = lines[i + 1].strip()
                i += 2
                flush_caption()
                continue
            i += 1
            continue

        # unordered list
        if re.match(r"^[-*]\s+", ln):
            flush_caption()
            out.append("<ul>")
            while i < n and re.match(r"^[-*]\s+", lines[i]):
                item = re.sub(r"^[-*]\s+", "", lines[i])
                out.append(f"<li>{inline(item)}</li>")
                i += 1
            out.append("</ul>")
            continue

        # ordered list
        if re.match(r"^\d+\.\s+", ln):
            flush_caption()
            out.append("<ol>")
            while i < n and re.match(r"^\d+\.\s+", lines[i]):
                item = re.sub(r"^\d+\.\s+", "", lines[i])
                out.append(f"<li>{inline(item)}</li>")
                i += 1
            out.append("</ol>")
            continue

        # paragraph (merge consecutive non-blank non-special)
        flush_caption()
        para = [ln]
        i += 1
        while i < n and lines[i].strip() and not re.match(r"^(#{1,3}\s+|[-*]\s+|\d+\.\s+|!\[|\|)", lines[i]):
            # stop before table separator-looking? keep simple
            if lines[i].startswith("|") and i + 1 < n and re.search(r"-{3,}", lines[i + 1]):
                break
            para.append(lines[i])
            i += 1
        text = " ".join(p.strip() for p in para)
        # italic-only caption already handled; if leftover italic line after figure missed:
        if re.match(r"^\*.*\*$", text) and out and "</figure>" in out[-1]:
            pending_caption = text
            flush_caption()
        else:
            out.append(f"<p>{inline(text)}</p>")

    flush_caption()
    return "\n".join(out), nav, title


def wrap(lang: str, title: str, subtitle: str, body: str, nav: list[tuple[str, str]]) -> str:
    nav_html = "".join(f'<a href="#{sid}">{html.escape(label)}</a>' for sid, label in nav)
    return f"""<!doctype html>
<html lang='{lang}'>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{html.escape(title)}</title>
<meta name='description' content='{html.escape(subtitle)}'>
<style>
{CSS}
</style>
</head>
<body>
<header><div class='in'><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div></header>
<div class='layout'>
<nav>{nav_html}</nav>
<main>
{body}
</main>
</div>
<footer><p>Generated from markdown with embedded figures. Paths in the report are relative to <code>scaling/results/summary/</code>.</p></footer>
</body>
</html>
"""


def build(md_name: str, html_name: str, lang: str, subtitle: str) -> None:
    md = (ROOT / md_name).read_text(encoding="utf-8")
    body, nav, title = md_to_html(md)
    # drop leading H1 duplicate: body may still have first paragraph from title line handled
    html_doc = wrap(lang, title, subtitle, body, nav)
    out = ROOT / html_name
    out.write_text(html_doc, encoding="utf-8")
    n_fig = html_doc.count("<figure>")
    print(f"wrote {out} ({out.stat().st_size/1e6:.2f} MB, {n_fig} figures)")


def main() -> None:
    build(
        "SUMMARY_REPORT.md",
        "SUMMARY_REPORT.html",
        "en",
        "HerdSim scaling_v2: claim-grade summary of Phases 1 (size), 2 (structure) and 4 (transfer).",
    )
    build(
        "SUMMARY_REPORT_vi.md",
        "SUMMARY_REPORT_vi.html",
        "vi",
        "HerdSim scaling_v2: tóm tắt mức xác nhận Giai đoạn 1 (kích thước), 2 (cấu trúc) và 4 (chuyển giao).",
    )


if __name__ == "__main__":
    main()
