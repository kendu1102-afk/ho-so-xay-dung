#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kho.py — Công cụ quản lý KHO_HO_SO_XAY_DUNG.
Chỉ dùng thư viện chuẩn Python 3.8+. Chạy: python kho.py <lệnh> [tham số]
Gõ: python kho.py --help  để xem danh sách lệnh.
"""
import argparse
import datetime as _dt
import difflib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import zipfile
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

TEN_KHO = "KHO_HO_SO_XAY_DUNG"
SKILL_DIR = Path(__file__).resolve().parent.parent

D_HT = "00_HE_THONG"
D_PC = "01_KHO_PHONG_CACH_CONG_TY"
D_DV = "02_TAI_LIEU_DAU_VAO"
D_DL = "03_HO_SO_DANG_LAM"
D_DX = "04_HO_SO_DA_XUAT"
D_KT = "05_BAO_CAO_KIEM_TRA"
D_BK = "06_BACKUP"
D_MOI = "07_CONG_TY_MOI"
D_QT = "08_QUY_TAC_CHUNG"
D_NK = "09_NHAT_KY_HE_THONG"
MAU_CTY = "_MAU_CONG_TY"
MAU_CT = "_MAU_CONG_TRINH"
DANH_BA = "danh_ba_cong_ty.json"
DANH_BA_CT = "danh_ba_cong_trinh.json"

FILE_BAT_BUOC = [
    f"{D_HT}/SIEU_LENH_CHINH.md", f"{D_HT}/HUONG_DAN_SU_DUNG.md", f"{D_HT}/QUY_TAC_HE_THONG.md",
    f"{D_HT}/QUY_TAC_BAO_VE_DU_LIEU.md", f"{D_HT}/NHAT_KY_CAP_NHAT.md", f"{D_HT}/PHIEN_BAN_HE_THONG.md",
    f"{D_QT}/QUY_TAC_KHOI_LUONG.md", f"{D_QT}/QUY_TAC_VAN_PHONG_CHUNG.md",
    f"{D_QT}/QUY_TRINH_THAM_TRA_PHAN_BIEN.md", f"{D_QT}/QUY_TRINH_XUAT_HO_SO.md",
    f"{D_QT}/DANH_MUC_LOAI_HO_SO.md", f"{D_QT}/tu_cam.json", f"{D_QT}/dinh_dang_mac_dinh.json",
]
FILE_CTY = [
    "THONG_TIN_CONG_TY.md", "QUY_CHUAN_PHONG_CACH.md", "QUY_CHUAN_TRINH_BAY.md",
    "QUY_CHUAN_VAN_PHONG.md", "QUY_TAC_KY_THUAT.md", "dinh_dang.json",
    "05_PHIEU_NHAN_DIEN_HO_SO/PHIEU_NHAN_DIEN.md",
]
THU_MUC_CTY = ["01_MAU_BIEU", "02_HO_SO_DA_HOAN_THIEN", "03_QUY_TAC_DA_CHAP_THUAN",
               "04_KINH_NGHIEM_VA_LOI_CAN_TRANH", "05_PHIEU_NHAN_DIEN_HO_SO", "06_PHIEN_BAN"]
LOAI_HO_SO = ["BPTC", "KH_KIEM_TRA_NGHIEM_THU", "KH_THI_NGHIEM", "KH_ATLD", "KSC_LCL",
              "THONG_BAO_HE_THONG_QLCL", "KH_TO_CHUC_THI_CONG", "HS_TRINH_DUYET", "NGHIEM_THU",
              "HOAN_CONG", "BAO_CAO", "TO_TRINH", "THANH_TOAN", "QUYET_TOAN", "KHAC"]

# Từ chỉ loại hình doanh nghiệp — bỏ khi so khớp tên
TU_LOAI_HINH = ["cong ty", "cty", "co phan", "tnhh", "trach nhiem huu han", "mot thanh vien",
                "mtv", "cp", "jsc", "co ltd", "ltd", "company", "corporation", "corp", "tap doan",
                "doanh nghiep tu nhan", "dntn", "hop tac xa", "htx"]


# ---------------------------------------------------------------- tiện ích
def bay_gio(fmt="%Y-%m-%d %H:%M:%S"):
    return _dt.datetime.now().strftime(fmt)


def bo_dau(s: str) -> str:
    s = s.replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def chuan_hoa(s: str) -> str:
    s = bo_dau(s).lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def loi_ten(s: str) -> str:
    """Phần cốt lõi của tên công ty (bỏ 'công ty', 'cổ phần', 'TNHH'...)."""
    s = " " + chuan_hoa(s) + " "
    for t in sorted(TU_LOAI_HINH, key=len, reverse=True):
        s = s.replace(" " + t + " ", " ")
    return re.sub(r"\s+", " ", s).strip()


def slug(s: str, toi_da=40) -> str:
    return chuan_hoa(s).replace(" ", "-")[:toi_da].strip("-") or "ho-so"


def doc_json(p: Path, mac_dinh=None):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return mac_dinh
    except json.JSONDecodeError as e:
        raise SystemExit(f"LỖI: file {p} bị hỏng định dạng JSON ({e}). Không tự sửa — hãy kiểm tra hoặc khôi phục từ backup.")


def ghi_json(p: Path, data):
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, p)


def thay_cho_trong(thu_muc: Path, bien: dict):
    for f in thu_muc.rglob("*.md"):
        t = f.read_text(encoding="utf-8")
        t2 = t
        for k, v in bien.items():
            t2 = t2.replace("{{" + k + "}}", v)
        if t2 != t:
            f.write_text(t2, encoding="utf-8")


# ---------------------------------------------------------------- tìm kho
def cac_vi_tri_ung_vien():
    ds = []
    if os.environ.get("HO_SO_KHO"):
        ds.append(("biến môi trường HO_SO_KHO", Path(os.environ["HO_SO_KHO"])))
    f = SKILL_DIR / "kho_path.txt"
    if f.exists():
        p = f.read_text(encoding="utf-8-sig").strip().strip('"')
        if p:
            ds.append(("file kho_path.txt", Path(p)))
    cwd = Path.cwd()
    for d in [cwd, *cwd.parents]:
        ds.append(("thư mục làm việc", d / TEN_KHO))
        if d.name == TEN_KHO:
            ds.append(("thư mục làm việc", d))
    for p in ["D:/" + TEN_KHO, "/d/" + TEN_KHO, "/mnt/d/" + TEN_KHO]:
        ds.append(("ổ D", Path(p)))
    ds.append(("thư mục người dùng", Path.home() / TEN_KHO))
    ds.append(("thư mục người dùng", Path.home() / "Documents" / TEN_KHO))
    return ds


def la_kho(p: Path) -> bool:
    return (p / D_HT / "SIEU_LENH_CHINH.md").is_file() and (p / D_PC).is_dir()


def tim_kho(chi_dinh=None) -> Path:
    if chi_dinh:
        p = Path(chi_dinh).expanduser().resolve()
        if la_kho(p):
            return p
        raise SystemExit(f"LỖI: '{p}' không phải kho hồ sơ hợp lệ (thiếu 00_HE_THONG/SIEU_LENH_CHINH.md).")
    for _, p in cac_vi_tri_ung_vien():
        try:
            if la_kho(p):
                return p.resolve()
        except OSError:
            continue
    msg = ["LỖI: KHÔNG TÌM THẤY KHO_HO_SO_XAY_DUNG. Đã tìm ở:"]
    msg += [f"  - {p}  ({nguon})" for nguon, p in cac_vi_tri_ung_vien()]
    msg.append("Cách xử lý: chạy lại trình cài đặt, hoặc ghi đường dẫn kho vào file "
               f"{SKILL_DIR / 'kho_path.txt'}")
    raise SystemExit("\n".join(msg))


def ghi_nhat_ky(kho: Path, thao_tac: str, chi_tiet: str):
    f = kho / D_NK / "NHAT_KY.md"
    f.parent.mkdir(parents=True, exist_ok=True)
    if not f.exists():
        f.write_text("# NHẬT KÝ THAO TÁC HỆ THỐNG\n\n| Thời gian | Thao tác | Chi tiết |\n|---|---|---|\n", encoding="utf-8")
    with f.open("a", encoding="utf-8") as h:
        h.write(f"| {bay_gio()} | {thao_tac} | {chi_tiet.replace('|', '/')} |\n")


# ---------------------------------------------------------------- danh bạ công ty
def doc_danh_ba(kho: Path):
    db = doc_json(kho / D_PC / DANH_BA, None)
    if db is None:
        db = {"ma_cuoi": 0, "cong_ty": []}
    return db


def ghi_danh_ba(kho: Path, db):
    ghi_json(kho / D_PC / DANH_BA, db)
    dong = ["# DANH SÁCH CÔNG TY", "",
            "File này sinh tự động từ `danh_ba_cong_ty.json`. Không sửa tay — dùng lệnh `kho.py`.", "",
            "| Mã | Tên công ty | Tên khác / viết tắt | Ngày tạo | Số công trình |", "|---|---|---|---|---|"]
    for c in db["cong_ty"]:
        so_ct = len(doc_json(kho / D_PC / c["ma"] / DANH_BA_CT, {"cong_trinh": []})["cong_trinh"])
        dong.append(f"| {c['ma']} | {c['ten']} | {', '.join(c.get('ten_khac', [])) or '—'} | {c['ngay_tao']} | {so_ct} |")
    if not db["cong_ty"]:
        dong.append("| — | Chưa có công ty nào | | | |")
    (kho / D_PC / "DANH_SACH_CONG_TY.md").write_text("\n".join(dong) + "\n", encoding="utf-8")


def diem_giong(a: str, b: str) -> float:
    la, lb = loi_ten(a), loi_ten(b)
    if not la or not lb:
        return 0.0
    if la == lb:
        return 1.0
    seq = difflib.SequenceMatcher(None, la, lb).ratio()
    ta, tb = set(la.split()), set(lb.split())
    jac = len(ta & tb) / len(ta | tb)
    chua = 0.85 if (la in lb or lb in la) and min(len(la), len(lb)) >= 3 else 0.0
    # viết tắt: "abc" ~ "an binh cuong"
    viet_tat = 0.0
    for x, y in ((la, lb), (lb, la)):
        if " " not in x and len(x) >= 2 and x == "".join(w[0] for w in y.split()):
            viet_tat = 0.8
    return max(seq, jac, chua, viet_tat)


def nhan_dien(kho: Path, ten: str):
    db = doc_danh_ba(kho)
    ket_qua = []
    for c in db["cong_ty"]:
        diem = max(diem_giong(ten, x) for x in [c["ten"], *c.get("ten_khac", [])])
        ket_qua.append((diem, c))
    ket_qua.sort(key=lambda x: -x[0])
    khop = [c for d, c in ket_qua if d >= 0.999]
    gan = [(d, c) for d, c in ket_qua if 0.6 <= d < 0.999]
    return khop, gan


def tim_cty(kho: Path, ma: str):
    for c in doc_danh_ba(kho)["cong_ty"]:
        if c["ma"].upper() == ma.upper():
            return c
    raise SystemExit(f"LỖI: không có công ty mã '{ma}'. Chạy 'kho.py danh-sach' để xem.")


# ---------------------------------------------------------------- lệnh
def lenh_tim_kho(a):
    kho = tim_kho(a.kho)
    print(f"KHO={kho}")
    print(f"Lệnh và công cụ: {SKILL_DIR}")


def lenh_danh_sach(a):
    kho = tim_kho(a.kho)
    db = doc_danh_ba(kho)
    if not db["cong_ty"]:
        print("Kho chưa có công ty nào.")
        return
    for c in db["cong_ty"]:
        khac = f"  (tên khác: {', '.join(c['ten_khac'])})" if c.get("ten_khac") else ""
        print(f"{c['ma']}: {c['ten']}{khac}")


def lenh_nhan_dien(a):
    kho = tim_kho(a.kho)
    khop, gan = nhan_dien(kho, a.ten)
    if len(khop) == 1:
        c = khop[0]
        print(f"KET_QUA=KHOP MA={c['ma']}")
        print(f"Đã tìm thấy: {c['ma']} — {c['ten']}")
        print(f"Kho phong cách: {kho / D_PC / c['ma']}")
        return 0
    if len(khop) > 1 or gan:
        print("KET_QUA=GAN_GIONG")
        print("Có công ty tên gần giống — CẦN NGƯỜI DÙNG XÁC NHẬN:")
        for c in khop:
            print(f"  - {c['ma']}: {c['ten']}  (trùng phần tên chính)")
        for d, c in gan:
            print(f"  - {c['ma']}: {c['ten']}  (giống {d:.0%})")
        return 2
    print("KET_QUA=CHUA_CO")
    print(f"Chưa có công ty '{a.ten}' trong kho. Có thể tạo mới bằng: kho.py tao-cong-ty \"{a.ten}\"")
    return 3


def lenh_tao_cong_ty(a):
    kho = tim_kho(a.kho)
    khop, gan = nhan_dien(kho, a.ten)
    if khop:
        print(f"KHÔNG TẠO: đã có công ty trùng tên: {khop[0]['ma']} — {khop[0]['ten']}")
        return 1
    if gan and not a.xac_nhan_moi:
        print("KHÔNG TẠO: có công ty tên gần giống. Hỏi người dùng; nếu đúng là công ty khác, chạy lại kèm --xac-nhan-moi")
        for d, c in gan:
            print(f"  - {c['ma']}: {c['ten']}  (giống {d:.0%})")
        return 2
    mau = kho / D_PC / MAU_CTY
    if not mau.is_dir():
        raise SystemExit(f"LỖI: thiếu khuôn {mau}")
    db = doc_danh_ba(kho)
    so = db.get("ma_cuoi", 0) + 1
    while (kho / D_PC / f"CONG_TY_{so:03d}").exists():
        so += 1
    ma = f"CONG_TY_{so:03d}"
    dich = kho / D_PC / ma
    shutil.copytree(mau, dich)
    ten_khac = [x.strip() for x in (a.ten_khac or []) if x.strip()]
    thay_cho_trong(dich, {"TEN_CONG_TY": a.ten, "MA_CONG_TY": ma, "NGAY_TAO": bay_gio("%Y-%m-%d"),
                          "TEN_KHAC": ", ".join(ten_khac) or "Chưa xác định"})
    for d in (D_DV, D_DL, D_DX):
        (kho / d / ma).mkdir(parents=True, exist_ok=True)
    ghi_json(dich / DANH_BA_CT, {"ma_cuoi": 0, "cong_trinh": []})
    db["ma_cuoi"] = so
    db["cong_ty"].append({"ma": ma, "ten": a.ten, "ten_khac": ten_khac, "ngay_tao": bay_gio("%Y-%m-%d")})
    ghi_danh_ba(kho, db)
    ghi_nhat_ky(kho, "TẠO CÔNG TY", f"{ma} — {a.ten}")
    print(f"KET_QUA=DA_TAO MA={ma}")
    print(f"Đã tạo kho công ty: {dich}")
    print(f"Thư mục tài liệu đầu vào: {kho / D_DV / ma}")
    return 0


def lenh_tao_cong_trinh(a):
    kho = tim_kho(a.kho)
    c = tim_cty(kho, a.ma_cty)
    ma_cty = c["ma"]
    f_db = kho / D_PC / ma_cty / DANH_BA_CT
    db = doc_json(f_db, {"ma_cuoi": 0, "cong_trinh": []})
    for ct in db["cong_trinh"]:
        if chuan_hoa(ct["ten"]) == chuan_hoa(a.ten):
            print(f"KHÔNG TẠO: công trình đã có: {ct['ma']} — {ct['ten']}")
            print(f"KET_QUA=DA_CO MA_CT={ct['ma']}")
            return 1
    gan = [ct for ct in db["cong_trinh"]
           if difflib.SequenceMatcher(None, chuan_hoa(ct["ten"]), chuan_hoa(a.ten)).ratio() >= 0.8]
    if gan and not a.xac_nhan_moi:
        print("KHÔNG TẠO: có công trình tên gần giống, hỏi người dùng rồi chạy lại kèm --xac-nhan-moi:")
        for ct in gan:
            print(f"  - {ct['ma']}: {ct['ten']}")
        return 2
    so = db.get("ma_cuoi", 0) + 1
    ma = f"CONG_TRINH_{so:03d}"
    bien = {"TEN_CONG_TRINH": a.ten, "MA_CONG_TRINH": ma, "TEN_CONG_TY": c["ten"],
            "MA_CONG_TY": ma_cty, "NGAY_TAO": bay_gio("%Y-%m-%d")}
    dv = kho / D_DV / ma_cty / ma
    shutil.copytree(kho / D_DV / MAU_CT, dv)
    dl = kho / D_DL / ma_cty / ma
    shutil.copytree(kho / D_DL / MAU_CT, dl)
    thay_cho_trong(dl, bien)
    (kho / D_DX / ma_cty / ma).mkdir(parents=True, exist_ok=True)
    db["ma_cuoi"] = so
    db["cong_trinh"].append({"ma": ma, "ten": a.ten, "ngay_tao": bay_gio("%Y-%m-%d")})
    ghi_json(f_db, db)
    dong = [f"# DANH SÁCH CÔNG TRÌNH — {ma_cty}", "", "| Mã | Tên công trình | Ngày tạo |", "|---|---|---|"]
    dong += [f"| {x['ma']} | {x['ten']} | {x['ngay_tao']} |" for x in db["cong_trinh"]]
    (kho / D_PC / ma_cty / "DANH_SACH_CONG_TRINH.md").write_text("\n".join(dong) + "\n", encoding="utf-8")
    ghi_danh_ba(kho, doc_danh_ba(kho))
    ghi_nhat_ky(kho, "TẠO CÔNG TRÌNH", f"{ma_cty}/{ma} — {a.ten}")
    print(f"KET_QUA=DA_TAO MA_CT={ma}")
    print(f"Đưa tài liệu vào: {dv}")
    print(f"Hồ sơ đang làm:   {dl}")
    print(f"Hồ sơ đã xuất:    {kho / D_DX / ma_cty / ma}")
    return 0


def lenh_tim_cong_trinh(a):
    kho = tim_kho(a.kho)
    c = tim_cty(kho, a.ma_cty)
    db = doc_json(kho / D_PC / c["ma"] / DANH_BA_CT, {"cong_trinh": []})
    kq = sorted(((difflib.SequenceMatcher(None, chuan_hoa(ct["ten"]), chuan_hoa(a.ten)).ratio(), ct)
                 for ct in db["cong_trinh"]), key=lambda x: -x[0])
    if kq and kq[0][0] >= 0.999:
        print(f"KET_QUA=KHOP MA_CT={kq[0][1]['ma']}  ({kq[0][1]['ten']})")
        return 0
    gan = [x for x in kq if x[0] >= 0.6]
    if gan:
        print("KET_QUA=GAN_GIONG")
        for d, ct in gan:
            print(f"  - {ct['ma']}: {ct['ten']}  (giống {d:.0%})")
        return 2
    print("KET_QUA=CHUA_CO")
    return 3


def lenh_thong_tin(a):
    kho = tim_kho(a.kho)
    c = tim_cty(kho, a.ma_cty)
    goc = kho / D_PC / c["ma"]
    print(f"CÔNG TY: {c['ma']} — {c['ten']}")
    print(f"KHO PHONG CÁCH: {goc}")
    print("\n[File quy chuẩn — đọc theo thứ tự]")
    for f in FILE_CTY:
        p = goc / f
        print(f"  {'✓' if p.exists() else '✗ THIẾU'} {p}")
    for nhom in ["01_MAU_BIEU", "02_HO_SO_DA_HOAN_THIEN", "03_QUY_TAC_DA_CHAP_THUAN",
                 "04_KINH_NGHIEM_VA_LOI_CAN_TRANH", "06_PHIEN_BAN"]:
        files = [p for p in sorted((goc / nhom).rglob("*")) if p.is_file() and p.name != ".gitkeep"]
        print(f"\n[{nhom}] {len(files)} file")
        for p in files[:200]:
            print(f"  - {p.relative_to(goc)}")
    db = doc_json(goc / DANH_BA_CT, {"cong_trinh": []})
    print(f"\n[Công trình] {len(db['cong_trinh'])}")
    for ct in db["cong_trinh"]:
        print(f"  - {ct['ma']}: {ct['ten']}")
    return 0


def lenh_tao_ho_so(a):
    kho = tim_kho(a.kho)
    c = tim_cty(kho, a.ma_cty)
    loai = a.loai.upper()
    if loai not in LOAI_HO_SO:
        raise SystemExit(f"LỖI: loại hồ sơ '{a.loai}' không có. Dùng một trong: {', '.join(LOAI_HO_SO)}")
    goc = kho / D_DL / c["ma"] / a.ma_ct
    if not goc.is_dir():
        raise SystemExit(f"LỖI: chưa có công trình {c['ma']}/{a.ma_ct}. Tạo bằng tao-cong-trinh trước.")
    ten = f"{bay_gio('%Y%m%d')}_{loai}_{slug(a.ten_ngan)}"
    d = goc / ten
    n = 2
    while d.exists():
        d = goc / f"{ten}_{n}"
        n += 1
    d.mkdir(parents=True)
    (d / "BAN_THAO.md").write_text(
        f"<!-- noi-bo -->\nCông ty: {c['ma']} — {c['ten']}\nCông trình: {a.ma_ct}\nLoại: {loai}\n"
        f"Tạo lúc: {bay_gio()}\nNguồn mẫu/phong cách: [ghi khi chọn mẫu]\n<!-- het-noi-bo -->\n\n# [TÊN HỒ SƠ]\n",
        encoding="utf-8")
    (d / "BAO_CAO_THAM_TRA.md").write_text(f"# BÁO CÁO THẨM TRA — {loai}\n\nCông ty: {c['ma']} — Công trình: {a.ma_ct}\n",
                                           encoding="utf-8")
    ghi_nhat_ky(kho, "TẠO HỒ SƠ", str(d.relative_to(kho)))
    print(f"THU_MUC_HO_SO={d}")
    print(f"THU_MUC_XUAT={kho / D_DX / c['ma'] / a.ma_ct}")
    return 0


def lenh_luu_phien_ban(a):
    kho = tim_kho(a.kho)
    f = Path(a.file).resolve()
    if not f.is_file():
        raise SystemExit(f"LỖI: không thấy file {f}")
    try:
        rel = f.relative_to(kho)
    except ValueError:
        raise SystemExit("LỖI: file không nằm trong kho.")
    parts = rel.parts
    if parts[0] == D_PC and len(parts) > 2 and parts[1].startswith("CONG_TY_"):
        dich_dir = kho / D_PC / parts[1] / "06_PHIEN_BAN"
        rel_ten = "__".join(parts[2:])
    else:
        dich_dir = kho / D_HT / "_PHIEN_BAN"
        rel_ten = "__".join(parts)
    dich_dir.mkdir(parents=True, exist_ok=True)
    dich = dich_dir / f"{Path(rel_ten).stem}__{bay_gio('%Y%m%d_%H%M%S')}{f.suffix}"
    shutil.copy2(f, dich)
    ghi_nhat_ky(kho, "LƯU PHIÊN BẢN", f"{rel} → {dich.relative_to(kho)}")
    print(f"DA_LUU={dich}")
    return 0


def _tao_zip(kho: Path, toan_bo: bool, ra: Path):
    nhom = None if toan_bo else [D_HT, D_PC, D_QT, D_NK, D_MOI]
    dem = 0
    with zipfile.ZipFile(ra, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(kho.rglob("*")):
            rel = p.relative_to(kho)
            if rel.parts[0] == D_BK:
                continue
            if nhom is not None and rel.parts[0] not in nhom:
                continue
            if p.is_file():
                z.write(p, Path(TEN_KHO) / rel)
                dem += 1
    with zipfile.ZipFile(ra) as z:
        hong = z.testzip()
    if hong:
        raise SystemExit(f"LỖI: file backup bị hỏng tại {hong}")
    return dem


def lenh_backup(a):
    kho = tim_kho(a.kho)
    loai = "TOAN_BO" if a.toan_bo else "HE_THONG_VA_PHONG_CACH"
    ra = kho / D_BK / f"BACKUP_{loai}_{bay_gio('%Y%m%d_%H%M%S')}.zip"
    ra.parent.mkdir(parents=True, exist_ok=True)
    dem = _tao_zip(kho, a.toan_bo, ra)
    ghi_nhat_ky(kho, "BACKUP", f"{ra.name} ({dem} file)")
    print(f"DA_BACKUP={ra}")
    print(f"Số file: {dem}; dung lượng: {ra.stat().st_size/1024:.1f} KB; kiểm tra nén: đạt")
    return 0


def lenh_khoi_phuc(a):
    kho = tim_kho(a.kho)
    z = Path(a.file).resolve()
    if not z.is_file():
        cand = kho / D_BK / a.file
        if cand.is_file():
            z = cand
        else:
            raise SystemExit(f"LỖI: không thấy file {a.file}")
    dich = kho / D_BK / f"KHOI_PHUC_{bay_gio('%Y%m%d_%H%M%S')}"
    dich.mkdir(parents=True)
    with zipfile.ZipFile(z) as zf:
        if zf.testzip():
            raise SystemExit("LỖI: file backup bị hỏng.")
        for m in zf.namelist():
            dest = (dich / m).resolve()
            if not str(dest).startswith(str(dich.resolve())):
                raise SystemExit(f"LỖI: file backup chứa đường dẫn không an toàn: {m}")
        zf.extractall(dich)
    ghi_nhat_ky(kho, "KHÔI PHỤC (giải nén)", f"{z.name} → {dich.relative_to(kho)}")
    print(f"DA_GIAI_NEN={dich}")
    print("Dữ liệu trong kho CHƯA bị thay đổi. Xem nội dung trong thư mục trên, "
          "sau đó chép những file cần khôi phục về kho (nên chạy 'kho.py backup' trước khi chép).")
    return 0


def kiem_tra_cau_truc(kho: Path):
    loi, ok = [], []
    for d in (D_HT, D_PC, D_DV, D_DL, D_DX, D_KT, D_BK, D_MOI, D_QT, D_NK):
        (ok if (kho / d).is_dir() else loi).append(f"thư mục {d}")
    for f in FILE_BAT_BUOC:
        (ok if (kho / f).is_file() else loi).append(f"file {f}")
    for f in (f"{D_PC}/{MAU_CTY}", f"{D_DV}/{MAU_CT}", f"{D_DL}/{MAU_CT}"):
        (ok if (kho / f).is_dir() else loi).append(f"khuôn {f}")
    try:
        for f in (kho / D_QT).glob("*.json"):
            json.loads(f.read_text(encoding="utf-8"))
        db = doc_danh_ba(kho)
        ok.append("danh bạ công ty đọc được")
    except SystemExit as e:
        loi.append(str(e))
        db = {"cong_ty": []}
    ma_set = set()
    for c in db["cong_ty"]:
        if c["ma"] in ma_set:
            loi.append(f"mã trùng {c['ma']}")
        ma_set.add(c["ma"])
        for f in FILE_CTY:
            if not (kho / D_PC / c["ma"] / f).exists():
                loi.append(f"{c['ma']} thiếu {f}")
    for p in (kho / D_PC).glob("CONG_TY_*"):
        if p.is_dir() and p.name not in ma_set:
            loi.append(f"thư mục {p.name} không có trong danh bạ")
    return ok, loi


def lenh_kiem_tra(a):
    kho = tim_kho(a.kho)
    ok, loi = kiem_tra_cau_truc(kho)
    print(f"KHO: {kho}")
    print(f"Đạt: {len(ok)} mục")
    if loi:
        print(f"LỖI ({len(loi)}):")
        for x in loi:
            print(f"  ✗ {x}")
        return 1
    print("KẾT LUẬN: cấu trúc kho đầy đủ.")
    return 0


# ---------------------------------------------------------------- tự kiểm tra
def lenh_tu_kiem_tra(a):
    kho_that = tim_kho(a.kho)
    py = sys.executable
    sd = Path(__file__).resolve().parent
    kq = []

    def ghi(so, ten, dat, chi_tiet=""):
        kq.append((so, ten, dat, chi_tiet))

    def chay(*args, cwd=None):
        r = subprocess.run([py, *map(str, args)], capture_output=True, text=True, encoding="utf-8", cwd=cwd)
        return r.returncode, r.stdout + r.stderr

    # Bài 1–2: lệnh và siêu lệnh
    skill = SKILL_DIR / "SKILL.md"
    t = skill.read_text(encoding="utf-8") if skill.exists() else ""
    ghi(1, "Lệnh /ho-so-xay-dung có file SKILL.md hợp lệ",
        bool(re.search(r"^name:\s*ho-so-xay-dung\s*$", t, re.M)), str(skill))
    sl = kho_that / D_HT / "SIEU_LENH_CHINH.md"
    t_sl = sl.read_text(encoding="utf-8") if sl.exists() else ""
    ghi(2, "Truy xuất được siêu lệnh chính", "QUY TẮC KHỐI LƯỢNG" in t_sl and "PHẢN BIỆN" in t_sl, str(sl))

    with tempfile.TemporaryDirectory() as td:
        kho = Path(td) / TEN_KHO
        bo_qua = shutil.ignore_patterns("CONG_TY_*", "*.zip", "KHOI_PHUC_*")
        shutil.copytree(kho_that, kho, ignore=bo_qua)
        if (kho / D_PC / DANH_BA).exists():
            (kho / D_PC / DANH_BA).unlink()
        K = ["--kho", str(kho)]
        me = [str(sd / "kho.py")]

        rc, out = chay(*me, "tim-kho", *K)
        ok, loi = kiem_tra_cau_truc(kho)
        ghi(3, "Truy xuất được kho dữ liệu", rc == 0 and not loi, "; ".join(loi) or "cấu trúc đầy đủ")

        rc_a, out_a = chay(*me, "tao-cong-ty", "Công ty Cổ phần Xây dựng Cầu đường Thử Nghiệm An Bình", *K)
        cty_a = kho / D_PC / "CONG_TY_001"
        con_cho_trong = [str(p.name) for p in cty_a.rglob("*.md") if "{{" in p.read_text(encoding="utf-8")] if cty_a.exists() else ["không có thư mục"]
        ghi(5, "Tạo được kho công ty mới đúng khuôn",
            rc_a == 0 and all((cty_a / f).exists() for f in FILE_CTY) and not con_cho_trong
            and all((cty_a / d).is_dir() for d in THU_MUC_CTY),
            "CONG_TY_001 tạo đủ file; còn chỗ trống: " + (", ".join(con_cho_trong) or "không"))

        r1, o1 = chay(*me, "nhan-dien", "cty CP xây dựng cầu đường thử nghiệm an bình", *K)
        r2, o2 = chay(*me, "nhan-dien", "Thử Nghiệm An", *K)
        r3, o3 = chay(*me, "nhan-dien", "Công ty TNHH Hoàn Toàn Khác Biệt", *K)
        ghi(4, "Nhận diện tên công ty (khớp / gần giống / chưa có)",
            "KET_QUA=KHOP MA=CONG_TY_001" in o1 and "GAN_GIONG" in o2 and "CHUA_CO" in o3,
            f"viết khác dấu/viết tắt loại hình → {o1.splitlines()[0] if o1 else '?'}; "
            f"tên thiếu → {o2.splitlines()[0] if o2 else '?'}; tên lạ → {o3.splitlines()[0] if o3 else '?'}")

        ten_b = "Công ty TNHH Đường Bộ Thử Nghiệm Bắc Hà"
        rb0, _ = chay(*me, "tao-cong-ty", ten_b, *K)  # tên gần giống → phải bị chặn chờ xác nhận
        rb, ob = chay(*me, "tao-cong-ty", ten_b, "--xac-nhan-moi", *K)  # người dùng đã xác nhận
        rdup, odup = chay(*me, "tao-cong-ty", "CÔNG TY CỔ PHẦN XÂY DỰNG CẦU ĐƯỜNG THỬ NGHIỆM AN BÌNH", *K)
        rct, oct_ = chay(*me, "tao-cong-trinh", "CONG_TY_001", "Sửa chữa mặt đường Km10-Km12 (thử)", *K)
        rtt, ott = chay(*me, "thong-tin", "CONG_TY_002", *K)
        cach_ly = (rb0 == 2 and rb == 0 and rdup != 0 and rct == 0
                   and (kho / D_DL / "CONG_TY_001" / "CONG_TRINH_001").is_dir()
                   and not (kho / D_DL / "CONG_TY_002" / "CONG_TRINH_001").exists()
                   and "CONG_TY_001" not in ott and "Km10" not in ott)
        ghi(6, "Phân biệt dữ liệu giữa các công ty", cach_ly,
            f"tên gần giống bị giữ lại chờ xác nhận (mã {rb0}); trùng tên bị chặn (mã {rdup}); "
            "công trình của 001 không xuất hiện ở 002; thông tin 002 không chứa dữ liệu 001")

        tv = (kho / D_QT / "tu_cam.json")
        bt = Path(td) / "BT.md"
        bt.write_text("# BIỆN PHÁP THI CÔNG\n\n## 1. Giới thiệu\nNhà thầu đảm bảo tuyệt đối chất lượng.\n\n"
                      "## 2. Khối lượng\n| TT | Công việc | Đơn vị | Khối lượng |\n|---|---|---|---|\n"
                      "| 1 | Đào nền | m3 | 12.345 |\n| 2 | Bê tông nhựa C12,5 | m2 | 8.900 |\n\n"
                      "Thiếu số hợp đồng [CẦN BỔ SUNG: số hợp đồng].\n", encoding="utf-8")
        lint = str(sd / "kiem_tra_ho_so.py")
        rv, ov = chay(lint, bt, "--loai", "BPTC", *K, "--cong-ty", "CONG_TY_001")
        ghi(7, "Đọc và áp dụng quy tắc văn phong", tv.exists() and "đảm bảo tuyệt đối" in ov, "phát hiện cụm 'đảm bảo tuyệt đối'")
        rtt2, ott2 = chay(lint, bt, "--loai", "THANH_TOAN", *K)
        ghi(8, "Chặn khối lượng chi tiết trong hồ sơ đầu vào", "KHOI_LUONG" in ov and rv != 0 and "KHOI_LUONG" not in ott2,
            "BPTC có bảng khối lượng → bị cảnh báo; cùng nội dung ở hồ sơ THANH_TOAN → không cảnh báo khối lượng")
        ghi(9, "Có cơ chế thẩm tra, phản biện, sửa lỗi",
            (kho / D_QT / "QUY_TRINH_THAM_TRA_PHAN_BIEN.md").exists() and "PHẢN BIỆN" in t_sl and "CAN_BO_SUNG" in ov,
            "quy trình 6 mặt + phản biện + công cụ soát lỗi chạy được")

        rh, oh = chay(*me, "tao-ho-so", "CONG_TY_001", "CONG_TRINH_001", "BPTC", "mat duong", *K)
        m = re.search(r"THU_MUC_XUAT=(.+)", oh)
        xuat_dir = Path(m.group(1).strip()) if m else None
        ok10, ct10 = False, oh.strip()[:200]
        if xuat_dir:
            ra = xuat_dir / "BPTC_CONG_TRINH_001_thu_v1.docx"
            rx1, ox1 = chay(str(sd / "xuat_docx.py"), bt, ra, *K, "--cong-ty", "CONG_TY_001")
            rx2, ox2 = chay(str(sd / "xuat_docx.py"), bt, ra, *K, "--cong-ty", "CONG_TY_001")
            v2 = xuat_dir / "BPTC_CONG_TRINH_001_thu_v2.docx"
            ok10 = rx1 == 0 and ra.exists() and v2.exists()
            ct10 = f"xuất vào {xuat_dir.relative_to(kho)}; lần 2 không ghi đè mà tạo _v2" if ok10 else (ox1 + ox2)[-300:]
        ghi(10, "Tạo file Word và lưu đúng thư mục", ok10, ct10)

        f_pc = cty_a / "QUY_CHUAN_VAN_PHONG.md"
        rp, op = chay(*me, "luu-phien-ban", f_pc, *K)
        ghi(11, "Cơ chế cập nhật kho phong cách có lưu phiên bản",
            rp == 0 and any((cty_a / "06_PHIEN_BAN").glob("QUY_CHUAN_VAN_PHONG__*.md")),
            "bản cũ được chép vào CONG_TY_001/06_PHIEN_BAN trước khi sửa")

        rk, ok_ = chay(*me, "backup", *K)
        mz = re.search(r"DA_BACKUP=(.+)", ok_)
        ok12 = False
        if mz:
            rr, orr = chay(*me, "khoi-phuc", mz.group(1).strip(), *K)
            mg = re.search(r"DA_GIAI_NEN=(.+)", orr)
            ok12 = rr == 0 and mg and (Path(mg.group(1).strip()) / TEN_KHO / D_HT / "SIEU_LENH_CHINH.md").exists()
        ghi(12, "Cơ chế backup và khôi phục", bool(ok12), "nén → kiểm tra nén → giải nén ra thư mục riêng, không ghi đè kho")

    kq.sort()
    dat = sum(1 for x in kq if x[2])
    dong = [f"# BÁO CÁO TỰ KIỂM TRA HỆ THỐNG — {bay_gio()}", "", f"Kho: `{kho_that}`",
            f"Lệnh: `{SKILL_DIR}`", "", "Kiểm tra chạy trên **bản sao tạm** của kho (không đụng dữ liệu thật).", "",
            "| # | Nội dung | Kết quả | Chi tiết |", "|---|---|---|---|"]
    for so, ten, d, ct in kq:
        dong.append(f"| {so} | {ten} | {'ĐẠT' if d else 'KHÔNG ĐẠT'} | {ct.replace('|', '/')} |")
    dong += ["", f"**Tổng: {dat}/{len(kq)} đạt.**"]
    bc = "\n".join(dong) + "\n"
    print(bc)
    if not a.khong_ghi:
        f = kho_that / D_KT / f"TU_KIEM_TRA_{bay_gio('%Y%m%d_%H%M%S')}.md"
        f.write_text(bc, encoding="utf-8")
        ghi_nhat_ky(kho_that, "TỰ KIỂM TRA", f"{dat}/{len(kq)} đạt — {f.name}")
        print(f"Đã lưu báo cáo: {f}")
    return 0 if dat == len(kq) else 1


def main():
    p = argparse.ArgumentParser(description="Quản lý KHO_HO_SO_XAY_DUNG")
    p.add_argument("--kho", help="đường dẫn kho (bỏ trống để tự tìm)")
    sp = p.add_subparsers(dest="lenh", required=True)

    def them(ten, ham, help_):
        x = sp.add_parser(ten, help=help_)
        x.add_argument("--kho", help=argparse.SUPPRESS, default=argparse.SUPPRESS)
        x.set_defaults(ham=ham)
        return x

    them("tim-kho", lenh_tim_kho, "in vị trí kho")
    them("danh-sach", lenh_danh_sach, "liệt kê công ty")
    x = them("nhan-dien", lenh_nhan_dien, "nhận diện công ty theo tên"); x.add_argument("ten")
    x = them("tao-cong-ty", lenh_tao_cong_ty, "tạo kho công ty mới"); x.add_argument("ten")
    x.add_argument("--ten-khac", nargs="*", help="tên viết tắt / tên gọi khác")
    x.add_argument("--xac-nhan-moi", action="store_true", help="người dùng đã xác nhận là công ty khác")
    x = them("tao-cong-trinh", lenh_tao_cong_trinh, "tạo công trình"); x.add_argument("ma_cty"); x.add_argument("ten")
    x.add_argument("--xac-nhan-moi", action="store_true")
    x = them("tim-cong-trinh", lenh_tim_cong_trinh, "tìm công trình theo tên"); x.add_argument("ma_cty"); x.add_argument("ten")
    x = them("thong-tin", lenh_thong_tin, "liệt kê kho phong cách của công ty"); x.add_argument("ma_cty")
    x = them("tao-ho-so", lenh_tao_ho_so, "tạo thư mục hồ sơ đang làm")
    x.add_argument("ma_cty"); x.add_argument("ma_ct"); x.add_argument("loai"); x.add_argument("ten_ngan")
    x = them("luu-phien-ban", lenh_luu_phien_ban, "lưu bản cũ của file trước khi sửa"); x.add_argument("file")
    x = them("backup", lenh_backup, "sao lưu"); x.add_argument("--toan-bo", action="store_true")
    x = them("khoi-phuc", lenh_khoi_phuc, "giải nén bản sao lưu ra thư mục riêng"); x.add_argument("file")
    them("kiem-tra", lenh_kiem_tra, "kiểm tra cấu trúc kho")
    x = them("tu-kiem-tra", lenh_tu_kiem_tra, "chạy 12 bài kiểm tra trên bản sao tạm")
    x.add_argument("--khong-ghi", action="store_true", help="không lưu báo cáo vào kho")
    x = them("ghi-nhat-ky", lambda a: (ghi_nhat_ky(tim_kho(a.kho), a.thao_tac, a.chi_tiet), print("đã ghi"))[0] or 0,
             "ghi một dòng nhật ký"); x.add_argument("thao_tac"); x.add_argument("chi_tiet")
    a = p.parse_args()
    if not hasattr(a, "kho"):
        a.kho = None
    rc = a.ham(a)
    sys.exit(rc or 0)


if __name__ == "__main__":
    main()
