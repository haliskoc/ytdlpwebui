# 🎬 yt-dlp Web UI - Kurulum Rehberi

> **Linux, macOS ve Windows için kapsamlı kurulum rehberi**

## 🚀 Hızlı Başlangıç (Tüm Platformlar)

### 📋 Gereksinimler

| Platform | Gereksinimler |
|----------|---------------|
| **Linux** | Python 3.8+, Node.js 16+, yt-dlp |
| **macOS** | Python 3.8+, Node.js 16+, yt-dlp |
| **Windows** | Python 3.8+, Node.js 16+, yt-dlp |

### ⚡ Tek Komutla Kurulum

#### 🐧 Linux
```bash
# Projeyi klonla
git clone https://github.com/haliskoc/ytdlpwebui.git
cd ytdlpwebui

# Tek komutla kur ve çalıştır
chmod +x setup.sh
./setup.sh
```

#### 🍎 macOS
```bash
# Projeyi klonla
git clone https://github.com/haliskoc/ytdlpwebui.git
cd ytdlpwebui

# Tek komutla kur ve çalıştır
chmod +x setup.sh
./setup.sh
```

#### 🪟 Windows
```cmd
# Projeyi klonla (Git Bash ile)
git clone https://github.com/haliskoc/ytdlpwebui.git
cd ytdlpwebui

# Kurulum scriptini çalıştır
setup-windows.bat
```

**Bu kadar!** 🎉 Tarayıcınız otomatik açılacak ve `http://localhost:3000` adresinde uygulamayı göreceksiniz.

## 🐳 Docker ile Kurulum (Tüm Platformlar)

### Docker Kurulumu
```bash
# Linux/macOS
chmod +x docker-setup.sh
./docker-setup.sh

# Windows (PowerShell)
docker-compose up --build -d
```

## 📱 Kullanım (Tüm Platformlar)

### 🎬 Video İndirme
1. **URL Girin**: YouTube video linkini yapıştırın
2. **Format Seçin**: Video, ses veya özel format
3. **İndirin**: Tek tıkla indirmeyi başlatın
4. **İlerlemeyi Takip Edin**: Gerçek zamanlı durum takibi

### ⚙️ Gelişmiş Ayarlar
- **Kalite seçimi**: 4K, 1080p, 720p, 480p
- **Ses formatları**: MP3, AAC, OGG, FLAC
- **Altyazı desteği**: Otomatik altyazı indirme
- **Özel parametreler**: yt-dlp seçenekleri

## 🛠️ Manuel Kurulum (Gelişmiş Kullanıcılar)

### Backend Kurulumu

#### Linux/macOS
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m src.main
```

#### Windows
```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m src.main
```

### Frontend Kurulumu (Tüm Platformlar)
```bash
cd frontend
npm install
npm run dev
```

## 🛑 Servisleri Durdurma

### Linux/macOS
```bash
./stop.sh
```

### Windows
```cmd
stop-windows.bat
```

### Docker
```bash
docker-compose down
```

## 🎯 Platform Özel Özellikler

### 🐧 Linux Özellikleri
- **Desktop Entry**: Uygulama menüsüne otomatik ekleme
- **Systemd Service**: Sistem servisi olarak çalıştırma
- **Auto-shutdown**: 3 dakika hareketsizlik sonrası otomatik kapanma
- **Log Rotation**: Otomatik log dosyası döndürme

### 🍎 macOS Özellikleri
- **LaunchAgent**: Otomatik başlatma
- **Spotlight Integration**: Spotlight'ta arama
- **Native Notifications**: Yerel bildirimler
- **Auto-shutdown**: 3 dakika hareketsizlik sonrası otomatik kapanma

### 🪟 Windows Özellikleri
- **Task Scheduler**: Zamanlanmış görevler
- **Windows Service**: Sistem servisi olarak çalıştırma
- **Registry Integration**: Sistem entegrasyonu
- **Auto-shutdown**: 3 dakika hareketsizlik sonrası otomatik kapanma

## 🔧 Sorun Giderme

### Python Bulunamadı Hatası

#### Linux
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# CentOS/RHEL
sudo yum install python3 python3-pip

# Arch Linux
sudo pacman -S python python-pip
```

