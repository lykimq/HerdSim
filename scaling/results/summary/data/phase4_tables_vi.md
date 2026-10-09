# Bảng dữ liệu Giai đoạn 4

Kết luận về bộ điều khiển dùng bản hợp nhất claim. Lưới khảo sát vẫn chỉ là bằng chứng lập kế hoạch. Bảng Package D so sánh kết quả bộ điều khiển cấp claim.

## Biên kích thước với bố cục compact

Nguồn Kubo: [`phase4/kubo_size/claim/packages/a/frontier.csv`](../../phase4/kubo_size/claim/packages/a/frontier.csv).

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

Nguồn FAT: [`phase4/fat_size/claim/packages/a/frontier.csv`](../../phase4/fat_size/claim/packages/a/frontier.csv).

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

Các trường biên trống với `hard_failure = True` nghĩa là không D nào đạt R = 0.90. Chúng không phải ước lượng giới hạn trên.

## Khoảng bootstrap D_min kích thước đầy đủ

Nguồn Kubo: [`phase4/kubo_size/claim/packages/a/dmin_bootstrap.csv`](../../phase4/kubo_size/claim/packages/a/dmin_bootstrap.csv).

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

Nguồn FAT: [`phase4/fat_size/claim/packages/a/dmin_bootstrap.csv`](../../phase4/fat_size/claim/packages/a/dmin_bootstrap.csv).

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

## Biên đầy đủ theo bộ điều khiển và bố cục

Nguồn: [`phase4/package_d/structure/frontier_by_method_layout.csv`](../../phase4/package_d/structure/frontier_by_method_layout.csv).

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

## Kubo outlier_rich, N = 200

Nguồn: [`phase4/kubo_structure/claim/outlier_rich_n200_window.json`](../../phase4/kubo_structure/claim/outlier_rich_n200_window.json).

| D | Seed | R | R >= 0.90 |
|---|---|---|---|
| 1 | 200 | 0.745 | không |
| 2 | 200 | 0.855 | không |
| 3 | 200 | 0.835 | không |
| 4 | 200 | 0.86 | không |
| 6 | 200 | 0.89 | không |
| 10 | 200 | 0.875 | không |
| 15 | 200 | 0.855 | không |
| 20 | 200 | 0.935 | có |
| 25 | 200 | 0.91 | có |
| 35 | 30 | 0.967 | có |

D_min điểm: 20. Khoảng bootstrap: [2, 20]. Giá trị D = 35 có 30 seed khảo sát vì ô này không được gieo lại claim; các giá trị D = 1 đến 25 ở trên có 200 seed claim.

## Bằng chứng chuyển giao kích thước đầy đủ

Nguồn tóm tắt: [`phase4/package_d/size/transfer_summary.csv`](../../phase4/package_d/size/transfer_summary.csv).

| n_rows | n_shared | n_shifted | n_absent |
|---|---|---|---|
| 44 | 8 | 7 | 29 |

Nguồn chi tiết: [`phase4/package_d/size/transfer_table.csv`](../../phase4/package_d/size/transfer_table.csv).

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

## Hợp nhất claim: Giai đoạn 4 Kubo kích thước

Nguồn đầy đủ: [`phase4/kubo_size/claim/merged_trials.csv`](../../phase4/kubo_size/claim/merged_trials.csv). Bảng lớn không được chép lại. Các thống kê dưới đây được tính trực tiếp từ CSV.

| Thuộc tính | Giá trị |
|---|---|
| Số dòng | 4,470 |
| Số cột | 77 |
| Số ô thiết kế | 100 |
| Phương pháp | kubo |
| Bố cục | compact |
| Các giá trị N | 5, 10, 25, 50, 75, 100, 150, 200, 300, 400 |
| Các giá trị D | 1, 2, 3, 4, 6, 10, 15, 20, 25, 35 |
| Khoảng seed | 2026 đến 2125 |

| Thuộc tính | Giá trị |
|---|---|
| Thành công | 4,428 |
| Thất bại | 42 |
| R toàn bộ | 0.991 |
| Trung vị tick, các thành công | 826 |
| P90 tick, các thành công | 1,785.3 |
| Trung vị quãng đường, các thành công | 291.202 |
| Nhãn thất bại | timeout: 42 |

