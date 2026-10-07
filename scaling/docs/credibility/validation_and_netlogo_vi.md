# Xác thực, NetLogo, và ranh giới kết luận

## Tách các lớp

**Nền tảng NetLogo.** NetLogo là môi trường mô phỏng dựa trên tác tử chung. Việc dùng NetLogo không tự động xác thực một mô hình cụ thể hoặc kết quả HerdSim.

**Twin đi kèm.** `integrations/netlogo/twins.json` đăng ký các mô hình `.nlogo` desktop đối ứng cho một số phương pháp. Giao diện HerdSim có thể liệt kê và mở chúng. Chúng phục vụ quan sát hành vi với cấu hình gần nhau.

**Bản thảo 2025.** Bản thảo dùng NetLogo, nhưng mô hình gom, giữ, và qua cổng không phải twin đi kèm. Nó không được chạy lại.

**Chồng kết luận HerdSim.** Kết luận scaling hiện tại đến từ giao thức Python `scaling_v2`, lưới đóng băng, các tầng seed, hợp nhất claim, bootstrap, provenance, và CSV xuất. Chúng không đến từ twin NetLogo.

![NetLogo và HerdSim có vai trò khác nhau.](../../results/summary/figures/schematics/vi/netlogo_vs_herdsim.svg)

## Danh bạ twin và cách dùng cho kết luận

Danh bạ hiện có năm mô hình đối ứng:

| Phương pháp HerdSim | Mô hình trong danh bạ | Mức claim trong báo cáo scaling | Ranh giới |
|---|---|---|---|
| `strombom` | `strombom.nlogo` | Không có gói claim scaling trực tiếp | Có mô hình đối ứng; không có điểm parity |
| `strombom_noise` | `strombom_noise.nlogo` | Không | Có mô hình đối ứng; không có điểm parity |
| `strombom_multi` | `strombom_multi.nlogo` | Có, Giai đoạn HerdSim 1 và 2 | Bằng chứng claim là dữ liệu Python, không phải twin |
| `kubo` | `kubo.nlogo` | Có, Giai đoạn HerdSim 4 | Bằng chứng claim là dữ liệu Python; quy ước thời gian khác giữa các họ |
| `flocking_dog` | `flocking_dog.nlogo` | Không có gói claim scaling hiện tại | Có mô hình đối ứng; không có điểm parity |
| `fat` | không có | Có, Giai đoạn HerdSim 4 | Chỉ HerdSim trong đối chiếu này |

Mô hình bản thảo 2025 không có trong danh bạ.

## Twin hỗ trợ điều gì

Hướng dẫn NetLogo mô tả các mô hình đối ứng với hành vi chăn đạt gần nhau cho Drive to Goal, các thiết lập có thể ghép bằng tay, chỉ số trực tiếp, và quan sát. Điều này hỗ trợ kiểm tra định tính như phương pháp có gom, lùa, dàn chó ra, dừng, hoặc làm đàn tách theo cách rộng tương tự hay không.

Quãng đường và tick hoàn thành chính xác không dự kiến khớp vì Python và NetLogo dùng bộ sinh ngẫu nhiên khác và có thể cập nhật tác tử theo thứ tự khác. Kubo đặc biệt nhạy với khác biệt tích phân rời rạc. Cùng giá trị seed không tạo cùng chuỗi ngẫu nhiên.

Vì vậy, twin hỗ trợ kiểm tra hành vi. Sự tồn tại của twin không tự động hỗ trợ tương đương số học.

## Kiểm thử chứng minh điều gì

| Khu vực kiểm thử | Điều được kiểm | Điều không được kiểm |
|---|---|---|
| API twin | Năm phương pháp và tên tệp mô hình dự kiến được trả về | Hành vi mô hình hoặc parity hai động cơ |
| API thư viện mô hình | Có thể liệt kê mô hình đi kèm; upload bị giới hạn | Giá trị khoa học |
| API mở desktop | Launcher NetLogo nhận đường dẫn mô hình | Một lần chạy khoa học thành công |
| Hỗ trợ đường dẫn | Đường dẫn mô hình được giải; có thể phát hiện NetLogo cục bộ | Quỹ đạo khớp |
| Tính xác định HerdSim | Lặp lại cấu hình và seed HerdSim có thể khớp | Ngẫu nhiên NetLogo khớp |
| Kiểm thử bộ điều khiển và chỉ số | Một số công thức, cấu hình, và bất biến chạy như mã | Đồng ý với triển khai ngoài trên một lưới nghiên cứu |
| Kiểm thử scaling | Trường giao thức và hàm phân tích theo quy tắc dự kiến | Kết quả bản thảo bên ngoài đúng |

Tệp liên quan:

- [Danh bạ twin](../../../integrations/netlogo/twins.json)
- [Kiểm thử API NetLogo](../../../tests/backend/api/test_netlogo_api.py)
- [Kiểm thử cầu nối NetLogo](../../../tests/backend/test_netlogo.py)
- [Kiểm thử đúng đắn HerdSim](../../../tests/backend/correctness/)
- [Kiểm thử đường chạy tốt HerdSim](../../../tests/backend/goodpath/)

## Bằng chứng kết luận HerdSim

Bằng chứng mạnh nhất hiện tại là khả năng lặp lại nội bộ theo giao thức đóng băng:

