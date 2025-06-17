# 🎯 SMARTNEED - AI-Powered Product Recommendation Engine

## Overview
SMARTNEED is an intelligent product discovery platform that uses natural language processing and semantic search to find the perfect products based on user needs, not just keywords.

## 🚀 Recent Updates - MongoDB Implementation
SMARTNEED has been completely restructured to use MongoDB for better scalability and performance:

- ✅ **MongoDB Integration**: Complete migration from PostgreSQL to MongoDB
- ✅ **Real Data Processing**: Removed mock data, implemented real web scraping
- ✅ **AI Embeddings**: Vector similarity search with MongoDB collections
- ✅ **Production Ready**: Clean architecture with proper service separation
- ✅ **Data Pipeline**: Automated scraping → processing → embedding → search

## Tech Stack
- **Frontend**: React + Tailwind CSS
- **Backend**: Python FastAPI
- **Database**: MongoDB (with vector embeddings)
- **AI**: Google Gemini API (embeddings & summaries)
- **Scraping**: BeautifulSoup + aiohttp for product data collection
- **Data Processing**: Automated ingestion and validation pipeline
- **Deployment**: Docker ready with production configuration

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+
- MongoDB (local or MongoDB Atlas)
- Google Gemini API key

### Installation

1. **Clone and setup**
```bash
cd smartneed
cp config/api_keys.env.example config/api_keys.env
# Edit config/api_keys.env with your API keys and MongoDB URL
```

2. **Initialize MongoDB**
```bash
# Install MongoDB locally or use MongoDB Atlas
# Update MONGODB_URL in config/api_keys.env
python init_mongodb.py
```

3. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
python -m app.main
```

4. **Frontend Setup**
```bash
cd frontend
npm install
npm start
```

### API Documentation
- Backend API: http://localhost:8000/docs
- Frontend: http://localhost:3000

## Project Structure
```
smartneed/
├── frontend/          # React + Tailwind UI
├── backend/           # FastAPI backend
├── data/              # Data processing pipeline
├── embeddings/        # Vector search engine
├── sheets/            # Google Sheets integration
├── scraper/           # Product data collection
├── config/            # Configuration files
├── tests/             # Testing suite
└── deployment/        # Docker & deployment
```

## Key Features
- 🔍 Natural language product search
- 🤖 AI-powered recommendations
- 📊 Side-by-side product comparison
- 📈 Export to Google Sheets
- 🎯 Budget and constraint optimization
- 🚀 Semantic search with embeddings

## Development Phases
- [x] Phase 1: Foundation & Setup
- [ ] Phase 2: Core Search Engine
- [ ] Phase 3: Advanced Features
- [ ] Phase 4: Polish & Deploy

## Contributing
See CONTRIBUTING.md for development guidelines.

## License
MIT License - see LICENSE file for details.
