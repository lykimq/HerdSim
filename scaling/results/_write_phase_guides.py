#!/usr/bin/env python3
"""Write flattened phase guides: REPORT_en.html + REPORT_vi.html under each guides/."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent

CSS = """
:root{--ink:#111827;--mut:#6b7280;--line:#e5e7eb;--acc:#2563eb;--bg:#f9fafb;--card:#fff;
      --ok:#166534;--bad:#991b1b;--warn:#92400e;--plan:#5b4a2f;--result:#1e3a8a}
*{box-sizing:border-box}
body{margin:0;font:16px/1.65 -apple-system,'Segoe UI',Inter,Roboto,sans-serif;color:var(--ink);background:var(--bg)}
header{background:linear-gradient(120deg,#1e3a8a,#0f766e);color:#fff;padding:40px 24px}
header .in{max-width:1000px;margin:auto}
header h1{margin:0 0 8px;font-size:1.85rem;line-height:1.25}
header p{margin:0;opacity:.92;max-width:46rem}
header a{color:#dbeafe}
.layout{display:grid;grid-template-columns:230px 1fr;gap:32px;max-width:1280px;margin:0 auto;padding:24px}
nav.side{position:sticky;top:16px;align-self:start;font-size:.88rem;max-height:calc(100vh - 32px);overflow:auto}
nav.side .side-title{font-weight:700;margin:0 0 8px;color:var(--ink)}
nav.side .side-group{color:var(--mut);font-size:.75rem;text-transform:uppercase;letter-spacing:.04em;margin:12px 0 4px}
nav.side a{display:block;padding:5px 10px;color:var(--mut);text-decoration:none;border-left:2px solid var(--line)}
nav.side a:hover,nav.side a:focus{color:var(--acc);border-color:var(--acc)}
main.content{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 40px 40px;min-width:0}
h2{margin-top:2.2em;padding-bottom:6px;border-bottom:2px solid var(--line);scroll-margin-top:16px;font-size:1.25rem}
h2:first-of-type{margin-top:1.2em}
h3{margin-top:1.6em;color:#1e3a8a;font-size:1.05rem}
.lead{font-size:1.05rem;margin:0 0 18px;color:var(--mut)}
.muted{color:var(--mut)}
a{color:var(--acc)}
.tag{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.04em;padding:2px 8px;border-radius:999px;margin-right:6px;vertical-align:middle}
.tag-out{background:#dbeafe;color:var(--result)}
.tag-plan{background:#fef3c7;color:var(--warn)}
.tag-run{background:#ffedd5;color:#9a3412}
.callout,.kpi-note{background:#eff6ff;border-left:4px solid var(--acc);padding:10px 14px;margin:12px 0;border-radius:0 8px 8px 0}
.note{background:#f3f4f6;padding:10px 12px;border-radius:8px;font-size:.92rem;color:var(--mut);margin:12px 0}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:12px 0}
.stat strong{display:block;font-size:1.2rem}
.stat span{color:var(--mut);font-size:.88rem}
.table-wrap{overflow-x:auto;margin:8px 0}
table{border-collapse:collapse;width:100%;font-size:.9rem;margin:8px 0}
th,td{border:1px solid var(--line);padding:6px 10px;text-align:left;vertical-align:top}
th{background:#f3f4f6}
.mono,code{background:#eef2ff;border-radius:4px;padding:1px 5px;font-size:.88em;word-break:break-word;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
pre.cmd{background:#111827;color:#f9fafb;padding:12px 14px;border-radius:8px;overflow:auto;font-size:.85rem}
figure{margin:24px 0;text-align:center}
figure img{max-width:100%;height:auto;display:block;margin:0 auto;border:1px solid var(--line);border-radius:8px;background:#fff}
figcaption{font-size:.88rem;color:var(--mut);margin-top:6px;text-align:left}
.viz-block{margin:28px 0}
.viz-block h3{margin-top:0}
.viz-block.layout-fig figure img{width:min(100%,480px)}
.badge{display:inline-block;padding:2px 9px;border-radius:99px;font-size:.78rem;font-weight:600}
.REJECTED,.BI_BAC_BO{background:#fee2e2;color:var(--bad)}
.SUPPORTED,.DUOC_UNG_HO,.OK{background:#dcfce7;color:var(--ok)}
.INCONCLUSIVE,.EVALUATED,.WEAK,.YEU,.PARTIAL,.MOT_PHAN{background:#fef3c7;color:var(--warn)}
.SKIPPED,.UNEVALUATED,.BO_QUA,.CHUA_DANH_GIA{background:#ffedd5;color:#9a3412}
ul{padding-left:1.2em}li{margin:6px 0}
.side-toggle{display:none;position:fixed;right:14px;bottom:14px;z-index:40;border:1px solid var(--line);background:#fff;border-radius:999px;padding:10px 14px;font-size:.9rem;box-shadow:0 4px 16px rgba(0,0,0,.12);cursor:pointer}
.side-backdrop{display:none}
footer{max-width:1280px;margin:0 auto;padding:0 24px 28px;color:var(--mut);font-size:.88rem}
footer p{margin:0}
@media(max-width:900px){
  .layout{grid-template-columns:1fr}
  nav.side{display:none}
  nav.side.open{display:block;position:fixed;inset:0 auto 0 0;width:min(300px,86vw);background:#fff;z-index:50;padding:16px;border-right:1px solid var(--line)}
  .side-toggle{display:inline-flex}
  .side-backdrop.show{display:block;position:fixed;inset:0;background:rgba(0,0,0,.35);z-index:45}
  main.content{padding:8px 18px 30px}
  header{padding:28px 18px}header h1{font-size:1.45rem}
}
"""

JS = """
<script>
(function(){
  var side=document.getElementById('side');
  var btn=document.getElementById('toggle');
  var bd=document.getElementById('backdrop');
  if(!side||!btn) return;
  function open(){ side.classList.add('open'); if(bd){ bd.hidden=false; bd.classList.add('show'); } }
  function close(){ side.classList.remove('open'); if(bd){ bd.hidden=true; bd.classList.remove('show'); } }
  btn.addEventListener('click', function(){ side.classList.contains('open')?close():open(); });
  if(bd) bd.addEventListener('click', close);
})();
</script>
"""


def wrap(
    lang: str,
    phase: str,
    title: str,
    lead: str,
    nav: str,
    other_lang_href: str,
    other_label: str,
    body: str,
) -> str:
    if lang == "vi":
        links = (
            f'<p style="margin-top:14px">'
            f'<a href="../../../docs/main_scaling_plan_vi.html">Kế hoạch chính</a>'
            f' · <a href="../../summary/SUMMARY_REPORT_vi.html">Báo cáo tổng hợp</a>'
            f' · <a href="{other_lang_href}">{other_label}</a>'
            f' · <a href="../../../docs/INDEX_vi.html">Mục lục tài liệu</a></p>'
        )
        footer_links = (
            f'<a href="../../../docs/main_scaling_plan_vi.html">Kế hoạch chính</a> · '
            f'<a href="../../summary/SUMMARY_REPORT_vi.html">Báo cáo tổng hợp</a> · '
            f'<a href="../../../docs/methods/README_vi.html">Phương pháp</a> · '
            f'<a href="../../../docs/setup/README_vi.html">Thiết lập</a> · '
            f'<a href="../../../docs/credibility/README_vi.html">Độ tin cậy</a> · '
            f'<a href="../../summary/data/phase{phase}_tables_vi.html">Bảng Giai đoạn {phase}</a> · '
            f'<a href="../../summary/data/run_ledger_vi.html">Nhật ký chạy</a>'
        )
        toggle = "Mục lục"
    else:
        links = (
            f'<p style="margin-top:14px">'
            f'<a href="../../../docs/main_scaling_plan.html">Main plan</a>'
            f' · <a href="../../summary/SUMMARY_REPORT.html">Cross-phase summary</a>'
            f' · <a href="{other_lang_href}">{other_label}</a>'
            f' · <a href="../../../docs/INDEX.html">Docs index</a></p>'
        )
        footer_links = (
            f'<a href="../../../docs/main_scaling_plan.html">Main plan</a> · '
            f'<a href="../../summary/SUMMARY_REPORT.html">Cross-phase summary</a> · '
            f'<a href="../../../docs/methods/README.html">Methods</a> · '
            f'<a href="../../../docs/setup/README.html">Setup</a> · '
            f'<a href="../../../docs/credibility/README.html">Credibility</a> · '
            f'<a href="../../summary/data/phase{phase}_tables.html">Phase {phase} tables</a> · '
            f'<a href="../../summary/data/run_ledger.html">Run ledger</a>'
        )
        toggle = "Contents"
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>{CSS}</style>
</head>
<body>
<header><div class="in">
  <h1>{title}</h1>
  <p>{lead}</p>
  {links}
</div></header>
<div class="layout">
  <nav class="side" id="side" aria-label="Contents">
{nav}
  </nav>
  <div class="side-backdrop" id="backdrop" hidden></div>
  <button type="button" class="side-toggle" id="toggle">{toggle}</button>
<main class="content">
{body}
</main>
</div>
<footer><p>{footer_links}</p></footer>
{JS}
</body>
</html>
"""


def nav_en(items: list[tuple[str, str, str]]) -> str:
    # items: (group, href, label)
    parts = ['    <p class="side-title">Contents</p>']
    cur = None
    for group, href, label in items:
        if group != cur:
            parts.append(f'    <div class="side-group">{group}</div>')
            cur = group
        parts.append(f'    <a href="{href}">{label}</a>')
    return "\n".join(parts)


def nav_vi(items: list[tuple[str, str, str]]) -> str:
    parts = ['    <p class="side-title">Mục lục</p>']
    cur = None
    for group, href, label in items:
        if group != cur:
            parts.append(f'    <div class="side-group">{group}</div>')
            cur = group
        parts.append(f'    <a href="{href}">{label}</a>')
    return "\n".join(parts)


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")
    print("wrote", path)


def four_layouts_visuals(lang: str, *, phase: str = "2") -> str:
    """One composite figure plus a definition table (no per-layout image repeats)."""
    if lang == "en":
        composite = "assets/layouts/four_layouts_en.svg"
        composite_alt = "Four starting layouts at N = 50"
        th_layout, th_def, th_role = "Layout", "Generator definition", "Role in the design"
        rows = [
            ("compact", "Gaussian, sigma = 0.3 x 30 = 9", "Tight reference flock (Phase 1 baseline geometry)"),
            ("wide", "Gaussian, sigma = 2.0 x 30 = 60", "Spread flock that must be collected first"),
            ("split", "2 clusters if N &lt; 12, else 3; separation at least 10", "Clustered start (check layout)"),
            (
                "outlier_rich",
                "Core ~80% (sigma = 12); ~20% outliers beyond r_a * N^(2/3)",
                "Core plus stragglers",
            ),
        ]
        if phase == "4":
            intro = (
                "  <p>Size transfer uses compact only. Structure transfer reuses the same four X0 families "
                "as Phase 2, on the same arena rules, so method contrasts are not confounded with a new layout set. "
                "Shared / shifted / absent labels are reported in Results.</p>"
            )
            composite_cap = (
                "The four X0 families reused for structure transfer (N = 50, seed 2026). "
                "Green = sheep, blue squares = dogs (schematic), red = outliers where shown."
            )
        else:
            intro = (
                "  <p>Only the sheep start pattern X0 changes. Field, goal, dogs, N grid, D grid, theta, "
                "and T0 stay aligned with Phase 1 so layout effects are not confounded with arena changes. "
                "Cost and D_min contrasts are reported in Results.</p>"
            )
            composite_cap = (
                "The four X0 families on the same arena (N = 50, seed 2026). "
                "Green = sheep, blue squares = dogs (schematic), red = outliers where shown."
            )
    else:
        composite = "assets/layouts/four_layouts_vi.svg"
        composite_alt = "Bốn bố cục xuất phát tại N = 50"
        th_layout, th_def, th_role = "Bố cục", "Định nghĩa generator", "Vai trò trong thiết kế"
        rows = [
            ("compact", "Gauss, sigma = 0.3 x 30 = 9", "Đàn gọn tham chiếu (hình học cơ sở Giai đoạn 1)"),
            ("wide", "Gauss, sigma = 2.0 x 30 = 60", "Đàn loãng cần gom trước"),
            ("split", "2 cụm nếu N &lt; 12, không thì 3; tách ít nhất 10", "Xuất phát cụm (bố cục kiểm tra)"),
            (
                "outlier_rich",
                "Lõi ~80% (sigma = 12); ~20% cá thể lạc ngoài r_a * N^(2/3)",
                "Lõi cộng cá thể lạc",
            ),
        ]
        if phase == "4":
            intro = (
                "  <p>Chuyển giao kích thước chỉ dùng compact. Chuyển giao cấu trúc dùng lại cùng bốn họ X0 "
                "như Giai đoạn 2, trên cùng quy tắc sân, để đối chiếu phương pháp không lẫn với bộ bố cục mới. "
                "Nhãn chia sẻ / dịch / vắng nằm ở mục Kết quả.</p>"
            )
            composite_cap = (
                "Bốn họ X0 dùng lại cho chuyển giao cấu trúc (N = 50, hạt 2026). "
                "Xanh lá = cừu, ô xanh = chó (minh họa), đỏ = cá thể lạc khi có."
            )
        else:
            intro = (
                "  <p>Chỉ đổi kiểu xuất phát cừu X0. Sân, đích, chó, lưới N, lưới D, theta và T0 "
                "giữ khớp Giai đoạn 1 để hiệu ứng bố cục không lẫn với đổi sân. "
                "Đối chiếu chi phí và D_min nằm ở mục Kết quả.</p>"
            )
            composite_cap = (
                "Bốn họ X0 trên cùng sân (N = 50, hạt 2026). "
                "Xanh lá = cừu, ô xanh = chó (minh họa), đỏ = cá thể lạc khi có."
            )
    body_rows = "\n".join(
        f"      <tr><td><span class=\"mono\">{name}</span></td><td>{defn}</td><td>{role}</td></tr>"
        for name, defn, role in rows
    )
    return f"""{intro}
  <figure>
    <img src="{composite}" alt="{composite_alt}" />
    <figcaption>{composite_cap}</figcaption>
  </figure>
  <div class="table-wrap">
  <table>
    <thead><tr><th>{th_layout}</th><th>{th_def}</th><th>{th_role}</th></tr></thead>
    <tbody>
{body_rows}
    </tbody>
  </table>
  </div>"""


# ---------------------------------------------------------------------------
# Phase 4
# ---------------------------------------------------------------------------

P4_NAV_EN = nav_en([
    ("Start", "#summary", "At a glance"),
    ("Start", "#question", "What Phase 4 asks"),
    ("Design and run", "#design", "What we froze"),
    ("Design and run", "#layouts", "Layouts"),
    ("Design and run", "#strategy", "How we ran it"),
    ("Results", "#results", "Results"),
    ("Results", "#outlier-n200", "Kubo outlier_rich N=200"),
    ("Results", "#claims", "Claim C4"),
    ("Results", "#limits", "Limits"),
    ("Results", "#next", "Next"),
    ("Appendix", "#raw-data", "Raw data"),
])

P4_NAV_VI = nav_vi([
    ("Bắt đầu", "#summary", "Nhìn nhanh"),
    ("Bắt đầu", "#question", "Giai đoạn 4 hỏi gì"),
    ("Thiết kế và chạy", "#design", "Những gì bị khóa"),
    ("Thiết kế và chạy", "#layouts", "Bố cục"),
    ("Thiết kế và chạy", "#strategy", "Cách đã chạy"),
    ("Kết quả", "#results", "Kết quả"),
    ("Kết quả", "#outlier-n200", "Kubo outlier_rich N=200"),
    ("Kết quả", "#claims", "Kết luận C4"),
    ("Kết quả", "#limits", "Giới hạn"),
    ("Kết quả", "#next", "Tiếp"),
    ("Phụ lục", "#raw-data", "Dữ liệu thô"),
])


def phase4_en() -> str:
    body = r'''
  <h2 id="summary"><span class="tag tag-out">SUMMARY</span> At a glance</h2>
  <div class="callout">
    <strong>One-sentence result:</strong>
    Kubo shares D_min = 1 with the baseline on compact size for N &gt;= 25, but structure transfer is incomplete
    (wide hard-failure; outlier_rich N = 200 shifted to D_min = 20).
    FAT does not transfer for N &gt;= 25. C4 is <strong>SUPPORTED (partial)</strong>.
  </div>
  <div class="grid">
    <div class="card stat"><span>Kubo size N&gt;=25</span><strong>D_min = 1 (shared)</strong></div>
    <div class="card stat"><span>Kubo wide</span><strong>no D_min (best R 0.47 to 0.54)</strong></div>
    <div class="card stat"><span>Kubo outlier_rich N=200</span><strong>D_min = 20 (200 seeds)</strong></div>
    <div class="card stat"><span>FAT N&gt;=25</span><strong>hard failure</strong></div>
  </div>

  <h2 id="question"><span class="tag tag-plan">QUESTION</span> What Phase 4 asks</h2>
  <p>RQ4 / Package D: do size and structure frontiers transfer across the three required methods?</p>
  <ul>
    <li><strong>C4:</strong> D_min / overcrowding shared across methods (including structure), or document where transfer is shifted / absent.</li>
  </ul>
  <p class="muted">Baseline size and structure already measured in Phases 1 and 2. This phase does not re-run strombom_multi.</p>

  <h2 id="design"><span class="tag tag-out">DESIGN</span> What we froze</h2>
  <table>
    <thead><tr><th>Choice</th><th>Value</th></tr></thead>
    <tbody>
      <tr><td>Methods</td><td>kubo, fat (vs Phase 1/2 strombom_multi)</td></tr>
      <tr><td>Size N / D</td><td>same grids as Phase 1; compact start only</td></tr>
      <tr><td>Structure N / layouts</td><td>{50,100,200} x the four X0 families (see Layouts)</td></tr>
      <tr><td>theta / T0</td><td>0.90 / 10,000</td></tr>
      <tr><td>Seeds</td><td>scout 30; claim 100; Kubo outlier_rich N=200 uses 200 seeds on D in {1,2,3,4,6,10,15,20,25}</td></tr>
      <tr><td>obs_mode</td><td>global</td></tr>
    </tbody>
  </table>

  <h2 id="layouts"><span class="tag tag-out">DESIGN</span> Layouts</h2>
  <figure>
    <img src="assets/layouts/arena_overview.svg" alt="Arena" />
    <figcaption>
      Shared arena sketch reused from Phases 1 and 2: 500 x 500 field, goal at (370, 250), dogs behind the flock.
      Phase 4 keeps this geometry fixed; methods change, and structure transfer varies only sheep X0.
    </figcaption>
  </figure>
__LAYOUTS__
  <h3>Transfer reading rule</h3>
  <figure>
    <img src="assets/figures/transfer_sketch_en.svg" alt="Transfer sketch" />
    <figcaption>
      Package D labels each frontier feature shared (same D_min), shifted (D_min moves), or absent
      (no D_min within the frozen grid). Measured labels are in Results and Claim C4.
    </figcaption>
  </figure>

  <h2 id="strategy"><span class="tag tag-run">RUN</span> How we ran it</h2>
  <table>
    <thead><tr><th>Step</th><th>Trials</th></tr></thead>
    <tbody>
      <tr><td>kubo size scout / claim</td><td>3,000 / 2,100</td></tr>
      <tr><td>kubo structure scout / claim</td><td>3,600 / 4,000</td></tr>
      <tr><td>fat size scout / claim</td><td>3,000 / 2,000</td></tr>
      <tr><td>fat structure scout / claim</td><td>3,600 / 2,400</td></tr>
    </tbody>
  </table>
  <p class="note">Kubo structure claim has 4,000 rows: outlier_rich N=200 uses 200 seeds on D in {1,2,3,4,6,10,15,20,25} (<span class="mono">../kubo_structure/claim/</span>).</p>
<pre class="cmd">make -C scaling scaling-transfer-size-scout TRANSFER_METHOD=kubo WORKERS=16
make -C scaling scaling-transfer-size-claim-reseed TRANSFER_METHOD=kubo WORKERS=16
# repeat fat; then structure scout/claim for kubo and fat</pre>

  <h2 id="results"><span class="tag tag-out">RESULTS</span> Results</h2>
  <figure>
    <img src="assets/figures/f1_reliability_heatmaps.png" alt="Size heatmaps" />
    <figcaption>
      Compact size maps of success rate R(N, D). Left panel is Phase 1 baseline (strombom_multi);
      middle and right are Kubo and FAT from this phase. Darker / higher R means more reliable cells.
      Source: Package A reliability CSVs under phase1 and phase4 size claim folders.
    </figcaption>
  </figure>

  <h3>Size-map D_min (compact, theta=0.90)</h3>
  <table>
    <thead><tr><th>N</th><th>strombom</th><th>kubo</th><th>fat</th></tr></thead>
    <tbody>
      <tr><td>5</td><td>2</td><td>3</td><td>1</td></tr>
      <tr><td>10</td><td>2</td><td>1</td><td>1</td></tr>
      <tr><td>25 to 400</td><td>1</td><td>1</td><td>none &lt;= 35</td></tr>
    </tbody>
  </table>
  <p class="muted">No overcrowding on compact size maps. FAT best R per N for N=50 to 400 is 0.40 to 0.53. Package D size: 8 shared, 7 shifted, 29 absent.</p>

  <h3>Structure D_min</h3>
  <table>
    <thead><tr><th>Layout</th><th>N</th><th>strombom</th><th>kubo</th><th>fat</th></tr></thead>
    <tbody>
      <tr><td>compact / split</td><td>50,100,200</td><td>1</td><td>1</td><td>none</td></tr>
      <tr><td>outlier_rich</td><td>50,100</td><td>1</td><td>1</td><td>none</td></tr>
      <tr><td>outlier_rich</td><td>200</td><td>1</td><td>20 (200 seeds)</td><td>none</td></tr>
      <tr><td>wide</td><td>50,100,200</td><td>1</td><td>none (best R 0.47 to 0.54)</td><td>none (R=0)</td></tr>
    </tbody>
  </table>
  <figure>
    <img src="assets/figures/f5_layout_reliability_curves.png" alt="R vs D at N=200" />
    <figcaption>
      Reliability R against dog count D at fixed N = 200, one curve family per layout.
      Shows where each controller crosses theta = 0.90 (or fails to). Source: current
      structure claim merges.
    </figcaption>
  </figure>
  <figure>
    <img src="assets/figures/f6_failure_modes.png" alt="Failure modes" />
    <figcaption>
      How size-map trials end (success vs failure labels) for the three controllers on compact starts.
      FAT contributes most of the failure mass on N &gt;= 25, matching the missing D_min rows.
      Source: failure_mode in claim merged_trials.csv for phase1, kubo_size, fat_size.
    </figcaption>
  </figure>

  <h2 id="outlier-n200"><span class="tag tag-out">RESULTS</span> Kubo outlier_rich N=200 (stated once)</h2>
  <p>
    D = 1,2,3,4,6,10,15 stay below 0.90 at <strong>200 seeds</strong>
    (R = 0.745, 0.855, 0.835, 0.860, 0.890, 0.875, 0.855).
    D_min = 20 at <strong>200 seeds</strong> (R = 0.935); D = 25 also at 200 seeds (R = 0.910).
    D = 35 remains at 30 seeds (R = 0.967). Bootstrap interval on D_min is <strong>[2, 20]</strong>. No overcrowding.
  </p>
  <figure>
    <img src="assets/figures/f9_kubo_outlier_rich_n200.png" alt="Kubo outlier_rich N=200 CI" />
    <figcaption>
      Kubo on outlier_rich at N = 200: Wilson 95% CI for R(D). Cells D in {1,2,3,4,6,10,15,20,25} use 200 seeds;
      D = 35 uses 30 seeds. Bootstrap on D_min is [2, 20]. Source: <span class="mono">../kubo_structure/claim/merged_trials.csv</span>.
    </figcaption>
  </figure>

  <h2 id="claims"><span class="tag tag-out">CLAIMS</span> Claim C4</h2>
  <div class="card">
    <p><strong>Verdict: SUPPORTED (partial).</strong></p>
    <p>
      C4 asks whether D_min / overcrowding transfer across the three methods, including structure.
      The measured answer is mixed: transfer holds on one slice and fails on others. That is why the
      label is partial, not full support and not a full reject.
    </p>
  </div>

  <h3>Why only partial (not full support)</h3>
  <ul>
    <li><strong>Shared slice:</strong> on compact size, Kubo and strombom_multi both have D_min = 1 for every N &gt;= 25.</li>
    <li><strong>Absent for FAT:</strong> FAT never reaches R &gt;= 0.90 for any D &lt;= 35 when N &gt;= 25 (size and every structure layout).</li>
    <li><strong>Absent for Kubo wide:</strong> best R stays about 0.47 to 0.54; no D_min in the frozen grid.</li>
    <li><strong>Shifted for Kubo outlier_rich N=200:</strong> D = 1..15 stay below theta at 200 seeds; D_min = 20 at 200 seeds (bootstrap [2, 20]).</li>
    <li><strong>Tiny-N size rows are shifted</strong> even where transfer is otherwise close (N = 5, 10).</li>
  </ul>
  <p>
    Size-only reading would overstate C4. The structure map is the binding contrast: controller choice
    can erase the baseline D_min = 1 answer even when compact size looked shared.
  </p>

  <h3>Measured transfer labels</h3>
  <table>
    <thead><tr><th>Property</th><th>kubo vs strombom</th><th>fat vs strombom</th></tr></thead>
    <tbody>
      <tr><td>D_min size N&gt;=25</td><td>shared</td><td>absent</td></tr>
      <tr><td>D_min size N=5,10</td><td>shifted</td><td>shifted</td></tr>
      <tr><td>Overcrowding size</td><td>absent (neither overcrowds)</td><td>absent</td></tr>
      <tr><td>Structure compact / split</td><td>shared (D_min = 1)</td><td>absent</td></tr>
      <tr><td>Structure wide</td><td>absent</td><td>absent</td></tr>
      <tr><td>Structure outlier_rich N=200</td><td>shifted (D_min = 20)</td><td>absent</td></tr>
    </tbody>
  </table>

  <h3>Verified evidence (claim merges and Package D tables)</h3>
  <p class="muted">Docs and trackers are not evidence. The verdict rests on these measured files:</p>
  <ul>
    <li><span class="mono">../package_d/size/transfer_summary.csv</span>, <span class="mono">../package_d/size/transfer_table.csv</span></li>
    <li><span class="mono">../package_d/structure/frontier_by_method_layout.csv</span> and <span class="mono">transfer_*.csv</span></li>
    <li><span class="mono">../kubo_size/claim/packages/a/</span>, <span class="mono">../fat_size/claim/packages/a/</span> (frontiers / reliability)</li>
    <li><span class="mono">../kubo_structure/claim/merged_trials.csv</span>, <span class="mono">merged_dmin_bootstrap.csv</span>, <span class="mono">outlier_rich_n200_window.json</span></li>
    <li>Baseline contrast already fixed in Phase 1 / Phase 2 claim merges (strombom_multi)</li>
  </ul>

  <h3>What would make the conclusion complete</h3>
  <p>Two different “complete” endings are possible; they are not the same claim:</p>
  <ol>
    <li>
      <strong>Complete as a transfer map (current C4 wording):</strong> already claim-grade for the mixed
      shared / shifted / absent labels above. No further run is required to keep the partial verdict.
    </li>
    <li>
      <strong>Complete as full method transfer (all methods share D_min / overcrowding on size and structure):</strong>
      not supported by current data. To reach that stronger conclusion you would need new claim-grade
      evidence that (a) FAT reaches R &gt;= 0.90 for N &gt;= 25 on compact and on the structure layouts,
      and (b) Kubo reaches R &gt;= 0.90 on wide.
      Under <span class="mono">obs_mode=global</span> and the frozen grids, FAT and Kubo-wide currently fail that bar.
      A redesign (for example local sensing / Phase 5 ladders) would be a new experiment, not a re-label of this one.
    </li>
  </ol>

  <h2 id="limits"><span class="tag tag-out">LIMITS</span> Limits</h2>
  <ul>
    <li>Kubo outlier_rich N=200 D_min bootstrap remains wide ([2, 20]) because several D &lt; 20 sit near theta.</li>
    <li>D = 35 on Kubo outlier_rich N=200 remains at 30 seeds.</li>
    <li>No overcrowding cells; Phase 3 / C2b stay skipped.</li>
    <li>obs_mode fixed to global; Phase 5 ladders not run.</li>
  </ul>

  <h2 id="next"><span class="tag tag-out">NEXT</span> Next</h2>
  <ul>
    <li>Do not treat full cross-method transfer as settled without new FAT / Kubo-wide evidence (see claims section).</li>
    <li>Cross-phase write-up: <span class="mono">../../summary/SUMMARY_REPORT.html</span>.</li>
  </ul>

  <h2 id="raw-data"><span class="tag tag-plan">APPENDIX</span> Raw data</h2>
  <table>
    <thead><tr><th>Path</th><th>What</th></tr></thead>
    <tbody>
      <tr><td><span class="mono">../kubo_size/claim/</span></td><td>Kubo size claim + Package A</td></tr>
      <tr><td><span class="mono">../fat_size/claim/</span></td><td>FAT size claim + Package A</td></tr>
      <tr><td><span class="mono">../kubo_structure/claim/</span></td><td>Kubo structure claim</td></tr>
      <tr><td><span class="mono">../fat_structure/claim/</span></td><td>FAT structure claim</td></tr>
      <tr><td><span class="mono">../package_d/size/</span></td><td>Package D size transfer tables (CSV)</td></tr>
      <tr><td><span class="mono">../package_d/structure/</span></td><td>Package D structure frontiers / transfer CSVs</td></tr>
    </tbody>
  </table>
'''
    body = body.replace("__LAYOUTS__", four_layouts_visuals("en", phase="4"))
    return wrap(
        "en",
        "4",
        "Phase 4: method transfer",
        "Claim-grade transfer of size and structure maps from baseline strombom_multi to kubo and fat under protocol scaling_v2.",
        P4_NAV_EN,
        "REPORT_vi.html",
        "Vietnamese report",
        body,
    )


def phase4_vi() -> str:
    body = r'''
  <h2 id="summary"><span class="tag tag-out">TÓM TẮT</span> Nhìn nhanh</h2>
  <div class="callout">
    <strong>Kết quả một câu:</strong>
    Kubo chia sẻ D_min = 1 với cơ sở trên kích thước tập trung khi N &gt;= 25, nhưng chuyển giao cấu trúc không đủ
    (wide thất bại cứng; outlier_rich N = 200 dịch sang D_min = 20).
    FAT không chuyển giao với N &gt;= 25. C4 <strong>ĐƯỢC ỦNG HỘ (một phần)</strong>.
  </div>
  <div class="grid">
    <div class="card stat"><span>Kubo kích thước N&gt;=25</span><strong>D_min = 1 (chia sẻ)</strong></div>
    <div class="card stat"><span>Kubo wide</span><strong>không D_min (R tốt nhất 0.47 đến 0.54)</strong></div>
    <div class="card stat"><span>Kubo outlier_rich N=200</span><strong>D_min = 20 (200 mẫu)</strong></div>
    <div class="card stat"><span>FAT N&gt;=25</span><strong>thất bại cứng</strong></div>
  </div>

  <h2 id="question"><span class="tag tag-plan">CÂU HỎI</span> Giai đoạn 4 hỏi gì?</h2>
  <p>RQ4 / Gói D: biên kích thước và cấu trúc có chuyển giữa ba phương pháp bắt buộc không?</p>
  <ul>
    <li><strong>C4:</strong> D_min / quá tải chia sẻ giữa các phương pháp (kể cả cấu trúc), hoặc ghi rõ chỗ dịch / vắng.</li>
  </ul>
  <p class="muted">Cơ sở kích thước và cấu trúc đã đo ở Giai đoạn 1 và 2. Giai đoạn này không chạy lại strombom_multi.</p>

  <h2 id="design"><span class="tag tag-out">THIẾT KẾ</span> Những gì bị khóa</h2>
  <table>
    <thead><tr><th>Lựa chọn</th><th>Giá trị</th></tr></thead>
    <tbody>
      <tr><td>Phương pháp</td><td>kubo, fat (so với strombom_multi Giai đoạn 1/2)</td></tr>
      <tr><td>N / D kích thước</td><td>cùng lưới Giai đoạn 1; chỉ xuất phát compact</td></tr>
      <tr><td>N / bố cục cấu trúc</td><td>{50,100,200} x bốn họ X0 (xem Bố cục)</td></tr>
      <tr><td>theta / T0</td><td>0.90 / 10,000</td></tr>
      <tr><td>Mẫu</td><td>dò 30; xác nhận 100; Kubo outlier_rich N=200 dùng 200 mẫu trên D trong {1,2,3,4,6,10,15,20,25}</td></tr>
      <tr><td>obs_mode</td><td>global</td></tr>
    </tbody>
  </table>

  <h2 id="layouts"><span class="tag tag-out">THIẾT KẾ</span> Bố cục</h2>
  <figure>
    <img src="assets/layouts/arena_overview.svg" alt="Sân" />
    <figcaption>
      Phác thảo sân dùng lại từ Giai đoạn 1 và 2: sân 500 x 500, đích (370, 250), chó sau đàn.
      Giai đoạn 4 giữ cố định hình học này; đổi phương pháp, và chuyển giao cấu trúc chỉ đổi X0 của cừu.
    </figcaption>
  </figure>
__LAYOUTS__
  <h3>Quy tắc đọc chuyển giao</h3>
  <figure>
    <img src="assets/figures/transfer_sketch_vi.svg" alt="Phác thảo chuyển giao" />
    <figcaption>
      Gói D gắn nhãn mỗi đặc trưng biên là chia sẻ (cùng D_min), dịch (D_min đổi), hoặc vắng
      (không có D_min trong lưới đã khóa). Nhãn đã đo nằm ở Kết quả và Kết luận C4.
    </figcaption>
  </figure>

  <h2 id="strategy"><span class="tag tag-run">CHẠY</span> Cách đã chạy</h2>
  <table>
    <thead><tr><th>Bước</th><th>Số lượt</th></tr></thead>
    <tbody>
      <tr><td>kubo kích thước dò / xác nhận</td><td>3,000 / 2,100</td></tr>
      <tr><td>kubo cấu trúc dò / xác nhận</td><td>3,600 / 4,000</td></tr>
      <tr><td>fat kích thước dò / xác nhận</td><td>3,000 / 2,000</td></tr>
      <tr><td>fat cấu trúc dò / xác nhận</td><td>3,600 / 2,400</td></tr>
    </tbody>
  </table>
  <p class="note">Xác nhận cấu trúc Kubo có 4,000 dòng: outlier_rich N=200 dùng 200 mẫu trên D trong {1,2,3,4,6,10,15,20,25} (<span class="mono">../kubo_structure/claim/</span>).</p>

  <h2 id="results"><span class="tag tag-out">KẾT QUẢ</span> Kết quả</h2>
  <figure>
    <img src="assets/figures/f1_reliability_heatmaps.png" alt="Biểu đồ nhiệt kích thước" />
    <figcaption>
      Bản đồ tỉ lệ thành công R(N, D) trên xuất phát tập trung. Bảng trái là cơ sở Giai đoạn 1 (strombom_multi);
      giữa và phải là Kubo và FAT của giai đoạn này. R cao hơn nghĩa là ô tin cậy hơn.
      Nguồn: CSV độ tin cậy Gói A trong thư mục xác nhận kích thước phase1 và phase4.
    </figcaption>
  </figure>

  <h3>D_min kích thước (compact, theta=0.90)</h3>
  <table>
    <thead><tr><th>N</th><th>strombom</th><th>kubo</th><th>fat</th></tr></thead>
    <tbody>
      <tr><td>5</td><td>2</td><td>3</td><td>1</td></tr>
      <tr><td>10</td><td>2</td><td>1</td><td>1</td></tr>
      <tr><td>25 đến 400</td><td>1</td><td>1</td><td>không &lt;= 35</td></tr>
    </tbody>
  </table>
  <p class="muted">Không quá tải trên bản đồ kích thước tập trung. R tốt nhất theo N của FAT với N=50 đến 400 là 0.40 đến 0.53. Gói D kích thước: 8 chia sẻ, 7 dịch, 29 vắng.</p>

  <h3>D_min cấu trúc</h3>
  <table>
    <thead><tr><th>Bố cục</th><th>N</th><th>strombom</th><th>kubo</th><th>fat</th></tr></thead>
    <tbody>
      <tr><td>compact / split</td><td>50,100,200</td><td>1</td><td>1</td><td>không</td></tr>
      <tr><td>outlier_rich</td><td>50,100</td><td>1</td><td>1</td><td>không</td></tr>
      <tr><td>outlier_rich</td><td>200</td><td>1</td><td>20</td><td>không</td></tr>
      <tr><td>wide</td><td>50,100,200</td><td>1</td><td>không (R tốt nhất 0.47 đến 0.54)</td><td>không (R=0)</td></tr>
    </tbody>
  </table>
  <figure>
    <img src="assets/figures/f5_layout_reliability_curves.png" alt="R theo D tại N=200" />
    <figcaption>
      Độ tin cậy R theo số chó D tại N = 200 cố định, mỗi họ đường ứng với một bố cục.
      Cho thấy bộ điều khiển nào vượt theta = 0.90 (hoặc không vượt được). Sinh lại từ hợp nhất
      xác nhận cấu trúc hiện tại.
    </figcaption>
  </figure>
  <figure>
    <img src="assets/figures/f6_failure_modes_vi.png" alt="Chế độ thất bại" />
    <figcaption>
      Cách các lượt bản đồ kích thước kết thúc (thành công so với nhãn thất bại) cho ba bộ điều khiển
      trên xuất phát tập trung. FAT chiếm phần lớn khối thất bại khi N &gt;= 25, khớp với các hàng D_min vắng.
      Nguồn: failure_mode trong merged_trials.csv xác nhận của phase1, kubo_size, fat_size.
    </figcaption>
  </figure>

  <h2 id="outlier-n200"><span class="tag tag-out">KẾT QUẢ</span> Kubo outlier_rich N=200 (nêu một lần)</h2>
  <p>
    D = 1,2,3,4,6,10,15 giữ dưới 0.90 ở <strong>200 mẫu</strong>
    (R = 0.745, 0.855, 0.835, 0.860, 0.890, 0.875, 0.855).
    D_min = 20 ở <strong>200 mẫu</strong> (R = 0.935); D = 25 cũng 200 mẫu (R = 0.910).
    D = 35 vẫn 30 mẫu (R = 0.967). Khoảng bootstrap trên D_min là <strong>[2, 20]</strong>. Không quá tải.
  </p>
  <figure>
    <img src="assets/figures/f9_kubo_outlier_rich_n200.png" alt="Kubo outlier_rich N=200" />
    <figcaption>
      Kubo trên outlier_rich tại N = 200: khoảng Wilson 95% cho R(D). Các ô D trong {1,2,3,4,6,10,15,20,25}
      dùng 200 mẫu; D = 35 dùng 30 mẫu. Bootstrap trên D_min là [2, 20]. Nguồn: <span class="mono">../kubo_structure/claim/merged_trials.csv</span>.
    </figcaption>
  </figure>

  <h2 id="claims"><span class="tag tag-out">KHẲNG ĐỊNH</span> Kết luận C4</h2>
  <div class="card">
    <p><strong>Đánh giá: ĐƯỢC ỦNG HỘ (một phần).</strong></p>
    <p>
      C4 hỏi D_min / quá tải có chuyển giữa ba phương pháp hay không, kể cả cấu trúc.
      Kết quả đo được là lẫn: chuyển giao đúng trên một lát cắt và thất bại trên các lát khác.
      Vì thế nhãn là một phần, không phải ủng hộ đầy đủ và cũng không phải bác bỏ toàn bộ.
    </p>
  </div>

  <h3>Vì sao chỉ một phần (không phải ủng hộ đầy đủ)</h3>
  <ul>
    <li><strong>Lát cắt chia sẻ:</strong> trên kích thước tập trung, Kubo và strombom_multi đều có D_min = 1 với mọi N &gt;= 25.</li>
    <li><strong>Vắng với FAT:</strong> FAT không bao giờ đạt R &gt;= 0.90 với mọi D &lt;= 35 khi N &gt;= 25 (kích thước và mọi bố cục cấu trúc).</li>
    <li><strong>Vắng với Kubo wide:</strong> R tốt nhất khoảng 0.47 đến 0.54; không có D_min trong lưới đã khóa.</li>
    <li><strong>Dịch với Kubo outlier_rich N=200:</strong> D = 1..15 dưới theta ở 200 mẫu; D_min = 20 ở 200 mẫu (bootstrap [2, 20]).</li>
    <li><strong>Hàng N rất nhỏ bị dịch</strong> ngay cả nơi chuyển giao gần đúng (N = 5, 10).</li>
  </ul>
  <p>
    Chỉ đọc bản đồ kích thước sẽ phóng đại C4. Bản đồ cấu trúc mới là đối chiếu ràng buộc: lựa chọn
    bộ điều khiển có thể xóa đáp án D_min = 1 của cơ sở dù kích thước tập trung nhìn như chia sẻ.
  </p>

  <h3>Nhãn chuyển giao đã đo</h3>
  <table>
    <thead><tr><th>Thuộc tính</th><th>kubo so với strombom</th><th>fat so với strombom</th></tr></thead>
    <tbody>
      <tr><td>D_min kích thước N&gt;=25</td><td>chia sẻ</td><td>vắng</td></tr>
      <tr><td>D_min kích thước N=5,10</td><td>dịch</td><td>dịch</td></tr>
      <tr><td>Quá tải kích thước</td><td>vắng (không bên nào quá tải)</td><td>vắng</td></tr>
      <tr><td>Cấu trúc compact / split</td><td>chia sẻ (D_min = 1)</td><td>vắng</td></tr>
      <tr><td>Cấu trúc wide</td><td>vắng</td><td>vắng</td></tr>
      <tr><td>Cấu trúc outlier_rich N=200</td><td>dịch (D_min = 20)</td><td>vắng</td></tr>
    </tbody>
  </table>

  <h3>Bằng chứng đã xác thực (hợp nhất xác nhận và bảng Gói D)</h3>
  <p class="muted">Tài liệu và tracker không phải bằng chứng. Đánh giá dựa trên các tệp đo được sau:</p>
  <ul>
    <li><span class="mono">../package_d/size/transfer_summary.csv</span>, <span class="mono">../package_d/size/transfer_table.csv</span></li>
    <li><span class="mono">../package_d/structure/frontier_by_method_layout.csv</span> và <span class="mono">transfer_*.csv</span></li>
    <li><span class="mono">../kubo_size/claim/packages/a/</span>, <span class="mono">../fat_size/claim/packages/a/</span> (biên / độ tin cậy)</li>
    <li><span class="mono">../kubo_structure/claim/merged_trials.csv</span>, <span class="mono">merged_dmin_bootstrap.csv</span>, <span class="mono">outlier_rich_n200_window.json</span></li>
    <li>Đối chiếu cơ sở đã khóa ở hợp nhất xác nhận Giai đoạn 1 / 2 (strombom_multi)</li>
  </ul>

  <h3>Cần gì để kết luận hoàn toàn</h3>
  <p>Có hai kiểu “hoàn toàn” khác nhau; chúng không cùng một khẳng định:</p>
  <ol>
    <li>
      <strong>Hoàn toàn như bản đồ chuyển giao (cách diễn C4 hiện tại):</strong> đã đủ mức xác nhận cho các nhãn
      chia sẻ / dịch / vắng ở trên. Không cần chạy thêm để giữ đánh giá một phần.
    </li>
    <li>
      <strong>Hoàn toàn như chuyển giao đầy đủ giữa mọi phương pháp (mọi phương pháp chia sẻ D_min / quá tải
      trên kích thước và cấu trúc):</strong> dữ liệu hiện tại không ủng hộ. Để đạt kết luận mạnh hơn đó cần
      bằng chứng xác nhận mới: (a) FAT đạt R &gt;= 0.90 với N &gt;= 25 trên compact và các bố cục cấu trúc,
      và (b) Kubo đạt R &gt;= 0.90 trên wide.
      Với <span class="mono">obs_mode=global</span> và lưới đã khóa, FAT và Kubo-wide hiện không đạt ngưỡng đó.
      Đổi thiết kế (ví dụ cảm biến cục bộ / thang Giai đoạn 5) là thí nghiệm mới, không phải gắn lại nhãn thí nghiệm này.
    </li>
  </ol>

  <h2 id="limits"><span class="tag tag-out">GIỚI HẠN</span> Giới hạn</h2>
  <ul>
    <li>Bootstrap D_min Kubo outlier_rich N=200 vẫn rộng ([2, 20]) vì vài D &lt; 20 nằm gần theta.</li>
    <li>D = 35 trên Kubo outlier_rich N=200 vẫn ở 30 mẫu.</li>
    <li>Không có ô quá tải; Giai đoạn 3 / C2b vẫn bỏ qua.</li>
    <li>obs_mode cố định global; thang Giai đoạn 5 chưa chạy.</li>
  </ul>

  <h2 id="next"><span class="tag tag-out">TIẾP</span> Tiếp</h2>
  <ul>
    <li>Không coi chuyển giao đầy đủ giữa mọi phương pháp là đã xong nếu chưa có bằng chứng mới cho FAT / Kubo-wide (xem mục khẳng định).</li>
    <li>Tổng hợp liên giai đoạn: <span class="mono">../../summary/SUMMARY_REPORT_vi.html</span>.</li>
  </ul>

  <h2 id="raw-data"><span class="tag tag-plan">PHỤ LỤC</span> Dữ liệu thô</h2>
  <table>
    <thead><tr><th>Đường dẫn</th><th>Nội dung</th></tr></thead>
    <tbody>
      <tr><td><span class="mono">../kubo_size/claim/</span></td><td>Xác nhận kích thước Kubo + Gói A</td></tr>
      <tr><td><span class="mono">../fat_size/claim/</span></td><td>Xác nhận kích thước FAT + Gói A</td></tr>
      <tr><td><span class="mono">../kubo_structure/claim/</span></td><td>Xác nhận cấu trúc Kubo (kèm cửa sổ outlier_rich N=200)</td></tr>
      <tr><td><span class="mono">../fat_structure/claim/</span></td><td>Xác nhận cấu trúc FAT</td></tr>
      <tr><td><span class="mono">../package_d/size/</span></td><td>Bảng chuyển giao kích thước Gói D (CSV)</td></tr>
      <tr><td><span class="mono">../package_d/structure/</span></td><td>Biên / CSV chuyển giao cấu trúc Gói D</td></tr>
    </tbody>
  </table>
'''
    body = body.replace("__LAYOUTS__", four_layouts_visuals("vi", phase="4"))
    return wrap(
        "vi",
        "4",
        "Giai đoạn 4: chuyển giao phương pháp",
        "Chuyển giao mức xác nhận bản đồ kích thước và cấu trúc từ cơ sở strombom_multi sang kubo và fat dưới giao thức scaling_v2.",
        P4_NAV_VI,
        "REPORT_en.html",
        "Bản tiếng Anh",
        body,
    )


# ---------------------------------------------------------------------------
# Phase 2
# ---------------------------------------------------------------------------

P2_NAV_EN = nav_en([
    ("Start", "#summary", "At a glance"),
    ("Start", "#question", "What Phase 2 asks"),
    ("Design and run", "#design", "What we froze"),
    ("Design and run", "#layouts", "Four layouts"),
    ("Design and run", "#strategy", "How we ran it"),
    ("Results", "#results", "Results"),
    ("Results", "#bstar", "Wide B*"),
    ("Results", "#claims", "Claims C1a / C1b"),
    ("Results", "#limits", "Limits"),
    ("Results", "#next", "Next"),
    ("Appendix", "#raw-data", "Raw data"),
])

P2_NAV_VI = nav_vi([
    ("Bắt đầu", "#summary", "Nhìn nhanh"),
    ("Bắt đầu", "#question", "Giai đoạn 2 hỏi gì"),
    ("Thiết kế và chạy", "#design", "Những gì bị khóa"),
    ("Thiết kế và chạy", "#layouts", "Bốn bố cục"),
    ("Thiết kế và chạy", "#strategy", "Cách đã chạy"),
    ("Kết quả", "#results", "Kết quả"),
    ("Kết quả", "#bstar", "B* trên wide"),
    ("Kết quả", "#claims", "C1a / C1b"),
    ("Kết quả", "#limits", "Giới hạn"),
    ("Kết quả", "#next", "Tiếp"),
    ("Phụ lục", "#raw-data", "Dữ liệu thô"),
])


def phase2_en() -> str:
    body = r'''
  <h2 id="summary"><span class="tag tag-out">SUMMARY</span> At a glance</h2>
  <div class="callout">
    <strong>One-sentence result:</strong>
    Every layout reaches R = 1.00 from D = 1 at N in {50, 100, 200}. C1a is <strong>REJECTED</strong>.
    Structure still changes effort and time by a large factor.
  </div>
  <div class="grid">
    <div class="card stat"><span>Claim D_min (all layouts)</span><strong>1 dog</strong></div>
    <div class="card stat"><span>C1a (D_min gap)</span><strong>REJECTED</strong></div>
    <div class="card stat"><span>C1b (state vs N,D)</span><strong>INCONCLUSIVE</strong></div>
    <div class="card stat"><span>Merge rows / R</span><strong>5,280 / 1.00</strong></div>
  </div>

  <h2 id="question"><span class="tag tag-plan">QUESTION</span> What Phase 2 asks</h2>
  <p>RQ1 / Package B: at the same flock size N, does a different X0 change D_min (R &gt;= 0.90)?</p>
  <ul>
    <li><strong>C1a:</strong> for at least one N, D_min differs by at least one dog-grid step across layouts.</li>
    <li><strong>C1b:</strong> early-state model predicts success better than (N, D) alone.</li>
  </ul>

  <h2 id="design"><span class="tag tag-out">DESIGN</span> What we froze</h2>
  <table>
    <thead><tr><th>Choice</th><th>Value</th></tr></thead>
    <tbody>
      <tr><td>Method</td><td>strombom_multi only</td></tr>
      <tr><td>N (claim)</td><td>50, 100, 200</td></tr>
      <tr><td>Layouts</td><td>four X0 families (see Four layouts)</td></tr>
      <tr><td>D grid / theta / T0</td><td>same as Phase 1 / 0.90 / 10,000</td></tr>
      <tr><td>Seeds</td><td>scout 30; claim 100 on D=1 and D=2 windows (24 cells)</td></tr>
    </tbody>
  </table>

  <h2 id="layouts"><span class="tag tag-out">DESIGN</span> Four layouts</h2>
  <figure>
    <img src="assets/layouts/arena_overview.svg" alt="Arena" />
    <figcaption>
      Shared arena sketch: 500 x 500 field, goal at (370, 250), dogs behind the flock.
      Phase 2 reuses this geometry for every layout; only sheep X0 changes.
    </figcaption>
  </figure>
__LAYOUTS__

  <h2 id="strategy"><span class="tag tag-run">RUN</span> How we ran it</h2>
  <ol>
    <li>Smoke: 600 trials.</li>
    <li>Scout: 3 N x 4 layouts x 10 D x 30 = 3,600.</li>
    <li>Claim: 24 cells x 100 = 2,400; merge 5,280 rows; Package B.</li>
  </ol>

  <h2 id="results"><span class="tag tag-out">RESULTS</span> Results</h2>
  <p>
    D_min = 1 for all 12 (layout, N) cells; bootstrap width zero. At D = 1 every claim cell has R = 1.00.
    Structure therefore does not move the reliability frontier on the baseline; it moves cost.
  </p>
  <figure>
    <img src="assets/figures/f4_layout_cost.png" alt="Layout cost" />
    <figcaption>
      Median total path at D = 1 by layout and N. Wide is about 19x to 36x the compact path;
      outlier_rich grows sharply with N (about 11x path at N = 200); split matches compact
      (treat as a check, not a finding). Source: <span class="mono">../claim/merged_trials.csv</span> (D = 1).
    </figcaption>
  </figure>
  <table>
    <thead><tr><th>Layout</th><th>N</th><th>R at D=1</th><th>Median ticks</th><th>Median path</th></tr></thead>
    <tbody>
      <tr><td>compact</td><td>50 / 100 / 200</td><td>1.00</td><td>195 / 204 / 191</td><td>157 / 161 / 144</td></tr>
      <tr><td>split</td><td>50 / 100 / 200</td><td>1.00</td><td>195 / 205 / 193</td><td>158 / 162 / 144</td></tr>
      <tr><td>outlier_rich</td><td>50 / 100 / 200</td><td>1.00</td><td>224 / 501 / 1,228</td><td>209 / 554 / 1,647</td></tr>
      <tr><td>wide</td><td>50 / 100 / 200</td><td>1.00</td><td>2,138 / 3,074 / 3,870</td><td>2,925 / 4,319 / 5,213</td></tr>
    </tbody>
  </table>
  <p class="muted">Source: <span class="mono">../claim/merged_trials.csv</span> (D = 1).</p>

  <h2 id="bstar"><span class="tag tag-out">RESULTS</span> Wide B*</h2>
  <p>
    On wide starts, B* = 2 (not 1) at N = 50, 100 and 200:
    path 2,337 vs 2,925; 3,003 vs 4,319; 3,694 vs 5,213.
    That is the only baseline <strong>layout</strong> where adding a dog reduces total path enough to matter.
    Source: <span class="mono">../claim/packages/b/frontier_by_layout.csv</span>.
  </p>
  <figure>
    <img src="assets/figures/f10_wide_bstar_path.png" alt="Wide B star path" />
    <figcaption>
      On wide starts only, the cheapest reliable dog count B* is 2 rather than 1:
      median path falls from 2,925 to 2,337 (N=50), 4,319 to 3,003 (N=100), and 5,213 to 3,694 (N=200).
      That is the only baseline layout where adding a dog cuts total path enough to matter.
      Source: <span class="mono">../claim/packages/b/frontier_by_layout.csv</span>.
    </figcaption>
  </figure>

  <h2 id="claims"><span class="tag tag-out">CLAIMS</span> Claims C1a / C1b</h2>
  <table>
    <thead><tr><th>Claim</th><th>Verdict</th><th>Evidence</th></tr></thead>
    <tbody>
      <tr><td>C1a</td><td>REJECTED</td><td><span class="mono">../claim/packages/b/frontier_by_layout.csv</span>: D_min = 1 on all 4 layouts</td></tr>
      <tr><td>C1b</td><td>INCONCLUSIVE</td><td>No D_min shift; Package B NLL not informative</td></tr>
    </tbody>
  </table>

  <h2 id="limits"><span class="tag tag-out">LIMITS</span> Limits</h2>
  <ul>
    <li>Baseline method only. Controller transfer is Phase 4.</li>
    <li>Floor effect: D_min cannot fall below 1 when R = 1.00 at D = 1.</li>
    <li>Split generator may not create a hard sub-flock problem (UNVERIFIED).</li>
  </ul>

  <h2 id="next"><span class="tag tag-out">NEXT</span> Next</h2>
  <p>Phase 4 transfer. Cross-phase: <span class="mono">../../summary/SUMMARY_REPORT.html</span>.</p>

  <h2 id="raw-data"><span class="tag tag-plan">APPENDIX</span> Raw data</h2>
  <table>
    <thead><tr><th>Path</th><th>What</th></tr></thead>
    <tbody>
      <tr><td><span class="mono">../claim/merged_trials.csv</span></td><td>5,280-row merge</td></tr>
      <tr><td><span class="mono">../claim/packages/b/</span></td><td>Package B frontiers</td></tr>
      <tr><td><span class="mono">../claim/README.md</span></td><td>Folder README</td></tr>
    </tbody>
  </table>
'''
    body = body.replace("__LAYOUTS__", four_layouts_visuals("en"))
    return wrap(
        "en",
        "2",
        "Phase 2: structure map",
        "Baseline structure contrast: at fixed N, does initial layout X0 change the dogs needed for reliable herding?",
        P2_NAV_EN,
        "REPORT_vi.html",
        "Vietnamese report",
        body,
    )


def phase2_vi() -> str:
    body = r'''
  <h2 id="summary"><span class="tag tag-out">TÓM TẮT</span> Nhìn nhanh</h2>
  <div class="callout">
    <strong>Kết quả một câu:</strong>
    Mọi bố cục đạt R = 1.00 từ D = 1 tại N trong {50, 100, 200}. C1a <strong>BỊ BÁC BỎ</strong>.
    Cấu trúc vẫn đổi công sức và thời gian rất lớn.
  </div>
  <div class="grid">
    <div class="card stat"><span>D_min xác nhận (mọi bố cục)</span><strong>1 chó</strong></div>
    <div class="card stat"><span>C1a (lệch D_min)</span><strong>BỊ BÁC BỎ</strong></div>
    <div class="card stat"><span>C1b (trạng thái vs N,D)</span><strong>KHÔNG RÕ RÀNG</strong></div>
    <div class="card stat"><span>Dòng hợp nhất / R</span><strong>5,280 / 1.00</strong></div>
  </div>

  <h2 id="question"><span class="tag tag-plan">CÂU HỎI</span> Giai đoạn 2 hỏi gì?</h2>
  <p>RQ1 / Gói B: cùng kích thước đàn N, X0 khác có đổi D_min (R &gt;= 0.90) không?</p>
  <ul>
    <li><strong>C1a:</strong> với ít nhất một N, D_min lệch ít nhất một bước lưới chó giữa các bố cục.</li>
    <li><strong>C1b:</strong> mô hình trạng thái sớm dự đoán thành công tốt hơn (N, D) đơn thuần.</li>
  </ul>

  <h2 id="design"><span class="tag tag-out">THIẾT KẾ</span> Những gì bị khóa</h2>
  <table>
    <thead><tr><th>Lựa chọn</th><th>Giá trị</th></tr></thead>
    <tbody>
      <tr><td>Phương pháp</td><td>chỉ strombom_multi</td></tr>
      <tr><td>N (xác nhận)</td><td>50, 100, 200</td></tr>
      <tr><td>Bố cục</td><td>bốn họ X0 (xem Bốn bố cục)</td></tr>
      <tr><td>Lưới D / theta / T0</td><td>như Giai đoạn 1 / 0.90 / 10,000</td></tr>
      <tr><td>Mẫu</td><td>dò 30; xác nhận 100 trên cửa sổ D=1 và D=2 (24 ô)</td></tr>
    </tbody>
  </table>

  <h2 id="layouts"><span class="tag tag-out">THIẾT KẾ</span> Bốn bố cục</h2>
  <figure>
    <img src="assets/layouts/arena_overview.svg" alt="Sân" />
    <figcaption>
      Phác thảo sân dùng chung: sân 500 x 500, đích (370, 250), chó sau đàn.
      Giai đoạn 2 dùng lại hình học này cho mọi bố cục; chỉ đổi X0 của cừu.
    </figcaption>
  </figure>
__LAYOUTS__

  <h2 id="strategy"><span class="tag tag-run">CHẠY</span> Cách đã chạy</h2>
  <ol>
    <li>Thử nghiệm: 600 lượt.</li>
    <li>Dò đường: 3 N x 4 bố cục x 10 D x 30 = 3,600.</li>
    <li>Xác nhận: 24 ô x 100 = 2,400; hợp nhất 5,280 dòng; Gói B.</li>
  </ol>

  <h2 id="results"><span class="tag tag-out">KẾT QUẢ</span> Kết quả</h2>
  <p>
    D_min = 1 với cả 12 ô (bố cục, N); bootstrap độ rộng 0. Tại D = 1 mọi ô xác nhận có R = 1.00.
    Vậy cấu trúc không dịch biên tin cậy trên cơ sở; nó dịch chi phí.
  </p>
  <figure>
    <img src="assets/figures/f4_layout_cost.png" alt="Chi phí theo bố cục" />
    <figcaption>
      Tổng đường trung vị tại D = 1 theo bố cục và N. Wide khoảng 19x đến 36x đường compact;
      outlier_rich tăng mạnh theo N (khoảng 11x đường tại N = 200); split khớp compact
      (coi là kiểm tra, không phải phát hiện). Nguồn: <span class="mono">../claim/merged_trials.csv</span> (D = 1).
    </figcaption>
  </figure>
  <table>
    <thead><tr><th>Bố cục</th><th>N</th><th>R tại D=1</th><th>Bước trung vị</th><th>Đường trung vị</th></tr></thead>
    <tbody>
      <tr><td>compact</td><td>50 / 100 / 200</td><td>1.00</td><td>195 / 204 / 191</td><td>157 / 161 / 144</td></tr>
      <tr><td>split</td><td>50 / 100 / 200</td><td>1.00</td><td>195 / 205 / 193</td><td>158 / 162 / 144</td></tr>
      <tr><td>outlier_rich</td><td>50 / 100 / 200</td><td>1.00</td><td>224 / 501 / 1,228</td><td>209 / 554 / 1,647</td></tr>
      <tr><td>wide</td><td>50 / 100 / 200</td><td>1.00</td><td>2,138 / 3,074 / 3,870</td><td>2,925 / 4,319 / 5,213</td></tr>
    </tbody>
  </table>
  <p class="muted">Nguồn: <span class="mono">../claim/merged_trials.csv</span> (D = 1).</p>

  <h2 id="bstar"><span class="tag tag-out">KẾT QUẢ</span> B* trên wide</h2>
  <p>
    Trên xuất phát wide, B* = 2 (không phải 1) tại N = 50, 100 và 200:
    đường 2,337 so 2,925; 3,003 so 4,319; 3,694 so 5,213.
    Đó là <strong>bố cục</strong> cơ sở duy nhất nơi thêm một chó giảm quãng đường đủ rõ.
  </p>
  <figure>
    <img src="assets/figures/f10_wide_bstar_path.png" alt="B sao wide" />
    <figcaption>
      Chỉ trên xuất phát wide, số chó tin cậy rẻ nhất B* là 2 chứ không phải 1:
      đường trung vị giảm từ 2,925 xuống 2,337 (N=50), 4,319 xuống 3,003 (N=100), và 5,213 xuống 3,694 (N=200).
      Đây là bố cục cơ sở duy nhất mà thêm một chó cắt tổng đường đủ rõ.
      Nguồn: <span class="mono">../claim/packages/b/frontier_by_layout.csv</span>.
    </figcaption>
  </figure>

  <h2 id="claims"><span class="tag tag-out">KHẲNG ĐỊNH</span> C1a / C1b</h2>
  <table>
    <thead><tr><th>Kết luận</th><th>Đánh giá</th><th>Bằng chứng</th></tr></thead>
    <tbody>
      <tr><td>C1a</td><td>BỊ BÁC BỎ</td><td><span class="mono">../claim/packages/b/frontier_by_layout.csv</span>: D_min = 1 cả 4 bố cục</td></tr>
      <tr><td>C1b</td><td>KHÔNG RÕ RÀNG</td><td>Không dịch D_min; NLL Gói B không thông tin</td></tr>
    </tbody>
  </table>

  <h2 id="limits"><span class="tag tag-out">GIỚI HẠN</span> Giới hạn</h2>
  <ul>
    <li>Chỉ phương pháp cơ sở. Chuyển giao bộ điều khiển là Giai đoạn 4.</li>
    <li>Hiệu ứng sàn: D_min không xuống dưới 1 khi R = 1.00 tại D = 1.</li>
    <li>Bộ sinh split có thể không tạo bài toán đàn con cứng (CHƯA XÁC NHẬN).</li>
  </ul>

  <h2 id="next"><span class="tag tag-out">TIẾP</span> Tiếp</h2>
  <p>Giai đoạn 4 chuyển giao. Tổng hợp: <span class="mono">../../summary/SUMMARY_REPORT_vi.html</span>.</p>

  <h2 id="raw-data"><span class="tag tag-plan">PHỤ LỤC</span> Dữ liệu thô</h2>
  <table>
    <thead><tr><th>Đường dẫn</th><th>Nội dung</th></tr></thead>
    <tbody>
      <tr><td><span class="mono">../claim/merged_trials.csv</span></td><td>Hợp nhất 5,280 dòng</td></tr>
      <tr><td><span class="mono">../claim/packages/b/</span></td><td>Biên Gói B</td></tr>
      <tr><td><span class="mono">../claim/README.md</span></td><td>README thư mục</td></tr>
    </tbody>
  </table>
'''
    body = body.replace("__LAYOUTS__", four_layouts_visuals("vi"))
    return wrap(
        "vi",
        "2",
        "Giai đoạn 2: bản đồ cấu trúc",
        "Đối chiếu cấu trúc cơ sở: ở N cố định, bố cục xuất phát X0 có đổi số chó cần để chăn tin cậy không?",
        P2_NAV_VI,
        "REPORT_en.html",
        "Bản tiếng Anh",
        body,
    )


# ---------------------------------------------------------------------------
# Phase 1
# ---------------------------------------------------------------------------

P1_NAV_EN = nav_en([
    ("Start", "#summary", "At a glance"),
    ("Start", "#question", "What Phase 1 asks"),
    ("Design and run", "#design", "What we froze"),
    ("Design and run", "#arena", "Arena and staging"),
    ("Design and run", "#strategy", "How we ran it"),
    ("Results", "#results", "Results"),
    ("Results", "#fits", "Package F"),
    ("Results", "#claims", "Claims"),
    ("Results", "#limits", "Limits"),
    ("Results", "#next", "Next"),
    ("Appendix", "#raw-data", "Raw data"),
])

P1_NAV_VI = nav_vi([
    ("Bắt đầu", "#summary", "Nhìn nhanh"),
    ("Bắt đầu", "#question", "Giai đoạn 1 hỏi gì"),
    ("Thiết kế và chạy", "#design", "Những gì bị khóa"),
    ("Thiết kế và chạy", "#arena", "Sân và phân tầng"),
    ("Thiết kế và chạy", "#strategy", "Cách đã chạy"),
    ("Kết quả", "#results", "Kết quả"),
    ("Kết quả", "#fits", "Gói F"),
    ("Kết quả", "#claims", "Kết luận"),
    ("Kết quả", "#limits", "Giới hạn"),
    ("Kết quả", "#next", "Tiếp"),
    ("Phụ lục", "#raw-data", "Dữ liệu thô"),
])


def phase1_en() -> str:
    body = r'''
  <h2 id="summary"><span class="tag tag-out">SUMMARY</span> At a glance</h2>
  <div class="callout">
    <strong>One-sentence result:</strong>
    On compact starts, D_min = 2 for N in {5, 10} and D_min = 1 for N = 25 to 400.
    No overcrowding. Extra dogs are mostly waste. Bootstrap intervals on baseline D_min have width zero.
  </div>
  <div class="grid">
    <div class="card stat"><span>Merge rows / R</span><strong>4,540 / 0.963</strong></div>
    <div class="card stat"><span>D_min N&gt;=25</span><strong>1</strong></div>
    <div class="card stat"><span>Regimes</span><strong>88 waste / 10 eff / 2 under</strong></div>
    <div class="card stat"><span>Overcrowding cells</span><strong>0</strong></div>
  </div>

  <h2 id="question"><span class="tag tag-plan">QUESTION</span> What Phase 1 asks</h2>
  <p>RQ2 / Package A: how does D_min change with flock size N on compact X0 for <span class="mono">strombom_multi</span>?</p>
  <ul>
    <li><strong>C2a:</strong> overcrowding appears on the size map.</li>
    <li><strong>C2b:</strong> T1 at 20,000 ticks on overcrowding cells.</li>
    <li><strong>C6a:</strong> leave-one-N-out scaling fits (Package F).</li>
  </ul>

  <h2 id="design"><span class="tag tag-out">DESIGN</span> What we froze</h2>
  <table>
    <thead><tr><th>Choice</th><th>Value</th></tr></thead>
    <tbody>
      <tr><td>Method / layout</td><td>strombom_multi / compact</td></tr>
      <tr><td>N grid</td><td>{5,10,25,50,75,100,150,200,300,400}</td></tr>
      <tr><td>D grid</td><td>{1,2,3,4,6,10,15,20,25,35}</td></tr>
      <tr><td>theta / T0</td><td>0.90 / 10,000</td></tr>
      <tr><td>Seeds</td><td>scout 30 everywhere; claim 100 on 22 reliability-window cells</td></tr>
      <tr><td>Field / goal</td><td>500 x 500; goal (370,250); radius 15 * sqrt(N/50)</td></tr>
    </tbody>
  </table>

  <h2 id="arena"><span class="tag tag-out">DESIGN</span> Arena and staging</h2>
  <figure>
    <img src="assets/schematics/arena_compact.svg" alt="Arena" />
    <figcaption>
      Compact-start arena used for the Phase 1 size map: 500 x 500 field, flock near the center,
      dogs behind the flock, goal at (370, 250) to the right. This is the fixed geometry for every (N, D) cell.
    </figcaption>
  </figure>
  <figure>
    <img src="assets/schematics/goal_radius.svg" alt="Goal radius" />
    <figcaption>
      Goal radius scales as 15 * sqrt(N/50). Larger flocks get a larger capture disk so area per sheep
      stays similar; otherwise growing N would make the task artificially harder.
    </figcaption>
  </figure>
  <figure>
    <img src="assets/schematics/pipeline.svg" alt="Pipeline" />
    <figcaption>
      Experiment staging: pilot smoke-checks the pipeline, scout maps the full N x D grid cheaply,
      claim reseeds a frontier window, then analysis merges claim and leftover scout rows.
      T1 (20,000-tick overcrowding check) is skipped here because Package A found 0 overcrowding cells.
    </figcaption>
  </figure>

  <div class="viz-block">
    <h3>Scout grid at 30 seeds</h3>
    <figure>
      <img src="assets/schematics/scout_grid.svg" alt="Scout covers the full N by D grid at 30 seeds" />
      <figcaption>
        Scout covers every frozen (N, D) cell at 30 independent seeds. That cheap pass sketches reliability R
        across the whole grid so we can see where the frontier sits before spending claim budget.
        Scout rows are for planning only; they are not the citeable claim surface.
      </figcaption>
    </figure>
  </div>
  <div class="viz-block">
    <h3>Claim window around the scout frontier</h3>
    <figure>
      <img src="assets/schematics/claim_window.svg" alt="Claim reseeds only a window around the scout frontier" />
      <figcaption>
        Claim reseeds only a reliability window around the scout frontier (here 22 cells at 100 seeds).
        Precision is spent where D_min is decided. On those cells the merge keeps claim seeds only;
        other cells keep their scout rows.
      </figcaption>
    </figure>
  </div>
  <div class="viz-block">
    <h3>One cell is many independent seeds</h3>
    <figure>
      <img src="assets/schematics/one_cell_seeds.svg" alt="One cell is many independent seeds" />
      <figcaption>
        Each (N, D) cell is not a single run. Reliability R is the fraction of independent seeds that succeed
        (win by timeout T0). Scout uses 30 seeds; claim uses 100 on the planned window.
      </figcaption>
    </figure>
  </div>
  <div class="viz-block">
    <h3>Regime labels along D</h3>
    <figure>
      <img src="assets/schematics/regimes.svg" alt="Regime sketch along D at fixed N" />
      <figcaption>
        At fixed N, labels along the dog-count axis: under-resourced below D_min, efficient near the useful D,
        and wasteful overspend when R is already high and extra dogs only add path. Phase 1 merge counts:
        88 wasteful, 10 efficient, 2 under-resourced.
      </figcaption>
    </figure>
  </div>

  <h2 id="strategy"><span class="tag tag-run">RUN</span> How we ran it</h2>
  <ol>
    <li>Pilot: 150 trials.</li>
    <li>Scout: 3,000 trials (10 N x 10 D x 30).</li>
    <li>Claim: 2,200 trials (22 cells x 100); merge = 22x100 + 78x30 = <strong>4,540</strong> rows.</li>
    <li>Packages A and F on the merge. T1 not run.</li>
  </ol>

  <h2 id="results"><span class="tag tag-out">RESULTS</span> Results</h2>
  <figure>
    <img src="assets/figures/reliability_heatmap.png" alt="Reliability heatmap" />
    <figcaption>
      Package A reliability heatmap on the claim merge: each cell is R(N, D), the fraction of seeds
      that succeed by timeout T0. The dark reliable band starts at D = 2 for N in {5, 10} and at D = 1
      for N = 25 to 400. Source: <span class="mono">../claim/packages/a/reliability.csv</span>.
    </figcaption>
  </figure>
  <figure>
    <img src="assets/figures/frontier_dmin.png" alt="Frontier" />
    <figcaption>
      D_min(N) frontier at theta = 0.90: smallest D with R &gt;= 0.90. Values are 2 for N in {5, 10}
      and 1 for N = 25 to 400. Bootstrap intervals on every baseline D_min have width zero
      (every resample agreed). Source: <span class="mono">../claim/packages/a/frontier.csv</span>.
    </figcaption>
  </figure>
  <table>
    <thead><tr><th>N</th><th>D_min</th></tr></thead>
    <tbody>
      <tr><td>5, 10</td><td>2</td></tr>
      <tr><td>25 to 400</td><td>1</td></tr>
    </tbody>
  </table>
  <p>
    Overall R = 0.963 (4,371 wins / 4,540). Failures almost only at D = 1 on tiny flocks:
    N=5 oscillation 93; N=10 stuck 58 + oscillation 18. Median ticks 183 (p90 198).
    For N &gt;= 25, median path per dog about 148.
  </p>
  <figure>
    <img src="assets/figures/regime_counts.png" alt="Regimes" />
    <figcaption>
      Counts of regime labels over the N x D map: 88 wasteful (already reliable; more dogs only add path),
      10 efficient (near the useful D), and 2 under-resourced (the tiny-flock cells at D = 1).
      That is why extra dogs above D_min are mostly waste on compact starts.
      Source: <span class="mono">../claim/packages/a/regimes.csv</span>.
    </figcaption>
  </figure>
  <figure>
    <img src="assets/figures/f3_cost_vs_d.png" alt="Cost vs D" />
    <figcaption>
      Cost against D on a log-log view: finish time stays roughly flat while total path grows with D.
      Median finish is about 183 ticks (p90 198); for N &gt;= 25 median path per dog is about 148.
      Source: <span class="mono">../claim/merged_trials.csv</span>.
    </figcaption>
  </figure>
  <figure>
    <img src="assets/figures/f2_dmin_vs_n.png" alt="Dmin vs N" />
    <figcaption>
      D_min against flock size N for the claim-grade baseline, with the 2025 draft curve shown only
      for contrast (draft numbers are not re-run here). The claim surface is nearly flat after N = 10.
      Source: <span class="mono">../claim/packages/a/frontier.csv</span> and draft Table A3.
    </figcaption>
  </figure>

  <h2 id="fits"><span class="tag tag-out">RESULTS</span> Package F</h2>
  <p>Observed D_min is only two levels {2, 1}. Leave-one-N-out RMSE: constant 0.44, linear 0.44, power 0.25, piecewise 0.13. Piecewise wins only by hard-coding the step. Not a real scaling law. C6b cannot be tested.</p>
  <figure>
    <img src="assets/figures/f8_scaling_rmse.svg" alt="Package F RMSE" />
    <figcaption>
      Leave-one-N-out RMSE by candidate scaling model (constant, linear, power, piecewise).
      Piecewise looks best only because it hard-codes the step from 2 to 1; there is no real growth law
      to fit, so C6b stays untestable. Source: <span class="mono">../claim/packages/f/scaling_cv.csv</span>.
    </figcaption>
  </figure>

  <h2 id="claims"><span class="tag tag-out">CLAIMS</span> Claims</h2>
  <table>
    <thead><tr><th>Claim</th><th>Verdict</th><th>Evidence</th></tr></thead>
    <tbody>
      <tr><td>C2a</td><td>REJECTED</td><td>Package A: 0 overcrowding cells</td></tr>
      <tr><td>C2b</td><td>SKIPPED</td><td>No overcrowding cells for T1</td></tr>
      <tr><td>C6a</td><td>EVALUATED, weak</td><td>Package F piecewise preferred but degenerate</td></tr>
    </tbody>
  </table>
  <p class="muted">Tracker: <span class="mono">../../docs/progress_tracker.md</span>. Narrative: <span class="mono">../claim/README.md</span>.</p>

  <h2 id="limits"><span class="tag tag-out">LIMITS</span> Limits</h2>
  <ul>
    <li>Single method, single layout. Structure is Phase 2; transfer is Phase 4.</li>
    <li>Ceiling effect: R = 1.00 at D = 1 on almost every mid/large N cell.</li>
    <li>Merge mixes 100-seed claim cells with 30-seed scout cells elsewhere (by design).</li>
  </ul>

  <h2 id="next"><span class="tag tag-out">NEXT</span> Next</h2>
  <p>Phase 2 structure. Cross-phase: <span class="mono">../../summary/SUMMARY_REPORT.html</span>.</p>

  <h2 id="raw-data"><span class="tag tag-plan">APPENDIX</span> Raw data</h2>
  <table>
    <thead><tr><th>Path</th><th>What</th></tr></thead>
    <tbody>
      <tr><td><span class="mono">../claim/merged_trials.csv</span></td><td>4,540-row merge</td></tr>
      <tr><td><span class="mono">../claim/packages/a/</span></td><td>Package A</td></tr>
      <tr><td><span class="mono">../claim/packages/f/</span></td><td>Package F</td></tr>
      <tr><td><span class="mono">../claim/README.md</span></td><td>Folder README</td></tr>
      <tr><td><span class="mono">../t1/README.md</span></td><td>T1 skipped note</td></tr>
    </tbody>
  </table>
'''
    return wrap(
        "en",
        "1",
        "Phase 1: size map",
        "Claim-grade map of how many dogs a compact flock needs as N grows, under protocol scaling_v2.",
        P1_NAV_EN,
        "REPORT_vi.html",
        "Vietnamese report",
        body,
    )


def phase1_vi() -> str:
    body = r'''
  <h2 id="summary"><span class="tag tag-out">TÓM TẮT</span> Nhìn nhanh</h2>
  <div class="callout">
    <strong>Kết quả một câu:</strong>
    Trên xuất phát tập trung, D_min = 2 với N trong {5, 10} và D_min = 1 với N = 25 đến 400.
    Không quá tải. Thêm chó phần lớn lãng phí. Khoảng bootstrap mọi D_min cơ sở có độ rộng 0.
  </div>
  <div class="grid">
    <div class="card stat"><span>Dòng hợp nhất / R</span><strong>4,540 / 0.963</strong></div>
    <div class="card stat"><span>D_min N&gt;=25</span><strong>1</strong></div>
    <div class="card stat"><span>Trạng thái</span><strong>88 lãng phí / 10 hiệu quả / 2 thiếu</strong></div>
    <div class="card stat"><span>Ô quá tải</span><strong>0</strong></div>
  </div>

  <h2 id="question"><span class="tag tag-plan">CÂU HỎI</span> Giai đoạn 1 hỏi gì?</h2>
  <p>RQ2 / Gói A: D_min đổi thế nào theo kích thước đàn N trên X0 tập trung với <span class="mono">strombom_multi</span>?</p>
  <ul>
    <li><strong>C2a:</strong> quá tải xuất hiện trên bản đồ kích thước.</li>
    <li><strong>C2b:</strong> T1 ở 20,000 bước trên ô quá tải.</li>
    <li><strong>C6a:</strong> khớp tỷ lệ leave-one-N-out (Gói F).</li>
  </ul>

  <h2 id="design"><span class="tag tag-out">THIẾT KẾ</span> Những gì bị khóa</h2>
  <table>
    <thead><tr><th>Lựa chọn</th><th>Giá trị</th></tr></thead>
    <tbody>
      <tr><td>Phương pháp / bố cục</td><td>strombom_multi / compact</td></tr>
      <tr><td>Lưới N</td><td>{5,10,25,50,75,100,150,200,300,400}</td></tr>
      <tr><td>Lưới D</td><td>{1,2,3,4,6,10,15,20,25,35}</td></tr>
      <tr><td>theta / T0</td><td>0.90 / 10,000</td></tr>
      <tr><td>Mẫu</td><td>dò 30 mọi ô; xác nhận 100 trên 22 ô cửa sổ tin cậy</td></tr>
      <tr><td>Sân / đích</td><td>500 x 500; đích (370,250); bán kính 15 * sqrt(N/50)</td></tr>
    </tbody>
  </table>

  <h2 id="arena"><span class="tag tag-out">THIẾT KẾ</span> Sân và phân tầng</h2>
  <figure>
    <img src="assets/schematics/arena_compact.svg" alt="Sân" />
    <figcaption>
      Sân xuất phát tập trung dùng cho bản đồ kích thước Giai đoạn 1: sân 500 x 500, đàn gần tâm,
      chó sau đàn, đích tại (370, 250) bên phải. Đây là hình học cố định cho mọi ô (N, D).
    </figcaption>
  </figure>
  <figure>
    <img src="assets/schematics/goal_radius.svg" alt="Bán kính đích" />
    <figcaption>
      Bán kính đích tỷ lệ 15 * sqrt(N/50). Đàn lớn hơn nhận đĩa bắt lớn hơn để diện tích mỗi cừu
      giữ tương tự; nếu không, tăng N sẽ làm bài toán khó giả tạo.
    </figcaption>
  </figure>
  <figure>
    <img src="assets/schematics/pipeline.svg" alt="Đường ống" />
    <figcaption>
      Phân tầng thí nghiệm: thử nghiệm khói kiểm đường ống, dò đường lập bản đồ lưới N x D giá rẻ,
      xác nhận gieo lại cửa sổ biên, rồi phân tích hợp nhất hàng xác nhận và hàng dò còn lại.
      T1 (kiểm quá tải 20,000 bước) bỏ qua vì Gói A không tìm thấy ô quá tải nào.
    </figcaption>
  </figure>

  <div class="viz-block">
    <h3>Lưới dò đường 30 mẫu</h3>
    <figure>
      <img src="assets/schematics/scout_grid.svg" alt="Dò đường phủ toàn lưới N nhân D ở 30 mẫu" />
      <figcaption>
        Dò đường phủ mọi ô (N, D) đã khóa với 30 mẫu độc lập. Lượt rẻ này phác thảo độ tin cậy R trên cả lưới
        để thấy biên nằm đâu trước khi chi ngân sách xác nhận.
        Hàng dò đường chỉ để lập kế hoạch; không phải mặt xác nhận được trích dẫn.
      </figcaption>
    </figure>
  </div>
  <div class="viz-block">
    <h3>Cửa sổ xác nhận quanh biên dò đường</h3>
    <figure>
      <img src="assets/schematics/claim_window.svg" alt="Xác nhận chỉ gieo lại cửa sổ quanh biên dò đường" />
      <figcaption>
        Xác nhận chỉ gieo lại cửa sổ tin cậy quanh biên dò đường (ở đây 22 ô với 100 mẫu).
        Độ chính xác dành cho chỗ quyết định D_min. Trên các ô đó hợp nhất chỉ giữ mẫu xác nhận;
        ô khác giữ hàng dò đường.
      </figcaption>
    </figure>
  </div>
  <div class="viz-block">
    <h3>Một ô là nhiều mẫu độc lập</h3>
    <figure>
      <img src="assets/schematics/one_cell_seeds.svg" alt="Một ô là nhiều mẫu độc lập" />
      <figcaption>
        Mỗi ô (N, D) không phải một lần chạy. Độ tin cậy R là tỉ lệ mẫu độc lập thành công
        (thắng trước hết giờ T0). Dò đường dùng 30 mẫu; xác nhận dùng 100 trên cửa sổ đã lên kế hoạch.
      </figcaption>
    </figure>
  </div>
  <div class="viz-block">
    <h3>Nhãn trạng thái theo D</h3>
    <figure>
      <img src="assets/schematics/regimes.svg" alt="Phác thảo trạng thái theo D ở N cố định" />
      <figcaption>
        Ở N cố định, nhãn dọc trục số chó: thiếu nguồn lực dưới D_min, hiệu quả gần D hữu ích,
        và lãng phí quá mức khi R đã cao và thêm chó chỉ thêm đường. Đếm hợp nhất Giai đoạn 1:
        88 lãng phí, 10 hiệu quả, 2 thiếu nguồn lực.
      </figcaption>
    </figure>
  </div>

  <h2 id="strategy"><span class="tag tag-run">CHẠY</span> Cách đã chạy</h2>
  <ol>
    <li>Thử nghiệm: 150 lượt.</li>
    <li>Dò đường: 3,000 lượt (10 N x 10 D x 30).</li>
    <li>Xác nhận: 2,200 lượt (22 ô x 100); hợp nhất = 22x100 + 78x30 = <strong>4,540</strong> dòng.</li>
    <li>Gói A và F trên hợp nhất. T1 không chạy.</li>
  </ol>

  <h2 id="results"><span class="tag tag-out">KẾT QUẢ</span> Kết quả</h2>
  <figure>
    <img src="assets/figures/reliability_heatmap.png" alt="Biểu đồ nhiệt" />
    <figcaption>
      Biểu đồ nhiệt độ tin cậy Gói A trên hợp nhất xác nhận: mỗi ô là R(N, D), tỉ lệ mẫu thành công
      trước hết giờ T0. Dải tin cậy tối bắt đầu ở D = 2 với N trong {5, 10} và ở D = 1 với N = 25 đến 400.
      Nguồn: <span class="mono">../claim/packages/a/reliability.csv</span>.
    </figcaption>
  </figure>
  <figure>
    <img src="assets/figures/frontier_dmin.png" alt="Biên" />
    <figcaption>
      Biên D_min(N) tại theta = 0.90: D nhỏ nhất có R &gt;= 0.90. Giá trị là 2 với N trong {5, 10}
      và 1 với N = 25 đến 400. Khoảng bootstrap mọi D_min cơ sở có độ rộng 0
      (mọi lần lấy lại mẫu cùng kết quả). Nguồn: <span class="mono">../claim/packages/a/frontier.csv</span>.
    </figcaption>
  </figure>
  <table>
    <thead><tr><th>N</th><th>D_min</th></tr></thead>
    <tbody>
      <tr><td>5, 10</td><td>2</td></tr>
      <tr><td>25 đến 400</td><td>1</td></tr>
    </tbody>
  </table>
  <p>
    R tổng = 0.963 (4,371 thắng / 4,540). Thất bại gần như chỉ tại D = 1 trên đàn rất nhỏ:
    N=5 dao động 93; N=10 kẹt 58 + dao động 18. Bước trung vị 183 (p90 198).
    Với N &gt;= 25, đường trung vị mỗi chó khoảng 148.
  </p>
  <figure>
    <img src="assets/figures/regime_counts.png" alt="Trạng thái" />
    <figcaption>
      Đếm nhãn trạng thái trên bản đồ N x D: 88 lãng phí (đã tin cậy; thêm chó chỉ thêm đường),
      10 hiệu quả (gần D hữu ích), và 2 thiếu nguồn lực (ô đàn rất nhỏ tại D = 1).
      Đó là lý do thêm chó trên D_min phần lớn lãng phí trên xuất phát tập trung.
      Nguồn: <span class="mono">../claim/packages/a/regimes.csv</span>.
    </figcaption>
  </figure>
  <figure>
    <img src="assets/figures/f3_cost_vs_d.png" alt="Chi phí theo D" />
    <figcaption>
      Chi phí theo D trên trục log-log: thời gian kết thúc gần như phẳng trong khi tổng đường tăng theo D.
      Thời gian kết thúc trung vị khoảng 183 bước (p90 198); với N &gt;= 25 đường trung vị mỗi chó khoảng 148.
      Nguồn: <span class="mono">../claim/merged_trials.csv</span>.
    </figcaption>
  </figure>
  <figure>
    <img src="assets/figures/f2_dmin_vs_n.png" alt="Dmin theo N" />
    <figcaption>
      D_min theo kích thước đàn N cho cơ sở mức xác nhận, kèm đường bản thảo 2025 chỉ để đối chiếu
      (số bản thảo không chạy lại ở đây). Mặt xác nhận gần như phẳng sau N = 10.
      Nguồn: <span class="mono">../claim/packages/a/frontier.csv</span> và bảng A3 bản thảo.
    </figcaption>
  </figure>

  <h2 id="fits"><span class="tag tag-out">KẾT QUẢ</span> Gói F</h2>
  <p>D_min quan sát chỉ hai mức {2, 1}. RMSE leave-one-N-out: hằng 0.44, tuyến tính 0.44, luỹ thừa 0.25, từng mảnh 0.13. Từng mảnh thắng chỉ vì mã hoá cứng bước nhảy. Không phải luật tỷ lệ thật. C6b không kiểm được.</p>
  <figure>
    <img src="assets/figures/f8_scaling_rmse.svg" alt="RMSE Gói F" />
    <figcaption>
      RMSE leave-one-N-out theo mô hình tỷ lệ ứng viên (hằng, tuyến tính, lũy thừa, từng đoạn).
      Mô hình từng đoạn trông tốt nhất chỉ vì nó cứng hóa bước từ 2 xuống 1; không có luật tăng trưởng thật
      để khớp, nên C6b vẫn không kiểm được. Nguồn: <span class="mono">../claim/packages/f/scaling_cv.csv</span>.
    </figcaption>
  </figure>

  <h2 id="claims"><span class="tag tag-out">KHẲNG ĐỊNH</span> Kết luận</h2>
  <table>
    <thead><tr><th>Kết luận</th><th>Đánh giá</th><th>Bằng chứng</th></tr></thead>
    <tbody>
      <tr><td>C2a</td><td>BỊ BÁC BỎ</td><td>Gói A: 0 ô quá tải</td></tr>
      <tr><td>C2b</td><td>BỎ QUA</td><td>Không có ô quá tải cho T1</td></tr>
      <tr><td>C6a</td><td>ĐÃ ĐÁNH GIÁ, yếu</td><td>Gói F ưa từng mảnh nhưng suy biến</td></tr>
    </tbody>
  </table>
  <p class="muted">Theo dõi: <span class="mono">../../docs/progress_tracker.md</span>. Diễn giải: <span class="mono">../claim/README.md</span>.</p>

  <h2 id="limits"><span class="tag tag-out">GIỚI HẠN</span> Giới hạn</h2>
  <ul>
    <li>Một phương pháp, một bố cục. Cấu trúc là Giai đoạn 2; chuyển giao là Giai đoạn 4.</li>
    <li>Hiệu ứng trần: R = 1.00 tại D = 1 trên gần như mọi ô N vừa/lớn.</li>
    <li>Hợp nhất trộn ô xác nhận 100 mẫu với ô dò đường 30 mẫu (theo thiết kế).</li>
  </ul>

  <h2 id="next"><span class="tag tag-out">TIẾP</span> Tiếp</h2>
  <p>Giai đoạn 2 cấu trúc. Tổng hợp: <span class="mono">../../summary/SUMMARY_REPORT_vi.html</span>.</p>

  <h2 id="raw-data"><span class="tag tag-plan">PHỤ LỤC</span> Dữ liệu thô</h2>
  <table>
    <thead><tr><th>Đường dẫn</th><th>Nội dung</th></tr></thead>
    <tbody>
      <tr><td><span class="mono">../claim/merged_trials.csv</span></td><td>Hợp nhất 4,540 dòng</td></tr>
      <tr><td><span class="mono">../claim/packages/a/</span></td><td>Gói A</td></tr>
      <tr><td><span class="mono">../claim/packages/f/</span></td><td>Gói F</td></tr>
      <tr><td><span class="mono">../claim/README.md</span></td><td>README thư mục</td></tr>
      <tr><td><span class="mono">../t1/README.md</span></td><td>Ghi chú T1 bỏ qua</td></tr>
    </tbody>
  </table>
'''
    return wrap(
        "vi",
        "1",
        "Giai đoạn 1: bản đồ kích thước",
        "Bản đồ mức xác nhận: đàn tập trung cần bao nhiêu chó khi N tăng, dưới giao thức scaling_v2.",
        P1_NAV_VI,
        "REPORT_en.html",
        "Bản tiếng Anh",
        body,
    )


def main() -> None:
    write(ROOT / "phase4/guides/REPORT_en.html", phase4_en())
    write(ROOT / "phase4/guides/REPORT_vi.html", phase4_vi())
    write(ROOT / "phase2/guides/REPORT_en.html", phase2_en())
    write(ROOT / "phase2/guides/REPORT_vi.html", phase2_vi())
    write(ROOT / "phase1/guides/REPORT_en.html", phase1_en())
    write(ROOT / "phase1/guides/REPORT_vi.html", phase1_vi())


if __name__ == "__main__":
    main()
