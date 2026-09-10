"""Benchmark metric definitions shared by UI summary and CSV export."""

from __future__ import annotations

# Columns shown in the Analytics summary table / charts.
SUMMARY_METRIC_DEFS: list[dict[str, str]] = [
    {
        "id": "algorithm",
        "label": "Algorithm",
        "description": "Algorithm id compared in this benchmark.",
    },
    {
        "id": "trials",
        "label": "Trials",
        "description": "Number of seeds run for this algorithm.",
    },
    {
        "id": "success_rate",
        "label": "Success",
        "description": "Share of trials that met the scenario success criterion before max ticks.",
    },
    {
        "id": "failure_rate",
        "label": "Failure",
        "description": "Share of trials that timed out without meeting the scenario criterion.",
    },
    {
        "id": "mean_ticks_success",
        "label": "Mean ticks",
        "description": "Average total_ticks over successful trials only, in simulation ticks (n/a if none).",
    },
    {
        "id": "median_ticks_success",
        "label": "Median ticks",
        "description": "Median total_ticks over successful trials only, in simulation ticks (n/a if none).",
    },
    {
        "id": "iqr_ticks_success",
        "label": "IQR ticks",
        "description": "Interquartile range of total_ticks over successful trials (n/a if fewer than two).",
    },
    {
        "id": "mean_auc_cohesion",
        "label": "AUC cohesion",
        "description": "Mean over trials of auc_cohesion (mean cohesion over ticks in each run).",
    },
    {
        "id": "mean_auc_fragmentation",
        "label": "AUC fragment",
        "description": "Mean over trials of auc_fragmentation (mean largest-component fraction over ticks).",
    },
    {
        "id": "mean_shepherd_path",
        "label": "Mean path",
        "description": "Average end-of-run cumulative shepherd travel distance in world units.",
    },
    {
        "id": "mean_control_efficiency",
        "label": "Ctrl eff.",
        "description": "Average goal progress per unit shepherd travel (gcm_start - gcm_end) / path.",
    },
    {
        "id": "mean_final_gcm_goal",
        "label": "Final GCM-goal",
        "description": "Average end-of-run distance from flock GCM to goal centre, in world units.",
    },
]

# Per-trial columns written by Export CSV.
CSV_COLUMN_DEFS: list[dict[str, str]] = [
    {"id": "sweep_label", "description": "Param-grid label when Analytics ran a sweep (empty otherwise)."},
    {"id": "algorithm", "description": "Algorithm id for this trial."},
    {"id": "scenario", "description": "Scenario id used for this trial."},
    {"id": "preset", "description": "Config preset: paper, scenario, or custom."},
    {"id": "seed", "description": "Random seed for this trial."},
    {"id": "n_sheep", "description": "Number of sheep in the trial."},
    {"id": "n_shepherds", "description": "Number of shepherds/dogs in the trial."},
    {
        "id": "success",
        "description": "True if the scenario success criterion was met before max ticks.",
    },
    {
        "id": "total_ticks",
        "description": "Simulation ticks executed before success or timeout (not wall-clock time).",
    },
    {
        "id": "first_success_tick",
        "description": (
            "First tick when the scenario success criterion was met, or -1 if never. "
            "Uses the scenario rule (which may allow a partial flock). "
            "Distinct from time_to_goal."
        ),
    },
    {
        "id": "time_to_goal",
        "description": (
            "End-of-run time_to_goal: simulation tick if ALL sheep are inside the goal, "
            "else -1 (strict full-goal metric; not wall-clock time)."
        ),
    },
    {
        "id": "final_success_rate",
        "description": "End-of-run fraction of sheep inside the goal zone (0-1). Occupancy, not trial success.",
    },
    {
        "id": "final_sheep_in_goal",
        "description": "End-of-run count of sheep inside the goal zone.",
    },
    {
        "id": "final_gcm_goal",
        "description": "End-of-run distance from flock GCM to goal centre, in world units.",
    },
    {
        "id": "shepherd_path",
        "description": "End-of-run cumulative shepherd travel distance, in world units.",
    },
    {
        "id": "final_min_separation",
        "description": "End-of-run minimum pairwise sheep distance, in world units.",
    },
    {
        "id": "control_efficiency",
        "description": "Goal progress per unit shepherd travel: (gcm_goal at start - end) / shepherd_path.",
    },
    {"id": "mean_cohesion", "description": "Mean flock cohesion over all ticks in the trial."},
    {"id": "min_cohesion", "description": "Minimum cohesion over ticks in the trial."},
    {"id": "max_cohesion", "description": "Maximum cohesion over ticks in the trial."},
    {"id": "auc_cohesion", "description": "Trajectory AUC of cohesion (mean over ticks)."},
    {"id": "mean_gcm_goal", "description": "Mean GCM-to-goal distance over ticks."},
    {"id": "min_gcm_goal", "description": "Minimum GCM-to-goal distance over ticks."},
    {"id": "max_gcm_goal", "description": "Maximum GCM-to-goal distance over ticks."},
    {"id": "auc_gcm_goal", "description": "Trajectory AUC of GCM-to-goal (mean over ticks)."},
    {"id": "mean_polarization", "description": "Mean polarization over ticks."},
    {"id": "min_polarization", "description": "Minimum polarization over ticks."},
    {"id": "max_polarization", "description": "Maximum polarization over ticks."},
    {"id": "auc_polarization", "description": "Trajectory AUC of polarization (mean over ticks)."},
    {
        "id": "mean_fragmentation",
        "description": "Mean largest-component fraction over ticks (measurement_radius).",
    },
    {"id": "min_fragmentation", "description": "Minimum fragmentation over ticks."},
    {"id": "max_fragmentation", "description": "Maximum fragmentation over ticks."},
    {"id": "auc_fragmentation", "description": "Trajectory AUC of fragmentation (mean over ticks)."},
    {"id": "mean_outlier_count", "description": "Mean outlier_count over ticks."},
    {"id": "min_outlier_count", "description": "Minimum outlier_count over ticks."},
    {"id": "max_outlier_count", "description": "Maximum outlier_count over ticks."},
    {"id": "auc_outlier_count", "description": "Trajectory AUC of outlier_count (mean over ticks)."},
]


def csv_definitions_preamble(columns: list[str] | None = None) -> str:
    """Comment block describing CSV columns (only those present if given)."""
    wanted = set(columns) if columns is not None else None
    lines = ["# HerdSim benchmark CSV column definitions"]
    for item in CSV_COLUMN_DEFS:
        if wanted is not None and item["id"] not in wanted:
            continue
        lines.append(f"# {item['id']}: {item['description']}")
    lines.append("#")
    return "\n".join(lines) + "\n"


def benchmark_definitions_payload() -> dict[str, list[dict[str, str]]]:
    return {
        "summary": SUMMARY_METRIC_DEFS,
        "csv": CSV_COLUMN_DEFS,
    }
