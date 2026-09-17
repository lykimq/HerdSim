# HerdSim Research Program: Scaling Laws of Indirect Control

**Central Objective:** To understand how many controllers (like shepherds or drones) it takes to reliably steer a group, and how that number changes as the group gets larger or changes shape. We want to discover if these "scaling rules" apply universally, regardless of the specific control algorithm used.

## 1. The Core Scientific Question

Herding provides a controlled experimental testbed. We can change the flock size, the number of shepherds, the algorithms they use, and precisely measure how often they succeed. 

We aren't just trying to build the "best" herding algorithm. We want to discover the fundamental rules of collective control.

The main question is:
> **How does the minimum number of controllers required for reliable steering scale with the size and structure of the group?**

To answer this, we look at a few key factors:
*   **Flock Size ($N$):** How many individuals are in the group?
*   **Structure ($X$):** Is the group tightly packed, spread out, or split into pieces?
*   **Controller Count ($D$):** How many shepherds/drones are doing the work?
*   **Information & Time ($I, T$):** What do the controllers know, and how long do they have to complete the task?

The primary metric we are trying to predict is the **Minimum Control Demand ($D_{\min}$)** — the absolute fewest controllers needed to guarantee a high success rate (e.g., 90% reliability). We want to understand what drives this demand.

---

## 2. The Four Levels of Inquiry

Our research progresses through four increasingly deep questions:

1.  **What scales?** Does the number of required controllers grow predictably as the flock gets larger?
2.  **What determines the scaling?** Is flock size the only thing that matters, or does the shape and structure of the flock change the requirement?
3.  **Why does it scale this way?** What physical interactions (e.g., controllers getting in each other's way) cause these limitations?
4.  **Is the scaling universal?** Do these rules still apply if we use completely different control algorithms?

---

## 3. The Eight-Phase Experimental Roadmap

### Phase I: Establish the Baseline Scaling Law
*   **Goal:** Find out if there is a predictable mathematical rule linking flock size to the number of controllers needed.
*   **How:** Keep everything constant except the flock size and the number of controllers. Test a range of flock sizes.
*   **Success looks like:** Finding a mathematical curve that can accurately predict the required controllers for *new, untested* flock sizes.

### Phase II: Does Flock Structure Matter?
*   **Goal:** Determine if two flocks of the exact same size, but different shapes, require different amounts of control.
*   **How:** Keep the flock size the same but change their starting shape (e.g., compact, spread out, split in two, or with many stragglers).
*   **Success looks like:** Proving whether flock size is the only important variable, or if we must account for the flock's structure.

### Phase III: Pinpoint the Crucial Structural Variables
*   **Goal:** Figure out exactly *which* aspects of the flock's shape drive the need for more controllers.
*   **How:** Analyze metrics like spread, fragmentation, and outlier count to see which ones best predict the minimum controller requirement.
*   **Success looks like:** Creating a "collective complexity" score that perfectly predicts how hard a group will be to herd.

### Phase IV: Uncover the Underlying Mechanisms
*   **Goal:** Explain *why* the rules from Phases I-III exist. For example, why does adding too many shepherds eventually cause the herd to break apart?
*   **How:** Measure phenomena like controllers interfering with one another, or redundant coverage. Then, actively intervene (e.g., force shepherds to ignore each other) to prove causality.
*   **Success looks like:** Moving beyond correlation to prove exactly what physical interactions cause control limits.

### Phase V: Test Across Different Algorithms
*   **Goal:** Prove that our findings are fundamental truths about controlling groups, not just quirks of one specific algorithm.
*   **How:** Rerun the core experiments using entirely different herding logic. Critically, we will track where algorithms fail. For instance, is there always a "maximum controller limit" ($D_{\max}$) where adding more shepherds causes chaos (overcrowding), regardless of the algorithm used?
*   **Success looks like:** Discovering that different algorithms share the same scaling shape and the same generic overcrowding limits.

### Phase VI: Search for a Universal "Control Ratio"
*   **Goal:** Create a single, universal mathematical relationship that works for any scenario.
*   **How:** We will try to define a ratio ($\Pi$) of "Control Capacity" (what the shepherds can do) divided by "Control Demand" (what the flock requires).
*   **Success looks like:** Showing that wildly different scenarios (different flock sizes, shapes, and algorithms) all collapse onto one single predictability curve when plotted using this ratio.

### Phase VII: Trade-offs with Information and Time
*   **Goal:** See if physical controllers can be swapped out for better sensors or more time.
*   **How:** Give the controllers more information (e.g., global radar instead of local sight) and see if the required number of physical controllers drops.
*   **Success looks like:** Quantifying the exact "exchange rate" between physical robots and better information.

### Phase VIII: The Ultimate Blind Test
*   **Goal:** Rigorously validate the discovered laws.
*   **How:** Test the scaling laws on completely new flock sizes, structures, and algorithms that the models have never seen before.
*   **Success looks like:** Successfully predicting the exact controller requirements in these brand new scenarios.

---

## 4. Defining Success

We define success in stages:

*   **Good:** We prove a reliable scaling rule based on flock size.
*   **Better:** We prove that flock structure is just as important as size in determining control demand.
*   **Great:** We prove that these structural scaling rules—and the limits of overcrowding—apply across multiple different algorithms.
*   **Exceptional:** We discover a universal "Control Ratio" that flawlessly predicts success in totally unseen, novel scenarios.

> *HerdSim is not just a simulator for herding algorithms; it is a controlled physics laboratory for discovering the universal laws of collective control.*
