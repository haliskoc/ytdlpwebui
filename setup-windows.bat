@echo off
setlocal enabledelayedexpansion

:: yt-dlp Web UI - Windows One-Click Setup Script
:: Bu script uygulamayı tek komutla kurar ve çalıştırır

title yt-dlp Web UI - Windows Kurulum

echo.
echo ========================================
echo    yt-dlp Web UI - Windows Kurulum
echo ========================================
echo.

:: Renk kodları (Windows 10+ için)
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

:: Fonksiyonlar
call :print_status "Windows kurulum başlatılıyor..."

:: Python kontrolü
call :check_python
if errorlevel 1 (
    call :print_error "Python 3.8+ gerekli ama yüklü değil"
    call :print_status "Lütfen Python 3.8+ yükleyin: https://www.python.org/downloads/"
    pause
    exit /b 1
)

:: Node.js kontrolü
call :check_nodejs
if errorlevel 1 (
    call :print_error "Node.js 16+ gerekli ama yüklü değil"
    call :print_status "Lütfen Node.js 16+ yükleyin: https://nodejs.org/"
    pause
    exit /b 1
)

:: npm kontrolü
call :check_npm
if errorlevel 1 (
    call :print_error "npm gerekli ama yüklü değil"
    pause
    exit /b 1
)

:: yt-dlp kontrolü ve kurulumu
call :check_ytdlp

:: Gerekli dizinleri oluştur
call :create_directories

:: Environment dosyası oluştur
call :create_env_file

:: Backend kurulumu
call :setup_backend
if errorlevel 1 (
    call :print_error "Backend kurulumu başarısız"
    pause
    exit /b 1
)

:: Frontend kurulumu
call :setup_frontend
if errorlevel 1 (
    call :print_error "Frontend kurulumu başarısız"
    pause
    exit /b 1
)

:: Servisleri başlat
call :start_services
if errorlevel 1 (
    call :print_error "Servisler başlatılamadı"
    pause
    exit /b 1
)

:: Başarı mesajı
echo.
call :print_success "🎉 yt-dlp Web UI başarıyla çalışıyor!"
echo.
echo %GREEN%📱 Frontend:%NC% http://localhost:3000
echo %GREEN%🔧 Backend:%NC%  http://localhost:8000
echo %GREEN%📊 Health:%NC%   http://localhost:8000/health
echo.
echo %YELLOW%📝 Loglar:%NC%
echo    Backend:  logs\backend.log
echo    Frontend: logs\frontend.log
echo.
echo %YELLOW%🛑 Durdurmak için:%NC% stop-windows.bat
echo.
echo %BLUE%💡 Tarayıcı otomatik açılıyor...%NC%

:: Tarayıcıyı aç
timeout /t 3 /nobreak >nul
start http://localhost:3000

echo.
echo %BLUE%🎯 Uygulama başarıyla başlatıldı!%NC%
echo %BLUE%   Tarayıcınızda http://localhost:3000 adresini açın%NC%
echo.
echo %YELLOW%⏰ Otomatik kapanma:%NC% 3 dakika hareketsizlikten sonra otomatik kapanır
echo %YELLOW%   Aktivite web arayüzü kullanıldığında takip edilir%NC%
echo.

:: Pid dosyalarını oluştur
echo %BACKEND_PID% > .backend.pid
echo %FRONTEND_PID% > .frontend.pid

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

:check_python
call :print_status "Python kontrol ediliyor..."
python --version >nul 2>&1
if errorlevel 1 (
    python3 --version >nul 2>&1
    if errorlevel 1 (
        exit /b 1
    ) else (
        set "PYTHON_CMD=python3"
        for /f "tokens=2" %%i in ('python3 --version 2^>^&1') do set "PYTHON_VERSION=%%i"
        call :print_success "Python %PYTHON_VERSION% bulundu"
        exit /b 0
    )
) else (
    set "PYTHON_CMD=python"
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%i"
    call :print_success "Python %PYTHON_VERSION% bulundu"
    exit /b 0
)
goto :eof

:check_nodejs
call :print_status "Node.js kontrol ediliyor..."
node --version >nul 2>&1
if errorlevel 1 (
    exit /b 1
) else (
    for /f %%i in ('node --version 2^>^&1') do set "NODE_VERSION=%%i"
    call :print_success "Node.js %NODE_VERSION% bulundu"
    exit /b 0
)
goto :eof

:check_npm
call :print_status "npm kontrol ediliyor..."
npm --version >nul 2>&1
if errorlevel 1 (
    exit /b 1
) else (
    for /f %%i in ('npm --version 2^>^&1') do set "NPM_VERSION=%%i"
    call :print_success "npm %NPM_VERSION% bulundu"
    exit /b 0
)
goto :eof

