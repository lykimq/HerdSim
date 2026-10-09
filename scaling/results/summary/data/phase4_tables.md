# Phase 4 data tables

Controller conclusions use claim merges. Scout grids remain planning evidence. The Package D tables compare claim-grade controller results.

## Compact-start size frontiers

Kubo source: [`phase4/kubo_size/claim/packages/a/frontier.csv`](../../phase4/kubo_size/claim/packages/a/frontier.csv).

| initial_layout | n_sheep | d_min | d_overcrowd | d_max | b_star_d | hard_failure |
|---|---|---|---|---|---|---|
| compact | 5 | 3 |  | 35 | 3 | False |
| compact | 10 | 1 |  | 35 | 1 | False |
| compact | 25 | 1 |  | 35 | 1 | False |
| compact | 50 | 1 |  | 35 | 1 | False |
| compact | 75 | 1 |  | 35 | 1 | False |
| compact | 100 | 1 |  | 35 | 1 | False |
| compact | 150 | 1 |  | 35 | 1 | False |
| compact | 200 | 1 |  | 35 | 1 | False |
| compact | 300 | 1 |  | 35 | 1 | False |
| compact | 400 | 1 |  | 35 | 1 | False |

FAT source: [`phase4/fat_size/claim/packages/a/frontier.csv`](../../phase4/fat_size/claim/packages/a/frontier.csv).

| initial_layout | n_sheep | d_min | d_overcrowd | d_max | b_star_d | hard_failure |
|---|---|---|---|---|---|---|
| compact | 5 | 1.0 |  | 35.0 | 1.0 | False |
| compact | 10 | 1.0 |  | 35.0 | 3.0 | False |
| compact | 25 |  |  |  |  | True |
| compact | 50 |  |  |  |  | True |
| compact | 75 |  |  |  |  | True |
| compact | 100 |  |  |  |  | True |
| compact | 150 |  |  |  |  | True |
| compact | 200 |  |  |  |  | True |
| compact | 300 |  |  |  |  | True |
| compact | 400 |  |  |  |  | True |

Blank frontier fields with `hard_failure = True` mean no tested D reached R = 0.90. They are not an upper-bound estimate.

## Complete size D_min bootstrap intervals

Kubo source: [`phase4/kubo_size/claim/packages/a/dmin_bootstrap.csv`](../../phase4/kubo_size/claim/packages/a/dmin_bootstrap.csv).

| initial_layout | n_sheep | d_min | d_min_ci_low | d_min_ci_high | n_boot | n_seeds_ref | n_boot_defined |
|---|---|---|---|---|---|---|---|
| compact | 5 | 3 | 1 | 3 | 1000 | 100 | 1000 |
| compact | 10 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 25 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 50 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 75 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 100 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 150 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 200 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 300 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 400 | 1 | 1 | 1 | 1000 | 100 | 1000 |

FAT source: [`phase4/fat_size/claim/packages/a/dmin_bootstrap.csv`](../../phase4/fat_size/claim/packages/a/dmin_bootstrap.csv).

| initial_layout | n_sheep | d_min | d_min_ci_low | d_min_ci_high | d_min_ci_low_above_grid | d_min_ci_high_above_grid | n_boot | n_seeds_ref | n_boot_defined |
|---|---|---|---|---|---|---|---|---|---|
| compact | 5 | 1.0 | 1.0 | 1.0 | False | False | 1000 | 100 | 1000 |
| compact | 10 | 1.0 | 1.0 | 1.0 | False | False | 1000 | 100 | 1000 |
| compact | 25 |  | 2.0 |  | False | True | 1000 | 100 | 130 |
| compact | 50 |  |  |  | True | True | 1000 | 100 | 0 |
| compact | 75 |  |  |  | True | True | 1000 | 100 | 0 |
| compact | 100 |  |  |  | True | True | 1000 | 100 | 0 |
| compact | 150 |  |  |  | True | True | 1000 | 100 | 0 |
| compact | 200 |  |  |  | True | True | 1000 | 100 | 0 |
| compact | 300 |  |  |  | True | True | 1000 | 100 | 0 |
| compact | 400 |  |  |  | True | True | 1000 | 100 | 0 |

## Complete controller and layout frontier

