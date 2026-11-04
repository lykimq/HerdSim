"""Trials stored by the study still replay exactly with the code as it is.

A test that replays only a trial it has just run cannot see the code drift since the study
ran; these replay rows from a committed results folder, with one dog and with several (the
multi-dog drive is where a last-bit change in the flock radius first shows).
"""

from __future__ import annotations

import pytest

from services.replay import open_run, replay_trial

RUN = "dmin_f99_m6"


@pytest.mark.parametrize(
    ("run", "method", "layout", "n", "d", "seed_index"),
    [
        (RUN, "strombom_multi", "compact", 100, 1, 0),
        (RUN, "strombom_multi", "compact", 200, 6, 0),
        (RUN, "strombom_multi", "wide", 50, 3, 2),
        ("dmin_f99_fat", "fat", "wide", 50, 2, 0),
        ("dmin_f99_indep", "independent", "wide", 50, 2, 0),
    ],
)
def test_a_stored_study_trial_replays_exactly(
    run: str, method: str, layout: str, n: int, d: int, seed_index: int
) -> None:
    job = open_run(run).job(method, layout, n, d, seed_index)
    result = replay_trial(job)
    assert (result.success, result.total_ticks) == job.stored
