# Quy mô đội để lùa một bầy cừu mô phỏng: Tối thiểu, đủ và quá nhiều chó

*Báo cáo nghiên cứu khoa học dự án HerdSim*  
*Đánh giá thực nghiệm qua 23 giao thức chiến dịch (164.740 lượt chạy mô phỏng) trên các kiến trúc chăn dắt đa tác tử, tiếp theo là 14 giao thức tiếp nối và ba lượt chạy tiếp (162.130 lượt): và hai giao thức của mô hình không gắn kết của Lama và di Bernardo (2024) (40.280 lượt): tổng cộng 39 giao thức và 367.150 lượt chạy, không có lỗi.*  
*(Lưu ý: Các phương trình động lực học vi mô và thuật toán điều phối được trình bày tại [docs/methods/models_vi.md](../methods/models_vi.md). Hình học nhiệm vụ, tính bất biến quy mô và cơ chế lấy mẫu thích ứng được trình bày tại [docs/experiments/task_design_vi.md](../experiments/task_design_vi.md). Báo cáo này tập trung chuyên sâu vào các quy luật mở rộng thực nghiệm, câu trả lời thống kê cho các câu hỏi nghiên cứu, phân tích vi mô cơ chế thất bại và các hàm ý khoa học.)*

---

## Tóm tắt (Abstract)

Cần bao nhiêu tác tử chăn dắt tự hành ($D$) để thu gom và lùa một bầy $N$ con cừu về vùng đích một cách tin cậy trước thời hạn? Quy mô tối thiểu để hoàn thành nhiệm vụ là bao nhiêu ($D_{\min}$), từ ngưỡng nào thì việc bổ sung thêm tác tử không còn mang lại lợi ích gia tốc ($D_{\mathrm{sat}}$), và trong những điều kiện nào sự quá tải tác tử sẽ phá vỡ toàn bộ cấu trúc đàn? Chúng tôi tiếp cận câu hỏi này thông qua khảo sát thực nghiệm quy mô lớn với 39 giao thức chiến dịch, bao gồm 367.150 lượt chạy mô phỏng tất định không phát sinh lỗi. 

Khác với các nghiên cứu trước đây vốn định nghĩa thành công dựa trên tỷ lệ bình quân dễ bị nhiễu bởi các lượt chạy may rủi, nghiên cứu này xác lập $D_{\min}$ dựa trên chuẩn độ tin cậy toán học khắt khe: cận dưới khoảng tin cậy nhị thức Clopper–Pearson hai phía ở mức ý nghĩa 99% phải đạt tối thiểu $90\%$ ($L \ge 0{,}90$). Nhờ động cơ lấy mẫu thích ứng tuần tự tập trung tính toán vào các ô tham số ranh giới (tối đa 200 hạt giống mỗi ô), 23 giao thức ban đầu (164.740 lượt) đã thiết lập bản đồ $D_{\min}$ qua 5 quy mô bầy ($N \in [25, 400]$), 4 hình thái không gian xuất phát (`compact`, `wide`, `split`, `outlier_rich`) và 3 mức áp lực thời hạn ($12\times$, $6\times$, $3\times$ thời gian lùa danh định) dưới cả hai tiêu chí: *chặn giữ tuyệt đối 100%* và *tiếp cận thực tế 99%*. Các chiến dịch tiếp nối tập trung vào tiêu chí 99%, mở rộng quy mô bầy lên $N = 566$ (và khảo sát ngoại biên tới $N = 3200$), phân rã các thành phần thuật toán (công tắc gom/lùa so với tầng phối hợp Hungarian), khảo sát nhiệm vụ giữ đàn (holding), tác tử có thể tích vật lý chiếm chỗ, độ gắn kết xã hội, tầm nhìn hạn chế, và tái lập trực tiếp mô hình mục tiêu Brown phi gắn kết của Lama và di Bernardo (2024).

Các kết quả thực nghiệm và phân tích động lực học vi mô chỉ ra:
1. **Tính bất biến của bầy co cụm**: Với bầy xuất phát tập trung sẵn (`compact`), $D_{\min} \equiv 1$ là một bất biến tuyệt đối trên mọi quy mô ($N = 25$ đến $400$) và mọi thời hạn. Do vận tốc tối đa của cừu bị giới hạn tự nhiên ($1{,}0\text{ m/s}$) và tổng xung lực đe dọa được chuẩn hóa, việc triển khai thêm chó không giúp rút ngắn thời gian lùa.
2. **Quy luật tăng trưởng dưới tuyến tính trên bầy phân tán**: Khi cừu phân tán trên đồng cỏ, $D_{\min} = 1$ cho các bầy nhỏ ($N \le 50$) do diện tích cánh đồng nằm trọn trong tầm cảm nhận tức thời của một chú chó. Trên bầy lớn ($N = 400$), thời hạn thong thả ($12\times$) chỉ đòi hỏi 2 đến 3 chó. Trong không gian log-log, độ dốc tăng trưởng $\alpha = \Delta \log_2 D_{\min} / \Delta \log_2 N$ dao động từ 0,27 đến 0,38 ở thời hạn $12\times$ và 0,38 đến 0,61 ở $6\times$—thấp hơn đáng kể so với giới hạn căn bậc hai $\alpha = 0{,}50$ của mục tiêu phi gắn kết nhờ lực hút xã hội tự nhiên giữa các cá thể cừu.
3. **Áp lực thời hạn chi phối mạnh hơn quy mô bầy**: Siết chặt thời hạn từ $12\times$ xuống $3\times$ làm bùng nổ nhu cầu tác tử trên bố cục `wide` ($N = 400$) từ 2 lên 5–6 chó; mức gia tăng này vượt qua cả tác động của việc nhân bốn kích thước đàn cừu, do thời gian cạn kiệt triệt tiêu khả năng gom cừu tuần tự.
4. **Hiệu ứng cá thể lạc đàn và Nút thắt của tiêu chí nghiêm ngặt**: Trong 97% số lượt thất bại nghiêm ngặt của các đội từ 6 chó trở lên, đàn chó đã đưa được 99% số cừu vào đích an toàn từ trước thời hạn. Sự thất bại bắt nguồn từ việc các chú chó khi đuổi theo 1–2 con cừu lạc cuối cùng đã vô tình đứng chắn cửa chuồng và lùa khối cừu chủ lực ngược ra ngoài. Giảm vận tốc chó xuống mức ôn hòa ($v_{\mathrm{dog}} = 1{,}15\text{ m/s}$) triệt tiêu được xung lực vượt đà này, đưa tỷ lệ thành công nghiêm ngặt trên `outlier_rich` ($N = 400$) từ thất bại toàn diện (`none`) lên $D_{\min} = 6$.
5. **Độ bền vững của tiêu chí tiếp cận 99%**: Tiêu chí 99% phản ánh đúng năng lực điều phối tập thể, duy trì $D_{\min}$ ổn định (lệch tối đa 1 chó) trước mọi biến thiên về quy ước thả chó, cự ly xuất phát và tham số thực địa GPS. Ngược lại, tiêu chí 100% phóng đại độ nhạy giả tạo do chịu ảnh hưởng thái quá bởi hành vi ngẫu nhiên của một cá thể đơn lẻ.
6. **Thất bại của thuật toán tham lam (FAT)**: Chiến lược bám đuổi thuần túy không phối hợp thất bại hoàn toàn ở $N \ge 200$ trên mọi bố cục phân tán (và cả trên bầy tập trung $N = 400$) do hiện tượng dồn cụm tác tử cục bộ.
7. **Ngưỡng bão hòa tốc độ ($D_{\mathrm{sat}}$) và chi phí dư thừa**: Vượt quá $D_{\mathrm{sat}}$, thời gian hoàn thành chỉ cải thiện tối đa 4% trong khi tổng công sức vận hành của đàn chó (`dog_time` $= D \times T$) tăng tỷ lệ thuận với $D$. Dữ liệu đo đạc vi mô chứng minh nhiều chó hơn không làm tăng tổng thời gian chịu đe dọa của cừu, vì việc gom nhanh giúp giảm số giây hoảng loạn tích lũy.
8. **Phân rã kiến trúc điều phối**: Công tắc chuyển đổi hành vi gom/lùa của Strömbom đủ sức gánh vác các bầy độc lập đến $N = 200$, nhưng tầng phân công tối ưu Hungarian là điều kiện tiên quyết để giải quyết bài toán ở $N = 400$.
9. **Sự sụp đổ do thể tích vật lý chiếm chỗ**: Các tác tử dạng chất điểm không bao giờ gây hại cho nhiệm vụ lùa mở. Tuy nhiên, khi các chú chó có thể tích chiếm chỗ vật lý (giữ khoảng cách an toàn $2\text{ m}$), hiện tượng sụp đổ do quá tải xuất hiện rõ nét trên bố cục `outlier_rich` ($N = 400$): tỷ lệ thành công lao dốc từ $D = 9$ và thất bại hoàn toàn đến $D = 24$ do nghẽn vòng cung lùa.
10. **Điểm kỳ dị giải tích tại $N = 1056$**: Khi quy mô bầy vượt qua $N = (r_s / r_a)^2 = (65 / 2)^2 = 1056$ con, cự ly lùa lý thuyết của Strömbom ($r_a\sqrt{N}$) vượt quá tầm phát hiện đe dọa của cừu ($65\text{ m}$), khiến chó đứng ngoài tầm nhìn và cừu ngừng di chuyển. Đặt trần cự ly lùa tại $63\text{ m}$ đã giải cứu bài toán, đưa $D_{\min} = 1$ tới $N = 1131$ trên bầy co cụm.
11. **Tái lập mô hình Lama & di Bernardo (2024)**: Chạy trong cùng một nền tảng mô phỏng, mô hình mục tiêu phi gắn kết tái lập chính xác quy luật căn bậc hai ($\alpha = 0{,}52\text{--}0{,}53$) dưới tầm nhìn vô hạn. Dưới tầm nhìn hạn chế, HerdSim phát hiện ra sự phân tách sâu sắc: thống kê tỷ lệ trung bình của bài báo gốc đạt 0,99 tại 144 mục tiêu chỉ với 11 người chăn vì bình quân hóa che giấu thất bại đuôi (tail risk), trong khi chuẩn Clopper–Pearson 99% của HerdSim đòi hỏi 17 đến 25 người chăn để loại bỏ các lượt thất lạc mục tiêu.

---

## 1. Câu hỏi nghiên cứu và mục tiêu

Các nghiên cứu trước đây về chăn dắt đa tác tử chủ yếu khảo sát các quy mô đội cố định hoặc trên các mục tiêu không liên kết (Pierson và Schwager 2015; Kubo et al. 2022; Lama và di Bernardo 2024). Để xác lập quy luật mở rộng quy mô của đội chăn tối thiểu dưới ảnh hưởng của lực hút bầy đàn, áp lực thời hạn và sự phân tán không gian, nghiên cứu này giải quyết 7 Câu hỏi Nghiên cứu (RQs):

- **RQ1 (Quy luật mở rộng quy mô $N$)**: Quy mô đội tối thiểu $D_{\min}$ tăng trưởng thế nào theo kích thước bầy $N \in [25, 400]$ trên các bố cục không gian và thời hạn khác nhau? Lực hút bầy đàn có làm giảm độ dốc tăng trưởng so với bầy không liên kết ($\sqrt{N}$) hay không?
- **RQ2 (Bố cục hình học so với quy mô dân số $N$)**: Với cùng một thời hạn, yếu tố nào chi phối $D_{\min}$ mạnh mẽ hơn: bố cục xuất phát (co cụm hay phân tán) hay quy mô đàn cừu $N$?
- **RQ3 (Áp lực thời hạn hoàn thành)**: Áp lực thời gian ($12\times \to 6\times \to 3\times$ thời gian lùa) làm dịch chuyển $D_{\min}$ ra sao? Tác động này là tuyến tính hay phi tuyến?
- **RQ4 (Tiêu chí thành công và Hiệu ứng cá thể lạc đàn)**: Tiêu chí nghiêm ngặt 100% khác biệt thế nào so với tiêu chí 99% tiếp cận? Cơ chế vi mô nào gây ra sự sụp đổ thành công của các đội nhiều chó dưới tiêu chí nghiêm ngặt?
- **RQ5 (Tính vững chắc trước các quy ước mô phỏng)**: Các quy luật mở rộng có đứng vững trước những thay đổi về quy ước thiết lập (vị trí thả chó, cự ly xuất phát, bán kính đích, tham số thực địa, vận tốc chó) hay không?
- **RQ6 (Sự cần thiết của phối hợp đa tác tử)**: Một đàn chó hoạt động độc lập không phối hợp (FAT) có thể đạt được $D_{\min}$ hữu hạn ở đàn lớn hay không?
- **RQ7 (Vượt quá $D_{\min}$: đủ chó và quá nhiều chó)**: Từ quy mô đội *D*<sub>sat</sub> nào thì thêm một con chó không còn làm việc lùa nhanh hơn, mỗi con chó vượt quá nó tốn bao nhiêu, nó có thêm áp lực lên cừu không, và có quy mô đội nào làm nhiệm vụ tệ đi không? (Phân tích tiếp theo trên các lượt chạy 99% hiện có; không chạy chiến dịch mới.)

Các chiến dịch tiếp theo (tiêu chí 99% xuyên suốt) bổ sung bảy câu hỏi:

- **RQ8 (Lưới dày hơn và hình dạng đường cong)**: Với chín kích thước bầy đến ngưỡng của mô hình ($N = 566$), $D_{\min}$ và *D*<sub>sat</sub> tăng nhanh thế nào, và có phân biệt được tăng đều với một đường cong chững lại không?
- **RQ9 (Phần nào của quy tắc quan trọng)**: Công tắc gom/lùa và tầng đội mỗi phần đóng góp gì, và một mô hình mà thời gian hoàn thành giảm theo $D$ (Kubo) bão hòa ra sao?
- **RQ10 (Quá nhiều chó)**: Việc giữ bầy trong đích, hay chó chiếm chỗ, có làm cho chó thêm gây hại không?
- **RQ11 (Độ gắn kết)**: Sự tăng của $D_{\min}$ thay đổi thế nào theo độ mạnh của sự gắn kết giữa các con cừu?
- **RQ12 (Chó nhìn thấy gì)**: Tầm cảm nhận giới hạn tốn thêm bao nhiêu chó, và việc chia sẻ những gì các chó thấy có bù lại được không?
- **RQ13 (N lớn)**: Điều gì xảy ra trên kích thước mà bầy của mô hình còn có kích thước riêng?
- **RQ14 (Mục tiêu không gắn kết)**: HerdSim có tái lập được đội tối thiểu, ngưỡng mật độ và quy luật căn bậc hai của Lama và di Bernardo (2024) cho các mục tiêu không tụ bầy không, và quy luật đó có giữ dưới quy tắc tin cậy của HerdSim cũng như dưới thống kê của bài báo không?

---

## 2. Phương pháp luận thống kê và quy tắc quyết định

