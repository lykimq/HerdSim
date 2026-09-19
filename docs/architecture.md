# HerdSim Architecture & Design

HerdSim is a factor-based platform for simulating and analyzing multi-agent shepherding. The engine separates sheep dynamics, shepherd observation, and dog control so experiments can vary information, heterogeneity, environment, and controller architecture independently.

## Design Requirements

- **Modularity:** sheep models, dog controllers, observation modes, scenarios, and metrics plug in without rewriting the runner.
- **Reproducibility:** discrete deterministic ticks with seeded RNG.
- **Factorial experiments:** herdability and sensing studies are first-class factor grids.
- **Separation of Concerns:** backend owns state and logic; frontend owns rendering.

## High-Level Data Flow

```mermaid
flowchart LR
  client([Client])
  apiHTTP["FastAPI REST"]
  apiWS["FastAPI WebSocket"]
  sessions["Session Manager"]
  runner["Simulation Engine"]
  factors["Experimental Factors"]
  sheep["Sheep Dynamics"]
  obs["Observation Model"]
  dogs["Dog Controller"]
  metrics["Metrics"]
  out(["Frame Data and Metrics"])

  client --> apiHTTP
  client --> apiWS
  apiHTTP --> sessions
  apiWS --> sessions
  sessions --> runner
  factors --> runner
  runner --> sheep
  runner --> obs
  obs --> dogs
  runner --> metrics
  runner --> out
```

## Tick Lifecycle

```text
state(t)
  -> environment updates (moving goal)
  -> failure factors
  -> sheep_dynamics.step
  -> observation.observe_all
  -> dog_controller.step(observations)
  -> robot constraints
  -> resolve obstacles/walls
  -> metrics(state(t+1))
```

## Experimental Factors

Defined in `core/experimental_factors.py`:

- Flock: `n_sheep`, layout, cohesion, stubborn fraction
- Shepherds: `n_shepherds`, speed scale, failure mode, kinematic limits
- Observation: `obs_mode`, sensing range, noise, communication
- Environment: world keys, `goal_mode`
- Model: `sheep_model`, `dog_controller`, scenario, preset

Named instruments in `core/presets.py` are factor bundles (e.g. `strombom` = Strombom sheep + Collect/Drive).

## Plugin Interfaces

- `BaseSheepDynamics` in `core/sheep_dynamics.py`
- `BaseObservationModel` / `ShepherdObservation` in `core/observation.py`
- `BaseDogController` in `core/dog_controller.py`
- Registries in `core/plugin_registry.py`
- Named instruments (presets) in `core/presets.py`

New sheep models, dog controllers, and observation modes register in `core/plugin_registry.py`. Scenarios and metrics register in their package registries. Named instruments are factor bundles in `core/presets.py` with package metadata under `algorithms/<id>/` (on-disk package name; UI and docs say instrument).

## Config Composition

`resolve_experiment_config` merges:

1. shared world defaults
2. sheep and dog defaults
3. instrument paper params
4. scenario overlay (`paper`/`custom`: world keys; `scenario`: full overlay)
5. explicit algorithm_params / world_overrides / agent counts

## Implementation Layout

- `api/`: FastAPI routers, factor-grid benchmarks, and shepherding-budget campaign runner (`budget_runner.py`, `budget_layout.py`)
- `core/`: runner, factors, observation, agent attributes, presets
- `dynamics/`, `controllers/`: sheep and dog plugins
- `algorithms/<id>/`: on-disk instrument packages (`info.json`, paper defaults, helpers). Folder name is historical; product language is instrument. This is not an HTTP path.
- `scenarios/`, `metrics/`: task and measurement plugins
- `analysis/`: failure taxonomy helpers plus `analysis/budget/` for shepherding-budget packages A--G
- `configs/budget/`: frozen protocol (`canonical_grid.yaml`) and per-run campaign subsets
- `scripts/`: `dev.sh` (local API + Vite; also `make dev`) and `scripts/budget/` (grid / factor-sweep / analyse CLIs)
- `Makefile.budget`: operator targets for budget campaigns (`make budget-help`)
- `results/budget/`: campaign run data under `phase{k}/{slug}/` (kept in git; see `results/budget/README.md`)
- `frontend/`: Vite SPA (Simulate, Compare, Experiments, NetLogo, Guide)
- `docs/`: architecture, Guide pages, and research plans under `docs/research/`
- `tests/`: pytest + frontend node tests

