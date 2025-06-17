"""
Products API endpoints for SMARTNEED
"""

from fastapi import APIRouter
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/stats")
async def get_product_stats():
    """Get product database statistics"""
    return {
        "total_products": 50000,
        "categories": {"electronics": 12000, "furniture": 8000},
        "brands": {"apple": 500, "dell": 300},
        "price_ranges": {"0-100": 15000, "100-500": 20000},
        "average_rating": 4.2
    }

@router.get("/")
async def get_products(skip: int = 0, limit: int = 20, category: str = None):
    """Get list of products with pagination"""
    products = [
        {"id": f"prod_{i}", "name": f"Product {i}", "price": 50 + i * 10}
        for i in range(skip, skip + limit)
    ]
    return products

@router.get("/{product_id}")
async def get_product(product_id: str):
    """Get a specific product by ID"""
    return {
        "id": product_id,
        "name": "Sample Product",
        "price": 99.99,
        "brand": "Sample Brand",
        "rating": 4.5,
        "description": "This is a sample product for development"
    }
