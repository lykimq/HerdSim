# Một đàn cừu cần bao nhiêu chó?

## 1. Phạm vi và tình trạng

Báo cáo này chỉ gồm kết quả thực nghiệm của các Giai đoạn **1**, **2**, và **4** đã hoàn tất trong `scaling_v2`.

![Các giai đoạn có trong báo cáo này.](figures/schematics/vi/phase_roadmap.svg)

*Các giai đoạn có số liệu cấp claim ở đây: 1, 2 và 4. Sơ đồ thiết lập và phương pháp nằm trong các tài liệu liên kết bên dưới.*

![Năm kết quả chính từ Giai đoạn 1, 2 và 4.](figures/schematics/vi/summary_at_a_glance.svg)

| Câu hỏi | Bằng chứng đã hoàn tất |
|---|---|
| Đàn lớn hơn thì cần bao nhiêu chó? | Giai đoạn 1, cơ sở `strombom_multi` trên xuất phát `compact` |
| Cấu trúc xuất phát có đổi câu trả lời không? | Giai đoạn 2, cơ sở trên bốn bố cục |
| Kết quả có chuyển sang luật chó khác không? | Giai đoạn 4, bản đồ kích thước và cấu trúc của `kubo` và `fat` |

| Đánh giá | Phát hiện | Số chính |
|---|---|---|
| D_min = 1 | Trên luật cơ sở với xuất phát compact, đàn từ 25 đến 400 cừu thành công tin cậy với một chó. | Đàn 5 và 10 cừu cần 2 chó. Tại một chó, R là 0.07 và 0.24. |
| Lãng phí | Khi xuất phát compact đã chạy được, thêm chó không giúp xong nhanh hơn; chó chỉ đi nhiều hơn. | Thời gian xong điển hình khoảng 183 tick; đường mỗi chó khoảng 148 với N >= 25. Trong 100 ô kích thước nhân số chó, 88 ô lãng phí. |
| Không tái hiện | Đường tăng mạnh về số chó cần trong bản thảo 2025 không xuất hiện ở đây. | Bản thảo báo khoảng 20 đến 35 chó với N >= 200. Ở đây một chó xong N = 400 trong trung vị 168 tick. |
| Chỉ đổi chi phí | Bố cục xuất phát trên cơ sở đổi thời gian và đường đi, nhưng không đổi D_min. | Xuất phát wide tốn khoảng 11x đến 20x thời gian và 19x đến 36x đường so với compact. Tại N = 200, `outlier_rich` đạt khoảng 6x thời gian và 11x đường. |
| Chuyển giao một phần | Kubo và FAT không chuyển đều từ cơ sở. | Kubo gần khớp cơ sở trên compact nhưng chỉ đạt R = 0.47 đến 0.54 trên wide. FAT chỉ đạt R >= 0.90 với N <= 10. |

| Giai đoạn | Câu hỏi | Phương pháp | Bố cục | Thử nhanh | Khảo sát | Kết luận |
|---|---|---|---|---:|---:|---:|
| 1 | Bản đồ kích thước | strombom_multi | compact | 150 | 3,000 | 2,200 |
| 2 | Cấu trúc | strombom_multi | 4 bố cục | 600 | 3,600 | 2,400 |
| 4a | Chuyển giao: kích thước | kubo | compact | không có | 3,000 | 2,100 |
| 4a | Chuyển giao: kích thước | fat | compact | không có | 3,000 | 2,000 |
| 4b | Chuyển giao: cấu trúc | kubo | 4 bố cục | không có | 3,600 | 4,000 |
| 4b | Chuyển giao: cấu trúc | fat | 4 bố cục | không có | 3,600 | 2,400 |
|  | **Tổng mô phỏng** |  |  |  |  | **35,650** |

Bản hợp nhất claim có 30,670 dòng. Các tầng thử nhanh, khảo sát và claim đã chạy có 35,650 dòng; ô được gieo lại bỏ dòng khảo sát khỏi bản hợp nhất claim. Claim cấu trúc Kubo có 4,000 dòng, gồm 200 seed tại `outlier_rich`, N = 200 với D trong {1, 2, 3, 4, 6, 10, 15, 20, 25}. Xem [nhật ký chạy](data/run_ledger_vi.md).

