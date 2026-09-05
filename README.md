# HerdSim

Generic research platform for agent-based sheep herding simulations with pluggable algorithms, scenarios, and algorithm-agnostic metrics.

## Features
- Algorithms: Strombom, Kubo, Flocking Dog, Strombom Multi-Dog, Strombom Noise
- Scenarios: drive to goal, containment, obstacle course, split flock, narrow gate, wide field
- Paper / scenario / custom experiment presets
- Live Vanilla JS + PixiJS frontend (Single / Arena / Analytics)
- Multi-seed benchmark API + Analytics comparison tables
- FastAPI + WebSocket streaming
- Batch CLI experiments and CSV/Markdown export

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
python scripts/export_report.py --input results/kubo.csv --out results/kubo_report.md
```

## Documentation
- `docs/developer_guide.md`
- `docs/simulation_environment.md`
- `docs/metrics_guide.md`
- `docs/algorithms/strombom_2014.md`
- `docs/algorithms/kubo_2022.md`

## Project layout
- `core/` simulation engine
- `algorithms/` pluggable herding models
- `scenarios/` task definitions
- `metrics/` generic evaluation measures
- `api/` FastAPI + WebSocket
- `frontend/` Vanilla JS + PixiJS UI
- `matlab/` upstream force-based MATLAB reference
