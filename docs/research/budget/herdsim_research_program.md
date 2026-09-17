# HerdSim Research Program

## Scaling Laws of Collective Control

### 1. Goal

This project asks a simple question:

> **How does the amount of control needed to reliably steer a collective grow as the collective becomes larger or more complex?**

HerdSim uses collective herding as a controlled setting for studying this question.

The immediate system is a group of agents being steered by a small number of shepherds. The broader goal is to understand whether there are general rules for controlling a collective without directly controlling each individual member.

The project has two main goals:

1. **Find how control demand scales with the size and structure of a collective.**
2. **Determine which parts of this scaling remain the same when the control method changes.**

The second goal is important. A relationship found with one shepherding algorithm may simply be a property of that algorithm. The project therefore treats different algorithms as different ways of testing the same underlying problem.

---

# 2. The central idea

Let:

* \(N\) = number of agents in the collective
* \(X\) = structure of the collective
* \(D\) = number of external controllers
* \(D_{\min}\) = minimum number of controllers needed to achieve a chosen level of reliability

The main quantity of interest is:

$$
D_{\min}(N,X)
$$

The first question is whether \(D_{\min}\) changes systematically with \(N\).

The next question is whether two collectives with the same \(N\) can require different amounts of control because their structures are different.

For example, a compact group and a widely spread or fragmented group may contain the same number of agents but present very different control demands.

The project therefore moves from:

$$
D_{\min}(N)
$$

to:

$$
D_{\min}(N,X).
$$

The exact form of this relationship is not assumed in advance.

A power law is one possibility:

$$
D_{\min}\propto N^\alpha
$$

but the data may instead support a different relationship, several scaling regions, or a more useful description based on collective structure.

---

# 3. What does "scaling" mean here?

Scaling means studying **how the amount of control changes when the size or structure of the collective changes**.

For example, if doubling the number of agents requires only 50% more control, control demand is growing differently than if it requires twice as much control.

The important question is not simply to find an exponent.

The goal is to determine:

> **What properties of a collective determine how much control it requires?**

This includes asking whether population size is enough to explain the control demand, or whether properties such as spread, fragmentation, density, or the presence of outliers are also important.

---

# 4. Research path

The project follows a simple progression.

```text
Collective size
      ↓
Collective structure
      ↓
Control demand
      ↓
Scaling relationship
      ↓
Why does the relationship occur?
      ↓
Does it survive different control methods?
      ↓
Can we describe the result in a general form?
```

Each step depends on the previous one.

---

# 5. Stage 1 — Scaling with collective size

### Question

> How does the required control capacity change as the collective becomes larger?

Start with one well-defined control method and a simple, controlled collective state.

Vary:

* collective size \(N\)
* number of controllers \(D\)

and measure the probability of successful steering.

From these experiments, estimate:

$$
D_{\min}(N).
$$

### Goal

Determine the basic scaling behaviour.

Possible outcomes include:

* approximately linear growth
* sublinear growth
* superlinear growth
* different scaling regions
* saturation
* or no simple scaling relationship.

No particular form is assumed beforehand.

### Important test

The resulting relationship must be tested on collective sizes that were not used to construct it.

The goal is therefore not simply to fit the existing experiments, but to determine whether the relationship can predict new cases.

---

# 6. Stage 2 — Scaling with collective structure

### Question

> Is the number of agents enough to predict control demand?

Keep \(N\) fixed while changing the structure of the collective.

Examples include:

* compact groups
* widely spread groups
* elongated groups
* fragmented groups
* groups with outliers

Measure how these changes affect:

$$
D_{\min}.
$$

The goal is to determine whether:

$$
D_{\min}=f(N)
$$

is sufficient, or whether a better description is:

$$
D_{\min}=f(N,X).
$$

Here, \(X\) represents measurable properties of the collective.

The project should not assume which properties matter most. Spread, fragmentation, density, connectivity, and outliers are candidate explanations that can be tested.

---

# 7. Stage 3 — Find what drives the scaling

Once a relationship between collective structure and control demand has been observed, ask:

> **Why does this relationship exist?**

Several mechanisms may contribute.

For example:

### Spatial demand

A larger or more dispersed collective may require controllers to influence more spatially separated regions.

### Fragmentation

A collective that separates into several groups may require controllers to deal with several control problems at once.

### Controller interference

Adding controllers may eventually cause them to work against each other.

### Redundant control

Additional controllers may stop adding useful control even though they continue to consume resources.

These are possible explanations, not assumptions.

The experiments will measure the relevant quantities during the simulations and test whether changes in these quantities are linked to changes in control demand.

Where possible, the project will also change the suspected mechanism directly. This is important because observing that two things occur together does not by itself show that one causes the other.

---

# 8. Stage 4 — Test different control methods

### Question

> **Which parts of the scaling are properties of the collective, and which are properties of the control method?**

Repeat the main scaling experiments using substantially different shepherding methods.

For each method \(m\), measure:

$$
D_{\min,m}(N,X).
$$

The comparison is not primarily about deciding which algorithm is better.

Instead, ask whether the **shape of the scaling relationship** remains similar.

For example, different methods may have different efficiency:

