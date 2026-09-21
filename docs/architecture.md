# HerdSim Architecture and Design

HerdSim is a factor-based platform for simulating and analyzing multi-agent shepherding. The engine separates sheep dynamics, shepherd observation, and dog control so experiments can vary information, heterogeneity, environment, and controller architecture independently.

## Design requirements

- **Modularity.** Sheep models, dog controllers, observation modes, scenarios, and metrics plug in without rewriting the runner.
- **Reproducibility.** Discrete deterministic ticks with seeded random number generation (RNG).
- **Factorial experiments.** Herdability and sensing studies are first-class factor grids.
- **Separation of concerns.** Backend owns state and logic. Frontend owns rendering.

## High-level data flow

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

## Tick lifecycle

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

## Experimental factors

Defined in `core/experimental_factors.py`:

- Flock: `n_sheep`, layout, cohesion, stubborn fraction
- Shepherds: `n_shepherds`, speed scale, failure mode, kinematic limits
- Observation: `obs_mode`, sensing range, noise, communication
- Environment: world keys, `goal_mode`
- Model: `sheep_model`, `dog_controller`, scenario, preset

Named instruments in `core/instruments.py` are factor bundles (for example `strombom` equals Strombom sheep plus Collect/Drive).

## Plugin interfaces

- `BaseSheepDynamics` in `core/sheep_dynamics.py`
- `BaseObservationModel` / `ShepherdObservation` in `core/observation.py`
- `BaseDogController` in `core/dog_controller.py`
- Registries in `core/plugin_registry.py`
- Named instruments (catalog) in `core/instruments.py`

New sheep models, dog controllers, and observation modes register in `core/plugin_registry.py`. Scenarios and metrics register in their package registries. Named instruments are factor bundles in `core/instruments.py` with package metadata under `instruments/<id>/`.

## Config composition

`resolve_experiment_config` merges:

1. shared world defaults
2. sheep and dog defaults
3. instrument paper params
4. scenario overlay (`paper`/`custom`: world keys; `scenario`: full overlay)
5. explicit algorithm_params / world_overrides / agent counts

## Implementation layout

- `api/`: FastAPI HTTP surface (`main.py`, `session_manager.py`, routers)
- `services/experiments/`: UI Experiments / factor-grid benchmark engine
- `services/budget/`: shepherding-budget campaign runner and layout
- `core/`: runner, factors, observation, agent attributes, instrument catalog
- `plugins/sheep/`, `plugins/dogs/`: sheep and dog plugins
- `instruments/<id>/`: instrument packages (`info.json`, paper defaults, helpers). This is not an HTTP path.
- `plugins/scenarios/`, `plugins/metrics/`: task and measurement plugins
- `analysis/`: failure taxonomy helpers plus `analysis/budget/` for shepherding-budget packages A to G
- `configs/budget/`: frozen protocol (`canonical_grid.yaml`) and per-run campaign subsets
- `scripts/`: `dev.sh` (local API + Vite; also `make dev`) and `scripts/budget/` (grid / factor-sweep / analyse CLIs)
- `Makefile.budget`: operator targets for budget campaigns (`make budget-help`)
- `results/budget/`: campaign run data under `phase{k}/{slug}/` (kept in git; see `results/budget/README.md`)
- `frontend/`: Vite SPA (Simulate, Compare, Experiments, NetLogo, Guide)
- `docs/`: architecture, Guide pages, and research plans under `docs/research/`
- `integrations/netlogo/`, `integrations/matlab/`: external tool bridges and models
- `tests/`: pytest + frontend node tests

## Shepherding-budget stack

Separate from the Experiments **UI** tab: a CLI campaign layer for the
shepherding-budget research program (Size / Structure / Mechanism / Generality,
then follow-ons). Science and status live under `docs/research/budget/`. This
section is the engineering shape.

### What exists now

| Piece | Role |
|-------|------|
| `configs/budget/canonical_grid.yaml` | Frozen protocol defaults (task, theta, N/D grids, T0/T1, seeds, methods) |
| `configs/budget/campaigns/*.yaml` | Per-run subsets (pilot, scout, state, factor sweep) with WHY comments |
| `services/budget/runner.py` | Expand grid, run trials, resume via `manifest.jsonl`, write timeseries |
| `services/budget/layout.py` | Path conventions (`phase{k}/{slug}/`, cell keys, package dirs) |
| `analysis/budget/` | Frontier, regimes, export, plots, plus modules for later packages |
| `scripts/budget/` | `run_grid.py`, `run_factor_sweep.py`, `analyse.py` |
| `Makefile.budget` | `budget-pilot`, `budget-scout`, `budget-pilot-state`, `budget-factor-sweep`, `budget-analyse` |
| `results/budget/phase{k}/{slug}/` | `campaign.yaml`, provenance, `trials.csv`, `timeseries/`, `packages/{a-g}/`, optional `REPORT.md` |

Operator entry: `make -f Makefile.budget help` (or `make budget-help`). Layout
detail: [results/budget/README.md](../results/budget/README.md).

### Target design (after the budget plan is finished)

The research plan drives a phase sequence. When the program is complete, the same
layout should support claim-grade work end to end, not only smoke/scout runs:

| Phase focus | Formal research questions (RQs) | Evidence package | Engineering outcome |
|-------------|---------------------------------|------------------|---------------------|
| Protocol freeze | S8 | all | Locked `canonical_grid.yaml` plus provenance on every campaign |
| Herdability maps | RQ2 (plus data for RQ6) | A | Reliability maps, D_min frontier, regimes, figures |
| Structure beyond N | RQ1 | B | All four X0 layouts; state vs (N, D) predictors |
| Overcrowding mechanism | RQ3 | C | I_dir / coverage timeseries plus mechanism tests |
| Cross-method transfer | RQ4 | D | Same grids on transfer instruments; transfer table |
| Information vs shepherds | RQ5 | E | Factor sweeps; substitution curves |
| Scaling fits | RQ6 | F | Model comparison on real (non-flat) frontiers |
| Early warning | RQ7 | G | Lead-time / AUROC from failure trajectories |

Caps I1 to I14 in the plan are the capability checklist (grid runner, frontier,
regimes, X0 generators, predictors, interference/coverage, mechanism tests,
transfer, substitution, scaling fits, early warning, dossier export, timeseries).
Several Caps are already built and unit-tested. Claim-grade use follows the
campaign waves in the progress tracker.

### Where to read the science

- Program framing: [docs/research/budget/herdsim_research_program.md](research/budget/herdsim_research_program.md)
- Detailed plan (RQs, claims, Caps, protocol): [docs/research/budget/main_shepherding_budget_plan.md](research/budget/main_shepherding_budget_plan.md)
- Status, hardware, ordered run plan: [docs/research/budget/progress_tracker.md](research/budget/progress_tracker.md)

Do not treat the Experiments UI exports as a substitute for this campaign stack.
UI batch studies stay in the browser. Budget campaigns write under `results/budget/`
and are meant to stay with the repo.

## HTTP API (instruments)

Discovery and UI payloads use **instrument** wording:

- `GET /api/instruments` lists named instruments (from `core/instruments.py`, with package metadata from `instruments/<id>/info.json` where present)
- Related routes under `/api/instruments/...` (for example models meta used by Experiments)

There is no `/api/algorithms` route. Prefer `instrument` / `instruments` in new API fields and clients.

Shepherding-budget campaigns are CLI/Makefile driven today. They wrap the same
simulation runner and instruments, not a separate HTTP surface.
