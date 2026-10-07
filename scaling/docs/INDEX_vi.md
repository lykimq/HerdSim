# Mục lục tài liệu scaling

Đây là bản đồ đọc chính cho `scaling_v2`. Mỗi tài liệu có một trách nhiệm chính. Bản tiếng Anh và tiếng Việt đi theo cặp khi tài liệu dành cho người đọc.

## Bắt đầu tại đây

| Nhu cầu | Tài liệu chuẩn |
|---|---|
| Hiểu kế hoạch đã được lập | [Kế hoạch scaling chính](main_scaling_plan_vi.md) |
| Hiểu các bộ điều khiển | [Mục lục phương pháp](methods/README_vi.md) |
| Hiểu tham số và thiết lập mô phỏng | [Thiết lập và tham chiếu](setup/README_vi.md) |
| Chạy, tiếp tục, hoặc phân tích một chiến dịch | [Hướng dẫn chạy](setup/run_guide_vi.md) |
| Đọc kết quả đã hoàn thành | [Báo cáo kết quả](../results/summary/SUMMARY_REPORT_vi.md) |
| Xem bảng bằng chứng dễ đọc | [Phụ lục dữ liệu](../results/summary/data/README_vi.md) |
| So sánh với bản thảo 2025 và NetLogo | [Độ tin cậy và so sánh](credibility/README_vi.md) |
| Kiểm tra trạng thái triển khai và kết luận claim | [Theo dõi tiến độ](progress_tracker.md) |

Mục lục tiếng Anh: [INDEX.md](INDEX.md).

## Trách nhiệm của từng nhóm tài liệu

| Lĩnh vực | Chịu trách nhiệm | Không chịu trách nhiệm |
|---|---|---|
| Kế hoạch | Câu hỏi nghiên cứu, phụ thuộc, tiêu chí claim, ngân sách, cổng quyết định | Kết quả số đã thực thi |
| Phương pháp | Nền tảng đã công bố, triển khai HerdSim, thiết lập và giới hạn riêng từng phương pháp | Kết luận tổng hợp qua các giai đoạn |
| Thiết lập | Tham số, lý do, định nghĩa, phân tầng, lệnh, đầu ra, nguồn gốc | Diễn giải khoa học |
| Kết quả | Quan sát Giai đoạn 1, 2 và 4 đã hoàn thành, độ bất định, giới hạn | Lý do giao thức hay hướng dẫn phương pháp |
| Độ tin cậy | So sánh bản thảo, phạm vi NetLogo, bằng chứng xác minh, điều không claim | Kết luận ngang hàng mới giữa các nền |
| Phụ lục dữ liệu | Bảng sinh từ nguồn, nhật ký chạy, schema, liên kết bằng chứng trực tiếp | Diễn giải nhập tay |
| Theo dõi | Trạng thái triển khai, chạy, và kết luận hiện tại | Văn kể giải thích ổn định |

## Lộ trình đọc

### Đọc lần đầu

1. [Kế hoạch scaling chính](main_scaling_plan_vi.md)
2. [Thiết lập thí nghiệm](setup/experiment_setup_vi.md)
3. [Mục lục phương pháp](methods/README_vi.md)
4. [Báo cáo kết quả](../results/summary/SUMMARY_REPORT_vi.md)
5. [Độ tin cậy và so sánh](credibility/README_vi.md)

### Tái tạo hoặc đối chiếu một kết quả

1. [Hướng dẫn chạy](setup/run_guide_vi.md)
2. [Nhật ký chạy](../results/summary/data/run_ledger_vi.md)
3. [Bảng dữ liệu theo giai đoạn](../results/summary/data/README_vi.md)
4. Các tệp `protocol.yaml`, `provenance.json`, `manifest.jsonl`, `status.json`, và các artifact CSV được liên kết

### Tra một thuật ngữ hoặc giá trị

- [Bảng thuật ngữ](setup/glossary_vi.md)
- [Tham chiếu tham số](setup/parameter_reference_vi.md)
- [Thiết lập thí nghiệm và lý do](setup/experiment_setup_vi.md)

## Phương pháp

- [Strombom Collect/Drive](methods/strombom_vi.md)
- [Mô hình lực Kubo](methods/kubo_vi.md)
- [FAT](methods/fat_vi.md)

## Kết quả và bằng chứng

- [Kết quả tổng hợp qua các giai đoạn](../results/summary/SUMMARY_REPORT_vi.md)
- [Bảng Giai đoạn 1 dễ đọc](../results/summary/data/phase1_tables_vi.md)
- [Bảng Giai đoạn 2 dễ đọc](../results/summary/data/phase2_tables_vi.md)
- [Bảng Giai đoạn 4 dễ đọc](../results/summary/data/phase4_tables_vi.md)
- [Thư mục chạy Giai đoạn 1](../results/phase1/)
- [Thư mục chạy Giai đoạn 2](../results/phase2/)
- [Thư mục chạy Giai đoạn 4](../results/phase4/)

## Ghi chú hỗ trợ và lịch sử

Các tệp trong [`discuss/`](discuss/) là ghi chú thảo luận ngắn theo giai đoạn. Các tệp trong [`notes/`](notes/) lưu công việc liên quan và tài liệu tham chiếu của bản thảo 2025. Chúng vẫn là bằng chứng hữu ích, nhưng các tài liệu tập trung ở trên mới là nguồn chính được duy trì cho người đọc.

Các đường dẫn `results/summary/RESEARCH_PLAN*` cũ là trang tương thích. Chúng trỏ đến bộ tài liệu đã tổ chức lại này và không nên trở thành nguồn thứ hai cho văn bản giao thức hay kết quả.
