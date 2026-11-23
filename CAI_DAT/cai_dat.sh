#!/usr/bin/env bash
# Trình cài đặt cho Linux / macOS / Git Bash / WSL.
#   bash CAI_DAT/cai_dat.sh                 # kho mặc định
#   bash CAI_DAT/cai_dat.sh --kho /duong/dan/KHO_HO_SO_XAY_DUNG
# Không xóa, không ghi đè dữ liệu kho đã có. Bản lệnh cũ được cất sang ~/.claude/ho-so-xay-dung_backup/.
set -euo pipefail
GOC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NGUON_KHO="$GOC/KHO_HO_SO_XAY_DUNG"
NGUON_LENH="$GOC/.claude/skills/ho-so-xay-dung"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
DICH_LENH="$CLAUDE_DIR/skills/ho-so-xay-dung"
GIO="$(date +%Y%m%d_%H%M%S)"
KHO=""
[[ "${1:-}" == "--kho" ]] && KHO="${2:-}"

echo "=== CÀI ĐẶT HỆ THỐNG SIÊU LỆNH LÀM HỒ SƠ XÂY DỰNG ==="
[[ -f "$NGUON_KHO/00_HE_THONG/SIEU_LENH_CHINH.md" ]] || { echo "Thiếu thư mục KHO_HO_SO_XAY_DUNG"; exit 1; }
[[ -f "$NGUON_LENH/SKILL.md" ]] || { echo "Thiếu .claude/skills/ho-so-xay-dung/SKILL.md"; exit 1; }

if [[ -z "$KHO" ]]; then
  for d in /d /mnt/d; do
    if [[ -d "$d" && -w "$d" ]]; then KHO="$d/KHO_HO_SO_XAY_DUNG"; break; fi
  done
  KHO="${KHO:-$HOME/KHO_HO_SO_XAY_DUNG}"
fi
echo "Kho dữ liệu: $KHO"

if [[ "$(cd "$NGUON_KHO" && pwd -P)" == "$(mkdir -p "$KHO" && cd "$KHO" && pwd -P)" ]]; then
  echo "Kho chính là thư mục nguồn — không cần chép."
else
  DA_CO=0; [[ -f "$KHO/00_HE_THONG/SIEU_LENH_CHINH.md" ]] && DA_CO=1
  # chỉ chép file còn thiếu (không ghi đè)
  (cd "$NGUON_KHO" && find . -type d ! -name __pycache__ -print0 | while IFS= read -r -d '' d; do mkdir -p "$KHO/$d"; done
   find . -type f ! -name .gitkeep ! -path '*/__pycache__/*' -print0 | while IFS= read -r -d '' f; do
     [[ -e "$KHO/$f" ]] || cp -p "$f" "$KHO/$f"; done)
  [[ $DA_CO == 1 ]] && echo "Kho đã tồn tại → chỉ bổ sung file còn thiếu." || echo "Đã tạo kho mới."
fi

mkdir -p "$CLAUDE_DIR/skills"
if [[ -e "$DICH_LENH" ]]; then
  mkdir -p "$CLAUDE_DIR/ho-so-xay-dung_backup"
  BK="$CLAUDE_DIR/ho-so-xay-dung_backup/$GIO"; n=2
  while [[ -e "$BK" ]]; do BK="$CLAUDE_DIR/ho-so-xay-dung_backup/${GIO}_$n"; n=$((n+1)); done
  mv "$DICH_LENH" "$BK"
  echo "Lệnh cũ đã cất sang: $BK"
fi
cp -R "$NGUON_LENH" "$DICH_LENH"
find "$DICH_LENH" -name __pycache__ -type d -prune -exec rm -rf {} +
printf '%s' "$KHO" > "$DICH_LENH/kho_path.txt"
echo "Đã cài lệnh: $DICH_LENH"

PY="$(command -v python3 || command -v python || true)"
if [[ -n "$PY" ]]; then
  "$PY" "$DICH_LENH/scripts/kho.py" kiem-tra || true
  "$PY" -c "import docx" 2>/dev/null || echo "Chưa có python-docx (xuất Word): $PY -m pip install python-docx"
else
  echo "CHƯA CÓ PYTHON 3 — hãy cài để dùng đầy đủ công cụ."
fi
echo "=== CÀI ĐẶT XONG ==="
echo "Lệnh: /ho-so-xay-dung   |   Kho: $KHO"
