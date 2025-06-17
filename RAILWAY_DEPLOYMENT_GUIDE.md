# SmartNeed Railway Deployment Guide

This guide will walk you through deploying the SmartNeed application on Railway platform.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **MongoDB Database**: Either MongoDB Atlas or Railway MongoDB plugin
4. **API Keys**: Gemini API key (required), eBay API key (optional)

## Step-by-Step Deployment

### 1. Prepare Your Repository

Ensure your repository has all the files we've created:
- `railway.toml` - Backend configuration
- `frontend-railway.toml` - Frontend configuration  
- `RAILWAY_ENV_SETUP.md` - Environment variables guide
- Updated `deployment/Dockerfile.backend`
- Updated `deployment/Dockerfile.frontend`
- Updated `deployment/nginx.conf`

### 2. Create Railway Project

1. Go to [railway.app](https://railway.app) and sign in
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your SmartNeed repository

### 3. Deploy Backend Service

1. Railway will automatically detect your project
2. Choose "Create Service" for the backend
3. In the service settings:
   - **Name**: `smartneed-backend`
   - **Build Configuration**: Use `railway.toml`
   - **Root Directory**: Leave empty (uses project root)

### 4. Configure Backend Environment Variables

Go to your backend service → Variables tab and add:

```bash
# Required Variables
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/smartneed
GEMINI_API_KEY=your_gemini_api_key_here
RAILWAY_ENVIRONMENT=true

# Optional Variables  
REDIS_URL=redis://redis-service:6379
EBAY_API_KEY=your_ebay_api_key_here
SECRET_KEY=your-super-secret-key-for-production
LOG_LEVEL=INFO
MAX_SEARCH_RESULTS=50
```

### 5. Deploy Frontend Service

1. In your Railway project, click "New Service"
2. Select "Deploy from GitHub repo" 
3. Choose the same repository
4. In the service settings:
   - **Name**: `smartneed-frontend`
   - **Build Configuration**: Create a new `railway.toml` or specify:
     - Builder: `DOCKERFILE`
     - Dockerfile Path: `deployment/Dockerfile.frontend`

### 6. Configure Frontend Environment Variables

Go to your frontend service → Variables tab and add:

```bash
REACT_APP_API_URL=https://smartneed-backend-production.up.railway.app
```

Replace the URL with your actual backend service URL from Railway.

### 7. Set Up Database

#### Option A: MongoDB Atlas (Recommended)
1. Create account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a new cluster (free tier available)
3. Create a database user
4. Get connection string
5. Add to `MONGODB_URL` environment variable

#### Option B: Railway MongoDB Plugin
1. In Railway project, click "Add Plugin"
2. Select "MongoDB"
3. Railway automatically creates `MONGODB_URL` variable

### 8. Get API Keys

#### Gemini API Key (Required)
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create new API key
3. Add to `GEMINI_API_KEY` environment variable

#### eBay API Key (Optional)
1. Go to [eBay Developers](https://developer.ebay.com/)
2. Create application
3. Get API key
4. Add to `EBAY_API_KEY` environment variable

### 9. Deploy and Test

1. Both services should automatically deploy after configuration
2. Check deployment logs for any errors
3. Visit your frontend URL to test the application
4. Test API endpoints using the backend URL + `/docs`

### 10. Configure Custom Domain (Optional)

1. In Railway project settings
2. Go to "Domains" tab
3. Add your custom domain
4. Update DNS records as instructed
5. Update `REACT_APP_API_URL` if using custom domain for backend

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check that all dependencies are in `requirements.txt` and `package.json`
   - Verify Dockerfile paths are correct
   - Check Railway build logs for specific errors

2. **Environment Variable Issues**
   - Ensure all required variables are set
   - Check variable names match exactly
   - Restart services after adding variables

3. **Database Connection Issues**
   - Verify MongoDB URL is correct
   - Check network access settings in MongoDB Atlas
   - Ensure database user has proper permissions

4. **CORS Issues**
   - Update `ALLOWED_ORIGINS` in backend settings
   - Add your frontend domain to allowed origins
   - Restart backend service after changes

### Health Checks

- Backend health: `https://your-backend-url.railway.app/health`
- Frontend health: `https://your-frontend-url.railway.app/health`
- API documentation: `https://your-backend-url.railway.app/docs`

### Monitoring

1. Railway provides built-in monitoring
2. Check service metrics in Railway dashboard
3. View application logs for debugging
4. Set up alerts for service downtime

## Production Considerations

1. **Security**
   - Use strong secrets for `SECRET_KEY`
   - Enable HTTPS (Railway provides this automatically)
   - Review and update CORS settings

2. **Performance**
   - Consider using Redis for caching
   - Monitor database performance
   - Optimize Docker images for faster builds

3. **Scaling**
   - Railway provides auto-scaling
   - Monitor resource usage
   - Consider multiple replicas for high availability

## Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Railway Community: [Railway Discord](https://discord.gg/railway)
- SmartNeed Issues: Create issues in your GitHub repository