Source: [`phase4/package_d/structure/frontier_by_method_layout.csv`](../../phase4/package_d/structure/frontier_by_method_layout.csv).

| method | initial_layout | n_sheep | d_min | d_overcrowd | d_max | b_star_d | hard_failure |
|---|---|---|---|---|---|---|---|
| fat | compact | 50 |  |  |  |  | True |
| fat | compact | 100 |  |  |  |  | True |
| fat | compact | 200 |  |  |  |  | True |
| fat | outlier_rich | 50 |  |  |  |  | True |
| fat | outlier_rich | 100 |  |  |  |  | True |
| fat | outlier_rich | 200 |  |  |  |  | True |
| fat | split | 50 |  |  |  |  | True |
| fat | split | 100 |  |  |  |  | True |
| fat | split | 200 |  |  |  |  | True |
| fat | wide | 50 |  |  |  |  | True |
| fat | wide | 100 |  |  |  |  | True |
| fat | wide | 200 |  |  |  |  | True |
| kubo | compact | 50 | 1.0 |  | 35.0 | 1.0 | False |
| kubo | compact | 100 | 1.0 |  | 35.0 | 1.0 | False |
| kubo | compact | 200 | 1.0 |  | 35.0 | 1.0 | False |
| kubo | outlier_rich | 50 | 1.0 |  | 35.0 | 1.0 | False |
| kubo | outlier_rich | 100 | 1.0 |  | 35.0 | 1.0 | False |
| kubo | outlier_rich | 200 | 20.0 |  | 35.0 | 20.0 | False |
| kubo | split | 50 | 1.0 |  | 35.0 | 1.0 | False |
| kubo | split | 100 | 1.0 |  | 35.0 | 1.0 | False |
| kubo | split | 200 | 1.0 |  | 35.0 | 1.0 | False |
| kubo | wide | 50 |  |  |  |  | True |
| kubo | wide | 100 |  |  |  |  | True |
| kubo | wide | 200 |  |  |  |  | True |
| strombom_multi | compact | 50 | 1.0 |  | 35.0 | 1.0 | False |
| strombom_multi | compact | 100 | 1.0 |  | 35.0 | 1.0 | False |
| strombom_multi | compact | 200 | 1.0 |  | 35.0 | 1.0 | False |
| strombom_multi | outlier_rich | 50 | 1.0 |  | 35.0 | 1.0 | False |
| strombom_multi | outlier_rich | 100 | 1.0 |  | 35.0 | 1.0 | False |
| strombom_multi | outlier_rich | 200 | 1.0 |  | 35.0 | 1.0 | False |
| strombom_multi | split | 50 | 1.0 |  | 35.0 | 1.0 | False |
| strombom_multi | split | 100 | 1.0 |  | 35.0 | 1.0 | False |
| strombom_multi | split | 200 | 1.0 |  | 35.0 | 1.0 | False |
| strombom_multi | wide | 50 | 1.0 |  | 35.0 | 2.0 | False |
| strombom_multi | wide | 100 | 1.0 |  | 35.0 | 2.0 | False |
| strombom_multi | wide | 200 | 1.0 |  | 35.0 | 2.0 | False |

## Kubo outlier-rich, N = 200

Source: [`phase4/kubo_structure/claim/outlier_rich_n200_window.json`](../../phase4/kubo_structure/claim/outlier_rich_n200_window.json).

| D | Seeds | R | R >= 0.90 |
|---|---|---|---|
| 1 | 200 | 0.745 | no |
| 2 | 200 | 0.855 | no |
| 3 | 200 | 0.835 | no |
| 4 | 200 | 0.86 | no |
| 6 | 200 | 0.89 | no |
| 10 | 200 | 0.875 | no |
| 15 | 200 | 0.855 | no |
| 20 | 200 | 0.935 | yes |
| 25 | 200 | 0.91 | yes |
| 35 | 30 | 0.967 | yes |

Point D_min: 20. Bootstrap interval: [2, 20]. The D = 35 value has 30 scout seeds because that cell was not claim-reseeded; the D = 1 through 25 values shown above have 200 claim seeds.

## Complete size-transfer evidence

Summary source: [`phase4/package_d/size/transfer_summary.csv`](../../phase4/package_d/size/transfer_summary.csv).

