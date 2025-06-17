"""
Product comparison API endpoints for SMARTNEED
"""

from fastapi import APIRouter
import logging
import random

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/")
async def compare_products(product_ids: dict):
    """Compare multiple products"""
    ids = product_ids.get("product_ids", [])
    
    comparisons = []
    for i, pid in enumerate(ids):
        comparisons.append({
            "id": pid,
            "name": f"Product {pid}",
            "price": 100 + i * 50,
            "rating": round(4 + random.random(), 1),
            "features": {
                "warranty": f"{1 + i} years",
                "color": ["Black", "White", "Silver"][i % 3],
                "weight": f"{1.5 + i * 0.3:.1f} kg"
            }
        })
    
    return {
        "products": comparisons,
        "comparison_matrix": {
            "best_price": comparisons[0]["id"] if comparisons else None,
            "best_rating": comparisons[-1]["id"] if comparisons else None,
            "recommended": comparisons[0]["id"] if comparisons else None
        }
    }
