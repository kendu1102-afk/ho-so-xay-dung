#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
xuat_docx.py — Xuất bản thảo Markdown thành Word theo định dạng của công ty.

python xuat_docx.py BAN_THAO.md ra.docx [--kho <kho>] [--cong-ty CONG_TY_001] [--mau mau.docx]
Cần thư viện python-docx (pip install python-docx).
Không ghi đè: nếu ra.docx đã có, tự lưu thành _v2, _v3...
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kho as K  # noqa: E402

try:
    from docx import Document
    from docx.enum.section import WD_ORIENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Mm, Pt, RGBColor
except ImportError:
    print("LỖI: máy chưa có thư viện python-docx. Cài bằng lệnh:  python -m pip install python-docx")
    sys.exit(2)

CAN = {"giua": WD_ALIGN_PARAGRAPH.CENTER, "trai": WD_ALIGN_PARAGRAPH.LEFT,
       "phai": WD_ALIGN_PARAGRAPH.RIGHT, "deu": WD_ALIGN_PARAGRAPH.JUSTIFY}


def tai_dinh_dang(kho, ma_cty):
    d = {}
    nguon = []
    if kho:
        d = K.doc_json(kho / K.D_QT / "dinh_dang_mac_dinh.json", {}) or {}
        nguon.append("mặc định chung")
        if ma_cty:
            rieng = K.doc_json(kho / K.D_PC / ma_cty / "dinh_dang.json", {}) or {}
            dem = 0
            for k, v in rieng.items():
                if k.startswith("_") or v in ("chua_xac_dinh", None, ""):
                    continue
                if isinstance(v, dict) and isinstance(d.get(k), dict):
                    d[k] = {**d[k], **v}
                else:
                    d[k] = v
                dem += 1
            nguon.append(f"{ma_cty}: {dem} mục riêng")
    mac = {"font": "Times New Roman", "co_chu": 13, "gian_dong": 1.15, "cach_doan_sau_pt": 6,
           "thut_dau_dong_cm": 1.0, "le_tren_mm": 20, "le_duoi_mm": 20, "le_trai_mm": 30, "le_phai_mm": 15,
           "kho_giay": "A4", "huong_giay": "doc", "tieu_de_ho_so": {"co_chu": 16, "dam": True, "in_hoa": True, "can": "giua"},
           "de_muc_1": {"dam": True, "in_hoa": True}, "de_muc_2": {"dam": True}, "de_muc_3": {"dam": True, "nghieng": True},
           "de_muc_4": {"nghieng": True}, "bang": {"co_chu": 12, "dong_tieu_de_dam": True, "vien": True},
           "header": "", "footer": "", "so_trang": "giua_duoi", "file_mau_word": ""}
    for k, v in mac.items():
        d.setdefault(k, v)
    return d, nguon


def dat_font(run, ten, co=None, dam=None, nghieng=None):
    run.font.name = ten
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.append(rf)
    for att in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rf.set(qn(att), ten)
    if co:
        run.font.size = Pt(co)
    if dam is not None:
        run.font.bold = dam
    if nghieng is not None:
        run.font.italic = nghieng


def them_inline(p, text, dd, co=None, dam=False, nghieng=False, in_hoa=False):
    if in_hoa:
        text = text.upper()
    phan = re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)", text)
    for x in phan:
        if not x:
            continue
        b, i = dam, nghieng
        if x.startswith("**") and x.endswith("**"):
            x, b = x[2:-2], True
        elif x.startswith("*") and x.endswith("*") and len(x) > 2:
            x, i = x[1:-1], True
        elif x.startswith("`") and x.endswith("`"):
            x = x[1:-1]
        r = p.add_run(x)
        dat_font(r, dd["font"], co or dd["co_chu"], b, i)


def them_truong_so_trang(p):
    r = p.add_run()
    for loai, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        if loai:
            e = OxmlElement("w:fldChar")
            e.set(qn("w:fldCharType"), loai)
        else:
            e = OxmlElement("w:instrText")
            e.set(qn("xml:space"), "preserve")
            e.text = txt
        r._element.append(e)


def ke_vien(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for canh in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{canh}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "4")
        e.set(qn("w:color"), "000000")
        b.append(e)
    tblPr.append(b)


def ten_khong_trung(p: Path) -> Path:
    if not p.exists():
        return p
    m = re.match(r"^(.*)_v(\d+)$", p.stem)
    goc, n = (m.group(1), int(m.group(2)) + 1) if m else (p.stem, 2)
    while True:
        q = p.with_name(f"{goc}_v{n}{p.suffix}")
        if not q.exists():
            return q
        n += 1


