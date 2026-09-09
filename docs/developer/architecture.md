# Architecture

HerdSim is a plugin-oriented herding simulator. Algorithms, scenarios, and metrics register independently. A shared runner advances ticks. FastAPI and WebSocket serve the UI; PixiJS renders the arena.

## System context

```mermaid
flowchart LR
  startNode([Start])
  uiSingle[Single_Arena_Guide]
  uiAnalytics[Analytics]
  apiHTTP[REST_API]
  apiWS[WebSocket]
  sessions[Session_manager]
  runner[SimulationRunner]
  algo[Algorithm_plugins]
  scenario[Scenario_plugins]
  metrics[Metric_plugins]
  world[World_obstacles_goal]
  endNode([Frame_metrics])

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

Legend: blue = UI, teal = wiring, green = domain, purple = shared core, orange = transport, grey = start/end.

## One simulation tick

```mermaid
flowchart TD
  startTick([Tick_begin])
  met[Compute_metrics]
  stepAlg[Algorithm_step]
  obst[resolve_obstacles]
  done([Tick_end_state])

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

Exact ordering lives in `core/simulation_runner.py`. Algorithms own sheep and shepherd updates inside `step()`. The runner applies obstacle resolution afterward. Velocity conventions differ by family; see [../research/environment.md](../research/environment.md).

## Plugin surfaces

| Kind | ABC | Registry |
|------|-----|----------|
| Algorithm | `core/base_algorithm.py` | `algorithms/registry.py` |
| Scenario | `core/base_scenario.py` | `scenarios/registry.py` |
| Metric | `core/base_metric.py` | `metrics/registry.py` |

## Frontend

Vanilla JS + Vite + PixiJS 8. View router: `frontend/src/main.js` (Single, Arena, Analytics, NetLogo, Guide). REST: `frontend/src/api/rest.js`. Guide loads markdown from `GET /api/docs/{slug}` (`docs/research/` pages listed in GuideView).

## Non-goals

- General ABM language or NetLogo replacement for arbitrary models
- GIS / 3D / agent kinds beyond sheep + shepherds without a new design
- CBF / QP / RL training loops inside the interactive `step()` path
- Deleting `docs/papers/`
