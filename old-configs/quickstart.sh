#!/bin/bash

# SMARTNEED Quick Start Script
# This script helps you get SMARTNEED running quickly

set -e  # Exit on any error

echo "🚀 SMARTNEED Quick Start Setup"
echo "================================"

# Color codes for output
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

# Check if we're in the right directory
if [[ ! -f "init_mongodb.py" ]]; then
    print_error "Please run this script from the SMARTNEED root directory"
    exit 1
fi

print_status "Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Check MongoDB
if ! command -v mongosh &> /dev/null && ! command -v mongo &> /dev/null; then
    print_warning "MongoDB client not found. Make sure MongoDB is installed and running."
fi

print_success "Prerequisites check completed"

# Step 1: Environment Configuration
print_status "Setting up environment configuration..."

if [[ ! -f "config/api_keys.env" ]]; then
    if [[ -f "config/api_keys.env.example" ]]; then
        cp config/api_keys.env.example config/api_keys.env
        print_success "Created config/api_keys.env from template"
    else
        print_error "Environment template not found"
        exit 1
    fi
else
    print_warning "config/api_keys.env already exists, skipping creation"
fi

# Check if Gemini API key is set
if grep -q "your_gemini_api_key_here" config/api_keys.env; then
    print_warning "⚠️  IMPORTANT: You need to edit config/api_keys.env and add your Gemini API key!"
    print_warning "   Get it from: https://makersuite.google.com/app/apikey"
    echo ""
    read -p "Do you want to edit the config file now? (y/n): " edit_config
    if [[ $edit_config == "y" || $edit_config == "Y" ]]; then
        ${EDITOR:-nano} config/api_keys.env
    fi
fi

# Step 2: Backend Setup
print_status "Setting up backend..."

cd backend

# Create virtual environment if it doesn't exist
if [[ ! -d "venv" ]]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt
print_success "Backend dependencies installed"

cd ..

# Step 3: Frontend Setup
print_status "Setting up frontend..."

cd frontend

# Install dependencies
if [[ ! -d "node_modules" ]]; then
    print_status "Installing Node.js dependencies..."
    npm install
    print_success "Frontend dependencies installed"
else
    print_warning "node_modules already exists, skipping npm install"
fi

cd ..

# Step 4: Initialize MongoDB
print_status "Initializing MongoDB database..."

# Load environment variables
export $(grep -v '^#' config/api_keys.env | xargs)

# Run MongoDB initialization
if python3 init_mongodb.py; then
    print_success "MongoDB initialized successfully"
else
    print_error "MongoDB initialization failed. Please check your MongoDB installation and connection."
    exit 1
fi

# Step 5: Instructions for starting the application
echo ""
print_success "🎉 SMARTNEED setup completed successfully!"
echo ""
echo "To start the application:"
echo ""
echo "1. Start the backend (in one terminal):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python -m app.main"
echo ""
echo "2. Start the frontend (in another terminal):"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "3. Open your browser and go to:"
echo "   http://localhost:3000"
echo ""
print_status "Backend will be available at: http://localhost:8000"
print_status "Frontend will be available at: http://localhost:3000"
print_status "API documentation at: http://localhost:8000/docs"
echo ""

# Option to start services automatically
read -p "Do you want to start the backend and frontend now? (y/n): " start_services

if [[ $start_services == "y" || $start_services == "Y" ]]; then
    print_status "Starting SMARTNEED services..."
    
    # Start backend in background
    cd backend
    source venv/bin/activate
    python -m app.main &
    BACKEND_PID=$!
    cd ..
    
    # Wait a moment for backend to start
    sleep 3
    
    # Start frontend
    cd frontend
    npm start &
    FRONTEND_PID=$!
    cd ..
    
    print_success "Services started!"
    print_status "Backend PID: $BACKEND_PID"
    print_status "Frontend PID: $FRONTEND_PID"
    
    echo ""
    echo "Press Ctrl+C to stop both services"
    
    # Wait for user to stop
    trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
    wait
fi

print_success "Setup complete! 🚀"
