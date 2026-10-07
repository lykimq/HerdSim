# Khả năng chăn dắt tập thể dưới shepherding: Kế hoạch scaling chính

Giao thức: `scaling_v2`.

Tài liệu này là kế hoạch khoa học. Nó định nghĩa mục tiêu nghiên cứu, phụ thuộc giữa các giai đoạn, câu hỏi nghiên cứu, tiêu chí claim, cấp bằng chứng, ngân sách, cổng quyết định, và giới hạn nghiên cứu. Nó không lặp lại lý do thiết lập, giải thích bộ điều khiển, quyền sở hữu triển khai, mục từ vựng, hay lệnh chạy.

Tài liệu chuẩn hỗ trợ:

- [Chương trình nghiên cứu](herdsim_research_program.md)
- [Mục lục thiết lập và tham chiếu](setup/README_vi.md)
- [Thiết lập thí nghiệm](setup/experiment_setup_vi.md)
- [Tham chiếu tham số](setup/parameter_reference_vi.md)
- [Bảng thuật ngữ](setup/glossary_vi.md)
- [Hướng dẫn phương pháp](methods/README_vi.md)
- [Độ tin cậy và so sánh](credibility/README_vi.md)
- [Chiến lược chạy](experiment_run_strategy.md)
- [Hướng dẫn chạy](setup/run_guide_vi.md)
- [Theo dõi tiến độ](progress_tracker.md)
- [Phụ lục dữ liệu](../results/summary/data/README_vi.md)

## 1. Mục tiêu nghiên cứu

Chương trình hỏi cần bao nhiêu kiểm soát bên ngoài để dẫn một tập thể một cách đáng tin cậy khi kích thước đàn và cấu trúc ban đầu thay đổi, những quá trình nào giải thích nhu cầu đó, và những mẫu nào chuyển giao giữa các phương pháp chăn dắt.

Đại lượng chính của nhu cầu kiểm soát là miền số người chăn khả dụng quanh `D_min` và biên quá tải nếu quan sát được, dưới một nhiệm vụ, ngưỡng độ tin cậy, ngân sách thời gian, bố cục, phương pháp, và điều kiện thông tin cố định. `D_min` không phải thuộc tính nội tại của một đàn.

Đơn vị công bố nhỏ nhất là RQ1, RQ2, RQ3, và giao thức đóng băng. RQ4 lặp lại cả bản đồ kích thước và đối sánh cấu trúc cho các phương pháp chuyển giao bắt buộc. RQ5 và RQ7 là nghiên cứu tiếp theo. RQ6 dùng các bản đồ biên đã hoàn tất và không được quyết định lưới theo dữ liệu sau khi chạy.

## 2. Bản đồ công việc và phụ thuộc

| Giai đoạn | Vai trò nghiên cứu | RQ | Gói | Phụ thuộc | Điều kiện hoàn tất trong kế hoạch |
|---|---|---|---|---|---|
| 0 | Đóng băng giao thức chung | S8 | all | không | YAML chuẩn và kế hoạch khoa học thống nhất |
| 1 | Bản đồ kích thước và chế độ cơ sở | RQ2 | A | Giai đoạn 0 | Biên cơ sở đã hợp nhất, chế độ, và quyết định T1 có điều kiện |
| 2 | Cấu trúc tại N cố định | RQ1 | B | Quy tắc scout và cửa sổ claim của Giai đoạn 1 | Biên theo bố cục đã hợp nhất và so sánh bộ dự báo |
| 3 | Đối sánh cơ chế | RQ3 | C | Ô hiệu quả và quá tải khớp từ Giai đoạn 1 hoặc 2 | Kiểm định trong cùng N đã định trước, hoặc trạng thái undefined rõ ràng |
| 4 | Chuyển giao giữa các phương pháp | RQ4 | D | Thiết kế Giai đoạn 1 và 2 đã cố định | Bản đồ kích thước và cấu trúc cho mọi phương pháp bắt buộc |
| 5 | Thay thế thông tin | RQ5 | E | Cơ sở phương pháp ổn định và đường ống chạy phân tầng | Biên của các thang quan sát, tầm, và giao tiếp |
| 6 | Khớp scaling | RQ6 | F | Bản đồ biên cấp CLAIM | So sánh đường cong bằng leave-one-N-out |
| 7 | Cảnh báo sớm | RQ7 | G | Quỹ đạo cấp CLAIM có chuỗi thời gian cần thiết | Đánh giá AUROC và thời gian dẫn trên tập holdout |

