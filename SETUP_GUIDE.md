# 🚀 SMARTNEED - Complete Setup Guide

## Prerequisites Installation

### 1. System Requirements
- **Node.js** 18+ (for frontend)
- **Python** 3.9+ (for backend)
- **MongoDB** (local installation or MongoDB Atlas cloud)

### 2. Install Prerequisites

#### Ubuntu/Linux:
```bash
# Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Python 3.9+
sudo apt update
sudo apt install python3 python3-pip python3-venv

# MongoDB (Local Installation)
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

#### macOS:
```bash
# Using Homebrew
brew install node python@3.9 mongodb/brew/mongodb-community
brew services start mongodb-community
```

#### Windows:
- Download Node.js from https://nodejs.org/
- Download Python from https://python.org/
- Download MongoDB from https://www.mongodb.com/try/download/community

## 🔧 Environment Configuration

### 1. Create Environment File
Copy the template and fill in your details:

```bash
cd /home/pranav/Desktop/Hackathon/smartneed
cp config/api_keys.env.example config/api_keys.env
```

### 2. Edit `config/api_keys.env` with Required Values:

```bash
# ================================
# SMARTNEED Environment Configuration
# Fill in ALL the values below
# ================================

# =====================================
# DATABASE CONFIGURATION (REQUIRED)
# =====================================
# Option 1: Local MongoDB
MONGODB_URL=mongodb://localhost:27017/smartneed

# Option 2: MongoDB Atlas (Cloud) - Replace with your connection string
# MONGODB_URL=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/smartneed?retryWrites=true&w=majority

# =====================================
# AI SERVICE CONFIGURATION (REQUIRED)
# =====================================
# Get your Gemini API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# =====================================
# OPTIONAL SERVICES
# =====================================
# Redis Cache (Optional - for better performance)
REDIS_URL=redis://localhost:6379

# eBay API (Optional - for enhanced scraping)
EBAY_API_KEY=your_ebay_api_key_here

# =====================================
# APPLICATION SETTINGS
# =====================================
# Security key (generate a random string for production)
SECRET_KEY=your-super-secret-jwt-key-change-in-production

# Environment
PROJECT_NAME=SMARTNEED
DEBUG=true
LOG_LEVEL=INFO

# CORS Origins (add your frontend URL)
ALLOWED_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]

# Search Configuration
MAX_SEARCH_RESULTS=50
CACHE_EXPIRE_SECONDS=3600
```

## 🔑 Getting Required API Keys

### 1. Google Gemini API Key (REQUIRED)
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it as `GEMINI_API_KEY` in your `.env` file

### 2. MongoDB Setup (Choose One Option)

#### Option A: Local MongoDB (Recommended for Development)
```bash
# MongoDB should be running after installation
# Test connection:
mongosh
# If connected successfully, type: exit

# Update your .env file:
MONGODB_URL=mongodb://localhost:27017/smartneed
```

#### Option B: MongoDB Atlas (Cloud - Recommended for Production)
1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a free account
3. Create a new cluster (choose free tier)
4. Create a database user:
   - Go to Database Access
   - Add new database user
   - Choose username/password authentication
5. Configure network access:
   - Go to Network Access
   - Add IP address (0.0.0.0/0 for development, specific IPs for production)
6. Get connection string:
   - Go to Clusters → Connect → Connect your application
   - Copy the connection string
   - Replace `<password>` with your database user password
   - Update your .env file with this URL

### 3. Optional Services

#### Redis (Optional - for caching)
```bash
# Ubuntu/Linux
sudo apt install redis-server
sudo systemctl start redis-server

# macOS
brew install redis
brew services start redis

# Test connection
redis-cli ping
# Should return: PONG
```

#### eBay API (Optional - for enhanced scraping)
1. Go to [eBay Developers](https://developer.ebay.com/)
2. Sign up for developer account
3. Create an application
4. Get your API key (App ID)
5. Add to .env file as `EBAY_API_KEY`

## 🚀 Installation Steps

### 1. Initialize MongoDB Database
```bash
cd /home/pranav/Desktop/Hackathon/smartneed

# This will create collections, indexes, and sample data
python init_mongodb.py
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
python -m app.main
```

The backend should start on: http://localhost:8000

### 3. Frontend Setup
```bash
# Open new terminal
cd /home/pranav/Desktop/Hackathon/smartneed/frontend

# Install dependencies
npm install

# Start development server
npm start
```

The frontend should start on: http://localhost:3000

## ✅ Verification Steps

### 1. Check Backend Health
```bash
curl http://localhost:8000/health
```
Should return database and service status.

### 2. Check MongoDB Connection
```bash
# Connect to MongoDB
mongosh smartneed

# Check collections
show collections
# Should show: products, embeddings, search_history, etc.

# Check sample data
db.products.countDocuments()
# Should return number > 0
```

### 3. Test Frontend
1. Open http://localhost:3000 in browser
2. Try searching for "wireless headphones"
3. Should return product results

### 4. Test Full Pipeline
```bash
# Test API search endpoint
curl -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "bluetooth headphones",
    "limit": 5
  }'
```

## 🛠️ Troubleshooting

### Common Issues:

#### 1. MongoDB Connection Error
```bash
# Check MongoDB status
sudo systemctl status mongod

# Start MongoDB if not running
sudo systemctl start mongod

# Check MongoDB logs
sudo tail -f /var/log/mongodb/mongod.log
```

#### 2. Python Module Import Errors
```bash
# Make sure virtual environment is activated
source backend/venv/bin/activate

# Install missing packages
pip install -r backend/requirements.txt
```

#### 3. Frontend Won't Start
```bash
cd frontend

# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### 4. API Connection Issues
- Check that backend is running on port 8000
- Verify CORS origins in backend settings
- Check firewall settings

### 5. Gemini API Issues
- Verify API key is correct
- Check API quotas and billing
- Test API key independently:
```bash
curl -H "Content-Type: application/json" \
     -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
     "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_API_KEY"
```

## 📚 Next Steps After Setup

1. **Add More Product Data**: Run scrapers to collect more products
2. **Generate Embeddings**: Create AI embeddings for better search
3. **Customize Search**: Adjust search parameters and filters
4. **Monitor Performance**: Check logs and database performance
5. **Production Deploy**: Configure for production environment

## 🔒 Security Notes

- **Change SECRET_KEY** in production
- **Use environment-specific** MongoDB URLs
- **Restrict CORS origins** to your actual domains
- **Enable MongoDB authentication** for production
- **Use HTTPS** in production
- **Keep API keys secure** - never commit to version control

## 📞 Support

If you encounter issues:
1. Check the logs in both backend and frontend terminals
2. Verify all environment variables are set correctly
3. Ensure all services (MongoDB, Redis) are running
4. Test individual components separately

Your SMARTNEED application should now be fully functional with real MongoDB data storage, AI-powered search, and a modern React frontend! 🎉
