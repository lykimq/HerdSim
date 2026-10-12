# HerdSim (scaling-cli)

HerdSim is a multi-agent shepherding simulator for studying how much external control a flock needs as size, initial structure, method, and information conditions change. Dogs (shepherds) drive sheep to a goal under fixed protocols; the main control-demand quantity is the viable shepherd range around `D_min` (and any overcrowding boundary) at a reliability threshold.

## Tech stack

| Layer | Choice |
|-------|--------|
| Language | Python 3.11+ |
| Numerics / data | NumPy, pandas, SciPy, PyArrow |
| Plots | Matplotlib |
| Protocols | YAML (PyYAML) |
| Packaging / env | uv, setuptools |
| Tests | pytest |
| Lint / types | Ruff, basedpyright |
| Campaign CLI | `cli/campaign.py` |

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
