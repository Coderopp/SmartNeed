"""
Simple settings configuration for SMARTNEED backend
"""

import os
from typing import List

class Settings:
    """Application settings"""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SMARTNEED"
    
    # Railway Environment Detection
    RAILWAY_ENVIRONMENT: bool = os.getenv("RAILWAY_ENVIRONMENT") is not None
    
    # CORS - Include Railway domains
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        # Add Railway frontend domain (will be updated after frontend deployment)
        "https://*.railway.app",
        "https://*.up.railway.app"
    ]
    
    # Database (MongoDB) - Railway compatible
    MONGODB_URL: str = os.getenv(
        "MONGODB_URL", 
        "mongodb://localhost:27017/smartneed" if not os.getenv("RAILWAY_ENVIRONMENT") else None
    )
    
    # Database mode - can be forced to mock for testing
   
    
    # Gemini API
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = "gemini-2.0-flash"
    GEMINI_EMBEDDING_MODEL: str = "embedding-001"
    
    # Google Sheets
    GOOGLE_SHEETS_CREDENTIALS_PATH: str = os.getenv(
        "GOOGLE_SHEETS_CREDENTIALS_PATH",
        "sheets/auth/credentials.json"
    )
    
    # eBay API (removed Amazon)
    EBAY_API_KEY: str = os.getenv("EBAY_API_KEY", "")
    
    # Redis Cache
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    CACHE_EXPIRE_SECONDS: int = 3600
    
    # Search Configuration
    MAX_SEARCH_RESULTS: int = int(os.getenv("MAX_SEARCH_RESULTS", "50"))
    EMBEDDING_DIMENSION: int = 768
    SIMILARITY_THRESHOLD: float = 0.7
    
    # Security
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", 
        "your-secret-key-change-in-production"
    )
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

# Global settings instance
def get_settings() -> Settings:
    """Get application settings"""
    return Settings()
