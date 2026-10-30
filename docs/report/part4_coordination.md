# Coordination and what the dogs see

Part 4 of the HerdSim report on team size. The [overview](d_min_report.md) holds the abstract, the research questions, the [decision rules](d_min_report.md#2-decision-rules-and-setup) that define $D_{\min}$, its brackets and lower bounds, the [start layouts and dog rules](d_min_report.md#22-start-layouts-dog-rules-and-protocols), the discussion and the [references](d_min_report.md#references). Terms are defined in the [glossary](../glossary.md).

The three sections of this part change the dogs and keep the sheep. [Section 3.6](#36-rq6-do-dogs-without-a-team-rule-reach-a-finite-d_min) runs dogs without coordination, [section 3.9](#39-rq9-which-part-of-the-team-rule-matters) dogs with only part of the team rule, and [section 3.12](#312-rq12-what-a-dog-sees-and-sharing-it) dogs that see only part of the flock.

## 3.6 RQ6: Do dogs without a team rule reach a finite D_min?

Dogs that do not coordinate and all go behind the sheep farthest from the goal ([FAT](../methods/models.md#uncoordinated-greedy-baseline-fat), farthest-agent targeting) have no reliable team up to 24 dogs on [scattered flocks](../glossary.md#start-layouts-and-dog-starts) from $N = 200$. The team rule [`strombom_multi`](../methods/models.md#coordinated-team-architecture-strombom_multi) has two parts that FAT lacks: Strömbom's collect/drive switch (collect sheep farther than the [collect distance](../glossary.md#sheep-models-and-dog-rules) from the flock centre, otherwise drive) and a team layer that gives each of the $D$ farthest outliers its own dog and spreads the dogs on an arc behind the flock.

1. FAT is reliable on small flocks: one dog at $N \le 100$ on every layout, except `outlier_rich` $N = 100$, where it needs 2. At $N \ge 200$ it has no reliable team on any scattered layout under either the strict or the [99% rule](../glossary.md#success-and-reliability), and adding dogs does not make it reliable (Table 1). On compact $N = 400$, where the team rule needs one dog, FAT has none under the strict rule and only the lower bound [12] under the 99% rule (12 dogs still undecided at 174 of 200 trials). The largest team does better than one dog in some cells without becoming reliable: on compact $N = 400$ under the strict rule success goes from 3 of 10 trials with one dog to 11 of 20 with 24, and on `split` $N = 200$ under the 99% rule from 12 of 20 to 88 of 110, with the median finish time falling from 742.5 s to 305.5 s (Figure 1).

2. FAT dogs bunch behind one sheep on `compact` and `split` but much less on `wide` and `outlier_rich` at $N = 400$. Every FAT dog sees every sheep and picks by the same rule, which may be why they bunch; we have not tested it. In the strict run `dmin_fat` (6 [drive times](../glossary.md#the-drive-task), teams of two or more), the median share of dogs with another dog within 2 m (stored column `mean_dog_overlap`, averaged over the ticks of a trial; no `dmin_tables.py` verb reports it) is, at $N = 200$ and 400, 0.86 and 0.96 on `compact`, 0.79 and 0.79 on `split`, 0.63 and 0.17 on `wide`, and 0.40 and 0.19 on `outlier_rich`; pooled over both sizes it is 0.86, 0.79, 0.46 and 0.30 (the `compact` pool is mostly $N = 200$, 1240 of 1330 trials).

   The flock is less spread with 24 FAT dogs than with one: the median `mean_extent` (RMS distance of the sheep to the flock centre, averaged over a trial) in `dmin_fat` is 64.4 m with one dog and 27.6 m with 24 on `wide` $N = 400$, and 61.9 m and 36.5 m on `outlier_rich` $N = 400$.

The independent shepherds of [section 3.9](#39-rq9-which-part-of-the-team-rule-matters) also lack the team layer but keep the switch, and they reach a finite $D_{\min}$ up to $N = 200$. FAT may fail because it has neither the team layer nor the switch; no run gave FAT the switch alone, so we have not tested it.

Table 1 gives FAT's $D_{\min}$ under the strict rule, then under the 99% rule, with `strombom_multi` in parentheses:

**Table 1: FAT against `strombom_multi` at 6 drive times, strict / 99% rule.**

| Layout | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `compact` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / [12] (1 / 1) |
| `wide` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (3 / 2) | none / none ([9] / 2-3) |
| `split` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (none / [1]) | none / none (none / [5]) |
| `outlier_rich` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 2 / 2 (3 / 2) | none / none ([12] / 2-3) | none / none (none / 3) |

*Data:* [results_tables.md: FAT dog rule, deadline 6](results_tables.md#fat-dog-rule-deadline-6-strict-then-99-percent) (`dmin_fat`, `dmin_f99_fat`); `strombom_multi` in [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success) and [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

![FAT against the coordinated team rule](../figures/fig26_fat.png)

**Figure 1: Success against team size for `strombom_multi` and FAT at 6 drive times, $N = 200$ and 400.** FAT reaches $\theta = 0.90$ at no team size in any panel; its highest success rate is 0.87 (174 of 200 trials, 12 dogs on `compact` $N = 400$, 99% rule). Under the 99% rule `strombom_multi` becomes reliable on `wide` and `outlier_rich`. Under the strict rule it is reliable on `compact` $N = 400$ and `wide` $N = 200$ only, and has the lower bounds [9] on `wide` $N = 400$ and [12] on `outlier_rich` $N = 200$.

- Marks: blue is `strombom_multi`, orange FAT. Solid lines are the strict rule, with circles for `strombom_multi` and up-pointing triangles for FAT. Dashed lines are the 99% rule, with squares for `strombom_multi` and down-pointing triangles for FAT. The dotted line is $\theta = 0.90$. Each marker is one cell. A hollow marker is a cell with fewer than 30 trials; it was decided early by the same 99% Clopper-Pearson rule as every other cell ([section 2.1](d_min_report.md#21-when-a-team-is-reliable)), so its decision holds, but its plotted rate rests on few trials.
- Panels: `compact` $N = 400$, `wide` $N = 200$ and 400, `outlier_rich` $N = 200$, and `split` $N = 200$. FAT stays below about 0.55 on `wide` and `outlier_rich`, and below 0.9 on `compact` $N = 400$ and `split` $N = 200$.

*Data:* `results/dmin_fat`, `dmin_f99_fat`, `dmin_m6` and `dmin_f99_m6`.

Animation 7 in [models](../methods/models.md#independent-paper-shepherds-independent) replays the team rule, independent dogs and FAT on one start flock of 400. Only the team rule brings it in.

## 3.9 RQ9: Which part of the team rule matters?

Dogs with the collect/drive switch alone are reliable up to $N = 200$; on `wide` and `outlier_rich` the team layer is needed at $N = 400$, and on `split` $N = 200$ independent shepherds do better than the team rule (Table 2). The run `dmin_f99_indep` uses [independent shepherds](../methods/models.md#independent-paper-shepherds-independent): each dog runs Strömbom's single-dog rule on the whole flock, so it has the switch but no assignment and no arc.

1. Independent shepherds have a reliable team on every scattered layout up to $N = 200$. At $N = 200$, where FAT has none, they need 2-3 dogs on `wide`, 3 on `outlier_rich` and 1-3 on `split`, where the team rule has only the lower bound [1]. FAT also differs from them in the sheep it aims at, so the gain cannot be put on the switch alone. This may be because switching to driving once the flock is gathered keeps it together, even when the dogs chase the same outlier; we have not tested it.

2. At $N = 400$ on `wide` and `outlier_rich`, independent shepherds have no reliable team up to 24 dogs, while the team rule needs 2-3 and 3. This may be because, without assignment, the dogs keep going after the same sheep while other parts of a large flock spread; we have not tested it.

   On `compact` $N = 400$ independent shepherds are reliable from one dog (60 of 60 trials); on `split` $N = 400$ neither rule has a reliable team (the team rule has the lower bound [5]).

   On `split` $N = 200$ independent shepherds have $D_{\min}$ 1-3: one and two dogs are undecided (183 of 200 and 188 of 200 trials) and every team from 3 to 24 is reliable. The team rule has only [1]; its one-dog cell is the same 183 of 200, since with one dog the two rules are the same. From 4 dogs up independent shepherds are reliable and the team rule is not ([section 4.1](part5_failures.md#41-why-more-dogs-do-not-help-on-split)).

3. With Kubo sheep more dogs keep helping, with diminishing returns. A reacting Strömbom sheep always moves at 1 m/s, while a Kubo sheep moves faster under a stronger push, up to a cap of 5 m/s that Kubo et al. (2022) do not state; HerdSim takes it from a public MATLAB port of the method.

   In `dmin_f99_kubo` (99% rule, compact starts only, a fixed 500 s limit, about 31 times the 16 s a sheep at the cap needs for the 80 m drive), one dog is enough on compact flocks of 25 to 100. At $N = 100$ the median finish time falls from 115 s with one dog to 76.3 s with two, 29 s with ten and 25 s with 24, so ten dogs give 95% of the gain of 24.

   Under the strict rule (`dmin_kubo`, up to 10 dogs) the median does not fall at every step: at $N = 100$ it is 115 s with one dog and with two, and at $N = 25$ it rises from 66.8 s with two dogs to 69.1 s with three. [$D_{\mathrm{sat}}$](../glossary.md#team-sizes) is still open, at least 16 or 17 dogs (16-24 at $N = 25$ and 100, 17-24 at 50).

**Table 2: $D_{\min}$ of the team rule, independent shepherds and FAT at 6 drive times, 99% rule.**

| `strombom_multi` / `independent` / `fat` | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: |
| `wide` | 2 / 2-3 / none | 2-3 / none / none |
| `outlier_rich` | 2-3 / 3 / none | 3 / none / none |
| `split` | [1] / 1-3 / none | [5] / none / none |

*Data:* [results_tables.md: Methods at 99 percent, 6 drive times](results_tables.md#methods-at-99-percent-6-drive-times-team-rule-independent-paper-shepherds-fat) and [results_tables.md: Kubo, compact, D to 24](results_tables.md#kubo-compact-d-to-24-99-percent); Kubo finish times from `results/dmin_f99_kubo` and `results/dmin_kubo` (`uv run cli/dmin_tables.py curve dmin_kubo dmin_f99_kubo --layout compact --n 25`, and `--n 100`).

## 3.12 RQ12: What a dog sees, and sharing it

Real dogs, robots and drones do not see the whole field. On `wide` $N = 200$ a sensing range of 30 to 65 m costs one or two dogs (one at 30 and 65 m, one or two at 45 m), and at 65 m sharing what the dogs see with the whole team brings $D_{\min}$ back to its full-sight value; at 15 m far more dogs are needed. On `split` $N = 200$ sharing does not help: dogs that do not share are reliable from 3 dogs at 30 to 65 m, and with sharing to the whole team no team of 4 or more is reliable (item 3). In these runs (99% rule, 6 drive times) each dog sees only the sheep within 15, 30, 45, 65 or 100 m. The range sweep runs without sharing (`none`). The sharing runs fix the range at 65 m and share what a dog sees with the dogs in range (`neighbour`) or with the whole team (`shared`, so the team plans once on every sheep any dog sees).

1. On `wide` $N = 200$, dogs that see everything need 2; with a range of 30 to 65 m they need 3 (3-4 at 45 m); at 100 m they need 2-3. On flocks of 100 or fewer a range of 30 m or more costs nothing (Figure 2).

2. With a range of 15 m on `wide`, no team up to 16 is reliable at $N = 50$, and at least 6 dogs are needed at $N = 100$ and 7 at $N = 200$. This may be because the dogs lose sight of the outer sheep once the range is shorter than the gaps between outliers; we have not tested it, and we have not measured those gaps.

3. At 65 m on `wide` $N = 200$, dogs that do not share need 3, and sharing with the whole team brings $D_{\min}$ back to 2. With two dogs the cell succeeds in 3 of 10 trials without sharing (99% interval 0.04-0.74) and in 88 of 90 with sharing (0.90-1.00; Animation 1). Sharing only with the dogs in range does not help (still 3). This may be because a dog far from an outlier gets no word of it from the dogs in its range; we have not tested it.

   On `split` $N = 200$ dogs that see everything have no reliable team ([1], a lower bound). Dogs that see 30 to 65 m and do not share succeed in 60 of 60 trials at every team tested from 3 to 16 dogs. At 15 m no team from 3 to 16 dogs is decided reliable ([3]), and at 100 m teams are reliable from 5 dogs ($D_{\min}$ 1-5). Sharing with the whole team is reliable with 3 dogs, but no team from 4 up is reliable: 4, 6, 8, 9, 13, 14 and 16 dogs are decided unreliable, and 10 and 12 dogs are undecided (170 and 171 of 200) ([section 3.7](part3_beyond_dmin.md#37-rq7-beyond-d_min-enough-dogs-cost-and-pressure-on-the-flock)). This may be related to the `split` failures of [section 4.1](part5_failures.md#41-why-more-dogs-do-not-help-on-split), where collecting dogs that plan on the whole flock crowd one cluster; we have not tested it.

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
