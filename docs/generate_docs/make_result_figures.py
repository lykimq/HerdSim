"""Figures of the results, drawn from runs under results/.

    uv run python docs/generate_docs/make_result_figures.py

Writes PNGs via result_figures.py; skips a figure when its run folder is missing.
Style and log/N-axis helpers in figstyle.py. Captions live in the report and README.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from docs.generate_docs.result_figures import (  # noqa: E402
    fig_compact,
    fig_deadline,
    fig_design,
    fig_dmin_vs_n,
    fig_effort,
    fig_fat,
    fig_growth_fits,
    fig_hold_goal,
    fig_lama,
    fig_lama_maps,
    fig_metrics,
    fig_pressure,
    fig_sensitivity,
    fig_spacing,
    fig_split_curves,
    fig_straggler,
    fig_strict_vs_99,
    fig_view,
)

FIGURES = (
    fig_dmin_vs_n,
    fig_deadline,
    fig_straggler,
    fig_strict_vs_99,
    fig_split_curves,
    fig_sensitivity,
    fig_fat,
    fig_metrics,
    fig_compact,
    fig_design,
    fig_effort,
    fig_pressure,
    fig_growth_fits,
    fig_spacing,
    fig_hold_goal,
    fig_view,
    fig_lama,
    fig_lama_maps,
)


def main() -> None:
    for draw in FIGURES:
        draw()


if __name__ == "__main__":
    main()
