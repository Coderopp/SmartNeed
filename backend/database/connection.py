"""
MongoDB connection and database setup for SMARTNEED
Auto-falls back to mock database when real MongoDB is unavailable
"""

import logging
import os
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)

# Try to import MongoDB dependencies, fall back to None if not available
try:
    from motor.motor_asyncio import AsyncIOMotorClient
    from pymongo import IndexModel, TEXT
    MONGODB_AVAILABLE = True
except ImportError as e:
    logger.warning(f"MongoDB dependencies not available: {e}. Running in mock-only mode.")
    AsyncIOMotorClient = None
    IndexModel = None
    TEXT = None
    MONGODB_AVAILABLE = False

# Import mock database components
from .mock_connection import MockDatabase as ImportedMockDatabase, MockMongoDB as ImportedMockMongoDB

class MockDatabase:
    """Mock database for testing without actual MongoDB"""
    
    def __init__(self):
        self.collections = {}
        self._mock_data = {
            'products': [
                {
                    '_id': '507f1f77bcf86cd799439011',
                    'name': 'Sony WH-1000XM4 Wireless Headphones',
                    'brand': 'Sony',
                    'category': 'Electronics',
                    'price': 299.99,
                    'rating': 4.6,
                    'description': 'Industry-leading noise canceling headphones',
                    'features': ['Active Noise Canceling', '30-hour battery', 'Touch controls'],
                    'source': 'demo'
                },
                {
                    '_id': '507f1f77bcf86cd799439012',
                    'name': 'Apple MacBook Air M2',
                    'brand': 'Apple',
                    'category': 'Electronics',
                    'price': 1199.00,
                    'rating': 4.8,
                    'description': 'Powerful laptop with M2 chip',
                    'features': ['M2 chip', '8GB RAM', '256GB SSD'],
                    'source': 'demo'
                }
            ]
        }
    
    def __getattr__(self, name):
        if name not in self.collections:
            self.collections[name] = MockCollection(name, self._mock_data.get(name, []))
        return self.collections[name]
    
    async def command(self, cmd):
        return {"ok": 1}
    
    async def list_collection_names(self):
        return list(self.collections.keys())

class MockCollection:
    """Mock collection for testing"""
    
    def __init__(self, name, initial_data=None):
        self.name = name
        self.data = initial_data or []
    
    async def find_one(self, filter_dict=None):
        if not filter_dict:
            return self.data[0] if self.data else None
        return self.data[0] if self.data else None
    
    def find(self, filter_dict=None, projection=None):
        return MockCursor(self.data)
    
    async def insert_one(self, document):
        self.data.append(document)
        return MockInsertResult()
    
    async def update_one(self, filter_dict, update_dict, upsert=False):
        return MockUpdateResult()
    
    async def count_documents(self, filter_dict=None):
        return len(self.data)
    
    async def create_indexes(self, indexes):
        pass
    
    def aggregate(self, pipeline):
        return MockCursor(self.data)

class MockCursor:
    """Mock cursor for find operations"""
    
    def __init__(self, data):
        self.data = data
        self.index = 0
    
    async def to_list(self, length=None):
        return self.data[:length] if length else self.data
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.index >= len(self.data):
            raise StopAsyncIteration
        result = self.data[self.index]
        self.index += 1
        return result

class MockInsertResult:
    """Mock insert result"""
    def __init__(self):
        self.inserted_id = '507f1f77bcf86cd799439013'

class MockUpdateResult:
    """Mock update result"""
    def __init__(self):
        self.modified_count = 1

