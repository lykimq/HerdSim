# HerdSim

Generic research platform for agent-based sheep herding simulations with pluggable algorithms, scenarios, and algorithm-agnostic metrics.

## Features
- Algorithms: Strombom, Kubo, Flocking Dog, Strombom Multi-Dog, Strombom Noise (plus roadmap additions as registered)
- Scenarios: drive to goal, containment, obstacle course, split flock, narrow gate, wide field
- Paper / scenario / custom experiment presets
- Live Vanilla JS + PixiJS frontend (Single / Arena / Analytics / NetLogo / Guide)
- Multi-seed benchmark API + Analytics comparison tables
- FastAPI + WebSocket streaming
- Batch CLI trials (`scripts/run_batch.py`) and Analytics UI CSV/JSON/Markdown export

## Quick start

```bash
pip install -e ".[dev]"
cd frontend && npm install && cd ..

# API
uvicorn api.main:app --reload --port 8000

# UI (separate terminal)
cd frontend && npm run dev
```

Open http://localhost:5173

## Tests

```bash
pytest tests/backend/ -v
cd frontend && npm run build
```

## Batch runs

```bash
python scripts/run_batch.py --algorithm kubo --n-shepherds 4 --seeds 1,2,3 --out results/kubo.csv
```

For comparison tables with provenance and caveats, use the Analytics tab Export CSV / JSON (Markdown is a short methods note).

## Documentation

- Guide tab (in-app): [`docs/research/`](docs/research/) -- algorithms, scenarios, metrics, environment, NetLogo
- Codebase: [`docs/developer/README.md`](docs/developer/README.md) -- architecture, configuration, and extending the simulator
- Paper PDFs: [`docs/papers/`](docs/papers/)

## Project layout
- `core/` simulation engine
- `algorithms/` pluggable herding models
- `scenarios/` task definitions
- `metrics/` generic evaluation measures
- `api/` FastAPI + WebSocket
- `frontend/` Vanilla JS + PixiJS UI
- `matlab/` upstream force-based MATLAB reference
