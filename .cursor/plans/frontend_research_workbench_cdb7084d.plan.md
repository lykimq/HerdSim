---
name: frontend research workbench
overview: Redesign all five HerdSim views as one coherent, responsive scientific workbench while retaining vanilla JavaScript and PixiJS. Preserve the current uncommitted factor work as the baseline, centralize product metadata, remove frontend legacy paths, and verify each workflow incrementally.
todos:
  - id: foundation
    content: Centralize experiment metadata and establish reusable design-system, status, form, and lifecycle primitives
    status: completed
  - id: shell-single
    content: Refactor the app shell and deliver the guided, responsive Simulate workspace
    status: completed
  - id: arena
    content: Deliver explicit fair/independent comparison workflows using shared controls and reports
    status: completed
  - id: analytics
    content: Deliver metadata-driven experiment design, progress, results hierarchy, and exports
    status: completed
  - id: netlogo-guide
    content: Align NetLogo and Guide with instrument terminology, dynamic metadata, and cross-navigation
    status: completed
  - id: cleanup-accessibility
    content: Remove frontend legacy/dead/duplicate paths and complete accessibility and responsive behavior
    status: completed
  - id: verification
    content: Add focused tests and progressively verify all five workflows, build, lint, and browser smoke behavior
    status: completed
isProject: false
---

# HerdSim Frontend Research Workbench

## Product direction

Keep the existing dark scientific-workbench identity, but reorganize the interface around user tasks rather than the old algorithm demo: **Simulate**, **Compare**, **Experiments**, **NetLogo**, and **Guide**. Use progressive disclosure so a first run is simple while model, sensing, heterogeneity, failure, environment, and advanced instrument parameters remain available.

Why: HerdSim now studies herdability, information limits, robustness, and generalization. The current UI exposes many of these features, but its layout, terminology, hardcoded metadata, and legacy sweep/algorithm paths still communicate the previous product model.

Trade-off: retaining vanilla JavaScript and PixiJS avoids a risky framework rewrite, but requires disciplined small components, shared render helpers, and explicit lifecycle cleanup.

## 1. Establish one frontend design and metadata foundation

- Refine tokens and reusable primitives in [`frontend/src/styles/variables.css`](frontend/src/styles/variables.css), [`frontend/src/styles/controls.css`](frontend/src/styles/controls.css), and new narrowly scoped style modules: spacing, type scale, semantic states, focus rings, cards, form rows, empty/loading/error states, and responsive breakpoints.
- Replace inline presentation styles and scattered color literals with semantic classes/tokens; keep runtime positioning/color only where data visualization requires it.
- Introduce shared UI helpers for safe markup, labeled fields, status/notice blocks, and listener cleanup instead of repeating DOM patterns across views.
- Extract the duplicated Single/Arena REST, WebSocket, history, playback, renderer-overlay, and teardown flow into one simulation-session controller built on [`frontend/src/utils/simulationSession.js`](frontend/src/utils/simulationSession.js). Keep view-specific rendering and status callbacks outside the controller.
- Consolidate repeated metric value/scale formatting and canvas hover helpers used by [`frontend/src/components/MetricsPanel.js`](frontend/src/components/MetricsPanel.js), [`frontend/src/components/MetricHistoryPanel.js`](frontend/src/components/MetricHistoryPanel.js), and [`frontend/src/components/DistributionPanel.js`](frontend/src/components/DistributionPanel.js).
- Make backend-owned experiment metadata the source of truth. Extend the existing metadata response in [`api/routers/algorithms.py`](api/routers/algorithms.py) from constants in [`core/experimental_factors.py`](core/experimental_factors.py), then consume it through [`frontend/src/api/rest.js`](frontend/src/api/rest.js) and [`frontend/src/utils/factors.js`](frontend/src/utils/factors.js). Keep transport names such as `algorithm_id` only at the API boundary.
- Preserve the current factor/session payload implementation; consolidate it rather than replacing working behavior.

## 2. Rebuild the application shell and navigation

- Refactor [`frontend/src/main.js`](frontend/src/main.js) into a small app shell plus view registry, with research-oriented labels, per-view descriptions, responsive navigation, consistent status display, and accessible active/focus states.
- Retain cached view behavior and pause-on-hide semantics, but centralize view metadata and lifecycle handling so navigation markup and switching logic do not drift.
- Replace the always-visible global seed/tick fields where they lack meaning with view-aware context; keep simulation state prominent in Simulate/Compare and experiment state in Analytics.
- Add clear boot, API failure, loading, and retry surfaces without hardcoded local filesystem instructions.

## 3. Turn Single into a guided simulation workspace