| n_rows | n_shared | n_shifted | n_absent |
|---|---|---|---|
| 44 | 8 | 7 | 29 |

Detailed source: [`phase4/package_d/size/transfer_table.csv`](../../phase4/package_d/size/transfer_table.csv).

| feature | n_sheep | baseline | method | baseline_value | method_value | transfer_label |
|---|---|---|---|---|---|---|
| d_min | 5.0 | strombom_multi | kubo | 2 | 3 | shifted |
| d_min | 10.0 | strombom_multi | kubo | 2 | 1 | shifted |
| d_min | 25.0 | strombom_multi | kubo | 1 | 1 | shared |
| d_min | 50.0 | strombom_multi | kubo | 1 | 1 | shared |
| d_min | 75.0 | strombom_multi | kubo | 1 | 1 | shared |
| d_min | 100.0 | strombom_multi | kubo | 1 | 1 | shared |
| d_min | 150.0 | strombom_multi | kubo | 1 | 1 | shared |
| d_min | 200.0 | strombom_multi | kubo | 1 | 1 | shared |
| d_min | 300.0 | strombom_multi | kubo | 1 | 1 | shared |
| d_min | 400.0 | strombom_multi | kubo | 1 | 1 | shared |
| overcrowd | 5.0 | strombom_multi | kubo |  |  | absent |
| overcrowd | 10.0 | strombom_multi | kubo |  |  | absent |
| overcrowd | 25.0 | strombom_multi | kubo |  |  | absent |
| overcrowd | 50.0 | strombom_multi | kubo |  |  | absent |
| overcrowd | 75.0 | strombom_multi | kubo |  |  | absent |
| overcrowd | 100.0 | strombom_multi | kubo |  |  | absent |
| overcrowd | 150.0 | strombom_multi | kubo |  |  | absent |
| overcrowd | 200.0 | strombom_multi | kubo |  |  | absent |
| overcrowd | 300.0 | strombom_multi | kubo |  |  | absent |
| overcrowd | 400.0 | strombom_multi | kubo |  |  | absent |
| i_dir_signature |  | strombom_multi | kubo | 0.261464147747486 | -0.0018854696882589974 | absent |
| coverage_saturation |  | strombom_multi | kubo | True | False | shifted |
| d_min | 5.0 | strombom_multi | fat | 2 | 1.0 | shifted |
| d_min | 10.0 | strombom_multi | fat | 2 | 1.0 | shifted |
| d_min | 25.0 | strombom_multi | fat | 1 |  | absent |
| d_min | 50.0 | strombom_multi | fat | 1 |  | absent |
| d_min | 75.0 | strombom_multi | fat | 1 |  | absent |
| d_min | 100.0 | strombom_multi | fat | 1 |  | absent |
| d_min | 150.0 | strombom_multi | fat | 1 |  | absent |
| d_min | 200.0 | strombom_multi | fat | 1 |  | absent |
| d_min | 300.0 | strombom_multi | fat | 1 |  | absent |
| d_min | 400.0 | strombom_multi | fat | 1 |  | absent |
| overcrowd | 5.0 | strombom_multi | fat |  |  | absent |
| overcrowd | 10.0 | strombom_multi | fat |  |  | absent |
| overcrowd | 25.0 | strombom_multi | fat |  |  | absent |
| overcrowd | 50.0 | strombom_multi | fat |  |  | absent |
| overcrowd | 75.0 | strombom_multi | fat |  |  | absent |
| overcrowd | 100.0 | strombom_multi | fat |  |  | absent |
| overcrowd | 150.0 | strombom_multi | fat |  |  | absent |
| overcrowd | 200.0 | strombom_multi | fat |  |  | absent |
| overcrowd | 300.0 | strombom_multi | fat |  |  | absent |
| overcrowd | 400.0 | strombom_multi | fat |  |  | absent |
| i_dir_signature |  | strombom_multi | fat | 0.261464147747486 | -0.8678074971276444 | shifted |
| coverage_saturation |  | strombom_multi | fat | True |  | shifted |

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

## Phase 4 Kubo size claim merge

Full source: [`phase4/kubo_size/claim/merged_trials.csv`](../../phase4/kubo_size/claim/merged_trials.csv). The large table is not reproduced. The summaries below are computed directly from the CSV.

