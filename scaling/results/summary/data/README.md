# Data appendices

This directory is the reproducible index for Phase 1, Phase 2, Phase 4, and Phase 5 evidence. Tables are generated directly from canonical CSV, JSON, status, and provenance artifacts. No reported number is entered by hand.

## Contents

* [Run ledger](run_ledger.md): pilot, scout, and claim grades; row counts; protocol hashes; provenance links.
* [Phase 1 tables](phase1_tables.md): size frontiers, regimes, scaling fits, and merge summaries.
* [Phase 2 tables](phase2_tables.md): layout frontiers, one-dog costs, predictors, and merge summaries.
* [Phase 4 tables](phase4_tables.md): Kubo and FAT transfer, hard failures, the difficult Kubo window, and merge summaries.
* Phase 5 observation / range / communication campaigns are listed in the [run ledger](run_ledger.md); Package E tables live under `phase5/*/packages/e/`.
* [Vietnamese index](README_vi.md).

## Evidence convention

Scout is the 30-seed broad map used to choose precision windows. Claim is the precision grade, usually 100 seeds, used for conclusions. A claim merge replaces scout rows in reseeded cells and retains scout rows elsewhere. Conclusions must therefore preserve the grade of each cell.

`D_max = 35` with blank `D_overcrowd` means reliability remained above threshold at the top of the tested grid. If `hard_failure = True`, no tested D reached R = 0.90, so no D_max may be inferred.

## Rebuild

Tables in this directory are frozen artifacts from the completed campaign. Regenerators were removed; edit the Markdown files directly if a correction is needed.
