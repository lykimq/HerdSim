# Contributing plugins

## Add an algorithm

1. Create `algorithms/<id>/` with `algorithm.py`, a config module, optional helpers, and `info.json` (optional `param_groups`).
2. Subclass `BaseAlgorithm` (`id`, `name`, `default_config`, `step`). Use `state.rng`; prefer `state.world.goal`.
3. Register in `algorithms/registry.py` `_auto_register()`.
4. Write `docs/research/algorithms/<page>.md` with the citation, written-out algorithm, parameter accounts, fidelity notes, and code pointers. Place a PDF under `docs/papers/` when available. Add a row to the algorithms overview page.
5. Add tests under `tests/backend/` (see Testing).
6. To show the page in the Guide tab, add the slug to `DOC_SLUGS` in `api/routers/docs.py` and to `NAV` in `frontend/src/components/GuideView.js`.

```mermaid
flowchart TD
  startNode([Start])
  pkg[Create_algorithms_id]
  impl[Implement_BaseAlgorithm]
  reg[Register_in_registry]
  info[Add_info_json]
  docs[Write_research_algorithms_page]
  tests[Add_backend_tests]
  guide[Update_Guide_if_needed]
  endNode([Done])

  startNode --> pkg --> impl --> reg --> info --> docs --> tests --> guide --> endNode

  classDef domain fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20
  classDef wiring fill:#b2dfdb,stroke:#00796b,color:#004d40
  classDef shared fill:#e1bee7,stroke:#7b1fa2,color:#4a148c
  classDef ui fill:#cfe2f3,stroke:#1565c0,color:#0d47a1
  classDef start fill:#eceff1,stroke:#546e7a,color:#263238

  class startNode,endNode start
  class pkg,impl,docs domain
  class reg,info wiring
  class tests shared
  class guide ui
```

## Add a metric

1. `metrics/<id>.py` subclassing `BaseMetric`
2. Register in `metrics/registry.py`
3. Document in `docs/research/metrics.md` and add a unit test

## Add a scenario

1. `scenarios/<id>.py` subclassing `BaseScenario`
2. Implement `create_world`, `initial_positions`, `is_success`, `max_ticks`, `default_config`
3. Register in `scenarios/registry.py`
4. Document in `docs/research/scenarios.md`; add layout keys to `core/shared_defaults.WORLD_KEYS` and frontend `SCENARIO_WORLD_KEYS`
