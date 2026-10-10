# Scaling protocols

Primary surface of the **scaling-cli** branch: tools and results for the
shepherding scaling research questions. Platform GUI code is not in this tree
(see `main`).

Reader entry point: [docs/final_report.md](docs/final_report.md) ([HTML](docs/final_report.html)).
Emailable short package: [docs/report/short_report.html](docs/report/short_report.html) (self-contained folder under `docs/report/`).

## Directory structure

- `configs/`: Canonical grid defaults and protocol YAMLs (`protocols/`).
- `docs/`: Final report (HTML), plan/status Markdown, and figures.
- `results/`: Simulation run outputs organized by phase (`phase1`, `phase2`, `phase4`, `phase5`).
- `scripts/`: CLI runners used by `make -C scaling` (`campaign.py`, `run_grid.py`, `plan_claim_cells.py`, `plan_t1_cells.py`, `run_factor_sweep.py`).
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

- Final report: [docs/final_report.md](docs/final_report.md) ([HTML](docs/final_report.html))
- Short report package (emailable): [docs/report/short_report.html](docs/report/short_report.html)
- Plan: [docs/main_scaling_plan.md](docs/main_scaling_plan.md)
- Research program: [docs/herdsim_research_program.md](docs/herdsim_research_program.md)
- Progress tracker: [docs/progress_tracker.md](docs/progress_tracker.md)
- Scaling code map (CLI / RQ file guide): [../docs/codes/map_codes.html](../docs/codes/map_codes.html)
