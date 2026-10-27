# Task design and experimental method

This document describes how HerdSim sets up its tasks: the geometry, the start layouts, the adaptive sampling, the decision rules, and why the grids stop where they do.

## Contents

- [1. Task geometry and scale](#1-task-geometry-and-scale)
- [2. Start layouts and dog starts](#2-start-layouts-and-dog-starts)
- [3. Adaptive sequential sampling engine](#3-adaptive-sequential-sampling-engine)
- [4. Why the grid stops where it does](#4-why-the-grid-stops-where-it-does)
- [5. Frontier rules and zones](#5-frontier-rules-and-zones)
- [6. The gather task (Lama and di Bernardo 2024)](#6-the-gather-task-lama-and-di-bernardo-2024)

## 1. Task geometry and scale

### Why the field grows with the flock

HerdSim has no walls: a wall would stop sheep the dogs failed to stop, and neither source model has one. Without walls the field is only the drawn extent, and what has to scale is the task itself. A goal of fixed radius would hold a flock of 25 with room to spare and a flock of 400 not at all, and a fixed drive of 100 m would be sixteen flock radii for the small flock and nine for the large one. HerdSim therefore sets the drive distance and the goal radius as multiples of the flock's own size, so the task has the same shape at every $N$ (Figure 1).

![Task geometry and physical scaling](../../docs/figures/fig6_task_geometry.png)

**Figure 1: Task geometry drawn to scale.** Left: the field at $N = 200$ sheep; middle: the drive distance $l$ against $N$, the largest of its three terms; right: the calibrated flock radius $R_f(N)$ and the goal radius across flock sizes.

### Sizing by the calibrated flock radius

Every length of the drive task is a multiple of the **calibrated flock radius $R_f(N)$**: the size a flock of $N$ sheep settles to while one dog drives it. It is $\sqrt{2}$ times the RMS distance of the sheep from the flock centre (the radius of a uniform disc with that RMS), averaged over the last 90 s of a 300 s drive by one all-seeing dog, and taken as the median over 3 seeds and two start sizes. It is measured once per method and $N$ at the start of a campaign, not per trial, and a size whose radius has not settled or depends on its start is refused. Table 1 lists the rules for each length.

**Table 1: Lengths of the drive task.**

| Quantity | Rule | Meaning |
| :--- | :--- | :--- |
| Flock radius $R_f(N)$ | Calibrated (for example $6.2$ m at $N = 25$, $11.4$ m at $N = 400$) | The size of an $N$-sheep flock under one driving dog. |
| Drive distance $l$ | $\max(13\,R_f(N),\ 80,\ l_{\mathrm{reach}} + R_{\mathrm{goal}} + R_f)$ | From the flock's start centre to the goal centre. Larger flocks are driven farther; the floor of 80 m keeps the smallest flocks from a drive of a few metres; the third term keeps the goal clear of every start ($l_{\mathrm{reach}}$ is the farthest any sheep can start, over every layout of the protocol). |
| Goal radius $R_{\mathrm{goal}}$ | $1.9\,R_f(N)$ | The goal holds the settled flock with the same margin at every $N$. The multiples 13 and 1.9 are conventions; the sensitivity runs test a goal of $1.5\,R_f$. |
| Field clearance | $80$ m around everything placed at the start (flock, dog stations, goal) | Only sizes the field; nothing stops the animals there. |
| Boundary | None | Animals can move anywhere, as in Strömbom et al. (2014) and Kubo et al. (2022). |

### Deadlines in drive times

A fixed 5-minute limit for every flock size would be unfair to large flocks, which are driven over 200 m against 80 m for small ones.

HerdSim writes deadlines as multiples of the **drive time** $T_{\mathrm{drive}}$, the time a sheep walking straight at its speed ($1.0$ m/s, the only speed of a Strömbom sheep) needs to cover the drive distance:

$$
T_{\mathrm{drive}} = \frac{l}{v_{\mathrm{sheep,max}}}
$$

A compact flock driven by one dog finishes in about $1.46$ to $1.74\,T_{\mathrm{drive}}$. The main protocols use deadlines of 3, 6 and 12 $T_{\mathrm{drive}}$: about two, four and eight times that one-dog time, each a doubling of the last. The loose deadline leaves one dog time to collect strays in turn; the tight one does not. Which deadline needs how many dogs is a result ([report, sections 3.1 and 3.3](../report/d_min_report.md)). The Kubo protocols use the paper's fixed limit of 500 s instead.

Table 2 gives the deadlines of the main grids (protocol `dmin_m12` and its variants, four layouts):

**Table 2: Deadlines of the main grids.**

| Flock size ($N$) | Flock radius $R_f$ | Drive distance $l$ | Drive time $T_{\mathrm{drive}}$ | $12\times$ deadline | $6\times$ deadline | $3\times$ deadline |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $N = 25$ | $6.20$ m | $80.6$ m | $80.6$ s (about 1.3 min) | $968$ s (about 16.1 min) | $484$ s (about 8.1 min) | $242$ s (about 4.0 min) |
| $N = 50$ | $7.60$ m | $98.8$ m | $98.8$ s (about 1.6 min) | $1186$ s (about 19.8 min) | $593$ s (about 9.9 min) | $297$ s (about 4.9 min) |
| $N = 100$ | $9.08$ m | $118.1$ m | $118.1$ s (about 2.0 min) | $1417$ s (about 23.6 min) | $709$ s (about 11.8 min) | $355$ s (about 5.9 min) |
| $N = 200$ | $10.47$ m | $139.8$ m | $139.8$ s (about 2.3 min) | $1678$ s (about 28.0 min) | $839$ s (about 14.0 min) | $420$ s (about 7.0 min) |
| $N = 400$ | $11.40$ m | $206.8$ m | $206.8$ s (about 3.4 min) | $2482$ s (about 41.4 min) | $1241$ s (about 20.7 min) | $621$ s (about 10.3 min) |

The scattered layouts grow as $N^{2/3}$ while $R_f(N)$ grows much slower, so from $N = 200$ the reach term wins and the drive is longer than $13\,R_f$ (18 $R_f$ at $N = 400$). The deadline is in drive times, so a longer drive gets a longer deadline, but the dogs on a large scattered flock drive farther, in flock radii, than on a small one.

### The holding task

Two follow-up protocols (`dmin_f99_hold`, `dmin_f99_hold_spacing`) change the end of the drive: a trial succeeds only once 99% of the flock has stayed inside the goal for one drive time. While the flock is in, the dogs withdraw to $r_s + r_a = 67$ m beyond the farthest sheep, so no sheep reacts to them and the flock grazes; a dog that only stopped would keep the nearest sheep in flight and push it through the goal. While the dogs withdraw they stay within $r_s$ of some sheep for 26 to 29 s, and the flock, which entered at the near edge, keeps walking: 13 to 17 m. At $N \le 50$ the goal of $1.9\,R_f$ (12 to 14 m) is too small for that walk, and below $N = 100$ the 99% share is every sheep, so the first sheep out ends the hold and calls the dogs back. Two more protocols (`dmin_f99_hold_goal`, `dmin_f99_hold_share`) sweep the goal from 1.9 to $3.0\,R_f$ and the share from 99% to 90% at $N \le 100$; a goal of about 16 to 19 m holds a small flock with one dog, and near that threshold extra dogs make holding fail ([report, section 3.10](../report/d_min_report.md)).

## 2. Start layouts and dog starts

### Flock start layouts

HerdSim has four start layouts, from a flock that needs no gathering to one that needs a lot (Figure 2):

![The four starting flock layouts at N = 200](../../docs/figures/fig7_layouts.png)

**Figure 2: The four start layouts.** Shown at $N = 200$ with $D = 4$ dogs, drawn to the same scale; the dashed circle is Strömbom's collect distance $f(N) = r_a N^{2/3}$, and a sheep that starts outside it has to be collected before the flock can be driven.

The scattered layouts are sized by Strömbom's collect distance $L = f(N) = 2\,N^{2/3}$ (with $r_a = 2$), so that "scattered" means the same thing at every $N$: a fixed share of the sheep starts beyond the distance at which the dogs must collect rather than drive.

- `compact`: a Gaussian with $\sigma = 0.5\,R_f$, cut at $3\sigma$. Every sheep starts within $f(N)$, so the dogs start by driving.
- `wide`: a Gaussian with $\sigma = 0.5\,L$, cut at $3\sigma$, so about 14% of the sheep ($e^{-2}$) start beyond $L$ at every $N$.
- `split`: three clusters of the compact density ($\sigma = 0.5\,R_f / \sqrt{3}$ each) with their centres on a circle of radius $L$ around the flock centre.
- `outlier_rich`: 80% of the sheep in a compact core and 20% on a ring between $1.1\,L$ and $1.6\,L$ from it.

### Why the layouts are not ordered by spread

The start spread $S_0$ (the RMS distance of the sheep from the flock centre at the start, read from `max_extent`, the flock's largest RMS radius in a trial) times $N$ is a first guess at how much gathering a layout asks for. Table 3 gives it at 6 drive times under the 99% rule:

**Table 3: Start spread and $D_{\min}$ by layout.**

| Layout | $N$ | Start spread $S_0$ (m) | $S_0 \times N$ | $D_{\min}$ (6 drive times, 99%) |
| :--- | :---: | :---: | :---: | :---: |
| `compact` | 25 | $4.8$ | 119 | 1 |
| `compact` | 100 | $6.7$ | 665 | 1 |
| `compact` | 400 | $8.3$ | 3316 | 1 |
| `wide` | 400 | $74.8$ | 29,931 | 2–3 |
| `outlier_rich` | 400 | $66.2$ | 26,496 | 3 |
| `split` | 400 | $108.8$ | 43,507 | [5] |

At $N = 400$ the scattered layouts have 8 to 13 times the value of `compact`, and they need more dogs. The measure does not order the scattered layouts, though: `outlier_rich` has a smaller spread than `wide` and needs more dogs. Where the strays lie matters as well as how far out they are.  
*Data:* `uv run cli/dmin_tables.py dispersion` on `dmin_m6` for $S_0$; $D_{\min}$ from `dmin_f99_m6`.

### Dog starts

The first dog circle lies $30$ m (`dog_start_gap`) beyond the farthest point any sheep of that layout can start, so no dog starts among the sheep. The gap is less than $r_s = 65$ m, so the sheep nearest the dogs react from the first tick; the gap and the spacing are conventions, and the sensitivity runs test gaps of 15 and 60 m. Dogs on one circle stand $5$ m (`dog_start_spacing`) apart or more; more dogs go on a circle $5$ m farther out. Three start patterns (Figure 3):

![Shepherd release configurations](../../docs/figures/fig8_dog_starts.png)

**Figure 3: Dog starts.** Top: the default arcs for $D = 1$ to $64$ behind an $N = 100$ flock; bottom: arcs, ring and handler start compared at $N = 200$ with $D = 8$ dogs.

- `arcs` (default): half circles behind the flock, on the side away from the goal, with the dogs spread evenly over each; one dog starts on the drive axis when the count is odd.
- `ring`: full circles round the flock, leaving out the cone that holds the goal.
- `handler`: every dog at one point straight behind the flock, as if released from a handler's post.

## 3. Adaptive sequential sampling engine

Running every cell to 200 trials would spend most of the time on cells whose answer is obvious (one dog against 400 scattered sheep at a tight deadline, or twelve dogs on 25 compact sheep).

HerdSim instead runs in rounds and adds trials only where the answer is still open.

Terms used below: a cell is one combination of protocol, layout, $N$ and $D$, and holds its trials, one per seed. A curve is the cells of one layout and $N$ over $D$. A cell is reliable when its success rate is at least $\theta = 0.90$ with 99% confidence. $D_{\mathrm{sat}}$ and $D_{\mathrm{best}}$, which the pruning rule uses, are defined in [section 5](#5-frontier-rules-and-zones).

### The adaptive sampling loop

The diagram shows one run: the flock radius is calibrated once, then rounds repeat until no cell is both undecided and under 200 seeds:

```mermaid
flowchart TB
    proto["Protocol (YAML)"] --> calib["Calibrate the flock radius R_f(N)"]
    calib --> round["Round: plan the seeds each cell still needs"]
    round --> pool["Worker pool runs the trials<br/>(separate random streams per trial)"]
    pool --> rules["Frontier rules:<br/>99% Clopper-Pearson interval (theta = 0.90)<br/>paired bootstrap finish-time comparisons"]
    rules --> more{"Any cell undecided<br/>and under 200 seeds?"}
    more -.->|yes| round
    more -->|no| stop["Stop: write the tables and status.json"]
```

### Stopping early with the 99% Clopper-Pearson interval

Each cell starts with a batch of 10 seeds. After each batch HerdSim computes the exact two-sided 99% Clopper-Pearson interval $[L, U]$ of the success rate:
- Unreliable: $U < 0.90$. Usually decided after 10 to 20 trials; the cell gets no more seeds.
- Reliable: $L \ge 0.90$. The smallest sample that reaches this is 51 straight successes, so the earliest a cell is called reliable is the end of its 60-trial batch.
- Undecided: otherwise; the cell gets another batch of 10, up to 200.

The interval is recomputed after each batch (Figure 4), so the 99% is the confidence of one look, not of the whole sequence; with up to 20 looks per cell the chance of a wrong stop is somewhat above 1%. The report lists this among its limitations.

![Sequential Refinement and Early Stopping](../../docs/figures/fig_adaptive_1_refinement.png)

**Figure 4: Stopping early.** Clear failures stop after 10 to 20 seeds; clear successes once 51 successes in a row are in, at the end of the 60-trial batch; only cells near the threshold continue toward 200.

### Midpoint densification

When two tested counts next to each other on a curve are in different zones (when finish times are not decided, this means one is reliable and the other not; for example $D = 2$ unreliable and $D = 4$ reliable) and differ by more than `refine_min_gap` $= 1$, the next round adds the count halfway between ($D = 3$, Figure 5). $D_{\min}$ is then found without testing every count.

![Adaptive Grid Densification](../../docs/figures/fig_adaptive_2_densification.png)

**Figure 5: Midpoint densification.** A change of zone between $D = 2$ and $D = 4$ adds $D = 3$ to the next round.

### Pruning above saturation

Once $D_{\mathrm{sat}}$ is decided and the next tested count is also saturated, every larger cell is pruned (Figure 6) when at least 90% of its dogs, averaged over ticks and trials, had another dog within 2 m (`prune_overlap`), unless the cell is unreliable or slower than $D_{\mathrm{best}}$. Dogs that close push as one, so the cell repeats the one below it and more seeds would not change its zone. Such cells are marked `pruned` in `frontier_cells.csv`.

![Saturation and Overlap Pruning](../../docs/figures/fig_adaptive_3_pruning.png)

**Figure 6: Pruning.** Above saturation, cells whose dogs overlap (at least 0.90) get no more seeds.

### Paired random streams

Seed $i$ of every cell is `master_seed + i` (for example $2026 + i$). Each trial draws the start positions, the sheep's random choices and the dogs' random choices from three separate streams.

So seed $i$ gives $D = 2$ and $D = 4$ the same start flock and the same sheep noise (Figure 7), and the finish-time difference at that seed is the effect of the team. The paired bootstrap of [section 5](#5-frontier-rules-and-zones) compares these per-seed differences.

![Deterministic Paired Comparisons](../../docs/figures/fig_adaptive_4_paired_seeds.png)

**Figure 7: Paired seeds.** Seed 2026 gives the same start flock at every dog count $D$.

### Saving trials and resuming

Every finished trial is appended to `trials.jsonl` at once. A run can be stopped at any time (`Ctrl+C`) and resumed with the same command without losing trials. A lock on the folder stops a second run from writing to it at the same time. Git keeps a gzip copy, `trials.jsonl.gz`, because the plain file of a large protocol passes GitHub's 100 MB limit; a run writes it when it ends, and a fresh clone unpacks it the first time the folder is opened.

## 4. Why the grid stops where it does

### Flock size

Table 4 gives the range of flock sizes $N$ for each setting and the reason it stops there:

**Table 4: Flock sizes by setting.**

| Setting | Range | Reason |
| :--- | :---: | :--- |
| Main grids and sensitivity | $25$ to $400$ | At $N \le 50$ every layout needs one dog at every deadline, so smaller sizes add nothing. $N = 400$ was the largest calibrated size when the first study ran. |
| Added sizes | $71, 141, 283, 566$ | Steps of $\sqrt{2}$, evenly spaced in $\log N$, so the fit is not dominated by the small sizes. $566 = 400\sqrt{2}$ is the last such step below about $N = 600$, above which the calibrated radius depends on the start layout, so one $R_f(N)$ no longer describes the flock. |
| Kubo model | $25$ to $100$ | The Kubo flock packs to a radius of about $6$ m ($5.9$ to $6.2$) at any $N$, so larger $N$ only makes it denser. |
| Sensing range | $50$ to $200$ | Each dog's sensing range is varied from 15 to 100 m around the sheep's reaction distance ($65$ m). The flock sizes stop at 200, where the collect distance $f(N) = 68$ m already reaches that distance; at larger $N$ the sweep would measure that limit as well as the sensing effect. |
| Gather task (`lama`) | $1$ to $400$ targets, perfect squares | The paper's cells up to $\sqrt{N} = 20$; its axis runs to 25. That range holds the threshold of its Table I ($\sqrt{N} = 8$ to 11) and the square-root rise above it, which are the results compared ([section 6](#6-the-gather-task-lama-and-di-bernardo-2024)). The five larger sizes would about double the run time and add nothing to the check. |
| Large $N$ | $566$ to $3200$ | Tests large flocks with $R_f$ imposed from the density of the $N = 566$ flock, since above about 600 the calibration gives no single radius, and the limit where the paper's drive point passes the sheep's reaction distance ($N \approx 1056$). |

### Team size

- Main grids ($1, 2, 3, 4, 6, 8, 12, 16, 24$): steps of about $1.5\times$, so at least two counts per doubling. $D = 24$ is well above every decided $D_{\min}$ of the main grids.
- Gather task ($1$ to $25$, every count): the paper's grid, at its resolution of one herder.
- Holding with dog spacing (adds $7, 9, 10, 11, 13$): the arc behind the flock holds about $7, 9, 10, 11, 12$ dogs 2 m apart at $N = 25$ to $400$; testing around those counts shows where crowding starts.
- Holding small flocks, goal and share (`dmin_f99_hold_share`, $1, 2, 4, 8, 24$): the question is the goal and the share, so the team grid is thinned; the largest $D$ stays 24 so the dog starts match `dmin_f99_hold`. `dmin_f99_hold_goal` keeps the grid of `dmin_f99_hold` up to 24.

### Seeds per cell (cap of 200)

The cap is 200 because at 200 seeds a cell is decided only if its success rate is at least $0.955$ or at most $0.835$. Doubling to 400 narrows that band only to $0.94$ and $0.86$, for twice the trials. Over the 41 protocols, 411 of 6,845 cells (6.0%) ended open at the cap. A curve whose $D_{\min}$ depends on an open cell is reported as a bracket (for example `2-3`).

### Success rules

- Strict: every sheep inside the goal at the same tick. Large teams often fail on the last sheep: chasing it, they can drive the flock back out of the goal.
- 99%: at least $\lceil 0.99\,N \rceil$ sheep inside at the same tick, so the two rules coincide below $N = 100$; from $N = 100$ one straggler is allowed, and four at $N = 400$.

## 5. Frontier rules and zones

The rules are in [`analysis/frontier.py`](../../analysis/frontier.py); Figure 8 shows the zones along $D$:

![Behavioral zones and frontier classification](../../docs/figures/def_D_zones.png)

**Figure 8: Zones along the dog count $D$.** The zones follow from the reliability of each cell and the paired finish-time comparisons.

### Frontier values

The finish-time values use the working range: the reliable $D$ from $D_{\min}$ up to $D_{\max}$. Two cells are compared on finish time with a paired bootstrap: the per-seed differences of the finish times of their shared successful seeds (at least 5) are resampled 4000 times, and the median difference, relative to the slower cell's median, gives a 99% interval. The cell is faster or slower when the whole interval lies beyond $\pm 5$% (`time_margin`), the same when it lies within, and undecided otherwise. $D_{\mathrm{best}}$ answers which team is as fast as the fastest; $D_{\mathrm{sat}}$ answers from which team more dogs stop helping. Table 5 defines the values.

**Table 5: Frontier values.**

| Value | Definition |
| :--- | :--- |
| $D_{\min}$ | Smallest reliable $D$ ($L \ge 0.90$). |
| $D_{\mathrm{overcrowd}}$ | Smallest $D$ above $D_{\min}$ where it and the next tested $D$ are both unreliable; two in a row, because one unreliable cell can be a sampling dip near the threshold. |
| $D_{\max}$ | Largest reliable $D$ below $D_{\mathrm{overcrowd}}$ (or the largest reliable $D$). |
| $D_{\mathrm{best}}$ | Smallest working $D$ whose paired comparison with the fastest working $D$ is decided same or faster. |
| $D_{\mathrm{sat}}$ | Smallest working $D$ that no larger working $D$ is faster than. |
| $D_{\mathrm{crowd}}$ | Smallest working $D$ above $D_{\mathrm{best}}$ that is slower than $D_{\mathrm{best}}$. |

### Zones

- `too_few`: unreliable, below $D_{\min}$.
- `improving`: reliable, below $D_{\mathrm{sat}}$; more dogs finish sooner.
- `saturated`: reliable, from $D_{\mathrm{sat}}$ up, and not slower than $D_{\mathrm{best}}$.
- `crowded`: reliable, but slower than $D_{\mathrm{best}}$.
- `unreliable_dip`: unreliable, between $D_{\min}$ and $D_{\mathrm{overcrowd}}$.
- `collapse`: unreliable, from $D_{\mathrm{overcrowd}}$ up.
- `recovered`: reliable again above $D_{\mathrm{overcrowd}}$, outside the working range.
- `undecided`: its reliability, or its comparison with $D_{\mathrm{best}}$, is still open.

A reliable cell slower than $D_{\mathrm{best}}$ is `crowded` wherever it lies; `improving` and `saturated` apply only to cells that are not slower.

### How failed trials end

Failed drive trials are split by where the flock ended (`analysis/dispersion_burden.py`):
- Far from the goal: the flock centre ended more than two goal radii from the goal centre.
- Near the goal: the flock centre ended within two goal radii, with the deadline passed or sheep still outside.

Over the six main protocols, 70% to 91% of failed trials end far from the goal ([report section 5.2](../report/d_min_report.md)). The split uses only where the flock ended; it does not say whether more time would have saved a trial.

### Crowding with dogs that take up room

In the main runs the dogs have no size, so two can stand at one point, and on `wide` and `outlier_rich` no cell above $D_{\min}$ was unreliable (on `split` a few are, [section 4 of the report](../report/d_min_report.md)). One setting was tested where extra dogs get in each other's way: dogs that take up room, with no dog allowed within 2 m of another; a dog whose step would end that close does not move that tick. On `outlier_rich` $N = 400$ in the holding task, every team from 9 dogs up is unreliable (success 0.77 at $D = 9$, 0.50 at $D = 16$). The arc behind the flock holds about 12 dogs at that spacing; failure starts before it is full, and a likely reason is that dogs blocked by a neighbour fall out of their arc slots and cannot leave the arc to catch a sheep that breaks away.

## 6. The gather task (Lama and di Bernardo 2024)

Everything above describes the drive task (`drive_to_goal`), used by every Strömbom and Kubo protocol. The `lama` method runs in a second task, `gather`, which reproduces the setting of [Lama & di Bernardo (2024)](https://doi.org/10.1103/PhysRevResearch.6.L032012) (model: [`docs/methods/models.md`](../methods/models.md#lama--di-bernardo-2024-non-cohesive-targets)). A protocol selects it with `task: gather`. Figure 8 of the [models document](../methods/models.md#local-herders-lama_herders) shows the herder rule and one real gather trial from start to end.

The runs cover the paper's grid (40,280 trials). HerdSim gives the thresholds of the paper's Table I to within one step of $\sqrt{N}$, and its maps have the same shape as the paper's Fig. 2; results in [report section 3.14](../report/d_min_report.md).

### Geometry: a disc round the goal

Table 6 lists the geometry of the gather task:

**Table 6: Geometry of the gather task.**

| Quantity | Rule | Source |
| :--- | :--- | :--- |
| Start disc $R$ | `gather_start_radius`, $50$ | The paper's main case (Fig. 2) |
| Goal radius | `gather_goal_fraction` $\times R = R/5 = 10$ | The paper's $r^{\ast} = R/5$ |
| Start (layout `uniform`) | Sheep and dogs uniform over the disc, goal included | The paper's $\Omega_0$ |
| Required share | `success_fraction` $= 0.99$ | The paper's $\chi^{\ast} = 0.99$ |
| Time limit | $166{,}667$ ticks $= 5000$ s at $\Delta t = 0.03$ | The paper's $t_{\max}$ (Fig. S8) |
| Boundary | None | As in the drive task |

The targets do not flock, so there is no driven flock radius to calibrate: the task is sized by $R$. Targets are drawn before herders, so a seed gives the same targets whatever the team size, and cells at different $D$ stay paired as in the drive task.

### When a trial ends and what counts as success

- Success: at least 99% of the targets are inside the goal at a tick when every herder is inside it. This is the paper's stop ("the simulation is stopped when all the herders are inside $\Omega_G$").
- Early end (a failure): the paper stops a trial when every herder is inside the goal. Read literally, that ends a one-herder trial at the first tick whenever the herder starts inside. HerdSim therefore ends a trial early only when every herder is inside and none of them senses a target outside it: the herders have brought in everything they can see, and the rest is lost.
- Otherwise: the trial runs to the time limit.

Failures are labelled `targets_lost` (some targets were out of every herder's sight at the end) or `outnumbered` (every target was seen, but the share was not reached in time). Every row also keeps the share inside at the end (`final_in_goal_fraction`), so the paper's statistic (the mean of that share over the seeds) can be computed next to HerdSim's reliability rule.

### Two statistics

Table 7 sets the paper's statistic beside HerdSim's:

**Table 7: Paper and HerdSim statistics.**

| | Paper | HerdSim |
| :--- | :--- | :--- |
| A team is enough when | the mean share inside at the end, over 50 runs, is at least $0.99$ | the 99% Clopper-Pearson interval of the success rate lies at or above $0.90$ |
| Seeds | 50 per cell | adaptive, 10 to 200 per cell |

Both are read from the same trial rows.

### Metrics recorded every 10 ticks

At $\Delta t = 0.03$ a failing trial runs $166{,}667$ ticks, and the per-tick metrics cost more than the model itself. The gather protocols therefore set `metrics_stride: 10` (one record every $0.3$ s). Success, the early end and the time limit are still checked every tick, and the last tick is always recorded, so the outcome of a trial does not depend on the stride. Only the first-arrival times (the first tick at which a given share of the targets is inside) are read from the recorded ticks, so they are never earlier than the exact time and can be later (a share reached and lost again between two records is missed).

### Protocols

Table 8 lists the gather protocols:

**Table 8: Gather protocols.**

| Protocol | Sensing radius $\xi$ | Paper figure |
| :--- | :---: | :--- |
| `lama_r50` | $10$ | Fig. 2b, Table I |
| `lama_r50_inf` | infinite | Fig. 2a |
