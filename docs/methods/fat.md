# Uncoordinated greedy baseline: `fat`

Farthest-agent targeting, or FAT, tests whether coordination is needed at all. Every dog aims at the point $r_a$ behind the sheep farthest from the goal, on its far side from the goal, and moves with [Strömbom's step, noise and stop rule](strombom_multi.md#dog-speed-step-and-stop-rule). Strömbom's rule takes the sheep farthest from the flock centre instead. FAT has no assignment, no drive arc, no communication and no collect/drive switch. Its dogs bunch on one sheep because nothing keeps them apart (Figure 1).

![Strömbom and FAT targets, and four FAT dogs bunching](../figures/fig4_fat.png)

**Figure 1: Bunching in FAT.** Every FAT dog picks the same sheep, so a team works like a single dog.

- Marks: blue dots are sheep, orange triangles dogs; the orange circle marks the chosen sheep, the cross the dog's target, the green arrow the direction to the goal.
- Left: Strömbom's single-dog rule, behind the sheep farthest from the GCM.
- Middle: FAT with one dog, behind the sheep farthest from the goal.
- Right: FAT with 4 dogs, bunched on the same sheep.

## References

1. Strömbom, D., et al. (2014). *Solving the shepherding problem: heuristics for herding autonomous, interacting agents*. Journal of the Royal Society Interface, 11(100), 20140719. [DOI: 10.1098/rsif.2014.0719](https://doi.org/10.1098/rsif.2014.0719)
