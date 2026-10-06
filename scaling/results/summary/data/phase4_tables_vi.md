# Bang du lieu Giai doan 4

Ket luan ve controller dung claim merge. Luoi scout van chi la bang chung lap ke hoach. Bang Package D so sanh ket qua controller cap claim.

## Bien kich thuoc voi bo cuc compact

Kubo source: [`phase4/kubo_size/claim/packages/a/frontier.csv`](../../phase4/kubo_size/claim/packages/a/frontier.csv).

| initial_layout | n_sheep | d_min | d_overcrowd | d_max | b_star_d | hard_failure |
|---|---|---|---|---|---|---|
| compact | 5 | 3 |  | 35 | 3 | False |
| compact | 10 | 1 |  | 35 | 1 | False |
| compact | 25 | 1 |  | 35 | 1 | False |
| compact | 50 | 1 |  | 35 | 1 | False |
| compact | 75 | 1 |  | 35 | 1 | False |
| compact | 100 | 1 |  | 35 | 1 | False |
| compact | 150 | 1 |  | 35 | 1 | False |
| compact | 200 | 1 |  | 35 | 1 | False |
| compact | 300 | 1 |  | 35 | 1 | False |
| compact | 400 | 1 |  | 35 | 1 | False |

FAT source: [`phase4/fat_size/claim/packages/a/frontier.csv`](../../phase4/fat_size/claim/packages/a/frontier.csv).

| initial_layout | n_sheep | d_min | d_overcrowd | d_max | b_star_d | hard_failure |
|---|---|---|---|---|---|---|
| compact | 5 | 1.0 |  | 35.0 | 1.0 | False |
| compact | 10 | 1.0 |  | 35.0 | 3.0 | False |
| compact | 25 |  |  |  |  | True |
| compact | 50 |  |  |  |  | True |
| compact | 75 |  |  |  |  | True |
| compact | 100 |  |  |  |  | True |
| compact | 150 |  |  |  |  | True |
| compact | 200 |  |  |  |  | True |
| compact | 300 |  |  |  |  | True |
| compact | 400 |  |  |  |  | True |

Cac truong bien trong voi `hard_failure = True` nghia la khong D nao dat R = 0.90. Chung khong phai uoc luong gioi han tren.

## Khoang bootstrap D_min kich thuoc day du

Kubo source: [`phase4/kubo_size/claim/packages/a/dmin_bootstrap.csv`](../../phase4/kubo_size/claim/packages/a/dmin_bootstrap.csv).

| initial_layout | n_sheep | d_min | d_min_ci_low | d_min_ci_high | n_boot | n_seeds_ref | n_boot_defined |
|---|---|---|---|---|---|---|---|
| compact | 5 | 3 | 1 | 3 | 1000 | 100 | 1000 |
| compact | 10 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 25 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 50 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 75 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 100 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 150 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 200 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 300 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 400 | 1 | 1 | 1 | 1000 | 100 | 1000 |

FAT source: [`phase4/fat_size/claim/packages/a/dmin_bootstrap.csv`](../../phase4/fat_size/claim/packages/a/dmin_bootstrap.csv).

| initial_layout | n_sheep | d_min | d_min_ci_low | d_min_ci_high | d_min_ci_low_above_grid | d_min_ci_high_above_grid | n_boot | n_seeds_ref | n_boot_defined |
|---|---|---|---|---|---|---|---|---|---|
| compact | 5 | 1.0 | 1.0 | 1.0 | False | False | 1000 | 100 | 1000 |
| compact | 10 | 1.0 | 1.0 | 1.0 | False | False | 1000 | 100 | 1000 |
| compact | 25 |  | 2.0 |  | False | True | 1000 | 100 | 130 |
| compact | 50 |  |  |  | True | True | 1000 | 100 | 0 |
| compact | 75 |  |  |  | True | True | 1000 | 100 | 0 |
| compact | 100 |  |  |  | True | True | 1000 | 100 | 0 |
| compact | 150 |  |  |  | True | True | 1000 | 100 | 0 |
| compact | 200 |  |  |  | True | True | 1000 | 100 | 0 |
| compact | 300 |  |  |  | True | True | 1000 | 100 | 0 |
| compact | 400 |  |  |  | True | True | 1000 | 100 | 0 |

## Bien day du theo controller va bo cuc

Source: [`phase4/package_d/structure/frontier_by_method_layout.csv`](../../phase4/package_d/structure/frontier_by_method_layout.csv).