| Property | Value |
|---|---|
| Rows | 4,470 |
| Columns | 77 |
| Design cells | 100 |
| Methods | kubo |
| Layouts | compact |
| N values | 5, 10, 25, 50, 75, 100, 150, 200, 300, 400 |
| D values | 1, 2, 3, 4, 6, 10, 15, 20, 25, 35 |
| Seed range | 2026 to 2125 |

| Property | Value |
|---|---|
| Successes | 4,428 |
| Failures | 42 |
| Overall R | 0.991 |
| Median ticks, successes | 826 |
| P90 ticks, successes | 1,785.3 |
| Median path, successes | 291.202 |
| Failure modes | timeout: 42 |

Representative-row rule: sort lexicographically by `method`, `initial_layout`, `n_sheep`, `n_shepherds`, and `seed`, then take 5 evenly spaced positions including both endpoints. This reproducible rule does not select on outcome.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| kubo | compact | 5 | 1 | 2026 | True | 1133 | 115.167 | none |
| kubo | compact | 25 | 2 | 2093 | True | 941 | 213.556 | none |
| kubo | compact | 75 | 25 | 2050 | True | 670 | 1,810 | none |
| kubo | compact | 200 | 3 | 2028 | True | 699 | 233.401 | none |
| kubo | compact | 400 | 35 | 2055 | True | 558 | 2,427.984 | none |

## Phase 4 FAT size claim merge

Full source: [`phase4/fat_size/claim/merged_trials.csv`](../../phase4/fat_size/claim/merged_trials.csv). The large table is not reproduced. The summaries below are computed directly from the CSV.

| Property | Value |
|---|---|
| Rows | 4,400 |
| Columns | 77 |
| Design cells | 100 |
| Methods | fat |
| Layouts | compact |
| N values | 5, 10, 25, 50, 75, 100, 150, 200, 300, 400 |
| D values | 1, 2, 3, 4, 6, 10, 15, 20, 25, 35 |
| Seed range | 2026 to 2125 |

| Property | Value |
|---|---|
| Successes | 2,194 |
| Failures | 2,206 |
| Overall R | 0.499 |
| Median ticks, successes | 232 |
| P90 ticks, successes | 2,371.8 |
| Median path, successes | 3,183 |
| Failure modes | oscillation: 1707, stuck: 295, timeout: 204 |

Representative-row rule: sort lexicographically by `method`, `initial_layout`, `n_sheep`, `n_shepherds`, and `seed`, then take 5 evenly spaced positions including both endpoints. This reproducible rule does not select on outcome.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| fat | compact | 5 | 1 | 2026 | True | 177 | 168 | none |
| fat | compact | 25 | 20 | 2036 | True | 182 | 3,190.5 | none |
| fat | compact | 100 | 1 | 2026 | True | 216 | 162 | none |
| fat | compact | 200 | 20 | 2035 | False | 10000 | 285,885 | oscillation |
| fat | compact | 400 | 35 | 2125 | True | 262 | 5,652 | none |

## Phase 4 Kubo structure claim merge

Full source: [`phase4/kubo_structure/claim/merged_trials.csv`](../../phase4/kubo_structure/claim/merged_trials.csv). The large table is not reproduced. The summaries below are computed directly from the CSV.

| Property | Value |
|---|---|
| Rows | 6,670 |
| Columns | 77 |
| Design cells | 120 |
| Methods | kubo |
| Layouts | compact, outlier_rich, split, wide |
| N values | 50, 100, 200 |
| D values | 1, 2, 3, 4, 6, 10, 15, 20, 25, 35 |
| Seed range | 2026 to 2225 |

| Property | Value |
|---|---|
| Successes | 5,679 |
| Failures | 991 |
| Overall R | 0.851 |
| Median ticks, successes | 1,093 |
| P90 ticks, successes | 3,193.2 |
| Median path, successes | 916.136 |
| Failure modes | scatter: 320, stuck: 13, timeout: 658 |