1. `scaling_v2` khóa nhiệm vụ, thế giới, lưới N và D, bố cục, theta, hạn, phương pháp, và seed gốc.
2. Scout lập bản đồ lưới với 30 seed mỗi ô và chỉ dùng để lập kế hoạch.
3. Claim gieo lại các cửa sổ biên đã chọn, thường với 100 seed.
4. Phân tích dùng hàng claim nơi có, và hàng scout ở nơi khác.
5. Bất định D_min được ước lượng với 1,000 bootstrap seed.
6. CSV, tệp trạng thái, ảnh chụp giao thức, và provenance vẫn có thể kiểm tra.

Đây là bằng chứng mức claim cho nhiệm vụ HerdSim mô phỏng và phạm vi đã thử. Nó không phải xác thực ngoài thực địa, tái lập bên ngoài, hoặc xác thực hai động cơ.

![Đường ống claim theo tầng.](../../results/summary/figures/schematics/vi/pipeline.svg)

![Một ô tin cậy gồm các seed độc lập.](../../results/summary/figures/schematics/vi/one_cell_seeds.svg)

## Bảng kết luận và không kết luận

| Phát biểu được hỗ trợ | Phát biểu mạnh hơn không được hỗ trợ |
|---|---|
| HerdSim tái sử dụng ý tưởng bộ điều khiển dựa trên bài báo | HerdSim tái hiện mọi giao thức bài báo đã trích |
| Một số phương pháp có mô hình NetLogo đối ứng | Mọi phương pháp HerdSim có twin NetLogo |
| Twin cho phép kiểm tra trực quan và theo chỉ số | Twin tương đương định lượng với HerdSim |
| Lần chạy HerdSim đóng băng hỗ trợ kết quả scaling hiện tại | NetLogo đã tái lập độc lập kết quả đó |
| Kết quả hiện tại bao phủ một nhiệm vụ mô phỏng, lưới đã thử, và theta = 0.90 | Kết quả lập một quy luật scaling nông trại hoặc sinh học phổ quát |
| D_max = 35 là trần lưới khi chưa thấy sụp | 35 là giới hạn vật lý phía trên đã đo |
| FAT không đạt theta trong các ô HerdSim đã nêu | FAT không thể chăn đàn lớn nói chung |
| Kết quả bản thảo khác kết quả HerdSim | Bản thảo đã bị bác bỏ |

![Các lớp kết luận và không kết luận.](../../results/summary/figures/schematics/vi/trust_herdsim.svg)

## Bằng chứng parity còn thiếu

Chưa có hiện vật nào trong kho cung cấp đầy đủ:

- Giao thức Python và NetLogo ghép cặp, đóng băng cho mỗi twin
- Ánh xạ tài liệu hóa cho mọi tham số, quy tắc khởi tạo, thứ tự cập nhật, và quy tắc biên
- Lần chạy hai động cơ trên cùng lưới điều kiện
- Chiến lược seed xử lý hai bộ sinh ngẫu nhiên khác nhau
- Chỉ số parity và dung sai được khai báo trước
- Đối chiếu phân phối với bất định trên nhiều lần chạy
- Bảng kết quả parity có phiên bản và provenance
- Quyết định đạt hoặc không đạt cho mỗi twin

Khi thiếu các mục này, không nên báo cáo điểm parity định lượng. Một nghiên cứu parity tương lai nên đối chiếu phân phối thay vì quỹ đạo từng tick, với các kết quả như xác suất thành công, phân phối thời gian hoàn thành theo đơn vị thời gian tương thích, khoảng cách đích cuối, cohesion, fragmentation, và bất biến định tính theo bộ điều khiển.

## Hướng dẫn đối chiếu

Compare trực tiếp là bằng chứng thăm dò cho một cặp HerdSim ghép điều kiện. Experiments cung cấp bằng chứng HerdSim nhiều seed và tệp xuất. NetLogo chạy trong ứng dụng desktop riêng. Không nên trộn ba quy trình mà không có giao thức khai báo trước.

Khi đối chiếu phương pháp HerdSim, khóa scenario, số cừu, số chó, quy tắc thành công, ngân sách thời gian, và danh sách seed. Paper preset trả lời câu hỏi khác vì phương pháp có thể có số tác tử mặc định khác. Shepherd path và số tick cũng cần thận trọng giữa Kubo và họ Strombom vì quy ước tích phân khác.

## Trích dẫn

- D. Strombom et al. "Solving the shepherding problem: heuristics for herding autonomous, interacting agents." *Journal of the Royal Society Interface* 11(100):20140719, 2014. DOI: `10.1098/rsif.2014.0719`.
- M. Kubo et al. "Herd guidance by multiple sheepdog agents with repulsive force." *Artificial Life and Robotics* 27:416-427, 2022. DOI: `10.1007/s10015-021-00726-7`.
- V. Jadhav et al. "Collective responses of flocking sheep (Ovis aries) to a herding dog (border collie)." *Communications Biology*, 2024. DOI: `10.1038/s42003-024-07245-8`.
- Z. Li et al. "Communication-free shepherding navigation with multiple steering agents." *Frontiers in Control Engineering* 4, 2023. DOI: `10.3389/fcteg.2023.989232`.
- Bản thảo 2025: [PDF trong kho](../../../docs/papers/sheep-scaling_paper2025.pdf). Khi trích dẫn phải giữ trạng thái bản thảo và đồng tác giả tạm.

Nguồn thêm: [nghiên cứu liên quan](../notes/related_work.md), [hướng dẫn NetLogo](../../../platform/docs/guide/netlogo.md), [hướng dẫn Compare](../../../platform/docs/guide/compare.md), [hướng dẫn Experiments](../../../platform/docs/guide/experiments.md), và [đối chiếu bản thảo](draft_comparison_vi.md).