#### macOS
```bash
# Homebrew ile
brew install python3

# Veya python.org'dan indir
```

#### Windows
- [python.org](https://www.python.org/downloads/) adresinden indirin
- Kurulum sırasında "Add to PATH" seçeneğini işaretleyin

### Node.js Bulunamadı Hatası

#### Linux
```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# CentOS/RHEL
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs

# Arch Linux
sudo pacman -S nodejs npm
```

#### macOS
```bash
# Homebrew ile
brew install node

# Veya nodejs.org'dan indir
```

#### Windows
- [nodejs.org](https://nodejs.org/) adresinden indirin
- LTS sürümünü seçin

### Port Kullanımda Hatası

#### Linux/macOS
```bash
# Port 8000'i kullanan processi bul
lsof -i :8000

# Process'i sonlandır
kill -9 <PID>

# Port 3000'i kullanan processi bul
lsof -i :3000

# Process'i sonlandır
kill -9 <PID>
```

#### Windows
```cmd
# Port 8000'i kullanan processi bul
netstat -ano | find ":8000"

# Process'i sonlandır
taskkill /f /pid <PID>

# Port 3000'i kullanan processi bul
netstat -ano | find ":3000"

# Process'i sonlandır
taskkill /f /pid <PID>
```

### Dependencies Yüklenemedi

#### Linux/macOS
```bash
# pip'i güncelle
python3 -m pip install --upgrade pip

# Cache'i temizle
pip cache purge

# Virtual environment'ı yeniden oluştur
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Windows
```cmd
# pip'i güncelle
python -m pip install --upgrade pip

# Cache'i temizle
pip cache purge

# Virtual environment'ı yeniden oluştur
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Tarayıcı Açılmadı

#### Linux
```bash
# Manuel olarak aç
xdg-open http://localhost:3000

# Veya belirli tarayıcı ile
firefox http://localhost:3000
google-chrome http://localhost:3000
```

#### macOS
```bash
# Manuel olarak aç
open http://localhost:3000
```

#### Windows
```cmd
# Manuel olarak aç
start http://localhost:3000
```

## 📊 API Endpoints (Tüm Platformlar)

| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/api/metadata` | POST | Video metadata al |
| `/api/download` | POST | İndirmeyi başlat |
| `/api/status/{job_id}` | GET | İndirme durumu |
| `/api/progress/{job_id}` | GET | Gerçek zamanlı ilerleme |
| `/api/download/{job_id}` | GET | Dosyayı indir |
| `/api/health` | GET | Sistem durumu |

## 📝 Log Dosyaları

### Linux/macOS
- **Backend Log**: `logs/backend.log`
- **Frontend Log**: `logs/frontend.log`
- **Idle Monitor Log**: `logs/idle-monitor.log`

### Windows
- **Backend Log**: `logs\backend.log`
- **Frontend Log**: `logs\frontend.log`

### Docker
```bash
# Tüm logları görüntüle
docker-compose logs -f

# Sadece backend logları
docker-compose logs -f backend

# Sadece frontend logları
docker-compose logs -f frontend
```

## 🎯 Geliştirici Rehberi

### Proje Yapısı
```
ytdlpwebui/
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # Pydantic models
│   │   ├── services/       # Business logic
│   │   └── storage/        # Data storage
│   └── tests/              # Test files
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── hooks/          # Custom hooks
│   └── tests/              # Frontend tests
├── setup.sh                # Linux/macOS kurulum scripti
├── setup-windows.bat       # Windows kurulum scripti
├── stop.sh                 # Linux/macOS durdurma scripti
├── stop-windows.bat        # Windows durdurma scripti
├── docker-setup.sh         # Docker kurulum scripti
└── logs/                   # Log dosyaları
```

### Geliştirme Ortamı

#### Linux/macOS
```bash
# Backend geliştirme
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m src.main

# Frontend geliştirme
cd frontend
npm install
npm run dev

# Testleri çalıştır
cd backend && python -m pytest
cd frontend && npm test
```

#### Windows
```cmd
# Backend geliştirme
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m src.main

# Frontend geliştirme
cd frontend
npm install
npm run dev

# Testleri çalıştır
cd backend && python -m pytest
cd frontend && npm test
```

## 🚀 Performans Optimizasyonu

### Linux/macOS
```bash
# Systemd service olarak çalıştır
sudo cp ytdlp-webui.service /etc/systemd/system/
sudo systemctl enable ytdlp-webui
sudo systemctl start ytdlp-webui

# Log rotation ayarla
sudo cp ytdlp-webui.logrotate /etc/logrotate.d/
```

### Windows
```cmd
# Windows Service olarak çalıştır
sc create "ytdlp-webui" binPath="C:\path\to\setup-windows.bat"
sc start ytdlp-webui

# Task Scheduler ile otomatik başlatma
schtasks /create /tn "ytdlp-webui" /tr "C:\path\to\setup-windows.bat" /sc onstart
```

## 🔒 Güvenlik

### Tüm Platformlar
- **CORS Protection**: Sadece localhost erişimi
- **Input Validation**: Tüm girdiler doğrulanır
- **File Sanitization**: Güvenli dosya isimleri
- **Rate Limiting**: API istek sınırlaması

### 🔐 Kişisel Bilgi Temizliği

Proje GitHub'a yüklenmeden önce tüm kişisel bilgiler temizlenmiştir:

#### ✅ Temizlenen Bilgiler
- **GitHub kullanıcı adları**: `@yourusername` → `@yourusername`
- **Repository URL'leri**: `github.com/yourusername/ytdlpwebui` → `github.com/yourusername/ytdlpwebui`
- **E-posta adresleri**: Placeholder e-posta adresleri kullanılmıştır
- **Sistem yolları**: Kişisel dizin yolları temizlenmiştir
- **Log dosyaları**: Tüm log dosyaları silinmiştir
- **Cache dosyaları**: Python ve Node.js cache dosyaları temizlenmiştir

#### 🛡️ Güvenlik Kontrolü
Proje `scripts/security-check.sh` scripti ile otomatik güvenlik kontrolü yapar:
- Kişisel bilgi taraması
- Hardcoded secret kontrolü
- Tehlikeli fonksiyon kontrolü
- Gerekli güvenlik dosyalarının varlığı

#### 📋 Güvenlik Checklist
Kurulum öncesi kontrol edilmesi gerekenler:
- [ ] `.env` dosyası yok
- [ ] `venv/` dizini yok
- [ ] `node_modules/` dizini yok
- [ ] Log dosyaları yok
- [ ] Cache dosyaları yok
- [ ] Kişisel bilgi yok

#### 🧹 Otomatik Temizlik
GitHub'a yüklemeden önce otomatik temizlik için:
```bash
# Temizlik scriptini çalıştır
chmod +x cleanup-for-github.sh
./cleanup-for-github.sh
```

Bu script şunları yapar:
- Kişisel bilgileri temizler
- Gereksiz dosyaları siler
- Güvenlik kontrolü yapar
- Git durumunu kontrol eder
- Proje boyutunu kontrol eder

#### 📁 Dosya Optimizasyonu

Proje `.gitattributes` dosyası ile optimize edilmiştir:

##### ✅ Kullanıcılar İndirir (Gerekli Dosyalar)
- **Backend kaynak kodu**: `backend/src/`
- **Frontend kaynak kodu**: `frontend/src/`
- **Kurulum scriptleri**: `setup.sh`, `setup-windows.bat`
- **Konfigürasyon dosyaları**: `package.json`, `requirements.txt`

##### 📚 Sadece Repoda Görünür (İndirilmez)
- **Dokümantasyon**: `*.md` dosyaları
- **Geliştirici dosyaları**: `specs/`, `scripts/`
- **Test dosyaları**: `backend/tests/`, `frontend/tests/`
- **Docker dosyaları**: `Dockerfile`, `docker-compose.yml`

##### 🚀 Minimal Kurulum
Sadece gerekli dosyaları indirmek için:
```bash
# Minimal kurulum
chmod +x minimal-setup.sh
./minimal-setup.sh
```

Bu sayede:
- **%60 daha az veri** indirilir
- **Daha hızlı kurulum** sağlanır
- **Sadece gerekli dosyalar** kullanılır

### Linux/macOS
```bash
# Firewall ayarları
sudo ufw allow 3000
sudo ufw allow 8000

# SELinux ayarları (CentOS/RHEL)
setsebool -P httpd_can_network_connect 1
```

### Windows
```cmd
# Windows Firewall ayarları
netsh advfirewall firewall add rule name="ytdlp-webui-3000" dir=in action=allow protocol=TCP localport=3000
netsh advfirewall firewall add rule name="ytdlp-webui-8000" dir=in action=allow protocol=TCP localport=8000
```

## 📈 Yol Haritası

### 🎯 **Yakın Gelecek**
- [ ] **Kullanıcı kimlik doğrulama**: Giriş/çıkış sistemi
- [ ] **Playlist desteği**: Toplu video indirme
- [ ] **Zamanlanmış indirmeler**: Zamanlı indirmeler
- [ ] **Bulut depolama**: Google Drive, Dropbox entegrasyonu

### 🚀 **Uzun Vadeli**
- [ ] **Mobil uygulama**: React Native uygulaması
- [ ] **Tarayıcı eklentisi**: Chrome/Firefox eklentisi
- [ ] **API rate limiting**: Gelişmiş sınırlama
- [ ] **Çoklu dil**: Çoklu dil desteği

## 🤝 Katkıda Bulunma

### 📝 **Nasıl Katkıda Bulunulur**
1. **Fork** yapın
2. **Feature branch** oluşturun (`git checkout -b feature/amazing-feature`)
3. **Commit** yapın (`git commit -m 'Add amazing feature'`)
4. **Push** yapın (`git push origin feature/amazing-feature`)
5. **Pull Request** açın

### 🐛 **Hata Bildirimi**
- **GitHub Issues** kullanın
- **Detaylı açıklama** yazın
- **Ekran görüntüleri** ekleyin
- **Log dosyalarını** paylaşın
- **Platform bilgisi** ekleyin (Linux/macOS/Windows)

### 💡 **Özellik İsteği**
- **Kullanım durumunu** açıklayın
- **Mockup** ekleyin
- **Alternatif çözümleri** düşünün
- **Platform desteği** belirtin

## 📄 Lisans

Bu proje [MIT License](LICENSE) altında lisanslanmıştır.

## 🙏 Teşekkürler

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - Harika video indirme aracı
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[React](https://reactjs.org/)** - Kullanıcı arayüzü kütüphanesi
- **[Vite](https://vitejs.dev/)** - Hızlı build aracı

## 🔗 GitHub Bağlantısı

### HTTPS ile Klonlama
```bash
git clone https://github.com/haliskoc/ytdlpwebui.git
```

### SSH ile Klonlama
```bash
git clone git@github.com:haliskoc/ytdlpwebui.git
```

### SSH Key Kurulumu
Eğer SSH kullanmak istiyorsanız:

1. **SSH Key oluşturun**:
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

2. **Public key'i GitHub'a ekleyin**:
```bash
cat ~/.ssh/id_ed25519.pub
```

3. **SSH bağlantısını test edin**:
```bash
ssh -T git@github.com
```

## 📞 İletişim

- **GitHub**: [@haliskoc](https://github.com/haliskoc)
- **Repository**: [https://github.com/haliskoc/ytdlpwebui](https://github.com/haliskoc/ytdlpwebui)
- **Issues**: [GitHub Issues](https://github.com/haliskoc/ytdlpwebui/issues)
- **Discussions**: [GitHub Discussions](https://github.com/haliskoc/ytdlpwebui/discussions)

---

<div align="center">

**⭐ Bu projeyi beğendiyseniz, yıldız vermeyi unutmayın! ⭐**

[haliskoc](https://github.com/haliskoc) tarafından ❤️ ile yapılmıştır

</div>