Tài liệu chuẩn:

- [Kế hoạch nghiên cứu](../../docs/main_scaling_plan_vi.md)
- [Thiết lập và tham chiếu tham số](../../docs/setup/README_vi.md)
- [Hướng dẫn phương pháp](../../docs/methods/README_vi.md)
- [Độ tin cậy và đối chiếu bản thảo](../../docs/credibility/README_vi.md)
- [Phụ lục dữ liệu tạo tự động](data/README_vi.md)

## 2. Giai đoạn 1: kích thước đàn

Bằng chứng: `../phase1/claim/README.md`, `../phase1/claim/packages/a/`, và `../phase1/claim/packages/f/`.

![Hình 1. Mặt tỉ lệ thành công của ba bộ điều khiển trên xuất phát compact.](figures/f1_reliability_heatmaps.png)

*Hình 1. Giai đoạn 1 là bảng trái; Kubo và FAT thuộc Giai đoạn 4. Nguồn: `../phase1/claim/packages/a/reliability.csv` và `../phase4/{kubo,fat}_size/claim/packages/a/reliability.csv`.*

| Kích thước đàn N | D_min | D_max | D_overcrowd | Ý nghĩa |
|---|---|---|---|---|
| 5, 10 | 2 | 35 (trần lưới) | không | Một chó không đủ tin cậy; D = 2 đến D = 35 vẫn tin cậy |
| 25 đến 400 | 1 | 35 (trần lưới) | không | Một chó đạt R >= 0.90; vẫn trên ngưỡng đến D = 35 |

Khoảng bootstrap của mọi D_min cơ sở có độ rộng 0. Nguồn: `../phase1/claim/packages/a/frontier.csv`.

| Sự kiện D_max | Cách đọc |
|---|---|
| D_max = 35 với mọi N | Không quan sát thấy overcrowding trên cơ sở |
| Vì sao là 35? | Đây là giá trị lớn nhất đã thử trong {1, 2, 3, 4, 6, 10, 15, 20, 25, 35} |
| 35 không phải gì | Không phải điểm sụp đã đo hay giới hạn trên chung |
| Thất bại cứng? | Không có ô thất bại cứng trong Giai đoạn 1 cơ sở |

Tỉ lệ thành công tổng trên merge Giai đoạn 1 là 0.963, với 169 thất bại trong 4,540 dòng. Thất bại tập trung tại một chó trên hai đàn nhỏ nhất.

| Ô | R tại D = 1 | R tại D = 2 | Nhãn thất bại chính |
|---|---:|---:|---|
| N = 5 | 0.07 | 1.00 | dao động: 93 |
| N = 10 | 0.24 | 1.00 | kẹt: 58, dao động: 18 |

| Chế độ | Số ô | Cách đọc |
|---|---:|---|
| Lãng phí quá mức | 88 | Đã tin cậy; thêm chó chỉ tăng đường |
| Hiệu quả | 10 | Gần D hữu ích |
| Thiếu nguồn lực | 2 | N = 5 và N = 10 tại D = 1 |

![Hình 2. Chi phí theo D.](figures/f3_cost_vs_d.png)

*Hình 2. Thời gian xong phẳng trong khi tổng đường tỉ lệ với D. Nguồn: `../phase1/claim/merged_trials.csv`.*

Thời gian xong trung vị là 183 tick (p90 = 198). Nếu chỉ tính lượt thành công, trung vị là 182 và p90 là 195. Với N >= 25, đường trung vị mỗi chó khoảng 148 đơn vị thế giới.

![Hình 3. D_min theo N, có bản thảo 2025 để đối chiếu.](figures/f2_dmin_vs_n.png)

*Hình 3. Nguồn: `../phase1/claim/packages/a/frontier.csv`, `../phase4/*/size/claim/packages/a/frontier.csv`, và Bảng A3 của bản thảo.*

