#!/usr/bin/env python3
"""
Test the application's database connection with fallback to mock
"""

import asyncio
import sys
import os
import logging
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.append('/home/pranav/Desktop/Hackathon/smartneed')

# Load environment variables
load_dotenv('config/.env')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_app_database():
    """Test the application's database connection"""
    try:
        # Import the database connection functions
        from database.connection import (
            init_database, 
            get_database, 
            check_database_connection,
            get_products_collection,
            get_embeddings_collection,
            mongodb
        )
        
        logger.info("🚀 Testing SMARTNEED Database Connection")
        logger.info("=" * 50)
        
        # Initialize database
        logger.info("🔗 Initializing database connection...")
        await init_database()
        
        # Check if we're using mock or real database
        if mongodb.is_mock:
            logger.info("🧪 Using Mock Database (MongoDB connection failed)")
        else:
            logger.info("✅ Using Real MongoDB Database")
        
        # Test database health
        logger.info("🏥 Checking database health...")
        is_healthy = await check_database_connection()
        
        if is_healthy:
            logger.info("✅ Database connection is healthy!")
        else:
            logger.error("❌ Database connection is unhealthy")
            return False
        
        # Get database instance
        db = await get_database()
        logger.info(f"📊 Database instance: {type(db).__name__}")
        
        # Test collections
        logger.info("📚 Testing collections...")
        
        # Test products collection
        products_collection = await get_products_collection()
        product_count = await products_collection.count_documents({})
        logger.info(f"📦 Products collection: {product_count} documents")
        
        if product_count > 0:
            # Get a sample product
            sample_product = await products_collection.find_one({})
            if sample_product:
                logger.info(f"📱 Sample product: {sample_product.get('name', 'Unknown')}")
                logger.info(f"   Brand: {sample_product.get('brand', 'Unknown')}")
                logger.info(f"   Price: ${sample_product.get('price', 0)}")
        
        # Test embeddings collection
        embeddings_collection = await get_embeddings_collection()
        embedding_count = await embeddings_collection.count_documents({})
        logger.info(f"🧠 Embeddings collection: {embedding_count} documents")
        
        # Test basic operations
        logger.info("🧪 Testing basic database operations...")
        
        # Test search functionality
        search_results = products_collection.find({'category': 'Electronics'})
        electronics_count = len(await search_results.to_list(None))
        logger.info(f"🔍 Electronics products: {electronics_count}")
        
        # Test price range search
        price_results = products_collection.find({'price': {'$lt': 500}})
        affordable_count = len(await price_results.to_list(None))
        logger.info(f"💰 Products under $500: {affordable_count}")
        
        logger.info("=" * 50)
        logger.info("🎉 Database connection test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"💥 Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_database_operations():
    """Test various database operations"""
    try:
        from database.connection import get_products_collection, get_search_history_collection
        
        logger.info("🧪 Testing Database Operations")
        logger.info("-" * 30)
        
        # Test product search operations
        products = await get_products_collection()
        
        # Test find operations
        all_products = await products.find({}).to_list(None)
        logger.info(f"📦 Total products: {len(all_products)}")
        
        # Test filtered search
        sony_products = await products.find({'brand': 'Sony'}).to_list(None)
        logger.info(f"📱 Sony products: {len(sony_products)}")
        
        # Test price range search
        budget_products = await products.find({
            'price': {'$lt': 1000}
        }).to_list(None)
        logger.info(f"💰 Products under $1000: {len(budget_products)}")
        
        # Test search history
        search_history = await get_search_history_collection()
        
        # Add a test search entry
        test_search = {
            'query': 'wireless headphones',
            'timestamp': '2024-06-17T21:00:00Z',
            'results_count': len(all_products),
            'user_session': 'test_session'
        }
        
        await search_history.insert_one(test_search)
        logger.info("📝 Added test search history entry")
        
        # Verify search history
        history_count = await search_history.count_documents({})
        logger.info(f"🔍 Search history entries: {history_count}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Database operations test failed: {e}")
        return False

async def main():
    """Main test function"""
    # Test application database connection
    db_test = await test_app_database()
    
    if db_test:
        # Test database operations
        ops_test = await test_database_operations()
        
        if ops_test:
            logger.info("🎉 All database tests passed!")
        else:
            logger.error("❌ Database operations test failed")
    else:
        logger.error("❌ Database connection test failed")

if __name__ == "__main__":
    asyncio.run(main())