Representative-row rule: sort lexicographically by `method`, `initial_layout`, `n_sheep`, `n_shepherds`, and `seed`, then take 5 evenly spaced positions including both endpoints. This reproducible rule does not select on outcome.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| kubo | compact | 50 | 1 | 2026 | True | 1062 | 117.755 | none |
| kubo | outlier_rich | 50 | 15 | 2053 | True | 873 | 1,339.3 | none |
| kubo | outlier_rich | 200 | 10 | 2160 | True | 2203 | 2,609.883 | none |
| kubo | split | 200 | 1 | 2118 | True | 990 | 109.823 | none |
| kubo | wide | 200 | 35 | 2125 | False | 10000 | 24,723.948 | timeout |

## Phase 4 FAT structure claim merge

Full source: [`phase4/fat_structure/claim/merged_trials.csv`](../../phase4/fat_structure/claim/merged_trials.csv). The large table is not reproduced. The summaries below are computed directly from the CSV.

| Property | Value |
|---|---|
| Rows | 5,280 |
| Columns | 77 |
| Design cells | 120 |
| Methods | fat |
| Layouts | compact, outlier_rich, split, wide |
| N values | 50, 100, 200 |
| D values | 1, 2, 3, 4, 6, 10, 15, 20, 25, 35 |
| Seed range | 2026 to 2125 |

| Property | Value |
|---|---|
| Successes | 906 |
| Failures | 4,374 |
| Overall R | 0.172 |
| Median ticks, successes | 215 |
| P90 ticks, successes | 243 |
| Median path, successes | 3,211.5 |
| Failure modes | oscillation: 2014, scatter: 474, split: 1298, stuck: 286, timeout: 302 |

Representative-row rule: sort lexicographically by `method`, `initial_layout`, `n_sheep`, `n_shepherds`, and `seed`, then take 5 evenly spaced positions including both endpoints. This reproducible rule does not select on outcome.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| fat | compact | 50 | 1 | 2026 | False | 10000 | 14,477.666 | oscillation |
| fat | outlier_rich | 50 | 1 | 2026 | False | 10000 | 13,264.5 | stuck |
| fat | split | 50 | 1 | 2026 | True | 205 | 160.5 | none |
| fat | split | 200 | 35 | 2125 | False | 10000 | 501,004.5 | oscillation |
| fat | wide | 200 | 35 | 2125 | False | 10000 | 524,968.5 | split |

## Phase 5 observation claim merge

Full source: [`phase5/obs_claim/merged_trials.csv`](../../phase5/obs_claim/merged_trials.csv). The large table is not reproduced. The summaries below are computed directly from the CSV.

| Property | Value |
|---|---|
| Rows | 1,920 |
| Columns | 77 |
| Design cells | 12 |
| Methods | strombom_multi |
| Layouts | compact |
| N values | 100, 200 |
| D values | 1, 2, 3, 4, 6, 10 |
| Seed range | 2026 to 2125 |

| Property | Value |
|---|---|
| Successes | 1,280 |
| Failures | 640 |
| Overall R | 0.667 |
| Median ticks, successes | 189 |
| P90 ticks, successes | 203 |
| Median path, successes | 294.917 |
| Failure modes | oscillation: 640 |

Representative-row rule: sort lexicographically by `method`, `initial_layout`, `n_sheep`, `n_shepherds`, and `seed`, then take 5 evenly spaced positions including both endpoints. This reproducible rule does not select on outcome.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | compact | 100 | 1 | 2026 | False | 10000 | 0 | oscillation |
| strombom_multi | compact | 100 | 3 | 2032 | True | 193 | 456.715 | none |
| strombom_multi | compact | 200 | 1 | 2026 | False | 10000 | 0 | oscillation |
| strombom_multi | compact | 200 | 3 | 2032 | True | 181 | 404.507 | none |
| strombom_multi | compact | 200 | 10 | 2125 | False | 10000 | 0 | oscillation |

## Phase 5 range claim merge

Full source: [`phase5/range_claim/merged_trials.csv`](../../phase5/range_claim/merged_trials.csv). The large table is not reproduced. The summaries below are computed directly from the CSV.

| Property | Value |
|---|---|
| Rows | 2,560 |
| Columns | 78 |
| Design cells | 12 |
| Methods | strombom_multi |
| Layouts | compact |
| N values | 100, 200 |
| D values | 1, 2, 3, 4, 6, 10 |
| Seed range | 2026 to 2125 |

