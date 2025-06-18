"""
Embedding service for MongoDB storage and vector similarity search
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from datetime import datetime
import sys
import os

# Add the parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.connection import get_products_collection, get_embeddings_collection
from database.models import ProductEmbeddingModel
from backend.app.services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for managing product embeddings in MongoDB"""
    
    def __init__(self):
        self.gemini_service = GeminiService()
        self.embedding_dimension = 768  # Gemini embedding dimension
    
    async def generate_and_store_embeddings(
        self, 
        batch_size: int = 50,
        force_regenerate: bool = False
    ) -> Dict[str, Any]:
        """Generate and store embeddings for all products"""
        try:
            logger.info("Starting embedding generation process")
            
            products_collection = await get_products_collection()
            embeddings_collection = await get_embeddings_collection()
            
            # Get products that need embeddings
            if force_regenerate:
                # Get all products
                query = {}
            else:
                # Get products without embeddings or with outdated embeddings
                existing_embeddings = set()
                async for embedding in embeddings_collection.find({}, {"product_id": 1}):
                    existing_embeddings.add(str(embedding["product_id"]))
                
                # Find products not in embeddings collection
                query = {"_id": {"$nin": [embedding["product_id"] for embedding in existing_embeddings]}}
            
            total_products = await products_collection.count_documents(query)
            logger.info(f"Found {total_products} products to process")
            
            processed = 0
            errors = 0
            
            # Process in batches
            cursor = products_collection.find(query)
            
            async for product in cursor:
                try:
                    # Create searchable text
                    searchable_text = self._create_searchable_text(product)
                    
                    # Generate embedding
                    embedding = await self.gemini_service.generate_embedding(searchable_text)
                    
                    # Store embedding
                    embedding_doc = ProductEmbeddingModel(
                        product_id=product["_id"],
                        embedding=embedding,
                        text_content=searchable_text,
                        created_at=datetime.utcnow()
                    )
                    
                    # Upsert embedding
                    await embeddings_collection.replace_one(
                        {"product_id": product["_id"]},
                        embedding_doc.dict(by_alias=True),
                        upsert=True
                    )
                    
                    # Update product embedding timestamp
                    await products_collection.update_one(
                        {"_id": product["_id"]},
                        {"$set": {"embedding_updated": datetime.utcnow()}}
                    )
                    
                    processed += 1
                    
                    if processed % 10 == 0:
                        logger.info(f"Processed {processed}/{total_products} products")
                    
                    # Rate limiting
                    await asyncio.sleep(0.2)
                    
                except Exception as e:
                    logger.error(f"Error processing product {product.get('_id')}: {e}")
                    errors += 1
                    continue
            
            result = {
                "total_products": total_products,
                "processed": processed,
                "errors": errors,
                "success_rate": processed / total_products if total_products > 0 else 0
            }
            
            logger.info(f"Embedding generation completed: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            raise
    
    async def search_similar_products(
        self, 
        query_text: str, 
        limit: int = 20,
        similarity_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Search for similar products using vector similarity"""
        try:
            # Generate query embedding
            query_embedding = await self.gemini_service.generate_embedding(query_text)
            
            products_collection = await get_products_collection()
            embeddings_collection = await get_embeddings_collection()
            
            # Get all embeddings (in production, you'd use a vector database)
            embeddings_cursor = embeddings_collection.find({})
            
            similarities = []
            
            async for embedding_doc in embeddings_cursor:
                try:
                    # Calculate similarity
                    similarity = self._calculate_cosine_similarity(
                        query_embedding,
                        embedding_doc["embedding"]
                    )
                    
                    if similarity >= similarity_threshold:
                        similarities.append({
                            "product_id": embedding_doc["product_id"],
                            "similarity": similarity
                        })
                        
                except Exception as e:
                    logger.error(f"Error calculating similarity: {e}")
                    continue
            
            # Sort by similarity
            similarities.sort(key=lambda x: x["similarity"], reverse=True)
            similarities = similarities[:limit]
            
            # Get product details
            product_ids = [item["product_id"] for item in similarities]
            products_cursor = products_collection.find({"_id": {"$in": product_ids}})
            
            products = []
            async for product in products_cursor:
                # Find similarity score
                similarity_score = next(
                    (item["similarity"] for item in similarities if item["product_id"] == product["_id"]),
                    0.0
                )
                
                product["similarity_score"] = similarity_score
                product["_id"] = str(product["_id"])  # Convert ObjectId to string
                products.append(product)
            
            # Sort products by similarity
            products.sort(key=lambda x: x["similarity_score"], reverse=True)
            
            logger.info(f"Found {len(products)} similar products for query: {query_text}")
            return products
            
        except Exception as e:
            logger.error(f"Similar products search failed: {e}")
            return []
    
    async def find_similar_to_product(
        self, 
        product_id: str, 
        limit: int = 10,
        similarity_threshold: float = 0.8
    ) -> List[Dict[str, Any]]:
        """Find products similar to a specific product"""
        try:
            embeddings_collection = await get_embeddings_collection()
            
            # Get the reference product's embedding
            reference_embedding = await embeddings_collection.find_one({"product_id": product_id})
            if not reference_embedding:
                logger.warning(f"No embedding found for product {product_id}")
                return []
            
            # Find similar embeddings
            similarities = []
            embeddings_cursor = embeddings_collection.find({"product_id": {"$ne": product_id}})
            
            async for embedding_doc in embeddings_cursor:
                try:
                    similarity = self._calculate_cosine_similarity(
                        reference_embedding["embedding"],
                        embedding_doc["embedding"]
                    )
                    
                    if similarity >= similarity_threshold:
                        similarities.append({
                            "product_id": embedding_doc["product_id"],
                            "similarity": similarity
                        })
                        
                except Exception as e:
                    logger.error(f"Error calculating similarity: {e}")
                    continue
            
            # Sort and limit
            similarities.sort(key=lambda x: x["similarity"], reverse=True)
            similarities = similarities[:limit]
            
            # Get product details
            products_collection = await get_products_collection()
            product_ids = [item["product_id"] for item in similarities]
            products_cursor = products_collection.find({"_id": {"$in": product_ids}})
            
            products = []
            async for product in products_cursor:
                similarity_score = next(
                    (item["similarity"] for item in similarities if item["product_id"] == product["_id"]),
                    0.0
                )
                
                product["similarity_score"] = similarity_score
                product["_id"] = str(product["_id"])
                products.append(product)
            
            products.sort(key=lambda x: x["similarity_score"], reverse=True)
            
            logger.info(f"Found {len(products)} similar products to {product_id}")
            return products
            
        except Exception as e:
            logger.error(f"Find similar products failed: {e}")
            return []
    
    async def get_embedding_stats(self) -> Dict[str, Any]:
        """Get embedding collection statistics"""
        try:
            products_collection = await get_products_collection()
            embeddings_collection = await get_embeddings_collection()
            
            total_products = await products_collection.count_documents({})
            total_embeddings = await embeddings_collection.count_documents({})
            
            # Get products with recent embeddings (last 7 days)
            recent_embeddings = await embeddings_collection.count_documents({
                "created_at": {"$gte": datetime.utcnow().replace(day=datetime.utcnow().day-7)}
            })
            
            stats = {
                "total_products": total_products,
                "total_embeddings": total_embeddings,
                "coverage_percentage": (total_embeddings / total_products * 100) if total_products > 0 else 0,
                "recent_embeddings": recent_embeddings,
                "embedding_dimension": self.embedding_dimension
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get embedding stats: {e}")
            return {}
    
    def _create_searchable_text(self, product: Dict[str, Any]) -> str:
        """Create searchable text from product data"""
        parts = []
        
        # Product name (most important)
        if product.get("name"):
            parts.append(product["name"])
        
        # Brand
        if product.get("brand"):
            parts.append(product["brand"])
        
        # Category
        if product.get("category"):
            parts.append(product["category"])
        
        # Description
        if product.get("description"):
            parts.append(product["description"])
        
        # Features
        if product.get("features"):
            parts.extend(product["features"])
        
        # Specifications
        if product.get("specifications"):
            for key, value in product["specifications"].items():
                parts.append(f"{key}: {value}")
        
        return " ".join(parts)
    
    def _calculate_cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        try:
            # Convert to numpy arrays
            a = np.array(vec1)
            b = np.array(vec2)
            
            # Calculate cosine similarity
            dot_product = np.dot(a, b)
            norm_a = np.linalg.norm(a)
            norm_b = np.linalg.norm(b)
            
            if norm_a == 0 or norm_b == 0:
                return 0.0
            
            similarity = dot_product / (norm_a * norm_b)
            
            # Normalize to 0-1 range and ensure it's positive
            return max(0.0, min(1.0, (similarity + 1) / 2))
            
        except Exception as e:
            logger.error(f"Similarity calculation failed: {e}")
            return 0.0
