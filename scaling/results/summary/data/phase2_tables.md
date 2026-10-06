# Phase 2 data tables

Claim evidence is used for results. Scout evidence selected the precision windows and must not be read as the final estimate.

## Complete layout frontier

Source: [`phase2/claim/packages/b/frontier_by_layout.csv`](../../phase2/claim/packages/b/frontier_by_layout.csv).

| initial_layout | n_sheep | d_min | d_overcrowd | d_max | b_star_d | b_star_t | b_star_effort | hard_failure |
|---|---|---|---|---|---|---|---|---|
| compact | 50 | 1 |  | 35 | 1 | 10000.0 | 157.49999999999977 | False |
| compact | 100 | 1 |  | 35 | 1 | 10000.0 | 161.35167363755858 | False |
| compact | 200 | 1 |  | 35 | 1 | 10000.0 | 144.17124164542776 | False |
| outlier_rich | 50 | 1 |  | 35 | 1 | 10000.0 | 209.24999999999994 | False |
| outlier_rich | 100 | 1 |  | 35 | 1 | 10000.0 | 553.8718780756371 | False |
| outlier_rich | 200 | 1 |  | 35 | 1 | 10000.0 | 1646.6909610899515 | False |
| split | 50 | 1 |  | 35 | 1 | 10000.0 | 157.5 | False |
| split | 100 | 1 |  | 35 | 1 | 10000.0 | 161.95821333206823 | False |
| split | 200 | 1 |  | 35 | 1 | 10000.0 | 144.40420419240473 | False |
| wide | 50 | 1 |  | 35 | 2 | 10000.0 | 2336.832941075605 | False |
| wide | 100 | 1 |  | 35 | 2 | 10000.0 | 3003.1703685972398 | False |
| wide | 200 | 1 |  | 35 | 2 | 10000.0 | 3693.6903356986063 | False |

Every layout and N has `D_min = 1`, `D_max = 35` at the grid ceiling, and no overcrowding. Wide layouts have `B_star_D = 2` even though one dog is reliable.

## Complete D_min bootstrap intervals

Source: [`phase2/claim/merged_dmin_bootstrap.csv`](../../phase2/claim/merged_dmin_bootstrap.csv).

| method | initial_layout | n_sheep | d_min | d_min_ci_low | d_min_ci_high | n_boot | n_seeds_ref | n_boot_defined |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | compact | 50 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | compact | 100 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | compact | 200 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | outlier_rich | 50 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | outlier_rich | 100 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | outlier_rich | 200 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | split | 50 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | split | 100 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | split | 200 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | wide | 50 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | wide | 100 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | wide | 200 | 1 | 1 | 1 | 1000 | 100 | 1000 |

## One-dog cost by layout

Computed from all D = 1 claim-merge rows. Medians use successful trials only.

| Layout | N | Successes | Seeds | R | Median ticks | Median path |
|---|---|---|---|---|---|---|
| compact | 50 | 100 | 100 | 1 | 195 | 157.5 |
| compact | 100 | 100 | 100 | 1 | 204 | 161.352 |
| compact | 200 | 100 | 100 | 1 | 191 | 144.171 |
| outlier_rich | 50 | 100 | 100 | 1 | 223.5 | 209.25 |
| outlier_rich | 100 | 100 | 100 | 1 | 501 | 553.872 |
| outlier_rich | 200 | 100 | 100 | 1 | 1,228 | 1,646.691 |
| split | 50 | 100 | 100 | 1 | 195 | 157.5 |
| split | 100 | 100 | 100 | 1 | 205 | 161.958 |
| split | 200 | 100 | 100 | 1 | 193 | 144.404 |
| wide | 50 | 100 | 100 | 1 | 2,138.5 | 2,925.126 |
| wide | 100 | 100 | 100 | 1 | 3,074 | 4,319.485 |
| wide | 200 | 100 | 100 | 1 | 3,869.5 | 5,213.019 |