*(Chi tiết đầy đủ về vòng lặp thích ứng, khoảng tin cậy Clopper–Pearson và hệ thống hạt giống ngẫu nhiên chung CRN được trình bày tại [docs/experiments/task_design_vi.md: Động cơ Lấy mẫu Thích ứng Tuần tự](../experiments/task_design_vi.md#3-động-cơ-lấy-mẫu-thích-ứng-tuần-tự-adaptive-sequential-sampling).)*

### 2.1 Tiêu chí quyết định hình thức cho *D*<sub>min</sub>
Một **ô (cell)** được xác định bởi bộ tham số (phương pháp, bố cục, $N$, thời hạn, $D$). Mỗi lượt chạy mô phỏng là một phép thử Bernoulli độc lập cho ra kết quả thành công ($1$) hoặc thất bại ($0$). Với một mẫu gồm $n_{\mathrm{trials}}$ hạt giống được đánh giá và $k$ lần thành công quan sát được, khoảng tin cậy nhị thức Clopper–Pearson hai phía 99% $[L, U]$ cho xác suất thành công thực tế $p$ được tính toán như sau:

$$
L = B\left(\frac{\alpha}{2}, k, n_{\mathrm{trials}} - k + 1\right), \quad U = B\left(1 - \frac{\alpha}{2}, k + 1, n_{\mathrm{trials}} - k\right)
$$

trong đó:
- $n_{\mathrm{trials}} \in [10, 200]$: Tổng số lượt mô phỏng tích lũy đã chạy cho ô tham số đó.
- $k \in [0, n_{\mathrm{trials}}]$: Số lượt mô phỏng ghi nhận thành công.
- $\alpha = 0{,}01$: Mức ý nghĩa thống kê, tương ứng với độ tin cậy hai phía $1 - \alpha = 99$% (mỗi phía đuôi phân phối chiếm $\alpha/2 = 0{,}005$).
- $B(q, a, b)$: Hàm phân vị (hàm phân phối tích lũy nghịch đảo) của phân phối Beta với hai tham số hình dạng $a$ và $b$, tính tại xác suất tích lũy $q$.
- $L$: Cận dưới thống kê của tỷ lệ thành công thực tế với độ tin cậy 99%.
- $U$: Cận trên thống kê của tỷ lệ thành công thực tế với độ tin cậy 99%.

Với ngưỡng tin cậy mục tiêu quy định là $\theta = 0{,}90$:
- **Đạt độ tin cậy (Reliable)**: $L \ge 0{,}90$. Chúng ta có độ tin cậy toán học 99% rằng tỷ lệ thành công thực tế đạt ít nhất 90% (đòi hỏi tối thiểu 51 trận thắng liên tiếp không có trận thua nào, được làm tròn thành 60 lượt chạy với kích thước lô 10).
- **Không đạt tin cậy (Unreliable)**: $U \lt 0{,}90$. Chúng ta tin cậy 99% rằng ô này không thể đạt ngưỡng 90%, kích hoạt cơ chế dừng sớm để tiết kiệm thời gian (thường dừng sau 10–20 lượt).
- **Chưa quyết định (Undecided)**: $L \lt 0{,}90 \le U$. Khoảng tin cậy vẫn đang bao trùm ngưỡng 90%, ô sẽ tiếp tục nhận các lô 10 hạt giống tiếp theo cho đến trần tối đa 200 hạt giống.

Trên một đường cong kiểm thử theo số lượng chó $D \in \mathcal{D}$:

$$
D_{\min} = \min \lbrace D \in \mathcal{D} \mid \mathrm{Cell}(D) \text{ is Reliable} \rbrace
$$

$$
D_{\min,\mathrm{low}} = \min \lbrace D \in \mathcal{D} \mid U(D) \ge \theta \rbrace
$$

- **Giá trị quyết định**: Khi $D_{\min,\mathrm{low}} = D_{\min}$, mọi $D \lt D_{\min}$ đều chắc chắn không đạt tin cậy ($U \lt 0{,}90$).
- **Khoảng chặn ($[D_{\min,\mathrm{low}}, D_{\min}]$)**: Khi $D_{\min}$ đạt tin cậy nhưng vẫn còn một số $D$ nhỏ hơn ở trạng thái chưa quyết định tại mốc 200 hạt giống (ví dụ `3-8`).
- **Cận dưới ($[n]$)**: Chưa có $D$ nào đạt tin cậy nhưng tồn tại $D \ge n$ chưa quyết định.
- **Thất bại (`none`)**: Toàn bộ các giá trị $D$ trên lưới kiểm thử (đến $D = 24$ ở các lượt chạy chính) đều chắc chắn không đạt độ tin cậy ($U \lt 0{,}90$).

### 2.2 Tổng quan ma trận giao thức thực nghiệm
Nghiên cứu đầu tiên bao gồm 23 giao thức (164.740 lượt chạy, 20 luồng worker, 0 lỗi):
- **Lưới chính (6 giao thức)**: Đánh giá đầy đủ 5 quy mô ($N \in [25, 400]$), 4 bố cục (`compact`, `wide`, `split`, `outlier_rich`), và 3 thời hạn ($12\times, 6\times, 3\times$ thời gian lùa) dưới cả hai tiêu chí Nghiêm ngặt 100% và Tiếp cận 99%.
- **Đối chứng không phối hợp (2 giao thức)**: `dmin_fat` và `dmin_f99_fat` ở thời hạn $6\times$.
- **Mô hình lực liên tục Kubo (1 giao thức)**: `dmin_kubo` trên bầy co cụm ($N \in [25, 100]$).
- **Bộ kiểm tra độ nhạy (14 giao thức)**: Đánh giá ở thời hạn $6\times$, một mốc cơ sở và 6 biến thể (cọc handler, vòng tròn ring, khoảng cách khởi đầu 15/60 so với mốc 30, bán kính đích $1{,}5 R_f$, tham số thực địa GPS, và tốc độ chó 1,15) dưới cả hai tiêu chí.

Phần tiếp theo bổ sung 14 giao thức và chạy tiếp ba lưới 99% (162.130 lượt, 0 lỗi, chỉ tiêu chí 99%), được liệt kê cùng RQ8–RQ13 và trong phụ lục. Hai giao thức của mô hình Lama và di Bernardo trên nhiệm vụ gom (40.280 lượt, 0 lỗi) trả lời RQ14.

---

## 3. Kết quả Thực nghiệm và Phân tích Cơ chế Chuyên sâu

### 3.1 RQ1: Quy luật mở rộng của Quy mô đội tối thiểu *D*<sub>min</sub> theo Quy mô đàn cừu *N*

Bài toán mở rộng quy mô (scaling) đặt ra một câu hỏi nền tảng: *Khi đàn cừu tăng gấp nhiều lần, số lượng chó chăn dắt cần thiết tăng trưởng tuyến tính, dưới tuyến tính, hay đột biến phi tuyến?* Kết quả từ 23 giao thức ban đầu và các lưới bổ sung mang lại cái nhìn sâu sắc:

- **Bầy tập trung (`compact`) — Bất biến tuyệt đối của trạng thái co cụm**: Khi bầy cừu khởi đầu ở trạng thái đã liên kết chặt chẽ, $D_{\min} \equiv 1$ duy trì như một hằng số bất biến trên mọi quy mô khảo sát ($N = 25$ đến $400$) và xuyên suốt cả ba mức thời hạn. Một chú chó duy nhất là đủ để áp đặt hướng di chuyển lên cả bầy mà không cần bất kỳ sự trợ giúp nào. Quan trọng hơn, việc điều động thêm chó không hề giúp đàn cừu về đích nhanh hơn: trung vị thời gian hoàn thành luôn dao động ổn định trong khoảng 1,44 đến 1,74 lần thời gian lùa danh định ($T_{\mathrm{drive}}$) cho mọi quy mô đội $D \in [1, 24]$.
- **Bầy phân tán (`wide`, `split`, `outlier_rich`) — Tính kinh tế theo quy mô**: Khi bầy cừu bị xé lẻ trên đồng cỏ, quy mô đội tối thiểu mở rộng **dưới tuyến tính (sub-linear)** theo $N$. Đáng chú ý, ở quy mô nhỏ ($N \le 50$), $D_{\min} = 1$ vẫn đủ sức gom và lùa thành công trên mọi hình thái phân tán dưới thời hạn thong thả và trung bình. Bản chất của hiện tượng này không nằm ở thuật toán gom bầy đặc biệt, mà xuất phát từ **hiệu ứng biên hình học**: với $N \le 50$, bán kính đàn chỉ $R_f \le 7{,}6\text{ m}$ và toàn bộ cánh đồng xuất phát nằm trọn trong tầm cảm nhận tức thời ($r_s = 65\text{ m}$) cũng như tốc độ bao quát ($1{,}5\text{ m/s}$) của một chú chó. Chỉ khi bầy cừu mở rộng lên $N = 400$ ($R_f = 11{,}4\text{ m}$, cánh đồng trải rộng hàng trăm mét), sự phân hóa mới xuất hiện rõ nét: thời hạn thong thả ($12\times$) đòi hỏi 2 đến 3 chó, trong khi thời hạn trung bình ($6\times$) đẩy ranh giới lên 2 đến 3 chó (dưới tiêu chí 99%) hoặc dẫn đến thất bại toàn diện (dưới tiêu chí 100%).

Bảng 1 tổng hợp ma trận ranh giới $D_{\min}$ (đối chiếu giữa tiêu chí Nghiêm ngặt 100% và Tiếp cận 99%):

| Thời hạn | Bố cục | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **12&times;** | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| **12&times;** | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 2 / 1–2 | 3 / 2 |
| **12&times;** | `split` | 1 / 1 | 1 / 1 | 1 / 1 | 1–2 / 1 | 3 / 2 |
| **12&times;** | `outlier_rich` | 1 / 1 | 1 / 1 | 1–3 / 1–2 | 2 / 2 | 3 / 2 |
| **6&times;** | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| **6&times;** | `wide` | 1 / 1 | 1 / 1 | 1 / 1 | 3 / 2 | [9] / 2–3 |
| **6&times;** | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / [1] | none / [5] |
| **6&times;** | `outlier_rich` | 1 / 1 | 1 / 1 | 3 / 2 | [12] / 2–3 | none / 3 |
| **3&times;** | `compact` | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| **3&times;** | `wide` | 1 / 1 | 1 / 1 | 3 / 2 | none / 3 | none / 5–6 |
| **3&times;** | `split` | 1 / 1 | 1 / 1 | 1 / 1 | none / none | none / none |
| **3&times;** | `outlier_rich` | 1 / 1 | 1 / 1 | 3–8 / 2 | none / 4–10 | none / [6] |

*Nguồn số liệu:* Tra cứu tại [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success) (`dmin_m12`, `dmin_m6`, `dmin_m3`) và [results_tables.md: 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent) (`dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3`).

![Quy mô D_min theo số cừu N](../figures/fig20_dmin_vs_n.png)

**Hình 1: Động lực học mở rộng quy mô của $D_{\min}$ theo số lượng cừu $N$ qua các mức thời hạn và bố cục xuất phát.**  
Biểu đồ ba khung thể hiện quỹ đạo ranh giới theo thời hạn giảm dần ($12\times \to 6\times \to 3\times$) trong hệ tọa độ log-log. Đường nét liền (tiêu chí 100%) và nét đứt (tiêu chí 99%) chạy song song ở quy mô nhỏ nhưng tách rời dữ dội khi $N \ge 100$: các đường 100% uốn cong dốc đứng và rơi vào trạng thái thất bại toàn diện ("none"), trong khi các đường 99% mở rộng thoai thoải và ổn định tới $N = 566$. Vùng bóng mờ dọc thể hiện các khoảng chặn chưa ngã ngũ tại trần 200 hạt giống (ví dụ $[3, 8]$).

![Thời gian hoàn thành trên bầy Compact](../figures/fig31_compact.png)

**Hình 2: So sánh cơ chế vận hành trên bầy xuất phát tập trung giữa hai trường phái vật lý.**  
Khung trái minh họa mô hình Strömbom với quy tắc đội `strombom_multi`: thời gian lùa hoàn toàn đi ngang vì cừu di chuyển ở vận tốc trần tự nhiên ($1{,}0\text{ m/s}$) và tổng vector đe dọa được chuẩn hóa về đơn vị, khiến thêm chó không thể gia tăng áp lực đẩy. Khung phải minh họa mô hình trường thế liên tục Kubo et al. (2022): do lực đẩy repulsive mang tính cộng dồn phi tuyến theo khoảng cách ($1/r^3$), đội hình đông chó nén bầy cừu mạnh hơn và đẩy thời gian hoàn thành từ $115\text{ s}$ (1 chó) lao dốc xuống $29\text{ s}$ (10 chó) tại $N = 100$.

Bảng 2 trình bày các hệ số góc tăng trưởng log-log thực nghiệm ($\alpha$ trong quan hệ $D_{\min} \propto N^\alpha$):

| Tiêu chí | Thời hạn | Độ dốc `wide` | Độ dốc `split` | Độ dốc `outlier_rich` |
| :--- | :---: | :---: | :---: | :---: |
| **Nghiêm ngặt 100%** | $12\times$ | 0,42 | 0,32 đến 0,42 | 0,42 |
| **Nghiêm ngặt 100%** | $6\times$ | 0,48 ($N \le 200$) | Đi ngang ($N \le 100$) | 0,79 ($N \le 100$) |
| **Nghiêm ngặt 100%** | $3\times$ | 0,79 ($N \le 100$) | Đi ngang ($N \le 100$) | 0,79 đến 1,50 ($N \le 100$) |
| **Tiếp cận 99%** | $12\times$ | 0,20 đến 0,30 | 0,20 | 0,30 |
| **Tiếp cận 99%** | $6\times$ | 0,30 đến 0,42 | Đi ngang ($N \le 100$) | 0,42 đến 0,48 |
| **Tiếp cận 99%** | $3\times$ | 0,62 đến 0,68 | Đi ngang ($N \le 100$) | 0,70 đến 1,10 ($N \le 200$) |

*Nguồn số liệu:* [results_tables.md: Growth with N, strict](results_tables.md#growth-with-n-strict) và [results_tables.md: Growth with N, 99 percent](results_tables.md#growth-with-n-99-percent).

**Bản chất cơ chế của Hệ số góc Log-Log ($\alpha$):**
1. **Lợi thế quy mô từ lực hút bầy đàn tự nhiên**:  
   Trong bài toán thu gom các hạt Brown rời rạc hoặc rác thải độc lập bằng robot, cận dưới lý thuyết luôn đòi hỏi $\alpha = 0{,}50$ ($D \propto \sqrt{M}$). Ngược lại, đối với bầy cừu gắn kết ở thời hạn thong thả ($12\times$), độ dốc thực nghiệm giảm mạnh xuống **0,20 đến 0,30** (dưới tiêu chí 99%). Điều này phản ánh rõ nét bản chất sinh học: lực hút xã hội ($c = 1{,}05$, tương tác $n = N - 1$) tự động kéo các cá thể về phía nhau. Người chăn dắt không cần phải "nhặt" từng con cừu; chỉ cần lùa các cá thể ngoài rìa vào tầm mắt của bầy, lực hút tập thể sẽ tự động làm nốt phần việc còn lại.
2. **Cơ chế bẻ gãy tính kinh tế quy mô dưới áp lực thời gian**:  
   Khi thời hạn bị siết chặt xuống $3\times$, độ dốc $\alpha$ vọt lên **0,62 đến 1,50**. Khi đồng hồ đếm ngược gấp gáp, khoảng thời gian để cừu tự co cụm bị triệt tiêu hoàn toàn. Một chú chó không thể gom tuần tự từng cụm mà toàn đội buộc phải phân tán song song để chặn các hướng tháo chạy cùng lúc. Áp lực thời gian đã lấn át cơ chế tự gắn kết tự nhiên, đẩy chi phí tác tử tiến thẳng về (hoặc vượt qua) mức tăng trưởng tuyến tính.

---

### 3.2 RQ2: Sự phân tán không gian so với Quy mô bầy: Yếu tố nào chi phối mạnh hơn?

**Đo lường độ phân tán thông qua "Số lần tăng đôi" (Doublings) trong Bảng 3**:
Vì quy mô bầy là biến số liên tục ($N \in [25, 400]$) trong khi các bố cục là các hình thái rời rạc (`compact`, `wide`, `split`, `outlier_rich`), chúng tôi so sánh mức độ tác động của chúng trên cùng một thước đo: số lần tăng gấp đôi ($\log_2$ span của $D_{\min}$):

$$
\text{Độ phân tán (doublings)} = \log_2 \left( \frac{D_{\min,\max}}{D_{\min,\min}} \right)
$$

Độ phân tán được lấy qua các bố cục tại mỗi $N$ rồi lấy trung bình theo $N$ (và qua các $N$ tại mỗi bố cục rồi lấy trung bình theo bố cục), dùng trung điểm nhân của khoảng chặn; các đường cong không có $D$ tin cậy nào trên lưới bị loại ra.

Bảng 3 so sánh mức độ phân tán định lượng:

| Tiêu chí | Thời hạn | Biến thiên qua các Bố cục (Cố định $N$) | Biến thiên qua $N$ (Cố định Bố cục) | Yếu tố chi phối |
| :--- | :---: | :---: | :---: | :--- |
| **Nghiêm ngặt** | $12\times$ | 0,68 doublings | 1,19 doublings | Quy mô bầy $N$ |
| **Nghiêm ngặt** | $6\times$ | 1,67 doublings | 1,69 doublings | Ngang nhau / Quy mô $N$ |
| **Nghiêm ngặt** | $3\times$ | 0,76 doublings | 0,97 doublings | Quy mô bầy $N$ |
| **99%** | $12\times$ | 0,50 doublings | 0,75 doublings | Quy mô bầy $N$ |
| **99%** | $6\times$ | 0,92 doublings | 1,30 doublings | Quy mô bầy $N$ |
| **99%** | $3\times$ | 1,25 doublings | 1,28 doublings | Ngang nhau / Quy mô $N$ |

Số liệu: tính từ các bảng số lần gấp đôi trong [Growth with N, strict](results_tables.md#growth-with-n-strict) và [Growth with N, 99 percent](results_tables.md#growth-with-n-99-percent).

**Kết luận cốt lõi từ Bảng 3**:
1. **Quy mô bầy $N$ là yếu tố chi phối hàng đầu**: Trong hầu hết điều kiện, sự biến thiên do tăng số lượng cừu luôn vượt qua sự biến thiên do thay đổi bố cục (trung bình 0,75 đến 1,69 lần tăng đôi so với 0,50 đến 1,67 lần tăng đôi).
2. **Tác động của bố cục chỉ mang tính nhị phân**: Gần như toàn bộ sự khác biệt giữa các bố cục bắt nguồn từ một bước chuyển duy nhất: chuyển từ **bầy đã co cụm sẵn (`compact`)** sang **đồng cỏ phân tán**. Dưới tiêu chí 99% ở $12\times$, việc cừu phân bố đều (`wide`) hay có cá thể lạc xa (`outlier_rich`) hiếm khi làm nhu cầu chênh quá 1 chó. Dưới tiêu chí nghiêm ngặt ở $6\times$ hai bố cục chênh nhau nhiều (3 so với [12] ở $N = 200$), và `split` có thể thất bại hoàn toàn trong khi hai bố cục kia có $D_{\min}$ hữu hạn.

---

### 3.3 RQ3: Áp lực thời hạn làm dịch chuyển *D*<sub>min</sub> như thế nào?

Áp lực thời hạn đóng vai trò như một hệ số nhân phi tuyến đối với $D_{\min}$, làm biến đổi căn bản phương thức phối hợp của bầy chó chăn dắt:

1. **Hiệu ứng phi tuyến của ngân sách thời gian**:  
   Dưới tiêu chí 99% trên các bố cục `wide` và `outlier_rich`, việc nới lỏng thời hạn từ $6\times$ lên $12\times$ chỉ giúp tiết kiệm tối đa 1 chú chó (dù dưới tiêu chí nghiêm ngặt và trên `split` mức chênh lệch lớn hơn do tính nhạy cảm biên). Tuy nhiên, khi siết chặt thời hạn từ $6\times$ xuống $3\times$, nhu cầu số lượng chó bùng nổ mạnh mẽ: trên `wide` $N = 400$, $D_{\min}$ nhảy vọt từ 2–3 lên 5–6 chó; trên `split` $N \ge 200$, thời hạn gấp gáp dẫn tới sự thất bại toàn diện trên mọi quy mô đội hình khảo sát ($D \le 24$).

2. **Cơ chế vật lý từ gom tuần tự sang bao vây song song**:  
   Sự phi tuyến này bắt nguồn từ giới hạn động học hữu hạn của cả hai loài tác tử ($v_{\mathrm{sheep}} = 1{,}0\text{ m/s}$, $v_{\mathrm{dog}} = 1{,}5\text{ m/s}$). Ở mốc thong thả $12\times$, quỹ thời gian $T_{\mathrm{budget}} = 12 \times (d_{\mathrm{start}} / v_{\mathrm{sheep}})$ đủ lớn để một chú chó duy nhất có thể tuần tự tiếp cận từng cá thể cừu lạc, lùa nó nhập vào bầy chính rồi mới chuyển sang mục tiêu tiếp theo. Ngược lại, tại $3\times$, tổng quãng đường di chuyển tuần tự vượt quá giới hạn vật lý của một cá thể trong thời gian cho phép; đàn chó bắt buộc phải chuyển sang chế độ phối hợp song song, phân chia đồng thời các phân khu không gian để chặn đứng đà tản mác của bầy cừu ngay từ những giây đầu tiên.

![Tác động của thời hạn](../figures/fig29_deadline.png)

**Hình 3: Tác động phi tuyến của áp lực thời hạn lên đường cong xác suất thành công và ranh giới $D_{\min}$.**  
*(Khung trái & giữa)* Tỷ lệ thành công kèm khoảng tin cậy Clopper-Pearson 99% theo số chó $D$ trên bố cục `wide` $N = 400$ (trái) và `outlier_rich` $N = 200$ (giữa) qua ba mốc thời hạn: $12\times$ (xanh nhạt), $6\times$ (xanh vừa) và $3\times$ (xanh đậm); đường chấm ngang đánh dấu ngưỡng tin cậy $\theta = 0{,}90$.  
*(Khung phải)* Quỹ đạo $D_{\min}$ (thang log) theo thời hạn cho `wide` và `outlier_rich` tại $N = 200$ (nét liền, tròn) và $N = 400$ (nét đứt, vuông); điểm rỗng biểu thị cận dưới của các ô chưa ngã ngũ. Khi ngân sách thời gian bị siết chặt, đường cong dịch chuyển phi tuyến sang phải do đòi hỏi bắt buộc phải phân công nhiệm vụ song song.  
*Số liệu:* `results/dmin_f99_m12`, `dmin_f99_m6` và `dmin_f99_m3`; chi tiết $D_{\min}$ tra cứu tại [results_tables.md: D_min by layout and N, success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

---

### 3.4 RQ4: Tiêu chí thành công và "Hiệu ứng cá thể lạc đàn" (Straggler Effect)

Sự khác biệt giữa tiêu chí tiếp cận 99% và tiêu chí nghiêm ngặt 100% không đơn thuần là một lựa chọn kỹ thuật về ngưỡng cắt thống kê, mà định hình sâu sắc cơ chế vật lý được đo lường:

1. **Độ lệch có hệ thống giữa hai tiêu chí**:  
   Tiêu chí 99% đòi hỏi số chó bằng hoặc ít hơn tiêu chí nghiêm ngặt 100% trên toàn bộ 34 ô bầy phân tán mà cả hai tiêu chí đều xác định được $D_{\min}$ hữu hạn. Tại các ô đã phân định dứt khoát, mức tiết kiệm thường là đúng 1 chú chó (ví dụ từ 3 xuống 2); riêng `outlier_rich` $N = 100$ ở $3\times$, $D_{\min}$ rút gọn từ khoảng chặn $[3, 8]$ xuống còn 2 chó. Đáng chú ý nhất, 6 ô bầy lớn hoàn toàn không thể đạt độ tin cậy dưới tiêu chí nghiêm ngặt (4 ô ghi nhận `none`, 2 ô còn mở) lại đạt độ tin cậy ổn định dưới tiêu chí 99% (2 ô phân định dứt khoát, 4 ô dạng khoảng chặn hẹp).

2. **Bản chất vi mô của Hiệu ứng cá thể lạc đàn (Straggler Effect)**:  
   Phân tích dữ liệu vi mô giải thích vì sao tiêu chí tuyệt đối thất bại trên các đàn lớn: trong **97% số lượt thất bại nghiêm ngặt** của các đội đông chó ($D \ge 6$) ở bộ thử cơ sở (`dmin_s_base`; 91% ở `dmin_m6`), **99% số cừu thực chất đã nằm gọn trong chuồng đích trước hạn chót**.  
   Hiện tượng nghịch lý này xảy ra do động học tiếp cận cửa chuồng: khi một đội 16 chú chó di chuyển ở vận tốc $1{,}5\text{ m/s}$ dồn lực truy đuổi 1–2 cá thể cừu cứng đầu còn sót lại bên ngoài, vị trí lùa đàn theo thuật toán buộc đàn chó phải chạy vòng ra sau lưng con cừu lạc. Động thái này vô tình đưa đàn chó tiến sát cửa chuồng, cắt ngang giữa đích đến và bầy cừu chủ lực đã vào chuồng trước đó. Lực đẩy hoảng loạn từ bầy chó đông đúc đã lùa ngược khối cừu 99% bên trong văng trở lại đồng cỏ mở, biến một nhiệm vụ gần như hoàn tất thành thất bại thảm hại.

3. **Giải trừ hiệu ứng bằng điều chỉnh vận tốc**:  
   Khi hạ tốc độ chó xuống mức điềm tĩnh hơn ($v_{\mathrm{dog}} = 1{,}15\text{ m/s}$), quán tính vượt ngưỡng cửa chuồng bị triệt tiêu hoàn toàn. Đàn chó tiếp cận cá thể lạc với gia tốc vừa phải, không tạo ra sóng xung kích đẩy bầy chính ra ngoài. Sự can thiệp này lập tức cứu vãn kịch bản `outlier_rich` $N = 400$ từ thất bại hoàn toàn (`none`) đạt thẳng tới $D_{\min} = 6$. Điều này khẳng định rằng thất bại ở tiêu chí nghiêm ngặt là một **tạo tác biên cục bộ (boundary artifact)** của bài toán đóng chuồng, chứ không phản ánh sự thiếu hụt năng lực kiểm soát bầy đàn tổng thể.

![Strict so với 99%](../figures/fig30_strict_vs_99.png)

**Hình 4: So sánh từng ô tham số giữa tiêu chí nghiêm ngặt 100% và tiêu chí tiếp cận 99% trên cùng tập hạt giống ngẫu nhiên.**  
Mỗi khung biểu diễn một mức thời hạn ($12\times$, $6\times$, $3\times$) cho các bố cục phân tán tại $N \ge 100$ (tương ứng 80, 57 và 33 ô có ít nhất 20 hạt giống chung). Trục hoành là tỷ lệ thành công nghiêm ngặt; trục tung là tỷ lệ thành công 99%; đường chéo biểu thị mức cân bằng $y = x$. Vùng bóng mờ phía trên bên trái chứa 40 ô (trong đó 31 ô tại $N \ge 200$) đạt độ tin cậy $\ge 90$% dưới tiêu chí 99% nhưng lại trượt dưới tiêu chí nghiêm ngặt. Tại vùng này, chính hành vi ngẫu nhiên của cá thể lạc cuối cùng, chứ không phải năng lực điều phối bầy, đã thao túng kết quả đánh giá.  
*Số liệu:* `results/dmin_m12`, `dmin_m6` và `dmin_m3`; đối chiếu chi tiết tại [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success) và [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

![Cơ chế cá thể lạc đàn](../figures/fig22_straggler.png)

**Hình 5: Động học vi mô giải thích Hiệu ứng cá thể lạc đàn tại khu vực cửa chuồng.**  
*(Khung trái)* Tỷ lệ các lượt chạy đưa được 99% cừu vào đích so với tỷ lệ đạt 100% tuyệt đối cho các đội $D \ge 6$. Với chó chạy nhanh ($1{,}50\text{ m/s}$), khoảng cách chênh lệch này lên tới 97%, trong khi chó chạy điềm tĩnh ($1{,}15\text{ m/s}$) xóa bỏ hoàn toàn sự cách biệt.  
*(Khung phải)* Quỹ đạo thời gian của một lượt chạy điển hình (`wide` $N = 400$, 16 chó, hạt giống 2): đồ thị trên thể hiện khoảng cách từ tâm bầy đến đích; đồ thị dưới thể hiện số cừu ngoài đích (thang đối xứng symlog). Chó chạy nhanh (xanh dương) đưa được 399 con vào chuồng, nhưng pha truy đuổi con cừu cuối cùng đã đẩy ngược bầy cừu ra ngoài chuồng tới hai lần liên tiếp. Chó chạy điềm tĩnh (cam) giữ nguyên cấu trúc vòng cung và hoàn tất nhiệm vụ chỉ trong một lượt tiếp cận duy nhất.  
*Số liệu:* `results/dmin_s_base` và `results/dmin_s_dogspeed`; tra cứu tại [results_tables.md: Sensitivity, strict: base / variant](results_tables.md#sensitivity-strict-base--variant).

---

### 3.5 RQ5: Những quy luật mở rộng nào đứng vững trước các biến thể kiểm tra độ nhạy?

Đánh giá độ nhạy trên 14 bộ giao thức kiểm chứng tại thời hạn $6\times$ làm sáng tỏ sự tương phản sâu sắc về tính bền vững giữa hai tiêu chí đánh giá:

1. **Tính bất biến của ranh giới dưới tiêu chí 99%**:  
   Dưới tiêu chí 99%, quy luật mở rộng thể hiện sức bền cơ học phi thường. Trước hàng loạt xáo trộn thực nghiệm—bao gồm phương thức bố trí xuất phát của chó (`handler`, `ring`, `arcs`), khoảng cách xuất phát ban đầu ($15, 30, 60\text{ m}$), vận tốc di chuyển của chó ($1{,}15$ so với $1{,}50\text{ m/s}$), và cả bộ tham số cừu sinh học thu nhận từ vòng đeo cổ GPS ngoài thực địa—giá trị $D_{\min}$ chỉ biến thiên trong biên độ hẹp đúng **$\pm 1$ chú chó** so với mốc cơ sở (độ lệch lớn nhất xảy ra ở bộ tham số matched trên `outlier_rich` $N = 200$, chuyển từ 1 lên 2–3 chó).

2. **Sự mong manh của tiêu chí nghiêm ngặt 100%**:  
   Trái ngược hoàn toàn, dưới tiêu chí 100%, giá trị $D_{\min}$ dao động dữ dội gấp 3 lần hoặc sụp đổ hoàn toàn sang trạng thái `none`. Những xáo trộn hình học rất nhỏ ở cự ly xuất phát làm sai lệch pha tiếp cận ban đầu, khiến con cừu lạc cuối cùng bị đẩy vào các quỹ đạo thoát hiểm ngẫu nhiên không thể đảo ngược.

3. **Nút thắt hình học chuồng đích**:  
   Trong số tất cả các biến thể thử nghiệm, việc thu hẹp bán kính chuồng đích từ $2{,}0 R_f$ xuống $1{,}5 R_f$ là yếu tố duy nhất làm tăng mạnh $D_{\min}$ dưới cả hai tiêu chí (dưới tiêu chí 99%, đẩy cấu hình `wide` $N = 400$ từ 2–3 lên 5–6 chó). Khi diện tích đích bị bóp nghẹt, mật độ cừu trong chuồng tăng cao làm bùng nổ lực đẩy nội tại giữa các cá thể cừu ($f_{\mathrm{rep}}$), đòi hỏi một vòng vây chó dày đặc hơn nhiều ở bên ngoài để giữ bầy không trào ngược ra.

![Bản đồ nhiệt độ nhạy](../figures/fig24_sensitivity.png)

**Hình 6: Bản đồ nhiệt đánh giá tính bền vững của $D_{\min}$ qua các biến thể độ nhạy ở thời hạn $6\times$.**  
Nửa trên thể hiện tiêu chí nghiêm ngặt 100%; nửa dưới thể hiện tiêu chí 99%. Các hàng biểu diễn các biến thể về cấu hình xuất phát (`handler`, `ring`), cự ly xuất phát (`gap 15`, `gap 60`), kích thước chuồng nhỏ (`goal 1.5 R_f`), tốc độ chó điềm tĩnh (`dog speed 1.15`), và tham số thực địa GPS (`matched sheep set`). Các cột tương ứng với các tổ hợp bố cục (`wide`, `outlier_rich`) và quy mô bầy ($N \in \lbrace 100, 200, 400\rbrace$). Độ đậm của màu tỷ lệ thuận với $D_{\min}$; các ô gạch chéo ghi "none" biểu thị không có quy mô đội nào đạt độ tin cậy. Tiêu chí 99% duy trì cấu trúc ranh giới ổn định gần như tuyệt đối (dao động $\le 1$ chó), trong khi tiêu chí nghiêm ngặt bị phân rã bởi các bất ổn biên.  
*Số liệu:* [results_tables.md: Sensitivity, strict: base / variant](results_tables.md#sensitivity-strict-base--variant) và [results_tables.md: Sensitivity, 99 percent: base / variant](results_tables.md#sensitivity-99-percent-base--variant).

---

---

### 3.6 RQ6: Đội chó không phối hợp (FAT) có đạt được quy mô *D*<sub>min</sub> hữu hạn không?

Mô hình đối chứng tham lam không phối hợp FAT (Furthest Agent Targeting) chứng minh rõ nét hậu quả của sự thiếu vắng cơ chế điều phối không gian:

1. **Sự sụp đổ toàn diện trên bầy cừu quy mô lớn**:  
   Mặc dù FAT có thể hoàn thành nhiệm vụ trên các đàn nhỏ ($N \le 100$), mô hình này ghi nhận **0 ô đạt độ tin cậy** khi bầy cừu mở rộng lên $N \ge 200$ trên mọi bố cục phân tán. Đáng kinh ngạc hơn, FAT thất bại ngay cả trên bầy tập trung (`compact`) tại $N = 400$—nơi thuật toán phối hợp `strombom_multi` chỉ cần đúng 1 chú chó duy nhất. Việc bổ sung thêm chó hoàn toàn bất lực trong việc cứu vãn tỷ lệ thành công của FAT.

2. **Cơ chế vật lý của hiện tượng dồn cục (Pack Clumping)**:  
   Nguyên nhân cốt lõi khiến FAT sụp đổ nằm ở sự đồng nhất thông tin và tính tham lam cục bộ: tất cả các chú chó đều có cùng góc nhìn toàn cục và cùng tính toán mục tiêu theo một hàm mục tiêu duy nhất—con cừu cách xa đích nhất ($\arg\max_i \lVert \mathbf{x}_i - \mathbf{x}_{\text{goal}} \rVert$). Do không có cơ chế gán việc tối ưu cũng như không có quy tắc tránh va chạm lẫn nhau, toàn bộ $D$ chú chó cùng lao đầu vào đúng một cá thể cừu.  
   Hành vi này dẫn tới hiện tượng chen chúc cực đoan: tỷ lệ chó có một đồng đội khác trong vòng $2\text{ m}$ đạt trung vị tới **0,86 trên `compact` và 0,79 trên `split`** ở $N \ge 200$ (0,46 trên `wide`, 0,30 trên `outlier_rich`). Thay vì tạo ra năng lực bao vây song song, việc tăng thêm chó trong FAT chỉ tạo ra một khối hỗn loạn dày đặc đuổi theo một con cừu, bỏ mặc toàn bộ phần còn lại của bầy cừu tản mát tự do khắp đồng cỏ.  
   Đáng lưu ý, đối chứng chó độc lập (Mục 3.9)—dù cũng không có tầng điều phối đội ngũ nhưng sở hữu máy trạng thái chuyển đổi hành vi gom/lùa của Strömbom—vẫn đạt $D_{\min}$ hữu hạn ở $N = 200$. Điều này chứng minh sự thất bại của FAT bắt nguồn từ sự kết hợp tai hại giữa tính tham lam không phân công và sự thiếu vắng máy trạng thái sinh học.

Bảng 5 so sánh $D_{\min}$ giữa FAT và `strombom_multi` ở thời hạn $6\times$:

| Bố cục | $N = 25$ | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `compact` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / [12] (1 / 1) |
| `wide` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (3 / 2) | none / none ([9] / 2–3) |
| `split` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | none / none (none / [1]) | none / none (none / [5]) |
| `outlier_rich` | 1 / 1 (1 / 1) | 1 / 1 (1 / 1) | 2 / 2 (3 / 2) | none / none ([12] / 2–3) | none / none (none / 3) |

*Số liệu:* [results_tables.md: FAT dog rule, deadline 6](results_tables.md#fat-dog-rule-deadline-6-strict-then-99-percent) (`dmin_fat`, `dmin_f99_fat`); các giá trị `strombom_multi` trong ngoặc tra cứu tại [results_tables.md: strict success](results_tables.md#d_min-by-layout-and-n-strict-success) và [results_tables.md: success at 99 percent](results_tables.md#d_min-by-layout-and-n-success-at-99-percent).

![FAT so với Team Rule](../figures/fig26_fat.png)

**Hình 7: Xác suất thành công theo số lượng chó $D$ của thuật toán phối hợp `strombom_multi` (xanh dương) so với đối chứng tham lam không phối hợp FAT (cam) ở thời hạn $6\times$.**  
Năm khung hình khảo sát các bố cục: `compact` $N = 400$, `wide` $N = 200$ và $400$, `outlier_rich` $N = 200$, và `split` $N = 200$. Đường nét liền và nét đứt tương ứng với tiêu chí nghiêm ngặt và 99%; đường chấm ngang đánh dấu ngưỡng tin cậy $\theta = 0{,}90$. Tỷ lệ thành công của FAT bị kẹt dưới mức 0,55 tại mọi $D > 2$ do hiện tượng dồn cục đàn chó. Ngược lại, `strombom_multi` duy trì độ tin cậy vượt trội trên `wide` và `outlier_rich` nhờ cơ chế phân công nhiệm vụ Hungarian và hình thành vòng cung lùa.  
*Số liệu:* `results/dmin_fat`, `dmin_f99_fat`, `dmin_m6` và `dmin_f99_m6`.

---

### 3.7 RQ7: Vượt quá *D*<sub>min</sub>: Bao nhiêu chó là đủ (*D*<sub>sat</sub>), Chi phí vận hành, và Áp lực lên bầy cừu

Việc xác định đội hình tối thiểu đạt độ tin cậy $D_{\min}$ trả lời cho câu hỏi về khả năng hoàn thành nhiệm vụ, nhưng đặt ra một bài toán kinh tế - kỹ thuật quan trọng: *Bổ sung thêm chó vượt quá $D_{\min}$ có giúp đàn cừu về đích nhanh hơn không? Chi phí vận hành gia tăng ra sao, và liệu đàn cừu có bị kiệt sức trước sự vây bọc của một đội quân chó săn đông đảo?*

Để giải quyết thấu đáo, chúng tôi phân tích toàn diện 11 thư mục giao thức dưới tiêu chí 99%, đồng thời tiến hành chạy replay chẩn đoán vi mô trên 164 lượt mô phỏng đại diện để đo lường áp lực hoảng loạn của từng cá thể cừu theo từng tích tắc thời gian (mọi lượt replay đều tái tạo bit-identical kết quả đã ghi nhận).

#### 1. Ngưỡng bão hòa tốc độ (*D*<sub>sat</sub>)
*D*<sub>sat</sub> được định nghĩa là quy mô đội tin cậy nhỏ nhất mà từ đó trở đi, việc bổ sung thêm chó không mang lại sự rút ngắn thời gian hoàn thành có ý nghĩa thống kê:
- **Trên bầy tập trung (`compact`) và các bầy nhỏ ($N \le 50$)**: $D_{\mathrm{sat}} = 1$ ngay từ đầu (trừ ngoại lệ `outlier_rich` $N = 50$ với khoảng chặn 1–24). Một chú chó duy nhất đã đủ sức lùa bầy cừu di chuyển ở vận tốc đi bộ tối đa ($1{,}0\text{ m/s}$); việc bổ sung thêm chó không thể ép cừu chạy nhanh hơn giới hạn sinh học tự nhiên của chúng.
- **Trên bầy phân tán ở thời hạn trung bình ($6\times$)**: $D_{\mathrm{sat}}$ dao động từ 2 đến 7 chó ở $N = 100\text{--}400$ (ví dụ `outlier_rich` $N = 100$ bão hòa tại $D_{\mathrm{sat}} = 3$; `wide` $N = 400$ bão hòa tại $D_{\mathrm{sat}} = 5$).
- **Phân định các khoảng chặn**: Các đợt chạy bổ sung hạt giống thời gian (Mục 3.8) đã phân định dứt khoát phần lớn các đường cong: trên `wide`, $D_{\mathrm{sat}}$ tiến triển tuần tự qua các mốc $1, 1, 1, 2, 3, 3, 4, 5$ từ $N = 25$ đến $400$.

#### 2. Hiệu suất giảm dần và Chi phí vận hành (*D* > *D*<sub>sat</sub>)
Bố trí thêm chó vượt quá ngưỡng bão hòa chỉ mang lại lợi ích tốc độ không đáng kể, nhưng làm bùng nổ chi phí vận hành:
- Trên toàn bộ 189 ô đạt tin cậy nằm phía trên một $D_{\mathrm{sat}}$ đã phân định ở thời hạn $6\times$, thời gian hoàn thành luôn duy trì nghiêm ngặt trong khoảng **0,96 đến 1,01 lần** thời gian tại mốc $D_{\mathrm{sat}}$ (chỉ rút ngắn tối đa 4%, đôi khi còn chậm đi 1%).
- Trong khi đó, **tổng khối lượng công việc của đàn chó** (`dog_time` $= D \times T$) và tổng năng lượng tiêu hao tăng tuyến tính theo đúng tỷ lệ $D / D_{\mathrm{sat}}$. Ví dụ, trên bầy tập trung $N = 50$, việc thả 24 chú chó tiêu tốn pin gấp 24 lần so với 1 chú chó, nhưng thời gian đưa đàn về đích hoàn toàn không đổi (154 s với 1 chó so với 154 s với 24 chó).

Bảng 6 tóm tắt chi phí vận hành tại mốc gấp đôi bão hòa ($2 D_{\mathrm{sat}}$) và tại mốc cực đại ($D = 24$) so với mốc chuẩn $D_{\mathrm{sat}}$ trên các đường cong phân tán ở $6\times$:

| Bố cục, Quy mô bầy $N$ | Ngưỡng $D_{\mathrm{sat}}$ | Tại $2 D_{\mathrm{sat}}$: Thời gian / Công sức chó | Tại $D = 24$: Thời gian / Công sức chó |
| :--- | :---: | :---: | :---: |
| `wide`, $N = 200$ | 3 | 0,97 / 1,94 | 0,96 / 7,70 |
| `wide`, $N = 400$ | 5 | 0,97 / 2,32 (tại $D = 12$) | 0,96 / 4,61 |
| `outlier_rich`, $N = 100$ | 3 | 0,99 / 1,98 | 0,98 / 7,85 |
| `outlier_rich`, $N = 400$ | 6–24 | 0,96 / 1,91 | 0,94 / 3,74 |
| `split`, $N = 100$ | 4 | 0,99 / 1,98 | 0,99 / 5,91 |

*Ý nghĩa của Bảng 6*: Tại $D = 24$, thời gian lùa chỉ nhanh hơn vỏn vẹn từ 1% đến 6% ($0{,}94 - 0{,}99$), nhưng tổng tiêu hao pin và công sức của đàn chó tăng vọt từ **3,7 đến 7,9 lần** ($3{,}74 - 7{,}85$).  
*Số liệu:* [results_tables.md: Effort, dmin_f99_m6](results_tables.md#effort-dmin_f99_m6-cost-of-dogs-beyond-d_sat-relative-to-the-d_sat-cell-1) và [results_tables.md: D_sat, dmin_f99_m6](results_tables.md#d_sat-dmin_f99_m6-d_sat-1).

#### 3. Tâm lý hoảng loạn và Phúc lợi bầy cừu
Phép đo đạc vi mô từng giây hé lộ một kết quả bất ngờ về phúc lợi động vật:
- **Tổng thời gian chạy trốn thực chất giảm đi**: Một con cừu chỉ hoảng loạn tháo chạy khi có chó tiến vào cự ly đe dọa $65\text{ m}$. Khi tăng số chó từ $D_{\min}$ lên $D_{\mathrm{sat}}$, việc gom cừu lạc diễn ra song song nhanh hơn nhiều, giúp rút ngắn tổng thời gian mỗi con cừu phải tháo chạy (trên `wide` $N = 400$, trung vị thời gian chạy trốn của mỗi con cừu giảm từ 485 s tại $D = 3$ xuống còn 359 s tại $D = 6$). Vượt quá $D_{\mathrm{sat}}$, thời gian chạy trốn đi ngang (361 s tại $D = 12$).
- **Áp lực tức thời tăng nhưng thời lượng phơi nhiễm ngắn lại**: Tại một thời điểm bất kỳ, một đội chó đông hơn sẽ giăng một vòng cung rộng hơn, khiến một tỷ lệ bầy cừu lớn hơn cùng chuyển động (trung vị tăng từ 68% bầy cừu tháo chạy tại $D = 3$ lên 84% tại $D = 12$). Tuy nhiên, do tổng thời gian hoàn thành ngắn hơn, tổng mức độ phơi nhiễm áp lực không hề bị đội lên.
- **Khoảng cách an toàn luôn được tôn trọng**: Dưới quy tắc giữ khoảng cách $3 r_a = 6\text{ m}$, thời gian một con cừu ở trong vòng 6 m của một chú chó luôn dưới 1,3 s mỗi con (trung vị) ở mọi quy mô $D$ thử nghiệm.

#### 4. Tính ổn định hệ thống: Không có hiện tượng sụp đổ do quá tải ở chó dạng điểm
Dưới tiêu chí 99%, trên toàn bộ 11 bộ thử nghiệm lên tới $D = 24$ chó, **chúng tôi không ghi nhận bất kỳ ngưỡng quá tải sụp đổ ($D_{\mathrm{overcrowd}}$) nào** trên năm quy mô bầy gốc. Không có đường cong nào bị rớt khỏi ngưỡng tin cậy sau khi đã đạt được nó. Sự sụp đổ từng thấy dưới tiêu chí 100% trên `split` $N = 100$ ở $3\times$ hoàn toàn biến mất dưới tiêu chí 99%. Mặc dù thêm chó làm chậm thời gian hoàn thành trên bố cục `split` ở thời hạn $12\times$ ($N = 400$: 950–1040 s với $D \ge 9$ so với 839 s tại $D = 5$), toàn bộ nhiệm vụ vẫn hoàn thành một cách tin cậy.

![Chi phí chó vượt quá D_sat](../figures/fig33_effort.png)

**Hình 8: Động học hiệu suất giảm dần và chi phí vận hành vượt quá quy mô bão hòa $D_{\mathrm{sat}}$ (thời hạn $6\times$, tiêu chí 99%).**  
*(Khung trái)* Tỷ số thời gian hoàn thành so với ô bão hòa ($T / T_{\mathrm{sat}}$) theo tỷ số quy mô đội ($D / D_{\mathrm{sat}}$, thang log). Mọi đường cong phân tán đều nằm trong dải hẹp 0,96 đến 1,01, khẳng định tốc độ lùa đàn đã chạm ngưỡng bão hòa.  
*(Khung phải)* Tổng công sức vận hành của đàn chó (`dog_time` $= D \times T$) chuẩn hóa theo mốc $D_{\mathrm{sat}}$. Đường chi phí bám sát đường tuyến tính $y = x$, thể hiện rõ việc tăng thêm chó chỉ gây lãng phí năng lượng mà không mang lại cải thiện tốc độ.  
*Số liệu:* [results_tables.md: Effort, dmin_f99_m6](results_tables.md#effort-dmin_f99_m6-cost-of-dogs-beyond-d_sat-relative-to-the-d_sat-cell-1).

![Áp lực lên bầy cừu](../figures/fig34_pressure.png)

**Hình 9: Động lực học chạy trốn vi mô và phúc lợi của bầy cừu qua các quy mô đội chó (thời hạn $6\times$, tiêu chí 99%).**  
Đồ thị thể hiện trung vị trên các hạt giống thành công cho $N = 100$ (tròn, nét chấm) và $N = 400$ (vuông, nét liền).  
*(Khung trái)* Tổng thời gian chạy trốn của mỗi cá thể cừu (thời gian nằm trong phạm vi đe dọa $65\text{ m}$). Tăng số chó từ $D_{\min}$ lên $D_{\mathrm{sat}}$ giúp giảm áp lực chạy trốn nhờ gom bầy nhanh hơn; vượt quá $D_{\mathrm{sat}}$, áp lực phơi nhiễm hoàn toàn đi ngang.  
*(Khung phải)* Tỷ lệ bầy cừu đang hoảng loạn tháo chạy tại một tích tắc thời gian. Đội hình đông chó giăng vòng cung lớn hơn khiến tỷ lệ cừu chạy trốn tức thời tăng cao, nhưng tổng thời gian chịu đe dọa lại ngắn hơn.  
*Số liệu:* [results_tables.md: Pressure, dmin_f99_m6](results_tables.md#pressure-dmin_f99_m6-replay-of-12-stored-seeds-per-cell-every-replay-reproduced-its-stored-trial).

---

### 3.8 RQ8: Tăng trưởng theo *N* trên Lưới dày, *D*<sub>sat</sub>, và Hình dạng đường cong

Để phân định dứt khoát dạng hàm số của quy luật mở rộng $D_{\min}(N)$, chúng tôi mở rộng các lưới thử nghiệm 99% ($12\times$ và $6\times$) thêm 4 quy mô bầy trung gian: $N = 71, 141, 283$ (các trung điểm logarit giữa 50 và 400) và $N = 566 = 400\sqrt{2}$.

**Lý do lựa chọn bước nhảy $\sqrt{2}$ và giới hạn $N = 566$:**  
Các bước tỷ lệ $\sqrt{2}$ phân bổ trọng số hình học đồng đều trong không gian log-log, tránh hiện tượng các bầy cực lớn lấn át hồi quy. Đồng thời, $N = 566$ là giới hạn vật lý tự nhiên của mô hình Strömbom: ở các quy mô dưới 600 con, đàn cừu luôn có khả năng tự co cụm về một bán kính dừng cân bằng $R_f(N)$. Khi vượt qua 600 con, bầy xuất phát lỏng lẻo không còn khả năng tự liên kết (ở $N = 630$, bán kính bầy rộng hơn 17% so với chuẩn; ở $N = 800$, quy trình hiệu chuẩn bán kính thất bại hoàn toàn).

1. **Hệ số góc được xác định với độ chính xác cao**:  
   Trên lưới 9 quy mô bầy, hệ số góc log-log của $D_{\min}$ theo $N$ dao động từ **0,27 đến 0,38** trên `wide` và **0,28 đến 0,38** trên `outlier_rich` ở thời hạn thong thả ($12\times$), và đạt **0,38 đến 0,61** ở thời hạn trung bình ($6\times$). Trong điều kiện thời gian đủ dài, tốc độ mở rộng luôn nằm dưới định luật căn bậc hai ($\alpha = 0{,}50$) của các hạt không liên kết.

2. ***D*<sub>sat</sub> mở rộng nhanh gấp đôi $D_{\min}$**:  
   Trên bố cục `wide` ở $6\times$, *D*<sub>sat</sub> tăng đều đặn: $1, 1, 1, 2, 3, 3, 4, 5$ chó từ $N = 25$ đến $400$, và đạt khoảng chặn $7\text{--}24$ tại $N = 566$ (độ dốc log-log **0,70 đến 0,91**). Khoảng cách giữa quy mô đội tối thiểu để đạt độ tin cậy và quy mô đội để đạt tốc độ tối đa ngày càng giãn rộng khi quy mô đàn cừu lớn dần.

3. **Thách thức phân định dạng đường cong (Lũy thừa hay Bão hòa)**:  
   Trong phạm vi $N \le 566$, dữ liệu thực nghiệm tương thích hoàn hảo với cả hai giả thuyết: hàm lũy thừa không chặn ($D \propto N^\alpha$) và hàm bão hòa tiệm cận ngang ($D \propto D_\infty / [1 + (N_0/N)^\gamma]$), với tỷ số hợp lý tương đương ($\Delta\log\text{-odds} \approx 0{,}0$). Khi ngoại suy lên $N = 1600$, hai mô hình dự báo dải giá trị từ 1,5 đến 6,7 chó ở $12\times$ (3,1 đến 10,4 ở $6\times$). Sự phân định giữa hai quy luật này bắt buộc phải dựa vào các thử nghiệm bầy cực lớn ($N > 1000$, Mục 3.13).

Bảng 7 thể hiện bước tiến thực nghiệm qua 9 quy mô bầy (tiêu chí 99%):

| $N$ | 25 | 50 | 71 | 100 | 141 | 200 | 283 | 400 | 566 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `wide`, $12\times$ | 1 | 1 | 1 | 1 | 2 | 1–2 | 2 | 2 | 2–3 |
| `outlier_rich`, $12\times$ | 1 | 1 | 1 | 1–2 | 2 | 2 | 2 | 2 | 2–3 |
| `wide`, $6\times$ | 1 | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3–7 |
| `outlier_rich`, $6\times$ | 1 | 1 | 1 | 2 | 2 | 2–3 | 2–3 | 3 | 3–6 |
| *D*<sub>sat</sub> `wide`, $6\times$ | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 | 7–24 |

*Số liệu:* [results_tables.md: Finish-time top-up, densified N, independent shepherds, Kubo to D = 24, 99 percent](results_tables.md#finish-time-top-up-densified-n-independent-shepherds-kubo-to-d--24-99-percent).

![D_min trên chín kích thước bầy](../figures/fig35_growth_fits.png)

**Hình 10: Quy mô đội tối thiểu $D_{\min}$ qua chín kích thước bầy và dải ngoại suy của hai mô hình tăng trưởng.**  
Khung trái thể hiện thời hạn $12\times$; khung phải thể hiện thời hạn $6\times$ trong tọa độ log-log (`wide` tròn, `outlier_rich` vuông). Các thanh dọc biểu diễn khoảng chặn $D_{\min}$; đường nét đứt dọc đánh dấu giới hạn hiệu chuẩn tự nhiên của mô hình ($N \approx 600$). Vùng bóng mờ bên phải biểu diễn dải ngoại suy được hỗ trợ bởi các đường cong lũy thừa (cạnh trên nét đứt) và bão hòa (cạnh trên nét chấm). Cả hai mô hình đều khớp xuất sắc với dữ liệu thực nghiệm $N \le 566$, đòi hỏi phải khảo sát các đàn khổng lồ ngoài phạm vi hiệu chuẩn để tìm ra ranh giới phân tách.  
*Số liệu:* [results_tables.md: D_min, dmin_f99_m12](results_tables.md#d_min-dmin_f99_m12), [results_tables.md: D_min, dmin_f99_m6](results_tables.md#d_min-dmin_f99_m6) và [results_tables.md: fits dmin_f99_m12](results_tables.md#fits-dmin_f99_m12-d_minn-power-law-against-saturating-curve).

---

### 3.9 RQ9: Phần nào của Quy tắc Đội đóng vai trò quyết định, và Mô hình lực liên tục

Trong Mục 3.6, mô hình không phối hợp FAT đã thất bại ở $N \ge 200$ trên các bố cục phân tán. Tuy nhiên, FAT thiếu cả *hai* thành phần: (1) máy trạng thái hành vi Strömbom (chuyển đổi giữa gom cừu lạc và lùa đàn), và (2) tầng phối hợp đa tác tử (phân công Hungarian và dàn vòng cung lùa).

---

### 3.9 RQ9: Phần nào của Quy tắc Đội đóng vai trò quyết định, và Động học Lực liên tục

Trong Mục 3.6, mô hình tham lam FAT thất bại hoàn toàn ở $N \ge 200$ trên các bố cục phân tán. Tuy nhiên, FAT thiếu vắng đồng thời cả hai cơ chế nền tảng: (1) máy trạng thái hành vi sinh học Strömbom (chuyển đổi linh hoạt giữa gom cừu lạc và lùa bầy), và (2) tầng phối hợp đa tác tử (thuật toán gán việc tối ưu Hungarian và dàn đội hình vòng cung lùa).

Để bóc tách độc lập vai trò của từng thành phần, chúng tôi thử nghiệm biến thể **chó độc lập (`dmin_f99_indep`)**: mỗi chú chó vận hành máy trạng thái một-chó nguyên bản của Strömbom (2014) hoàn toàn độc lập, không hề có kênh truyền thông tin hay cơ chế phân chia nhiệm vụ tập thể.

1. **Máy trạng thái gánh vác đội hình tới $N = 200$; Tầng phối hợp mở lối cho $N = 400$**:  
   Kết quả thực nghiệm hé lộ một ranh giới phân tầng rõ nét:  
   - Đội chó độc lập đạt độ tin cậy trên toàn bộ các bố cục phân tán lên đến quy mô $N = 200$—nơi FAT thất bại 100%. Điều này khẳng định rằng ở quy mô đàn vừa và nhỏ, riêng cơ chế chuyển đổi hành vi (nhận diện cá thể xa bầy để gom trước khi lùa) đã đủ để duy trì tính ổn định của hệ thống mà chưa cần tới sự phối hợp phức tạp giữa các chú chó.  
   - Tuy nhiên, khi đàn cừu đạt tới $N = 400$, đội chó độc lập sụp đổ hoàn toàn trên mọi bố cục phân tán (không có quy mô nào đạt tin cậy). Ngược lại, thuật toán phối hợp `strombom_multi` thành công vững chắc với $D_{\min} = 2\text{--}3$ chó trên `wide` và $3$ chó trên `outlier_rich`. Trên các đàn cừu lớn, sự can thiệp của thuật toán gán việc Hungarian—phân bổ mỗi chú chó phụ trách một phân vùng cừu lạc riêng biệt—trở thành điều kiện tiên quyết để ngăn chặn các xung đột hành vi triệt tiêu lẫn nhau.

2. **Động lực học của Mô hình trường thế liên tục (Kubo et al. đến 24 chó)**:  
   - Trên bầy tập trung (`compact`), mô hình Kubo tái khẳng định phát hiện cốt lõi của chúng tôi: $D_{\min} = 1$ trên toàn bộ các quy mô $N \in [25, 100]$.  
   - Tuy nhiên, cơ chế động học giữa hai trường phái có sự khác biệt căn bản: trong khi cừu Strömbom chuẩn hóa tổng lực đẩy về đơn vị khiến vận tốc lùa bị kịch trần tự nhiên ($1{,}0\text{ m/s}$), cừu Kubo chịu các lực trường thế đẩy cộng dồn phi tuyến theo nghịch đảo lập phương khoảng cách ($1/r^3$). Tại $N = 100$, việc tăng số chó nén mạnh bầy cừu, rút ngắn thời gian lùa từ $115\text{ s}$ (1 chó) xuống $29\text{ s}$ (10 chó) và tiệm cận $25\text{ s}$ tại $D = 24$. Đáng chú ý, hơn 80% mức cải thiện tốc độ đạt được trước mốc $D = 10$, xác nhận tính quy luật của hiện tượng hiệu suất giảm dần trên cả hai hệ tiên đề động lực học.

Bảng 8 so sánh năng lực của chó độc lập với thuật toán phối hợp và đối chứng FAT ở thời hạn $6\times$:

| Phương pháp (`strombom_multi` / `independent` / `fat`), 99%, $6\times$ | $N = 200$ | $N = 400$ |
| :--- | :---: | :---: |
| `wide` | 2 / 2–3 / none | 2–3 / none / none |
| `outlier_rich` | 2–3 / 3 / none | 3 / none / none |
| `split` | [1] / 1–3 / none | [5] / none / none |

*Số liệu:* [results_tables.md: Methods at 99 percent, 6 drive times](results_tables.md#methods-at-99-percent-6-drive-times-team-rule-independent-paper-shepherds-fat) và [results_tables.md: Kubo, compact, D to 24](results_tables.md#kubo-compact-d-to-24-99-percent); thời gian Kubo lấy từ `results/dmin_f99_kubo`.

---

### 3.10 RQ10: Quá nhiều chó: Bài toán Giữ đàn và Chó chiếm chỗ không gian

Trong bài toán lùa đàn mở, việc đưa thêm chó vượt quá mức bão hòa không gây đổ vỡ nhiệm vụ dưới tiêu chí 99%. Tuy nhiên, trong lý thuyết robot bầy đàn, hiện tượng quá tải tắc nghẽn thường bộc lộ rõ nhất ở giai đoạn vây hãm và chặn giữ (Green et al. 2022). Để kiểm chứng giới hạn này, chúng tôi thiết kế hai kịch bản nâng cao:

1. **Nhiệm vụ Giữ đàn (Holding Task)**: Nhiệm vụ chỉ được công nhận thành công khi 99% cừu ở yên trong đích trọn vẹn một khoảng thời gian lùa ($T_{\mathrm{drive}}$). Khi đàn cừu đã vào chuồng, các chú chó phải chủ động lùi xa ngoài tầm đe dọa ($65 + 2 = 67\text{ m}$) để cừu bình tâm gặm cỏ.
2. **Kích thước vật lý và Chiếm chỗ không gian (Dog Spacing)**: Tác tử không còn là các chất điểm vô hình mà có kích thước cơ thể thực tế: không chú chó nào được xâm phạm phạm vi $2\text{ m}$ của đồng đội (`dog_spacing = 2.0`). Chu vi hữu hạn của vòng cung lùa tạo ra một mức trần sức chứa vật lý: $D_{\mathrm{cap}} \approx 7, 9, 10, 11, 12$ tương ứng với $N = 25$ đến $400$.

#### Kết quả phân tích cơ chế:

1. **Nút thắt hình học chuồng đích ở bầy nhỏ ($N \le 50$)**:  
   Nhiệm vụ Giữ đàn thành công tin cậy trên các đàn lớn ($N \ge 100$) trên bố cục `wide` và `compact`, với $D_{\min}$ trùng khớp hoàn toàn với bài toán lùa mở (1, 2, và 3 chó tại $N = 100, 200, 400$).  
   Tuy nhiên, nhiệm vụ này thất bại toàn diện trên các bầy nhỏ ($N \le 50$). Phân tích nguyên nhân cho thấy đây là một nghịch lý hình học: với bầy nhỏ, bán kính chuồng đích chỉ vỏn vẹn $12\text{--}14\text{ m}$. Quy tắc rút lui buộc chó phải lùi ra xa $67\text{ m}$, vượt quá bán kính quan sát hiệu quả của cừu đối với chuồng. Các lượt chạy thất bại ở $N \le 50$ chủ yếu do cừu tản mát ngẫu nhiên khỏi một chuồng đích quá nhỏ khi không còn lực đe dọa từ xa, dẫn tới hết giờ chứ không phải do thiếu năng lực gom bầy.

2. **Kích thước cơ thể kích hoạt hiện tượng sụp đổ do quá tải ($D_{\mathrm{overcrowd}}$)**:  
   Trên bố cục phức tạp `outlier_rich` tại $N = 400$, sự hiện diện của kích thước vật lý $2\text{ m}$ gây ra một sự sụp đổ thảm họa:
   - Với các đội nhỏ ($D = 3\text{--}6$), tỷ lệ thành công đạt 92,5–94% (chưa ngã ngũ ranh giới tin cậy).  
   - Tuy nhiên, khi quy mô đội tăng lên $D \ge 9$, **toàn bộ các đội hình tới $D = 24$ đều bị xác nhận không đạt độ tin cậy**; xác suất thành công lao dốc thẳng đứng: 0,77 tại $D = 9$, 0,65 tại $D = 12$, và chỉ còn 0,50 tại $D = 16$.  
   - *Cơ chế tắc nghẽn*: Sức chứa tối đa của vòng cung lùa ở $N = 400$ là $D_{\mathrm{cap}} \approx 12$ chó. Khi số chó vượt ngưỡng, sự tranh chấp không gian khiến các chú chó đẩy nhau chệch khỏi vị trí tối ưu, gây kẹt cứng đội hình và làm tê liệt hoàn toàn khả năng bọc lót khi có cừu vượt tuyến.  
   - Ngược lại, trên bố cục `wide` và `compact`, các chú chó không chen chân được vào vòng cung sẽ tự động đứng chờ ở tuyến sau, giúp hệ thống bảo toàn độ tin cậy tới 24 chó. Điều này chứng minh rằng tác hại của sự đông đúc phụ thuộc mật thiết vào hình thái không gian của bầy mục tiêu và cấu trúc phân bổ hình học của tác tử.

![Giữ đàn với chó chiếm chỗ](../figures/fig36_spacing.png)

**Hình 11: Độ tin cậy của nhiệm vụ Giữ đàn tại $N = 400$ so sánh giữa tác tử dạng điểm và tác tử có kích thước cơ thể (giãn cách $2\text{ m}$).**  
Khung trái khảo sát bố cục `wide`; khung phải khảo sát `outlier_rich` theo số chó $D$ (thang log). Đường nét chấm xám biểu diễn chó dạng điểm; đường nét liền xanh dương biểu diễn chó có giãn cách vật lý $2\text{ m}$; dải cam đánh dấu sức chứa hình học của vòng cung lùa ($D_{\mathrm{cap}} \approx 10\text{--}12$ chó); đường nét đứt ngang là ngưỡng tin cậy $\theta = 0{,}90$. Trên `wide`, các tác tử thừa đứng lùi lại phía sau giúp duy trì thành công. Trên `outlier_rich`, sự tranh chấp vị trí gây ùn ứ nghiêm trọng, khiến tỷ lệ thành công sụp đổ hoàn toàn từ $D \ge 9$.  
*Số liệu:* [results_tables.md: D_min, dmin_f99_hold](results_tables.md#d_min-dmin_f99_hold) và [results_tables.md: D_min, dmin_f99_hold_spacing](results_tables.md#d_min-dmin_f99_hold_spacing).

---

---

### 3.11 RQ11: Độ gắn kết xã hội làm thay đổi quy luật mở rộng ra sao?

Quy luật tỷ lệ căn bậc hai $\alpha = 0{,}50$ ($D \propto \sqrt{M}$) của Lama và di Bernardo (2024) được xác lập trên các mục tiêu hoàn toàn độc lập, không có tương tác gắn kết nội tại. Để bắc nhịp cầu định lượng giữa các hạt Brown vô tri và bầy cừu sinh học có tính xã hội, chúng tôi can thiệp vào hai tham số lực gắn kết: (1) trọng số lực hút xã hội $c$ (từ chuẩn sinh học $1{,}05$ tăng lên $1{,}3, 1{,}6$, và $2{,}0$), và (2) số lượng láng giềng tương tác $n$ (giảm từ toàn bầy $n = N - 1$ xuống còn một nửa bầy $n = 0{,}5N$).

1. **Gắn kết mạnh hơn chỉ mang lại lợi thế biên tối thiểu**:  
   Khi tăng trọng số hút từ $c = 1{,}05$ lên các mức cực đoan $1{,}3, 1{,}6$, hoặc $2{,}0$, hệ số góc log-log trên bố cục `wide` hoàn toàn không thay đổi ($\alpha = 0{,}20$). Sự gia tăng lực hút chỉ giúp tiết kiệm tối đa 1 chú chó trên toàn bộ các quy mô bầy khảo sát. Cơ chế vật lý giải thích điều này: lực hút tự nhiên sẵn có ($c = 1{,}05$) với mạng lưới tương tác toàn cầu ($n = N - 1$) đã đủ mạnh để giữ bầy cừu thành một khối liên tục khi di chuyển; việc nén chặt hơn nữa không mang lại thêm lợi thế hình học nào cho đàn chó lùa ở phía sau.

2. **Làm suy yếu gắn kết đẩy hệ thống tiệm cận quy luật căn bậc hai**:  
   Ngược lại, khi giới hạn phạm vi tương tác xã hội xuống $n = 0{,}5N$, hệ số góc tăng trưởng $\alpha$ dựng đứng lên **0,40 đến 0,70**—bao hàm mốc lý thuyết $\alpha = 0{,}50$ của các hạt không liên kết.  
   Đặc biệt trên bố cục `split`, bầy cừu có xu hướng phân rã thành các cụm nhỏ độc lập ngay khi chịu áp lực lùa, đẩy $D_{\min}$ từ 1 lên 3–4 chó tại $N = 200$, và từ 2 lên 4–5 chó tại $N = 400$. Thử nghiệm này chứng minh rằng tính kinh tế quy mô dưới tuyến tính ($\alpha < 0{,}50$) trong chăn dắt sinh học phụ thuộc sống còn vào mạng lưới tương tác xã hội toàn bầy; khi tương tác suy giảm, bài toán chăn dắt tập thể thoái hóa trực tiếp về bài toán thu gom hạt rời rạc.

Bảng 9 tóm tắt độ dốc mở rộng qua các mức độ gắn kết (`wide`, tiếp cận 99%, $12\times$):

| Mức độ gắn kết (`wide`, 99%, $12\times$) | $N = 50$ | $N = 100$ | $N = 200$ | $N = 400$ | Hệ số góc log-log $\alpha$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Gắn kết yếu ($n = 0{,}5N$)** | 1 | 1 | 2 | 2–4 | **0,40 đến 0,70** |
| **Mốc chuẩn sinh học ($c = 1{,}05$)** | 1 | 1 | 1–2 | 2 | **0,20 đến 0,30** |
| **Gắn kết rất mạnh ($c = 1{,}3, 1{,}6, 2{,}0$)** | 1 | 1 | 1 | 2 | **0,20** |

*Số liệu:* Hàng mốc chuẩn tra cứu tại [results_tables.md: dmin_f99_m12](results_tables.md#dmin_f99_m12) và [results_tables.md: Growth with N, 99 percent](results_tables.md#growth-with-n-99-percent); các biến thể độ gắn kết tại [results_tables.md: D_min, dmin_f99_c1.3](results_tables.md#d_min-dmin_f99_c13), [results_tables.md: dmin_f99_c1.6](results_tables.md#d_min-dmin_f99_c16), [results_tables.md: dmin_f99_c2.0](results_tables.md#d_min-dmin_f99_c20) và [results_tables.md: D_min, dmin_f99_k05](results_tables.md#d_min-dmin_f99_k05); cột độ dốc tại [results_tables.md: dmin_f99_c1.3](results_tables.md#dmin_f99_c13), [results_tables.md: dmin_f99_c1.6](results_tables.md#dmin_f99_c16), [results_tables.md: dmin_f99_c2.0](results_tables.md#dmin_f99_c20) và [results_tables.md: dmin_f99_k05](results_tables.md#dmin_f99_k05) (growth).

---

### 3.12 RQ12: Giới hạn Tầm nhìn và Mạng lưới Giao tiếp giữa các Chú chó

Trong các ứng dụng thực tế với robot hoặc thiết bị bay không người lái (drone), giả định về tầm nhìn toàn cảnh cánh đồng là phi thực tế. Chúng tôi đánh giá hiệu năng chăn dắt khi mỗi chú chó bị giới hạn trong một bán kính cảm nhận hữu hạn ($r_{\mathrm{view}} \in \lbrace 15, 30, 45, 65, 100\rbrace\text{ m}$), kết hợp với ba cấu hình chia sẻ thông tin: không giao tiếp (`none`), chia sẻ láng giềng cục bộ (`neighbour`), và mạng truyền thông toàn đội (`shared`).

1. **Cái giá của tầm nhìn cục bộ 30–65 m**:  
   Trên bố cục `wide`, đội có tầm nhìn toàn cục cần $D_{\min} = 2$ tại $N = 200$. Khi giới hạn tầm nhìn trong dải thực tế $30\text{--}65\text{ m}$, nhu cầu số lượng chó tăng thêm đúng **1 cá thể** ($D_{\min} = 3$; khoảng chặn 3–4 tại $45\text{ m}$). Ở các đàn nhỏ ($N \le 100$), việc giới hạn tầm nhìn không gây thiệt hại nào vì toàn bộ bầy cừu nằm gọn trong phạm vi quét $65\text{ m}$.

2. **Ngưỡng sụp đổ do mất dấu dưới 30 m**:  
   Khi bán kính cảm nhận bị bóp nghẹt xuống $15\text{ m}$, hệ thống sụp đổ thảm hại trên bố cục `wide`: tại $N = 50$, không đội hình nào tới 16 chó đạt được độ tin cậy; tại $N = 100$, nhu cầu tăng vọt lên ít nhất 6 chó. Các chú chó không thể duy trì dấu vết của các cá thể cừu lạc ngoài tầm mắt hẹp, rơi vào trạng thái tuần tra ngẫu nhiên mất phương hướng.

3. **Mạng lưới giao tiếp khôi phục năng lực như tầm nhìn toàn cảnh**:  
   Tại tầm nhìn $65\text{ m}$ trên `wide` ($N = 200$), việc thiết lập mạng lưới truyền thông chia sẻ vị trí mục tiêu cho toàn đội (`shared`) lập tức đưa $D_{\min}$ từ 3 rút gọn trở lại mức 2 chó—ngang bằng với năng lực khi có tầm nhìn toàn cảnh hoàn hảo, mà không đòi hỏi phải nâng cấp tầm cảm biến phần cứng.  
   Đáng chú ý, cấu hình chỉ chia sẻ với các chó ở gần (`neighbour`) không mang lại cải thiện nào (vẫn cần 3 chó), khẳng định thông tin phân tán toàn cục đóng vai trò quyết định trong việc điều hướng các tác tử ở xa. Trên bố cục `split` $N = 200$, giao tiếp mạng lưới không thể đưa $D_{\min}$ về mức toàn cục (3 so với $[1]$), phản ánh sự chi phối của dị thường phân cụm topo.

![D_min theo tầm nhìn và giao tiếp](../figures/fig37_view.png)

**Hình 12: Tác động của tầm cảm nhận hữu hạn và mạng lưới giao tiếp đa tác tử lên quy mô đội $D_{\min}$.**  
*(Khung trái)* $D_{\min}$ theo bán kính cảm nhận cho `wide` (tròn) và `split` (vuông) tại $N = 100$ (mờ) và $N = 200$; thanh dọc biểu thị khoảng chặn; tam giác rỗng là cận dưới; đường nét đứt dọc đánh dấu mốc $r_s = 65\text{ m}$. Tầm nhìn dưới $30\text{ m}$ gây thất bại nặng nề trên `wide`.  
*(Khung phải)* Tỷ lệ thành công theo số chó trên `wide` $N = 200$ ở tầm nhìn $65\text{ m}$ qua các cấu hình giao tiếp: độc lập không chia sẻ (xanh nét chấm), chia sẻ láng giềng (xanh nét đứt), chia sẻ toàn đội (xanh nét liền), và đối chứng toàn cảnh (đen nét liền). Mạng lưới toàn đội khôi phục trọn vẹn năng lực của hệ thống về ngang hàng với tầm nhìn toàn cục.  
*Số liệu:* [results_tables.md: Views: sensing range](results_tables.md#views-sensing-range-no-sharing-base-row--range-0-global) và [results_tables.md: Views: sharing at range 65](results_tables.md#views-sharing-at-range-65-beside-the-no-sharing-rows-of-dmin_f99_view_range).

---

### 3.13 RQ13: Đàn cừu quy mô cực lớn và Giới hạn Toán học của Quy tắc Lùa đàn

Để kiểm tra giới hạn mở rộng tận cùng của bài toán chăn dắt đa tác tử, chúng tôi khảo sát các siêu đàn cừu từ $N = 800$ đến $3200$ con ở thời hạn thong thả ($12\times$). Phía trên ngưỡng hiệu chuẩn sinh học ($N = 566$), bán kính đàn cừu được áp đặt theo nguyên lý bảo toàn mật độ diện tích: $R_f(N) = R_f(566)\sqrt{N/566}$.

#### 1. Phát hiện Điểm kỳ dị Toán học tại $N \approx 1056$
Trong mô hình gốc của Strömbom et al. (2014), vị trí lùa đàn $\mathbf{P}_d$ của chó được xác định dựa trên trọng tâm bầy (GCM) theo công thức:
$$
\mathbf{P}_d = \mathrm{GCM} + r_a \sqrt{N} \, \hat{\mathbf{e}}_{\mathrm{GCM} \to \mathrm{goal}}
$$
Trong đó $r_a = 2\text{ m}$ là bán kính tương tác đẩy giữa các cá thể cừu. Khoảng cách lùi của đàn chó phía sau trọng tâm bầy là $d_{\mathrm{drive}} = r_a \sqrt{N} = 2\sqrt{N}\text{ m}$.  
Đồng thời, tầm cảm nhận đe dọa của cừu đối với chó có bán kính hữu hạn $r_s = 65\text{ m}$. Điểm kỳ dị toán học xuất hiện khi khoảng cách lùi vượt quá tầm nhìn của cừu:
$$
r_a \sqrt{N} > r_s \iff 2\sqrt{N} > 65 \iff \sqrt{N} > 32{,}5 \iff N > 1056{,}25
$$
Tại các quy mô $N \ge 1056$, thuật toán đặt đàn chó lùi xa hơn $65\text{ m}$ phía sau tâm bầy. Kết quả là **toàn bộ bầy cừu hoàn toàn không cảm nhận được sự hiện diện của đàn chó** và tiếp tục gặm cỏ bình thản; đàn chó lùa đẩy vào khoảng không vô định. Tại $N = 1131$, không đội chó nào tới $D = 12$ hoàn thành nhiệm vụ (0/10 lượt thành công ở mọi $D$).

#### 2. Giải pháp Áp trần Cự ly Lùa đàn ($63\text{ m}$ cap)
Bằng cách áp đặt một mức trần khoảng cách lùa tối đa $d_{\mathrm{drive}} \le r_s - r_a = 63\text{ m}$, đàn chó luôn duy trì tiếp xúc giác quan với rìa sau của đàn cừu:
- **Trên bầy tập trung (`compact`)**: 1 chú chó duy nhất ($D_{\min} = 1$) lùa nhẹ nhàng siêu đàn $N = 800$ và $1131$ con về đích, và chỉ cần 2 chó cho đàn $N = 1600$. Tại $N = 3200$, các đội từ 3 đến 12 chó đạt tỷ lệ thành công tuyệt đối trong toàn bộ 42 lượt chạy thử nghiệm.
- **Trên bầy phân tán (`wide`)**: Nhu cầu số lượng chó tăng vọt: 3 chó ở $N = 800$, 5–9 chó ở $N = 1131$, và vượt quá 12 chó ở $N = 1600$. Sự bùng nổ này phản ánh yêu cầu hình học: chu vi của một bầy phân tán khổng lồ đòi hỏi một đội ngũ tác tử lớn để dàn thành hàng rào ngăn cản các luồng tháo chạy sang hai cánh.

Bảng 10 tóm tắt kết quả với quy tắc lùa có giới hạn trần cự ly (tiêu chí 99%, $12\times$):

| Giới hạn cự ly lùa ($63\text{ m}$ cap), 99%, $12\times$ | $N = 800$ | $N = 1131$ | $N = 1600$ | $N = 3200$ (Kiểm thử một phần) |
| :--- | :---: | :---: | :---: | :---: |
| `compact` | 1 | 1 | 2 | 42 / 42 thành công ở $D = 3$–12 ($D = 1, 2$ chưa chạy) |
| `wide` | 3 | 5–9 | none đến 12 | **none** (0 / 58 ở $D = 2\text{--}12$) |

*Số liệu:* [results_tables.md: dmin_f99_big_cap](results_tables.md#dmin_f99_big_cap); cột $N = 3200$ lấy từ `results/dmin_f99_big_cap` (100 lượt, kết thúc sớm). Các lượt không giới hạn tra cứu tại [results_tables.md: D_min, dmin_f99_big](results_tables.md#d_min-dmin_f99_big).

---

### 3.14 RQ14: Mục tiêu không gắn kết: Tái lập và Phân tích Phản biện Quy luật Căn bậc hai của Lama & di Bernardo (2024)

Nhằm đặt các phát hiện về bầy cừu sinh học vào bức tranh tổng thể của lý thuyết điều khiển bầy đàn, chúng tôi tích hợp trực tiếp mô hình mục tiêu Brown không gắn kết của Lama và di Bernardo (2024) vào HerdSim dưới định danh phương pháp `lama` trên nhiệm vụ thu gom `gather` ([Mô hình](../methods/models_vi.md#mô-hình-mục-tiêu-brownian-không-liên-kết-lama-2024) và [Nhiệm vụ](../experiments/task_design_vi.md#6-nhiệm-vụ-gom-lama-và-di-bernardo-2024)). Mục tiêu chuyển động Brown bị người chăn trong bán kính $\lambda = 2{,}5$ đẩy tuyến tính ra xa; người chăn truy đuổi mục tiêu xa đích nhất trong tầm nhìn; mọi tác tử xuất phát ngẫu nhiên trong đĩa bán kính $R = 50$ quanh chuồng đích bán kính $R/5$; trần thời gian 5000 s.

#### 1. Sự phân kỳ giữa Hai Thước đo Thống kê
Chúng tôi đánh giá đồng thời hai tiêu chuẩn nghiệm thu từ cùng một tập dữ liệu mô phỏng:
- **Thống kê của Lama et al. (Mean Target Share)**: Tỷ lệ trung bình mục tiêu được đưa vào đích tính trên toàn bộ các lượt chạy; một quy mô đội được coi là đạt khi $\bar{S}_{\mathrm{gathered}} \ge 0{,}99$.
- **Thống kê của HerdSim (Clopper-Pearson Reliability)**: Tỷ lệ các lượt chạy đưa được $\ge 99\%$ mục tiêu vào đích phải đạt $\ge 0{,}90$ với độ tin cậy thống kê 99% ($L \ge 0{,}90$).

#### 2. Kết quả đối chiếu và Cơ chế Vật lý
1. **Tái lập thành công bản đồ gốc của bài báo**:  
   Trên toàn bộ lưới tham số, tỷ lệ thu gom trung bình của HerdSim bám sát Hình 2 của bài báo gốc với độ lệch trung vị chỉ 0,034 ở bán kính cảm nhận hữu hạn $r_{\mathrm{view}} = 10$ (448 ô) và 0,003 với tầm nhìn vô hạn (451 ô). Đội tối thiểu của HerdSim bằng hoặc chỉ nhỏ hơn bài báo đúng 1 người chăn ở mọi quy mô $\sqrt{N} \ge 12$.

2. **Quy luật căn bậc hai giữ vững dưới tầm nhìn vô hạn**:  
   Với tầm nhìn vô hạn, đội tối thiểu dưới cả hai thước đo thống kê trùng khớp hoàn toàn ở mọi quy mô trừ đúng một ô (289 mục tiêu: 15 so với 14–15): cần 8 người chăn cho 100 mục tiêu, 13 cho 225, và 17 cho 400. Số mũ lũy thừa khớp thực nghiệm đạt **0,52** (theo Lama) và **0,53** (theo HerdSim), xác nhận định luật tỷ lệ $\sqrt{M}$ đối với các hạt rời rạc.

3. **Ngưỡng mật độ và Sự che giấu rủi ro đuôi (Tail Risk) của giá trị trung bình**:  
   Với bán kính cảm nhận hữu hạn 10, một ngưỡng mật độ khắc nghiệt xuất hiện: dưới 81 mục tiêu, không đội nào tới 25 người chăn có thể đạt độ tin cậy do hiện tượng mục tiêu phân tán bị mất dấu ngoài tầm nhìn (`targets_lost`).  
   Đặc biệt, tại vùng chuyển tiếp ($\sqrt{N} \in [12, 14]$, tương ứng 144 đến 196 mục tiêu), **hai thước đo thống kê tách rời sâu sắc**:  
   - Ở 144 mục tiêu, một đội 11 người chăn đạt tỷ lệ gom trung bình $\bar{S} = 0{,}992$ (được bài báo Lama công nhận đạt yêu cầu). Tuy nhiên, tỷ lệ thành công của từng lượt chạy thực tế chỉ đạt **70%**. Nguyên nhân là các lượt thất bại mất 2 con cừu (đạt $142/144 = 0{,}986$) khi lấy trung bình với các lượt hoàn hảo vẫn cho ra kết quả $\ge 0{,}99$.  
   - Thước đo độ tin cậy Clopper-Pearson của HerdSim thẳng thừng bác bỏ quy mô 11 người chăn này, và đòi hỏi đội hình từ **17 đến 25 người chăn** mới có thể đảm bảo 90% số lượt chạy đạt chuẩn.  
   - Sự phân kỳ này mang tính cảnh báo sâu sắc: việc sử dụng tỷ lệ gom trung bình đã che đậy rủi ro đuôi chí tử trong môi trường thưa thớt, tạo ra một cảm giác an toàn giả tạo trong điều khiển hệ thống thực tế.

![Mô hình Lama và di Bernardo trong HerdSim](../figures/fig38_lama.png)

**Hình 13: Đội chăn dắt tối thiểu theo quy mô mục tiêu trong nhiệm vụ thu gom của Lama & di Bernardo (2024).**  
Khung trái thể hiện bán kính cảm nhận hữu hạn 10 (vùng ngưỡng mật độ tô xám); khung phải thể hiện tầm nhìn vô hạn. Hình vuông biểu diễn số liệu đọc từ Hình 2 bài báo gốc; hình tròn biểu diễn thống kê trung bình $\ge 0{,}99$ của Lama chạy trên dữ liệu HerdSim; hình thoi và thanh biểu diễn ranh giới tin cậy $D_{\min}$ của HerdSim ($L \ge 0{,}90$). Với cảm nhận vô hạn, hai phương pháp thống nhất ở số mũ $\approx 0{,}53$. Ở bán kính cảm nhận 10 gần ngưỡng mật độ, thước đo trung bình của Lama chấp nhận đội hình quá sớm (11 người chăn tại 144 mục tiêu), trong khi tiêu chuẩn tin cậy của HerdSim phơi bày rủi ro thất bại và yêu cầu đội hình từ 17–25 tác tử.  
*Số liệu:* [results_tables.md: Lama and di Bernardo (2024): gather task](results_tables.md#lama-and-di-bernardo-2024-gather-task).

---

## 4. Phân tích Vi mô: Dị thường Bố cục Phân cụm và Đo đạc Từng tích tắc

### 4.1 Dị thường Bố cục `split` (Bầy phân cụm) và Sự mù quáng Topo của Thuật toán Hungarian
Trên bố cục `split` tại $N \ge 200$, việc bổ sung thêm chó hoàn toàn không cải thiện xác suất thành công: ở thời hạn $6\times$ dưới tiêu chí 99%, tỷ lệ thành công chỉ dao động quanh 0,60–0,90 với mọi $D \ge 4$ (và tụt xuống 0,10–0,76 dưới tiêu chí nghiêm ngặt), trong khi ở thời hạn gấp gáp $3\times$, tỷ lệ thành công sụp đổ về gần bằng 0 trên mọi quy mô đội hình.

Phân tích replay chẩn đoán từng tích tắc vạch trần hai cơ chế tương hỗ làm tê liệt hệ thống:
1. **Sự mù quáng topo của thuật toán gán việc Hungarian ($D = 4$)**:  
   Thuật toán Hungarian tối ưu hóa việc phân công tác tử bằng cách cực tiểu hóa tổng khoảng cách hình học thuần túy: $\min \sum \lVert \mathbf{x}_{\mathrm{dog}} - \mathbf{x}_{\mathrm{sheep}} \rVert$. Tuy nhiên, thuật toán này hoàn toàn **không nhận thức được cấu trúc cụm topo (cluster-blind)**. Khi một bầy cừu bị tách thành hai hoặc nhiều cụm không gian riêng biệt, một cụm tình cờ nằm gần hơn hoặc có nhiều cá thể tản mác hơn sẽ thu hút toàn bộ các chú chó. Cả đàn chó bị kéo dồn về một cụm con duy nhất, bỏ mặc cụm còn lại trôi dạt tự do ra rìa đồng cỏ. Khi chúng tôi can thiệp vào quy tắc chọn mục tiêu, buộc các chú chó phải phân bổ đều cho các cá thể cách nhau tối thiểu một bán kính bầy $f(N) = r_a N^{2/3}$, thời gian hoàn thành trung vị tại $D = 4$ giảm một nửa: từ $631\text{ s}$ xuống còn $318\text{ s}$ ($N = 200$, $6\times$).

2. **Hiện tượng Chó bị "đóng băng" do Quy tắc Giữ khoảng cách $3 r_a$ ($D \ge 4$)**:  
   Hành vi nguyên bản của Strömbom quy định một chú chó phải dừng bước đứng yên ngay khi khoảng cách tới bất kỳ con cừu nào nhỏ hơn $3 r_a = 6\text{ m}$. Trên các bố cục liên tục (`wide`, `outlier_rich`), tỷ lệ chó bị đứng yên chỉ chiếm từ 1% đến 7%.  
   Ngược lại, trên bố cục `split`, do bầy cừu bị vỡ mảnh thành các cụm nhỏ nằm xen kẽ với hướng di chuyển của đàn chó, **trung bình có tới 25% số chó trong đội hình bị rơi vào trạng thái đứng yên bất động**. Khi tiến hành replay chẩn đoán với khoảng cách dừng được rút ngắn xuống kích thước cơ thể thực $r_a = 2\text{ m}$, thời gian lùa giảm ngay 21–24% tại $D = 8$ và 16, đạt tỷ lệ thành công tuyệt đối 12/12 tại $D = 16$ ($N = 200$, $6\times$).  
   Tuy nhiên, ở thời hạn gấp gáp $3\times$, sự can thiệp này vẫn không thể cứu vãn nhiệm vụ: ngân sách thời gian quá ngắn khiến sự thiếu vắng cơ chế nhận thức topo trở thành bản án tử hình đối với thuật toán.

![Đường cong Split](../figures/fig23_split_curves.png)

**Hình 14: Hiện tượng chững hiệu suất và phân tích ranh giới trên bố cục bầy phân cụm `split` ($N \ge 200$, thời hạn $6\times$).**  
Bốn khung hình so sánh tỷ lệ thành công kèm khoảng tin cậy Clopper-Pearson 99% theo số chó $D$ (thang log) trên `split` ($N = 100, 200, 400$) và `wide` ($N = 400$) để đối chứng. Chấm tròn xanh thể hiện tiêu chí nghiêm ngặt 100%; ô vuông cam thể hiện tiêu chí 99%; đường chấm ngang là ngưỡng tin cậy $\theta = 0{,}90$. Trong khi trên `wide` $N = 400$, tỷ lệ thành công tiệm cận 1,0 khi tăng số chó, trên `split` đường cong đi ngang và không thể đạt tin cậy do hiện tượng dồn cụm và đứng yên đóng băng của tác tử.  
*Số liệu:* `results/dmin_m6` và `results/dmin_f99_m6`; tra cứu tại [results_tables.md: dmin_m6](results_tables.md#dmin_m6) và [results_tables.md: dmin_f99_m6](results_tables.md#dmin_f99_m6).

### 4.2 Tương quan Đo đạc Vi mô Từng tích tắc
Dữ liệu đo đạc chi tiết lưu giữ các giá trị trung bình, cực tiểu và cực đại của toàn bộ các chỉ số vật lý qua từng tích tắc thời gian:
- **Tương quan nghịch giữa Độ tản bầy và Xác suất Thành công**:  
  Hệ số tương quan thứ hạng Spearman giữa độ tản trung bình của bầy cừu trong một ô tham số (bán kính hiệu dụng RMS, mét) và tỷ lệ thành công của ô đó đạt mức rất cao: **$r = -0{,}71$ đến $-0{,}76$** ở thời hạn $6\times$ ($-0{,}57$ đến $-0{,}68$ ở $3\times$) trên các ô có ít nhất 20 hạt giống. Các chiến thuật điều phối giữ được bầy cừu ở trạng thái nén chặt luôn có xác suất thành công áp đảo.
- **Mức độ chen chúc giữa các chú chó**:  
  Trong thuật toán phối hợp `strombom_multi`, tỷ lệ các chú chó có đồng đội trong cự ly $2\text{ m}$ bằng 0 cho tới $D = 6$ trên bố cục `wide`, và tăng lên 0,45–0,59 tại $D = 16$ trên cả ba bố cục phân tán. Ngược lại, ở mô hình không phối hợp FAT, con số này luôn duy trì ở mức báo động 0,56–0,82 ngay từ $D = 2$, phản ánh bản chất dồn cục hỗn loạn.

![Đo đạc từng tích tắc](../figures/fig27_metrics.png)

**Hình 15: Tương quan đo đạc vi mô và chẩn đoán trạng thái tác tử qua từng tích tắc thời gian.**  
*(Khung a)* Tương quan tuyến tính âm mạnh mẽ giữa độ tản bầy trung bình (bán kính RMS, mét) và tỷ lệ thành công ở thời hạn $6\times$ ($r = -0{,}71$ đến $-0{,}76$).  
*(Khung b)* Trung vị tỷ lệ chó bị rơi vào trạng thái đứng yên đóng băng theo số chó $D$ tại $N = 200$ (tiêu chí 99%) cho `wide`, `split` và `outlier_rich`. Bố cục `split` ghi nhận xấp xỉ một phần tư lực lượng chó bị vô hiệu hóa do quy tắc dừng $3 r_a = 6\text{ m}$.  
*(Khung c)* Trung vị tỷ lệ chó có đồng đội trong phạm vi $2\text{ m}$ theo $D$, cho thấy mức độ chen chúc tăng đều khi quy mô đội mở rộng trên cả ba bố cục.  
*Số liệu:* `results/dmin_m6` và `results/dmin_f99_m6`.

---

## 5. Thảo luận và Hàm ý Khoa học

### 5.1 So sánh với các Định luật Mở rộng Lý thuyết
Hệ số góc tăng trưởng dưới tuyến tính của chúng tôi ($\alpha = 0{,}20 - 0{,}42$ ở $12\times$ trên 5 kích thước; 0,27–0,38 trên 9 kích thước, mục 3.8) tương phản sâu sắc với định luật tỷ lệ $\sqrt{M}$ ($\alpha = 0{,}50$) được chứng minh bởi Lama và di Bernardo (2024) trên các mục tiêu không gắn kết. Sự khác biệt này bắt nguồn từ bản chất sinh học: với các hạt rời rạc, mỗi hạt lạc phải được tiếp cận trực tiếp bởi một tác tử chăn dắt. Với bầy cừu có tính xã hội, lực hút toàn cục ($n = N - 1$) giúp một chú chó có thể gián tiếp tác động lên cả bầy ngay khi đưa được các con lạc vào tầm giao tiếp thị giác, giảm mạnh số lượng tác tử cần thiết.

Các lượt chạy độ gắn kết (mục 3.11) kiểm tra trực tiếp cách giải thích này. Làm bầy gắn kết hơn mức của bài báo hầu như không đổi độ dốc (0,20 trên `wide`, so với 0,20–0,30 của bầy gốc), còn bầy yếu hơn duy nhất mà mô hình tạo được (mỗi con cừu bị hút về một nửa bầy) làm độ dốc tăng lên 0,40–0,70, một khoảng chứa mốc 0,5 của mục tiêu không gắn kết. Thời hạn cũng có tác dụng tương tự: ở $6\times$ độ dốc là 0,38–0,61. Độ gắn kết và áp lực thời gian cùng quyết định một bầy nằm ở phía nào của quy luật căn bậc hai.

Mục 3.14 nay cho phía không gắn kết ngay trong HerdSim. Mô hình của bài báo, chạy ở đây, tái lập chính quy luật của nó: số mũ 0,52–0,53 với cảm nhận vô hạn và 0,41–0,42 trên ngưỡng mật độ với bán kính cảm nhận 10, theo cả thống kê của bài báo lẫn của HerdSim. Cả hai đều lớn hơn 0,27–0,38 của bầy Strömbom ở 12 lần thời gian lùa, đúng như cách giải thích ở trên dự đoán. Hai loạt chạy vẫn khác nhau cả về nhiệm vụ và quy tắc người chăn chứ không chỉ về độ gắn kết, nên phần khoảng cách thuộc về độ gắn kết vẫn chưa được đo.

### 5.2 Bản chất Hai giai đoạn và Phân loại Thất bại trong Chăn dắt Tập thể

Kết quả phân tích 367.150 lượt chạy chỉ ra rằng bài toán chăn dắt tập thể bao gồm hai giai đoạn vật lý hoàn toàn khác biệt, dẫn đến một hệ phân loại thất bại rõ ràng:

1. **Phân loại Thất bại: Có Cấu trúc (Structural) vs. Do Ranh giới Thời gian (Boundary/Temporal)**:
   - **Thất bại có Cấu trúc (Structural Failures)**: Xảy ra trong pha Gom ban đầu (Collecting). Khi quy mô đội chó không đạt ngưỡng tối thiểu ($D < D_{\min}$), đàn chó thiếu năng lực hình học để khống chế tốc độ tản dạt tự nhiên của các cá thể cừu. Bầy cừu liên tục tách nhóm nhanh hơn khả năng thu gom tuần tự của các chú chó đơn lẻ, dẫn đến bế tắc vĩnh viễn (stalling). Đối với các thất bại có cấu trúc này, việc kéo dài thời gian deadline cũng không thể giúp bầy thành công.
   - **Thất bại do Ranh giới & Thời gian (Boundary & Temporal Failures)**: Xảy ra trong pha Lùa (Driving) hoặc Đóng chuồng (Terminal Penning). Đội chó đã hoàn thành xuất sắc việc gom đàn và lùa khối cừu gắn kết vượt qua bãi cỏ mở (đã đưa $\ge 99\%$ cừu vào chuồng), nhưng bị quá giờ do deadline hoặc thất bại vì nhiễu động ranh giới cửa chuồng (hiệu ứng con cừu lạc cuối cùng - Straggler Effect).
   - Sự phân tách này giải thích một cách cơ học vì sao tiêu chí 99% arrival đo lường năng lực phối hợp tập thể thực chất (loại bỏ nhiễu động ranh giới cửa chuồng), trong khi tiêu chí 100% bị chi phối bởi các thất bại thời gian cục bộ.
   - *Số liệu Phân loại Thực nghiệm từ 367.150 lượt chạy*:
     
     | Giao thức | Mô tả Nhiệm vụ | Số Lượt Thất bại | Thất bại Cấu trúc (Kẹt pha gom) | Thất bại Ranh giới (Nghẽn cổng) | Tỷ lệ Thất bại Cấu trúc |
     | :--- | :--- | :---: | :---: | :---: | :---: |
     | `dmin_m12` | 100% Chứa đàn, 12× Thời gian | 235 | 180 | 55 | **76,6%** |
     | `dmin_m6` | 100% Chứa đàn, 6× Thời gian | 889 | 639 | 250 | **71,9%** |
     | `dmin_m3` | 100% Chứa đàn, 3× Thời gian | 710 | 571 | 139 | **80,4%** |
     | `dmin_f99_m12` | 99% Vào đích, 12× Thời gian | 235 | 213 | 22 | **90,6%** |
     | `dmin_f99_m6` | 99% Vào đích, 6× Thời gian | 1.511 | 1.067 | 444 | **70,6%** |
     | `dmin_f99_m3` | 99% Vào đích, 3× Thời gian | 584 | 457 | 127 | **78,3%** |

     *Kết luận định lượng:* Trên mọi giao thức, **70% đến 90%** các lượt thất bại bắt nguồn từ việc thiếu tác tử thu gom ở pha đầu (thất bại cấu trúc). Dưới tiêu chuẩn 99% ở thời hạn thong thả 12×, tỷ lệ thất bại cấu trúc đạt tới **90,6%**, chứng minh tiêu chuẩn 99% đã loại bỏ thành công phần lớn nhiễu động ranh giới cục bộ.

2. **Chỉ số Tải trọng Tản mác Tổng thể ($S_0 \times N$)**:
   - Khi nghiên cứu động lực học gom bầy, tích số giữa độ tản mác ban đầu của bầy $S_0$ (bán kính tản mác bình phương trung bình) và quy mô đàn $N$, tức $S_0 \times N$, đại diện cho tổng công hình học mà đàn chó phải bỏ ra để nén bầy về trạng thái gắn kết.
   - Trên bãi cỏ tập trung (`compact`), $S_0$ rất nhỏ nên $S_0 \times N \approx 0$, giải thích vì sao $D_{\min} = 1$ bất kể $N$ tăng lên 400 hay 1131.
   - Trên bãi cỏ tản mác (`wide`, `split`, `outlier_rich`), $S_0$ lớn khiến $S_0 \times N$ tăng vọt, buộc thời hạn khẩn cấp phải tăng mạnh số lượng chó để gom song song trước khi cừu phân tán thêm.
   - *Bảng Tải trọng Tản mác Thực nghiệm ($S_0 \times N$) và Tỷ lệ Thành công (`dmin_m6`)*:

     | Bố cục | Quy mô $N$ | Độ tản mác ban đầu $S_0$ | Tải trọng $S_0 \times N$ | Tỷ lệ Thành công Tổng thể |
     | :--- | :---: | :---: | :---: | :---: |
     | `compact` | 25 | $3{,}59\text{ m}$ | **89,9** | 100,0% |
     | `compact` | 100 | $5{,}67\text{ m}$ | **567,2** | 100,0% |
     | `compact` | 400 | $7{,}68\text{ m}$ | **3.073,5** | 100,0% |
     | `wide` | 400 | $8{,}11\text{ m}$ | **3.242,3** | 83,8% |
     | `outlier_rich` | 400 | $10{,}16\text{ m}$ | **4.065,6** | 55,3% |
     | `split` | 400 | $8{,}81\text{ m}$ | **3.524,2** | 21,1% |

     Khi tải trọng $S_0 \times N$ vượt ngưỡng $\approx 3.500$, tỷ lệ thành công sụp đổ thảm hại nếu không có đội hình chó song song đủ lớn để phân chia không gian bao quát.

3. **Cơ chế Quá tải Hai đầu (Dual-Regime Crowding Collapse)**:
   - Hiện tượng quá tải không chỉ giới hạn ở một phía mà xuất hiện ở hai đầu cực trị quy mô:
     - *Ở đàn lớn ($N \ge 400$)*: Quá tải xuất hiện khi mật độ tuyến tính của chó trên vòng cung lùa vượt quá giới hạn hình học ($D > D_{\mathrm{cap}} \approx 12$) khi chó có kích thước chiếm chỗ $2\text{ m}$, gây nghẽn đường và cản trở việc cơ động gom cừu lạc.
     - *Ở đàn cực nhỏ ($N \le 10$)*: Quá tải xuất hiện khi tỷ lệ chó/cừu quá lớn ($D/N \gg 1$). Khi một đàn chó đông vây quanh một cụm cừu nhỏ, các vector áp lực đe dọa từ mọi phía triệt tiêu hoàn toàn hành lang thoát hiểm tự nhiên của cừu, gây hỗn loạn và làm vỡ bầy.

### 5.3 Mười Đóng góp Khoa học Chính

1. **Bản đồ Ranh giới Thực nghiệm Hoàn chỉnh**: Thiết lập bản đồ ranh giới $D_{\min}$ và $D_{\mathrm{sat}}$ có độ tin cậy toán học 99% đầu tiên qua các quy mô đàn ($N \le 566$, mở rộng đến 3200), bố cục và thời hạn.
2. **Tiêu chí Thành công Định hình Vật lý**: Chứng minh tiêu chí tuyệt đối 100% tạo ra nút thắt cổ chai nhân tạo (Hiệu ứng cá thể lạc đàn), trong khi tiêu chí 99% phản ánh đúng năng lực phối hợp tập thể.
3. **Tách bạch Độ tin cậy khỏi Tốc độ**: Chứng minh quy mô đội để đạt tốc độ tối đa ($D_{\mathrm{sat}}$) tăng nhanh gấp đôi quy mô đội chỉ để đạt độ tin cậy ($D_{\min}$). Chó bổ sung vượt quá $D_{\mathrm{sat}}$ chỉ làm tăng chi phí mà không mang lại tốc độ.
4. **Giải phẫu Tầng Phối hợp Đa Tác tử**: Chứng minh việc chuyển trạng thái gom/lùa đưa đội chó độc lập tới $N = 200$, nhưng tầng phân công tối ưu Hungarian là bắt buộc ở $N \ge 400$.
5. **Hiện tượng Quá tải do Kích thước Vật lý**: Chứng minh tác hại của sự đông đúc không xuất hiện ở chó dạng điểm, nhưng bộc lộ rõ rệt khi chó có thể tích chiếm chỗ ($2\text{ m}$), gây nghẽn vòng cung lùa.
6. **Mục tiêu Gắn kết và Không Gắn kết**: Liên hệ độ mạnh của lực gắn kết với số mũ tăng trưởng: bầy của bài báo tăng chậm hơn quy luật $\sqrt{N}$ ở thời hạn thong thả, và làm yếu độ gắn kết đưa số mũ về phía 0,5.
7. **Ranh giới Giải tích của Quy tắc Lùa Strömbom**: Phát hiện giới hạn toán học tại $N = 1056$ nơi khoảng cách lùa vượt quá tầm cảm nhận của cừu, chỉ ra sự cần thiết phải đặt trần cự ly cho các đàn khổng lồ.
8. **Đánh đổi giữa Cảm biến và Giao tiếp**: Đo cái giá của tầm nhìn cục bộ ($30\text{--}65\text{ m}$, khoảng một chó ở $N = 200$) và cho thấy, ở tầm 65 m, chia sẻ với cả đội đưa $D_{\min}$ về giá trị toàn cục trên `wide` $N = 200$ (không đạt trên `split`).
9. **Khung Phân loại Thất bại và Tải trọng Tản mác ($S_0 \times N$)**: Cung cấp cơ sở lý thuyết phân biệt thất bại cấu trúc khỏi thất bại thời gian ranh giới, đồng thời giải thích bằng tải trọng tản mác tổng thể.
10. **Hệ thống Mô phỏng Mã nguồn mở Minh bạch**: Cung cấp bộ công cụ mô phỏng tất định, an toàn trước sự cố, có thể tái lập chính xác qua 367.150 lượt chạy.

### 5.4 Gợi ý Ứng dụng Thực tế (Robot & Drone)

- **Định cỡ Đội hình**: Ở thời hạn thong thả, 1 đến 3 robot có thể kiểm soát đàn cừu tản mác lên tới 400 con, và một đàn tập trung cần 1 robot tới $N = 1131$ (2 ở 1600). Áp lực thời hạn làm dịch chuyển nhu cầu tương đương với việc tăng đàn cừu lên gấp 4 lần, do đó cần xác định quỹ thời gian trước khi chốt số lượng robot.
- **Tốc độ tốn kém hơn Độ tin cậy**: Trên bầy `wide` và `outlier_rich`, đội hình chạy nhanh nhất đòi hỏi số lượng robot gấp 1,5 đến 2,5 lần đội hình tối thiểu (nhiều hơn trên `split`); robot vượt quá ngưỡng này chỉ làm hao pin vô ích (Bảng 6).
- **Kích thước vật lý giới hạn quy mô đội**: Robot không thể đứng gần nhau dưới 2 m sẽ gây nghẽn vòng cung lùa của bầy `outlier_rich` từ khoảng 9 thiết bị tại $N = 400$.
- **Chia sẻ bản đồ trước khi mua thêm robot**: Tầm nhìn cục bộ tốn thêm khoảng 1 robot ở $N = 200$; chia sẻ dữ liệu giữa mọi robot lấy lại được robot đó trên `wide` (không đạt trên `split`).
- **Lùi xa để Giữ đàn**: Robot bắt buộc phải rút lui ra ngoài tầm phản ứng của động vật để giữ chúng trong chuồng; robot đứng lại ở cửa chuồng chỉ làm đàn vật nuôi tiếp tục bỏ chạy.

---

## 6. Hạn chế và Đe dọa Tính Đúng đắn

1. **Giản lược Động học 2D**: Cừu và chó được mô hình hóa dưới dạng chất điểm chuyển hướng tức thì và không bị mệt mỏi thể lực.
2. **Điều kiện Biên Mở**: Đồng cỏ mô phỏng không có hàng rào; đồng cỏ thực tế có hàng rào giúp chó dồn những con cừu lạc.
3. **Các Khoảng chặn Ranh giới**: Các ô tham số mấp mé ngưỡng $\theta = 0{,}90$ vẫn chưa ngã ngũ tại mốc trần 200 hạt giống, đòi hỏi phải báo cáo dưới dạng khoảng chặn.
4. **Tầm nhìn Toàn cục trong Lưới chính**: Ngoại trừ các thử nghiệm ở mục 3.12, mô hình giả định chó biết vị trí của mọi con cừu. Mục 3.12 thử tầm nhìn giới hạn với vị trí đã biết trong tầm đó; cảm nhận chỉ theo góc hướng (bearing-only) chưa được mô hình hóa.
5. **Các Thiết lập Kỹ thuật Bổ sung**: Quy tắc rút lui giữ đàn, giãn cách chó $2\text{ m}$, và trần cự ly lùa là các giải pháp kỹ thuật do HerdSim đưa ra chứ không có nguồn gốc từ tài liệu sinh học.
6. **Mức trần Hiệu chuẩn Bầy và Giả định Đĩa Mét**: Vượt quá $N \approx 600$, bầy cừu Strömbom không còn tự co cụm về kích thước riêng; các nghiên cứu trên 600 con dựa trên mật độ đàn được áp đặt. Mô hình sử dụng khoảng cách mét tuyệt đối ($r_a = 2\text{ m}$) thay vì tương tác tô pô ($k$ láng giềng gần nhất); ở quy mô cực lớn ($N = 3200$), vùng lõi bầy cừu có xu hướng bị nén ép nhẹ do tương tác mét chưa tính đến sự che khuất thị giác giữa các cá thể.
7. **Cỡ mẫu Replay Chẩn đoán**: Các phép thử replay áp lực và dị thường split sử dụng 12 hạt giống mỗi ô, mang tính chỉ báo cơ chế chứ không phải phân tích giới hạn toàn diện.
8. **Tiên đề Mô hình hóa về Chuẩn hóa Lực Sợ hãi**:
   - Mô hình gốc của Strömbom chỉ áp dụng cho một chú chó. HerdSim chuẩn hóa tổng vector lực đẩy từ các chú chó trong phạm vi $65\text{ m}$ về độ dài đơn vị tiêu chuẩn ($\lVert \mathbf{R}_{s,i} \rVert = 1.0$).
   - *Vì sao không dùng phép cộng lực đại số*: Lực gắn kết xã hội của cừu là $c = 1{,}05$. Nếu cộng dồn lực đẩy độc lập từ hai chú chó ở góc $\theta$, độ lớn tổng lực là $2\cos(\theta/2)$, luôn lớn hơn $1{,}05$ trừ khi hai chú chó đứng đối diện nhau ở góc $\gt 116^\circ$. Do đó, phép cộng lực tuyến tính sẽ khiến 2 chú chó đi cạnh nhau xé toạc đàn cừu ngay từ $D = 2$.
   - *Tính chất tiên đề*: Chuẩn hóa vector đơn vị là một tiên đề mô hình hóa có chủ đích (modeling postulate) nhằm bảo toàn tính gắn kết bầy đàn và cô lập năng lực điều phối không gian. Trong sinh học thực địa, phản xạ hoảng loạn phi tuyến của động vật khi bị nhiều kẻ săn mồi vây hãm có thể làm thay đổi động lực học bầy đàn, đây là một câu hỏi mở cho các nhà sinh học thực nghiệm.
9. **Kẹp cứng Vận tốc Rời rạc so với Mô hình Lực Liên tục**:
   - Trong Strömbom, vận tốc cừu bị kẹp cứng ở bước nhảy tối đa $\delta = 1{,}0\text{ m/s}$. Ngưỡng bão hòa $D_{\mathrm{sat}}$ (nơi thêm chó không làm tăng tốc độ lùa) là một hệ quả động học tất yếu khi toàn bộ vòng cung lùa đã được lấp đầy.
   - Ngược lại, trong mô hình trường lực liên tục Kubo et al. (2022), các lực đẩy thế năng cộng dồn có thể gia tốc bầy cừu vượt mốc vận tốc cơ bản, giải thích vì sao Kubo tiếp tục giảm thời gian hoàn thành khi tăng $D$.
10. **Phạm vi Đảm bảo Tính Tất định Số thực (Floating-Point Portability)**:
    - Tính năng Replay đảm bảo tái lập chuẩn xác từng bit (bit-identical) trên cùng một vi kiến trúc CPU x86_64 dưới môi trường khóa cứng `uv.lock` và chế độ đơn luồng BLAS (`OPENBLAS_NUM_THREADS=1`).
    - Việc chuyển đổi mã nguồn sang các kiến trúc khác nhau (ví dụ: ARM NEON vs x86 AVX-512) hoặc các trình biên dịch C/BLAS khác nhau có thể tạo ra sai lệch 1 ULP ở các phép tính lượng giác, có thể làm thay đổi kết quả ở một số hạt giống mấp mé ranh giới timeout.
11. **Bảo vệ Thiên kiến Dừng Sớm trong Lấy mẫu Tuần tự**:
    - HerdSim áp dụng khoảng tin cậy Clopper-Pearson 99%. Do bản chất của Clopper-Pearson là cực kỳ bảo thủ (độ bao phủ thực tế luôn $\ge 99\%$, thường đạt $99{,}5\%$ do tính rời rạc của số nguyên), kết hợp với việc phân bổ theo khối rời rạc 10 hạt giống (đòi hỏi tối thiểu 51 hạt giống thắng liên tiếp mới đạt độ tin cậy), thuật toán tự động triệt tiêu thiên kiến lạc quan (optional stopping bias) mà không làm phồng sai số Loại I.
12. **Mô hình Lama và di Bernardo là bản tái lập từ văn bản bài báo**: bài báo không công bố mã. Ở những chỗ văn bản không nói rõ, HerdSim đưa ra các lựa chọn có ghi lại (lực đẩy hướng ra xa người chăn; một lượt kết thúc khi mọi người chăn ở trong đích và không ai thấy mục tiêu bên ngoài; mục tiêu và người chăn được tích phân từ cùng một trạng thái). Giá trị của bài báo được đọc từ hình với độ phân giải một người chăn và 50 lượt mỗi ô. Đội của HerdSim vẫn nhỏ hơn đội của bài báo tối đa một người chăn ở biên thiếu người chăn; nguyên nhân của người chăn cuối cùng đó chưa được tìm ra.

---

## 7. Kết luận và Hướng Nghiên cứu Tương lai

Thông qua 367.150 lượt mô phỏng trên 39 giao thức, HerdSim đã lập bản đồ toàn diện về quy mô đội tối thiểu $D_{\min}$, quy mô bão hòa $D_{\mathrm{sat}}$, và các điều kiện khiến việc tăng thêm chó gây hại. Đàn cừu tập trung chỉ cần 1 chú chó tới $N = 1131$; trên đồng cỏ phân tán, số chó cần thiết tăng trưởng dưới tuyến tính với độ dốc 0,27–0,38 ở $12\times$ và 0,38–0,61 ở $6\times$, trong khi đội nhanh nhất tăng nhanh gấp khoảng hai lần. Dưới tiêu chí nghiêm ngặt, con cừu lạc cuối cùng chi phối cuộc chơi; dưới tiêu chí 99%, kết quả có tính bền vững cao trước các quy ước mô phỏng. Sự phối hợp đội ngũ quan trọng ở các đàn lớn; chó dạng điểm thêm vào không bao giờ làm mất độ tin cậy trên `wide` hay `outlier_rich` nhưng làm `split` chậm đi, và chó chiếm chỗ vật lý gây thất bại; và quy tắc lùa kinh nghiệm của Strömbom bộc lộ giới hạn giải tích ở đàn trên một ngàn con. Chạy trong cùng mô phỏng, các mục tiêu không gắn kết của Lama và di Bernardo tái lập quy luật căn bậc hai của họ, và quy luật này cũng giữ dưới quy tắc tin cậy của HerdSim, trừ gần ngưỡng mật độ, nơi tỷ lệ trung bình 0,99 che đi những lượt mất một mục tiêu.

### Hướng Nghiên cứu Tiếp theo

1. **Phân bổ Nhiệm vụ Nhận thức Cụm trên Bố cục Phân cụm**: Giải quyết hiện tượng tắc nghẽn trên bố cục `split` bằng cách thiết kế thuật toán phân công chó tỏa đều ra các cụm cấu trúc topo khác nhau thay vì chọn theo khoảng cách trọng tâm toàn cục.
2. **Nhiệm vụ Giữ đàn có Hàng rào Cổng**: Đánh giá giai đoạn giữ đàn bằng cổng rào vật lý thay vì rút lui ra đồng cỏ mở, kiểm tra xem nút thắt giữ đàn có còn tồn tại khi lối thoát bị chặn.
3. **Cảm nhận Góc nhìn Thuần túy (Bearing-Only)**: Mở rộng mô hình tầm nhìn cục bộ sang cảm nhận chỉ có góc hướng mà không có cự ly chính xác, mô phỏng chân thực camera trên các thiết bị drone.
4. **Ghép chéo hai mô hình trên cùng một nhiệm vụ**: Chạy quy tắc đội Strömbom trên mục tiêu Lama trong nhiệm vụ gom, và người chăn Lama trên cừu Strömbom, để tách khoảng cách giữa các số mũ ở mục 3.14 thành phần do độ gắn kết và phần do quy tắc người chăn và nhiệm vụ. Mỗi quy tắc đọc những đại lượng mà phía kia không có (quy tắc đội đọc khoảng cách gom vô nghĩa khi không có gắn kết, người chăn đọc khoảng cách tới một đích mà trong nhiệm vụ lùa nằm xa bầy), nên mỗi phép ghép cần thiết kế riêng trước.
5. **Thu thập Dữ liệu Thực địa Đa Chó / Drone với Vòng đeo GPS**: Hợp tác với các nhà nghiên cứu động vật thực địa để đo đạc phản ứng của đàn cừu khi bị rượt đuổi bởi từ 2 chú chó trở lên, kiểm tra xem cừu thật cảm nhận nỗi sợ theo kiểu cộng dồn hay chuẩn hóa.
6. **Ước lượng Trọng tâm Bầy bằng Gradient Mật độ Cục bộ**: Thay thế giả định cừu nhận biết Trọng tâm Toàn cục (GCM) bằng cơ chế sinh học thực tế: cừu ước tính hướng về trung tâm bầy thông qua vector gradient mật độ của các láng giềng gần nhất, loại bỏ hoàn toàn nhu cầu về giác quan viễn thám toàn cầu mà vẫn bảo toàn góc lệch điều hướng dưới $15^\circ - 20^\circ$.

---

## Tính Sẵn sàng của Dữ liệu và Mã nguồn

Mọi lượt chạy và quyết định của từng ô được lưu trong `results/<protocol>/`. Các bảng chứa số liệu của báo cáo này nằm trong [results_tables.md](results_tables.md); mỗi khối ghi rõ script đã tạo ra nó. Cách chạy lại toàn bộ nghiên cứu và tạo lại các bảng: xem [cli/README.md](../../cli/README.md) và [tài liệu tham chiếu CLI](../guides/cli_reference.md).

---

## Tài liệu Tham khảo

- Auletta F, Fiore D, Richardson MJ, di Bernardo M (2021). Herding stochastic autonomous agents via local control rules and online global target selection strategies. *arXiv:2010.00386*.
- Brown D, Garrity T, Perkins D, Hunter D, Pochman W (2025). Optimal control strategies for multi-agent sheep herding. *arXiv:2510.25115*.
- di Bernardo M (2026). Multi-scale control of large agent populations: from density dynamics to individual actuation. *arXiv:2603.15160*.
- Green T, et al. (2022). A minimalist solution to the multi-robot barrier coverage problem. *Towards Autonomous Robotic Systems (TAROS 2021)*, LNCS 13054.
- Jadhav V, Pasqua R, Zanon C, Roy M, Tredan G, Bon R, Guttal V, Theraulaz G (2024). Collective responses of flocking sheep (*Ovis aries*) to a herding dog (border collie). *Communications Biology* 7: 1543.
- Kubo M, Tashiro M, Sato H, Yamaguchi A (2022). Herd guidance by multiple sheepdog agents with repulsive force. *Artificial Life and Robotics* 27: 416–427.
- Lama A, di Bernardo M (2024). Shepherding control and herdability in complex multiagent systems. *Physical Review Research* 6: L032012.
- Li A, Ogura M, Wakamiya N (2025). Swarm shepherding using bearing-only measurements. *Philosophical Transactions of the Royal Society A* 383: 20240145.
- Pierson A, Schwager M (2015). Bio-inspired non-cooperative multi-robot herding. *IEEE International Conference on Robotics and Automation (ICRA)*.
- Ranganathan A, et al. Emergent strategies for shepherding a flock. *arXiv:2211.04352*.
- Strömbom D, Mann RP, Wilson AM, Hailes S, Morton AJ, Sumpter DJT, King AJ (2014). Solving the shepherding problem: heuristics for herding autonomous, interacting agents. *Journal of the Royal Society Interface* 11(100): 20140719.
- Yaxley KJ, Joiner KF, Abbass H (2021). Drone approach parameters leading to lower stress sheep flocking and movement: sky shepherding. *Scientific Reports* 11: 7803.

---

## Phụ lục: Nhật ký Các Giao thức Thực nghiệm

| Giao thức | Tổng lượt chạy | Số ô khảo sát | Số ô quyết định | Ô mở tại trần (200) | Lỗi | Thời gian chạy |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `dmin_m12` | 17.220 | 183 | 179 | 4 | 0 | 1,24 h |
| `dmin_m6` | 13.470 | 191 | 170 | 21 | 0 | 0,28 h |
| `dmin_m3` | 9.530 | 183 | 178 | 5 | 0 | 0,17 h |
| `dmin_f99_m12` | 11.100 | 180 | 178 | 2 | 0 | 0,41 h |
| `dmin_f99_m6` | 14.240 | 191 | 174 | 17 | 0 | 0,49 h |
| `dmin_f99_m3` | 11.140 | 185 | 177 | 8 | 0 | 0,27 h |
| `dmin_fat` | 8.660 | 181 | 179 | 2 | 0 | 0,22 h |
| `dmin_f99_fat` | 8.670 | 184 | 183 | 1 | 0 | 0,23 h |
| `dmin_kubo` | 1.080 | 18 | 18 | 0 | 0 | 0,08 h |
| Các giao thức độ nhạy (14 runs) | 69.630 | 921 | 800 | 121 | 0 | 3,27 h |
| **Tổng cộng** | **164.740** | **2.417** | **2.236** | **181** | **0** | **~6,7 h** |

Các lượt chạy tiếp nối (tiêu chí 99%; thời gian ở 20 workers):

| Giao thức | Lượt chạy | Số ô | Ô mở tại trần | Lỗi | Số giờ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `dmin_f99_m12`, `dmin_f99_m6`, `dmin_f99_m3` (chạy tiếp: hạt giống thời gian; thêm $N$ 71, 141, 283, 566 cho hai lưới đầu) | +38.770 | | | 0 | 4,0 |
| `dmin_f99_indep` | 12.990 | 181 | 18 | 0 | 0,30 |
| `dmin_f99_kubo` | 3.260 | 38 | 6 | 0 | 0,18 |
| `dmin_f99_hold` | 14.280 | 280 | 18 | 0 | 0,74 |
| `dmin_f99_hold_spacing` (chạy lại với quy tắc khoảng cách cứng) | 13.930 | 283 | 19 | 0 | 0,70 |
| `dmin_f99_c1.3`, `_c1.6`, `_c2.0` | 10.800 / 10.830 / 10.780 | 180 mỗi protocol | 1 / 0 / 0 | 0 | 0,31 / 0,29 / 0,41 |
| `dmin_f99_k05` | 11.630 | 149 | 14 | 0 | 2,29 |
| `dmin_f99_view_range` | 21.040 | 293 | 27 | 0 | 0,53 |
| `dmin_f99_view_comm` | 6.890 | 102 | 3 | 0 | 0,20 |
| `dmin_f99_big` | 2.230 | 84 | 1 | 0 | 3,12 |
| `dmin_f99_big_dense`, `_loose` | 1.320 / 830 | 15 / 14 | 2 / 1 | 0 | 0,73 / 0,26 |
| `dmin_f99_big_cap` | 2.550 (+100 ở $N = 3200$, không tính) | 45 | 3 | 0 | 5,5 (7,6 tính cả $N = 3200$) |
| `lama_r50` (nhiệm vụ gom, bán kính cảm nhận 10) | 17.660 | 500 | 23 | 0 | 6,53 |
| `lama_r50_inf` (nhiệm vụ gom, cảm nhận vô hạn) | 22.620 | 500 | 1 | 0 | 6,47 |

Replay chẩn đoán: 164 lượt replay áp lực và 768 lượt replay split, mọi lượt replay không đổi đều cho kết quả bit-identical với lượt chạy đã lưu. Các pilot kiểm chứng mô hình Lama (8.200 lượt trong hai lần, thư mục tạm không giữ lại) được mô tả ở mục 3.14.

---

## Phụ lục B: Ma trận Yêu sách – Bằng chứng Thực nghiệm (Claim–Evidence Matrix)

Nhằm đảm bảo tính trung thực học thuật và cho phép chuyên gia phản biện kiểm chứng độc lập, bảng dưới đây phân loại toàn bộ 10 phát hiện cốt lõi của báo cáo theo 6 cấp độ nhận thức khoa học:

| # | Luận điểm / Yêu sách Khoa học | Cấp độ Nhận thức | Bằng chứng Thực nghiệm & Nguồn dữ liệu | Độ tin cậy Thống kê | Giới hạn & Cảnh báo (Caveat) |
| :-: | :--- | :---: | :--- | :---: | :--- |
| **1** | **Bất biến Bầy co cụm**: Đàn cừu tập trung (`compact`) chỉ cần 1 chó ($D_{\min} \equiv 1$) tới $N = 1131$. | **Measured & Derived** | `dmin_f99_m12`, `dmin_f99_big_cap`. 42/42 lượt thành công ở $N = 1131, D = 1$. | Tuyệt đối ($L = 1{,}0$) | Đòi hỏi bầy cừu phải bắt đầu ở trạng thái đã liên kết xã hội chặt chẽ. |
| **2** | **Hiệu ứng Biên $N \le 50$**: $D_{\min} \equiv 1$ trên mọi bố cục phân tán và mọi thời hạn. | **Measured & Interpreted** | 23 giao thức cơ sở; toàn bộ các ô $N \le 50$ đều quyết định tại $D = 1$. $R_f \le 7{,}6\text{ m} \ll r_s = 65\text{ m}$. | Rất cao ($L \ge 0{,}90$) | Chỉ đúng khi chó di chuyển nhanh hơn cừu ($v_{\mathrm{dog}} = 1{,}5\text{ m/s}$). |
| **3** | **Mở rộng Dưới tuyến tính**: $D_{\min}$ tăng theo số mũ $\alpha \in [0{,}27, 0{,}38]$ ($12\times$) và $[0{,}38, 0{,}61]$ ($6\times$). | **Measured & Derived** | Khớp lũy thừa log-log trên 9 quy mô đàn ($N = 25\text{--}566$), 367.150 lượt chạy. | Rất cao ($R^2 \ge 0{,}91$) | Áp dụng trong vùng hiệu chuẩn sinh học ($N \le 566$). Trên 566 cần áp đặt mật độ. |
| **4** | **Hiệu ứng Con cừu Lạc cuối cùng (Straggler Effect)**: 97% thất bại nghiêm ngặt ở $N \ge 100$ do xung lượng rượt đuổi ở cửa chuồng. | **Measured & Interpreted** | Đo đạc vi mô từng tích tắc trong `dmin_m6`. Replay điều chỉnh tốc độ chó xuống $1{,}15\text{ m/s}$ triệt tiêu 100% thất bại. | Cao (Phân tích chẩn đoán) | Hiện tượng gắn liền với hình học chuồng đích hở và tiêu chí nghiêm ngặt 100%. |
| **5** | **Sự Mù quáng Topo của Thuật toán Hungarian**: Gán việc khoảng cách thuần túy làm tê liệt đội hình trên bố cục `split`. | **Observed & Interpreted** | `dmin_f99_m6`. Tỷ lệ thành công đi ngang 0,60–0,90. Replay giãn khoảng cách gom $f(N)$ giảm 50% thời gian ($D=4$). | Cao (Replay đối chứng) | Đòi hỏi thuật toán gom nhận thức cụm phân cấp để giải quyết triệt để ở $3\times$. |
| **6** | **Gắn kết Xã hội Bắc cầu tới Định luật Căn bậc hai**: Giảm tương tác xuống $n = 0{,}5N$ đẩy $\alpha$ lên $0{,}40\text{--}0{,}70$. | **Measured & Derived** | `dmin_f99_k05`, `dmin_f99_c1.3` đến `_c2.0`. Bảng 9 và dữ liệu khớp số mũ. | Rất cao ($L \ge 0{,}90$) | Mô hình chưa khảo sát mạng lưới tô-pô phức tạp (small-world hoặc scale-free). |
| **7** | **Điểm Kỳ dị Toán học $N = 1056$**: Cự ly lùi $2\sqrt{N} > 65\text{ m}$ khiến chó bị vô hình; trần $63\text{ m}$ khôi phục lái bầy tới $N = 3200$. | **Derived & Measured** | Chứng minh giải tích $2\sqrt{N} > 65$. Thất bại 0/10 tại $N = 1131$ (không trần). Thành công 42/42 (có trần). | Tuyệt đối (Giải tích & Đo đạc) | Giả định bán kính phản xạ sợ hãi $r_s = 65\text{ m}$ là hằng số sinh học bất biến. |
| **8** | **Sụp đổ do Quá tải Chiếm chỗ ($D \ge 9$)**: Kích thước vật lý $2\text{ m}$ gây nghẽn vòng cung lùa trên `outlier_rich` ($N = 400$). | **Measured & Observed** | `dmin_f99_hold_spacing`. Thành công rơi từ 0,94 ($D=6$) xuống 0,77 ($D=9$) và 0,50 ($D=16$). | Rất cao ($L < 0{,}90$) | Chỉ xuất hiện khi có ràng buộc không gian cứng và bố cục tản mác phức tạp. |
| **9** | **Tầm nhìn Hẹp & Khôi phục Mạng lưới**: Tầm nhìn $< 30\text{ m}$ sụp đổ; mạng toàn đội ở $65\text{ m}$ lấy lại $D_{\min} = 2$. | **Measured** | `dmin_f99_view_range`, `dmin_f99_view_comm`. Bảng so sánh 3 cấu hình giao tiếp. | Rất cao ($L \ge 0{,}90$) | Giả định mạng truyền thông không có độ trễ gói tin (zero packet delay). |
| **10** | **Phân kỳ Thống kê Mô hình Lama (2024)**: Tỷ lệ gom trung bình $\ge 0{,}99$ che giấu $30\%$ rủi ro thất bại tại $N = 144$. | **Measured & Interpreted** | `lama_r50` (17.660 lượt). 11 người chăn đạt $\bar{S} = 0{,}992$ nhưng tỷ lệ thành công chỉ đạt $70\%$. | Rất cao ($L \ge 0{,}90$ vs Mean) | Bài toán gom mục tiêu Brown trên đĩa phẳng $R = 50$, không có lực hút xã hội. |

---

## Phụ lục C: Bảng Kiểm định Khả năng Tái lập Nghiên cứu (Reproducibility Checklist)

| Mục kiểm định | Trạng thái | Minh chứng Thực tế trong Repository |
| :--- | :---: | :--- |
| **Mã nguồn & Nhánh** | `Verified` | Nhánh `scaling-cli-d-min-max`, kho lưu trữ `HerdSim`. |
| **Cam kết Mã (Commit)** | `Verified` | Commit gốc đối sánh: `3fc2267` (và các commit kế thừa). |
| **Môi trường & Phụ thuộc** | `Verified` | Trình quản lý `uv` với Python 3.12+; cấu hình xác định trong `pyproject.toml` và `uv.lock`. |
| **Dữ liệu Đầu vào / Bố cục** | `Verified` | Hàm sinh tất định trong `sim/core/world/layouts.py` (`compact`, `wide`, `split`, `outlier_rich`). |
| **Bộ Tạo Số Ngẫu nhiên** | `Verified` | Ghép cặp dòng ngẫu nhiên chung (Common Random Numbers): `master_seed + i` độc lập cho cừu và chó. |
| **Phần cứng Thực thi** | `Verified` | Hệ thống máy trạm Linux đa nhân; chạy song song trên 20 worker threads (`--workers 20`). |
| **Dữ liệu Thô (Raw Data)** | `Verified` | Đầy đủ 367.150 bản ghi tại `results/<protocol>/trials.jsonl` và tệp tổng kết `trials.csv`. |
| **Quy trình Thực thi (Command)**| `Verified` | Chuỗi lệnh duy nhất: `uv run cli/campaign.py run --protocol <id>` và `uv run cli/run_queue.py`. |
| **Mã Phân tích Bảng** | `Verified` | `cli/dmin_tables.py` xuất tự động toàn bộ số liệu sang [results_tables.md](results_tables.md). |
| **Kiểm thử Tự động (Tests)** | `Verified` | `make test` thực thi 28 bộ kiểm thử đơn vị, kiểm thử tầng phân cấp kiến trúc (`tests/test_layers.py`). |
| **Kiểm chứng Replay Bit-Identical**| `Verified` | `services/replay.py` kiểm định 932 lượt chạy lại; xác nhận trùng khớp trạng thái từng tích tắc 100%. |
