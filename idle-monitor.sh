#!/bin/bash

# yt-dlp Web UI - Idle Monitor Script
# Monitors activity and shuts down services after 3 minutes of inactivity

IDLE_TIMEOUT=180  # 3 minutes in seconds
LOG_FILE="logs/idle-monitor.log"
LAST_ACTIVITY_FILE=".last_activity"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[IDLE-MONITOR]${NC} $1" | tee -a "$LOG_FILE"
}

print_warning() {
    echo -e "${YELLOW}[IDLE-MONITOR]${NC} $1" | tee -a "$LOG_FILE"
}

print_success() {
    echo -e "${GREEN}[IDLE-MONITOR]${NC} $1" | tee -a "$LOG_FILE"
}

# Function to update last activity timestamp
update_activity() {
    echo $(date +%s) > "$LAST_ACTIVITY_FILE"
}

# Function to check if services are running
check_services() {
    local backend_running=false
    local frontend_running=false
    
    if [ -f ".backend.pid" ]; then
        local backend_pid=$(cat .backend.pid)
        if kill -0 "$backend_pid" 2>/dev/null; then
            backend_running=true
        fi
    fi
    
    if [ -f ".frontend.pid" ]; then
        local frontend_pid=$(cat .frontend.pid)
        if kill -0 "$frontend_pid" 2>/dev/null; then
            frontend_running=true
        fi
    fi
    
    if [ "$backend_running" = true ] || [ "$frontend_running" = true ]; then
        return 0  # Services are running
    else
        return 1  # Services are not running
    fi
}

# Function to shutdown services
shutdown_services() {
    print_warning "No activity detected for $IDLE_TIMEOUT seconds. Shutting down services..."
    
    # Stop backend
    if [ -f ".backend.pid" ]; then
        local backend_pid=$(cat .backend.pid)
        if kill -0 "$backend_pid" 2>/dev/null; then
            print_status "Stopping backend (PID: $backend_pid)..."
            kill "$backend_pid"
        fi
        rm -f .backend.pid
    fi
    
    # Stop frontend
    if [ -f ".frontend.pid" ]; then
        local frontend_pid=$(cat .frontend.pid)
        if kill -0 "$frontend_pid" 2>/dev/null; then
            print_status "Stopping frontend (PID: $frontend_pid)..."
            kill "$frontend_pid"
        fi
        rm -f .frontend.pid
    fi
    
    # Kill any remaining processes
    pkill -f "python -m src.main" 2>/dev/null || true
    pkill -f "npm run dev" 2>/dev/null || true
    pkill -f "vite" 2>/dev/null || true
    pkill -f "uvicorn" 2>/dev/null || true
    
    print_success "Services shut down due to inactivity"
    
    # Exit the monitor
    exit 0
}

# Function to monitor API activity
monitor_api_activity() {
    while true; do
        if check_services; then
            # Check if there's been recent API activity
            if [ -f "$LAST_ACTIVITY_FILE" ]; then
                local last_activity=$(cat "$LAST_ACTIVITY_FILE")
                local current_time=$(date +%s)
                local time_diff=$((current_time - last_activity))
                
                if [ $time_diff -ge $IDLE_TIMEOUT ]; then
                    shutdown_services
                else
                    local remaining=$((IDLE_TIMEOUT - time_diff))
                    print_status "Services active. Shutdown in $remaining seconds if no activity..."
                fi
            else
                # No activity file, create one
                update_activity
            fi
        else
            print_status "Services not running, exiting monitor..."
            exit 0
        fi
        
        sleep 10  # Check every 10 seconds
    done
}

# Function to start monitoring
start_monitoring() {
    print_status "Starting idle monitor (timeout: $IDLE_TIMEOUT seconds)..."
    
    # Initialize activity file
    update_activity
    
    # Start monitoring
    monitor_api_activity
}

# Main execution
main() {
    case "${1:-start}" in
        "start")
            start_monitoring
            ;;
        "update")
            update_activity
            print_status "Activity updated"
            ;;
        *)
            echo "Usage: $0 {start|update}"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
