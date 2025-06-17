#!/usr/bin/env python3
"""
Test Real MongoDB Atlas Connection
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Add project to path
sys.path.append('/home/pranav/Desktop/Hackathon/smartneed')

# Load environment variables
load_dotenv('config/.env')

async def test_real_mongodb():
    """Test direct connection to MongoDB Atlas"""
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        
        mongo_url = os.getenv("MONGODB_URL")
        print(f"🔗 Testing MongoDB Atlas connection...")
        print(f"   URL: {mongo_url[:50]}...")
        
        # Create client with longer timeout
        client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=30000)
        
        # Test connection
        print("🏥 Testing connection...")
        await client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        
        # Test database access
        db = client.smartneed
        print("📊 Testing database access...")
        
        # List collections
        collections = await db.list_collection_names()
        print(f"📋 Collections: {collections}")
        
        # Test products collection
        products = db.products
        count = await products.count_documents({})
        print(f"📦 Current products in database: {count}")
        
        # Insert test document
        test_doc = {'test': True, 'timestamp': '2024-06-17'}
        result = await products.insert_one(test_doc)
        print(f"✅ Test insert successful: {result.inserted_id}")
        
        # Remove test document
        await products.delete_one({'_id': result.inserted_id})
        print("✅ Test document removed")
        
        client.close()
        print("🎉 MongoDB Atlas connection test SUCCESSFUL!")
        return True
        
    except Exception as e:
        print(f"❌ MongoDB Atlas connection FAILED: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_real_mongodb())
