"""Values the paper states, HerdSim's readings where it is silent, and the grids run.

Sources: the paper's Table 1, section 4.1, the captions of Figs 2 and 3, and its text on
Fig. 3 and on the distance study (p. 4).
"""

from __future__ import annotations

import math

import yaml

from services.protocol import CANONICAL, RESULTS_ROOT
from sim.strombom.params import DEFAULTS

# Stated by the paper.
FIELD_SIDE = 150.0  # m, L (Table 1)
SHEEP_BOX = (FIELD_SIDE / 2, FIELD_SIDE)  # the upper right quarter (section 4.1)
MAX_STEPS = 8000  # time steps allowed (Fig. 3 caption)
FIG3_DETECTION = 45.0  # m, r_s (Fig. 3 caption)
TABLE1_DETECTION = float(DEFAULTS["r_s"])  # 65 m, Table 1, used by the distance study
FIG3_TRIALS = 50  # "over 50 simulations" (text on Fig. 3)
RUNS = 100  # "100 simulations" per distance of the distance study
DISTANCE_FLOCK = 46  # agents of the distance study
DISTANCE_BOX_SIDE = 50.0  # m, their start square, centred at (l + 25 sqrt 2, l + 25 sqrt 2)

# HerdSim's reading: the paper ends at "a certain distance" (section 4.1) and gives 10 units
# for one example (Fig. 2 caption).
DONE_DISTANCE = 10.0  # m, flock centre to the origin

# HerdSim's grids over the paper's. Fig. 3: sizes N and neighbour counts n as shares of N, plus
# the global case n = N - 1, chosen to cover the paper's three regions (always, transition,
# rare) at a cost of minutes, not every (N, n). Distances: the paper's 10 to 500, every 50
# after 10.
FLOCK_SIZES = (10, 20, 30, 40, 50, 60, 80, 100, 125, 150)
NEIGHBOUR_SHARES = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8)
DISTANCES = (10, *range(50, 501, 50))

# The engine records per-tick metrics that change no trial; they take the study's values, and
# the paper has no lost-sheep rule, so no sheep counts as lost.
_CANONICAL = yaml.safe_load(CANONICAL.read_text())
METRIC_SETUP = {
    "measurement_radius": float(_CANONICAL["measurement_radius"]),
    "dog_overlap_distance": float(_CANONICAL["dog_overlap_distance"]),
    "lost_radius": math.inf,
}

RESULTS = RESULTS_ROOT / "paper_check"
