"""
Mock database connection for development and testing
Provides a fallback when MongoDB is not available
"""

import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class MockCollection:
    """Mock MongoDB collection"""
    
    def __init__(self, name: str, initial_data: List[Dict] = None):
        self.name = name
        self.data = initial_data or []
        
    async def find_one(self, filter_dict: Dict = None, projection: Dict = None):
        """Find one document"""
        if not self.data:
            return None
        if not filter_dict:
            return self.data[0]
        # Simple filter implementation
        for doc in self.data:
            if self._matches_filter(doc, filter_dict):
                return doc
        return None
    
    def find(self, filter_dict: Dict = None, projection: Dict = None):
        """Find multiple documents"""
        filtered_data = self.data
        if filter_dict:
            filtered_data = [doc for doc in self.data if self._matches_filter(doc, filter_dict)]
        return MockCursor(filtered_data)
    
    async def insert_one(self, document: Dict):
        """Insert one document"""
        doc_copy = document.copy()
        if '_id' not in doc_copy:
            doc_copy['_id'] = f"mock_id_{len(self.data) + 1}"
        self.data.append(doc_copy)
        return MockInsertResult(doc_copy['_id'])
    
    async def insert_many(self, documents: List[Dict]):
        """Insert multiple documents"""
        inserted_ids = []
        for doc in documents:
            result = await self.insert_one(doc)
            inserted_ids.append(result.inserted_id)
        return MockInsertManyResult(inserted_ids)
    
    async def update_one(self, filter_dict: Dict, update_dict: Dict, upsert: bool = False):
        """Update one document"""
        for i, doc in enumerate(self.data):
            if self._matches_filter(doc, filter_dict):
                if '$set' in update_dict:
                    doc.update(update_dict['$set'])
                elif '$inc' in update_dict:
                    for key, value in update_dict['$inc'].items():
                        doc[key] = doc.get(key, 0) + value
                else:
                    doc.update(update_dict)
                return MockUpdateResult(1)
        
        if upsert:
            new_doc = filter_dict.copy()
            if '$set' in update_dict:
                new_doc.update(update_dict['$set'])
            await self.insert_one(new_doc)
            return MockUpdateResult(0, 1)
        
        return MockUpdateResult(0)
    
    async def delete_one(self, filter_dict: Dict):
        """Delete one document"""
        for i, doc in enumerate(self.data):
            if self._matches_filter(doc, filter_dict):
                del self.data[i]
                return MockDeleteResult(1)
        return MockDeleteResult(0)
    
    async def delete_many(self, filter_dict: Dict):
        """Delete multiple documents"""
        deleted_count = 0
        # Work backwards to avoid index issues
        for i in range(len(self.data) - 1, -1, -1):
            if self._matches_filter(self.data[i], filter_dict):
                del self.data[i]
                deleted_count += 1
        return MockDeleteResult(deleted_count)
    
    async def count_documents(self, filter_dict: Dict = None):
        """Count documents"""
        if not filter_dict:
            return len(self.data)
        count = 0
        for doc in self.data:
            if self._matches_filter(doc, filter_dict):
                count += 1
        return count
    
    async def create_indexes(self, indexes):
        """Create indexes (no-op for mock)"""
        logger.info(f"Mock: Creating indexes for {self.name} collection")
        pass
    
    def aggregate(self, pipeline: List[Dict]):
        """Aggregate (simplified)"""
        # Simple aggregation - just return all data for now
        return MockCursor(self.data)
    
    def _matches_filter(self, doc: Dict, filter_dict: Dict) -> bool:
        """Simple filter matching"""
        for key, value in filter_dict.items():
            if key not in doc:
                return False
            if isinstance(value, dict):
                # Handle operators like $in, $gt, etc.
                if '$in' in value:
                    if doc[key] not in value['$in']:
                        return False
                elif '$gt' in value:
                    if not (doc[key] > value['$gt']):
                        return False
                elif '$lt' in value:
                    if not (doc[key] < value['$lt']):
                        return False
                elif '$regex' in value:
                    import re
                    if not re.search(value['$regex'], str(doc[key]), re.IGNORECASE):
                        return False
            else:
                if doc[key] != value:
                    return False
        return True

