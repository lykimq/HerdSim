"""Scaling analysis package for shepherding herdability protocols."""

from analysis.scaling.early_warning import evaluate_early_warning
from analysis.scaling.export import export_package_a, export_package_dossier
from analysis.scaling.frontier import extract_frontier
from analysis.scaling.mechanism import evaluate_overcrowding_mechanisms
from analysis.scaling.predictors import compare_state_vs_nd_predictors
from analysis.scaling.provenance import build_provenance_stamp
from analysis.scaling.regimes import label_regimes
from analysis.scaling.fits import fit_scaling_models
from analysis.scaling.substitution import substitution_curves
from analysis.scaling.transfer import build_transfer_table

__all__ = [
    "build_provenance_stamp",
    "extract_frontier",
    "label_regimes",
    "export_package_a",
    "export_package_dossier",
    "compare_state_vs_nd_predictors",
    "evaluate_overcrowding_mechanisms",
    "build_transfer_table",
    "substitution_curves",
    "fit_scaling_models",
    "evaluate_early_warning",
]