Quy tắc phụ thuộc:

1. Giai đoạn 0 đứng trước mọi lần chạy khoa học.
2. Giai đoạn 1, 2, và 4 dùng bản đồ scout trước khi gieo lại claim.
3. Giai đoạn 3 là phân tích các ô đối sánh đã thu. Giai đoạn này undefined nếu các chế độ cần thiết không tồn tại.
4. Claim cấu trúc của Giai đoạn 4 chờ bản đồ cấu trúc từ mọi phương pháp bắt buộc.
5. Giai đoạn 5 gồm ba thang riêng, không phải tích Descartes.
6. Giai đoạn 6 chỉ khớp sau khi có biên.
7. Giai đoạn 7 cần chuỗi thời gian cấp CLAIM và holdout toàn bộ N.

## 3. Hợp đồng kế hoạch chung

Giá trị máy đọc nằm trong [`canonical_grid.yaml`](../configs/canonical_grid.yaml). Ý nghĩa và lý do của tham số nằm trong [tham chiếu tham số](setup/parameter_reference_vi.md) và [thiết lập thí nghiệm](setup/experiment_setup_vi.md).

Kế hoạch khóa các ràng buộc sau:

- Nhiệm vụ: `drive_to_goal`, chỉ thành công khi mọi cừu đến đích trước hạn.
- Ngưỡng độ tin cậy chính: `theta = 0.90`; cũng báo cáo 0,50 và 0,70.
- Phương pháp cơ sở: `strombom_multi`.
- Tập chuyển giao bắt buộc: `strombom_multi`, `kubo`, và `fat`.
- Phương pháp chuyển giao khuyến nghị nhưng không nằm trong tập tối thiểu: `communication_free`.
- Lưới kích thước đàn: `{5, 10, 25, 50, 75, 100, 150, 200, 300, 400}`.
- Lưới số người chăn: `{1, 2, 3, 4, 6, 10, 15, 20, 25, 35}`.
- Bố cục: `compact`, `wide`, `split`, và `outlier_rich`.
- Kích thước cấu trúc: `{50, 100, 200}`.
- Kích thước thông tin: `{100, 200}`.
- Hạn: `T0 = 10000`; `T1 = 20000` có điều kiện.
- Danh sách seed khóa từ seed chủ 2026.
- Độ sâu scout: 30 seed mỗi ô được chọn.
- Độ sâu claim: thông thường 100 seed mỗi ô được chọn.
- Bootstrap: 1000 lần lấy mẫu lại seed.

Hiệu ứng theo số chó được đo bằng bước cục bộ của lưới. Nghiên cứu không phân giải được chênh lệch nhỏ hơn một bước cục bộ của lưới D đã thử.

### Quy tắc biên và chế độ

Đặt `R(m, tau, N, D, T, X0, I)` là xác suất thành công trên các seed đã khóa.

