# Cơ sở Strombom Collect/Drive

## Cảm hứng từ công bố

Strombom và cộng sự (2014) mô tả một người chăn chuyển giữa hai hành động. Ở chế độ Collect, người chăn đi ra sau con cừu xa tâm đàn nhất và đẩy nó vào trong. Ở chế độ Drive, người chăn đi ra sau tâm đàn theo hướng ngược đích và đẩy đàn đã kết dính tiến về đích.

Quy tắc chuyển chế độ dùng:

```text
f(N) = r_a * N^(2/3)
```

Nếu có cừu cách tâm khối lượng toàn đàn xa hơn `f(N)`, đàn được xem là đang trải và người chăn Collect. Nếu không, người chăn Drive. Mô hình công bố cũng là cơ sở cho các quy tắc hút, đẩy, quán tính, ăn cỏ, nhiễu, và dừng của cừu Strombom trong HerdSim.

Tài liệu: D. Strombom và cộng sự, "Solving the shepherding problem: heuristics for herding autonomous, interacting agents," Journal of The Royal Society Interface 11(100), 2014. DOI: `10.1098/rsif.2014.0719`.

![strombom_multi: gom / lùa.](../../results/summary/figures/schematics/vi/alg_strombom_multi.svg)

## Hiện thực HerdSim chính xác

HerdSim tách động lực cừu và bộ điều khiển chó.

Preset `strombom` kết hợp:

- `sheep_model=strombom`;
- `dog_controller=collect_drive`;
- mặc định một người chăn.

Nghiên cứu scaling hoàn tất không dùng preset này. Nghiên cứu dùng `strombom_multi`, vẫn dùng cừu Strombom nhưng ghép với `dog_controller=collect_drive_multi`.

### Cừu

Khi mọi chó đang hoạt động đều cách xa hơn `r_s`, cừu ăn cỏ. Cừu thường đứng yên và bước ngẫu nhiên với xác suất `graze_move_prob`. Khi có chó trong `r_s`, cừu kết hợp hướng trước, lực hút về tâm láng giềng, lực đẩy cừu ở tầm ngắn, lực đẩy khỏi chó đang hoạt động, và nhiễu ngẫu nhiên. Sau đó cừu đi `sheep_speed`.

Mặc định của bundle gồm `r_a = 2`, `r_s = 65`, `c = 1.05`, `inertia = 0.5`, `noise_strength = 0.3`, `sheep_speed = 1.0`, và `shepherd_speed = 1.5`.

### Bộ điều khiển nhiều chó

Trong quan sát global của các giai đoạn scaling hoàn tất, mỗi chó thấy toàn đàn và tính cùng tâm cùng ngưỡng.

Trong Collect:

- cừu ngoài `f(N)` được sắp theo khoảng cách đến tâm;
- chó `i` nhận cá thể lạc `i mod k`, với `k` là số cá thể lạc;
- đích cơ sở nằm sau cá thể được gán một khoảng `r_a` theo hướng ra xa tâm;
- lệch tiếp tuyến `2 * r_a` mỗi slot tách các chó cùng tiếp cận một cá thể.

Trong Drive:

- đích cơ sở nằm sau tâm đàn một khoảng `r_a * sqrt(N)` theo hướng ngược đích;
- các chó nằm ở góc cách đều trên đường tròn bán kính `4 * r_a` quanh đích cơ sở.

Mỗi chó dừng khi gần hơn `shepherd_stop_multiple * r_a` với bất kỳ cừu nào trong view đang dùng. Giá trị mặc định của multiple là 3. Chuyển động chó có nhiễu góc Strombom.

Gán cá thể lạc, lệch tiếp tuyến trong Collect, và đường tròn Drive là phần bổ sung của HerdSim. Chúng không nằm trong thuật toán một người chăn năm 2014 và không được khẳng định là bản port của một bộ điều khiển nhiều người chăn đã công bố khác.

Bằng chứng hiện thực:

- [`../../../core/methods.py`](../../../core/methods.py)
- [`../../../plugins/sheep/strombom.py`](../../../plugins/sheep/strombom.py)
- [`../../../plugins/dogs/collect_drive_multi.py`](../../../plugins/dogs/collect_drive_multi.py)
- [`../../../methods/strombom/heuristics.py`](../../../methods/strombom/heuristics.py)
- [`../../../methods/strombom/config.py`](../../../methods/strombom/config.py)

## Thiết lập `scaling_v2`

`strombom_multi` là bộ điều khiển cơ sở trong giao thức đóng băng.

- Giai đoạn 1: bố cục compact, lưới kích thước `N = {5, 10, 25, 50, 75, 100, 150, 200, 300, 400}`.
- Giai đoạn 2: `compact`, `wide`, `split`, và `outlier_rich` tại `N = {50, 100, 200}`.
- Lưới chó: `{1, 2, 3, 4, 6, 10, 15, 20, 25, 35}`.
- Chế độ quan sát trong so sánh hoàn tất: global.
- Ngưỡng tin cậy: `R >= 0.90`.
- Scout: 30 seed mỗi ô trên toàn lưới.
- Claim: 100 seed trong cửa sổ biên đã lên kế hoạch.

