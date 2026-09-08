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
        "id": "mean_cohesion",
        "label": "Mean cohesion",
        "description": "Average final-tick flock cohesion in world units (mean sheep distance to GCM).",
    },
    {
        "id": "mean_shepherd_path",
        "label": "Mean path",
        "description": "Average final-tick cumulative shepherd travel distance in world units.",
    },
    {
        "id": "mean_gcm_goal",
        "label": "Mean GCM-goal",
        "description": "Average final-tick distance from flock GCM to goal centre, in world units.",
    },
]

# Per-trial columns written by Export CSV (final-tick snapshot + run metadata).
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
    {"id": "total_ticks", "description": "Simulation ticks executed before success or timeout (not wall-clock time)."},
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
            "Final-tick time_to_goal: simulation tick if ALL sheep are inside the goal, "
            "else -1 (strict full-goal metric; not wall-clock time)."
        ),
    },
    {
        "id": "success_rate",
        "description": (
            "Final-tick fraction of sheep inside the goal zone (0-1). "
            "This is occupancy, not the boolean trial success column."
        ),
    },
    {
        "id": "cohesion",
        "description": "Final-tick mean sheep distance to flock centroid, in world units.",
    },
    {
        "id": "gcm_goal",
        "description": "Final-tick distance from flock GCM to goal centre, in world units.",
    },
    {
        "id": "shepherd_path",
        "description": "Final-tick cumulative shepherd travel distance, in world units.",
    },
    {
        "id": "polarization",
        "description": "Final-tick mean sheep heading alignment (0-1, unitless).",
    },
    {
        "id": "outlier_count",
        "description": "Final-tick count of sheep beyond r_a * N^(2/3) from the GCM.",
    },
    {
        "id": "min_separation",
        "description": "Final-tick minimum pairwise sheep distance, in world units.",
    },
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
