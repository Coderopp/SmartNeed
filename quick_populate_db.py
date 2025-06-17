#!/usr/bin/env python3
"""
Quick Data Ingestion - Populate MongoDB with Real Product Data
"""

import asyncio
import sys
import random
from datetime import datetime

# Add project to path
sys.path.append('/home/pranav/Desktop/Hackathon/smartneed')

async def quick_data_ingestion():
    """Quick ingestion of realistic product data"""
    try:
        from database.connection import init_database, get_products_collection
        
        print("🚀 Starting Quick Data Ingestion...")
        
        # Initialize database
        await init_database()
        products_collection = await get_products_collection()
        
        # Clear existing products for fresh start
        await products_collection.delete_many({})
        print("🗑️ Cleared existing products")
        
        # Generate realistic product data
        products = [
            # Electronics - Headphones
            {
                'name': 'Sony WH-1000XM5 Wireless Noise Canceling Headphones',
                'brand': 'Sony',
                'category': 'Electronics',
                'price': 349.99,
                'original_price': 399.99,
                'rating': 4.7,
                'review_count': 2156,
                'description': 'Industry-leading noise canceling with Auto NC Optimizer, crystal clear hands-free calling, and 30-hour battery life.',
                'features': ['Active Noise Canceling', '30-hour battery', 'Quick Charge', 'Voice Assistant', 'Touch Controls'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://via.placeholder.com/400x400?text=Sony+WH-1000XM5',
                'product_url': 'https://www.sony.com/electronics/headband-headphones/wh-1000xm5',
                'sku': 'SONY-WH1000XM5-BLK',
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            },
            {
                'name': 'Apple AirPods Pro (2nd Generation)',
                'brand': 'Apple',
                'category': 'Electronics',
                'price': 249.99,
                'original_price': 279.99,
                'rating': 4.8,
                'review_count': 3421,
                'description': 'Active Noise Cancellation, Transparency mode, Spatial Audio, and up to 6 hours of listening time.',
                'features': ['Active Noise Cancellation', 'Transparency Mode', 'Spatial Audio', 'MagSafe Charging', 'Sweat Resistant'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://via.placeholder.com/400x400?text=AirPods+Pro+2',
                'product_url': 'https://www.apple.com/airpods-pro/',
                'sku': 'APPLE-AIRPODS-PRO2',
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            },
            {
                'name': 'Bose QuietComfort 45 Wireless Headphones',
                'brand': 'Bose',
                'category': 'Electronics',
                'price': 299.99,
                'original_price': 329.99,
                'rating': 4.6,
                'review_count': 1892,
                'description': 'Premium noise canceling headphones with TriPort acoustic architecture and 24-hour battery life.',
                'features': ['Noise Canceling', '24-hour battery', 'TriPort Acoustic', 'Lightweight', 'Voice Assistant'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://via.placeholder.com/400x400?text=Bose+QC45',
                'product_url': 'https://www.bose.com/en_us/products/headphones/over_ear_headphones/quietcomfort-45-headphones.html',
                'sku': 'BOSE-QC45-BLK',
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            },
            
            # Electronics - Laptops
            {
                'name': 'MacBook Air 15-inch M3',
                'brand': 'Apple',
                'category': 'Electronics',
                'price': 1299.99,
                'original_price': 1399.99,
                'rating': 4.9,
                'review_count': 847,
                'description': 'Incredibly thin and light laptop with M3 chip, 15.3-inch Liquid Retina display, and up to 18 hours of battery life.',
                'features': ['M3 chip', '15.3-inch Liquid Retina display', '18-hour battery', '8GB RAM', '256GB SSD'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://via.placeholder.com/400x400?text=MacBook+Air+15',
                'product_url': 'https://www.apple.com/macbook-air-15/',
                'sku': 'APPLE-MBA15-M3-256',
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            },
            {
                'name': 'Dell XPS 13 Plus',
                'brand': 'Dell',
                'category': 'Electronics',
                'price': 1199.99,
                'original_price': 1299.99,
                'rating': 4.5,
                'review_count': 1234,
                'description': 'Premium ultrabook with 13.4-inch OLED display, Intel Core i7, and edge-to-edge keyboard.',
                'features': ['Intel Core i7', '13.4-inch OLED', '16GB RAM', '512GB SSD', 'Edge-to-edge keyboard'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://via.placeholder.com/400x400?text=Dell+XPS+13',
                'product_url': 'https://www.dell.com/en-us/shop/dell-laptops/xps-13-plus-laptop/spd/xps-13-9320-laptop',
                'sku': 'DELL-XPS13-PLUS-I7',
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            },
            {
                'name': 'ASUS ROG Zephyrus G14',
                'brand': 'ASUS',
                'category': 'Electronics',
                'price': 1499.99,
                'original_price': 1699.99,
                'rating': 4.7,
                'review_count': 956,
                'description': 'Gaming laptop with AMD Ryzen 9, RTX 4060, and AniMe Matrix LED display on the lid.',
                'features': ['AMD Ryzen 9', 'RTX 4060', '16GB RAM', '1TB SSD', 'AniMe Matrix Display'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://via.placeholder.com/400x400?text=ASUS+ROG+G14',
                'product_url': 'https://rog.asus.com/laptops/13-14-inch/rog-zephyrus-g14-2023/',
                'sku': 'ASUS-ROG-G14-R9',
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            },
            
            # Electronics - Smartphones
            {
                'name': 'iPhone 15 Pro',
                'brand': 'Apple',
                'category': 'Electronics',
                'price': 999.99,
                'original_price': 1099.99,
                'rating': 4.8,
                'review_count': 5243,
                'description': 'Titanium design with A17 Pro chip, Pro camera system, and Action button.',
                'features': ['A17 Pro chip', 'Titanium design', 'Pro camera system', 'Action button', 'USB-C'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://via.placeholder.com/400x400?text=iPhone+15+Pro',
                'product_url': 'https://www.apple.com/iphone-15-pro/',
                'sku': 'APPLE-IP15PRO-128',
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            },
            {
                'name': 'Samsung Galaxy S24 Ultra',
                'brand': 'Samsung',
                'category': 'Electronics',
                'price': 1199.99,
                'original_price': 1299.99,
                'rating': 4.7,
                'review_count': 3876,
                'description': 'Premium smartphone with S Pen, 200MP camera, and AI-powered features.',
                'features': ['S Pen included', '200MP camera', 'AI features', '5000mAh battery', '12GB RAM'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://via.placeholder.com/400x400?text=Galaxy+S24+Ultra',
                'product_url': 'https://www.samsung.com/us/smartphones/galaxy-s24-ultra/',
                'sku': 'SAMSUNG-S24U-256',
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            },
            {
                'name': 'Google Pixel 8 Pro',
                'brand': 'Google',
                'category': 'Electronics',
                'price': 999.99,
                'original_price': 1099.99,
                'rating': 4.6,
                'review_count': 2134,
                'description': 'AI-powered smartphone with Magic Eraser, Real Tone, and 7 years of updates.',
                'features': ['Google Tensor G3', 'Magic Eraser', 'Real Tone', '7 years updates', 'Pro camera'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://via.placeholder.com/400x400?text=Pixel+8+Pro',
                'product_url': 'https://store.google.com/product/pixel_8_pro',
                'sku': 'GOOGLE-P8PRO-128',
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            },
            
            # Gaming
            {
                'name': 'PlayStation 5 Console',
                'brand': 'Sony',
                'category': 'Gaming',
                'price': 499.99,
                'original_price': 499.99,
                'rating': 4.8,
                'review_count': 4567,
                'description': 'Next-gen gaming console with lightning-fast SSD, ray tracing, and 4K gaming.',
                'features': ['4K gaming', 'Ray tracing', 'Lightning-fast SSD', 'DualSense controller', '3D Audio'],
                'source': 'data_ingestion',
                'availability': 'limited_stock',
                'image_url': 'https://via.placeholder.com/400x400?text=PlayStation+5',
                'product_url': 'https://www.playstation.com/en-us/ps5/',
                'sku': 'SONY-PS5-CONSOLE',
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            },
            {
                'name': 'Xbox Series X',
                'brand': 'Microsoft',
                'category': 'Gaming',
                'price': 499.99,
                'original_price': 499.99,
                'rating': 4.7,
                'review_count': 3421,
                'description': 'Most powerful Xbox ever with 4K gaming, Smart Delivery, and Game Pass.',
                'features': ['4K 120fps', 'Smart Delivery', '1TB SSD', 'Game Pass', 'Quick Resume'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://via.placeholder.com/400x400?text=Xbox+Series+X',
                'product_url': 'https://www.xbox.com/en-US/consoles/xbox-series-x',
                'sku': 'MICROSOFT-XBSX-1TB',
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            },
            
            # Home & Garden
            {
                'name': 'Dyson V15 Detect Cordless Vacuum',
                'brand': 'Dyson',
                'category': 'Home & Garden',
                'price': 649.99,
                'original_price': 749.99,
                'rating': 4.5,
                'review_count': 1876,
                'description': 'Cordless vacuum with laser detection, LCD screen, and up to 60 minutes of runtime.',
                'features': ['Laser detection', 'LCD screen', '60-min runtime', 'HEPA filtration', 'Lightweight'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://via.placeholder.com/400x400?text=Dyson+V15',
                'product_url': 'https://www.dyson.com/vacuum-cleaners/cordless/v15/detect',
                'sku': 'DYSON-V15-DETECT',
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            },
            {
                'name': 'Instant Pot Duo 7-in-1 Electric Pressure Cooker',
                'brand': 'Instant Pot',
                'category': 'Home & Garden',
                'price': 79.99,
                'original_price': 99.99,
                'rating': 4.6,
                'review_count': 12456,
                'description': '7-in-1 multi-cooker: pressure cooker, slow cooker, rice cooker, steamer, sauté, yogurt maker, and warmer.',
                'features': ['7-in-1 functionality', '6 quart capacity', '14 smart programs', 'Safe and easy', 'Stainless steel'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://via.placeholder.com/400x400?text=Instant+Pot',
                'product_url': 'https://instantpot.com/products/instant-pot-duo-7-in-1',
                'sku': 'INSTANT-DUO-6QT',
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
        ]
        
        # Insert products
        result = await products_collection.insert_many(products)
        print(f"✅ Inserted {len(result.inserted_ids)} products into database")
        
        # Verify insertion
        total_count = await products_collection.count_documents({})
        print(f"📊 Total products in database: {total_count}")
        
        # Show sample products by category
        categories = ['Electronics', 'Gaming', 'Home & Garden']
        for category in categories:
            count = await products_collection.count_documents({'category': category})
            print(f"   📱 {category}: {count} products")
        
        print("🎉 Quick data ingestion completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Data ingestion failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(quick_data_ingestion())
