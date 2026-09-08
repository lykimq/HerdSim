# Contributing plugins

## Add an algorithm

```mermaid
flowchart TD
  startNode([Start])
  pkg[Create_algorithms_id]
  impl[Implement_BaseAlgorithm]
  reg[Register_in_registry]
  info[Add_info_json]
  docs[Write_research_algorithms_page]
  tests[Add_backend_tests]
  guide[Update_docs_API_whitelist_if_needed]
  endNode([Done])

  startNode --> pkg --> impl --> reg --> info --> docs --> tests --> guide --> endNode

  classDef ui fill:#cfe2f3,stroke:#1565c0,color:#0d47a1
  classDef wiring fill:#b2dfdb,stroke:#00796b,color:#004d40
  classDef domain fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20
  classDef shared fill:#e1bee7,stroke:#7b1fa2,color:#4a148c
  classDef transport fill:#ffe0b2,stroke:#ef6c00,color:#e65100
  classDef question fill:#fff9c4,stroke:#f9a825,color:#5d4037
  classDef start fill:#eceff1,stroke:#546e7a,color:#263238

  class startNode,endNode start
  class pkg,impl,docs domain
  class reg,info wiring
  class tests shared
  class guide ui
```

Legend: blue = UI, teal = wiring/config, green = domain models, purple = shared core, orange = transport, yellow = decision, grey = start/end.

1. Create `algorithms/<id>/` with `algorithm.py`, config module, optional helpers, `info.json` (optional `param_groups`).
2. Subclass `BaseAlgorithm` (`id`, `name`, `default_config`, `step`). Use `state.rng`; prefer `state.world.goal`.
3. Register in `algorithms/registry.py` `_auto_register()`.
4. Write `docs/research/algorithms/<page>.md` using the self-contained template (cite, write out algorithm, full param accounts, fidelity, code, tests). Link PDF under `docs/papers/` when present.
5. Add tests under `tests/backend/`.
6. If the Guide should list the page, ensure the slug is in the docs API whitelist.

## Add a metric

1. `metrics/<id>.py` subclassing `BaseMetric`
2. Register in `metrics/registry.py`
3. Document in `docs/research/metrics.md` and add a unit test

## Add a scenario

1. `scenarios/<id>.py` subclassing `BaseScenario`
2. `create_world`, `initial_positions`, `is_success`, `max_ticks`, `default_config`
3. Register in `scenarios/registry.py`
4. Document in `docs/research/scenarios.md`; add layout keys to `core/shared_defaults.WORLD_KEYS` and frontend `SCENARIO_WORLD_KEYS`

## Decision checklist (new algorithm)

1. Which paper (DOI) and figures/settings?
2. Fits sheep+shepherd `step()` without solver/trainer?
3. Which scenarios/metrics stay valid?
4. What adaptations (goal, walls, `dt`)?
5. Paper preset and success criterion?
6. Fair comparison notes vs Strombom/Kubo?
