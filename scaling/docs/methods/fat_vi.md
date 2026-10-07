# FAT: nhắm cá thể xa nhất

## Cảm hứng từ công bố

FAT được truyền cảm hứng bởi quy tắc chăn đàn với camera cục bộ trong Tsunoda và cộng sự (2018): tác động lên cá thể xa nhất trong tập mà người chăn nhìn thấy, không cần tọa độ toàn đàn.

HerdSim không hiện thực đầy đủ mô hình camera, xử lý sai số vị trí, động lực cừu, luật điều hướng, hay hiệu chỉnh thí nghiệm của bài báo. Vì vậy phần công bố chỉ là cảm hứng cho cách chọn mục tiêu, không phải khẳng định tái tạo toàn bộ mô hình.

Tài liệu: Y. Tsunoda và cộng sự, "Analysis of local-camera-based shepherding navigation," Advanced Robotics 32(23), 2018. DOI: `10.1080/01691864.2018.1539410`.

![FAT nhắm cá thể xa nhất so với chó.](../../results/summary/figures/schematics/vi/alg_fat.svg)

## Hiện thực HerdSim chính xác

Bundle `fat` kết hợp:

- `sheep_model=strombom`;
- `dog_controller=fat`;
- mặc định hai chó khi không có ghi đè thí nghiệm.

Cừu dùng quy tắc ăn cỏ, tạo đàn, đẩy, và dịch chuyển cố định của Strombom trong HerdSim. Bộ điều khiển chó không có chuyển Collect/Drive và không kiểm tra kết dính toàn đàn.

Với mỗi chó đang hoạt động trong mỗi tick:

1. Đọc quan sát của chó sau các bộ lọc chế độ quan sát và cảm biến.
2. Nếu không thấy cừu, để chó đứng yên.
3. Chọn con cừu quan sát được xa chính con chó nhất.
4. Đặt đích cách `r_a` sau con cừu trên tia đi từ đích qua cừu.
5. Đi về đích đó với `shepherd_speed` và nhiễu góc Strombom.
6. Dừng nếu có cừu trong view đang dùng gần hơn `shepherd_stop_multiple * r_a`.

Mỗi chó chọn độc lập. FAT không có lực đẩy giữa chó, đàm phán gán mục tiêu, hay khoảng cách đội hình rõ ràng. "Xa nhất" là xa con chó nhất, khác Collect Strombom (xa tâm đàn nhất) và Kubo (xa đích nhất).

Bằng chứng hiện thực:

- [`../../../core/methods.py`](../../../core/methods.py)
- [`../../../plugins/dogs/fat.py`](../../../plugins/dogs/fat.py)
- [`../../../plugins/sheep/strombom.py`](../../../plugins/sheep/strombom.py)
- [`../../../methods/strombom/heuristics.py`](../../../methods/strombom/heuristics.py)
- [`../../../methods/strombom/config.py`](../../../methods/strombom/config.py)

## Thiết lập `scaling_v2`

FAT là phương pháp chuyển giao Giai đoạn 4 trên cùng nhiệm vụ và lưới với Kubo và cơ sở.

- Bản đồ kích thước: compact trên toàn lưới kích thước và số chó.
- Bản đồ cấu trúc: bốn bố cục tại `N = {50, 100, 200}`.
- Quan sát: global.
- Giao tiếp: bộ điều khiển FAT không thêm phối hợp.
- Hạn: `T0 = 10000`.
- Ngưỡng tin cậy: `R >= 0.90`.
- Phân tầng: 30 seed scout, sau đó 100 seed claim trong cửa sổ đã chọn.

Thiết lập global rất quan trọng. Dù ý tưởng chọn mục tiêu đến từ cảm biến cục bộ, các Giai đoạn 1, 2, và 4 hoàn tất cho mỗi chó FAT thấy toàn đàn. Các kết quả này không kiểm tra giới hạn thông tin camera cục bộ. Thí nghiệm chế độ quan sát được lập kế hoạch cho Giai đoạn 5 nhưng chưa chạy.

Bằng chứng cấu hình:

- [`../../configs/canonical_grid.yaml`](../../configs/canonical_grid.yaml)
- [`../../configs/protocols/phase4_fat_size_claim.yaml`](../../configs/protocols/phase4_fat_size_claim.yaml)
- [`../../configs/protocols/phase4_fat_structure_claim.yaml`](../../configs/protocols/phase4_fat_structure_claim.yaml)

