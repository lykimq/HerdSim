# Testing

## Layout

| Area | Path |
|------|------|
| Backend correctness | `tests/backend/correctness/` |
| Backend scenarios | `tests/backend/scenarios/` |
| Frontend unit | `tests/frontend/*.test.js` |

## Expectations for a new algorithm

- Determinism: same seed => same trajectories (or documented RNG use).
- Registry lists the new id.
- Docs page exists under `docs/research/algorithms/` and sync test (if present) passes.
- Behavioural checks for any novel threshold, assignment, or heterogeneity rule.

## Commands

```bash
pytest tests/backend/ -q -m "not stress"
node --test tests/frontend/*.test.js
```

## Local stack

```bash
pip install -e ".[dev]"
cd frontend && npm install && cd ..
uvicorn api.main:app --reload --port 8000
cd frontend && npm run dev
```
