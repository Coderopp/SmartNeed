#!/bin/bash

# SmartNeed Development Setup Script
# This script sets up the development environment for both frontend and backend

set -e

echo "🚀 Setting up SmartNeed development environment..."

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists node; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

if ! command_exists python3; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

if ! command_exists pip; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Setup backend
echo "🐍 Setting up backend..."
cd backend

if [ ! -f ".env" ]; then
    echo "📝 Creating backend .env file from example..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env with your actual values"
fi

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Backend setup complete"

# Setup frontend
echo "⚛️  Setting up frontend..."
cd ../frontend

if [ ! -f ".env" ]; then
    echo "📝 Creating frontend .env file from example..."
    cp .env.example .env
    echo "⚠️  Please edit frontend/.env with your actual values"
fi

echo "📦 Installing Node.js dependencies..."
npm install

echo "✅ Frontend setup complete"

# Back to root
cd ..

echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit backend/.env with your API keys and database URL"
echo "2. Edit frontend/.env with your backend URL"
echo ""
echo "🚀 To start development:"
echo "Backend:  cd backend && uvicorn app.main:app --reload"
echo "Frontend: cd frontend && npm start"
echo ""
echo "🌐 Default URLs:"
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
