Absolutely. I went a level deeper and treated this as a **state-of-the-art and research-gap study**, rather than simply a bibliography.

The important result is that the field is moving in a direction that gives **HerdSim a potentially much stronger role** than "compare several shepherding algorithms."

I would position HerdSim around:

> **understanding the limits, information requirements, robustness, generalization, and adaptability of multi-agent shepherding.**

The literature supports this direction quite strongly, including several developments from 2024–2026 that were not in the original set of papers you gave me. ([DOI][1])

---

# 1. Executive view: where the field is today

The research landscape can be organized like this:

```text
                    COMPUTATIONAL SHEPHERDING
                              │
        ┌─────────────────────┼──────────────────────┐
        │                     │                      │
   BIOLOGICAL /          CONTROL / ROBOTICS      THEORY
   BEHAVIOURAL
        │                     │                      │
  Strömbom 2014          Kubo 2022              Herdability 2024
  Jadhav 2024            FAT / OTS              Field theory 2025
  Early 2020             Consensus              General control
        │                Decentralized
        │                     │
        └─────────────────────┼──────────────────────┘
                              │
                    ADAPTIVE / LEARNING
                              │
                 RL / neuroevolution
                 context-aware control
                 heterogeneous agents
                              │
                              ↓
                       REAL ROBOTICS
                              │
                    UAV / UGV / TurtleBot
                    physical constraints
                    obstacle avoidance
                              │
                              ↓
                       OPEN PROBLEM
                              │
              "What makes a flock herdeable?"
```

The field has therefore moved considerably beyond:

> "Can a dog move sheep to a goal?"

The interesting questions now concern **limits and generality**.

---

# 2. The most important change: from algorithms to conditions

The early literature mostly asks:

> **What control rule should the shepherd use?**

For example, Strömbom's model provides a behavioural heuristic based around collection and driving. ([PubMed][2])

Kubo instead explores a force-based formulation for multiple sheepdogs.

But newer work increasingly asks:

> **Under what conditions can shepherding work at all?**

This is a major conceptual shift.

The 2024 *Physical Review Research* paper by Lama & di Bernardo is especially important. They explicitly relax assumptions of:

* cohesive target behaviour;
* global sensing.

They investigate the **minimum number of herders required**, density thresholds, and a "herdability graph" whose connectivity helps explain when shepherding becomes possible. ([DOI][1])

That paper should be one of the foundations of your new research direction.

---

# 3. My recommended 25-paper state-of-the-art map

I would organize your literature review into the following families.

## A. Foundational shepherding

| Work                     | Main question                                           | What it introduced                             | What remains                                         |
| ------------------------ | ------------------------------------------------------- | ---------------------------------------------- | ---------------------------------------------------- |
| **Lien et al. 2005**     | Can multiple shepherds cooperate?                       | Multi-shepherd behaviour without communication | Limited realism/generalization                       |
| **Strömbom et al. 2014** | How can one/multiple shepherds herd flocking agents?    | Collect/drive heuristic                        | Strong assumptions about flock and sensing           |
| **Tsunoda et al. 2018**  | Can a shepherd use local camera observations?           | Farthest-Agent Targeting (FAT)                 | Limited sensing but still relatively simple sheep    |
| **Kubo et al. 2022**     | Can multiple dogs guide sheep using force interactions? | Force-based multi-dog model                    | Generality and realistic sensing                     |
| **Strömbom et al. 2026** | What if sheep follow rather than evade?                 | Adaptive lead/herd strategy                    | Very recent; broader behavioural variability remains |

Lien is particularly important because it already studied cooperative multiple shepherds **without communication** as early as 2005. ([Illinois Experts][3]) Strömbom established the influential collect/drive framework. ([PubMed Central (PMC)][4]) FAT introduced a local-camera perspective. ([Taylor & Francis Online][5]) And the new 2026 work explicitly challenges the assumption that transporters must always herd rather than lead. ([arXiv][6])

---

# 4. Foundational work is not the research frontier anymore

This is important for your project.

If your thesis simply says:

> "We implemented Strömbom and Kubo and compared them."

that's useful but relatively incremental.

Those models answer:

> **How can we solve the nominal shepherding task?**

Your opportunity is to ask:

> **How far does the solution remain valid when its assumptions are systematically violated?**

That is the key.

---

# 5. Family B — Multi-shepherd coordination

Here the central question is:

> **How should multiple shepherds cooperate?**

Important works include:

### Lien et al. 2005

Multiple shepherds cooperate without communication. ([Illinois Experts][3])

### Campbell et al. 2021

**Distributed Multi-agent Shepherding with Consensus**

The work asks whether shepherds benefit from sharing contextual awareness, particularly consensus around the flock centre. They report improved performance from consensus. ([IASEI][7])

### Li, Ogura & Wakamiya 2023

**Communication-Free Shepherding Navigation with Multiple Steering Agents**

Each shepherd acts from its own observation without inter-agent communication; the paper studies success, cost, robustness and resilience. ([Frontiers][8])

This gives you an obvious experimental dimension:

```text
             INFORMATION SHARING

                  global
                    │
            ┌───────┴───────┐
            │               │
       centralized      decentralized
                            │
                    ┌───────┴───────┐
                    │               │
                communication   no communication
```

### HerdSim question

> **How much communication is actually necessary for a multi-dog team?**

That is much more interesting than just implementing another algorithm.

---

# 6. Family C — Limited sensing

This is one of the strongest trends.

Historically:

```text
dog knows:
position of every sheep
```

But that's unrealistic.

Tsunoda et al. investigated local-camera-based shepherding and showed that a farthest-agent strategy can operate without knowing all sheep positions, including under positional errors and lost observations. ([Taylor & Francis Online][5])

More recently, bearing-only shepherding explicitly asks how little information is sufficient. It uses directional/bearing measurements and investigates accuracy and communication requirements. ([PubMed Central (PMC)][9])

And the 2024 herdability paper pushes this much further by studying local information without assuming cohesive target dynamics. ([DOI][1])

