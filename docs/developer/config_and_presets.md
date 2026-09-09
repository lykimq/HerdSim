# Config and presets

`resolve_experiment_config` merges layers into one resolved config for a session or benchmark trial. Code: `core/experiment_config.py`, `core/shared_defaults.py`.

## Merge order

```mermaid
flowchart TD
  startNode([Resolve_config])
  shared[SHARED_WORLD_DEFAULTS]
  algo[Algorithm_default_config]
  scenQ{Preset}
  paper[Paper_algo_agents_behavior]
  scen[Scenario_default_config]
  custom[User_overrides]
  out([Resolved_config])

  startNode --> shared --> algo --> scenQ
  scenQ -->|paper| paper --> out
  scenQ -->|scenario| scen --> out
  scenQ -->|custom| custom --> out
  paper -.->|world_from_scenario| scen

  classDef wiring fill:#b2dfdb,stroke:#00796b,color:#004d40
  classDef domain fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20
  classDef question fill:#fff9c4,stroke:#f9a825,color:#5d4037
  classDef start fill:#eceff1,stroke:#546e7a,color:#263238

  class startNode,out start
  class shared,algo wiring
  class paper,scen,custom domain
  class scenQ question
```

## Presets

| Preset | Behaviour |
|--------|-----------|
| `paper` | Algorithm agent counts + behaviour defaults; world/layout from the selected scenario |
| `scenario` | Scenario `default_config` for agents + world |
| `custom` | Explicit `algorithm_params` / `world_overrides` / agent counts |

Session create accepts `preset`, optional `num_sheep` / `num_shepherds`, `algorithm_params`, and `world_overrides`.
