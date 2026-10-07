# Đối chiếu bản thảo 2025 và HerdSim

## Trạng thái đối chiếu

Bản thảo 2025, *Collective Nudging that Scales. How many dogs do I need to herd sheep?*, báo cáo một nghiên cứu NetLogo 7.0.3. HerdSim `scaling_v2` là một nghiên cứu mô phỏng Python riêng. Hai nghiên cứu chia sẻ câu hỏi rộng, lưới số chó, hạn 10,000 tick, và ngưỡng tin cậy 90%. Chúng không chia sẻ cùng nhiệm vụ, sân, khởi tạo, bộ điều khiển, hoặc định nghĩa biên.

Bản thảo không được chạy lại trong HerdSim hoặc NetLogo trong chương trình hiện tại. Giá trị bản thảo bên dưới được chép từ PDF và ghi chú trong kho. Giá trị HerdSim đến từ dữ liệu tầng claim. Đây là đối chiếu kết quả giữa hai giao thức, không phải kiểm tra tái lập.

![Bản thảo gom, giữ, ra cổng so với HerdSim lùa vào đích.](../../results/summary/figures/schematics/vi/draft_vs_herdsim.svg)

## Đối chiếu giao thức

| Mục | Bản thảo 2025 | HerdSim `scaling_v2` |
|---|---|---|
| Động cơ | NetLogo 7.0.3 trên lưới patch | HerdSim trong không gian liên tục với tick rời rạc |
| Nhiệm vụ | Gom, giữ 800 tick, rồi đưa qua cổng | `drive_to_goal`, mọi cừu nằm trong đĩa đích |
| Thành công | Mọi cừu qua cổng trước 10,000 tick | Tỉ lệ trong đĩa đích đạt 1.0 trước T0 = 10,000 |
| Sân | 101 x 71 patch, vùng giữ ở tâm, cổng trên tường phải | Sân 500 x 500, đàn tại (250, 250), đích tại (370, 250) |
| Vùng giữ hoặc đích | `rc = clamp(2.5 * sqrt(N), 23, 27)` | Bán kính `15 * sqrt(N/50)` |
| Khởi tạo cừu | Rải ngẫu nhiên, có đệm với tường và chó | Các họ `compact`, `wide`, `split`, và `outlier_rich` được kiểm soát |
| Khởi tạo chó | Lưới tại góc trên trái | Sau đàn, đối diện đích, lệch 50 với nhiễu `+/-5` |
| Bộ điều khiển | Một họ NetLogo gom, lùa, và tuần tra | Cơ sở `strombom_multi`; chuyển giao `kubo` và `fat` |
| Lưới D | `{1, 2, 3, 4, 6, 10, 15, 20, 25, 35}` | Giống |
| Lưới N | `{5, 10, 25, 50, 100, 150, 200, 250, 300, 350, 400}` | `{5, 10, 25, 50, 75, 100, 150, 200, 300, 400}` |
| Lấy mẫu | 100 lần mỗi ô, tổng 11,000 | Scout 30 mỗi ô; claim thường gieo lại 100 trên cửa sổ đã chọn |
| Seed | Seed gốc không nêu trong ghi chú | Seed gốc 2026; seed thử nghiệm `2026 + i` |
| Tin cậy | SR >= 90% | R >= theta, với theta = 0.90 cho biên claim |
| D_min | D nhỏ nhất có SR >= 90% | D đã thử nhỏ nhất có R >= theta |
| D_overcrowd | D đầu tiên trên D_min nơi SR bắt đầu giảm | Đầu của hai D liên tiếp dưới theta sau D_min |
| D_max | D đầu tiên trên D_min có SR < 90%, nếu không thì trần | D tin cậy lớn nhất trước D_overcrowd; nếu không thì trần lưới 35 |
| Bất định | Không báo cáo khoảng nhị thức hoặc bootstrap D_min | 1,000 bootstrap seed cho D_min |
| Cấu trúc | Độ rải phát sinh, tóm tắt bằng `S_bar` | Bố cục khởi tạo kiểm soát, cohesion, fragmentation, và mean spread |
| Chỉ số | Thành công, tick, pha, spread, path, và cừu lạc | Thành công, tick, path, cohesion, fragmentation, spread, interference, và nhãn thất bại |

![Các pha nhiệm vụ bản thảo được báo cáo.](../../results/summary/figures/schematics/vi/draft_task_phases.svg)

## Kết quả bản thảo được báo cáo

Tại SR >= 90%, Bảng A3 của bản thảo báo cáo:

| N | D_min bản thảo | D_max bản thảo | SR tối đa |
|---|---:|---:|---:|
| 5 | 1 | chưa đạt | 100% |
| 10 | 1 | 15 | 100% |
| 25 | 1 | 25 | 100% |
| 50 | 1 | 25 | 100% |
| 100 | 1 | chưa đạt | 100% |
| 150 | 3 | chưa đạt | 99% |
| 200 | 20 | 35 | 94% |
| 250 | 25 | chưa đạt | 93% |
| 300 | 20 | chưa đạt | 93% |
| 350 | 35 | chưa đạt | 91% |
| 400 | 35 | chưa đạt | 91% |

