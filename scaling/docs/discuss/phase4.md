# Phase 4 discussion note (high level)

Audience: email / meeting. Detail lives in the plan, tracker, and run `REPORT.md` files.  
Protocol: `scaling_v2`. Date context: runs completed 2026-10-04 on host `gwen`.

Meeting backlog: [notice-meeting.md](../notice-meeting.md).  
Full plan: [main_scaling_plan.md](../main_scaling_plan.md).  
Run staging: [experiment_run_strategy.md](../experiment_run_strategy.md).  
Status: [progress_tracker.md](../progress_tracker.md).  
Interactive HTML Dossier: [../../results/phase4/guides/share_en/REPORT_en.html](../../results/phase4/guides/share_en/REPORT_en.html).

---

## 1. Question (what Phase 4 asks)

**RQ4 / Package D (cross-method transfer).** Are the scaling frontiers ($D_{\min}$ and overcrowding) discovered in Phase 1 (Size) and Phase 2 (Structure) universal across dog algorithms, or controller-specific?

We test two contrasting multi-shepherd algorithms against the baseline `strombom_multi`:
1. **Kubo et al.**: Local cyclic/rotational patrol dynamics with switching rules.
2. **FAT (Force-field Attractive / Target)**: Potential-field guidance based on distance gradients.

Claims this phase addresses:
- **C4**: $D_{\min}$ or overcrowding behavior is shared across the three required methods (`strombom_multi`, `kubo`, `fat`) on both size and structure grids.

---

## 2. Design & Staging

| Dimension | Scope | Trials / Seeds |
|---|---|---|
| **Size Scaling** | 10 flock sizes ($N \in \{5 \dots 400\}$), compact layout, 10 $D$ | Scout: 30 seeds (3,000 trials)<br>Claim: 100 seeds on boundary cells |
| **Structure Scaling** | 3 sizes ($N \in \{50, 100, 200\}$), 4 layouts, 10 $D$ | Scout: 30 seeds (3,600 trials)<br>Claim: 100 seeds on boundary cells |
| **Methods** | `kubo` and `fat` (compared against `strombom_multi` from Phase 1 & 2) | Full transfer table compiled in **Package D** |

---

## 3. Execution & Rerun Audit

- **Runs Executed**:
  - `kubo_size`: Scout (3,000) + Claim (2,100) = **5,100 trials** (DONE 2026-09-26)
  - `kubo_structure`: Scout (3,600) + Claim (2,800) = **6,400 trials** (DONE 2026-09-27)
  - `fat_structure`: Scout (3,600) + Claim (2,400) = **6,000 trials** (DONE 2026-10-02)
  - `fat_size`: Interrupted on 2026-09-28; full re-scout completed 2026-10-03 (3,000 trials), claim completed 2026-10-04 (2,000 trials) = **5,000 trials**
- **Total Phase 4 Trials**: **22,500 trials** executed and verified complete.
- **Evidence Packages**: Package D generated for both `size/` and `structure/`.

---

## 4. Results (transfer findings)

```text
Flock size N       Strombom (baseline)   Kubo             FAT
N = 5              D_min = 2             D_min = 3        D_min = 1
N = 10             D_min = 2             D_min = 1        D_min = 1
N = 25 .. 400      D_min = 1 (flat)      D_min = 1 (flat) Hard Failure (R < 0.90)
Overcrowding       None                  None             None
```

### Key Insights
1. **Kubo Transfers Strongly**:
   - For all $N \ge 25$ through 400, Kubo matches the baseline: **$D_{\min} = 1$ is shared**.
   - At small sizes ($N=5, 10$), Kubo has a minor shift ($D=3$ at $N=5$, $D=1$ at $N=10$).
   - Overcrowding is absent across all tested dog counts (up to 35 dogs).
2. **FAT Suffers Hard Failure at Scale**:
   - FAT performs well on tiny flocks ($N \le 10$).
   - For $N \ge 25$, FAT **cannot reach $\theta = 0.90$ reliability** on this drive task within 10,000 ticks, regardless of whether 1, 10, or 35 dogs are deployed. The force-field balance tends to disperse or circle large flocks without completing the pen drive.
3. **Structure Transfer**:
   - `kubo_structure` confirms $D_{\min}=1$ across all four layouts, identical to Strombom in Phase 2.

---

## 5. Report / Claims (discussion stance)

| Claim | Verdict | Evidence |
|---|---|---|
| **C4** (shared $D_{\min}$ / overcrowding) | **SUPPORTED (Partial)** | **Shared between Strombom and Kubo** for all $N \ge 25$ on both size and structure. **FAT deviates** through large-flock hard failure. |

**Key Takeaway for Meetings**:
Herdability scaling is **not purely universal across all controllers**. While reactive collect/drive algorithms (Strombom, Kubo) maintain high reliability with $D_{\min} \approx 1$ up to 400 sheep, potential-field controllers (FAT) exhibit severe scalability limits on open-field drive tasks.
