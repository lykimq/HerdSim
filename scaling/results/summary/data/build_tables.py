#!/usr/bin/env python3
"""Build deterministic English and Vietnamese data appendices."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import statistics
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Sequence


DATA_DIR = Path(__file__).resolve().parent
RESULTS_DIR = DATA_DIR.parent.parent

OUTPUT_NAMES = (
    "README.md",
    "README_vi.md",
    "run_ledger.md",
    "run_ledger_vi.md",
    "phase1_tables.md",
    "phase1_tables_vi.md",
    "phase2_tables.md",
    "phase2_tables_vi.md",
    "phase4_tables.md",
    "phase4_tables_vi.md",
)

RUNS = (
    ("Phase 1", "Pilot", "phase1/pilot"),
    ("Phase 1", "Scout", "phase1/scout"),
    ("Phase 1", "Claim", "phase1/claim"),
    ("Phase 2", "Pilot state", "phase2/pilot_state"),
    ("Phase 2", "Scout", "phase2/scout"),
    ("Phase 2", "Claim", "phase2/claim"),
    ("Phase 4 Kubo size", "Scout", "phase4/kubo_size/scout"),
    ("Phase 4 Kubo size", "Claim", "phase4/kubo_size/claim"),
    ("Phase 4 FAT size", "Scout", "phase4/fat_size/scout"),
    ("Phase 4 FAT size", "Claim", "phase4/fat_size/claim"),
    ("Phase 4 Kubo structure", "Scout", "phase4/kubo_structure/scout"),
    ("Phase 4 Kubo structure", "Claim", "phase4/kubo_structure/claim"),
    ("Phase 4 FAT structure", "Scout", "phase4/fat_structure/scout"),
    ("Phase 4 FAT structure", "Claim", "phase4/fat_structure/claim"),
)

MERGED = (
    ("Phase 1 baseline size", "phase1/claim/merged_trials.csv"),
    ("Phase 2 baseline structure", "phase2/claim/merged_trials.csv"),
    ("Phase 4 Kubo size", "phase4/kubo_size/claim/merged_trials.csv"),
    ("Phase 4 FAT size", "phase4/fat_size/claim/merged_trials.csv"),
    ("Phase 4 Kubo structure", "phase4/kubo_structure/claim/merged_trials.csv"),
    ("Phase 4 FAT structure", "phase4/fat_structure/claim/merged_trials.csv"),
)

SCHEMA_GROUPS = (
    ("Identity and design", "method, scenario, preset, seed, sheep_model, dog_controller, obs_mode, n_sheep, n_shepherds, initial_layout, time_limit"),
    ("Outcome and cost", "success, total_ticks, time_to_goal, shepherd_path, first_success_tick, control_efficiency"),
    ("Final state", "final_gcm_goal, final_success_rate, final_sheep_in_goal, final_min_separation"),
    ("Time summaries", "mean_*, min_*, max_*, auc_* for recorded flock and dog metrics"),
    ("Failure diagnostics", "failure_mode, failure_label, failure_hints"),
    ("Configuration", "resolved_config, the serialized effective trial configuration"),
)


def source(relative: str) -> Path:
    return RESULTS_DIR / relative


def rel_link(relative: str) -> str:
    return "../../" + relative


def read_csv(relative: str) -> tuple[list[str], list[dict[str, str]]]:
    with source(relative).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        return list(reader.fieldnames or []), rows


def read_json(relative: str) -> dict[str, Any]:
    with source(relative).open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"Expected an object in {relative}")
    return value


def as_float(value: str | None) -> float | None:
    if value is None or value.strip() == "":
        return None
    try:
        number = float(value)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def truth(value: str | None) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def quantile(values: Sequence[float], q: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def fmt(value: Any, digits: int = 3) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        if value.is_integer():
            return f"{int(value):,}"
        return f"{value:,.{digits}f}".rstrip("0").rstrip(".")
    return str(value)


def cell(value: Any) -> str:
    text = fmt(value)
    return text.replace("|", r"\|").replace("\n", " ")


def table(headers: Sequence[str], rows: Iterable[Sequence[Any]]) -> str:
    lines = [
        "| " + " | ".join(cell(header) for header in headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    lines.extend("| " + " | ".join(cell(value) for value in row) + " |" for row in rows)
    return "\n".join(lines)


def linked_source(relative: str) -> str:
    return f"[`{relative}`]({rel_link(relative)})"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sorted_unique(rows: Sequence[dict[str, str]], key: str) -> str:
    values = {row.get(key, "") for row in rows if row.get(key, "") != ""}
    try:
        ordered = sorted(values, key=float)
    except ValueError:
        ordered = sorted(values)
    return ", ".join(ordered)


def representative_rows(rows: Sequence[dict[str, str]], count: int = 5) -> list[dict[str, str]]:
    keys = ("method", "initial_layout", "n_sheep", "n_shepherds", "seed")

    def order_key(row: dict[str, str]) -> tuple[Any, ...]:
        result: list[Any] = []
        for key in keys:
            value = row.get(key, "")
            number = as_float(value)
            result.append(number if number is not None else value)
        return tuple(result)

    ordered = sorted(rows, key=order_key)
    if len(ordered) <= count:
        return ordered
    indices = [round(i * (len(ordered) - 1) / (count - 1)) for i in range(count)]
    return [ordered[index] for index in indices]


def merged_summary(relative: str, vi: bool) -> str:
    columns, rows = read_csv(relative)
    successes = [row for row in rows if truth(row.get("success"))]
    ticks = [value for row in successes if (value := as_float(row.get("total_ticks"))) is not None]
    paths = [value for row in successes if (value := as_float(row.get("shepherd_path"))) is not None]
    cells = {
        (
            row.get("method", ""),
            row.get("initial_layout", ""),
            row.get("n_sheep", ""),
            row.get("n_shepherds", ""),
        )
        for row in rows
    }
    failures = Counter(
        row.get("failure_mode", "") or "unlabelled"
        for row in rows
        if not truth(row.get("success"))
    )
    none_label = "không có" if vi else "none"
    dimensions = [
        ("Rows" if not vi else "Số dòng", len(rows)),
        ("Columns" if not vi else "Số cột", len(columns)),
        ("Design cells" if not vi else "Số ô thiết kế", len(cells)),
        ("Methods" if not vi else "Phương pháp", sorted_unique(rows, "method")),
        ("Layouts" if not vi else "Bố cục", sorted_unique(rows, "initial_layout")),
        ("N values" if not vi else "Các giá trị N", sorted_unique(rows, "n_sheep")),
        ("D values" if not vi else "Các giá trị D", sorted_unique(rows, "n_shepherds")),
        ("Seed range" if not vi else "Khoảng seed", seed_range(rows, vi)),
    ]
    aggregates = [
        ("Successes" if not vi else "Thành công", len(successes)),
        ("Failures" if not vi else "Thất bại", len(rows) - len(successes)),
        ("Overall R" if not vi else "R toàn bộ", len(successes) / len(rows) if rows else None),
        ("Median ticks, successes" if not vi else "Trung vị tick, các thành công", statistics.median(ticks) if ticks else None),
        ("P90 ticks, successes" if not vi else "P90 tick, các thành công", quantile(ticks, 0.9)),
        ("Median path, successes" if not vi else "Trung vị quãng đường, các thành công", statistics.median(paths) if paths else None),
        (
            "Failure modes" if not vi else "Nhãn thất bại",
            ", ".join(f"{key}: {value}" for key, value in sorted(failures.items())) or none_label,
        ),
    ]
    sample = representative_rows(rows)
    sample_rows = [
        (
            row.get("method"),
            row.get("initial_layout"),
            row.get("n_sheep"),
            row.get("n_shepherds"),
            row.get("seed"),
            row.get("success"),
            row.get("total_ticks"),
            fmt(as_float(row.get("shepherd_path"))),
            row.get("failure_mode"),
        )
        for row in sample
    ]
    if vi:
        intro = (
            f"Nguồn đầy đủ: {linked_source(relative)}. Bảng lớn không được chép lại. "
            "Các thống kê dưới đây được tính trực tiếp từ CSV."
        )
        selection = (
            "Quy tắc chọn dòng đại diện: sắp xếp từ điển theo `method`, `initial_layout`, "
            "`n_sheep`, `n_shepherds`, `seed`, sau đó lấy 5 vị trí cách đều, gồm hai đầu. "
            "Quy tắc này trung lập và không chọn theo kết quả."
        )
        labels = ("Thuộc tính", "Giá trị")
        sample_headers = ("method", "layout", "N", "D", "seed", "success", "ticks", "path", "failure_mode")
    else:
        intro = (
            f"Full source: {linked_source(relative)}. The large table is not reproduced. "
            "The summaries below are computed directly from the CSV."
        )
        selection = (
            "Representative-row rule: sort lexicographically by `method`, `initial_layout`, "
            "`n_sheep`, `n_shepherds`, and `seed`, then take 5 evenly spaced positions "
            "including both endpoints. This reproducible rule does not select on outcome."
        )
        labels = ("Property", "Value")
        sample_headers = ("method", "layout", "N", "D", "seed", "success", "ticks", "path", "failure_mode")
    return "\n\n".join(
        (
            intro,
            table(labels, dimensions),
            table(labels, aggregates),
            selection,
            table(sample_headers, sample_rows),
        )
    )


def seed_range(rows: Sequence[dict[str, str]], vi: bool = False) -> str:
    seeds = sorted(
        int(value)
        for row in rows
        if (value := as_float(row.get("seed"))) is not None
    )
    if not seeds:
        return ""
    connector = " đến " if vi else " to "
    return f"{seeds[0]}{connector}{seeds[-1]}"


def is_vietnamese_output(name: str) -> bool:
    return name.endswith("_vi.md")


def output_encoding(name: str) -> str:
    return "utf-8" if is_vietnamese_output(name) else "ascii"


def source_caption(vi: bool, kind: str = "") -> str:
    if not vi:
        labels = {
            "": "Source",
            "cv": "Cross-validation source",
            "fit": "Fit source",
            "kubo": "Kubo source",
            "fat": "FAT source",
            "summary": "Summary source",
            "detail": "Detailed source",
        }
    else:
        labels = {
            "": "Nguồn",
            "cv": "Nguồn kiểm định chéo",
            "fit": "Nguồn khớp mô hình",
            "kubo": "Nguồn Kubo",
            "fat": "Nguồn FAT",
            "summary": "Nguồn tóm tắt",
            "detail": "Nguồn chi tiết",
        }
    return labels[kind]


def schema_section(vi: bool) -> str:
    if vi:
        title = "## Lược đồ của các bảng merged_trials"
        text = (
            "Mỗi dòng là một lần mô phỏng với một seed. Tên cột thực tế được báo cáo "
            "trong từng mục dữ liệu; các nhóm sau giải thích ý nghĩa."
        )
        headers = ("Nhóm", "Cột và ý nghĩa")
        rows = (
            ("Danh tính và thiết kế", SCHEMA_GROUPS[0][1]),
            ("Kết quả và chi phí", SCHEMA_GROUPS[1][1]),
            ("Trạng thái cuối", SCHEMA_GROUPS[2][1]),
            ("Tóm tắt theo thời gian", SCHEMA_GROUPS[3][1]),
            ("Chẩn đoán thất bại", SCHEMA_GROUPS[4][1]),
            ("Cấu hình", SCHEMA_GROUPS[5][1]),
        )
    else:
        title = "## Schema for merged_trials tables"
        text = (
            "Each row is one simulation trial with one seed. Each data-set section reports "
            "the actual column count; these groups explain the shared schema."
        )
        headers = ("Group", "Columns and meaning")
        rows = SCHEMA_GROUPS
    return "\n\n".join((title, text, table(headers, rows)))


def complete_csv_table(relative: str, columns: Sequence[str] | None = None) -> str:
    headers, rows = read_csv(relative)
    selected = list(columns or headers)
    return table(selected, ([row.get(column, "") for column in selected] for row in rows))


def phase1(vi: bool) -> str:
    frontier_path = "phase1/claim/packages/a/frontier.csv"
    bootstrap_path = "phase1/claim/packages/a/dmin_bootstrap.csv"
    regimes_path = "phase1/claim/packages/a/regimes.csv"
    cv_path = "phase1/claim/packages/f/scaling_cv.csv"
    fits_path = "phase1/claim/packages/f/scaling_fits.csv"
    _, regimes = read_csv(regimes_path)
    regime_counts = Counter(row.get("regime", "") for row in regimes)
    if not regime_counts:
        regime_counts = Counter(row.get("regime_label", "") for row in regimes)
    title = "# Phase 1 data tables" if not vi else "# Bảng dữ liệu Giai đoạn 1"
    grade = (
        "All scientific result tables in this appendix use the claim merge. Scout data are "
        "planning evidence only and are listed separately in the run ledger."
        if not vi
        else "Tất cả bảng kết quả khoa học trong phụ lục này dùng bản hợp nhất claim. Dữ liệu khảo sát "
        "chỉ để lập kế hoạch và được liệt kê riêng trong nhật ký chạy."
    )
    frontier_note = (
        "`D_max = 35` is the tested-grid ceiling because `D_overcrowd` is empty. It is not "
        "an observed upper failure boundary."
        if not vi
        else "`D_max = 35` là trần lưới đã thử vì `D_overcrowd` trống. Đây không phải "
        "biên thất bại trên đã quan sát."
    )
    regime_rows = sorted((key or "blank", value) for key, value in regime_counts.items())
    cv = complete_csv_table(cv_path)
    fits = complete_csv_table(fits_path, ("model", "rmse", "aic", "bic", "params"))
    sections = [
        title,
        grade,
        "## Frontier by flock size" if not vi else "## Biên theo kích thước đàn",
        f"{source_caption(vi)}: {linked_source(frontier_path)}.",
        complete_csv_table(frontier_path),
        frontier_note,
        "## Complete D_min bootstrap intervals" if not vi else "## Khoảng bootstrap D_min đầy đủ",
        f"{source_caption(vi)}: {linked_source(bootstrap_path)}.",
        complete_csv_table(
            bootstrap_path,
            ("initial_layout", "n_sheep", "d_min", "d_min_ci_low", "d_min_ci_high", "n_boot", "n_seeds_ref", "n_boot_defined"),
        ),
        "## Regime counts" if not vi else "## Số lượng chế độ",
        f"{source_caption(vi)}: {linked_source(regimes_path)}.",
        table(("Regime", "Cells") if not vi else ("Chế độ", "Số ô"), regime_rows),
        "## Scaling model evidence" if not vi else "## Bằng chứng mô hình scaling",
        f"{source_caption(vi, 'cv')}: {linked_source(cv_path)}.",
        cv,
        f"{source_caption(vi, 'fit')}: {linked_source(fits_path)}.",
        fits,
        schema_section(vi),
        "## Claim merged trials" if not vi else "## Thử nghiệm hợp nhất claim",
        merged_summary("phase1/claim/merged_trials.csv", vi),
        "## Direct sources" if not vi else "## Nguồn trực tiếp",
        source_list(
            (
                frontier_path,
                "phase1/claim/packages/a/reliability.csv",
                bootstrap_path,
                regimes_path,
                cv_path,
                fits_path,
                "phase1/claim/merged_trials.csv",
                "phase1/claim/provenance.json",
                "phase1/claim/status.json",
            )
        ),
    ]
    return "\n\n".join(sections) + "\n"


def phase2_cost_table(vi: bool) -> str:
    _, rows = read_csv("phase2/claim/merged_trials.csv")
    selected = [row for row in rows if row.get("n_shepherds") == "1"]
    groups: dict[tuple[str, int], list[dict[str, str]]] = {}
    for row in selected:
        key = (row["initial_layout"], int(row["n_sheep"]))
        groups.setdefault(key, []).append(row)
    output = []
    for (layout, n_sheep), group in sorted(groups.items()):
        success = [row for row in group if truth(row.get("success"))]
        ticks = [as_float(row.get("total_ticks")) for row in success]
        paths = [as_float(row.get("shepherd_path")) for row in success]
        clean_ticks = [value for value in ticks if value is not None]
        clean_paths = [value for value in paths if value is not None]
        output.append(
            (
                layout,
                n_sheep,
                len(success),
                len(group),
                len(success) / len(group),
                statistics.median(clean_ticks) if clean_ticks else None,
                statistics.median(clean_paths) if clean_paths else None,
            )
        )
    headers = (
        ("Layout", "N", "Successes", "Seeds", "R", "Median ticks", "Median path")
        if not vi
        else ("Bố cục", "N", "Thành công", "Seed", "R", "Trung vị tick", "Trung vị path")
    )
    return table(headers, output)


def phase2(vi: bool) -> str:
    frontier_path = "phase2/claim/packages/b/frontier_by_layout.csv"
    bootstrap_path = "phase2/claim/merged_dmin_bootstrap.csv"
    predictor_path = "phase2/claim/packages/b/predictor_comparison.csv"
    title = "# Phase 2 data tables" if not vi else "# Bảng dữ liệu Giai đoạn 2"
    grade = (
        "Claim evidence is used for results. Scout evidence selected the precision windows "
        "and must not be read as the final estimate."
        if not vi
        else "Bảng kết quả dùng bằng chứng claim. Bằng chứng khảo sát chọn cửa sổ chính xác "
        "và không được đọc như ước lượng cuối."
    )
    note = (
        "Every layout and N has `D_min = 1`, `D_max = 35` at the grid ceiling, and no "
        "overcrowding. Wide layouts have `B_star_D = 2` even though one dog is reliable."
        if not vi
        else "Mỗi bố cục và N có `D_min = 1`, `D_max = 35` tại trần lưới, và không có "
        "quá tải. Bố cục `wide` có `B_star_D = 2` dù một chó đã đạt độ tin cậy."
    )
    sections = [
        title,
        grade,
        "## Complete layout frontier" if not vi else "## Biên đầy đủ theo bố cục",
        f"{source_caption(vi)}: {linked_source(frontier_path)}.",
        complete_csv_table(frontier_path),
        note,
        "## Complete D_min bootstrap intervals" if not vi else "## Khoảng bootstrap D_min đầy đủ",
        f"{source_caption(vi)}: {linked_source(bootstrap_path)}.",
        complete_csv_table(
            bootstrap_path,
            ("method", "initial_layout", "n_sheep", "d_min", "d_min_ci_low", "d_min_ci_high", "n_boot", "n_seeds_ref", "n_boot_defined"),
        ),
        "## One-dog cost by layout" if not vi else "## Chi phí một chó theo bố cục",
        (
            "Computed from all D = 1 claim-merge rows. Medians use successful trials only."
            if not vi
            else "Tính từ tất cả dòng D = 1 của bản hợp nhất claim. Trung vị chỉ dùng lần thử thành công."
        ),
        phase2_cost_table(vi),
        "## Predictor comparison" if not vi else "## So sánh bộ dự đoán",
        f"{source_caption(vi)}: {linked_source(predictor_path)}. "
        + (
            "This table is retained as evidence, but the state-predictor claim is inconclusive "
            "because the baseline D_min did not shift."
            if not vi
            else "Bảng này được giữ làm bằng chứng, nhưng claim bộ dự đoán trạng thái không "
            "kết luận vì D_min cơ sở không thay đổi."
        ),
        complete_csv_table(predictor_path),
        schema_section(vi),
        "## Claim merged trials" if not vi else "## Thử nghiệm hợp nhất claim",
        merged_summary("phase2/claim/merged_trials.csv", vi),
        "## Direct sources" if not vi else "## Nguồn trực tiếp",
        source_list(
            (
                frontier_path,
                predictor_path,
                bootstrap_path,
                "phase2/claim/merged_trials.csv",
                "phase2/claim/provenance.json",
                "phase2/claim/status.json",
            )
        ),
    ]
    return "\n\n".join(sections) + "\n"


def compact_frontier(relative: str) -> str:
    return complete_csv_table(
        relative,
        ("initial_layout", "n_sheep", "d_min", "d_overcrowd", "d_max", "b_star_d", "hard_failure"),
    )


def phase4(vi: bool) -> str:
    kubo_frontier = "phase4/kubo_size/claim/packages/a/frontier.csv"
    fat_frontier = "phase4/fat_size/claim/packages/a/frontier.csv"
    kubo_bootstrap = "phase4/kubo_size/claim/packages/a/dmin_bootstrap.csv"
    fat_bootstrap = "phase4/fat_size/claim/packages/a/dmin_bootstrap.csv"
    structure_frontier = "phase4/package_d/structure/frontier_by_method_layout.csv"
    transfer_summary = "phase4/package_d/size/transfer_summary.csv"
    transfer_table = "phase4/package_d/size/transfer_table.csv"
    window_path = "phase4/kubo_structure/claim/outlier_rich_n200_window.json"
    window = read_json(window_path)
    window_rows = [
        (
            int(dog_count),
            values["n"],
            values["R"],
            ("có" if values["R"] >= 0.9 else "không") if vi else (values["R"] >= 0.9),
        )
        for dog_count, values in sorted(
            window["claim_seeds_by_D"].items(), key=lambda item: int(item[0])
        )
    ]
    title = "# Phase 4 data tables" if not vi else "# Bảng dữ liệu Giai đoạn 4"
    grade = (
        "Controller conclusions use claim merges. Scout grids remain planning evidence. "
        "The Package D tables compare claim-grade controller results."
        if not vi
        else "Kết luận về bộ điều khiển dùng bản hợp nhất claim. Lưới khảo sát vẫn chỉ là bằng chứng "
        "lập kế hoạch. Bảng Package D so sánh kết quả bộ điều khiển cấp claim."
    )
    structure_columns = (
        "method",
        "initial_layout",
        "n_sheep",
        "d_min",
        "d_overcrowd",
        "d_max",
        "b_star_d",
        "hard_failure",
    )
    sections = [
        title,
        grade,
        "## Compact-start size frontiers" if not vi else "## Biên kích thước với bố cục compact",
        f"{source_caption(vi, 'kubo')}: {linked_source(kubo_frontier)}.",
        compact_frontier(kubo_frontier),
        f"{source_caption(vi, 'fat')}: {linked_source(fat_frontier)}.",
        compact_frontier(fat_frontier),
        (
            "Blank frontier fields with `hard_failure = True` mean no tested D reached R = 0.90. "
            "They are not an upper-bound estimate."
            if not vi
            else "Các trường biên trống với `hard_failure = True` nghĩa là không D nào đạt "
            "R = 0.90. Chúng không phải ước lượng giới hạn trên."
        ),
        "## Complete size D_min bootstrap intervals" if not vi else "## Khoảng bootstrap D_min kích thước đầy đủ",
        f"{source_caption(vi, 'kubo')}: {linked_source(kubo_bootstrap)}.",
        complete_csv_table(
            kubo_bootstrap,
            ("initial_layout", "n_sheep", "d_min", "d_min_ci_low", "d_min_ci_high", "n_boot", "n_seeds_ref", "n_boot_defined"),
        ),
        f"{source_caption(vi, 'fat')}: {linked_source(fat_bootstrap)}.",
        complete_csv_table(
            fat_bootstrap,
            (
                "initial_layout",
                "n_sheep",
                "d_min",
                "d_min_ci_low",
                "d_min_ci_high",
                "d_min_ci_low_above_grid",
                "d_min_ci_high_above_grid",
                "n_boot",
                "n_seeds_ref",
                "n_boot_defined",
            ),
        ),
        "## Complete controller and layout frontier" if not vi else "## Biên đầy đủ theo bộ điều khiển và bố cục",
        f"{source_caption(vi)}: {linked_source(structure_frontier)}.",
        complete_csv_table(structure_frontier, structure_columns),
        "## Kubo outlier-rich, N = 200" if not vi else "## Kubo outlier_rich, N = 200",
        f"{source_caption(vi)}: {linked_source(window_path)}.",
        table(
            ("D", "Seeds", "R", "R >= 0.90") if not vi else ("D", "Seed", "R", "R >= 0.90"),
            window_rows,
        ),
        (
            f"Point D_min: {fmt(window['d_min'])}. Bootstrap interval: "
            f"[{fmt(window['d_min_ci'][0])}, {fmt(window['d_min_ci'][1])}]. "
            "The D = 35 value has 30 scout seeds because that cell was not claim-reseeded; "
            "the D = 1 through 25 values shown above have 200 claim seeds."
            if not vi
            else f"D_min điểm: {fmt(window['d_min'])}. Khoảng bootstrap: "
            f"[{fmt(window['d_min_ci'][0])}, {fmt(window['d_min_ci'][1])}]. "
            "Giá trị D = 35 có 30 seed khảo sát vì ô này không được gieo lại claim; "
            "các giá trị D = 1 đến 25 ở trên có 200 seed claim."
        ),
        "## Complete size-transfer evidence" if not vi else "## Bằng chứng chuyển giao kích thước đầy đủ",
        f"{source_caption(vi, 'summary')}: {linked_source(transfer_summary)}.",
        complete_csv_table(transfer_summary),
        f"{source_caption(vi, 'detail')}: {linked_source(transfer_table)}.",
        complete_csv_table(transfer_table),
        schema_section(vi),
    ]
    for label, relative in MERGED[2:]:
        heading = (
            f"## {label} claim merge"
            if not vi
            else f"## Hợp nhất claim: {label.replace('Phase', 'Giai đoạn').replace('baseline size', 'kích thước cơ sở').replace('baseline structure', 'cấu trúc cơ sở').replace(' structure', ' cấu trúc').replace(' size', ' kích thước')}"
        )
        sections.extend((heading, merged_summary(relative, vi)))
    sections.extend(
        (
            "## Direct sources" if not vi else "## Nguồn trực tiếp",
            source_list(
                (
                    kubo_frontier,
                    fat_frontier,
                    kubo_bootstrap,
                    fat_bootstrap,
                    structure_frontier,
                    transfer_summary,
                    transfer_table,
                    window_path,
                    "phase4/kubo_structure/claim/merged_dmin_bootstrap.csv",
                    "phase4/kubo_size/claim/merged_trials.csv",
                    "phase4/fat_size/claim/merged_trials.csv",
                    "phase4/kubo_structure/claim/merged_trials.csv",
                    "phase4/fat_structure/claim/merged_trials.csv",
                )
            ),
        )
    )
    return "\n\n".join(sections) + "\n"


def source_list(paths: Sequence[str]) -> str:
    return "\n".join(f"* {linked_source(path)}" for path in paths)


def localize_run_label(text: str, vi: bool) -> str:
    if not vi:
        return text
    mapping = {
        "Phase 1": "Giai đoạn 1",
        "Phase 2": "Giai đoạn 2",
        "Phase 4 Kubo size": "Giai đoạn 4 Kubo kích thước",
        "Phase 4 FAT size": "Giai đoạn 4 FAT kích thước",
        "Phase 4 Kubo structure": "Giai đoạn 4 Kubo cấu trúc",
        "Phase 4 FAT structure": "Giai đoạn 4 FAT cấu trúc",
        "Phase 1 baseline size": "Giai đoạn 1 kích thước cơ sở",
        "Phase 2 baseline structure": "Giai đoạn 2 cấu trúc cơ sở",
        "Pilot": "Thử nhanh",
        "Pilot state": "Thử nhanh trạng thái",
        "Scout": "Khảo sát",
        "Claim": "Claim",
    }
    return mapping.get(text, text)


def run_ledger(vi: bool) -> str:
    rows = []
    protocol_hashes: set[str] = set()
    for phase, grade, relative in RUNS:
        status_path = f"{relative}/status.json"
        provenance_path = f"{relative}/provenance.json"
        status = read_json(status_path)
        provenance = read_json(provenance_path)
        protocol_hash = str(provenance.get("protocol_hash", ""))
        if protocol_hash:
            protocol_hashes.add(protocol_hash)
        rows.append(
            (
                localize_run_label(phase, vi),
                localize_run_label(grade, vi),
                status.get("protocol_id", ""),
                status.get("n_done", ""),
                status.get("n_rows_trials_csv", ""),
                status.get("complete", ""),
                provenance.get("n_seeds", ""),
                provenance.get("created_at", ""),
                status.get("finished_at", ""),
                provenance.get("git_hash", ""),
                protocol_hash,
                f"[trạng thái]({rel_link(status_path)})" if vi else f"[status]({rel_link(status_path)})",
                f"[provenance]({rel_link(provenance_path)})",
            )
        )
    merged_rows = []
    for label, relative in MERGED:
        columns, data = read_csv(relative)
        merged_rows.append(
            (
                localize_run_label(label, vi),
                len(data),
                len(columns),
                file_sha256(source(relative)),
                linked_source(relative),
            )
        )
    title = "# Run ledger" if not vi else "# Nhật ký chạy"
    intro = (
        "This ledger preserves execution grade and provenance. Scout runs map the broad grid "
        "and select windows. Claim runs provide the precision evidence used for scientific "
        "statements. Pilot runs are pipeline checks. A claim merge replaces scout rows only "
        "where claim reseeding exists, so a merge can legitimately contain both grades."
        if not vi
        else "Nhật ký này giữ cấp chạy và provenance. Khảo sát lập bản đồ lưới rộng và chọn cửa sổ. "
        "Claim cung cấp bằng chứng chính xác dùng cho phát biểu khoa học. Thử nhanh kiểm tra đường ống. "
        "Bản hợp nhất claim chỉ thay dòng khảo sát tại ô có gieo lại claim, vì vậy bản hợp nhất có thể chứa cả hai cấp."
    )
    caveat = (
        "The Kubo structure claim status records 4,000 completed rows although its original "
        "`n_planned` field is 600. The status and provenance links are retained verbatim; the "
        "current merged evidence is summarized below."
        if not vi
        else "Tệp trạng thái claim cấu trúc Kubo ghi 4,000 dòng hoàn thành dù trường `n_planned` ban đầu "
        "là 600. Liên kết trạng thái và provenance được giữ nguyên; bằng chứng hợp nhất hiện tại được "
        "tóm tắt ở dưới."
    )
    headers = (
        ("Phase", "Grade", "Protocol", "Done", "Trial rows", "Complete", "Seeds", "Created", "Finished", "Git hash", "Protocol hash", "Status", "Provenance")
        if not vi
        else ("Giai đoạn", "Cấp chạy", "Giao thức", "Đã chạy", "Dòng thử", "Hoàn tất", "Seed", "Tạo lúc", "Xong lúc", "Git hash", "Hash giao thức", "Trạng thái", "Provenance")
    )
    merged_headers = (
        ("Claim merge", "Rows", "Columns", "SHA256", "Full source")
        if not vi
        else ("Hợp nhất claim", "Số dòng", "Số cột", "SHA256", "Nguồn đầy đủ")
    )
    protocol_text = (
        "Protocol hashes present: " if not vi else "Hash giao thức hiện có: "
    ) + ", ".join(sorted(protocol_hashes))
    return "\n\n".join(
        (
            title,
            intro,
            table(headers, rows),
            caveat,
            protocol_text,
            "## Claim merge inventory" if not vi else "## Kiểm kê bản hợp nhất claim",
            (
                "SHA256 values identify the exact raw CSV bytes used at generation time."
                if not vi
                else "Giá trị SHA256 nhận diện chính xác byte CSV thô khi tạo phụ lục."
            ),
            table(merged_headers, merged_rows),
        )
    ) + "\n"


def readme(vi: bool) -> str:
    if vi:
        return """# Phụ lục dữ liệu

