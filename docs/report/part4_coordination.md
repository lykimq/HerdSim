# Coordination and what the dogs see

Part 4 of the HerdSim report on team size. The [overview](d_min_report.md) holds the abstract, the research questions, the [decision rules](d_min_report.md#2-decision-rules-and-setup) that define $D_{\min}$, its brackets and lower bounds, the [start layouts and dog rules](d_min_report.md#22-start-layouts-dog-rules-and-protocols), the discussion and the [references](d_min_report.md#references). Terms are defined in the [glossary](../glossary.md).

The three sections of this part change the dogs and keep the sheep. [Section 3.6](#36-rq6-do-dogs-without-a-team-rule-reach-a-finite-d_min) runs dogs without coordination, [section 3.9](#39-rq9-which-part-of-the-team-rule-matters) dogs with only part of the team rule, and [section 3.12](#312-rq12-what-a-dog-sees-and-sharing-it) dogs that see only part of the flock.

## 3.6 RQ6: Do dogs without a team rule reach a finite D_min?

The question here is whether a team needs its dogs to coordinate at all. The team rule `strombom_multi` has two parts. The first is Strömbom's collect/drive switch: while any sheep is farther than the [collect distance](../glossary.md#sheep-models-and-dog-rules) from the flock centre (an outlier), the dogs collect outliers, and otherwise they drive the flock. The second is the team layer. While the dogs collect, it gives each of the $D$ farthest outliers its own dog, matched for the least total walk. This is the assignment problem often solved by the Hungarian method; the code solves it with scipy's `linear_sum_assignment`, a Jonker-Volgenant variant. When there are fewer outliers than dogs, the dogs left over drive the core of the flock from an arc behind it. While the dogs drive, the team layer spreads them all on an arc behind the flock in angular order. FAT (farthest-agent targeting) is a baseline with neither part: every dog goes behind the sheep farthest from the goal.

FAT dogs do not coordinate at all, and on large flocks FAT has no reliable team on the grid (up to 24 dogs). From $N = 200$ it has no reliable team on any [scattered layout](../glossary.md#start-layouts-and-dog-starts), and adding dogs does not make it reliable (item 1). Its dogs end up close together behind the same sheep (item 2). This holds for FAT only. The independent shepherds of [section 3.9](#39-rq9-which-part-of-the-team-rule-matters) have no team layer either, and they are reliable at $N = 200$ on every layout.

1. FAT fails on large flocks: it is reliable on small flocks ($N \le 100$). At $N \ge 200$ it has no reliable team on any scattered layout, under either rule. On compact $N = 400$, where the team rule needs one dog, FAT has none under the strict rule. Under the 99% rule it has only the lower bound [12]: 12 dogs are still undecided at 174 of 200 trials. Adding dogs does not make FAT reliable, although the largest team does better than one dog in some cells. On compact $N = 400$ under the strict rule, success goes from 3 of 10 trials with one dog to 11 of 20 with 24. On `split` $N = 200$ under the 99% rule it goes from 12 of 20 to 88 of 110, and the median finish time falls from 742.5 s to 305.5 s (Figure 1).

2. FAT dogs bunch behind one sheep: every dog sees every sheep and picks by the same rule, so all $D$ dogs chase the same sheep. The measure is the share of dogs with another dog within 2 m, averaged over the ticks of a trial (the stored column `mean_dog_overlap` in `trials.csv`; no `dmin_tables.py` verb reports it). In the strict run `dmin_fat` (6 drive times), for teams of two or more, the median of that share over trials is, at $N = 200$ and $N = 400$:

   - `compact`: 0.86 and 0.96.
   - `split`: 0.79 and 0.79.
   - `wide`: 0.63 and 0.17.
   - `outlier_rich`: 0.40 and 0.19.

   Pooling both sizes gives 0.86 on `compact`, 0.79 on `split`, 0.46 on `wide` and 0.30 on `outlier_rich`. The pool weights each cell by the trials the campaign gave it, so on `compact` it is mostly $N = 200$ (1240 of 1330 trials). The 99% run `dmin_f99_fat` gives pooled values of 0.92, 0.79, 0.45 and 0.30. The flock is less spread with 24 FAT dogs than with one. The stored measure is the flock's extent (RMS distance of the sheep to the flock centre) averaged over a trial, `mean_extent`. In `dmin_fat` its median over trials on `wide` $N = 400$ is 64.4 m with one dog and 27.6 m with 24, and on `outlier_rich` $N = 400$ it is 61.9 m and 36.5 m.

   The independent shepherds of [section 3.9](#39-rq9-which-part-of-the-team-rule-matters) also have no team layer. They keep Strömbom's collect/drive switch, though, and they reach a finite $D_{\min}$ up to $N = 200$. FAT may fail because it has neither the team layer nor the switch; no run gave FAT the switch alone, so we have not tested it.

Table 1 compares FAT with `strombom_multi` at 6 [drive times](../glossary.md#the-drive-task). Each cell gives FAT's $D_{\min}$ under the strict rule, then under the [99% rule](../glossary.md#success-and-reliability), with `strombom_multi` in parentheses:

**Table 1: FAT against `strombom_multi` at 6 drive times, strict / 99% rule.**

| Layout | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `compact` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / [12] (1 / 1) |
| `wide` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (3 / 2) | none / none ([9] / 2-3) |
| `split` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (none / [1]) | none / none (none / [5]) |
| `outlier_rich` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 2 / 2 (3 / 2) | none / none ([12] / 2-3) | none / none (none / 3) |

*Data:* [results_tables.md: FAT dog rule, deadline 6](results_tables.md#fat-dog-rule-deadline-6-strict-then-99-percent) (`dmin_fat`, `dmin_f99_fat`); `strombom_multi` in [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success) and [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

![FAT against the coordinated team rule](../figures/fig26_fat.png)

**Figure 1: Success against team size for `strombom_multi` and FAT at 6 drive times, $N = 200$ and 400.** FAT reaches $\theta = 0.90$ at no team size in any panel; its highest success rate is 0.87 (174 of 200 trials, 12 dogs on `compact` $N = 400$, 99% rule). Under the 99% rule `strombom_multi` becomes reliable on `wide` and `outlier_rich`. Under the strict rule it does so only on `wide` $N = 200$, and has the lower bounds [9] on `wide` $N = 400$ and [12] on `outlier_rich` $N = 200$.

- Marks: blue is `strombom_multi`, orange FAT. Solid lines are the strict rule, with circles for `strombom_multi` and up-pointing triangles for FAT. Dashed lines are the 99% rule, with squares for `strombom_multi` and down-pointing triangles for FAT. The dotted line is $\theta = 0.90$. Each marker is one cell. A hollow marker is a cell with fewer than 30 trials; it was decided early by the same 99% Clopper-Pearson rule as every other cell ([section 2.1](d_min_report.md#21-when-a-team-is-reliable)), so its decision holds, but its plotted rate rests on few trials.
- Panels: `compact` $N = 400$, `wide` $N = 200$ and 400, `outlier_rich` $N = 200$, and `split` $N = 200$. FAT stays below about 0.55 on `wide` and `outlier_rich`, and below 0.9 on `compact` $N = 400$ and `split` $N = 200$.

*Data:* `results/dmin_fat`, `dmin_f99_fat`, `dmin_m6` and `dmin_f99_m6`.

Animation 7 in [models](../methods/models.md#independent-paper-shepherds-independent) replays the team rule, independent dogs and FAT on one start flock of 400. Only the team rule brings it in.

## 3.9 RQ9: Which part of the team rule matters?

[Section 3.6](#36-rq6-do-dogs-without-a-team-rule-reach-a-finite-d_min) removed both parts of the team rule at once. This section asks which of the two a team needs. The answer depends on flock size: dogs with the collect/drive switch alone are reliable up to $N = 200$, and on `wide` and `outlier_rich` the team layer is needed at $N = 400$ (items 1 and 2, Table 2). On `split` $N = 200$ the order reverses (item 2).

To separate the two parts, `dmin_f99_indep` runs a team of independent shepherds. Each dog runs Strömbom's single-dog rule on the whole flock, so it has the switch but no assignment and no arc.

1. Independent shepherds are reliable up to $N = 200$: they have a reliable team on every scattered layout up to $N = 200$. At $N = 200$, where FAT has none, they need 2-3 dogs on `wide`, 3 on `outlier_rich` and 1-3 on `split`, where the team rule has only the lower bound [1]. FAT differs from them in the sheep it aims at as well as in lacking the switch, so the gain cannot be put on the switch alone. This may be because switching to driving once the flock is gathered keeps it together, even when the dogs chase the same outlier; we have not tested it.

2. On `wide` and `outlier_rich` at $N = 400$ the team layer is needed: there independent shepherds have no reliable team up to 24 dogs, while the team rule needs 2-3 dogs on `wide` and 3 on `outlier_rich`. This may be because, without assignment, the dogs keep going after the same sheep while other parts of a large flock spread; we have not tested it. The other two layouts at $N = 400$ do not show this. On `compact` independent shepherds are reliable from one dog (60 of 60 trials). On `split` they have no reliable team, but the team rule has none either, only the lower bound [5].

   On `split` $N = 200$ the order reverses. Independent shepherds have $D_{\min}$ in the bracket 1-3: one and two dogs are still undecided (183 of 200 and 188 of 200 trials), and every team from 3 to 24 dogs is reliable. The team rule has only the lower bound [1]. Its one-dog cell is the same 183 of 200 trials as for independent shepherds, since with one dog the two rules are the same. The reversal is clear from 4 dogs up, where independent shepherds are reliable and the team rule is not ([section 4.1](part5_failures.md#41-why-more-dogs-do-not-help-on-split)).

3. In the Kubo model more dogs keep helping, with diminishing returns: with Kubo sheep (`dmin_f99_kubo`, 99% rule, compact starts only, a fixed 500 s limit), one dog is enough on compact flocks of 25 to 100. The 500 s limit is about 31 times the 16 s a sheep at the Kubo speed cap of 5 m/s needs for the 80 m drive. In the Strömbom model a sheep that reacts to a dog always moves at `sheep_speed` = 1 m/s, and a grazing sheep stays put or, with probability 0.05 per tick, takes one step. Kubo sheep move faster under a stronger push, up to the 5 m/s cap, so more dogs shorten the drive. Kubo et al. (2022) do not state that cap; HerdSim takes it from a public MATLAB port of the method. At $N = 100$ the median finish time falls from 115 s with one dog to 76.3 s with two, 29 s with ten and 25 s with 24. Ten dogs already give 95% of the gain of 24. Under the strict rule (`dmin_kubo`, up to 10 dogs) the median does not fall at every step. At $N = 100$ it is 115 s with one dog and with two, and at $N = 25$ it rises from 66.8 s with two dogs to 69.1 s with three. [$D_{\mathrm{sat}}$](../glossary.md#team-sizes), the smallest working team that no larger working team beats on finish time by more than 5% with 99% confidence, is still open. It is at least 16 or 17 dogs (16-24 at $N = 25$ and 100, 17-24 at 50).

Table 2 compares the three rules at 6 drive times (99% rule):

**Table 2: $D_{\min}$ of the team rule, independent shepherds and FAT at 6 drive times, 99% rule.**

| `strombom_multi` / `independent` / `fat` | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: |
| `wide` | 2 / 2-3 / none | 2-3 / none / none |
| `outlier_rich` | 2-3 / 3 / none | 3 / none / none |
| `split` | [1] / 1-3 / none | [5] / none / none |

*Data:* [results_tables.md: Methods at 99 percent, 6 drive times](results_tables.md#methods-at-99-percent-6-drive-times-team-rule-independent-paper-shepherds-fat) and [results_tables.md: Kubo, compact, D to 24](results_tables.md#kubo-compact-d-to-24-99-percent); Kubo finish times from `results/dmin_f99_kubo` and `results/dmin_kubo` (`uv run cli/dmin_tables.py curve dmin_kubo dmin_f99_kubo --layout compact --n 25`, and `--n 100`).

## 3.12 RQ12: What a dog sees, and sharing it

Real dogs, robots and drones do not see the whole field. This section asks how many more dogs a team needs when each one sees only part of the flock, and whether sharing what they see makes up for it. Each dog sees only the sheep within a sensing range of 15, 30, 45, 65 or 100 m. The dogs share what they see in one of three ways: not at all (`none`), with the dogs in range (`neighbour`), or with the whole team (`shared`, so the team plans once on every sheep any dog sees). The runs use the 99% rule at 6 drive times.

On `wide` $N = 200$ a range of 30 to 65 m costs about one dog. At 65 m, sharing with the whole team brings $D_{\min}$ back to its full-sight value. At 15 m far more dogs are needed (items 1 to 3, Figure 2). On `split` $N = 200$ the result reverses (item 3).

1. A range of 30 to 65 m costs about one dog: on `wide` $N = 200$, dogs that see everything need 2. With a range of 30 to 65 m they need 3 (3-4 at 45 m). On flocks of 100 or fewer a range of 30 m or more costs nothing (Figure 2).

2. At 15 m far more dogs are needed: with a range of 15 m on `wide`, no team up to 16 is reliable at $N = 50$, and at $N = 100$ at least 6 dogs are needed. This may be because the dogs lose sight of the outer sheep once the range is shorter than the gaps between outliers; we have not tested it, and we have not measured those gaps.

3. Sharing with the whole team brings $D_{\min}$ back to full sight on `wide`: at 65 m on `wide` $N = 200$, dogs that do not share need 3. Sharing with the whole team brings $D_{\min}$ back to 2, as with full sight. With two dogs the cell succeeds in 3 of 10 trials without sharing (99% interval 0.04-0.74) and in 88 of 90 with sharing (0.90-1.00; Animation 1). Sharing only with the dogs in range does not help (still 3). This may be because a dog far from an outlier gets no word of it from the dogs in its range; we have not tested it.

   On `split` $N = 200$ the order reverses. Dogs that see everything have no reliable team ([1], a lower bound). Dogs that see 30 to 65 m and do not share succeed in 60 of 60 trials at every team tested from 3 to 16 dogs. Sharing with the whole team is reliable with 3 dogs, but no team from 4 up is reliable ([section 3.7](part3_beyond_dmin.md#37-rq7-beyond-d_min-enough-dogs-cost-and-pressure-on-the-flock)). This may be related to the `split` failures of [section 4.1](part5_failures.md#41-why-more-dogs-do-not-help-on-split), where collecting dogs that plan on the whole flock crowd one cluster; we have not tested it.

![D_min against sensing range, and sharing](../figures/fig37_view.png)

**Figure 2: $D_{\min}$ against sensing range, and the effect of sharing (99% rule, 6 drive times).** At 15 m `wide` needs at least 6 dogs at $N = 100$ and 7 at $N = 200$; on `wide` at a range of 65 m, sharing what each dog sees with the whole team matches full sight.

- Left: $D_{\min}$ against the range for `wide` (circles) and `split` (squares) at $N = 100$ (faded) and $N = 200$, with a bar for a bracket and a hollow triangle for a lower bound ([section 2.1](d_min_report.md#21-when-a-team-is-reliable)); each layout and $N$ is shifted sideways a little. The dashed line marks 65 m, the distance at which a sheep reacts.
- Right: success against $D$ on `wide` $N = 200$ at a range of 65 m, with no sharing (dotted blue), sharing with dogs in range (dashed blue), sharing with the whole team (solid blue) and full sight (solid black). The dashed black line is $\theta = 0.90$. Hollow markers are cells with fewer than 30 trials, decided early by the same 99% rule.

*Data:* [results_tables.md: Views: sensing range](results_tables.md#views-sensing-range-no-sharing-base-row--range-0-global) and [results_tables.md: Views: sharing at range 65](results_tables.md#views-sharing-at-range-65-beside-the-no-sharing-rows-of-dmin_f99_view_range).

![Animation of two dogs with a 65 m range, without and with sharing](../gifs/sight_sharing.gif)

**Animation 1: Two dogs that see 65 m, without and with sharing, replayed (`wide`, $N = 200$, $D = 2$, seed 0, 99% rule, 6 drive times).** Sharing what each dog sees turns a failed trial into a success. Each replay reproduces its stored trial (`dmin_f99_view_range`, `dmin_f99_view_comm`).

- Marks: dashed circles are each dog's sensing range; hollow dots are sheep that no dog sees.
- Left: without sharing each dog plans on its own view. The two dogs end up on either side of a long, thin flock, and a few outliers at its ends stay unseen. The trial runs out of time at 817 s.
- Right: with sharing the team plans once on every sheep either dog sees, gathers the flock and brings it in at 275 s.
