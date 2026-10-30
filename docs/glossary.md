# Glossary

This page defines the terms HerdSim's docs use, one short definition each, with a link to the section that explains it in full. The other docs link here at a term's first use instead of repeating its definition, and that includes the design terms of [architecture](codes/architecture.md). See also [README](../README.md) for an overview of the study.

## Trials and experiments

- $N$ and $D$: $N$ is the number of sheep (the flock size) and $D$ the number of dogs (the team size). The code and the protocol files call a dog a shepherd (so `shepherd_counts` is the list of team sizes), and the [gather task](#the-gather-task) calls it a herder.
- Protocol: the recipe of one experiment, a YAML file in `protocols/configs/protocols/`. It fixes the methods, layouts, flock sizes, team sizes, [success rule](#success-and-reliability) and [deadline](#the-drive-task). A protocol with `extends:` starts from its parent protocol and changes only what it names. For example, `dmin_f99_s_goal` takes the $1.5 R_f$ goal from `dmin_s_goal`, and `dmin_f99_hold` takes the 99% rule and the 6-drive-time deadline from `dmin_f99_m6`. Every setting that neither the protocol nor a parent names, a canonical setting, keeps its default from `protocols/configs/canonical.yaml`.
- Protocol id: the protocol's name, built from parts. `dmin` is the [$D_{\min}$](#team-sizes) study on the [drive task](#the-drive-task); `f99` the [99% rule](#success-and-reliability) (no `f99` means the strict rule); `m12`, `m6` and `m3` the deadline in [drive times](#the-drive-task); `s_` a sensitivity variant; the last part names the variant (`fat`, `kubo`, `indep`, `hold`, `big`, `view`, `k05`, `c1.3` and so on). `lama_r50` is the [gather task](#the-gather-task) on a start disc of radius 50, `lama_r50_inf` the same with infinite sensing.
- Method: a sheep model (the rule each sheep moves by) paired with a dog controller (the rule each dog moves by). `strombom_multi` pairs Strömbom sheep with the team rule, `fat` and `independent` pair them with the two baseline dog rules, and `kubo` and `lama` are the published models ([sheep models and dog rules](#sheep-models-and-dog-rules)).
- Factor: a canonical setting that a protocol sweeps over several values (its levels), each level giving its own curves. For example, `dmin_s_gap` sweeps `dog_start_gap` over 15, 30 and 60 m. A method parameter cannot be a factor, because [$R_f$](#the-drive-task) is calibrated once per method; each of its values runs as its own protocol.
- Cell: the question "can 3 dogs herd 200 sheep in this setup?" for one method, layout, $N$, $D$ and set of factor levels within one protocol, which fixes the deadline and the success rule. Each cell gets 10 to 200 trials.
- Curve (or group, in the code): the cells of one method, layout, set of factor levels and $N$, one cell for each tested team size.
- Grid: the layouts, flock sizes and team sizes a protocol tests. The top of the grid is its largest team size.
- Trial: one run of one cell with one seed, so one team on one start flock. It runs until it succeeds, ends early or reaches its time limit.
- Tick: one time step of a trial; 1 s for the Strömbom model, 0.05 s for the Kubo model and 0.03 s for the Lama model. Strömbom et al. (2014) give lengths in m and speeds in m per time step (their Table 1: $r_s$ = 65 m, $r_a$ = 2 m, sheep 1 m and dog 1.5 m per time step), but no unit for the time step. HerdSim reads one Strömbom tick as 1 s, so a sheep's step of 1 m per tick is 1 m/s. The Kubo and Lama models give no length unit, and HerdSim reads theirs as 1 m.
- Seed: the number that fixes a trial's random streams (start flock, sheep noise, dog noise). Seed $i$ of a cell is the protocol's master seed (`master_seed`, 2026 by default) plus $i$, so seed $i$ starts from the same flock at every team size ([paired random streams](experiments/task_design.md#paired-random-streams)). Docs name a stored trial by $i$; a few figures give the seed value itself instead, such as 2026, which is seed 0 at the default master seed.
- Seed 0: the first stored trial of a cell. Most animations use it, so that the trial shown is not picked for how it looks; a caption names any other seed.
- Replay: running a stored trial again from its configuration and seed. An unchanged replay must give the stored outcome exactly, the same success and the same number of ticks, and HerdSim raises an error when it does not.
- Campaign: the manager that runs a protocol into its results folder, `results/<protocol id>/`, and spends extra seeds on the cells that are still [undecided](#success-and-reliability). It works in rounds ([adaptive sampling](experiments/task_design.md#3-adaptive-sampling)).
- Sitting: one run of the campaign command on a results folder. A folder can grow over several sittings.
- Round: one pass of a sitting that plans the seeds each undecided cell still needs and runs them ([sampling loop](experiments/task_design.md#the-adaptive-sampling-loop)).
- Batch: the 10 seeds a cell gets at a time (`batch_seeds`).
- Seed cap: the most seeds a cell can get, 200 (`max_seeds`).
- Calibration: the short run at the start of a campaign that measures the flock radius $R_f$ ([drive task](#the-drive-task)) once for each method and flock size. One dog drives a compact flock for 300 s, over 3 seeds and two start flocks, a tight one of radius $\sqrt{N/\pi}$ m and a loose one three times as wide. The gather task sizes itself from its settings and does not calibrate.
- Main runs: the three strict and three 99% protocols at 12, 6 and 3 [drive times](#the-drive-task), on $N = 25$ to 400 and $D = 1$ to 24. The 99% grids at 12 and 6 drive times were later extended to nine flock sizes, 25, 50, 71, 100, 141, 200, 283, 400 and 566. From 50 up each is about $\sqrt{2}$ times the one before; 50 is twice 25.
- Top-up: a later sitting that adds finish-time seeds to existing 99% grids, so that $D_{\mathrm{sat}}$ ([team sizes](#team-sizes)) can be decided.
- Sensitivity runs: 14 protocols at 6 drive times, a base run and six variants under each of the two [success rules](#success-and-reliability). The base run (`dmin_s_base`, `dmin_f99_s_base`) keeps the main setup on `wide` and `outlier_rich`, $N = 100$-400, with a team grid that stops at 16 dogs. Each variant changes one setup choice, on the same seeds: the dog start (`handler`, `ring`), the start gap, the goal radius, the dog speed or the sheep ([field-matched sheep](#variants)).

## The drive task

- Drive task: the dogs gather the flock if needed and drive it into a circular goal.
- $R_f$: the calibrated flock radius, the size a compact flock of $N$ sheep settles to while one dog drives it ($\sqrt{2}$ times its RMS distance to the centre). It sizes the field, the goal and the drive ([sizing](experiments/task_design.md#sizing-by-the-calibrated-flock-radius)).
- Calibration edge: about $N = 600$. Above it a driven flock no longer settles to one radius, so the large-flock protocols impose an $R_f$ on every flock above 566, the largest calibrated size ($400 \times \sqrt{2}$). In `dmin_f99_big` and `dmin_f99_big_cap` the imposed $R_f$ keeps the density of the 566 flock. `dmin_f99_big_dense` and `dmin_f99_big_loose` scale that radius by $1/\sqrt{2}$ and $\sqrt{2}$, for a denser and a looser flock.
- Goal: a circle of radius $1.9 R_f$ by default.
- Drive distance $l$: from the flock's start centre to the goal centre. It is $13 R_f$ by default, and never less than 80 m or than the farthest any sheep can start, over all the protocol's layouts, plus the goal radius plus $R_f$.
- Drive time $T_{\mathrm{drive}}$: the time a sheep walking straight at 1 m/s needs to cover the drive distance ([deadlines](experiments/task_design.md#deadlines-in-drive-times)).
- Deadline: the time limit of a trial, as a multiple of the drive time; 12, 6 or 3 drive times in the drive task. The [Kubo](#sheep-models-and-dog-rules) runs use a fixed 500 s and the gather task 5000 s.
- Finish time: the time a successful trial takes.
- Dog time: $D$ times the finish time, the total time the dogs work.

## Start layouts and dog starts

- Layout: how the sheep are placed at the start ([layouts](experiments/task_design.md#flock-start-layouts)). The Gaussian layouts give their spread as a standard deviation and place no sheep beyond three spreads; the scattered layouts are sized by the [collect distance](#sheep-models-and-dog-rules).
- `compact`: a tight Gaussian flock with a spread of $0.5 R_f$, so no sheep starts beyond $1.5 R_f$. Every sheep starts within the collect distance, so the dogs start by driving.
- `wide`: a Gaussian whose spread is half the collect distance, so about 13% of the sheep start beyond the collect distance at every $N$.
- `split`: three compact clusters (two below $N = 12$) on a circle round the flock centre whose radius is the collect distance.
- `outlier_rich`: 80% of the sheep in a compact core and 20% on a ring 1.1 to 1.6 collect distances from it.
- Scattered layouts: `wide`, `split` and `outlier_rich`, the layouts the dogs must collect before they drive.
- `uniform`: the gather task's start, targets and herders spread uniformly over a disc.
- Dog starts ([dog starts](experiments/task_design.md#dog-starts)):
  - `arcs`: the default, on half circles behind the flock;
  - `ring`: on full circles round it, except toward the goal;
  - `handler`: all dogs at one point behind it.
- Start gap: how far beyond the farthest possible start sheep the first dog circle lies, 30 m by default (`dog_start_gap`). Dogs on one circle stand at least 5 m apart (`dog_start_spacing`), and dogs that do not fit go on a circle 5 m farther out.

## Success and reliability

- Strict rule: a trial succeeds when every sheep is inside the goal at one tick.
- 99% rule: a trial succeeds when at least 99% of the sheep, $\lceil 0.99 N \rceil$, are inside at one tick. Below $N = 100$, $\lceil 0.99 N \rceil = N$, so the two rules agree there.
- Holding task: a trial succeeds only once 99% of the flock has stayed inside the goal for one drive time, while the dogs withdraw to 67 m beyond the farthest sheep ([holding](experiments/task_design.md#the-holding-task)). `dmin_f99_hold_share` also tries shares of 95% and 90%.
- $\theta$: the reliability threshold, 0.90.
- Reliable cell: a cell whose 99% Clopper-Pearson interval of the success rate lies at or above $\theta$ ([stopping early](experiments/task_design.md#stopping-early-with-the-99-clopper-pearson-interval)). An unreliable cell's interval lies below $\theta$ and an undecided cell's straddles it. Reliable and unreliable cells are decided. A reliable decision needs at least 51 successes without a failure. Seeds come in batches of 10, so the earliest is at 60 trials: 60 of 60 gives a lower bound of 0.915, and 59 of 60 gives 0.883, still undecided.
- Open cell: a cell that still asks for seeds, because its reliability is undecided or, in runs with `decide_finish_times` true, one of its finish-time comparisons is. Cells with a trial that raised an error, and cells [pruned above saturation](experiments/task_design.md#pruning-above-saturation), get no seeds and are not counted (`cells_needing_seeds` in `status.json`, and `cells_at_max_seeds_undecided` for those at the seed cap).
- Frontier rules: the rules that turn a curve's stored trials into its frontier, the decision of each cell and the team-size values below ([frontier rules](experiments/task_design.md#5-frontier-rules-and-zones)).

## Team sizes

- $D_{\min}$: the smallest reliable team on a curve ([report, section 2.1](report/d_min_report.md#21-when-a-team-is-reliable)).
- Bracket, written `3-8`, and $D_{\min,\mathrm{low}}$: 8 dogs are reliable, and 3 dogs are still undecided, so $D_{\min}$ lies between 3 and 8. The lower end, $D_{\min,\mathrm{low}}$, is the smallest team whose interval still reaches $\theta$, the smallest team not yet decided unreliable.
- Lower bound, written `[5]`: no team is reliable yet, and $D_{\min}$ is at least 5, its $D_{\min,\mathrm{low}}$.
- `none`: every tested team up to the top of the grid is unreliable. The generated tables write it `none on grid`.
- $D_{\mathrm{overcrowd}}$: the first team from which two tested team sizes in a row are unreliable, looked for above $D_{\min}$ (above $D_{\min,\mathrm{low}}$ on a curve with no reliable team). One unreliable cell can be a sampling dip near the threshold, so it takes two.
- $D_{\max}$: the largest reliable team below $D_{\mathrm{overcrowd}}$, or the largest reliable team when a curve has no $D_{\mathrm{overcrowd}}$. These reliable teams below $D_{\mathrm{overcrowd}}$ are the working teams. At the top of the grid $D_{\max}$ is only a lower bound, because no upper limit was found.
- $D_{\mathrm{sat}}$: the smallest working team that no larger working team beats on finish time ([frontier values](experiments/task_design.md#frontier-values)). One team beats another when, on the seeds both finished, the bootstrap 99% interval of the paired median difference lies more than 5% of the slower median below zero.
- $D_{\mathrm{best}}$ and $D_{\mathrm{crowd}}$: compared the same way, the smallest working team as fast as the fastest one (within 5%), and the first working team above $D_{\mathrm{best}}$ that is more than 5% slower than $D_{\mathrm{best}}$.
- Zone: the label of a cell along its curve ([zones](experiments/task_design.md#zones)): `too_few`, `improving`, `saturated`, `crowded`, `unreliable_dip` (unreliable between $D_{\min}$, or $D_{\min,\mathrm{low}}$ on a curve with no reliable team, and $D_{\mathrm{overcrowd}}$), `collapse` (unreliable from $D_{\mathrm{overcrowd}}$ up), `recovered` (reliable again above $D_{\mathrm{overcrowd}}$) and `undecided`.

## Sheep models and dog rules

- Strömbom model: the sheep model of Strömbom et al. (2014) that HerdSim runs by default ([models](methods/models.md#1-sheep-flocking-models)).
- $r_a$: 2 m, the distance below which sheep push each other apart.
- $r_s$: 65 m, the distance within which a sheep reacts to a dog; a sheep with no dog that close grazes.
- GCM and $\mathrm{LCM}_i$: the global centre of mass, the mean position of the whole flock, and the local centre of mass of sheep $i$, the mean position of its nearest neighbours (by default all the other sheep, `n_neighbors`).
- Collect distance $f(N) = r_a N^{2/3}$: a sheep farther than this from the GCM is an outlier. The dogs collect while any sheep is that far out and drive otherwise. Outlier is the one term the docs use for such a sheep.
- Collect point $P_c$ and drive point $P_d$: where a dog aims when it collects an outlier or drives the flock. $P_d$ lies $r_a \sqrt{N}$ behind the flock centre ([team rule](methods/models.md#coordinated-team-architecture-strombom_multi)).
- Team rule: HerdSim's multi-dog rule, the dog controller `collect_drive_multi`; the method `strombom_multi` runs it with Strömbom sheep. While the dogs collect, the $D$ farthest outliers each get one dog, assigned by the Hungarian algorithm (the least total walk); with fewer outliers than dogs, the dogs left over drive the core of the flock, the sheep within $f(N)$ of the GCM, from behind. When they drive, they spread over an arc behind the flock through $P_d$ ([driving](methods/models.md#3-driving-and-its-limit-for-large-flocks)).
- `independent`: every dog runs Strömbom's single-dog rule on its own, with no team layer.
- FAT (farthest-agent targeting, method `fat`): every dog goes behind the sheep farthest from the goal, with no assignment and no collect/drive switch.
- Kubo model (`kubo`): the force model of Kubo et al. (2022), whose sheep speed up under a stronger push.
- Point dogs: dogs with no size, as in the main runs, so two can stand at one point.
- Dogs kept 2 m apart: dogs that may not step within 2 m of another (`dog_spacing` 2, a different setting from `dog_start_spacing`); a dog already that close walks away, and one whose step would end that close does not move that tick ([crowding](experiments/task_design.md#crowding-with-dogs-that-take-up-room)).
- Arc capacity $D_{\mathrm{cap}}$: how many dogs kept 2 m apart fit on the team rule's drive arc, its length divided by 2 m.
- Stop rule: a dog stands still while any sheep is within $3 r_a = 6$ m.

## Variants

- Drive offset cap: a HerdSim variant (`drive_offset_cap`) that limits the drive point to $r_s - r_a = 63$ m behind the flock centre. It acts from about 992 sheep, where $r_a \sqrt{N}$ reaches 63 m, and keeps the drive point within the sheep's reaction distance above about 1056, where the uncapped point leaves it ([drive limit](methods/models.md#3-driving-and-its-limit-for-large-flocks)).
- Sensing range and sharing: dogs of the team rule that see only the sheep within a range (`sensing_range`, 0 for every sheep), and the setting `communication` says whom they share what they see with: no one (`none`), the dogs in range (`neighbour`) or the whole team (`shared`). Every dog knows where the other dogs are. The gather task's herders use their own setting, the sensing radius ([gather task](#the-gather-task)).
- Field-matched sheep: the sheep parameters that Strömbom et al. (2014) set to mimic real sheep and sheepdogs, $r_a$ = 1 m, noise 0.1 and $r_s$ = 75 m instead of 2 m, 0.3 and 65 m. The noise of 0.1 applies to the dogs as well, because HerdSim uses one noise setting (`noise_strength`) for sheep and dogs. That is HerdSim's choice: Table 1 of the paper lists the shepherd's noise (0.3) apart from the sheep's, and its Fig. 5 caption gives one value, $e$ = 0.1. The runs with these sheep (`dmin_s_matched`, `dmin_f99_s_matched`) also set `separation_scale` to 1.0 instead of 2.0, which halves the spread of the scattered start layouts, and `dog_overlap_distance` to 1.0 instead of 2.0.

## The gather task

- Gather task: the task of Lama and di Bernardo (2024); targets and herders start spread over a disc of radius 50, and the herders bring the targets into a goal of radius 10 at its centre ([gather task](experiments/task_design.md#6-the-gather-task-lama-and-di-bernardo-2024)).
- Targets and herders: the gather task's sheep and dogs. Targets do not flock.
- Sensing radius $\xi$: the distance within which a herder senses targets and other herders; 10, or infinite. It is the `sensing_radius` parameter of the `lama` method, a different setting from the team rule's `sensing_range`.
- `targets_lost`: a failure in which some targets were out of every herder's sight at the end; `outnumbered`: every target was seen, but too few were in the goal in time.

## Records

- Physics hash: a digest of every setting that changes a trial, checked at every start so that a folder whose hash differs from its protocol is refused ([architecture](codes/architecture.md)). It covers the task, the layouts, the largest team size, each method's parameters and time limit, and the canonical settings with `master_seed`, but leaves out the flock sizes, smaller team sizes and factor levels (so a run can be extended), the seed-spending and decision rules such as $\theta$ and the seed cap, another task's settings, and later-added settings left at their neutral value, the off value at which they change no trial. It also covers `metrics_stride` when that is not 1: the stride changes no outcome, but it changes the stored metric columns, which must agree within a folder.
- Code identity: the trial-code hash, commit, uncommitted-edit flag and Python and library versions, recorded for each sitting; a changed code hash between sittings gives a warning, and the run goes on.
