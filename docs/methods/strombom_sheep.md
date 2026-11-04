# Strombom et al. (2014) discrete behavioral model

In the local-interaction model of [Strombom et al. (2014)](https://doi.org/10.1098/rsif.2014.0719), each sheep updates its own position once per tick ($\Delta t = 1$ s) before the dogs move (Figure 1):

- Reacting sheep (any dog within $r_s = 65$ m): computes a new heading $\mathbf{H}_i'$ as a weighted sum of five unit vectors and steps $\delta = 1$ m along $\mathbf{H}_i'$.
- Grazing sheep (no dog within $r_s = 65$ m): mostly stands still, taking a random step of length $\delta = 1$ m with probability $p = 0.05$ ([grazing](#grazing)).

![Sheep i, its neighbours and a dog, and the five heading vectors](../figures/fig_sheep_forces.png)

**Figure 1: The sheep rule of Strombom et al. (2014).** A reacting sheep combines five weighted unit vectors into its new heading $\mathbf{H}_i'$.

- Legend: the black dot is focal sheep $i$, blue dots are flock-mates, the red dot is a neighbour closer than $r_a = 2$ m, the green `+` is the local centre of mass $\mathrm{LCM}_i$, and the orange triangle is a dog inside $r_s = 65$ m.
- Left: interaction geometry around sheep $i$ ($r_a = 2$ m repulsion zone drawn $3\times$ for visibility, $r_s = 65$ m dog detection circle).
- Right: the five weighted vectors and their resultant heading $\mathbf{H}_i'$.

## Reacting heading and step

For a reacting sheep $i$ at position $\mathbf{x}_i^t$, its unnormalized heading $\mathbf{H}_i'$ combines five terms, and the sheep advances by $\delta = 1$ m along the normalized result:

$$
\mathbf{H}_i' = h\,\mathbf{H}_i + c\,\mathbf{C}_i + \rho_a\,\mathbf{R}_{a,i} + \rho_s\,\mathbf{R}_{s,i} + e\,\boldsymbol{\epsilon}_i, \qquad \mathbf{x}_i^{t+1} = \mathbf{x}_i^t + \delta\,\frac{\mathbf{H}_i'}{\lVert \mathbf{H}_i' \rVert}
$$

- Previous heading $\mathbf{H}_i$ (inertia weight $h = 0.5$): unit direction of the sheep's previous step $(\mathbf{x}_i^t - \mathbf{x}_i^{t-1}) / \lVert \mathbf{x}_i^t - \mathbf{x}_i^{t-1} \rVert$, or $\mathbf{0}$ if the sheep stood still on the previous tick.
- Keeping space $\mathbf{R}_{a,i}$ (repulsion weight $\rho_a = 2.0$, highest): normalized sum of unit vectors pointing away from all neighbours closer than $r_a = 2$ m ($\mathcal{N}_a(i) = \{j \ne i \mid \lVert \mathbf{x}_i - \mathbf{x}_j \rVert < r_a\}$), or $\mathbf{0}$ if $\mathcal{N}_a(i)$ is empty:

$$
\mathbf{R}_{a,i} = \frac{\sum_{j \in \mathcal{N}_a(i)} \widehat{\mathbf{x}_i - \mathbf{x}_j}}{\left\lVert \sum_{j \in \mathcal{N}_a(i)} \widehat{\mathbf{x}_i - \mathbf{x}_j} \right\rVert}
$$

- Running from the dog $\mathbf{R}_{s,i}$ (repulsion weight $\rho_s = 1.0$): unit vector pointing away from the threatening dog(s) within $r_s = 65$ m ([multi-dog push blending](#multi-dog-push-blending-herdsim-extension)).
- Angular noise $\boldsymbol{\epsilon}_i$ (weight $e = 0.3$): unit vector at a random angle drawn uniformly from $[0, 2\pi)$.

### Attraction to the flock

The cohesion vector $\mathbf{C}_i$ (weight $c = 1.05$) points toward the local centre of mass $\mathrm{LCM}_i$ of the $n$ nearest other sheep $\mathcal{N}_n(i)$:

$$
\mathbf{C}_i = \frac{\mathrm{LCM}_i - \mathbf{x}_i}{\lVert \mathrm{LCM}_i - \mathbf{x}_i \rVert}, \qquad \mathrm{LCM}_i = \frac{1}{n} \sum_{k \in \mathcal{N}_n(i)} \mathbf{x}_k
$$

- Global vs local attraction: the model parameter `n_neighbors` sets $n$ ([setting it in a protocol](../guides/configuration.md#model-parameters)); the default `-1` selects the paper's global case $n = N - 1$ (used across all six study protocols), while a string such as `"0.25N"` selects $\lceil 0.25\,N \rceil$.

## Grazing

When no dog lies within $r_s = 65$ m of sheep $i$, the sheep grazes (Animation 1):

$$
\mathbf{x}_i^{t+1} = \begin{cases}
\mathbf{x}_i^t + \delta\,\boldsymbol{\epsilon}_{\mathrm{graze}}, & \text{with probability } p = 0.05 \\
\mathbf{x}_i^t, & \text{with probability } 0.95
\end{cases}
$$

- Default (`graze_repulsion: false`): used in all six main study protocols; grazing sheep ignore neighbours closer than $r_a$ and only take the $5\%$ random walk above.
- Grazing repulsion (`graze_repulsion: true`): matches Section 2 of Strombom et al. (2014), where sheep repel each other regardless of dog distance (used in the [paper check](strombom_check.md) and the grazing pilots in the [report](../report/d_min_report.md#4-limitations)). Under this option, any grazing sheep with $\mathcal{N}_a(i) \ne \emptyset$ steps $\delta = 1$ m along the normalized sum $h\,\mathbf{H}_i + \rho_a\,\mathbf{R}_{a,i} + e\,\boldsymbol{\epsilon}_i$.

![Animation of sheep reacting as the dogs come within r_s](../gifs/sheep_reaction.gif)

**Animation 1: Sheep switch from grazing to reacting as dogs enter $r_s = 65$ m (`wide`, $N = 200$, $D = 4$, seed 0, first 120 s of `dmin_f99_m6`).** As the dogs circle behind the flock, the reacting zone spreads from 13 sheep at 1 s to all 200 sheep by 120 s.

- Legend: filled blue dots are reacting sheep (at least one dog within $r_s = 65$ m), hollow blue dots are grazing sheep, and orange triangles are dogs.

## Multi-dog push blending (HerdSim extension)

Strombom et al. (2014) defines $\mathbf{R}_{s,i}$ for a single dog. For multiple dogs within $r_s$ ($\mathrm{threat}_i = \{j \mid \lVert \mathbf{x}_i - \mathbf{y}_j \rVert < r_s\}$), HerdSim sums the unit repulsion vectors from each threatening dog and normalizes the result (Animation 2):

$$
\mathbf{R}_{s,i} = \frac{\sum_{j \in \mathrm{threat}_i} \widehat{\mathbf{x}_i - \mathbf{y}_j}}{\left\lVert \sum_{j \in \mathrm{threat}_i} \widehat{\mathbf{x}_i - \mathbf{y}_j} \right\rVert}
$$

- Why normalize: without normalization, two dogs separated by angle $\phi < 116.7^\circ$ exert a combined push of $2\cos(\phi/2) > c = 1.05$, overpowering flock cohesion and splitting the flock. Normalizing keeps the dog repulsion weight at $\rho_s = 1.0$ regardless of $D$, while blending the push directions (for example, two symmetric flank dogs push the sheep straight forward).
- Constant walking speed: because every reacting step has length $\delta = 1$ m, adding dogs changes the sheep's heading and the fraction of the flock inside $r_s$, never a reacting sheep's walking speed.

![Animation of one dog and eight dogs driving the same flock](../gifs/push_blending.gif)

**Animation 2: One dog vs eight dogs on the same compact flock (`compact`, $N = 100$, seed 0, 99% rule, 6 drive times, `dmin_f99_m6`).** Because reacting sheep always walk at 1 m/s and $\mathbf{R}_{s,i}$ is normalized, 8 dogs drive a compact flock at the same speed as 1 dog.

- Legend: blue dots are sheep, orange triangles are dogs, and the green circle is the goal; the bottom-left label shows elapsed time and sheep remaining outside the goal.
- Left: $D = 1$ dog, finishing at 195 s.
- Right: $D = 8$ dogs on the driving arc, finishing at 192 s.

## References

- Strombom, D., et al. (2014). *Solving the shepherding problem: heuristics for herding autonomous, interacting agents*. Journal of the Royal Society Interface, 11(100), 20140719. [DOI: 10.1098/rsif.2014.0719](https://doi.org/10.1098/rsif.2014.0719)
