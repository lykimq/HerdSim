# Scaling protocols

Tools and results for the shepherding scaling experiments.

Reader documentation: [English index](docs/INDEX.md) | [Vietnamese index](docs/INDEX_vi.md).

## Directory structure

- `configs/`: Canonical grid defaults and protocol YAMLs (`protocols/`).
- `docs/`: Focused plan, methods, setup, credibility, status, and discussion documents.
- `results/`: Simulation outputs organized by phase (`phase1`, `phase2`, `phase4`).
- `scripts/`: CLI runners used by `make -C scaling` (`campaign.py`, `run_grid.py`, `plan_claim_cells.py`, `plan_t1_cells.py`, `run_factor_sweep.py`, `analyse.py`).
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

## Main documents

- Plan: [docs/main_scaling_plan.md](docs/main_scaling_plan.md)
- Methods: [docs/methods/README.md](docs/methods/README.md)
- Setup and run reference: [docs/setup/README.md](docs/setup/README.md)
- Results: [results/summary/SUMMARY_REPORT.md](results/summary/SUMMARY_REPORT.md)
- Data appendices: [results/summary/data/README.md](results/summary/data/README.md)
- Credibility and comparison: [docs/credibility/README.md](docs/credibility/README.md)