- Split [`frontend/src/components/ControlPanel.js`](frontend/src/components/ControlPanel.js), [`frontend/src/components/controlPanelMarkup.js`](frontend/src/components/controlPanelMarkup.js), [`frontend/src/components/controlPanelFactors.js`](frontend/src/components/controlPanelFactors.js), and [`frontend/src/components/controlPanelParams.js`](frontend/src/components/controlPanelParams.js) into focused shared sections: run setup, instrument/model, experimental factors, advanced parameters, playback, and display.
- Present the primary workflow in order: choose instrument and scenario, set agent counts/seed, optionally customize factors, initialize, then run. Show a compact resolved-configuration summary before initialization.
- Use factor metadata for human labels, descriptions, valid options/ranges, and conditional fields. Examples: sensing controls depend on observation mode; failure tick depends on failure mode; goal velocity depends on moving goals. Validate inline before creating a session.
- Rebalance [`frontend/src/components/SingleView.js`](frontend/src/components/SingleView.js) so the Pixi field remains primary, essential live outcomes are scannable, detailed distributions/history are collapsible, and the end-of-run report includes a download action using existing report helpers.
- Keep advanced paper parameters available without mixing them with scientific factor controls.

## 4. Make Arena a trustworthy comparison workspace

- Recompose [`frontend/src/components/ArenaView.js`](frontend/src/components/ArenaView.js), [`frontend/src/components/ArenaSide.js`](frontend/src/components/ArenaSide.js), and [`frontend/src/components/arenaMarkup.js`](frontend/src/components/arenaMarkup.js) around an explicit fair-comparison workflow.
- Put shared scenario, seed, counts, and locked factors in one comparison header; show each side's instrument/model/controller and intentional differences. Make independent runs a secondary mode instead of an implicit state transition.
- Reuse the same setup/factor components and payload builder as Single; do not duplicate controls or session rules.
- Improve deltas with metric direction/context and add compact per-side result summaries/history using existing metric and report components rather than new calculation paths.
- Add responsive stacking for narrower screens while preserving canvas resize behavior.

## 5. Make Analytics the experiment-design center

- Restructure [`frontend/src/components/AnalyticsDashboard.js`](frontend/src/components/AnalyticsDashboard.js), [`frontend/src/components/analyticsMarkup.js`](frontend/src/components/analyticsMarkup.js), and [`frontend/src/components/analyticsMode.js`](frontend/src/components/analyticsMode.js) into setup, design validation, run progress, and results stages.
- Keep instrument comparison and factor grid as distinct study types. Use metadata-driven, type-aware factor editors: enum selects, validated numeric values, unique keys, readable labels, and visible cell/trial/runtime scale before launch.
- Centralize study templates and grid parsing in the shared factor model; remove frontend `sweep` compatibility branches, hardcoded legacy default instrument IDs, and duplicated labels.
- Reorganize results so headline success/herdability findings appear first, followed by heatmap, distributions, efficiency trade-offs, detailed table, methods, and exports. Reuse existing Plotly functions in [`frontend/src/utils/analyticsCharts.js`](frontend/src/utils/analyticsCharts.js) and [`frontend/src/utils/analyticsFormat.js`](frontend/src/utils/analyticsFormat.js), extracting shared chart states/options rather than duplicating rendering logic.
- Replace the global Plotly CDN script in [`frontend/index.html`](frontend/index.html) with a pinned frontend dependency loaded only by Analytics, so builds and offline use are reproducible without loading the chart library in simulation-only workflows.
- Preserve streamed progress and exports; improve actionable validation/error/empty states without changing benchmark science.

## 6. Align NetLogo and Guide with the platform model

- Update [`frontend/src/components/NetLogoView.js`](frontend/src/components/NetLogoView.js) to use instrument-twin language, a short setup/status flow, clearer parity limitations, and shared form/status components. Retain upload and desktop-launch behavior.
- Refactor [`frontend/src/components/GuideView.js`](frontend/src/components/GuideView.js) to build navigation from the existing docs index and live instrument metadata instead of a hardcoded legacy list. Add lightweight filtering, local page outline, and deep links from instrument documentation to Simulate.
- Keep documentation single-source through the existing docs API; update [`docs/user_guide.md`](docs/user_guide.md) only where labels/workflows change, using ASCII-only prose.
- Remove stale variant-oriented links or copy only when they no longer represent active instrument bundles or supported docs.

## 7. Cleanup, accessibility, and progressive verification

- Rename internal frontend concepts from algorithm/sweep to instrument/factor-grid where the backend contract does not require legacy names; remove aliases, unreachable branches, unused helpers, repeated listeners, inline styles, and dead CSS after callers are migrated.
- Add keyboard navigation, form labels/descriptions, ARIA status/live regions, visible focus, reduced-motion support, contrast checks, and layouts for desktop/tablet/mobile.
- Extend existing `node:test` coverage under [`tests/frontend/`](tests/frontend/) for metadata normalization, factor dependencies/validation, payload boundaries, view-state reducers, grid design, and shared formatters. Add targeted backend metadata contract tests under [`tests/backend/api/`](tests/backend/api/).
- Verify progressively after each view: focused tests, `make test-frontend`, lint on edited files, then browser smoke tests at desktop and narrow widths for Simulate, fair Compare, a factor-grid Experiment, NetLogo status handling, and Guide navigation. Finish with the relevant backend API tests and a dead-code/legacy-term search.

## Implementation boundaries

- No React or other framework migration.
- No simulation-engine redesign and no duplicate scientific calculations in the browser.
- No removal of required backend compatibility fields; isolate them at transport boundaries.
- No unrelated reformatting, generated summary document, or replacement of the current working factor changes.
- All new comments and documentation remain ASCII-only and describe current behavior only.