---
name: Frontend factors docs tests
overview: Expose the existing factor-based backend in the frontend (Single/Arena/Analytics), align docs and UI language with instruments/factors, then add targeted tests so the product matches the herdability platform already implemented in core.
todos:
  - id: fe-factor-helpers
    content: Add frontend factors helpers + fetchModels REST client
    status: pending
  - id: fe-control-panel
    content: Wire Single/Arena control panel instrument + factor controls into session create
    status: pending
  - id: fe-analytics-grid
    content: Replace Analytics 2-param sweep with multi-key factor-grid UI and payloads
    status: pending
  - id: docs-copy
    content: Align user guide and UI labels with instruments/factors language
    status: pending
  - id: tests-factors-ui
    content: Add frontend factor tests and backend tests for UI-exposed factor paths
    status: pending
isProject: false
---

# Frontend factors, docs, and tests plan

## Goal

Make the UI and docs match the factor-based backend already shipped: users can run information, heterogeneity, failure, and multi-axis factor experiments from Single/Arena/Analytics without editing raw JSON or using only CLI scripts.

Do not redesign the simulation engine again. Wire existing APIs and factor keys into the product surface, then lock behavior with tests and docs.

## Current gap

Backend already supports:

- instruments / presets
- `sheep_model`, `dog_controller`, `obs_mode`, stubborn/cohesion/failure/goal factors
- multi-key factor grids via [api/benchmark_sweep.py](api/benchmark_sweep.py) and [scripts/run_factor_grid.py](scripts/run_factor_grid.py)

Frontend still centers on:

- "Algorithm" dropdown and `algorithm_id` in [ControlPanel.js](frontend/src/components/ControlPanel.js)
- paper/scenario/custom param panels in [controlPanelParams.js](frontend/src/components/controlPanelParams.js)
- Analytics compare + 2-key numeric sweep in [analyticsMode.js](frontend/src/components/analyticsMode.js)
- user guide language about algorithms only in [docs/user_guide.md](docs/user_guide.md)

---

## Phase 1: Shared frontend factor model

Add a small shared factor helpers module, e.g. [frontend/src/utils/factors.js](frontend/src/utils/factors.js):

- canonical factor groups and labels (flock, shepherds, observation, environment, model)
- allowlisted factor keys matching backend (`obs_mode`, `sensing_range`, `noise_sigma`, `communication`, `stubborn_fraction`, `cohesion_scale`, `failure_mode`, `failure_tick`, `goal_mode`, `speed_scale`, ...)
- helpers to build `createSession` / benchmark payloads:
  - keep `algorithm_id` / instrument for preset selection
  - add `sheep_model`, `dog_controller`, `obs_mode`, and factor overrides into `algorithm_params` / top-level fields the API already accepts

Extend [frontend/src/api/rest.js](frontend/src/api/rest.js):

- `fetchModels()` -> `GET /api/algorithms/meta/models`
- keep `fetchAlgorithms()` as instrument list

Why: one payload builder for Single, Arena, and Analytics avoids duplicated factor wiring.

---

## Phase 2: Single / Arena control panel factors

Update [controlPanelMarkup.js](frontend/src/components/controlPanelMarkup.js), [ControlPanel.js](frontend/src/components/ControlPanel.js), and [controlPanelParams.js](frontend/src/components/controlPanelParams.js):

1. Relabel **Algorithm** to **Instrument** (still backed by presets).
2. Add an **Experimental factors** section (custom preset editable; paper/scenario show resolved values read-only):
   - Model: `sheep_model`, `dog_controller` selects from `/meta/models`
   - Observation: `obs_mode`, `sensing_range`, `noise_sigma`, `communication`
   - Flock: `stubborn_fraction`, `cohesion_scale`
   - Shepherds: `failure_mode`, `failure_tick`, optional `speed_scale`
   - Environment: `goal_mode` (and goal velocity when moving)
3. When instrument changes, seed sheep/dog defaults from the preset, but allow custom overrides.
4. `getConfig()` / session create must send instrument + factor fields so backend observation/failure paths are actually used from the UI.

