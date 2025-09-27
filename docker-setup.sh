#!/bin/bash

# yt-dlp Web UI - Docker One-Click Setup Script

echo "🐳 yt-dlp Web UI - Docker Setup"
echo "==============================="

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

# Check if Docker is installed
check_docker() {
    print_status "Checking Docker installation..."
    
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
        print_success "Docker $DOCKER_VERSION found"
    else
        print_error "Docker is required but not installed"
        print_status "Please install Docker and try again"
        exit 1
    fi
    
    if command -v docker-compose &> /dev/null; then
        COMPOSE_VERSION=$(docker-compose --version | cut -d' ' -f3 | cut -d',' -f1)
        print_success "Docker Compose $COMPOSE_VERSION found"
    else
        print_error "Docker Compose is required but not installed"
        print_status "Please install Docker Compose and try again"
        exit 1
    fi
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    mkdir -p downloads logs
    print_success "Directories created"
}

# Build and start with Docker Compose
start_docker() {
    print_status "Building and starting with Docker Compose..."
    
    # Stop any existing containers
    docker-compose down 2>/dev/null || true
    
    # Build and start
    docker-compose up --build -d
    
    if [ $? -eq 0 ]; then
        print_success "Docker containers started successfully"
    else
        print_error "Failed to start Docker containers"
        exit 1
    fi
}

# Wait for service to be ready
wait_for_service() {
    print_status "Waiting for service to be ready..."
    
    for i in {1..30}; do
        if curl -s http://localhost:8000/health > /dev/null; then
            print_success "Service is ready!"
            return 0
        fi
        echo -n "."
        sleep 2
    done
    
    print_warning "Service might still be starting up"
}

# Main execution
main() {
    check_docker
    create_directories
    start_docker
    wait_for_service
    
    echo ""
    print_success "🎉 yt-dlp Web UI is now running with Docker!"
    echo ""
    echo -e "${GREEN}🌐 Application:${NC} http://localhost:8000"
    echo -e "${GREEN}📊 Health:${NC}     http://localhost:8000/health"
    echo ""
    echo -e "${YELLOW}📝 Logs:${NC}"
    echo -e "   docker-compose logs -f"
    echo ""
    echo -e "${YELLOW}🛑 To stop:${NC} docker-compose down"
    echo ""
    echo -e "${BLUE}💡 Open your browser and go to: http://localhost:8000${NC}"
}

# Run main function
main "$@"

