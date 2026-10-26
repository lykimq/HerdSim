"""Post-simulation analysis and reporting utilities.

Modules in this package process trial results and summary tables without re-running simulations:
- frontier: Reliability and speed thresholds, team-size boundaries (D_min, D_sat), and zoning.
- results: Parsing campaign outputs and rendering Markdown tables.
- dmin: Evaluating D_min under counterfactual deadlines from existing trial data.
- dmin_tables: Tabulation helpers for reports and CLI commands.
- dispersion_burden: Analyzing initial spread metrics (S0 x N) and failure classifications.
- growth_fits: Fitting power-law vs saturating models to D_min scaling curves.
- herdability: Comparing HerdSim reliability metrics with literature herdability criteria.
- pressure: Measuring herding pressure and flight duration during trial replays.
"""

