"""Figures of the results, drawn from runs under results/.

    uv run python docs/generate_docs/make_result_figures.py

Writes PNGs via result_figures.py; skips a figure when its run folder is missing.
Style and log/N-axis helpers in figstyle.py. Captions live in the report and README.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from docs.generate_docs.result_figures import (  # noqa: E402
    fig_deadline,
    fig_dmin_vs_n,
    fig_growth_fits,
)

FIGURES = (fig_dmin_vs_n, fig_deadline, fig_growth_fits)


def main() -> None:
    for draw in FIGURES:
        draw()


if __name__ == "__main__":
    main()
