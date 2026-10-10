# Campaign runners (`run/`)

CLI protocols for shepherding scaling research questions.

## Contents

- `configs/`: Canonical grid and protocol YAMLs
- `scripts/`: `campaign.py`, `run_grid.py`, `run_factor_sweep.py`, claim/T1 planners
- `services/scaling/`: Multiprocess runner and resume ledger
- `packaging/`: End-of-trial row builders (failure labels, aggregates, provenance)

Post-run plots and package dossiers live under `../analysis/`. Trial data under `../results/`.

## Quickstart

```bash
make -C run help
make -C run scaling-test
make -C run scaling-scout WORKERS=18
```

Resume an interrupted run by re-running the same target; `manifest.jsonl` skips finished cells.

## Documents

- Science: [../docs/science/final_report.md](../docs/science/final_report.md)
- Tracker: [../docs/science/progress_tracker.md](../docs/science/progress_tracker.md)
- Architecture: [../docs/architecture.md](../docs/architecture.md)
