"""
Data ingestion and processing service for SMARTNEED
Handles product data cleaning, validation, and storage in MongoDB
"""

import logging
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import re
import sys
import os

# Add the parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.connection import get_products_collection, get_categories_collection
from database.models import ProductModel, CategoryModel

logger = logging.getLogger(__name__)

class DataProcessor:
    """Service for processing and ingesting product data"""
    
    def __init__(self):
        """Initialize data processor"""
        self.products_collection = None
        self.categories_collection = None
        logger.info("Data processor initialized")
    
    async def _init_collections(self):
        """Initialize database collections"""
        if not self.products_collection:
            self.products_collection = await get_products_collection()
        if not self.categories_collection:
            self.categories_collection = await get_categories_collection()
    
    async def process_product_data(self, raw_product: Dict[str, Any]) -> Optional[ProductModel]:
        """
        Clean and validate raw product data
        
        Args:
            raw_product: Raw product data from scraper
            
        Returns:
            Validated ProductModel or None if invalid
        """
        try:
            # Clean and normalize product data
            cleaned_data = await self._clean_product_data(raw_product)
            
            # Validate required fields
            if not self._validate_product_data(cleaned_data):
                logger.warning(f"Invalid product data: {cleaned_data.get('name', 'Unknown')}")
                return None
            
            # Create ProductModel instance
            product = ProductModel(**cleaned_data)
            
            return product
            
        except Exception as e:
            logger.error(f"Failed to process product data: {e}")
            return None
    
    async def _clean_product_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and normalize raw product data"""
        cleaned = {}
        
        # Clean name
        name = raw_data.get('name', '').strip()
        if name:
            cleaned['name'] = re.sub(r'\s+', ' ', name)[:500]
        
        # Clean brand
        brand = raw_data.get('brand', '').strip()
        if brand:
            cleaned['brand'] = brand[:100]
        
        # Normalize category
        category = raw_data.get('category', '').strip()
        if category:
            cleaned['category'] = self._normalize_category(category)
        
        # Clean subcategory
        subcategory = raw_data.get('subcategory', '').strip()
        if subcategory:
            cleaned['subcategory'] = subcategory[:100]
        
        # Parse price
        price = self._parse_price(raw_data.get('price'))
        if price is not None:
            cleaned['price'] = price
        
        # Parse original price
        original_price = self._parse_price(raw_data.get('original_price'))
        if original_price is not None:
            cleaned['original_price'] = original_price
        
        # Clean currency
        currency = raw_data.get('currency', 'USD').upper()
        cleaned['currency'] = currency[:3]
        
        # Clean description
        description = raw_data.get('description', '').strip()
        if description:
            cleaned['description'] = description[:2000]
        
        # Clean features list
        features = raw_data.get('features', [])
        if isinstance(features, list):
            cleaned['features'] = [str(f).strip()[:200] for f in features if f]
        
        # Clean specifications
        specs = raw_data.get('specifications', {})
        if isinstance(specs, dict):
            cleaned['specifications'] = {k: str(v)[:500] for k, v in specs.items() if v}
        
        # Clean images
        images = raw_data.get('images', [])
        if isinstance(images, list):
            cleaned['images'] = [str(img).strip() for img in images if img]
        
        # Parse rating
        rating = self._parse_rating(raw_data.get('rating'))
        if rating is not None:
            cleaned['rating'] = rating
        
        # Parse review count
        review_count = self._parse_int(raw_data.get('review_count'))
        if review_count is not None:
            cleaned['review_count'] = max(0, review_count)
        
        # Parse availability
        availability = raw_data.get('availability')
        if isinstance(availability, bool):
            cleaned['availability'] = availability
        elif isinstance(availability, str):
            cleaned['availability'] = availability.lower() in ['true', 'yes', 'available', 'in stock']
        else:
            cleaned['availability'] = True
        
        # Parse stock quantity
        stock_quantity = self._parse_int(raw_data.get('stock_quantity'))
        if stock_quantity is not None:
            cleaned['stock_quantity'] = max(0, stock_quantity)
        
        # Clean source info
        source = raw_data.get('source', '').strip()
        if source:
            cleaned['source'] = source[:50]
        
        source_url = raw_data.get('source_url', '').strip()
        if source_url:
            cleaned['source_url'] = source_url
        
        source_id = raw_data.get('source_id', '').strip()
        if source_id:
            cleaned['source_id'] = source_id
        
        # Clean tags
        tags = raw_data.get('tags', [])
        if isinstance(tags, list):
            cleaned['tags'] = [str(t).strip().lower()[:50] for t in tags if t]
        
        # Set timestamps
        cleaned['created_at'] = datetime.utcnow()
        cleaned['updated_at'] = datetime.utcnow()
        
        return cleaned
    
    def _normalize_category(self, category: str) -> str:
        """Normalize category name"""
        # Remove special characters and normalize
        normalized = re.sub(r'[^a-zA-Z0-9\s&]', '', category)
        normalized = re.sub(r'\s+', ' ', normalized).strip().title()
        return normalized[:100]
    
    def _parse_price(self, price_str: Any) -> Optional[float]:
        """Parse price from string or number"""
        if price_str is None:
            return None
        
        if isinstance(price_str, (int, float)):
            return max(0.0, float(price_str))
        
        if isinstance(price_str, str):
            # Remove currency symbols and spaces
            price_clean = re.sub(r'[^\d.,]', '', price_str.strip())
            if price_clean:
                try:
                    # Handle different decimal separators
                    if ',' in price_clean and '.' in price_clean:
                        # Assume comma is thousands separator
                        price_clean = price_clean.replace(',', '')
                    elif ',' in price_clean:
                        # Assume comma is decimal separator (European format)
                        price_clean = price_clean.replace(',', '.')
                    
                    return max(0.0, float(price_clean))
                except ValueError:
                    pass
        
        return None
    
    def _parse_rating(self, rating_str: Any) -> Optional[float]:
        """Parse rating from string or number"""
        if rating_str is None:
            return None
        
        if isinstance(rating_str, (int, float)):
            rating = float(rating_str)
            return max(0.0, min(5.0, rating))
        
        if isinstance(rating_str, str):
            # Extract number from rating string
            match = re.search(r'(\d+\.?\d*)', rating_str)
            if match:
                try:
                    rating = float(match.group(1))
                    return max(0.0, min(5.0, rating))
                except ValueError:
                    pass
        
        return None
    
    def _parse_int(self, value: Any) -> Optional[int]:
        """Parse integer from various input types"""
        if value is None:
            return None
        
        if isinstance(value, int):
            return value
        
        if isinstance(value, float):
            return int(value)
        
        if isinstance(value, str):
            # Remove non-digit characters
            digits = re.sub(r'[^\d]', '', value)
            if digits:
                try:
                    return int(digits)
                except ValueError:
                    pass
        
        return None
    
    def _validate_product_data(self, data: Dict[str, Any]) -> bool:
        """Validate that product data has required fields"""
        required_fields = ['name', 'category', 'source']
        
        for field in required_fields:
            if not data.get(field):
                return False
        
        # Must have a valid price
        if data.get('price') is None or data.get('price') <= 0:
            return False
        
        return True
    
    async def store_product(self, product: ProductModel) -> Optional[str]:
        """
        Store product in MongoDB
        
        Args:
            product: Validated product model
            
        Returns:
            Product ID if successful, None otherwise
        """
        try:
            await self._init_collections()
            
            # Check if product already exists by source and source_id
            if product.source and product.source_id:
                existing = await self.products_collection.find_one({
                    'source': product.source,
                    'source_id': product.source_id
                })
                
                if existing:
                    # Update existing product
                    update_data = product.dict(exclude={'_id', 'created_at'})
                    update_data['updated_at'] = datetime.utcnow()
                    
                    await self.products_collection.update_one(
                        {'_id': existing['_id']},
                        {'$set': update_data}
                    )
                    
                    logger.info(f"Updated existing product: {product.name}")
                    return str(existing['_id'])
            
            # Insert new product
            product_dict = product.dict(exclude={'_id'})
            result = await self.products_collection.insert_one(product_dict)
            
            # Update category counts
            await self._update_category_count(product.category)
            
            logger.info(f"Stored new product: {product.name}")
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"Failed to store product: {e}")
            return None
    
    async def _update_category_count(self, category_name: str):
        """Update product count for category"""
        try:
            await self.categories_collection.update_one(
                {'name': category_name},
                {
                    '$inc': {'product_count': 1},
                    '$setOnInsert': {
                        'name': category_name,
                        'slug': category_name.lower().replace(' ', '-'),
                        'is_active': True,
                        'created_at': datetime.utcnow()
                    }
                },
                upsert=True
            )
        except Exception as e:
            logger.error(f"Failed to update category count: {e}")
    
    async def process_batch(self, raw_products: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Process a batch of raw product data
        
        Args:
            raw_products: List of raw product data
            
        Returns:
            Processing statistics
        """
        stats = {
            'processed': 0,
            'stored': 0,
            'updated': 0,
            'failed': 0
        }
        
        for raw_product in raw_products:
            try:
                stats['processed'] += 1
                
                # Process product data
                product = await self.process_product_data(raw_product)
                if not product:
                    stats['failed'] += 1
                    continue
                
                # Store product
                product_id = await self.store_product(product)
                if product_id:
                    stats['stored'] += 1
                else:
                    stats['failed'] += 1
                    
            except Exception as e:
                logger.error(f"Failed to process product in batch: {e}")
                stats['failed'] += 1
        
        logger.info(f"Batch processed: {stats}")
        return stats
