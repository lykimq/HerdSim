"""Post-run analysis (frontiers, plots, package export).

End-of-trial packaging used while writing trials.csv lives in ``protocols.packaging``.
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
    select_t1_windows,
)
from analysis.mechanism import (
    evaluate_overcrowding_mechanisms,
    evaluate_temporal_order,
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
    "evaluate_overcrowding_mechanisms",
    "evaluate_temporal_order",
    "export_package_a",
    "export_package_dossier",
    "extract_frontier",
    "fit_scaling_models",
    "label_regimes",
    "merge_scout_and_claim",
    "select_claim_windows",
    "select_t1_windows",
    "substitution_curves",
    "substitution_curves_communication",
    "substitution_curves_range",
    "summarize_substitution",
    "transfer_summary",
]
