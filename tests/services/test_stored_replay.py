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
    ("layout", "n", "d", "seed_index"),
    [("compact", 100, 1, 0), ("compact", 200, 6, 0), ("wide", 50, 3, 0)],
)
def test_a_stored_study_trial_replays_exactly(layout: str, n: int, d: int, seed_index: int) -> None:
    job = open_run(RUN).job("strombom_multi", layout, n, d, seed_index)
    result = replay_trial(job)
    assert (result.success, result.total_ticks) == job.stored