## Kết quả hoàn tất đã quan sát

### Bản đồ kích thước compact

- `D_min = 1` tại `N = 5` và `N = 10`.
- Với mọi `N >= 25`, không số chó nào đến 35 đạt `R >= 0.90`.
- Các ô này là thất bại cứng: `D_min` và `D_max` không xác định, không phải 0 và cũng không phải 35.
- Độ tin cậy tốt nhất theo kích thước với `N = 50` đến 400 khoảng 0.40 đến 0.53.
- Khoảng nửa các lần chạy kích thước FAT thất bại. Báo cáo tổng hợp gán khoảng 39% toàn bộ trial cho oscillation và 7% cho stuck.

![Heatmap compact của ba phương pháp.](../../results/phase4/guides/assets/figures/f1_reliability_heatmaps.png)

*Bề mặt R(N, D) trên compact. FAT chỉ đạt ngưỡng ở N = 5 và 10; từ N = 25 trở lên không ô nào đạt 0.90.*

![So sánh kiểu thất bại.](../../results/summary/figures/f6_failure_modes_vi.png)

*FAT thất bại chủ yếu bằng oscillation hoặc stuck, khác Kubo (timeout) và cơ sở (ít thất bại hơn nhiều).*

### Cấu trúc ban đầu

FAT không đạt 90% trong bất kỳ ô cấu trúc nào tại `N = 50, 100, 200`.

- Compact có `R` tốt nhất: 0.47, 0.40, 0.47 với `N = 50, 100, 200`.
- Split có `R` tốt nhất: 0.50, 0.47, 0.40.
- `outlier_rich` có `R` tốt nhất: 0.10, 0.00, 0.00.
- Wide có `R` tốt nhất: 0.00 ở cả ba kích thước.

![Đường độ tin cậy theo bố cục.](../../results/summary/figures/f5_layout_reliability_curves_vi.png)

*R theo D tại N = 200. FAT không đạt 0.90 ở bất kỳ bố cục nào trên lưới đã thử.*

Báo cáo tổng hợp cũng ghi nhận liên hệ âm mạnh giữa nhiễu hướng FAT và thành công trên merge kích thước, với Pearson `r` khoảng `-0.87`. Đây là quan sát, không chứng minh nhiễu là nguyên nhân thất bại.

![Nhiễu hướng theo số chó.](../../results/summary/figures/f7_interference_vi.png)

*Chỉ số nhiễu hướng theo D. Liên hệ âm với thành công FAT là quan sát trên merge kích thước, không phải phép thử nhân quả.*

Bằng chứng:

- [`../../results/phase4/fat_size/claim/packages/a/frontier.csv`](../../results/phase4/fat_size/claim/packages/a/frontier.csv)
- [`../../results/phase4/fat_size/claim/merged_trials.csv`](../../results/phase4/fat_size/claim/merged_trials.csv)
- [`../../results/phase4/fat_structure/claim/merged_trials.csv`](../../results/phase4/fat_structure/claim/merged_trials.csv)
- [`../../results/phase4/package_d/structure/frontier_by_method_layout.csv`](../../results/phase4/package_d/structure/frontier_by_method_layout.csv)

## Giới hạn và điều không khẳng định

- Đây là bộ điều khiển FAT tối giản của HerdSim trên cừu Strombom, không phải mô hình đầy đủ của Tsunoda và cộng sự.
- Kết quả hoàn tất dùng quan sát global. Chúng không đo che khuất camera, điều khiển chỉ có góc, sai số vị trí, hay phục hồi khi mất dấu vết.
- Thất bại cứng nghĩa là không số chó đã thử nào đạt thanh 90% trước `T0`. Nó không chứng minh FAT không thể hoạt động với `D` lớn hơn, timeout khác, hay nhiệm vụ khác.
- Tăng số chó không cứu được đàn lớn trên lưới này. Quan sát đó không tách được cơ chế nhân quả.
- Tương quan nhiễu không phải phép thử nhân quả có kiểm soát.
- FAT không có twin NetLogo trong registry: [`../../../integrations/netlogo/twins.json`](../../../integrations/netlogo/twins.json).
- Kết quả không chứng minh hiệu năng ngoài đồng và không tái tạo kết quả định lượng của bài báo 2018.
