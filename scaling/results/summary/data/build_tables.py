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
    dimensions = [
        ("Rows" if not vi else "So dong", len(rows)),
        ("Columns" if not vi else "So cot", len(columns)),
        ("Design cells" if not vi else "So o thiet ke", len(cells)),
        ("Methods" if not vi else "Phuong phap", sorted_unique(rows, "method")),
        ("Layouts" if not vi else "Bo cuc", sorted_unique(rows, "initial_layout")),
        ("N values" if not vi else "Cac gia tri N", sorted_unique(rows, "n_sheep")),
        ("D values" if not vi else "Cac gia tri D", sorted_unique(rows, "n_shepherds")),
        ("Seed range" if not vi else "Khoang seed", seed_range(rows)),
    ]
    aggregates = [
        ("Successes" if not vi else "Thanh cong", len(successes)),
        ("Failures" if not vi else "That bai", len(rows) - len(successes)),
        ("Overall R" if not vi else "R toan bo", len(successes) / len(rows) if rows else None),
        ("Median ticks, successes" if not vi else "Trung vi tick, ca thanh cong", statistics.median(ticks) if ticks else None),
        ("P90 ticks, successes" if not vi else "P90 tick, ca thanh cong", quantile(ticks, 0.9)),
        ("Median path, successes" if not vi else "Trung vi quang duong, ca thanh cong", statistics.median(paths) if paths else None),
        ("Failure modes" if not vi else "Nhan that bai", ", ".join(f"{key}: {value}" for key, value in sorted(failures.items())) or "none"),
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
            f"Nguon day du: {linked_source(relative)}. Bang lon khong duoc chep lai. "
            "Cac thong ke duoi day duoc tinh truc tiep tu CSV."
        )
        selection = (
            "Quy tac chon dong dai dien: sap xep tu dien theo `method`, `initial_layout`, "
            "`n_sheep`, `n_shepherds`, `seed`, sau do lay 5 vi tri cach deu, gom hai dau. "
            "Quy tac nay trung lap duoc va khong chon theo ket qua."
        )
        labels = ("Thuoc tinh", "Gia tri")
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


def seed_range(rows: Sequence[dict[str, str]]) -> str:
    seeds = sorted(
        int(value)
        for row in rows
        if (value := as_float(row.get("seed"))) is not None
    )
    if not seeds:
        return ""
    return f"{seeds[0]} to {seeds[-1]}"


