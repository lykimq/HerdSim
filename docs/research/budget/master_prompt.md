# Deep Research Prompt

## Designing a New Scientific Research Program Around HerdSim

I am developing a research project using HerdSim, a simulation platform for shepherding and collective behaviour.

I have an existing draft/private research paper and an existing research agenda. The draft paper contains an approach and some preliminary findings from a relatively narrow shepherding setting.

**Important: Do NOT treat this draft paper as the scientific foundation, benchmark, or primary source of novelty for the new research program.**

The draft paper should be treated only as:

* preliminary work,
* evidence of what has already been explored by our group,
* a source of potentially useful observations,
* and a starting point from which we can move toward broader and more important questions.

The new research program should stand on its **own scientific foundation**.

The central objective is to identify a research direction that is:

* scientifically important,
* genuinely open,
* broader than one shepherding algorithm,
* relevant to real-world collective-control problems,
* experimentally feasible in HerdSim,
* technically implementable,
* capable of producing strong scientific contributions,
* and honest about what simulation can and cannot establish.

I want you to independently determine what the strongest research direction should be rather than preserving the assumptions of my current agenda.

---

# 1. START FROM THE SCIENTIFIC FIELD, NOT FROM THE EXISTING PAPER

First investigate the broader scientific landscape surrounding:

* collective behaviour,
* collective control,
* shepherding,
* swarm robotics,
* multi-agent systems,
* distributed control,
* human/animal crowd control,
* collective transport,
* multi-robot coordination,
* autonomous agricultural robotics,
* indirect control of groups,
* complex adaptive systems,
* nonlinear collective dynamics.

Identify the major scientific questions that the field is currently trying to understand.

Look for:

* important unresolved questions,
* contradictions between studies,
* limitations of current models,
* missing mechanisms,
* missing theoretical understanding,
* missing experimental evidence,
* scalability problems,
* robustness problems,
* information limitations,
* control-resource limitations,
* and gaps between simulation and real-world systems.

Do not assume that shepherding itself is the ultimate research topic.

Ask whether shepherding can serve as a **controlled model system for a broader scientific problem**.

---

# 2. IDENTIFY REAL-WORLD PROBLEMS FIRST

Before designing HerdSim experiments, identify important real-world situations where a system must influence or control a collective population indirectly.

Examples may include:

* agricultural robotics,
* livestock management,
* search and rescue,
* evacuation,
* crowd guidance,
* autonomous vehicle coordination,
* drone/robot swarms,
* environmental robotics,
* distributed sensing,
* ecological management,
* collective transport.

Do not assume all of these are appropriate.

For each potential application ask:

1. What is the real-world control problem?
2. Why is direct individual control difficult?
3. Why might indirect collective control be useful?
4. What scientific knowledge is currently missing?
5. Can a shepherding-style model provide a meaningful abstraction?
6. What could HerdSim realistically contribute?
7. What cannot be inferred from simulation?

The purpose is not to claim immediate deployment.

The purpose is to identify **scientific problems whose solutions could eventually matter in real systems**.

---

# 3. DEFINE THE BROADER SCIENTIFIC PROBLEM

After reviewing the field, determine whether there is a fundamental problem underlying several applications.

Potential examples to investigate include:

> How can an external controller reliably influence a large collective without directly controlling its individual members?

or:

> What determines the controllability limits of emergent collective systems?

or:

> How should limited control resources be allocated when the target population has nonlinear collective dynamics?

Do not assume any of these formulations is correct.

Compare possible formulations and select the one that has the strongest combination of:

* scientific importance,
* novelty,
* tractability,
* generality,
* measurable variables,
* theoretical potential,
* and real-world relevance.

---

# 4. USE THE EXISTING DRAFT PAPER ONLY AS PRELIMINARY CONTEXT

After independently understanding the broader field, examine the existing draft paper.

Ask:

* What did this work already investigate?
* What observations does it provide?
* Which findings may be useful clues?
* Which assumptions are narrow?
* Which conclusions cannot be generalized?
* What questions does it leave open?
* Which directions would merely reproduce the same research?
* Which directions would genuinely move beyond it?

Do NOT structure the new research around reproducing the draft.

Do NOT assume that its variables are the correct variables.

Do NOT assume that its methodology defines the research problem.

Do NOT assume that its conclusions are general laws.

Instead ask:

> **What can we learn from this preliminary work that helps us formulate a much broader scientific question?**

---

# 5. FIND GENUINE RESEARCH GAPS

For every potential research direction, perform a literature check.

Classify the state of knowledge as:

### Established

Strong evidence already exists.

### Partially understood

Evidence exists but important mechanisms or boundaries remain unclear.

### Contested

Different studies provide different conclusions.

### Underexplored

The question has received limited attention.

### Unknown

There is insufficient evidence to answer the question.

Do not call something a "research gap" merely because the existing draft paper did not study it.

A gap must be evaluated against the broader field.

---

# 6. IDENTIFY QUESTIONS THAT COULD CHANGE THE FIELD

Look beyond incremental questions such as:

