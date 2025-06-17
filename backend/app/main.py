"""
SMARTNEED FastAPI Application
AI-powered product recommendation engine
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import logging
import sys
import os
from typing import Dict, Any

# Add the parent directory to Python path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.routers import search, products, export, comparison
from app.services.gemini_service import GeminiService
from app.settings import get_settings
from database.connection import mongodb, get_database

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("🚀 Starting SMARTNEED API...")
    
    # Initialize database
    try:
        await mongodb.connect()
        logger.info("✅ Database connection established")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        # Don't raise - allow app to start without DB for development
    
    # Initialize Gemini service
    try:
        gemini = GeminiService()
        app.state.gemini_service = gemini
        logger.info("✅ Gemini AI service initialized")
    except Exception as e:
        logger.warning(f"⚠️ Gemini service initialization failed: {e}")
        app.state.gemini_service = None
    
    logger.info("🎯 SMARTNEED API is ready!")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down SMARTNEED API...")

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-powered product recommendation engine with semantic search",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Health check endpoints
@app.get("/", tags=["Health"])
async def root() -> Dict[str, Any]:
    """Root endpoint with basic info"""
    return {
        "service": settings.PROJECT_NAME,
        "version": "1.0.0",
        "status": "healthy",
        "message": "Welcome to SMARTNEED API 🚀",
        "docs": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    health_status = {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "1.0.0",
        "components": {}
    }
    
    # Check database
    try:
        db = await get_database()
        # Test database connection with a simple ping
        await db.command('ping')
        
        # Check if using mock database
        db_status = "healthy"
        if mongodb.is_mock:
            db_status = "healthy (mock mode)"
        
        health_status["components"]["database"] = db_status
    except Exception:
        health_status["components"]["database"] = "unhealthy"
    
    # Check Gemini service
    gemini_service = getattr(app.state, 'gemini_service', None)
    health_status["components"]["gemini"] = "healthy" if gemini_service else "unhealthy"
    
    return health_status

# Include routers
app.include_router(
    search.router,
    prefix=f"{settings.API_V1_STR}/search",
    tags=["Search"]
)

app.include_router(
    products.router,
    prefix=f"{settings.API_V1_STR}/products",
    tags=["Products"]
)

app.include_router(
    export.router,
    prefix=f"{settings.API_V1_STR}/export",
    tags=["Export"]
)

app.include_router(
    comparison.router,
    prefix=f"{settings.API_V1_STR}/comparison",
    tags=["Comparison"]
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return HTTPException(
        status_code=500,
        detail="Internal server error"
    )

if __name__ == "__main__":
    import uvicorn
    # Railway provides PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload in production
        log_level="info"
    )