def tao_tai_lieu(dd, mau, kho, ma_cty):
    duong_mau = None
    if mau:
        duong_mau = Path(mau)
    elif dd.get("file_mau_word"):
        q = Path(dd["file_mau_word"])
        if not q.is_absolute() and kho and ma_cty:
            q = kho / K.D_PC / ma_cty / q
        duong_mau = q
    if duong_mau and duong_mau.is_file():
        doc = Document(str(duong_mau))
        body = doc.element.body
        for el in list(body):
            if el.tag != qn("w:sectPr"):
                body.remove(el)
        return doc, f"file mẫu Word: {duong_mau}"
    doc = Document()
    s = doc.sections[0]
    if dd.get("kho_giay", "A4") == "A4":
        s.page_width, s.page_height = Mm(210), Mm(297)
    if dd.get("huong_giay") == "ngang":
        s.orientation = WD_ORIENT.LANDSCAPE
        s.page_width, s.page_height = s.page_height, s.page_width
    s.top_margin, s.bottom_margin = Mm(dd["le_tren_mm"]), Mm(dd["le_duoi_mm"])
    s.left_margin, s.right_margin = Mm(dd["le_trai_mm"]), Mm(dd["le_phai_mm"])
    if dd.get("header"):
        hp = s.header.paragraphs[0]
        them_inline(hp, dd["header"], dd, co=dd["co_chu"] - 2, nghieng=True)
    fp = s.footer.paragraphs[0]
    if dd.get("footer"):
        them_inline(fp, dd["footer"] + "    ", dd, co=dd["co_chu"] - 2)
    if dd.get("so_trang"):
        fp.alignment = CAN.get(dd["so_trang"].split("_")[0], WD_ALIGN_PARAGRAPH.CENTER)
        them_truong_so_trang(fp)
    return doc, ("file mẫu Word KHÔNG TÌM THẤY: " + str(duong_mau) + " — dùng trang trắng") if duong_mau else "trang trắng theo dinh_dang.json"


def dinh_dang_doan(p, dd, thut=True):
    pf = p.paragraph_format
    pf.line_spacing = dd["gian_dong"]
    pf.space_after = Pt(dd["cach_doan_sau_pt"])
    pf.space_before = Pt(0)
    if thut and dd.get("thut_dau_dong_cm"):
        pf.first_line_indent = Cm(dd["thut_dau_dong_cm"])
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY


def xuat(md: str, doc, dd):
    md = re.sub(r"<!--\s*noi-bo\s*-->.*?<!--\s*het-noi-bo\s*-->", "", md, flags=re.S | re.I)
    dong = md.splitlines()
    i, dem = 0, {"doan": 0, "bang": 0, "de_muc": 0}
    buf = []

    def xa_buf():
        if buf:
            p = doc.add_paragraph()
            dinh_dang_doan(p, dd)
            them_inline(p, " ".join(x.strip() for x in buf), dd)
            dem["doan"] += 1
            buf.clear()

    while i < len(dong):
        d = dong[i]
        s = d.strip()
        if re.match(r"<!--\s*ngat-trang\s*-->", s):
            xa_buf()
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        elif s.startswith("<!--"):
            pass
        elif not s:
            xa_buf()
        elif s.startswith("|"):
            xa_buf()
            rows = []
            while i < len(dong) and dong[i].strip().startswith("|"):
                r = dong[i].strip().strip("|")
                if not re.fullmatch(r"[\s:\-|]+", r):
                    rows.append([c.strip() for c in r.split("|")])
                i += 1
            i -= 1
            if rows:
                n = max(len(r) for r in rows)
                t = doc.add_table(rows=len(rows), cols=n)
                if dd["bang"].get("vien", True):
                    ke_vien(t)
                for ri, r in enumerate(rows):
                    for ci in range(n):
                        cell = t.cell(ri, ci)
                        p = cell.paragraphs[0]
                        them_inline(p, r[ci] if ci < len(r) else "", dd, co=dd["bang"].get("co_chu", dd["co_chu"] - 1),
                                    dam=(ri == 0 and dd["bang"].get("dong_tieu_de_dam", True)))
                        if ri == 0:
                            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                doc.add_paragraph().paragraph_format.space_after = Pt(0)
                dem["bang"] += 1
        elif re.match(r"^#{1,4}\s", s):
            xa_buf()
            cap = len(s.split()[0])
            text = s[cap:].strip()
            p = doc.add_paragraph()
            if cap == 1:
                cfg = dd["tieu_de_ho_so"]
                p.alignment = CAN.get(cfg.get("can", "giua"), WD_ALIGN_PARAGRAPH.CENTER)
                p.paragraph_format.space_after = Pt(12)
            else:
                cfg = dd.get(f"de_muc_{cap-1}", {})
                p.paragraph_format.space_before = Pt(6)
                p.paragraph_format.space_after = Pt(dd["cach_doan_sau_pt"])
                p.paragraph_format.keep_with_next = True
                # mức dàn ý để hiện trong Navigation Pane
                ppr = p._p.get_or_add_pPr()
                ol = OxmlElement("w:outlineLvl")
                ol.set(qn("w:val"), str(cap - 2))
                ppr.append(ol)
            them_inline(p, text, dd, co=cfg.get("co_chu", dd["co_chu"]), dam=cfg.get("dam", False),
                        nghieng=cfg.get("nghieng", False), in_hoa=cfg.get("in_hoa", False))
            for r in p.runs:
                r.font.color.rgb = RGBColor(0, 0, 0)
            dem["de_muc"] += 1
        elif re.match(r"^([-*+]|\d+[.)])\s+", s):
            xa_buf()
            m = re.match(r"^([-*+]|\d+[.)])\s+(.*)$", s)
            ky = "–" if m.group(1) in "-*+" else m.group(1)
            muc = (len(d) - len(d.lstrip())) // 2
            p = doc.add_paragraph()
            dinh_dang_doan(p, dd, thut=False)
            p.paragraph_format.left_indent = Cm(1.0 + 0.75 * muc)
            p.paragraph_format.first_line_indent = Cm(-0.6)
            them_inline(p, f"{ky} {m.group(2)}", dd)
            dem["doan"] += 1
        else:
            buf.append(s)
        i += 1
    xa_buf()
    return dem


