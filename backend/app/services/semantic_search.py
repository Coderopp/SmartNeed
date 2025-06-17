"""
Semantic search service using vector embeddings
"""

import logging
import asyncio
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from app.services.gemini_service import GeminiService
from app.models.search import ProductSearchResult, SearchAnalysis
from database.connection import get_database, get_products_collection, get_embeddings_collection, get_search_history_collection

logger = logging.getLogger(__name__)

class SemanticSearchService:
    """Service for semantic product search using vector embeddings"""
    
    def __init__(self):
        """Initialize semantic search service"""
        self.gemini_service = GeminiService()
        self.embedding_cache = {}  # Simple in-memory cache
        logger.info("Semantic search service initialized")
    
    async def search_products(
        self, 
        query: str, 
        limit: int = 20, 
        offset: int = 0,
        analysis: Optional[SearchAnalysis] = None
    ) -> List[ProductSearchResult]:
        """
        Perform semantic search for products
        
        Args:
            query: Search query text
            limit: Maximum number of results
            offset: Number of results to skip
            analysis: Optional pre-computed query analysis
            
        Returns:
            List of matching products with similarity scores
        """
        try:
            logger.info(f"Performing semantic search for: {query}")
            
            # Generate query embedding
            query_embedding = await self.gemini_service.generate_embedding(query)
            
            # Get products from database with their embeddings
            products = await self._get_products_with_embeddings(limit + offset)
            
            # Calculate similarity scores
            scored_products = []
            for product in products:
                if product.get('embedding'):
                    similarity = self._calculate_similarity(
                        query_embedding, 
                        product['embedding']
                    )
                    
                    if similarity > 0.3:  # Similarity threshold
                        product_result = ProductSearchResult(
                            id=product['id'],
                            name=product['name'],
                            brand=product.get('brand'),
                            price=product['price'],
                            rating=product.get('rating'),
                            description=product.get('description'),
                            category=product.get('category'),
                            source=product.get('source', 'unknown'),
                            similarity_score=similarity,
                            features=product.get('features', []),
                            availability=product.get('availability', True)
                        )
                        scored_products.append(product_result)
            
            # Sort by similarity score
            scored_products.sort(key=lambda x: x.similarity_score, reverse=True)
            
            # Apply offset and limit
            results = scored_products[offset:offset + limit]
            
            logger.info(f"Found {len(results)} relevant products")
            return results
            
        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            # Return fallback results
            return await self._get_fallback_results(query, limit, offset)
    
    async def find_similar_products(
        self, 
        product_id: str, 
        limit: int = 10
    ) -> List[ProductSearchResult]:
        """
        Find products similar to a given product
        
        Args:
            product_id: Reference product ID
            limit: Number of similar products to return
            
        Returns:
            List of similar products
        """
        try:
            # Get reference product and its embedding
            reference_product = await self._get_product_by_id(product_id)
            if not reference_product or not reference_product.get('embedding'):
                return []
            
            reference_embedding = reference_product['embedding']
            
            # Get all products with embeddings
            all_products = await self._get_products_with_embeddings()
            
            # Calculate similarities
            similar_products = []
            for product in all_products:
                if product['id'] != product_id and product.get('embedding'):
                    similarity = self._calculate_similarity(
                        reference_embedding,
                        product['embedding']
                    )
                    
                    if similarity > 0.5:  # Higher threshold for similarity
                        product_result = ProductSearchResult(
                            id=product['id'],
                            name=product['name'],
                            brand=product.get('brand'),
                            price=product['price'],
                            rating=product.get('rating'),
                            category=product.get('category'),
                            source=product.get('source', 'unknown'),
                            similarity_score=similarity
                        )
                        similar_products.append(product_result)
            
            # Sort and limit results
            similar_products.sort(key=lambda x: x.similarity_score, reverse=True)
            return similar_products[:limit]
            
        except Exception as e:
            logger.error(f"Similar products search failed: {e}")
            return []
    
    async def get_autocomplete_suggestions(
        self, 
        partial_query: str, 
        limit: int = 10
    ) -> List[str]:
        """
        Get autocomplete suggestions for partial query
        
        Args:
            partial_query: Partial search query
            limit: Maximum number of suggestions
            
        Returns:
            List of suggested completions
        """
        try:
            # Get popular queries that start with partial_query
            suggestions = await self._get_query_suggestions(partial_query, limit)
            
            # Add product name suggestions
            product_suggestions = await self._get_product_name_suggestions(partial_query, limit // 2)
            suggestions.extend(product_suggestions)
            
            # Remove duplicates and limit
            unique_suggestions = list(dict.fromkeys(suggestions))[:limit]
            
            return unique_suggestions
            
        except Exception as e:
            logger.error(f"Autocomplete failed: {e}")
            return self._get_fallback_suggestions(partial_query, limit)
    
    async def get_search_suggestions(
        self, 
        query: str, 
        count: int = 5
    ) -> List[str]:
        """
        Get related search suggestions for a query
        
        Args:
            query: Original search query
            count: Number of suggestions to return
            
        Returns:
            List of related search suggestions
        """
        try:
            # Use Gemini to generate smart suggestions
            suggestions = await self.gemini_service.suggest_similar_queries(query, count)
            
            # Fallback to query-based suggestions
            if not suggestions:
                suggestions = await self._get_related_queries(query, count)
            
            return suggestions[:count]
            
        except Exception as e:
            logger.error(f"Search suggestions failed: {e}")
            return self._get_fallback_related_queries(query, count)
    
    async def get_popular_searches(
        self, 
        category: Optional[str] = None, 
        limit: int = 10
    ) -> List[str]:
        """
        Get popular search queries
        
        Args:
            category: Optional category filter
            limit: Number of popular searches to return
            
        Returns:
            List of popular search queries
        """
        try:
            search_history_collection = await get_search_history_collection()
            
            # Get popular searches from database
            pipeline = [
                {"$group": {"_id": "$query", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": limit}
            ]
            
            if category:
                # Add category filter to pipeline
                pipeline.insert(0, {"$match": {"query": {"$regex": category, "$options": "i"}}})
            
            popular_cursor = search_history_collection.aggregate(pipeline)
            popular = []
            async for doc in popular_cursor:
                popular.append(doc["_id"])
            
            # Fallback to static popular searches if none found
            if not popular:
                popular = [
                    "wireless headphones",
                    "laptop for work", 
                    "running shoes",
                    "smartphone under 500",
                    "office chair ergonomic",
                    "kitchen appliances",
                    "gaming mouse",
                    "fitness tracker",
                    "coffee maker",
                    "outdoor gear"
                ]
                
                return popular[:limit]
                
        except Exception as e:
            logger.error(f"Popular searches failed: {e}")
            return ["laptop", "headphones", "shoes"][:limit]
    
    async def index_product_embeddings(self, products: List[Dict[str, Any]]):
        """
        Generate and store embeddings for products
        
        Args:
            products: List of product dictionaries to index
        """
        try:
            logger.info(f"Indexing embeddings for {len(products)} products")
            
            for product in products:
                # Create searchable text from product data
                searchable_text = self._create_searchable_text(product)
                
                # Generate embedding
                embedding = await self.gemini_service.generate_embedding(searchable_text)
                
                # Store embedding with product
                await self._store_product_embedding(product['id'], embedding)
                
                # Small delay to respect rate limits
                await asyncio.sleep(0.1)
            
            logger.info("Product embedding indexing completed")
            
        except Exception as e:
            logger.error(f"Product indexing failed: {e}")
    
    def _calculate_similarity(
        self, 
        embedding1: List[float], 
        embedding2: List[float]
    ) -> float:
        """
        Calculate cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score between 0 and 1
        """
        try:
            # Convert to numpy arrays
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            # Calculate cosine similarity
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            similarity = dot_product / (norm1 * norm2)
            
            # Normalize to 0-1 range
            return max(0.0, min(1.0, (similarity + 1) / 2))
            
        except Exception as e:
            logger.error(f"Similarity calculation failed: {e}")
            return 0.0
    
    def _create_searchable_text(self, product: Dict[str, Any]) -> str:
        """Create searchable text representation of product"""
        parts = []
        
        if product.get('name'):
            parts.append(product['name'])
        if product.get('brand'):
            parts.append(product['brand'])
        if product.get('category'):
            parts.append(product['category'])
        if product.get('description'):
            parts.append(product['description'])
        if product.get('features'):
            parts.extend(product['features'])
        
        return ' '.join(parts)
    
    async def _get_products_with_embeddings(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get products with their embeddings from database"""
        # TODO: Implement actual database query
        # For now, return mock data
        mock_products = [
            {
                'id': '1',
                'name': 'MacBook Pro 14" M3',
                'brand': 'Apple',
                'price': 1999,
                'category': 'electronics',
                'description': 'Powerful laptop for professionals',
                'embedding': [0.1] * 768,  # Mock embedding
                'source': 'ebay'
            },
            {
                'id': '2',
                'name': 'Dell XPS 13',
                'brand': 'Dell',
                'price': 1299,
                'category': 'electronics',
                'description': 'Ultra-portable business laptop',
                'embedding': [0.2] * 768,  # Mock embedding
                'source': 'ebay'
            }
        ]
        
        return mock_products[:limit] if limit else mock_products
    
    async def _get_product_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific product by ID"""
        # TODO: Implement actual database query
        products = await self._get_products_with_embeddings()
        for product in products:
            if product['id'] == product_id:
                return product
        return None
    
    async def _store_product_embedding(self, product_id: str, embedding: List[float]):
        """Store product embedding in database"""
        # TODO: Implement database storage
        logger.info(f"Stored embedding for product {product_id}")
    
    async def _get_fallback_results(self, query: str, limit: int, offset: int) -> List[ProductSearchResult]:
        """Fallback search results when semantic search fails"""
        mock_results = [
            ProductSearchResult(
                id="fallback_1",
                name=f"Product matching '{query}'",
                price=99.99,
                similarity_score=0.8,
                source="fallback"
            )
        ]
        return mock_results[:limit]
    
    def _get_fallback_suggestions(self, partial_query: str, limit: int) -> List[str]:
        """Fallback autocomplete suggestions"""
        base_suggestions = [
            f"{partial_query} for work",
            f"{partial_query} reviews",
            f"best {partial_query}",
            f"cheap {partial_query}",
            f"{partial_query} comparison"
        ]
        return base_suggestions[:limit]
    
    def _get_fallback_related_queries(self, query: str, count: int) -> List[str]:
        """Fallback related query suggestions"""
        return [
            f"best {query}",
            f"{query} reviews",
            f"cheap {query}",
            f"{query} comparison"
        ][:count]
    
    async def _get_query_suggestions(self, partial_query: str, limit: int) -> List[str]:
        """Get query suggestions from search history"""
        # TODO: Implement database query for popular queries
        return []
    
    async def _get_product_name_suggestions(self, partial_query: str, limit: int) -> List[str]:
        """Get product name suggestions"""
        # TODO: Implement database query for product names
        return []
    
    async def _get_related_queries(self, query: str, count: int) -> List[str]:
        """Get related queries from search history"""
        # TODO: Implement database query for related searches
        return []
