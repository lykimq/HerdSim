# HerdSim (scaling-cli)

This branch is for **scaling research questions** only: protocol campaigns, trial results, and post-run analysis packages.

The interactive platform GUI lives on **`main`**. Do not expect `platform/` or a web UI here.

Report package prose under `docs/report/` is kept as published (do not rewrite those files casually).

## Purpose layout

```text
sim/          RUN: tick engine (core, plugins, methods)
run/          RUN: campaigns, protocols, end-of-trial packaging
analysis/     AFTER: frontiers, plots, package export (no tick loop)
results/      DATA: trials.csv, manifests, packages
docs/         DOCS: architecture, science, codes, report package
tests/        Engine + campaign + analysis tests
```

Dependency rule: `analysis` must not import `SimulationRunner`. `run` may use `sim` and `run/packaging` only.

## Getting started

```bash
make install
make scaling-help
make test-ci
```

## Common commands

```bash
make -C run help
make -C run scaling-test
make -C run scaling-scout WORKERS=18
# Resume: re-run the same target; completed cells in manifest.jsonl are skipped.
```

Phase 5 ladders:

```bash
make -C run scaling-factor-sweep WORKERS=18
WORKERS=18 bash results/phase5/run_all_ladders.sh
```

## Documents

- Science: [docs/science/final_report.md](docs/science/final_report.md), [progress_tracker.md](docs/science/progress_tracker.md)
- Architecture: [docs/architecture.md](docs/architecture.md)
- CLI / RQ map: [docs/codes/map_codes.html](docs/codes/map_codes.html)
- Published report package: [docs/report/](docs/report/) (contents frozen for this tree)

## Branch policy

| Branch | Purpose |
|--------|---------|
| `main` | Platform GUI + shared engine |
| `scaling-cli` | RQ campaigns + analysis (this tree) |