| Đại lượng | Định nghĩa kế hoạch |
|---|---|
| `D_min` | D nhỏ nhất đã thử với `R >= theta` |
| `D_overcrowd` | D nhỏ nhất sau `D_min` mà D đó và D kế tiếp trong lưới đều thấp hơn theta |
| `D_max` | D tin cậy lớn nhất dưới `D_overcrowd`; khi không có quá tải, là D tin cậy lớn nhất đã thử và có thể chỉ là trần lưới |
| `B*` | `(D, T)` tin cậy có trung vị đường đi người chăn nhỏ nhất; nếu bằng nhau, chọn D nhỏ hơn rồi thời gian thành công trung vị nhanh hơn |
| Thất bại cứng | Không có D đã thử nào đạt theta |
| Thất bại thiếu nguồn lực | `R < theta` dưới `D_overcrowd` |
| Vận hành hiệu quả | `R >= theta` và trung vị đường đi dưới ngưỡng lãng phí |
| Chi tiêu lãng phí | `R >= theta` và trung vị đường đi cao hơn `B*` ít nhất 20 phần trăm; cũng báo cáo 10 và 30 phần trăm |
| Sụp đổ quá tải | `R < theta` tại hoặc trên `D_overcrowd` |

Một `D_max` bằng 35 khi không có `D_overcrowd` là trần lưới đã thử, không phải điểm sụp đổ đã đo.

## 4. Cấp bằng chứng và ngân sách dự kiến

| Cấp độ | Mục đích | Độ sâu dự kiến | Được dùng cho claim |
|---|---|---:|---|
| SMOKE hoặc Pilot | Kiểm tra đường dẫn, chỉ số, máy chủ, và hành vi tiếp tục | Lưới chẩn đoán nhỏ, thông thường 5 seed | Không |
| SCOUT | Lập bản đồ rộng và chọn cửa sổ chính xác | 30 seed | Chỉ lập kế hoạch và chẩn đoán |
| CLAIM | Ước lượng biên đã chọn và đại lượng claim | Thông thường 100 seed | Có, sau khi kiểm tra nguồn gốc và tài liệu chạy |
| T1 | Thử hạn dài hơn trên ô quá tải đã phát hiện | 100 seed | Có, chỉ khi điều kiện kích hoạt tồn tại |

Với mỗi phương pháp, bố cục, và N, kế hoạch claim chọn:

1. `D_min` từ scout, cùng D trước và sau trong lưới.
2. Khi hai giá trị D liên tiếp xác lập một khởi phát quá tải ứng viên, chọn hai giá trị đó và D tin cậy cuối.
3. Nếu không D nào đạt theta, chọn hai giá trị D lớn nhất đã thử.

Dòng claim thay dòng scout trong ô đã gieo lại. Không bao giờ chồng dòng scout và claim của cùng ô. Ô không được chọn giữ độ sâu scout. Bootstrap lấy mẫu lại seed trong mỗi D; lần lấy mẫu không có `D_min` vẫn bị kiểm duyệt phải trên lưới đã thử. Nếu khoảng `D_min` trải hơn một bước lưới D, nâng cửa sổ đó lên 200 seed trước khi dùng cho claim cấu trúc.

### Ước lượng theo kế hoạch

Những số này là ước lượng ngân sách, không phải số đã thực thi:

| Chiến dịch | Ước lượng scout | Ước lượng claim | Ghi chú kế hoạch |
|---|---:|---:|---|
| Một bản đồ kích thước | Khoảng 3000 | Tối đa khoảng 6000 | Ước lượng claim giả định tối đa sáu giá trị D mỗi N |
| Một đối sánh cấu trúc | Khoảng 3600 | Tối đa khoảng 7200 | Ba N, bốn bố cục, toàn bộ lưới D cho scout |
| Lõi cơ sở | Khoảng 20000 tổng cộng | Đã gồm bên trong | Kích thước, T1 có điều kiện, và cấu trúc, làm tròn để lập kế hoạch |
| Mỗi phương pháp chuyển giao bắt buộc | Lặp lại ngân sách kích thước và cấu trúc | Tính lại sau scout | Cửa sổ claim phụ thuộc scout của phương pháp đó |

Công việc thực tế phải đọc từ artifact trạng thái và nguồn gốc, không suy ra từ các ước lượng này.

## 5. Câu hỏi nghiên cứu và phép thử dự kiến

### RQ1: Cấu trúc

`D_min` có thay đổi giữa các bố cục ban đầu tại N cố định không?

