# Parameter reference

Values in this page are frozen by [`scaling/configs/canonical_grid.yaml`](../../configs/canonical_grid.yaml) or recorded controller defaults from the linked configuration modules. A protocol YAML may select a subset but must not silently redefine the canonical protocol.

## Core protocol

| Parameter | Frozen value | Meaning and reason |
|---|---|---|
| `protocol_id` | `scaling_v2` | Stable provenance identifier for the locked rules |
| `frozen_on` | `2026-09-22` | Freeze date recorded by the canonical YAML |
| `task` | `drive_to_goal` | Every sheep must enter the goal disk before the deadline |
| `world_width`, `world_height` | 500, 500 | Square field large enough for wide and outlier-rich starts |
| flock centre | `(250, 250)` | Field centre |
| `goal_center` | `(370, 250)` | Midline point 120 units right of the flock |
| `drive_length` | 120 | Fixed centre-to-centre task distance |
| `goal_radius_at_n50` | 15 | Application-scale target at N = 50 |
| goal radius | `15 * sqrt(N/50)` | Keeps target area per sheep constant |
| `initial_spread` | 30 | Base scale used by all layout generators |
| `measurement_radius` | 5 | Connectivity radius for fragmentation |
| `reliability_theta` | 0.90 | Primary reliable-band threshold |
| `reliability_sensitivity` | 0.50, 0.70 | Additional reported thresholds, not the D_min bar |
| `baseline_method` | `strombom_multi` | Baseline collect-and-drive controller |
| `transfer_methods` | baseline, `kubo`, `fat`, `communication_free` | Full planned transfer list |
| `required_transfer_methods` | baseline, `kubo`, `fat` | Minimum transfer claim set |
| `flock_sizes` | 5, 10, 25, 50, 75, 100, 150, 200, 300, 400 | Frozen N grid |
| `shepherd_counts` | 1, 2, 3, 4, 6, 10, 15, 20, 25, 35 | Frozen D grid |
| `structure_flock_sizes` | 50, 100, 200 | Phase 2 and transfer-structure N values |
| `rq5_flock_sizes` | 100, 200 | Information-ladder claim sizes |
| `x0_families` | compact, wide, split, outlier_rich | Initial-layout factor |
| `time_limit_t0` | 10,000 | Main deadline, about 80 straight 120-unit crossings at speed 1 |
| `time_limit_t1` | 20,000 | Long deadline only for overcrowding cells |
| `scout_seeds` | 30 | Broad-map depth |
| `claim_grade_seeds` | 100 | Claim-window depth |
| `master_seed` | 2026 | Base for a shared deterministic seed list |
| `bootstrap_resamples` | 1,000 | Seed resamples for frontier uncertainty |
| `predictor_window_ticks` | 100 | Initial-state feature window, shorter than a straight drive |
| `wasteful_effort_tolerance` | 0.20 | Default excess-path bar |
| `wasteful_effort_sensitivity` | 0.10, 0.30 | Reported sensitivity bars |

At R = 0.90, 30 seeds have standard error about 0.055 and 100 seeds about 0.03. The approximate R interval at 100 seeds is plus or minus 0.06. This is uncertainty on R, not directly on D_min.

## Layout parameters

| Parameter | Value | Meaning |
|---|---:|---|
| compact sigma | 9 | `0.3 * initial_spread` |
| wide sigma | 60 | `2.0 * initial_spread` |
| split cluster count | 2 below N = 12, else 3 | Avoids tiny three-way groups |
| minimum split gap | 10 | `2 * measurement_radius` |
| outlier core | about 80 percent | Main flock |
| outliers | about 20 percent | Drawn beyond `r_a * N^(2/3)` |

Invalid points outside the field or inside the goal are redrawn.

## `strombom_multi`

| Parameter | Value | Meaning |
|---|---:|---|
| `r_a` | 2 | Sheep interaction length used in packing and collect threshold calculations |
| `r_s` | 65 | Distance within which sheep react to a shepherd; base sensing range |
| `sheep_speed` | 1.0 | Sheep displacement per tick |
| `shepherd_speed` | 1.5 | Shepherd displacement per tick |
| `noise_strength` | 0.3 | Angular process-noise strength in sheep motion |
| `inertia` | 0.5 | Previous-heading weight in sheep motion |
| collect threshold | `r_a * N^(2/3)` | Radius used to switch between collect and drive |

The coverage radius is `sensing_range` when an information factor sets it, otherwise the method's `r_s`. It is not the sheep-sheep repulsion distance.

## `kubo`

| Parameter | Value | Meaning |
|---|---:|---|
| `radius` | 60 | Local sensing radius |
| `K_s1` | 10 | Sheep-sheep repulsion gain |
| `K_s2` | 0.5 | Sheep velocity-alignment gain |
| `K_s3` | 2 | Sheep cohesion gain |
| `K_s4` | 5000 | Sheep repulsion from dogs |
| `K_f1` | 10 | Dog attraction to the target sheep |
| `K_f2` | 200 | Dog repulsion from the target sheep |
| `K_f3` | 8 | Dog repulsion from the goal |
| `K_f4` | 3000 | Dog-dog repulsion |
| `dt` | 0.05 | Force-integration time step |
| `sheep_speed_max` | 5 | Sheep speed clamp |
| `dog_speed_max` | 10 | Dog speed clamp |

