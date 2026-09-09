# Testing

## Layout

| Area | Path |
|------|------|
| Backend correctness | `tests/backend/correctness/` |
| Backend scenarios | `tests/backend/scenarios/` |
| Frontend unit | `tests/frontend/*.test.js` |

## Expectations for a new algorithm

- Determinism: same seed yields the same trajectories (or document intentional RNG use).
- Registry lists the new id.
- Docs page exists under `docs/research/algorithms/` and any docs-sync test passes.
- Behavioural checks for novel thresholds, assignment, or heterogeneity rules.

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
