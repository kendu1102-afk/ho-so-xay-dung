# QUY TRÌNH XUẤT HỒ SƠ

## 1. Chuẩn bị bản thảo
- Bản thảo `BAN_THAO.md` đã qua thẩm tra – phản biện, không còn lỗi nghiêm trọng.
- Quy ước viết bản thảo để xuất Word đẹp:
  - `# ` tên hồ sơ (in hoa, căn giữa ở trang đầu)
  - `## `, `### `, `#### ` đề mục cấp 1, 2, 3
  - Gạch đầu dòng `- `; danh sách số `1. `
  - Bảng dạng `| cột | cột |`
  - `**chữ đậm**`, `*chữ nghiêng*`
  - Ngắt trang: dòng riêng `<!-- ngat-trang -->`
  - Phần chỉ dùng nội bộ (ghi chú, câu hỏi) đặt giữa `<!-- noi-bo -->` và `<!-- het-noi-bo -->` → không xuất ra Word.

## 2. Xuất
```
python xuat_docx.py <BAN_THAO.md> <file_ra.docx> --kho <kho> --cong-ty <MÃ>
```
- Định dạng lấy từ `01_KHO_PHONG_CACH_CONG_TY/<MÃ>/dinh_dang.json`; mục nào công ty ghi "chưa xác định" thì dùng `08_QUY_TAC_CHUNG/dinh_dang_mac_dinh.json`.
- Nếu `dinh_dang.json` có `"file_mau_word"` trỏ tới một file .docx mẫu của công ty, công cụ dùng file đó làm nền (giữ header, footer, logo, kiểu chữ).
- Không ghi đè: nếu file ra đã tồn tại, công cụ tự thêm `_v2`, `_v3`…

## 3. Kiểm tra sau xuất (công cụ tự in kết quả)
- Số đoạn, số bảng, số đề mục.
- Ký hiệu Markdown sót (`**`, `##`, `|---`).
- Chỗ **[CẦN BỔ SUNG]**, **[KIỂM TRA HIỆU LỰC]** còn trong file.
- Số trang (nếu máy có LibreOffice để đếm; không có thì báo "chưa đếm được").
Sau đó AI mở lại file Word đọc lướt toàn bộ để kiểm tra bằng mắt: tiêu đề, bảng không vỡ, đánh số liên tục.

## 4. Lưu
- File chính: `04_HO_SO_DA_XUAT/<CTY>/<CT>/<LOAI>_<MA_CT>_<ten-ngan>_v<N>.docx`.
- Bản thảo và báo cáo thẩm tra giữ ở `03_HO_SO_DANG_LAM/`.
- Không tự gửi, không tự trình ký.
- Khi người dùng xác nhận hồ sơ đã được duyệt/đạt: đề xuất chép một bản vào `01_.../<MÃ>/02_HO_SO_DA_HOAN_THIEN/` để làm mẫu cho lần sau.