Dùng N trong `{50, 100, 200}`, cả bốn bố cục, và toàn bộ lưới D. So sánh `D_min` theo bước lưới. So sánh mô hình `(N, D)` với mô hình dùng thêm bố cục và trạng thái chỉ đo trong 100 tick đầu. Holdout toàn bộ N. Không dùng thống kê toàn lần thử làm bộ dự báo.

### RQ2: Kích thước và chế độ vận hành

Biên người chăn tin cậy và chế độ vận hành thay đổi theo N như thế nào?

Lập bản đồ `R(N, D)` tại T0 cho phương pháp cơ sở và bố cục compact. Ước lượng biên và nhãn chế độ theo quy tắc chung. Chỉ chạy T1 cho ô được chọn bởi điều kiện kích hoạt quá tải quan sát từ scout hoặc claim.

### RQ3: Cơ chế

Những chữ ký cơ chế nào đã định trước phân biệt ô hiệu quả và quá tải tại cùng N?

Dùng một trung vị mỗi ô `(N, D)`, kiểm định hạng, và hiệu chỉnh Holm trên các giả thuyết.

| Giả thuyết | Chữ ký bắt buộc |
|---|---|
| Nhiễu (interference) | Trung vị `I_dir` cao hơn trong ô quá tải |
| Phân mảnh cảm ứng | Tỷ lệ thành phần lớn nhất thấp hơn trong ô quá tải |
| Bảo hòa độ phủ | Trong ô tin cậy, trung vị độ phủ trên 0,5, miền theo D dưới 0,1, và trung vị đường đi tăng; đường cong gần không không phải bảo hòa |
| Nỗ lực dư thừa | Trung vị đường đi cao hơn mà độ tin cậy không tăng |

RQ3 không thêm lưới mới. Nếu một phương pháp không có nhãn quá tải, đối sánh cơ chế undefined cho phương pháp đó.

### RQ4: Tính tổng quát giữa các phương pháp

Những mẫu biên, chế độ, và cấu trúc nào chuyển giao giữa ba phương pháp bắt buộc?

Lặp lại bản đồ kích thước và đối sánh cấu trúc cho `kubo` và `fat`, rồi so sánh với `strombom_multi`.

| Thuộc tính | Chung (shared) | Dịch (shifted) | Vắng (absent) |
|---|---|---|---|
| `D_min` | Cùng D đã thử | D đã thử khác | Một bên không có `D_min` |
| Quá tải | Có ở cả hai và D/N trong hệ số 1,5 | Có ở cả hai với khoảng cách lớn hơn | Không có ở cả hai |
| `I_dir` | `r(I_dir, success) < -0.3` ở cả hai | Mẫu dấu cùng hướng nhưng độ lớn khác | Thiếu mẫu có ý nghĩa bắt buộc |
| Bảo hòa độ phủ | Quy tắc bảo hòa đúng ở cả hai | Đúng ở một bên | Không đúng ở cả hai |

Chỉ điền dòng chuyển giao phụ thuộc trạng thái khi mọi phương pháp được so sánh có lần chạy cấu trúc bắt buộc.

### RQ5: Thông tin so với số người chăn

Quan sát, tầm cảm biến, hoặc giao tiếp phong phú hơn có làm giảm `D_min` tại độ tin cậy cố định không?

Dùng N trong `{100, 200}`. Thử thang quan sát `bearing_only`, `local_positions`, `global`; hệ số tầm `0.5, 1, 1.5, 2` lần `r_s` của phương pháp; và thang giao tiếp `none`, `neighbour_broadcast`, `global_shared`. Với `strombom_multi`, thông tin chia sẻ là hợp các cừu được cảm nhận, không phải chân lý giả lập đặc quyền.

### RQ6: Khớp scaling

Đường cong dự kiến nào dự báo N holdout tốt nhất, và một quy luật lũy thừa duy nhất có đủ không?

