# HƯỚNG DẪN SỬ DỤNG — HỆ THỐNG SIÊU LỆNH LÀM HỒ SƠ XÂY DỰNG

Hướng dẫn này viết cho người không cần biết lập trình. Mọi thao tác kỹ thuật, Claude sẽ tự làm; anh/chị chỉ cần gõ yêu cầu bằng tiếng Việt.

---

## 0. Hệ thống gồm 2 phần

| Phần | Là gì | Nằm ở đâu |
|---|---|---|
| **Lệnh `/ho-so-xay-dung`** | "Nút bấm" để gọi hệ thống trong Claude Code | Windows: `C:\Users\<tên>\.claude\skills\ho-so-xay-dung\` |
| **Kho hồ sơ** `KHO_HO_SO_XAY_DUNG` | Nơi chứa quy tắc, mẫu của từng công ty, tài liệu, hồ sơ | Ưu tiên `D:\KHO_HO_SO_XAY_DUNG` |

**Cài đặt trên máy Windows (làm 1 lần):**
1. Vào trang GitHub `kendu1102-afk/ho-so-xay-dung` → nút xanh **Code** → **Download ZIP** → giải nén (ví dụ ra Desktop).
2. Mở thư mục vừa giải nén → thư mục `CAI_DAT` → nháy đúp **`CAI_DAT_WINDOWS.bat`**.
3. Cửa sổ đen hiện lên, chờ đến dòng "CÀI ĐẶT XONG". Đọc dòng "Kho dữ liệu" để biết kho nằm ở đâu.
   - Nếu máy có ổ D: kho ở `D:\KHO_HO_SO_XAY_DUNG`.
   - Không có ổ D: kho ở `C:\Users\<tên>\Documents\KHO_HO_SO_XAY_DUNG`.
4. Cài thêm Python (nếu máy chưa có) tại python.org — khi cài nhớ tích ô **"Add Python to PATH"**. Python giúp hệ thống tự tạo kho công ty, kiểm tra hồ sơ, xuất Word.

Cách khác: mở Claude Code trong thư mục vừa giải nén và gõ: *"Chạy file CAI_DAT/CAI_DAT_WINDOWS.bat giúp tôi"*.

Trình cài đặt **không xóa, không ghi đè** kho cũ. Nếu kho đã có, nó chỉ bổ sung file còn thiếu.

---

## 1. Cách gọi lệnh

Mở Claude Code (ở bất kỳ thư mục nào), gõ:

```
/ho-so-xay-dung
```

Claude sẽ hiện khung nhập và danh sách công ty đang có. Anh/chị cũng có thể gõ luôn yêu cầu sau lệnh.

## 2–6. Cách nhập yêu cầu

```
/ho-so-xay-dung
TÊN CÔNG TY: Công ty CP Xây dựng Giao thông Minh Phát
TÊN CÔNG TRÌNH: Bảo dưỡng thường xuyên QL1 đoạn Km120–Km150 năm 2027
HẠNG MỤC: Toàn bộ
LOẠI HỒ SƠ: Biện pháp thi công
TÀI LIỆU: D:\Du an\BDTX QL1\
YÊU CẦU: Làm theo mẫu BPTC năm ngoái của công ty, có phần đảm bảo giao thông chi tiết
```

- **TÊN CÔNG TY**: gõ tên đầy đủ hoặc quen gọi. Có dấu hay không dấu, "Cty CP" hay "Công ty Cổ phần" đều được. Đây là "chìa khóa" để hệ thống mở đúng kho của công ty đó.
- **TÊN CÔNG TRÌNH**: tên ngắn gọn, dễ nhận ra. Lần sau gõ gần đúng là hệ thống tìm ra.
- **LOẠI HỒ SƠ**: BPTC, KH kiểm tra nghiệm thu, KH thí nghiệm, KH ATLĐ, KSC LCL, Thông báo hệ thống QLCL, Nghiệm thu, Hoàn công, Báo cáo, Tờ trình, Thanh toán, Quyết toán, Khác.
- **TÀI LIỆU**: đường dẫn thư mục chứa bản vẽ, dự toán, hợp đồng… Hoặc ghi "đã để trong kho".
- **YÊU CẦU**: điều đặc biệt muốn thêm/bớt.

Viết thành câu bình thường cũng được:
```
/ho-so-xay-dung Lập kế hoạch thí nghiệm cho công ty Minh Phát, công trình BDTX QL1 Km120-150, tài liệu đã để trong kho
```

**Công ty đã có trong kho**: hệ thống tự nhận ra, đọc mẫu và quy tắc riêng của công ty, báo lại cho anh/chị vài dòng rồi bắt đầu làm.
**Tên gần giống nhiều công ty**: hệ thống hỏi anh/chị chọn — không tự đoán.

## 5. Đưa tài liệu vào

Hai cách:
1. Ghi đường dẫn ở dòng TÀI LIỆU. Claude sẽ hỏi có muốn chép vào kho không (chỉ chép, không di chuyển file gốc).
2. Tự chép file vào kho theo thư mục:
```
D:\KHO_HO_SO_XAY_DUNG\02_TAI_LIEU_DAU_VAO\CONG_TY_001\CONG_TRINH_001\
    BAN_VE\       ← bản vẽ (PDF, ảnh)
    DU_TOAN\      ← dự toán, BOQ (Excel, PDF)
    HOP_DONG\     ← hợp đồng, phụ lục
    PHAP_LY\      ← quyết định, văn bản pháp lý, chỉ dẫn kỹ thuật
    HO_SO_MAU\    ← hồ sơ mẫu riêng của công trình
    TAI_LIEU_KHAC\