| method | initial_layout | n_sheep | d_min | d_overcrowd | d_max | b_star_d | hard_failure |
|---|---|---|---|---|---|---|---|
| fat | compact | 50 |  |  |  |  | True |
| fat | compact | 100 |  |  |  |  | True |
| fat | compact | 200 |  |  |  |  | True |
| fat | outlier_rich | 50 |  |  |  |  | True |
| fat | outlier_rich | 100 |  |  |  |  | True |
| fat | outlier_rich | 200 |  |  |  |  | True |
| fat | split | 50 |  |  |  |  | True |
| fat | split | 100 |  |  |  |  | True |
| fat | split | 200 |  |  |  |  | True |
| fat | wide | 50 |  |  |  |  | True |
| fat | wide | 100 |  |  |  |  | True |
| fat | wide | 200 |  |  |  |  | True |
| kubo | compact | 50 | 1.0 |  | 35.0 | 1.0 | False |
| kubo | compact | 100 | 1.0 |  | 35.0 | 1.0 | False |
| kubo | compact | 200 | 1.0 |  | 35.0 | 1.0 | False |
| kubo | outlier_rich | 50 | 1.0 |  | 35.0 | 1.0 | False |
| kubo | outlier_rich | 100 | 1.0 |  | 35.0 | 1.0 | False |
| kubo | outlier_rich | 200 | 20.0 |  | 35.0 | 20.0 | False |
| kubo | split | 50 | 1.0 |  | 35.0 | 1.0 | False |
| kubo | split | 100 | 1.0 |  | 35.0 | 1.0 | False |
| kubo | split | 200 | 1.0 |  | 35.0 | 1.0 | False |
| kubo | wide | 50 |  |  |  |  | True |
| kubo | wide | 100 |  |  |  |  | True |
| kubo | wide | 200 |  |  |  |  | True |
| strombom_multi | compact | 50 | 1.0 |  | 35.0 | 1.0 | False |
| strombom_multi | compact | 100 | 1.0 |  | 35.0 | 1.0 | False |
| strombom_multi | compact | 200 | 1.0 |  | 35.0 | 1.0 | False |
| strombom_multi | outlier_rich | 50 | 1.0 |  | 35.0 | 1.0 | False |
| strombom_multi | outlier_rich | 100 | 1.0 |  | 35.0 | 1.0 | False |
| strombom_multi | outlier_rich | 200 | 1.0 |  | 35.0 | 1.0 | False |
| strombom_multi | split | 50 | 1.0 |  | 35.0 | 1.0 | False |
| strombom_multi | split | 100 | 1.0 |  | 35.0 | 1.0 | False |
| strombom_multi | split | 200 | 1.0 |  | 35.0 | 1.0 | False |
| strombom_multi | wide | 50 | 1.0 |  | 35.0 | 2.0 | False |
| strombom_multi | wide | 100 | 1.0 |  | 35.0 | 2.0 | False |
| strombom_multi | wide | 200 | 1.0 |  | 35.0 | 2.0 | False |

## Kubo outlier-rich, N = 200

Source: [`phase4/kubo_structure/claim/outlier_rich_n200_window.json`](../../phase4/kubo_structure/claim/outlier_rich_n200_window.json).

| D | Seeds | R | R >= 0.90 |
|---|---|---|---|
| 1 | 200 | 0.745 | no |
| 2 | 200 | 0.855 | no |
| 3 | 200 | 0.835 | no |
| 4 | 200 | 0.86 | no |
| 6 | 200 | 0.89 | no |
| 10 | 200 | 0.875 | no |
| 15 | 200 | 0.855 | no |
| 20 | 200 | 0.935 | yes |
| 25 | 200 | 0.91 | yes |
| 35 | 30 | 0.967 | yes |

D_min diem: 20. Khoang bootstrap: [2, 20]. Gia tri D = 35 co 30 seed scout vi o nay khong duoc gieo lai claim; cac gia tri D = 1 den 25 o tren co 200 seed claim.

## Bang chung transfer kich thuoc day du

Summary source: [`phase4/package_d/size/transfer_summary.csv`](../../phase4/package_d/size/transfer_summary.csv).

| n_rows | n_shared | n_shifted | n_absent |
|---|---|---|---|
| 44 | 8 | 7 | 29 |

Detailed source: [`phase4/package_d/size/transfer_table.csv`](../../phase4/package_d/size/transfer_table.csv).

