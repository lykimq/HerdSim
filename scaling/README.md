# Scaling protocols

Tools and results for the shepherding scaling experiments.

## Directory structure

- `configs/`: Section 8 canonical grid defaults and protocol YAMLs (`protocols/`).
- `docs/`: Protocol specification (`main_scaling_plan.md`), progress tracker (`progress_tracker.md`), and discussion notes (`discuss/`).
- `results/`: Simulation outputs organized by phase (`phase1`, `phase2`, `phase4`).
- `scripts/`: CLI runners (`run_grid.py`, `plan_claim_cells.py`, `analyse.py`).
- `services/scaling/`: Multiprocess simulation runner and manifest ledger.

## Quickstart

Run commands with `make -C scaling <target>`:

```bash
# Run tests
make -C scaling scaling-test

# View all targets
make -C scaling help
```

Simulation data is stored in `scaling/results/`. To resume an interrupted run, re-run the same command; completed trials recorded in `manifest.jsonl` are skipped automatically.