| Property | Value |
|---|---|
| Successes | 2,560 |
| Failures | 0 |
| Overall R | 1 |
| Median ticks, successes | 189 |
| P90 ticks, successes | 203 |
| Median path, successes | 295.197 |
| Failure modes | none |

Representative-row rule: sort lexicographically by `method`, `initial_layout`, `n_sheep`, `n_shepherds`, and `seed`, then take 5 evenly spaced positions including both endpoints. This reproducible rule does not select on outcome.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | compact | 100 | 1 | 2026 | True | 205 | 163.226 | none |
| strombom_multi | compact | 100 | 2 | 2086 | True | 195 | 300.579 | none |
| strombom_multi | compact | 200 | 1 | 2026 | True | 191 | 147.115 | none |
| strombom_multi | compact | 200 | 2 | 2085 | True | 183 | 270.683 | none |
| strombom_multi | compact | 200 | 10 | 2055 | True | 182 | 1,341.797 | none |

## Phase 5 communication claim merge

Full source: [`phase5/comm_claim/merged_trials.csv`](../../phase5/comm_claim/merged_trials.csv). The large table is not reproduced. The summaries below are computed directly from the CSV.

| Property | Value |
|---|---|
| Rows | 1,920 |
| Columns | 78 |
| Design cells | 12 |
| Methods | strombom_multi |
| Layouts | compact |
| N values | 100, 200 |
| D values | 1, 2, 3, 4, 6, 10 |
| Seed range | 2026 to 2125 |

| Property | Value |
|---|---|
| Successes | 1,860 |
| Failures | 60 |
| Overall R | 0.969 |
| Median ticks, successes | 186 |
| P90 ticks, successes | 204 |
| Median path, successes | 277.558 |
| Failure modes | oscillation: 60 |

Representative-row rule: sort lexicographically by `method`, `initial_layout`, `n_sheep`, `n_shepherds`, and `seed`, then take 5 evenly spaced positions including both endpoints. This reproducible rule does not select on outcome.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | compact | 100 | 1 | 2026 | True | 205 | 163.226 | none |
| strombom_multi | compact | 100 | 2 | 2086 | True | 189 | 286.598 | none |
| strombom_multi | compact | 200 | 1 | 2026 | True | 191 | 147.115 | none |
| strombom_multi | compact | 200 | 2 | 2085 | True | 183 | 270.683 | none |
| strombom_multi | compact | 200 | 10 | 2055 | False | 10000 | 10,643.92 | oscillation |

## Direct sources

* [`phase4/kubo_size/claim/packages/a/frontier.csv`](../../phase4/kubo_size/claim/packages/a/frontier.csv)
* [`phase4/fat_size/claim/packages/a/frontier.csv`](../../phase4/fat_size/claim/packages/a/frontier.csv)
* [`phase4/kubo_size/claim/packages/a/dmin_bootstrap.csv`](../../phase4/kubo_size/claim/packages/a/dmin_bootstrap.csv)
* [`phase4/fat_size/claim/packages/a/dmin_bootstrap.csv`](../../phase4/fat_size/claim/packages/a/dmin_bootstrap.csv)
* [`phase4/package_d/structure/frontier_by_method_layout.csv`](../../phase4/package_d/structure/frontier_by_method_layout.csv)
* [`phase4/package_d/size/transfer_summary.csv`](../../phase4/package_d/size/transfer_summary.csv)
* [`phase4/package_d/size/transfer_table.csv`](../../phase4/package_d/size/transfer_table.csv)
* [`phase4/kubo_structure/claim/outlier_rich_n200_window.json`](../../phase4/kubo_structure/claim/outlier_rich_n200_window.json)
* [`phase4/kubo_structure/claim/merged_dmin_bootstrap.csv`](../../phase4/kubo_structure/claim/merged_dmin_bootstrap.csv)
* [`phase4/kubo_size/claim/merged_trials.csv`](../../phase4/kubo_size/claim/merged_trials.csv)
* [`phase4/fat_size/claim/merged_trials.csv`](../../phase4/fat_size/claim/merged_trials.csv)
* [`phase4/kubo_structure/claim/merged_trials.csv`](../../phase4/kubo_structure/claim/merged_trials.csv)
* [`phase4/fat_structure/claim/merged_trials.csv`](../../phase4/fat_structure/claim/merged_trials.csv)