| feature | n_sheep | baseline | method | baseline_value | method_value | transfer_label |
|---|---|---|---|---|---|---|
| d_min | 5.0 | strombom_multi | kubo | 2 | 3 | shifted |
| d_min | 10.0 | strombom_multi | kubo | 2 | 1 | shifted |
| d_min | 25.0 | strombom_multi | kubo | 1 | 1 | shared |
| d_min | 50.0 | strombom_multi | kubo | 1 | 1 | shared |
| d_min | 75.0 | strombom_multi | kubo | 1 | 1 | shared |
| d_min | 100.0 | strombom_multi | kubo | 1 | 1 | shared |
| d_min | 150.0 | strombom_multi | kubo | 1 | 1 | shared |
| d_min | 200.0 | strombom_multi | kubo | 1 | 1 | shared |
| d_min | 300.0 | strombom_multi | kubo | 1 | 1 | shared |
| d_min | 400.0 | strombom_multi | kubo | 1 | 1 | shared |
| overcrowd | 5.0 | strombom_multi | kubo |  |  | absent |
| overcrowd | 10.0 | strombom_multi | kubo |  |  | absent |
| overcrowd | 25.0 | strombom_multi | kubo |  |  | absent |
| overcrowd | 50.0 | strombom_multi | kubo |  |  | absent |
| overcrowd | 75.0 | strombom_multi | kubo |  |  | absent |
| overcrowd | 100.0 | strombom_multi | kubo |  |  | absent |
| overcrowd | 150.0 | strombom_multi | kubo |  |  | absent |
| overcrowd | 200.0 | strombom_multi | kubo |  |  | absent |
| overcrowd | 300.0 | strombom_multi | kubo |  |  | absent |
| overcrowd | 400.0 | strombom_multi | kubo |  |  | absent |
| i_dir_signature |  | strombom_multi | kubo | 0.261464147747486 | -0.0018854696882589974 | absent |
| coverage_saturation |  | strombom_multi | kubo | True | False | shifted |
| d_min | 5.0 | strombom_multi | fat | 2 | 1.0 | shifted |
| d_min | 10.0 | strombom_multi | fat | 2 | 1.0 | shifted |
| d_min | 25.0 | strombom_multi | fat | 1 |  | absent |
| d_min | 50.0 | strombom_multi | fat | 1 |  | absent |
| d_min | 75.0 | strombom_multi | fat | 1 |  | absent |
| d_min | 100.0 | strombom_multi | fat | 1 |  | absent |
| d_min | 150.0 | strombom_multi | fat | 1 |  | absent |
| d_min | 200.0 | strombom_multi | fat | 1 |  | absent |
| d_min | 300.0 | strombom_multi | fat | 1 |  | absent |
| d_min | 400.0 | strombom_multi | fat | 1 |  | absent |
| overcrowd | 5.0 | strombom_multi | fat |  |  | absent |
| overcrowd | 10.0 | strombom_multi | fat |  |  | absent |
| overcrowd | 25.0 | strombom_multi | fat |  |  | absent |
| overcrowd | 50.0 | strombom_multi | fat |  |  | absent |
| overcrowd | 75.0 | strombom_multi | fat |  |  | absent |
| overcrowd | 100.0 | strombom_multi | fat |  |  | absent |
| overcrowd | 150.0 | strombom_multi | fat |  |  | absent |
| overcrowd | 200.0 | strombom_multi | fat |  |  | absent |
| overcrowd | 300.0 | strombom_multi | fat |  |  | absent |
| overcrowd | 400.0 | strombom_multi | fat |  |  | absent |
| i_dir_signature |  | strombom_multi | fat | 0.261464147747486 | -0.8678074971276444 | shifted |
| coverage_saturation |  | strombom_multi | fat | True |  | shifted |

## Luoc do cua cac bang merged_trials

Moi dong la mot lan mo phong voi mot seed. Ten cot thuc te duoc bao cao trong tung muc du lieu; cac nhom sau giai thich y nghia.

| Nhom | Cot va y nghia |
|---|---|
| Danh tinh va thiet ke | method, scenario, preset, seed, sheep_model, dog_controller, obs_mode, n_sheep, n_shepherds, initial_layout, time_limit |
| Ket qua va chi phi | success, total_ticks, time_to_goal, shepherd_path, first_success_tick, control_efficiency |
| Trang thai cuoi | final_gcm_goal, final_success_rate, final_sheep_in_goal, final_min_separation |
| Tom tat theo thoi gian | mean_*, min_*, max_*, auc_* for recorded flock and dog metrics |
| Chan doan that bai | failure_mode, failure_label, failure_hints |
| Cau hinh | resolved_config, the serialized effective trial configuration |

## Claim merge: Phase 4 Kubo size

Nguon day du: [`phase4/kubo_size/claim/merged_trials.csv`](../../phase4/kubo_size/claim/merged_trials.csv). Bang lon khong duoc chep lai. Cac thong ke duoi day duoc tinh truc tiep tu CSV.

