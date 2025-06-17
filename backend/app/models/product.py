"""
Product data models for SMARTNEED
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from app.database.connection import Base

class Product(Base):
    """Product database model"""
    __tablename__ = "products"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(500), nullable=False, index=True)
    brand = Column(String(200), index=True)
    category = Column(String(200), index=True)
    subcategory = Column(String(200))
    
    # Pricing
    price = Column(Float)
    original_price = Column(Float)
    currency = Column(String(10), default="USD")
    discount_percentage = Column(Float)
    
    # Product details
    description = Column(Text)
    features = Column(ARRAY(String))
    specifications = Column(JSON)
    
    # Media
    image_url = Column(String(1000))
    additional_images = Column(ARRAY(String))
    
    # Ratings and reviews
    rating = Column(Float)
    review_count = Column(Integer, default=0)
    
    # Source information
    source = Column(String(100))  # ebay, walmart, etc.
    source_url = Column(String(1000))
    affiliate_link = Column(String(1000))
    
    # Availability
    in_stock = Column(Boolean, default=True)
    stock_quantity = Column(Integer)
    
    # SEO and search
    tags = Column(ARRAY(String))
    keywords = Column(ARRAY(String))
    
    # Embeddings for semantic search
    embedding = Column(Vector(768))  # Gemini embedding dimension
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_scraped = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)

class ProductEmbedding(Base):
    """Separate table for product embeddings (if needed for optimization)"""
    __tablename__ = "product_embeddings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(String(255), unique=True, index=True, nullable=False)
    embedding = Column(Vector(768))
    embedding_version = Column(String(50))  # Track embedding model version
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Pydantic models for API

class ProductBase(BaseModel):
    """Base product model for API"""
    name: str = Field(..., min_length=1, max_length=500)
    brand: Optional[str] = Field(None, max_length=200)
    category: Optional[str] = Field(None, max_length=200)
    subcategory: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    original_price: Optional[float] = Field(None, ge=0)
    currency: str = Field(default="USD", max_length=10)
    description: Optional[str] = None
    features: List[str] = Field(default_factory=list)
    specifications: Dict[str, Any] = Field(default_factory=dict)
    image_url: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    review_count: int = Field(default=0, ge=0)
    source: Optional[str] = None
    source_url: Optional[str] = None
    in_stock: bool = Field(default=True)
    tags: List[str] = Field(default_factory=list)

class ProductCreate(ProductBase):
    """Product creation model"""
    product_id: str = Field(..., min_length=1, max_length=255)

class ProductUpdate(BaseModel):
    """Product update model"""
    name: Optional[str] = Field(None, min_length=1, max_length=500)
    price: Optional[float] = Field(None, ge=0)
    description: Optional[str] = None
    features: Optional[List[str]] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    review_count: Optional[int] = Field(None, ge=0)
    in_stock: Optional[bool] = None

class ProductResponse(ProductBase):
    """Product response model"""
    id: uuid.UUID
    product_id: str
    discount_percentage: Optional[float] = None
    additional_images: List[str] = Field(default_factory=list)
    stock_quantity: Optional[int] = None
    affiliate_link: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_scraped: Optional[datetime] = None
    is_active: bool
    
    class Config:
        from_attributes = True

class ProductSearchResult(BaseModel):
    """Product search result with similarity score"""
    product: ProductResponse
    similarity_score: float = Field(..., ge=0, le=1)
    match_reasons: List[str] = Field(default_factory=list)

class ProductComparison(BaseModel):
    """Product comparison model"""
    products: List[ProductResponse]
    comparison_summary: str
    pros_cons: Dict[str, Dict[str, List[str]]] = Field(default_factory=dict)
    recommendations: Dict[str, str] = Field(default_factory=dict)

class ProductFilter(BaseModel):
    """Product filtering options"""
    category: Optional[str] = None
    brand: Optional[str] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    min_rating: Optional[float] = Field(None, ge=0, le=5)
    in_stock_only: bool = Field(default=True)
    source: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

class ProductStats(BaseModel):
    """Product statistics"""
    total_products: int
    categories: Dict[str, int]
    brands: Dict[str, int]
    price_ranges: Dict[str, int]
    sources: Dict[str, int]
    average_rating: float
    last_updated: datetime
