# HerdSim Research Program: Scaling Laws of Collective Control

## 1. Scientific Goal
This project asks a single, progressively deeper question:
> **How does the amount of external control required to reliably steer a collective scale with its size and internal structure, and which parts of that scaling are properties of the collective rather than of a particular control method?**

Our fundamental hypothesis is intentionally modest: *The control required to reliably steer a collective changes systematically with collective size and structure, and some features of this scaling may remain consistent across different control methods.* 

We do not assume the answer is a power law, nor do we presuppose a complex multidimensional interaction. The experiments will determine the true functional form.

## 2. Model System
HerdSim provides a controlled simulation environment in which external agents (shepherds) steer a collective (a flock) without directly controlling its individual members. It serves as a model system to measure **control demand** in collective systems.

## 3. Central Quantity
The conceptual centerpiece of the entire research program is **Control Demand**: the minimum number of controllers required to achieve a specified level of reliability for a specified task.

We define this as **$D_{\min}(N, X)$**, where:
*   **$N$** = collective size (number of agents)
*   **$X$** = internal structure of the collective (e.g., spread, fragmentation)

The research program is defined by the intuitive mathematical progression of this quantity:
$$D_{\min}(N) \rightarrow D_{\min}(N, X) \rightarrow D_{\min,m}(N, X) \rightarrow D_{\min}(N, X, I, T)$$

## 4. Research Questions

### RQ1 — Size Scaling
**How does minimum control demand change as collective size increases?**
*Focus:* $D_{\min}(N)$. We seek to determine the functional form of the scaling relationship. A power law could be the result, but so could piecewise scaling, saturation, a threshold, or a more complex function. 

### RQ2 — Structural Scaling
**At the same collective size, how does internal structure change control demand?**
*Focus:* $D_{\min}(N, X)$. Is size alone enough, or do properties like spread and fragmentation fundamentally alter the demand?

### RQ3 — Mechanisms
**What collective and controller-level processes produce the observed scaling and its breakdown?**
*Focus:* Exploring mechanisms like spatial spread, fragmentation, spatial coverage, and controller interference to explain *why* the scaling behaves the way it does. Within the scaling relationship, are there distinct regions where additional control becomes ineffective or harmful (overcrowding)?

### RQ4 — Cross-Method Generality
**Which features of the scaling relationship remain when the control method changes?**
*Focus:* $D_{\min,m}(N, X)$ for different control methods $m$. This tests the generality of the *scaling*, not just the mechanism. It asks if the collective determines the underlying scaling structure, while the control method merely changes the prefactor (efficiency).

### RQ5 — Resource Extensions
**How do information and time change the control demand?**
*Focus:* $D_{\min}(N, X, I, T)$. Once the basic physical scaling is understood, can providing controllers with more information ($I$) or more time ($T$) reduce the physical demand?

### RQ6 — Generalization and Prediction
**Can the discovered relationship predict control demand for unseen collective sizes, structures, and methods?**
*Focus:* The ultimate test of the scaling law. The strongest evidence of success is prediction without refitting.

## 5. Research Strategy
The project follows a strict linear progression, where every step explains, qualifies, or tests the scaling relationship:
**Size $\rightarrow$ Structure $\rightarrow$ Mechanism $\rightarrow$ Cross-Method Test $\rightarrow$ Extensions $\rightarrow$ Validation.**

Previous work (e.g., our 2025 paper) found preliminary evidence that required shepherd count increases with flock size and relates to spread. This new program asks: *What is the underlying scaling relationship, what aspects of collective structure determine it, why does it take that form, and does it persist across control methods?*

## 6. What Would Count as a Result
We do not define success as "finding a power law." Possible outcomes include:
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

## 8. Scope and Limitations
HerdSim is a model system. Claims initially apply only to the simulated collective-control setting. Generalization to real-world livestock, drone swarms, or crowd control requires additional physical validation outside the scope of this project.

## 9. Extensions (Future Work)
Topics that are useful but scientifically downstream from the core scaling question are deferred to future extensions. These include:
*   **Early Warning Systems:** Predicting imminent control failure in real-time.
*   **Information Substitution:** Deep dives into the multidimensional control budget.
*   **Algorithm Optimization:** Finding the absolute "best" controller.