## `fat`

FAT uses the Strombom sheep parameters above. Its dog rule selects the observed sheep farthest from that dog and takes a stand-off position `r_a` behind it in the direction away from the goal. Observation is `global` in Phases 1, 2, and 4.

## Information ladders

| Factor | Values | Meaning |
|---|---|---|
| `obs_mode` | `bearing_only`, `local_positions`, `global` | Increasing observation content |
| `sensing_range` | 32.5, 65, 97.5, 130 | 0.5, 1, 1.5, and 2 times Strombom `r_s` |
| `communication` | `none`, `neighbour_broadcast`, `global_shared` | Own observation, neighbor union, or globally shared sensed union |

For `strombom_multi`, `global_shared` uses the union of sensed sheep, not privileged simulator truth. Phase 5 scout protocols use D in `{1, 2, 3, 4, 6, 10}` because this low-D band is where a one-step saving can appear.

## Protocol recipe fields

| Field | Meaning |
|---|---|
| `protocol_id` | Identifier resolved under `scaling/configs/protocols/` and stamped into outputs |
| `phase` | Research phase number |
| `grade` | SMOKE, SCOUT, or CLAIM evidence grade |
| `canonical` | Path to the frozen defaults |
| `extends` | Parent protocol YAML whose values are inherited |
| `output` | Destination under `scaling/results/` |
| `methods` or `method` | Controller list or factor-run controller |
| `layouts` | Initial-layout subset |
| `flock_sizes` | N subset |
| `shepherd_counts` | D subset |
| `seeds` | Number of trial seeds per selected cell |
| `seed_mode` | Stage semantics such as scout or claim |
| `runner` | Grid or factor execution path |
| `upstream_protocol` | Scout or claim protocol used to plan later cells |
| `store_timeseries` | Whether to write per-trial Parquet histories |
| `packages` | Analysis packages to export after the run |
| `obs_modes`, `sensing_ranges`, `communications` | Values for one information ladder |

`canonical` imports defaults; `extends` inherits a complete parent recipe. In either case, a resolved `protocol.yaml` is copied into the result directory so inherited values remain inspectable.

## Outcomes and state metrics

| Quantity | Definition |
|---|---|
| success | Binary indicator that all sheep enter the goal by the deadline |
| `t_s` or finish time | First tick at which success is met |
| `shepherd_path` | Sum of Euclidean step lengths of all dogs, in arena units |
| path per dog | `shepherd_path / D` |
| cohesion | Mean sheep distance to the flock centre of mass |
| fragmentation | Largest connected-component size divided by N, using radius 5 |
| outlier count | Sheep beyond `r_a * N^(2/3)` |
| spread | Variance of sheep distances to the centroid |
| extent | Root-mean-square distance to the centroid |
| perimeter | Convex-hull perimeter |
| hull area | Convex-hull area |
| flock density | N divided by hull area; zero for degenerate area |
| aspect ratio | PCA major-axis to minor-axis ratio; one is round |
| `I_dir` | `1 - ||sum unit_velocity|| / M_active` for dogs faster than `1e-6` |
| coverage C | Fraction of peripheral sheep, those above median GCM distance, within the influence radius |

If no dog moves, `I_dir = 0`. It uses realized velocities, so constraints such as wall reflections are included. Missing coverage radius produces NaN.

## Reliability, frontiers, and regimes

`R(m, tau, N, D, T, X0, I)` is the probability of success estimated over locked seeds for method m, protocol tau, flock size N, shepherd count D, deadline T, layout X0, and information condition I.

| Quantity | Definition |
|---|---|
| D_min | Smallest tested D with R at least theta |
| D_overcrowd | First D after D_min for which that D and the next grid D are both below theta |
| D_max | Largest reliable D below D_overcrowd; without overcrowding, the largest tested reliable D, which may be a grid ceiling |
| B* | Reliable `(D, T)` with minimum median path; ties use smaller D, then faster median finish |
| hard failure | No tested D reaches theta; frontier values remain empty |
| under-resourced failure | R below theta before D_overcrowd |
| efficient operation | R at least theta and path below the wasteful bar |
| wasteful overspend | Reliable, but median path at least 20 percent above B*; also report 10 and 30 percent |
| overcrowding collapse | R below theta at or above D_overcrowd |

Frontier effects are measured in local D-grid steps. A D_max of 35 with empty D_overcrowd means no collapse was observed through the tested ceiling. It does not mean collapse begins at 35.

Bootstrap resamples seeds within each D 1,000 times. A resample with no D_min remains right-censored above the largest tested D. The 2.5 and 97.5 percentiles are grid values or `above grid`.

## Prediction and early warning

RQ7 uses horizon `k = 500`, feature window `w = 200`, and evaluation ticks 1,000 through 8,000 in steps of 200. Features use only `(t - 200, t]`; the label is failure in the next 500 ticks, only when the horizon remains within T0. Evaluation begins after the initial layout transient and ends early enough to retain the horizon.

State and N,D models hold out entire N values. Scaling-fit candidates are constant, linear, power `A * N^alpha`, and two-piece linear. Selection uses leave-one-N-out RMSE.