Thí nghiệm ghi đè số chó mặc định khi quét `D`. Các phương trình điều khiển và mặc định Strombom ở trên được giữ.

Bằng chứng cấu hình:

- [`../../configs/canonical_grid.yaml`](../../configs/canonical_grid.yaml)
- [`../../configs/protocols/phase1_claim.yaml`](../../configs/protocols/phase1_claim.yaml)
- [`../../configs/protocols/phase2_claim.yaml`](../../configs/protocols/phase2_claim.yaml)

## Kết quả hoàn tất đã quan sát

### Bản đồ kích thước compact

Tại ngưỡng tin cậy 90%:

- `D_min = 2` với `N = 5` và `N = 10`;
- `D_min = 1` với mọi `N` đã thử từ 25 đến 400;
- không quan sát thấy overcrowding;
- `D_max = 35` là trần lưới cho mọi kích thước, không phải điểm sụp đã đo.

![Heatmap độ tin cậy compact.](../../results/phase1/guides/assets/figures/reliability_heatmap.png)

*Mỗi ô là R(N, D) trên merge claim Giai đoạn 1 (compact). Ô tối hơn là dưới ngưỡng 0.90.*

Bản merge claim Giai đoạn 1 có 4,540 dòng và `R = 0.963` toàn bộ. Phần lớn 169 lần thất bại tập trung ở một chó với hai đàn nhỏ nhất.

![D_min theo kích thước đàn.](../../results/phase1/guides/assets/figures/f2_dmin_vs_n.png)

*D_min cơ sở theo N, kèm đường bản thảo 2025 chỉ để đối chiếu. Hai mức quan sát: 2 ở N = 5 và 10; 1 từ N = 25 trở lên.*

Thời gian hoàn thành trung vị trên merge là 183 tick. Với `N >= 25`, đường trung vị mỗi chó khoảng 148 đơn vị.

![Chi phí theo số chó.](../../results/phase1/guides/assets/figures/f3_cost_vs_d.png)

*Tổng đường trung vị theo D trên bản đồ kích thước compact. Thêm chó sau D_min chủ yếu là lãng phí đường, không phải sụp độ tin cậy trong lưới đã thử.*

### Cấu trúc ban đầu

Tại `N = 50, 100, 200`, cả bốn bố cục đều có `D_min = 1`, với độ rộng bootstrap bằng 0. Cấu trúc đổi chi phí, không đổi số chó tin cậy tối thiểu:

- wide cần khoảng 11 đến 20 lần thời gian compact và 19 đến 36 lần đường compact ở một chó;
- `outlier_rich`, `N = 200` có trung vị 1,228 tick và đường 1,647 ở một chó;
- trên wide, lựa chọn tin cậy có đường nhỏ nhất `B*` là hai chó ở cả ba kích thước.

![So sánh chi phí bố cục.](../../results/phase2/guides/assets/figures/f4_layout_cost.png)

*Tổng đường trung vị tại D = 1 theo bố cục. Wide và outlier_rich đắt hơn nhiều so với compact dù vẫn đạt R = 1.00 ở một chó.*

![Đường wide với một và hai chó.](../../results/phase2/guides/assets/figures/f10_wide_bstar_path.png)

*Trên wide, hai chó cắt đường trung vị so với một chó tại N = 50, 100, và 200, nên B* = 2 dù D_min vẫn = 1.*

Bằng chứng:

- [`../../results/phase1/claim/packages/a/frontier.csv`](../../results/phase1/claim/packages/a/frontier.csv)
- [`../../results/phase1/claim/merged_trials.csv`](../../results/phase1/claim/merged_trials.csv)
- [`../../results/phase2/claim/packages/b/frontier_by_layout.csv`](../../results/phase2/claim/packages/b/frontier_by_layout.csv)
- [`../../results/phase2/claim/merged_trials.csv`](../../results/phase2/claim/merged_trials.csv)

## Giới hạn và điều không khẳng định

- Cơ sở cấp claim là `strombom_multi` của HerdSim, không phải thuật toán một người chăn đã công bố mà không sửa đổi.
- Nhiệm vụ compact dễ tạo hiệu ứng trần. Một chó thành công với mọi `N >= 25`, nên dữ liệu này không hỗ trợ một quy luật số chó tăng theo scaling.
- `D_max = 35` nghĩa là chưa thấy sụp trong lưới đã thử. Nó không phải giới hạn sinh học hay vận hành.
- Bố cục split hoạt động gần giống compact trong phân tích hoàn tất. Báo cáo tổng hợp đánh dấu việc tách cụm ban đầu cần được xác nhận thêm trong generator, nên không đưa ra kết luận cơ chế mạnh cho split.
- Twin NetLogo được đăng ký chỉ cho thấy có bản đối ứng, không chứng minh bằng nhau từng tick. Registry: [`../../../integrations/netlogo/twins.json`](../../../integrations/netlogo/twins.json).
- Kết quả không chứng minh hiệu năng chó thật và không tái tạo kết quả định lượng của bài báo 2014.