* Does algorithm A outperform algorithm B?
* How many shepherds are required?
* Does sensing range improve performance?
* Does cohesion correlate with success?

Those may be useful experiments but should not automatically become the central scientific contribution.

Instead investigate questions involving:

* fundamental controllability limits,
* critical transitions,
* emergent phenomena,
* scaling principles,
* resource trade-offs,
* information/control equivalence,
* controller interference,
* collective-state representations,
* failure mechanisms,
* adaptive control,
* generality across control architectures.

For each candidate question ask:

> If this question were answered convincingly, would it change how researchers understand collective control?

If the answer is no, treat it as a supporting question rather than a central RQ.

---

# 7. IDENTIFY SCIENTIFIC BREAKPOINTS

Actively search for phenomena where the system changes regime.

Examples:

$$
\text{controllable}
\rightarrow
\text{uncontrollable}
$$

$$
\text{beneficial controllers}
\rightarrow
\text{redundant controllers}
\rightarrow
\text{harmful controllers}
$$

$$
\text{local information sufficient}
\rightarrow
\text{information insufficient}
$$

$$
\text{cohesive collective}
\rightarrow
\text{fragmented collective}
$$

$$
\text{scaling regime A}
\rightarrow
\text{scaling regime B}
$$

Determine which transitions are:

* already known,
* partially known,
* genuinely unexplored,
* or potentially discoverable with HerdSim.

The research should prioritize **mechanistically meaningful transitions**, not arbitrary thresholds.

---

# 8. DEVELOP A SMALL SET OF FUNDAMENTAL RESEARCH QUESTIONS

Produce no more than approximately 3–6 major research questions.

For each question provide:

## Research Question

Precise formulation.

## Why It Matters

Scientific and real-world significance.

## What Is Already Known

Literature-supported evidence.

## What Is Unknown

The actual unresolved part.

## Why It Is Potentially Novel

What has not yet been established.

## Hypotheses

Falsifiable hypotheses, without assuming the desired result.

## Experimental Variables

Independent variables, dependent variables, controls, confounders.

## HerdSim Experiment

Exactly what would be simulated.

## Required Measurements

Exactly what HerdSim must observe.

## Analysis

How the data would be analysed.

## Alternative Explanations

What could produce the same result.

## Possible Results

What different outcomes would imply.

## Scientific Contribution

What knowledge would be added.

---

# 9. DISTINGUISH THREE LEVELS OF CONTRIBUTION

For every research question classify the potential contribution as:

### Level 1 — Empirical characterization

A new measurement or empirical relationship.

### Level 2 — Mechanism

An explanation of why a collective-control phenomenon occurs.

### Level 3 — General principle

A mechanism or law that appears to apply across different collective states, control strategies, or systems.

Prioritize questions capable of reaching Level 2 or Level 3.

Do not claim Level 3 unless the experimental evidence supports generalization.

---

# 10. DESIGN HERDSIM FROM THE SCIENTIFIC QUESTIONS

Only after defining the research questions should you inspect and redesign HerdSim.

Audit the actual source code.

Determine:

* current architecture,
* simulation core,
* agent models,
* shepherd controllers,
* environment,
* scenario system,
* experiment system,
* metrics,
* telemetry,
* random-number handling,
* seed management,
* batch execution,
* data export,
* configuration,
* tests,
* reproducibility mechanisms.

Do not assume the current documentation accurately describes the implementation.

Verify against source code.

---

# 11. REDESIGN HERDSIM AS A SCIENTIFIC INSTRUMENT

The architecture should separate:

```text
Scientific Question
        ↓
Experiment Definition
        ↓
Scenario
        ↓
Collective Model
        ↓
Controller
        ↓
Simulation
        ↓
Instrumentation
        ↓
Telemetry
        ↓
Trial Results
        ↓
Statistical Analysis
        ↓
Scientific Conclusion
```

The simulator should not contain scientific conclusions.

The experimental framework should make it possible to test competing hypotheses without changing the underlying simulation unnecessarily.

---

# 12. DESIGN THE MINIMUM REQUIRED HERDSIM CAPABILITIES

For every proposed research question determine:

* what simulation capability is required,
* what metric is required,
* what telemetry is required,
* what experiment configuration is required,
* what statistical analysis is required.

Do not implement metrics simply because they are interesting.

Every new HerdSim feature should answer:

> **Which scientific question does this feature enable us to investigate?**

Create a traceability table:

| Scientific Question | Experiment | HerdSim Capability | Metric | Analysis |
| ------------------- | ---------- | ------------------ | ------ | -------- |

---

# 13. DESIGN THE EXPERIMENTAL STRATEGY

Do not begin with a huge brute-force parameter sweep.

Use a scientific discovery process:

### Stage A — Exploration

Find interesting regions and possible transitions.

### Stage B — Boundary identification

Concentrate experiments around potential critical regions.

### Stage C — Mechanism testing

Manipulate candidate causal mechanisms.

### Stage D — Robustness

Test alternative initial conditions, population sizes, environments and stochastic conditions.

### Stage E — Generalization

Test alternative control algorithms and information architectures.

### Stage F — External validity

