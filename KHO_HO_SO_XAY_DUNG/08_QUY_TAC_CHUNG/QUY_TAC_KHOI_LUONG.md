# QUY TẮC KHỐI LƯỢNG TRONG HỒ SƠ

## 1. Phân nhóm

### Nhóm A — Hồ sơ đầu vào / trình duyệt trước thi công: KHÔNG đưa khối lượng chi tiết
- Biện pháp thi công (BPTC), biện pháp tổ chức thi công
- Kế hoạch tổ chức thi công, tiến độ thi công (tiến độ thể hiện theo hạng mục/thời gian, không kèm cột khối lượng)
- Kế hoạch kiểm tra, nghiệm thu
- Kế hoạch thí nghiệm, kiểm định
- Kế hoạch / biện pháp an toàn lao động, vệ sinh môi trường, PCCN, đảm bảo giao thông
- Biện pháp kiểm soát chất lượng (KSC LCL)
- Thông báo hệ thống quản lý chất lượng
- Hồ sơ trình duyệt trước thi công

### Nhóm B — Hồ sơ cần số liệu: CÓ khối lượng, phải đối chiếu
- Hồ sơ thanh toán, quyết toán, phát sinh
- Báo cáo khối lượng, báo cáo tháng/quý có phần khối lượng hoàn thành
- Hồ sơ hoàn công, bản vẽ hoàn công
- Biên bản nghiệm thu có xác định khối lượng
- Bảng tính, thuyết minh tính toán, hồ sơ chuyên biệt có yêu cầu số liệu

## 2. Nhóm A — được làm / không được làm

| Được | Không được |
|---|---|
| Đọc bản vẽ, dự toán, BOQ, hợp đồng để hiểu công trình | Chép bảng dự toán/BOQ vào hồ sơ |
| Nêu quy mô tổng quát từ hồ sơ thiết kế: "tuyến dài khoảng 4,2 km", "cầu BTCT 3 nhịp dầm Super-T" | Liệt kê "đào nền 12.345 m³, đắp K95 8.900 m³…" |
| Nêu danh mục hạng mục, công việc, trình tự | Bảng tiến độ có cột khối lượng từng công việc |
| Nêu danh mục thiết bị, nhân lực chủ chốt dự kiến (nếu mẫu yêu cầu) | Tính số mẫu thí nghiệm cụ thể = khối lượng ÷ tần suất (chỉ nêu tần suất theo tiêu chuẩn/CDKT) |
| Lưu phân tích khối lượng trong `00_PHAN_TICH_NOI_BO/` để dùng nội bộ | Đưa phụ lục khối lượng vào file xuất |

## 3. Ngoại lệ
Chỉ đưa khối lượng vào hồ sơ nhóm A khi:
1. Người dùng yêu cầu rõ trong phiên làm việc, hoặc
2. Mẫu bắt buộc của CĐT/hợp đồng có mục khối lượng.
Khi đó ghi chú trong báo cáo thẩm tra: "Có khối lượng theo yêu cầu: <nguồn>".

## 4. Nhóm B — yêu cầu đối chiếu
- Khối lượng phải truy được về: bản vẽ thiết kế/hoàn công, biên bản đo đạc, nhật ký, biên bản nghiệm thu.
- Đối chiếu chéo: dự toán ↔ hợp đồng ↔ hoàn công ↔ thanh toán lũy kế. Chênh lệch phải liệt kê, nêu nguyên nhân.
- Đơn vị tính, cách làm tròn thống nhất với hợp đồng.
- Không "cân" số cho khớp. Nếu không khớp thì báo người dùng.
