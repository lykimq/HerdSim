"""Unit test for local density gradient diagnostic."""

import numpy as np
import pytest

from cli.diagnostics.gradient_validation import (
    evaluate_flock_gradient_error,
    run_gradient_validation,
)


def test_evaluate_gradient_error_on_symmetric_flock():
    # Symmetric 4-point flock + 1 central point
    # Outer sheep at (+-10, 0) and (0, +-10)
    # Centroid is (0, 0).
    flock = np.array([
        [0.0, 0.0],
        [10.0, 0.0],
        [-10.0, 0.0],
        [0.0, 10.0],
        [0.0, -10.0],
    ])
    # With k=3 neighbors, neighbors include center (0, 0) and 2 adjacent outer sheep
    errors = evaluate_flock_gradient_error(flock, k_neighbors=3, outer_only=True)
    assert len(errors) == 4
    # Symmetrically, each outer sheep's local sum points directly toward origin (0, 0)
    for err in errors:
        assert err == pytest.approx(0.0, abs=1e-5)



def test_run_gradient_validation_structure():
    results = run_gradient_validation(
        flock_sizes=(25,),
        layouts=("compact",),
        k_values=(5,),
        n_seeds=2,
    )
    assert "compact" in results
    assert 25 in results["compact"]
    assert 5 in results["compact"][25]
    stats = results["compact"][25][5]
    assert "mean_deg" in stats
    assert "median_deg" in stats
    assert 0.0 <= stats["mean_deg"] <= 180.0
