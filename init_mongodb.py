#!/usr/bin/env python3
"""
MongoDB initialization and testing script for SMARTNEED
"""

import asyncio
import logging
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config/api_keys.env')

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.connection import mongodb, get_database, get_products_collection
from database.models import ProductModel, ProductEmbeddingModel, CategoryModel
from services.data_ingestion.data_processor import DataProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_connection():
    """Test MongoDB connection"""
    try:
        logger.info("Testing MongoDB connection...")
        await mongodb.connect()
        db = await get_database()
        
        # Test with a simple ping
        await db.command('ping')
        logger.info("✅ MongoDB connection successful!")
        
        # List collections
        collections = await db.list_collection_names()
        logger.info(f"Available collections: {collections}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        return False

async def create_sample_data():
    """Create sample product data for testing"""
    try:
        logger.info("Creating sample product data...")
        
        # Sample products
        sample_products = [
            {
                "name": "Sony WH-1000XM4 Wireless Noise Canceling Headphones",
                "brand": "Sony",
                "category": "Electronics",
                "subcategory": "Audio",
                "price": 299.99,
                "original_price": 349.99,
                "currency": "USD",
                "description": "Industry-leading noise canceling with Dual Noise Sensor technology. Premium sound quality with 30-hour battery life.",
                "features": [
                    "Active Noise Canceling",
                    "30-hour battery life",
                    "Quick Charge",
                    "Touch controls",
                    "Voice Assistant compatible"
                ],
                "specifications": {
                    "driver_size": "40mm",
                    "frequency_response": "4Hz-40kHz",
                    "weight": "254g",
                    "connectivity": "Bluetooth 5.0, NFC"
                },
                "rating": 4.6,
                "review_count": 12453,
                "availability": True,
                "source": "demo",
                "source_id": "sony-wh1000xm4-001",
                "tags": ["wireless", "noise-canceling", "premium", "sony"]
            },
            {
                "name": "Apple MacBook Air M2 13-inch",
                "brand": "Apple",
                "category": "Electronics",
                "subcategory": "Computers",
                "price": 1199.00,
                "currency": "USD",
                "description": "Supercharged by the M2 chip, the redesigned MacBook Air combines incredible performance and up to 18 hours of battery life.",
                "features": [
                    "M2 chip with 8-core CPU",
                    "8GB unified memory",
                    "256GB SSD storage",
                    "13.6-inch Liquid Retina display",
                    "1080p FaceTime HD camera"
                ],
                "specifications": {
                    "processor": "Apple M2 chip",
                    "memory": "8GB",
                    "storage": "256GB SSD",
                    "display": "13.6-inch Liquid Retina",
                    "weight": "2.7 pounds"
                },
                "rating": 4.8,
                "review_count": 3421,
                "availability": True,
                "source": "demo",
                "source_id": "apple-macbook-air-m2-001",
                "tags": ["laptop", "apple", "m2", "portable", "premium"]
            },
            {
                "name": "Nike Air Max 270 Running Shoes",
                "brand": "Nike",
                "category": "Shoes",
                "subcategory": "Athletic",
                "price": 150.00,
                "currency": "USD",
                "description": "Nike's biggest heel Air unit yet delivers the bouncy, responsive feel you need to take on any run.",
                "features": [
                    "Large Air unit in heel",
                    "Engineered mesh upper",
                    "Comfortable fit",
                    "Durable rubber outsole"
                ],
                "specifications": {
                    "upper_material": "Engineered mesh",
                    "sole_material": "Rubber",
                    "closure": "Lace-up",
                    "heel_height": "Medium"
                },
                "rating": 4.3,
                "review_count": 8967,
                "availability": True,
                "source": "demo",
                "source_id": "nike-air-max-270-001",
                "tags": ["running", "nike", "air-max", "athletic", "comfortable"]
            }
        ]
        
        # Process and store sample products
        processor = DataProcessor()
        stats = await processor.process_batch(sample_products)
        
        logger.info(f"✅ Sample data created: {stats}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to create sample data: {e}")
        return False

async def test_search():
    """Test product search functionality"""
    try:
        logger.info("Testing product search...")
        
        products_collection = await get_products_collection()
        
        # Test text search
        cursor = products_collection.find(
            {"$text": {"$search": "wireless headphones"}},
            {"name": 1, "price": 1, "brand": 1}
        )
        
        products = await cursor.to_list(length=10)
        logger.info(f"Found {len(products)} products for 'wireless headphones'")
        
        for product in products:
            logger.info(f"  - {product['name']} by {product.get('brand', 'Unknown')} - ${product['price']}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Search test failed: {e}")
        return False

async def get_database_stats():
    """Get database statistics"""
    try:
        logger.info("Getting database statistics...")
        
        db = await get_database()
        
        # Get collection counts
        collections_stats = {}
        for collection_name in ['products', 'embeddings', 'search_history', 'user_feedback', 'categories']:
            try:
                count = await db[collection_name].count_documents({})
                collections_stats[collection_name] = count
            except Exception:
                collections_stats[collection_name] = 0
        
        logger.info("Database Statistics:")
        for collection, count in collections_stats.items():
            logger.info(f"  {collection}: {count} documents")
        
        # Get database size info
        stats = await db.command("dbStats")
        logger.info(f"Database size: {stats.get('dataSize', 0) / 1024 / 1024:.2f} MB")
        
        return collections_stats
        
    except Exception as e:
        logger.error(f"❌ Failed to get database stats: {e}")
        return {}

async def main():
    """Main initialization function"""
    logger.info("🚀 Starting SMARTNEED MongoDB initialization...")
    
    # Test connection
    if not await test_connection():
        logger.error("Cannot proceed without database connection")
        return False
    
    # Get current stats
    initial_stats = await get_database_stats()
    
    # Create sample data if database is empty
    if initial_stats.get('products', 0) == 0:
        logger.info("Database appears empty, creating sample data...")
        await create_sample_data()
    else:
        logger.info("Database contains existing data, skipping sample data creation")
    
    # Test search functionality
    await test_search()
    
    # Get final stats
    final_stats = await get_database_stats()
    
    logger.info("✅ MongoDB initialization completed successfully!")
    logger.info("🎯 SMARTNEED is ready to use with MongoDB!")
    
    # Cleanup
    await mongodb.disconnect()
    
    return True

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        if result:
            print("\n✅ Initialization completed successfully!")
            print("You can now start the backend server with: python -m backend.app.main")
        else:
            print("\n❌ Initialization failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Initialization interrupted by user")
    except Exception as e:
        print(f"\n❌ Initialization failed with error: {e}")
        sys.exit(1)