---

# 7. This creates an excellent HerdSim experiment

Instead of simply implementing "bearing-only shepherding", make **information availability a controlled experimental factor**.

For example:

| Information level | Dog knows                     |
| ----------------- | ----------------------------- |
| I0                | complete global state         |
| I1                | local positions               |
| I2                | local distances               |
| I3                | bearings only                 |
| I4                | noisy bearings                |
| I5                | intermittent observations     |
| I6                | partial/occluded observations |

Then measure:

$$
P(\mathrm{success})
$$

$$
T_{\mathrm{success}}
$$

$$
\text{fragmentation}
$$

$$
\text{dog effort}
$$

as a function of information quality.

This could produce a very interesting **information–performance curve**.

---

# 8. Family D — Heterogeneous sheep

This is another major gap.

The classical assumption is:

```text
sheep_1 ≈ sheep_2 ≈ ... ≈ sheep_N
```

But real sheep obviously differ.

Fujioka, Ogura & Wakamiya specifically identify homogeneous sheep dynamics as a major simplifying assumption and survey approaches to heterogeneous flocks. ([arXiv][10])

Himo et al. study sheep that are **unresponsive to the shepherd**, and develop an iterative method that attempts to incorporate such sheep into the herding process. ([AIMS Press][11])

Another paper develops a shepherding algorithm with **model-based discrimination** for heterogeneous flocks. ([Taylor & Francis Online][12])

---

# 9. This is a particularly good HerdSim research axis

Define sheep types:

```text
                     SHEEP
                       │
       ┌───────────────┼────────────────┐
       ↓               ↓                ↓
  responsive        weakly          unresponsive
                    responsive
```

Then define a heterogeneity parameter:

$$
h = \frac{N_{\text{responsive}}}{N}
$$

Run:

```text
h = 1.0
h = 0.8
h = 0.6
h = 0.4
h = 0.2
h = 0.0
```

Now ask:

> **At what level of behavioural heterogeneity does each algorithm fail?**

This is considerably more scientifically interesting than "Kubo vs Strömbom."

---

# 10. Family E — Herdability theory

This may be the **most important theoretical direction** for HerdSim.

Lama & di Bernardo 2024 explicitly define a herdability problem and study the minimum number of herders needed as a function of target number and density. They identify a critical density threshold associated with connectivity/percolation of a herdability graph. ([DOI][1])

Their central question is essentially:

> **Is this population actually herdable under these conditions?**

That gives HerdSim an opportunity to move from:

```text
algorithm performance
```

to:

```text
system phase space
```

---

# 11. HerdSim could produce herdability maps

For example:

```text
              DOGS
         1   2   3   4   5
       ┌────────────────────
  200  │ X   X   X   ?   ✓
  150  │ X   X   ?   ✓   ✓
  100  │ X   ?   ✓   ✓   ✓
   50  │ ?   ✓   ✓   ✓   ✓
   20  │ ✓   ✓   ✓   ✓   ✓
       └────────────────────
               SHEEP
```

But instead of a simple sheep/dog matrix, you could make:

$$
\mathcal{H}
=
f(N_{\text{sheep}},
N_{\text{dogs}},
\rho,
r_{\text{sense}},
v_{\text{dog}},
\sigma_{\text{noise}},
h)
$$

where \(\mathcal{H}\) is some measure of herdability.

That could become a central scientific product of HerdSim.

---

# 12. Family F — Environmental complexity

El-Fiqi et al. 2020 is very important here.

Their paper explicitly investigates:

* relative sheep/dog speed;
* initial sheep configuration;
* number of shepherds;
* obstacle density.

They identify a **phase transition** in reactive shepherding as obstacle density and shepherd number change. ([IEEE Xplore][13])

This is exactly the sort of experiment HerdSim is structurally capable of running.

---

# 13. This gives you another research question

Instead of:

> "Does Kubo work with obstacles?"

ask:

> **"How does environmental complexity change the phase boundary between feasible and infeasible shepherding?"**

For example:

$$
P(\mathrm{success})
=
f(
N_D,
\rho_{\mathrm{obstacle}},
N_S,
v_D/v_S
)
$$

You can then look for critical regions.

---

# 14. Recent work is moving beyond static obstacles

A 2024 *Scientific Reports* paper studies **reactive shepherding along a dynamic path**, where multiple robots must keep a group within boundaries while navigating turns and constrained corridors. The study identifies sensitivity to group velocity and robot/group size ratios. ([Nature][14])

Then in 2026, Tomaselli et al. go further with **multi-robot obstacle-aware shepherding of non-cohesive targets**. Their model does not assume that targets flock cohesively; it combines target steering with obstacle-tangent motion and has been tested in simulation and with TurtleBot4/Osoyoo robots. ([arXiv][15])

This is one of the clearest signs of where the field is going.

---

# 15. Family G — Non-cohesive sheep

This is particularly interesting.

Most sheep models say:

```text
sheep ↔ sheep
strong cohesion
```

But Lama & di Bernardo deliberately study targets that do **not** necessarily have intrinsic collective cohesion. ([DOI][1])

The 2026 Tomaselli work similarly considers non-cohesive target agents in obstacle-rich environments. ([arXiv][15])

This raises a fundamental question:

> **How much does a shepherding algorithm rely on the sheep already being a flock?**

That question has not been fully resolved.

---

# 16. HerdSim can test this systematically

Define sheep cohesion strength:

$$
C_s \in [0,1]
$$

Then:

```text
C_s = 1.0   strongly cohesive
C_s = 0.7
C_s = 0.4
C_s = 0.1
C_s = 0.0   independent agents
```

Run every controller across the same spectrum.

Now you can discover:

> Strömbom works because of cohesion.

or:

> Kubo remains effective when cohesion decreases.

or:

> Algorithm X has a critical cohesion threshold.

That is an actual scientific result.

---

# 17. Family H — Adaptive/context-aware shepherding

A 2024 *Swarm Intelligence* paper explicitly develops **contextually aware intelligent control agents for heterogeneous swarms**. It emphasizes limited sensing/local information and adaptive selection of control behaviour. ([Springer][16])

