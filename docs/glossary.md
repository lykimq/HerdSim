# Glossary

A definition for each term HerdSim's docs use, with a link to the section that explains it in full. Other docs, including [architecture](codes/architecture.md), link here at a term's first use. See also [README](../README.md) for an overview of the study.

## Trials and experiments

- $N$ and $D$: the number of sheep (flock size) and of dogs (team size). The code and protocol files call a dog a shepherd (`shepherd_counts` lists the team sizes); the [gather task](#the-gather-task) calls it a herder.
- Protocol: the recipe of one experiment, a YAML file in `protocols/configs/protocols/` that fixes the methods, layouts, flock sizes, team sizes, [success rule](#success-and-reliability) and [deadline](#the-drive-task). A protocol with `extends:` changes only what it names in its parent. A setting the protocol does not name (a canonical setting) keeps its default from `protocols/configs/canonical.yaml`.
- Protocol id: the protocol's name, built from parts: `dmin` the [$D_{\min}$](#team-sizes) study on the [drive task](#the-drive-task), `f99` the [99% rule](#success-and-reliability) (absent for the strict rule), `m12`, `m6` or `m3` the deadline in [drive times](#the-drive-task), `s_` a sensitivity variant, and a last part naming the variant (such as `fat`, `hold` or `big`). `lama_r50` is the [gather task](#the-gather-task) on a start disc of radius 50, `lama_r50_inf` the same with infinite sensing.
- Method: a sheep model paired with a dog controller, such as `strombom_multi` (Strömbom sheep with the team rule); see [sheep models and dog rules](#sheep-models-and-dog-rules).
- Factor: a canonical setting a protocol sweeps over several values (levels), each giving its own curves, such as `dog_start_gap` in `dmin_s_gap`. A method parameter cannot be a factor, because [$R_f$](#the-drive-task) is calibrated once per method.
- Cell: the question "can 3 dogs herd 200 sheep in this setup?" for one method, layout, $N$, $D$ and set of factor levels within one protocol. It gets trials in batches of 10, up to 200; a cell with an errored trial stops earlier.
- Group: one setup, meaning one method, layout, set of factor levels and flock size $N$, in which the team sizes are compared.
- Curve: the cells of one group, one per tested team size.
- Grid: the layouts, flock sizes and team sizes a protocol tests. The top of the grid is its largest team size.
- Trial: one run of one cell with one seed, until it succeeds, ends early or reaches its time limit.
- Tick: one time step; 1 s for the Strömbom model, 0.05 s for Kubo and 0.03 s for Lama. The Strömbom and Lama papers give no time unit, and the Kubo and Lama papers no length unit; HerdSim reads them as 1 s and 1 m.
- Seed: the number that fixes a trial's random streams. Seed $i$ of a cell is `master_seed` (2026 by default) plus $i$, so it starts from the same flock at every team size ([paired random streams](experiments/task_design.md#paired-random-streams)). A few figures give the value, such as 2026 for seed 0.
- Seed 0: the first stored trial of a cell. Most animations show it, so the trial is not picked for its looks; captions name any other seed.
- Replay: running a stored trial again from its configuration and seed. An unchanged replay that does not give the stored success and tick count raises an error.
- Campaign: the manager that runs a protocol into `results/<protocol id>/` and spends extra seeds on [undecided](#success-and-reliability) cells, in rounds ([adaptive sampling](experiments/task_design.md#3-adaptive-sampling)).
- Sitting: one run of the campaign command on a results folder; a folder can grow over several.
- Round: one pass of a sitting that plans and runs the seeds each undecided cell still needs ([sampling loop](experiments/task_design.md#the-adaptive-sampling-loop)).
- Batch: the 10 seeds a cell gets at a time (`batch_seeds`).
- Seed cap: the most seeds a cell can get, 200 (`max_seeds`).
- Calibration: the short run at the start of a campaign that measures $R_f$ ([drive task](#the-drive-task)) for each method and flock size, with one dog driving for 300 s ([sizing](experiments/task_design.md#sizing-by-the-calibrated-flock-radius)). The gather task does not calibrate.
- Main runs: the three strict and three 99% protocols at 12, 6 and 3 [drive times](#the-drive-task), on $N = 25$-400 and $D = 1$-24. The 99% grids at 12 and 6 drive times add 71, 141, 283 and 566, for nine flock sizes ([flock size](experiments/task_design.md#flock-size)).
- Top-up: a later sitting that adds finish-time seeds to existing 99% grids, so that $D_{\mathrm{sat}}$ ([team sizes](#team-sizes)) can be decided.
- Sensitivity runs: 14 protocols at 6 drive times, a base run and six variants under each [success rule](#success-and-reliability). The base run (`dmin_s_base`, `dmin_f99_s_base`) is the main setup on `wide` and `outlier_rich`, $N = 100$-400, with up to 16 dogs; each variant changes one choice on the same seeds.

## The drive task

- Drive task: the dogs gather the flock if needed and drive it into a circular goal.
- $R_f$: the calibrated flock radius, the size a compact flock of $N$ sheep settles to while one dog drives it ($\sqrt{2}$ times its RMS distance to the centre). It sizes the field, the goal and the drive ([sizing](experiments/task_design.md#sizing-by-the-calibrated-flock-radius)).
- Calibration edge: about $N = 600$, above which a driven flock no longer settles to one radius. The large-flock protocols impose $R_f$ above 566, the largest calibrated size, from the density of the 566 flock or scaled from it ([protocols](guides/protocols.md)).
- Goal: a circle of radius $1.9 R_f$ by default.
- Drive distance $l$: from the flock's start centre to the goal centre, $13 R_f$ by default, but at least 80 m and at least the farthest any sheep can start (over the protocol's layouts) plus the goal radius plus $R_f$.
- Drive time $T_{\mathrm{drive}}$: the time a sheep walking straight at 1 m/s needs to cover the drive distance ([deadlines](experiments/task_design.md#deadlines-in-drive-times)).
- Deadline: a trial's time limit; 12, 6 or 3 drive times on the drive task, a fixed 500 s in the [Kubo](#sheep-models-and-dog-rules) runs and a time limit of 5000 s (166,667 ticks of 0.03 s, stored as 5000.01 s) on the gather task.
- Finish time: the time a successful trial takes.
- Dog time: $D$ times the finish time.

## Start layouts and dog starts

- Layout: how the sheep are placed at the start ([layouts](experiments/task_design.md#flock-start-layouts)). A Gaussian layout's spread is a standard deviation, cut at three spreads; scattered layouts are sized by the [collect distance](#sheep-models-and-dog-rules), beyond which a sheep is an [outlier](#sheep-models-and-dog-rules).
- `compact`: a Gaussian with spread $0.5 R_f$, so every sheep starts within $1.5 R_f$ and within the collect distance, and the dogs start by driving.
- `wide`: a Gaussian whose spread is half the collect distance, so about 13% of the sheep start beyond it at every $N$.
- `split`: three compact clusters (two below $N = 12$) on a circle of radius the collect distance round the flock centre.
- `outlier_rich`: 80% of the sheep in a compact core and 20% on a ring 1.1-1.6 collect distances from it.
- Scattered layouts: `wide`, `split` and `outlier_rich`, where the dogs must collect before they drive.
- `uniform`: the gather task's start, targets and herders spread uniformly over a disc.
- Dog starts ([dog starts](experiments/task_design.md#dog-starts)): `arcs` (the default) on half circles behind the flock, `ring` on full circles round it except toward the goal, `handler` with all dogs at one point behind it.
- Start gap: how far beyond the farthest possible start sheep the first dog circle lies, 30 m by default (`dog_start_gap`). Dogs on a circle stand at least 5 m apart (`dog_start_spacing`), and the rest go on a circle 5 m farther out.

## Success and reliability

- Strict rule: a trial succeeds when every sheep is inside the goal at one tick.
- 99% rule: a trial succeeds when at least $\lceil 0.99 N \rceil$ sheep are inside at one tick. Below $N = 100$ that is $N$, so the two rules agree there.
- Holding task: a trial succeeds once 99% of the flock has stayed in the goal for one drive time while the dogs withdraw to 67 m beyond the farthest sheep ([holding](experiments/task_design.md#the-holding-task)). `dmin_f99_hold_share` also tries 95% and 90%.
- $\theta$: the reliability threshold, 0.90.
- Reliable cell: a cell whose 99% Clopper-Pearson interval of the success rate lies at or above $\theta$, which takes at least 51 successes without a failure (60 of 60 gives a lower bound of 0.915). An unreliable cell's interval lies below $\theta$ and an undecided cell's straddles it; the first two are decided ([stopping early](experiments/task_design.md#stopping-early-with-the-99-clopper-pearson-interval)).
- Open cell: a cell that still asks for seeds, because its reliability is undecided or, with `decide_finish_times` true, a finish-time comparison is. Cells with an errored trial and cells [pruned above saturation](experiments/task_design.md#pruning-above-saturation) get no seeds and are not counted.
- Frontier rules: the rules that turn a curve's stored trials into each cell's decision and the team sizes below ([frontier rules](experiments/task_design.md#5-frontier-rules-and-zones)).

## Team sizes

- $D_{\min}$: the smallest reliable team on a curve ([report, section 2.1](report/d_min_report.md#21-when-a-team-is-reliable)).
- Bracket, written `3-8`, and $D_{\min,\mathrm{low}}$: 8 dogs are reliable and 3 are undecided, so $D_{\min}$ lies between 3 and 8. $D_{\min,\mathrm{low}}$, the lower end, is the smallest team whose interval still reaches $\theta$.
- Lower bound, written `[5]`: no team is reliable yet, and $D_{\min}$ is at least 5, its $D_{\min,\mathrm{low}}$.
- `none`: every tested team up to the top of the grid is unreliable; the generated tables write `none on grid`.
- $D_{\mathrm{overcrowd}}$: the first team from which two tested team sizes in a row are unreliable, searched above $D_{\min}$ (above $D_{\min,\mathrm{low}}$ with no reliable team). One unreliable cell can be a sampling dip, so it takes two.
- $D_{\max}$: the largest reliable team below $D_{\mathrm{overcrowd}}$, or the largest reliable team when there is none. The reliable teams below $D_{\mathrm{overcrowd}}$ are the working teams. At the top of the grid $D_{\max}$ is only a lower bound.
- $D_{\mathrm{sat}}$: the smallest working team that no larger working team beats on finish time ([frontier values](experiments/task_design.md#frontier-values)). One team beats another when, on the seeds both finished, the bootstrap 99% interval of the paired median difference lies more than 5% of the slower median below zero.
- $D_{\mathrm{best}}$ and $D_{\mathrm{crowd}}$: by the same comparison, the smallest working team within 5% of the fastest, and the first working team above $D_{\mathrm{best}}$ more than 5% slower than it.
- Zone: a cell's label along its curve, one of `too_few`, `improving`, `saturated`, `crowded`, `unreliable_dip`, `collapse`, `recovered` and `undecided` ([zones](experiments/task_design.md#zones)).

## Sheep models and dog rules

- Strömbom model: the sheep model of Strömbom et al. (2014), HerdSim's default ([models](methods/models.md#1-sheep-flocking-models)).
- $r_a$: 2 m, the distance below which sheep push each other apart.
- $r_s$: 65 m, the distance within which a sheep reacts to a dog; with no dog that close it grazes.
- GCM and $\mathrm{LCM}_i$: the global centre of mass (mean position of the flock) and the local centre of mass of sheep $i$ (mean position of its nearest neighbours, by default all other sheep, `n_neighbors`).
- Collect distance $f(N) = r_a N^{2/3}$: a sheep farther than this from the GCM is an outlier, the one term the docs use for it. The dogs collect while any sheep is that far out, and drive otherwise.
- Collect point $P_c$ and drive point $P_d$: where a dog aims to collect an outlier or to drive. $P_d$ lies $r_a \sqrt{N}$ behind the flock centre ([team rule](methods/models.md#coordinated-team-architecture-strombom_multi)).
- Team rule: HerdSim's multi-dog controller `collect_drive_multi`, run with Strömbom sheep as `strombom_multi`. While collecting, the $D$ farthest outliers each get one dog (Hungarian algorithm, least total walk) and spare dogs drive the core from behind; while driving, the dogs spread over an arc through $P_d$ ([driving](methods/models.md#3-driving-and-its-limit-for-large-flocks)).
- `independent`: every dog runs Strömbom's single-dog rule on its own, with no team layer.
- FAT (farthest-agent targeting, method `fat`): every dog goes behind the sheep farthest from the goal, with no assignment and no collect/drive switch.
- Kubo model (`kubo`): the force model of Kubo et al. (2022), whose sheep speed up under a stronger push.
- Point dogs: dogs with no size, as in the main runs, so two can stand at one point.
- Dogs kept 2 m apart: dogs that may not step within 2 m of another (`dog_spacing` 2, unrelated to `dog_start_spacing`). A dog already that close walks away; one whose step would end that close does not move that tick ([crowding](experiments/task_design.md#crowding-with-dogs-that-take-up-room)).
- Arc capacity $D_{\mathrm{cap}}$: how many dogs kept 2 m apart fit on the team rule's drive arc, its length divided by 2 m.
- Stop rule: a dog stands still while any sheep is within $3 r_a = 6$ m.

## Variants

- Drive offset cap: a HerdSim variant (`drive_offset_cap`) that keeps the drive point at most $r_s - r_a = 63$ m behind the flock centre. It acts from about 992 sheep, where $r_a \sqrt{N}$ reaches 63 m; above about 1056 the uncapped point would leave the sheep's reaction distance ([drive limit](methods/models.md#3-driving-and-its-limit-for-large-flocks)).
- Sensing range and sharing: team-rule dogs see only the sheep within `sensing_range` (0 for all sheep), and `communication` sets whom they share them with: no one (`none`), dogs in range (`neighbour`) or the whole team (`shared`). Every dog knows where the other dogs are. The gather task uses its own sensing radius ([gather task](#the-gather-task)).
- Field-matched sheep: the values Strömbom et al. (2014) set to mimic real sheep and sheepdogs, $r_a$ = 1 m, noise 0.1 and $r_s$ = 75 m instead of 2 m, 0.3 and 65 m. HerdSim has one noise setting (`noise_strength`), so the dogs get 0.1 too; the paper's Table 1 lists the shepherd's noise (0.3) apart, and its Fig. 5 caption gives one value, $e$ = 0.1. These runs (`dmin_s_matched`, `dmin_f99_s_matched`) also halve `separation_scale` (the spread of the scattered layouts) and `dog_overlap_distance`, from 2.0 to 1.0.

## The gather task

- Gather task: the task of Lama and di Bernardo (2024). Targets and herders start over a disc of radius 50, and the herders bring the targets into a goal of radius 10 at its centre ([gather task](experiments/task_design.md#6-the-gather-task-lama-and-di-bernardo-2024)).
- Targets and herders: the gather task's sheep and dogs. Targets do not flock.
- Sensing radius $\xi$: the distance within which a herder senses targets and other herders, 10 or infinite; the `sensing_radius` parameter of `lama`, unrelated to the team rule's `sensing_range`.
- `targets_lost`: a failure in which some targets were out of every herder's sight at the end; `outnumbered`: every target was seen, but too few were in the goal in time.

## Records

- Physics hash: a digest of every setting that changes a trial; a folder whose hash differs from its protocol is refused ([architecture](codes/architecture.md), [physics hash](guides/configuration.md#physics-hash)). Flock sizes, smaller team sizes and factor levels stay out, so a run can be extended. `metrics_stride` is in it when not 1, because it changes the stored metric columns, though no outcome.
- Code identity: the trial-code hash, git commit, uncommitted-edit flag and Python and library versions, recorded for each sitting. A changed code hash between sittings gives a warning, and the run goes on.
