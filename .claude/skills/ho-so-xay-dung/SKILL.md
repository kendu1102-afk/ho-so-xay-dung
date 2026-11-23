---
name: ho-so-xay-dung
description: Hệ thống siêu lệnh làm hồ sơ xây dựng cầu đường và bảo dưỡng thường xuyên đường bộ (BPTC, kế hoạch nghiệm thu, thí nghiệm, ATLĐ, KSC LCL, thông báo hệ thống QLCL, nghiệm thu, hoàn công, báo cáo, tờ trình, thanh quyết toán) theo kho phong cách riêng của từng công ty trong KHO_HO_SO_XAY_DUNG. Dùng khi người dùng gọi /ho-so-xay-dung hoặc yêu cầu lập, thẩm tra, xuất hồ sơ xây dựng cho một công ty/công trình, tạo công ty mới trong kho, cập nhật mẫu, sao lưu hoặc khôi phục kho hồ sơ.
argument-hint: "TÊN CÔNG TY: … | TÊN CÔNG TRÌNH: … | LOẠI HỒ SƠ: … (bỏ trống để xem hướng dẫn nhập)"
---

# /ho-so-xay-dung — HỆ THỐNG SIÊU LỆNH LÀM HỒ SƠ XÂY DỰNG

Giao tiếp với người dùng **bằng tiếng Việt đơn giản**. Người dùng là kỹ sư quản lý dự án, không phải lập trình viên: không bắt họ gõ lệnh, tự chạy công cụ và chỉ báo kết quả.

Nội dung người dùng nhập kèm lệnh:

```
$ARGUMENTS
```

## BƯỚC 0 — Nạp hệ thống (bắt buộc mỗi lần)

1. Công cụ nằm ở `${CLAUDE_SKILL_DIR}/scripts/` (nếu biến này không được thay thế, dùng thư mục chứa file SKILL.md này: thường là `~/.claude/skills/ho-so-xay-dung/` hoặc `.claude/skills/ho-so-xay-dung/` trong dự án).
   Gọi Python theo thứ tự thử: `python`, `python3`, `py -3`. Ký hiệu dưới đây: `KHO_PY` = `python "${CLAUDE_SKILL_DIR}/scripts/kho.py"`.
2. Chạy `KHO_PY tim-kho` → lấy dòng `KHO=<đường dẫn>`. Gọi đường dẫn đó là `<KHO>`.
   - Nếu báo không tìm thấy: đọc mục "Xử lý khi không tìm thấy kho" trong file HUONG_DAN_SU_DUNG.md nằm cùng repo/bộ cài; hỏi người dùng kho đang ở đâu, rồi ghi đường dẫn vào `${CLAUDE_SKILL_DIR}/kho_path.txt` (sau khi người dùng đồng ý). Không tự tạo kho mới ở chỗ khác khi chưa hỏi.
   - Nếu không có Python: báo người dùng, đề nghị cài Python (python.org) — trong lúc chờ vẫn có thể làm thủ công bằng công cụ đọc/ghi file, theo đúng quy tắc trong kho.
3. Đọc đầy đủ: `<KHO>/00_HE_THONG/SIEU_LENH_CHINH.md` và `<KHO>/00_HE_THONG/QUY_TAC_BAO_VE_DU_LIEU.md`. Hai file này là luật cao nhất của hệ thống (sau pháp luật/hợp đồng). Các quy tắc chung đọc khi cần theo hướng dẫn bên dưới: `<KHO>/08_QUY_TAC_CHUNG/`.

## BƯỚC 1 — Đọc yêu cầu

**Nếu phần "Nội dung người dùng nhập kèm lệnh" ở trên trống**: chỉ hiển thị khung dưới đây rồi dừng, chờ người dùng nhập.

