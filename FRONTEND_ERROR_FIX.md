# Frontend Deployment Error Fix

## Error Analysis
The error shows:
```
"/backend/requirements.txt": not found
```

This indicates Railway is trying to build from the wrong context or using an old cached configuration.

## Solution 1: Use Root-Level Deployment (Recommended)

Let's create a simplified approach by putting the frontend Dockerfile back in the root:

### 1. Create Root-Level Frontend Dockerfile
```dockerfile
# Build stage
FROM node:18-alpine as build

WORKDIR /app

# Copy frontend package files
COPY frontend/package.json frontend/package-lock.json ./

# Install dependencies
RUN npm ci --only=production

# Copy frontend source
COPY frontend/ .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Install curl for health checks
RUN apk add --no-cache curl

# Copy built app to nginx
COPY --from=build /app/build /usr/share/nginx/html

# Create nginx config with health check
RUN echo 'server { \
  listen 80; \
  server_name _; \
  root /usr/share/nginx/html; \
  index index.html; \
  location / { \
    try_files $uri $uri/ /index.html; \
  } \
  location /health { \
    access_log off; \
    return 200 "healthy\\n"; \
    add_header Content-Type text/plain; \
  } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
```

### 2. Root Railway Configuration
```toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "Dockerfile.frontend"

[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
```

## Solution 2: Railway Service Configuration

In Railway dashboard:

1. **Create New Service**
2. **Service Settings:**
   - Root Directory: `frontend`
   - Build Command: (leave empty, use Dockerfile)
   - Start Command: (leave empty, use Dockerfile)
3. **Variables:**
   ```
   REACT_APP_API_URL=https://your-backend.railway.app/api
   ```

## Solution 3: Manual Configuration Override

If Railway is still using old config:

1. **Delete the service** in Railway
2. **Create a new service**
3. **Set root directory to `frontend`**
4. **Use the Dockerfile in frontend directory**

## Quick Fix Commands

Run these to apply the root-level approach:
```bash
# Copy frontend Dockerfile to root with corrected paths
cp frontend/Dockerfile ./Dockerfile.frontend

# Update the Dockerfile paths
sed -i 's|COPY package.json package-lock.json|COPY frontend/package.json frontend/package-lock.json|' Dockerfile.frontend
sed -i 's|COPY \. \.|COPY frontend/ .|' Dockerfile.frontend

# Create root railway config for frontend
cat > railway-frontend.toml << 'EOF'
[build]
builder = "DOCKERFILE"
dockerfilePath = "Dockerfile.frontend"

[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
EOF
```
