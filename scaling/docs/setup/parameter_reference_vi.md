# Tham chiếu tham số

Giá trị trên trang này được đóng băng bởi [`scaling/configs/canonical_grid.yaml`](../../configs/canonical_grid.yaml) hoặc là mặc định bộ điều khiển ghi trong các mô-đun cấu hình được liên kết. YAML giao thức có thể chọn tập con nhưng không được định nghĩa lại ngầm giao thức chuẩn.

## Giao thức cốt lõi

| Tham số | Giá trị đóng băng | Ý nghĩa và lý do |
|---|---|---|
| `protocol_id` | `scaling_v2` | Định danh nguồn gốc ổn định cho quy tắc đã khóa |
| `frozen_on` | `2026-09-22` | Ngày đóng băng ghi bởi YAML chuẩn |
| `task` | `drive_to_goal` | Mọi cừu phải vào đĩa đích trước hạn |
| `world_width`, `world_height` | 500, 500 | Sân vuông đủ lớn cho điểm xuất phát wide và outlier_rich |
| tâm đàn | `(250, 250)` | Tâm sân |
| `goal_center` | `(370, 250)` | Điểm đường giữa cách đàn 120 đơn vị về bên phải |
| `drive_length` | 120 | Khoảng cách nhiệm vụ tâm-đến-tâm cố định |
| `goal_radius_at_n50` | 15 | Đích quy mô ứng dụng tại N = 50 |
| bán kính đích | `15 * sqrt(N/50)` | Giữ diện tích đích trên mỗi cừu không đổi |
| `initial_spread` | 30 | Thang cơ sở dùng bởi mọi bộ sinh bố cục |
| `measurement_radius` | 5 | Bán kính liên thông cho phân mảnh |
| `reliability_theta` | 0.90 | Ngưỡng dải tin cậy chính |
| `reliability_sensitivity` | 0.50, 0.70 | Ngưỡng báo cáo thêm, không phải thanh D_min |
| `baseline_method` | `strombom_multi` | Bộ điều khiển thu thập-và-đẩy cơ sở |
| `transfer_methods` | baseline, `kubo`, `fat`, `communication_free` | Danh sách chuyển giao đầy đủ theo kế hoạch |
| `required_transfer_methods` | baseline, `kubo`, `fat` | Tập claim chuyển giao tối thiểu |
| `flock_sizes` | 5, 10, 25, 50, 75, 100, 150, 200, 300, 400 | Lưới N đóng băng |
| `shepherd_counts` | 1, 2, 3, 4, 6, 10, 15, 20, 25, 35 | Lưới D đóng băng |
| `structure_flock_sizes` | 50, 100, 200 | Giá trị N cho Giai đoạn 2 và cấu trúc chuyển giao |
| `rq5_flock_sizes` | 100, 200 | Kích thước claim thang thông tin |
| `x0_families` | compact, wide, split, outlier_rich | Nhân tố bố cục ban đầu |
| `time_limit_t0` | 10.000 | Hạn chính, khoảng 80 lần cắt thẳng 120 đơn vị ở tốc độ 1 |
| `time_limit_t1` | 20.000 | Hạn dài chỉ cho ô quá tải |
| `scout_seeds` | 30 | Độ sâu bản đồ rộng |
| `claim_grade_seeds` | 100 | Độ sâu cửa sổ claim |
| `master_seed` | 2026 | Gốc cho danh sách seed xác định dùng chung |
| `bootstrap_resamples` | 1.000 | Số lần lấy mẫu lại seed cho bất định biên |
| `predictor_window_ticks` | 100 | Cửa sổ đặc trưng trạng thái đầu, ngắn hơn một lần đẩy thẳng |
| `wasteful_effort_tolerance` | 0.20 | Thanh đường đi dư mặc định |
| `wasteful_effort_sensitivity` | 0.10, 0.30 | Thanh độ nhạy được báo cáo |

Tại R = 0,90, 30 seed có sai số chuẩn khoảng 0,055 và 100 seed khoảng 0,03. Khoảng R xấp xỉ tại 100 seed là cộng trừ 0,06. Đây là bất định của R, không trực tiếp của D_min.

## Tham số bố cục

| Tham số | Giá trị | Ý nghĩa |
|---|---:|---|
| sigma compact | 9 | `0.3 * initial_spread` |
| sigma wide | 60 | `2.0 * initial_spread` |
| số cụm split | 2 dưới N = 12, ngược lại 3 | Tránh nhóm ba quá nhỏ |
| khe split tối thiểu | 10 | `2 * measurement_radius` |
| lõi outlier | khoảng 80 phần trăm | Đàn chính |
| outlier | khoảng 20 phần trăm | Rút ngoài `r_a * N^(2/3)` |