## Predictor comparison

Source: [`phase2/claim/packages/b/predictor_comparison.csv`](../../phase2/claim/packages/b/predictor_comparison.csv). This table is retained as evidence, but the state-predictor claim is inconclusive because the baseline D_min did not shift.

| n_folds | nd_nll | state_nll | prefers_state | state_cols | note |
|---|---|---|---|---|---|
| 0 |  |  | False | ['early_cohesion', 'early_gcm_goal', 'early_time_to_goal', 'early_shepherd_path', 'early_success_rate', 'early_sheep_in_goal', 'early_polarization', 'early_outlier_count', 'early_min_separation', 'early_fragmentation', 'early_mean_spread', 'early_extent', 'early_perimeter', 'early_hull_area', 'early_flock_density', 'early_aspect_ratio', 'early_i_dir', 'early_coverage'] | need at least two flock sizes and both outcomes |

## Schema for merged_trials tables

Each row is one simulation trial with one seed. Each data-set section reports the actual column count; these groups explain the shared schema.

| Group | Columns and meaning |
|---|---|
| Identity and design | method, scenario, preset, seed, sheep_model, dog_controller, obs_mode, n_sheep, n_shepherds, initial_layout, time_limit |
| Outcome and cost | success, total_ticks, time_to_goal, shepherd_path, first_success_tick, control_efficiency |
| Final state | final_gcm_goal, final_success_rate, final_sheep_in_goal, final_min_separation |
| Time summaries | mean_*, min_*, max_*, auc_* for recorded flock and dog metrics |
| Failure diagnostics | failure_mode, failure_label, failure_hints |
| Configuration | resolved_config, the serialized effective trial configuration |

## Claim merged trials

Full source: [`phase2/claim/merged_trials.csv`](../../phase2/claim/merged_trials.csv). The large table is not reproduced. The summaries below are computed directly from the CSV.

| Property | Value |
|---|---|
| Rows | 5,280 |
| Columns | 77 |
| Design cells | 120 |
| Methods | strombom_multi |
| Layouts | compact, outlier_rich, split, wide |
| N values | 50, 100, 200 |
| D values | 1, 2, 3, 4, 6, 10, 15, 20, 25, 35 |
| Seed range | 2026 to 2125 |

| Property | Value |
|---|---|
| Successes | 5,280 |
| Failures | 0 |
| Overall R | 1 |
| Median ticks, successes | 197 |
| P90 ticks, successes | 1,313 |
| Median path, successes | 1,802.569 |
| Failure modes | none |

Representative-row rule: sort lexicographically by `method`, `initial_layout`, `n_sheep`, `n_shepherds`, and `seed`, then take 5 evenly spaced positions including both endpoints. This reproducible rule does not select on outcome.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | compact | 50 | 1 | 2026 | True | 198 | 157.5 | none |
| strombom_multi | outlier_rich | 50 | 1 | 2026 | True | 434 | 362.088 | none |
| strombom_multi | split | 50 | 1 | 2026 | True | 195 | 151.5 | none |
| strombom_multi | split | 200 | 35 | 2055 | True | 181 | 4,681.49 | none |
| strombom_multi | wide | 200 | 35 | 2055 | True | 1544 | 53,992.82 | none |

## Direct sources

* [`phase2/claim/packages/b/frontier_by_layout.csv`](../../phase2/claim/packages/b/frontier_by_layout.csv)
* [`phase2/claim/packages/b/predictor_comparison.csv`](../../phase2/claim/packages/b/predictor_comparison.csv)
* [`phase2/claim/merged_dmin_bootstrap.csv`](../../phase2/claim/merged_dmin_bootstrap.csv)
* [`phase2/claim/merged_trials.csv`](../../phase2/claim/merged_trials.csv)
* [`phase2/claim/provenance.json`](../../phase2/claim/provenance.json)
* [`phase2/claim/status.json`](../../phase2/claim/status.json)
