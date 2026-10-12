# Simulation engine (`sim/`)

Tick-level shepherding simulation used by RQ campaigns (`cli/` + `protocols/`).

## Layout

```text
sim/
|-- core/                Runner, state, observation, config, world
|   |-- config/          Experiment factors + resolved run config
|   `-- world/           Arena, X0 layouts, goal, world defaults
|-- plugins/
|   |-- sheep/           Sheep dynamics + base + helpers
|   |-- dogs/            Dog controllers + base + helpers
|   |-- scenarios/       Task defs + BaseScenario
|   `-- metrics/         Metrics + BaseMetric
`-- methods/             Paper math (strombom, kubo)
```

## Methods

| Method | Sheep | Dog | Role |
|--------|-------|-----|------|
| `strombom` | strombom | collect_drive | Single-dog Collect/Drive base |
| `strombom_multi` | strombom | collect_drive_multi | RQ baseline |
| `kubo` | kubo | kubo_forces | RQ4 transfer |
| `fat` | strombom | fat | RQ4 transfer |
| `communication_free` | strombom | communication_free | Local Collect/Drive without sharing |

Scenario used by campaigns: `drive_to_goal`. All registered metrics are written into `trials.csv`.
