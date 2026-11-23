# QUY TẮC HỆ THỐNG

## 1. Bản đồ kho

| Thư mục | Chứa gì | Ai được sửa |
|---|---|---|
| `00_HE_THONG/` | Siêu lệnh, hướng dẫn, quy tắc hệ thống, nhật ký, phiên bản | Chỉ sửa khi người dùng chấp thuận; sao lưu vào `_PHIEN_BAN/` trước |
| `01_KHO_PHONG_CACH_CONG_TY/` | Mỗi công ty một thư mục `CONG_TY_NNN`; `danh_ba_cong_ty.json` là sổ đăng ký gốc, `DANH_SACH_CONG_TY.md` sinh tự động | Chỉ qua `kho.py` hoặc khi người dùng chấp thuận |
| `01_.../_MAU_CONG_TY/` | Khuôn để tạo công ty mới | Sửa khi muốn đổi khuôn chung |
| `02_TAI_LIEU_DAU_VAO/<CTY>/<CT>/` | Tài liệu gốc người dùng đưa vào | **Chỉ đọc**. Không sửa, không xóa, không đổi tên |
| `03_HO_SO_DANG_LAM/<CTY>/<CT>/` | Phân tích nội bộ, bản thảo, báo cáo thẩm tra | AI ghi tự do trong thư mục hồ sơ đang làm |
| `04_HO_SO_DA_XUAT/<CTY>/<CT>/` | File Word/PDF hoàn chỉnh | Chỉ thêm file mới, không ghi đè |
| `05_BAO_CAO_KIEM_TRA/` | Báo cáo tự kiểm tra hệ thống | Công cụ ghi |
| `06_BACKUP/` | File nén sao lưu | Chỉ thêm |
| `07_CONG_TY_MOI/` | "Hộp thư đến" — tài liệu của công ty chưa có mã | Người dùng thả file; AI chuyển sang kho sau khi được đồng ý |
| `08_QUY_TAC_CHUNG/` | Quy tắc dùng chung mọi công ty | Chỉ sửa khi người dùng chấp thuận |
| `09_NHAT_KY_HE_THONG/` | Nhật ký thao tác (tạo công ty, backup, khôi phục…) | Công cụ ghi |

## 2. Quy ước đặt tên

- Mã công ty: `CONG_TY_001`, `CONG_TY_002`… cấp tuần tự, không tái sử dụng mã.
- Mã công trình: `CONG_TRINH_001`… đánh riêng trong từng công ty.
- Thư mục hồ sơ đang làm: `YYYYMMDD_<LOAI>_<ten-ngan>` (ví dụ `20261123_BPTC_mat-duong-km12`).
- File xuất: `<LOAI>_<MA_CT>_<ten-ngan>_v<N>.docx`.
- Tên file, thư mục: không dấu, không khoảng trắng (tránh lỗi mã hóa khi chép qua Windows, USB, Zip, Git). Tên thật có dấu ghi trong file nội dung.

## 3. Loại hồ sơ (mã dùng trong tên file)

`BPTC`, `KH_KIEM_TRA_NGHIEM_THU`, `KH_THI_NGHIEM`, `KH_ATLD`, `KSC_LCL`, `THONG_BAO_HE_THONG_QLCL`, `KH_TO_CHUC_THI_CONG`, `HS_TRINH_DUYET`, `NGHIEM_THU`, `HOAN_CONG`, `BAO_CAO`, `TO_TRINH`, `THANH_TOAN`, `QUYET_TOAN`, `KHAC`. Chi tiết trong `08_QUY_TAC_CHUNG/DANH_MUC_LOAI_HO_SO.md`.

## 4. Công cụ

Nằm trong thư mục cài lệnh: `~/.claude/skills/ho-so-xay-dung/scripts/` (Windows: `C:\Users\<tên>\.claude\skills\ho-so-xay-dung\scripts\`).

| Công cụ | Việc |
|---|---|
| `kho.py tim-kho` | Tìm vị trí kho |
| `kho.py danh-sach` | Liệt kê công ty |
| `kho.py nhan-dien "<tên>"` | Nhận diện công ty theo tên |
| `kho.py tao-cong-ty "<tên>"` | Tạo kho công ty mới |
| `kho.py tao-cong-trinh <MÃ CTY> "<tên CT>"` | Tạo thư mục công trình |
| `kho.py thong-tin <MÃ CTY>` | Liệt kê tài liệu phong cách của công ty |
| `kho.py tao-ho-so <MÃ CTY> <MÃ CT> <LOAI> <ten-ngan>` | Tạo thư mục hồ sơ đang làm |
| `kho.py luu-phien-ban <file>` | Lưu bản cũ trước khi sửa |
| `kho.py backup [--toan-bo]` | Sao lưu |
| `kho.py khoi-phuc <file.zip>` | Giải nén bản sao lưu ra thư mục riêng |
| `kho.py kiem-tra` | Kiểm tra cấu trúc kho |
| `kho.py tu-kiem-tra` | Chạy bộ 12 bài kiểm tra trên bản sao tạm |
| `kiem_tra_ho_so.py <BAN_THAO.md> --loai <LOAI>` | Soát lỗi bản thảo |
| `xuat_docx.py <BAN_THAO.md> <ra.docx> --cong-ty <MÃ>` | Xuất Word theo định dạng công ty |

## 5. Vị trí kho được tìm theo thứ tự

1. Biến môi trường `HO_SO_KHO`.
2. File `kho_path.txt` trong thư mục cài lệnh (trình cài đặt ghi file này).
3. Thư mục `KHO_HO_SO_XAY_DUNG` trong thư mục làm việc hiện tại hoặc thư mục cha.
4. `D:\KHO_HO_SO_XAY_DUNG`.
5. `<thư mục người dùng>\KHO_HO_SO_XAY_DUNG`.
