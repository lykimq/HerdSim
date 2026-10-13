# Package D: size transfer

Side-by-side compact size-map transfer: Strombom vs Kubo vs FAT, N in {5, 10, 25, 50, 75, 100, 150, 200, 300, 400}, D freeze up to 35. Built from the Phase 1 / Phase 4 size claim merges.

Strombom and Kubo share `D_min` = 1 for N >= 25 (Kubo needs 3 dogs at N=5; Strombom needs 2 at N in {5, 10}). FAT is absent for N >= 25 (hard failure). Counts in `artefacts.json`: 8 shared, 7 shifted, 29 absent. Feeds **C4** (partial): size transfer holds for Strombom/Kubo mid/large N, not for FAT.

## How we get this

Built by analysis Package D from the method trial tables in this folder. Interpretation also in `../../README.md`.

## Files from this run

Machine-written outputs in this folder (do not edit by hand):

- `artefacts.json`: machine-readable index of paths this export wrote.
- `provenance.json`: run stamp (hash, seeds, metrics, timestamps) so later analysis can check what executed.
- `strombom_multi_trials.csv`: Strombom trial rows for the transfer comparison.
- `kubo_trials.csv`: Kubo trial rows for the transfer comparison.
- `fat_trials.csv`: FAT trial rows for the transfer comparison.
- `transfer_table.csv`: per-feature / per-N baseline vs method values with transfer_label (shared/shifted/absent).
- `transfer_summary.csv`: counts of shared / shifted / absent rows.
