#!/usr/bin/env python3
"""
Database connection test script for SMARTNEED
Tests MongoDB connection and basic operations
"""

import asyncio
import os
import logging
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv('config/.env')

async def test_database_connection():
    """Test MongoDB database connection"""
    try:
        # Try to import MongoDB dependencies
        from motor.motor_asyncio import AsyncIOMotorClient
        logger.info("✅ MongoDB dependencies are available")
        
        # Get MongoDB URL from environment
        mongo_url = os.getenv("MONGODB_URL")
        if not mongo_url:
            logger.error("❌ MONGODB_URL not found in environment variables")
            return False
            
        logger.info(f"🔗 Attempting to connect to MongoDB...")
        logger.info(f"   Connection string: {mongo_url[:20]}...")
        
        # Create MongoDB client
        client = AsyncIOMotorClient(mongo_url)
        
        # Test connection with ping
        await asyncio.wait_for(client.admin.command('ping'), timeout=10.0)
        logger.info("✅ Successfully connected to MongoDB!")
        
        # Get database
        database = client.smartneed
        
        # Test basic operations
        logger.info("🧪 Testing basic database operations...")
        
        # List collections
        collections = await database.list_collection_names()
        logger.info(f"📋 Available collections: {collections}")
        
        # Test products collection
        products_collection = database.products
        product_count = await products_collection.count_documents({})
        logger.info(f"📦 Products in database: {product_count}")
        
        if product_count > 0:
            # Get a sample product
            sample_product = await products_collection.find_one({})
            if sample_product:
                logger.info(f"📱 Sample product: {sample_product.get('name', 'Unknown')}")
        
        # Test embeddings collection
        embeddings_collection = database.embeddings
        embedding_count = await embeddings_collection.count_documents({})
        logger.info(f"🧠 Embeddings in database: {embedding_count}")
        
        # Test search_history collection
        search_history_collection = database.search_history
        search_count = await search_history_collection.count_documents({})
        logger.info(f"🔍 Search history entries: {search_count}")
        
        # Close connection
        client.close()
        logger.info("✅ Database connection test completed successfully!")
        return True
        
    except ImportError as e:
        logger.error(f"❌ MongoDB dependencies not installed: {e}")
        logger.info("💡 Run: pip install motor pymongo")
        return False
        
    except asyncio.TimeoutError:
        logger.error("❌ Connection timeout - MongoDB server might be unreachable")
        logger.info("💡 Check your MONGODB_URL and network connection")
        return False
        
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        logger.info("💡 Check your MongoDB URL and credentials")
        return False

async def test_environment_variables():
    """Test if all required environment variables are set"""
    logger.info("🔍 Checking environment variables...")
    
    required_vars = {
        'MONGODB_URL': 'Database connection string',
        'GEMINI_API_KEY': 'AI service API key'
    }
    
    optional_vars = {
        'REDIS_URL': 'Cache service URL',
        'EBAY_API_KEY': 'eBay API key for enhanced scraping',
        'SECRET_KEY': 'JWT secret key'
    }
    
    all_good = True
    
    # Check required variables
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            logger.info(f"✅ {var}: {description} - Set")
        else:
            logger.error(f"❌ {var}: {description} - Missing!")
            all_good = False
    
    # Check optional variables
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value and value != f"your_{var.lower()}_here":
            logger.info(f"✅ {var}: {description} - Set")
        else:
            logger.warning(f"⚠️  {var}: {description} - Not set (optional)")
    
    return all_good

async def main():
    """Main test function"""
    logger.info("🚀 Starting SMARTNEED Database Connection Test")
    logger.info("=" * 50)
    
    # Test environment variables
    env_ok = await test_environment_variables()
    logger.info("=" * 50)
    
    if not env_ok:
        logger.error("❌ Environment setup incomplete. Please check your config/.env file")
        return
    
    # Test database connection
    db_ok = await test_database_connection()
    
    logger.info("=" * 50)
    if db_ok:
        logger.info("🎉 All tests passed! Database is ready to use.")
    else:
        logger.error("💥 Database connection test failed. Please check the issues above.")

if __name__ == "__main__":
    asyncio.run(main())
