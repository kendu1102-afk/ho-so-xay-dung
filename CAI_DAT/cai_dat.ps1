# Trinh cai dat HE THONG SIEU LENH LAM HO SO XAY DUNG cho Windows.
# Chay bang: nhay dup CAI_DAT_WINDOWS.bat (khong can mo file nay).
# - Cai lenh /ho-so-xay-dung vao %USERPROFILE%\.claude\skills\ho-so-xay-dung (dung cho moi du an)
# - Tao/bo sung kho du lieu: uu tien D:\KHO_HO_SO_XAY_DUNG
# - KHONG xoa, KHONG ghi de du lieu kho da co. Ban lenh cu (neu co) duoc cat sang thu muc backup.
param([string]$Kho = "")

$ErrorActionPreference = "Stop"
$Goc = Split-Path -Parent $PSScriptRoot
$NguonKho = Join-Path $Goc "KHO_HO_SO_XAY_DUNG"
$NguonLenh = Join-Path $Goc ".claude\skills\ho-so-xay-dung"
$ThuMucClaude = Join-Path $env:USERPROFILE ".claude"
$DichLenh = Join-Path $ThuMucClaude "skills\ho-so-xay-dung"
$Gio = Get-Date -Format "yyyyMMdd_HHmmss"

function Ghi($t) { Write-Host $t }
function ThuGhi($thuMuc) {
    try {
        if (-not (Test-Path $thuMuc)) { return $false }
        $f = Join-Path $thuMuc (".thu_ghi_" + [guid]::NewGuid().ToString() + ".tmp")
        [IO.File]::WriteAllText($f, "x"); Remove-Item $f -Force; return $true
    } catch { return $false }
}

Ghi "=== CAI DAT HE THONG SIEU LENH LAM HO SO XAY DUNG ==="
if (-not (Test-Path (Join-Path $NguonKho "00_HE_THONG\SIEU_LENH_CHINH.md"))) { throw "Khong thay thu muc KHO_HO_SO_XAY_DUNG canh thu muc CAI_DAT. Hay giai nen day du roi chay lai." }
if (-not (Test-Path (Join-Path $NguonLenh "SKILL.md"))) { throw "Khong thay .claude\skills\ho-so-xay-dung\SKILL.md. Hay giai nen day du (ke ca thu muc an .claude)." }

# 1. Chon vi tri kho
if (-not $Kho) {
    if (ThuGhi "D:\") { $Kho = "D:\KHO_HO_SO_XAY_DUNG" }
    else {
        $Kho = Join-Path ([Environment]::GetFolderPath("MyDocuments")) "KHO_HO_SO_XAY_DUNG"
        Ghi "Khong co o D: hoac khong ghi duoc -> dung $Kho"
    }
}
Ghi "Kho du lieu: $Kho"

# 2. Tao / bo sung kho (chi chep file con thieu, khong ghi de)
$daCo = Test-Path (Join-Path $Kho "00_HE_THONG\SIEU_LENH_CHINH.md")
New-Item -ItemType Directory -Force -Path $Kho | Out-Null
robocopy "$NguonKho" "$Kho" /E /XC /XN /XO /XF .gitkeep /XD __pycache__ /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw "Loi khi chep kho (robocopy ma $LASTEXITCODE)." }
if ($daCo) { Ghi "Kho da ton tai -> chi bo sung file con thieu, KHONG ghi de file cu." } else { Ghi "Da tao kho moi." }

# 3. Cai lenh /ho-so-xay-dung (toan may)
New-Item -ItemType Directory -Force -Path (Join-Path $ThuMucClaude "skills") | Out-Null
if (Test-Path $DichLenh) {
    $Bk = Join-Path $ThuMucClaude ("ho-so-xay-dung_backup\" + $Gio)
    $n = 2
    while (Test-Path $Bk) { $Bk = Join-Path $ThuMucClaude ("ho-so-xay-dung_backup\" + $Gio + "_" + $n); $n++ }
    New-Item -ItemType Directory -Force -Path (Split-Path $Bk) | Out-Null
    Move-Item $DichLenh $Bk
    Ghi "Lenh cu da duoc cat sang: $Bk"
}
Copy-Item $NguonLenh $DichLenh -Recurse
Get-ChildItem $DichLenh -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force
[IO.File]::WriteAllText((Join-Path $DichLenh "kho_path.txt"), $Kho)
Ghi "Da cai lenh: $DichLenh"

# 4. Kiem tra bang Python (neu co)
$py = $null
foreach ($c in @(@("py", "-3"), @("python"), @("python3"))) {
    try {
        $args0 = @(); if ($c.Length -gt 1) { $args0 = $c[1..($c.Length-1)] }
        & $c[0] @args0 -c "import sys; assert sys.version_info >= (3,8)" 2>$null
        if ($LASTEXITCODE -eq 0) { $py = $c; break }
    } catch {}
}
if ($py) {
    $args0 = @(); if ($py.Length -gt 1) { $args0 = $py[1..($py.Length-1)] }
    $kp = Join-Path $DichLenh "scripts\kho.py"
    Ghi ""
    Ghi "--- Kiem tra cau truc kho ---"
    & $py[0] @args0 $kp kiem-tra
    & $py[0] @args0 -c "import docx" 2>$null
    if ($LASTEXITCODE -ne 0) { Ghi "Chua co thu vien xuat Word (python-docx). Claude se xin phep cai khi can, hoac tu chay: py -m pip install python-docx" }
} else {
    Ghi "CHUA CO PYTHON. Hay cai Python 3 tai https://www.python.org/downloads/ (tich 'Add Python to PATH'), sau do mo lai Claude Code."
}

Ghi ""
Ghi "=== CAI DAT XONG ==="
Ghi "Lenh kich hoat : /ho-so-xay-dung   (mo lai Claude Code neu dang mo)"
Ghi "Kho du lieu    : $Kho"
Ghi "Huong dan      : $Kho\00_HE_THONG\HUONG_DAN_SU_DUNG.md"
