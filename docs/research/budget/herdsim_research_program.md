# HerdSim Research Program: Scaling Laws of Indirect Control

> **Central Objective:** To determine how the control capacity required to reliably steer a collective scales with the size and structure of that collective, and to identify which components of this scaling persist across different control algorithms.

## 1. Scientific Vision & Central Question

Herding provides a controlled experimental system in which the collective can be systematically varied, the number of controllers controlled, algorithms changed, and success measured. The ultimate goal is *not* to identify the best herding algorithm, but to determine whether there are **structural scaling relationships governing collective control that persist across different control algorithms.**

The primary question is:

> **How does the minimum control capacity required for reliable collective steering scale with collective size and structure?**

Define $R_m(N,D,X,I,T)$ as the probability of successful control, where:
*   **$N$** = collective population size
*   **$D$** = number of controllers/shepherds
*   **$X$** = collective structural state (geometry, fragmentation, outliers, etc.)
*   **$I$** = information available to the controllers
*   **$T$** = available control time
*   **$m$** = control algorithm

For a required reliability $\theta$, define the minimum control demand:
$$D_{\min,m}(N,X,I,T;\theta) = \min_D \{D : R_m(N,D,X,I,T) \geq \theta\}$$

This function is the **central object of the research program.** Everything else exists to understand this function.

---

## 2. The Four Levels of Inquiry

The program progresses through four increasingly general questions:

1.  **What scales?** $D_{\min}(N)$ - Does the control requirement systematically change with population size?
2.  **What determines the scaling?** $D_{\min}(N,X)$ - Does population size alone explain control demand, or does internal structure matter?
3.  **Why does the scaling occur?** Identify the mechanisms (spatial coverage, directional conflict, interference, etc.).
4.  **Is the scaling generic?** Compare algorithms to determine which features are algorithm-specific, algorithm-robust, or generic.

---

## 3. The Research Phases

### Phase I: Establish the baseline scaling law
**Objective:** Determine if there is a reproducible relationship between collective size and control demand.
*   **Method:** Fix all variables except $N$ and $D$. Use one baseline algorithm (e.g., `strombom_multi`).
*   **Experiment:** Measure $R(N,D)$ and estimate $D_{\min}(N;\theta)$ for an initial range (e.g., $N = 10, 20, 40, 80, 160$).
*   **Goal:** Test candidate models (linear, power-law, saturating). **Critical requirement:** The fitted relationship must predict $D_{\min}$ for *unseen* population sizes.

### Phase II: Determine whether population size is sufficient
**Objective:** Test if collectives with identical $N$ but different structures $X$ have different control demands.
*   **Method:** Systematically vary spatial organization (compact, dispersed, elongated, fragmented, outlier-rich) while holding $N$ fixed.
*   **Experiment:** Measure $D_{\min}(N,X)$ and compare variance explained against $D_{\min}(N)$.
*   **Goal:** Establish whether population size is the fundamental variable, or if structure is required.

### Phase III: Discover the relevant structural variables
**Objective:** Find the minimum description of collective structure needed to predict control demand.
*   **Method:** Analyze which components of $X$ (Spread $S$, Fragmentation $F$, Outliers $O$, etc.) drive the scaling.
*   **Goal:** Discover relationships like $D_{\min} \sim N^\alpha S^\beta$ or derive a composite collective-complexity measure $C(X)$ such that $D_{\min} = f(N,C)$.

### Phase IV: Identify the mechanisms generating the scaling
**Objective:** Explain *why* the observed relationship exists.
*   **Method:** Measure candidate mechanisms (spatial coverage, directional conflict, controller interference, redundancy, saturation).
*   **Experiment:** Perform **interventions** (e.g., reduce interference, enforce spatial assignment) to see if changing the mechanism shifts $D_{\min}$. Causality over correlation.