So sánh các ứng viên hằng, tuyến tính, lũy thừa `A * N^alpha`, và tuyến tính hai đoạn theo đơn vị số chó. Chọn bằng RMSE leave-one-N-out. Chỉ báo cáo độ dốc log trong một miền N và bố cục được nói rõ.

### RQ7: Cảnh báo sớm

Trạng thái gần đây có dự báo thất bại sau này tốt hơn chỉ N và D không?

Tại tick 1000 đến 8000, bước 200, chỉ dùng đặc trưng từ `(t - 200, t]`. Gán nhãn thất bại trong 500 tick tiếp theo chỉ khi chân trời vẫn nằm trong T0. Huấn luyện trên các N khác. Thời gian dẫn được đo từ lần vượt ngưỡng huấn luyện đầu đến thất bại và có thể lớn hơn 500 tick.

## 6. Tiêu chí hỗ trợ claim

Kết luận là `UNEVALUATED`, `SUPPORTED`, `REJECTED`, hoặc `INCONCLUSIVE`. Một phân tích có điều kiện không thể chạy vì điều kiện kích hoạt vắng mặt được đánh dấu `SKIPPED` trong trạng thái chạy và giải thích trong bộ theo dõi. Chỉ được gán kết luận từ bằng chứng cấp CLAIM.

| Claim | RQ | Được hỗ trợ khi |
|---|---|---|
| C1a | RQ1 | Với ít nhất một N, `D_min` khác ít nhất một bước lưới D giữa các bố cục tại theta 0,90 |
| C1b | RQ1 | Mô hình trạng thái có negative log-likelihood leave-one-N-out thấp hơn mô hình `(N, D)` |
| C2a | RQ2 | Phương pháp cơ sở có `D_overcrowd` tại theta 0,90 cho ít nhất một N |
| C2b | RQ2 | Ít nhất một D trên `D_overcrowd` vẫn dưới theta tại T = 20000 |
| C3 | RQ3 | Tại N cố định, ô quá tải và hiệu quả khác nhau về `I_dir` và/hoặc phân mảnh với hạng `p < 0.05` sau hiệu chỉnh Holm |
| C4 | RQ4 | `D_min` hoặc quá tải chung trên ba phương pháp bắt buộc; dòng cấu trúc cần thêm mọi lần chạy cấu trúc |
| C5a | RQ5 | Một bước thang làm giảm `D_min` ít nhất một bước lưới D tại N trong `{100, 200}` |
| C5b | RQ5 | Bước thang thứ hai tiết kiệm ít chó hơn bước đầu |
| C6a | RQ6 | Lũy thừa có RMSE leave-one-N-out cao hơn piecewise hoặc đường cong riêng theo bố cục |
| C6b | RQ6 | Độ dốc của log `D_min` theo log N dưới 1 trong miền N và bố cục đã nêu |
| C7a | RQ7 | AUROC trạng thái holdout cao hơn cơ sở `(N, D)` holdout |
| C7b | RQ7 | Ít nhất 30 phần trăm lần thử thất bại có thời gian dẫn ít nhất 500 tick |

Những tiêu chí này chỉ hỗ trợ phát biểu trong giao thức đã thử. Chúng không hỗ trợ quy luật phổ quát, nhiệm vụ chưa thử, hiệu quả ngoài thực địa, hay chênh lệch số chó dưới một bước lưới.

## 7. Trạng thái thực thi, không phải kết quả khoa học

Mục này ghi công việc dự kiến đã chạy hay chưa. Mục này không nêu cỡ hiệu ứng, giá trị biên, hay diễn giải khoa học. [Theo dõi tiến độ](progress_tracker.md) quản lý trạng thái chạy và kết luận hiện tại. [Nhật ký chạy](../results/summary/data/run_ledger_vi.md) quản lý số đã thực thi và nguồn gốc.

Trạng thái được ghi vào ngày 2026-10-06:

| Giai đoạn | Trạng thái chạy | Ghi chú số đã thực thi |
|---|---|---|
| 0 | DONE | Giao thức đã đóng băng |
| 1 | DONE; T1 có điều kiện SKIPPED | Scout 3000 dòng; gieo lại claim 2200 dòng; T1 không chạy vì điều kiện kích hoạt chọn zero ô |
| 2 | DONE | Scout 3600 dòng; gieo lại claim 2400 dòng |
| 3 | SKIPPED | Phân tích cơ chế có điều kiện không có đối sánh quá tải đủ điều kiện |
| 4 | DONE cho chiến dịch kích thước và cấu trúc bắt buộc của Kubo và FAT | Số scout, claim, và hợp nhất chính xác nằm trong nhật ký chạy |
| 5 | TODO | Không claim chiến dịch thang thông tin đã hoàn tất |
| 6 | DONE cho gói khớp cơ sở đã dự kiến | Chỉ là trạng thái phân tích |
| 7 | TODO | Phân tích cảnh báo sớm chưa chạy |

Các từ `DONE`, `SKIPPED`, và `TODO` chỉ mô tả trạng thái thực thi. Một giai đoạn hoàn tất có thể cho claim bị từ chối hoặc không kết luận. Một giai đoạn có điều kiện bị bỏ qua nghĩa là điều kiện kích hoạt định trước vắng mặt, không nghĩa đã quan sát một kết quả khoa học tại điều kiện không chạy.

## 8. Cổng quyết định tương lai

| Cổng | Bằng chứng kiểm tra | Quyết định |
|---|---|---|
| G1 Tính nhất quán giao thức | YAML chuẩn, giao thức đã resolve, và kế hoạch | Dừng nếu giá trị đóng băng khác nhau; tạo phiên bản cho thay đổi giao thức có chủ đích |
| G2 Chất lượng scout | Hoàn tất, bản đồ độ tin cậy, và nguồn gốc | Dừng và sửa bản đồ hỏng trước khi lập kế hoạch claim |
| G3 Độ chính xác cửa sổ claim | Khoảng bootstrap của `D_min` | Nâng cửa sổ đã chọn lên 200 seed khi khoảng trải hơn một bước lưới D |
| G4 Điều kiện kích hoạt T1 | Hai D liên tiếp sau biên dưới theta | Chỉ chạy T1 trên ô quá tải đã chọn; nếu không, ghi `SKIPPED` |
| G5 Điều kiện cơ chế | Ô hiệu quả và quá tải tại cùng N | Chỉ chạy RQ3 nơi đối sánh khớp tồn tại |
| G6 Đầy đủ chuyển giao | Bản đồ kích thước và cấu trúc cho mọi phương pháp bắt buộc | Không điền claim chuyển giao cấu trúc đầy đủ trước khi mọi bản đồ tồn tại |
| G7 Mở rộng cấu trúc | Bản đồ claim cấu trúc ba kích thước | Thêm N = 300 và 400 chủ yếu nếu cả bốn bố cục vẫn ở sàn `D_min`; nếu không, mở rộng là tùy chọn |
| G8 Chiến dịch thông tin | Cơ sở ổn định và giao thức thang riêng | Chạy quan sát, tầm, và giao tiếp thành các chiến dịch phân tầng riêng |
| G9 Cảnh báo sớm | Chuỗi thời gian cấp CLAIM và cả hai lớp kết cục | Không báo cáo AUROC hoặc thời gian dẫn nếu không có dữ liệu holdout đủ điều kiện |
| G10 Vận tốc dự định E1 | Bằng chứng cấp CLAIM về đỉnh `I_dir` do tường | Giữ E1 chưa xây trừ khi nhu cầu chẩn đoán được chứng minh |
| G11 Parity bên ngoài | Giao thức khớp giữa engine và dung sai định trước | Không claim parity NetLogo định lượng trước khi đạt yêu cầu độ tin cậy |

## 9. Phạm vi và nguy cơ

