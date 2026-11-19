# Strombom et al. (2014) sheep model

This doc describes how each sheep moves in HerdSim: the rule of [Strombom et al. (2014)](https://doi.org/10.1098/rsif.2014.0719), plus one HerdSim extension for several dogs. The dog rules are in [`strombom_multi`](strombom_multi.md), [`independent`](independent.md) and [`fat`](fat.md).

Each tick lasts $\Delta t = 1$ s. All sheep move first, then the dogs. A sheep's behaviour depends on whether any dog is closer than the detection radius $r_s = 65$ m:

- Reacting: a dog is closer than $r_s$. The sheep picks a heading from five pulls (its last direction, the flock, its neighbours, the dogs, noise) and walks $\delta = 1$ m along it.
- Grazing: no dog is closer than $r_s$. The sheep mostly stands still and takes a random 1 m step 5% of the time.

![Sheep i, its neighbours and a dog, and the five heading vectors](../figures/fig_sheep_forces.png)

**Figure 1: The sheep rule of Strombom et al. (2014).** A reacting sheep adds five weighted unit vectors to get its new heading $\mathbf{H}_i'$.

- Marks: the black dot is the focal sheep $i$, blue dots are flock-mates, the red dot is a neighbour closer than $r_a = 2$ m, the green `+` is the local centre of mass $\mathrm{LCM}_i$, and the orange triangle is a dog inside $r_s = 65$ m.
- Left: the zones around sheep $i$ (the $r_a = 2$ m zone is drawn 3x larger so it can be seen, and the detection radius $r_s = 65$ m).
- Right: the five weighted vectors and their sum $\mathbf{H}_i'$.

## Reacting heading and step

A reacting sheep $i$ at position $\mathbf{x}_i^t$ adds five unit vectors, each with its own weight:

$$
\mathbf{H}_i' = h\,\mathbf{H}_i + c\,\mathbf{C}_i + \rho_a\,\mathbf{R}_{a,i} + \rho_s\,\mathbf{R}_{s,i} + e\,\boldsymbol{\epsilon}_i
$$

It then walks $\delta = 1$ m in the direction of that sum. Only the direction of $\mathbf{H}_i'$ is used, so a reacting sheep always walks 1 m per tick, however many dogs push it:

$$
\mathbf{x}_i^{t+1} = \mathbf{x}_i^t + \delta\,\frac{\mathbf{H}_i'}{\lVert \mathbf{H}_i' \rVert}
$$

The five vectors, from the strongest weight to the weakest:

- Keeping space $\mathbf{R}_{a,i}$ (weight $\rho_a = 2.0$): points away from all neighbours closer than $r_a = 2$ m. These neighbours form the set $\mathcal{N}_a(i) = \{j \ne i \mid \lVert \mathbf{x}_i - \mathbf{x}_j \rVert < r_a\}$. The vector is the normalized sum of the unit vectors pointing away from each of them, or $\mathbf{0}$ if the set is empty.
- Attraction to the flock $\mathbf{C}_i$ (weight $c = 1.05$): points toward the local centre of mass $\mathrm{LCM}_i$, the mean position of the $n$ nearest other sheep (described below).
- Running from the dogs $\mathbf{R}_{s,i}$ (weight $\rho_s = 1.0$): points away from the dogs closer than $r_s = 65$ m (see [multi-dog push blending](#multi-dog-push-blending-herdsim-extension)).
- Previous heading $\mathbf{H}_i$ (weight $h = 0.5$): the direction of the sheep's last step, or $\mathbf{0}$ if it stood still on the last tick. It smooths the path.
- Noise $\boldsymbol{\epsilon}_i$ (weight $e = 0.3$): a unit vector at a random angle drawn uniformly from $[0, 2\pi)$.

The vector that keeps space is written out because it is the one with the highest weight:

$$
\mathbf{R}_{a,i} = \frac{\sum_{j \in \mathcal{N}_a(i)} \widehat{\mathbf{x}_i - \mathbf{x}_j}}{\left\lVert \sum_{j \in \mathcal{N}_a(i)} \widehat{\mathbf{x}_i - \mathbf{x}_j} \right\rVert}
$$

Here $\widehat{\mathbf{v}}$ is the unit vector $\mathbf{v} / \lVert \mathbf{v} \rVert$.

### Attraction to the flock

The vector $\mathbf{C}_i$ points from the sheep to the mean position $\mathrm{LCM}_i$ of its $n$ nearest other sheep, written $\mathcal{N}_n(i)$:

$$
\mathbf{C}_i = \frac{\mathrm{LCM}_i - \mathbf{x}_i}{\lVert \mathrm{LCM}_i - \mathbf{x}_i \rVert}, \qquad \mathrm{LCM}_i = \frac{1}{n} \sum_{k \in \mathcal{N}_n(i)} \mathbf{x}_k
$$

The model parameter `n_neighbors` sets $n$ ([setting it in a protocol](../guides/configuration.md#model-parameters)). Its default `-1` selects the paper's global case $n = N - 1$, in which every sheep is pulled toward the mean of all the others; all nine study protocols use it. A string such as `"0.25N"` selects $\lceil 0.25\,N \rceil$.

## Grazing

When no dog is closer than $r_s = 65$ m, sheep $i$ grazes (Animation 1). With probability $p = 0.05$ it takes one step of $\delta = 1$ m at a random angle $\boldsymbol{\epsilon}_{\mathrm{graze}}$; otherwise it stays where it is:

$$
\mathbf{x}_i^{t+1} = \begin{cases}
\mathbf{x}_i^t + \delta\,\boldsymbol{\epsilon}_{\mathrm{graze}}, & \text{with probability } p = 0.05 \\
\mathbf{x}_i^t, & \text{with probability } 0.95
\end{cases}
$$

By default (`graze_repulsion: false`, used in all nine study protocols), a grazing sheep ignores neighbours closer than $r_a$ and only takes this random step. Setting `graze_repulsion: true` follows Section 2 of Strombom et al. (2014), which states that sheep keep their distance from each other even with no dog nearby; the step rule below is HerdSim's reading of it. It is used in the [paper check](strombom_check.md) and in the grazing pilots of the [report](../report/d_min_report.md#32-grazing-repulsion-pilots). With it, a grazing sheep with at least one neighbour closer than $r_a$ steps $\delta = 1$ m along the normalized sum $h\,\mathbf{H}_i + \rho_a\,\mathbf{R}_{a,i} + e\,\boldsymbol{\epsilon}_i$: the reacting heading without the flock and dog terms.

![Animation of sheep reacting as the dogs come within r_s](../gifs/sheep_reaction.gif)

**Animation 1: Sheep switch from grazing to reacting as dogs come within $r_s = 65$ m (`wide`, $N = 200$, $D = 4$, seed 0, first 120 s of `dmin_f99_m6`).** As the dogs circle behind the flock, the number of reacting sheep grows from 13 at 1 s to all 200 by 120 s.

- Marks: filled blue dots are reacting sheep (at least one dog within $r_s = 65$ m), hollow blue dots are grazing sheep, and orange triangles are dogs.

## Multi-dog push blending (HerdSim extension)

Strombom et al. (2014) defines the push $\mathbf{R}_{s,i}$ for one dog. When several dogs are closer than $r_s$, HerdSim adds the unit vectors pointing away from each of them and normalizes the sum, so the result is again a unit vector (Animation 2). With $\mathrm{threat}_i = \{j \mid \lVert \mathbf{x}_i - \mathbf{y}_j \rVert < r_s\}$ the set of those dogs, at positions $\mathbf{y}_j$:

$$
\mathbf{R}_{s,i} = \frac{\sum_{j \in \mathrm{threat}_i} \widehat{\mathbf{x}_i - \mathbf{y}_j}}{\left\lVert \sum_{j \in \mathrm{threat}_i} \widehat{\mathbf{x}_i - \mathbf{y}_j} \right\rVert}
$$

The sum is normalized so that the dogs' total weight stays $\rho_s = 1.0$ for any number of dogs $D$. Without it, two dogs pushing in directions less than 116.7 deg apart would give a push longer than the flock attraction $c = 1.05$ (two unit vectors at angle $\phi$ add up to length $2\cos(\phi/2)$). This could split the flock; we have not tested it.

The walking speed does not depend on this normalization: the whole heading $\mathbf{H}_i'$ is normalized, so a reacting sheep walks 1 m per tick however many dogs push it. More dogs change the direction a sheep walks and how many sheep react, not how fast they walk.

![Animation of one dog and eight dogs driving the same flock](../gifs/push_blending.gif)

**Animation 2: One dog and eight dogs on the same compact flock (`compact`, $N = 100$, seed 0, 99% rule, 6 drive times, `dmin_f99_m6`).** Reacting sheep always walk 1 m/s, so 8 dogs drive a compact flock at about the same speed as 1 dog.

- Marks: blue dots are sheep, orange triangles are dogs, and the green circle is the goal; the bottom-left label shows the elapsed time and the number of sheep still outside the goal.
- Left: $D = 1$ dog, finishing at 195 s.
- Right: $D = 8$ dogs on the driving arc, finishing at 192 s.

## References

1. Strombom, D., et al. (2014). *Solving the shepherding problem: heuristics for herding autonomous, interacting agents*. Journal of the Royal Society Interface, 11(100), 20140719, [10.1098/rsif.2014.0719](https://doi.org/10.1098/rsif.2014.0719).
