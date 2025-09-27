# 🎬 yt-dlp Web UI

> **Modern, fast and user-friendly YouTube video downloader web interface**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 16+](https://img.shields.io/badge/node.js-16+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-red.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org/)

## 📸 Screenshot

<div align="center">
  <img src="https://raw.githubusercontent.com/haliskoc/ytdlpwebui/main/frontend/public/screenshot.png" alt="yt-dlp Web UI Screenshot" width="600" style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
  <p><em>Clean and modern web interface for downloading YouTube videos</em></p>
</div>

## ✨ Features

### 🚀 **One-Click Setup**
- **Automatic installation**: Run with single command `./setup.sh`
- **Smart dependency management**: Python and Node.js packages auto-installed
- **Cross-platform**: Linux, macOS support
- **Docker support**: Run in container with `./docker-setup.sh`

### 🎯 **Modern Web Interface**
- **Responsive design**: Mobile and desktop compatible
- **Real-time progress**: Live download status tracking
- **Format selection**: Video, audio, quality options
- **Advanced settings**: Custom yt-dlp parameters
- **Log viewing**: Detailed process logs

### ⚡ **Performance & Security**
- **Auto-shutdown**: Closes itself after 3 minutes of inactivity
- **Secure downloads**: Sanitized file names
- **Error handling**: Comprehensive error catching and reporting
- **CORS protection**: Localhost access only
- **Rate limiting**: Protects system resources

### 🔧 **Technical Features**
- **FastAPI backend**: High-performance API
- **React frontend**: Modern, fast user interface
- **Server-Sent Events**: Real-time updates
- **Async/await**: Non-blocking operations
- **Type safety**: Data validation with Pydantic models

## 🚀 Quick Start

### 📋 Requirements
- **Python 3.8+**
- **Node.js 16+**
- **yt-dlp** (auto-installed)

### ⚡ One-Command Installation

```bash
# Clone repository
git clone https://github.com/haliskoc/ytdlpwebui.git
cd ytdlpwebui

# One command setup and run
chmod +x setup.sh
./setup.sh
```

**That's it!** 🎉 Your browser will open automatically and you'll see the app at `http://localhost:3000`.

> **💡 Tip**: The interface will look exactly like the screenshot above - clean, modern, and easy to use!

### 🐳 Run with Docker

```bash
# Run with Docker in one command
chmod +x docker-setup.sh
./docker-setup.sh
```

## 📱 Usage

### 🎬 Video Downloading
1. **Enter URL**: Paste YouTube video link
2. **Select format**: Video, audio or custom format
3. **Download**: Start download with one click
4. **Track progress**: Monitor status with real-time progress

### ⚙️ Advanced Settings
- **Quality selection**: 4K, 1080p, 720p, 480p
- **Audio formats**: MP3, AAC, OGG, FLAC
- **Subtitle support**: Automatic subtitle download
- **Custom parameters**: yt-dlp options

## 🛠️ Developer Guide

### 📁 Project Structure
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
├── scripts/                # Helper scripts
└── docs/                   # Documentation
```

### 🔧 Development Environment

```bash
# Backend development
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m src.main

# Frontend development
cd frontend
npm install
npm run dev

# Run tests
cd backend && python -m pytest
cd frontend && npm test
```

### 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/metadata` | POST | Get video metadata |
| `/api/download` | POST | Start download |
| `/api/status/{job_id}` | GET | Download status |
| `/api/progress/{job_id}` | GET | Real-time progress |
| `/api/download/{job_id}` | GET | Download file |
| `/api/health` | GET | System status |

## 🎯 Feature Details

### 🚀 **Smart Setup**
- **Automatic dependency check**: Detects missing packages
- **Virtual environment**: Isolates Python packages
- **Node.js management**: Installs frontend dependencies
- **yt-dlp update**: Auto-installs latest version

### 🎨 **Modern Interface**
- **Responsive design**: Perfect appearance on all devices
- **Dark/Light mode**: User preference
- **Progress indicators**: Visual progress bars
- **Error handling**: User-friendly error messages

### ⚡ **Performance**
- **Async operations**: Non-blocking operations
- **Memory efficient**: Low RAM usage
- **Fast startup**: Quick startup time
- **Auto-cleanup**: Automatic file cleanup

### 🔒 **Security**
- **Input validation**: All inputs validated
- **File sanitization**: Secure file names
- **CORS protection**: Cross-origin protection
- **Rate limiting**: API request limiting

## 📈 Roadmap

### 🎯 **Near Future**
- [ ] **User authentication**: Login/logout system
- [ ] **Playlist support**: Bulk video download
- [ ] **Scheduled downloads**: Timed downloads
- [ ] **Cloud storage**: Google Drive, Dropbox integration

### 🚀 **Long Term**
- [ ] **Mobile app**: React Native application
- [ ] **Browser extension**: Chrome/Firefox extension
- [ ] **API rate limiting**: Advanced limiting
- [ ] **Multi-language**: Multi-language support

## 🤝 Contributing

### 📝 **How to Contribute**
1. **Fork** the repository
2. **Create feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open Pull Request**

### 🐛 **Bug Reports**
- Use **GitHub Issues**
- Write **detailed description**
- Add **screenshots**
- Share **log files**

### 💡 **Feature Requests**
- Explain **use case**
- Add **mockup**
- Consider **alternative solutions**

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - Amazing video downloader tool
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[React](https://reactjs.org/)** - User interface library
- **[Vite](https://vitejs.dev/)** - Fast build tool

## 📞 Contact

- **GitHub**: [@haliskoc](https://github.com/haliskoc)
- **Issues**: [GitHub Issues](https://github.com/haliskoc/ytdlpwebui/issues)
- **Discussions**: [GitHub Discussions](https://github.com/haliskoc/ytdlpwebui/discussions)

---

<div align="center">

**⭐ If you like this project, don't forget to give it a star! ⭐**

Made with ❤️ by [haliskoc](https://github.com/haliskoc)

</div>