| Nguy cơ hoặc giới hạn | Phản hồi trong kế hoạch |
|---|---|
| Một nhiệm vụ mô phỏng | Giới hạn kết luận trong `drive_to_goal`; nhiệm vụ thứ hai là công việc sau |
| Phụ thuộc phương pháp | Yêu cầu RQ4 trước phát biểu tổng quát cho phương pháp |
| Gây nhiễu bố cục và trạng thái | Dùng N khớp và đối sánh bố cục định trước |
| Lưới D rời rạc | Biểu diễn hiệu ứng theo bước lưới cục bộ và giữ kiểm duyệt trên lưới |
| Biên độ tin cậy mềm | Dùng seed khóa, cửa sổ claim, khoảng bootstrap, và cổng chính xác 200 seed |
| Phân tích có điều kiện | Đánh dấu công việc thiếu điều kiện kích hoạt là undefined hoặc skipped, không coi là null đo được tại điều kiện không chạy |
| Quy ước thời gian giữa phương pháp | Tránh diễn giải vật lý trực tiếp của tick thô giữa các họ bộ điều khiển |
| Công tắc thu thập Strombom rộng hơn đích | Không diễn giải thất bại của nó là thất bại xếp chặt |
| Bộ điều khiển mô phỏng | Không claim ngoài thực địa, nông trại, hay giá trị sinh học |
| Twin NetLogo và bản thảo 2025 | Coi là lớp bằng chứng riêng; theo tài liệu độ tin cậy |
| Trần lưới | Không diễn giải D = 35 là giới hạn vật lý |
| Độ chính xác chọn lọc | Giữ cấp của ô sau hợp nhất và không chồng dòng scout và claim |

Sân mặc định của ứng dụng, mô hình cừu, và luật lực chó nằm ngoài phạm vi sửa đổi của giao thức này. Giới hạn chi tiết và biên xác minh nằm trong [độ tin cậy và so sánh](credibility/README_vi.md).

## 10. Thứ tự ưu tiên nguồn và quyền sở hữu tài liệu

Khi các nguồn khác nhau, dùng thứ tự sau:

1. [`canonical_grid.yaml`](../configs/canonical_grid.yaml) định nghĩa mặc định máy đọc đóng băng của `scaling_v2`.
2. YAML đã resolve trong [`configs/protocols/`](../configs/protocols/) định nghĩa tập con của một chiến dịch.
3. `protocol.yaml`, `provenance.json`, `manifest.jsonl`, và `status.json` đã sao chép của lần chạy định nghĩa điều đã thực thi.
4. Kế hoạch này định nghĩa câu hỏi nghiên cứu, phụ thuộc, tiêu chí claim, cấp bằng chứng, ngân sách, cổng, và phạm vi.
5. [Tài liệu thiết lập](setup/README_vi.md) định nghĩa lý do tham số, bảng thuật ngữ, lớp triển khai, và tham chiếu vận hành.
6. [Hướng dẫn phương pháp](methods/README_vi.md) định nghĩa diễn giải bộ điều khiển và giới hạn riêng của phương pháp.
7. [Tài liệu độ tin cậy](credibility/README_vi.md) định nghĩa biên so sánh và xác minh.
8. [Chiến lược chạy](experiment_run_strategy.md) và [hướng dẫn chạy](setup/run_guide_vi.md) định nghĩa ý định phân tầng và lệnh.
9. [Theo dõi tiến độ](progress_tracker.md) định nghĩa trạng thái mã, chạy, và claim hiện tại.
10. [Phụ lục dữ liệu](../results/summary/data/README_vi.md) và artifact trực tiếp định nghĩa số đã thực thi và bằng chứng đã báo cáo.

Kết quả không bao giờ định nghĩa lại kế hoạch đóng băng. Nếu ước lượng kế hoạch khác artifact lần chạy, giữ ước lượng là kế hoạch và báo cáo artifact là đã thực thi. Nếu giao thức đã sao chép của lần chạy khác văn bản tổng quát, giao thức đã sao chép và nguồn gốc chi phối diễn giải lần chạy đó.
