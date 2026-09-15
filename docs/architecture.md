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
- `algorithms/registry.py` exposes `instrument_registry` for scripts and docs sync; prefer `core.presets` or `instrument` in new code

New sheep models, dog controllers, and observation modes register in `core/plugin_registry.py`. Scenarios and metrics register in their package registries. Named instruments are factor bundles in `core/presets.py` with package metadata under `algorithms/<id>/` (on-disk package name; UI and docs say instrument).

## Config Composition

`resolve_experiment_config` merges:

1. shared world defaults
2. sheep and dog defaults
3. instrument paper params
4. scenario overlay (`paper`/`custom`: world keys; `scenario`: full overlay)
5. explicit algorithm_params / world_overrides / agent counts

## Implementation Layout

- `api/`: FastAPI routers and factor-grid benchmarks
- `core/`: runner, factors, observation, agent attributes, presets
- `dynamics/`, `controllers/`: sheep and dog plugins
- `algorithms/<id>/`: instrument packages (`info.json`, paper defaults, helpers)
- `scenarios/`, `metrics/`: task and measurement plugins
- `analysis/`: herdability, behavioural, failure taxonomy, propagation helpers
- `scripts/`: fair compare, factor grids, generalization, policy train
- `frontend/`: Vite SPA (Simulate, Compare, Experiments, NetLogo, Guide)
- `docs/`: architecture and research docs
- `tests/`: pytest + frontend node tests

API fields use `instrument` / `instruments` for endpoint payloads and UI strings. On disk, instrument packages remain under `algorithms/<id>/`.
