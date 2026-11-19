# Glossary

Short definitions of the terms and symbols used across HerdSim's docs. Each entry links to the doc that explains it in full, mainly the [task design](experiments/task_design.md), the [methods](methods/strombom_multi.md) and the [report](report/d_min_report.md).

## Trials and experiments

These terms describe how HerdSim organises experiments, trials and adaptive sampling:

- $N$ and $D$: the number of sheep (flock size) and dogs (team size). Code and protocol files call a dog a shepherd (`shepherd_counts`).
- Protocol: the YAML recipe for one experiment in `protocols/configs/protocols/`. It fixes the method, layouts, flock sizes, team sizes, [success rule](#success-and-reliability) and [deadline](#the-drive-task) ([configuration guide](guides/configuration.md#protocol-overrides)).
- Protocol id: the protocol's name. `dmin` marks the $D_{\min}$ study, `f99` the [99% rule](#success-and-reliability) (no `f99` means the strict rule), and `m12`, `m6`, `m3` the deadline in [drive times](#the-drive-task); `fat` and `indep` mark the baseline protocols at 6 drive times.
- Main runs: the nine study protocols listed in the [README](../README.md#study-runs-and-how-reliability-is-decided).
- Method: a sheep model paired with a dog rule (`strombom_multi`, `fat` or `independent`; see [sheep model and dog rule](#sheep-model-and-dog-rule)).
- Grid: the layouts, flock sizes and team sizes a protocol tests; the top of the grid is its largest team size ($D = 24$ in the study).
- Group and curve: a group is one setup (one layout and flock size $N$); its curve is the sequence of its cells over the tested team sizes $D$.
- Cell: one $(layout, N, D)$ point on a curve, answering "can $D$ dogs herd $N$ sheep in this layout?". A cell gets trials in batches of 10 seeds (`batch_seeds`) up to 200 (`max_seeds`).
- Trial and tick: a trial is one simulation run of a cell with one seed, stepped one tick (1 s) at a time until it succeeds or reaches the deadline.
- Seed: the integer that fixes a trial's random streams (`master_seed + i`, with `master_seed = 2026` by default), so trial $i$ starts from the same flock at every team size ([paired random streams](experiments/task_design.md#paired-random-streams)).
- Replay: rerunning a stored trial from its settings and seed; a different outcome or tick count raises an error.
- Campaign, sitting and round: the campaign is the manager that runs a protocol into `results/<protocol_id>/` ([adaptive sampling](experiments/task_design.md#3-adaptive-sampling)). Each call of the command-line tool is a sitting, and each pass that gives another batch of seeds to the [open cells](#success-and-reliability) is a round ([architecture](codes/architecture.md#how-a-campaign-runs)).
- Calibration: the first step of a campaign, which measures $R_f$ at each flock size ([sizing](experiments/task_design.md#sizing-by-the-calibrated-flock-radius)).

## The drive task

These terms define the field and the time limits:

- Drive task: dogs gather a flock if it is scattered and drive it into a circular goal.
- Calibrated flock radius $R_f$: the radius a compact flock of $N$ sheep settles to while one dog drives it ($\sqrt{2}$ times the root-mean-square distance to the flock centre). It sets the size of the goal and the drive distance ([sizing](experiments/task_design.md#sizing-by-the-calibrated-flock-radius)).
- Calibration edge: the smallest tested flock size at which calibration fails its 5% limits ($N = 630$ with 3 seeds per start, 660 with 20). The study stops at $N = 566$, the last $\sqrt{2}$ step below it ([flock size](experiments/task_design.md#flock-size)).
- Goal: a circle of radius $1.9 R_f$.
- Drive distance $l$: the distance from the flock's start centre to the goal centre, the largest of $13 R_f$, 80 m, and the room the widest start layout needs ([sizing](experiments/task_design.md#sizing-by-the-calibrated-flock-radius)).
- Drive time $T_{\mathrm{drive}}$ and deadline: one drive time is the time a sheep walking straight at 1 m/s needs to cover $l$. A trial's deadline is 12, 6 or 3 drive times ([deadlines](experiments/task_design.md#deadlines-in-drive-times)).
- Finish time: the number of ticks (seconds) a successful trial takes to meet its success rule.

## Start layouts and dog starts

These terms describe where sheep and dogs are at tick 0 ([layouts](experiments/task_design.md#flock-start-layouts), [dog starts](experiments/task_design.md#dog-starts)):

- Layout: how the sheep are spread at the start: `compact`, `wide`, `split` or `outlier_rich`.
- `compact`: a tight cluster with every sheep within the [collect distance](#sheep-model-and-dog-rule), so the dogs drive at once.
- `wide`: a loose cluster with about 13% of the sheep beyond the collect distance at every $N$.
- `split`: three compact clusters (two when $N < 12$) on a circle whose radius is the collect distance.
- `outlier_rich`: a compact core with 80% of the sheep and a ring with the other 20% at 1.1 to 1.6 collect distances.
- Scattered layouts: `wide`, `split` and `outlier_rich`, where some sheep start beyond the collect distance and must be collected before driving.
- Dog start (`arcs`): dogs start on semicircles behind the flock, 30 m beyond the farthest possible start of a sheep (`dog_start_gap`), at least 5 m apart (`dog_start_spacing`).

## Success and reliability

These terms define when a trial succeeds and when a cell is decided ([stopping rule](experiments/task_design.md#stopping-early-with-the-99-clopper-pearson-interval)):

- Strict rule: a trial succeeds when all $N$ sheep are inside the goal at the same tick before the deadline.
- 99% rule: a trial succeeds when at least $\lceil 0.99 N \rceil$ sheep are inside the goal at the same tick before the deadline; below $N = 100$ this is the strict rule.
- Reliability threshold $\theta$: the success rate a team must reach, $\theta = 0.90$.
- Reliable, unreliable and undecided: with $[L, U]$ the two-sided 99% Clopper-Pearson interval of a cell's success rate, a cell is reliable when $L \ge \theta$ and it has no trial errors, unreliable when $U < \theta$, and undecided on reliability otherwise.
- Open cell: a cell that still needs seeds, because it is undecided on reliability or, when `decide_finish_times` is on, on a finish-time comparison. Errored and [pruned](experiments/task_design.md#pruning-above-saturation) cells get no more seeds, and neither does an open cell at 200 seeds; `status.json` still lists it (`cells_needing_seeds`).
- Frontier rules and zones: the rules that give each cell of a curve a zone label (such as `too_few`, `improving`, `saturated` or `undecided`) and find the critical team sizes ([frontier rules](experiments/task_design.md#5-frontier-rules-and-zones)).

## Team sizes

These terms describe the critical team sizes of a curve ([report, section 1](report/d_min_report.md#1-the-question)):

- $D_{\min}$: the smallest reliable team size on a curve.
- Bracket (`3-8`) and $D_{\min,\mathrm{low}}$: 8 dogs are reliable, and smaller teams down to $D_{\min,\mathrm{low}} = 3$ (the smallest team whose interval still reaches $\theta$) are undecided at 200 seeds.
- Lower bound (`[5]`): no tested team is reliable yet, and the smallest team not yet ruled out is $D_{\min,\mathrm{low}} = 5$.
- `none` (`none on grid`): every tested team up to the top of the grid is unreliable.
- $D_{\min,\mathrm{stable}}$: on a curve where a team above $D_{\min,\mathrm{low}}$ is unreliable, the smallest reliable team above the last unreliable one ([report, section 2.1](report/d_min_report.md#teams-that-fail-above-d_min)).
- Saturation team size $D_{\mathrm{sat}}$: the smallest reliable team that no larger reliable team beats on finish time over shared seeds. The campaign uses it to [prune seeds](experiments/task_design.md#pruning-above-saturation); it and the other frontier values are defined in [frontier values](experiments/task_design.md#frontier-values).

## Sheep model and dog rule

These terms define how sheep and dogs move ([sheep model](methods/strombom_sheep.md), [team rule](methods/strombom_multi.md)):

- Strombom model: the sheep and one-dog rules of Strombom et al. (2014).
- Interaction distances $r_a$ and $r_s$: a sheep moves away from other sheep closer than $r_a = 2$ m, and reacts to any dog closer than the detection radius $r_s = 65$ m; with no dog that close it grazes. The Figure 3 part of the [paper check](methods/strombom_check.md) uses $r_s = 45$ m, from the paper's Figure 3 caption.
- Grazing repulsion (`graze_repulsion`): sheep keep $r_a$ apart even when grazing. It is off in the nine study runs and on in the paper check and the grazing pilots ([grazing](methods/strombom_sheep.md#grazing)).
- Neighbour count $n$: the number of nearest neighbours that attract each sheep; $n = N - 1$ (all other sheep) in the study, varied in the [paper check](methods/strombom_check.md#terms).
- $\mathrm{GCM}$ and $\mathrm{LCM}_i$: the mean position of all $N$ sheep, and of sheep $i$'s $n$ nearest neighbours.
- Collect distance $f(N) = r_a N^{2/3}$: a sheep farther than this from the $\mathrm{GCM}$ is an outlier, and the dogs collect before they drive.
- Collect point $P_c$ and drive point $P_d$: the dog's target $r_a$ behind an outlier when collecting, and $r_a \sqrt{N}$ behind the $\mathrm{GCM}$ when driving.
- Team rule (`strombom_multi`): HerdSim's multi-dog rule. Each of the $D$ farthest outliers gets its own dog, and when all sheep are within $f(N)$ the dogs spread on an arc behind the flock ([details](methods/strombom_multi.md)).
- Farthest-agent targeting (`fat`): the uncoordinated baseline; every dog aims $r_a$ behind the sheep farthest from the goal ([details](methods/fat.md)).
- Independent paper shepherds (`independent`): the baseline in which every dog runs Strombom's one-dog rule, so all dogs aim at the same target ([details](methods/independent.md)).
- Stop rule: a dog stands still for a tick when any sheep is closer than $3 r_a = 6$ m.

## Records

These terms describe how stored results are checked:

- Physics hash: a digest of the protocol settings that affect trial trajectories. A results folder refuses a run whose physics hash differs from the stored one ([configuration guide](guides/configuration.md#physics-hash)).
- Code identity: the trial-code hash, git commit, dirty-worktree flag and package versions that each sitting logs in `runs.jsonl`, with a warning when the trial-code hash changes ([results folder](guides/configuration.md#what-a-simulation-run-writes)).
