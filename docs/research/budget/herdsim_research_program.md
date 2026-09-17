# HerdSim Research Program: Scaling Laws of Collective Control

## 1. Scientific Goal
This project asks a single, progressively deeper question:
> **How does the amount of external control required to reliably steer a collective scale with its size and internal structure, and which parts of that scaling are properties of the collective rather than of a particular control method?**

## 2. Model System
HerdSim provides a controlled simulation environment in which external agents (shepherds) steer a collective (a flock) without directly controlling its individual members. It serves as a model system to measure control demand in collective systems.

## 3. Central Quantity
The central object of the entire research program is **$D_{\min}(N, X)$**.

Where:
*   **$N$** = collective size (number of agents)
*   **$X$** = internal structure of the collective (e.g., spread, fragmentation)
*   **$D_{\min}$** = the smallest number of controllers needed to reach a chosen reliability under a fixed task condition.

The research program is defined by the progressive extension of this quantity:
$D_{\min}(N) \rightarrow D_{\min}(N, X) \rightarrow D_{\min,m}(N, X)$

## 4. Research Questions

### RQ1 — Size
**How does control demand change as the collective becomes larger?**
*Focus:* $D_{\min}(N)$

### RQ2 — Structure
**Is size alone enough, or does internal structure change control demand?**
*Focus:* $D_{\min}(N, X)$

### RQ3 — Mechanism
**What features of the collective create the observed scaling?**
*Focus:* Exploring mechanisms like spatial spread, fragmentation, spatial coverage, and controller interference to explain *why* the scaling behaves the way it does.

### RQ4 — Generality
**Does the scaling relationship remain when the control method changes?**
*Focus:* $D_{\min,m}(N, X)$ for different control methods $m$. Are phenomena like "overcrowding collapse" universal structural bounds, or just artifacts of specific algorithm designs?

### RQ5 — Extensions
**Can information, time, or other resources change the scaling relationship?**
*Focus:* Once the basic physical scaling is understood, we ask if giving controllers more information ($I$) or more time ($T$) fundamentally shifts the demand.

## 5. Research Strategy
The project follows a strict linear progression, where every step explains, qualifies, or tests the scaling relationship:
**Size $\rightarrow$ Structure $\rightarrow$ Mechanism $\rightarrow$ Cross-Method Test $\rightarrow$ Extensions $\rightarrow$ Validation.**

## 6. What Would Count as a Result
We deliberately do not define success simply as "finding a power law." The scientific target is open. 

Possible outcomes include:
*   Simple scaling with $N$
*   Structure-dependent scaling
*   Multiple distinct scaling regimes
*   Method-dependent scaling
*   Shared scaling structure across entirely different methods
*   Eventually, perhaps a normalized/general scaling relationship (a universal control ratio).

## 7. Validation
A scaling relationship is only as good as its predictive power. We will test the discovered relationship on:
*   Unseen collective sizes
*   Unseen structures
*   Different controller configurations
*   Different control methods
*The strongest evidence of success is prediction without refitting.*

## 8. Scope and Limitations
HerdSim is a model system. Claims initially apply only to the simulated collective-control setting. Generalization to real-world livestock, drone swarms, or crowd control requires additional physical validation outside the scope of this project.

## 9. Extensions (Future Work)
Topics that are useful but scientifically downstream from the core scaling question are deferred to future extensions. These include:
*   **Early Warning Systems:** Predicting imminent control failure in real-time.
*   **Information Substitution:** Deep dives into the multidimensional control budget.
*   **Algorithm Optimization:** Finding the absolute "best" controller.
