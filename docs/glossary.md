# Glossary

The terms HerdSim's docs use, one short definition each, with a link to the section that explains it in full. The other docs link here at a term's first use instead of repeating its definition; this includes the design terms of [architecture](codes/architecture.md). See also [README](../README.md) for an overview of the study.

## Trials and experiments

- Trial: one simulation of one team on one start flock, run until it succeeds, ends early or reaches its time limit.
- Tick: one time step of a trial; 1 s for the Strömbom model, 0.05 s for the Kubo model and 0.03 s for the Lama model.
- Seed: the number that fixes a trial's random streams (start flock, sheep noise, dog noise). Seed $i$ of a cell is the protocol's master seed plus $i$, so seed $i$ starts from the same flock at every team size ([paired random streams](experiments/task_design.md#paired-random-streams)). A few figures give the random seed itself instead, such as 2026.
- Seed 0: the first stored trial of a cell. Most animations use it, so that the trial shown is not picked for how it looks; a caption names any other seed.
- Replay: running a stored trial again from its configuration and seed; it must reproduce the stored outcome exactly, and HerdSim raises an error when it does not.
- Protocol: one experiment, written as a YAML file in `protocols/configs/protocols/`. It fixes the methods, layouts, flock sizes, team sizes, success rule and deadline.
- Protocol id: the protocol's name, built from parts. `dmin` is the $D_{\min}$ study on the drive task; `f99` the 99% rule (no `f99` means the strict rule); `m12`, `m6` and `m3` the deadline in drive times; `s_` a sensitivity variant; the last part names the variant (`fat`, `kubo`, `indep`, `hold`, `big`, `view`, `k05`, `c1.3` and so on). `lama_r50` is the gather task on a start disc of radius 50, `lama_r50_inf` the same with infinite sensing.
- Campaign: running a protocol into its results folder, `results/<protocol id>/`, in rounds that add seeds where cells are still undecided ([adaptive sampling](experiments/task_design.md#3-adaptive-sequential-sampling-engine)).
- Round: one pass of a sitting that plans the seeds each undecided cell still needs and runs them ([sampling loop](experiments/task_design.md#the-adaptive-sampling-loop)).
- Batch: the 10 seeds a cell gets at a time.
- Seed cap: the most seeds a cell can get, 200.
- Calibration: the short run at the start of a campaign that measures the flock radius $R_f$ for one method and flock size.
- Method: a sheep model paired with a dog controller, such as `strombom_multi` (Strömbom sheep with the team rule) or `lama`.
- Factor: a canonical setting that a protocol sweeps over several values, each value giving its own curves.
- Cell: one method, layout, flock size $N$ and team size $D$ (with any factor levels) within one protocol, which fixes the deadline and the rule. Each cell gets 10 to 200 trials.
- Curve (or group, in the code): the cells of one method, layout, factor levels and $N$ across the tested team sizes.
- Grid: the layouts, flock sizes and team sizes a protocol tests.
- Main runs: the three strict and three 99% protocols at 12, 6 and 3 drive times, on $N = 25$ to 400 and $D = 1$ to 24; the 99% grids at 12 and 6 drive times were later extended to nine flock sizes up to 566.
- Top-up: a later sitting that adds finish-time seeds to existing 99% grids, so that $D_{\mathrm{sat}}$ can be decided.
- Sensitivity runs: protocols that change one setting of the main runs (dog start, start gap, goal radius, dog speed, field-matched sheep) and compare with a base run on the same seeds.

## The drive task

- $N$: the number of sheep; $D$: the number of dogs (the team size).
- Drive task: the dogs gather the flock if needed and drive it into a circular goal.
- $R_f$: the calibrated flock radius, the size a compact flock of $N$ sheep settles to while one dog drives it ($\sqrt{2}$ times its RMS distance to the centre). It sizes the field, the goal and the drive ([sizing](experiments/task_design.md#sizing-by-the-calibrated-flock-radius)).
- Calibration edge: about $N = 600$; above it a driven flock no longer settles to one radius, so the large-flock protocols impose $R_f$ at the density of the 566 flock.
- Goal: a circle of radius $1.9 R_f$ by default.
- Drive distance $l$: from the flock's start centre to the goal centre.
- Drive time $T_{\mathrm{drive}}$: the time a sheep walking straight at 1 m/s needs to cover the drive distance ([deadlines](experiments/task_design.md#deadlines-in-drive-times)).
- Deadline: the time limit of a trial, as a multiple of the drive time: 12, 6 or 3 drive times in the drive task. The Kubo runs use a fixed 500 s and the gather task 5000 s.
- Finish time: the time a successful trial takes.
- Dog time: $D$ times the finish time, the total time the dogs work.

## Start layouts and dog starts

- Layout: how the sheep are placed at the start ([layouts](experiments/task_design.md#flock-start-layouts)).
- `compact`: a tight Gaussian flock; every sheep starts within the collect distance, so the dogs start by driving.
- `wide`: a Gaussian whose spread is half the collect distance, cut at three spreads, so about 13% of the sheep start beyond the collect distance.
- `split`: three compact clusters on a circle round the flock centre.
- `outlier_rich`: 80% of the sheep in a compact core and 20% on a ring beyond the collect distance.
- Scattered layouts: `wide`, `split` and `outlier_rich`, the layouts the dogs must collect before they drive.
- `uniform`: the gather task's start, targets and herders spread uniformly over a disc.
- Dog starts ([dog starts](experiments/task_design.md#dog-starts)):
  - `arcs`: the default, on half circles behind the flock;
  - `ring`: on full circles round it, except toward the goal;
  - `handler`: all dogs at one point behind it.
- Start gap: how far beyond the farthest possible start sheep the first dog circle lies, 30 m by default.

## Success and reliability

- Strict rule: a trial succeeds when every sheep is inside the goal at one tick.
- 99% rule: a trial succeeds when at least 99% of the sheep are inside at one tick.
- Holding task: a trial succeeds only once 99% of the flock has stayed inside the goal for one drive time, while the dogs withdraw ([holding](experiments/task_design.md#the-holding-task)).
- $\theta$: the reliability threshold, 0.90.
- Reliable cell: the 99% Clopper-Pearson interval of its success rate lies at or above $\theta$; unreliable: it lies below; undecided: it straddles $\theta$ ([stopping early](experiments/task_design.md#stopping-early-with-the-99-clopper-pearson-interval)).
- Open: still undecided when the cell reached its cap of 200 trials.
- Frontier rules: the rules that decide reliability, the finish-time comparisons and the team-size values below from the stored trials ([frontier rules](experiments/task_design.md#5-frontier-rules-and-zones)).

## Team sizes

- $D_{\min}$: the smallest reliable team on a curve ([report, section 2.1](report/d_min_report.md#21-when-a-team-is-reliable)).
- $D_{\min,\mathrm{low}}$: the smallest team whose interval still reaches $\theta$; the lower end of a bracket.
- Bracket, written `3-8`: 8 dogs are reliable and a smaller team from 3 up is still undecided.
- Lower bound, written `[5]`: no team is reliable yet, and $D_{\min}$ is at least 5.
- `none`: every tested team up to the top of the grid is unreliable.
- $D_{\mathrm{sat}}$: the smallest reliable team that no larger reliable team beats on finish time by more than 5% with 99% confidence ([frontier values](experiments/task_design.md#frontier-values)).
- $D_{\max}$: the largest reliable team below $D_{\mathrm{overcrowd}}$, or the largest reliable team. At the top of the grid it is only a lower bound: no upper limit was found.
- $D_{\mathrm{overcrowd}}$: the first team from which two tested team sizes in a row are unreliable, looked for above $D_{\min}$ (above $D_{\min,\mathrm{low}}$ on a curve with no reliable team).
- $D_{\mathrm{best}}$ and $D_{\mathrm{crowd}}$: the smallest team as fast as the fastest, and the first reliable team above $D_{\mathrm{best}}$ that is slower than $D_{\mathrm{best}}$.
- Zone: the label of a cell along its curve (improving, saturated, crowded, collapse and the rest), explained in [zones](experiments/task_design.md#zones).

## Sheep models and dog rules

- Strömbom model: the sheep model of Strömbom et al. (2014) that HerdSim runs by default ([models](methods/models.md#1-sheep-flocking-models)).
- $r_a$: 2 m, the distance below which sheep push each other apart.
- $r_s$: 65 m, the distance within which a sheep reacts to a dog; a sheep with no dog that close grazes.
- Collect distance $f(N) = r_a N^{2/3}$: a sheep farther than this from the flock centre is an outlier (or stray), and the dogs collect while any sheep is that far out; otherwise they drive.
- GCM: the centre of the whole flock; $\mathrm{LCM}_i$: the centre of sheep $i$'s nearest neighbours.
- Collect point $P_c$ and drive point $P_d$: where a dog aims when it collects an outlier or drives the flock ([team rule](methods/models.md#coordinated-team-architecture-strombom_multi)).
- Team rule, `strombom_multi`: HerdSim's multi-dog rule; the dogs collect different outliers, assigned by the Hungarian algorithm, and drive from an arc behind the flock.
- `independent`: every dog runs Strömbom's single-dog rule on its own, with no team layer.
- FAT (farthest-agent targeting): every dog goes behind the sheep farthest from the goal, with no assignment and no collect/drive switch.
- Kubo model (`kubo`): the force model of Kubo et al. (2022), whose sheep speed up under a stronger push.
- Point dogs: dogs with no size, as in the main runs, so two can stand at one point.
- Dogs kept 2 m apart: no dog may come within 2 m of another; a dog whose step would end that close does not move that tick ([crowding](experiments/task_design.md#crowding-with-dogs-that-take-up-room)).
- Arc capacity $D_{\mathrm{cap}}$: how many dogs kept 2 m apart fit on the arc behind the flock.
- Stop rule: a dog stands still while any sheep is within $3 r_a = 6$ m.

## Variants

- Drive offset cap: a HerdSim variant that limits the drive point to $r_s - r_a = 63$ m behind the flock centre. It acts from about 992 sheep and keeps the drive point within the sheep's reaction distance above about 1056, where the uncapped point leaves it ([drive limit](methods/models.md#3-driving-and-its-limit-for-large-flocks)).
- Sensing range and sharing: dogs that see only the sheep within a range, sharing what they see with no one, with the dogs in range, or with the whole team.
- Field-matched sheep: the sheep parameters that Strömbom et al. (2014) set to mimic real sheep and sheepdogs (their Fig. 5).

## The gather task

- Gather task: the task of Lama and di Bernardo (2024); targets and herders start spread over a disc of radius 50, and the herders bring the targets into a goal of radius 10 at its centre ([gather task](experiments/task_design.md#6-the-gather-task-lama-and-di-bernardo-2024)).
- Targets and herders: the gather task's sheep and dogs. Targets do not flock.
- Sensing radius $\xi$: the distance within which a herder senses targets and other herders; 10, or infinite.
- `targets_lost`: a failure in which some targets were out of every herder's sight at the end; `outnumbered`: every target was seen, but too few were in the goal in time.

## Records

- Physics hash: a digest of the settings that change a trial's outcome, leaving out the flock sizes, factor levels and sampling strategy so that a run can be extended; a folder whose hash differs from its protocol is refused ([architecture](codes/architecture.md)).
- Code identity: the hash of the trial code, the commit and the library versions, recorded for each sitting.
- Sitting: one run of the campaign command on a results folder.
