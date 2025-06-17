#!/bin/bash

# SmartNeed Railway Deployment Preparation Script
# This script prepares your local environment for Railway deployment

set -e

echo "🚀 Preparing SmartNeed for Railway deployment..."

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

# Check if required files exist
print_status "Checking deployment files..."

required_files=(
    "railway.toml"
    "railway.json" 
    "frontend-railway.toml"
    "RAILWAY_DEPLOYMENT_GUIDE.md"
    "RAILWAY_ENV_SETUP.md"
    "deployment/Dockerfile.backend"
    "deployment/Dockerfile.frontend"
    "deployment/nginx.conf"
)

for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        print_success "✓ $file exists"
    else
        print_error "✗ $file missing"
        exit 1
    fi
done

# Check if git is initialized
if [[ ! -d ".git" ]]; then
    print_warning "Git repository not initialized. Initializing..."
    git init
    git add .
    git commit -m "Initial commit for Railway deployment"
    print_success "Git repository initialized"
else
    print_success "✓ Git repository exists"
fi

# Create .gitignore if it doesn't exist
if [[ ! -f ".gitignore" ]]; then
    print_status "Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Dependencies
node_modules/
backend/venv/
backend/__pycache__/
backend/app/__pycache__/

# Environment files
.env
.env.local
.env.production
.env.development
config/api_keys.env

# Logs
*.log
logs/

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDE files
.vscode/
.idea/
*.swp
*.swo

# Python
*.pyc
*.pyo
*.pyd
__pycache__/
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Node.js
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# React build
frontend/build/

# Database
*.db
*.sqlite3

# Docker
.dockerignore
EOF
    print_success "✓ .gitignore created"
fi

# Check Railway CLI installation
if command -v railway &> /dev/null; then
    print_success "✓ Railway CLI is installed"
    railway_version=$(railway --version)
    print_status "Railway CLI version: $railway_version"
else
    print_warning "Railway CLI not found. Installing..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install railway
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl -fsSL https://railway.app/install.sh | sh
    else
        print_error "Please install Railway CLI manually: https://docs.railway.app/develop/cli"
        exit 1
    fi
    print_success "✓ Railway CLI installed"
fi

# Summary
echo ""
print_success "🎉 SmartNeed is ready for Railway deployment!"
echo ""
print_status "Next steps:"
echo "1. Push your code to GitHub if not already done"
echo "2. Go to https://railway.app and create a new project"
echo "3. Follow the RAILWAY_DEPLOYMENT_GUIDE.md for detailed deployment steps"
echo "4. Set up environment variables as described in RAILWAY_ENV_SETUP.md"
echo ""
print_status "Quick Railway deployment:"
echo "   railway login"
echo "   railway link [your-project-id]"
echo "   railway up"
echo ""
print_warning "Don't forget to:"
echo "• Set up MongoDB (Atlas or Railway plugin)"
echo "• Get your Gemini API key"
echo "• Configure environment variables"
echo "• Update frontend API URL after backend deployment"