:check_ytdlp
call :print_status "yt-dlp kontrol ediliyor..."
yt-dlp --version >nul 2>&1
if errorlevel 1 (
    call :print_warning "yt-dlp bulunamadı, yükleniyor..."
    %PYTHON_CMD% -m pip install yt-dlp
    if errorlevel 1 (
        call :print_error "yt-dlp yüklenemedi"
        exit /b 1
    )
    call :print_success "yt-dlp yüklendi"
) else (
    for /f %%i in ('yt-dlp --version 2^>^&1') do set "YTDLP_VERSION=%%i"
    call :print_success "yt-dlp %YTDLP_VERSION% bulundu"
)
goto :eof

:create_directories
call :print_status "Gerekli dizinler oluşturuluyor..."
if not exist "logs" mkdir logs
if not exist "backend\downloads" mkdir backend\downloads
call :print_success "Dizinler oluşturuldu"
goto :eof

:create_env_file
call :print_status "Environment dosyası oluşturuluyor..."
if not exist ".env" (
    if exist "env.example" (
        copy "env.example" ".env" >nul
        call :print_success "Environment dosyası oluşturuldu"
    ) else (
        call :print_warning "env.example bulunamadı, varsayılan .env oluşturuluyor..."
        echo # yt-dlp Web UI Environment Configuration > .env
        echo BACKEND_HOST=localhost >> .env
        echo BACKEND_PORT=8000 >> .env
        echo FRONTEND_PORT=3000 >> .env
        echo DOWNLOAD_PATH=./downloads >> .env
        echo MAX_FILE_SIZE=1073741824 >> .env
        call :print_success "Varsayılan environment dosyası oluşturuldu"
    )
) else (
    call :print_status "Environment dosyası zaten mevcut"
)
goto :eof

:setup_backend
call :print_status "Backend kurulumu başlatılıyor..."

cd backend

:: Virtual environment oluştur
if not exist "venv" (
    call :print_status "Python virtual environment oluşturuluyor..."
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        call :print_error "Virtual environment oluşturulamadı"
        cd ..
        exit /b 1
    )
)

:: Virtual environment'ı aktifleştir
call :print_status "Virtual environment aktifleştiriliyor..."
call venv\Scripts\activate.bat

:: Dependencies yükle
call :print_status "Python dependencies yükleniyor..."
pip install -r requirements.txt
if errorlevel 1 (
    call :print_error "Dependencies yüklenemedi"
    cd ..
    exit /b 1
)

call :print_success "Backend kurulumu tamamlandı"
cd ..
goto :eof

:setup_frontend
call :print_status "Frontend kurulumu başlatılıyor..."

cd frontend

:: Dependencies yükle
call :print_status "Node.js dependencies yükleniyor..."
npm install
if errorlevel 1 (
    call :print_error "Frontend dependencies yüklenemedi"
    cd ..
    exit /b 1
)

call :print_success "Frontend kurulumu tamamlandı"
cd ..
goto :eof

:start_services
call :print_status "Servisler başlatılıyor..."

:: Mevcut processleri sonlandır
taskkill /f /im python.exe 2>nul
taskkill /f /im node.exe 2>nul

:: Backend'i başlat
call :print_status "Backend server başlatılıyor..."
cd backend
call venv\Scripts\activate.bat
start /b python -m src.main > ..\logs\backend.log 2>&1
cd ..

:: Backend'in başlamasını bekle
call :print_status "Backend'in başlaması bekleniyor..."
timeout /t 5 /nobreak >nul

:: Backend kontrolü
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    call :print_warning "Backend henüz hazır değil, biraz daha bekleniyor..."
    timeout /t 5 /nobreak >nul
    curl -s http://localhost:8000/health >nul 2>&1
    if errorlevel 1 (
        call :print_error "Backend başlatılamadı"
        exit /b 1
    )
)
call :print_success "Backend başarıyla başlatıldı: http://localhost:8000"

:: Frontend'i başlat
call :print_status "Frontend server başlatılıyor..."
cd frontend
start /b npm run dev > ..\logs\frontend.log 2>&1
cd ..

:: Frontend'in başlamasını bekle
call :print_status "Frontend'in başlaması bekleniyor..."
timeout /t 10 /nobreak >nul

:: Frontend kontrolü
curl -s http://localhost:3000 >nul 2>&1
if errorlevel 1 (
    call :print_warning "Frontend farklı bir portta başlamış olabilir, logları kontrol edin"
) else (
    call :print_success "Frontend başarıyla başlatıldı: http://localhost:3000"
)

:: Process ID'lerini al
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq python.exe" /fo csv ^| find "python.exe"') do set "BACKEND_PID=%%i"
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq node.exe" /fo csv ^| find "node.exe"') do set "FRONTEND_PID=%%i"

goto :eof
