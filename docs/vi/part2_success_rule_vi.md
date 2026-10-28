# Quy tắc thành công và các thay đổi thiết lập

Phần 2 của báo cáo HerdSim về quy mô đội. [Phần tổng quan](d_min_report_vi.md) gồm tóm tắt, các câu hỏi nghiên cứu, [quy tắc quyết định](d_min_report_vi.md#2-quy-tắc-quyết-định) định nghĩa $D_{\min}$, khoảng và cận dưới của nó, phần thảo luận và [tài liệu tham khảo](d_min_report_vi.md#tài-liệu-tham-khảo). Các thuật ngữ được định nghĩa trong [bảng thuật ngữ](glossary_vi.md).

## 3.4 RQ4: Quy tắc thành công và con cừu cuối cùng

Đòi mọi con cừu vào đích (quy tắc nghiêm ngặt) hay chỉ 99% có khác nhau không? Trên bầy phân tán lớn thì có. Quy tắc 99% không bao giờ cần nhiều chó hơn, và ở sáu đường cong bầy lớn nó có đội tin cậy trong khi quy tắc nghiêm ngặt không có (ý 1). Dưới quy tắc nghiêm ngặt, đội lớn phần lớn thất bại vì vài con cừu cuối cùng, sau khi 99% bầy đã ở trong đích; một biến thể với chó chậm hơn ủng hộ điều này (ý 2 và 3).

1. Quy tắc 99% không bao giờ cần nhiều chó hơn.  
   Ở cả 34 đường cong phân tán mà cả hai quy tắc đều có đội tin cậy, quy tắc 99% cần bằng hoặc ít chó hơn. Ở những đường cả hai đều đã quyết định và khác nhau, mức tiết kiệm là đúng một chó (từ 3 xuống 2 chẳng hạn); trên `outlier_rich` $N = 100$ ở 3 lần thời gian lùa, $D_{\min}$ đi từ khoảng 3–8 xuống 2. Sáu đường cong bầy lớn thất bại dưới quy tắc nghiêm ngặt (bốn `none`, hai còn mở ở 200 lượt) có đội tin cậy dưới quy tắc 99% (hai đã quyết định, ba khoảng hẹp và một khoảng rộng, 4–10).

2. Vì sao đội lớn thất bại dưới quy tắc nghiêm ngặt.  
   Trong 97% số lượt thất bại nghiêm ngặt với 6 chó trở lên ở lượt chạy cơ sở của phần độ nhạy (`dmin_s_base`; 91% ở `dmin_m6`), 99% bầy đã từng ở trong đích trước thời hạn (Hình 2). Một hai con cừu cuối cùng quyết định lượt chạy. Trong một lượt mẫu (`wide` $N = 400$, 16 chó, hạt giống 2), các chó đuổi theo con lạc cuối cùng, đứng vào giữa bầy và đích, và lùa bầy đã vào đích ra ngoài trở lại, hai lần (Hình 2). Phần lớn các lượt thất bại như vậy kết thúc với cả bầy ở ngoài: 286 trong 379 lượt (75%) kết thúc với không con cừu nào trong đích. Khi quy tắc nghiêm ngặt thành công trên `wide` $N = 400$ (6 chó trở lên, `dmin_s_base`), 1% cuối của bầy cần trung vị 460 s sau khi 99% đã vào, so với 2 s trên `wide` $N = 200$ ([bảng theo từng lượt](../report/results_tables.md#single-trials-and-curves-across-folders)).

3. Chó chậm hơn tránh được điều đó.  
   Với chó 1,15 m/s thay vì 1,5 (`dmin_s_dogspeed`), $D_{\min}$ nghiêm ngặt trên `outlier_rich` $N = 400$ giảm từ không có trên lưới xuống 6, và trên `wide` $N = 400$ từ [9] xuống 5. Điều này gợi ý rằng các thất bại nghiêm ngặt này xảy ra ở cuối lượt lùa, tại đích. Chó chậm hơn cũng khác ở giai đoạn gom bầy, nên biến thể này ủng hộ cách hiểu đó chứ chưa chứng minh nó.

![Thành công nghiêm ngặt so với 99%](../figures/fig30_strict_vs_99.png)

**Hình 1: Thành công nghiêm ngặt so với 99%, từng ô, trên cùng các hạt giống.** Ở 40 ô (32 ở $N \ge 200$), tỷ lệ thành công 99% từ 0,90 trở lên trong khi tỷ lệ nghiêm ngặt ở dưới mức đó; ở đó, con cừu cuối cùng có vào được hay không quyết định kết quả nghiêm ngặt.

- Ký hiệu: mỗi điểm là một ô (một bố cục, một $N$ và một $D$), tô màu theo bố cục, với tỷ lệ thành công nghiêm ngặt ở trục hoành và tỷ lệ thành công 99% ở trục tung. Đường chéo là $y = x$, và không điểm nào nằm dưới nó, vì một lượt đưa mọi con cừu vào đích cũng đạt quy tắc 99%. Vùng tô ở góc trên trái chứa 40 ô nói trên.
- Các khung: mỗi khung một thời hạn (12, 6 và 3 lần thời gian lùa), các bố cục phân tán ở $N \ge 100$, với 80, 57 và 33 ô chung có ít nhất 20 hạt giống.

*Dữ liệu:* `results/dmin_m12`, `dmin_m6` và `dmin_m3`; giá trị trong [results_tables.md: strict success](../report/results_tables.md#d_min-by-layout-and-n-strict-success) và [results_tables.md: success at 99 percent](../report/results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

![Con cừu cuối cùng](../figures/fig22_straggler.png)

**Hình 2: Con cừu cuối cùng quyết định.** Với chó 1,5 m/s, bầy tới đích nhưng con cừu cuối cùng thường không vào; với chó 1,15 m/s, gần như mọi lượt đưa được mọi con cừu vào.

- Trái: tỷ lệ các lượt có 6 chó trở lên, mỗi nhóm cột một bố cục và một $N$, mà mọi con cừu đều vào (xanh đậm), mà 99% số cừu đã ở trong đích tại một thời điểm nào đó (gạch chéo), và mà mọi con cừu đều vào khi chó đi 1,15 m/s (cam). Với chó 1,5 m/s, hai cột đầu chênh nhau khoảng 30 điểm.
- Phải: một lượt chạy (`wide` $N = 400$, 16 chó, hạt giống 2), khoảng cách từ tâm bầy đến đích (trên) và số cừu ngoài đích theo thang symlog (dưới). Chó nhanh (xanh) đưa 399 con vào, rồi lùa bầy ra ngoài hai lần khi đuổi con cuối cùng; chó chậm hơn (cam) xong trong một lượt.

*Dữ liệu:* `results/dmin_s_base` và `results/dmin_s_dogspeed`; giá trị trong [results_tables.md: Sensitivity, strict: base / variant](../report/results_tables.md#sensitivity-strict-base--variant).

![Hoạt ảnh một bầy xuất phát được lùa bởi chó nhanh và chó chậm](../gifs/last_sheep.gif)

**Hoạt ảnh 1: Con cừu cuối cùng, chạy lại (`wide`, $N = 400$, 16 chó, hạt giống 2, quy tắc nghiêm ngặt, 6 lần thời gian lùa).** Lượt chạy ở bên phải Hình 2 khi nó diễn ra: chó nhanh để mất con cừu cuối cùng và cả bầy theo nó, chó chậm hơn xong trong một lượt. Cả hai xuất phát từ cùng một bầy, và mỗi lượt chạy lại khớp với lượt đã lưu.

- Trái: chó 1,5 m/s đưa bầy tới đích nhưng còn thiếu một hai con, lùa bầy ra ngoài lần nữa khi đuổi những con đó, rồi hết giờ.
- Phải: chó 1,15 m/s đưa mọi con cừu vào ngay lần đầu.

## 3.5 RQ5: Kết quả nào giữ nguyên khi đổi thiết lập?

Các câu trả lời có phụ thuộc vào những lựa chọn thiết lập không có giá trị thực tế, như nơi chó xuất phát, không? Theo quy tắc 99% thì hầu như không: chỉ một đích nhỏ hơn làm $D_{\min}$ lệch quá khoảng một chó (ý 1 và 3). Theo quy tắc nghiêm ngặt, cùng những thay đổi đó làm $D_{\min}$ thay đổi nhiều, theo cả hai chiều (ý 2).

14 giao thức độ nhạy ở 6 lần thời gian lùa mỗi lần đổi một lựa chọn thiết lập (Hình 3).

1. Dưới quy tắc 99%, $D_{\min}$ hầu như không đổi.  
   Thả chó từ một điểm hoặc từ vòng tròn, đổi khoảng cách xuất phát (15, 30, 60 m), cho chó chậm hơn (1,15 m/s) hay dùng bộ tham số cừu khớp thực địa làm $D_{\min}$ thay đổi nhiều nhất khoảng một chó. Thay đổi lớn nhất là bộ cừu khớp thực địa trên `outlier_rich` $N = 200$, từ 2–3 xuống 1; bộ cừu khớp thực địa chắc chắn làm giảm $D_{\min}$ ở 3 trong 6 đường cong và ở tối đa 5 trong phạm vi các khoảng (`wide` $N = 100$ vẫn là 1).

2. Dưới quy tắc nghiêm ngặt, nó thay đổi nhiều.  
   Cùng những thay đổi đó làm nó dịch theo cả hai chiều. Một số biến một $D_{\min}$ hữu hạn thành "không có trên lưới" hoặc một cận dưới (chẳng hạn `wide` $N = 200$ từ 3 thành none với bộ cừu khớp thực địa, hoặc thành cận dưới [3] với khoảng cách 15). Số khác đưa một cận dưới về một đội hữu hạn: khoảng cách xuất phát 60 m đưa `wide` $N = 400$ từ [9] xuống 6–7 và `outlier_rich` $N = 200$ từ [12] xuống 5, còn chó chậm hơn (1,15 m/s) đưa `outlier_rich` $N = 200$ từ [12] xuống 4. Có thể là do thay đổi nhỏ trong thiết lập làm thay đổi cách con cừu cuối cùng đi vào; điều này chưa được kiểm chứng.

3. Kích thước đích là thiết lập duy nhất có tác động dưới cả hai quy tắc.  
   Với bán kính đích $1{,}5 R_f$ thay vì $1{,}9 R_f$, $D_{\min}$ tăng dưới cả hai quy tắc: dưới quy tắc 99%, `wide` $N = 400$ từ 2–3 lên 5–6 chó, và `outlier_rich` $N = 400$ từ 3 thành none. Một bầy đã ổn định chỉ vừa khít trong đích nhỏ hơn.

![Bản đồ nhiệt độ nhạy](../figures/fig24_sensitivity.png)

**Hình 3: $D_{\min}$ cho từng thay đổi thiết lập ở 6 lần thời gian lùa.** Dưới quy tắc 99%, phần lớn các thay đổi khớp cơ sở trong vòng một chó; dưới quy tắc nghiêm ngặt, nhiều thay đổi thì không.

- Ký hiệu: mỗi ô ghi $D_{\min}$ theo các dạng ở [mục 2.1](d_min_report_vi.md#21-khi-nào-một-đội-là-tin-cậy), một giá trị, một khoảng như `2-3`, hoặc một cận dưới như `[9]`. Xanh đậm hơn là đội lớn hơn; khoảng và cận dưới được tô nhạt vì còn mở; ô gạch ghi "none" không có đội tin cậy đến 16, đỉnh của các lưới này.
- Các hàng: cơ sở, rồi các thay đổi, vị trí thả chó (`handler`, `ring`), khoảng cách xuất phát (15, 60), bán kính đích $1{,}5 R_f$, tốc độ chó 1,15 và bộ cừu khớp thực địa. Nửa trên dùng quy tắc nghiêm ngặt, nửa dưới quy tắc 99%.
- Các cột: bố cục và quy mô bầy ($N = 100, 200, 400$).

*Dữ liệu:* [results_tables.md: Sensitivity, strict: base / variant](../report/results_tables.md#sensitivity-strict-base--variant) và [results_tables.md: Sensitivity, 99 percent: base / variant](../report/results_tables.md#sensitivity-99-percent-base--variant).
