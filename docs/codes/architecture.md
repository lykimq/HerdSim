# HerdSim Architecture (scaling-cli)

Batch research campaigns over a tick-level multi-agent shepherding simulator. Dogs drive sheep to a goal; campaigns measure control demand (`D_min` and related frontiers) under frozen protocols.

## Context

```mermaid
flowchart LR
  operator["Operator"]
  cli["cli/campaign.py"]
  configs["protocols/configs"]
  services["services/"]
  sim["sim/"]
  packaging["protocols/packaging"]
  results["results/"]
  analysis["analysis/"]

  operator --> cli
  cli --> configs
  cli --> services
  services --> sim
  services --> packaging
  services --> results
  analysis --> results
  analysis --> packaging
```

Quality attributes:

- Resumable grids via `manifest.jsonl` cell keys
- Protocol freeze: resolved YAML copied into the run folder; content hash in `provenance.json`
- Deterministic seeds from `master_seed + i`
- Reproducible trial rows in `trials.csv` (flushed after each finished cell)

## Logical layers

```mermaid
%%{init: {"flowchart": {"curve": "basis", "nodeSpacing": 40, "rankSpacing": 50}}}%%
flowchart TB
  cli["cli/"]
  cli --> configs["protocols/configs/"]
  cli --> services["services/"]

  services --> sim["sim/"]
  services --> packaging["protocols/packaging/"]
  services --> results["results/"]

  analysis["analysis/"]
  analysis --> packaging
  analysis --> results
```

## Components

| Piece | Path | Role |
|-------|------|------|
| Tick engine | `sim/core/simulation_runner.py` | Step loop until success or timeout |
| Config resolve | `sim/core/config/experiment.py` | `resolve_experiment_config` |
| Method catalog | `sim/core/methods.py` | Sheep x dog bundles |
| Plugin registries | `sim/core/plugin_registry.py` | Sheep, dogs, observation, scenarios, metrics |
| Campaign CLI | `cli/campaign.py` | Verbs: `run`, `claim-plan`, `claim-reseed`, `t1-plan`, `t1` |
| Grid / factor runners | `cli/run_grid.py`, `cli/run_factor_sweep.py` | Expand cells from protocol |
| Claim / T1 planners | `cli/plan_claim_cells.py`, `cli/plan_t1_cells.py` | Windows then optional reseed |
| Orchestration | `services/runner.py`, `services/layout.py` | Resume, status, `_run_cell` |
| Packaging | `protocols/packaging/` | Failure labels, trial fields, provenance stamp |
| Analysis | `analysis/` | Frontiers, regimes, fits, transfer, export |

### Methods

| Method | Sheep | Dog | Role |
|--------|-------|-----|------|
| `strombom` | strombom | collect_drive | Single-dog Collect/Drive base |
| `strombom_multi` | strombom | collect_drive_multi | RQ baseline |
| `kubo` | kubo | kubo_forces | RQ4 transfer |
| `fat` | strombom | fat | RQ4 transfer |
| `communication_free` | strombom | communication_free | Local Collect/Drive without sharing |

Campaign scenario: `drive_to_goal`. Registered metrics are written into each trial row.

### Plugin model

Registries bind string ids to implementations:

- Sheep dynamics (`plugins/sheep/`)
- Dog controllers (`plugins/dogs/`)
- Observation models (`core/observation.py`)
- Scenarios (`plugins/scenarios/`)
- Metrics (`plugins/metrics/`)

## Protocol configs

Layout:

```text
protocols/
|-- configs/
|   |-- canonical_grid.yaml
|   `-- protocols/           # one YAML per stage id
`-- packaging/
```

YAML keys:

- `protocol_id`: id matching the filename stem (and usually the results folder slug)
- `canonical`: path to frozen defaults (normally `protocols/configs/canonical_grid.yaml`)
- `extends`: optional parent protocol YAML; child keys override
- `grade`: `SMOKE` / `SCOUT` / `CLAIM` (seed depth convention)
- `output`: destination under `results/`
- `seed_mode`: `scout` for `run`; `claim` for claim-reseed / t1
- `upstream_protocol` / `upstream_trials`: claim and T1 inputs
- `store_timeseries`: write `timeseries/*.parquet` when true

