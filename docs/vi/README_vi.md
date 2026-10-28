# HerdSim

[![Giấy phép: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../../LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Kiểm thử](https://img.shields.io/badge/tests-332%20passed-brightgreen.svg)](../../tests)
[![Lượt mô phỏng](https://img.shields.io/badge/simulated%20trials-439%2C120-success.svg)](../../results)

Một con chó chăn cừu có thể gom một bầy cừu gắn kết và lùa vào chuồng. Khi cừu xuất phát rải rác và công việc có thời hạn, một con chó không thể ở khắp nơi cùng lúc. Một nhiệm vụ như vậy cần bao nhiêu chó, và thêm chó có luôn giúp ích không?

HerdSim là một bộ mô phỏng mã nguồn mở và một nghiên cứu được xây dựng để trả lời câu hỏi đó. Nó chạy mô hình cừu của Strömbom et al. (2014) với một đội chó và đếm xem một đội $D$ chó đưa được một bầy $N$ con cừu vào đích trước thời hạn thường xuyên đến đâu. Qua 439.120 lượt mô phỏng trong 41 giao thức, không có lỗi mô phỏng nào, nó bao quát các bầy từ 25 đến 566 con (với các lượt chạy đến 3200 con), bốn bố cục xuất phát, ba thời hạn, và các biến thể của chó và cừu. Bốn con số mô tả tỷ lệ thành công và thời gian hoàn thành thay đổi thế nào theo quy mô đội:

- $D_{\min}$: đội nhỏ nhất thành công ở ít nhất 90% số lượt, với độ tin cậy 99%.
- $D_{\mathrm{sat}}$: đội mà vượt quá nó, thêm chó không còn làm việc lùa nhanh hơn.
- $D_{\max}$: đội lớn nhất vẫn còn tin cậy.
- $D_{\mathrm{overcrowd}}$: đội mà từ đó hai quy mô đội đã thử liên tiếp đều không tin cậy.

Hình 1 cho thấy một lượt chạy. Các thuật ngữ khác (bố cục xuất phát như `wide`, thời gian lùa, quy tắc nghiêm ngặt và quy tắc 99%, tên giao thức như `dmin_f99_m6`) được định nghĩa trong [bảng thuật ngữ](glossary_vi.md).

![Một lượt mô phỏng](../figures/fig17_trial.png)
**Hình 1: Một lượt chạy trong HerdSim ($N = 200$ cừu, $D = 4$ chó, xuất phát `wide`, hạt giống ngẫu nhiên 2026), ở các bước 0, 55, 139 và 279.** Chó gom bầy đang tản mác từ nhiều phía trước, rồi lùa bầy từ phía sau vào đích.

- Ký hiệu: vòng tròn xanh lá bên phải là đích ($R_{\mathrm{goal}} = 1{,}9 R_f$); tam giác cam là chó, kèm vệt đường đi; chấm xanh dương là cừu.
- Các khung: bốn bước trong lưới 2 × 2, đọc từ trái sang phải, rồi từ trên xuống dưới. Các chó xuất phát trên một cung sau bầy và khép lại trong lúc bầy gom lại.

![Một lượt chạy dạng hoạt ảnh](../gifs/one_trial.gif)

**Hoạt ảnh 1: Một lượt chạy từ đầu đến đích (xuất phát `wide`, N = 200, D = 4, hạt giống 0, quy tắc 99%, 6 lần thời gian lùa).** Chó gom các con lạc của một bầy xuất phát tản mát trước, rồi lùa cả bầy đã gom vào đích. Đây là bản chạy lại một lượt đã lưu của `dmin_f99_m6`.

- Ký hiệu: chấm xanh dương là cừu, tam giác cam là chó, và vòng tròn xanh lá là đích.

## Các phát hiện khoa học cốt lõi

[Báo cáo](d_min_report_vi.md) chứa toàn bộ phân tích, chia thành sáu phần theo chủ đề kèm các hình, và [các bảng số liệu](../report/results_tables.md) phía sau nó. Mỗi phát hiện dưới đây dẫn tới mục chứa bằng chứng của nó.

### 1. Một bầy xuất phát gần nhau cần một chó
Khi cừu xuất phát gần nhau (`compact`), một chó là tin cậy ở mọi quy mô của các lưới chính: $N = 25$ đến 400 theo cả hai quy tắc và mọi thời hạn, và 566 theo quy tắc 99% ở 12 và 6 lần thời gian lùa. Ở đó thêm chó không làm việc lùa nhanh hơn, có lẽ vì trong mô hình, một con cừu phản ứng với chó đi 1 m/s bất kể chó làm gì ([báo cáo, mục 3.1](part1_growth_vi.md#31-rq1-d_min-tăng-thế-nào-theo-n)).

### 2. Ở thời hạn thong thả, đội tăng chậm hơn nhiều so với bầy
Khi cừu xuất phát rải rác (`wide`, `split`, `outlier_rich`), chó phải đưa các con lạc về trước. Dù vậy, ở 12 lần thời gian lùa theo quy tắc 99%, $D_{\min}$ tăng với độ dốc log-log 0,27–0,38 trên `wide` và 0,28–0,38 trên `outlier_rich` (chín quy mô bầy); độ dốc 0,5 nghĩa là bầy lớn gấp bốn cần gấp đôi số chó. Có thể là do mỗi con cừu bị hút về cả bầy, nên con lạc mà chó lùa quay lại sẽ tự đi về bầy; làm yếu lực hút đó đã làm độ dốc tăng trên `wide` nhưng không tăng trên `outlier_rich` ([báo cáo, mục 3.8 và 3.11](part1_growth_vi.md#38-rq8-mức-tăng-theo-n-trên-lưới-dày-hơn-d_sat-và-hình-dạng-đường-cong)).

### 3. Một thời hạn gấp có thể tốn nhiều chó hơn một bầy lớn hơn
Theo quy tắc 99%, rút thời hạn từ 12 xuống 3 lần thời gian lùa làm $D_{\min}$ trên một bầy `wide` 400 con tăng từ 2 chó lên 5–6. Làm bầy đó lớn gấp bốn (từ $N = 100$ lên 400) ở 12 lần thời gian lùa chỉ làm nó tăng từ 1 chó lên 2 ([báo cáo, mục 3.3](part1_growth_vi.md#33-rq3-thời-hạn-làm-d_min-thay-đổi-thế-nào)).

### 4. Không phối hợp thì thêm chó không giúp được bầy lớn
Ở đối chứng FAT, mọi chó đi tới phía sau con cừu xa đích nhất, nên tất cả chọn cùng một con. Ở 6 lần thời gian lùa theo quy tắc 99%, FAT không có đội tin cậy nào khi $N \ge 200$ trên mọi bố cục phân tán, trong khi quy tắc đội cần 2 hoặc 3 chó trên `wide` và `outlier_rich`. Trên hai bố cục đó, riêng công tắc gom/lùa của Strömbom đưa được một đội đến $N = 200$; ở $N = 400$ cần thêm tầng đội phân công chó cho các con lạc ([báo cáo, mục 3.6 và 3.9](part4_coordination_vi.md#36-rq6-chó-không-có-quy-tắc-đội-có-đạt-d_min-hữu-hạn-không)).

### 5. Với đội lớn, đòi mọi con cừu vào đích chủ yếu là đo vài con cừu cuối cùng
Khi mọi con cừu phải ở trong đích cùng lúc (quy tắc nghiêm ngặt), các đội lớn (từ 6 chó) trên bầy lớn phần lớn thất bại sau khi bầy đã được gom: ở 6 lần thời gian lùa, trong 97% số lượt thất bại nghiêm ngặt với 6 chó trở lên ở lượt chạy cơ sở của phần độ nhạy, 99% bầy đã từng ở trong đích. Tính một lượt là thành công khi 99% số cừu vào đích tránh được điều này, và theo quy tắc đó (6 lần thời gian lùa, `wide` và `outlier_rich`, $N = 100$ đến 400) $D_{\min}$ lệch nhiều nhất khoảng một chó khi thiết lập thay đổi, trừ một đích nhỏ hơn ([báo cáo, mục 3.4 và 3.5](part2_success_rule_vi.md#34-rq4-quy-tắc-thành-công-và-con-cừu-cuối-cùng)).

### 6. Quá một vài chó, thêm chó tốn thời gian nhưng hiếm khi gây hại
Theo quy tắc 99% ở 6 lần thời gian lùa, chó vượt $D_{\mathrm{sat}}$ chỉ làm lượt lùa nhanh hơn nhiều nhất khoảng 4% (trên 27 đường cong có $D_{\mathrm{sat}}$ đã quyết định), trong khi thời gian chó tăng theo đội. Trong ba lượt chạy chính theo quy tắc 99%, $D_{\max}$ là đỉnh lưới, 24 chó, ở 84 trong 85 đường cong có $D_{\min}$, nên chưa tìm thấy giới hạn trên nào dưới 24 chó. Thêm chó có gây hại trong một vài lượt chạy tiếp theo, rõ nhất khi chó giữ cách nhau 2 m và phải giữ một bầy `outlier_rich` 400 con trong đích: tỷ lệ thành công giảm từ 0,87–0,94 với 3 đến 8 chó (mỗi ô 200 lượt) xuống 0,50–0,77 từ 9 chó trở lên (10 đến 70 lượt mỗi ô) ([báo cáo, mục 3.7 và 3.10](part3_beyond_dmin_vi.md#37-rq7-vượt-quá-d_min-đủ-chó-chi-phí-và-áp-lực-lên-bầy)).

### 7. Đội có chững lại với bầy rất lớn hay không vẫn còn bỏ ngỏ
Theo quy tắc 99% đến $N = 566$, một đường cong tăng mãi và một đường cong chững lại ở một đội lớn nhất khớp $D_{\min}$ trên `wide` và `outlier_rich` tốt như nhau. Mô hình này không giải quyết được câu hỏi bằng bầy lớn hơn: trên khoảng 600 con, một bán kính bầy không còn mô tả được bầy, và trên khoảng 1056 con, quy tắc lùa của Strömbom đặt chó ra ngoài tầm của cừu. Khi giới hạn điểm lùa (quy tắc 99%, 12 lần thời gian lùa, bán kính bầy đặt theo mật độ của bầy 566), một bầy `wide` cần 3 chó ở $N = 800$, 5–9 ở 1131 và hơn 12 ở 1600 ([báo cáo, mục 3.8 và 3.13](part1_growth_vi.md#38-rq8-mức-tăng-theo-n-trên-lưới-dày-hơn-d_sat-và-hình-dạng-đường-cong)).

### 8. Khi thấy mọi thứ, mục tiêu không gắn kết theo quy luật căn bậc hai, cả trong HerdSim
Lama và di Bernardo (2024) nghiên cứu các mục tiêu hoàn toàn không hút nhau. Chạy trong HerdSim, mô hình của họ cho kết quả gần với ngưỡng trong Bảng I của phần tài liệu bổ sung của bài báo cho $R = 50$ và bán kính cảm nhận 10 ($\sqrt{N} = 8$, 9 và 12 ở các mức 90%, 95% và 99%, so với 8, 9 và 11 của bài báo). Khi thấy mọi thứ, đội nhỏ nhất tăng theo căn bậc hai của số mục tiêu (số mũ 0,52–0,53, $N \ge 100$), dốc hơn các độ dốc ở phát hiện 2, dù hai bên còn khác nhau về nhiệm vụ, quy tắc người chăn, quy mô bầy và cách khớp độ dốc. Với bán kính cảm nhận 10, mức trung bình của bài báo và cách đếm từng lượt của HerdSim tách nhau ngay trên ngưỡng: ở 144 mục tiêu, mức trung bình chấp nhận 11 người chăn, nhưng 9 trong 30 lượt của họ để sót hai đến bốn mục tiêu (21 trong 30 thành công, khoảng 99% là 0,45–0,89), và $D_{\min}$ của HerdSim là khoảng 17–25 ([báo cáo, mục 3.14](part6_square_root_law_vi.md#314-rq14-mục-tiêu-không-gắn-kết-quy-luật-căn-bậc-hai-của-lama-và-di-bernardo-2024)).

## Động cơ mô phỏng HerdSim

- Mô hình cừu của Strömbom et al. (2014):
   Mỗi con cừu cân nhắc hướng cũ, lực hút về bầy, giữ khoảng cách với hàng xóm gần, chạy khỏi chó, và nhiễu. Các tác giả đã so mô hình với dữ liệu GPS của một bầy cừu và một chó thật ([Strömbom et al. 2014](https://doi.org/10.1098/rsif.2014.0719)).
- Một quy tắc đội cho nhiều chó:
   Quy tắc một chó của Strömbom mở rộng cho cả đội: các con lạc được phân cho chó bằng thuật toán Hungarian, vị trí lùa trải trên một vòng cung sau bầy theo thứ tự góc, và lực đẩy của nhiều chó lên một con cừu được chuẩn hóa về độ lớn lực đẩy của một chó.
- Nhiệm vụ định cỡ theo bầy:
   Không có tường, và quãng lùa, bán kính đích và thời hạn được tính theo bán kính bầy đã hiệu chỉnh $R_f(N)$, nên một bầy lớn không được giúp hay bị cản bởi một cánh đồng quá nhỏ.
- Lấy mẫu thích ứng:
   Sau mỗi lô 10 hạt giống, khoảng Clopper-Pearson 99% của từng ô quyết định ô đó có cần thêm hay không. Các ô rõ ràng dừng sau 10 đến 60 hạt giống; chỉ những ô gần ngưỡng mới tiếp tục, đến tối đa 200.
- Tái lập được và dừng an toàn:
   Mỗi lượt có các dòng ngẫu nhiên riêng cho vị trí xuất phát, cho cừu và cho chó, nên một lượt chạy lại chính xác từ cấu hình và hạt giống của nó trên cùng một máy. Mỗi lượt xong được ghi ngay xuống đĩa (`trials.jsonl`), nên một lượt chạy có thể dừng và chạy tiếp.
- Ba mô hình nguồn, hai nhiệm vụ:
   Ngoài bầy cừu Strömbom, HerdSim chạy mô hình lực liên tục của Kubo et al. (2022) trên cùng nhiệm vụ lùa, và mô hình mục tiêu không gắn kết cùng người chăn cảm nhận cục bộ của Lama & di Bernardo (2024) trên nhiệm vụ gom riêng (cừu và chó xuất phát rải đều trong một đĩa và chó đưa mục tiêu vào tâm). Mô hình Lama được thêm vào để kiểm tra quy luật $\sqrt{N}$ đã công bố ngay trong cùng một mô phỏng và cùng một lớp thống kê ([phát hiện 8](#8-khi-thấy-mọi-thứ-mục-tiêu-không-gắn-kết-theo-quy-luật-căn-bậc-hai-cả-trong-herdsim)).

## Bắt đầu nhanh & khả năng tái lập nghiên cứu

### Cài đặt môi trường

HerdSim cần Python 3.11+ và dùng [`uv`](https://docs.astral.sh/uv/) để quản lý gói phụ thuộc:

```bash
# Nhân bản mã nguồn từ GitHub
git clone https://github.com/lykimq/HerdSim.git
cd HerdSim

# Cài đặt môi trường phát triển và toàn bộ phụ thuộc
make install     # uv sync --extra dev

# Kiểm tra lint, kiểu và chạy 332 bài kiểm thử
make check

# Chạy 23 bài kiểm tra benchmark, sáu chiến dịch thu nhỏ trọn vẹn (khoảng 1,5 phút)
make bench
```

Để chạy lại toàn bộ các chiến dịch hoặc kiểm tra một lượt chạy lại cho đúng kết quả, xem [phụ lục về khả năng tái lập](appendix_run_record_vi.md#phụ-lục-c-khả-năng-tái-lập) và [các bảng kết quả](../report/results_tables.md).

## Vận hành chiến dịch và quy trình lệnh

Các chiến dịch được chạy từ bộ công cụ dòng lệnh trong [`cli/`](../../cli):

```bash
# 1. Xem một protocol sẽ chạy gì: các ô, hạt giống vòng đầu, phần chạy tiếp
uv run cli/campaign.py plan --protocol dmin_m6

# 2. Chạy một protocol với 16 tiến trình xử lý
uv run cli/campaign.py run --protocol dmin_m6 --workers 16

# 3. Xem tiến độ của một protocol đang chạy hoặc đã xong
uv run cli/campaign.py status --protocol dmin_m6

# 4. Chạy hàng đợi 41 protocol nghiên cứu (bỏ qua protocol đã xong, chạy tiếp protocol bị dừng)
uv run cli/run_queue.py --workers 20

# 5. Dựng các bảng kết quả Markdown từ các thư mục kết quả
uv run cli/dmin_tables.py record
uv run cli/dmin_tables.py dmin dmin_m12 dmin_m6 dmin_m3
```

Để xem chi tiết các tùy chọn tham số và kịch bản chạy replay chẩn đoán, xem tại [`docs/guides/cli_reference.md`](../guides/cli_reference.md).

## Kiến trúc mã nguồn dự án

HerdSim được chia thành các tầng chỉ import xuống dưới:

```text
HerdSim/
├── sim/                    # Mô hình: một lượt chạy, từng bước
│   ├── core/               # Trạng thái, vòng lặp bước, thế giới, bố cục xuất phát
│   ├── methods/            # Các mô hình: Strombom (2014), Kubo (2022), Lama (2024)
│   └── plugins/            # Mô hình cừu, bộ điều khiển chó, nhiệm vụ, số đo
├── services/               # Chạy: protocol, chiến dịch, hiệu chỉnh, chạy lại
│   ├── adaptive.py         # Chiến dịch thích ứng: các vòng hạt giống đến khi mọi ô được quyết định
│   ├── calibration.py      # Bán kính bầy R_f(N)
│   └── runner.py           # Chạy một lô lượt trong các tiến trình worker
├── records/                # Một lượt thành một dòng bảng; physics hash và nhận dạng code của thư mục
├── analysis/               # Quy tắc quyết định (frontier) và các bảng kết quả
├── protocols/configs/      # Các protocol (giá trị mặc định canonical + phần ghi đè)
├── cli/                    # Công cụ dòng lệnh (campaign.py, run_queue.py, dmin_tables.py)
├── docs/                   # Báo cáo, ghi chú phương pháp, hướng dẫn, hình và hoạt ảnh
├── results/                # Các thư mục kết quả (439.120 lượt chạy trong các protocol nghiên cứu)
└── tests/                  # Kiểm thử đơn vị, bất biến và hồi quy
```

## Bản đồ tài liệu

### Nghiên cứu

- Báo cáo ([`d_min_report_vi.md`](d_min_report_vi.md), [EN](../report/d_min_report.md)):
  Nghiên cứu: tóm tắt, câu hỏi, quy tắc quyết định, thảo luận và kết luận. Mục 3 của nó dẫn tới các kết quả, chia thành sáu phần theo chủ đề, và nhật ký chạy.
- Bảng kết quả ([`docs/report/results_tables.md`](../report/results_tables.md)):
  Mọi bảng đứng sau báo cáo, sinh ra từ các lượt chạy đã lưu.
- Mô hình ([`models_vi.md`](models_vi.md), [EN](../methods/models.md)):
  Mô hình cừu, quy tắc đội, phân công Hungarian, các đối chứng, và hai mô hình Kubo và Lama.
- Thiết kế nhiệm vụ ([`task_design_vi.md`](task_design_vi.md), [EN](../experiments/task_design.md)):
  Cánh đồng và đích định cỡ theo $R_f(N)$, thời hạn tính theo thời gian lùa, vì sao $N$ và $D$ dừng ở những giới hạn đã chọn, và nhiệm vụ gom.
- Bảng thuật ngữ ([`glossary_vi.md`](glossary_vi.md), [EN](../glossary.md)):
  Một định nghĩa ngắn cho mỗi thuật ngữ mà các tài liệu dùng, kèm liên kết tới chỗ giải thích đầy đủ.

### Mã nguồn

- Kiến trúc ([`docs/codes/architecture.md`](../codes/architecture.md)):
  Mã được tổ chức thế nào và cách thêm một mô hình, một bộ điều khiển hay một nhiệm vụ.
- Cấu hình ([`docs/guides/configuration.md`](../guides/configuration.md)):
  Cách các protocol kế thừa nhau, các thiết lập ở phần tiếp theo, và các thư mục kết quả.
- Tài liệu tham chiếu CLI ([`docs/guides/cli_reference.md`](../guides/cli_reference.md)):
  Lập kế hoạch và chạy chiến dịch, và các lượt chạy lại chẩn đoán.
- Công cụ dòng lệnh ([`cli/README.md`](../../cli/README.md)):
  Dùng công cụ nào cho việc gì, theo thứ tự một nghiên cứu dùng chúng.

## Tài liệu tham khảo

HerdSim cài đặt các mô hình của ba bài báo:

1. Strömbom, D., et al. (2014). *Solving the shepherding problem: heuristics for herding autonomous, interacting agents*. Journal of the Royal Society Interface, 11(100), 20140719. [DOI: 10.1098/rsif.2014.0719](https://doi.org/10.1098/rsif.2014.0719)
2. Kubo, M., Tashiro, M., Sato, H., Yamaguchi, A. (2022). *Herd guidance by multiple sheepdog agents with repulsive force*. Artificial Life and Robotics, 27, 416–427. [DOI: 10.1007/s10015-021-00726-7](https://doi.org/10.1007/s10015-021-00726-7)
3. Lama, A., & di Bernardo, M. (2024). *Shepherding and herdability in complex multiagent systems*. Physical Review Research, 6, L032012. [DOI: 10.1103/PhysRevResearch.6.L032012](https://doi.org/10.1103/PhysRevResearch.6.L032012)

Các bảng đứng sau báo cáo nằm ở [`docs/report/results_tables.md`](../report/results_tables.md), và danh sách đầy đủ các công trình được trích dẫn trong nghiên cứu nằm ở [phần tài liệu tham khảo của báo cáo](d_min_report_vi.md#tài-liệu-tham-khảo).
