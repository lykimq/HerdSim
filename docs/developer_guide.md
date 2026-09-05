# Developer Guide

## Add an algorithm (5 steps)
1. Create `algorithms/<id>/` with `algorithm.py`, config module, optional `forces.py`/`heuristics.py`, and `info.json`.
2. Subclass `BaseAlgorithm` (`id`, `name`, `default_config`, `step`).
3. Use `state.rng` for randomness; prefer `state.world.goal` for goal position.
4. Register the instance in `algorithms/registry.py` `_auto_register()`.
5. Add `docs/algorithms/<id>.md` using the template in `docs/implementation_plan.md` section 6, plus tests under `tests/backend/`.

## Add a metric (3 steps)
1. Create `metrics/<id>.py` subclassing `BaseMetric`.
2. Register the class in `metrics/registry.py`.
3. Document it in `docs/metrics_guide.md` and add a unit test.

## Add a scenario (4 steps)
1. Create `scenarios/<id>.py` subclassing `BaseScenario`.
2. Implement `create_world`, `initial_positions`, `is_success`, `max_ticks`.
3. Register in `scenarios/registry.py`.
4. Add tests in `tests/backend/test_scenarios.py`.

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
python scripts/run_batch.py --algorithm strombom --seeds 1,2,3 --out results/strombom.csv
python scripts/export_report.py --input results/strombom.csv --out results/report.md
```
