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
    fig_fat,
    fig_hungarian_matching,
    fig_independent,
    fig_kubo,
    fig_lama,
    fig_layouts,
    fig_sheep_forces,
    fig_task_geometry,
    fig_team_rule,
    fig_trial,
)

FIGURES = (
    fig_sheep_forces,
    fig_team_rule,
    fig_hungarian_matching,
    fig_driving_arc,
    fig_fat,
    fig_independent,
    fig_kubo,
    fig_lama,
    fig_task_geometry,
    fig_layouts,
    fig_dog_starts,
    fig_trial,
)


def main() -> None:
    for draw in FIGURES:
        draw()


if __name__ == "__main__":
    main()