```
(Mã `CONG_TY_001`, `CONG_TRINH_001` xem trong file `01_KHO_PHONG_CACH_CONG_TY\DANH_SACH_CONG_TY.md`.)

## 7. Tạo công ty mới

```
/ho-so-xay-dung TẠO CÔNG TY: Công ty TNHH Cầu Đường Hưng Thịnh (viết tắt Hưng Thịnh)
```
Hệ thống cấp mã (ví dụ `CONG_TY_002`), tạo đủ thư mục và phiếu nhận diện, các mục chưa biết để "Chưa xác định".
Nếu có sẵn hồ sơ mẫu của công ty đó: chép vào `07_CONG_TY_MOI\<tên thư mục bất kỳ>\` rồi gõ:
```
/ho-so-xay-dung TẠO CÔNG TY: Công ty TNHH Cầu Đường Hưng Thịnh. TÀI LIỆU: 07_CONG_TY_MOI\hung-thinh
```
Claude sẽ phân tích mẫu (font, lề, bố cục, văn phong…), trình anh/chị xem, đồng ý mới lưu thành phong cách của công ty.

## 8. Lưu mẫu hồ sơ

Khi có một hồ sơ đạt yêu cầu muốn làm mẫu cho lần sau:
```
/ho-so-xay-dung LƯU MẪU: công ty Minh Phát, file D:\...\BPTC_da_duyet.docx, loại BPTC
```
File được **chép** vào `01_KHO_PHONG_CACH_CONG_TY\CONG_TY_001\01_MAU_BIEU\BPTC\`. Trùng tên thì tự thêm `_v2`, không đè mẫu cũ.

## 9. Cập nhật mẫu / quy tắc

Cuối mỗi bộ hồ sơ, Claude sẽ liệt kê các "quy tắc mới" phát hiện được và hỏi: *quy tắc chung của công ty hay chỉ riêng công trình này?* Chỉ khi anh/chị trả lời đồng ý, nó mới ghi vào kho; bản cũ được cất vào thư mục `06_PHIEN_BAN` của công ty.

Muốn chủ động dạy hệ thống:
```
/ho-so-xay-dung Công ty Minh Phát: từ nay mọi BPTC dùng font Times New Roman 14, đánh số mục kiểu I, 1, 1.1. Hãy cập nhật kho.
```

## 10. Sao lưu (backup)

```
/ho-so-xay-dung BACKUP
```
Tạo file nén trong `06_BACKUP\` (mặc định: hệ thống + kho phong cách công ty + nhật ký). Muốn sao lưu cả tài liệu và hồ sơ: gõ `BACKUP TOÀN BỘ`.
Khuyên dùng: mỗi tuần chép thư mục `06_BACKUP` sang USB/ổ cứng khác hoặc Google Drive.

## 11. Khôi phục

```
/ho-so-xay-dung KHÔI PHỤC
```
Claude liệt kê các bản sao lưu để anh/chị chọn. Bản sao lưu được **giải nén ra thư mục riêng** `06_BACKUP\KHOI_PHUC_<ngày giờ>\` — kho hiện tại không bị đụng tới. Anh/chị xem, rồi bảo Claude chép lại những file cần thiết (Claude sẽ sao lưu trạng thái hiện tại trước khi chép).

## 12. Kiểm tra hệ thống đã cài thành công

```
/ho-so-xay-dung KIỂM TRA HỆ THỐNG
```
Claude chạy 12 bài kiểm tra trên **bản sao tạm** (không đụng dữ liệu thật) và báo bảng ĐẠT / KHÔNG ĐẠT. Báo cáo lưu ở `05_BAO_CAO_KIEM_TRA\`.

Nếu gõ `/ho-so-xay-dung` mà Claude Code báo không có lệnh: đóng hẳn Claude Code, mở lại. Vẫn không có thì chạy lại `CAI_DAT_WINDOWS.bat`.

## 13. Xử lý khi Claude không tìm thấy kho

Thường do kho bị đổi chỗ hoặc đổi tên. Cách sửa (chọn một):
1. Gõ cho Claude: *"Kho hồ sơ của tôi nằm ở E:\KHO_HO_SO_XAY_DUNG, hãy ghi nhớ đường dẫn này cho lệnh /ho-so-xay-dung"*. Claude sẽ ghi đường dẫn vào file `kho_path.txt` trong thư mục lệnh.
2. Hoặc tự mở Notepad, gõ đúng một dòng đường dẫn kho, lưu thành `C:\Users\<tên>\.claude\skills\ho-so-xay-dung\kho_path.txt`.
3. Hoặc chạy lại trình cài đặt.

Thứ tự hệ thống tự tìm kho: đường dẫn trong `kho_path.txt` → thư mục đang mở trong Claude Code → `D:\KHO_HO_SO_XAY_DUNG` → `C:\Users\<tên>\KHO_HO_SO_XAY_DUNG` → `C:\Users\<tên>\Documents\KHO_HO_SO_XAY_DUNG`.

## 14. Gọi lệnh từ một dự án khác

Lệnh được cài "toàn máy" nên mở Claude Code ở thư mục nào cũng gọi được `/ho-so-xay-dung`. Kho dữ liệu luôn là một chỗ duy nhất (ví dụ `D:\KHO_HO_SO_XAY_DUNG`), không phụ thuộc thư mục đang mở. Ví dụ đang làm việc trong `D:\Du an\Cau Song Hinh\`, gõ:
```
/ho-so-xay-dung Công ty Hưng Thịnh, công trình Cầu Sông Hinh, lập KH ATLĐ, tài liệu ở thư mục hiện tại
```

---

## Những điều hệ thống KHÔNG BAO GIỜ làm
- Không xóa, sửa, di chuyển tài liệu gốc của anh/chị.
- Không ghi đè hồ sơ đã xuất (bản mới tự thêm `_v2`, `_v3`).
- Không trộn mẫu, thông tin giữa các công ty.
- Không bịa số liệu, kết quả thí nghiệm, chữ ký, số văn bản. Chỗ thiếu ghi **[CẦN BỔ SUNG: …]**.
- Không đưa bảng khối lượng chi tiết vào BPTC, kế hoạch nghiệm thu, kế hoạch thí nghiệm, ATLĐ, KSC LCL, thông báo HT QLCL… trừ khi anh/chị yêu cầu.
- Không tự gửi hồ sơ, không tự trình ký.

## Bản đồ kho (tóm tắt)
```
KHO_HO_SO_XAY_DUNG\
  00_HE_THONG\                 Siêu lệnh, hướng dẫn, quy tắc, nhật ký, phiên bản
  01_KHO_PHONG_CACH_CONG_TY\   Mỗi công ty 1 thư mục CONG_TY_xxx (mẫu, quy chuẩn, phiếu nhận diện)
  02_TAI_LIEU_DAU_VAO\         Tài liệu gốc theo công ty / công trình (chỉ đọc)
  03_HO_SO_DANG_LAM\           Bản thảo, phân tích nội bộ, báo cáo thẩm tra
  04_HO_SO_DA_XUAT\            File Word hoàn chỉnh
  05_BAO_CAO_KIEM_TRA\         Báo cáo tự kiểm tra hệ thống
  06_BACKUP\                   Bản sao lưu
  07_CONG_TY_MOI\              Chỗ thả mẫu của công ty chưa có mã
  08_QUY_TAC_CHUNG\            Quy tắc dùng chung (khối lượng, văn phong, thẩm tra, xuất file)
  09_NHAT_KY_HE_THONG\         Nhật ký thao tác
```
