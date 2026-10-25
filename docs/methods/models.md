# Agent Models and Multi-Dog Coordination

This document details the mathematical formulation, biological rationale, and algorithmic implementations of the animal and robot controllers in **HerdSim**.

HerdSim bridges the gap between empirical animal behavior literature and autonomous multi-agent systems. It models individual sheep dynamics derived from GPS field data and extends single-shepherd heuristics into distributed, collision-aware multi-dog teams.

---

## Table of Contents

- [1. Sheep Flocking Models](#1-sheep-flocking-models)
  - [Strömbom et al. (2014) Discrete Behavioral Model](#strombom-et-al-2014-discrete-behavioral-model)
  - [Multi-Dog Push Blending (HerdSim Extension)](#multi-dog-push-blending-herdsim-extension)
  - [Kubo et al. (2022) Continuous Potential Fields](#kubo-et-al-2022-continuous-potential-fields)
  - [Lama & di Bernardo (2024) Non-Cohesive Targets](#lama--di-bernardo-2024-non-cohesive-targets)
- [2. Shepherd Controllers](#2-shepherd-controllers)
  - [Coordinated Team Architecture: `strombom_multi`](#coordinated-team-architecture-strombom_multi)
  - [Uncoordinated Greedy Baseline: `fat`](#uncoordinated-greedy-baseline-fat)
  - [Independent Paper Shepherds: `independent`](#independent-paper-shepherds-independent)
  - [Continuous Force Shepherds: `kubo`](#continuous-force-shepherds-kubo)
  - [Brownian Herders: `lama`](#brownian-herders-lama)
- [References](#references)

---

## 1. Sheep Flocking Models

### Strömbom et al. (2014) Discrete Behavioral Model

Based on high-frequency GPS tracking of real sheep flocks pursued by a border collie ([Strömbom et al. 2014](https://doi.org/10.1098/rsif.2014.0719)), domestic sheep do not follow global flock plans. Instead, each individual sheep balances **competing physical and social instincts** at every discrete time step ($t \to t+1$, where 1 tick = 1 second).

![Multi-dog coordination mechanisms](../../docs/figures/fig3_team_rule.png)
*Figure 1: How sheep and dogs interact. Sheep switch between peaceful grazing and active flight depending on dog distance. When fleeing, sheep balance collision avoidance, flock cohesion, momentum, predator repulsion, and random noise.*

#### Active Flight Mode (Dog Distance $< r_s$)

When any shepherd dog comes within the threat sensing distance $r_s = 65\text{ m}$ (the visual detection horizon of domestic sheep), sheep $i$ enters **active flight mode**. Its desired heading vector $\mathbf{H}_i'$ combines five unit vectors scaled by behavioral weights:

$$\mathbf{H}_i' = h\,\mathbf{H}_i + c\,\mathbf{C}_i + \rho_a\,\mathbf{R}_{a,i} + \rho_s\,\mathbf{R}_{s,i} + e\,\mathbf{\epsilon}_i$$

1. **Momentum / Inertia ($\mathbf{H}_i$, weight $h = 0.5$)**:
   - *Why?* Real animals have physical mass and cannot pivot instantaneously.
   - Vector: Direction of travel from the previous tick:
     $$\mathbf{H}_i = \frac{\mathbf{x}_i^t - \mathbf{x}_i^{t-1}}{\lVert \mathbf{x}_i^t - \mathbf{x}_i^{t-1} \rVert}$$

2. **Social Cohesion ($\mathbf{C}_i$, weight $c = 1.05$)**:
   - *Why?* Safety in numbers. An isolated sheep feels vulnerable and is strongly attracted toward its flock-mates.
   - Vector: Points from sheep $\mathbf{x}_i$ toward the Local Center of Mass ($\mathrm{LCM}_i$) of its $n$ nearest neighbors:
     $$\mathbf{C}_i = \frac{\mathrm{LCM}_i - \mathbf{x}_i}{\lVert \mathrm{LCM}_i - \mathbf{x}_i \rVert}, \quad \text{where } \mathrm{LCM}_i = \frac{1}{n} \sum_{k \in \mathcal{N}_n(i)} \mathbf{x}_k$$
   - In the canonical model, $n = N - 1$ (interaction with all flock members).

3. **Collision Avoidance ($\mathbf{R}_{a,i}$, weight $\rho_a = 2.0$)**:
   - *Why?* Animals prioritize not crashing into or trampling each other above all else. Notice this term carries the highest weight ($\rho_a = 2.0$).
   - Any neighbor $j$ closer than personal space $r_a = 2\text{ m}$ exerts repulsion:
     $$\mathbf{R}_{a,i} = \frac{\sum_{j \ne i, \lVert \mathbf{x}_i - \mathbf{x}_j \rVert < r_a} \frac{\mathbf{x}_i - \mathbf{x}_j}{\lVert \mathbf{x}_i - \mathbf{x}_j \rVert}}{\left\lVert \sum_{j \ne i, \lVert \mathbf{x}_i - \mathbf{x}_j \rVert < r_a} \frac{\mathbf{x}_i - \mathbf{x}_j}{\lVert \mathbf{x}_i - \mathbf{x}_j \rVert} \right\rVert}$$

4. **Predator Escape ($\mathbf{R}_{s,i}$, weight $\rho_s = 1.0$)**:
   - Direct repulsion away from threat dogs within $r_s = 65\text{ m}$. (See multi-dog blending below).

5. **Random Behavioral Noise ($\mathbf{\epsilon}_i$, weight $e = 0.3$)**:
   - Simulates imperfect sensing and behavioral jitter. $\mathbf{\epsilon}_i$ is a unit vector oriented at an angle drawn uniformly from $[0, 2\pi)$.

#### Position Update
At each tick ($1\text{ s}$), sheep $i$ steps forward by distance $\delta = 1\text{ m}$ along its normalized heading:

$$\mathbf{x}_i^{t+1} = \mathbf{x}_i^t + \delta\,\frac{\mathbf{H}_i'}{\lVert \mathbf{H}_i' \rVert}$$

This caps maximum sheep running speed at $1.0\text{ m/s}$.

#### Grazing Mode (Dog Distance $\ge r_s$)
When all dogs are farther than $r_s = 65\text{ m}$, the sheep relax. With probability $p = 0.95$ they stand still; with $p = 0.05$ they take a casual step in a random direction:

$$\mathbf{x}_i^{t+1} = \begin{cases} \mathbf{x}_i^t + \delta\,\mathbf{\epsilon}_{\mathrm{graze}}, & \text{with probability } 0.05 \\ \mathbf{x}_i^t, & \text{with probability } 0.95 \end{cases}$$

---

### Multi-Dog Push Blending (HerdSim Extension)

The original 2014 Strömbom model was designed for a **single dog**. If one naively sums independent repulsion vectors from $D = 4$ or $8$ dogs, the combined fear force would scale up to $8\times$, overpowering the flock cohesion ($c = 1.05$) and violently scattering the herd.

HerdSim resolves this by **vectorially summing and normalizing** all active threat directions to unit length:

$$\mathbf{R}_{s,i} = \frac{\sum_{j \in \mathrm{threat}} \frac{\mathbf{x}_i - \mathbf{y}_j}{\lVert \mathbf{x}_i - \mathbf{y}_j \rVert}}{\left\lVert \sum_{j \in \mathrm{threat}} \frac{\mathbf{x}_i - \mathbf{y}_j}{\lVert \mathbf{x}_i - \mathbf{y}_j \rVert} \right\rVert}$$

where $\mathrm{threat} = \{j \mid \lVert \mathbf{x}_i - \mathbf{y}_j \rVert < r_s\}$.

#### Intuitive Flanking Example
Consider a sheep at $(0, 5)$ pursued by two flanking dogs: Dog 1 at $(-3, 0)$ (rear-left) and Dog 2 at $(3, 0)$ (rear-right):
- Dog 1 pushes the sheep forward and right $(+x, +y)$.
- Dog 2 pushes the sheep forward and left $(-x, +y)$.
- Vector addition cancels lateral pushes while reinforcing forward propulsion.
- Normalization restores standard fear intensity ($\lVert \mathbf{R}_{s,i} \rVert = 1.0$), steering the sheep smoothly forward without artificial force inflation.

---

### Kubo et al. (2022) Continuous Potential Fields

As a cross-paradigm benchmark, HerdSim implements the continuous physics model of [Kubo et al. (2022)](https://doi.org/10.1007/s10015-021-00726-7). Unlike Strömbom's rule-based state machine, agents move under smooth, continuous artificial potential fields:

![Kubo continuous force model](../../docs/figures/fig5_kubo.png)
*Figure 2: The Kubo et al. (2022) potential field model. Left: Forces acting on a sheep (repulsion, social attraction, dog fear, velocity alignment). Middle: Forces acting on a dog (attraction to farthest sheep, repulsion from goal boundary, mutual dog repulsion). Right: Simulation snapshot showing mutual dog repulsion naturally fanning out shepherds.*

- **Kubo Sheep Forces**:
  1. Inter-sheep collision repulsion ($1/r^2$).
  2. Velocity alignment with neighbors.
  3. Social attraction toward neighbor center of mass ($-1/r$).
  4. Predator escape force ($1/r^3$).
- **Key differences from Strömbom**:
  - In Kubo, adding more dogs accelerates drive completion even on compact flocks (from $\sim 115\text{ s}$ with 1 dog to $29\text{ s}$ with 10 dogs) because forces are additive and non-linearly distance-dependent.
  - Sheep only interact within a fixed radius ($20\text{ m}$), requiring `compact` starting layouts.

---

### Lama & di Bernardo (2024) Non-Cohesive Targets

HerdSim integrates the non-cohesive target model from [Lama & di Bernardo (2024)](https://doi.org/10.1103/PhysRevResearch.6.L032012):
- **Targets (the "sheep")**: Pure Brownian random walkers with diffusion coefficient 1, **no social cohesion**, and no alignment.
- **Escape Dynamics**: A herder closer than $\lambda = 2.5$ exerts a repulsive push that drops linearly to zero at distance $\lambda$.
- **Purpose**: Establishes an empirical baseline to compare flocking animals against non-cohesive swarms (validating the theoretical $D \propto \sqrt{N}$ scaling conjecture).

---

## 2. Shepherd Controllers

HerdSim implements four distinct shepherd architectures:

```text
Shepherd Controllers
├── strombom_multi   (Coordinated autonomous team: Hungarian matching + driving arc)
├── fat              (Greedy uncoordinated baseline: Farthest-Agent Targeting)
├── independent      (Independent single-dog agents: collect/drive switch without team layer)
└── kubo_forces      (Physics-based continuous fields with mutual dog repulsion)
```

---

### Coordinated Team Architecture: `strombom_multi`

Extends Strömbom's heuristics into an autonomous, collision-aware multi-dog team:

#### 1. Outlier Detection Threshold ($f(N) = r_a N^{2/3}$)
- *Why $r_a N^{2/3}$?* In 2D dense packing of disks with diameter $r_a$, a solid cluster radius scales as $\sim N^{1/2}$. In 3D spheres, it scales as $\sim N^{1/3}$. On an open pasture, sheep spread with fractal cluster density, making $N^{2/3}$ the natural geometric boundary where an animal is perceptually separated from the collective.
- If any sheep lies farther than $f(N)$ from the Global Center of Mass ($\mathrm{GCM} = \frac{1}{N} \sum_k \mathbf{x}_k$), the flock is classified as scattered, triggering **Outlier Collection Mode**.

#### 2. Outlier Assignment via Hungarian Matching
- For each detected outlier $o$, the collection waypoint $P_c$ is positioned $r_a = 2\text{ m}$ directly behind the stray relative to the flock's center:
  $$P_c = \mathbf{x}_o + r_a \frac{\mathbf{x}_o - \mathrm{GCM}}{\lVert \mathbf{x}_o - \mathrm{GCM} \rVert}$$
- The $D$ farthest outliers are assigned 1-to-1 to the $D$ available dogs using the Hungarian algorithm (`scipy.optimize.linear_sum_assignment`). This minimizes total dog running distance and prevents crossing trajectories. Surplus dogs join the driving formation.

#### 3. Cohesive Driving Formation ($P_d$)
- When all sheep are within $f(N)$, the flock is cohesive, and dogs switch to **Drive Mode**.
- The nominal driving point $P_d$ is placed behind the flock along the goal axis:
  $$P_d = \mathrm{GCM} + r_a \sqrt{N} \frac{\mathrm{GCM} - \mathbf{x}_{\mathrm{goal}}}{\lVert \mathrm{GCM} - \mathbf{x}_{\mathrm{goal}} \rVert}$$
- *Why $r_a \sqrt{N}$?* A cohesive flock forms an approximate disk of radius proportional to $r_a\sqrt{N}$. This standoff distance places shepherds immediately behind the herd's rear boundary.
- Multiple dogs fan out along an arc of radius $R$ spanning the flock's angular width ($\pm \arcsin(R_{\mathrm{flock}} / R)$). Dogs maintain their polar angular order to prevent crossing paths.

#### 4. Speed & Standoff Rule
- **Speed**: $v_{\mathrm{dog}} = 1.5\text{ m/s}$ ($1.5\times$ sheep speed, matching the biological border collie ratio).
- **Standoff Rule**: If a dog approaches closer than $3 r_a = 6\text{ m}$ to any sheep, it stops moving ($\mathbf{v}_{\mathrm{dog}} = 0$) to avoid spooking animals into panic or causing trampling.

---

### Uncoordinated Greedy Baseline: `fat`

The **Farthest-Agent Targeting (FAT)** controller tests whether coordination is truly necessary:
- **Rule**: Each dog independently identifies whichever sheep is farthest from the goal and sprints $r_a$ behind it.
- **What is missing**: No Hungarian assignment, no driving arc, no communication, and no inter-dog collision avoidance.

![FAT baseline clumping](../../docs/figures/fig4_fat.png)
*Figure 3: FAT baseline pathology. Without assignment, all dogs target the identical farthest sheep, clumping into a single disordered pack. Adding dogs yields zero scaling benefit.*

---

### Independent Paper Shepherds: `independent`

Each dog independently executes the original single-dog rule of Strömbom (2014):
- Decides the collect/drive switch based on the entire flock.
- Walks to target waypoints with individual step noise and stopping rules.
- Contains the behavioral state machine but **lacks the multi-agent coordination layer**.
- *Finding*: Sufficient up to $N = 200$ sheep; fails at $N = 400$ where coordinated multi-dog teams are mandatory.

---

### Continuous Force Shepherds: `kubo`

Guides shepherds via continuous potential fields rather than discrete states:
1. Attracted toward the farthest sheep.
2. Repelled when too close to that sheep ($1/r^3$).
3. Repelled from the goal perimeter.
4. **Mutual dog repulsion**: A strong repulsive force ($1/r^3$, weight $K_{f4} = 3000$) between dogs.
- Shepherds act like like-charged particles, self-organizing into an arc along the flock boundary without any centralized coordinator.

---

## References

1. **Strömbom, D., et al. (2014)**. *Solving the shepherding problem: heuristics for herding autonomous, interacting agents*. Journal of the Royal Society Interface, 11(100), 20140719. [DOI: 10.1098/rsif.2014.0719](https://doi.org/10.1098/rsif.2014.0719)
2. **Kubo, M., Tashiro, M., Sato, H., Yamaguchi, A. (2022)**. *Herd guidance by multiple sheepdog agents with repulsive force*. Artificial Life and Robotics, 27, 416–427. [DOI: 10.1007/s10015-021-00726-7](https://doi.org/10.1007/s10015-021-00726-7)
3. **Lama, A., & di Bernardo, M. (2024)**. *Universal scaling laws in multi-agent herding of non-cohesive targets*. Physical Review Research, 6(L032012). [DOI: 10.1103/PhysRevResearch.6.L032012](https://doi.org/10.1103/PhysRevResearch.6.L032012)