| N | Strombom | Kubo | FAT | Bản thảo 2025 |
|---:|---:|---:|---:|---:|
| 5 | 2 | 3 | 1 | 1 |
| 10 | 2 | 1 | 1 | 1 |
| 25 | 1 | 1 | không <= 35 | 1 |
| 50 | 1 | 1 | không <= 35 | 1 |
| 75 | 1 | 1 | không <= 35 | không có |
| 100 | 1 | 1 | không <= 35 | 1 |
| 150 | 1 | 1 | không <= 35 | 3 |
| 200 | 1 | 1 | không <= 35 | 20 |
| 300 | 1 | 1 | không <= 35 | 20 |
| 400 | 1 | 1 | không <= 35 | 35 |

*D_min tại theta = 0.90 trên xuất phát compact. Kubo tại N = 5 có bootstrap [1, 3]; R là 0.77 tại D = 1, 0.71 tại D = 2, và 0.97 tại D = 6. Nguồn: các tệp frontier và `dmin_bootstrap.csv` nêu trên.*

D_min cơ sở quan sát chỉ có hai mức: 2 với N trong {5, 10}, và 1 với N >= 25.

| Mô hình | RMSE leave-one-N-out | Cách đọc |
|---|---:|---|
| Hằng | 0.44 | Một D_min phẳng |
| Tuyến tính | 0.44 | Đường thẳng theo N |
| Lũy thừa | 0.25 | Đường cong log-log mượt |
| Từng mảnh | 0.13 | Hai mức, điểm gãy tại N = 10 |

![Hình 4. RMSE leave-one-N-out theo mô hình.](figures/f8_scaling_rmse_vi.svg)

*Hình 4. Fit từng mảnh hưởng lợi vì mã hóa bước nhảy quan sát. Nguồn: `../phase1/claim/packages/f/scaling_cv.csv`. Không thể kiểm C6b vì không có dải tăng trưởng để fit.*

## 3. Giai đoạn 2: cấu trúc xuất phát

Bằng chứng: `../phase2/claim/README.md` và `../phase2/claim/packages/b/`.

![Bốn bố cục xuất phát.](figures/schematics/vi/four_layouts.svg)

*Đối chiếu cấu trúc giữ N cố định và chỉ đổi hình xuất phát.*

D_min = 1 cho cả 12 ô bố cục nhân N, và mọi khoảng bootstrap có độ rộng 0. Tại D = 1, mọi ô có R = 1.00. D_max = 35 là trần lưới trong mọi ô, không có D_overcrowd.

![Hình 5. Tổng đường trung vị tại D = 1 theo bố cục.](figures/f4_layout_cost.png)

*Hình 5. Nguồn: `../phase2/claim/merged_trials.csv` tại D = 1.*

| Bố cục | N | R tại D = 1 | Tick trung vị | so với compact | Đường trung vị | so với compact |
|---|---:|---:|---:|---:|---:|---:|
| compact | 50 | 1.00 | 195 | 1.0x | 157 | 1.0x |
| compact | 100 | 1.00 | 204 | 1.0x | 161 | 1.0x |
| compact | 200 | 1.00 | 191 | 1.0x | 144 | 1.0x |
| split | 50 | 1.00 | 195 | 1.0x | 158 | 1.0x |
| split | 100 | 1.00 | 205 | 1.0x | 162 | 1.0x |
| split | 200 | 1.00 | 193 | 1.0x | 144 | 1.0x |
| outlier_rich | 50 | 1.00 | 224 | 1.1x | 209 | 1.3x |
| outlier_rich | 100 | 1.00 | 501 | 2.5x | 554 | 3.4x |
| outlier_rich | 200 | 1.00 | 1,228 | 6.4x | 1,647 | 11.4x |
| wide | 50 | 1.00 | 2,138 | 11.0x | 2,925 | 18.6x |
| wide | 100 | 1.00 | 3,074 | 15.1x | 4,319 | 26.8x |
| wide | 200 | 1.00 | 3,870 | 20.3x | 5,213 | 36.2x |

