# Bang du lieu Giai doan 2

Bang ket qua dung bang chung claim. Bang chung scout chon cua so chinh xac va khong duoc doc nhu uoc luong cuoi.

## Bien day du theo bo cuc

Source: [`phase2/claim/packages/b/frontier_by_layout.csv`](../../phase2/claim/packages/b/frontier_by_layout.csv).

| initial_layout | n_sheep | d_min | d_overcrowd | d_max | b_star_d | b_star_t | b_star_effort | hard_failure |
|---|---|---|---|---|---|---|---|---|
| compact | 50 | 1 |  | 35 | 1 | 10000.0 | 157.49999999999977 | False |
| compact | 100 | 1 |  | 35 | 1 | 10000.0 | 161.35167363755858 | False |
| compact | 200 | 1 |  | 35 | 1 | 10000.0 | 144.17124164542776 | False |
| outlier_rich | 50 | 1 |  | 35 | 1 | 10000.0 | 209.24999999999994 | False |
| outlier_rich | 100 | 1 |  | 35 | 1 | 10000.0 | 553.8718780756371 | False |
| outlier_rich | 200 | 1 |  | 35 | 1 | 10000.0 | 1646.6909610899515 | False |
| split | 50 | 1 |  | 35 | 1 | 10000.0 | 157.5 | False |
| split | 100 | 1 |  | 35 | 1 | 10000.0 | 161.95821333206823 | False |
| split | 200 | 1 |  | 35 | 1 | 10000.0 | 144.40420419240473 | False |
| wide | 50 | 1 |  | 35 | 2 | 10000.0 | 2336.832941075605 | False |
| wide | 100 | 1 |  | 35 | 2 | 10000.0 | 3003.1703685972398 | False |
| wide | 200 | 1 |  | 35 | 2 | 10000.0 | 3693.6903356986063 | False |

Moi bo cuc va N co `D_min = 1`, `D_max = 35` tai tran luoi, va khong co overcrowding. Bo cuc wide co `B_star_D = 2` du mot cho da dat do tin cay.

## Khoang bootstrap D_min day du

Source: [`phase2/claim/merged_dmin_bootstrap.csv`](../../phase2/claim/merged_dmin_bootstrap.csv).

| method | initial_layout | n_sheep | d_min | d_min_ci_low | d_min_ci_high | n_boot | n_seeds_ref | n_boot_defined |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | compact | 50 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | compact | 100 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | compact | 200 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | outlier_rich | 50 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | outlier_rich | 100 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | outlier_rich | 200 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | split | 50 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | split | 100 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | split | 200 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | wide | 50 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | wide | 100 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| strombom_multi | wide | 200 | 1 | 1 | 1 | 1000 | 100 | 1000 |

## Chi phi mot cho theo bo cuc

Tinh tu tat ca dong D = 1 cua claim merge. Trung vi chi dung trial thanh cong.

| Bo cuc | N | Thanh cong | Seed | R | Trung vi tick | Trung vi path |
|---|---|---|---|---|---|---|
| compact | 50 | 100 | 100 | 1 | 195 | 157.5 |
| compact | 100 | 100 | 100 | 1 | 204 | 161.352 |
| compact | 200 | 100 | 100 | 1 | 191 | 144.171 |
| outlier_rich | 50 | 100 | 100 | 1 | 223.5 | 209.25 |
| outlier_rich | 100 | 100 | 100 | 1 | 501 | 553.872 |
| outlier_rich | 200 | 100 | 100 | 1 | 1,228 | 1,646.691 |
| split | 50 | 100 | 100 | 1 | 195 | 157.5 |
| split | 100 | 100 | 100 | 1 | 205 | 161.958 |
| split | 200 | 100 | 100 | 1 | 193 | 144.404 |
| wide | 50 | 100 | 100 | 1 | 2,138.5 | 2,925.126 |
| wide | 100 | 100 | 100 | 1 | 3,074 | 4,319.485 |
| wide | 200 | 100 | 100 | 1 | 3,869.5 | 5,213.019 |

## So sanh predictor

Source: [`phase2/claim/packages/b/predictor_comparison.csv`](../../phase2/claim/packages/b/predictor_comparison.csv). Bang nay duoc giu lam bang chung, nhung claim predictor trang thai khong ket luan vi D_min baseline khong thay doi.

| n_folds | nd_nll | state_nll | prefers_state | state_cols | note |
|---|---|---|---|---|---|
| 0 |  |  | False | ['early_cohesion', 'early_gcm_goal', 'early_time_to_goal', 'early_shepherd_path', 'early_success_rate', 'early_sheep_in_goal', 'early_polarization', 'early_outlier_count', 'early_min_separation', 'early_fragmentation', 'early_mean_spread', 'early_extent', 'early_perimeter', 'early_hull_area', 'early_flock_density', 'early_aspect_ratio', 'early_i_dir', 'early_coverage'] | need at least two flock sizes and both outcomes |

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

## Trial merge claim

Nguon day du: [`phase2/claim/merged_trials.csv`](../../phase2/claim/merged_trials.csv). Bang lon khong duoc chep lai. Cac thong ke duoi day duoc tinh truc tiep tu CSV.

| Thuoc tinh | Gia tri |
|---|---|
| So dong | 5,280 |
| So cot | 77 |
| So o thiet ke | 120 |
| Phuong phap | strombom_multi |
| Bo cuc | compact, outlier_rich, split, wide |
| Cac gia tri N | 50, 100, 200 |
| Cac gia tri D | 1, 2, 3, 4, 6, 10, 15, 20, 25, 35 |
| Khoang seed | 2026 to 2125 |

| Thuoc tinh | Gia tri |
|---|---|
| Thanh cong | 5,280 |
| That bai | 0 |
| R toan bo | 1 |
| Trung vi tick, ca thanh cong | 197 |
| P90 tick, ca thanh cong | 1,313 |
| Trung vi quang duong, ca thanh cong | 1,802.569 |
| Nhan that bai | none |

Quy tac chon dong dai dien: sap xep tu dien theo `method`, `initial_layout`, `n_sheep`, `n_shepherds`, `seed`, sau do lay 5 vi tri cach deu, gom hai dau. Quy tac nay trung lap duoc va khong chon theo ket qua.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | compact | 50 | 1 | 2026 | True | 198 | 157.5 | none |
| strombom_multi | outlier_rich | 50 | 1 | 2026 | True | 434 | 362.088 | none |
| strombom_multi | split | 50 | 1 | 2026 | True | 195 | 151.5 | none |
| strombom_multi | split | 200 | 35 | 2055 | True | 181 | 4,681.49 | none |
| strombom_multi | wide | 200 | 35 | 2055 | True | 1544 | 53,992.82 | none |

## Nguon truc tiep

* [`phase2/claim/packages/b/frontier_by_layout.csv`](../../phase2/claim/packages/b/frontier_by_layout.csv)
* [`phase2/claim/packages/b/predictor_comparison.csv`](../../phase2/claim/packages/b/predictor_comparison.csv)
* [`phase2/claim/merged_dmin_bootstrap.csv`](../../phase2/claim/merged_dmin_bootstrap.csv)
* [`phase2/claim/merged_trials.csv`](../../phase2/claim/merged_trials.csv)
* [`phase2/claim/provenance.json`](../../phase2/claim/provenance.json)
* [`phase2/claim/status.json`](../../phase2/claim/status.json)
