@echo off
chcp 65001 >nul
echo Dang cai dat he thong lam ho so xay dung...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0cai_dat.ps1" %*
echo.
pause