"Chưa đạt" nghĩa là biên thất bại phía trên chưa được tìm thấy tại D = 35. Đây là giá trị bản thảo báo cáo, không phải kết quả được tạo lại bởi kho này.

Bản thảo cũng báo cáo liên hệ âm giữa mean spread và thành công, gồm Spearman rho = -0.701 cho `S_bar` với SR và rho = -0.828 cho `S_bar * N` với SR trên 110 tổng hợp điều kiện. Phân tích nhạy cảm và density gradient không được chạy lại ở đây.

![Tóm tắt trực quan chép từ Bảng A3 của bản thảo.](../../results/summary/figures/schematics/vi/draft_main_results.svg)

## Kết quả HerdSim dùng để đối chiếu

Với cơ sở `strombom_multi` trên xuất phát compact, dữ liệu claim cho D_min = 2 tại N trong `{5, 10}` và D_min = 1 từ N = 25 đến 400. D_max = 35 là trần lưới đã thử trong mọi ô Giai đoạn 1 vì không thấy cặp overcrowding. Nó không phải điểm sụp phía trên đã đo.

Đổi bố cục khởi tạo không đổi D_min cơ sở tại N trong `{50, 100, 200}`, nhưng đổi chi phí rõ rệt. Kubo gần khớp cơ sở compact, trong khi Kubo trên wide và FAT trên đàn lớn thường không đạt R = 0.90 tại bất kỳ D nào trong lưới. Đây là kết quả chuyển giao HerdSim, không phải kết quả parity với bản thảo hoặc NetLogo.

| Phát hiện bản thảo | Kết quả HerdSim theo giao thức của nó | Trạng thái |
|---|---|---|
| Một chó đủ đến khoảng N = 100 rồi sụp | Một chó đạt R >= 0.90 đến N = 400 trên cơ sở compact | Không tái hiện |
| D_min tăng lên 20 đến 35 khi N >= 200 | D_min cơ sở vẫn là 1 | Không tái hiện |
| D cao có thể gây overcrowding cho đàn nhỏ | Không có cặp overcrowding cơ sở đến D = 35 | Không tái hiện |
| Thời gian giảm theo D; quãng đường bão hòa | Thời gian cơ sở gần phẳng; tổng đường chó tăng theo D | Hình dạng đo khác |
| Spread dự đoán thất bại | Chưa có phân tích đối ứng có kiểm soát ở mức claim | Chưa kiểm parity |
| Một bộ điều khiển, không bất định D_min | Ba bộ điều khiển HerdSim, bốn bố cục, và bootstrap | Bằng chứng HerdSim bổ sung |

![Các phân tích bản thảo không được chạy lại.](../../results/summary/figures/schematics/vi/draft_extra_analyses.svg)

## Vì sao kết quả có thể khác

Khác biệt có thể đến từ pha giữ và qua cổng, cừu rải lúc đầu, chó xuất phát ở góc, hình học vùng giữ, và chi tiết bộ điều khiển của bản thảo. HerdSim dùng đường lùa nội bộ ngắn hơn với chó đã ở sau đàn. Đây chỉ là diễn giải. Không có thí nghiệm thay từng thành phần để tách một nguyên nhân.

Vì vậy, "không tái hiện" nghĩa là kết quả không xuất hiện dưới giao thức HerdSim khác. Nó không chứng minh kết quả bản thảo sai.

## Đã chạy và chưa chạy lại

| Mục | Trạng thái |
|---|---|
| Dữ liệu claim HerdSim Giai đoạn 1, 2, và 4 | Đã chạy và dùng cho kết luận hiện tại |
| Thí nghiệm 11,000 lần của bản thảo 2025 | Không chạy lại |
| Các ô nhạy cảm của bản thảo | Không chạy lại |
| Phân tích density gradient của bản thảo | Không chạy lại |
| Bộ phân loại và tương quan spread của bản thảo | Không chạy lại |
| Mô hình bản thảo như một twin đi kèm | Không, không có trong `twins.json` |
| Thay giao thức có kiểm soát giữa bản thảo và HerdSim | Chưa chạy |

## Trích dẫn và nguồn gốc

Nguồn bản thảo chính:

*Collective Nudging that Scales. How many dogs do I need to herd sheep?* Bản thảo, khoảng 2025, đồng tác giả tạm. Bản trong kho: [PDF](../../../docs/papers/sheep-scaling_paper2025.pdf).

Tài liệu hỗ trợ diễn giải:

- [Ghi chú tham chiếu bản thảo](../notes/sheep-scaling_paper2025.md)
- [Báo cáo tổng hợp tiếng Anh](../../results/summary/SUMMARY_REPORT.md)
- [Báo cáo tổng hợp tiếng Việt](../../results/summary/SUMMARY_REPORT_vi.md)
- [Ranh giới xác thực và NetLogo](validation_and_netlogo_vi.md)