The conceptual transition is:

```text
old:

state → fixed controller → action
```

to:

```text
state
 ↓
classify situation
 ↓
select behaviour
 ↓
action
```

This is important because real shepherding isn't necessarily one fixed rule.

---

# 18. HerdSim could test adaptive policies

For example:

```text
             flock state
                  │
       ┌──────────┼───────────┐
       ↓          ↓           ↓
 dispersed    cohesive    fragmented
       │          │           │
    collect      drive      recover
```

Then compare:

### Fixed policy

Always use one controller.

### Adaptive policy

Switch between controllers.

And ask:

> **Does behavioural adaptation improve robustness across unseen conditions?**

---

# 19. Family I — Reinforcement learning

Learning-based shepherding is already active.

Hussein et al. 2022 use curriculum-based RL and decompose shepherding into sub-tasks. Their approach achieved about 96% success in their experimental setting, but they also found that curriculum design matters and that skills learned in intermediate tasks do not automatically transfer well to the full task. ([University of Canberra Research Portal][17])

There is also hierarchical deep RL work where an aerial shepherd controls ground robots, including physical experiments and simulation-to-real/scale generalization. ([arXiv][18])

And automatic design/neuroevolution has been applied to robot shepherding, automatically producing controllers for a swarm of shepherd robots. ([arXiv][19])

---

# 20. The important research question is not "Can RL herd?"

That's already been demonstrated.

The more interesting question is:

> **Does learned shepherding generalize better than hand-designed shepherding?**

For example:

### Train

```text
50 sheep
2 dogs
open environment
global sensing
low noise
```

### Test

```text
100 sheep
4 dogs
obstacles
heterogeneous sheep
local sensing
high noise
```

Then calculate:

$$
\text{generalization gap}
=
P_{\mathrm{train}}-P_{\mathrm{test}}
$$

This would be a very useful HerdSim experiment.

---

# 21. Family J — Real animal behaviour

This is where Jadhav et al. 2024 becomes extremely important.

They collected high-resolution UWB trajectories from **14 sheep and a Border Collie**, studied directional information propagation, and built an agent-based model that reproduces key aspects of the observed response. ([Nature][20])

Crucially, the data and code are public. ([GitHub][21])

Their work shows something that classical simulations don't capture well:

> **the flock's internal information dynamics matter.**

They found directional information can propagate from the front of the flock toward the rear during dog-induced movement. ([Nature][20])

---

# 22. This suggests a completely new class of HerdSim metrics

Current metrics such as:

* cohesion
* polarization
* goal distance

measure **what the flock does**.

But Jadhav suggests measuring:

> **how information moves through the flock.**

For example:

$$
C_{ij}(\tau)
=
\mathrm{corr}
\left(
v_i(t),
v_j(t+\tau)
\right)
$$

Then estimate:

* information propagation direction;
* propagation delay;
* leader/follower structure;
* directional influence;
* response latency.

This is a very interesting extension.

---

# 23. Family K — Behavioural realism

The 2020 livestock-herding study is important for a different reason.

Early et al. analysed real dog–sheep interactions using **lag sequential analysis**, identifying sequences such as dog chasing → sheep escape and sheep movement → dog following. They also found trial score predicted efficient performance. ([MDPI][22])

This suggests a potential HerdSim validation strategy:

> Don't just ask whether the simulation reaches the goal.

Ask:

> **Does the simulated sequence of behaviours resemble real herding?**

For example:

```text
dog approaches
       ↓
sheep accelerate
       ↓
flock compresses
       ↓
dog adjusts position
       ↓
flock turns
```

You could compare event sequences between simulation and empirical data.

---

# 24. This leads to a "reality gap" experiment

I think this could be a very good research contribution.

Create increasingly realistic sheep models:

```text
Model 0
simple particles

      ↓

Model 1
flocking sheep

      ↓

Model 2
heterogeneous sheep

      ↓

Model 3
empirically calibrated sheep

      ↓

Model 4
empirical sheep + noisy sensing

      ↓

Model 5
robot constraints
```

Then ask:

> **At which realism level do conclusions about algorithm performance change?**

That's a very interesting scientific question.

---

# 25. Family L — Decision-making theory

The 2025 *Nature Communications* paper by Lama, di Bernardo & Klapp is another paper I would definitely include.

They derive a **nonreciprocal field theory for decision-making in multi-agent control**, using shepherding as the example. They identify two key decision processes:

1. target selection;
2. trajectory planning.

Different choices produce different macroscopic collective states. ([DOI][23])

This is important because it gives you a bridge:

```text
MICROSCOPIC
decision rule
      ↓
agent dynamics
      ↓
COLLECTIVE
behaviour
      ↓
MACROSCOPIC
flock state
```

HerdSim could experimentally investigate this connection.

---

# 26. Family M — Physical robot constraints

This is becoming increasingly important in 2026.

The recent CMFF + MPC work develops a collaborative multi-agent herding platform using a collective-motion flow field combined with nonlinear model predictive control, explicitly considering robot guidance/control and hyperparameter sensitivity. ([ScienceDirect][24])

The 2026 UAV work similarly argues that classical sheepdog models often treat agents as point masses, while real robots have:

* velocity limits;
* acceleration limits;
* motion constraints.

It proposes predicting swarm behaviour over a short horizon while selecting feasible actions. ([arXiv][25])

---

# 27. This reveals another gap

Most classical HerdSim-style algorithms assume:

```text
dog can instantly move
in any direction
at any velocity
```

A real robot cannot.

So introduce:

$$
v_{\max}
$$

$$
a_{\max}
$$

$$
\omega_{\max}
$$

$$
\tau_{\text{latency}}
$$

and perhaps:

$$
R_{\text{turn}}
$$

Then test:

> **Does the algorithm still work when the shepherd has realistic dynamics?**

Again, that's much more valuable than adding another abstract controller.

---

# 28. The newest conceptual development: leading versus herding

