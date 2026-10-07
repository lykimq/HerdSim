# Bảng dữ liệu Giai đoạn 2

Bảng kết quả dùng bằng chứng claim. Bằng chứng khảo sát chọn cửa sổ chính xác và không được đọc như ước lượng cuối.

## Biên đầy đủ theo bố cục

Nguồn: [`phase2/claim/packages/b/frontier_by_layout.csv`](../../phase2/claim/packages/b/frontier_by_layout.csv).

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

Mỗi bố cục và N có `D_min = 1`, `D_max = 35` tại trần lưới, và không có quá tải. Bố cục `wide` có `B_star_D = 2` dù một chó đã đạt độ tin cậy.

## Khoảng bootstrap D_min đầy đủ

Nguồn: [`phase2/claim/merged_dmin_bootstrap.csv`](../../phase2/claim/merged_dmin_bootstrap.csv).

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

## Chi phí một chó theo bố cục

Tính từ tất cả dòng D = 1 của bản hợp nhất claim. Trung vị chỉ dùng lần thử thành công.

| Bố cục | N | Thành công | Seed | R | Trung vị tick | Trung vị path |
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

## So sánh bộ dự đoán

Nguồn: [`phase2/claim/packages/b/predictor_comparison.csv`](../../phase2/claim/packages/b/predictor_comparison.csv). Bảng này được giữ làm bằng chứng, nhưng claim bộ dự đoán trạng thái không kết luận vì D_min cơ sở không thay đổi.

| n_folds | nd_nll | state_nll | prefers_state | state_cols | note |
|---|---|---|---|---|---|
| 0 |  |  | False | ['early_cohesion', 'early_gcm_goal', 'early_time_to_goal', 'early_shepherd_path', 'early_success_rate', 'early_sheep_in_goal', 'early_polarization', 'early_outlier_count', 'early_min_separation', 'early_fragmentation', 'early_mean_spread', 'early_extent', 'early_perimeter', 'early_hull_area', 'early_flock_density', 'early_aspect_ratio', 'early_i_dir', 'early_coverage'] | need at least two flock sizes and both outcomes |

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

Nguồn đầy đủ: [`phase2/claim/merged_trials.csv`](../../phase2/claim/merged_trials.csv). Bảng lớn không được chép lại. Các thống kê dưới đây được tính trực tiếp từ CSV.

| Thuộc tính | Giá trị |
|---|---|
| Số dòng | 5,280 |
| Số cột | 77 |
| Số ô thiết kế | 120 |
| Phương pháp | strombom_multi |
| Bố cục | compact, outlier_rich, split, wide |
| Các giá trị N | 50, 100, 200 |
| Các giá trị D | 1, 2, 3, 4, 6, 10, 15, 20, 25, 35 |
| Khoảng seed | 2026 đến 2125 |

| Thuộc tính | Giá trị |
|---|---|
| Thành công | 5,280 |
| Thất bại | 0 |
| R toàn bộ | 1 |
| Trung vị tick, các thành công | 197 |
| P90 tick, các thành công | 1,313 |
| Trung vị quãng đường, các thành công | 1,802.569 |
| Nhãn thất bại | không có |

Quy tắc chọn dòng đại diện: sắp xếp từ điển theo `method`, `initial_layout`, `n_sheep`, `n_shepherds`, `seed`, sau đó lấy 5 vị trí cách đều, gồm hai đầu. Quy tắc này trung lập và không chọn theo kết quả.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | compact | 50 | 1 | 2026 | True | 198 | 157.5 | none |
| strombom_multi | outlier_rich | 50 | 1 | 2026 | True | 434 | 362.088 | none |
| strombom_multi | split | 50 | 1 | 2026 | True | 195 | 151.5 | none |
| strombom_multi | split | 200 | 35 | 2055 | True | 181 | 4,681.49 | none |
| strombom_multi | wide | 200 | 35 | 2055 | True | 1544 | 53,992.82 | none |

## Nguồn trực tiếp

* [`phase2/claim/packages/b/frontier_by_layout.csv`](../../phase2/claim/packages/b/frontier_by_layout.csv)
* [`phase2/claim/packages/b/predictor_comparison.csv`](../../phase2/claim/packages/b/predictor_comparison.csv)
* [`phase2/claim/merged_dmin_bootstrap.csv`](../../phase2/claim/merged_dmin_bootstrap.csv)
* [`phase2/claim/merged_trials.csv`](../../phase2/claim/merged_trials.csv)
* [`phase2/claim/provenance.json`](../../phase2/claim/provenance.json)
* [`phase2/claim/status.json`](../../phase2/claim/status.json)
