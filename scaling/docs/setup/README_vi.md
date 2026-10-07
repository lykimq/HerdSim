# Thiết lập và tham chiếu scaling

Thư mục này là tài liệu vận hành cho giao thức `scaling_v2`. Tài liệu giải thích thiết lập đóng băng, tham số, thuật ngữ, và lệnh chiến dịch mà không thay đổi kế hoạch nghiên cứu.

## Thứ tự đọc

1. [Thiết lập thí nghiệm](experiment_setup_vi.md): nhiệm vụ, sân, bố cục, phân tầng, lý do, lớp triển khai, và giới hạn nghiên cứu.
2. [Tham chiếu tham số](parameter_reference_vi.md): giá trị đóng băng, mặc định bộ điều khiển, chỉ số, biên, và phân tích.
3. [Hướng dẫn chạy](run_guide_vi.md): kiểm tra, chạy, tiếp tục, lập kế hoạch, gieo lại, T1, phân tích, đầu ra, và nguồn gốc.
4. [Bảng thuật ngữ](glossary_vi.md): ký hiệu và định nghĩa vận hành.

Bản tiếng Anh:

- [Experiment setup](experiment_setup.md)
- [Parameter reference](parameter_reference.md)
- [Run guide](run_guide.md)
- [Glossary](glossary.md)

## Thứ tự ưu tiên nguồn

Khi các nguồn khác nhau, dùng thứ tự sau:

1. [`scaling/configs/canonical_grid.yaml`](../../configs/canonical_grid.yaml) là nguồn có thẩm quyền cho mặc định máy đọc đóng băng của `scaling_v2`.
2. YAML đã resolve trong [`scaling/configs/protocols/`](../../configs/protocols/) định nghĩa một chiến dịch cụ thể và có thể thu hẹp lưới chuẩn.
3. Tệp `protocol.yaml` đã sao chép trong thư mục kết quả ghi đúng công thức đã dùng cho lần chạy đó.
4. [`scaling/docs/main_scaling_plan.md`](../main_scaling_plan.md) định nghĩa câu hỏi nghiên cứu, phụ thuộc, quy tắc biên và chế độ, tiêu chí claim, ngân sách, và cổng quyết định.
5. [`scaling/docs/experiment_run_strategy.md`](../experiment_run_strategy.md) định nghĩa phân tầng và ý định vận hành.
6. [`scaling/Makefile`](../../Makefile) và `uv run scaling/scripts/campaign.py help` định nghĩa cách nối lệnh hiện tại.
7. [`scaling/results/README.md`](../../results/README.md) và các báo cáo tổng hợp mô tả artifact đã sinh và trạng thái chạy thực tế. Kết quả không bao giờ định nghĩa lại giao thức đóng băng.

Bảng tham số và định nghĩa đại lượng mô phỏng trước đây nằm trong Phụ lục A và B của Báo cáo tổng hợp hiện được duy trì tại [tham chiếu tham số](parameter_reference_vi.md) và [bảng thuật ngữ](glossary_vi.md).

Nếu giao thức đã sao chép và tài liệu kế hoạch khác nhau về một lần chạy đã hoàn thành, dùng giao thức đã sao chép cùng `provenance.json`, `manifest.jsonl`, và `status.json` của lần chạy đó. Không sửa ngầm một giá trị đóng băng. Đổi giao thức đòi hỏi cập nhật lý do chuẩn và kế hoạch chính, và thông thường là một định danh giao thức mới.

## Sơ đồ

Bộ đầy đủ cũng được nhúng theo ngữ cảnh trong [thiết lập thí nghiệm](experiment_setup_vi.md). Thư viện dưới đây giữ mọi sơ đồ setup ở một chỗ.

![Tổng quan sân](../../results/summary/figures/schematics/vi/arena_overview.svg)

![Sân với bố cục compact](../../results/summary/figures/schematics/vi/arena_compact.svg)

![Quy tắc bán kính đích](../../results/summary/figures/schematics/vi/goal_radius.svg)

![Sân, quãng lùa, hạn thời gian](../../results/summary/figures/schematics/vi/design_timeout.svg)

![Lưới N và D](../../results/summary/figures/schematics/vi/design_nd_grids.svg)

![Theta định nghĩa D_min](../../results/summary/figures/schematics/vi/design_theta.svg)

![Bốn bố cục](../../results/summary/figures/schematics/vi/four_layouts.svg)

![strombom_multi](../../results/summary/figures/schematics/vi/alg_strombom_multi.svg)

![Kubo](../../results/summary/figures/schematics/vi/alg_kubo.svg)

![FAT](../../results/summary/figures/schematics/vi/alg_fat.svg)

![Ý nghĩa xa nhất theo bộ điều khiển](../../results/summary/figures/schematics/vi/alg_farthest_compare.svg)

![Ví dụ lãng phí / D_max / D_overcrowd](../../results/summary/figures/schematics/vi/overcrowd_example.svg)

![Nhãn biên](../../results/summary/figures/schematics/vi/design_frontier.svg)

![Các chế độ](../../results/summary/figures/schematics/vi/regimes.svg)

![Nhãn thất bại](../../results/summary/figures/schematics/vi/design_failures.svg)

![Đường ống phân tầng](../../results/summary/figures/schematics/vi/pipeline.svg)

![Một ô và các seed](../../results/summary/figures/schematics/vi/one_cell_seeds.svg)

![Lưới khảo sát](../../results/summary/figures/schematics/vi/scout_grid.svg)

![Cửa sổ claim](../../results/summary/figures/schematics/vi/claim_window.svg)

![Ý tưởng bootstrap](../../results/summary/figures/schematics/vi/design_bootstrap.svg)

![Lộ trình giai đoạn](../../results/summary/figures/schematics/vi/phase_roadmap.svg)

## Phạm vi

Các trang này chỉ mô tả thiết lập và vận hành. Kết luận claim vẫn nằm trong bộ theo dõi và báo cáo cấp CLAIM. Thiết lập hỗ trợ kết luận trong mô phỏng, nhiệm vụ, lưới đã thử, và độ phân giải tick rời rạc này. Nó không thiết lập quy luật phổ quát cho nhiệm vụ khác hay nông trại thật, và không phân giải được chênh lệch số chó nhỏ hơn một bước cục bộ của lưới.
