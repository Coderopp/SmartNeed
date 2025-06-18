# Railway Deployment Checklist

## Pre-Deployment Setup

### 1. Repository Structure ✅
- [x] Monorepo format with `frontend/` and `backend/` directories
- [x] Each service has its own `Dockerfile` and `railway.json`
- [x] Root-level `railway.json` for project configuration
- [x] Documentation in `docs/` directory

### 2. Backend Configuration ✅
- [x] `backend/Dockerfile` - Python 3.11 based container
- [x] `backend/railway.json` - Railway service configuration
- [x] `backend/requirements.txt` - Python dependencies
- [x] `backend/.env.example` - Environment variables template
- [x] Health check endpoint at `/health`

### 3. Frontend Configuration ✅
- [x] `frontend/Dockerfile` - Node.js + Nginx based container
- [x] `frontend/railway.json` - Railway service configuration
- [x] `frontend/package.json` - Node.js dependencies
- [x] `frontend/.env.example` - Environment variables template
- [x] Health check endpoint at `/health`

## Railway Deployment Steps

### Step 1: Create Railway Project
- [ ] Sign up/login to Railway
- [ ] Create new project
- [ ] Connect GitHub repository

### Step 2: Deploy Backend Service
- [ ] Add new service in Railway project
- [ ] Select GitHub repo
- [ ] Set root directory to `backend`
- [ ] Configure environment variables:
  - [ ] `GEMINI_API_KEY`
  - [ ] `MONGODB_URL`
  - [ ] `PORT=8000`
  - [ ] `CORS_ORIGINS` (set after frontend deployment)

### Step 3: Deploy Frontend Service
- [ ] Add new service in Railway project
- [ ] Select GitHub repo
- [ ] Set root directory to `frontend`
- [ ] Configure environment variables:
  - [ ] `REACT_APP_API_URL` (backend Railway domain)
  - [ ] `PORT=80`

### Step 4: Configure Service Communication
- [ ] Note Railway domains for both services
- [ ] Update backend `CORS_ORIGINS` with frontend domain
- [ ] Update frontend `REACT_APP_API_URL` with backend domain
- [ ] Redeploy both services

### Step 5: Verify Deployment
- [ ] Backend health check: `https://backend-domain.railway.app/health`
- [ ] Frontend health check: `https://frontend-domain.railway.app/health`
- [ ] API documentation: `https://backend-domain.railway.app/docs`
- [ ] Frontend application loads correctly
- [ ] Frontend can communicate with backend

## Environment Variables

### Backend Required
```bash
GEMINI_API_KEY=your_api_key
MONGODB_URL=mongodb_connection_string
CORS_ORIGINS=https://frontend-domain.railway.app
```

### Frontend Required
```bash
REACT_APP_API_URL=https://backend-domain.railway.app
```

## Common Issues & Solutions

### CORS Errors
- Ensure `CORS_ORIGINS` includes exact frontend domain
- Include `https://` in the URL
- No trailing slash in domain

### Build Failures
- Check Dockerfile syntax
- Verify all dependencies in requirements.txt/package.json
- Check Railway build logs

### Service Communication
- Verify environment variables are set correctly
- Test backend health endpoint directly
- Check network connectivity between services

## Post-Deployment

### Security
- [ ] Set up custom domains (optional)
- [ ] Review CORS settings
- [ ] Rotate API keys regularly
- [ ] Monitor error logs

### Performance
- [ ] Monitor resource usage
- [ ] Set up alerts for downtime
- [ ] Consider scaling options

### Maintenance
- [ ] Set up automated deployments
- [ ] Create backup strategy
- [ ] Document deployment process for team

## Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [Monorepo Deployment Guide](./docs/RAILWAY_DEPLOYMENT.md)
- [API Documentation](https://backend-domain.railway.app/docs) (after deployment)

---

✅ = Completed during repository restructuring
⬜ = To be completed during deployment
