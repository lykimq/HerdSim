# HerdSim Developer Guide

Welcome to the HerdSim developer documentation. This guide covers the system architecture, core simulation loop, codebase organization, and instructions for extending the platform with new plugins.

## System Architecture

HerdSim is built as a decoupled system: a Python-based simulation engine backend and a JavaScript/PixiJS frontend. The backend handles the heavy lifting of the tick-based simulation, while the frontend handles rendering and user interaction via REST and WebSockets.

### High-Level Data Flow

The following diagram illustrates how the frontend interacts with the backend components, and how the simulation runner drives the various plugins.

```mermaid
flowchart LR
  startNode([Client])
  uiSingle[Single Arena View]
  uiAnalytics[Analytics Dashboard]
  apiHTTP[FastAPI REST]
  apiWS[FastAPI WebSocket]
  sessions[Session Manager]
  runner[Simulation Engine]
  algo[Algorithm Plugins]
  scenario[Scenario Plugins]
  metrics[Metric Plugins]
  world[World State (Obstacles/Goals)]
  endNode([Frame Data & Metrics])

  startNode --> uiSingle
  startNode --> uiAnalytics
  uiSingle --> apiHTTP
  uiSingle --> apiWS
  uiAnalytics --> apiHTTP
  apiHTTP --> sessions
  apiWS --> sessions
  sessions --> runner
  runner --> metrics
  runner --> algo
  algo --> world
  scenario --> world
  runner --> endNode

  classDef ui fill:#cfe2f3,stroke:#1565c0,color:#0d47a1
  classDef wiring fill:#b2dfdb,stroke:#00796b,color:#004d40
  classDef domain fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20
  classDef shared fill:#e1bee7,stroke:#7b1fa2,color:#4a148c
  classDef transport fill:#ffe0b2,stroke:#ef6c00,color:#e65100
  classDef start fill:#eceff1,stroke:#546e7a,color:#263238

  class uiSingle,uiAnalytics ui
  class apiHTTP,apiWS transport
  class sessions,runner wiring
  class algo,scenario,metrics domain
  class world shared
  class startNode,endNode start
```

## The Simulation Engine

The core of HerdSim is the simulation runner (`core/simulation_runner.py`). It manages the state of the world and advances the simulation in discrete time steps (ticks).

### Tick Lifecycle

During each tick, the engine guarantees a strict execution order to ensure reproducible and deterministic behavior:

```mermaid
flowchart TD
  startTick([Tick Begin])
  met[Evaluate Metrics]
  stepAlg[Algorithm Step (Agent Movement)]
  obst[Resolve Collisions & Obstacles]
  done([Tick End])

  startTick --> met
  met --> stepAlg
  stepAlg --> obst
  obst --> done

  classDef domain fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20
  classDef shared fill:#e1bee7,stroke:#7b1fa2,color:#4a148c
  classDef start fill:#eceff1,stroke:#546e7a,color:#263238

  class startTick,done start
  class met,stepAlg domain
  class obst shared
```

Algorithms are responsible for calculating intent (velocity vectors for sheep and shepherds). The engine applies obstacle resolution and environment constraints *after* the algorithm has run, ensuring agents don't move out of bounds or overlap illegally.

## Codebase Structure

- **`api/`**: FastAPI routers, REST endpoints, and WebSocket session handlers.
- **`core/`**: The simulation engine, base classes (e.g., `BaseAlgorithm`), state definitions, and config resolution.
- **`algorithms/`**, **`scenarios/`**, **`metrics/`**: Plugin directories. Each implements specific interfaces defined in `core/`.
- **`frontend/`**: Vanilla JavaScript SPA using Vite. The main view router is in `src/main.js`. Rendering is handled by PixiJS.
- **`docs/`**: Project documentation, split between research papers/theories and developer guides.
- **`tests/`**: Pytest suite for the backend and Node tests for the frontend.

## Configuration & Overrides

Simulation configurations are layered. When a new simulation session starts, the engine merges configs in the following priority (highest to lowest):

1. **User Overrides**: Explicit parameters passed via the API (e.g., custom sheep count, specific algorithm params).
2. **Scenario Defaults**: The scenario plugin can dictate specific agent counts or world layouts.
3. **Paper/Preset Defaults**: Replications of research papers often define specific parameters.
4. **Algorithm Defaults**: Fallback parameters defined by the algorithm implementation.
5. **Global Shared Defaults**: Base world settings defined in `core/shared_defaults.py`.

## Extending the Simulator

HerdSim is designed around a plugin architecture. You can drop in new logic without altering the core simulation runner.

### 1. Adding an Algorithm
Algorithms control the behavior of the agents (sheep and shepherds).
- Subclass `core.base_algorithm.BaseAlgorithm`.
- Implement the `step(self, state)` method.
- Register your algorithm in `algorithms/registry.py`.
- Define any custom configuration parameters in your algorithm's `default_config`.

### 2. Adding a Scenario
Scenarios define the initial state of the world, such as arena boundaries, obstacles, and starting positions.
- Subclass `core.base_scenario.BaseScenario`.
- Implement `create_world()` and `initial_positions()`.
- Register the scenario in `scenarios/registry.py`.

### 3. Adding a Metric
Metrics evaluate the state of the simulation at each tick (e.g., center of mass, success conditions).
- Subclass `core.base_metric.BaseMetric`.
- Implement the evaluation logic using the current state.
- Register it in `metrics/registry.py`.

## Development Workflow

### Starting the Stack
```bash
# 1. Install backend dependencies (Python 3.10+)
pip install -e ".[dev]"

# 2. Install frontend dependencies (Node.js)
cd frontend
npm install
cd ..

# 3. Start the FastAPI backend
uvicorn api.main:app --reload --port 8000

# 4. Start the Vite dev server (in a separate terminal)
cd frontend
npm run dev
```

### Running Tests
Ensure changes don't break determinism or core logic.
```bash
# Run backend tests (excludes heavy stress tests)
pytest tests/backend/ -q -m "not stress"

# Run frontend unit tests
node --test tests/frontend/*.test.js
```
