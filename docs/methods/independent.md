# Independent paper shepherds: `independent`

This baseline asks what a team gets from the paper's rule alone. Every dog runs Strömbom's single-dog rule on its own: the collect/drive decision on the whole flock, the sheep farthest from the flock centre or the drive point as target, and Strömbom's step, noise and stop rule. With no team layer, every dog sees the same flock and makes the same choice, so the controller is one dog with $D$ copies (Figure 1). The comparison with the team rule is in [report, section 3.9](../report/part4_coordination.md#39-rq9-which-part-of-the-team-rule-matters).

![Team rule and independent dogs collecting and driving](../figures/fig_independent.png)

**Figure 1: The team rule against `independent` ($N = 100, D = 4$).** Without a team layer the dogs all make the same choice, both when collecting and when driving.

- Marks: as in Figure 1 of [the team rule](strombom_multi.md#coordinated-team-architecture-strombom_multi); arrows are dashed for `independent`.
- Left: the team rule; the 4 dogs collect 4 different outliers in parallel.
- Middle: `independent`, collecting; all 4 chase the same outlier while the others wait.
- Right: `independent`, driving; all dogs go to $P_d$ instead of the arc (dotted green), so they crowd and leave the flock's sides open.

Animation 1 runs the team rule and both baselines on one start flock.

![Animation of three dog rules on one start flock](../gifs/controllers.gif)

**Animation 1: Three dog rules on the same start flock (`wide`, $N = 400$, $D = 4$, seed 0, 99% rule, 6 drive times).** Only the team rule brings the flock in; both baselines fail when time is up.

- Marks: blue dots are sheep, orange triangles dogs, the green circle the goal; the bottom-left text gives the time and the sheep outside the goal.
- Left: the team rule gives each dog its own outlier while collecting, then drives from an arc, and succeeds at 569 s.
- Middle: the `independent` dogs all make the same choice, and once they meet they move as one, so a single triangle shows.
- Right: every FAT dog aims at the sheep farthest from the goal; the bulk of the flock gathers, but outliers stay far out to the end.

## References

1. Strömbom, D., et al. (2014). *Solving the shepherding problem: heuristics for herding autonomous, interacting agents*. Journal of the Royal Society Interface, 11(100), 20140719. [DOI: 10.1098/rsif.2014.0719](https://doi.org/10.1098/rsif.2014.0719)
