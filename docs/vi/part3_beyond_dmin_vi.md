# Đủ chó và quá nhiều chó

Phần 3 của báo cáo HerdSim về quy mô đội. [Phần tổng quan](d_min_report_vi.md) gồm tóm tắt, các câu hỏi nghiên cứu, [quy tắc quyết định](d_min_report_vi.md#2-quy-tắc-quyết-định) định nghĩa $D_{\min}$, khoảng và cận dưới của nó, phần thảo luận và [tài liệu tham khảo](d_min_report_vi.md#tài-liệu-tham-khảo). Các thuật ngữ được định nghĩa trong [bảng thuật ngữ](glossary_vi.md).

## 3.7 RQ7: Vượt quá D_min: đủ chó, chi phí, và áp lực lên bầy

Biết đội tin cậy nhỏ nhất vẫn để lại những câu hỏi thực tế. Thêm chó có lùa nhanh hơn không? Mỗi chó thêm tốn bao nhiêu? Thêm chó có làm cừu căng thẳng hơn không? Chúng tôi đọc các câu trả lời từ các lượt chạy 99% (11 giao thức), và chạy lại 164 lượt đã lưu để đo thời gian mỗi con cừu chạy trốn (mọi lượt chạy lại đều cho đúng lượt đã lưu). Các ý 1 đến 5 lần lượt trả lời. Từ một quy mô đội gọi là $D_{\mathrm{sat}}$ trở đi, thêm chó không còn làm lượt lùa nhanh hơn (ý 1); vượt quá nó, mỗi chó thêm thời gian chó ($D$ nhân thời gian hoàn thành) nhưng thêm rất ít tốc độ (ý 2); thêm chó làm nhiều cừu chạy trốn cùng lúc hơn nhưng tổng thời gian hầu như không lâu hơn (ý 3); và theo quy tắc 99%, thêm chó hầu như không bao giờ làm nhiệm vụ thất bại (ý 4 và 5).

### 1. Khi nào thêm chó không còn giúp (D_sat)
$D_{\mathrm{sat}}$ là đội tin cậy nhỏ nhất mà không đội tin cậy lớn hơn nào nhanh hơn quá 5% thời gian hoàn thành, với độ tin cậy 99%; khi một phép so sánh còn chưa quyết định, $D_{\mathrm{sat}}$ được ghi dưới dạng một khoảng ([cách so sánh các đội](task_design_vi.md#các-giá-trị-ranh-giới)).
- Bầy tập trung và $N \le 50$: $D_{\mathrm{sat}} = 1$ (trừ `outlier_rich` $N = 50$, khoảng 1–24). Một chó đã giữ bầy đi với 1 m/s.
- Bầy phân tán ở 6 lần thời gian lùa: $D_{\mathrm{sat}}$ là 2 đến 7 ở những chỗ đã quyết định với $N = 100$ đến 400 (`outlier_rich` $N = 100$: 3; `wide` $N = 400$: 5; `split` $N = 141$: 7); trên `outlier_rich` ở $N \ge 283$ đầu trên của khoảng vẫn còn mở.
- Sau các lượt chạy bổ sung thời gian hoàn thành ([mục 3.8](part1_growth_vi.md#38-rq8-mức-tăng-theo-n-trên-lưới-dày-hơn-d_sat-và-hình-dạng-đường-cong)), $D_{\mathrm{sat}}$ trên `wide` là 1, 1, 1, 2, 3, 3, 4, 5 từ $N = 25$ đến 400.
- $D_{\mathrm{sat}}$ không đổi giữa 12 và 6 lần thời gian lùa; ở 3 lần, $D_{\min}$ tăng lên tới $D_{\mathrm{sat}}$ trên `wide` nhưng không trên `outlier_rich` hay `split` ([mục 3.3](part1_growth_vi.md#33-rq3-thời-hạn-làm-d_min-thay-đổi-thế-nào)).

### 2. Chó vượt D_sat tốn bao nhiêu
- Ở cả 189 ô tin cậy trên một $D_{\mathrm{sat}}$ đã quyết định ở 6 lần thời gian lùa, thời gian hoàn thành bằng 0,96 đến 1,01 lần thời gian tại $D_{\mathrm{sat}}$: nhanh hơn nhiều nhất 4%, đôi khi chậm hơn 1% (Hình 1).
- Thời gian chó ($D$ nhân thời gian hoàn thành) tăng theo $D / D_{\mathrm{sat}}$. Trên một bầy tập trung 50 con, 24 chó mất đúng 154 s như một chó, với thời gian chó gấp 24 lần. Các chó di chuyển gần như suốt thời gian đó: ở $N = 400$ (6 lần thời gian lùa, quy tắc 99%), chó ở mức trung vị chạy 1,44–1,50 m/s trên `compact`, `wide` và `outlier_rich`, gần tốc độ tối đa 1,5 m/s của nó, và 1,20–1,40 m/s trên `split`, nơi đến 20% số chó đứng yên.

Bảng 1 so gấp đôi $D_{\mathrm{sat}}$ và $D = 24$ với ô $D_{\mathrm{sat}}$ (bầy phân tán, 6 lần thời gian lùa):

**Bảng 1: Thời gian hoàn thành và thời gian chó tại hai lần $D_{\mathrm{sat}}$ và tại $D = 24$, so với ô $D_{\mathrm{sat}}$.**

| Bố cục, $N$ | $D_{\mathrm{sat}}$ | Tại $2 D_{\mathrm{sat}}$: thời gian hoàn thành / thời gian chó | Tại $D = 24$: thời gian hoàn thành / thời gian chó |
| :--- | :---: | :---: | :---: |
| `wide`, $N = 200$ | 3 | 0,97 / 1,94 | 0,96 / 7,70 |
| `wide`, $N = 400$ | 5 | 0,97 / 2,32 (tại $D = 12$) | 0,96 / 4,61 |
| `outlier_rich`, $N = 100$ | 3 | 0,99 / 1,98 | 0,98 / 7,85 |
| `outlier_rich`, $N = 400$ | 6–24 | 0,96 / 1,91 | 0,94 / 3,74 |
| `split`, $N = 100$ | 4 | 0,99 / 1,98 | 0,99 / 5,91 |

Tại $D = 24$, việc lùa nhanh hơn 1% đến 6% so với tại $D_{\mathrm{sat}}$, với thời gian chó gấp 3,7 đến 7,9 lần.  
*Dữ liệu:* [results_tables.md: Effort, dmin_f99_m6](../report/results_tables.md#effort-dmin_f99_m6-cost-of-dogs-beyond-d_sat-relative-to-the-d_sat-cell-1) và [results_tables.md: D_sat, dmin_f99_m6](../report/results_tables.md#d_sat-dmin_f99_m6-d_sat-1).

### 3. Áp lực lên cừu
Một con cừu chạy trốn khi có chó trong vòng 65 m ($r_s$). Các lượt chạy lại đo khoảng thời gian đó (Hình 2).
- Mỗi con cừu chạy trốn ít hơn, cho đến $D_{\mathrm{sat}}$: nhiều chó gom bầy sớm hơn, nên lượt lùa ngắn hơn. Trên `wide` $N = 400$, trung vị thời gian chạy trốn mỗi con giảm từ 485 s ở $D = 3$ xuống 359 s ở $D = 6$, rồi giữ ở đó (361 s ở $D = 12$). Lượt chạy lại dùng $D = 6$ làm $D_{\mathrm{sat}}$, là giá trị trước đợt bổ sung thời gian hoàn thành; nay nó là 5.
- Nhiều cừu chạy trốn cùng lúc hơn: một đội lớn hơn trải trên một vòng cung rộng hơn, và trung vị tỷ lệ bầy đang chạy trốn tại một thời điểm tăng từ 68% ở $D = 3$ lên 84% ở $D = 12$. Vì lượt lùa xong sớm hơn, tổng thời gian mỗi con cừu chạy trốn không tăng.
- Chó không áp sát cừu: thời gian một con cừu ở trong vòng 6 m ($3 r_a$, khoảng cách dừng của chó) quanh một chó dưới 1,3 s mỗi con (trung vị) ở mọi quy mô đội.

### 4. Thêm chó hầu như không bao giờ làm nhiệm vụ thất bại
Dưới quy tắc 99%, trên năm quy mô bầy ban đầu và đến 24 chó, không đường cong nào đã đạt một đội tin cậy lại trở thành không tin cậy ở các đội lớn hơn. Các ngoại lệ, và những chỗ thêm chó chỉ làm lượt lùa chậm lại:
- Chỗ trũng: trên lưới dày hơn có một chỗ (`split` $N = 141$, $D = 4$, thành công 0,80). Theo quy tắc nghiêm ngặt còn hai chỗ nữa, đều trên `split` $N = 100$. Ở 3 lần thời gian lùa, một chó là tin cậy (60 trong 60), 2 đến 4 chó thì không (5 trong 10, 5 trong 10, 97 trong 120), và từ 5 chó đội lại tin cậy; ở 6 lần thời gian lùa, 3 chó được quyết định là không tin cậy (36 trong 50) giữa 1 chó tin cậy và 5 chó tin cậy.
- Lùa chậm hơn: trên `split` $N = 400$ ở 12 lần thời gian lùa, trung vị thời gian hoàn thành là 950–1040 s với $D \ge 9$ so với 839 s ở $D = 5$, dù nhiệm vụ vẫn thành công.
- Thời gian đi đâu: bầy vào đích thành hai phần. Ở 12 lần thời gian lùa, trên `split` ở $N = 200$ đến 566, các đội từ 3 chó trở lên (từ 2 chó ở $N = 283$, từ 4 chó ở $N = 566$) đưa 90% bầy vào rồi cần trung vị 294 đến 694 s cho 9% tiếp theo, và trên `outlier_rich` $N = 566$ các đội từ 12 chó trở lên cần 465 đến 578 s; trên `outlier_rich` $N = 283$ chỉ 5 và 8 chó có khoảng trễ này (380 và 330 s), các đội khác cần 8 đến 12 s ([mục 4.1](part5_failures_vi.md#41-vì-sao-thêm-chó-không-giúp-trên-split)).
- Các giá trị đầu trên của `outlier_rich` $N = 566$ ([ý 5](#5-đầu-trên-của-các-đường-cong-d_max-d_crowd-và-d_overcrowd)): những con về muộn có lẽ quyết định $D_{\max}$ (12 ở 6 lần thời gian lùa). Ở 12 lần, 16 và 24 chó thành công 130 trong 130 và 100 trong 100 lượt, và vì thời hạn ngắn hơn chỉ cắt chính các lượt đó ([mục 3.3](part1_growth_vi.md#33-rq3-thời-hạn-làm-d_min-thay-đổi-thế-nào)), các thất bại ở 6 lần là những lượt xong muộn hơn. $D_{\mathrm{crowd}}$ của nó (15 ở 12 lần) đến từ cùng sự chậm lại này.
- Hai nhóm lượt chạy trên `outlier_rich` $N = 283$ ở 6 lần thời gian lùa: ở $D = 5$, tứ phân vị là 367 và 799 s và trung vị, 725 s, nằm trong nhóm chậm, còn ở 6 đến 12 chó trung vị nằm trong nhóm nhanh (357–375 s) và tứ phân vị trên nằm trong nhóm chậm (774–815 s). Trung vị so sánh các đội như vậy rất kém, và $D_{\mathrm{sat}}$ của nó vẫn là khoảng từ 5 (5–24).

### 5. Đầu trên của các đường cong: D_max, D_crowd và D_overcrowd
Có một đội lớn nhất còn làm được việc, mà vượt quá nó thì thêm chó sẽ thất bại không? Trong ba lượt chạy chính theo quy tắc 99%, chưa tìm thấy đội như vậy dưới 24 chó, đỉnh của lưới. Ba giá trị giới hạn một đường cong từ phía trên ([các giá trị ranh giới](task_design_vi.md#các-giá-trị-ranh-giới)): $D_{\max}$, đội tin cậy lớn nhất dưới mọi vùng sụp đổ; $D_{\mathrm{crowd}}$, đội tin cậy đầu tiên trên $D_{\mathrm{best}}$ mà chậm hơn $D_{\mathrm{best}}$; và $D_{\mathrm{overcrowd}}$, đội đầu tiên mà từ đó hai quy mô đã thử liên tiếp đều không tin cậy. Trong ba lượt chạy chính theo quy tắc 99%:
- $D_{\max}$ gần như luôn là đỉnh lưới: 84 trong 85 đường cong có $D_{\min}$ vẫn tin cậy ở 24 chó, nên chưa tìm thấy giới hạn trên và $D_{\max}$ chỉ là một cận dưới. Ngoại lệ duy nhất, `outlier_rich` $N = 566$ ở 6 lần thời gian lùa, có $D_{\max} = 12$ vì 16 và 24 chó còn chưa quyết định ở 0,94, chứ không phải vì chúng thất bại.
- $D_{\mathrm{crowd}}$ có ở 6 đường cong ở 12 lần thời gian lùa: `split` ở $N = 71$, 200, 283, 400 và 566 (từ 2 đến 14 chó) và `outlier_rich` $N = 566$ (15 chó). Các đội này vẫn thành công nhưng xong muộn hơn đội nhanh nhất, chính là việc chậm lại nêu ở mục 4.
- $D_{\mathrm{overcrowd}}$ có ở 4 đường cong mà không đội nào được quyết định là tin cậy: `split` $N = 200$, 283 và 400 ở 6 lần thời gian lùa (từ 4, 15 và 10 chó) và `outlier_rich` $N = 400$ ở 3 lần (từ 7). Trên các đường cong này, các đội lớn hơn ở gần nhưng phần lớn dưới $\theta$ (`split` $N = 200$: 0,60–0,95; $N = 283$ và 400 từ 5 chó: 0,70–0,93; `outlier_rich` $N = 400$ từ 5 chó: 0,60–0,86), nên điểm bắt đầu này là chỗ đầu tiên mà hai quy mô đã thử liên tiếp được quyết định là không tin cậy, trên một đường cong chưa bao giờ vượt $\theta$, chứ không phải một cú tụt từ một đội tin cậy.

Thêm chó có làm nhiệm vụ thất bại trong một vài lượt chạy tiếp theo. Khi chia sẻ với cả đội ở tầm 65 m, `split` $N = 200$ tin cậy với 3 chó, được quyết định là không tin cậy ở 4, 6, 8, 9, 13, 14 và 16 chó và chưa quyết định ở 0,85 với 10 và 12 chó ([mục 3.12](part4_coordination_vi.md#312-rq12-chó-thấy-gì-và-chia-sẻ-điều-đó)); gần đích nhỏ nhất giữ được bầy 25 con, các đội lớn hơn thất bại ([mục 3.10](#310-rq10-khi-nào-thêm-chó-gây-hại-giữ-bầy-và-chó-chiếm-chỗ)). Cú tụt lớn nhất là với chó giữ cách nhau 2 m trong nhiệm vụ giữ bầy: trên `outlier_rich` $N = 400$, các đội 3 đến 8 chó đạt 0,87–0,94 (mỗi ô 200 lượt), còn từ 9 chó trở lên tỷ lệ thành công là 0,50–0,77 (10 đến 70 lượt mỗi ô), nên $D_{\mathrm{overcrowd}} = 9$.  
*Dữ liệu:* [results_tables.md: đầu trên của các đường cong](../report/results_tables.md#the-upper-end-of-the-curves-d_max-d_crowd-and-d_overcrowd) (`uv run cli/dmin_tables.py upper ...`); tỷ lệ thành công theo ô trong `frontier_cells.csv` của mỗi thư mục.

![Chi phí của chó vượt D_sat](../figures/fig33_effort.png)

**Hình 1: Chi phí của chó vượt $D_{\mathrm{sat}}$ (6 lần thời gian lùa, quy tắc 99%).** Trên các đường cong có $D_{\mathrm{sat}}$ đã quyết định, chó vượt nó làm lượt lùa nhanh hơn nhiều nhất khoảng 4%, trong khi thời gian chó tăng tỷ lệ với đội.

- Ký hiệu: mỗi đường là một đường cong (một bố cục và một $N$, tô màu theo bố cục) có $D_{\mathrm{sat}}$ đã quyết định, và mỗi điểm là một đội tin cậy từ $D_{\mathrm{sat}}$ trở lên, 27 đường và 189 ô phía trên $D_{\mathrm{sat}}$ của chúng. Trục hoành là $D / D_{\mathrm{sat}}$ (thang log), nên mọi đường bắt đầu ở 1 và $x = 2$ nghĩa là gấp đôi đội cần thiết; trên `wide` $N = 400$ ($D_{\mathrm{sat}} = 5$), $D = 24$ nằm ở 4,8.
- Trái: trung vị thời gian hoàn thành chia cho của ô $D_{\mathrm{sat}}$, nên 0,97 nghĩa là nhanh hơn 3%. Mọi đường đều nằm trong khoảng xấp xỉ 0,96 đến 1,01 (tỷ số lớn nhất là 1,012), một khoảng hẹp mà trục đã kéo giãn. Các điểm dưới 1 không mâu thuẫn với $D_{\mathrm{sat}}$, vì một đội lớn hơn chỉ được tính là nhanh hơn khi nó tiết kiệm hơn 5% thời gian với độ tin cậy 99% (bootstrap ghép cặp trên các hạt giống chung), và không đội nào như vậy.
- Phải: thời gian chó ($D$ nhân thời gian hoàn thành) chia cho của ô $D_{\mathrm{sat}}$. Các đường đi theo đường chéo $y = x$, nên gấp đôi số chó thì tốn gấp đôi thời gian chó.

*Dữ liệu:* [results_tables.md: Effort, dmin_f99_m6](../report/results_tables.md#effort-dmin_f99_m6-cost-of-dogs-beyond-d_sat-relative-to-the-d_sat-cell-1).

![Áp lực lên bầy](../figures/fig34_pressure.png)

**Hình 2: Thời gian cừu chạy trốn theo quy mô đội (6 lần thời gian lùa, quy tắc 99%).** Đội lớn hơn làm nhiều cừu chạy cùng lúc hơn, trong thời gian ngắn hơn.

- Ký hiệu: trung vị trên các lượt thành công cho $N = 100$ (hình tròn, chấm) và $N = 400$ (hình vuông, liền); xanh dương là `wide`, xanh lá là `outlier_rich`. Mỗi đường chỉ có điểm ở các quy mô đội đã chạy lại, $D = 1$, $D_{\min}$, $D_{\mathrm{sat}}$ và $2 D_{\mathrm{sat}}$, theo giá trị trước đợt chạy bổ sung thời gian hoàn thành ($D_{\mathrm{sat}} = 6$ trên `wide` $N = 400$ khi đó, nay là 5). Ở $N = 400$ một chó không thành công lượt nào trong 10 lượt và $D = 2$ không được chạy lại, nên các đường đó bắt đầu ở 3.
- Trái: số giây mỗi con cừu có chó trong vòng 65 m. Từ $D_{\min}$ đến $D_{\mathrm{sat}}$ nó giảm, vì bầy được gom sớm hơn; vượt $D_{\mathrm{sat}}$ nó đi ngang.
- Phải: tỷ lệ bầy đang chạy trốn, lấy trung bình trên mỗi lượt.

*Dữ liệu:* [results_tables.md: Pressure, dmin_f99_m6](../report/results_tables.md#pressure-dmin_f99_m6-replay-of-12-stored-seeds-per-cell-every-replay-reproduced-its-stored-trial).

![Hoạt ảnh cừu chạy trốn 3 chó và 12 chó](../gifs/flock_pressure.gif)

**Hoạt ảnh 1: Bầy dưới 3 chó và 12 chó, chạy lại (`wide`, $N = 400$, hạt giống 0, quy tắc 99%, 6 lần thời gian lùa).** Với 12 chó, nhiều cừu chạy trốn cùng lúc hơn, nhưng lượt lùa ngắn hơn, như ở Hình 2. Cả hai xuất phát từ cùng một bầy, và mỗi lượt chạy lại khớp với lượt đã lưu.

- Ký hiệu: chấm đặc là cừu cách một chó dưới $r_s = 65$ m, đang chạy trốn; chấm rỗng là cừu đang gặm cỏ.
- Trái: 3 chó. Ở 148 s, 129 trong 400 con chạy trốn, và bầy vào đích ở 727 s.
- Phải: 12 chó. Ở 148 s, 395 con chạy trốn, và bầy vào đích ở 431 s.

## 3.10 RQ10: Khi nào thêm chó gây hại? Giữ bầy, và chó chiếm chỗ

Khi nào thêm chó làm mọi việc tệ hơn? Trong nhiệm vụ lùa thường (không giữ bầy) dưới quy tắc 99%, thêm [chó dạng điểm](glossary_vi.md#mô-hình-cừu-và-quy-tắc-chó) (chó không có kích thước, như trong mọi lượt chạy chính) chưa bao giờ làm mất một đội tin cậy trong các lượt chạy chính (trừ một chỗ lõm, [mục 3.7](#37-rq7-vượt-quá-d_min-đủ-chó-chi-phí-và-áp-lực-lên-bầy)). Thêm chó có gây hại trong một vài lượt chạy tiếp theo ([mục 3.7](#37-rq7-vượt-quá-d_min-đủ-chó-chi-phí-và-áp-lực-lên-bầy), ý 5), rõ nhất khi bầy phải ở yên trong đích trong lúc chó lùi ra (giữ bầy): với chó giữ cách nhau 2 m trên `outlier_rich` $N = 400$ (ý 2), và với một đích vừa hơi nhỏ so với bầy 25 con (ý 3). Khi phải giữ 99% bầy, giữ một bầy 50 con trở xuống với đích mặc định thất bại dù đội thế nào, có lẽ vì bầy đi ra khỏi đích trong lúc chó lùi ra (ý 1).

Ba nhóm giao thức thay đổi phần cuối của nhiệm vụ hoặc chỗ mỗi chó chiếm:

1. Giữ bầy (`dmin_f99_hold`): [nhiệm vụ giữ bầy](task_design_vi.md#nhiệm-vụ-giữ-bầy); một lượt chỉ thành công khi 99% bầy đã ở trong đích suốt một lần thời gian lùa trong lúc chó lùi ra.
2. Chó chiếm chỗ (`dmin_f99_hold_spacing`): cùng nhiệm vụ với [chó giữ cách nhau 2 m](task_design_vi.md#cản-trở-khi-chó-chiếm-chỗ). Vòng cung sau bầy khi đó chỉ có chỗ cho một số chó nhất định, khoảng $D_{\mathrm{cap}} = 7, 9, 10, 11, 12$ ở $N = 25$ đến 400 (chiều dài cung chia cho khoảng cách 2 m).
3. Đích giữ được bầy nhỏ (`dmin_f99_hold_goal`, `dmin_f99_hold_share`): nhiệm vụ giữ bầy ở $N = 25$, 50 và 100 với bán kính đích nâng từ $1{,}9 R_f$ lên 2,1; 2,3 và $2{,}5 R_f$, kết hợp với tỷ lệ phải ở lại (99%, 95%, 90%), và lên $3{,}0 R_f$ ở 99%, trên các hạt giống của `dmin_f99_hold`.

### Kết quả

1. Khi phải giữ 99% bầy, giữ bầy thất bại trên bầy nhỏ, có lẽ vì bầy đi ra khỏi một đích nhỏ.  
   Trên bầy lớn hơn ($N \ge 100$), giữ bầy thành công trên `wide` và `compact`, với $D_{\min}$ bằng lúc lùa thường hoặc thêm một (1, 2 và 3 chó trên `wide` ở $N = 100$, 200, 400). Trên `split` nó thất bại từ $N = 200$ ngay cả với chó dạng điểm: ở $N = 200$, một hoặc hai chó thành công 98 trong 120 và 171 trong 200 lượt, các đội lớn hơn 10% đến 75% (10 đến 60 lượt mỗi ô), và ở $N = 400$ không đội nào vượt 0,70; với chó giữ cách nhau 2 m, `split` $N = 200$ giảm xuống 0–10% từ 6 chó.  
   Trên bầy nhỏ ($N \le 50$), không đội nào giữ được bầy, và 72% số lượt thất bại kết thúc mà không còn con cừu nào trong đích. Bầy vào đích ở mép gần với chó ở phía sau. Trong lúc lùi ra, chó vẫn ở trong vòng 65 m của một số con cừu trong 26 đến 29 s, và bầy tiếp tục đi: tâm bầy di chuyển trung vị 17 m ở $N = 25$, 15 m ở $N = 50$ và 13 m ở $N = 100$ (`cli/diagnostics/hold_walk.py`: 239 trên 240 lượt chạy lại các lượt đã lưu với đích $3{,}0 R_f$, đủ lớn để không cắt ngắn quãng đi; một lượt chó không bao giờ rút xong). Một đích $1{,}9 R_f$ chỉ là 11,8 m ở $N = 25$ và 14,4 m ở $N = 50$, nên những con đi đầu vượt qua mép xa. Dưới $N = 100$, tỷ lệ 99% là mọi con cừu, nên con đầu tiên ra ngoài là kết thúc việc giữ; chó quay lại, lùa bầy từ phía xa và đẩy nó ra xa hơn. Điều này chỉ ra cỡ đích so với quãng đi đó là nguyên nhân của thất bại; bản thân quãng đi chưa được thay đổi để thử.

2. Chó chiếm chỗ làm chó thêm trở nên có hại trên `outlier_rich` $N = 400$ (Hình 3).  
   - Với 3 đến 6 chó, tỷ lệ thành công là 0,925–0,94, chưa quyết định.  
   - Từ $D = 9$ trở lên, mọi đội đến 24 đều được quyết định là không tin cậy: thành công 0,77 ở $D = 9$, 0,65 ở $D = 12$, 0,50 ở $D = 16$.  
   - Có thể là do vòng cung sau bầy chỉ chứa khoảng 10 đến 12 chó cách nhau 2 m (Hình 3); khi gần hoặc vượt số đó, các chó đẩy nhau ra khỏi chỗ trên vòng cung và không thể rời vòng cung để bắt một con cừu tách ra. Điều này chưa được kiểm chứng, và nó không giải thích vì sao thất bại bắt đầu từ 9 chó, hơi dưới số đó.  
   - Trên `wide` và `compact`, những chó thừa không vừa vòng cung đứng phía sau mà không cản đường, và nhiệm vụ vẫn tin cậy đến 24 chó. Vậy thêm chó có gây hại hay không còn tùy bố cục, chứ không chỉ tùy khoảng chỗ mỗi chó chiếm.

![Giữ bầy với chó dạng điểm và chó cách nhau 2 m](../figures/fig36_spacing.png)

**Hình 3: Giữ bầy ở $N = 400$, chó dạng điểm so với chó giữ cách nhau 2 m.** Trên `wide`, các chó thừa đứng phía sau và thành công giữ nguyên; trên `outlier_rich`, nó giảm từ $D = 9$.

- Ký hiệu: tỷ lệ thành công theo $D$ (thang log), chấm xám cho chó dạng điểm và liền xanh cho chó cách nhau 2 m. Dải cam là sức chứa vòng cung ($D_{\mathrm{cap}} \approx 10$–12), đường đứt là $\theta = 0{,}90$, và điểm rỗng là ô có dưới 30 lượt.
- Các khung: `wide` (trái) và `outlier_rich` (phải).

*Dữ liệu:* [results_tables.md: D_min, dmin_f99_hold](../report/results_tables.md#d_min-dmin_f99_hold) và [results_tables.md: D_min, dmin_f99_hold_spacing](../report/results_tables.md#d_min-dmin_f99_hold_spacing).

3. Một đích khoảng 16 đến 19 m giữ được bầy nhỏ với một chó (Hình 4).  
   Bảng 2 cho, với mỗi tỷ lệ, đích nhỏ nhất đã thử mà từ đó một chó được kết luận tin cậy trên mọi bố cục; một khoảng nghĩa là ở đích nhỏ hơn một chó vẫn còn chưa quyết định.
   - Với 99% phải ở lại, ngưỡng là $2{,}5$–$3{,}0 R_f$ (15,5–18,6 m) ở $N = 25$ và $2{,}1$–$2{,}3 R_f$ (16,0–17,5 m) ở $N = 50$. Ở $N = 100$, đích mặc định $1{,}9 R_f$ (17,3 m) đã giữ được bầy với một chó trên ba bố cục; đó là cận trên, vì không thử đích nào nhỏ hơn. Tính bằng mét, các ngưỡng gần nhau, còn tính theo bán kính bầy thì giảm từ khoảng 2,5 xuống 1,9. Quãng đi dự đoán đúng điều này. Một bầy vào đích với con cuối cùng ở mép gần và đi thêm $w$ chỉ giữ được mọi con trong đích nếu bán kính đích lớn hơn khoảng $w/2$ cộng khoảng cách từ con xa nhất đến tâm bầy: 14,3; 15,7 và 17,2 m ở $N = 25$, 50 và 100 (trung vị qua các lượt chạy lại), bằng hoặc thấp hơn một chút so với các ngưỡng quan sát. Sự khớp này phù hợp với việc quãng đi là nguyên nhân; bản thân quãng đi không được thay đổi để thử.
   - Cho phép một số con ở ngoài làm giảm đích cần thiết: ở $N = 25$, cho một con ra ngoài (95%) giảm nó một bước của lưới đã thử, từ 15,5 xuống 14,3 m, và con thứ hai (90%) giảm thêm tối đa một bước nữa, còn 13,0–14,3 m. Ở $N = 50$, cho hai con ra ngoài (95%) là đủ để đích mặc định 14,4 m giữ được bầy, thấp hơn ngưỡng 99% ít nhất 1,6 m.
   - Gần ngưỡng, thêm chó gây hại: ở đâu đích giữ được bầy với dư dả, một chó là đủ và đội lớn hơn cũng làm được. Ở đích hụt một chút so với đó, một chó làm tốt nhất: ở $N = 25$, 90%, $2{,}1 R_f$, một chó tin cậy trên `split` và `outlier_rich`, trong khi trên mọi bố cục các đội từ 3 đến 7 chó trở lên bị kết luận không tin cậy (thành công xuống tới 0,50); ở $N = 50$, 99%, $2{,}1 R_f$, 4 chó bị kết luận không tin cậy trên `wide` và `outlier_rich`. Một lý do khả dĩ: bầy đi xa thêm khoảng một mét trong lúc rút khi có từ hai chó trở lên so với một chó (16,6 m so với 17,5–17,8 m ở $N = 25$), đủ để làm một đích sát ngưỡng thất bại.
   - Ở $N = 100$ chỉ `outlier_rich` cần hơn một chó: 3 ở đích mặc định với 99%, 2 với mọi đích lớn hơn hoặc tỷ lệ nhỏ hơn.
   - Các ô mà ba giao thức giữ bầy dùng chung (đích mặc định ở 99%, và $2{,}5 R_f$ ở 99%) tái lập đúng các lượt của nhau: 2410, 3750 và 7420 lượt chung, cùng kết quả và cùng độ dài.

Bảng 2 liệt kê đích nhỏ nhất đã thử mà từ đó một chó được kết luận tin cậy trên mọi bố cục (giữ bầy một lần thời gian lùa, 6 lần thời gian lùa; "≤" khi đích mặc định $1{,}9 R_f$, đích nhỏ nhất đã thử, đã giữ được):

**Bảng 2: Đích nhỏ nhất đã thử mà từ đó một chó được kết luận tin cậy trên mọi bố cục.**

| Tỷ lệ phải ở lại | $N = 25$ | $N = 50$ | $N = 100$ |
| :--- | :---: | :---: | :---: |
| 99% (ra ngoài: không con nào dưới $N = 100$, một ở 100) | $2{,}5$–$3{,}0 R_f$ = 15,5–18,6 m | $2{,}1$–$2{,}3 R_f$ = 16,0–17,5 m | ≤ $1{,}9 R_f$ = 17,3 m (`outlier_rich` 3) |
| 95% (ra ngoài: một trên 25, hai trên 50, năm trên 100) | $2{,}3 R_f$ = 14,3 m | ≤ $1{,}9 R_f$ = 14,4 m | ≤ $1{,}9 R_f$ = 17,3 m (`outlier_rich` 2) |
| 90% (ra ngoài: hai trên 25, năm trên 50, mười trên 100) | $2{,}1$–$2{,}3 R_f$ = 13,0–14,3 m | ≤ $1{,}9 R_f$ = 14,4 m | ≤ $1{,}9 R_f$ = 17,3 m (`outlier_rich` 2) |

Ở $N = 25$ và 99%, $2{,}5 R_f$ giữ được `compact` và `split` với một chó, còn `wide` (1–2) và `outlier_rich` (1–3) vẫn còn mở; ở $N = 25$ và 90%, $2{,}1 R_f$ giữ được `split` và `outlier_rich` với một chó, còn `compact` và `wide` vẫn là cận dưới ([1]); ở $N = 50$ và 99%, một chó ở $2{,}1 R_f$ chưa quyết định trên mọi bố cục (thành công 0,90–0,94 qua 200 hạt giống).  
*Dữ liệu:* [results_tables.md: dmin_f99_hold_goal](../report/results_tables.md#dmin_f99_hold_goal-dmin_f99_hold--dmin_f99_hold_goal), [results_tables.md: dmin_f99_hold_share](../report/results_tables.md#dmin_f99_hold_share-dmin_f99_hold--dmin_f99_hold_share) và [results_tables.md: quãng đi khi chó rút](../report/results_tables.md#walk-while-the-dogs-withdraw-dmin_f99_hold_goal-at-30-r_f-replay-of-5-stored-seeds-per-cell-every-replay-reproduced-its-stored-trial).

![Giữ bầy nhỏ: tỷ lệ thành công theo bán kính đích](../figures/fig40_hold_goal.png)

**Hình 4: Tỷ lệ giữ bầy thành công theo bán kính đích tính bằng mét, cho mỗi tỷ lệ phải ở lại.** Với 99% phải ở lại, đường của $N = 25$ và 50 tăng trong khoảng 13 đến 17,5 m, còn $N = 100$ đã ở trên $\theta$ ngay ở đích mặc định 17,3 m; cho phép một hai con ra ngoài dời chỗ tăng của bầy nhỏ sang đích nhỏ hơn.

- Ký hiệu: mỗi điểm là trung bình tỷ lệ thành công trên 20 ô của một quy mô bầy và một cỡ đích (4 bố cục × $D = 1, 2, 4, 8, 24$, mỗi ô tính một lần, không tính các điểm giữa mà lượt chạy thích ứng thêm vào). Thanh dọc là khoảng giữa các ô đó, và gần ngưỡng đầu dưới của nó là các đội lớn; ở $N = 100$, đầu dưới là `outlier_rich` với một chó. Xanh dương là $N = 25$, cam $N = 50$, xanh lá $N = 100$; điểm có vòng tròn là đích mặc định $1{,}9 R_f$, và đường đứt là $\theta = 0{,}90$.
- Các khung: 90%, 95% và 99% bầy phải ở trong đích suốt một lần thời gian lùa, từ trái sang phải.

*Dữ liệu:* `results/dmin_f99_hold_share` và `results/dmin_f99_hold_goal` (các điểm $3{,}0 R_f$).

Hoạt ảnh 1 trong [thiết kế nhiệm vụ](task_design_vi.md#nhiệm-vụ-giữ-bầy) chạy lại một chó giữ bầy 25 con trong đích $1{,}9 R_f$, nơi bầy đi ra ngoài, và $3{,}0 R_f$, nơi bầy được giữ.
