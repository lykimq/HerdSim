"""Figures of the model and the task, drawn from the real simulation code.

    uv run python docs/generate_docs/make_figures.py

Writes PNGs to docs/figures/ via figures.py. Style and N-axis in figstyle.py.
Captions live in the README and report.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from docs.generate_docs.figures import (  # noqa: E402
    fig_dog_starts,
    fig_driving_arc,
    fig_hungarian_matching,
    fig_layouts,
    fig_sheep_forces,
    fig_task_geometry,
    fig_team_rule,
    fig_trial,
    fig_zones,
)
from docs.generate_docs.paper_figures import fig_paper_layout  # noqa: E402

FIGURES = (
    fig_sheep_forces,
    fig_team_rule,
    fig_hungarian_matching,
    fig_driving_arc,
    fig_task_geometry,
    fig_layouts,
    fig_dog_starts,
    fig_trial,
    fig_zones,
    fig_paper_layout,
)


def main() -> None:
    for draw in FIGURES:
        draw()


if __name__ == "__main__":
    main()
