# Một đàn cừu cần bao nhiêu người chăn?

HerdSim scaling_v2: tổng hợp Phase 1 (kích thước), Phase 2 (cấu trúc) và Phase 4 (chuyển giao).
Bản HTML có nhúng sẵn hình: `SUMMARY_REPORT_vi.html`. Bản tiếng Anh: `SUMMARY_REPORT.md`.

## Tóm tắt

Câu hỏi: một đàn cần bao nhiêu người chăn khi đàn lớn lên, và câu trả lời có phụ thuộc vào bộ điều khiển và cách đàn xuất phát không. Báo cáo này gồm ba phase đã xong ở mức claim: **Phase 1** (bản đồ kích thước, baseline), **Phase 2** (cấu trúc xuất phát, baseline) và **Phase 4** (chuyển giao sang Kubo và FAT).

- **Với task này, baseline chỉ cần một chó chăn từ N = 25 đến N = 400.** Chỉ N = 5 và 10 cần hai chó, vì một chó dao động (oscillation) trên đàn rất nhỏ (tỉ lệ thành công 7% và 24% tại D = 1).
- **Thêm chó không giúp gì mà tốn nhiều.** Thời gian hoàn thành trung vị giữ quanh 183 ticks với mọi D; tổng quãng đường tăng khoảng 146 đơn vị cho mỗi chó thêm. 88 trong 100 ô (N, D) được gán nhãn wasteful overspend.
- **Đường D_min(N) dốc và hiện tượng overcrowding của bản draft 2025 không được tái hiện.** Draft cần 20 đến 35 chó khi N >= 200. Ở đây một chó hoàn thành N = 400 với trung vị 168 ticks. Hai task khác nhau (collect + giữ 800 ticks + thoát qua cổng, so với lùa 120 đơn vị vào vùng đích), nên đây là nhận định về task, không phải bác bỏ draft (mục 6).
- **Cấu trúc xuất phát đổi chi phí, không đổi D_min (baseline).** Xuất phát wide cần nhiều ticks gấp 11 đến 20 lần và quãng đường gấp 19 đến 36 lần so với compact với cùng một chó; outlier_rich tăng theo N (đến 6x ticks, 11x path tại N = 200).
- **Các bộ điều khiển khác nhau rõ rệt.** Kubo giống baseline ở xuất phát compact nhưng thất bại ở wide (R <= 0.54 với mọi D) và ở mức giáp ranh với outlier_rich tại N = 200. FAT chỉ đạt R >= 0.90 khi N <= 10.
- **Lưu ý cho mọi kết quả tích cực:** hiệu ứng trần (ceiling). R = 1.00 tại D = 1 không còn gì để đo, nên benchmark chưa cho thấy độ khó tập thể scale thế nào. Mục 8 nêu cách làm cho nó có ích hơn.

## 1. Vì sao chạy và liên hệ với draft 2025

Draft 2025 (`docs/papers/sheep-scaling_paper2025.pdf`) quét số chó D và kích thước đàn N trong mô hình NetLogo, và báo cáo một dải D đáng tin cậy cho mỗi N. Kết quả: một chó xử lý được đến khoảng 100 cừu, đàn lớn hơn cần nhiều chó hơn hẳn với lợi ích giảm dần, và quá nhiều chó có thể gây hại. Draft không có độ bất định cho D_min và dùng cố định 100 seed mỗi ô.

HerdSim (`scaling_v2`, [main_scaling_plan.md](../../docs/main_scaling_plan.md)) hỏi lại câu này với giao thức đã đóng băng: cùng lưới D, khoảng bootstrap cho D_min, một lượt scout rẻ rồi reseed 100 seed gần biên (claim), thêm yếu tố cấu trúc (layout xuất phát) và phép thử chuyển giao giữa các bộ điều khiển. Các câu hỏi nghiên cứu: RQ1 cấu trúc, RQ2 kích thước, RQ3 cơ chế, RQ4 chuyển giao, RQ5 thông tin, RQ6 fit, RQ7 cảnh báo sớm. Phase 1, 2, 4 ứng với RQ2, RQ1, RQ4.

