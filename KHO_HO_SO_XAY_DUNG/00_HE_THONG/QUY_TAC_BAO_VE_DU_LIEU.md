# QUY TẮC BẢO VỆ DỮ LIỆU

Các quy tắc dưới đây là **bắt buộc**, không có ngoại lệ nếu người dùng chưa đồng ý rõ ràng trong phiên làm việc.

## 1. Dữ liệu gốc
- Không xóa, không ghi đè, không đổi tên, không di chuyển file trong `02_TAI_LIEU_DAU_VAO/` và các file người dùng đưa vào.
- Muốn sửa nội dung tài liệu gốc (ví dụ sửa dự toán sai): tạo **bản sao** trong `03_HO_SO_DANG_LAM/`, sửa bản sao, ghi rõ chỗ sửa và lý do.
- Tài liệu trong `07_CONG_TY_MOI/` chỉ được chép (không cắt) sang kho công ty sau khi người dùng xác nhận.

## 2. Không tạo dữ liệu giả
- Không tạo chữ ký, con dấu, chữ ký số giả.
- Không tạo kết quả thí nghiệm, số liệu quan trắc, nhật ký thi công, biên bản nghiệm thu với số liệu không có thật.
- Không bịa số hiệu văn bản, số chứng chỉ hành nghề, tên người, số điện thoại, số hợp đồng.
- Không trích dẫn tiêu chuẩn/văn bản pháp luật khi chưa xác định hiệu lực — đánh dấu **[KIỂM TRA HIỆU LỰC]**.

## 3. Không hành động ra bên ngoài
- Không tự gửi email, không tải hồ sơ lên mạng, không tự trình ký, không đẩy dữ liệu công ty lên kho GitHub công khai.
- Không chia sẻ dữ liệu công ty này cho phiên làm hồ sơ của công ty khác.

## 4. Cấu hình Claude Code
- Không sửa `settings.json`, các Skill/Command khác, file cấu hình của người dùng.
- Trình cài đặt chỉ tạo/thay thư mục `skills/ho-so-xay-dung` (có sao lưu bản cũ trước).

## 5. Sao lưu và phiên bản
- Trước khi sửa bất kỳ file nào trong `00_HE_THONG/`, `08_QUY_TAC_CHUNG/` hoặc kho phong cách công ty: chạy `kho.py luu-phien-ban <file>`.
- Trước thay đổi lớn (sửa nhiều file, đổi cấu trúc, khôi phục): chạy `kho.py backup`.
- Khôi phục không bao giờ ghi thẳng vào kho: giải nén ra `06_BACKUP/KHOI_PHUC_<thời gian>/`, người dùng xem rồi mới chép lại.
- File xuất không ghi đè: thêm hậu tố `_v2`, `_v3`.

## 6. Kho GitHub
Kho GitHub `ho-so-xay-dung` hiện để **công khai**. File `.gitignore` chặn dữ liệu công ty, công trình, bản sao lưu, nhật ký. Không gỡ các dòng chặn này khi kho còn công khai.
