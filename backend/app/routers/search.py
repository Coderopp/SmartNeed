"""
Search API endpoints for SMARTNEED
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
import logging
import time
import asyncio
import sys
import os

# Add the parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from app.models.search import (
    SearchQuery, SearchResult, AutocompleteRequest, 
    AutocompleteResponse, SearchFeedback, SearchMetrics,
    SearchAnalysis
)
from app.services.semantic_search import SemanticSearchService
from app.services.gemini_service import GeminiService
from database.connection import get_database, get_products_collection, get_search_history_collection, get_user_feedback_collection

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=SearchResult)
async def search_products(query: SearchQuery) -> SearchResult:
    """
    Main product search endpoint with AI-powered semantic search
    
    Args:
        query: Search query parameters
        
    Returns:
        SearchResult: Comprehensive search results with AI analysis
    """
    start_time = time.time()
    
    try:
        logger.info(f"Processing search query: {query.query}")
        
        # Initialize services
        gemini_service = GeminiService()
        search_service = SemanticSearchService()
        
        # Analyze query using AI
        analysis_dict = await gemini_service.analyze_search_query(query.query)
        
        # Convert to SearchAnalysis object
        analysis = SearchAnalysis(**analysis_dict)
        
        # Perform semantic search
        products = await search_service.search_products(
            query=query.query,
            limit=query.limit,
            offset=query.offset,
            analysis=analysis
        )
        
        # Generate search suggestions
        suggestions = await search_service.get_search_suggestions(
            query.query, 
            count=5
        )
        
        search_time = (time.time() - start_time) * 1000
        
        # Store search analytics
        await _log_search_event(query.query, len(products), search_time)
        
        return SearchResult(
            query=query.query,
            analysis=analysis,
            products=products,
            total_count=len(products),
            search_time_ms=search_time,
            suggestions=suggestions
        )
        
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.get("/autocomplete", response_model=AutocompleteResponse)
async def autocomplete(
    q: str = Query(..., min_length=1, description="Partial query for autocomplete"),
    limit: int = Query(default=10, ge=1, le=20, description="Number of suggestions")
) -> AutocompleteResponse:
    """
    Get autocomplete suggestions for search queries
    
    Args:
        q: Partial query string
        limit: Maximum number of suggestions
        
    Returns:
        AutocompleteResponse: List of suggested completions
    """
    try:
        logger.info(f"Autocomplete request: {q}")
        
        search_service = SemanticSearchService()
        suggestions = await search_service.get_autocomplete_suggestions(q, limit)
        
        return AutocompleteResponse(suggestions=suggestions)
        
    except Exception as e:
        logger.error(f"Autocomplete failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Autocomplete service unavailable")

@router.get("/suggestions")
async def get_search_suggestions(
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(default=10, ge=1, le=50, description="Number of suggestions")
) -> List[str]:
    """
    Get popular search suggestions
    
    Args:
        category: Optional category filter
        limit: Maximum number of suggestions
        
    Returns:
        List of popular search queries
    """
    try:
        search_service = SemanticSearchService()
        suggestions = await search_service.get_popular_searches(category, limit)
        
        return suggestions
        
    except Exception as e:
        logger.error(f"Failed to get suggestions: {str(e)}")
        raise HTTPException(status_code=500, detail="Suggestions service unavailable")

@router.post("/feedback")
async def submit_search_feedback(feedback: SearchFeedback):
    """
    Submit user feedback for search results
    
    Args:
        feedback: User feedback data
        
    Returns:
        Success message
    """
    try:
        logger.info(f"Received search feedback: {feedback}")
        
        # Store feedback in database
        feedback_collection = await get_user_feedback_collection()
        feedback_doc = {
            "search_query": feedback.query,
            "product_id": feedback.product_id,
            "feedback_type": feedback.feedback_type,
            "rating": feedback.rating,
            "comment": feedback.comment,
            "user_session": feedback.user_session,
            "user_id": feedback.user_id,
            "timestamp": feedback.timestamp
        }
        await feedback_collection.insert_one(feedback_doc)
        
        return {"message": "Feedback submitted successfully", "status": "success"}
        
    except Exception as e:
        logger.error(f"Failed to submit feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to submit feedback")

@router.get("/metrics", response_model=SearchMetrics)
async def get_search_metrics(
    days: int = Query(default=30, ge=1, le=365, description="Number of days to analyze")
) -> SearchMetrics:
    """
    Get search analytics and metrics
    
    Args:
        days: Number of days to include in metrics
        
    Returns:
        SearchMetrics: Comprehensive search statistics
    """
    try:
        search_history_collection = await get_search_history_collection()
        
        # Get search metrics from database
        total_searches = await search_history_collection.count_documents({})
        
        # Calculate average results per search and response time
        # For now, using placeholder values - implement proper aggregation
        metrics = SearchMetrics(
            total_searches=total_searches,
            avg_results_per_search=15.3,
            avg_search_time_ms=245.7
        )
        
        return metrics
        
    except Exception as e:
        logger.error(f"Failed to get metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Metrics service unavailable")

@router.post("/similar")
async def find_similar_products(
    product_id: str,
    limit: int = Query(default=10, ge=1, le=50)
):
    """
    Find products similar to a given product
    
    Args:
        product_id: ID of the reference product
        limit: Maximum number of similar products
        
    Returns:
        List of similar products
    """
    try:
        search_service = SemanticSearchService()
        similar_products = await search_service.find_similar_products(product_id, limit)
        
        return similar_products
        
    except Exception as e:
        logger.error(f"Failed to find similar products: {str(e)}")
        raise HTTPException(status_code=500, detail="Similar products service unavailable")

@router.get("/categories")
async def get_search_categories():
    """
    Get available product categories with counts
    
    Returns:
        List of categories with product counts
    """
    try:
        products_collection = await get_products_collection()
        
        # Get categories from database with product counts
        pipeline = [
            {"$group": {"_id": "$category", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        
        categories_cursor = products_collection.aggregate(pipeline)
        categories = []
        async for category_doc in categories_cursor:
            categories.append({
                "name": category_doc["_id"],
                "count": category_doc["count"],
                "slug": category_doc["_id"].lower().replace(" ", "-")
            })
        
        # Add some default categories if none found
        if not categories:
            categories = [
                {"name": "Electronics", "count": 0, "slug": "electronics"},
                {"name": "Clothing", "count": 0, "slug": "clothing"},
                {"name": "Books", "count": 0, "slug": "books"},
                {"name": "Home & Garden", "count": 0, "slug": "home-garden"}
            ]
        
        return categories
        
    except Exception as e:
        logger.error(f"Failed to get categories: {str(e)}")
        raise HTTPException(status_code=500, detail="Categories service unavailable")

@router.get("/trending")
async def get_trending_searches(
    limit: int = Query(default=20, ge=1, le=100),
    time_period: str = Query(default="week", regex="^(day|week|month)$")
):
    """
    Get trending search queries
    
    Args:
        limit: Number of trending queries to return
        time_period: Time period for trending analysis
        
    Returns:
        List of trending search queries with metadata
    """
    try:
        search_history_collection = await get_search_history_collection()
        
        # Get trending searches from the last period
        # TODO: Implement proper trending calculation based on time_period
        pipeline = [
            {"$group": {"_id": "$query", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]
        
        trending_cursor = search_history_collection.aggregate(pipeline)
        trending = []
        async for trend_doc in trending_cursor:
            trending.append({
                "query": trend_doc["_id"],
                "count": trend_doc["count"],
                "change": "+5%"  # Placeholder for change calculation
            })
        
        # Fallback trending queries if none found
        if not trending:
            trending = [
                {"query": "wireless headphones", "count": 450, "change": "+15%"},
                {"query": "laptop for work", "count": 380, "change": "+8%"},
                {"query": "running shoes", "count": 320, "change": "+12%"}
            ]
        
        return trending[:limit]
        
    except Exception as e:
        logger.error(f"Failed to get trending searches: {str(e)}")
        raise HTTPException(status_code=500, detail="Trending service unavailable")

async def _log_search_event(query: str, result_count: int, search_time_ms: float):
    """Log search event for analytics"""
    try:
        # TODO: Implement search event logging
        logger.info(f"Search logged: {query} -> {result_count} results in {search_time_ms:.2f}ms")
    except Exception as e:
        logger.error(f"Failed to log search event: {e}")
        # Don't raise - logging failure shouldn't break search