|  | Draft 2025 | HerdSim `scaling_v2` |
|---|---|---|
| Task | Collect, giữ 800 ticks, thoát qua cổng | `drive_to_goal`: mọi con cừu nằm trong vùng đích |
| Sân | 101 x 71 patch, chuồng ở giữa | 500 x 500, đích tại (370, 250), bán kính 15 * sqrt(N / 50) |
| Giới hạn thời gian | 10,000 ticks | T0 = 10,000 (T1 = 20,000 cho ô overcrowding) |
| Lưới | 11 N x 10 D, mỗi ô 100 seed | 10 N x 10 D; 30 seed, rồi 100 ở vùng biên |
| Độ bất định D_min | không có | bootstrap theo seed (1,000 lần lấy mẫu) |
| Yếu tố ngoài N và D | không có | layout X0, bộ điều khiển, thông tin (phase sau) |

*Bảng 1. Draft so với giao thức hiện tại.*

## 2. Các thí nghiệm được chạy như thế nào

Mỗi giao thức đi qua ba mức. **Pilot** (smoke): vài ô để kiểm tra code chạy. **Scout**: 30 seed trên mọi ô (N, D). **Claim**: với mỗi (method, layout, N), các ô quyết định D_min (D_min của scout và các D lân cận, cùng cửa sổ overcrowding nếu có) được chạy lại với 100 seed mới. Phân tích claim dùng 100 seed ở các ô đó và 30 seed ở nơi khác. Một trial thành công khi mọi con cừu nằm trong vùng đích trước giới hạn thời gian.

| Phase | Câu hỏi | Method | Layout | Pilot | Scout | Claim |
|---|---|---|---|---|---|---|
| 1 | Size map | strombom_multi | compact | 150 | 3,000 | 2,200 |
| 2 | Structure | strombom_multi | 4 layouts | 600 | 3,600 | 2,400 |
| 4a | Transfer: size | kubo | compact | - | 3,000 | 2,100 |
| 4a | Transfer: size | fat | compact | - | 3,000 | 2,000 |
| 4b | Transfer: structure | kubo | 4 layouts | - | 3,600 | 2,800 |
| 4b | Transfer: structure | fat | 4 layouts | - | 3,600 | 2,400 |
|  | **Total simulations** |  |  |  |  | **34,450** |

*Bảng 2. Số trial theo từng giai đoạn (số dòng `trials.csv`; file merged lớn hơn một chút).*

Cách đọc heatmap: hàng là kích thước đàn, cột là số chó, mỗi ô là phần trăm seed thành công. D_min là cột đầu tiên trong hàng đạt 90%.

## 3. Phase 1: đàn kích thước N cần bao nhiêu chó?

Mục tiêu: lập bản đồ tỉ lệ thành công R(N, D) cho bộ điều khiển baseline `strombom_multi` với xuất phát compact, từ đó suy ra D_min, D_overcrowd, D_max và D rẻ nhất mà vẫn đáng tin.

![Hình 1. Bề mặt tỉ lệ thành công của ba bộ điều khiển với xuất phát compact. Phase 1 là bảng bên trái; hai bảng kia thuộc Phase 4 (mục 5).](figures/f1_reliability_heatmaps.png)

*Hình 1. Bề mặt tỉ lệ thành công của ba bộ điều khiển với xuất phát compact. Phase 1 là bảng bên trái; hai bảng kia thuộc Phase 4 (mục 5).*

### Kết quả (baseline)