This is something I strongly recommend you include because it was published in 2026.

Strömbom, Hoitt & Cloud propose **"Lead When Possible, Herd When Necessary."**

The problem:

* herding works when agents evade the transporter;
* leading works when agents follow;
* real groups can contain both behavioural types;
* individual agents can even switch strategies over time.

Their algorithm switches adaptively between leading and herding. ([arXiv][6])

This is directly relevant to your heterogeneity problem.

---

# 29. It also changes the definition of "shepherding"

The classical model assumes:

```text
DOG → sheep → goal
```

But the broader transport problem is:

```text
CONTROLLER
     ↓
understand response
     ↓
choose influence mechanism
     ↓
transport group
```

The influence could be:

* repulsion;
* attraction;
* leadership;
* containment;
* positioning;
* communication.

This is a much more general formulation.

---

# 30. The 2026 research landscape is therefore moving toward this

```text
                    CLASSICAL
                       │
              fixed shepherding rule
                       ↓
               multi-dog control
                       ↓
               local information
                       ↓
              heterogeneous agents
                       ↓
               adaptive control
                       ↓
             predictive control
                       ↓
           physically constrained robots
                       ↓
             empirical animal dynamics
                       ↓
              GENERAL TRANSPORT
```

This is the trajectory I would align HerdSim with.

---

# 31. Here is the research-gap matrix I would use for your project

| Research problem        | Field status    | What papers have done           | What remains                                | HerdSim opportunity  |
| ----------------------- | --------------- | ------------------------------- | ------------------------------------------- | -------------------- |
| Basic herding           | Mature          | Strömbom                        | Mostly solved nominal case                  | Baseline             |
| Multiple dogs           | Active          | Lien, Kubo                      | Coordination principles                     | Compare mechanisms   |
| Communication           | Active          | Consensus / communication-free  | Information-performance tradeoff            | **Strong**           |
| Limited sensing         | Active          | FAT, bearing-only               | Minimal information requirements            | **Strong**           |
| Herdability             | Emerging        | Lama & di Bernardo              | Algorithm-specific vs universal limits      | **Very strong**      |
| Heterogeneous sheep     | Emerging        | Himo, Fujioka                   | General robustness                          | **Very strong**      |
| Non-cohesive flock      | Emerging        | Lama; Tomaselli                 | Transition from flock to independent agents | **Strong**           |
| Obstacles               | Active          | El-Fiqi, Tomaselli              | Generalization across environments          | **Strong**           |
| Dynamic environments    | Emerging        | dynamic-path work               | Robust adaptation                           | **Strong**           |
| Adaptive controller     | Emerging        | context-aware work              | General adaptive principles                 | **Very strong**      |
| RL                      | Active          | Hussein et al., hierarchical RL | Generalization / interpretability           | **Strong**           |
| Neuroevolution          | Emerging        | Garzón Ramos & Birattari        | Transferability                             | Possible             |
| Real sheep              | Emerging        | Jadhav, Early                   | Simulation validation                       | **Very strong**      |
| Information propagation | Emerging        | Jadhav                          | Relation to control                         | **Very strong**      |
| Robot constraints       | Emerging        | MPC / UAV work                  | Comparison against abstract models          | **Strong**           |
| Leadership + herding    | **Very recent** | Strömbom 2026                   | Mixed behavioural populations               | **Very strong**      |
| Standard benchmark      | Underdeveloped  | fragmented evaluations          | Cross-paper comparability                   | **Core opportunity** |

---

# 32. The most important thing I would NOT do

I would not create this:

```text
HerdSim

Strömbom
Kubo
FAT
RL
Consensus
...
```

and stop there.

That becomes a **catalogue**.

Instead, I would create:

```text
                    HERDSIM

                       ↓

              Experimental Factors
                       │
       ┌───────────────┼────────────────┐
       ↓               ↓                ↓
   Behaviour       Information      Environment
       │               │                │
 heterogeneity      sensing         obstacles
 responsiveness     noise           density
 cohesion           communication   dynamics
       │               │                │
       └───────────────┼────────────────┘
                       ↓
                  Controllers
                       │
         ┌─────────────┼─────────────┐
         ↓             ↓             ↓
      heuristic      force          learned
         │             │             │
         └─────────────┼─────────────┘
                       ↓
                    Metrics
                       ↓
                Phase diagrams
                       ↓
                Scientific laws
```

That is a research platform.

---

# 33. The five research programmes I think HerdSim could support

I would prioritize these.

## RQ1 — Herdability

> **What determines whether a group is herdeable?**

Variables:

* sheep number;
* dog number;
* density;
* cohesion;
* sheep responsiveness;
* dog speed;
* sensing range.

Output:

**herdability phase diagrams.**

---

## RQ2 — Information

> **What is the minimum information required for successful shepherding?**

Variables:

* global position;
* local position;
* distance;
* bearing;
* noisy bearing;
* occlusion;
* communication.

Output:

**information-performance curves.**

---

## RQ3 — Robustness and heterogeneity

> **How do shepherding strategies degrade when agents are heterogeneous or fail?**

Variables:

* responsive/unresponsive sheep;
* sheep speed;
* dog speed;
* dog failure;
* sensing failure;
* behavioural switching.

Output:

**robustness curves and failure boundaries.**

---

## RQ4 — Generalization

> **Do algorithms generalize beyond the environment and flock conditions they were designed for?**

Train/tune under:

```text
easy environment
```

Test under:

```text
different flock
different environment
different sensing
different noise
```

Output:

**generalization gap.**

---

## RQ5 — Reality gap

> **Which assumptions of idealized agent-based models materially affect conclusions about shepherding?**

Compare:

```text
ideal sheep
     ↓
heterogeneous
     ↓
empirical
     ↓
realistic sensing
     ↓
robot dynamics
```

Output:

**model-validity map.**

This one could become particularly distinctive.

---

# 34. I would combine them into one overarching research question

Rather than having five unrelated projects, I would formulate:

