"""Figures of the results (README findings, report), drawn from the runs in results/.

    uv run python docs/generate_docs/make_result_figures.py

Needs matplotlib (the dev extra). Every figure reads frontier_groups.csv, frontier_cells.csv,
trials.csv or the kept per-tick files of a folder under results/ and is skipped when its folder
is missing.
Shapes carry the success rule (circle strict, square 99 percent) and colour the layout, so the
meaning does not rest on colour alone.

The figures are in result_figures/, one module per topic, and the settings, data access and axis
helpers they share are in result_figures/common.py. Each figure function starts with the runs
and panels it draws, so a figure is changed there; a style shared by several figures is changed
once in common.py. The captions are in the report and README; each function's docstring says
what the figure shows.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from docs.generate_docs.result_figures.design import (  # noqa: E402
    fig_design,
    fig_effort,
    fig_growth_fits,
    fig_pressure,
)
from docs.generate_docs.result_figures.dmin import (  # noqa: E402
    fig_compact,
    fig_deadline,
    fig_dmin_vs_n,
    fig_split_curves,
    fig_straggler,
    fig_strict_vs_99,
)
from docs.generate_docs.result_figures.lama import fig_lama, fig_lama_maps  # noqa: E402
from docs.generate_docs.result_figures.sensitivity import (  # noqa: E402
    fig_fat,
    fig_hold_goal,
    fig_metrics,
    fig_sensitivity,
    fig_spacing,
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
