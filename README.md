# HerdSim (scaling-cli)

This branch is for **scaling research questions** only: protocol campaigns, trial results, and post-run analysis packages.

The interactive platform GUI (Simulate, Compare, Experiments, NetLogo, Guide) lives on **`main`**. Do not expect `platform/` or a web UI here.

## What this branch is for

1. Run RQ protocol grids (scout / claim / transfer / information ladders).
2. Resume interrupted campaigns from `manifest.jsonl`.
3. Export analysis packages (frontiers, regimes, fits, figures) under `scaling/results/.../packages/`.

Shared simulation engine (ticks, plugins, methods) stays in-tree so campaigns can run without depending on the GUI.

## Getting started

You need [uv](https://docs.astral.sh/uv/). Node.js is not required on this branch.

```bash
make install
make scaling-help
make test-ci
```

## Layout

```text
core/                 Simulation engine (tick loop, factors, config)
plugins/              Sheep, dogs, scenarios, metrics
methods/              Named method defaults (paper-style bundles)
services/shared/      Trial aggregate helpers
analysis/             Failure taxonomy + analysis/scaling (plots, export, RQs)
scaling/
  configs/            canonical_grid.yaml + protocols/*.yaml
  scripts/            campaign / grid / factor-sweep CLIs
  services/scaling/   Multiprocess runner + resume ledger
  docs/               Plan, tracker, final report
  results/            trials.csv, manifests, packages
docs/                 Architecture + code map
tests/backend/        Engine + scaling stack tests
```

## Common commands

```bash
make scaling-help
make -C scaling scaling-test
make -C scaling scaling-scout WORKERS=18
# Resume: re-run the same target; completed cells in manifest.jsonl are skipped.
```

Phase 5 information ladders (after an interrupt):

```bash
make -C scaling scaling-factor-sweep WORKERS=18
# or full ladder script:
WORKERS=18 bash scaling/results/phase5/run_all_ladders.sh
```

## Main documents

- Final report: [scaling/docs/final_report.md](scaling/docs/final_report.md)
- Progress tracker: [scaling/docs/progress_tracker.md](scaling/docs/progress_tracker.md)
- Plan: [scaling/docs/main_scaling_plan.md](scaling/docs/main_scaling_plan.md)
- Architecture: [docs/architecture.md](docs/architecture.md)
- CLI / RQ code map: [docs/codes/map_codes.html](docs/codes/map_codes.html)

## Branch policy

| Branch | Purpose |
|--------|---------|
| `main` | Platform GUI + shared engine (backup / product tree) |
| `scaling-cli` | RQ campaigns + analysis (this tree) |

Engine fixes that both need should land on `main` first, then merge into `scaling-cli`. RQ-only work stays on this branch.
