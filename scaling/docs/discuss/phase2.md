# Phase 2 discussion note (high level)

Audience: email / meeting. Detail lives in the plan, tracker, and run `REPORT.md` files.  
Protocol: `scaling_v2`. Date context: runs completed 2026-09-25 on host `gwen`.

Meeting backlog: [notice-meeting.md](../notice-meeting.md).  
Full plan: [main_scaling_plan.md](../main_scaling_plan.md).  
Run staging: [experiment_run_strategy.md](../experiment_run_strategy.md).  
Status: [progress_tracker.md](../progress_tracker.md).  
Interactive HTML Dossier: [../../results/phase2/guides/share_en/REPORT_en.html](../../results/phase2/guides/share_en/REPORT_en.html).

---

## 1. Question (what Phase 2 asks)

**RQ1 / Package B (initial structure).** Does the spatial geometry of the flock $X_0$ change the minimum number of dogs $D_{\min}$ required to achieve 90% reliability ($\theta = 0.90$) at fixed flock sizes $N \in \{50, 100, 200\}$?

Does an elongated, wide, split, or outlier-heavy flock require more shepherds than a packed, compact flock?

Claims this phase addresses:
- **C1a**: For at least one $N$, $D_{\min}$ differs by at least one grid step across layout families.
- **C1b**: A state-augmented model predicting failure has lower out-of-sample negative log-likelihood than an $(N, D)$ baseline.

---

## 2. Design (what we froze)

| Choice | Setting |
|---|---|
| Task | Drive flock into goal disk; success = all sheep in goal within $T_0 = 10,000$ |
| Arena | $500 \times 500$; drive length 120; goal radius $15 \times \sqrt{N/50}$ |
| Method | `strombom_multi` (baseline) |
| Layouts $X_0$ | `compact`, `wide`, `split`, `outlier_rich` |
| Flock sizes $N$ | $\{50, 100, 200\}$ |
| Shepherd counts $D$ | $\{1, 2, 3, 4, 6, 10, 15, 20, 25, 35\}$ |
| Sampling | Scout: 30 seeds; Claim reseed: 100 seeds on boundary windows |
| Staging | Pilot state (600) → Scout (3,600) → Claim plan (24 cells) → Claim reseed (2,400) → Package B |

---

## 3. Plan vs what we ran

| Step | Intent | Status |
|---|---|---|
| Pilot state | Validate layout generators and state logging | DONE (600 trials, 7 min) |
| Scout | Full 4 layouts $\times$ 3 sizes $\times$ 10 $D$ at 30 seeds | DONE (3,600 trials, ~3.2 hours) |
| Claim plan | Boundary detection around $D_{\min}$ for each layout | DONE (24 boundary cells) |
| Claim reseed | 100 seeds on boundary cells; merge with scout | DONE (2,400 claim trials; 5,280 merged rows) |
| Package B | Frontier comparison, state predictors, figure generation | DONE (Package B compiled) |
| HTML dossier | Standalone interactive report | DONE (`phase2/guides/share_en/REPORT_en.html`) |

---

## 4. Results (claim-grade picture)

```text
initial_layout  N    D_min  B*_D  B*_effort
compact         50   1      1     157.5
compact         100  1      1     161.4
compact         200  1      1     144.2

split           50   1      1     157.5
split           100  1      1     162.0
split           200  1      1     144.4

outlier_rich    50   1      1     209.2
outlier_rich    100  1      1     553.9
outlier_rich    200  1      1     1646.7

wide            50   1      2     2336.8
wide            100  1      2     3003.2
wide            200  1      2     3693.7
```

- **$D_{\min} = 1$ Across All Layouts**: Even under `wide`, `split`, or `outlier_rich` initial conditions, a single Strombom shepherd achieves $\ge 0.90$ reliability given $T_0 = 10,000$ ticks.
- **Effort ($B^*$ Path Length) Explodes**: While $D_{\min}$ is unchanged, layout dramatically alters the energy required:
  - `compact` and `split` require ~150 path units.
  - `wide` requires ~3,000 path units (a 20-fold increase) and its optimal operating point $B^*$ shifts to **2 dogs**.
  - `outlier_rich` effort scales steeply with $N$ (from 209 at $N=50$ to 1,647 at $N=200$).

---

## 5. Report / Claims (discussion stance)

| Claim | Verdict | Evidence |
|---|---|---|
| **C1a** ($D_{\min}$ differs across layouts) | **REJECTED** | $D_{\min} = 1$ everywhere for $N \in \{50, 100, 200\}$ at $\theta=0.90$. |
| **C1b** (state predictor vs $N, D$) | **INCONCLUSIVE** | Because $D_{\min}$ did not shift, state-based classification does not outperform the flat $(N, D)$ baseline. |

**Key Takeaway for Meetings**:
Structure does not increase the shepherd count needed to succeed on this task, but it dramatically increases the **time and total path effort**. The shepherd spends substantial effort gathering peripheral sheep before commencing the drive, which is successfully accomplished by 1 dog given sufficient ticks.
