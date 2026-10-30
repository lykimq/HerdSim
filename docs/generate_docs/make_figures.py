"""Figures of the model and the task in the README, drawn from the real code.

    uv run python docs/generate_docs/make_figures.py

Needs matplotlib (the dev extra). Every picture calls the same functions a campaign
uses (start layouts, dog arcs, the team rule, a real trial), so if the code changes, running
this script redraws them. The pictures are written to docs/figures. Flock radii come from
the calibration of the finished runs. The results figures are drawn by make_result_figures.py.

The figures are in model_figures/, one module per topic, and the seed, flock radii and the
helpers that draw the pieces every scene uses are in model_figures/scene.py. Colours, matplotlib
defaults and saving are in figstyle.py. The captions are in the README and report; each
function's docstring says what the figure shows.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from docs.generate_docs.model_figures.models import (  # noqa: E402
    fig_fat,
    fig_kubo,
    fig_lama,
    fig_sheep_forces,
)
from docs.generate_docs.model_figures.task import (  # noqa: E402
    fig_dog_starts,
    fig_layouts,
    fig_task_geometry,
    fig_trial,
)
from docs.generate_docs.model_figures.team_rule import (  # noqa: E402
    fig_driving_arc,
    fig_hungarian_matching,
    fig_independent,
    fig_team_rule,
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
