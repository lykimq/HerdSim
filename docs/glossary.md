# Glossary

Definitions for the terms and symbols used across HerdSim's documentation, with links to the sections that explain them in full.

## Trials and experiments

These terms describe how HerdSim organises experiments, trials and adaptive sampling:

- $N$ and $D$: the number of sheep (flock size) and dogs (team size). Code and protocol files call a dog a shepherd (`shepherd_counts`).
- Protocol: the YAML recipe for one experiment in `protocols/configs/protocols/`, fixing the method, layouts, flock sizes, team sizes, [success rule](#success-and-reliability) and [deadline](#the-drive-task) ([configuration guide](guides/configuration.md#protocol-overrides)).
- Protocol id: the protocol's name, built from `dmin` for the [$D_{\min}$](#team-sizes) study, `f99` for the [99% rule](#success-and-reliability) (omitted for the strict rule), and `m12`, `m6`, `m3` for the deadline in [drive times](#the-drive-task) or `fat` / `indep` for the baseline protocols at 6 drive times.
- Main runs: the six `strombom_multi` study protocols (`dmin_m12`, `dmin_m6`, `dmin_m3` under the strict rule and `dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3` under the 99% rule) tested on $N = 25$-400 and $D = 1$-24, plus $N = 71, 141, 283, 566$ in the 99% runs at 12 and 6 drive times ([flock size](experiments/task_design.md#flock-size)), together with the two uncoordinated `fat` baseline protocols (`dmin_fat`, `dmin_f99_fat`) and the `independent` paper shepherds protocol (`dmin_f99_indep`) at 6 drive times.
- Method: a sheep model paired with a dog controller; HerdSim uses `strombom_multi` (Strombom sheep with the team rule), the uncoordinated baseline `fat` and independent paper shepherds `independent` ([sheep model and dog rule](#sheep-model-and-dog-rule)).
- Grid: the full set of layouts, flock sizes and team sizes a protocol tests; the top of the grid is its largest team size ($D = 24$ in the study).
- Group and curve: one setup (a single layout and flock size $N$) is a group, and the sequence of cells across tested team sizes $D$ for that group is its curve.
- Cell: a single $(layout, N, D)$ point on a curve, answering "can $D$ dogs herd $N$ sheep in this layout?" A cell receives trials in batches of 10 seeds (`batch_seeds`) up to the seed cap of 200 (`max_seeds`), stopping early once decided or if a trial errors.
- Trial and tick: one simulation run of a cell with one random seed is a trial, stepped one tick (1 s) at a time until it succeeds, ends early or reaches the deadline.
- Seed: the integer that fixes a trial's random streams (`master_seed + i`, with `master_seed = 2026` by default), so trial $i$ starts from the same flock at every team size and across the nine study protocols ([paired random streams](experiments/task_design.md#paired-random-streams)).
- Replay: re-running a stored trial from its configuration and seed; any mismatch in outcome or tick count raises an error.
- Campaign, sitting and round: the campaign is the manager that runs a protocol into `results/<protocol_id>/` ([adaptive sampling](experiments/task_design.md#3-adaptive-sampling)); each invocation of the CLI is a sitting, and each pass within a sitting that allocates another seed batch to [open cells](#success-and-reliability) is a round ([architecture](codes/architecture.md#how-a-campaign-runs)).
- Calibration: the initial pass of a campaign that drives a compact flock with one dog for 300 s at each flock size to measure $R_f$ ([sizing](experiments/task_design.md#sizing-by-the-calibrated-flock-radius)).

## The drive task

These terms define the arena geometry and time limits:

- Drive task: the task in which dogs gather a flock if scattered and drive it into a circular goal.
- Calibrated flock radius $R_f$: the radius a compact flock of $N$ sheep settles to when driven by one dog ($\sqrt{2}$ times its root-mean-square distance to the flock centre), used to scale the arena, goal and drive distance ([sizing](experiments/task_design.md#sizing-by-the-calibrated-flock-radius)).
- Calibration edge: the smallest tested flock size where calibration exceeds its 5% drift or start-agreement limits ($N = 630$ at 3 seeds per start where 600 passes, and $N = 660$ at 20 seeds where 630 passes); the study stops at $N = 566$, the last $\sqrt{2}$ step below it ([flock size](experiments/task_design.md#flock-size)).
- Goal: a circle of radius $1.9 R_f$.
- Drive distance $l$: the distance from the flock's initial centre to the goal centre, set to $13 R_f$ (at least 80 m, and at least the farthest possible initial sheep distance across the protocol's layouts plus the goal radius plus $R_f$).
- Drive time $T_{\mathrm{drive}}$ and deadline: one drive time is the duration a sheep walking straight at 1 m/s takes to cover the drive distance $l$, and a trial's deadline is 12, 6 or 3 drive times ([deadlines](experiments/task_design.md#deadlines-in-drive-times)).
- Finish time: the number of ticks (seconds) a successful trial takes to reach the goal condition.

## Start layouts and dog starts

These terms describe the initial placement of sheep and dogs at tick 0:

- Layout: the initial spatial distribution of the sheep ([layouts](experiments/task_design.md#flock-start-layouts)), where Gaussian layouts are truncated at three standard deviations and scattered layouts are scaled by the [collect distance](#sheep-model-and-dog-rule).
- `compact`: a tight Gaussian cluster with standard deviation $0.5 R_f$ (truncated at $1.5 R_f$) that keeps all sheep within the collect distance so dogs begin driving immediately.
- `wide`: a loose Gaussian cluster with standard deviation equal to half the collect distance that places about 13% of the sheep beyond the collect distance at every $N$.
- `split`: three compact clusters (two when $N < 12$) placed on a circle of radius equal to the collect distance around the flock centre.
- `outlier_rich`: a compact core containing 80% of the sheep surrounded by the remaining 20% on a ring at 1.1-1.6 collect distances.
- Scattered layouts: the three layouts (`wide`, `split` and `outlier_rich`) in which sheep start beyond the collect distance and must be collected before driving.
- Dog start (`arcs`): the initial placement of dogs on semicircular arcs behind the flock, with the inner arc 30 m behind the farthest possible initial sheep (`dog_start_gap`), at least 5 m between dogs (`dog_start_spacing`), and any overflow placed on a second arc 5 m farther out ([dog starts](experiments/task_design.md#dog-starts)).

## Success and reliability

These terms define trial success and cell-level statistical decisions:

- Strict rule: a trial succeeds when all $N$ sheep are inside the goal at the same tick before the deadline.
- 99% rule: a trial succeeds when at least $\lceil 0.99 N \rceil$ sheep are inside the goal at the same tick before the deadline, which equals the strict rule for $N < 100$.
- Reliability threshold $\theta$: the target success rate $\theta = 0.90$.
- Reliable, unreliable and undecided cells: using the exact two-sided 99% Clopper-Pearson confidence interval $[L, U]$ for a cell's success rate, a cell is reliable when $L \ge \theta$ (requiring at least 51/51 successes) with no trial errors, unreliable when $U < \theta$, and undecided on reliability when $L < \theta \le U$ or when $L \ge \theta$ with a trial error ([stopping early](experiments/task_design.md#stopping-early-with-the-99-clopper-pearson-interval)).
- Open cell: a cell that still needs seeds under the protocol's stopping rule (either undecided on reliability, or undecided on finish-time comparison when `decide_finish_times` is enabled), excluding errored cells and cells [pruned above saturation](experiments/task_design.md#pruning-above-saturation); at `max_seeds` (200) an open cell remains listed in `status.json` (`cells_needing_seeds`) but receives no more seeds.
- Frontier rules and zones: the rules that evaluate a curve's cells to assign each cell a zone label (such as `too_few`, `improving`, `saturated` or `undecided`) and extract critical team sizes ([frontier rules](experiments/task_design.md#5-frontier-rules-and-zones)).

## Team sizes

These terms describe the critical team sizes reported for a curve:

- $D_{\min}$: the smallest reliable team size on a curve ([report, section 1](report/d_min_report.md#1-the-question)).
- Bracket (`3-8`) and $D_{\min,\mathrm{low}}$: notation indicating that 8 dogs are reliable while a smaller team (down to $D_{\min,\mathrm{low}} = 3$, the smallest team whose interval still reaches $\theta$) remains undecided at 200 seeds.
- Lower bound (`[5]`): notation indicating that no tested team on the curve is reliable yet, and the smallest team not yet ruled out is $D_{\min,\mathrm{low}} = 5$.
- `none` (`none on grid`): notation indicating that every tested team size up to the top of the grid is unreliable.
- $D_{\min,\mathrm{stable}}$: on a curve where a team size above $D_{\min,\mathrm{low}}$ is unreliable, the smallest reliable team size above the last unreliable team ([report, section 3](report/d_min_report.md#3-exceptions-and-pilot-checks)).
- Saturation team size $D_{\mathrm{sat}}$ and other frontier values: $D_{\mathrm{sat}}$ is the smallest reliable team that no larger reliable team beats on paired finish time (used by the campaign to [prune seeds above saturation](experiments/task_design.md#pruning-above-saturation)), stored alongside $D_{\max}$, $D_{\mathrm{overcrowd}}$, $D_{\mathrm{best}}$ and $D_{\mathrm{crowd}}$ in `frontier_groups.csv` ([frontier values](experiments/task_design.md#frontier-values)).

## Sheep model and dog rule

These terms define the agent physics in `sim/`:

- Strombom model: the sheep and single-dog interaction rules of Strombom et al. (2014) ([Strombom sheep](methods/strombom_sheep.md)).
- Interaction distances $r_a$ and $r_s$: sheep repel one another within $r_a = 2$ m and react to any dog within $r_s = 65$ m (grazing when no dog is within $r_s$).
- Grazing repulsion (`graze_repulsion`): sheep-to-sheep repulsion within $r_a$ applied even when no dog is within $r_s$; disabled in the nine main multi-dog study runs and enabled in the paper check and grazing pilots ([grazing](methods/strombom_sheep.md#grazing)).
- Neighbour count $n$: the number of nearest neighbours that attract each sheep ($n = N - 1$, the global case, in the multi-dog study; varied in the [paper check](methods/strombom_check.md#terms)).
- $\mathrm{GCM}$ and $\mathrm{LCM}_i$: the global centre of mass of all $N$ sheep and the local centre of mass of sheep $i$'s $n$ nearest neighbours.
- Collect distance $f(N) = r_a N^{2/3}$: the radius around the $\mathrm{GCM}$ beyond which a sheep is classified as an outlier, which triggers collection rather than driving.
- Collect point $P_c$ and drive point $P_d$: the target point $r_a$ behind an outlier for collection ($P_c$) and $r_a \sqrt{N}$ behind the $\mathrm{GCM}$ for driving ($P_d$) ([team rule](methods/strombom_multi.md)).
- Team rule (`strombom_multi`): HerdSim's multi-dog controller, which matches dogs to the $D$ farthest outliers via the Hungarian algorithm (minimum total distance) while spare dogs drive the core, and spreads all $D$ dogs on an arc through $P_d$ once all sheep are within $f(N)$ ([driving](methods/strombom_multi.md#driving-and-its-limit-for-large-flocks)).
- Farthest-agent targeting (`fat`): the uncoordinated multi-dog baseline in which every dog sees the whole flock and aims $r_a$ behind the single sheep farthest from the goal ($P_{\mathrm{FAT}}$), without a collect/drive mode switch or multi-dog assignment ([FAT baseline](methods/fat.md)).
- Independent paper shepherds (`independent`): the baseline in which each dog runs Strömbom's single-dog rule on the whole flock with a collect/drive switch but without multi-dog assignment or driving slots, so all dogs aim at the same target ([independent baseline](methods/independent.md)).
- Stop rule: a dog pauses for the current tick whenever any sheep is within $3 r_a = 6$ m.

## Records

These terms describe provenance and reproducibility checks on stored results:

- Physics hash: a digest of all protocol settings that affect trial trajectories; a results folder refuses a run if its stored physics hash differs from the protocol's ([configuration guide](guides/configuration.md#physics-hash)).
- Code identity: the trial-code hash, git commit, dirty-worktree flag and Python/package versions logged in `runs.jsonl` for each sitting, which warns if the trial-code hash changes between sittings.