- **D_min = 1 với N >= 25, D_min = 2 với N = 5 và 10.** Khoảng bootstrap của D_min có độ rộng 0 với mọi N.
- **Không có overcrowding.** R luôn >= 0.90 đến D = 35 với mọi N, nên D_overcrowd không xác định và D_max là trần của lưới.
- **Thất bại hiếm và chỉ ở D = 1 trên đàn nhỏ.** Tỉ lệ thành công chung 96%; trong 169 thất bại, 93 là oscillation tại N = 5, và 18 oscillation cộng 58 stuck tại N = 10. Các ô này có R = 0.07 và 0.24 tại D = 1, và 1.00 tại D = 2.
- **Nhãn regime trên 100 ô (N, D):** 88 wasteful overspend, 10 efficient operation, 2 under-resourced failure.

![Hình 2. Chi phí theo D (log-log). Thời gian hoàn thành phẳng: task là lùa 120 đơn vị với tốc độ 1, nên khoảng 120 ticks là không tránh được và thêm chó không rút ngắn được. Quãng đường tỉ lệ với D.](figures/f3_cost_vs_d.png)

*Hình 2. Chi phí theo D (log-log). Thời gian hoàn thành phẳng: task là lùa 120 đơn vị với tốc độ 1, nên khoảng 120 ticks là không tránh được và thêm chó không rút ngắn được. Quãng đường tỉ lệ với D.*

### Vì sao

Thời gian phẳng vì collect và drive đã nhanh với một chó (trung vị 183 ticks, p90 198, so với ngân sách 10,000 ticks). Path tăng theo D vì mỗi chó đi suốt cả trial: khoảng 146 đơn vị mỗi chó với N >= 25. Vì thế gần như mọi ô đều wasteful: chỉ con chó đầu tiên làm việc có ích.

Vì sao N = 5 và 10 cần hai chó thì chưa được kiểm tra ở đây. Một cách giải thích hợp lý, phù hợp với dữ liệu nhưng chưa được chứng minh, là một chó trên đàn vài con cừu cứ luân phiên giữa collect và drive mà không ổn định (nhãn lỗi chính là `oscillation`). Chó thứ hai loại bỏ sự luân phiên đó.

![Hình 3. D_min theo N. Đường xám là draft 2025 (Bảng A3). Draft cần nhiều chó từ N = 150 trở lên; baseline HerdSim giữ ở một. FAT không có D_min với N >= 25.](figures/f2_dmin_vs_n.png)

*Hình 3. D_min theo N. Đường xám là draft 2025 (Bảng A3). Draft cần nhiều chó từ N = 150 trở lên; baseline HerdSim giữ ở một. FAT không có D_min với N >= 25.*

| N | Strombom | Kubo | FAT | Draft 2025 |
|---|---|---|---|---|
| 5 | 2 | 3 | 1 | 1 |
| 10 | 2 | 1 | 1 | 1 |
| 25 | 1 | 1 | none <= 35 | 1 |
| 50 | 1 | 1 | none <= 35 | 1 |
| 75 | 1 | 1 | none <= 35 | n/a |
| 100 | 1 | 1 | none <= 35 | 1 |
| 150 | 1 | 1 | none <= 35 | 3 |
| 200 | 1 | 1 | none <= 35 | 20 |
| 300 | 1 | 1 | none <= 35 | 20 |
| 400 | 1 | 1 | none <= 35 | 35 |

*Bảng 3. D_min tại theta = 0.90 theo kích thước đàn (xuất phát compact). Giá trị draft lấy từ Bảng A3 của nó.*

### Fit scaling (Package F)

RMSE leave-one-N-out của D_min là 0.44 cho hằng số, 0.44 tuyến tính, 0.25 power law và 0.13 piecewise. Cần đọc kỹ: D_min chỉ nhận hai giá trị 2 (N <= 10) và 1 (N >= 25), nên mô hình piecewise khớp hoàn hảo theo cấu tạo (điểm gãy tại N = 10). Nó không chứng tỏ một quy luật scaling, và không thể kiểm tra claim C6b (độ dốc log-log dưới 1 trong một dải N) vì không có sự tăng trưởng nào để fit.

## 4. Phase 2: cấu trúc xuất phát có đổi câu trả lời không?