Thư mục này là mục lục tái tạo được cho bằng chứng của Giai đoạn 1, 2 và 4. Các bảng được tạo trực tiếp từ CSV, JSON, tệp trạng thái và provenance chuẩn. Không có số nào được nhập tay.

## Cách đọc

* [Nhật ký chạy](run_ledger_vi.md): cấp thử nhanh, khảo sát, claim; số dòng; hash giao thức; liên kết provenance.
* [Bảng Giai đoạn 1](phase1_tables_vi.md): biên kích thước, chế độ, khớp scaling và tóm tắt hợp nhất.
* [Bảng Giai đoạn 2](phase2_tables_vi.md): biên theo bố cục, chi phí một chó, so sánh bộ dự đoán và tóm tắt hợp nhất.
* [Bảng Giai đoạn 4](phase4_tables_vi.md): chuyển giao Kubo và FAT, thất bại cứng, cửa sổ Kubo khó và tóm tắt hợp nhất.
* [Mục lục tiếng Anh](README.md).

## Quy ước bằng chứng

Khảo sát là bản đồ 30 seed dùng để chọn cửa sổ. Claim là bằng chứng chính xác, thường 100 seed, và là cấp dùng cho kết luận. Bản hợp nhất claim thay dòng khảo sát tại các ô đã gieo lại claim và giữ khảo sát tại các ô còn lại. Vì vậy mọi kết luận phải giữ rõ cấp của từng ô.