### Phase V: Test algorithm independence
**Objective:** Move from a HerdSim-specific result to a collective-control result, and determine if generic "herdability regimes" exist independently of specific algorithms.
*   **Method:** Repeat the core scaling experiments using substantially different controllers. Critically, track not just the minimum controllers required ($D_{\min}$), but the full regime boundaries: $D_{\text{overcrowd}}$ (the point where adding controllers reduces reliability) and $D_{\max}$ (the absolute maximum controllers before failure).
*   **Goal:** Determine if algorithms share a common exponent, a common functional structure, and whether phenomena like "overcrowding collapse" ($D > D_{\text{overcrowd}}$) are universal structural bounds of collective control or merely artefacts of specific algorithm designs.

### Phase VI: Search for a generic control-capacity variable
**Objective:** Find a dimensionless collapse of the scaling laws.
*   **Method:** Define a ratio $\Pi = \frac{\text{available control capacity}}{\text{collective control demand}}$.
*   **Goal:** Test the hypothesis that reliability takes a universal form $R \approx F(\Pi)$. If successful, radically different systems (different $N$, $D$, $X$, algorithms) will collapse onto a common curve.

### Phase VII: Extend the scaling to information and time
**Objective:** Determine if physical control, information, and time are interchangeable resources.
*   **Method:** Introduce information $I$ and time $T$ as variables: $D_{\min} = f(N,X,I,T)$.
*   **Goal:** Verify if the core scaling structure survives when available resources change, and quantify the exchange rates (e.g., $D=4, I_{\text{low}} \approx D=3, I_{\text{high}}$).

### Phase VIII: Out-of-sample validation
**Objective:** Rigorous scientific validation of the discovered laws.
*   **Method:** Test the established scaling laws on conditions they have never seen (held-out $N$, held-out structures, held-out algorithms).
*   **Goal:** Prove the scaling captures something fundamental rather than merely overfitting the experimental grid.

---

## 4. The Experimental Roadmap

1.  **Exp A1 (Population scaling):** $(N,D) \rightarrow R \implies D_{\min}(N)$
2.  **Exp A2 (Scaling validation):** Predict unseen $N$. Output: Validated baseline scaling law.
3.  **Exp B1 (State scaling):** $(N,X,D) \rightarrow R \implies D_{\min}(N,X)$
4.  **Exp B2 (Structural reduction):** Determine which components of $X$ matter. Output: Collective structural complexity representation.
5.  **Exp C1 (Mechanism measurement):** Measure coverage, interference, fragmentation.
6.  **Exp C2 (Mechanism intervention):** Modify mechanism logic. Output: Causal/mechanistic evidence.
7.  **Exp D1 (Cross-algorithm scaling):** Repeat core grid for algorithms $m$. Output: $D_{\min,m}(N,X)$.
8.  **Exp D2 (Universality test):** Output: Algorithm-independent vs dependent components.
9.  **Exp E1 (Information scaling):** $D_{\min}(N,X,I)$. Output: Information-control tradeoff.
10. **Exp E2 (Time scaling):** $D_{\min}(N,X,I,T)$. Output: Time-control tradeoff.
11. **Exp F1 (Scaling collapse):** Search for $\Pi$ such that $R \approx F(\Pi)$. Output: Candidate generic law.
12. **Exp F2 (Blind validation):** Test on completely new configurations.

---

## 5. Success Conditions

*   **Minimum success:** Demonstrate reproducible scaling of control demand with population size.
*   **Stronger success:** Show that collective structure explains systematic deviations from simple population scaling.
*   **Stronger still:** Show that the same structural scaling persists across different control algorithms.
*   **Major success:** Identify a dimensionless control-capacity variable ($\Pi$) that produces approximate scaling collapse across populations and structures.
*   **Exceptional outcome:** Demonstrate that this same relationship predicts previously unseen collective states and control architectures.

---
*HerdSim provides a controlled computational experimental framework for discovering and testing scaling relationships between collective structure and the control capacity required for reliable collective steering.*
