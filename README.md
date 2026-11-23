# HỆ THỐNG SIÊU LỆNH LÀM HỒ SƠ XÂY DỰNG

Lệnh `/ho-so-xay-dung` cho Claude Code: lập – thẩm tra – phản biện – xuất Word hồ sơ cầu đường và bảo dưỡng thường xuyên đường bộ, theo **kho phong cách riêng của từng công ty**.

## Cài đặt trên Windows
1. Nút **Code → Download ZIP**, giải nén.
2. Vào thư mục `CAI_DAT`, nháy đúp `CAI_DAT_WINDOWS.bat`.
3. Mở lại Claude Code, gõ `/ho-so-xay-dung`.

Kho dữ liệu mặc định: `D:\KHO_HO_SO_XAY_DUNG` (không có ổ D thì vào `Documents`).
Linux/Mac/WSL: `bash CAI_DAT/cai_dat.sh`.

## Hướng dẫn đầy đủ
[`KHO_HO_SO_XAY_DUNG/00_HE_THONG/HUONG_DAN_SU_DUNG.md`](KHO_HO_SO_XAY_DUNG/00_HE_THONG/HUONG_DAN_SU_DUNG.md)

## Cấu trúc
| Thư mục | Nội dung |
|---|---|
| `.claude/skills/ho-so-xay-dung/` | Lệnh `/ho-so-xay-dung` (SKILL.md) và công cụ `scripts/` (kho.py, kiem_tra_ho_so.py, xuat_docx.py) |
| `KHO_HO_SO_XAY_DUNG/` | Khuôn kho dữ liệu: siêu lệnh, quy tắc chung, khuôn công ty/công trình |
| `CAI_DAT/` | Trình cài đặt |

> Kho GitHub này công khai: `.gitignore` chặn mọi dữ liệu công ty/công trình. Dữ liệu thật chỉ nằm trên máy của bạn.
