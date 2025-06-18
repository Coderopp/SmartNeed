# Railway Deployment Environment Variables

## Required Environment Variables for Backend Service

### Database Configuration
```
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/smartneed
```

### AI Service Configuration  
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### Railway Specific
```
RAILWAY_ENVIRONMENT=true
PORT=8000
```

### Optional Services
```
REDIS_URL=redis://redis-service:6379
EBAY_API_KEY=your_ebay_api_key_here
SECRET_KEY=your-super-secret-key-for-production
LOG_LEVEL=INFO
MAX_SEARCH_RESULTS=50
```

## Frontend Environment Variables

### API Configuration
```
REACT_APP_API_URL=https://your-backend-service.railway.app
```

## How to Set Environment Variables in Railway

1. Go to your Railway project dashboard
2. Select your service (backend or frontend)
3. Go to the "Variables" tab
4. Add each environment variable with its corresponding value
5. Deploy the service

## MongoDB Setup Options

### Option 1: MongoDB Atlas (Recommended)
1. Create a free account at https://www.mongodb.com/atlas
2. Create a new cluster
3. Get the connection string
4. Add it as MONGODB_URL environment variable

### Option 2: Railway MongoDB Plugin
1. In Railway dashboard, click "Add Plugin"
2. Select "MongoDB"
3. Railway will automatically create MONGODB_URL environment variable

## API Keys Required

### Gemini API Key
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Add it as GEMINI_API_KEY environment variable

### eBay API Key (Optional)
1. Go to https://developer.ebay.com/
2. Create an application
3. Get your API key
4. Add it as EBAY_API_KEY environment variable