## Shepherding-budget stack

Separate from the Experiments **UI** tab: a CLI campaign layer for the
shepherding-budget research program (Size / Structure / Mechanism / Generality,
then follow-ons). Science and status live under `docs/research/budget/`; this
section is the engineering shape.

### What exists now

| Piece | Role |
|-------|------|
| `configs/budget/canonical_grid.yaml` | Frozen protocol defaults (task, θ, N/D grids, T₀/T₁, seeds, methods) |
| `configs/budget/campaigns/*.yaml` | Per-run subsets (pilot, scout, state, factor sweep) with WHY comments |
| `api/budget_runner.py` | Expand grid, run trials, resume via `manifest.jsonl`, write timeseries |
| `api/budget_layout.py` | Path conventions (`phase{k}/{slug}/`, cell keys, package dirs) |
| `analysis/budget/` | Frontier, regimes, export, plots, plus modules for later packages |
| `scripts/budget/` | `run_grid.py`, `run_factor_sweep.py`, `analyse.py` |
| `Makefile.budget` | `budget-pilot`, `budget-scout`, `budget-pilot-state`, `budget-factor-sweep`, `budget-analyse` |
| `results/budget/phase{k}/{slug}/` | `campaign.yaml`, provenance, `trials.csv`, `timeseries/`, `packages/{a-g}/`, optional `REPORT.md` |

Operator entry: `make -f Makefile.budget help` (or `make budget-help`). Layout
detail: [results/budget/README.md](../results/budget/README.md).

### Target design (after the budget plan is finished)

The research plan drives a phase sequence. When the program is complete, the same
layout should support claim-grade work end to end -- not only smoke/scout runs:

| Phase focus | Formal RQs | Evidence package | Engineering outcome |
|-------------|------------|------------------|---------------------|
| Protocol freeze | S8 | all | Locked `canonical_grid.yaml` + provenance on every campaign |
| Herdability maps | RQ2 (+ data for RQ6) | A | Reliability maps, D_min frontier, regimes, figures |
| Structure beyond N | RQ1 | B | All four X₀ layouts; state vs (N, D) predictors |
| Overcrowding mechanism | RQ3 | C | I_dir / coverage timeseries + mechanism tests |
| Cross-method transfer | RQ4 | D | Same grids on transfer instruments; transfer table |
| Information vs shepherds | RQ5 | E | Factor sweeps; substitution curves |
| Scaling fits | RQ6 | F | Model comparison on real (non-flat) frontiers |
| Early warning | RQ7 | G | Lead-time / AUROC from failure trajectories |

Caps I1--I14 in the plan are the capability checklist (grid runner, frontier,
regimes, X₀ generators, predictors, interference/coverage, mechanism tests,
transfer, substitution, scaling fits, early warning, dossier export, timeseries).
Several Caps are already built and unit-tested; claim-grade use follows the
campaign waves in the progress tracker.

### Where to read the science

- Program framing: [docs/research/budget/herdsim_research_program.md](research/budget/herdsim_research_program.md)
- Detailed plan (RQs, claims, Caps, protocol): [docs/research/budget/main_shepherding_budget_plan.md](research/budget/main_shepherding_budget_plan.md)
- Status, hardware, ordered run plan: [docs/research/budget/progress_tracker.md](research/budget/progress_tracker.md)

Do not treat the Experiments UI exports as a substitute for this campaign stack:
UI batch studies stay in the browser; budget campaigns write under `results/budget/`
and are meant to stay with the repo.

## HTTP API (instruments)

Discovery and UI payloads use **instrument** wording:

- `GET /api/instruments` lists named instruments (from `core/presets.py`, with package metadata from `algorithms/<id>/info.json` where present)
- Related routes under `/api/instruments/...` (for example models meta used by Experiments)

There is no `/api/algorithms` route. Prefer `instrument` / `instruments` in new API fields and clients. On disk, packages remain under `algorithms/<id>/` until a deliberate folder rename.

Shepherding-budget campaigns are CLI/Makefile driven today; they wrap the same
simulation runner and instruments, not a separate HTTP surface.
