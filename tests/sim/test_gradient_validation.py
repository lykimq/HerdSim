"""The neighbour-gradient diagnostic (cli/diagnostics/gradient_validation.py)."""

from __future__ import annotations

import numpy as np
import pytest

from cli.diagnostics.gradient_validation import (
    evaluate_flock_gradient_error,
    run_gradient_validation,
)


def test_symmetric_flock_has_no_error():
    # Four sheep on a cross round one at the centre: each outer sheep's three nearest
    # neighbours (the centre and its two side neighbours) sum to a vector straight inward.
    flock = np.array([[0.0, 0.0], [10.0, 0.0], [-10.0, 0.0], [0.0, 10.0], [0.0, -10.0]])
    errors = evaluate_flock_gradient_error(flock, k_neighbors=3, outer_only=True)
    assert len(errors) == 4
    assert errors == pytest.approx(np.zeros(4), abs=1e-5)


def test_results_are_keyed_by_layout_n_and_k():
    results = run_gradient_validation(
        flock_sizes=(25,), layouts=("compact",), k_values=(5,), n_seeds=2
    )
    stats = results["compact"][25][5]
    assert set(stats) == {"mean_deg", "median_deg", "std_deg"}
    assert 0.0 <= stats["mean_deg"] <= 180.0
