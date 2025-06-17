"""
Google Gemini AI service for embeddings and text generation
"""

import logging
from typing import List, Dict, Any, Optional
import asyncio
import json

try:
    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None
    HarmCategory = None
    HarmBlockThreshold = None

from app.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class GeminiService:
    """Service for interacting with Google Gemini AI"""
    
    def __init__(self):
        """Initialize Gemini service"""
        self.initialized = False
        
        if not GEMINI_AVAILABLE:
            logger.warning("Google Generative AI not available. Install with: pip install google-generativeai")
            return
            
        if not settings.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY not set in environment variables")
            return
            
        try:
            # Configure Gemini API
            genai.configure(api_key=settings.GEMINI_API_KEY)
            
            # Configure safety settings
            self.safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            }
            
            # Initialize models
            self.generative_model = genai.GenerativeModel(
                model_name=settings.GEMINI_MODEL,
                safety_settings=self.safety_settings
            )
            
            self.initialized = True
            logger.info("✅ Gemini service initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini service: {e}")
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using Gemini"""
        if not self.initialized:
            raise RuntimeError("Gemini service not properly initialized")
            
        try:
            cleaned_text = self._clean_text(text)
            if not cleaned_text.strip():
                raise ValueError("Text cannot be empty after cleaning")
            
            # Generate embedding using Gemini
            result = genai.embed_content(
                model=f"models/{settings.GEMINI_EMBEDDING_MODEL}",
                content=cleaned_text,
                task_type="retrieval_document"
            )
            
            embedding = result['embedding']
            
            if not embedding or len(embedding) != settings.EMBEDDING_DIMENSION:
                raise ValueError(f"Invalid embedding dimension")
            
            return embedding
            
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            return [0.0] * settings.EMBEDDING_DIMENSION
    
    async def analyze_search_query(self, query: str) -> Dict[str, Any]:
        """Analyze search query using Gemini"""
        if not self.initialized:
            return self._fallback_query_analysis(query)
        
        try:
            prompt = f"""
            Analyze this search query: "{query}"
            
            Return JSON with:
            - intent: product_discovery/price_comparison/specific_product
            - category: electronics/clothing/books/etc
            - confidence: 0.0-1.0
            """
            
            response = self.generative_model.generate_content(prompt)
            
            try:
                analysis = json.loads(response.text)
                return analysis
            except json.JSONDecodeError:
                return self._fallback_query_analysis(query)
                
        except Exception as e:
            logger.error(f"Failed to analyze query: {e}")
            return self._fallback_query_analysis(query)
    
    def _clean_text(self, text: str) -> str:
        """Clean and prepare text for processing"""
        if not text:
            return ""
        
        cleaned = ' '.join(text.split())
        max_length = 8000
        if len(cleaned) > max_length:
            cleaned = cleaned[:max_length].rsplit(' ', 1)[0]
        
        return cleaned
    
    def _fallback_query_analysis(self, query: str) -> Dict[str, Any]:
        """Fallback analysis when Gemini is not available"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['compare', 'vs', 'versus']):
            intent = "price_comparison"
        elif any(word in query_lower for word in ['best', 'top', 'recommend']):
            intent = "product_discovery"
        else:
            intent = "specific_product"
        
        return {
            "intent": intent,
            "category": "general",
            "brands": [],
            "price_range": None,
            "features": [],
            "sentiment": "neutral",
            "confidence_score": 0.6,
            "enhanced_query": query
        }
