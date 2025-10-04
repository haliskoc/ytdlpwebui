# 🎬 yt-dlp Web UI - Windows Kurulum Rehberi

> **Windows kullanıcıları için özel kurulum rehberi**

## 🚀 Hızlı Başlangıç (Windows)

### 📋 Gereksinimler

Windows sisteminizde aşağıdaki yazılımların yüklü olması gerekiyor:

- **Python 3.8+** - [İndir](https://www.python.org/downloads/)
- **Node.js 16+** - [İndir](https://nodejs.org/)
- **Git** (opsiyonel) - [İndir](https://git-scm.com/download/win)

### ⚡ Tek Komutla Kurulum

1. **Projeyi indirin** (ZIP olarak veya Git ile)
2. **Klasöre gidin** ve `setup-windows.bat` dosyasını çift tıklayın
3. **Kurulum tamamlanana kadar bekleyin**
4. **Tarayıcınız otomatik açılacak** - `http://localhost:3000`

**Bu kadar!** 🎉 Uygulama kullanıma hazır.

## 📱 Kullanım

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
```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m src.main
```

### Frontend Kurulumu
```cmd
cd frontend
npm install
npm run dev
```

## 🎯 Özellikler

### 🚀 **Akıllı Kurulum**
- **Otomatik bağımlılık kontrolü**: Eksik paketleri tespit eder
- **Virtual environment**: Python paketlerini izole eder
- **Node.js yönetimi**: Frontend bağımlılıklarını yükler
- **yt-dlp güncelleme**: En son sürümü otomatik yükler

### 🎨 **Modern Arayüz**
- **Responsive tasarım**: Tüm cihazlarda mükemmel görünüm
- **Koyu/Açık mod**: Kullanıcı tercihi
- **İlerleme göstergeleri**: Görsel ilerleme çubukları
- **Hata yönetimi**: Kullanıcı dostu hata mesajları

### ⚡ **Performans**
- **Async işlemler**: Engellenmeyen işlemler
- **Bellek verimli**: Düşük RAM kullanımı
- **Hızlı başlatma**: Hızlı başlatma süresi
- **Otomatik temizlik**: Otomatik dosya temizliği

### 🔒 **Güvenlik**
- **Girdi doğrulama**: Tüm girdiler doğrulanır
- **Dosya sanitizasyonu**: Güvenli dosya isimleri
- **CORS koruması**: Cross-origin koruması
- **Rate limiting**: API istek sınırlaması

## 🛑 Servisleri Durdurma

### Otomatik Durdurma
- **3 dakika hareketsizlik** sonrası otomatik kapanır
- **Web arayüzü kullanımı** aktivite olarak sayılır

### Manuel Durdurma
```cmd
stop-windows.bat
```

## 📊 API Endpoints

| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/api/metadata` | POST | Video metadata al |
| `/api/download` | POST | İndirmeyi başlat |
| `/api/status/{job_id}` | GET | İndirme durumu |
| `/api/progress/{job_id}` | GET | Gerçek zamanlı ilerleme |
| `/api/download/{job_id}` | GET | Dosyayı indir |
| `/api/health` | GET | Sistem durumu |

## 🔧 Sorun Giderme

### Python Bulunamadı Hatası
```
[ERROR] Python 3.8+ gerekli ama yüklü değil
```
**Çözüm**: Python'u [python.org](https://www.python.org/downloads/) adresinden indirin ve yükleyin.

### Node.js Bulunamadı Hatası
```
[ERROR] Node.js 16+ gerekli ama yüklü değil
```
**Çözüm**: Node.js'i [nodejs.org](https://nodejs.org/) adresinden indirin ve yükleyin.

### Port Kullanımda Hatası
```
[ERROR] Port 8000/3000 kullanımda
```
**Çözüm**: 
1. `stop-windows.bat` çalıştırın
2. Veya Task Manager'dan python.exe ve node.exe processlerini sonlandırın

### Dependencies Yüklenemedi
```
[ERROR] Dependencies yüklenemedi
```
**Çözüm**:
1. İnternet bağlantınızı kontrol edin
2. Antivirus yazılımınızı geçici olarak devre dışı bırakın
3. Yönetici olarak çalıştırmayı deneyin

### Tarayıcı Açılmadı
**Çözüm**: Manuel olarak `http://localhost:3000` adresini açın.

## 📝 Log Dosyaları

Kurulum ve çalışma sırasında oluşan loglar:

- **Backend Log**: `logs\backend.log`
- **Frontend Log**: `logs\frontend.log`

Log dosyalarını kontrol ederek sorunları tespit edebilirsiniz.

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
├── setup-windows.bat       # Windows kurulum scripti
├── stop-windows.bat        # Windows durdurma scripti
└── logs/                   # Log dosyaları
```

### Geliştirme Ortamı

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

### 💡 **Özellik İsteği**
- **Kullanım durumunu** açıklayın
- **Mockup** ekleyin
- **Alternatif çözümleri** düşünün

## 📄 Lisans

Bu proje [MIT License](LICENSE) altında lisanslanmıştır.

## 🙏 Teşekkürler

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - Harika video indirme aracı
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[React](https://reactjs.org/)** - Kullanıcı arayüzü kütüphanesi
- **[Vite](https://vitejs.dev/)** - Hızlı build aracı

## 📞 İletişim

- **GitHub**: [@haliskoc](https://github.com/haliskoc)
- **Issues**: [GitHub Issues](https://github.com/haliskoc/ytdlpwebui/issues)
- **Discussions**: [GitHub Discussions](https://github.com/haliskoc/ytdlpwebui/discussions)

---

<div align="center">

**⭐ Bu projeyi beğendiyseniz, yıldız vermeyi unutmayın! ⭐**

[haliskoc](https://github.com/haliskoc) tarafından ❤️ ile yapılmıştır

</div>
