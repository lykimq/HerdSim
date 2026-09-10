# Related work

HerdSim sits among agent-based shepherding models that guide interacting
followers with one or more steering agents. The platform focuses on three
implemented families and on algorithm-independent evaluation.

## Model families in HerdSim

### Strombom et al. 2014

Heuristic Collect/Drive shepherding with local sheep attraction/repulsion.
HerdSim plugin: `strombom` (plus noise and multi-dog variants).

### Kubo et al. 2022

Force-based multi-sheepdog guidance with dog-dog repulsion and continuous
integration. HerdSim plugin: `kubo` (MATLAB-faithful force parameters).

### Jadhav et al. 2024

Empirically informed collective responses of flocking sheep to a herding dog,
with topological neighbour rules. HerdSim plugin: `flocking_dog`.

## Background context

Multi-shepherd cooperation, reactive shepherding limits, and biologically
inspired robotic herding provide context for why a shared simulation and metric
suite is useful. HerdSim cites this literature to situate the comparison
framework; it does not treat those papers as an implementation backlog.

Representative background:

- Lien et al. on shepherding with multiple shepherds.
- El-Fiqi et al. on limits of reactive shepherding and configuration effects.
- King et al. on biologically inspired herding of animal groups by robots.

## What HerdSim emphasizes

Many papers propose a new controller. Fewer define a reusable, model-independent
metric and scenario stack for comparing mechanisms. HerdSim's emphasis is that
stack: shared engine, scenarios, metrics, seeds, and provenance for
Strombom, Kubo, and Jadhav under equivalent conditions.
