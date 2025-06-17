#!/usr/bin/env python3
"""
FINAL DATA INGESTION - Populate SmartNeed Database
"""

import asyncio
import sys
from datetime import datetime

sys.path.append('/home/pranav/Desktop/Hackathon/smartneed')

async def populate_database():
    """Populate database with comprehensive product data"""
    try:
        from database.connection import init_database, get_products_collection
        
        print("🚀 SMARTNEED - Final Data Ingestion")
        print("=" * 50)
        
        # Initialize database
        await init_database()
        products_collection = await get_products_collection()
        
        # Clear existing data for fresh start
        print("🗑️ Clearing existing products...")
        try:
            # Use delete_one in a loop since delete_many might not be implemented
            count = 0
            while True:
                result = await products_collection.delete_one({})
                if result.deleted_count == 0:
                    break
                count += 1
            print(f"🗑️ Cleared {count} existing products")
        except:
            print("🗑️ Database cleared (or was already empty)")
        
        # Real product data for ingestion
        real_products = [
            # HEADPHONES & AUDIO
            {
                'name': 'Sony WH-1000XM5 Wireless Noise Canceling Headphones',
                'brand': 'Sony',
                'category': 'Electronics',
                'price': 349.99,
                'original_price': 399.99,
                'rating': 4.7,
                'review_count': 2156,
                'description': 'Industry-leading noise canceling with Auto NC Optimizer, crystal clear hands-free calling, and 30-hour battery life. Two processors control 8 microphones for unprecedented noise canceling quality.',
                'features': ['Active Noise Canceling', '30-hour battery', 'Quick Charge (3min = 3hrs)', 'Voice Assistant', 'Touch Controls', 'Multi-device pairing'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://m.media-amazon.com/images/I/51QeA1zZ1ML._AC_SL1500_.jpg',
                'product_url': 'https://www.sony.com/electronics/headband-headphones/wh-1000xm5',
                'sku': 'SONY-WH1000XM5-BLACK',
                'specifications': {
                    'connectivity': 'Bluetooth 5.2, USB-C',
                    'weight': '250g',
                    'driver_size': '30mm',
                    'frequency_response': '4Hz-40kHz'
                }
            },
            {
                'name': 'Apple AirPods Pro (2nd Generation)',
                'brand': 'Apple',
                'category': 'Electronics',
                'price': 249.99,
                'original_price': 279.99,
                'rating': 4.8,
                'review_count': 3421,
                'description': 'Active Noise Cancellation that blocks outside noise. Transparency mode that lets outside sound in. Spatial Audio with dynamic head tracking.',
                'features': ['Active Noise Cancellation', 'Transparency Mode', 'Spatial Audio', 'MagSafe Charging', 'Sweat & Water Resistant (IPX4)', 'Find My support'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/MQD83?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=1660803972361',
                'product_url': 'https://www.apple.com/airpods-pro/',
                'sku': 'APPLE-AIRPODS-PRO2-WHITE'
            },
            {
                'name': 'Bose QuietComfort 45 Wireless Headphones',
                'brand': 'Bose',
                'category': 'Electronics',
                'price': 299.99,
                'original_price': 329.99,
                'rating': 4.6,
                'review_count': 1892,
                'description': 'Premium noise canceling headphones with TriPort acoustic architecture for deep, clear sound and up to 24 hours of battery life.',
                'features': ['Noise Canceling', '24-hour battery', 'TriPort Acoustic Architecture', 'Lightweight comfort', 'Voice Assistant', 'Multi-device pairing'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://assets.bose.com/content/dam/cloudassets/Bose_DAM/Web/consumer_electronics/global/products/headphones/qc45/product_silo_images/QC45_PDP_Ecom-Gallery-B02.jpg',
                'product_url': 'https://www.bose.com/en_us/products/headphones/over_ear_headphones/quietcomfort-45-headphones.html',
                'sku': 'BOSE-QC45-BLACK'
            },
            
            # LAPTOPS
            {
                'name': 'MacBook Air 15-inch with M3 chip',
                'brand': 'Apple',
                'category': 'Electronics',
                'price': 1299.99,
                'original_price': 1399.99,
                'rating': 4.9,
                'review_count': 847,
                'description': 'Incredibly thin and light laptop with M3 chip, 15.3-inch Liquid Retina display, up to 18 hours of battery life, and a silent, fanless design.',
                'features': ['M3 chip (8-core CPU)', '15.3-inch Liquid Retina display', '18-hour battery life', '8GB unified memory', '256GB SSD storage', 'Silent fanless design'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/mba15-midnight-select-202306?wid=904&hei=840&fmt=jpeg&qlt=90&.v=1684340990559',
                'product_url': 'https://www.apple.com/macbook-air-15/',
                'sku': 'APPLE-MBA15-M3-256GB-MIDNIGHT'
            },
            {
                'name': 'Dell XPS 13 Plus',
                'brand': 'Dell',
                'category': 'Electronics',
                'price': 1199.99,
                'original_price': 1299.99,
                'rating': 4.5,
                'review_count': 1234,
                'description': 'Premium 13.4-inch laptop with stunning OLED display, Intel 12th Gen processors, and edge-to-edge keyboard with haptic feedback.',
                'features': ['Intel Core i7-1260P', '13.4-inch OLED (3456x2160)', '16GB LPDDR5 RAM', '512GB PCIe SSD', 'Edge-to-edge keyboard', 'Haptic touchpad'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://i.dell.com/is/image/DellContent/content/dam/ss2/product-images/dell-client-products/notebooks/xps-notebooks/xps-13-9320/media-gallery/notebook-xps-13-9320-t-sl-gallery-504x350.psd',
                'product_url': 'https://www.dell.com/en-us/shop/dell-laptops/xps-13-plus-laptop/spd/xps-13-9320-laptop',
                'sku': 'DELL-XPS13PLUS-I7-OLED'
            },
            {
                'name': 'ASUS ROG Zephyrus G14 Gaming Laptop',
                'brand': 'ASUS',
                'category': 'Electronics',
                'price': 1499.99,
                'original_price': 1699.99,
                'rating': 4.7,
                'review_count': 956,
                'description': 'Compact gaming powerhouse with AMD Ryzen 9 7940HS, RTX 4060, and the iconic AniMe Matrix LED display on the lid.',
                'features': ['AMD Ryzen 9 7940HS', 'NVIDIA RTX 4060', '16GB DDR5 RAM', '1TB PCIe 4.0 SSD', 'AniMe Matrix LED Display', '14-inch QHD+ 165Hz display'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://dlcdnwebimgs.asus.com/gain/A1BB8B00-F15A-4F3F-87F8-6C2A146D00EE/w800/h800',
                'product_url': 'https://rog.asus.com/laptops/13-14-inch/rog-zephyrus-g14-2023/',
                'sku': 'ASUS-ROG-G14-R9-RTX4060'
            },
            
            # SMARTPHONES
            {
                'name': 'iPhone 15 Pro',
                'brand': 'Apple',
                'category': 'Electronics',
                'price': 999.99,
                'original_price': 1099.99,
                'rating': 4.8,
                'review_count': 5243,
                'description': 'Titanium smartphone with A17 Pro chip, advanced Pro camera system, Action button, and USB-C connectivity.',
                'features': ['A17 Pro chip', 'Titanium design', 'Pro camera system (48MP)', 'Action button', 'USB-C connector', '128GB storage'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-pro-finish-select-202309-6-1inch-naturaltitanium?wid=5120&hei=2880&fmt=p-jpg&qlt=80&.v=1692895395658',
                'product_url': 'https://www.apple.com/iphone-15-pro/',
                'sku': 'APPLE-IP15PRO-128GB-NATURAL'
            },
            {
                'name': 'Samsung Galaxy S24 Ultra',
                'brand': 'Samsung',
                'category': 'Electronics',
                'price': 1199.99,
                'original_price': 1299.99,
                'rating': 4.7,
                'review_count': 3876,
                'description': 'Premium Android smartphone with S Pen, 200MP camera with AI zoom, and powerful Snapdragon 8 Gen 3 processor.',
                'features': ['Snapdragon 8 Gen 3', 'S Pen included', '200MP main camera', 'AI-powered features', '5000mAh battery', '256GB storage'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://images.samsung.com/is/image/samsung/p6pim/us/2401/gallery/us-galaxy-s24-s928-sm-s928uzaaxaa-539572200',
                'product_url': 'https://www.samsung.com/us/smartphones/galaxy-s24-ultra/',
                'sku': 'SAMSUNG-S24ULTRA-256GB-TITANIUM'
            },
            {
                'name': 'Google Pixel 8 Pro',
                'brand': 'Google',
                'category': 'Electronics',
                'price': 999.99,
                'original_price': 1099.99,
                'rating': 4.6,
                'review_count': 2134,
                'description': 'AI-powered smartphone with Google Tensor G3, Magic Eraser, Real Tone photography, and 7 years of software updates.',
                'features': ['Google Tensor G3', 'AI Magic Eraser', 'Real Tone camera', '7 years of updates', 'Pro camera features', '128GB storage'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://lh3.googleusercontent.com/BKsrOKUqOcJK2jyBGnLWGJhJTSuLyEjKQRHrmA5zVKMFaNxfT7OTlGSwUEYZDyGUOjLfCQFINWWNYXOOPd7LUlCh-KkJcR-_RA',
                'product_url': 'https://store.google.com/product/pixel_8_pro',
                'sku': 'GOOGLE-PIXEL8PRO-128GB-OBSIDIAN'
            },
            
            # GAMING CONSOLES
            {
                'name': 'PlayStation 5 Console',
                'brand': 'Sony',
                'category': 'Gaming',
                'price': 499.99,
                'original_price': 499.99,
                'rating': 4.8,
                'review_count': 4567,
                'description': 'Next-generation gaming console with lightning-fast SSD, ray tracing graphics, haptic feedback, and 4K gaming capabilities.',
                'features': ['4K gaming at 120fps', 'Ray tracing technology', 'Lightning-fast SSD', 'DualSense haptic controller', '3D Audio technology', '825GB SSD storage'],
                'source': 'data_ingestion',
                'availability': 'limited_stock',
                'image_url': 'https://gmedia.playstation.com/is/image/SIEPDC/ps5-product-thumbnail-01-en-14sep21',
                'product_url': 'https://www.playstation.com/en-us/ps5/',
                'sku': 'SONY-PS5-CONSOLE-STANDARD'
            },
            {
                'name': 'Xbox Series X',
                'brand': 'Microsoft',
                'category': 'Gaming',
                'price': 499.99,
                'original_price': 499.99,
                'rating': 4.7,
                'review_count': 3421,
                'description': 'Most powerful Xbox console with 12 teraflops, Smart Delivery, Quick Resume, and backwards compatibility.',
                'features': ['12 teraflops GPU', '4K gaming at 120fps', 'Smart Delivery', 'Quick Resume', '1TB custom SSD', 'Backwards compatibility'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://assets.xboxservices.com/assets/fb/d2/fbd2cb53-5c15-4493-9fb6-84db2abb4d00.jpg',
                'product_url': 'https://www.xbox.com/en-US/consoles/xbox-series-x',
                'sku': 'MICROSOFT-XBSX-1TB-BLACK'
            },
            {
                'name': 'Nintendo Switch OLED Model',
                'brand': 'Nintendo',
                'category': 'Gaming',
                'price': 349.99,
                'original_price': 349.99,
                'rating': 4.8,
                'review_count': 2987,
                'description': 'Portable gaming console with vibrant 7-inch OLED screen, enhanced audio, and the flexibility to play anywhere.',
                'features': ['7-inch OLED screen', 'Enhanced audio', 'Portable and docked gaming', 'Joy-Con controllers', '64GB internal storage', 'Enhanced kickstand'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://assets.nintendo.com/image/upload/ar_16:9,c_lpad,w_1240/b_white/f_auto/q_auto/ncom/software/switch/70010000000025/7137262b5a64d921e193653f8aa0b722925abc5680380ca0e18a5cfd91697f58',
                'product_url': 'https://www.nintendo.com/us/store/products/nintendo-switch-oled-model/',
                'sku': 'NINTENDO-SWITCH-OLED-WHITE'
            },
            
            # HOME & KITCHEN
            {
                'name': 'Dyson V15 Detect Cordless Vacuum',
                'brand': 'Dyson',
                'category': 'Home & Garden',
                'price': 649.99,
                'original_price': 749.99,
                'rating': 4.5,
                'review_count': 1876,
                'description': 'Advanced cordless vacuum with laser dust detection, LCD screen showing particle count, and up to 60 minutes of runtime.',
                'features': ['Laser dust detection', 'LCD particle counter', 'Up to 60-min runtime', 'HEPA filtration', 'Lightweight design', '14 cleaning tools'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://dyson-h.assetsadobe2.com/is/image/content/dam/dyson/products/vacuum-cleaners/372536-01.jpg',
                'product_url': 'https://www.dyson.com/vacuum-cleaners/cordless/v15/detect',
                'sku': 'DYSON-V15-DETECT-YELLOW'
            },
            {
                'name': 'Instant Pot Duo 7-in-1 Electric Pressure Cooker',
                'brand': 'Instant Pot',
                'category': 'Home & Garden',
                'price': 79.99,
                'original_price': 99.99,
                'rating': 4.6,
                'review_count': 12456,
                'description': 'Multi-functional electric pressure cooker that combines 7 appliances in one: pressure cooker, slow cooker, rice cooker, steamer, sauté pan, yogurt maker, and warmer.',
                'features': ['7-in-1 functionality', '6-quart capacity', '14 smart programs', 'Stainless steel cooking pot', 'Easy-seal lid', 'Dishwasher safe'],
                'source': 'data_ingestion',
                'availability': 'in_stock',
                'image_url': 'https://instantpot.com/wp-content/uploads/2022/09/IP-Duo-7in1-6qt-Stainless-Steel-Hero-1080x1080-1.png',
                'product_url': 'https://instantpot.com/products/instant-pot-duo-7-in-1',
                'sku': 'INSTANTPOT-DUO-6QT-STEEL'
            }
        ]
        
        # Insert products one by one with progress
        print(f"📦 Inserting {len(real_products)} products...")
        inserted_count = 0
        
        for i, product in enumerate(real_products, 1):
            try:
                # Add timestamp
                product['created_at'] = datetime.utcnow().isoformat()
                product['updated_at'] = datetime.utcnow().isoformat()
                
                result = await products_collection.insert_one(product)
                inserted_count += 1
                print(f"   ✅ {i:2d}/{len(real_products)} - {product['name'][:50]}...")
                
            except Exception as e:
                print(f"   ❌ Failed to insert {product['name']}: {e}")
        
        print("=" * 50)
        print(f"🎉 Data Ingestion Complete!")
        print(f"📊 Successfully inserted: {inserted_count}/{len(real_products)} products")
        
        # Verify final count
        total_count = await products_collection.count_documents({})
        print(f"📋 Total products in database: {total_count}")
        
        # Show breakdown by category
        categories = ['Electronics', 'Gaming', 'Home & Garden']
        for category in categories:
            count = await products_collection.count_documents({'category': category})
            print(f"   📱 {category}: {count} products")
        
        # Show breakdown by brand
        print("\n🏷️ Products by Brand:")
        brands = ['Apple', 'Sony', 'Samsung', 'Microsoft', 'Google', 'Dell', 'ASUS', 'Bose', 'Nintendo', 'Dyson']
        for brand in brands:
            count = await products_collection.count_documents({'brand': brand})
            if count > 0:
                print(f"   🔖 {brand}: {count} products")
        
        print("\n✅ Database is now populated with real product data!")
        print("🚀 Ready to test the SmartNeed application!")
        
        return True
        
    except Exception as e:
        print(f"❌ Data ingestion failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(populate_database())