def kiem_tra_sau_xuat(ra: Path):
    doc = Document(str(ra))
    text = "\n".join(p.text for p in doc.paragraphs)
    for t in doc.tables:
        for row in t.rows:
            for c in row.cells:
                text += "\n" + c.text
    van_de = []
    for ky in ("**", "##", "|---", "<!--"):
        if ky in text:
            van_de.append(f"còn ký hiệu Markdown '{ky}'")
    con = re.findall(r"\[(?:CẦN BỔ SUNG|KIỂM TRA HIỆU LỰC)[^\]]*\]", text)
    so_trang = "chưa đếm được (máy không có LibreOffice)"
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if soffice:
        try:
            with tempfile.TemporaryDirectory() as td:
                subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", td, str(ra)],
                               capture_output=True, timeout=180)
                pdf = next(Path(td).glob("*.pdf"), None)
                if pdf:
                    b = pdf.read_bytes()
                    so_trang = str(len(re.findall(rb"/Type\s*/Page(?!s)", b)))
        except Exception as e:  # noqa: BLE001
            so_trang = f"chưa đếm được ({e.__class__.__name__})"
    return len(doc.paragraphs), len(doc.tables), so_trang, van_de, con


def main():
    p = argparse.ArgumentParser()
    p.add_argument("vao")
    p.add_argument("ra")
    p.add_argument("--kho")
    p.add_argument("--cong-ty")
    p.add_argument("--mau", help="file Word mẫu làm nền (giữ header/footer/logo)")
    a = p.parse_args()
    try:
        kho = K.tim_kho(a.kho)
    except SystemExit:
        kho = None
    dd, nguon = tai_dinh_dang(kho, a.cong_ty)
    doc, nen = tao_tai_lieu(dd, a.mau, kho, a.cong_ty)
    st = doc.styles["Normal"]
    st.font.name = dd["font"]
    st.font.size = Pt(dd["co_chu"])
    st.element.get_or_add_rPr()
    md = Path(a.vao).read_text(encoding="utf-8")
    dem = xuat(md, doc, dd)
    ra = ten_khong_trung(Path(a.ra))
    ra.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(ra))
    so_doan, so_bang, so_trang, van_de, con = kiem_tra_sau_xuat(ra)
    print(f"DA_XUAT={ra}")
    print(f"Định dạng: {', '.join(nguon) or 'mặc định trong công cụ'}; nền: {nen}")
    print(f"Đề mục: {dem['de_muc']} | đoạn: {so_doan} | bảng: {so_bang} | số trang: {so_trang}")
    print("Lỗi trình bày: " + ("; ".join(van_de) if van_de else "không phát hiện"))
    if con:
        print(f"CÒN {len(con)} CHỖ CHƯA HOÀN THIỆN trong file: " + "; ".join(sorted(set(con)))[:500])
    if Path(a.ra) != ra:
        print(f"Lưu ý: file {Path(a.ra).name} đã tồn tại nên KHÔNG ghi đè, lưu thành {ra.name}")
    sys.exit(0)


if __name__ == "__main__":
    main()