Also update Arena side payloads in [ArenaSide.js](frontend/src/components/ArenaSide.js) to pass the same factor config.

Keep advanced numeric paper params in the existing Settings details panel; do not dump every backend key into the new factor section.

---

## Phase 3: Analytics factor-grid UI

Update Analytics runner mode in [analyticsMode.js](frontend/src/components/analyticsMode.js), [analyticsSweep.js](frontend/src/utils/analyticsSweep.js), and related markup:

1. Rename compare "algorithms" to "instruments".
2. Replace/extend the old 2-param numeric sweep with a **Factor grid** mode:
   - add/remove factor rows (key + comma-separated values)
   - key dropdown from allowlisted scientific factors plus selected instrument numeric params
   - no hard UI cap at 2 keys; show estimated cell count and warn near backend `MAX_FACTOR_GRID_CELLS`
3. Build benchmark payload `sweep: [{key, values}, ...]` exactly as the backend grid API expects.
4. Summary/charts continue to use `sweep_label` / `factor_label` already returned by the runner.

Optional small enhancement: preset grid templates ("Herdability N x M", "Sensing degradation", "Stubborn fraction") that fill the factor rows.

---

## Phase 4: Docs and copy alignment

Update docs and UI strings so they describe the shipped platform:

- [docs/user_guide.md](docs/user_guide.md): instrument + factors workflow; how to run sensing / heterogeneity / factor-grid experiments in Analytics; point to CLI scripts for larger grids
- [frontend/src/utils/params.js](frontend/src/utils/params.js): rename preset labels from "Algorithm (paper)" to "Instrument (paper)" / equivalent
- Short notes on existing instrument pages that they are presets over sheep_model x dog_controller
- Guide nav already lists FAT/adaptive/communication-free; ensure user guide mentions them as instruments

No new long markdown report files. Keep ASCII-only docs.

---

## Phase 5: Tests

### Frontend

Add focused Node tests (same style as existing frontend tests):

- `factors.js` payload builder: instrument + obs_mode + stubborn_fraction serialization
- Analytics factor-grid parser: multi-key specs, rejects empty values, estimates cell count
- Control-panel config shape includes factor fields when custom

### Backend

Fill coverage gaps around features the UI will expose:

- API create session with `obs_mode=local_positions` / `bearing_only` and assert config echo
- FAT / communication-free / adaptive controller behaviour smoke tests (mode metadata, local-obs no crash)
- failure_mode inactive/blind/reduced-speed changes shepherd masks
- robot constraint helpers clamp velocity/latency
- `run_factor_grid` / generalization helper unit tests for parsing and report shape (not full long grids)

### Docs

- Extend docs sync / Guide whitelist checks if new user-guide sections or slugs are added
- Keep instrument info.json + docs pages in sync for presets shown in UI

---

## Phase 6: Deferred product polish (only after 1-5)

Not required to close the frontend gap, but next if continuing:

- richer Analytics visualizations for herdability heatmaps from factor grids
- in-app launchers for generalization / empirical-gap scripts
- deeper RL / Jadhav fitting / behavioural validation research pipelines

---

## Implementation order

1. `frontend/src/utils/factors.js` + REST `fetchModels`
2. Control panel factor section + session payload wiring (Single/Arena)
3. Analytics factor-grid mode
4. User guide + preset/label copy
5. Frontend and backend tests for the new paths
6. Manual smoke: create session with local sensing; run Analytics herdability grid; confirm Guide text matches UI

## Success criteria

- From Single, a user can select instrument `strombom`, set `obs_mode=local_positions`, `stubborn_fraction=0.5`, initialize, and see a run that uses those backend factors.
- From Analytics, a user can run a 3-axis grid such as `n_sheep x n_shepherds x obs_mode` and export labeled trial rows.
- User guide and control-panel labels speak in instruments/factors, not only "algorithms".
- New frontend factor helpers and backend factor-exposed paths have tests; existing backend suite stays green.