Determine what can reasonably be connected to real-world systems.

For each stage specify:

* experiment,
* parameter ranges,
* replication,
* statistical method,
* expected evidence,
* decision criteria for proceeding.

---

# 14. BUILD THE STATISTICAL DESIGN BEFORE RUNNING EXPERIMENTS

Define:

* stochastic replication,
* confidence intervals,
* effect sizes,
* uncertainty,
* model comparison,
* breakpoint detection,
* scaling-law analysis,
* sensitivity analysis,
* out-of-sample validation.

Avoid arbitrary thresholds unless scientifically justified.

If a threshold is required, perform sensitivity analysis.

Do not define a "breakpoint" merely as the first parameter value where the result changes on a coarse grid.

Use appropriate statistical or functional modelling.

---

# 15. DESIGN FOR FALSIFICATION

For every major hypothesis ask:

> What result would prove this hypothesis wrong?

For example:

Hypothesis:

> Collective-state variables provide information about controllability beyond population size.

Falsification:

If models using collective state do not improve out-of-sample prediction or explanation beyond \(N\) and resource variables, the hypothesis is not supported.

Do this for every major claim.

---

# 16. AVOID SCIENTIFIC OVERCLAIMING

Explicitly distinguish:

* simulation result,
* empirical mechanism,
* theoretical interpretation,
* general principle,
* real-world implication.

Do not claim:

* universal laws,
* universal scaling,
* theoretical impossibility,
* real-world effectiveness,
* biological validity,

unless the evidence supports them.

Use cautious language where appropriate:

> "within the tested parameter domain"

> "consistent with"

> "supports the hypothesis that"

> "provides evidence for"

rather than:

> "proves"

when the experiment cannot establish proof.

---

# 17. DETERMINE WHAT THE FINAL RESEARCH PROGRAM SHOULD NOT DO

Explicitly identify:

* experiments that are interesting but scientifically secondary,
* features that are unnecessary,
* research questions that are redundant with existing literature,
* analyses that would produce only incremental results,
* claims that HerdSim cannot support,
* applications that are too distant from the model assumptions.

This is important.

A good research plan should define its boundaries.

---

# 18. PRODUCE THE FINAL RESEARCH PROGRAM

The final output should contain:

# HerdSim Research Program

## 1. Scientific Vision

What broader scientific problem does this project address?

## 2. Real-World Motivation

Why does solving this problem matter?

## 3. State of the Field

What is already understood?

## 4. Genuine Research Gap

What remains unresolved?

## 5. Position of Our Existing Work

What does the draft paper contribute as preliminary context, and why is the new program broader?

## 6. Central Scientific Question

The single fundamental question.

## 7. Central Hypothesis

The main proposition being tested.

## 8. Major Research Questions

3–6 carefully selected RQs.

## 9. Scientific Breakpoints

Potential transitions or boundaries to investigate.

## 10. Experimental Program

A staged set of experiments.

## 11. Required HerdSim Capabilities

What the simulator must be able to do.

## 12. HerdSim Architecture

Recommended software architecture.

## 13. Telemetry and Metrics

What must be measured and why.

## 14. Statistical Design

How evidence will be evaluated.

## 15. Research-to-Code Traceability

Map every RQ to implementation and experiments.

## 16. Expected Contributions

Separate:

* empirical,
* mechanistic,
* theoretical,
* methodological,
* applied.

## 17. Possible Outcomes

Explain what different experimental results would mean.

## 18. Limitations

What cannot be concluded.

## 19. Implementation Roadmap

What should be implemented first, second, third, etc.

## 20. Experimental Roadmap

What experiments should actually be run and in what order.

## 21. Publication/Contribution Strategy

Explain which findings would constitute:

* a useful result,
* a strong scientific contribution,
* and a potentially broader contribution to collective-control science.

---

# FINAL PRINCIPLE

The entire research program should follow this logic:

```text
REAL-WORLD PROBLEM
        ↓
FUNDAMENTAL SCIENTIFIC QUESTION
        ↓
WHAT IS ALREADY KNOWN?
        ↓
WHAT IS ACTUALLY UNKNOWN?
        ↓
COMPETING HYPOTHESES
        ↓
EXPERIMENTAL DESIGN
        ↓
HERDSIM CAPABILITIES
        ↓
SIMULATION
        ↓
STATISTICAL EVIDENCE
        ↓
MECHANISM
        ↓
GENERALIZATION
        ↓
SCIENTIFIC CONTRIBUTION
```

The existing draft paper should appear only as:

```text
PRELIMINARY WORK
      ↓
useful observations
      ↓
questions that motivate broader investigation
```

It should NOT become:

```text
OLD PAPER
    ↓
extend its method
    ↓
run larger experiments
    ↓
claim new contribution
```

The goal is to build a research program that would still be scientifically meaningful **even if the existing draft paper did not exist**.

The strongest possible outcome is not:

> "We found a better shepherding strategy."

It is:

> **"We discovered and experimentally characterized a previously unresolved principle governing how collective systems can be controlled through limited external agents."**

Only pursue that claim if the evidence actually supports it.