> **How do agent heterogeneity, information constraints, environmental complexity, and controller architecture determine the herdability, robustness, and generalization of multi-agent shepherding systems?**

Then your subquestions are:

### SQ1

How does the minimum number of shepherds scale with flock size and density?

### SQ2

How does limited sensing alter that scaling?

### SQ3

How does behavioural heterogeneity alter herdability?

### SQ4

How much communication is necessary between shepherds?

### SQ5

Do adaptive policies outperform fixed policies under distribution shift?

### SQ6

Do conclusions obtained using idealized sheep remain valid under empirically calibrated sheep dynamics?

### SQ7

How do realistic robot constraints change the ranking of algorithms?

That's a coherent research programme.

---

# 35. The experimental design becomes very powerful

Imagine this experiment.

### Models

```text
Strömbom
Kubo
FAT
Communication-free
Adaptive
RL
```

### Sheep

```text
20 / 50 / 100 / 200
```

### Dogs

```text
1 / 2 / 4 / 8
```

### Cohesion

```text
high / medium / low / none
```

### Responsiveness

```text
100 / 75 / 50 / 25%
```

### Observation

```text
global
local
bearing
noisy bearing
```

### Communication

```text
global
limited
none
```

### Environment

```text
open
obstacles
corridor
dynamic path
```

### Dog dynamics

```text
ideal
velocity constrained
acceleration constrained
latency
```

That's potentially thousands of experiments.

And **that is exactly where automation and a platform like HerdSim become valuable.**

---

# 36. Your output should not be one leaderboard

I'd produce several scientific outputs.

### 1. Success surface

$$
P(success)
$$

### 2. Herdability boundary

$$
N_{\text{dogs}}^*(N_{\text{sheep}},\rho,\ldots)
$$

### 3. Robustness curve

$$
P(success \mid noise)
$$

### 4. Information curve

$$
P(success \mid sensing)
$$

### 5. Heterogeneity curve

$$
P(success \mid h)
$$

### 6. Generalization gap

$$
G = P_{train}-P_{test}
$$

### 7. Efficiency frontier

$$
success \quad vs \quad dog\ effort
$$

Now you're generating scientific knowledge rather than simply benchmark scores.

---

# 37. There is another very interesting possibility: identify universality

This is more ambitious, but I think it is worth considering.

Suppose Strömbom, Kubo and FAT look very different internally.

Could you discover that they all succeed when:

$$
\frac{v_{\text{dog}}}{v_{\text{sheep}}} > c_1
$$

and

$$
\rho_{\text{flock}} > c_2
$$

and

$$
r_{\text{sensing}} > c_3?
$$

Then perhaps the details of the controller matter less than certain **dimensionless system parameters**.

That would be a much more fundamental contribution.

Instead of saying:

> "Kubo is better."

you could say:

> **"Across three fundamentally different shepherding mechanisms, success is governed primarily by these dimensionless ratios."**

That would be extremely interesting.

---

# 38. This connects directly to the herdability work

The Lama & di Bernardo work is already moving in this direction by looking for scaling laws and critical density thresholds rather than simply ranking algorithms. ([DOI][1])

HerdSim could extend that idea to:

$$
\Pi_1 =
\frac{v_D}{v_S}
$$

$$
\Pi_2 =
\frac{r_{\text{sensing}}}{d_{\text{flock}}}
$$

$$
\Pi_3 =
\frac{N_D}{N_S}
$$

$$
\Pi_4 =
\frac{r_{\text{interaction}}}{d_{\text{mean}}}
$$

etc.

Then search for **dimensionless predictors of herdability**.

That is much more scientifically ambitious.

---

# 39. Another major opportunity: algorithm-independent metrics

This comes back to your original requirement.

Your metrics should ultimately answer:

> **What happened to the flock?**

not:

> **Did the algorithm follow its own internal rules?**

So I would make your primary metric layer completely model-independent:

### Task

* success
* goal error
* completion time

### Collective

* cohesion
* fragmentation
* polarization
* density
* connectivity

### Control

* dog path length
* dog energy proxy
* control smoothness

### Information

* response latency
* directional propagation
* observability

### Robustness

* failure probability
* recovery time
* degradation slope

Then model-specific diagnostics are secondary.

---

# 40. This is where Jadhav could change HerdSim substantially

Their empirical study gives you access to something most shepherding simulations lack:

**ground truth trajectories.**

They provide UWB data and model code. ([GitHub][21])

That means HerdSim could eventually support:

```text
             EMPIRICAL DATA
                   ↓
             parameter fitting
                   ↓
             empirical sheep model
                   ↓
                 HerdSim
                   ↓
        algorithm comparison
```

You could ask:

> Does the conclusion "algorithm A is better than B" survive when the sheep model is calibrated from real animals?

That's a very strong question.

---

# 41. And your "Sequential Analysis" paper provides another validation route

Early et al. gives behavioural event sequences from actual livestock herding. ([MDPI][22])

So you can eventually compare:

```text
REAL:

dog stops
 → sheep stop
 → sheep move
 → dog follows
 → sheep escape
```

against:

```text
SIMULATION:

dog stops
 → sheep stop
 → sheep move
 → dog follows
 → sheep escape
```

Not necessarily exact trajectories.

Instead:

> **Do the transition probabilities between behavioural states look similar?**

That would be a novel and useful validation layer.

---

# 42. I would therefore add a "behavioural validation" module to HerdSim

Something like:

```text
simulation trajectory
        ↓
event detector
        ↓
behaviour sequence
        ↓
transition matrix
```

For example:

$$
P(B_{t+1}=j \mid B_t=i)
$$

Then compare simulation vs empirical data.

That takes HerdSim beyond purely geometric metrics.

---

# 43. A possible final architecture

I would eventually want HerdSim to look conceptually like:

```text
                           HerdSim
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
    MODELS                EXPERIMENTS             DATA
       │                      │                      │
 Strömbom                  Factors              trajectories
 Kubo                      seeds                empirical
 FAT                       scenarios            real-world
 Adaptive                  perturbations
 RL
       │                      │
       └──────────────┬───────┘
                      ↓
                  SIMULATOR
                      ↓
                 OBSERVATIONS
                      ↓
     ┌────────────────┼────────────────┐
     ↓                ↓                ↓
  outcome          collective       behavioural
   metrics          metrics          metrics
     │                │                │
     └────────────────┼────────────────┘
                      ↓
                  STATISTICS
                      ↓
       ┌──────────────┼──────────────┐
       ↓              ↓              ↓
   comparison     robustness     herdability
       │              │              │
       └──────────────┼──────────────┘
                      ↓
                 SCIENTIFIC
                  DISCOVERY
```

---

# 44. What I would implement in HerdSim, in order

Not all at once.

## Stage 1 — Make HerdSim a rigorous benchmark

Before adding many algorithms:

* common state representation;
* common observation interface;
* common action interface;
* model-independent metrics;
* trajectory recording;
* experiment manifests;
* reproducible seeds;
* statistical analysis.

---

## Stage 2 — Reproduce four different paradigms

I would choose:

### A. Strömbom

Behavioural heuristic. ([PubMed Central (PMC)][4])

### B. Kubo

Force-based multi-dog model.

### C. FAT / communication-free

Local-information controller. ([Frontiers][8])

### D. Jadhav

Empirically informed sheep/dog dynamics. ([Nature][20])

That's enough initially.

---

# 45. Stage 3 — Introduce perturbations

Build a systematic perturbation framework:

```text
Perturbation
├── sheep number
├── dog number
├── density
├── cohesion
├── responsiveness
├── noise
├── sensing range
├── occlusion
├── communication
├── obstacles
├── dog speed
├── dog failure
└── dynamic goals
```

Now HerdSim becomes an **experimental generator**.

---

# 46. Stage 4 — Study one open question deeply

Don't attempt everything.

My strongest candidate is:

> **How does limited information affect herdability in heterogeneous flocks?**

Why?

Because it combines several active research areas:

```text
herdability
+
limited sensing
+
heterogeneity
+
multiple dogs
```

And it can be studied almost entirely in simulation initially.

---

# 47. A concrete thesis experiment

### Research question

> How does the minimum number of shepherds required for successful herding change with flock heterogeneity and sensing limitations?

Define:

$$
N_D^*
=
\min
\{N_D:P(success)\geq 0.95\}
$$

Then measure:

$$
N_D^*
=
f(N_S,\rho,h,r_s,\sigma)
$$

where:

* \(N_S\) = sheep count;
* \(\rho\) = density;
* \(h\) = heterogeneity;
* \(r_s\) = sensing range;
* \(\sigma\) = sensing noise.

That's a clear mathematical research question.

---

# 48. Then compare algorithms

For each model:

```text
Strömbom
Kubo
FAT
Adaptive
```

estimate:

$$
N_D^*(\cdot)
$$

Now you might discover:

```text
               Required dogs

heterogeneity ↑

Strömbom       █████████████
Kubo           █████████
FAT            ███████
Adaptive       █████
```

Or perhaps the opposite.

The important point is that you're discovering **failure boundaries**, not simply ranking algorithms.

---

# 49. Another excellent experiment: "algorithm ranking reversal"

This is something I'd actively look for.

Suppose:

### Easy environment

```text
Strömbom > Kubo > FAT
```

But:

### Noisy sensing

```text
FAT > Kubo > Strömbom
```

And:

### Heterogeneous sheep

```text
Adaptive > FAT > Kubo
```

Then the conclusion is:

> **There is no universally best shepherding algorithm; algorithm performance is conditional on information and environment.**

That's a much more meaningful result.

---

# 50. The 2026 papers make this even more relevant

The field is now explicitly moving toward:

* adaptive lead/herd behaviour; ([arXiv][6])
* obstacle-aware non-cohesive multi-robot shepherding; ([arXiv][15])
* predictive control under physical constraints; ([ScienceDirect][24])
* theoretical treatment of decision-making; ([DOI][23])

So a thesis that only reproduces 2014–2022 models would risk looking behind the current frontier.

A thesis that uses those models **as baselines for studying these newer questions** is much stronger.

---

# 51. My proposed literature review structure for your thesis

I would write the state-of-the-art chapter approximately like this:

## 2.1 Shepherding as a multi-agent control problem

Definition, sheepdogs, target agents, goals.

## 2.2 Behavioural shepherding

Strömbom, collect/drive.

## 2.3 Multi-shepherd coordination

Lien, Kubo, consensus, communication-free.

## 2.4 Local sensing and information constraints

FAT, local cameras, bearing-only.

## 2.5 Heterogeneous and non-cohesive populations

Himo, Fujioka, Lama, Tomaselli.

## 2.6 Environmental complexity

Obstacles, corridors, dynamic paths.

## 2.7 Learning and adaptive shepherding

RL, curriculum learning, neuroevolution, context-aware control.

## 2.8 Empirical animal behaviour

Early, Jadhav.

## 2.9 Physical robot implementation

UAV, UGV, MPC, physical validation.

## 2.10 Herdability and theoretical limits

Lama & di Bernardo, continuum/field theory.

## 2.11 Research gap

**Lack of a unified experimental framework for systematically studying the interaction between controller architecture, information, population heterogeneity, environment and herdability.**

## 2.12 HerdSim

Your platform addresses this gap.

---

# 52. The key gap statement I'd investigate

I would currently formulate the gap approximately as:

> Existing shepherding studies have proposed a wide range of behavioural, force-based, decentralized, adaptive and learning-based controllers, but these approaches are generally evaluated within model-specific experimental settings. Consequently, it remains difficult to determine whether observed performance differences arise from the controller itself or from differences in assumptions concerning sensing, flock cohesion, agent heterogeneity, environmental complexity, and physical constraints.

Then:

> **HerdSim can provide a controlled experimental environment in which these assumptions are independently varied while the underlying task, metrics, randomization and statistical procedures remain consistent.**

That is a very strong justification for your platform.

---

# 53. And then your novel contribution becomes clearer