| Thuoc tinh | Gia tri |
|---|---|
| So dong | 4,470 |
| So cot | 77 |
| So o thiet ke | 100 |
| Phuong phap | kubo |
| Bo cuc | compact |
| Cac gia tri N | 5, 10, 25, 50, 75, 100, 150, 200, 300, 400 |
| Cac gia tri D | 1, 2, 3, 4, 6, 10, 15, 20, 25, 35 |
| Khoang seed | 2026 to 2125 |

| Thuoc tinh | Gia tri |
|---|---|
| Thanh cong | 4,428 |
| That bai | 42 |
| R toan bo | 0.991 |
| Trung vi tick, ca thanh cong | 826 |
| P90 tick, ca thanh cong | 1,785.3 |
| Trung vi quang duong, ca thanh cong | 291.202 |
| Nhan that bai | timeout: 42 |

Quy tac chon dong dai dien: sap xep tu dien theo `method`, `initial_layout`, `n_sheep`, `n_shepherds`, `seed`, sau do lay 5 vi tri cach deu, gom hai dau. Quy tac nay trung lap duoc va khong chon theo ket qua.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| kubo | compact | 5 | 1 | 2026 | True | 1133 | 115.167 | none |
| kubo | compact | 25 | 2 | 2093 | True | 941 | 213.556 | none |
| kubo | compact | 75 | 25 | 2050 | True | 670 | 1,810 | none |
| kubo | compact | 200 | 3 | 2028 | True | 699 | 233.401 | none |
| kubo | compact | 400 | 35 | 2055 | True | 558 | 2,427.984 | none |

## Claim merge: Phase 4 FAT size

Nguon day du: [`phase4/fat_size/claim/merged_trials.csv`](../../phase4/fat_size/claim/merged_trials.csv). Bang lon khong duoc chep lai. Cac thong ke duoi day duoc tinh truc tiep tu CSV.

| Thuoc tinh | Gia tri |
|---|---|
| So dong | 4,400 |
| So cot | 77 |
| So o thiet ke | 100 |
| Phuong phap | fat |
| Bo cuc | compact |
| Cac gia tri N | 5, 10, 25, 50, 75, 100, 150, 200, 300, 400 |
| Cac gia tri D | 1, 2, 3, 4, 6, 10, 15, 20, 25, 35 |
| Khoang seed | 2026 to 2125 |

| Thuoc tinh | Gia tri |
|---|---|
| Thanh cong | 2,194 |
| That bai | 2,206 |
| R toan bo | 0.499 |
| Trung vi tick, ca thanh cong | 232 |
| P90 tick, ca thanh cong | 2,371.8 |
| Trung vi quang duong, ca thanh cong | 3,183 |
| Nhan that bai | oscillation: 1707, stuck: 295, timeout: 204 |

Quy tac chon dong dai dien: sap xep tu dien theo `method`, `initial_layout`, `n_sheep`, `n_shepherds`, `seed`, sau do lay 5 vi tri cach deu, gom hai dau. Quy tac nay trung lap duoc va khong chon theo ket qua.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| fat | compact | 5 | 1 | 2026 | True | 177 | 168 | none |
| fat | compact | 25 | 20 | 2036 | True | 182 | 3,190.5 | none |
| fat | compact | 100 | 1 | 2026 | True | 216 | 162 | none |
| fat | compact | 200 | 20 | 2035 | False | 10000 | 285,885 | oscillation |
| fat | compact | 400 | 35 | 2125 | True | 262 | 5,652 | none |

## Claim merge: Phase 4 Kubo structure

Nguon day du: [`phase4/kubo_structure/claim/merged_trials.csv`](../../phase4/kubo_structure/claim/merged_trials.csv). Bang lon khong duoc chep lai. Cac thong ke duoi day duoc tinh truc tiep tu CSV.

| Thuoc tinh | Gia tri |
|---|---|
| So dong | 6,670 |
| So cot | 77 |
| So o thiet ke | 120 |
| Phuong phap | kubo |
| Bo cuc | compact, outlier_rich, split, wide |
| Cac gia tri N | 50, 100, 200 |
| Cac gia tri D | 1, 2, 3, 4, 6, 10, 15, 20, 25, 35 |
| Khoang seed | 2026 to 2225 |

| Thuoc tinh | Gia tri |
|---|---|
| Thanh cong | 5,679 |
| That bai | 991 |
| R toan bo | 0.851 |
| Trung vi tick, ca thanh cong | 1,093 |
| P90 tick, ca thanh cong | 3,193.2 |
| Trung vi quang duong, ca thanh cong | 916.136 |
| Nhan that bai | scatter: 320, stuck: 13, timeout: 658 |