## Runtime

### Campaign flow

```mermaid
flowchart TB
  cmd["uv run cli/campaign.py verb --protocol id"]
  load["Load protocol YAML + canonical grid"]
  verb{"verb"}

  cmd --> load --> verb

  verb -->|run| grid["cli/run_grid.py or run_factor_sweep.py"]
  verb -->|claim-plan| plan["plan_claim_cells --plan-only"]
  verb -->|claim-reseed| reseed["plan_claim_cells then grid"]
  verb -->|t1-plan / t1| t1["plan_t1_cells"]

  grid --> prep["protocol.yaml, provenance.json, status.json"]
  reseed --> prep
  t1 --> prep
  prep --> pool["expand cells; skip ok keys in manifest"]
  pool --> cell["_run_cell"]
  cell --> eng["SimulationRunner"]
  eng --> pack["packaging: metrics + failure label"]
  pack --> write["trials.csv, manifest.jsonl, optional timeseries/"]
  plan --> boundaries["boundary_cells.csv, boundary_plan.json"]
  reseed --> merge["merged_trials.csv, dmin_bootstrap.csv"]
```

### One cell

`_run_cell` builds a config via `resolve_experiment_config`, then steps until success or timeout.

### Tick order

```text
state(t)
  -> environment updates / failure factors
  -> sheep_dynamics.step
  -> observation.observe_all
  -> dog_controller.step
  -> constraints / walls
  -> metrics(state(t+1))
```

### Artifacts under `results/phase{k}/{slug}/`

| Artifact | When written |
|----------|--------------|
| `protocol.yaml` | Start of run / claim / t1 (resolved freeze) |
| `provenance.json` | Start of grid (hash, seeds, metric ids) |
| `status.json` | Start, each cell, finish |
| `trials.csv` | After each finished cell |
| `manifest.jsonl` | After each ok cell (resume keys) |
| `timeseries/*.parquet` | After each cell if `store_timeseries` |
| `boundary_cells.csv`, `boundary_plan.json` | Claim plan / start of claim-reseed |
| `merged_trials.csv`, `*dmin_bootstrap.csv` | End of claim-reseed |
| `t1_cells.csv`, `t1_plan.json` | T1 plan / start of t1 |
| `packages/{a-g}/` | Separate analysis export (not the campaign runner) |
| `README.md` | Handwritten notes |

## Phase and RQ code map

| Results folder | RQ | Question | Primary method |
|----------------|----|----------|----------------|
| `phase1/` | RQ2 | Size map: how `D_min` changes with N | `strombom_multi` |
| `phase2/` | RQ1 | Structure: does start layout move `D_min`? | `strombom_multi` |
| (analyse only) | RQ3 | Mechanism of overcrowding | needs RQ2 overcrowding cells |
| `phase4/` | RQ4 | Transfer across kubo / fat | `kubo`, `fat` |
| `phase5/` | RQ5 | Information ladders | `strombom_multi` + factors |
| (analyse on RQ2) | RQ6 | Scaling curve fits | Package F |
| (analyse on RQ2) | RQ7 | Early warning | Package G |

### RQ2 size (phase1)

Protocols: `phase1_pilot`, `phase1_scout`, `phase1_claim`, `phase1_t1`.

```bash
uv run cli/campaign.py run --protocol phase1_scout --workers 16
uv run cli/campaign.py claim-plan --protocol phase1_claim
uv run cli/campaign.py claim-reseed --protocol phase1_claim --workers 16
```

Code path:

```mermaid
flowchart LR
  camp["cli/campaign.py"]
  grid["cli/run_grid.py"]
  claim["cli/plan_claim_cells.py"]
  runner["services/runner.py"]
  method["strombom_multi"]
  pkgA["Package A"]

  camp --> grid
  camp --> claim
  grid --> runner
  claim --> runner
  runner --> method
  method --> pkgA
```

| Step | Path / symbols |
|------|----------------|
| Runner | `expand_scaling_grid`, `run_scaling_grid`, `_run_cell` |
| Method | `plugins/dogs/collect_drive_multi.py`, `methods/strombom/heuristics.py` |
| Package A | `analysis/frontier.py`, `regimes.py`, `export.py` |

