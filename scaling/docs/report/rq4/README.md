# RQ4: transfer across methods

Question: if we switch herding method, which parts of the size and structure pattern stay the same?

Required methods: baseline `strombom_multi` (reference from RQ1/RQ2), then `kubo` and `fat` on the same grids. Protocol: `scaling_v2`.

Story and numbers: [short report](../short_report.html). Frozen defaults: [../protocol/canonical_grid.yaml](../protocol/canonical_grid.yaml).

## Folders

| Path | Meaning |
|------|---------|
| `kubo_size/` | Kubo compact size map (scout + claim) |
| `kubo_structure/` | Kubo four-layout structure map (scout + claim) |
| `fat_size/` | FAT compact size map (scout + claim) |
| `fat_structure/` | FAT four-layout structure map (scout + claim) |
| `package_d/` | Side-by-side transfer tables (size + structure) |

## Common files inside each scout/claim folder

| File | Meaning |
|------|---------|
| `README.md` | Human note for that run (when present) |
| `protocol.yaml` | Frozen settings |
| `provenance.json` | Host, timestamps, protocol hash |
| `status.json` | Progress and completion |
| `manifest.jsonl` | Resume ledger |
| `trials.csv` | One row per simulation |
| `merged_trials.csv` | Claim merge used for analysis (claim folders) |
| `boundary_*.csv/json` | Claim window plan |
| `*dmin_bootstrap.csv` | Bootstrap on `D_min` |
| `packages/` | Package A or B exports |

Extras: `kubo_structure/claim/outlier_rich_n200_window.json` for the soft-edge Kubo cell. Trajectory parquet is not retained here.

## Takeaway

On compact starts, Strombom and Kubo share a low `D_min` floor for larger flocks. FAT does not: for N >= 25 nothing reaches 90% success through D = 35. Structure breaks transfer further (Kubo wide fails; Kubo outlier_rich at N = 200 shifts). Claim C4 SUPPORTED (partial).
