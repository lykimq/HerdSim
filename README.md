# HerdSim (scaling-cli)

HerdSim is a multi-agent shepherding simulator for studying how much external control a flock needs as size, initial structure, method, and information conditions change. Dogs (shepherds) drive sheep to a goal under fixed protocols; the main control-demand quantity is the viable shepherd range around `D_min` (and any overcrowding boundary) at a reliability threshold.

## Project structure

```text
HerdSim/
|-- sim/                 Tick engine
|   |-- core/            Runner, state, observation, config, world
|   |-- plugins/         Sheep, dogs, scenarios, metrics
|   `-- methods/         Paper math (strombom, kubo)
|-- protocols/           Protocol definition (configs + packaging)
|   |-- configs/         Canonical grid + protocol YAMLs
|   `-- packaging/       End-of-trial rows for trials.csv
|-- cli/                 Campaign entry scripts
|-- services/            Campaign engine (layout, resume, cell runner)
|-- analysis/            Post-run packages (frontiers, fits, export)
`-- tests/
    |-- sim/             Engine / plugin tests
    |-- services/        Campaign / protocol-load tests
    |-- protocols/       Packaging tests
    `-- analysis/        Package A-G tests
```

Dependency rule: `analysis` must not import `SimulationRunner`. Campaign code may use `sim` and `protocols.packaging`. Claim/T1 planners may call frontier helpers from `analysis` for window selection.

Import map (disk under `sim/`, imports without the `sim.` prefix):

- `sim/core/` -> `core`
- `sim/plugins/` -> `plugins`
- `sim/methods/` -> `methods`
- Protocol YAMLs: `protocols/configs/`

## Setup

```bash
make install
```

## Tests

```bash
make test
```

## Run campaigns

```bash
make help
uv run cli/campaign.py help
uv run cli/campaign.py run --protocol phase1_scout --workers 18
uv run cli/campaign.py claim-plan --protocol phase1_claim
uv run cli/campaign.py claim-reseed --protocol phase1_claim --workers 18
uv run cli/campaign.py run --protocol phase5_factor_sweep --workers 18
```

Verbs: `run`, `claim-plan`, `claim-reseed`, `t1-plan`, `t1`. Protocol ids live under `protocols/configs/protocols/`. Resume an interrupted run by repeating the same command; finished cells in `manifest.jsonl` are skipped.

## Analysis packages

Post-run helpers live in `analysis/` (import as `analysis`). Package A export:

```bash
uv run python -c "from analysis import export_package_a; import pandas as pd; export_package_a(pd.read_csv('results/phase1/claim/merged_trials.csv'), 'results/phase1/claim/packages/a', protocol={'protocol_id':'phase1_claim'}, protocol_id='phase1_claim')"
```

| Package | Entry | Typical input |
|---------|-------|---------------|
| A | `export_package_a` | merged/scout `trials.csv` |
| B | `compare_state_vs_nd_predictors` | structure trials |
| C | `evaluate_overcrowding_mechanisms` | regimes + trials |
| D | `build_transfer_table` | trials by method |
| E | `substitution_curves*` | factor-sweep trials |
| F | `fit_scaling_models` | frontier table |
| G | `evaluate_early_warning_campaign` | timeseries + outcomes |

Outputs land under `results/.../packages/{a-g}/`.
