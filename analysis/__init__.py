"""Post-run analysis for the scaling study (Packages A-G except C).

This package turns finished campaign tables (``trials.csv``, merges, trajectories)
into scientific artefacts: frontiers, regime labels, scaling fits, transfer tables,
information ladders, early-warning scores, and package dossiers under
``results/.../packages/``.

What lives here vs elsewhere:
- ``analysis/``: compute and export after simulations finish.
- ``protocols.packaging``: end-of-trial row packaging while writing ``trials.csv``.
- Hand-written protocol-folder ``README.md`` files are not produced here; only
  auto-generated package dossiers (see ``analysis.export``).

Import the public entry points from this module (or from the submodules below).
"""

from analysis.early_warning import (
    evaluate_early_warning,
    evaluate_early_warning_campaign,
)
from analysis.export import export_package_a, export_package_dossier
from analysis.fits import fit_scaling_models
from analysis.frontier import (
    bootstrap_d_min_ci,
    extract_frontier,
    merge_scout_and_claim,
    select_claim_windows,
)
from analysis.predictors import compare_state_vs_nd_predictors
from analysis.regimes import label_regimes
from analysis.substitution import (
    substitution_curves,
    substitution_curves_communication,
    substitution_curves_range,
    summarize_substitution,
)
from analysis.transfer import build_transfer_table, transfer_summary

__all__ = [
    "bootstrap_d_min_ci",
    "build_transfer_table",
    "compare_state_vs_nd_predictors",
    "evaluate_early_warning",
    "evaluate_early_warning_campaign",
    "export_package_a",
    "export_package_dossier",
    "extract_frontier",
    "fit_scaling_models",
    "label_regimes",
    "merge_scout_and_claim",
    "select_claim_windows",
    "substitution_curves",
    "substitution_curves_communication",
    "substitution_curves_range",
    "summarize_substitution",
    "transfer_summary",
]
