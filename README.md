# SmartNeed - AI-Powered Product Recommendation Engine

A modern monorepo containing both frontend and backend services for an AI-powered product recommendation system.

## 🏗️ Monorepo Structure

```
smartneed/
├── frontend/              # React.js frontend application
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── Dockerfile
│   └── railway.json
├── backend/               # FastAPI backend application
│   ├── app/
│   ├── services/
│   ├── database/
│   ├── config/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── railway.json
├── docs/                  # Documentation
├── old-configs/          # Legacy configuration files
└── railway.json          # Main Railway configuration
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- Docker (for containerization)

### Local Development

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

## 🚢 Railway Deployment

This repository is configured for Railway's monorepo deployment pattern. Each service (frontend and backend) can be deployed as separate Railway services within the same project.

### Deployment Steps

1. **Connect Repository to Railway**
   - Go to [Railway Dashboard](https://railway.app)
   - Create a new project
   - Connect your GitHub repository

2. **Deploy Backend Service**
   - Add a new service to your Railway project
   - Select "Deploy from GitHub repo"
   - Set the root directory to `backend`
   - Railway will automatically detect the `Dockerfile` and `railway.json`

3. **Deploy Frontend Service**
   - Add another service to the same Railway project
   - Select "Deploy from GitHub repo"
   - Set the root directory to `frontend`
   - Railway will automatically detect the `Dockerfile` and `railway.json`

### Environment Variables

#### Backend Service
Configure these environment variables in Railway:

```
GEMINI_API_KEY=your_gemini_api_key
MONGODB_URL=your_mongodb_connection_string
CORS_ORIGINS=https://your-frontend-domain.railway.app
PORT=8000
```

#### Frontend Service
Configure these environment variables in Railway:

```
REACT_APP_API_URL=https://your-backend-domain.railway.app
PORT=80
```

### Service Communication

The frontend service will communicate with the backend service using the Railway-provided domains. Make sure to:

1. Set the `REACT_APP_API_URL` in the frontend to your backend's Railway domain
2. Configure `CORS_ORIGINS` in the backend to include your frontend's Railway domain

## 📁 Service Details

### Backend Service
- **Framework**: FastAPI
- **Language**: Python 3.11
- **Database**: MongoDB
- **AI**: Google Gemini API
- **Port**: 8000
- **Health Check**: `/health`

### Frontend Service
- **Framework**: React.js
- **Language**: JavaScript
- **Styling**: Tailwind CSS
- **Build Tool**: Create React App
- **Web Server**: Nginx
- **Port**: 80
- **Health Check**: `/health`

## 🔧 Configuration Files

### Railway Configuration
- `railway.json` (root): Main project configuration
- `backend/railway.json`: Backend service configuration
- `frontend/railway.json`: Frontend service configuration

### Docker Configuration
- `backend/Dockerfile`: Backend containerization
- `frontend/Dockerfile`: Frontend containerization

## 🎯 Features

- **AI-Powered Recommendations**: Uses Google Gemini for intelligent product suggestions
- **Semantic Search**: Advanced search capabilities using embeddings
- **Product Comparison**: Side-by-side product analysis
- **Export Functionality**: Export search results and comparisons
- **Responsive Design**: Modern, mobile-friendly interface
- **Real-time Updates**: Fast, interactive user experience

## 🛠️ Development Tools

- **Backend Testing**: FastAPI automatic docs at `/docs`
- **Frontend Testing**: React Testing Library
- **Code Quality**: ESLint, Prettier (frontend)
- **API Documentation**: Swagger/OpenAPI

## 📚 API Documentation

Once deployed, the backend API documentation is available at:
- Swagger UI: `https://your-backend-domain.railway.app/docs`
- ReDoc: `https://your-backend-domain.railway.app/redoc`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both frontend and backend
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