```
HỆ THỐNG LÀM HỒ SƠ XÂY DỰNG — sẵn sàng. Kho: <KHO>
Công ty đang có: <kết quả KHO_PY danh-sach, tối đa 10 dòng>

Anh/chị nhập theo mẫu (dòng nào chưa có thì bỏ trống):
TÊN CÔNG TY: ...
TÊN CÔNG TRÌNH: ...
HẠNG MỤC: ...
LOẠI HỒ SƠ: ... (BPTC, KH kiểm tra nghiệm thu, KH thí nghiệm, KH ATLĐ, KSC LCL, Thông báo HT QLCL, Nghiệm thu, Hoàn công, Báo cáo, Tờ trình, Thanh toán, Quyết toán, Khác)
TÀI LIỆU: ... (đường dẫn thư mục/file, hoặc "đã để trong kho")
YÊU CẦU: ...

Lệnh nhanh: DANH SÁCH CÔNG TY | TẠO CÔNG TY: <tên> | LƯU MẪU | BACKUP | KHÔI PHỤC | KIỂM TRA HỆ THỐNG | HƯỚNG DẪN
```

**Nếu có nội dung**: tách các trường trên (chấp nhận viết tắt, không dấu, thứ tự bất kỳ, viết thành câu tự nhiên). Trường bắt buộc để lập hồ sơ: TÊN CÔNG TY, LOẠI HỒ SƠ. Thiếu thì hỏi đúng trường thiếu — không hỏi lại những gì đã có.

**Lệnh nhanh**:
| Người dùng gõ | Làm |
|---|---|
| DANH SÁCH CÔNG TY | `KHO_PY danh-sach` |
| TẠO CÔNG TY: <tên> | Bước 2 nhánh "chưa có" |
| LƯU MẪU | Mục "Lưu mẫu" ở Bước 8 |
| BACKUP | `KHO_PY backup` (hỏi có cần `--toan-bo` không nếu kho có nhiều tài liệu) |
| KHÔI PHỤC | Liệt kê file trong `<KHO>/06_BACKUP/`, hỏi chọn file, `KHO_PY khoi-phuc <file>`, giải thích kết quả; chỉ chép đè về kho khi người dùng đồng ý từng phần và đã chạy backup trước |
| KIỂM TRA HỆ THỐNG | `KHO_PY kiem-tra` rồi `KHO_PY tu-kiem-tra`; báo bảng kết quả |
| HƯỚNG DẪN | Tóm tắt `<KHO>/00_HE_THONG/HUONG_DAN_SU_DUNG.md` |

## BƯỚC 2 — Nhận diện công ty (TÊN CÔNG TY là khóa)

`KHO_PY nhan-dien "<TÊN CÔNG TY>"`
- `KET_QUA=KHOP MA=...` → dùng mã đó. Báo: "Đã nhận diện: <mã> — <tên>".
- `KET_QUA=GAN_GIONG` → hỏi người dùng chọn công ty nào trong danh sách hay tạo mới. **Không tự chọn.**
- `KET_QUA=CHUA_CO` → hỏi xác nhận tạo mới (kèm tên viết tắt nếu có) → `KHO_PY tao-cong-ty "<tên>" --ten-khac <viết tắt>` (thêm `--xac-nhan-moi` chỉ khi người dùng đã xác nhận đây là công ty khác với các tên gần giống).
  Sau khi tạo: nếu người dùng có hồ sơ mẫu (hoặc có thư mục trong `<KHO>/07_CONG_TY_MOI/`), hỏi đồng ý rồi **chép** vào `01_KHO_PHONG_CACH_CONG_TY/<MÃ>/01_MAU_BIEU/<LOẠI>/` và phân tích phong cách (Bước 8 — "Xây dựng phong cách ban đầu").

**Từ đây trở đi chỉ được đọc/ghi trong thư mục của đúng mã công ty này** (và thư mục chung 00, 08). Không mở kho công ty khác.

## BƯỚC 3 — Nạp phong cách công ty

1. `KHO_PY thong-tin <MÃ>` để có danh sách file.
2. Đọc theo thứ tự ở mục 2 của Siêu lệnh: THONG_TIN_CONG_TY → PHIEU_NHAN_DIEN → QUY_CHUAN_PHONG_CACH → QUY_CHUAN_TRINH_BAY → QUY_CHUAN_VAN_PHONG → QUY_TAC_KY_THUAT → 03_QUY_TAC_DA_CHAP_THUAN → 04_KINH_NGHIEM_VA_LOI_CAN_TRANH → mẫu trong `01_MAU_BIEU/<LOẠI>/` → hồ sơ cùng loại trong `02_HO_SO_DA_HOAN_THIEN/`.
   File Word/PDF/Excel: đọc nội dung bằng công cụ phù hợp (PDF đọc trực tiếp; .docx dùng python-docx hoặc pandoc; .xlsx dùng openpyxl).
