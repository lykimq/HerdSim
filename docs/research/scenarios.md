# Scenarios

Each scenario is a pluggable task under `scenarios/`. Algorithms and scenarios are independent: any registered algorithm can run in any scenario.

| ID | What it reveals | Success criterion |
|----|-----------------|-------------------|
| `drive_to_goal` | Baseline herding into a corner goal | Fraction of sheep in goal >= `success_fraction` (default 1.0) |
| `containment` | Keeping a flock inside a pen over time | Pen occupancy >= `containment_fraction` sustained for `containment_min_ticks` |
| `obstacle_course` | Navigation around rectangular obstacles | Fraction in goal >= `success_fraction` |
| `split_flock` | Collect / recovery from 2-3 clusters | Fraction in goal >= `success_fraction` (default 0.95); may set `collect_threshold_scale` |
| `narrow_gate` | Choke-point herding through a gate | Fraction in goal >= `success_fraction` |
| `wide_field` | Long-drive efficiency on a larger arena | Fraction in goal >= `success_fraction` |

## Layout keys

Scenario-owned keys (merged under paper/custom presets) include world size, goal/pen geometry, obstacles, gate params (`gate_x`, `gate_width`, `wall_thickness`), containment thresholds, and optional `collect_threshold_scale`. See `core/shared_defaults.py` `WORLD_KEYS` and frontend `SCENARIO_WORLD_KEYS`.

## Success vs metrics

- Scenario **success** is whatever `BaseScenario.is_success` defines (fraction in goal, containment dwell time, etc.).
- Metric `success_rate` is instantaneous goal occupancy (fraction of sheep in the goal zone).
- Metric `time_to_goal` is strict: current tick only when **all** sheep are in the goal, else -1.
- Benchmark `first_success_tick` is the tick when the **scenario** criterion first held; it can differ from `time_to_goal` under partial `success_fraction`.

## Presets

- `paper` -- algorithm paper defaults (agents + behaviour); world from scenario
- `scenario` -- scenario `default_config` for agents + world
- `custom` -- explicit overrides

## Code

- Implementations: `scenarios/<id>.py`
- Registry: `scenarios/registry.py`
- Tests: `tests/backend/scenarios/` and config resolution tests under `tests/backend/correctness/`
