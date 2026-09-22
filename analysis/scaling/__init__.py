"""Scaling analysis package for shepherding herdability protocols."""

from analysis.scaling.early_warning import (
    evaluate_early_warning,
    evaluate_early_warning_campaign,
)
from analysis.scaling.export import export_package_a, export_package_dossier
from analysis.scaling.fits import fit_scaling_models
from analysis.scaling.frontier import (
    bootstrap_d_min_ci,
    extract_frontier,
    select_claim_windows,
    select_t1_windows,
)
from analysis.scaling.mechanism import (
    evaluate_overcrowding_mechanisms,
    evaluate_temporal_order,
)
from analysis.scaling.predictors import compare_state_vs_nd_predictors
from analysis.scaling.provenance import build_provenance_stamp
from analysis.scaling.regimes import label_regimes
from analysis.scaling.substitution import substitution_curves
from analysis.scaling.transfer import build_transfer_table

__all__ = [
    "build_provenance_stamp",
    "extract_frontier",
    "select_claim_windows",
    "select_t1_windows",
    "bootstrap_d_min_ci",
    "label_regimes",
    "export_package_a",
    "export_package_dossier",
    "compare_state_vs_nd_predictors",
    "evaluate_overcrowding_mechanisms",
    "evaluate_temporal_order",
    "build_transfer_table",
    "substitution_curves",
    "fit_scaling_models",
    "evaluate_early_warning",
    "evaluate_early_warning_campaign",
]
