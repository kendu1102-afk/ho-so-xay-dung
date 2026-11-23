# QUY TRÌNH THẨM TRA – PHẢN BIỆN – SỬA LỖI

Kết quả ghi vào `BAO_CAO_THAM_TRA.md` trong thư mục hồ sơ đang làm, theo mẫu ở mục 4.

## 1. Thẩm tra (6 mặt)

| Mặt | Câu hỏi kiểm tra |
|---|---|
| **Pháp lý** | Căn cứ có đúng hợp đồng, quyết định duyệt, hồ sơ thiết kế của công trình? Văn bản pháp luật/tiêu chuẩn có đúng số hiệu, còn hiệu lực? (chưa chắc → **[KIỂM TRA HIỆU LỰC]**) Tên CĐT, TVGS, nhà thầu, số hợp đồng có khớp tài liệu? |
| **Kỹ thuật** | Trình tự thi công đúng kết cấu trong bản vẽ? Vật liệu, chỉ tiêu, dung sai đúng CDKT? Có hạng mục nào trong bản vẽ bị bỏ sót, hay có nội dung không thuộc công trình? |
| **Chất lượng** | Mỗi công việc có: tiêu chí kiểm tra, người kiểm tra, thời điểm, hồ sơ ghi nhận? Điểm dừng nghiệm thu có rõ? Xử lý khi không đạt? |
| **Thực tế** | Làm được ngoài hiện trường không? Phù hợp điều kiện: đường đang khai thác, mùa mưa, mặt bằng, nguồn vật liệu, thiết bị nhà thầu có? Tiến độ có hợp lý? |
| **Thống nhất** | Tên gọi, viết tắt, số liệu, đánh số mục, dẫn chiếu chéo giữa các phần có khớp? Giữa hồ sơ này với các hồ sơ đã trình trước (BPTC ↔ KH nghiệm thu ↔ KH thí nghiệm) có mâu thuẫn? |
| **Trình bày & văn phong** | Đúng mẫu/quy chuẩn công ty? Không sáo rỗng, không lặp, không quảng cáo? Quy tắc khối lượng có được tuân thủ? Còn **[CẦN BỔ SUNG]** nào? |

Chạy công cụ:
```
python kiem_tra_ho_so.py <BAN_THAO.md> --loai <LOAI> --kho <đường dẫn kho> --cong-ty <MÃ>
```
Công cụ chỉ hỗ trợ; kết luận cuối cùng do thẩm tra bằng đọc hiểu.

## 2. Phản biện độc lập
Đổi vai: "Tôi là TVGS/kiểm toán viên, nhận bộ hồ sơ này lần đầu, tìm mọi lý do để trả lại."
- Đọc từ đầu đến cuối, không dựa vào giả định của người soạn.
- Hỏi từng mục: "Căn cứ đâu?", "Ai chịu trách nhiệm?", "Kiểm tra bằng cách nào?", "Nếu sai thì sao?"
- Đặc biệt soi: số liệu không nguồn, nội dung chung chung có thể dán vào bất kỳ công trình nào, mâu thuẫn với tài liệu đầu vào.

## 3. Sửa và kiểm tra lại
1. Sửa lỗi Nghiêm trọng → Trung bình → Nhẹ.
2. Lỗi do thiếu dữ liệu → chuyển thành **[CẦN BỔ SUNG]** + câu hỏi cho người dùng.
3. Chạy lại mục 1. Tối đa 3 vòng. Còn lỗi nghiêm trọng thì không gọi là hoàn chỉnh.

## 4. Mẫu báo cáo thẩm tra

```
# BÁO CÁO THẨM TRA — <tên hồ sơ>
Công ty: <MÃ> — Công trình: <MÃ> — Ngày: <…>
Nguồn mẫu/phong cách: <…>

## Vòng 1
| # | Vị trí | Mặt | Lỗi | Căn cứ | Mức độ | Cách sửa | Trạng thái |
|---|---|---|---|---|---|---|---|

## Vòng 2 …

## Kết quả công cụ kiem_tra_ho_so.py
<dán tóm tắt>

## Kết luận
- Lỗi đã sửa: …
- Lỗi còn lại / cần người dùng quyết định: …
- Thông tin cần bổ sung: …
```
