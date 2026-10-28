# Quy mô đội để lùa một bầy cừu mô phỏng: tối thiểu, đủ và quá nhiều chó

Báo cáo nghiên cứu HerdSim  
41 giao thức và 439.120 lượt chạy, không có lỗi mô phỏng nào: 23 giao thức của nghiên cứu đầu (164.740 lượt), 16 giao thức tiếp theo và ba lượt chạy tiếp (234.100 lượt), và hai giao thức của mô hình mục tiêu không gắn kết của Lama và di Bernardo (2024) (40.280 lượt).  
Các mô hình và quy tắc đội được mô tả ở [docs/methods/models_vi.md](models_vi.md), hình học nhiệm vụ và cách lấy mẫu ở [docs/experiments/task_design_vi.md](task_design_vi.md). Báo cáo này trình bày kết quả, trong các phần liệt kê ở [mục 3](#3-kết-quả). Các thuật ngữ như tên bố cục, thời gian lùa, ô, khoảng, $D_{\min}$, $D_{\mathrm{sat}}$, chó dạng điểm và tên giao thức được định nghĩa trong [bảng thuật ngữ](glossary_vi.md).

## Tóm tắt

Cần bao nhiêu chó ($D$) để gom một bầy $N$ con cừu và lùa vào đích trước thời hạn? Chúng tôi hỏi ba điều: ít nhất là bao nhiêu ($D_{\min}$), bao nhiêu là đủ trước khi thêm chó không còn giúp gì ($D_{\mathrm{sat}}$), và khi nào thêm chó lại làm tệ đi. $D_{\min}$ là đội nhỏ nhất có tỷ lệ thành công ít nhất 0,90 với độ tin cậy 99% (khoảng Clopper–Pearson chính xác). Một bộ chạy thích ứng chỉ thêm lượt chạy cho những ô chưa có câu trả lời, tối đa 200 lượt mỗi ô.

23 giao thức đầu bao phủ các quy mô bầy $N = 25$ đến 400, bốn bố cục xuất phát (`compact`, `wide`, `split`, `outlier_rich`) và ba thời hạn (12, 6 và 3 lần thời gian lùa, tức thời gian một con cừu đi thẳng với 1 m/s cần để hết quãng đường lùa), mỗi thứ dưới hai quy tắc thành công: mọi con cừu vào đích (nghiêm ngặt) và 99% số cừu vào đích. Các giao thức tiếp theo chỉ dùng quy tắc 99%. Chúng thêm $D_{\mathrm{sat}}$, bốn quy mô bầy nữa đến $N = 566$, các quy tắc đội khác, giữ bầy trong đích, chó chiếm chỗ, độ gắn kết, tầm cảm nhận giới hạn, và bầy đến $N = 3200$. Hai giao thức cuối chạy mô hình mục tiêu không gắn kết của Lama và di Bernardo (2024) trên nhiệm vụ của chính họ.

Kết quả chính:

1. Bầy tập trung cần một chó: $D_{\min} = 1$ ở mọi quy mô bầy đến 566 và mọi thời hạn, và đến 566 thêm chó không rút ngắn thời gian lùa. Với điểm lùa bị giới hạn, một chó vẫn đủ ở $N = 1131$ nhưng cần khoảng 2,8 lần thời gian của hai chó, và $N = 1600$ cần hai chó ([mục 3.13](part1_growth_vi.md#313-rq13-bầy-rất-lớn-và-một-giới-hạn-của-quy-tắc-lùa)).
2. Bầy phân tán chỉ cần thêm vài chó: $D_{\min} = 1$ đến $N = 50$ và chỉ 2 hoặc 3 chó ở $N = 400$ với thời hạn thong thả. Trên thang log-log, độ dốc tăng là 0,20–0,42 ở 12 lần thời gian lùa và 0,30–0,79 ở 6 lần (cả hai quy tắc, năm quy mô bầy; 0,27–0,38 và 0,38–0,61 trên chín quy mô, mục 8).
3. Thời hạn quan trọng hơn quy mô bầy: rút từ 12 xuống 3 lần thời gian lùa làm $D_{\min}$ trên `wide` $N = 400$ tăng từ 2 lên 5–6, nhiều hơn khi đi từ $N = 100$ lên 400.
4. Dưới quy tắc nghiêm ngặt, con cừu cuối cùng quyết định: trong 97% số lượt thất bại nghiêm ngặt với 6 chó trở lên (lượt chạy cơ sở của phần độ nhạy), 99% bầy đã từng ở trong đích. Với chó chậm hơn (1,15 m/s thay vì 1,5), $D_{\min}$ nghiêm ngặt trên `outlier_rich` $N = 400$ giảm từ không có trên lưới xuống 6.
5. Quy tắc 99% ổn định trước các lựa chọn thiết lập: dưới quy tắc này, $D_{\min}$ thay đổi nhiều nhất khoảng một chó khi đổi vị trí thả chó, khoảng cách xuất phát, tốc độ chó hay tham số cừu; chỉ đích nhỏ hơn làm nó tăng nhiều hơn. Dưới quy tắc nghiêm ngặt, cùng những thay đổi đó làm nó thay đổi nhiều, theo cả hai chiều.
6. Chó không có quy tắc đội thì không mở rộng được: với FAT, mọi chó đuổi cùng một con cừu, nên không đội nào tin cậy ở $N \ge 200$ trên bất kỳ bố cục phân tán nào, kể cả bầy tập trung $N = 400$.
7. Vượt $D_{\mathrm{sat}}$, thêm chó tốn kém nhưng không gây hại ([mục 3.7](part3_beyond_dmin_vi.md#37-rq7-vượt-quá-d_min-đủ-chó-chi-phí-và-áp-lực-lên-bầy)): trên các đường cong có $D_{\mathrm{sat}}$ đã quyết định, thời gian hoàn thành ở mức 0,96–1,01 lần thời gian tại $D_{\mathrm{sat}}$, trong khi thời gian chó tăng theo $D$, và thời gian mỗi con cừu chạy trốn hầu như không tăng. Dưới quy tắc 99%, không đường cong nào đã đạt một đội tin cậy lại mất nó ở các đội lớn hơn trên năm quy mô ban đầu (một chỗ trũng trên lưới dày hơn); thêm chó chủ yếu làm chậm bầy `split` và `outlier_rich` ở $N = 566$. Trong ba lượt chạy chính theo quy tắc 99%, $D_{\max}$, đội tin cậy lớn nhất, là đỉnh lưới ở 84 trong 85 đường cong có $D_{\min}$: chưa tìm thấy giới hạn trên nào dưới 24 chó.
8. Lưới dày hơn ([mục 3.8](part1_growth_vi.md#38-rq8-mức-tăng-theo-n-trên-lưới-dày-hơn-d_sat-và-hình-dạng-đường-cong)): trên chín quy mô bầy, $D_{\min}$ tăng với độ dốc 0,27–0,38 ở 12 lần thời gian lùa và 0,38–0,61 ở 6 lần, còn $D_{\mathrm{sat}}$ tăng nhanh gấp khoảng 1,6 lần (1,15 đến 2,4 lần theo hai đầu khoảng). Đến $N = 566$, một luật lũy thừa và một đường cong chững lại khớp dữ liệu như nhau.
9. Phần nào của quy tắc đội quan trọng ([mục 3.9](part4_coordination_vi.md#39-rq9-phần-nào-của-quy-tắc-đội-quan-trọng)): riêng công tắc gom/lùa của Strömbom đã đưa một đội chó độc lập đến $N = 200$; ở $N = 400$ cần đến tầng đội.
10. Quá nhiều chó ([mục 3.10](part3_beyond_dmin_vi.md#310-rq10-khi-nào-thêm-chó-gây-hại-giữ-bầy-và-chó-chiếm-chỗ)): khi chó giữ cách nhau 2 m, `outlier_rich` $N = 400$ thất bại từ $D = 9$ trở lên; chó dạng điểm ở đó còn chưa quyết định ở mức 0,85–0,92, chưa bao giờ bị kết luận không tin cậy. Khi phải giữ 99% bầy, giữ bầy thất bại với bầy 25 và 50 con ở đích mặc định: bầy đi thêm khoảng 15 đến 17 m trong lúc chó lùi ra, và đó có lẽ là nguyên nhân. Một đích khoảng 16 đến 19 m giữ được chúng với một chó, cho một hai con ở ngoài làm giảm con số đó, và gần ngưỡng này thêm chó làm việc giữ bầy thất bại.
11. Độ gắn kết và tầm cảm nhận (mục [3.11](part6_square_root_law_vi.md#311-rq11-độ-gắn-kết-và-mức-tăng-của-d_min), [3.12](part4_coordination_vi.md#312-rq12-chó-thấy-gì-và-chia-sẻ-điều-đó)): trên `wide`, gắn kết yếu hơn làm $D_{\min}$ tăng nhanh hơn, về phía 0,5 của mục tiêu không gắn kết; trên `wide` $N = 200$ tầm nhìn cục bộ tốn khoảng một chó, và ở 65 m chia sẻ những gì mọi chó thấy đưa $D_{\min}$ về bằng khi thấy mọi thứ, còn trên `split` $N = 200$ tầm nhìn cục bộ 30 đến 65 m tốt hơn thấy mọi thứ.
12. Một giới hạn của quy tắc lùa ([mục 3.13](part1_growth_vi.md#313-rq13-bầy-rất-lớn-và-một-giới-hạn-của-quy-tắc-lùa)): trên $N \approx 1056$, điểm lùa của Strömbom nằm ngoài khoảng cách mà cừu phản ứng với chó, và ở $N = 1131$ không đội nào đến 12 chó thành công. Khi giới hạn điểm lùa trong tầm, một bầy phân tán cần 3 chó ở $N = 800$, 5–9 ở 1131 và hơn 12 ở 1600.
13. Mục tiêu không gắn kết ([mục 3.14](part6_square_root_law_vi.md#314-rq14-mục-tiêu-không-gắn-kết-quy-luật-căn-bậc-hai-của-lama-và-di-bernardo-2024)): HerdSim cho kết quả gần với ngưỡng mà Lama và di Bernardo công bố cho $R = 50$ và bán kính cảm nhận 10 trong Bảng I của phần tài liệu bổ sung của họ ($\sqrt{N} = 8$, 9 và 12 so với 8, 9 và 11 của họ), và khi đặt cạnh nhau, bản đồ của HerdSim có cùng hình dạng với bản đồ của họ. Khi thấy mọi thứ, đội nhỏ nhất tăng theo căn bậc hai của số mục tiêu (số mũ 0,52–0,53) theo cả thống kê của bài báo lẫn của HerdSim. Với bán kính cảm nhận 10, hai cách tách nhau gần ngưỡng: ở 144 mục tiêu, trung bình của bài báo đạt 0,99 với 11 người chăn, trong khi với 17 đến 25 người chăn vẫn có lượt kết thúc với từ hai mục tiêu trở lên ở ngoài, nên $D_{\min}$ của HerdSim là khoảng 17–25.

## 1. Câu hỏi nghiên cứu

Các nghiên cứu trước về nhiều chó chăn khảo sát các đội có quy mô cố định hoặc các mục tiêu không tụ bầy (Pierson và Schwager 2015; Kubo et al. 2022; Lama và di Bernardo 2024). Nghiên cứu này hỏi đội tối thiểu tăng thế nào khi cừu tụ bầy, khi thời hạn gấp và khi bầy xuất phát phân tán. Nghiên cứu đầu có bảy câu hỏi:

- RQ1 (quy mô bầy): $D_{\min}$ tăng thế nào theo $N$ từ 25 đến 400, qua các bố cục và thời hạn? Độ gắn kết có làm thay đổi mức tăng $\sqrt{N}$ thấy ở mục tiêu không gắn kết không?
- RQ2 (bố cục so với quy mô): ở cùng một thời hạn, bố cục xuất phát hay $N$ làm $D_{\min}$ thay đổi nhiều hơn?
- RQ3 (thời hạn): $D_{\min}$ thay đổi thế nào từ 12 xuống 6 rồi 3 lần thời gian lùa, và thay đổi đó từ từ hay đột ngột?
- RQ4 (quy tắc thành công): quy tắc nghiêm ngặt và quy tắc 99% khác nhau thế nào, và vì sao các đội lớn thất bại dưới quy tắc nghiêm ngặt?
- RQ5 (lựa chọn thiết lập): kết quả có giữ nguyên khi đổi các lựa chọn không có giá trị thực tế không (vị trí thả chó, khoảng cách xuất phát, bán kính đích, tham số cừu, tốc độ chó)?
- RQ6 (phối hợp): các chó không phối hợp có đạt được $D_{\min}$ hữu hạn trên bầy lớn không?
- RQ7 (đủ và quá nhiều): từ đội $D_{\mathrm{sat}}$ nào thì thêm một chó không còn rút ngắn thời gian lùa, mỗi chó vượt quá tốn bao nhiêu, nó có thêm áp lực lên cừu không, và có đội nào làm nhiệm vụ thất bại không (đội tin cậy lớn nhất $D_{\max}$, và $D_{\mathrm{overcrowd}}$)? (Đọc từ các lượt chạy 99% sẵn có.)

Các lượt chạy tiếp theo (quy tắc 99% xuyên suốt) thêm bảy câu hỏi:

- RQ8 (lưới dày hơn): trên chín quy mô bầy đến $N = 566$, $D_{\min}$ và $D_{\mathrm{sat}}$ tăng nhanh thế nào, và có phân biệt được tăng đều với một đường cong chững lại không?
- RQ9 (các phần của quy tắc): công tắc gom/lùa và tầng đội mỗi phần thêm gì, và một mô hình mà thời gian hoàn thành giảm theo $D$ (Kubo) bão hòa ra sao?
- RQ10 (quá nhiều chó): giữ bầy trong đích, hay chó chiếm chỗ, có làm thêm chó trở nên có hại không, và giữ một bầy nhỏ cần đích cỡ nào?
- RQ11 (độ gắn kết): mức tăng của $D_{\min}$ thay đổi thế nào theo độ mạnh của sự gắn kết?
- RQ12 (chó thấy gì): tầm cảm nhận giới hạn tốn bao nhiêu chó, và chia sẻ những gì các chó thấy có bù lại được không?
- RQ13 (N lớn): điều gì xảy ra trên quy mô mà bầy của mô hình còn có kích thước riêng?
- RQ14 (mục tiêu không gắn kết): HerdSim có cho lại kết quả của Lama và di Bernardo (2024) không, và quy luật căn bậc hai của họ có đúng dưới quy tắc tin cậy của HerdSim cũng như dưới thống kê của họ không?

## 2. Quy tắc quyết định

(Bộ chạy thích ứng, các khoảng tin cậy và hạt giống dùng chung được mô tả ở [task_design_vi.md: lấy mẫu thích ứng](task_design_vi.md#3-động-cơ-lấy-mẫu-thích-ứng-tuần-tự-adaptive-sequential-sampling).)

### 2.1 Khi nào một đội là tin cậy
Một **ô** là một phương pháp, bố cục, $N$ và $D$ trong một giao thức, giao thức này cố định thời hạn và quy tắc thành công ([bảng thuật ngữ](glossary_vi.md#lượt-chạy-và-thí-nghiệm)). Mỗi lượt chạy thành công hoặc thất bại. Với $n$ lượt và $k$ lượt thành công, $[L, U]$ là khoảng Clopper–Pearson hai phía 99% chính xác cho tỷ lệ thành công thật $p$:

$$
L = B\left(\frac{\alpha}{2}, k, n - k + 1\right), \quad U = B\left(1 - \frac{\alpha}{2}, k + 1, n - k\right)
$$

trong đó $B(q, a, b)$ là phân vị $q$ của phân phối Beta với tham số $a$ và $b$, $\alpha = 0{,}01$, và $n$ từ 10 đến 200 lượt mỗi ô.

Với ngưỡng $\theta = 0{,}90$:
- Tin cậy: $L \ge 0{,}90$.
- Không tin cậy: $U < 0{,}90$.
- Chưa quyết định: $L < 0{,}90 \le U$. Ô nhận thêm hạt giống, đến tối đa 200 ([khi nào ngừng lấy mẫu](task_design_vi.md#dừng-sớm-bằng-khoảng-tin-cậy-clopper-pearson-99)).

Với một đường cong các số chó đã thử ở cùng phương pháp, bố cục, $N$ và thời hạn:

$$
D_{\min} = \min \lbrace D \mid \text{ô } D \text{ tin cậy} \rbrace, \qquad
D_{\min,\mathrm{low}} = \min \lbrace D \mid U(D) \ge \theta \rbrace
$$

Các bảng ghi $D_{\min}$ theo bốn dạng:
- Một giá trị (`3`): mọi $D$ nhỏ hơn đều không tin cậy.
- Một khoảng (`3-8`): $D = 8$ tin cậy nhưng một $D$ nhỏ hơn từ 3 trở lên vẫn chưa quyết định ở 200 lượt.
- Một cận dưới (`[5]`): chưa $D$ nào tin cậy, và $D_{\min}$ ít nhất là 5.
- `none`: mọi $D$ đã thử đến đỉnh lưới (24 ở các lượt chạy chính) đều không tin cậy.

### 2.2 Các giao thức
Nghiên cứu đầu có 23 giao thức (164.740 lượt, 20 worker, không lỗi):
- Lưới chính (6 lượt chạy): 5 quy mô bầy, 4 bố cục và 3 thời hạn, mỗi thứ dưới quy tắc nghiêm ngặt và quy tắc 99%.
- Đối chứng FAT (2 lượt chạy): `dmin_fat` và `dmin_f99_fat` ở 6 lần thời gian lùa.
- Mô hình Kubo (1 lượt chạy): `dmin_kubo` trên bầy tập trung 25 đến 100.
- Độ nhạy (14 lượt chạy): ở 6 lần thời gian lùa, một cơ sở và sáu biến thể (thả chó từ một điểm, chó trên vòng tròn, khoảng cách xuất phát 15 và 60 thay vì 30, bán kính đích $1{,}5 R_f$, bộ tham số cừu khớp thực địa, tốc độ chó 1,15), mỗi thứ dưới cả hai quy tắc.

Phần tiếp theo thêm 16 giao thức và chạy tiếp ba lưới 99% (234.100 lượt, không lỗi, chỉ quy tắc 99%, với 90% và 95% thêm vào trong một giao thức giữ bầy); chúng được liệt kê cùng RQ8–RQ13 và trong [phụ lục A](appendix_run_record_vi.md#phụ-lục-a-nhật-ký-chạy-giao-thức). Hai giao thức của mô hình Lama và di Bernardo (40.280 lượt, không lỗi) trả lời RQ14.

## 3. Kết quả

Kết quả nằm trong sáu phần theo chủ đề, mỗi phần đánh số hình và bảng từ 1, và nhật ký chạy nằm trong một phụ lục:

- [Mức tăng của đội nhỏ nhất theo quy mô bầy, bố cục và thời hạn](part1_growth_vi.md): các mục [3.1](part1_growth_vi.md#31-rq1-d_min-tăng-thế-nào-theo-n), [3.2](part1_growth_vi.md#32-rq2-bố-cục-hay-quy-mô-bầy-làm-d_min-thay-đổi-nhiều-hơn), [3.3](part1_growth_vi.md#33-rq3-thời-hạn-làm-d_min-thay-đổi-thế-nào), [3.8](part1_growth_vi.md#38-rq8-mức-tăng-theo-n-trên-lưới-dày-hơn-d_sat-và-hình-dạng-đường-cong), [3.13](part1_growth_vi.md#313-rq13-bầy-rất-lớn-và-một-giới-hạn-của-quy-tắc-lùa).
- [Quy tắc thành công và các thay đổi thiết lập](part2_success_rule_vi.md): các mục [3.4](part2_success_rule_vi.md#34-rq4-quy-tắc-thành-công-và-con-cừu-cuối-cùng), [3.5](part2_success_rule_vi.md#35-rq5-kết-quả-nào-giữ-nguyên-khi-đổi-thiết-lập).
- [Đủ chó và quá nhiều chó](part3_beyond_dmin_vi.md): các mục [3.7](part3_beyond_dmin_vi.md#37-rq7-vượt-quá-d_min-đủ-chó-chi-phí-và-áp-lực-lên-bầy), [3.10](part3_beyond_dmin_vi.md#310-rq10-khi-nào-thêm-chó-gây-hại-giữ-bầy-và-chó-chiếm-chỗ).
- [Sự phối hợp và những gì chó thấy](part4_coordination_vi.md): các mục [3.6](part4_coordination_vi.md#36-rq6-chó-không-có-quy-tắc-đội-có-đạt-d_min-hữu-hạn-không), [3.9](part4_coordination_vi.md#39-rq9-phần-nào-của-quy-tắc-đội-quan-trọng), [3.12](part4_coordination_vi.md#312-rq12-chó-thấy-gì-và-chia-sẻ-điều-đó).
- [Vì sao các lượt thất bại: bố cục `split` và cách các lượt thất bại kết thúc](part5_failures_vi.md): các mục [4](part5_failures_vi.md#4-xem-kỹ-hơn-bố-cục-split-và-các-số-đo-theo-từng-bước), [5.2](part5_failures_vi.md#52-các-lượt-thất-bại-kết-thúc-thế-nào-và-độ-trải-lúc-xuất-phát).
- [Độ gắn kết và quy luật căn bậc hai](part6_square_root_law_vi.md): các mục [3.11](part6_square_root_law_vi.md#311-rq11-độ-gắn-kết-và-mức-tăng-của-d_min), [3.14](part6_square_root_law_vi.md#314-rq14-mục-tiêu-không-gắn-kết-quy-luật-căn-bậc-hai-của-lama-và-di-bernardo-2024), [5.1](part6_square_root_law_vi.md#51-so-với-quy-luật-căn-bậc-hai).
- [Nhật ký chạy, các khẳng định và khả năng tái lập](appendix_run_record_vi.md): các phụ lục [A](appendix_run_record_vi.md#phụ-lục-a-nhật-ký-chạy-giao-thức), [B](appendix_run_record_vi.md#phụ-lục-b-các-khẳng-định-và-bằng-chứng), [C](appendix_run_record_vi.md#phụ-lục-c-khả-năng-tái-lập).

## 5. Thảo luận

### 5.3 Nghiên cứu này thêm được gì

1. Một bản đồ quy mô đội đã quyết định: $D_{\min}$ và $D_{\mathrm{sat}}$ qua các quy mô bầy ($N \le 566$, với các lượt chạy đến 3200), bố cục và thời hạn, mỗi ô được quyết định với độ tin cậy 99% hoặc báo cáo dưới dạng khoảng.
2. Quy tắc thành công thay đổi câu trả lời: dưới quy tắc nghiêm ngặt, con cừu cuối cùng thường quyết định một lượt; quy tắc 99% đo những gì cả đội làm được với bầy.
3. Đội tin cậy và đội nhanh là hai đội khác nhau: đội nhanh nhất tăng theo $N$ nhanh gấp khoảng 1,6 lần đội tin cậy nhỏ nhất (1,15 đến 2,4 lần theo hai đầu khoảng), và chó vượt quá nó chỉ thêm chi phí mà không thêm tốc độ.
4. Phần nào của quy tắc đội quan trọng: công tắc gom/lùa đưa một đội không phối hợp đến $N = 200$; ở $N = 400$ cần phân công.
5. Khi nào thêm chó gây hại: trong các lượt chạy chính theo quy tắc 99%, chó dạng điểm chưa bao giờ làm mất một đội tin cậy trên `wide` hay `outlier_rich` (một chỗ trũng trên `split` ở lưới dày hơn, và theo quy tắc nghiêm ngặt thêm hai chỗ trên `split` $N = 100$); chó giữ cách nhau 2 m thất bại trên `outlier_rich` $N = 400$ từ khoảng 9 chó, và khi chia sẻ với cả đội, `split` $N = 200$ thất bại khi có hơn 3 chó.
6. Độ gắn kết và quy luật căn bậc hai: bầy Strömbom tăng chậm hơn $\sqrt{N}$ ở thời hạn thong thả, và gắn kết yếu hơn đẩy nó về phía 0,5.
7. Một giới hạn của quy tắc lùa: trên $N \approx 1056$, điểm lùa của Strömbom nằm ngoài khoảng cách phản ứng của cừu; giới hạn nó lại làm việc lùa hoạt động trở lại.
8. Cảm nhận và chia sẻ: tầm nhìn cục bộ tốn khoảng một chó trên `wide` $N = 200$, và chia sẻ với cả đội lấy lại được; trên `split`, tầm nhìn cục bộ 30 đến 65 m không chia sẻ còn tốt hơn thấy mọi thứ (ở 15 m thì kém hơn).
9. Các thất bại kết thúc thế nào: phần lớn các lượt lùa thất bại kết thúc xa đích.
10. Một bộ mô phỏng tái lập được: mọi lượt có thể chạy lại từ cấu hình và hạt giống của nó; 1172 lượt chạy lại chẩn đoán cho đúng các lượt đã lưu.

### 5.4 Ứng dụng khả dĩ

Ứng dụng trực tiếp là chăn dắt bằng robot và drone, nơi phải chọn quy mô đội trước khi chạy. Với người chăn cừu thực thụ, các con số chỉ mang tính gián tiếp: họ quyết định bằng kinh nghiệm và tự điều khiển chó, và cừu của mô hình khác cừu thật (bầy lỏng hơn, một khoảng cách phản ứng cố định).

Dưới đây, một *đơn vị* là một thành viên của đội: một chó, một robot hay một drone. Số đơn vị chính là quy mô đội $D$, nên "một đến ba đơn vị" nghĩa là $D = 1$ đến 3.

- Định cỡ một đội: ở thời hạn thong thả, một đến ba đơn vị xử lý được một bầy phân tán đến 400 con, và một bầy tập trung cần một đơn vị đến $N = 1131$ (hai ở 1600, với điểm lùa bị giới hạn), dù ở 1131 một chó cần khoảng 2,8 lần thời gian của hai chó. Thời hạn làm thay đổi câu trả lời nhiều hơn một bầy lớn gấp bốn, nên hãy chốt thời gian có được trước khi chọn quy mô đội.
- Tốc độ tốn hơn độ tin cậy: trên `wide` và `outlier_rich`, đội nhanh nhất lớn gấp rưỡi đến hai lần rưỡi đội tối thiểu (nhiều hơn trên `split`), và các đơn vị vượt quá nó chỉ thêm thời gian chạy mà không thêm lợi ích ([Bảng 1 của mục 3.7](part3_beyond_dmin_vi.md#2-chó-vượt-d_sat-tốn-bao-nhiêu)).
- Chỗ mỗi đơn vị chiếm giới hạn đội hữu ích: các đơn vị không thể đến gần nhau dưới 2 m làm chật vòng cung sau một bầy `outlier_rich` từ khoảng 9 đơn vị ở $N = 400$.
- Chia sẻ bản đồ trước khi thêm đơn vị với một bầy mở: trên `wide` $N = 200$ tầm nhìn cục bộ tốn khoảng một đơn vị và chia sẻ những gì mọi đơn vị thấy đã lấy lại được. Với một bầy chia cụm thì không như vậy: trên `split` $N = 200$ tầm nhìn cục bộ làm tốt hơn thấy mọi thứ, và chia sẻ với cả đội thất bại từ 4 đơn vị.
- Lùi ra để giữ bầy, và định cỡ vùng giữ cho việc đó: các đơn vị phải lùi ra ngoài khoảng cách chạy trốn của con vật để giữ bầy tại chỗ; các đơn vị chỉ dừng lại thì vẫn làm bầy di chuyển. Trong lúc chúng lùi ra, bầy vẫn tiếp tục đi (13 đến 17 m ở đây), nên vùng giữ phải chứa được quãng đi đó cộng phần bầy tự chiếm.
- Bầy lớn cần điểm lùa gần hơn: một bộ điều khiển dùng quy tắc lùa của Strömbom phải giới hạn khoảng đứng ở khoảng cách chạy trốn với bầy trên khoảng một nghìn con.
- Phúc lợi động vật: trong mô hình, thời gian mỗi con cừu chạy trốn không tăng khi thêm đơn vị. Đây là một giả thuyết để thử ngoài thực địa theo tinh thần của Yaxley et al. (2021), không phải một phát hiện về động vật.

## 6. Hạn chế

1. Cơ thể đơn giản: cừu và chó là các điểm, quay hướng tức thì và không mệt.
2. Không có hàng rào: cánh đồng thật có hàng rào giúp chó giữ các con lạc; mô hình không có.
3. Các khoảng: các ô có tỷ lệ thành công thật gần 0,90 vẫn chưa quyết định ở 200 lượt, nên một số câu trả lời là khoảng.
4. Thấy mọi thứ ở phần lớn lượt chạy: ngoài [mục 3.12](part4_coordination_vi.md#312-rq12-chó-thấy-gì-và-chia-sẻ-điều-đó), chó biết vị trí của mọi con cừu. [Mục 3.12](part4_coordination_vi.md#312-rq12-chó-thấy-gì-và-chia-sẻ-điều-đó) giới hạn tầm nhưng vẫn cho vị trí chính xác trong tầm; việc chỉ cảm nhận hướng không được mô hình hóa.
5. Các lựa chọn của HerdSim ở phần tiếp theo: quy tắc lùi ra khi giữ bầy, khoảng cách 2 m giữa các chó và điểm lùa bị giới hạn là lựa chọn của HerdSim, không phải quan sát từ chó thật. Các cỡ đích giữ được bầy nhỏ ([mục 3.10](part3_beyond_dmin_vi.md#310-rq10-khi-nào-thêm-chó-gây-hại-giữ-bầy-và-chó-chiếm-chỗ)) gắn với quy tắc lùi ra này: với chó lùi sớm hơn hay chậm hơn, quãng đi của bầy và do đó cỡ đích cần thiết sẽ khác.
6. Giới hạn hiệu chỉnh: trên khoảng $N = 600$, bầy Strömbom không ổn định về một kích thước, nên kết quả ở $N$ lớn hơn là ở một mật độ được áp đặt. Ở $N = 800$ đến 1131, bầy tập trung trong một lượt chỉ bằng 0,5–0,8 lần bán kính áp đặt (`cli/dmin_tables.py extent`).
7. Mẫu chẩn đoán nhỏ: các lượt chạy lại về áp lực và về `split` dùng 12 hạt giống mỗi ô, các lượt chạy lại đo quãng đi khi giữ bầy dùng 5. Chúng cho thấy xu hướng, không phải cận chặt.
8. Nhiều chó cùng đẩy một con cừu: mô hình của Strömbom định nghĩa lực đẩy của một chó. HerdSim chuẩn hóa tổng lực đẩy của mọi chó trong vòng 65 m về độ lớn lực đẩy của một chó, vì cộng thẳng sẽ xé bầy từ $D = 2$ trở lên ([chuẩn hóa lực đẩy](models_vi.md#chuẩn-hóa-tổng-lực-đẩy-từ-nhiều-chó-cải-tiến-của-herdsim)). Đây là một lựa chọn mô hình; liệu cừu thật có chạy mạnh hơn khi gặp nhiều chó không là câu hỏi cho dữ liệu thực địa.
9. Tốc độ cừu: một con cừu Strömbom đang phản ứng luôn đi với 1 m/s, nên thời gian hoàn thành phẳng sau $D_{\mathrm{sat}}$ là hệ quả của mô hình. Cừu Kubo tăng tốc khi bị đẩy mạnh hơn (đến 5 m/s), vì thế thêm chó Kubo vẫn tiếp tục rút ngắn lượt lùa.
10. Tái lập trên máy khác: chạy lại cho kết quả chính xác trên cùng một máy, với các phiên bản phụ thuộc đã khóa (`uv.lock`) và một luồng BLAS mỗi tiến trình. Trên CPU khác, các bit cuối của phép tính dấu phẩy động có thể khác, có thể làm đổi kết quả của những lượt hiếm kết thúc sát thời hạn.
11. Xem kết quả giữa các lô: độ tin cậy được quyết định sau mỗi lô 10 hạt giống. Khoảng Clopper–Pearson thận trọng và một ô tin cậy cần ít nhất 51 lượt thành công liên tiếp, nhưng việc xem nhiều lần không được hiệu chỉnh, nên độ tin cậy 99% của một quyết định chỉ là gần đúng: với tối đa 20 lần xem mỗi ô, xác suất dừng sai cao hơn 1% một chút.
12. Mô hình Lama và di Bernardo được dựng lại từ văn bản bài báo; không có mã nguồn công bố. Ở những chỗ văn bản không nói, HerdSim chọn và ghi rõ (lực đẩy hướng ra xa người chăn; một lượt kết thúc khi mọi người chăn ở trong đích và không ai thấy mục tiêu nào bên ngoài; mục tiêu và người chăn được di chuyển từ cùng một trạng thái). [Mục 3.14](part6_square_root_law_vi.md#314-rq14-mục-tiêu-không-gắn-kết-quy-luật-căn-bậc-hai-của-lama-và-di-bernardo-2024) chỉ so bằng số với Bảng I của bài báo và so phần còn lại bằng cách đặt hình của HerdSim cạnh hình của bài báo.

## 7. Kết luận và hướng tiếp theo

Qua 439.120 lượt trong 41 giao thức, HerdSim lập bản đồ đội tin cậy nhỏ nhất $D_{\min}$, đội mà vượt quá nó thêm chó không còn giúp ($D_{\mathrm{sat}}$), và những tình huống mà thêm chó gây hại. Một bầy tập trung cần một chó đến $N = 1131$ (với điểm lùa bị giới hạn trên 1056). Trên bầy phân tán, đội nhỏ nhất tăng chậm hơn bầy, với độ dốc 0,27–0,38 ở 12 lần thời gian lùa và 0,38–0,61 ở 6 lần, trong khi đội nhanh nhất tăng nhanh gấp khoảng 1,6 lần. Dưới quy tắc nghiêm ngặt, con cừu cuối cùng quyết định; dưới quy tắc 99%, câu trả lời giữ nguyên khi đổi thiết lập. Phối hợp quan trọng ở bầy lớn. Trong các lượt chạy chính theo quy tắc 99%, thêm chó dạng điểm chưa bao giờ làm mất một đội tin cậy trên `wide` hay `outlier_rich` nhưng làm chậm `split` và bầy `outlier_rich` lớn nhất, còn chó chiếm chỗ thì có gây thất bại. Giữ một bầy nhỏ có lẽ thất bại vì cỡ đích hơn là vì thiếu chó: bầy vẫn đi khi chó lùi ra, và một đích khoảng 16 đến 19 m giữ được nó với một chó. Bản thân quy tắc lùa của Strömbom ngừng hoạt động trên khoảng một nghìn con. Chạy trong cùng bộ mô phỏng, các mục tiêu không gắn kết của Lama và di Bernardo theo đúng quy luật căn bậc hai của họ, cả dưới quy tắc tin cậy của HerdSim, trừ gần ngưỡng của họ, nơi một mức trung bình 0,99 che đi những lượt sót từ hai mục tiêu trở lên.

### Hướng tiếp theo

1. Phân công có nhìn thấy cụm: trên `split`, phân công chó sao cho mỗi cụm đều có chó, thay vì chỉ theo tổng quãng đường. Quy tắc buộc các chó gom chọn những con lạc cách xa nhau đã có sẵn và mới chỉ được chạy lại trên 12 hạt giống mỗi ô; bước đầu là một giao thức trên lưới `split`.  
   Điều này cần thiết vì `split` là bố cục duy nhất mà thêm chó dạng điểm làm chậm việc lùa, và các lượt chạy lại chỉ ra hai nguyên nhân: cách phân công và việc chó bị quy tắc dừng giữ đứng yên ([mục 4.1](part5_failures_vi.md#41-vì-sao-thêm-chó-không-giúp-trên-split)).  
   Hướng này sẽ kiểm tra trên toàn lưới xem sự chậm lại đó thuộc về quy tắc phân công chứ không phải cỡ đội, và một quy tắc tốt hơn có hạ được $D_{\min}$ ở 3 lần thời gian lùa không, nơi cả hai thay đổi đã chạy lại đều chưa đủ.
2. Ước lượng cục bộ tâm bầy: thay việc cừu biết tâm của cả bầy bằng hướng về các hàng xóm gần nhất. Hướng đó lệch bao nhiêu trên các bố cục xuất phát được đo trong [mô hình](models_vi.md#2-lực-hút-về-bầy). Chỉ quy tắc của cừu thay đổi, nhưng phải chạy lại các lưới chính.  
   Điều này cần thiết vì độ dốc thấp của $D_{\min}$ có lẽ dựa trên việc mỗi con cừu bị hút về cả bầy, nên một con lạc tự đi về ([mục 3.1](part1_growth_vi.md#31-rq1-d_min-tăng-thế-nào-theo-n)). Cừu thật chỉ thấy các con bên cạnh.  
   Hướng này sẽ cho thấy bao nhiêu phần trong chênh lệch giữa độ dốc của bầy (0,27–0,61) và quy luật căn bậc hai của các mục tiêu không gắn kết đến từ hiểu biết toàn cục đó.
3. Chỉ cảm nhận hướng: cho chó cảm nhận hướng tới một con cừu mà không biết khoảng cách, như một camera trên drone. Quy tắc đội chọn con lạc và điểm lùa theo khoảng cách, nên phải thiết kế lại trước.  
   Điều này cần thiết vì chó ở đây biết vị trí của mọi con cừu trong tầm; một drone với một camera thì không.  
   Hướng này sẽ đo xem $D_{\min}$ phụ thuộc bao nhiêu vào thông tin khoảng cách, và thêm chó có bù được khi mất thông tin đó không.
4. Ghép chéo hai mô hình trên một nhiệm vụ: chạy quy tắc đội của Strömbom trên các mục tiêu của Lama trong nhiệm vụ gom, và người chăn của Lama trên cừu Strömbom. Mỗi quy tắc đọc những đại lượng mà phía kia không có (quy tắc đội đọc khoảng cách gom, vô nghĩa khi không có gắn kết; người chăn đọc khoảng cách đến một đích mà trong nhiệm vụ lùa nằm xa bầy), nên mỗi cách ghép cần thiết kế riêng trước.  
   Điều này cần thiết vì [mục 3.14](part6_square_root_law_vi.md#314-rq14-mục-tiêu-không-gắn-kết-quy-luật-căn-bậc-hai-của-lama-và-di-bernardo-2024) so hai mô hình khác nhau cùng lúc ở mục tiêu, quy tắc người chăn và nhiệm vụ.  
   Hướng này sẽ tách chênh lệch số mũ thành phần do độ gắn kết và phần do quy tắc người chăn và nhiệm vụ.
5. Giữ bầy có cổng: một đích lớn hơn đã giữ được bầy nhỏ ([mục 3.10](part3_beyond_dmin_vi.md#310-rq10-khi-nào-thêm-chó-gây-hại-giữ-bầy-và-chó-chiếm-chỗ)). Một chuồng đóng cần hàng rào tác động lên cừu, một cổng, cách bố trí xuất phát quanh nó và một quy tắc lùa nhắm vào cổng, những thứ thế giới mô phỏng hiện chưa có.  
   Điều này cần thiết vì ở trang trại, bầy được giữ trong chuồng, không phải trong một vòng tròn mở lớn hơn quãng đi của nó.  
   Hướng này sẽ kiểm tra hàng rào có bỏ được nhu cầu chọn cỡ vùng giữ theo quãng đi không, và một chuồng cần đội bao nhiêu chó.
6. Dữ liệu thực địa với nhiều chó: hợp tác với các nhà nghiên cứu chăn nuôi để thu dữ liệu GPS khi chăn bằng nhiều chó hoặc drone. Việc này cần đối tác, vật nuôi và giấy phép ngoài bộ mô phỏng.  
   Điều này cần thiết vì trong mô hình Strömbom, lực đẩy của nhiều chó được chuẩn hóa về cỡ lực đẩy của một chó, nên thời gian hoàn thành phẳng sau $D_{\mathrm{sat}}$ là hệ quả của mô hình ([mục 6](#6-hạn-chế), hạn chế 9).  
   Hướng này sẽ kiểm tra cừu thật có chạy mạnh hơn khi gặp nhiều chó không, điều quyết định $D_{\mathrm{sat}}$ có tồn tại trong thực tế hay không.

## Dữ liệu và mã

Mọi lượt chạy và quyết định của từng ô được lưu trong `results/<protocol>/`. Các bảng chứa số liệu của báo cáo này nằm trong [results_tables.md](../report/results_tables.md); mỗi khối ghi lệnh đã tạo ra nó. Cách chạy lại nghiên cứu và tạo lại các bảng: xem [cli/README.md](../../cli/README.md) và [tài liệu tham chiếu CLI](../guides/cli_reference.md).

## Tài liệu tham khảo

- Auletta F, Fiore D, Richardson MJ, di Bernardo M (2021). Herding stochastic autonomous agents via local control rules and online global target selection strategies. *arXiv:2010.00386*.
- Brown D, Garrity T, Perkins D, Hunter D, Pochman W (2025). Optimal control strategies for multi-agent sheep herding. *arXiv:2510.25115*.
- di Bernardo M (2026). Multi-scale control of large agent populations: from density dynamics to individual actuation. *arXiv:2603.15160*.
- Green T, et al. (2022). A minimalist solution to the multi-robot barrier coverage problem. *Towards Autonomous Robotic Systems (TAROS 2021)*, LNCS 13054.
- Jadhav V, Pasqua R, Zanon C, Roy M, Tredan G, Bon R, Guttal V, Theraulaz G (2024). Collective responses of flocking sheep (*Ovis aries*) to a herding dog (border collie). *Communications Biology* 7: 1543.
- Kubo M, Tashiro M, Sato H, Yamaguchi A (2022). Herd guidance by multiple sheepdog agents with repulsive force. *Artificial Life and Robotics* 27: 416–427.
- Lama A, di Bernardo M (2024). Shepherding and herdability in complex multiagent systems. *Physical Review Research* 6: L032012.
- Li A, Ogura M, Wakamiya N (2025). Swarm shepherding using bearing-only measurements. *Philosophical Transactions of the Royal Society A* 383: 20240145.
- Pierson A, Schwager M (2015). Bio-inspired non-cooperative multi-robot herding. *IEEE International Conference on Robotics and Automation (ICRA)*.
- Ranganathan A, et al. Emergent strategies for shepherding a flock. *arXiv:2211.04352*.
- Strömbom D, Mann RP, Wilson AM, Hailes S, Morton AJ, Sumpter DJT, King AJ (2014). Solving the shepherding problem: heuristics for herding autonomous, interacting agents. *Journal of the Royal Society Interface* 11(100): 20140719.
- Yaxley KJ, Joiner KF, Abbass H (2021). Drone approach parameters leading to lower stress sheep flocking and movement: sky shepherding. *Scientific Reports* 11: 7803.
