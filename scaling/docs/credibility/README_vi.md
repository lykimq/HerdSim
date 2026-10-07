# Độ tin cậy và đối chiếu

Thư mục này tách bốn đối tượng không được xem là tương đương:

1. **Bản thảo 2025** là một nghiên cứu NetLogo đang bản thảo, với nhiệm vụ gom, giữ, và đưa đàn qua cổng.
2. **NetLogo** là một nền tảng mô phỏng dựa trên tác tử chung.
3. Các **twin NetLogo** đi kèm là mô hình desktop đối ứng cho một số phương pháp HerdSim.
4. **Chồng kết luận HerdSim** gồm giao thức `scaling_v2` đóng băng, các tầng chạy, bootstrap, và dữ liệu xuất dùng cho kết luận hiện tại.

Mô hình của bản thảo không phải twin. Nó không được chạy lại trong kho này. Một mục twin chỉ cho biết có mô hình đối ứng có thể mở. Nó không chứng minh parity định lượng với HerdSim.

## Tài liệu

- [Đối chiếu bản thảo](draft_comparison_vi.md): đối chiếu giao thức và kết quả giữa bản thảo 2025 và HerdSim.
- [Xác thực, NetLogo, và ranh giới kết luận](validation_and_netlogo_vi.md): mức độ bằng chứng, phạm vi twin, kiểm thử, và parity còn thiếu.
- [Bản tiếng Anh](README.md)

## Mức độ bằng chứng

| Mức | Bằng chứng hiện có | Cách đọc cho phép |
|---|---|---|
| Mức kết luận | Giao thức đóng băng, seed tầng claim, CSV hợp nhất, bootstrap, và provenance | Hỗ trợ kết quả HerdSim đã nêu trong nhiệm vụ và lưới đã thử |
| Bằng chứng triển khai | Kiểm thử tính xác định, công thức, cấu hình, API, đường dẫn, và launcher | Hỗ trợ hành vi mã nguồn và công cụ |
| Kiểm tra hành vi | Có thể cấu hình và quan sát một twin NetLogo | Chỉ hỗ trợ đối chiếu định tính |
| Kết quả bên ngoài được báo cáo | PDF bản thảo và ghi chú trong kho tóm tắt nghiên cứu khác | Có thể trích là kết quả bản thảo, không phải bằng chứng chạy lại |
| Còn thiếu | Bảng thử nghiệm ghép cặp hai động cơ và tiêu chí parity định lượng | Không có kết luận parity số học NetLogo với HerdSim |

![Nhiệm vụ bản thảo 2025 và HerdSim khác nhau.](../../results/summary/figures/schematics/vi/draft_vs_herdsim.svg)

![NetLogo là nền tảng, HerdSim là chồng thí nghiệm.](../../results/summary/figures/schematics/vi/netlogo_vs_herdsim.svg)

![Bốn lớp lập luận tin cậy của HerdSim.](../../results/summary/figures/schematics/vi/trust_herdsim.svg)

## Ranh giới ngắn

HerdSim có thể kết luận về kết quả mô phỏng lặp lại được theo giao thức đóng băng và mô tả ý tưởng bộ điều khiển dựa trên bài báo. HerdSim không thể kết luận tương đương NetLogo theo từng tick, parity twin định lượng đã công bố, twin NetLogo cho `fat`, hoặc bản thảo 2025 đã được chạy lại.

## Nguồn

- [Báo cáo kết quả tiếng Anh](../../results/summary/SUMMARY_REPORT.md), cho so sánh thực nghiệm
- [Báo cáo kết quả tiếng Việt](../../results/summary/SUMMARY_REPORT_vi.md), cho so sánh thực nghiệm
- [Ghi chú bản thảo 2025](../notes/sheep-scaling_paper2025.md)
- [Ghi chú nghiên cứu liên quan](../notes/related_work.md)
- [Danh bạ twin NetLogo](../../../integrations/netlogo/twins.json)
- [Hướng dẫn NetLogo](../../../platform/docs/guide/netlogo.md)
- [Hướng dẫn Compare](../../../platform/docs/guide/compare.md)
- [Hướng dẫn Experiments](../../../platform/docs/guide/experiments.md)
- [Kiểm thử API NetLogo](../../../tests/backend/api/test_netlogo_api.py)
- [Kiểm thử cầu nối NetLogo](../../../tests/backend/test_netlogo.py)
