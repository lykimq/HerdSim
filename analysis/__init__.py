"""Post-run analysis for the scaling study (Packages A, D, E, F, G).

This package turns finished campaign tables (``trials.csv``, merges, trajectories)
into scientific artefacts: frontiers, regime labels, scaling fits, transfer tables,
information ladders, early-warning scores, and package dossiers under
``results/.../packages/``.

What lives here vs elsewhere:
- ``analysis/``: compute and export after simulations finish.
- ``protocols.packaging``: end-of-trial row packaging while writing ``trials.csv``.
- Hand-written protocol-folder ``README.md`` files are not produced here;
  ``analysis.export`` writes only package CSV tables + ``provenance.json``.

Entry points by package:
- A (size / structure maps): ``export.export_package_a`` (uses ``frontier``, ``regimes``)
- D (transfer, RQ4): ``transfer.build_transfer_table``, ``transfer.transfer_summary``
- E (information ladders, RQ5): ``substitution.substitution_curves``,
  ``substitution.summarize_substitution``
- F (scaling fits, RQ6): ``fits.fit_scaling_models``
- G (early warning, RQ7): ``early_warning.evaluate_early_warning_campaign``
- D-G tables: ``export.export_package_dossier`` writes named CSVs + provenance

Import from the submodules directly; this module does not re-export them, so
importing ``analysis.frontier`` (as the claim planner does) stays light.
"""