Quy tac chon dong dai dien: sap xep tu dien theo `method`, `initial_layout`, `n_sheep`, `n_shepherds`, `seed`, sau do lay 5 vi tri cach deu, gom hai dau. Quy tac nay trung lap duoc va khong chon theo ket qua.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| kubo | compact | 50 | 1 | 2026 | True | 1062 | 117.755 | none |
| kubo | outlier_rich | 50 | 15 | 2053 | True | 873 | 1,339.3 | none |
| kubo | outlier_rich | 200 | 10 | 2160 | True | 2203 | 2,609.883 | none |
| kubo | split | 200 | 1 | 2118 | True | 990 | 109.823 | none |
| kubo | wide | 200 | 35 | 2125 | False | 10000 | 24,723.948 | timeout |

## Claim merge: Phase 4 FAT structure

Nguon day du: [`phase4/fat_structure/claim/merged_trials.csv`](../../phase4/fat_structure/claim/merged_trials.csv). Bang lon khong duoc chep lai. Cac thong ke duoi day duoc tinh truc tiep tu CSV.

| Thuoc tinh | Gia tri |
|---|---|
| So dong | 5,280 |
| So cot | 77 |
| So o thiet ke | 120 |
| Phuong phap | fat |
| Bo cuc | compact, outlier_rich, split, wide |
| Cac gia tri N | 50, 100, 200 |
| Cac gia tri D | 1, 2, 3, 4, 6, 10, 15, 20, 25, 35 |
| Khoang seed | 2026 to 2125 |

| Thuoc tinh | Gia tri |
|---|---|
| Thanh cong | 906 |
| That bai | 4,374 |
| R toan bo | 0.172 |
| Trung vi tick, ca thanh cong | 215 |
| P90 tick, ca thanh cong | 243 |
| Trung vi quang duong, ca thanh cong | 3,211.5 |
| Nhan that bai | oscillation: 2014, scatter: 474, split: 1298, stuck: 286, timeout: 302 |

Quy tac chon dong dai dien: sap xep tu dien theo `method`, `initial_layout`, `n_sheep`, `n_shepherds`, `seed`, sau do lay 5 vi tri cach deu, gom hai dau. Quy tac nay trung lap duoc va khong chon theo ket qua.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| fat | compact | 50 | 1 | 2026 | False | 10000 | 14,477.666 | oscillation |
| fat | outlier_rich | 50 | 1 | 2026 | False | 10000 | 13,264.5 | stuck |
| fat | split | 50 | 1 | 2026 | True | 205 | 160.5 | none |
| fat | split | 200 | 35 | 2125 | False | 10000 | 501,004.5 | oscillation |
| fat | wide | 200 | 35 | 2125 | False | 10000 | 524,968.5 | split |

## Nguon truc tiep

* [`phase4/kubo_size/claim/packages/a/frontier.csv`](../../phase4/kubo_size/claim/packages/a/frontier.csv)
* [`phase4/fat_size/claim/packages/a/frontier.csv`](../../phase4/fat_size/claim/packages/a/frontier.csv)
* [`phase4/kubo_size/claim/packages/a/dmin_bootstrap.csv`](../../phase4/kubo_size/claim/packages/a/dmin_bootstrap.csv)
* [`phase4/fat_size/claim/packages/a/dmin_bootstrap.csv`](../../phase4/fat_size/claim/packages/a/dmin_bootstrap.csv)
* [`phase4/package_d/structure/frontier_by_method_layout.csv`](../../phase4/package_d/structure/frontier_by_method_layout.csv)
* [`phase4/package_d/size/transfer_summary.csv`](../../phase4/package_d/size/transfer_summary.csv)
* [`phase4/package_d/size/transfer_table.csv`](../../phase4/package_d/size/transfer_table.csv)
* [`phase4/kubo_structure/claim/outlier_rich_n200_window.json`](../../phase4/kubo_structure/claim/outlier_rich_n200_window.json)
* [`phase4/kubo_structure/claim/merged_dmin_bootstrap.csv`](../../phase4/kubo_structure/claim/merged_dmin_bootstrap.csv)
* [`phase4/kubo_size/claim/merged_trials.csv`](../../phase4/kubo_size/claim/merged_trials.csv)
* [`phase4/fat_size/claim/merged_trials.csv`](../../phase4/fat_size/claim/merged_trials.csv)
* [`phase4/kubo_structure/claim/merged_trials.csv`](../../phase4/kubo_structure/claim/merged_trials.csv)
* [`phase4/fat_structure/claim/merged_trials.csv`](../../phase4/fat_structure/claim/merged_trials.csv)