| Bố cục | Cách đọc thực nghiệm |
|---|---|
| wide | 11x đến 20x tick và 19x đến 36x đường so với compact |
| outlier_rich | Tại N = 200, 6.4x tick và 11.4x đường so với compact |
| split | Trung vị khớp compact; fragmentation trung bình khoảng 0.99, nên coi là kiểm tra thay vì phát hiện |
| compact | Mốc tham chiếu |

Với xuất phát wide, B* = 2 tại N = 50, 100, và 200. Tổng đường trung vị giảm từ 2,925 xuống 2,337, từ 4,319 xuống 3,003, và từ 5,213 xuống 3,694. Nguồn: `../phase2/claim/packages/b/frontier_by_layout.csv`.

![Hình 6. Xuất phát wide: đường trung vị tại D = 1 so với D = 2.](figures/f10_wide_bstar_path_vi.png)

*Hình 6. Nguồn: `../phase2/claim/merged_trials.csv`, bố cục wide.*

## 4. Giai đoạn 4: chuyển giao bộ điều khiển

Bằng chứng: `../phase4/README.md`, `../phase4/kubo_structure/claim/README.md`, `../phase4/package_d/`, và `../phase4/kubo_structure/claim/outlier_rich_n200_window.json`.

![Ý tưởng chuyển giao giữa các phương pháp.](figures/schematics/vi/transfer_sketch.svg)

*Cùng lưới và bố cục; gắn nhãn từng đặc trưng biên là chia sẻ, dịch, hoặc vắng.*

### Bản đồ kích thước compact

Kubo có D_min = 3 tại N = 5 và D_min = 1 từ N = 10 đến 400. D_max = 35 là trần lưới cho mọi ô kích thước, không có overcrowding. Tỉ lệ thành công tổng là 0.991, và mọi thất bại đều là timeout.

FAT có D_min = 1 tại N trong {5, 10}; hai ô đều có D_max = 35 như trần lưới. Với N >= 25, không D <= 35 nào đạt R >= 0.90, nên D_min và D_max không xác định. Với N = 50 đến 400, R tốt nhất theo N là 0.40 đến 0.53, còn R của từng ô xuống tới khoảng 0.17. Khoảng một nửa lượt FAT kích thước thất bại: 39% do dao động và 7% do kẹt.

| Trường hợp | Trường biên | Cách đọc thực nghiệm |
|---|---|---|
| D_max = 35, không D_overcrowd | Có D_min | Tin cậy tại trần lưới; chưa đo được điểm sụp trên |
| Thất bại cứng | D_min và D_max trống | Không D đã thử nào đạt theta |
| Overcrowding thật | Có D_overcrowd và D_max dưới 35 | Không quan sát thấy trong các giai đoạn đã hoàn tất |

Nhãn Package D kích thước gồm 8 chia sẻ, 7 dịch, và 29 vắng. Số vắng chủ yếu đến từ các dòng quá tải vì không bộ điều khiển nào quá tải trên compact. Nguồn: `../phase4/package_d/size/transfer_summary.csv`.

![Hình 7. Cách các lượt kết thúc trên bản đồ kích thước.](figures/f6_failure_modes_vi.png)

*Hình 7. Nguồn: `failure_mode` trong `merged_trials.csv` claim của Giai đoạn 1, Kubo kích thước, và FAT kích thước.*

### Bản đồ cấu trúc

| Bố cục | N | Strombom | Kubo | FAT |
|---|---:|---:|---:|---:|
| compact | 50 | 1 | 1 | không (R tốt nhất = 0.47) |
| compact | 100 | 1 | 1 | không (R tốt nhất = 0.40) |
| compact | 200 | 1 | 1 | không (R tốt nhất = 0.47) |
| split | 50 | 1 | 1 | không (R tốt nhất = 0.50) |
| split | 100 | 1 | 1 | không (R tốt nhất = 0.47) |
| split | 200 | 1 | 1 | không (R tốt nhất = 0.40) |
| outlier_rich | 50 | 1 | 1 | không (R tốt nhất = 0.10) |
| outlier_rich | 100 | 1 | 1 | không (R tốt nhất = 0.00) |
| outlier_rich | 200 | 1 | 20 | không (R tốt nhất = 0.00) |
| wide | 50 | 1 | không (R tốt nhất = 0.49) | không (R tốt nhất = 0.00) |
| wide | 100 | 1 | không (R tốt nhất = 0.54) | không (R tốt nhất = 0.00) |
| wide | 200 | 1 | không (R tốt nhất = 0.47) | không (R tốt nhất = 0.00) |