Mục tiêu: giữ N cố định ở 50, 100, 200 và chỉ đổi layout xuất phát. **compact**: đám Gaussian chặt. **wide**: Gaussian rộng gấp 6.7 lần, cừu cách xa nhau. **split**: ba cụm. **outlier_rich**: phần lõi cùng khoảng 20% cừu lạc nằm ngoài bán kính collect của bộ điều khiển. Phép thử là D_min có dịch ít nhất một bước lưới giữa các layout không (claim C1a).

**Kết quả về D_min: không.** D_min = 1 ở cả 12 ô (layout, N) và khoảng bootstrap có độ rộng 0. Mọi ô tại D = 1 đều đạt R = 1.00, nên D_min không thể giảm thêm và hiệu ứng cấu trúc lên D_min không đo được với bộ điều khiển và task này (hiệu ứng sàn).

**Kết quả về chi phí: có, rất lớn.** Thành công tại D = 1 là 100% ở mọi nơi, nhưng công sức để đạt được khác nhau một bậc độ lớn:

![Hình 4. Tổng quãng đường trung vị tại D = 1 theo layout. Tỉ lệ thành công ghi trên mỗi cột.](figures/f4_layout_cost.png)

*Hình 4. Tổng quãng đường trung vị tại D = 1 theo layout. Tỉ lệ thành công ghi trên mỗi cột.*

| Layout | N | R tại D=1 | Ticks trung vị | so với compact | Path trung vị | so với compact |
|---|---|---|---|---|---|---|
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

*Bảng 4. Chi phí của một chó ở baseline theo layout (100 seed mỗi ô).*

- **wide** tốn nhiều ticks gấp 11 đến 20 lần và path gấp 19 đến 36 lần so với compact. Khoảng cách tăng theo N (tỉ số path 19x, 27x, 36x), vì đàn phải được gom từ vùng rộng hơn.
- **outlier_rich** rẻ ở N = 50 (khoảng 1.1x ticks) và đắt ở N = 200 (6.4x ticks, 11x path): số cừu lạc tăng theo N, mỗi con cần một chuyến gom riêng.
- **split trông giống compact** (trung vị y hệt tại N = 50). Ba cụm được gom gần như ngay lập tức (độ phân mảnh trung bình trong trial là 0.98 cho cả hai). Hãy coi đây là điều cần kiểm tra lại, không phải một phát hiện: layout có thể không tạo ra bài toán đàn con khó cho bộ điều khiển này.
- **Nhiều chó có ích ở xuất phát wide.** D rẻ nhất mà vẫn đáng tin (B*) là 2, không phải 1, ở layout wide (path 2,337 tại N = 50 so với 2,925 tại D = 1). Đây là chỗ duy nhất trong dữ liệu baseline mà chó thứ hai đáng đồng tiền.

Diễn giải: cấu trúc xuất phát tác động qua công sức và thời gian từ rất lâu trước khi nó dịch biên độ tin cậy. Phân tích chỉ dựa trên biên sẽ bỏ sót. Chúng tôi khuyến nghị báo cáo path và ticks cạnh D_min mỗi khi thay đổi cấu trúc.

## 5. Phase 4: các kết quả có chuyển sang bộ điều khiển khác không?

Mục tiêu: lặp lại bản đồ kích thước và phép đối chiếu cấu trúc với **Kubo** và **FAT** (potential-field), rồi so với baseline. Một đặc trưng là **shared** nếu hai bộ điều khiển có cùng D_min, **shifted** nếu khác nhau, **absent** nếu một bên không có.

### Bản đồ kích thước

