# Scripts

Local helpers and CLI entry points that sit outside the web UI.

## `dev.sh`

Starts the FastAPI backend and Vite frontend together. Waits for the API
health check before launching the frontend. Ctrl+C stops both.

```bash
./scripts/dev.sh
# or: make dev
```

Optional env: `HERDSIM_API_URL`, `HERDSIM_API_WAIT_SECONDS`.

## `budget/`

Shepherding-budget campaign CLIs (also wired through `Makefile.budget`):

| Script | Role |
|--------|------|
| `budget/run_grid.py` | N x D (x layout / instrument) grid with resume |
| `budget/run_factor_sweep.py` | RQ5-style information / communication sweeps |
| `budget/analyse.py` | Export evidence packages under `packages/{a-g}/` |

```bash
make budget-help
# or: make -f Makefile.budget help
```

Campaign outputs land in `results/budget/phase{k}/{slug}/` (kept in git). See
[results/budget/README.md](../results/budget/README.md) and
[docs/architecture.md](../docs/architecture.md) (Shepherding-budget stack).

UI batch studies (fair compares, factor grids in the browser) still run from the
**Experiments** tab. See `docs/experiments.md` and
`docs/research/comparison_framework.md`.