Quy tắc chọn dòng đại diện: sắp xếp từ điển theo `method`, `initial_layout`, `n_sheep`, `n_shepherds`, `seed`, sau đó lấy 5 vị trí cách đều, gồm hai đầu. Quy tắc này trung lập và không chọn theo kết quả.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| kubo | compact | 5 | 1 | 2026 | True | 1133 | 115.167 | none |
| kubo | compact | 25 | 2 | 2093 | True | 941 | 213.556 | none |
| kubo | compact | 75 | 25 | 2050 | True | 670 | 1,810 | none |
| kubo | compact | 200 | 3 | 2028 | True | 699 | 233.401 | none |
| kubo | compact | 400 | 35 | 2055 | True | 558 | 2,427.984 | none |

## Hợp nhất claim: Giai đoạn 4 FAT kích thước

Nguồn đầy đủ: [`phase4/fat_size/claim/merged_trials.csv`](../../phase4/fat_size/claim/merged_trials.csv). Bảng lớn không được chép lại. Các thống kê dưới đây được tính trực tiếp từ CSV.

| Thuộc tính | Giá trị |
|---|---|
| Số dòng | 4,400 |
| Số cột | 77 |
| Số ô thiết kế | 100 |
| Phương pháp | fat |
| Bố cục | compact |
| Các giá trị N | 5, 10, 25, 50, 75, 100, 150, 200, 300, 400 |
| Các giá trị D | 1, 2, 3, 4, 6, 10, 15, 20, 25, 35 |
| Khoảng seed | 2026 đến 2125 |

| Thuộc tính | Giá trị |
|---|---|
| Thành công | 2,194 |
| Thất bại | 2,206 |
| R toàn bộ | 0.499 |
| Trung vị tick, các thành công | 232 |
| P90 tick, các thành công | 2,371.8 |
| Trung vị quãng đường, các thành công | 3,183 |
| Nhãn thất bại | oscillation: 1707, stuck: 295, timeout: 204 |

Quy tắc chọn dòng đại diện: sắp xếp từ điển theo `method`, `initial_layout`, `n_sheep`, `n_shepherds`, `seed`, sau đó lấy 5 vị trí cách đều, gồm hai đầu. Quy tắc này trung lập và không chọn theo kết quả.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| fat | compact | 5 | 1 | 2026 | True | 177 | 168 | none |
| fat | compact | 25 | 20 | 2036 | True | 182 | 3,190.5 | none |
| fat | compact | 100 | 1 | 2026 | True | 216 | 162 | none |
| fat | compact | 200 | 20 | 2035 | False | 10000 | 285,885 | oscillation |
| fat | compact | 400 | 35 | 2125 | True | 262 | 5,652 | none |

## Hợp nhất claim: Giai đoạn 4 Kubo cấu trúc

Nguồn đầy đủ: [`phase4/kubo_structure/claim/merged_trials.csv`](../../phase4/kubo_structure/claim/merged_trials.csv). Bảng lớn không được chép lại. Các thống kê dưới đây được tính trực tiếp từ CSV.

| Thuộc tính | Giá trị |
|---|---|
| Số dòng | 6,670 |
| Số cột | 77 |
| Số ô thiết kế | 120 |
| Phương pháp | kubo |
| Bố cục | compact, outlier_rich, split, wide |
| Các giá trị N | 50, 100, 200 |
| Các giá trị D | 1, 2, 3, 4, 6, 10, 15, 20, 25, 35 |
| Khoảng seed | 2026 đến 2225 |

| Thuộc tính | Giá trị |
|---|---|
| Thành công | 5,679 |
| Thất bại | 991 |
| R toàn bộ | 0.851 |
| Trung vị tick, các thành công | 1,093 |
| P90 tick, các thành công | 3,193.2 |
| Trung vị quãng đường, các thành công | 916.136 |
| Nhãn thất bại | scatter: 320, stuck: 13, timeout: 658 |

