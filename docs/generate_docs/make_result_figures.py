"""Figures of the results, drawn from runs under results/.

    uv run python docs/generate_docs/make_result_figures.py

Writes PNGs via result_figures.py; stops with an error when a run folder is missing.
Style and log/N-axis helpers in figstyle.py. Captions live in the report and README.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from docs.generate_docs.paper_figures import FIGURES as PAPER_FIGURES  # noqa: E402
from docs.generate_docs.result_figures import (  # noqa: E402
    fig_deadline,
    fig_densification,
    fig_dmin_vs_n,
    fig_fat,
    fig_growth_fits,
    fig_paired_seeds,
    fig_pruning,
    fig_reach,
    fig_stopping,
)

FIGURES = (
    fig_dmin_vs_n,
    fig_reach,
    fig_deadline,
    fig_growth_fits,
    fig_fat,
    fig_stopping,
    fig_densification,
    fig_pruning,
    fig_paired_seeds,
    *PAPER_FIGURES,
)


def main() -> None:
    for draw in FIGURES:
        draw()


if __name__ == "__main__":
    main()
