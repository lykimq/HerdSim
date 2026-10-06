# Bang du lieu Giai doan 1

Tat ca bang ket qua khoa hoc trong phu luc nay dung merge claim. Du lieu scout chi de lap ke hoach va duoc liet ke rieng trong so cai chay.

## Bien theo kich thuoc dan

Source: [`phase1/claim/packages/a/frontier.csv`](../../phase1/claim/packages/a/frontier.csv).

| initial_layout | n_sheep | d_min | d_overcrowd | d_max | b_star_d | b_star_t | b_star_effort | hard_failure |
|---|---|---|---|---|---|---|---|---|
| compact | 5 | 2 |  | 35 | 2 | 10000.0 | 335.0757209570848 | False |
| compact | 10 | 2 |  | 35 | 2 | 10000.0 | 328.75622089181064 | False |
| compact | 25 | 1 |  | 35 | 1 | 10000.0 | 163.4999999999999 | False |
| compact | 50 | 1 |  | 35 | 1 | 10000.0 | 157.49999999999977 | False |
| compact | 75 | 1 |  | 35 | 1 | 10000.0 | 155.8911078292099 | False |
| compact | 100 | 1 |  | 35 | 1 | 10000.0 | 161.35167363755858 | False |
| compact | 150 | 1 |  | 35 | 1 | 10000.0 | 153.02725443107565 | False |
| compact | 200 | 1 |  | 35 | 1 | 10000.0 | 144.17124164542776 | False |
| compact | 300 | 1 |  | 35 | 1 | 10000.0 | 130.81134639802144 | False |
| compact | 400 | 1 |  | 35 | 1 | 10000.0 | 119.83311309692806 | False |

`D_max = 35` la tran cua luoi da thu vi `D_overcrowd` trong. Day khong phai bien that bai tren da quan sat.

## Khoang bootstrap D_min day du

Source: [`phase1/claim/packages/a/dmin_bootstrap.csv`](../../phase1/claim/packages/a/dmin_bootstrap.csv).

| initial_layout | n_sheep | d_min | d_min_ci_low | d_min_ci_high | n_boot | n_seeds_ref | n_boot_defined |
|---|---|---|---|---|---|---|---|
| compact | 5 | 2 | 2 | 2 | 1000 | 100 | 1000 |
| compact | 10 | 2 | 2 | 2 | 1000 | 100 | 1000 |
| compact | 25 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 50 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 75 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 100 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 150 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 200 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 300 | 1 | 1 | 1 | 1000 | 100 | 1000 |
| compact | 400 | 1 | 1 | 1 | 1000 | 100 | 1000 |

## So luong che do

Source: [`phase1/claim/packages/a/regimes.csv`](../../phase1/claim/packages/a/regimes.csv).

| Che do | So o |
|---|---|
| efficient_operation | 10 |
| under_resourced_failure | 2 |
| wasteful_overspend | 88 |

## Bang chung mo hinh scaling

Cross-validation source: [`phase1/claim/packages/f/scaling_cv.csv`](../../phase1/claim/packages/f/scaling_cv.csv).

| constant | linear | power | piecewise |
|---|---|---|---|
| 0.4444444444444445 | 0.4434280392420368 | 0.24698127485541224 | 0.1317615691736825 |

Fit source: [`phase1/claim/packages/f/scaling_fits.csv`](../../phase1/claim/packages/f/scaling_fits.csv).

| model | rmse | aic | bic | params |
|---|---|---|---|---|
| constant | 0.4 | -16.3258146374206 | -16.023229544426552 | {"c": 1.2} |
| linear | 0.34811575966952635 | -17.104404235766783 | -16.499234049778693 | {"a": 1.4058156229784944, "b": -0.0015651378173269586} |
| power | 0.19957997128601312 | -28.230805287709877 | -27.625635101721784 | {"A": 2.7282498520863614, "alpha": -0.2067095373892277, "log_log_slope": -0.16464473304683952} |
| piecewise | 5.438959822042073e-16 | -266.3102111592855 | -264.79728569431524 | {"break_n": 10.0, "a1": 1.9999999999999987, "b1": 1.5888218580782547e-16, "a2": 0.9999999999999996, "b2": -7.054072800592629e-19} |

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

Nguon day du: [`phase1/claim/merged_trials.csv`](../../phase1/claim/merged_trials.csv). Bang lon khong duoc chep lai. Cac thong ke duoi day duoc tinh truc tiep tu CSV.

| Thuoc tinh | Gia tri |
|---|---|
| So dong | 4,540 |
| So cot | 61 |
| So o thiet ke | 100 |
| Phuong phap | strombom_multi |
| Bo cuc | compact |
| Cac gia tri N | 5, 10, 25, 50, 75, 100, 150, 200, 300, 400 |
| Cac gia tri D | 1, 2, 3, 4, 6, 10, 15, 20, 25, 35 |
| Khoang seed | 2026 to 2125 |

| Thuoc tinh | Gia tri |
|---|---|
| Thanh cong | 4,371 |
| That bai | 169 |
| R toan bo | 0.963 |
| Trung vi tick, ca thanh cong | 182 |
| P90 tick, ca thanh cong | 195 |
| Trung vi quang duong, ca thanh cong | 502.335 |
| Nhan that bai | oscillation: 111, stuck: 58 |

Quy tac chon dong dai dien: sap xep tu dien theo `method`, `initial_layout`, `n_sheep`, `n_shepherds`, `seed`, sau do lay 5 vi tri cach deu, gom hai dau. Quy tac nay trung lap duoc va khong chon theo ket qua.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | compact | 5 | 1 | 2026 | False | 10000 | 2,718 | oscillation |
| strombom_multi | compact | 25 | 2 | 2041 | True | 180 | 331.006 | none |
| strombom_multi | compact | 75 | 20 | 2046 | True | 183 | 2,975.227 | none |
| strombom_multi | compact | 200 | 2 | 2110 | True | 179 | 269.961 | none |
| strombom_multi | compact | 400 | 35 | 2055 | True | 164 | 3,955.479 | none |

## Nguon truc tiep

* [`phase1/claim/packages/a/frontier.csv`](../../phase1/claim/packages/a/frontier.csv)
* [`phase1/claim/packages/a/reliability.csv`](../../phase1/claim/packages/a/reliability.csv)
* [`phase1/claim/packages/a/dmin_bootstrap.csv`](../../phase1/claim/packages/a/dmin_bootstrap.csv)
* [`phase1/claim/packages/a/regimes.csv`](../../phase1/claim/packages/a/regimes.csv)
* [`phase1/claim/packages/f/scaling_cv.csv`](../../phase1/claim/packages/f/scaling_cv.csv)
* [`phase1/claim/packages/f/scaling_fits.csv`](../../phase1/claim/packages/f/scaling_fits.csv)
* [`phase1/claim/merged_trials.csv`](../../phase1/claim/merged_trials.csv)
* [`phase1/claim/provenance.json`](../../phase1/claim/provenance.json)
* [`phase1/claim/status.json`](../../phase1/claim/status.json)
