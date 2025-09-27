#!/bin/bash

# yt-dlp Web UI - Stop Script
# This script stops all running services

echo "🛑 Stopping yt-dlp Web UI..."

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

# Stop backend
if [ -f ".backend.pid" ]; then
    BACKEND_PID=$(cat .backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        print_status "Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        print_success "Backend stopped"
    else
        print_status "Backend process not found"
    fi
    rm -f .backend.pid
else
    print_status "No backend PID file found, killing any running backend processes..."
    pkill -f "python -m src.main" 2>/dev/null || true
fi

# Stop frontend
if [ -f ".frontend.pid" ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        print_status "Stopping frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        print_success "Frontend stopped"
    else
        print_status "Frontend process not found"
    fi
    rm -f .frontend.pid
else
    print_status "No frontend PID file found, killing any running frontend processes..."
    pkill -f "npm run dev" 2>/dev/null || true
fi

# Stop idle monitor
if [ -f ".idle-monitor.pid" ]; then
    IDLE_MONITOR_PID=$(cat .idle-monitor.pid)
    if kill -0 $IDLE_MONITOR_PID 2>/dev/null; then
        print_status "Stopping idle monitor (PID: $IDLE_MONITOR_PID)..."
        kill $IDLE_MONITOR_PID
        print_success "Idle monitor stopped"
    else
        print_status "Idle monitor process not found"
    fi
    rm -f .idle-monitor.pid
else
    print_status "No idle monitor PID file found, killing any running idle monitor processes..."
    pkill -f "idle-monitor.sh" 2>/dev/null || true
fi

# Kill any remaining processes
print_status "Cleaning up any remaining processes..."
pkill -f "vite" 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true

print_success "🎉 All services stopped successfully!"

