"""The paper's experiments through HerdSim's engine: grid, seeds and stored trials."""

from __future__ import annotations

import pytest

from paper_check import settings as paper
from paper_check.sweep import fig3_counts, read
from paper_check.trials import run_fig3_trial, seed_of


def test_every_flock_size_ends_at_the_global_case() -> None:
    for n_sheep in paper.FLOCK_SIZES:
        counts = fig3_counts(n_sheep)
        assert counts == sorted(set(counts))
        assert counts[-1] == n_sheep - 1


def test_the_global_case_finishes_the_paper_task() -> None:
    # Strombom et al. (2014) Fig. 3: with n = N - 1 the dog always brings the flock in.
    trial = run_fig3_trial(20, 19, seed_of(20, 0))
    assert trial.success
    assert trial.steps < paper.MAX_STEPS


@pytest.mark.parametrize("success", [True, False])
def test_the_engine_replays_a_stored_fig3_trial(success: bool) -> None:
    stored = read("fig3")
    row = stored[(stored["n_sheep"] == 20) & (stored["success"] == success)].iloc[0]
    trial = run_fig3_trial(20, int(row["n_neighbors"]), int(row["seed"]))
    assert (trial.success, trial.steps) == (bool(row["success"]), int(row["steps"]))
