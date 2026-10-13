# Phase 4: transfer across dog rules

Do the same fewest-dogs answers show up with Kubo and FAT, or only with baseline `strombom_multi`?

Size maps use compact starts, N in {5..400}, D in {1..35}. Structure maps use four layouts, N in {50, 100, 200}, and the same D grid. Sim total about **20d 0h 7m** (largest piece: Kubo structure claim ~9d 16h).

- **Size:** Kubo shares `D_min` = 1 with Strombom for N >= 25; FAT hard-fails for N >= 25.
- **Structure:** Kubo matches on compact and split; hard-fails on wide; outlier_rich N=200 shifts to `D_min` = 20 (200 seeds; bootstrap [2, 20]). FAT hard-fails on every structure cell.

### Claims

- **C4** (`D_min` or overcrowding is shared across Strombom, Kubo, and FAT, including structure): **SUPPORTED (partial)**.

Shared on compact N >= 25 (Strombom/Kubo). Kubo wide is absent. Kubo outlier_rich N=200 is shifted. FAT is absent for N >= 25 and on structure. Transfer is mixed, not universal.

Details: [kubo_structure/claim/](kubo_structure/claim/), [package_d/size/](package_d/size/), [package_d/structure/](package_d/structure/).

## How we get this

```bash
uv run cli/campaign.py run --protocol phase4_{kubo,fat}_{size,structure}_scout --workers 16
uv run cli/campaign.py claim-reseed --protocol phase4_{kubo,fat}_{size,structure}_claim --workers 16
```

| Folder | Role |
|--------|------|
| `kubo_size/`, `fat_size/` | compact size scout + claim |
| `kubo_structure/`, `fat_structure/` | structure scout + claim |
| `package_d/size/`, `package_d/structure/` | transfer tables |