Điểm không hợp lệ ngoài sân hoặc trong đích được rút lại.

## `strombom_multi`

| Tham số | Giá trị | Ý nghĩa |
|---|---:|---|
| `r_a` | 2 | Độ dài tương tác cừu dùng trong tính xếp và ngưỡng thu thập |
| `r_s` | 65 | Khoảng cách cừu phản ứng với người chăn; tầm cảm biến cơ sở |
| `sheep_speed` | 1.0 | Dịch chuyển cừu mỗi tick |
| `shepherd_speed` | 1.5 | Dịch chuyển người chăn mỗi tick |
| `noise_strength` | 0.3 | Độ mạnh nhiễu quá trình góc trong chuyển động cừu |
| `inertia` | 0.5 | Trọng số hướng trước trong chuyển động cừu |
| ngưỡng thu thập | `r_a * N^(2/3)` | Bán kính dùng để chuyển giữa thu thập và đẩy |

Bán kính độ phủ là `sensing_range` khi nhân tố thông tin đặt nó, nếu không là `r_s` của phương pháp. Nó không phải khoảng cách đẩy cừu-cừu.

## `kubo`

| Tham số | Giá trị | Ý nghĩa |
|---|---:|---|
| `radius` | 60 | Bán kính cảm biến cục bộ |
| `K_s1` | 10 | Hệ số đẩy cừu-cừu |
| `K_s2` | 0.5 | Hệ số căn chỉnh vận tốc cừu |
| `K_s3` | 2 | Hệ số kết dính cừu |
| `K_s4` | 5000 | Đẩy cừu khỏi chó |
| `K_f1` | 10 | Hút chó tới cừu mục tiêu |
| `K_f2` | 200 | Đẩy chó khỏi cừu mục tiêu |
| `K_f3` | 8 | Đẩy chó khỏi đích |
| `K_f4` | 3000 | Đẩy chó-chó |
| `dt` | 0.05 | Bước thời gian tích phân lực |
| `sheep_speed_max` | 5 | Kẹp tốc độ cừu |
| `dog_speed_max` | 10 | Kẹp tốc độ chó |

## `fat`

FAT dùng tham số cừu Strombom ở trên. Luật chó chọn cừu quan sát được xa chó đó nhất và lấy vị trí đứng cách `r_a` phía sau theo hướng ra xa đích. Quan sát là `global` trong Giai đoạn 1, 2, và 4.

## Thang thông tin

| Nhân tố | Giá trị | Ý nghĩa |
|---|---|---|
| `obs_mode` | `bearing_only`, `local_positions`, `global` | Nội dung quan sát tăng dần |
| `sensing_range` | 32.5, 65, 97.5, 130 | 0,5, 1, 1,5, và 2 lần `r_s` Strombom |
| `communication` | `none`, `neighbour_broadcast`, `global_shared` | Quan sát riêng, hợp láng giềng, hoặc hợp cảm nhận chia sẻ toàn cục |

Với `strombom_multi`, `global_shared` dùng hợp các cừu đã cảm nhận, không phải chân lý giả lập đặc quyền. Giao thức scout Giai đoạn 5 dùng D trong `{1, 2, 3, 4, 6, 10}` vì dải D thấp là nơi tiết kiệm một bước có thể xuất hiện.

## Trường công thức giao thức

| Trường | Ý nghĩa |
|---|---|
| `protocol_id` | Định danh resolve dưới `scaling/configs/protocols/` và đóng dấu vào đầu ra |
| `phase` | Số giai đoạn nghiên cứu |
| `grade` | Cấp bằng chứng SMOKE, SCOUT, hoặc CLAIM |
| `canonical` | Đường dẫn tới mặc định đóng băng |
| `extends` | YAML giao thức cha được kế thừa |
| `output` | Đích dưới `scaling/results/` |
| `methods` hoặc `method` | Danh sách bộ điều khiển hoặc bộ điều khiển của lần chạy nhân tố |
| `layouts` | Tập con bố cục ban đầu |
| `flock_sizes` | Tập con N |
| `shepherd_counts` | Tập con D |
| `seeds` | Số seed lần thử mỗi ô đã chọn |
| `seed_mode` | Ngữ nghĩa giai đoạn như scout hoặc claim |
| `runner` | Đường thực thi lưới hoặc nhân tố |
| `upstream_protocol` | Giao thức scout hoặc claim dùng để lập kế hoạch ô sau |
| `store_timeseries` | Có ghi lịch sử Parquet theo lần thử hay không |
| `packages` | Gói phân tích xuất sau lần chạy |
| `obs_modes`, `sensing_ranges`, `communications` | Giá trị cho một thang thông tin |

