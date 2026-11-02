# Settings

> AUTO-GENERATED: do not modify. Re-run the producing command to refresh this file. Command: `uv run python docs/generate_docs/make_docs.py`. Source: `protocols/configs/canonical.yaml` and its comments.

Every canonical setting, with its default and the note written beside it in `protocols/configs/canonical.yaml`. A protocol changes a setting by naming it ([configuration](configuration.md#protocol-overrides)). The model parameters ($r_a$, $c$ and the rest) are not canonical settings: they live with the method and are listed in the method docs: [Strombom sheep](../methods/strombom_sheep.md) and [team rule](../methods/strombom_multi.md).

The kind of a setting says where it may change. A per-trial setting changes what a trial does. A whole-protocol setting is fixed for the protocol, because calibration or the seeds depend on it. A sampling setting only steers the adaptive run, so it stays out of the physics hash and a folder can resume after it changes.

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
| `dog_start`, `dog_start_gap`, `dog_start_spacing` | arcs; 30; 5 | per trial | Where the dogs stand at tick 0, a convention with no real-world rule behind it. arcs: half circles behind the flock, spread evenly (the base). ring: circles round the flock, leaving out the cone that holds the goal. handler: every dog at one point straight behind the flock. The first circle is dog_start_gap beyond the farthest sheep that can start. A circle holds as many dogs as fit dog_start_spacing apart; more dogs go on the next one, dog_start_spacing farther out. |
| `dog_overlap_distance` | 2 | per trial | A dog with another dog closer than this has a twin (dog_overlap metric). The adaptive run uses it to stop spending seeds on copies of a dog. 2 is the Strombom distance r_a. |

## Metrics

| Setting | Default | Kind | Note |
| :--- | :--- | :--- | :--- |
| `measurement_radius`, `lost_radius_multiple` | 5; 2.5 | per trial | Sheep closer than measurement_radius are in the same group (fragmentation). Sheep farther than lost_radius_multiple x R_f from the centroid count as lost. |

## Calibration of R_f

| Setting | Default | Kind | Note |
| :--- | :--- | :--- | :--- |
| `calibration_seeds`, `calibration_seconds`, `calibration_window_seconds`, `calibration_starts` | 3; 300; 90; 1, 3 | whole protocol | One dog drives a compact flock toward a goal it cannot reach for calibration_seconds. R_f is sqrt(2) x the RMS radius over the last calibration_window_seconds, median over seeds and over the start sizes in calibration_starts (a start of s has radius s x sqrt(N / pi) m). |
| `settled_tolerance`, `start_agreement` | 0.15; 0.25 | whole protocol | Calibration raises when R_f changed by more than settled_tolerance between the last two windows, or differs by more than start_agreement between the start sizes. Strombom sheep settle up to N = 600. |

## Seeds and decisions

| Setting | Default | Kind | Note |
| :--- | :--- | :--- | :--- |
| `master_seed` | 2026 | whole protocol | Seed i of every cell is master_seed + i, so cells share start flocks. |
| `reliability_theta`, `confidence` | 0.9; 0.99 | sampling | A cell is reliable when the confidence interval of its success rate lies at or above theta, unreliable when it lies below, undecided otherwise. At theta 0.90 and 99% confidence a cell needs 51 successes in a row to be reliable. |
| `batch_seeds`, `max_seeds` | 10; 200 | sampling | Seeds are added in batches until every open cell is decided or has max_seeds. |
| `time_margin`, `min_pairs`, `bootstrap_resamples` | 0.05; 5; 4000 | sampling | Two finish times are the same when their paired median difference is within time_margin of the slower median (paired bootstrap, bootstrap_resamples draws). min_pairs is the fewest shared finished seeds a comparison accepts. |
| `refine_min_gap` | 1 | sampling | A dog count is added halfway between two neighbours more than refine_min_gap apart whose zones differ (whose reliability differs, when decide_finish_times is false). |
| `decide_finish_times` | false | sampling | Off: seeds only decide reliability (D_min). On: seeds also decide the finish-time values D_best, D_sat and D_crowd, which costs more trials. |
| `prune_overlap` | 0.9 | sampling | Above a confirmed saturation, a cell whose dogs were copies (mean dog_overlap at least this) and that is neither slower nor unreliable gets no more seeds. Above 1 turns it off. |
| `timeseries_seeds` | 3 | sampling | The first timeseries_seeds seeds of every cell keep their per-tick history as Parquet. |
| `budget_hours` | 72 | sampling | A run starts no new batch after this many hours (calibration not counted). Trials are saved as they finish and a rerun continues where it stopped. |