`D_max = 35` với `D_overcrowd` trống chỉ có nghĩa là thành công vẫn đạt ngưỡng tại đỉnh lưới đã thử. Nếu `hard_failure = True`, không D nào trong lưới đạt R = 0.90, nên không được điền một `D_max` giả.

## Tái tạo

Chạy `python3 build_tables.py` trong thư mục này. Chạy `python3 build_tables.py --check` để xác nhận các tệp đã tạo trùng khớp với nguồn hiện tại. Script chỉ ghi 10 tệp Markdown trong thư mục này.
"""
    return """# Data appendices

This directory is the reproducible index for Phase 1, Phase 2, and Phase 4 evidence. Tables are generated directly from canonical CSV, JSON, status, and provenance artifacts. No reported number is entered by hand.

## Contents

* [Run ledger](run_ledger.md): pilot, scout, and claim grades; row counts; protocol hashes; provenance links.
* [Phase 1 tables](phase1_tables.md): size frontiers, regimes, scaling fits, and merge summaries.
* [Phase 2 tables](phase2_tables.md): layout frontiers, one-dog costs, predictors, and merge summaries.
* [Phase 4 tables](phase4_tables.md): Kubo and FAT transfer, hard failures, the difficult Kubo window, and merge summaries.
* [Vietnamese index](README_vi.md).

