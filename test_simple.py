#!/usr/bin/env python3
import asyncio
import sys
sys.path.append('/home/pranav/Desktop/Hackathon/smartneed')

async def test_populate():
    try:
        from database.connection import init_database, get_products_collection
        print("🔗 Connecting to database...")
        await init_database()
        
        products_collection = await get_products_collection()
        print("✅ Got products collection")
        
        # Test insert
        test_product = {
            'name': 'Test Product',
            'brand': 'TestBrand',
            'category': 'Electronics',
            'price': 99.99,
            'rating': 4.5
        }
        
        result = await products_collection.insert_one(test_product)
        print(f"✅ Inserted product with ID: {result.inserted_id}")
        
        # Count products
        count = await products_collection.count_documents({})
        print(f"📊 Total products: {count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_populate())