class MongoDB:
    """MongoDB connection and database manager with automatic mock fallback"""
    
    def __init__(self):
        self.client = None
        self.database = None
        self.is_mock = False
        self.mock_instance = None
        
    async def connect(self):
        """Connect to MongoDB with automatic fallback to mock"""
        # Check if mock mode is forced or MongoDB is not available
        force_mock = os.getenv("USE_MOCK_DATABASE", "false").lower() == "true"
        
        if force_mock or not MONGODB_AVAILABLE:
            if force_mock:
                logger.info("🔧 Mock database mode forced via USE_MOCK_DATABASE=true")
            else:
                logger.info("🔧 MongoDB dependencies not available, using mock database")
            await self._connect_mock()
            return
        
        # First try to connect to real MongoDB
        try:
            # MongoDB connection string
            mongo_url = os.getenv(
                "MONGODB_URL", 
                "mongodb://localhost:27017/smartneed"
            )
            
            self.client = AsyncIOMotorClient(mongo_url)
            self.database = self.client.smartneed
            
            # Test connection with a longer timeout
            await asyncio.wait_for(self.client.admin.command('ping'), timeout=30.0)
            logger.info("✅ Connected to real MongoDB successfully")
            
            # Create indexes
            await self._create_indexes()
            self.is_mock = False
            
        except Exception as e:
            logger.warning(f"⚠️  Failed to connect to real MongoDB: {e}")
            logger.info("🔄 Falling back to mock database for development...")
            await self._connect_mock()
    
    async def _connect_mock(self):
        """Connect to mock database"""
        self.mock_instance = ImportedMockMongoDB()
        await self.mock_instance.connect()
        self.database = self.mock_instance.database
        self.is_mock = True
        logger.info("✅ Mock database ready for development")
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.is_mock and self.mock_instance:
            await self.mock_instance.disconnect()
        elif self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    async def _create_indexes(self):
        """Create necessary indexes for optimal performance (real MongoDB only)"""
        if self.is_mock or not MONGODB_AVAILABLE:
            return  # Skip for mock database or when MongoDB is not available
            
        try:
            # Products collection indexes
            await self.database.products.create_indexes([
                IndexModel([("name", TEXT), ("description", TEXT), ("brand", TEXT)]),
                IndexModel([("category", 1)]),
                IndexModel([("price", 1)]),
                IndexModel([("rating", -1)]),
                IndexModel([("source", 1)]),
                IndexModel([("created_at", -1)]),
                IndexModel([("embedding_updated", 1)]),
            ])
            
            # Embeddings collection indexes
            await self.database.embeddings.create_indexes([
                IndexModel([("product_id", 1)], unique=True),
                IndexModel([("created_at", -1)]),
            ])
            
            # Search history indexes
            await self.database.search_history.create_indexes([
                IndexModel([("query", TEXT)]),
                IndexModel([("timestamp", -1)]),
                IndexModel([("user_session", 1)]),
            ])
            
            # User feedback indexes
            await self.database.user_feedback.create_indexes([
                IndexModel([("product_id", 1)]),
                IndexModel([("search_query", 1)]),
                IndexModel([("timestamp", -1)]),
            ])
            
            logger.info("✅ MongoDB indexes created successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to create indexes: {e}")

# Global MongoDB instance
mongodb = MongoDB()

async def get_database():
    """Get MongoDB database instance"""
    if not mongodb.database:
        await mongodb.connect()
    return mongodb.database

async def init_database():
    """Initialize database connection"""
    await mongodb.connect()

async def check_database_connection():
    """Check if database connection is healthy"""
    try:
        db = await get_database()
        await db.command('ping')
        return True
    except Exception:
        return False

async def get_products_collection():
    """Get products collection"""
    db = await get_database()
    return db.products

async def get_embeddings_collection():
    """Get embeddings collection"""
    db = await get_database()
    return db.embeddings

async def get_search_history_collection():
    """Get search history collection"""
    db = await get_database()
    return db.search_history

async def get_user_feedback_collection():
    """Get user feedback collection"""
    db = await get_database()
    return db.user_feedback

async def get_categories_collection():
    """Get categories collection"""
    db = await get_database()
    return db.categories

async def get_scraping_jobs_collection():
    """Get scraping jobs collection"""
    db = await get_database()
    return db.scraping_jobs
