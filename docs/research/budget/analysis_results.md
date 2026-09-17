# Honest Review: Shepherding Budget Agenda vs. Sheep-Scaling Paper 2025

## 1. What the Sheep-Scaling Paper 2025 Already Does

The paper ([sheep-scaling_paper2025.pdf](file:///home/quyen/HerdSim/docs/papers/sheep-scaling_paper2025.pdf)) is a solid empirical study with a **narrow, clearly answered scope**:

| What it does well | Limitation |
|---|---|
| 11,000 runs (110 conditions × 100 seeds) — strong stats | **One method only** (its own Strombom-derived model) |
| Reports `D_min(N)` and `D_max(N)` with overcrowding evidence | No multi-method comparison; no transfer claims |
| Introduces mean-spread `S̄` as a macro-predictor of success | `S̄` tested only inside its own model |
| Identifies overcrowding at high D for small N (e.g. D≥15, N=10 → SR drops to 70%) | Treats overcrowding anecdotally — no formal regime taxonomy |
| Clean experimental tables (Table III, Appendix E) | Budget = only `(D, N)`; no time or effort cost analysis |
| Density-gradient as a local GCM approximation (RQ3) | Biological modeling contribution, not a controllability contribution |

**Its RQs in brief:**
- RQ1: How does the viable `[D_min, D_max]` interval change with N?
- RQ2: Can a flock macro-measure (mean-spread) predict required D?
- RQ3: How can sheep maintain GCM attraction from local info?

These are **descriptive/correlational questions** inside a single model. The paper does not ask *why* the frontier has the shape it does, whether it transfers to other methods, or what resources besides dog-count matter.

---

## 2. What the Shepherding Budget Agenda Adds

The [shepherding_budget_agenda.md](file:///home/quyen/HerdSim/docs/research/shepherding_budget_agenda.md) reframes the problem from "how many dogs?" to "what budget achieves reliable herding?" This is a **conceptual upgrade**, not just more experiments. Here's my question-by-question assessment:

### Spine Questions (Q1–Q4)

#### Q1 — Budget Frontier

> For a fixed task and reliability threshold, which budget combinations `B=(D,T,E)` achieve reliable herding as N grows?

| Criterion | Assessment |
|---|---|
| **Novelty vs. paper** | 🟢 **High.** The paper only sweeps `(N, D)`. Adding time budget `T` and effort `E` as first-class coordinates creates a multi-dimensional Pareto analysis that nobody has published for shepherding. |
| **Field value** | 🟢 **High.** The multi-robot community already thinks in terms of multi-resource budgets (energy, time, communication). Shepherding is weirdly behind on this. Bringing this framing in closes a genuine gap. |
| **Feasibility** | 🟢 HerdSim already records time and path length. This is mostly an analysis-layer upgrade. |

#### Q2 — Regime Taxonomy

> Where are under-budget / efficient / wasteful / overcrowding / hard-failure regimes?

| Criterion | Assessment |
|---|---|
| **Novelty vs. paper** | 🟡 **Medium-High.** The paper *observes* overcrowding but doesn't name or formalize regimes. The agenda's five-regime taxonomy is genuinely new vocabulary for the field. |
| **Field value** | 🟢 **High.** The overcrowding effect is known anecdotally (see recent literature on "coordination tax" and non-linear scalability). Nobody has published a formal regime taxonomy with crisp definitions and boundary estimates. This is the kind of framework that other papers would cite and reuse. |
| **Risk** | 🟡 The "wasteful overspend" regime (high R but bad efficiency) may be hard to distinguish cleanly from "overcrowding" without very sharp definitions. You need to be rigorous here. |

#### Q3 — Method Transfer

> Which frontier properties transfer across herding methods?

| Criterion | Assessment |
|---|---|
| **Novelty vs. paper** | 🟢 **Very High.** The paper is single-method. Nobody in the shepherding literature has published comparative frontiers across methods under locked protocols. Lama & di Bernardo (2024) derive scaling laws but also for a single (non-cohesive) model. |
| **Field value** | 🟢🟢 **This is the most valuable question in the agenda.** If you can show that certain regime structures (e.g., overcrowding always happens) are method-invariant while exact `D_min` values are method-specific, that is a **high-impact finding**. Even a negative result ("nothing transfers") would be important — it would caution the field against generalizing from single-model studies. |
| **Risk** | 🔴 **Execution difficulty.** You need 3–4 working instruments in HerdSim, all running under the exact same task/seed/metric protocol. This is the hardest implementation requirement. |

#### Q4 — Scaling Shape

> Is `D_min(N)` sublinear, piecewise, method-dependent?

| Criterion | Assessment |
|---|---|
| **Novelty vs. paper** | 🟡 **Medium.** The paper shows `D_min(N)` implicitly in Table III. Lama & di Bernardo already claim `D* ∝ √M` for non-cohesive targets. Your added value is: (a) cohesive flocks, (b) multi-method comparison, (c) checking if piecewise fits beat power-law fits. |
| **Field value** | 🟢 Moderate-high if tied to Q3. The interesting question isn't "what's the exponent?" but "does every method share the same exponent or not?" |

### Amplifier Questions (Q5–Q6)

#### Q5 — Resource Substitution

> Can better sensing/coordination substitute for more shepherds?

| Criterion | Assessment |
|---|---|
| **Novelty** | 🟢 **High.** This is almost completely unstudied. The multi-robot community talks about sensing-vs-actuation tradeoffs in general, but nobody has published iso-reliability contours for shepherding. |
| **Field value** | 🟢🟢 **Very high for applications.** If you can show "doubling sensor range saves 2 dogs at N=200," that's directly actionable for precision livestock or drone-herding. |
| **Risk** | 🟡 Requires a clean way to parameterize "sensing quality" and "coordination capacity" in HerdSim. If the instruments don't have comparable knobs, the comparison is muddy. |

#### Q6 — Predictive Macro-Measures

> Which flock measures predict required budget across methods?

| Criterion | Assessment |
|---|---|
| **Novelty vs. paper** | 🟡 **Medium.** The paper already proposes `S̄ × N` as a predictor with 87% accuracy. Your upgrade is testing whether that predictor works *across methods*. |
| **Field value** | 🟢 The cross-method test is what makes this valuable. If mean-spread works for Strombom but not for Kubo, that's an important limitation to document. |

### Deferred (Q7 — Robustness)

Smart to defer. Not enough baseline to compare against yet.

---

## 3. Verdict: Is the Agenda More Valuable Than the Paper?

### Short answer: **Yes, significantly — but with caveats.**

### Where the agenda clearly wins

| Dimension | Paper 2025 | Agenda |
|---|---|---|
| **Framing** | Dog count as the variable | Multi-resource budget as the variable |
| **Scope** | Single method | Comparative, multi-method |
| **Regime analysis** | Overcrowding observed | Five-regime taxonomy formalized |
| **Transfer** | Not addressed | Core question (Q3) |
| **Resource substitution** | Not addressed | Explicit question (Q5) |
| **Reusable protocol** | Implicit | Explicit contribution (F) |
| **Predictor validation** | Within-model only | Cross-method test (Q6) |

### Where the paper still has advantages over the agenda *as written*

> [!WARNING]
> The agenda is a *research program*, not a *paper*. It will only be more valuable if it produces results.

| Concern | Detail |
|---|---|
| **The paper is done; the agenda is a plan** | A published 11,000-run study with clear tables beats an unfrozen protocol with zero results. Execution risk is real. |
| **Scope creep** | 7 questions, 4 phases, 6 contributions, 11 requirements — this is ambitious for a single study. The paper was focused and deliverable. |
| **The paper's biological contribution (RQ3)** is orthogonal | The density-gradient for local GCM is a neat sheep-modeling contribution that the agenda doesn't replicate. Different value axis. |

---

## 4. Honest Field-Level Assessment: Will This Get Published / Get Cited?

### What reviewers will love

1. **The budget-frontier framing** is overdue. The shepherding literature is stuck on `D = f(N)`. Treating it as multi-resource controllability aligns with how the broader multi-robot community already thinks, which means the paper would appeal to a wider audience.

2. **Comparative transfer tests** are the single strongest selling point. The field has dozens of herding algorithms, each tested in their own simulator with their own metrics. A standardized comparison is exactly what conference reviewers ask for in related work sections: "How does this compare to X?"

3. **The overcrowding regime taxonomy** gives other researchers vocabulary. Papers that introduce useful vocabulary (think "exploration vs. exploitation") get cited heavily.

### What reviewers will challenge

1. **"Is this really a controllability problem?"** — You use the word "controllability" but don't connect to formal controllability theory (Kalman-style or graph-theoretic). Lama & di Bernardo actually use PDE-based analysis. If you stay purely empirical, call it "empirical budget analysis" rather than "controllability" to avoid misleading expectations.

2. **"Your budget B=(D,T,E) — is E really a budget or an outcome?"** — This is acknowledged in the agenda (Section 4.2 notes), but reviewers will push hard on it. Time T is a constraint; effort E is an observation. Including an observation in the "budget" is conceptually fuzzy. Consider: budget = `(D, T)` as inputs, effort = `E` as output, and the frontier is over `(D, T) → (R, E)`.

3. **"Four methods is not really comparative."** — If all four are Strombom variants in the same simulator, reviewers may say you're comparing parameter settings, not methods. You need at least one fundamentally different approach (e.g., a learning-based or potential-field-based method) to make the "transfer" claim convincing.

4. **"Where's the theory?"** — The agenda claims theory contributions (A, C, D) but doesn't derive any analytical results. If you're purely computational, frame it as "computational investigation" not "theory."

---

## 5. Recommendations

### Do This Now

1. **Trim to a first paper**: Q1 + Q2 + Q3 with 2-3 methods is a complete, publishable unit. Q4-Q7 can be follow-ups.
2. **Fix the B definition**: Make `B = (D, T)` as the budget (inputs), and `E` as an efficiency outcome. The frontier is then: "for each `(D, T)`, what reliability `R` and cost `E` do we get?"
3. **Freeze the protocol**: The agenda has been "pending confirm" since creation. Freeze it. Running experiments is worth more than perfecting definitions.

### Do This Before Claiming "Theory"

4. **Connect to formal controllability or don't call it that.** Either derive a condition under which a budget achieves controllability (even a simple one), or rebrand as "empirical budget analysis."
5. **Ensure method diversity**: At minimum, include one method that is NOT a Strombom-family collect-and-drive heuristic. A potential-field approach (e.g., Lama & di Bernardo style) or an RL-based controller would strengthen the transfer claim enormously.

### Don't Do This

6. **Don't try to answer all 7 questions before publishing anything.** The paper's strength was focus. Match that.
7. **Don't add HerdSim features speculatively.** The agenda already says this — follow your own rule.

---

## 6. Summary Scorecard

| Question | Novelty vs. Paper | Novelty vs. Field | Application Value | Execution Risk | Priority |
|---|---|---|---|---|---|
| Q1 (Budget frontier) | 🟢 High | 🟢 High | 🟢 High | 🟢 Low | **Must-do** |
| Q2 (Regime taxonomy) | 🟡 Med-High | 🟢 High | 🟢 High | 🟢 Low | **Must-do** |
| Q3 (Method transfer) | 🟢 Very High | 🟢🟢 Very High | 🟢 High | 🔴 High | **Must-do (but hard)** |
| Q4 (Scaling shape) | 🟡 Medium | 🟡 Medium | 🟡 Medium | 🟢 Low | Nice-to-have (falls out of Q1-Q3) |
| Q5 (Substitution) | 🟢 High | 🟢🟢 Very High | 🟢🟢 Very High | 🟡 Medium | **Phase 2 priority** |
| Q6 (Predictors) | 🟡 Medium | 🟡 Medium | 🟢 High | 🟢 Low | Phase 2 |
| Q7 (Robustness) | 🟢 High | 🟢 High | 🟢 High | 🟡 Medium | Defer (correct call) |

**Bottom line**: The agenda asks questions that the paper didn't and couldn't — specifically the multi-resource and cross-method questions. These are genuinely valuable to the field. The risk is entirely in execution: can you actually produce the multi-method comparative data with locked protocols? If yes, this is a stronger contribution than the paper. If the scope balloons and nothing gets frozen, the paper wins by default because it exists.