3. Báo người dùng 3–6 dòng: mẫu sẽ dùng, định dạng, quy tắc đặc biệt, những điểm còn "chưa xác định".

## BƯỚC 4 — Công trình và tài liệu

1. `KHO_PY tim-cong-trinh <MÃ> "<TÊN CÔNG TRÌNH>"` → KHOP thì dùng; GAN_GIONG thì hỏi; CHUA_CO thì hỏi rồi `KHO_PY tao-cong-trinh <MÃ> "<tên>"`.
2. Tài liệu: nếu người dùng chỉ đường dẫn ngoài kho, hỏi có muốn **chép** vào `<KHO>/02_TAI_LIEU_DAU_VAO/<MÃ>/<MÃ_CT>/<nhóm>/` không (BAN_VE, DU_TOAN, HOP_DONG, PHAP_LY, HO_SO_MAU, TAI_LIEU_KHAC). Không cắt/di chuyển file gốc.
3. `KHO_PY tao-ho-so <MÃ> <MÃ_CT> <LOAI> <ten-ngan>` → lấy `THU_MUC_HO_SO` và `THU_MUC_XUAT`.
4. Nghiên cứu toàn bộ tài liệu theo mục 5 Siêu lệnh; ghi `03_HO_SO_DANG_LAM/<MÃ>/<MÃ_CT>/00_PHAN_TICH_NOI_BO/PHIEU_PHAN_TICH_TAI_LIEU.md`. Cập nhật `THONG_TIN_CONG_TRINH.md` (chỉ thông tin có nguồn).
5. Có mâu thuẫn tài liệu ảnh hưởng nội dung → báo và hỏi trước khi soạn phần đó.

## BƯỚC 5 — Lập hồ sơ

- Đọc `<KHO>/08_QUY_TAC_CHUNG/DANH_MUC_LOAI_HO_SO.md`, `QUY_TAC_KHOI_LUONG.md`, `QUY_TAC_VAN_PHONG_CHUNG.md`.
- Soạn **toàn văn** vào `<THU_MUC_HO_SO>/BAN_THAO.md` theo quy ước Markdown trong `QUY_TRINH_XUAT_HO_SO.md` (ghi nguồn mẫu trong khối `<!-- noi-bo -->` đầu file).
- **Quy tắc khối lượng**: hồ sơ nhóm A (BPTC, KH nghiệm thu, KH thí nghiệm, KH ATLĐ, KSC LCL, Thông báo HT QLCL, KH tổ chức thi công, hồ sơ trình duyệt trước thi công) **không đưa khối lượng chi tiết** trừ khi người dùng yêu cầu rõ. Phân tích khối lượng chỉ để ở `00_PHAN_TICH_NOI_BO`.
- Thiếu dữ liệu → `[CẦN BỔ SUNG: …]`; văn bản chưa chắc hiệu lực → `[KIỂM TRA HIỆU LỰC]`. Tuyệt đối không bịa.
- Hồ sơ dài: soạn từng phần, lưu file thường xuyên.

## BƯỚC 6 — Thẩm tra, phản biện, sửa lỗi

Theo `<KHO>/08_QUY_TAC_CHUNG/QUY_TRINH_THAM_TRA_PHAN_BIEN.md`:
1. Thẩm tra 6 mặt (pháp lý – kỹ thuật – chất lượng – thực tế – thống nhất – trình bày/văn phong).
2. Chạy `python "${CLAUDE_SKILL_DIR}/scripts/kiem_tra_ho_so.py" "<THU_MUC_HO_SO>/BAN_THAO.md" --loai <LOAI> --kho "<KHO>" --cong-ty <MÃ>`.
3. Phản biện độc lập (đóng vai TVGS/kiểm toán khó tính). Có thể giao cho một agent phụ đọc bản thảo độc lập nếu hồ sơ dài.
4. Sửa → kiểm tra lại, tối đa 3 vòng. Ghi `<THU_MUC_HO_SO>/BAO_CAO_THAM_TRA.md`.
5. Còn lỗi nghiêm trọng → dừng, báo người dùng, không xuất như hồ sơ hoàn chỉnh.