*D_min theo bố cục và bộ điều khiển. `không` nghĩa là không D <= 35 nào đạt R = 0.90. Nguồn: `../phase4/package_d/structure/frontier_by_method_layout.csv`.*

![Hình 8. R theo D tại N = 200 theo bố cục.](figures/f5_layout_reliability_curves_vi.png)

*Hình 8. Nguồn: các tệp `merged_trials.csv` claim cấu trúc.*

| D | Số seed | R | R >= 0.90? |
|---:|---:|---:|:---:|
| 1 | 200 | 0.745 | không |
| 2 | 200 | 0.855 | không |
| 3 | 200 | 0.835 | không |
| 4 | 200 | 0.860 | không |
| 6 | 200 | 0.890 | không |
| 10 | 200 | 0.875 | không |
| 15 | 200 | 0.855 | không |
| 20 | 200 | 0.935 | có |
| 25 | 200 | 0.910 | có |
| 35 | 30 | 0.967 | có |

| Kubo `outlier_rich`, N = 200 | Giá trị |
|---|---|
| D_min | 20 |
| Khoảng bootstrap | [2, 20] từ `merged_dmin_bootstrap.csv`, `n_seeds_ref = 200` |
| Overcrowding | không |
| Bất định | Vài D < 20 nằm gần 0.90, nên bootstrap có thể đặt D_min dưới 20 |

![Hình 9. Kubo outlier_rich N = 200 với khoảng Wilson 95%.](figures/f9_kubo_outlier_rich_n200_vi.png)

*Hình 9. Nguồn: `../phase4/kubo_structure/claim/merged_trials.csv`, `merged_dmin_bootstrap.csv`, và `outlier_rich_n200_window.json`.*

| Phát hiện | Cách đọc thực nghiệm |
|---|---|
| Kubo + wide | R tốt nhất là 0.47 đến 0.54; thất bại là timeout hoặc scatter; thêm chó nâng R về khoảng 0.5 nhưng không tới 0.90 |
| Kubo + outlier_rich, N = 200 | Dịch sang D_min = 20, bootstrap [2, 20] |
| Cấu trúc FAT | Không bố cục nào tại N >= 50 đạt R = 0.90 |

| Bộ điều khiển | I_dir trung bình tại D = 35, N = 100 | I_dir trung bình trên mọi D tại N = 100 |
|---|---:|---:|
| Cơ sở (`strombom_multi`) | khoảng 0.09 | khoảng 0.05 |
| Kubo | khoảng 0.15 | khoảng 0.10 |
| FAT | khoảng 0.48 | khoảng 0.40 |

| Kiểm tra liên hệ | Giá trị | Cách đọc |
|---|---:|---|
| Pearson r(I_dir, success), merge FAT kích thước | khoảng -0.87 | Liên hệ âm mạnh |
| Kết luận nhân quả | không | Liên hệ quan sát, không phải thí nghiệm cơ chế có kiểm soát |

![Hình 10. Chỉ số nhiễu hướng theo D.](figures/f7_interference_vi.png)

*Hình 10. Nguồn: `mean_i_dir` trong các tệp `merged_trials.csv` claim.*

## 5. Tổng hợp và ảnh chụp claim

![Bảng điểm claim từ tracker và các gói claim.](figures/schematics/vi/claims_scorecard.svg)

*Màu phán quyết khớp bảng dưới. Phán quyết sống: `../../docs/progress_tracker.md`.*

