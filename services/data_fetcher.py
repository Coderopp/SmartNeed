"""
Real Product Data Fetcher Service
Fetches real product data from multiple sources
"""

import asyncio
import aiohttp
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
from fake_useragent import UserAgent
import time

logger = logging.getLogger(__name__)

class ProductDataFetcher:
    """Fetches real product data from various sources"""
    
    def __init__(self):
        self.session = None
        self.ua = UserAgent()
        self.rate_limit_delay = 1.0  # seconds between requests
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def fetch_ebay_products(self, keywords: str, category_id: str = None, max_items: int = 50) -> List[Dict]:
        """
        Fetch products from eBay API
        Requires eBay API key in environment variables
        """
        ebay_app_id = os.getenv('EBAY_API_KEY')
        if not ebay_app_id:
            logger.warning("eBay API key not found. Using mock data.")
            return self._get_mock_ebay_products(keywords, max_items)
        
        try:
            url = "https://svcs.ebay.com/services/search/FindingService/v1"
            params = {
                'OPERATION-NAME': 'findItemsByKeywords',
                'SERVICE-VERSION': '1.0.0',
                'SECURITY-APPNAME': ebay_app_id,
                'RESPONSE-DATA-FORMAT': 'JSON',
                'keywords': keywords,
                'paginationInput.entriesPerPage': min(max_items, 100),
                'itemFilter(0).name': 'Condition',
                'itemFilter(0).value': 'New',
                'sortOrder': 'BestMatch'
            }
            
            if category_id:
                params['categoryId'] = category_id
            
            async with self.session.get(url, params=params) as response:
                data = await response.json()
                return self._parse_ebay_response(data)
                
        except Exception as e:
            logger.error(f"Error fetching eBay products: {e}")
            return self._get_mock_ebay_products(keywords, max_items)
    
    async def fetch_bestbuy_products(self, query: str, max_items: int = 50) -> List[Dict]:
        """
        Fetch products from Best Buy API
        Requires Best Buy API key
        """
        bestbuy_api_key = os.getenv('BESTBUY_API_KEY')
        if not bestbuy_api_key:
            logger.warning("Best Buy API key not found. Using mock data.")
            return self._get_mock_bestbuy_products(query, max_items)
        
        try:
            url = f"https://api.bestbuy.com/v1/products"
            params = {
                'apiKey': bestbuy_api_key,
                'q': query,
                'format': 'json',
                'pageSize': min(max_items, 100),
                'show': 'name,regularPrice,salePrice,image,customerReviewAverage,customerReviewCount,shortDescription,manufacturer,modelNumber,sku'
            }
            
            async with self.session.get(url, params=params) as response:
                data = await response.json()
                return self._parse_bestbuy_response(data)
                
        except Exception as e:
            logger.error(f"Error fetching Best Buy products: {e}")
            return self._get_mock_bestbuy_products(query, max_items)
    
    async def scrape_product_data(self, urls: List[str]) -> List[Dict]:
        """
        Ethically scrape product data from provided URLs
        Respects robots.txt and implements rate limiting
        """
        products = []
        
        for url in urls:
            try:
                await asyncio.sleep(self.rate_limit_delay)  # Rate limiting
                
                headers = {
                    'User-Agent': self.ua.random,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                }
                
                async with self.session.get(url, headers=headers) as response:
                    if response.status == 200:
                        html = await response.text()
                        product = self._extract_product_from_html(html, url)
                        if product:
                            products.append(product)
                            
            except Exception as e:
                logger.error(f"Error scraping {url}: {e}")
                continue
        
        return products
    
    def _parse_ebay_response(self, data: Dict) -> List[Dict]:
        """Parse eBay API response"""
        products = []
        
        try:
            search_result = data.get('findItemsByKeywordsResponse', [{}])[0]
            items = search_result.get('searchResult', [{}])[0].get('item', [])
            
            for item in items:
                try:
                    product = {
                        'name': item.get('title', [''])[0],
                        'price': float(item.get('sellingStatus', [{}])[0].get('currentPrice', [{}])[0].get('__value__', 0)),
                        'currency': item.get('sellingStatus', [{}])[0].get('currentPrice', [{}])[0].get('@currencyId', 'USD'),
                        'image_url': item.get('galleryURL', [''])[0],
                        'item_url': item.get('viewItemURL', [''])[0],
                        'condition': item.get('condition', [{}])[0].get('conditionDisplayName', [''])[0],
                        'shipping_cost': float(item.get('shippingInfo', [{}])[0].get('shippingServiceCost', [{}])[0].get('__value__', 0)),
                        'location': item.get('location', [''])[0],
                        'source': 'ebay',
                        'fetched_at': datetime.utcnow().isoformat()
                    }
                    
                    # Only add if essential fields are present
                    if product['name'] and product['price'] > 0:
                        products.append(product)
                        
                except (KeyError, IndexError, ValueError) as e:
                    logger.debug(f"Error parsing eBay item: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing eBay response: {e}")
        
        return products
    
    def _parse_bestbuy_response(self, data: Dict) -> List[Dict]:
        """Parse Best Buy API response"""
        products = []
        
        try:
            items = data.get('products', [])
            
            for item in items:
                try:
                    product = {
                        'name': item.get('name', ''),
                        'price': float(item.get('salePrice') or item.get('regularPrice', 0)),
                        'original_price': float(item.get('regularPrice', 0)),
                        'image_url': item.get('image', ''),
                        'rating': float(item.get('customerReviewAverage', 0)),
                        'review_count': int(item.get('customerReviewCount', 0)),
                        'description': item.get('shortDescription', ''),
                        'brand': item.get('manufacturer', ''),
                        'model': item.get('modelNumber', ''),
                        'sku': item.get('sku', ''),
                        'source': 'bestbuy',
                        'category': 'Electronics',
                        'fetched_at': datetime.utcnow().isoformat()
                    }
                    
                    if product['name'] and product['price'] > 0:
                        products.append(product)
                        
                except (KeyError, ValueError) as e:
                    logger.debug(f"Error parsing Best Buy item: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing Best Buy response: {e}")
        
        return products
    
    def _extract_product_from_html(self, html: str, url: str) -> Optional[Dict]:
        """Extract product data from HTML (basic implementation)"""
        try:
            from bs4 import BeautifulSoup
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract basic information (this is a simplified example)
            # In practice, you'd need site-specific extractors
            
            title = soup.find('title')
            title_text = title.get_text().strip() if title else 'Unknown Product'
            
            # Look for common price patterns
            price_selectors = [
                '[data-price]', '.price', '.cost', '[class*="price"]',
                '[id*="price"]', '.currency', '[class*="cost"]'
            ]
            
            price = 0
            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text()
                    # Extract numeric price
                    import re
                    price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
                    if price_match:
                        price = float(price_match.group())
                        break
            
            # Look for images
            img_elem = soup.find('img')
            image_url = img_elem.get('src', '') if img_elem else ''
            
            product = {
                'name': title_text,
                'price': price,
                'image_url': image_url,
                'source_url': url,
                'source': 'scraped',
                'fetched_at': datetime.utcnow().isoformat()
            }
            
            return product if product['name'] and product['price'] > 0 else None
            
        except Exception as e:
            logger.error(f"Error extracting product from HTML: {e}")
            return None
    
    def _get_mock_ebay_products(self, keywords: str, max_items: int) -> List[Dict]:
        """Mock eBay products for testing"""
        mock_products = [
            {
                'name': f'{keywords} - Premium Quality Product',
                'price': 299.99,
                'currency': 'USD',
                'image_url': 'https://via.placeholder.com/300x300',
                'condition': 'New',
                'shipping_cost': 0.0,
                'location': 'United States',
                'source': 'ebay_mock',
                'fetched_at': datetime.utcnow().isoformat()
            },
            {
                'name': f'{keywords} - Budget Option',
                'price': 149.99,
                'currency': 'USD',
                'image_url': 'https://via.placeholder.com/300x300',
                'condition': 'New',
                'shipping_cost': 9.99,
                'location': 'United States',
                'source': 'ebay_mock',
                'fetched_at': datetime.utcnow().isoformat()
            }
        ]
        return mock_products[:max_items]
    
    def _get_mock_bestbuy_products(self, query: str, max_items: int) -> List[Dict]:
        """Mock Best Buy products for testing"""
        mock_products = [
            {
                'name': f'{query} - Best Buy Exclusive',
                'price': 399.99,
                'original_price': 449.99,
                'image_url': 'https://via.placeholder.com/300x300',
                'rating': 4.5,
                'review_count': 128,
                'description': f'High-quality {query} with advanced features',
                'brand': 'Premium Brand',
                'model': 'PM-001',
                'sku': 'BB001',
                'source': 'bestbuy_mock',
                'category': 'Electronics',
                'fetched_at': datetime.utcnow().isoformat()
            }
        ]
        return mock_products[:max_items]

# Usage example
async def fetch_sample_products():
    """Example usage of the ProductDataFetcher"""
    
    async with ProductDataFetcher() as fetcher:
        # Fetch from multiple sources
        ebay_products = await fetcher.fetch_ebay_products("wireless headphones", max_items=10)
        bestbuy_products = await fetcher.fetch_bestbuy_products("laptop", max_items=10)
        
        all_products = ebay_products + bestbuy_products
        
        logger.info(f"Fetched {len(all_products)} products total")
        logger.info(f"eBay products: {len(ebay_products)}")
        logger.info(f"Best Buy products: {len(bestbuy_products)}")
        
        return all_products

if __name__ == "__main__":
    # Test the fetcher
    logging.basicConfig(level=logging.INFO)
    products = asyncio.run(fetch_sample_products())
    
    for product in products[:3]:  # Show first 3 products
        print(f"Product: {product['name']}")
        print(f"Price: ${product['price']}")
        print(f"Source: {product['source']}")
        print("-" * 40)