## BƯỚC 7 — Xuất file

`python "${CLAUDE_SKILL_DIR}/scripts/xuat_docx.py" "<THU_MUC_HO_SO>/BAN_THAO.md" "<THU_MUC_XUAT>/<LOAI>_<MÃ_CT>_<ten-ngan>_v1.docx" --kho "<KHO>" --cong-ty <MÃ>`
- Thiếu python-docx: hỏi người dùng cho phép chạy `python -m pip install python-docx`.
- Đọc kết quả kiểm tra sau xuất (số trang, bảng, ký hiệu sót, chỗ chưa hoàn thiện); mở lại file Word đọc soát. Sửa và xuất lại nếu cần (công cụ tự tạo `_v2`, không ghi đè).
- Không gửi đi, không trình ký, không tạo chữ ký/con dấu.

## BƯỚC 8 — Cập nhật kho phong cách (chỉ khi người dùng chấp thuận)

Đề xuất danh sách: quy tắc mới, chỉnh sửa người dùng đã yêu cầu trong phiên, mẫu nên thành mẫu chuẩn, lỗi cần ghi nhớ. Với mỗi mục hỏi: **"Quy tắc chung của công ty hay chỉ riêng công trình này?"**
Khi được đồng ý:
1. `KHO_PY luu-phien-ban <file sẽ sửa>` (bắt buộc trước khi sửa bất kỳ file quy chuẩn nào).
2. Sửa file liên quan (QUY_CHUAN_*, `dinh_dang.json`, `tu_cam.json`, `03_QUY_TAC_DA_CHAP_THUAN/DANH_SACH_QUY_TAC.md`, `04_.../KINH_NGHIEM.md`).
3. Tăng "Phiên bản hiện tại" trong `05_PHIEU_NHAN_DIEN_HO_SO/PHIEU_NHAN_DIEN.md`.
4. Thêm dòng vào `<KHO>/00_HE_THONG/NHAT_KY_CAP_NHAT.md`.

**Lưu mẫu**: chép file người dùng chỉ định vào `01_MAU_BIEU/<LOẠI>/` (hoặc `02_HO_SO_DA_HOAN_THIEN/`), không ghi đè — trùng tên thì thêm `_v2`. Cập nhật bảng "Mẫu đang dùng" trong QUY_CHUAN_PHONG_CACH.md.

**Xây dựng phong cách ban đầu** (công ty mới có mẫu): đọc các mẫu, rút ra font, cỡ chữ, lề, bố cục, cách đánh số, bảng, header/footer, trang bìa, khối ký tên, văn phong, thuật ngữ → trình bày cho người dùng xem → được đồng ý mới ghi vào PHIEU_NHAN_DIEN, QUY_CHUAN_* và `dinh_dang.json` (có thể đặt `"file_mau_word": "01_MAU_BIEU/<LOẠI>/<file>.docx"` để xuất Word giữ nguyên header/logo). Thông tin không thấy trong mẫu → để "Chưa xác định".

## BƯỚC 9 — Báo cáo cuối phiên (ngắn gọn)

File đã xuất (đường dẫn, số trang) · mẫu/phong cách đã dùng · lỗi đã sửa / còn lại · danh sách [CẦN BỔ SUNG] · mâu thuẫn tài liệu · đề xuất cập nhật kho đang chờ chấp thuận.

## Luật bất di bất dịch
- Không trộn dữ liệu giữa các công ty.
- Không xóa/ghi đè/di chuyển tài liệu gốc; không ghi đè hồ sơ đã xuất, mẫu chuẩn cũ.
- Không bịa thông tin, chữ ký, kết quả thí nghiệm, số hiệu văn bản.
- Không gửi dữ liệu ra ngoài; không đẩy dữ liệu công ty lên kho GitHub công khai.
- Không sửa cấu hình Claude Code hay Skill/Command khác.
- Không báo "hoàn thành" khi chưa kiểm tra.
