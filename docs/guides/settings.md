# Settings

> AUTO-GENERATED: do not modify. Re-run the producing command to refresh this file. Command: `uv run python docs/generate_docs/make_docs.py`. Source: `protocols/configs/canonical.yaml` and its comments.

Every canonical setting, with its default and the note written beside it in `protocols/configs/canonical.yaml`. A protocol changes a setting by naming it ([configuration](configuration.md#protocol-overrides)). The model parameters ($r_a$, $c$, the Kubo and Lama constants) are not canonical settings: they live with each method and are listed in the method docs: [Strömbom sheep](../methods/strombom_sheep.md), [team rule](../methods/strombom_multi.md), [FAT](../methods/fat.md), [independent](../methods/independent.md), [Kubo](../methods/kubo.md) and [Lama](../methods/lama.md).

The kind of a setting says where it may change:

- per trial: it can differ between curves of one protocol, as a factor;
- whole protocol: it is fixed for every curve of a protocol, because calibration or the seeds depend on it;
- sampling: it only steers the adaptive run, so it stays out of the physics hash and a folder can resume after it changes.

Settings that share a note are one entry, with their defaults in the same order, separated by semicolons. The physics hash that decides whether a folder can resume is in the [configuration guide](configuration.md#physics-hash).

## Task

- `task` (default drive_to_goal; whole protocol): The task every trial of a protocol runs: drive_to_goal, or gather for the model of Lama and di Bernardo 2024. Each task reads only its own section below.

## Task: drive the flock into a goal

- `drive_distance_multiple`, `drive_distance_min` (default 13; 80; per trial): The goal lies this many flock radii from the flock start. It is never closer than the minimum (in m) or closer than the widest start layout plus the goal plus one flock radius. The sign gives the direction; a negative value mirrors the drive.
- `goal_radius_multiple` (default 1.9; per trial): Goal radius in flock radii.
- `success_fraction` (default 1; per trial): Share of the sheep that must be inside the goal at one tick for a trial to succeed. 1 is every sheep, the aim of Kubo et al. 2022. Below 1 (0.99), one or two late sheep no longer decide a trial: with the strict rule a flock can reach the goal with 99% inside and then be driven past it.
- `hold_drive_multiple`, `hold_withdraw` (default 0; false; per trial): Holding task. The goal counts as reached only after the share above has stayed inside without a break for hold_drive_multiple drive times (0: at the first such tick, the D_min rule). With hold_withdraw true, the dogs of collect_drive_multi withdraw while the share is inside, to r_s + r_a beyond the farthest sheep. A Strombom sheep flees while any dog is closer than r_s, so dogs that only stopped would keep pushing the flock through the goal.
- `dog_spacing` (default 0; per trial): Dogs that take up room: no dog steps to within dog_spacing of another. Dogs move one after another; a dog already that close walks straight away at its speed, and a dog whose step would end that close does not step this tick. 0: dogs are points, as in the papers. Not for the Kubo and Lama dogs, which keep apart on their own.
- `sensing_range`, `communication` (default 0; none; per trial): What a dog of collect_drive_multi knows. With sensing_range 0 it knows every sheep, as the paper's shepherd does. Above 0 it knows the sheep closer than that range, and communication sets what it learns from other dogs: none (its own view only), neighbour (also the views of the dogs within sensing_range of it), shared (every dog's view, planned once for the team). Every dog knows the dog positions. A dog that knows no sheep walks to the flock centre it last knew (at first the flock's start).
- `drive_offset_cap` (default 0; per trial): Cap on the Strombom drive offset r_a sqrt(N). The paper's offset passes the sheep reaction distance r_s at N = (r_s / r_a)^2 = 1056, so above that the dog stands where few sheep feel it and no team size can drive the flock. A cap of r_s - r_a keeps the drive point within reach. It changes the paper rule, so it is a labelled variant. 0 is off.
- `field_clearance` (default 80; per trial): Free margin around the start, in m (a little more than the sheep reaction distance 65). The field only places the start; there is no boundary, as in the papers.

## Task: gather

- `gather_start_radius`, `gather_goal_fraction` (default 50; 0.2; per trial): The task of Lama and di Bernardo 2024 (task: gather). Sheep and dogs start uniform over a disc of radius gather_start_radius (the paper's R, 50 in its main figure) centred on the goal, a disc of gather_goal_fraction x R (the paper's r* = R / 5). Success is the share success_fraction inside (the paper's chi*, 0.99). The task sizes itself from R and does not calibrate. Read only by the gather task, and in the physics hash only when it runs.

## Start layouts

- `compact_spread` (default 0.5; per trial): compact: a Gaussian with sigma = compact_spread x R_f, cut at 3 sigma.
- `separation_scale` (default 2; per trial): The scattered layouts are sized by L = separation_scale x N^(2/3), the distance from the flock centre beyond which Strombom 2014 collects (r_a N^(2/3), r_a = 2).
- `wide_sigma` (default 0.5; per trial): wide: a Gaussian with sigma = wide_sigma x L, cut at 3 sigma.
- `split_ring` (default 1; per trial): split: 3 compact clusters (2 when N < 12) on a ring of split_ring x L around the centre.
- `outlier_fraction`, `outlier_near`, `outlier_far` (default 0.2; 1.1; 1.6; per trial): outlier_rich: outlier_fraction of the sheep at outlier_near to outlier_far x L from a compact core.

## Dogs

- `dog_start`, `dog_start_gap`, `dog_start_spacing` (default arcs; 30; 5; per trial): Where the dogs stand at tick 0, a convention with no real-world rule behind it (a real dog starts at the handler, far from the sheep, and runs out round the flock). arcs: half circles behind the flock, spread evenly (the base). ring: circles round the flock, goal side included, leaving out the cone that holds the goal. handler: every dog at one point straight behind the flock, as if released from a post. The first circle is dog_start_gap beyond the farthest sheep that can start. A circle holds as many dogs as fit dog_start_spacing apart; more dogs go on the next one, dog_start_spacing farther out. The gap and the spacing are conventions; the sensitivity protocols sweep them.
- `dog_overlap_distance` (default 2; per trial): A dog with another dog closer than this has a twin (dog_overlap metric). The adaptive run uses it to stop spending seeds on copies of a dog. 2 is the Strombom interaction distance r_a.

## Metrics

- `measurement_radius`, `lost_radius_multiple` (default 5; 2.5; per trial): Sheep closer than measurement_radius are in the same group (fragmentation). Sheep farther than lost_radius_multiple x R_f from the centroid count as lost.
- `metrics_stride` (default 1; per trial): Metrics are recorded at tick 0, every metrics_stride ticks and at the last tick; success and the end of a trial are checked every tick whatever the stride. 1 records every tick. A method with a small time step (Lama, dt 0.03) records every 10th tick, because a failing trial runs 166,667 ticks and the metrics cost more per tick than the model. A first arrival is then read from the recorded ticks, so the arrival times of a strided run are never earlier than the exact ones. Calibration always records every tick.

## Calibration of R_f

- `calibration_seeds`, `calibration_seconds`, `calibration_window_seconds`, `calibration_starts` (default 3; 300; 90; 1, 3; whole protocol): One dog drives a compact flock toward a goal it cannot reach for calibration_seconds. R_f is sqrt(2) x the RMS radius over the last calibration_window_seconds, median over seeds and over the start sizes in calibration_starts (a start of s has radius s x sqrt(N / pi) m).
- `settled_tolerance`, `start_agreement` (default 0.15; 0.25; whole protocol): Calibration raises when R_f changed by more than settled_tolerance between the last two windows, or differs by more than start_agreement between the start sizes. Strombom sheep settle up to N = 600; from about 630 a loose start keeps part of its size.
- `impose_radius_above`, `imposed_radius_scale` (default 0; 1; whole protocol): Above the edge a protocol may impose R_f instead: with impose_radius_above = N_cal, every N above it gets imposed_radius_scale x R_f(N_cal) x sqrt(N / N_cal), the density of the N_cal flock held constant. 0 is off.

## Seeds and decisions

- `master_seed` (default 2026; whole protocol): Seed i of every cell is master_seed + i, so cells share start flocks.
- `reliability_theta`, `confidence` (default 0.9; 0.99; sampling): A cell is reliable when the confidence interval of its success rate lies at or above theta, unreliable when it lies below, undecided otherwise. At theta 0.90 and 99% confidence a cell needs 51 successes in a row to be reliable.
- `batch_seeds`, `max_seeds` (default 10; 200; sampling): Seeds are added in batches until every open cell is decided or has max_seeds.
- `time_margin`, `min_pairs`, `bootstrap_resamples` (default 0.05; 5; 4000; sampling): Two finish times are the same when their paired median difference is within time_margin of the slower median (paired bootstrap, bootstrap_resamples draws). min_pairs is the fewest shared finished seeds a comparison accepts.
- `refine_min_gap` (default 1; sampling): A dog count is added halfway between two neighbours more than refine_min_gap apart whose zones differ (whose reliability differs, when decide_finish_times is false).
- `decide_finish_times` (default false; sampling): Off, seeds are spent only to decide reliability (D_min), and the finish-time values D_best, D_sat and D_crowd stay in the tables flagged undecided. On, seeds also decide them, which costs more trials. Runs that ask for D_sat turn it on.
- `prune_overlap` (default 0.9; sampling): Above a confirmed saturation, a cell whose dogs were copies (mean dog_overlap at least this) and that is neither slower nor unreliable gets no more seeds. Above 1 turns it off.
- `timeseries_seeds` (default 3; sampling): The first timeseries_seeds seeds of every cell keep their per-tick history as Parquet.
- `budget_hours` (default 72; sampling): A run starts no new batch after this many hours (calibration not counted). Trials are saved as they finish and a rerun continues where it stopped.
