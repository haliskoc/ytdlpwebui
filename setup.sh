#!/bin/bash

# yt-dlp Web UI - One-Click Setup Script
# This script sets up and runs the application with a single command

set -e  # Exit on any error

echo "🚀 yt-dlp Web UI - One-Click Setup"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if running on supported OS
check_os() {
    print_status "Checking operating system..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_success "Linux detected"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        print_success "macOS detected"
    else
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION found"
    else
        print_error "Python 3 is required but not installed"
        print_status "Please install Python 3 and try again"
        exit 1
    fi
    
    # Check Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_success "Node.js $NODE_VERSION found"
    else
        print_error "Node.js is required but not installed"
        print_status "Please install Node.js and try again"
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
    
    # Check yt-dlp
    if command -v yt-dlp &> /dev/null; then
        YTDLP_VERSION=$(yt-dlp --version)
        print_success "yt-dlp $YTDLP_VERSION found"
    else
        print_warning "yt-dlp not found, installing..."
        pip3 install yt-dlp
        print_success "yt-dlp installed"
    fi
}

# Setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    cd backend
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    print_success "Backend setup complete"
    cd ..
}

# Setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    cd frontend
    
    # Install dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    print_success "Frontend setup complete"
    cd ..
}

# Create environment file
create_env() {
    print_status "Creating environment configuration..."
    
    if [ ! -f ".env" ]; then
        cp env.example .env
        print_success "Environment file created"
    else
        print_status "Environment file already exists"
    fi
}

# Start services
start_services() {
    print_status "Starting services..."
    
    # Kill any existing processes
    pkill -f "python -m src.main" 2>/dev/null || true
    pkill -f "npm run dev" 2>/dev/null || true
    
    # Start backend in background
    print_status "Starting backend server..."
    cd backend
    source venv/bin/activate
    nohup python -m src.main > ../logs/backend.log 2>&1 &
    BACKEND_PID=$!
    cd ..
    
    # Wait for backend to start
    print_status "Waiting for backend to start..."
    sleep 5
    
    # Check if backend is running
    if curl -s http://localhost:8000/health > /dev/null; then
        print_success "Backend started successfully on http://localhost:8000"
    else
        print_error "Backend failed to start"
        exit 1
    fi
    
    # Start frontend in background
    print_status "Starting frontend server..."
    cd frontend
    nohup npm run dev > ../logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..
    
    # Wait for frontend to start
    print_status "Waiting for frontend to start..."
    sleep 10
    
    # Check if frontend is running
    if curl -s http://localhost:3000 > /dev/null; then
        print_success "Frontend started successfully on http://localhost:3000"
    else
        print_warning "Frontend might be starting on a different port, check logs"
    fi
    
    # Save PIDs for cleanup
    echo $BACKEND_PID > .backend.pid
    echo $FRONTEND_PID > .frontend.pid
    
    # Start idle monitor
    print_status "Starting idle monitor (3-minute timeout)..."
    nohup ./idle-monitor.sh start > logs/idle-monitor.log 2>&1 &
    IDLE_MONITOR_PID=$!
    echo $IDLE_MONITOR_PID > .idle-monitor.pid
}

# Create logs directory
create_logs_dir() {
    mkdir -p logs
}

# Install desktop entry
install_desktop_entry() {
    print_status "Installing desktop entry..."
    
    # Make desktop file executable
    chmod +x ytdlp-webui.desktop
    
    # Copy to applications directory
    if [ -d "$HOME/.local/share/applications" ]; then
        cp ytdlp-webui.desktop "$HOME/.local/share/applications/"
        print_success "Desktop entry installed - App will appear in applications menu"
    else
        print_warning "Could not install desktop entry - applications directory not found"
    fi
    
    # Update desktop database
    if command -v update-desktop-database &> /dev/null; then
        update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
    fi
}

# Main execution
main() {
    print_status "Starting yt-dlp Web UI setup..."
    
    check_os
    check_prerequisites
    create_logs_dir
    create_env
    setup_backend
    setup_frontend
    install_desktop_entry
    start_services
    
    echo ""
    print_success "🎉 yt-dlp Web UI is now running!"
    echo ""
    echo -e "${GREEN}📱 Frontend:${NC} http://localhost:3000"
    echo -e "${GREEN}🔧 Backend:${NC}  http://localhost:8000"
    echo -e "${GREEN}📊 Health:${NC}   http://localhost:8000/health"
    echo ""
    echo -e "${YELLOW}📝 Logs:${NC}"
    echo -e "   Backend:  tail -f logs/backend.log"
    echo -e "   Frontend: tail -f logs/frontend.log"
    echo ""
    echo -e "${YELLOW}🛑 To stop:${NC} ./stop.sh"
    echo ""
    echo -e "${BLUE}🎯 App installed in applications menu!${NC}"
    echo -e "${BLUE}   You can now launch it from your app launcher${NC}"
    echo ""
    echo -e "${YELLOW}⏰ Auto-shutdown:${NC} Services will automatically stop after 3 minutes of inactivity"
    echo -e "${YELLOW}   Activity is tracked when you use the web interface${NC}"
    echo ""
    echo -e "${BLUE}💡 Opening browser automatically...${NC}"
    
    # Wait a bit more for frontend to be fully ready
    sleep 3
    
    # Open browser automatically
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:3000 &
        print_success "Browser opened automatically"
    elif command -v firefox &> /dev/null; then
        firefox http://localhost:3000 &
        print_success "Firefox opened automatically"
    elif command -v google-chrome &> /dev/null; then
        google-chrome http://localhost:3000 &
        print_success "Chrome opened automatically"
    elif command -v chromium-browser &> /dev/null; then
        chromium-browser http://localhost:3000 &
        print_success "Chromium opened automatically"
    else
        print_warning "Could not detect browser, please open manually: http://localhost:3000"
    fi
}

# Run main function
main "$@"

