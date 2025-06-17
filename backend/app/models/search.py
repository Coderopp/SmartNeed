"""
Pydantic models for search functionality
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class SearchIntent(str, Enum):
    """Search intent types"""
    PRODUCT_DISCOVERY = "product_discovery"
    PRICE_COMPARISON = "price_comparison"
    SPECIFIC_PRODUCT = "specific_product"

class SortOrder(str, Enum):
    """Sorting options for search results"""
    RELEVANCE = "relevance"
    PRICE_LOW_TO_HIGH = "price_asc"
    PRICE_HIGH_TO_LOW = "price_desc"
    RATING_HIGH_TO_LOW = "rating_desc"
    NEWEST_FIRST = "newest_first"

class SearchQuery(BaseModel):
    """Search query request model"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    query: str = Field(..., min_length=1, max_length=500, description="Search query text")
    limit: int = Field(default=20, ge=1, le=100, description="Maximum number of results")
    offset: int = Field(default=0, ge=0, description="Number of results to skip")
    category: Optional[str] = Field(None, max_length=100, description="Filter by category")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price filter")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price filter")
    sort_by: SortOrder = Field(default=SortOrder.RELEVANCE, description="Sort order for results")
    include_out_of_stock: bool = Field(default=False, description="Include out of stock products")

class SearchAnalysis(BaseModel):
    """AI analysis of the search query"""
    intent: SearchIntent = Field(..., description="Detected search intent")
    category: Optional[str] = Field(None, description="Detected product category")
    brands: List[str] = Field(default_factory=list, description="Detected brand names")
    price_range: Optional[Dict[str, float]] = Field(None, description="Detected price range")
    features: List[str] = Field(default_factory=list, description="Detected features/specifications")
    sentiment: str = Field(default="neutral", description="Query sentiment")
    confidence_score: float = Field(..., ge=0, le=1, description="Analysis confidence score")
    enhanced_query: str = Field(..., description="AI-enhanced version of the query")

class ProductSearchResult(BaseModel):
    """Individual product in search results"""
    id: str = Field(..., description="Unique product identifier")
    name: str = Field(..., description="Product name")
    brand: Optional[str] = Field(None, description="Product brand")
    price: float = Field(..., ge=0, description="Product price")
    original_price: Optional[float] = Field(None, ge=0, description="Original price if discounted")
    currency: str = Field(default="USD", description="Price currency")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Average user rating")
    review_count: int = Field(default=0, ge=0, description="Number of reviews")
    image_url: Optional[str] = Field(None, description="Product image URL")
    description: Optional[str] = Field(None, max_length=1000, description="Product description")
    category: Optional[str] = Field(None, description="Product category")
    availability: bool = Field(default=True, description="Product availability")
    source: str = Field(..., description="Data source (ebay, walmart, etc.)")
    source_url: Optional[str] = Field(None, description="Link to product on source site")
    similarity_score: float = Field(..., ge=0, le=1, description="Relevance score")
    features: List[str] = Field(default_factory=list, description="Key product features")
    specifications: Dict[str, Any] = Field(default_factory=dict, description="Technical specifications")

class SearchResult(BaseModel):
    """Complete search result response"""
    query: str = Field(..., description="Original search query")
    analysis: SearchAnalysis = Field(..., description="AI analysis of the query")
    products: List[ProductSearchResult] = Field(..., description="Found products")
    total_count: int = Field(..., ge=0, description="Total number of matching products")
    search_time_ms: float = Field(..., ge=0, description="Search execution time in milliseconds")
    suggestions: List[str] = Field(default_factory=list, description="Related search suggestions")
    filters_applied: Dict[str, Any] = Field(default_factory=dict, description="Active filters")
    pagination: Dict[str, Any] = Field(default_factory=dict, description="Pagination information")

class AutocompleteRequest(BaseModel):
    """Autocomplete request model"""
    partial_query: str = Field(..., min_length=1, max_length=100, description="Partial search query")
    limit: int = Field(default=10, ge=1, le=20, description="Maximum number of suggestions")
    include_categories: bool = Field(default=True, description="Include category suggestions")

class AutocompleteResponse(BaseModel):
    """Autocomplete response model"""
    suggestions: List[str] = Field(..., description="Query completion suggestions")
    categories: List[str] = Field(default_factory=list, description="Relevant category suggestions")
    trending: List[str] = Field(default_factory=list, description="Trending search terms")

class SearchFeedback(BaseModel):
    """User feedback for search results"""
    search_query: str = Field(..., min_length=1, description="Original search query")
    result_product_id: Optional[str] = Field(None, description="Product ID user interacted with")
    feedback_type: str = Field(..., description="Type of feedback (click, purchase, etc.)")
    rating: Optional[int] = Field(None, ge=1, le=5, description="User rating for results")
    comment: Optional[str] = Field(None, max_length=500, description="Optional user comment")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Feedback timestamp")
    user_session: Optional[str] = Field(None, description="User session identifier")

class SearchMetrics(BaseModel):
    """Search analytics and metrics"""
    total_searches: int = Field(default=0, ge=0, description="Total number of searches")
    unique_queries: int = Field(default=0, ge=0, description="Number of unique queries")
    avg_results_per_search: float = Field(default=0.0, ge=0, description="Average results per search")
    avg_search_time_ms: float = Field(default=0.0, ge=0, description="Average search time")
    popular_queries: List[str] = Field(default_factory=list, description="Most popular search queries")
    popular_categories: Dict[str, int] = Field(default_factory=dict, description="Popular categories with counts")
    conversion_rate: float = Field(default=0.0, ge=0, le=1, description="Search to action conversion rate")
    success_rate: float = Field(default=0.0, ge=0, le=1, description="Searches with at least one result")

class TrendingQuery(BaseModel):
    """Trending search query information"""
    query: str = Field(..., description="Search query text")
    search_count: int = Field(..., ge=0, description="Number of searches")
    growth_rate: float = Field(..., description="Growth rate percentage")
    category: Optional[str] = Field(None, description="Primary category")
    time_period: str = Field(..., description="Time period for the trend")

class CategoryInfo(BaseModel):
    """Product category information"""
    name: str = Field(..., description="Category name")
    slug: str = Field(..., description="URL-friendly category identifier")
    product_count: int = Field(..., ge=0, description="Number of products in category")
    subcategories: List[str] = Field(default_factory=list, description="Subcategory names")
    trending_products: List[str] = Field(default_factory=list, description="Trending products in category")

class SearchFilter(BaseModel):
    """Search filter configuration"""
    name: str = Field(..., description="Filter name")
    type: str = Field(..., description="Filter type (range, select, boolean, etc.)")
    options: List[str] = Field(default_factory=list, description="Available filter options")
    min_value: Optional[float] = Field(None, description="Minimum value for range filters")
    max_value: Optional[float] = Field(None, description="Maximum value for range filters")
    active: bool = Field(default=False, description="Whether filter is currently active")

class SearchSession(BaseModel):
    """User search session tracking"""
    session_id: str = Field(..., description="Unique session identifier")
    user_id: Optional[str] = Field(None, description="User identifier if logged in")
    queries: List[str] = Field(default_factory=list, description="Queries in this session")
    start_time: datetime = Field(default_factory=datetime.utcnow, description="Session start time")
    last_activity: datetime = Field(default_factory=datetime.utcnow, description="Last activity time")
    total_searches: int = Field(default=0, ge=0, description="Total searches in session")
    actions_taken: List[str] = Field(default_factory=list, description="Actions taken by user")
