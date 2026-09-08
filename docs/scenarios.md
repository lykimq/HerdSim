# HerdSim Scenarios

Each scenario is a pluggable task definition under `scenarios/`.
Algorithms and scenarios are independent: any algorithm can run in any scenario.

| ID | What it reveals | Default success idea |
|----|-----------------|----------------------|
| `drive_to_goal` | Baseline herding into a corner goal | Fraction of sheep in goal >= `success_fraction` (default 1.0) |
| `containment` | Keeping a flock inside a pen over time | Pen occupancy >= `containment_fraction` after `containment_min_ticks` |
| `obstacle_course` | Navigation around rectangular obstacles | Fraction in goal >= `success_fraction` |
| `split_flock` | Collect / recovery from 2-3 clusters | Fraction in goal >= `success_fraction` (default 0.95); may set `collect_threshold_scale` |
| `narrow_gate` | Choke-point herding through a gate | Fraction in goal >= `success_fraction` |
| `wide_field` | Long-drive efficiency on a larger arena | Fraction in goal >= `success_fraction` |

Scenario-owned layout keys (merged under paper/custom presets) include world size, goal/pen geometry, obstacles, gate params (`gate_x`, `gate_width`, `wall_thickness`), containment thresholds, and optional `collect_threshold_scale`.

## Presets
- `paper`: algorithm paper defaults (agent counts + behavior); world/layout from the selected scenario
- `scenario`: overlay that scenario's `default_config` (agent counts + world)
- `custom`: user overrides for agents/world

## Adding a scenario
1. Create `scenarios/<id>.py` subclassing `BaseScenario`
2. Provide `default_config`, `create_world`, `initial_positions`, `is_success`, `max_ticks`
3. Register in `scenarios/registry.py`
4. Add a row to this table
5. Add any new layout keys to `core/shared_defaults.WORLD_KEYS` and `frontend/src/utils/params.js` `SCENARIO_WORLD_KEYS`
