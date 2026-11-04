# Glossary

A definition for each term HerdSim's docs use, with a link to the section that explains it in full. Other docs, including [architecture](codes/architecture.md), link here at a term's first use. The [README](../README.md) gives an overview of the study.

## Trials and experiments

**$N$ and $D$**: the number of sheep (flock size) and of dogs (team size). The code and protocol files call a dog a shepherd (`shepherd_counts` lists the team sizes).

**Protocol**: the recipe of one experiment, a YAML file in `protocols/configs/protocols/` that fixes the method, layouts, flock sizes, team sizes, [success rule](#success-and-reliability) and [deadline](#the-drive-task). How a protocol inherits from a parent and from the canonical defaults is in the [configuration guide](guides/configuration.md#protocol-overrides).

**Protocol id**: the protocol's name, built from parts: `dmin` for the [$D_{\min}$](#team-sizes) study, `f99` for the [99% rule](#success-and-reliability) (absent for the strict rule), and `m12`, `m6` or `m3` for the deadline in [drive times](#the-drive-task).

**Method**: a sheep model paired with a dog controller. HerdSim has one, `strombom_multi`, Strombom sheep with the team rule ([sheep model and dog rule](#sheep-model-and-dog-rule)).

**Cell**: the question "can 3 dogs herd 200 sheep in this setup?" for one layout, $N$ and $D$ within one protocol. It gets trials in batches of 10, up to 200; a cell with an errored trial stops earlier.

**Group**: one setup, meaning one layout and flock size $N$, in which the team sizes are compared.

**Curve**: the cells of one group, one per tested team size.

**Grid**: the layouts, flock sizes and team sizes a protocol tests. The top of the grid is its largest team size.

**Trial**: one run of one cell with one seed, until it succeeds, ends early or reaches its time limit.

**Tick**: one time step, 1 s. The Strombom paper gives no time unit, and HerdSim reads it as 1 s.

**Seed**: the number that fixes a trial's random streams. Seed $i$ of a cell is `master_seed` (2026 by default) plus $i$, so it starts from the same flock at every team size and in every protocol ([paired random streams](experiments/task_design.md#paired-random-streams)).

**Replay**: running a stored trial again from its configuration and seed. A replay that does not give the stored success and tick count raises an error.

**Campaign**: the manager that runs a protocol into `results/<protocol id>/` and spends extra seeds on [undecided](#success-and-reliability) cells, in rounds ([adaptive sampling](experiments/task_design.md#3-adaptive-sampling)).

**Sitting**: one run of the campaign command on a results folder; a folder can grow over several.

**Round**: one pass of a sitting that plans and runs the seeds each undecided cell still needs ([campaign](codes/architecture.md#how-a-campaign-runs)).

**Batch**: the 10 seeds a cell gets at a time (`batch_seeds`).

**Seed cap**: the most seeds a cell can get, 200 (`max_seeds`).

**Calibration**: the short run at the start of a campaign that measures $R_f$ ([drive task](#the-drive-task)) for each flock size, with one dog driving for 300 s ([sizing](experiments/task_design.md#sizing-by-the-calibrated-flock-radius)).

**Main runs**: the six protocols of the study, three strict and three 99%, at 12, 6 and 3 [drive times](#the-drive-task), on $N = 25$-400 and $D = 1$-24. The 99% grids at 12 and 6 drive times add 71, 141, 283 and 566, for nine flock sizes ([flock size](experiments/task_design.md#flock-size)).

## The drive task

**Drive task**: the dogs gather the flock if needed and drive it into a circular goal.

**$R_f$**: the calibrated flock radius, the size a compact flock of $N$ sheep settles to while one dog drives it ($\sqrt{2}$ times its RMS distance to the centre). It sizes the field, the goal and the drive ([sizing](experiments/task_design.md#sizing-by-the-calibrated-flock-radius)).

**Calibration edge**: about $N = 600$, above which a driven flock no longer settles to one radius. The study stops at 566.

**Goal**: a circle of radius $1.9 R_f$.

**Drive distance $l$**: from the flock's start centre to the goal centre, $13 R_f$, but at least 80 m and at least the farthest any sheep can start (over the protocol's layouts) plus the goal radius plus $R_f$.

**Drive time $T_{\mathrm{drive}}$**: the time a sheep walking straight at 1 m/s needs to cover the drive distance ([deadlines](experiments/task_design.md#deadlines-in-drive-times)).

**Deadline**: a trial's time limit, 12, 6 or 3 drive times.

**Finish time**: the time a successful trial takes.

## Start layouts and dog starts

**Layout**: how the sheep are placed at the start ([layouts](experiments/task_design.md#flock-start-layouts)). A Gaussian layout's spread is a standard deviation, cut at three spreads. The scattered layouts are sized by the [collect distance](#sheep-model-and-dog-rule), beyond which a sheep is an outlier.

**`compact`**: a Gaussian with spread $0.5 R_f$, so every sheep starts within $1.5 R_f$ and within the collect distance, and the dogs start by driving.

**`wide`**: a Gaussian whose spread is half the collect distance, so about 13% of the sheep start beyond it at every $N$.

**`split`**: three compact clusters (two below $N = 12$) on a circle of radius the collect distance round the flock centre.

**`outlier_rich`**: 80% of the sheep in a compact core and 20% on a ring 1.1-1.6 collect distances from it.

**Scattered layouts**: `wide`, `split` and `outlier_rich`, where the dogs must collect before they drive.

**Dog start**: where the dogs stand at tick 0 ([dog starts](experiments/task_design.md#dog-starts)). The study uses `arcs`, half circles behind the flock, the first 30 m beyond the farthest possible start sheep (`dog_start_gap`), with dogs at least 5 m apart (`dog_start_spacing`) and the rest on a circle 5 m farther out.

## Success and reliability

**Strict rule**: a trial succeeds when every sheep is inside the goal at one tick.

**99% rule**: a trial succeeds when at least $\lceil 0.99 N \rceil$ sheep are inside at one tick. Below $N = 100$ that is $N$, so the two rules agree there.

**$\theta$**: the reliability threshold, 0.90.

**Reliable cell**: a cell whose 99% Clopper-Pearson interval of the success rate lies at or above $\theta$, which takes at least 51 successes without a failure (60 of 60 gives a lower bound of 0.915). An unreliable cell's interval lies below $\theta$ and an undecided cell's straddles it; the first two are decided ([stopping early](experiments/task_design.md#stopping-early-with-the-99-clopper-pearson-interval)).

**Open cell**: a cell that still asks for seeds, because its reliability is undecided or, with `decide_finish_times` true, a finish-time comparison is. Cells with an errored trial and cells [pruned above saturation](experiments/task_design.md#pruning-above-saturation) get no seeds and are not counted.

**Frontier rules**: the rules that turn a curve's stored trials into each cell's decision and the team sizes below ([frontier rules](experiments/task_design.md#5-frontier-rules-and-zones)).

## Team sizes

**$D_{\min}$**: the smallest reliable team on a curve ([report, section 2.3](report/d_min_report.md#23-when-a-team-is-reliable)).

**Bracket**, written `3-8`, and **$D_{\min,\mathrm{low}}$**: 8 dogs are reliable and 3 are undecided, so $D_{\min}$ lies between 3 and 8. $D_{\min,\mathrm{low}}$, the lower end, is the smallest team whose interval still reaches $\theta$.

**Lower bound**, written `[5]`: no team is reliable yet, and $D_{\min}$ is at least 5, its $D_{\min,\mathrm{low}}$.

**$D_{\min,\mathrm{stable}}$**: on a curve where a team above $D_{\min,\mathrm{low}}$ is unreliable, the smallest reliable team above the last such team ([report, section 2.3](report/d_min_report.md#23-when-a-team-is-reliable)).

**`none`**: every tested team up to the top of the grid is unreliable; the generated tables write `none on grid`.

**$D_{\mathrm{sat}}$**: the smallest reliable team that no larger reliable team beats on finish time ([frontier values](experiments/task_design.md#frontier-values)). One team beats another when, on the seeds both finished, the bootstrap 99% interval of the paired median difference lies more than 5% of the slower median below zero. The campaign uses it to stop seeding copies above it ([pruning](experiments/task_design.md#pruning-above-saturation)); the report does not use it.

**Other frontier values**: the frontier rules also store $D_{\max}$, $D_{\mathrm{overcrowd}}$, $D_{\mathrm{best}}$ and $D_{\mathrm{crowd}}$ in `frontier_groups.csv` ([frontier values](experiments/task_design.md#frontier-values)).

**Zone**: a cell's label along its curve, such as `too_few`, `improving` or `saturated` ([zones](experiments/task_design.md#zones)).

## Sheep model and dog rule

**Strombom model**: the sheep model of Strombom et al. (2014) ([Strombom sheep](methods/strombom_sheep.md)).

**$r_a$**: 2 m, the distance below which sheep push each other apart.

**$r_s$**: 65 m, the distance within which a sheep reacts to a dog; with no dog that close it grazes.

**Grazing repulsion** (`graze_repulsion`): grazing sheep also push apart when closer than $r_a$, as in the paper. Off in the six study runs, on in the check against the paper and the grazing pilots ([grazing](methods/strombom_sheep.md#grazing)).

**Neighbour count $n$**: how many nearest neighbours attract a sheep; all $N - 1$ in the study. The check against the paper varies it, and there a trial finishes when the flock centre is within 10 m of the goal ([terms](methods/strombom_check.md#terms)).

**GCM and $\mathrm{LCM}_i$**: the global centre of mass (mean position of the flock) and the local centre of mass of sheep $i$ (mean position of its nearest neighbours, all other sheep by default).

**Collect distance $f(N) = r_a N^{2/3}$**: a sheep farther than this from the GCM is an outlier. The dogs collect while any sheep is that far out, and drive otherwise.

**Collect point $P_c$ and drive point $P_d$**: where a dog aims to collect an outlier or to drive. $P_d$ lies $r_a \sqrt{N}$ behind the flock centre ([team rule](methods/strombom_multi.md)).

**Team rule**: HerdSim's multi-dog collect and drive rule, run with Strombom sheep as `strombom_multi`. While collecting, the $D$ farthest outliers each get one dog (Hungarian algorithm, least total walk) and spare dogs drive the core from behind; while driving, the dogs spread over an arc through $P_d$ ([driving](methods/strombom_multi.md#driving-and-its-limit-for-large-flocks)).

**Point dogs**: dogs with no size, so two can stand at one point.

**Stop rule**: a dog stands still while any sheep is within $3 r_a = 6$ m.

## Records

**Physics hash**: a digest of every setting that changes a trial; a folder whose hash differs from its protocol is refused (the [configuration guide](guides/configuration.md#physics-hash) says what it covers and leaves out).

**Code identity**: the trial-code hash, git commit, uncommitted-edit flag and Python and library versions, recorded for each sitting. A changed code hash between sittings gives a warning, and the run goes on.
