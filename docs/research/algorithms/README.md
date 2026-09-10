# Instruments (sheep model x dog controller)

HerdSim no longer treats each paper as a monolithic algorithm. Named instruments
are presets over orthogonal plugins.

## Sheep models

| id | Role |
|----|------|
| `strombom` | Strombom 2014 sheep heading rules |
| `kubo` | Kubo 2022 force-based sheep |
| `jadhav` | Jadhav 2024 topological flocking sheep |

## Dog controllers

| id | Role |
|----|------|
| `collect_drive` | Strombom Collect/Drive |
| `collect_drive_multi` | Multi-dog outlier assignment |
| `kubo_forces` | Kubo dog forces |
| `v_formation` | V-arc drive |
| `obstacle_aware_drive` | Obstacle-deflected drive |
| `fat` | Farthest-agent targeting |
| `communication_free` | Independent local Collect/Drive |
| `adaptive` | Context-aware collect/drive/recover/lead |
| `policy_file` | Frozen linear / learned policy |

## Observation modes

`global`, `local_positions`, `bearing_only`, `noisy_bearing`, `intermittent`

## Named presets

See Guide pages and `core/presets.py` for `strombom`, `kubo`, `flocking_dog`,
`heterogeneous` (stubborn_fraction), `strombom_noise` (noise factor), and others.