I would not claim:

> "HerdSim is the first shepherding simulator."

That would be unnecessarily risky.

I would aim for:

> **HerdSim provides a modular and reproducible framework for controlled comparative experiments on multi-agent shepherding, enabling systematic investigation of herdability, information requirements, robustness, heterogeneity and generalization across distinct shepherding mechanisms.**

That's much more defensible.

---

# 54. The 20 papers I would put at the center of your reading list

If you don't want to read 100 papers immediately, start with these groups:

### Core foundations

1. **Lien et al. (2005)** — Multiple shepherds. ([Illinois Experts][3])
2. **Strömbom et al. (2014)** — Collect/drive heuristic. ([PubMed Central (PMC)][4])
3. **Tsunoda et al. (2018)** — Local-camera/FAT. ([Taylor & Francis Online][5])
4. **Kubo et al. (2022)** — Force-based multiple dogs.

### Limits / environment

5. **El-Fiqi et al. (2020)** — Limits of reactive shepherding. ([IEEE Xplore][13])
6. **Himo et al. (2022)** — Heterogeneous responsivity. ([AIMS Press][11])
7. **Fujioka et al. (2023)** — Heterogeneous flocks. ([arXiv][10])
8. **Lama & di Bernardo (2024)** — Herdability. ([DOI][1])

### Distributed / information

9. **Campbell et al. (2021)** — Consensus. ([IASEI][7])
10. **Li et al. (2023)** — Communication-free shepherding. ([Frontiers][8])
11. **Bearing-only shepherding** — Information requirements. ([PubMed Central (PMC)][9])

### Adaptive / learning

12. **Hussein et al. (2022)** — Curriculum RL. ([University of Canberra Research Portal][17])
13. **Contextually aware control agents (2024)**. ([Springer][16])
14. **Automatic design / neuroevolution (2024)**. ([arXiv][19])
15. **Hierarchical RL shepherding**. ([arXiv][18])

### Empirical / biological

16. **Early et al. (2020)** — Real dog/sheep behavioural sequences. ([MDPI][22])
17. **Jadhav et al. (2024)** — Real sheep + Border Collie + ABM. ([Nature][20])
18. **King et al. (2023)** — Bio-herding roadmap. ([DOI][26])

### New frontier

19. **Lama et al. (2025)** — Nonreciprocal field theory / decision-making. ([DOI][23])
20. **Strömbom et al. (2026)** — Lead when possible, herd when necessary. ([arXiv][6])
21. **Tomaselli et al. (2026)** — Obstacle-aware non-cohesive multi-robot shepherding. ([arXiv][15])
22. **Tsunoda et al. (2026)** — Predictive shepherding under robot motion constraints. ([arXiv][25])
23. **CMFF + MPC robot herding (2026)** — Predictive physical control. ([ScienceDirect][24])

So actually I'd make your **core bibliography around 23 papers**, with perhaps another 15–20 papers in the extended bibliography.

---

# 55. My ranking of research opportunities for HerdSim

If I rank them by **scientific value × feasibility for your current platform**, I get:

| Rank | Problem                                 | Scientific value | Feasibility |
| ---- | --------------------------------------- | ---------------: | ----------: |
| 🥇   | Herdability phase diagrams              |            ★★★★★ |       ★★★★★ |
| 🥈   | Limited information / sensing           |            ★★★★★ |       ★★★★★ |
| 🥉   | Heterogeneous sheep                     |            ★★★★★ |       ★★★★★ |
| 4    | Generalization under distribution shift |            ★★★★★ |       ★★★★★ |
| 5    | Communication vs performance            |            ★★★★☆ |       ★★★★★ |
| 6    | Adaptive controller switching           |            ★★★★★ |       ★★★★☆ |
| 7    | Failure/resilience                      |            ★★★★☆ |       ★★★★★ |
| 8    | Empirical sheep calibration             |            ★★★★★ |       ★★★☆☆ |
| 9    | Information propagation                 |            ★★★★★ |       ★★★☆☆ |
| 10   | Realistic robot dynamics                |            ★★★★☆ |       ★★★★☆ |
| 11   | RL benchmarking                         |            ★★★★☆ |       ★★★☆☆ |
| 12   | Full physical robot validation          |            ★★★★★ |       ★★☆☆☆ |

---

# 56. If this were my PhD/Master's project, I would choose this

I would make the central research objective:

> **Develop a computational framework to identify the conditions under which multi-agent shepherding succeeds, fails, and generalizes across different population dynamics, sensing capabilities and control strategies.**

Then the contribution is threefold:

### Contribution 1 — Framework

HerdSim.

### Contribution 2 — Methodology

A model-independent experimental/metric framework.

### Contribution 3 — Science

New evidence about:

* herdability;
* sensing requirements;
* heterogeneity;
* robustness;
* generalization.

That is much stronger than "we implemented several algorithms."

---

# 57. The particularly nice thing about this direction

You don't have to solve all of these.

You can make the project progressive:

```text
                     HerdSim
                        │
                 ┌──────┴──────┐
                 │             │
            Existing       New research
            models          questions
                 │             │
         Strömbom/Kubo       herdability
                 │             sensing
                 │             heterogeneity
                 │             robustness
                 │             generalization
                 │
                 └──────┬──────┘
                        ↓
                 common framework
                        ↓
                  new knowledge
```

The existing models are therefore **not the contribution by themselves**. They are the experimental instruments with which you study the new questions.

---

## My strongest recommendation for the next step

Before you implement another algorithm, I would turn this literature analysis into a **formal research requirements specification for HerdSim**.

It should have four levels:

### Level A — What the literature currently assumes

For every paper:

* sheep dynamics;
* dog dynamics;
* number of sheep;
* number of dogs;
* sensing;
* communication;
* heterogeneity;
* obstacles;
* goal;
* noise;
* physical constraints;
* metrics.

### Level B — What each paper actually solves

Not just the algorithm, but:

> **What question did the paper answer?**

### Level C — What remains unanswered

For example:

