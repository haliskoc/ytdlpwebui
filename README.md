# 🎬 yt-dlp Web UI

> **Modern, hızlı ve kullanıcı dostu YouTube video indirici web arayüzü**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 16+](https://img.shields.io/badge/node.js-16+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-red.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org/)

## ✨ Özellikler

### 🚀 **Tek Tıkla Kurulum**
- **Otomatik kurulum**: `./setup.sh` ile tek komutla çalışır
- **Akıllı bağımlılık yönetimi**: Python ve Node.js paketleri otomatik kurulur
- **Cross-platform**: Linux, macOS desteği
- **Docker desteği**: `./docker-setup.sh` ile container'da çalıştır

### 🎯 **Modern Web Arayüzü**
- **Responsive tasarım**: Mobil ve desktop uyumlu
- **Real-time progress**: Canlı indirme durumu takibi
- **Format seçimi**: Video, audio, kalite seçenekleri
- **Gelişmiş ayarlar**: Özel yt-dlp parametreleri
- **Log görüntüleme**: Detaylı işlem logları

### ⚡ **Performans & Güvenlik**
- **Otomatik kapanma**: 3 dakika kullanılmadığında kendini kapatır
- **Güvenli indirme**: Sanitized dosya isimleri
- **Hata yönetimi**: Kapsamlı hata yakalama ve raporlama
- **CORS koruması**: Sadece localhost erişimi
- **Rate limiting**: Sistem kaynaklarını korur

### 🔧 **Teknik Özellikler**
- **FastAPI backend**: Yüksek performanslı API
- **React frontend**: Modern, hızlı kullanıcı arayüzü
- **Server-Sent Events**: Gerçek zamanlı güncellemeler
- **Async/await**: Non-blocking işlemler
- **Type safety**: Pydantic modelleri ile veri doğrulama

## 🚀 Hızlı Başlangıç

### 📋 Gereksinimler
- **Python 3.8+**
- **Node.js 16+**
- **yt-dlp** (otomatik kurulur)

### ⚡ Tek Komutla Kurulum

```bash
# Repository'yi klonla
git clone https://github.com/haliskoc/ytdlpwebui.git
cd ytdlpwebui

# Tek komutla kur ve çalıştır
chmod +x setup.sh
./setup.sh
```

**Bu kadar!** 🎉 Tarayıcınız otomatik açılacak ve `http://localhost:3000` adresinde uygulamayı göreceksiniz.

### 🐳 Docker ile Çalıştırma

```bash
# Docker ile tek komutla çalıştır
chmod +x docker-setup.sh
./docker-setup.sh
```

## 📱 Kullanım

### 🎬 Video İndirme
1. **URL girin**: YouTube video linkini yapıştırın
2. **Format seçin**: Video, audio veya özel format
3. **İndir**: Tek tıkla indirme başlatın
4. **Takip edin**: Real-time progress ile durumu izleyin

### ⚙️ Gelişmiş Ayarlar
- **Kalite seçimi**: 4K, 1080p, 720p, 480p
- **Audio formatları**: MP3, AAC, OGG, FLAC
- **Subtitle desteği**: Otomatik altyazı indirme
- **Özel parametreler**: yt-dlp seçenekleri

## 🛠️ Geliştirici Rehberi

### 📁 Proje Yapısı
```
ytdlpwebui/
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # Pydantic modelleri
│   │   ├── services/       # İş mantığı
│   │   └── storage/        # Veri depolama
│   └── tests/              # Test dosyaları
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # UI bileşenleri
│   │   ├── pages/          # Sayfa bileşenleri
│   │   ├── services/       # API servisleri
│   │   └── hooks/          # Custom hooks
│   └── tests/              # Frontend testleri
├── scripts/                # Yardımcı scriptler
└── docs/                   # Dokümantasyon
```

### 🔧 Geliştirme Ortamı

```bash
# Backend geliştirme
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m src.main

# Frontend geliştirme
cd frontend
npm install
npm run dev

# Test çalıştırma
cd backend && python -m pytest
cd frontend && npm test
```

### 📊 API Endpoints

| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/api/metadata` | POST | Video metadata al |
| `/api/download` | POST | İndirme başlat |
| `/api/status/{job_id}` | GET | İndirme durumu |
| `/api/progress/{job_id}` | GET | Real-time progress |
| `/api/download/{job_id}` | GET | Dosya indir |
| `/api/health` | GET | Sistem durumu |

## 🎯 Özellikler Detayı

### 🚀 **Akıllı Kurulum**
- **Otomatik bağımlılık kontrolü**: Eksik paketleri tespit eder
- **Virtual environment**: Python paketlerini izole eder
- **Node.js yönetimi**: Frontend bağımlılıklarını kurar
- **yt-dlp güncelleme**: En son versiyonu otomatik kurar

### 🎨 **Modern Arayüz**
- **Responsive design**: Tüm cihazlarda mükemmel görünüm
- **Dark/Light mode**: Kullanıcı tercihi
- **Progress indicators**: Görsel ilerleme çubukları
- **Error handling**: Kullanıcı dostu hata mesajları

### ⚡ **Performans**
- **Async operations**: Non-blocking işlemler
- **Memory efficient**: Düşük RAM kullanımı
- **Fast startup**: Hızlı başlatma süresi
- **Auto-cleanup**: Otomatik dosya temizliği

### 🔒 **Güvenlik**
- **Input validation**: Tüm girdiler doğrulanır
- **File sanitization**: Güvenli dosya isimleri
- **CORS protection**: Cross-origin koruması
- **Rate limiting**: API istek sınırlaması

## 📈 Roadmap

### 🎯 **Yakın Gelecek**
- [ ] **Kullanıcı kimlik doğrulama**: Login/logout sistemi
- [ ] **Playlist desteği**: Toplu video indirme
- [ ] **Scheduled downloads**: Zamanlanmış indirmeler
- [ ] **Cloud storage**: Google Drive, Dropbox entegrasyonu

### 🚀 **Uzun Vadeli**
- [ ] **Mobile app**: React Native uygulaması
- [ ] **Browser extension**: Chrome/Firefox eklentisi
- [ ] **API rate limiting**: Gelişmiş sınırlama
- [ ] **Multi-language**: Çoklu dil desteği

## 🤝 Katkıda Bulunma

### 📝 **Nasıl Katkıda Bulunabilirsiniz**
1. **Fork** yapın
2. **Feature branch** oluşturun (`git checkout -b feature/amazing-feature`)
3. **Commit** yapın (`git commit -m 'Add amazing feature'`)
4. **Push** edin (`git push origin feature/amazing-feature`)
5. **Pull Request** açın

### 🐛 **Bug Raporlama**
- **GitHub Issues** kullanın
- **Detaylı açıklama** yazın
- **Screenshots** ekleyin
- **Log dosyalarını** paylaşın

### 💡 **Özellik İstekleri**
- **Use case** açıklayın
- **Mockup** ekleyin
- **Alternatif çözümler** düşünün

## 📄 Lisans

Bu proje [MIT License](LICENSE) altında lisanslanmıştır.

## 🙏 Teşekkürler

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - Harika video indirme aracı
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[React](https://reactjs.org/)** - Kullanıcı arayüzü kütüphanesi
- **[Vite](https://vitejs.dev/)** - Hızlı build tool

## 📞 İletişim

- **GitHub**: [@haliskoc](https://github.com/haliskoc)
- **Issues**: [GitHub Issues](https://github.com/haliskoc/ytdlpwebui/issues)
- **Discussions**: [GitHub Discussions](https://github.com/haliskoc/ytdlpwebui/discussions)

---

<div align="center">

**⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! ⭐**

Made with ❤️ by [haliskoc](https://github.com/haliskoc)

</div>