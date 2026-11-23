#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kiem_tra_ho_so.py — Soát lỗi máy móc cho bản thảo hồ sơ (Markdown).
Không thay thế thẩm tra bằng đọc hiểu; chỉ bắt các lỗi dễ sót.

python kiem_tra_ho_so.py BAN_THAO.md --loai BPTC [--kho <kho>] [--cong-ty CONG_TY_001]
Mã thoát: 0 = không có lỗi nặng; 1 = có lỗi nặng (ví dụ khối lượng trong hồ sơ đầu vào).
"""
import argparse
import difflib
import json
import re
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kho as K  # noqa: E402

NHOM_A = {"BPTC", "KH_KIEM_TRA_NGHIEM_THU", "KH_THI_NGHIEM", "KH_ATLD", "KSC_LCL",
          "THONG_BAO_HE_THONG_QLCL", "KH_TO_CHUC_THI_CONG", "HS_TRINH_DUYET"}

DON_VI = r"(m3|m³|m2|m²|md|m\.dài|tấn|tan|kg|lít|lit|cái|cọc|bộ|ca máy|công|100m3|100m2|1000m3|km2)"
RE_SO_DV = re.compile(r"(?<![\d.,])\d(?:[\d.,]*\d)?\s*" + DON_VI + r"(?![a-zA-ZÀ-ỹ0-9])", re.I)
RE_CHO_TRONG = re.compile(r"(XXX+|xxx+|\{\{.*?\}\}|TODO|\[\s*\.\.\.\s*\]|…{2,}|\.{4,}|_{5,})")
RE_BO_SUNG = re.compile(r"\[(CẦN BỔ SUNG|KIỂM TRA HIỆU LỰC)[^\]]*\]")


def bo_noi_bo(t: str) -> str:
    return re.sub(r"<!--\s*noi-bo\s*-->.*?<!--\s*het-noi-bo\s*-->", "", t, flags=re.S | re.I)


def tai_tu_cam(kho, ma_cty):
    ds = []
    if kho:
        for f in [kho / K.D_QT / "tu_cam.json"] + ([kho / K.D_PC / ma_cty / "tu_cam.json"] if ma_cty else []):
            d = K.doc_json(f, {"cum_tu": []}) or {"cum_tu": []}
            ds += d.get("cum_tu", [])
    return ds


def main():
    p = argparse.ArgumentParser()
    p.add_argument("file")
    p.add_argument("--loai", required=True)
    p.add_argument("--kho")
    p.add_argument("--cong-ty")
    a = p.parse_args()

    try:
        kho = K.tim_kho(a.kho)
    except SystemExit:
        kho = None
        print("Cảnh báo: không tìm thấy kho — chỉ soát các lỗi cơ bản, không có danh sách từ cấm.")

    goc = Path(a.file).read_text(encoding="utf-8")
    t = bo_noi_bo(goc)
    dong = t.splitlines()
    loai = a.loai.upper()
    nang, nhe, tin = [], [], []

    # 1. Khối lượng trong hồ sơ nhóm A
    if loai in NHOM_A:
        for i, d in enumerate(dong, 1):
            if d.lstrip().startswith("#"):
                continue
            la_bang = d.strip().startswith("|")
            if la_bang and re.search(r"khối\s*lượng|k\.?\s*lượng", d, re.I):
                nang.append(("KHOI_LUONG", i, "Bảng có cột 'Khối lượng' trong hồ sơ đầu vào", d.strip()[:120]))
            elif RE_SO_DV.search(d) and (la_bang or re.search(r"khối\s*lượng", d, re.I)):
                nang.append(("KHOI_LUONG", i, "Số lượng kèm đơn vị khối lượng", d.strip()[:120]))
            elif RE_SO_DV.search(d):
                nhe.append(("KHOI_LUONG_NGHI_VAN", i, "Có số kèm đơn vị — kiểm tra có phải khối lượng chi tiết không", d.strip()[:120]))

    # 2. Từ cấm / sáo rỗng
    thap = t.lower()
    for c in tai_tu_cam(kho, a.cong_ty):
        cum = c["cum"].lower()
        if cum in thap:
            for i, d in enumerate(dong, 1):
                if cum in d.lower():
                    nhe.append(("TU_CAM", i, f"'{c['cum']}' ({c.get('ly_do', '')}) → {c.get('thay_bang', '')}", d.strip()[:120]))

    # 3. Chỗ trống, chữ giữ chỗ
    for i, d in enumerate(dong, 1):
        if RE_CHO_TRONG.search(d):
            nhe.append(("CHO_TRONG", i, "Chữ giữ chỗ / chỗ trống", d.strip()[:120]))
        for m in RE_BO_SUNG.finditer(d):
            tin.append(("CAN_BO_SUNG", i, m.group(0), ""))

    # 4. Lặp đoạn
    doan = [(i, re.sub(r"\s+", " ", x).strip()) for i, x in enumerate(re.split(r"\n\s*\n", t))]
    doan = [(i, x) for i, x in doan if len(x) >= 80 and not x.startswith("|")]
    for j in range(len(doan)):
        for k in range(j + 1, len(doan)):
            r = difflib.SequenceMatcher(None, doan[j][1], doan[k][1]).quick_ratio()
            if r > 0.9 and difflib.SequenceMatcher(None, doan[j][1], doan[k][1]).ratio() > 0.9:
                nhe.append(("LAP_DOAN", 0, f"Hai đoạn gần như trùng nhau (đoạn {doan[j][0]+1} và {doan[k][0]+1})", doan[k][1][:100]))

    # 5. Câu quá dài
    for i, d in enumerate(dong, 1):
        if d.strip().startswith("|"):
            continue
        for cau in re.split(r"(?<=[.;:!?])\s+", d):
            if len(cau.split()) > 70:
                nhe.append(("CAU_DAI", i, f"Câu dài {len(cau.split())} từ — nên tách", cau[:100]))

    # 6. Ký hiệu đề mục đánh số nhảy cóc (## 1., ## 2. …)
    for cap in ("## ", "### "):
        so_truoc = None
        for i, d in enumerate(dong, 1):
            if d.startswith(cap):
                m = re.match(re.escape(cap) + r"(\d+)(?:\.(\d+))?", d)
                if m:
                    so = int(m.group(2) or m.group(1))
                    if so_truoc is not None and so not in (so_truoc + 1, 1):
                        nhe.append(("DANH_SO", i, f"Đánh số mục nhảy từ {so_truoc} sang {so}", d.strip()))
                    so_truoc = so
            elif cap == "### " and d.startswith("## "):
                so_truoc = None

    print(f"KIỂM TRA: {a.file}  | loại: {loai} ({'nhóm A — hồ sơ đầu vào' if loai in NHOM_A else 'nhóm B / khác'})")
    for ten, ds in (("LỖI NẶNG", nang), ("CẦN XEM LẠI", nhe), ("THÔNG TIN", tin)):
        print(f"\n== {ten}: {len(ds)}")
        for ma, i, mo_ta, trich in ds:
            vt = f"dòng {i}" if i else ""
            print(f"  [{ma}] {vt}: {mo_ta}" + (f"\n      » {trich}" if trich else ""))
    print(f"\nTÓM TẮT: nặng={len(nang)} | xem lại={len(nhe)} | chờ bổ sung={len(tin)}")
    sys.exit(1 if nang else 0)


if __name__ == "__main__":
    main()