class MockCursor:
    """Mock MongoDB cursor"""
    
    def __init__(self, data: List[Dict]):
        self.data = data
        self.index = 0
    
    async def to_list(self, length: Optional[int] = None):
        """Convert cursor to list"""
        if length is not None:
            return self.data[:length]
        return self.data
    
    def limit(self, count: int):
        """Limit results"""
        self.data = self.data[:count]
        return self
    
    def skip(self, count: int):
        """Skip results"""
        self.data = self.data[count:]
        return self
    
    def sort(self, key_or_list, direction=1):
        """Sort results"""
        if isinstance(key_or_list, str):
            reverse = direction == -1
            self.data.sort(key=lambda x: x.get(key_or_list, 0), reverse=reverse)
        return self
    
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
    def __init__(self, inserted_id):
        self.inserted_id = inserted_id

class MockInsertManyResult:
    """Mock insert many result"""
    def __init__(self, inserted_ids):
        self.inserted_ids = inserted_ids

class MockUpdateResult:
    """Mock update result"""
    def __init__(self, matched_count, modified_count=None):
        self.matched_count = matched_count
        self.modified_count = modified_count if modified_count is not None else matched_count
        self.upserted_id = None

class MockDeleteResult:
    """Mock delete result"""
    def __init__(self, deleted_count):
        self.deleted_count = deleted_count

class MockDatabase:
    """Mock MongoDB database"""
    
    def __init__(self):
        self.collections = {}
        self._initialize_mock_data()
    
    def _initialize_mock_data(self):
        """Initialize with sample data"""
        sample_products = [
            {
                '_id': '507f1f77bcf86cd799439011',
                'name': 'Sony WH-1000XM4 Wireless Headphones',
                'brand': 'Sony',
                'category': 'Electronics',
                'price': 299.99,
                'original_price': 349.99,
                'rating': 4.6,
                'review_count': 1524,
                'description': 'Industry-leading noise canceling headphones with 30-hour battery life',
                'features': ['Active Noise Canceling', '30-hour battery', 'Touch controls', 'Quick Charge'],
                'source': 'mock_data',
                'availability': 'in_stock',
                'image_url': 'https://example.com/sony-headphones.jpg'
            },
            {
                '_id': '507f1f77bcf86cd799439012',
                'name': 'Apple MacBook Air M2',
                'brand': 'Apple',
                'category': 'Electronics',
                'price': 1199.00,
                'original_price': 1299.00,
                'rating': 4.8,
                'review_count': 892,
                'description': 'Powerful laptop with M2 chip, perfect for work and creativity',
                'features': ['M2 chip', '8GB RAM', '256GB SSD', 'Retina display'],
                'source': 'mock_data',
                'availability': 'in_stock',
                'image_url': 'https://example.com/macbook-air.jpg'
            },
            {
                '_id': '507f1f77bcf86cd799439013',
                'name': 'Samsung Galaxy S24 Ultra',
                'brand': 'Samsung',
                'category': 'Electronics',
                'price': 1199.99,
                'original_price': 1299.99,
                'rating': 4.7,
                'review_count': 2156,
                'description': 'Latest flagship smartphone with S Pen and advanced camera system',
                'features': ['S Pen included', '200MP camera', '5000mAh battery', '12GB RAM'],
                'source': 'mock_data',
                'availability': 'in_stock',
                'image_url': 'https://example.com/galaxy-s24.jpg'
            }
        ]
        
        self.collections['products'] = MockCollection('products', sample_products)
        self.collections['embeddings'] = MockCollection('embeddings', [])
        self.collections['search_history'] = MockCollection('search_history', [])
        self.collections['user_feedback'] = MockCollection('user_feedback', [])
        self.collections['categories'] = MockCollection('categories', [])
        self.collections['scraping_jobs'] = MockCollection('scraping_jobs', [])
    
    def __getattr__(self, name):
        """Get collection by name"""
        if name not in self.collections:
            self.collections[name] = MockCollection(name)
        return self.collections[name]
    
    async def command(self, cmd):
        """Execute database command"""
        if cmd == 'ping':
            return {"ok": 1}
        return {"ok": 1}
    
    async def list_collection_names(self):
        """List collection names"""
        return list(self.collections.keys())

class MockMongoDB:
    """Mock MongoDB connection manager"""
    
    def __init__(self):
        self.database = None
        self.connected = False
    
    async def connect(self):
        """Connect to mock database"""
        self.database = MockDatabase()
        self.connected = True
        logger.info("✅ Mock MongoDB connected")
    
    async def disconnect(self):
        """Disconnect from mock database"""
        self.connected = False
        logger.info("Mock MongoDB disconnected")