Quy tắc chọn dòng đại diện: sắp xếp từ điển theo `method`, `initial_layout`, `n_sheep`, `n_shepherds`, `seed`, sau đó lấy 5 vị trí cách đều, gồm hai đầu. Quy tắc này trung lập và không chọn theo kết quả.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| kubo | compact | 50 | 1 | 2026 | True | 1062 | 117.755 | none |
| kubo | outlier_rich | 50 | 15 | 2053 | True | 873 | 1,339.3 | none |
| kubo | outlier_rich | 200 | 10 | 2160 | True | 2203 | 2,609.883 | none |
| kubo | split | 200 | 1 | 2118 | True | 990 | 109.823 | none |
| kubo | wide | 200 | 35 | 2125 | False | 10000 | 24,723.948 | timeout |

## Hợp nhất claim: Giai đoạn 4 FAT cấu trúc

Nguồn đầy đủ: [`phase4/fat_structure/claim/merged_trials.csv`](../../phase4/fat_structure/claim/merged_trials.csv). Bảng lớn không được chép lại. Các thống kê dưới đây được tính trực tiếp từ CSV.

| Thuộc tính | Giá trị |
|---|---|
| Số dòng | 5,280 |
| Số cột | 77 |
| Số ô thiết kế | 120 |
| Phương pháp | fat |
| Bố cục | compact, outlier_rich, split, wide |
| Các giá trị N | 50, 100, 200 |
| Các giá trị D | 1, 2, 3, 4, 6, 10, 15, 20, 25, 35 |
| Khoảng seed | 2026 đến 2125 |

| Thuộc tính | Giá trị |
|---|---|
| Thành công | 906 |
| Thất bại | 4,374 |
| R toàn bộ | 0.172 |
| Trung vị tick, các thành công | 215 |
| P90 tick, các thành công | 243 |
| Trung vị quãng đường, các thành công | 3,211.5 |
| Nhãn thất bại | oscillation: 2014, scatter: 474, split: 1298, stuck: 286, timeout: 302 |

Quy tắc chọn dòng đại diện: sắp xếp từ điển theo `method`, `initial_layout`, `n_sheep`, `n_shepherds`, `seed`, sau đó lấy 5 vị trí cách đều, gồm hai đầu. Quy tắc này trung lập và không chọn theo kết quả.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| fat | compact | 50 | 1 | 2026 | False | 10000 | 14,477.666 | oscillation |
| fat | outlier_rich | 50 | 1 | 2026 | False | 10000 | 13,264.5 | stuck |
| fat | split | 50 | 1 | 2026 | True | 205 | 160.5 | none |
| fat | split | 200 | 35 | 2125 | False | 10000 | 501,004.5 | oscillation |
| fat | wide | 200 | 35 | 2125 | False | 10000 | 524,968.5 | split |

## Hợp nhất claim: Giai đoạn 5 observation

Nguồn đầy đủ: [`phase5/obs_claim/merged_trials.csv`](../../phase5/obs_claim/merged_trials.csv). Bảng lớn không được chép lại. Các thống kê dưới đây được tính trực tiếp từ CSV.

| Thuộc tính | Giá trị |
|---|---|
| Số dòng | 1,920 |
| Số cột | 77 |
| Số ô thiết kế | 12 |
| Phương pháp | strombom_multi |
| Bố cục | compact |
| Các giá trị N | 100, 200 |
| Các giá trị D | 1, 2, 3, 4, 6, 10 |
| Khoảng seed | 2026 đến 2125 |

| Thuộc tính | Giá trị |
|---|---|
| Thành công | 1,280 |
| Thất bại | 640 |
| R toàn bộ | 0.667 |
| Trung vị tick, các thành công | 189 |
| P90 tick, các thành công | 203 |
| Trung vị quãng đường, các thành công | 294.917 |
| Nhãn thất bại | oscillation: 640 |

Quy tắc chọn dòng đại diện: sắp xếp từ điển theo `method`, `initial_layout`, `n_sheep`, `n_shepherds`, `seed`, sau đó lấy 5 vị trí cách đều, gồm hai đầu. Quy tắc này trung lập và không chọn theo kết quả.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | compact | 100 | 1 | 2026 | False | 10000 | 0 | oscillation |
| strombom_multi | compact | 100 | 3 | 2032 | True | 193 | 456.715 | none |
| strombom_multi | compact | 200 | 1 | 2026 | False | 10000 | 0 | oscillation |
| strombom_multi | compact | 200 | 3 | 2032 | True | 181 | 404.507 | none |
| strombom_multi | compact | 200 | 10 | 2125 | False | 10000 | 0 | oscillation |