| Claim | Phán quyết | Bằng chứng | Cách đọc |
|---|---|---|---|
| C1a | BỊ BÁC BỎ | Giai đoạn 2 Package B: D_min = 1 cho bốn bố cục tại N = 50, 100, 200; bootstrap rộng 0 | Chỉ cho cơ sở; cấu trúc Kubo có dịch |
| C1b | KHÔNG RÕ | Không có dịch D_min trên cơ sở; Package B báo likelihood NaN | Chi phí vẫn phụ thuộc mạnh vào bố cục |
| C2a | BỊ BÁC BỎ | Giai đoạn 1 Package A: 0 ô overcrowding tại theta = 0.90 | Giai đoạn 4 cũng không có |
| C2b | BỎ QUA | Không có ô overcrowding để chạy T = 20,000 | Không chạy T1 |
| C3 | KHÔNG RÕ | Đối chiếu cơ chế cơ sở cần overcrowding | Có ô đối chiếu Kubo nhưng Package C chưa hoàn tất |
| C4 | ĐƯỢC ỦNG HỘ, một phần | Strombom và Kubo chia sẻ D_min compact với N >= 25; FAT vắng; Kubo wide vắng; Kubo `outlier_rich`, N = 200 dịch | Chuyển giao phụ thuộc điều kiện |
| C6a | ĐÃ ĐÁNH GIÁ, yếu | RMSE từng mảnh 0.13 so với lũy thừa 0.25 | Fit chỉ dùng hai mức quan sát {2, 1}; không phải quy luật scaling |
| C5a/b, C6b, C7a/b | CHƯA ĐÁNH GIÁ | Giai đoạn 5 và 7 chưa chạy; C6b không có dải tăng trưởng đã nêu | Không có kết luận kết quả |

## 6. Bất định, giới hạn, và giai đoạn chưa chạy

| Tình trạng | Chủ đề | Giới hạn hiện tại |
|---|---|---|
| Hiệu ứng trần | Độ tin cậy cơ sở | R = 1.00 tại D = 1 trên gần mọi ô cơ sở, nên khó thấy scaling |
| Trần lưới | D_max = 35 | Chưa đo điểm sụp trên; hành vi trên 35 chưa biết |
| Thất bại cứng | FAT và Kubo wide | D_min và D_max trống nghĩa là không D đã thử nào đạt 0.90, không phải đã tìm thấy biên trên |
| Khoảng rộng | Kubo `outlier_rich`, N = 200 | Ước điểm D_min = 20 tại 200 seed, R = 0.935, nhưng bootstrap là [2, 20] |
| Fit yếu | C6a | Hai mức D_min quan sát không hỗ trợ quy luật scaling chung |
| Chỉ quan sát | I_dir | r khoảng -0.87 không chứng minh interference gây thất bại |
| Hành vi bộ sinh chưa xác minh | Bố cục `split` | Chi phí và D_min khớp compact; vẫn cần xác nhận tách cụm tại t = 0 |
| Một nhiệm vụ mô phỏng | Giá trị bên ngoài | Kết quả không chứng minh hiệu năng ngoài đồng, độ trung thực sinh học, hay quy tắc nông trại chung |
| Lưới D rời rạc | Độ phân giải | Không phân giải được khác biệt nhỏ hơn các bước số chó đã thử |

Giai đoạn chưa chạy:

- Giai đoạn 3 và C2b bị bỏ qua vì cơ sở có 0 ô overcrowding.
- Giai đoạn 5 về cảm biến, tầm, và giao tiếp chưa chạy.
- Giai đoạn 7 và Package G về cảnh báo sớm chưa chạy.
- Bản thảo 2025 không được chạy lại, và parity định lượng với NetLogo chưa được xác lập.

Nội dung thiết lập, phương pháp, bản thảo, NetLogo, provenance, và thuật ngữ đã bỏ khỏi báo cáo này nằm trong các tài liệu chuẩn liên kết ở mục 1. Các bảng thực nghiệm tạo tự động và đường dẫn nguồn nằm trong [data/README_vi.md](data/README_vi.md).
