# Package D: structure transfer

Side-by-side structure frontiers: Strombom vs Kubo vs FAT, layouts compact / wide / split / outlier_rich, N in {50, 100, 200}.

| Layout | Strombom | Kubo | FAT |
|--------|----------|------|-----|
| compact | D_min = 1 | D_min = 1 | hard failure |
| split | D_min = 1 | D_min = 1 | hard failure |
| outlier_rich | D_min = 1 | D_min = 1 at N=50,100; D_min = 20 at N=200 | hard failure |
| wide | D_min = 1 | hard failure | hard failure |

### Claims

- **C4** (`D_min` or overcrowding is shared across the three required methods, and structure must be included): **SUPPORTED (partial)**. 

Compact/split shared for Strombom/Kubo; Kubo wide absent; Kubo outlier_rich N=200 shifted; FAT absent everywhere on this structure map.

## How we get this

Built by analysis Package D from the method trial tables in this folder. Kubo outlier_rich N=200 detail: `../../kubo_structure/claim/outlier_rich_n200_window.json`. 

## Files from this run

Machine-written outputs in this folder (do not edit by hand):

- `strombom_multi_trials.csv`: Strombom trial rows for the transfer comparison.
- `kubo_trials.csv`: Kubo trial rows for the transfer comparison.
- `fat_trials.csv`: FAT trial rows for the transfer comparison.
- `frontier_by_method_layout.csv`: `D_min` / hard_failure by method x layout x N.
- `transfer_compact.csv`: structure-transfer labels for compact only.
- `transfer_split.csv`: structure-transfer labels for split only.
- `transfer_outlier_rich.csv`: structure-transfer labels for outlier_rich (includes Kubo N=200 shift).
- `transfer_wide.csv`: structure-transfer labels for wide only.