- **Kubo** có D_min = 1 với N từ 10 đến 400, giống baseline, và D_min = 3 tại N = 5 (thành công 77% tại D = 1, 71% tại D = 2, sau đó 100%). Tỉ lệ thành công chung 99%; mọi thất bại đều là timeout.
- **FAT** có D_min = 1 với N = 5 và 10 nhưng không bao giờ đạt 0.90 với N >= 25 ở mọi D đến 35: R là 0.6 đến 0.8 tại N = 25, 0.2 đến 0.5 ở trên đó. Thêm chó không giúp. Một nửa số trial FAT thất bại, chủ yếu do oscillation (39% số trial) và bị kẹt (7%).
- Bảng size của Package D: 8 mục D_min shared, 7 shifted, 29 absent. 29 mục absent phần lớn là mục overcrowding (không bộ điều khiển nào overcrowd ở xuất phát compact), nên con số này không đo mức bất đồng.

![Hình 5. Các trial kết thúc ra sao. FAT chiếm phần lớn thất bại; baseline hầu như không thất bại.](figures/f6_failure_modes.png)

*Hình 5. Các trial kết thúc ra sao. FAT chiếm phần lớn thất bại; baseline hầu như không thất bại.*

### Cấu trúc tại N = 50, 100, 200

| Layout | N | Strombom | Kubo | FAT |
|---|---|---|---|---|
| compact | 50 | 1 | 1 | none (best R=0.47) |
| compact | 100 | 1 | 1 | none (best R=0.40) |
| compact | 200 | 1 | 1 | none (best R=0.47) |
| split | 50 | 1 | 1 | none (best R=0.50) |
| split | 100 | 1 | 1 | none (best R=0.47) |
| split | 200 | 1 | 1 | none (best R=0.40) |
| outlier_rich | 50 | 1 | 1 | none (best R=0.10) |
| outlier_rich | 100 | 1 | 1 | none (best R=0.00) |
| outlier_rich | 200 | 1 | 4, overcrowd at 10 | none (best R=0.00) |
| wide | 50 | 1 | none (best R=0.49) | none (best R=0.00) |
| wide | 100 | 1 | none (best R=0.54) | none (best R=0.00) |
| wide | 200 | 1 | none (best R=0.47) | none (best R=0.00) |

*Bảng 5. D_min theo layout và bộ điều khiển. 'none' = không có D <= 35 nào đạt 0.90; R tốt nhất theo D trong ngoặc.*

![Hình 6. R theo D tại N = 200 cho từng layout (ở baseline cả bốn đường nằm trên R = 1.00 và chồng lên nhau). Xuất phát wide của Kubo chững quanh 0.4 đến 0.5 và đường outlier_rich dao động quanh mức 0.90; FAT không bao giờ tới gần.](figures/f5_layout_reliability_curves.png)

*Hình 6. R theo D tại N = 200 cho từng layout (ở baseline cả bốn đường nằm trên R = 1.00 và chồng lên nhau). Xuất phát wide của Kubo chững quanh 0.4 đến 0.5 và đường outlier_rich dao động quanh mức 0.90; FAT không bao giờ tới gần.*

- **Kubo ở xuất phát wide thất bại** với mọi N (R gộp khoảng 0.42 đến 0.48, D đơn lẻ tốt nhất 0.54). Thất bại là timeout và scatter: đàn không được gom trong 10,000 ticks. Thêm chó nâng R chậm (0.2 tại D = 1 lên khoảng 0.5), nhưng không đạt ngưỡng.
- **Kubo ở outlier_rich tại N = 200** có D_min = 4 và bị gán overcrowded tại D = 10. Đường cong (0.70, 0.84, 0.86, 0.93, 0.91, 0.85, 0.87, 0.93 ...) là một dải nhiễu quanh 0.90, không phải sụp đổ. Hãy coi đây là biên mềm: với 100 seed, khoảng 0.06 của R phủ toàn bộ dải.
- **FAT**: không layout nào đạt ngưỡng với N >= 50. wide và outlier_rich gần bằng 0; compact và split khoảng 0.3.
- **Giao thoa (interference).** I_dir trung bình bão hòa theo D (khoảng 0.09 baseline, 0.15 Kubo, 0.48 FAT tại N = 100). Nó bằng 0 tại D = 1 theo cấu tạo, nên liên hệ với thành công bị lẫn với D; giá trị Package D r(I_dir, success) = -0.87 của FAT có thể chủ yếu phản ánh việc FAT thất bại ở D lớn với I_dir cao, chưa phải cơ chế đã được kiểm tra.

