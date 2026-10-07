# Phụ lục dữ liệu

Thư mục này là mục lục tái tạo được cho bằng chứng của Giai đoạn 1, 2 và 4. Các bảng được tạo trực tiếp từ CSV, JSON, tệp trạng thái và provenance chuẩn. Không có số nào được nhập tay.

## Cách đọc

* [Nhật ký chạy](run_ledger_vi.md): cấp thử nhanh, khảo sát, claim; số dòng; hash giao thức; liên kết provenance.
* [Bảng Giai đoạn 1](phase1_tables_vi.md): biên kích thước, chế độ, khớp scaling và tóm tắt hợp nhất.
* [Bảng Giai đoạn 2](phase2_tables_vi.md): biên theo bố cục, chi phí một chó, so sánh bộ dự đoán và tóm tắt hợp nhất.
* [Bảng Giai đoạn 4](phase4_tables_vi.md): chuyển giao Kubo và FAT, thất bại cứng, cửa sổ Kubo khó và tóm tắt hợp nhất.
* [Mục lục tiếng Anh](README.md).

## Quy ước bằng chứng

Khảo sát là bản đồ 30 seed dùng để chọn cửa sổ. Claim là bằng chứng chính xác, thường 100 seed, và là cấp dùng cho kết luận. Bản hợp nhất claim thay dòng khảo sát tại các ô đã gieo lại claim và giữ khảo sát tại các ô còn lại. Vì vậy mọi kết luận phải giữ rõ cấp của từng ô.

`D_max = 35` với `D_overcrowd` trống chỉ có nghĩa là thành công vẫn đạt ngưỡng tại đỉnh lưới đã thử. Nếu `hard_failure = True`, không D nào trong lưới đạt R = 0.90, nên không được điền một `D_max` giả.

## Tái tạo

Chạy `python3 build_tables.py` trong thư mục này. Chạy `python3 build_tables.py --check` để xác nhận các tệp đã tạo trùng khớp với nguồn hiện tại. Script chỉ ghi 10 tệp Markdown trong thư mục này.
