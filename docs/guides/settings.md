# Settings

> AUTO-GENERATED: do not modify. Re-run the producing command to refresh this file. Command: `uv run python docs/generate_docs/make_docs.py`. Source: `protocols/configs/canonical.yaml` and its comments.

Every canonical setting, with its default and the note written beside it in `protocols/configs/canonical.yaml`. A protocol changes a setting by naming it ([configuration](configuration.md#protocol-overrides)). The model parameters ($r_a$, $c$ and the rest) are not canonical settings: they live with the method and are listed in the method docs: [Strombom sheep](../methods/strombom_sheep.md), [team rule](../methods/strombom_multi.md), [FAT baseline](../methods/fat.md) and [independent baseline](../methods/independent.md).

The kind of a setting says where it may change. A per-trial setting changes what a trial does. A whole-protocol setting is fixed for the protocol, because calibration or the seeds depend on it. A sampling setting only steers the adaptive run, so it stays out of the physics hash and a folder can resume after it changes. A calibration check only decides whether calibration stops, never the flock radius $R_f$ it measures, so it stays out of the physics hash as a sampling setting does.

Settings that share a note are one row, with their defaults in the same order, separated by semicolons. The physics hash that decides whether a folder can resume is in the [configuration guide](configuration.md#physics-hash).

## Task

| Setting | Default | Kind | Note |
| :--- | :--- | :--- | :--- |
| `task` | drive_to_goal | whole protocol | The task every trial runs. |

## Task: drive the flock into a goal

| Setting | Default | Kind | Note |
| :--- | :--- | :--- | :--- |
| `drive_distance_multiple`, `drive_distance_min` | 13; 80 | per trial | The goal lies this many flock radii from the flock start. It is never closer than the minimum (in m) or closer than the widest start layout plus the goal plus one flock radius. The sign gives the direction; a negative value mirrors the drive. |
| `goal_radius_multiple` | 1.9 | per trial | Goal radius in flock radii. |
| `success_fraction` | 1 | per trial | Share of the sheep that must be inside the goal at one tick for a trial to succeed. 1 is every sheep. At 0.99 one or two late sheep no longer decide a trial. |
| `field_clearance` | 80 | per trial | Free margin around the start, in m (a little more than the sheep reaction distance 65). The field only places the start; there is no boundary, as in the paper. |

## Start layouts

| Setting | Default | Kind | Note |
| :--- | :--- | :--- | :--- |
| `compact_spread` | 0.5 | per trial | compact: a Gaussian with sigma = compact_spread x R_f, cut at 3 sigma. |
| `separation_scale` | 2 | per trial | The scattered layouts are sized by L = separation_scale x N^(2/3), the distance from the flock centre beyond which Strombom 2014 collects (r_a N^(2/3), r_a = 2). |
| `wide_sigma` | 0.5 | per trial | wide: a Gaussian with sigma = wide_sigma x L, cut at 3 sigma. |
| `split_ring` | 1 | per trial | split: 3 compact clusters (2 when N < 12) on a ring of split_ring x L around the centre. |
| `outlier_fraction`, `outlier_near`, `outlier_far` | 0.2; 1.1; 1.6 | per trial | outlier_rich: outlier_fraction of the sheep at outlier_near to outlier_far x L from a compact core. |

## Dogs

| Setting | Default | Kind | Note |
| :--- | :--- | :--- | :--- |
| `dog_start`, `dog_start_gap`, `dog_start_spacing` | arcs; 30; 5 | per trial | Tick-0 dog placement (arcs: even half-circles behind the flock; ring: full circles minus the goal cone; handler: all dogs at one point behind the flock). The inner arc lies dog_start_gap beyond the farthest starting sheep; dogs keep dog_start_spacing apart along an arc and between successive arcs. |
| `dog_overlap_distance` | 2 | per trial | Distance (m) within which two dogs count as overlapping (dog_overlap metric); 2.0 is r_a. |

## Metrics

| Setting | Default | Kind | Note |
| :--- | :--- | :--- | :--- |
| `measurement_radius`, `lost_radius_multiple` | 5; 2.5 | per trial | Connected-component link distance (m) for fragmentation, and centroid distance (in R_f) beyond which a sheep counts as lost. |

## Calibration of R_f

| Setting | Default | Kind | Note |
| :--- | :--- | :--- | :--- |
| `calibration_seeds`, `calibration_seconds`, `calibration_window_seconds`, `calibration_starts` | 3; 300; 90; 1, 3 | whole protocol | One dog drives a compact flock toward an unreachable goal for calibration_seconds. R_f is sqrt(2) x the RMS radius over the last calibration_window_seconds, taking the median across seeds and across start densities in calibration_starts (radius s x sqrt(N / pi) m). |
| `settled_tolerance`, `start_agreement` | 0.05; 0.05 | calibration check | Max relative drift between the last two windows and max relative spread across start sizes. At 0.05 every study size (N <= 566) passes at 3 and 20 seeds per start, while larger flocks fail from N = 630 (3 seeds) or N = 660 (20 seeds) once the flock outgrows the settle window. Excluded from the physics hash because tolerances only gate whether calibration stops. |

## Seeds and decisions

| Setting | Default | Kind | Note |
| :--- | :--- | :--- | :--- |
| `master_seed` | 2026 | whole protocol | Seed i of every cell is master_seed + i, so cells share starting flocks. |
| `reliability_theta`, `confidence` | 0.9; 0.99 | sampling | A cell is reliable when its success-rate confidence interval lies at or above reliability_theta (51/51 successes at theta = 0.90, confidence = 0.99), unreliable when below, undecided otherwise. |
| `batch_seeds`, `max_seeds` | 10; 200 | sampling | Seeds are added in batches of batch_seeds up to max_seeds per undecided cell. |
| `time_margin`, `min_pairs`, `bootstrap_resamples` | 0.05; 5; 4000 | sampling | Paired-bootstrap finish-time equivalence margin (fraction of the slower median), minimum shared finished seeds required to compare two cells, and bootstrap resample count. |
| `refine_min_gap` | 1 | sampling | Insert a midpoint D between neighbouring dog counts more than refine_min_gap apart when their zones differ (or when their reliability differs if decide_finish_times is false). |
| `decide_finish_times` | false | sampling | False: allocate seeds only for reliability (D_min). True: also resolve finish-time regimes (D_best, D_sat, D_crowd). |
| `prune_overlap` | 0.9 | sampling | Stop adding seeds to a reliable, non-slowed cell above the saturation team once its mean dog_overlap reaches this threshold (> 1 disables pruning). |
| `timeseries_seeds` | 3 | sampling | Number of initial seeds per cell whose per-tick history is saved as Parquet. |
| `budget_hours` | 72 | sampling | Wall-clock limit (hours, excluding calibration) after which no new batch is started. |
