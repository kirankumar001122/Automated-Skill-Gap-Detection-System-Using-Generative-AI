#!/bin/bash

# Autonomous Coding Agent - Startup Script
# This script helps you start the application quickly

set -e

echo "🚀 Autonomous Coding Agent - Startup Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if Docker is running
check_docker() {
    print_header "Checking Docker installation..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        echo "Visit: https://docker.com"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker Desktop/daemon."
        exit 1
    fi
    
    print_status "Docker is installed and running ✓"
}

# Check if Ollama is running
check_ollama() {
    print_header "Checking Ollama installation..."
    
    if ! command -v ollama &> /dev/null; then
        print_error "Ollama is not installed."
        echo "Install with: curl -fsSL https://ollama.ai/install.sh | sh"
        exit 1
    fi
    
    # Check if Ollama is running
    if ! curl -s http://localhost:11434/api/tags &> /dev/null; then
        print_warning "Ollama is not running. Starting it..."
        ollama serve &
        sleep 5
        
        # Check again
        if ! curl -s http://localhost:11434/api/tags &> /dev/null; then
            print_error "Failed to start Ollama. Please start it manually with: ollama serve"
            exit 1
        fi
    fi
    
    print_status "Ollama is installed and running ✓"
}

# Check if models are installed
check_models() {
    print_header "Checking Ollama models..."
    
    models=$(ollama list 2>/dev/null | grep -v "NAME" | wc -l)
    
    if [ "$models" -eq 0 ]; then
        print_warning "No models found. Installing recommended models..."
        
        print_status "Pulling codellama:7b (this may take a while)..."
        ollama pull codellama:7b
        
        print_status "Pulling deepseek-coder:6.7b (this may take a while)..."
        ollama pull deepseek-coder:6.7b
        
        print_status "Models installed successfully ✓"
    else
        print_status "Found $models model(s) ✓"
        ollama list
    fi
}

# Check environment file
check_env() {
    print_header "Checking environment configuration..."
    
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating from template..."
        cp .env.example .env
        print_status "Created .env file from template ✓"
        print_warning "You may want to edit .env file for custom configuration"
    else
        print_status ".env file exists ✓"
    fi
}

# Start the application
start_application() {
    print_header "Starting Autonomous Coding Agent..."
    
    # Check if docker-compose exists
    if command -v docker-compose &> /dev/null; then
        COMPOSE_CMD="docker-compose"
    else
        COMPOSE_CMD="docker compose"
    fi
    
    print_status "Using: $COMPOSE_CMD"
    
    # Stop any existing containers
    print_status "Stopping existing containers..."
    $COMPOSE_CMD down 2>/dev/null || true
    
    # Build and start services
    print_status "Building and starting services..."
    $COMPOSE_CMD up --build
    
    # If we get here, the user pressed Ctrl+C
    echo ""
    print_status "Application stopped."
}

# Show final instructions
show_instructions() {
    echo ""
    echo "🎉 Autonomous Coding Agent is starting up!"
    echo ""
    echo "📱 Access the application at:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend:  http://localhost:8000"
    echo "   API Docs: http://localhost:8000/docs"
    echo ""
    echo "💡 Try these example prompts:"
    echo "   • Create a function that calculates factorial"
    echo "   • Build a simple REST API for user management"
    echo "   • Write a script to process CSV files"
    echo ""
    echo "🔧 To stop the application, press Ctrl+C"
    echo "   Or run: docker-compose down"
    echo ""
}

# Main execution
main() {
    echo ""
    
    # Run all checks
    check_docker
    check_ollama
    check_models
    check_env
    
    # Show instructions before starting
    show_instructions
    
    # Start the application
    start_application
}

# Trap Ctrl+C to cleanup
trap 'echo ""; print_status "Shutting down..."; docker-compose down; exit 0' INT

# Run main function
main
