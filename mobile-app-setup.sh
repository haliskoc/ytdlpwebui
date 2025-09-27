#!/bin/bash

# yt-dlp Web UI - Mobile App Setup Script
# Creates native Android/iOS apps using Capacitor

echo "📱 yt-dlp Web UI - Mobile App Setup"
echo "==================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_success "Node.js $NODE_VERSION found"
    else
        print_error "Node.js is required but not installed"
        exit 1
    fi
    
    # Check npm
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        print_success "npm $NPM_VERSION found"
    else
        print_error "npm is required but not installed"
        exit 1
    fi
}

# Install Capacitor
install_capacitor() {
    print_status "Installing Capacitor..."
    
    # Install Capacitor CLI globally
    npm install -g @capacitor/cli
    
    # Install Capacitor core and Android
    cd frontend
    npm install @capacitor/core @capacitor/android
    
    print_success "Capacitor installed"
}

# Initialize Capacitor
init_capacitor() {
    print_status "Initializing Capacitor..."
    
    cd frontend
    
    # Initialize Capacitor if not already done
    if [ ! -f "capacitor.config.ts" ]; then
        npx cap init "yt-dlp Web UI" "com.ytdlp.webui" --web-dir=dist
    fi
    
    # Add Android platform
    npx cap add android
    
    print_success "Capacitor initialized"
}

# Build frontend
build_frontend() {
    print_status "Building frontend for mobile..."
    
    cd frontend
    
    # Install dependencies
    npm install
    
    # Build for production
    npm run build
    
    print_success "Frontend built"
}

# Configure for mobile
configure_mobile() {
    print_status "Configuring for mobile..."
    
    cd frontend
    
    # Create mobile-specific config
    cat > capacitor.config.ts << 'EOF'
import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.ytdlp.webui',
  appName: 'yt-dlp Web UI',
  webDir: 'dist',
  server: {
    androidScheme: 'https'
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 2000,
      backgroundColor: "#3b82f6",
      showSpinner: false
    },
    StatusBar: {
      style: 'dark'
    }
  }
};

export default config;
EOF

    print_success "Mobile configuration created"
}

# Add mobile plugins
add_plugins() {
    print_status "Adding mobile plugins..."
    
    cd frontend
    
    # Install useful plugins
    npm install @capacitor/status-bar @capacitor/splash-screen @capacitor/filesystem @capacitor/share @capacitor/toast
    
    # Sync plugins
    npx cap sync
    
    print_success "Mobile plugins added"
}

# Create mobile-specific components
create_mobile_components() {
    print_status "Creating mobile-specific components..."
    
    cd frontend/src
    
    # Create mobile service
    cat > services/mobile.js << 'EOF'
import { Capacitor } from '@capacitor/core';
import { Filesystem, Directory } from '@capacitor/filesystem';
import { Share } from '@capacitor/share';
import { Toast } from '@capacitor/toast';

export const mobileService = {
  isNative: () => Capacitor.isNativePlatform(),
  
  async downloadFile(url, filename) {
    if (this.isNative()) {
      // Native file download
      try {
        const response = await fetch(url);
        const blob = await response.blob();
        
        const base64 = await this.blobToBase64(blob);
        
        await Filesystem.writeFile({
          path: `Downloads/${filename}`,
          data: base64,
          directory: Directory.ExternalStorage
        });
        
        await Toast.show({
          text: `File saved: ${filename}`
        });
        
        return true;
      } catch (error) {
        console.error('Download error:', error);
        return false;
      }
    }
    return false;
  },
  
  async shareFile(filePath) {
    if (this.isNative()) {
      try {
        await Share.share({
          title: 'Downloaded File',
          text: 'Check out this file I downloaded!',
          url: filePath
        });
      } catch (error) {
        console.error('Share error:', error);
      }
    }
  },
  
  blobToBase64(blob) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result.split(',')[1]);
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  }
};
EOF

    print_success "Mobile components created"
}

# Build Android APK
build_android() {
    print_status "Building Android APK..."
    
    cd frontend
    
    # Sync with native
    npx cap sync android
    
    # Open Android Studio (if available)
    if command -v studio &> /dev/null; then
        print_status "Opening Android Studio..."
        npx cap open android
    else
        print_warning "Android Studio not found. Please install Android Studio and run:"
        print_warning "cd frontend && npx cap open android"
    fi
    
    print_success "Android project ready"
}

# Create build script
create_build_script() {
    print_status "Creating build script..."
    
    cat > ../build-mobile.sh << 'EOF'
#!/bin/bash

echo "📱 Building Mobile App..."

cd frontend

# Build web app
npm run build

# Sync with native
npx cap sync

# Open Android Studio
npx cap open android

echo "✅ Mobile app ready for building in Android Studio!"
EOF

    chmod +x ../build-mobile.sh
    
    print_success "Build script created"
}

# Main execution
main() {
    print_status "Starting mobile app setup..."
    
    check_prerequisites
    install_capacitor
    init_capacitor
    build_frontend
    configure_mobile
    add_plugins
    create_mobile_components
    build_android
    create_build_script
    
    echo ""
    print_success "🎉 Mobile app setup complete!"
    echo ""
    echo -e "${GREEN}📱 Next steps:${NC}"
    echo -e "   1. Install Android Studio"
    echo -e "   2. Run: ./build-mobile.sh"
    echo -e "   3. Build APK in Android Studio"
    echo ""
    echo -e "${YELLOW}📁 Files created:${NC}"
    echo -e "   - frontend/android/ (Android project)"
    echo -e "   - build-mobile.sh (Build script)"
    echo -e "   - Mobile-specific components"
    echo ""
    echo -e "${BLUE}🚀 To build APK:${NC}"
    echo -e "   ./build-mobile.sh"
}

# Run main function
main "$@"

