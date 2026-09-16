# Scripts

Only local development helpers live here.

## `dev.sh`

Starts the FastAPI backend and Vite frontend together. Waits for the API
health check before launching the frontend. Ctrl+C stops both.

```bash
./scripts/dev.sh
# or: make dev
```

Optional env: `HERDSIM_API_URL`, `HERDSIM_API_WAIT_SECONDS`.

Batch experiments, fair compares, and factor grids run in the **Experiments**
tab in the web UI (same `run_benchmark` engine). See
`docs/research/comparison_framework.md`.
