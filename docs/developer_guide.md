# Developer Guide

## Add an algorithm (5 steps)
1. Create `algorithms/<id>/` with `algorithm.py`, config module, optional `forces.py`/`heuristics.py`, and `info.json`.
2. Subclass `BaseAlgorithm` (`id`, `name`, `default_config`, `step`).
3. Use `state.rng` for randomness; prefer `state.world.goal` for goal position.
4. Register the instance in `algorithms/registry.py` `_auto_register()`.
5. Add `docs/algorithms/<id>.md` using existing algorithm docs as templates, plus tests under `tests/backend/`.

## Add a metric (3 steps)
1. Create `metrics/<id>.py` subclassing `BaseMetric`.
2. Register the class in `metrics/registry.py`.
3. Document it in `docs/metrics_guide.md` and add a unit test.

## Add a scenario (4 steps)
1. Create `scenarios/<id>.py` subclassing `BaseScenario`.
2. Implement `create_world`, `initial_positions`, `is_success`, `max_ticks`.
3. Register in `scenarios/registry.py`.
4. Add tests in `tests/backend/scenarios/` and document layout keys in `core/shared_defaults.py`.

## Experiment presets
- `paper`: algorithm paper defaults (agent counts + behavior); world/layout from the selected scenario
- `scenario`: overlay scenario `default_config` (world + recommended agents)
- `custom`: user overrides for agents/world
Session create accepts `preset`, optional `num_sheep`/`num_shepherds`, `algorithm_params`, and `world_overrides`.

## Benchmarks
```bash
curl -X POST http://localhost:8000/api/benchmarks/run \
  -H 'Content-Type: application/json' \
  -d '{"algorithm_ids":["strombom","kubo"],"scenario_id":"split_flock","seeds":[1,2,3],"preset":"paper"}'
```

Or use the Analytics tab in the UI.

## Local development
```bash
pip install -e ".[dev]"
cd frontend && npm install
# terminal 1
uvicorn api.main:app --reload --port 8000
# terminal 2
cd frontend && npm run dev
```

Open http://localhost:5173

## Frontend architecture
Vanilla JS + Vite + PixiJS 8:
- `src/main.js` view router (Single / Arena / Analytics)
- `src/renderer/PixiRenderer.js` consumes backend `world` metadata
- `src/api/rest.js` + `src/api/websocket.js`

## Batch experiments
```bash
python scripts/run_batch.py --algorithm strombom --preset paper --seeds 1,2,3 --out results/strombom.csv
```

For research exports with experiment design, metric definitions, and caveats, use the Analytics tab (CSV / JSON; Markdown is a short summary note).