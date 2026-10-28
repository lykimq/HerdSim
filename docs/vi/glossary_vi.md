# Bảng thuật ngữ

Các thuật ngữ mà tài liệu HerdSim dùng, mỗi thuật ngữ một định nghĩa ngắn, kèm liên kết tới phần giải thích đầy đủ. Các tài liệu khác liên kết tới đây ở lần dùng đầu tiên của một thuật ngữ thay vì lặp lại định nghĩa. Xem thêm [README](README_vi.md) để có cái nhìn tổng quan về nghiên cứu.

## Mục lục

- [Lượt chạy và thí nghiệm](#lượt-chạy-và-thí-nghiệm)
- [Nhiệm vụ lùa](#nhiệm-vụ-lùa)
- [Bố cục xuất phát và vị trí xuất phát của chó](#bố-cục-xuất-phát-và-vị-trí-xuất-phát-của-chó)
- [Thành công và độ tin cậy](#thành-công-và-độ-tin-cậy)
- [Quy mô đội](#quy-mô-đội)
- [Mô hình cừu và quy tắc chó](#mô-hình-cừu-và-quy-tắc-chó)
- [Biến thể](#biến-thể)
- [Nhiệm vụ gom](#nhiệm-vụ-gom)
- [Bản ghi](#bản-ghi)

## Lượt chạy và thí nghiệm

- Lượt chạy (trial): một lần mô phỏng một đội trên một bầy xuất phát, chạy tới khi thành công, kết thúc sớm hoặc hết giới hạn thời gian.
- Bước (tick): một bước thời gian của lượt chạy; 1 s với mô hình Strömbom, 0,05 s với mô hình Kubo và 0,03 s với mô hình Lama.
- Hạt giống (seed): con số cố định các dòng ngẫu nhiên của một lượt (bầy xuất phát, nhiễu của cừu, nhiễu của chó). Hạt giống $i$ của một ô là hạt giống gốc của giao thức cộng $i$, nên hạt giống $i$ xuất phát từ cùng một bầy ở mọi quy mô đội ([dòng ngẫu nhiên ghép cặp](task_design_vi.md#dòng-ngẫu-nhiên-ghép-cặp)). Một vài hình ghi thẳng hạt giống ngẫu nhiên, ví dụ 2026.
- Hạt giống 0: lượt đầu tiên được lưu của một ô. Phần lớn hoạt ảnh dùng nó để lượt được chiếu không bị chọn vì trông đẹp; chú thích nêu tên mọi hạt giống khác.
- Chạy lại (replay): chạy lại một lượt đã lưu từ cấu hình và hạt giống của nó; kết quả phải khớp đúng với kết quả đã lưu, và HerdSim báo lỗi nếu không khớp.
- Giao thức (protocol): một thí nghiệm, viết thành một tệp YAML trong `protocols/configs/protocols/`. Nó cố định phương pháp, bố cục, quy mô bầy, quy mô đội, quy tắc thành công và thời hạn.
- Tên giao thức: tên của giao thức, ghép từ các phần. `dmin` là nghiên cứu $D_{\min}$ trên nhiệm vụ lùa; `f99` là quy tắc 99% (không có `f99` là quy tắc nghiêm ngặt); `m12`, `m6` và `m3` là thời hạn tính theo số lần thời gian lùa; `s_` là một biến thể độ nhạy; phần cuối là tên biến thể (`fat`, `kubo`, `indep`, `hold`, `big`, `view`, `k05`, `c1.3` và các tên khác). `lama_r50` là nhiệm vụ gom trên đĩa xuất phát bán kính 50, `lama_r50_inf` là như vậy nhưng cảm nhận vô hạn.
- Chiến dịch (campaign): chạy một giao thức vào thư mục kết quả của nó, `results/<tên giao thức>/`, theo từng vòng thêm hạt giống cho các ô còn chưa quyết định ([lấy mẫu thích ứng](task_design_vi.md#3-động-cơ-lấy-mẫu-thích-ứng-tuần-tự-adaptive-sequential-sampling)).
- Lô (batch): 10 hạt giống mà một ô nhận mỗi lần.
- Ô (cell): một phương pháp, bố cục, quy mô bầy $N$ và quy mô đội $D$ (kèm các mức yếu tố nếu có) trong một giao thức, giao thức này cố định thời hạn và quy tắc. Mỗi ô nhận 10 đến 200 lượt.
- Đường cong (curve): các ô của một phương pháp, bố cục, mức yếu tố và $N$ qua các quy mô đội đã thử.
- Lưới (grid): các bố cục, quy mô bầy và quy mô đội mà một giao thức thử.
- Các lượt chạy chính: ba giao thức nghiêm ngặt và ba giao thức 99% ở 12, 6 và 3 lần thời gian lùa, trên $N = 25$ đến 400 và $D = 1$ đến 24; các lưới 99% ở 12 và 6 lần thời gian lùa sau đó được mở rộng lên chín quy mô bầy, tới 566.
- Chạy bổ sung (top-up): một đợt chạy sau thêm hạt giống cho việc so sánh thời gian hoàn thành vào các lưới 99% có sẵn, để quyết định được $D_{\mathrm{sat}}$.
- Lượt chạy độ nhạy: các giao thức thay đổi một thiết lập của các lượt chạy chính (vị trí thả chó, khoảng cách xuất phát, bán kính đích, tốc độ chó, bộ cừu khớp thực địa) và so với một lượt cơ sở trên cùng các hạt giống.

## Nhiệm vụ lùa

- $N$: số cừu; $D$: số chó (quy mô đội).
- Nhiệm vụ lùa: chó gom bầy nếu cần rồi lùa bầy vào một đích hình tròn.
- $R_f$: bán kính bầy đã hiệu chỉnh, cỡ mà một bầy tập trung $N$ con ổn định khi một chó lùa nó ($\sqrt{2}$ lần khoảng cách RMS tới tâm). Nó định cỡ cánh đồng, đích và quãng lùa ([định cỡ](task_design_vi.md#định-cỡ-theo-bán-kính-bầy-đã-hiệu-chỉnh)).
- Giới hạn hiệu chỉnh: khoảng $N = 600$; trên mức đó, bầy được lùa không còn ổn định ở một bán kính, nên các giao thức bầy lớn áp $R_f$ theo mật độ của bầy 566 con.
- Đích: hình tròn bán kính $1{,}9 R_f$ theo mặc định.
- Quãng lùa $l$: từ tâm bầy lúc xuất phát tới tâm đích.
- Thời gian lùa $T_{\mathrm{drive}}$: thời gian một con cừu đi thẳng với 1 m/s cần để đi hết quãng lùa ([thời hạn](task_design_vi.md#thời-hạn-tính-theo-thời-gian-lùa)).
- Thời hạn: giới hạn thời gian của một lượt, tính bằng số lần thời gian lùa: 12, 6 hoặc 3 lần trong nhiệm vụ lùa. Các lượt Kubo dùng giới hạn cố định 500 s và nhiệm vụ gom dùng 5000 s.
- Thời gian hoàn thành: thời gian một lượt thành công cần.
- Thời gian chó: $D$ nhân thời gian hoàn thành, tổng thời gian các chó làm việc.

## Bố cục xuất phát và vị trí xuất phát của chó

- Bố cục: cách đặt cừu lúc xuất phát ([bố cục](task_design_vi.md#bố-cục-xuất-phát-của-bầy)).
- `compact`: một bầy Gauss chặt; mọi con cừu xuất phát trong khoảng cách gom, nên chó bắt đầu bằng việc lùa.
- `wide`: một bầy Gauss có độ trải bằng nửa khoảng cách gom, cắt ở ba lần độ trải, nên khoảng 13% số cừu xuất phát ngoài khoảng cách gom.
- `split`: ba cụm tập trung trên một vòng tròn quanh tâm bầy.
- `outlier_rich`: 80% số cừu trong một lõi tập trung và 20% trên một vành ngoài khoảng cách gom.
- Bố cục phân tán: `wide`, `split` và `outlier_rich`, các bố cục mà chó phải gom trước khi lùa.
- `uniform`: lúc xuất phát của nhiệm vụ gom, mục tiêu và người chăn trải đều trên một đĩa.
- Vị trí xuất phát của chó ([vị trí xuất phát](task_design_vi.md#vị-trí-xuất-phát-của-chó)):
  - `arcs`: mặc định, trên các nửa vòng tròn sau bầy;
  - `ring`: trên các vòng tròn đầy đủ quanh bầy, trừ phía đích;
  - `handler`: mọi chó ở một điểm sau bầy.
- Khoảng cách xuất phát: vòng chó đầu tiên nằm xa hơn con cừu xuất phát xa nhất có thể bao nhiêu, mặc định 30 m.

## Thành công và độ tin cậy

- Quy tắc nghiêm ngặt: một lượt thành công khi mọi con cừu ở trong đích tại một bước.
- Quy tắc 99%: một lượt thành công khi ít nhất 99% số cừu ở trong đích tại một bước.
- Nhiệm vụ giữ bầy: một lượt chỉ thành công khi 99% bầy đã ở trong đích suốt một lần thời gian lùa, trong lúc chó lùi ra ([giữ bầy](task_design_vi.md#nhiệm-vụ-giữ-bầy)).
- $\theta$: ngưỡng tin cậy, 0,90.
- Ô tin cậy: khoảng Clopper–Pearson 99% của tỷ lệ thành công nằm từ $\theta$ trở lên; không tin cậy: nằm dưới; chưa quyết định: vắt qua $\theta$ ([dừng sớm](task_design_vi.md#dừng-sớm-bằng-khoảng-tin-cậy-clopper-pearson-99)).
- Còn mở: vẫn chưa quyết định khi ô đã chạm trần 200 lượt.

## Quy mô đội

- $D_{\min}$: đội tin cậy nhỏ nhất trên một đường cong ([báo cáo, mục 2.1](d_min_report_vi.md#21-khi-nào-một-đội-là-tin-cậy)).
- $D_{\min,\mathrm{low}}$: đội nhỏ nhất có khoảng tin cậy còn chạm $\theta$; đầu dưới của một khoảng.
- Khoảng, viết `3-8`: 8 chó là tin cậy và một đội nhỏ hơn từ 3 trở lên còn chưa quyết định.
- Cận dưới, viết `[5]`: chưa đội nào tin cậy, và $D_{\min}$ ít nhất là 5.
- `none`: mọi đội đã thử tới đỉnh lưới đều không tin cậy.
- $D_{\mathrm{sat}}$: đội tin cậy nhỏ nhất mà không đội tin cậy lớn hơn nào nhanh hơn quá 5% thời gian hoàn thành với độ tin cậy 99% ([các giá trị ranh giới](task_design_vi.md#các-giá-trị-ranh-giới)).
- $D_{\max}$: đội tin cậy lớn nhất dưới $D_{\mathrm{overcrowd}}$, hoặc đội tin cậy lớn nhất. Ở đỉnh lưới nó chỉ là một cận dưới: chưa tìm thấy giới hạn trên.
- $D_{\mathrm{overcrowd}}$: đội đầu tiên mà từ đó hai quy mô đội đã thử liên tiếp đều không tin cậy, tìm ở phía trên $D_{\min}$ (phía trên $D_{\min,\mathrm{low}}$ trên một đường cong chưa có đội tin cậy nào).
- $D_{\mathrm{best}}$ và $D_{\mathrm{crowd}}$: đội nhỏ nhất nhanh bằng đội nhanh nhất, và đội tin cậy đầu tiên trên $D_{\mathrm{best}}$ mà chậm hơn $D_{\mathrm{best}}$. Cùng với các vùng (cải thiện, bão hòa, chật chội, sụp đổ và các vùng khác), chúng được giải thích ở [các vùng](task_design_vi.md#các-vùng).

## Mô hình cừu và quy tắc chó

- Mô hình Strömbom: mô hình cừu của Strömbom et al. (2014) mà HerdSim chạy theo mặc định ([mô hình](models_vi.md#1-mô-hình-bầy-cừu)).
- $r_a$: 2 m, khoảng cách mà dưới mức đó các con cừu đẩy nhau ra.
- $r_s$: 65 m, khoảng cách mà trong đó cừu phản ứng với chó; cừu không có chó nào gần như vậy thì gặm cỏ.
- Khoảng cách gom $f(N) = r_a N^{2/3}$: con cừu xa tâm bầy hơn mức này là con lạc, và chó gom khi còn con cừu nào ở xa như vậy; nếu không, chúng lùa.
- GCM: tâm của cả bầy; $\mathrm{LCM}_i$: tâm các hàng xóm gần nhất của cừu $i$.
- Điểm gom $P_c$ và điểm lùa $P_d$: nơi chó nhắm tới khi gom một con lạc hoặc lùa bầy ([quy tắc đội](models_vi.md#quy-tắc-đội-strombom_multi)).
- Quy tắc đội, `strombom_multi`: quy tắc nhiều chó của HerdSim; các chó gom những con lạc khác nhau, được phân công bằng thuật toán Hungarian, và lùa từ một cung sau bầy.
- `independent`: mỗi chó chạy quy tắc một chó của Strömbom một mình, không có tầng đội.
- FAT (farthest-agent targeting): mọi chó đi sau con cừu xa đích nhất, không phân công và không chuyển giữa gom và lùa.
- Mô hình Kubo (`kubo`): mô hình lực của Kubo et al. (2022), trong đó cừu tăng tốc khi bị đẩy mạnh hơn.
- Chó dạng điểm: chó không có kích thước, như trong các lượt chạy chính, nên hai chó có thể đứng cùng một điểm.
- Chó giữ cách nhau 2 m: không chó nào được tới gần chó khác dưới 2 m; chó nào có bước đi kết thúc gần như vậy thì đứng yên ở bước đó ([chó chiếm chỗ](task_design_vi.md#cản-trở-khi-chó-chiếm-chỗ)).
- Sức chứa vòng cung $D_{\mathrm{cap}}$: số chó giữ cách nhau 2 m vừa trên cung sau bầy.
- Quy tắc dừng: chó đứng yên khi có con cừu nào trong vòng $3 r_a = 6$ m.

## Biến thể

- Giới hạn độ lệch điểm lùa: một biến thể của HerdSim giới hạn điểm lùa ở tối đa $r_s - r_a = 63$ m sau tâm bầy. Nó tác động từ khoảng 992 con và giữ điểm lùa trong khoảng cách phản ứng của cừu khi bầy trên khoảng 1056 con, nơi điểm lùa không giới hạn đã ra ngoài khoảng đó ([giới hạn lùa](models_vi.md#3-lùa-và-giới-hạn-của-nó-với-bầy-lớn)).
- Tầm cảm nhận và chia sẻ: chó chỉ thấy các con cừu trong một tầm, và chia sẻ những gì chúng thấy với không ai, với các chó trong tầm, hoặc với cả đội.
- Bộ cừu khớp thực địa: bộ tham số cừu mà Strömbom et al. (2014) đặt để mô phỏng cừu và chó chăn thật (Hình 5 của họ).

## Nhiệm vụ gom

- Nhiệm vụ gom: nhiệm vụ của Lama và di Bernardo (2024); mục tiêu và người chăn xuất phát trải trên một đĩa bán kính 50, và người chăn đưa mục tiêu vào một đích bán kính 10 ở tâm đĩa ([nhiệm vụ gom](task_design_vi.md#6-nhiệm-vụ-gom-lama-và-di-bernardo-2024)).
- Mục tiêu và người chăn: cừu và chó của nhiệm vụ gom. Mục tiêu không kết bầy.
- Bán kính cảm nhận $\xi$: khoảng cách mà trong đó người chăn cảm nhận mục tiêu và người chăn khác; 10, hoặc vô hạn.
- `targets_lost`: thất bại khi lúc kết thúc một số mục tiêu nằm ngoài tầm của mọi người chăn; `outnumbered`: mọi mục tiêu đều được thấy, nhưng không đủ số vào đích kịp thời.

## Bản ghi

- Băm vật lý (physics hash): bản tóm tắt các thiết lập làm thay đổi kết quả một lượt, bỏ ra ngoài quy mô bầy, mức yếu tố và chiến lược lấy mẫu để một lượt chạy có thể được mở rộng; thư mục có băm khác với giao thức sẽ bị từ chối ([kiến trúc](../codes/architecture.md)).
- Định danh code: băm của code lượt chạy, commit và phiên bản thư viện, ghi lại cho mỗi đợt chạy.
- Đợt chạy (sitting): một lần chạy lệnh chiến dịch trên một thư mục kết quả.