def schema_section(vi: bool) -> str:
    if vi:
        title = "## Luoc do cua cac bang merged_trials"
        text = (
            "Moi dong la mot lan mo phong voi mot seed. Ten cot thuc te duoc bao cao "
            "trong tung muc du lieu; cac nhom sau giai thich y nghia."
        )
        headers = ("Nhom", "Cot va y nghia")
        rows = (
            ("Danh tinh va thiet ke", SCHEMA_GROUPS[0][1]),
            ("Ket qua va chi phi", SCHEMA_GROUPS[1][1]),
            ("Trang thai cuoi", SCHEMA_GROUPS[2][1]),
            ("Tom tat theo thoi gian", SCHEMA_GROUPS[3][1]),
            ("Chan doan that bai", SCHEMA_GROUPS[4][1]),
            ("Cau hinh", SCHEMA_GROUPS[5][1]),
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
    title = "# Phase 1 data tables" if not vi else "# Bang du lieu Giai doan 1"
    grade = (
        "All scientific result tables in this appendix use the claim merge. Scout data are "
        "planning evidence only and are listed separately in the run ledger."
        if not vi
        else "Tat ca bang ket qua khoa hoc trong phu luc nay dung merge claim. Du lieu scout "
        "chi de lap ke hoach va duoc liet ke rieng trong so cai chay."
    )
    frontier_note = (
        "`D_max = 35` is the tested-grid ceiling because `D_overcrowd` is empty. It is not "
        "an observed upper failure boundary."
        if not vi
        else "`D_max = 35` la tran cua luoi da thu vi `D_overcrowd` trong. Day khong phai "
        "bien that bai tren da quan sat."
    )
    regime_rows = sorted((key or "blank", value) for key, value in regime_counts.items())
    cv = complete_csv_table(cv_path)
    fits = complete_csv_table(fits_path, ("model", "rmse", "aic", "bic", "params"))
    sections = [
        title,
        grade,
        "## Frontier by flock size" if not vi else "## Bien theo kich thuoc dan",
        f"Source: {linked_source(frontier_path)}.",
        complete_csv_table(frontier_path),
        frontier_note,
        "## Complete D_min bootstrap intervals" if not vi else "## Khoang bootstrap D_min day du",
        f"Source: {linked_source(bootstrap_path)}.",
        complete_csv_table(
            bootstrap_path,
            ("initial_layout", "n_sheep", "d_min", "d_min_ci_low", "d_min_ci_high", "n_boot", "n_seeds_ref", "n_boot_defined"),
        ),
        "## Regime counts" if not vi else "## So luong che do",
        f"Source: {linked_source(regimes_path)}.",
        table(("Regime", "Cells") if not vi else ("Che do", "So o"), regime_rows),
        "## Scaling model evidence" if not vi else "## Bang chung mo hinh scaling",
        f"Cross-validation source: {linked_source(cv_path)}.",
        cv,
        f"Fit source: {linked_source(fits_path)}.",
        fits,
        schema_section(vi),
        "## Claim merged trials" if not vi else "## Trial merge claim",
        merged_summary("phase1/claim/merged_trials.csv", vi),
        "## Direct sources" if not vi else "## Nguon truc tiep",
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
        else ("Bo cuc", "N", "Thanh cong", "Seed", "R", "Trung vi tick", "Trung vi path")
    )
    return table(headers, output)


def phase2(vi: bool) -> str:
    frontier_path = "phase2/claim/packages/b/frontier_by_layout.csv"
    bootstrap_path = "phase2/claim/merged_dmin_bootstrap.csv"
    predictor_path = "phase2/claim/packages/b/predictor_comparison.csv"
    title = "# Phase 2 data tables" if not vi else "# Bang du lieu Giai doan 2"
    grade = (
        "Claim evidence is used for results. Scout evidence selected the precision windows "
        "and must not be read as the final estimate."
        if not vi
        else "Bang ket qua dung bang chung claim. Bang chung scout chon cua so chinh xac "
        "va khong duoc doc nhu uoc luong cuoi."
    )
    note = (
        "Every layout and N has `D_min = 1`, `D_max = 35` at the grid ceiling, and no "
        "overcrowding. Wide layouts have `B_star_D = 2` even though one dog is reliable."
        if not vi
        else "Moi bo cuc va N co `D_min = 1`, `D_max = 35` tai tran luoi, va khong co "
        "overcrowding. Bo cuc wide co `B_star_D = 2` du mot cho da dat do tin cay."
    )
    sections = [
        title,
        grade,
        "## Complete layout frontier" if not vi else "## Bien day du theo bo cuc",
        f"Source: {linked_source(frontier_path)}.",
        complete_csv_table(frontier_path),
        note,
        "## Complete D_min bootstrap intervals" if not vi else "## Khoang bootstrap D_min day du",
        f"Source: {linked_source(bootstrap_path)}.",
        complete_csv_table(
            bootstrap_path,
            ("method", "initial_layout", "n_sheep", "d_min", "d_min_ci_low", "d_min_ci_high", "n_boot", "n_seeds_ref", "n_boot_defined"),
        ),
        "## One-dog cost by layout" if not vi else "## Chi phi mot cho theo bo cuc",
        (
            "Computed from all D = 1 claim-merge rows. Medians use successful trials only."
            if not vi
            else "Tinh tu tat ca dong D = 1 cua claim merge. Trung vi chi dung trial thanh cong."
        ),
        phase2_cost_table(vi),
        "## Predictor comparison" if not vi else "## So sanh predictor",
        f"Source: {linked_source(predictor_path)}. "
        + (
            "This table is retained as evidence, but the state-predictor claim is inconclusive "
            "because the baseline D_min did not shift."
            if not vi
            else "Bang nay duoc giu lam bang chung, nhung claim predictor trang thai khong "
            "ket luan vi D_min baseline khong thay doi."
        ),
        complete_csv_table(predictor_path),
        schema_section(vi),
        "## Claim merged trials" if not vi else "## Trial merge claim",
        merged_summary("phase2/claim/merged_trials.csv", vi),
        "## Direct sources" if not vi else "## Nguon truc tiep",
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
        (int(dog_count), values["n"], values["R"], values["R"] >= 0.9)
        for dog_count, values in sorted(
            window["claim_seeds_by_D"].items(), key=lambda item: int(item[0])
        )
    ]
    title = "# Phase 4 data tables" if not vi else "# Bang du lieu Giai doan 4"
    grade = (
        "Controller conclusions use claim merges. Scout grids remain planning evidence. "
        "The Package D tables compare claim-grade controller results."
        if not vi
        else "Ket luan ve controller dung claim merge. Luoi scout van chi la bang chung "
        "lap ke hoach. Bang Package D so sanh ket qua controller cap claim."
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
        "## Compact-start size frontiers" if not vi else "## Bien kich thuoc voi bo cuc compact",
        f"Kubo source: {linked_source(kubo_frontier)}.",
        compact_frontier(kubo_frontier),
        f"FAT source: {linked_source(fat_frontier)}.",
        compact_frontier(fat_frontier),
        (
            "Blank frontier fields with `hard_failure = True` mean no tested D reached R = 0.90. "
            "They are not an upper-bound estimate."
            if not vi
            else "Cac truong bien trong voi `hard_failure = True` nghia la khong D nao dat "
            "R = 0.90. Chung khong phai uoc luong gioi han tren."
        ),
        "## Complete size D_min bootstrap intervals" if not vi else "## Khoang bootstrap D_min kich thuoc day du",
        f"Kubo source: {linked_source(kubo_bootstrap)}.",
        complete_csv_table(
            kubo_bootstrap,
            ("initial_layout", "n_sheep", "d_min", "d_min_ci_low", "d_min_ci_high", "n_boot", "n_seeds_ref", "n_boot_defined"),
        ),
        f"FAT source: {linked_source(fat_bootstrap)}.",
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
        "## Complete controller and layout frontier" if not vi else "## Bien day du theo controller va bo cuc",
        f"Source: {linked_source(structure_frontier)}.",
        complete_csv_table(structure_frontier, structure_columns),
        "## Kubo outlier-rich, N = 200" if not vi else "## Kubo outlier-rich, N = 200",
        f"Source: {linked_source(window_path)}.",
        table(
            ("D", "Seeds", "R", "R >= 0.90"),
            window_rows,
        ),
        (
            f"Point D_min: {fmt(window['d_min'])}. Bootstrap interval: "
            f"[{fmt(window['d_min_ci'][0])}, {fmt(window['d_min_ci'][1])}]. "
            "The D = 35 value has 30 scout seeds because that cell was not claim-reseeded; "
            "the D = 1 through 25 values shown above have 200 claim seeds."
            if not vi
            else f"D_min diem: {fmt(window['d_min'])}. Khoang bootstrap: "
            f"[{fmt(window['d_min_ci'][0])}, {fmt(window['d_min_ci'][1])}]. "
            "Gia tri D = 35 co 30 seed scout vi o nay khong duoc gieo lai claim; "
            "cac gia tri D = 1 den 25 o tren co 200 seed claim."
        ),
        "## Complete size-transfer evidence" if not vi else "## Bang chung transfer kich thuoc day du",
        f"Summary source: {linked_source(transfer_summary)}.",
        complete_csv_table(transfer_summary),
        f"Detailed source: {linked_source(transfer_table)}.",
        complete_csv_table(transfer_table),
        schema_section(vi),
    ]
    for label, relative in MERGED[2:]:
        heading = f"## {label} claim merge" if not vi else f"## Claim merge: {label}"
        sections.extend((heading, merged_summary(relative, vi)))
    sections.extend(
        (
            "## Direct sources" if not vi else "## Nguon truc tiep",
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
                phase,
                grade,
                status.get("protocol_id", ""),
                status.get("n_done", ""),
                status.get("n_rows_trials_csv", ""),
                status.get("complete", ""),
                provenance.get("n_seeds", ""),
                provenance.get("created_at", ""),
                status.get("finished_at", ""),
                provenance.get("git_hash", ""),
                protocol_hash,
                f"[status]({rel_link(status_path)})",
                f"[provenance]({rel_link(provenance_path)})",
            )
        )
    merged_rows = []
    for label, relative in MERGED:
        columns, data = read_csv(relative)
        merged_rows.append(
            (
                label,
                len(data),
                len(columns),
                file_sha256(source(relative)),
                linked_source(relative),
            )
        )
    title = "# Run ledger" if not vi else "# So cai cac lan chay"
    intro = (
        "This ledger preserves execution grade and provenance. Scout runs map the broad grid "
        "and select windows. Claim runs provide the precision evidence used for scientific "
        "statements. Pilot runs are pipeline checks. A claim merge replaces scout rows only "
        "where claim reseeding exists, so a merge can legitimately contain both grades."
        if not vi
        else "So cai nay giu cap chay va provenance. Scout lap ban do luoi rong va chon cua so. "
        "Claim cung cap bang chung chinh xac dung cho phat bieu khoa hoc. Pilot kiem tra pipeline. "
        "Claim merge chi thay dong scout tai o co gieo lai claim, vi vay merge co the chua ca hai cap."
    )
    caveat = (
        "The Kubo structure claim status records 4,000 completed rows although its original "
        "`n_planned` field is 600. The status and provenance links are retained verbatim; the "
        "current merged evidence is summarized below."
        if not vi
        else "Status claim Kubo structure ghi 4,000 dong hoan thanh du truong `n_planned` ban dau "
        "la 600. Lien ket status va provenance duoc giu nguyen; bang chung merge hien tai duoc "
        "tom tat o duoi."
    )
    headers = (
        ("Phase", "Grade", "Protocol", "Done", "Trial rows", "Complete", "Seeds", "Created", "Finished", "Git hash", "Protocol hash", "Status", "Provenance")
        if not vi
        else ("Giai doan", "Cap", "Protocol", "Da chay", "Dong trial", "Hoan tat", "Seed", "Tao luc", "Xong luc", "Git hash", "Protocol hash", "Status", "Provenance")
    )
    merged_headers = (
        ("Claim merge", "Rows", "Columns", "SHA256", "Full source")
        if not vi
        else ("Claim merge", "So dong", "So cot", "SHA256", "Nguon day du")
    )
    protocol_text = (
        "Protocol hashes present: " if not vi else "Protocol hash hien co: "
    ) + ", ".join(sorted(protocol_hashes))
    return "\n\n".join(
        (
            title,
            intro,
            table(headers, rows),
            caveat,
            protocol_text,
            "## Claim merge inventory" if not vi else "## Kiem ke claim merge",
            (
                "SHA256 values identify the exact raw CSV bytes used at generation time."
                if not vi
                else "Gia tri SHA256 nhan dien chinh xac byte CSV tho khi tao phu luc."
            ),
            table(merged_headers, merged_rows),
        )
    ) + "\n"


def readme(vi: bool) -> str:
    if vi:
        return """# Phu luc du lieu

Thu muc nay la muc luc tai tao duoc cho bang chung cua Giai doan 1, 2 va 4. Cac bang duoc tao truc tiep tu CSV, JSON, status va provenance chinh tac. Khong co so nao duoc nhap tay.

## Cach doc

* [So cai chay](run_ledger_vi.md): cap pilot, scout, claim; so dong; hash protocol; lien ket provenance.
* [Bang Giai doan 1](phase1_tables_vi.md): bien kich thuoc, che do, fit scaling va tom tat merge.
* [Bang Giai doan 2](phase2_tables_vi.md): bien theo bo cuc, chi phi mot cho, predictor va tom tat merge.
* [Bang Giai doan 4](phase4_tables_vi.md): transfer Kubo va FAT, hard failure, cua so Kubo kho va tom tat merge.
* [English index](README.md).

## Quy uoc bang chung

Scout la ban do 30 seed dung de chon cua so. Claim la bang chung chinh xac, thuong 100 seed, va la cap dung cho ket luan. Merge claim thay dong scout tai cac o da gieo lai claim va giu scout tai cac o con lai. Vi vay moi ket luan phai giu ro cap cua tung o.

`D_max = 35` voi `D_overcrowd` trong chi co nghia la thanh cong van dat nguong tai dinh luoi da thu. Neu `hard_failure = True`, khong D nao trong luoi dat R = 0.90, nen khong duoc dien mot `D_max` gia.

## Tai tao

Chay `python3 build_tables.py` trong thu muc nay. Chay `python3 build_tables.py --check` de xac nhan cac tep da tao trung khop voi nguon hien tai. Script chi ghi 10 tep Markdown trong thu muc nay.
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
        try:
            text.encode("ascii")
        except UnicodeEncodeError as error:
            raise ValueError(f"{name} contains non-ASCII text") from error
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
            or (DATA_DIR / name).read_text(encoding="ascii") != content
        ]
        if stale:
            print("Stale generated files: " + ", ".join(stale), file=sys.stderr)
            return 1
        print(f"Verified {len(outputs)} generated Markdown files.")
        return 0
    for name, content in outputs.items():
        (DATA_DIR / name).write_text(content, encoding="ascii", newline="\n")
    print(f"Wrote {len(outputs)} generated Markdown files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