## Hợp nhất claim: Giai đoạn 5 range

Nguồn đầy đủ: [`phase5/range_claim/merged_trials.csv`](../../phase5/range_claim/merged_trials.csv). Bảng lớn không được chép lại. Các thống kê dưới đây được tính trực tiếp từ CSV.

| Thuộc tính | Giá trị |
|---|---|
| Số dòng | 2,560 |
| Số cột | 78 |
| Số ô thiết kế | 12 |
| Phương pháp | strombom_multi |
| Bố cục | compact |
| Các giá trị N | 100, 200 |
| Các giá trị D | 1, 2, 3, 4, 6, 10 |
| Khoảng seed | 2026 đến 2125 |

| Thuộc tính | Giá trị |
|---|---|
| Thành công | 2,560 |
| Thất bại | 0 |
| R toàn bộ | 1 |
| Trung vị tick, các thành công | 189 |
| P90 tick, các thành công | 203 |
| Trung vị quãng đường, các thành công | 295.197 |
| Nhãn thất bại | không có |

Quy tắc chọn dòng đại diện: sắp xếp từ điển theo `method`, `initial_layout`, `n_sheep`, `n_shepherds`, `seed`, sau đó lấy 5 vị trí cách đều, gồm hai đầu. Quy tắc này trung lập và không chọn theo kết quả.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | compact | 100 | 1 | 2026 | True | 205 | 163.226 | none |
| strombom_multi | compact | 100 | 2 | 2086 | True | 195 | 300.579 | none |
| strombom_multi | compact | 200 | 1 | 2026 | True | 191 | 147.115 | none |
| strombom_multi | compact | 200 | 2 | 2085 | True | 183 | 270.683 | none |
| strombom_multi | compact | 200 | 10 | 2055 | True | 182 | 1,341.797 | none |

## Hợp nhất claim: Giai đoạn 5 communication

Nguồn đầy đủ: [`phase5/comm_claim/merged_trials.csv`](../../phase5/comm_claim/merged_trials.csv). Bảng lớn không được chép lại. Các thống kê dưới đây được tính trực tiếp từ CSV.

| Thuộc tính | Giá trị |
|---|---|
| Số dòng | 1,920 |
| Số cột | 78 |
| Số ô thiết kế | 12 |
| Phương pháp | strombom_multi |
| Bố cục | compact |
| Các giá trị N | 100, 200 |
| Các giá trị D | 1, 2, 3, 4, 6, 10 |
| Khoảng seed | 2026 đến 2125 |

| Thuộc tính | Giá trị |
|---|---|
| Thành công | 1,860 |
| Thất bại | 60 |
| R toàn bộ | 0.969 |
| Trung vị tick, các thành công | 186 |
| P90 tick, các thành công | 204 |
| Trung vị quãng đường, các thành công | 277.558 |
| Nhãn thất bại | oscillation: 60 |

Quy tắc chọn dòng đại diện: sắp xếp từ điển theo `method`, `initial_layout`, `n_sheep`, `n_shepherds`, `seed`, sau đó lấy 5 vị trí cách đều, gồm hai đầu. Quy tắc này trung lập và không chọn theo kết quả.

| method | layout | N | D | seed | success | ticks | path | failure_mode |
|---|---|---|---|---|---|---|---|---|
| strombom_multi | compact | 100 | 1 | 2026 | True | 205 | 163.226 | none |
| strombom_multi | compact | 100 | 2 | 2086 | True | 189 | 286.598 | none |
| strombom_multi | compact | 200 | 1 | 2026 | True | 191 | 147.115 | none |
| strombom_multi | compact | 200 | 2 | 2085 | True | 183 | 270.683 | none |
| strombom_multi | compact | 200 | 10 | 2055 | False | 10000 | 10,643.92 | oscillation |

## Nguồn trực tiếp

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
