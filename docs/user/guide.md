# HerdSim user guide

HerdSim is a herding agent-based simulation platform: pluggable shepherding algorithms, task scenarios, shared metrics, live visualization, and multi-seed analytics. It is not a general NetLogo host for arbitrary models. Python algorithms power Single, Arena, and Analytics; the NetLogo tab opens Drive-to-Goal twins in the desktop NetLogo app for behavioural comparison.

## Views

| Tab | Role |
|-----|------|
| **Single** | One algorithm, one scenario, live metrics, trails, overlays, scrub history, end-of-run report |
| **Arena** | Side-by-side A/B with shared seed, scenario, and sheep count |
| **Analytics** | Multi-seed benchmarks and parameter sweeps; CSV / JSON export (Markdown methods note) |
| **NetLogo** | Open algorithm twins or other `.nlogo` files in desktop NetLogo; jump back to Single |
| **Guide** | In-app documentation from `docs/user/` and `docs/research/` |

## Presets

Experiment config merges shared world defaults, algorithm behaviour, and scenario layout.

| Preset | Meaning |
|--------|---------|
| **paper** | Algorithm published defaults (agent counts + behaviour parameters). World/layout still come from the selected scenario. |
| **scenario** | Scenario `default_config` overlays recommended agents and world/layout for that task. |
| **custom** | Explicit overrides for agents and world keys exposed in the control panel. |

Full parameter accounts (symbol, purpose, code location, expected effect) live under [../research/algorithms/](../research/algorithms/). The usage guide does not duplicate every symbol.

## First experiment

1. Open **Single**.
2. Choose an algorithm (for example `strombom`) and scenario `drive_to_goal`.
3. Leave preset on **paper** unless you are exploring layout changes.
4. Set a seed, create/reset the session, run or step.
5. Watch cohesion, occupancy, outliers, and GCM-goal; scrub Metric history when useful.
6. When the run finishes (success or timeout), read the Run report (methods-note wording: ticks, success criterion, path, cohesion).

## Compare and export

- **Arena** -- same seed and scenario; compare two algorithms visually and with live deltas.
- **Analytics** -- multi-seed algorithm comparison or a parameter grid; export **CSV** (trial rows) and **JSON** (full provenance: version, resolved config, metric definitions, caveats). Markdown is a short methods note from the same report model. Provenance does not include git commit hashes.
- Caveats in exports include time-step family differences (displacement-per-tick vs Kubo `dt`) and scenario success vs strict `time_to_goal`.

## Model documentation

- Algorithms: [../research/algorithms/](../research/algorithms/)
- Scenarios: [../research/scenarios.md](../research/scenarios.md)
- Metrics: [../research/metrics.md](../research/metrics.md)
- Environment (tick / `dt`, walls): [../research/environment.md](../research/environment.md)
- NetLogo twins: [../research/netlogo.md](../research/netlogo.md)
- Paper PDFs: [../papers/](../papers/)

## Codebase documentation

Extension and architecture notes: [../developer/](../developer/).