> Limited sensing has been studied, but limited sensing × heterogeneous sheep × multiple dogs has not been systematically mapped.

### Level D — What HerdSim should provide

For example:

```text
Research gap
     ↓
HerdSim capability
     ↓
experiment
     ↓
metric
     ↓
hypothesis
     ↓
expected scientific contribution
```

That would give you a **requirements matrix + literature matrix + research-question matrix + implementation roadmap**. It would also tell you which features of HerdSim are genuinely necessary and which are merely nice software features.

And, importantly, I would include the **2025–2026 papers as the "frontier" column**, because the new lead/herd, non-cohesive obstacle-aware, decision-theoretic, and predictive robot-control work changes what a state-of-the-art HerdSim should be capable of. ([arXiv][6])

[1]: https://doi.org/10.1103/PhysRevResearch.6.L032012?utm_source=chatgpt.com "Shepherding and herdability in complex multiagent systems | Phys. Rev. Research"
[2]: https://pubmed.ncbi.nlm.nih.gov/25165603/?utm_source=chatgpt.com "Solving the shepherding problem: heuristics for herding autonomous, interacting agents - PubMed"
[3]: https://experts.illinois.edu/en/publications/shepherding-behaviors-with-multiple-shepherds?utm_source=chatgpt.com "Shepherding behaviors with multiple shepherds - Illinois Experts"
[4]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4191104/?utm_source=chatgpt.com "Solving the shepherding problem: heuristics for herding autonomous, interacting agents - PMC"
[5]: https://www.tandfonline.com/doi/full/10.1080/01691864.2018.1539410?utm_source=chatgpt.com "Analysis of local-camera-based shepherding navigation: Advanced Robotics: Vol 32 , No 23 - Get Access"
[6]: https://arxiv.org/abs/2602.16750?utm_source=chatgpt.com "Re-Solving the Shepherding Problem: Lead When Possible, Herd When Necessary"
[7]: https://www.iasei.org/icsi2021/2021_Book_AdvancesInSwarmIntelligence-2.pdf?utm_source=chatgpt.com "| LNCS 12690 | Ying Tan Yuhui Shi (Eds.) Advances"
[8]: https://www.frontiersin.org/journals/control-engineering/articles/10.3389/fcteg.2023.989232/full?utm_source=chatgpt.com "Frontiers | Communication-free shepherding navigation with multiple steering agents"
[9]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11779540/?utm_source=chatgpt.com "Swarm shepherding using bearing-only measurements - PMC"
[10]: https://arxiv.org/abs/2304.03951?utm_source=chatgpt.com "Shepherding Heterogeneous Flocks: Overview and Prospect"
[11]: https://www.aimspress.com/article/doi/10.3934/mbe.2022162?utm_source=chatgpt.com "Iterative shepherding control for agents with heterogeneous responsivity"
[12]: https://www.tandfonline.com/doi/abs/10.1080/01691864.2022.2133552?utm_source=chatgpt.com "Shepherding algorithm for heterogeneous flock with model-based discrimination: Advanced Robotics: Vol 37, No 1-2"
[13]: https://ieeexplore.ieee.org/document/9256255/?utm_source=chatgpt.com "The Limits of Reactive Shepherding Approaches for Swarm Guidance | IEEE Journals & Magazine | IEEE Xplore"
[14]: https://www.nature.com/articles/s41598-024-65894-5?utm_source=chatgpt.com "Reactive shepherding along a dynamic path | Scientific Reports"
[15]: https://arxiv.org/abs/2604.22327?utm_source=chatgpt.com "Multi-robot obstacle-aware shepherding of non-cohesive target agents"
[16]: https://link.springer.com/article/10.1007/s11721-024-00235-w?utm_source=chatgpt.com "Contextually aware intelligent control agents for heterogeneous swarms | Swarm Intelligence | Springer Nature Link"
[17]: https://researchprofiles.canberra.edu.au/en/publications/autonomous-swarm-shepherding-using-curriculum-based-reinforcement/?utm_source=chatgpt.com "Autonomous Swarm Shepherding Using Curriculum-Based Reinforcement Learning - University of Canberra Research Portal"
[18]: https://arxiv.org/abs/2004.11543?utm_source=chatgpt.com "Continuous Deep Hierarchical Reinforcement Learning for Ground-Air Swarm Shepherding"
[19]: https://arxiv.org/abs/2404.18221?utm_source=chatgpt.com "Automatically designing robot swarms in environments populated by other robots: an experiment in robot shepherding"
[20]: https://www.nature.com/articles/s42003-024-07245-8?utm_source=chatgpt.com "Collective responses of flocking sheep (Ovis aries) to a herding dog (border collie) | Communications Biology"
[21]: https://github.com/tee-lab/collective-responses-of-flocking-sheep-to-herding-dog?utm_source=chatgpt.com "GitHub - tee-lab/collective-responses-of-flocking-sheep-to-herding-dog: This repository contains codes for data and agent-based model analysed in the article \"Collective responses of flocking sheep (Ovis aries) to a herding dog (border collie)\". · GitHub"
[22]: https://www.mdpi.com/2076-2615/10/2/352?utm_source=chatgpt.com "Sequential Analysis of Livestock Herding Dog and Sheep Interactions | MDPI"
[23]: https://doi.org/10.1038/s41467-025-63071-4?utm_source=chatgpt.com "Nonreciprocal field theory for decision-making in multi-agent control systems | Nature Communications"
[24]: https://www.sciencedirect.com/science/article/abs/pii/S016816992600709X?utm_source=chatgpt.com "A robot herding strategy combining CMFF and MPC for shepherding - ScienceDirect"
[25]: https://arxiv.org/abs/2604.17189?utm_source=chatgpt.com "Shepherding UAV Swarm with Action Prediction Based on Movement Constraints"
[26]: https://doi.org/10.1111%2F2041-210X.14049?utm_source=chatgpt.com "Biologically inspired herding of animal groups by robots - King - 2023 - Methods in Ecology and Evolution - Wiley Online Library"
