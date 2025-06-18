"""
MongoDB data models using Pydantic for SMARTNEED
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any, Annotated
from datetime import datetime

# Handle bson import gracefully
try:
    from bson import ObjectId
    BSON_AVAILABLE = True
except ImportError:
    # Create a simple ObjectId replacement for when bson is not available
    class ObjectId:
        def __init__(self, oid=None):
            import uuid
            self._id = str(uuid.uuid4()) if oid is None else str(oid)
        
        def __str__(self):
            return self._id
        
        def __repr__(self):
            return f"ObjectId('{self._id}')"
    
    BSON_AVAILABLE = False

class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic v2"""
    
    @classmethod
    def __get_pydantic_json_schema__(cls, _schema, handler):
        return {"type": "string"}
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, _info):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

# Custom type annotation for ObjectId
ObjectIdAnnotation = Annotated[PyObjectId, Field(default_factory=PyObjectId)]

class ProductModel(BaseModel):
    """Product data model for MongoDB"""
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
    
    id: Optional[ObjectIdAnnotation] = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(..., min_length=1, max_length=500)
    brand: Optional[str] = Field(None, max_length=100)
    category: str = Field(..., max_length=100)
    subcategory: Optional[str] = Field(None, max_length=100)
    price: float = Field(..., ge=0)
    original_price: Optional[float] = Field(None, ge=0)
    currency: str = Field(default="USD", max_length=3)
    description: Optional[str] = Field(None, max_length=2000)
    features: List[str] = Field(default_factory=list)
    specifications: Dict[str, Any] = Field(default_factory=dict)
    images: List[str] = Field(default_factory=list)
    rating: Optional[float] = Field(None, ge=0, le=5)
    review_count: int = Field(default=0, ge=0)
    availability: bool = Field(default=True)
    stock_quantity: Optional[int] = Field(None, ge=0)
    source: str = Field(..., max_length=50)  # ebay, walmart, etc.
    source_url: Optional[str] = Field(None)
    source_id: Optional[str] = Field(None)  # ID on the source platform
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    embedding_updated: Optional[datetime] = Field(None)

class ProductEmbeddingModel(BaseModel):
    """Product embedding data model for MongoDB"""
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
    
    id: Optional[ObjectIdAnnotation] = Field(default_factory=PyObjectId, alias="_id")
    product_id: ObjectIdAnnotation = Field(...)
    embedding: List[float] = Field(...)
    embedding_model: str = Field(default="gemini-embedding-001")
    text_content: str = Field(...)  # The text that was embedded
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SearchHistoryModel(BaseModel):
    """Search history data model for MongoDB"""
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
    
    id: Optional[ObjectIdAnnotation] = Field(default_factory=PyObjectId, alias="_id")
    query: str = Field(...)
    user_session: Optional[str] = Field(None)
    user_id: Optional[str] = Field(None)
    results_count: int = Field(default=0)
    search_time_ms: float = Field(default=0.0)
    filters_applied: Dict[str, Any] = Field(default_factory=dict)
    clicked_products: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class UserFeedbackModel(BaseModel):
    """User feedback data model for MongoDB"""
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
    
    id: Optional[ObjectIdAnnotation] = Field(default_factory=PyObjectId, alias="_id")
    search_query: str = Field(...)
    product_id: Optional[ObjectIdAnnotation] = Field(None)
    feedback_type: str = Field(...)  # click, like, purchase, etc.
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=1000)
    user_session: Optional[str] = Field(None)
    user_id: Optional[str] = Field(None)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class CategoryModel(BaseModel):
    """Product category data model for MongoDB"""
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
    
    id: Optional[ObjectIdAnnotation] = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=100)
    parent_category: Optional[str] = Field(None)
    description: Optional[str] = Field(None, max_length=500)
    product_count: int = Field(default=0, ge=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ScrapingJobModel(BaseModel):
    """Web scraping job tracking model for MongoDB"""
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
    
    id: Optional[ObjectIdAnnotation] = Field(default_factory=PyObjectId, alias="_id")
    source: str = Field(...)  # ebay, walmart, etc.
    job_type: str = Field(...)  # full_crawl, incremental, category_specific
    status: str = Field(default="pending")  # pending, running, completed, failed
    products_scraped: int = Field(default=0)
    products_updated: int = Field(default=0)
    errors_count: int = Field(default=0)
    start_time: Optional[datetime] = Field(None)
    end_time: Optional[datetime] = Field(None)
    error_messages: List[str] = Field(default_factory=list)
    config: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