### RQ1 structure (phase2)

Protocols: `phase2_pilot_state`, `phase2_scout`, `phase2_claim`.

Extra modules: `core/world/layouts.py`; Package B in `analysis/predictors.py`.

### RQ3 mechanism (analyse only)

`analysis/mechanism.py` (`evaluate_overcrowding_mechanisms`, `evaluate_temporal_order`). Needs matched efficient vs overcrowding cells at the same N.

### RQ4 transfer (phase4)

Protocols: `phase4_{kubo,fat}_{size,structure}_{scout,claim}`.

```bash
uv run cli/campaign.py run --protocol phase4_kubo_size_scout --workers 16
uv run cli/campaign.py claim-reseed --protocol phase4_kubo_size_claim --workers 16
```

Analysis: `analysis/transfer.py` (`build_transfer_table`, Package D).

### RQ5 information (phase5)

Protocols: `phase5_factor_sweep`, `phase5_obs_claim`, `phase5_range_{scout,claim}`, `phase5_comm_{scout,claim}`.

Code path: `cli/run_factor_sweep.py`, observation modes in `core/observation.py`, Package E in `analysis/substitution.py`. Ladder script: `results/phase5/run_all_ladders.sh`.

### RQ6 fits / RQ7 early warning (analyse)

- RQ6: `analysis/fits.py` (`fit_scaling_models`) on phase1 claim frontier
- RQ7: `analysis/early_warning.py` on claim timeseries when stored

### Analysis packages A-G

| Pkg | RQ | Module | Entry |
|-----|----|--------|-------|
| A | RQ2 / size maps | `export.py`, frontier, regimes | `export_package_a` |
| B | RQ1 | `predictors.py` | `compare_state_vs_nd_predictors` |
| C | RQ3 | `mechanism.py` | `evaluate_overcrowding_mechanisms` |
| D | RQ4 | `transfer.py` | `build_transfer_table` |
| E | RQ5 | `substitution.py` | `substitution_curves*` |
| F | RQ6 | `fits.py` | `fit_scaling_models` |
| G | RQ7 | `early_warning.py` | `evaluate_early_warning_campaign` |

### How to trace a run

1. Open the protocol YAML under `protocols/configs/protocols/`.
2. Note `output`, grids, and any `upstream_protocol`.
3. Run the matching `uv run cli/campaign.py` verb.
4. Sims end in `services.runner._run_cell` -> method bundle -> plugins.
5. Analysis ends in `analysis/` and `results/.../packages/`.

Example:

```bash
uv run cli/campaign.py run --protocol phase1_scout --workers 16
# cli/campaign.py -> cli/run_grid.py -> services.runner -> _run_cell
# out: results/phase1/scout/trials.csv
```

## Design decisions

- Protocol YAML is the source of truth; each run freezes a resolved copy as `protocol.yaml`
- Resume identity is `_cell_key(ScalingCell)` in `manifest.jsonl`; completed `status=ok` keys are skipped
- Scout maps broadly; claim-plan selects windows; claim-reseed deepens seeds and merges
- Analysis is post-hoc on CSVs/timeseries and must not step the simulation
- Provenance stamp stores hash, seed list, and metric ids (not a second full protocol body)

## Extension points

| Add | Where |
|-----|-------|
| Method bundle | `sim/core/methods.py` + sheep/dog plugins + optional `sim/methods/<name>/` |
| Sheep dynamics | `sim/plugins/sheep/` + registry |
| Dog controller | `sim/plugins/dogs/` + registry |
| Metric | `sim/plugins/metrics/` + registry |
| Protocol stage | `protocols/configs/protocols/<id>.yaml` |
| Analysis package | `analysis/` module + export helper |

## Operator entry

```bash
make install
make test
make help
uv run cli/campaign.py help
uv run cli/campaign.py run --protocol phase1_scout --workers 18
uv run cli/campaign.py claim-plan --protocol phase1_claim
uv run cli/campaign.py claim-reseed --protocol phase1_claim --workers 18
```
