# Railway Deployment Guide - SmartNeed Monorepo

This guide explains how to deploy the SmartNeed application using Railway's monorepo deployment pattern.

## Overview

The SmartNeed application consists of two services:
1. **Backend**: FastAPI application (Python)
2. **Frontend**: React application (JavaScript/Node.js)

Both services are deployed as separate Railway services within the same project.

## Prerequisites

1. Railway account (sign up at [railway.app](https://railway.app))
2. GitHub repository with the SmartNeed code
3. Environment variables ready (API keys, database URLs, etc.)

## Step-by-Step Deployment

### 1. Create Railway Project

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your SmartNeed repository
5. Name your project (e.g., "smartneed-production")

### 2. Deploy Backend Service

1. In your Railway project, click "Add Service"
2. Select "GitHub Repo"
3. Choose your repository
4. Set the following configuration:
   - **Service Name**: `smartneed-backend`
   - **Root Directory**: `backend`
   - **Build Command**: (leave empty - Docker will handle this)
   - **Start Command**: (leave empty - Docker will handle this)

5. Railway will automatically detect:
   - `backend/Dockerfile`
   - `backend/railway.json`
   - `backend/requirements.txt`

### 3. Configure Backend Environment Variables

In the backend service settings, add these environment variables:

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here
MONGODB_URL=mongodb://username:password@host:port/database

# Optional (will use defaults if not set)
PORT=8000
ENVIRONMENT=production
LOG_LEVEL=info

# CORS (set after frontend is deployed)
CORS_ORIGINS=https://your-frontend-domain.railway.app
```

### 4. Deploy Frontend Service

1. In your Railway project, click "Add Service"
2. Select "GitHub Repo"
3. Choose the same repository
4. Set the following configuration:
   - **Service Name**: `smartneed-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: (leave empty - Docker will handle this)
   - **Start Command**: (leave empty - Docker will handle this)

### 5. Configure Frontend Environment Variables

In the frontend service settings, add these environment variables:

```bash
# Point to your backend service
REACT_APP_API_URL=https://your-backend-domain.railway.app

# Optional
PORT=80
NODE_ENV=production
```

### 6. Update CORS Configuration

After both services are deployed:

1. Note the domains Railway assigns to each service
2. Update the backend's `CORS_ORIGINS` environment variable
3. Update the frontend's `REACT_APP_API_URL` environment variable
4. Redeploy both services

## Railway Domains

Railway will provide domains like:
- Backend: `https://smartneed-backend-production.railway.app`
- Frontend: `https://smartneed-frontend-production.railway.app`

You can also set up custom domains in Railway if needed.

## Monitoring and Logs

### Viewing Logs
1. Go to your Railway project dashboard
2. Click on a service
3. Go to the "Deployments" tab
4. Click on a deployment to view logs

### Health Checks
Both services have health check endpoints:
- Backend: `https://your-backend-domain.railway.app/health`
- Frontend: `https://your-frontend-domain.railway.app/health`

## Environment-Specific Configuration

### Development
- Use Railway's preview deployments for feature branches
- Set different environment variables for development

### Production
- Use Railway's production environment
- Set up custom domains
- Configure environment variables for production APIs

## Troubleshooting

### Backend Issues
1. Check logs in Railway dashboard
2. Verify environment variables are set
3. Test health endpoint: `/health`
4. Check MongoDB connection

### Frontend Issues
1. Check build logs for compilation errors
2. Verify `REACT_APP_API_URL` points to correct backend
3. Test static file serving
4. Check browser console for errors

### Common Issues

#### CORS Errors
- Ensure `CORS_ORIGINS` in backend includes frontend domain
- Check that domains match exactly (including https://)

#### API Connection Issues
- Verify `REACT_APP_API_URL` is correct
- Check that backend service is running
- Test backend health endpoint directly

#### Build Failures
- Check that all dependencies are listed in `package.json` or `requirements.txt`
- Verify Docker builds work locally
- Check Railway build logs for specific errors

## Scaling and Performance

### Auto-scaling
Railway automatically scales based on:
- CPU usage
- Memory usage
- Request volume

### Performance Optimization
- Enable gzip compression (already configured)
- Use Railway's CDN for static assets
- Monitor response times in Railway dashboard

## Database Setup

If using MongoDB:
1. Deploy MongoDB as a separate Railway service, or
2. Use MongoDB Atlas (recommended for production)
3. Set the `MONGODB_URL` environment variable

## Security Best Practices

1. **Environment Variables**: Never commit secrets to git
2. **CORS**: Restrict to specific domains
3. **HTTPS**: Railway provides SSL certificates automatically
4. **API Keys**: Rotate regularly and use Railway's variable management

## Cost Optimization

1. **Hobby Plan**: Good for development and small projects
2. **Pro Plan**: Recommended for production
3. **Monitor Usage**: Check Railway dashboard for resource usage
4. **Sleep Mode**: Enable for non-production services

## Backup Strategy

1. **Database**: Regular MongoDB backups
2. **Code**: Version control with git
3. **Environment Variables**: Document in secure location
4. **Deployment Config**: Keep railway.json files in version control

This deployment pattern provides a robust, scalable foundation for the SmartNeed application with proper separation of concerns and easy maintenance.