![Hình 7. Chỉ số giao thoa theo D. Nó tăng từ 0 với một chó rồi đi ngang.](figures/f7_interference.png)

*Hình 7. Chỉ số giao thoa theo D. Nó tăng từ 0 với một chó rồi đi ngang.*

Diễn giải: kiến trúc bộ điều khiển quan trọng hơn số chó. Các bộ điều khiển phản ứng collect-and-drive (Strombom, Kubo) bị giới hạn bởi cách đàn xuất phát; bộ điều khiển potential-field bị giới hạn bởi động lực học của chính nó và không số chó nào cứu được nó trong task này.

## 6. So sánh với draft 2025

| Phát hiện của draft | HerdSim ở đây | Nhận xét |
|---|---|---|
| Một chó đủ đến N ~ 100, rồi sụp đổ (N = 150, D = 1: SR ~ 1%) | Một chó đủ đến N = 400 (R = 1.00 tại N = 150 và 400) | Không tái hiện. Task và sân khác nhau. |
| D_min tăng lên 20 đến 35 với N >= 200 | D_min = 1 | Không tái hiện. |
| Overcrowding (vd. N = 10, D >= 20 tệ hơn ít chó) | R = 1.00 tại D = 35 với N = 5 đến 400 (baseline) | Không tái hiện ở baseline; bằng chứng yếu ở Kubo outlier_rich. |
| Thời gian giảm theo D và tăng theo N; quãng đường bão hòa | Thời gian phẳng theo D và N; path tuyến tính theo D | Hình dạng khác: ở đây không có bão hòa. |
| Độ trải liên quan đến thất bại (rho = -0.70; S_bar * N: -0.83) | Chưa kiểm tra (Phase 3 cần ô overcrowding) | Các metric cohesion/spread đã được ghi và có thể phân tích trên trial hiện có. |
| Một sơ đồ duy nhất, không có độ bất định cho D_min | Khoảng bootstrap, ba bộ điều khiển, bốn layout | Mới: khoảng rộng 0; hiệu ứng cấu trúc và bộ điều khiển. |

*Bảng 6. Phát hiện nào của draft còn đúng ở đây.*

Vì sao kết quả khác: sự sụp đổ trong draft đến từ các pha **collect và hold**, nơi đàn phải được nén lại và giữ trong vòng chứa 800 ticks, và 90% thất bại của nó kẹt ở khâu collect. `drive_to_goal` bỏ hẳn hold và exit, dùng bán kính đích scale theo N, và đàn xuất phát ở tâm sân 500 đơn vị với quãng cần đi 120. Baseline xong trong khoảng 183 trên 10,000 ticks, nên ngân sách thời gian (thứ khiến cần thêm chó trong draft) không bao giờ là ràng buộc. Đây là cách đọc của tôi về giao thức; chưa được kiểm chứng bằng cách đổi task.

## 7. Bảng điểm claim