$$
D_{\min,A}=a_A f(N,X)
$$

$$
D_{\min,B}=a_B f(N,X)
$$

while sharing the same underlying function \(f\).

If this happens, the algorithms differ in their efficiency but the collective may impose a common scaling structure.

Alternatively, the scaling may change substantially between methods. That would show that the observed relationship is strongly tied to the control architecture.

Both outcomes are informative.

---

# 9. Stage 5 — Add information and time

Once the basic scaling relationship is understood, the project can examine other control resources.

The first extension is information.

For example:

* local versus global observation
* limited versus extended sensing
* no communication versus shared information

The question is:

> **Can better information reduce the amount of physical control required?**

This extends the basic relationship to:

$$
D_{\min}(N,X,I).
$$

where \(I\) represents the available information.

A second extension is time.

A collective may require more controllers to achieve a goal quickly than to achieve the same goal given more time.

The relationship can therefore eventually be extended to:

$$
D_{\min}(N,X,I,T).
$$

These experiments are extensions of the main scaling problem, not separate research goals.

---

# 10. Stage 6 — Look for a general description

The final goal is to determine whether the observations can be described by a more general measure of control demand.

One possibility is that the important quantity is not the number of controllers alone, but the ratio between available control and the difficulty of the collective:

$$
\Pi =
\frac{\text{available control capacity}}
{\text{collective control demand}}.
$$

If such a quantity can be identified, different experiments may follow a common relationship:

$$
R \approx F(\Pi)
$$

where \(R\) is the probability of successful control.

This would allow systems with different population sizes, structures, and control methods to be compared using the same underlying measure.

This is an open research goal, not an assumption of the project.

---

# 11. Stage 7 — Test the result on new cases

A scaling relationship is useful only if it can describe cases beyond those from which it was constructed.

The final tests will therefore use conditions that were not used to discover the relationship.

Examples include:

* new collective sizes
* new collective structures
* new controller configurations
* different control methods

The strongest test is whether a relationship discovered in one set of experiments can predict another set without being refitted.

This provides a direct test of whether the scaling captures something general rather than simply describing the simulation data.

---

# 12. What the project is trying to discover

The project is deliberately open about the final form of the answer.

Several outcomes are possible.

### Outcome 1 — Simple scaling

Control demand follows a reasonably simple relationship with collective size:

$$
D_{\min}\sim N^\alpha.
$$

### Outcome 2 — State-dependent scaling

Population size alone is insufficient:

$$
D_{\min}=f(N,X).
$$

### Outcome 3 — Algorithm-dependent scaling

Different control methods produce different scaling relationships.

### Outcome 4 — Shared scaling structure

Different methods have different efficiencies but share the same underlying dependence on collective size and structure:

$$
D_{\min,m}=a_m f(N,X).
$$

### Outcome 5 — General control-capacity relationship

Different collective sizes, structures, and control methods can be described by a common normalized measure of control capacity.

The project should not assume which of these outcomes will occur.

---

# 13. What would count as a strong result?

The project has several levels of possible contribution.

### First level

Show that control demand changes systematically with collective size.

### Second level

Show that collective structure explains important differences that population size alone cannot explain.

### Third level

Identify mechanisms that explain why control demand changes.

### Fourth level

Show that important parts of the scaling persist across different control methods.

### Strongest outcome

Find a simple, testable relationship that describes control demand across different collective sizes, structures, and control methods, and successfully predicts cases that were not used to develop it.

The project should claim only the level supported by the experiments.

---

# 14. Role of HerdSim

HerdSim is not intended to prove that one particular shepherding algorithm is optimal.

Its role is to provide a controlled environment in which the relationship between **collective structure and control demand** can be measured systematically.

The simulation makes it possible to vary one factor at a time, repeat experiments under controlled conditions, compare different control methods, and record the internal state of the collective throughout each experiment.

This makes shepherding a useful model problem for studying a broader question:

> **How much external control is required to reliably steer a collective?**

The results should initially be interpreted as results about the simulated system. Applying them to real livestock, robot teams, crowds, or other collective systems would require additional validation.

---

# 15. What is deliberately not part of the core goal

The following are useful extensions, but they are not required to answer the central question:

* predicting failure in real time
* optimizing a particular shepherding algorithm
* finding the best controller
* reproducing real livestock behaviour in every detail
* immediately transferring the results to other collective systems

These can be studied later if the scaling results provide a reason to do so.

The core project remains:

$$
\boxed{
\text{Collective size and structure}
\rightarrow
\text{control demand}
\rightarrow
\text{scaling}
\rightarrow
\text{generality}
}
$$

---

# 16. Summary

The research program can therefore be reduced to four questions:

### 1. Size
**How does control demand change as the collective gets larger?**
$$
D_{\min}(N)
$$

### 2. Structure
**How does the internal structure of the collective change that demand?**
$$
D_{\min}(N,X)
$$

### 3. Cause
**What creates the observed scaling?**

### 4. Generality
**Which parts of the scaling remain when the control method changes?**

If these questions can be answered, the project can then ask the broader question:

> **Can the control of different collectives be described by a common scaling principle?**

That is the long-term goal of HerdSim.