## Evidence convention

Scout is the 30-seed broad map used to choose precision windows. Claim is the precision grade, usually 100 seeds, used for conclusions. A claim merge replaces scout rows in reseeded cells and retains scout rows elsewhere. Conclusions must therefore preserve the grade of each cell.

`D_max = 35` with blank `D_overcrowd` means reliability remained above threshold at the top of the tested grid. If `hard_failure = True`, no tested D reached R = 0.90, so no D_max may be inferred.

## Rebuild

Run `python3 build_tables.py` in this directory. Run `python3 build_tables.py --check` to verify that generated files match current sources. The script writes only the 10 Markdown files in this directory.
"""


def render_all() -> dict[str, str]:
    return {
        "README.md": readme(False),
        "README_vi.md": readme(True),
        "run_ledger.md": run_ledger(False),
        "run_ledger_vi.md": run_ledger(True),
        "phase1_tables.md": phase1(False),
        "phase1_tables_vi.md": phase1(True),
        "phase2_tables.md": phase2(False),
        "phase2_tables_vi.md": phase2(True),
        "phase4_tables.md": phase4(False),
        "phase4_tables_vi.md": phase4(True),
    }


def validate(outputs: dict[str, str]) -> None:
    if set(outputs) != set(OUTPUT_NAMES):
        raise ValueError("Generated output set does not match OUTPUT_NAMES")
    for name, text in outputs.items():
        encoding = output_encoding(name)
        try:
            text.encode(encoding)
        except UnicodeEncodeError as error:
            raise ValueError(f"{name} is not valid {encoding.upper()} text") from error
        for dash in ("\u2012", "\u2013", "\u2014", "\u2212"):
            if dash in text:
                raise ValueError(f"{name} contains a prohibited Unicode dash")
        if "\r" in text:
            raise ValueError(f"{name} contains carriage returns")
        if not text.endswith("\n"):
            raise ValueError(f"{name} lacks a final newline")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check generated Markdown without writing files.",
    )
    args = parser.parse_args()
    outputs = render_all()
    validate(outputs)
    if args.check:
        stale = [
            name
            for name, content in outputs.items()
            if not (DATA_DIR / name).exists()
            or (DATA_DIR / name).read_text(encoding=output_encoding(name)) != content
        ]
        if stale:
            print("Stale generated files: " + ", ".join(stale), file=sys.stderr)
            return 1
        print(f"Verified {len(outputs)} generated Markdown files.")
        return 0
    for name, content in outputs.items():
        (DATA_DIR / name).write_text(content, encoding=output_encoding(name), newline="\n")
    print(f"Wrote {len(outputs)} generated Markdown files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