| Claim | Kết luận | Bằng chứng | Nhận xét |
|---|---|---|---|
| C1a | REJECTED | Baseline: D_min = 1 ở cả 4 layout tại N = 50, 100, 200 (khoảng bootstrap có độ rộng 0). | Đúng với baseline. Không đúng với Kubo: D_min = 4 ở outlier_rich N = 200 và không có D_min ở wide (Phase 4). |
| C1b | INCONCLUSIVE | Baseline không có D_min thay đổi nên phép so sánh state với (N, D) không có gì để giải thích. | Package B báo likelihood NaN. Chi phí (path, ticks) có phụ thuộc layout, xem mục 4. |
| C2a | REJECTED | Baseline: không có ô overcrowding trên bản đồ compact (R >= 0.90 đến D = 35). | Overcrowding chỉ xuất hiện ở Kubo outlier_rich N = 200 (D_overcrowd = 10) và là hiệu ứng yếu. |
| C2b | SKIPPED | Không có ô overcrowding để kéo dài đến T = 20,000. |  |
| C3 | INCONCLUSIVE | Kiểm tra cơ chế cần ô overcrowding; baseline không có. | Kubo outlier_rich N = 200 là ô ứng viên đã có sẵn trong dữ liệu. |
| C4 | SUPPORTED (partial) | Baseline và Kubo chia sẻ D_min = 1 với N >= 25; FAT không chuyển giao được. | Tracker ghi SUPPORTED, discuss/phase4.md ghi một phần. "Một phần" là cách ghi chính xác. |
| C6a | EVALUATED, weak | Piecewise thắng power law về RMSE leave-one-N-out (0.13 so với 0.25). | Mô hình 'piecewise' chỉ là hai mức {2, 1} với điểm gãy tại N = 10. Đó không phải quy luật scaling. |
| C5a/b, C6b, C7a/b | UNEVALUATED | Phase 5 và 7 chưa chạy; C6b chưa có dải N nào được nêu. |  |

## 8. Giới hạn và bước tiếp theo đề xuất

- **Hiệu ứng trần.** R = 1.00 tại D = 1 ở gần như mọi ô baseline. Bề mặt phẳng, nên C1 đến C3 không thể được ủng hộ hay bác bỏ một cách có ý nghĩa. Cần một thiết lập khó hơn trước khi các phase sau có giá trị. Các nút chỉnh có thể thử (chưa thử): T0 ngắn hơn, quãng lùa dài hơn, đích nhỏ hơn, pha hold, quan sát nhiễu hoặc hạn chế (Phase 5).
- **Tài liệu không khớp.** `docs/discuss/phase4.md` nêu Kubo có D_min = 1 ở cả bốn layout và không overcrowding; dữ liệu (Bảng 5) cho thấy không có D_min ở wide và D_min = 4 kèm overcrowding tại 10 ở outlier_rich N = 200.
- **Cách ghi trong tracker.** C4 ghi SUPPORTED trong khi discussion ghi một phần; C6a ghi EVALUATED nhưng phép fit bị suy biến.
- **Biên mềm.** Kubo outlier_rich N = 200 nằm trong khoảng +/-0.06 của R. Theo quy tắc trong plan, hãy nâng cửa sổ đó lên 200 seed trước khi coi D_overcrowd = 10 là thật.
- **Có sẵn một phép thử cơ chế khả dụng.** C3 bị ghi inconclusive vì thiếu ô overcrowding, nhưng Kubo outlier_rich N = 200 (và Kubo wide, nơi thành công không cải thiện theo D) có thể làm ô đối chiếu.
- **Layout split.** Cần xác nhận bộ sinh tạo ra các cụm tách biệt lúc đầu chứ không chỉ chỉ số phân mảnh trung bình thấp hơn; kết quả không phân biệt được với compact.
- **Phạm vi.** Một task, các bộ điều khiển mô phỏng, một theta; kết quả chỉ nói về mô phỏng này.

## 9. Số liệu đến từ đâu

| Mục | Nguồn |
|---|---|
| Các dòng trial | `scaling/results/phase*/**/merged_trials.csv` |
| D_min, regime | `phase1/claim/packages/a/`, `phase4/*_size/claim/packages/a/` |
| Biên theo cấu trúc | `phase2/claim/packages/b/`, `phase4/package_d/structure/frontier_by_method_layout.csv` |
| Bảng chuyển giao | `phase4/package_d/` |
| Fit | `phase1/claim/packages/f/` |
| Giá trị draft | `scaling/docs/notes/sheep-scaling_paper2025.md` (từ Bảng A3 của PDF) |

*Bảng 7. Nguồn gốc dữ liệu.*
