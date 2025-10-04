@echo off
setlocal enabledelayedexpansion

:: yt-dlp Web UI - Windows Durdurma Scripti
:: Bu script çalışan servisleri güvenli şekilde durdurur

title yt-dlp Web UI - Durdurma

echo.
echo ========================================
echo    yt-dlp Web UI - Servisleri Durdur
echo ========================================
echo.

:: Renk kodları (Windows 10+ için)
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

:: Fonksiyonlar
call :print_status "Servisler durduruluyor..."

:: PID dosyalarını kontrol et
if exist ".backend.pid" (
    set /p BACKEND_PID=<.backend.pid
    call :print_status "Backend PID: %BACKEND_PID%"
)

if exist ".frontend.pid" (
    set /p FRONTEND_PID=<.frontend.pid
    call :print_status "Frontend PID: %FRONTEND_PID%"
)

:: Python processlerini durdur
call :print_status "Python processleri durduruluyor..."
tasklist /fi "imagename eq python.exe" /fo csv | find "python.exe" >nul
if not errorlevel 1 (
    taskkill /f /im python.exe >nul 2>&1
    if errorlevel 1 (
        call :print_warning "Python processleri durdurulamadı"
    ) else (
        call :print_success "Python processleri durduruldu"
    )
) else (
    call :print_status "Çalışan Python processi bulunamadı"
)

:: Node.js processlerini durdur
call :print_status "Node.js processleri durduruluyor..."
tasklist /fi "imagename eq node.exe" /fo csv | find "node.exe" >nul
if not errorlevel 1 (
    taskkill /f /im node.exe >nul 2>&1
    if errorlevel 1 (
        call :print_warning "Node.js processleri durdurulamadı"
    ) else (
        call :print_success "Node.js processleri durduruldu"
    )
) else (
    call :print_status "Çalışan Node.js processi bulunamadı"
)

:: npm processlerini durdur
call :print_status "npm processleri durduruluyor..."
tasklist /fi "imagename eq npm.exe" /fo csv | find "npm.exe" >nul
if not errorlevel 1 (
    taskkill /f /im npm.exe >nul 2>&1
    call :print_success "npm processleri durduruldu"
) else (
    call :print_status "Çalışan npm processi bulunamadı"
)

:: Port kontrolü ve temizlik
call :print_status "Port kontrolü yapılıyor..."

:: Port 8000 kontrolü
netstat -ano | find ":8000" >nul
if not errorlevel 1 (
    call :print_warning "Port 8000 hala kullanımda, zorla temizleniyor..."
    for /f "tokens=5" %%a in ('netstat -ano ^| find ":8000"') do (
        taskkill /f /pid %%a >nul 2>&1
    )
)

:: Port 3000 kontrolü
netstat -ano | find ":3000" >nul
if not errorlevel 1 (
    call :print_warning "Port 3000 hala kullanımda, zorla temizleniyor..."
    for /f "tokens=5" %%a in ('netstat -ano ^| find ":3000"') do (
        taskkill /f /pid %%a >nul 2>&1
    )
)

:: PID dosyalarını temizle
if exist ".backend.pid" del ".backend.pid"
if exist ".frontend.pid" del ".frontend.pid"
if exist ".idle-monitor.pid" del ".idle-monitor.pid"

call :print_success "PID dosyaları temizlendi"

:: Geçici dosyaları temizle
if exist "backend\__pycache__" rmdir /s /q "backend\__pycache__"
if exist "backend\src\__pycache__" rmdir /s /q "backend\src\__pycache__"
if exist "backend\src\api\__pycache__" rmdir /s /q "backend\src\api\__pycache__"
if exist "backend\src\models\__pycache__" rmdir /s /q "backend\src\models\__pycache__"
if exist "backend\src\services\__pycache__" rmdir /s /q "backend\src\services\__pycache__"
if exist "backend\src\storage\__pycache__" rmdir /s /q "backend\src\storage\__pycache__"
if exist "backend\src\middleware\__pycache__" rmdir /s /q "backend\src\middleware\__pycache__"

call :print_success "Geçici dosyalar temizlendi"

:: Son kontrol
timeout /t 2 /nobreak >nul

:: Port kontrolü
netstat -ano | find ":8000" >nul
if errorlevel 1 (
    call :print_success "Port 8000 serbest"
) else (
    call :print_warning "Port 8000 hala kullanımda"
)

netstat -ano | find ":3000" >nul
if errorlevel 1 (
    call :print_success "Port 3000 serbest"
) else (
    call :print_warning "Port 3000 hala kullanımda"
)

echo.
call :print_success "🎉 Tüm servisler başarıyla durduruldu!"
echo.
echo %GREEN%✅ Backend durduruldu%NC%
echo %GREEN%✅ Frontend durduruldu%NC%
echo %GREEN%✅ Portlar temizlendi%NC%
echo %GREEN%✅ Geçici dosyalar silindi%NC%
echo.
echo %BLUE%💡 Tekrar başlatmak için: setup-windows.bat%NC%
echo.

pause
goto :eof

:: ========================================
:: FONKSIYONLAR
:: ========================================

:print_status
echo %BLUE%[INFO]%NC% %~1
goto :eof

:print_success
echo %GREEN%[SUCCESS]%NC% %~1
goto :eof

:print_warning
echo %YELLOW%[WARNING]%NC% %~1
goto :eof

:print_error
echo %RED%[ERROR]%NC% %~1
goto :eof