`canonical` nhập mặc định; `extends` kế thừa công thức cha đầy đủ. Trong cả hai trường hợp, `protocol.yaml` đã resolve được sao chép vào thư mục kết quả để giá trị kế thừa vẫn kiểm tra được.

## Kết quả và chỉ số trạng thái

| Đại lượng | Định nghĩa |
|---|---|
| thành công | Chỉ báo nhị phân mọi cừu vào đích trước hạn |
| `t_s` hoặc thời gian kết thúc | Tick đầu tiên đạt thành công |
| `shepherd_path` | Tổng độ dài bước Euclidean của mọi chó, theo đơn vị sân |
| đường đi mỗi chó | `shepherd_path / D` |
| độ kết dính | Trung bình khoảng cách cừu tới tâm khối đàn |
| phân mảnh | Kích thước thành phần liên thông lớn nhất chia N, bán kính 5 |
| số outlier | Cừu ngoài `r_a * N^(2/3)` |
| trải (spread) | Phương sai khoảng cách cừu tới tâm |
| extent | Căn bậc hai trung bình bình phương khoảng cách tới tâm |
| chu vi | Chu vi bao lồi |
| diện tích bao | Diện tích bao lồi |
| mật độ đàn | N chia diện tích bao; không nếu diện tích suy biến |
| tỷ lệ khung hình | Tỷ số trục chính/trục phụ PCA; một là tròn |
| `I_dir` | `1 - ||sum unit_velocity|| / M_active` cho chó nhanh hơn `1e-6` |
| độ phủ C | Tỷ lệ cừu ngoại vi (trên trung vị khoảng cách GCM) nằm trong bán kính ảnh hưởng |

Nếu không chó nào chuyển động, `I_dir = 0`. Chỉ số dùng vận tốc thực hiện, nên ràng buộc như phản xạ tường được gồm. Thiếu bán kính độ phủ cho NaN.

## Độ tin cậy, biên, và chế độ

`R(m, tau, N, D, T, X0, I)` là xác suất thành công ước lượng trên seed đã khóa cho phương pháp m, giao thức tau, kích thước đàn N, số người chăn D, hạn T, bố cục X0, và điều kiện thông tin I.

| Đại lượng | Định nghĩa |
|---|---|
| D_min | D nhỏ nhất đã thử có R ít nhất theta |
| D_overcrowd | D đầu sau D_min mà D đó và D lưới kế tiếp đều dưới theta |
| D_max | D tin cậy lớn nhất dưới D_overcrowd; khi không có quá tải, D tin cậy lớn nhất đã thử, có thể chỉ là trần lưới |
| B* | `(D, T)` tin cậy có trung vị đường đi nhỏ nhất; hòa thì D nhỏ hơn, rồi thời gian kết thúc trung vị nhanh hơn |
| thất bại cứng | Không D đã thử nào đạt theta; giá trị biên để trống |
| thất bại thiếu nguồn lực | R dưới theta trước D_overcrowd |
| vận hành hiệu quả | R ít nhất theta và đường đi dưới thanh lãng phí |
| chi tiêu lãng phí | Tin cậy nhưng trung vị đường đi cao hơn B* ít nhất 20 phần trăm; cũng báo cáo 10 và 30 phần trăm |
| sụp đổ quá tải | R dưới theta tại hoặc sau D_overcrowd |

Hiệu ứng biên đo bằng bước cục bộ của lưới D. D_max bằng 35 với D_overcrowd trống nghĩa là chưa quan sát sụp đổ tới trần đã thử. Nó không nghĩa sụp đổ bắt đầu tại 35.

Bootstrap lấy mẫu lại seed trong mỗi D 1.000 lần. Lần lấy mẫu không có D_min vẫn bị kiểm duyệt phải trên D lớn nhất đã thử. Phân vị 2,5 và 97,5 là giá trị lưới hoặc `above grid`.

## Dự báo và cảnh báo sớm

RQ7 dùng chân trời `k = 500`, cửa sổ đặc trưng `w = 200`, và tick đánh giá từ 1.000 đến 8.000 bước 200. Đặc trưng chỉ dùng `(t - 200, t]`; nhãn là thất bại trong 500 tick tiếp theo, chỉ khi chân trời còn trong T0. Đánh giá bắt đầu sau tạm thời bố cục ban đầu và kết thúc đủ sớm để giữ chân trời.

Mô hình trạng thái và N,D giữ nguyên cả giá trị N khi holdout. Ứng viên khớp scaling là hằng, tuyến tính, lũy thừa `A * N^alpha`, và tuyến tính hai đoạn. Chọn bằng RMSE leave-one-N-out.
