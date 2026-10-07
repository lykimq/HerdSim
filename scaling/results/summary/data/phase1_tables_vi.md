# Bảng dữ liệu Giai đoạn 1

Tất cả bảng kết quả khoa học trong phụ lục này dùng bản hợp nhất claim. Dữ liệu khảo sát chỉ để lập kế hoạch và được liệt kê riêng trong nhật ký chạy.

## Biên theo kích thước đàn

Nguồn: [`phase1/claim/packages/a/frontier.csv`](../../phase1/claim/packages/a/frontier.csv).

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

`D_max = 35` là trần lưới đã thử vì `D_overcrowd` trống. Đây không phải biên thất bại trên đã quan sát.

## Khoảng bootstrap D_min đầy đủ

Nguồn: [`phase1/claim/packages/a/dmin_bootstrap.csv`](../../phase1/claim/packages/a/dmin_bootstrap.csv).

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

## Số lượng chế độ

Nguồn: [`phase1/claim/packages/a/regimes.csv`](../../phase1/claim/packages/a/regimes.csv).

| Chế độ | Số ô |
|---|---|
| efficient_operation | 10 |
| under_resourced_failure | 2 |
| wasteful_overspend | 88 |

## Bằng chứng mô hình scaling

Nguồn kiểm định chéo: [`phase1/claim/packages/f/scaling_cv.csv`](../../phase1/claim/packages/f/scaling_cv.csv).

| constant | linear | power | piecewise |
|---|---|---|---|
| 0.4444444444444445 | 0.4434280392420368 | 0.24698127485541224 | 0.1317615691736825 |

Nguồn khớp mô hình: [`phase1/claim/packages/f/scaling_fits.csv`](../../phase1/claim/packages/f/scaling_fits.csv).

| model | rmse | aic | bic | params |
|---|---|---|---|---|
| constant | 0.4 | -16.3258146374206 | -16.023229544426552 | {"c": 1.2} |
| linear | 0.34811575966952635 | -17.104404235766783 | -16.499234049778693 | {"a": 1.4058156229784944, "b": -0.0015651378173269586} |
| power | 0.19957997128601312 | -28.230805287709877 | -27.625635101721784 | {"A": 2.7282498520863614, "alpha": -0.2067095373892277, "log_log_slope": -0.16464473304683952} |
| piecewise | 5.438959822042073e-16 | -266.3102111592855 | -264.79728569431524 | {"break_n": 10.0, "a1": 1.9999999999999987, "b1": 1.5888218580782547e-16, "a2": 0.9999999999999996, "b2": -7.054072800592629e-19} |

## Lược đồ của các bảng merged_trials

Mỗi dòng là một lần mô phỏng với một seed. Tên cột thực tế được báo cáo trong từng mục dữ liệu; các nhóm sau giải thích ý nghĩa.

| Nhóm | Cột và ý nghĩa |
|---|---|
| Danh tính và thiết kế | method, scenario, preset, seed, sheep_model, dog_controller, obs_mode, n_sheep, n_shepherds, initial_layout, time_limit |
| Kết quả và chi phí | success, total_ticks, time_to_goal, shepherd_path, first_success_tick, control_efficiency |
| Trạng thái cuối | final_gcm_goal, final_success_rate, final_sheep_in_goal, final_min_separation |
| Tóm tắt theo thời gian | mean_*, min_*, max_*, auc_* for recorded flock and dog metrics |
| Chẩn đoán thất bại | failure_mode, failure_label, failure_hints |
| Cấu hình | resolved_config, the serialized effective trial configuration |

## Thử nghiệm hợp nhất claim

Nguồn đầy đủ: [`phase1/claim/merged_trials.csv`](../../phase1/claim/merged_trials.csv). Bảng lớn không được chép lại. Các thống kê dưới đây được tính trực tiếp từ CSV.

| Thuộc tính | Giá trị |
|---|---|
| Số dòng | 4,540 |
| Số cột | 61 |
| Số ô thiết kế | 100 |
| Phương pháp | strombom_multi |
| Bố cục | compact |
| Các giá trị N | 5, 10, 25, 50, 75, 100, 150, 200, 300, 400 |
| Các giá trị D | 1, 2, 3, 4, 6, 10, 15, 20, 25, 35 |
| Khoảng seed | 2026 đến 2125 |

| Thuộc tính | Giá trị |
|---|---|
| Thành công | 4,371 |
| Thất bại | 169 |
| R toàn bộ | 0.963 |
| Trung vị tick, các thành công | 182 |
| P90 tick, các thành công | 195 |
| Trung vị quãng đường, các thành công | 502.335 |
| Nhãn thất bại | oscillation: 111, stuck: 58 |

Quy tắc chọn dòng đại diện: sắp xếp từ điển theo `method`, `initial_layout`, `n_sheep`, `n_shepherds`, `seed`, sau đó lấy 5 vị trí cách đều, gồm hai đầu. Quy tắc này trung lập và không chọn theo kết quả.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | compact | 5 | 1 | 2026 | False | 10000 | 2,718 | oscillation |
| strombom_multi | compact | 25 | 2 | 2041 | True | 180 | 331.006 | none |
| strombom_multi | compact | 75 | 20 | 2046 | True | 183 | 2,975.227 | none |
| strombom_multi | compact | 200 | 2 | 2110 | True | 179 | 269.961 | none |
| strombom_multi | compact | 400 | 35 | 2055 | True | 164 | 3,955.479 | none |

## Nguồn trực tiếp

* [`phase1/claim/packages/a/frontier.csv`](../../phase1/claim/packages/a/frontier.csv)
* [`phase1/claim/packages/a/reliability.csv`](../../phase1/claim/packages/a/reliability.csv)
* [`phase1/claim/packages/a/dmin_bootstrap.csv`](../../phase1/claim/packages/a/dmin_bootstrap.csv)
* [`phase1/claim/packages/a/regimes.csv`](../../phase1/claim/packages/a/regimes.csv)
* [`phase1/claim/packages/f/scaling_cv.csv`](../../phase1/claim/packages/f/scaling_cv.csv)
* [`phase1/claim/packages/f/scaling_fits.csv`](../../phase1/claim/packages/f/scaling_fits.csv)
* [`phase1/claim/merged_trials.csv`](../../phase1/claim/merged_trials.csv)
* [`phase1/claim/provenance.json`](../../phase1/claim/provenance.json)
* [`phase1/claim/status.json`](../../phase1/claim/status.json)
