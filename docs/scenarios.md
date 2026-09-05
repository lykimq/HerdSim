# HerdSim Scenarios

Each scenario is a pluggable task definition under `scenarios/`.
Algorithms and scenarios are independent: any algorithm can run in any scenario.

| ID | What it reveals |
|----|-----------------|
| `drive_to_goal` | Baseline herding into a corner goal |
| `containment` | Keeping a flock inside a pen over time |
| `obstacle_course` | Navigation around rectangular obstacles (layouts are config-driven) |
| `split_flock` | Collect / recovery when sheep start in 2-3 separated clusters |
| `narrow_gate` | Choke-point herding through a narrow gate |
| `wide_field` | Long-drive efficiency and scaling on a larger arena |

## Presets
- `paper`: algorithm paper defaults
- `scenario`: overlay that scenario's `default_config` (agent counts + world)
- `custom`: user overrides for agents/world

## Adding a scenario
1. Create `scenarios/<id>.py` subclassing `BaseScenario`
2. Provide `default_config`, `create_world`, `initial_positions`, `is_success`, `max_ticks`
3. Register in `scenarios/registry.py`
4. Add a row to this table
