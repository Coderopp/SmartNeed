import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Filter, Grid, List, Clock } from 'lucide-react';
import SearchInterface from '../components/SearchInterface';
import ProductCard from '../components/ProductCard';
import FilterPanel from '../components/FilterPanel';

const Search = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [query, setQuery] = useState(searchParams.get('q') || '');
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [viewMode, setViewMode] = useState('grid');
  const [showFilters, setShowFilters] = useState(false);
  const [searchTime, setSearchTime] = useState(0);

  // Mock search results for now
  const mockResults = [
    {
      id: '1',
      product_id: 'laptop-1',
      name: 'MacBook Pro 14" M3',
      brand: 'Apple',
      price: 1999,
      rating: 4.8,
      review_count: 256,
      image_url: '/api/placeholder/300/300',
      description: 'Powerful laptop with M3 chip for professional work',
      similarity_score: 0.95,
      match_reasons: ['High performance', 'Professional grade', 'Excellent for video calls']
    },
    {
      id: '2',
      product_id: 'laptop-2',
      name: 'Dell XPS 13',
      brand: 'Dell',
      price: 1299,
      rating: 4.6,
      review_count: 189,
      image_url: '/api/placeholder/300/300',
      description: 'Compact ultrabook with excellent build quality',
      similarity_score: 0.88,
      match_reasons: ['Portable design', 'Good for productivity', 'Quiet operation']
    },
    {
      id: '3',
      product_id: 'laptop-3',
      name: 'ThinkPad X1 Carbon',
      brand: 'Lenovo',
      price: 1599,
      rating: 4.7,
      review_count: 143,
      image_url: '/api/placeholder/300/300',
      description: 'Business laptop with exceptional keyboard and durability',
      similarity_score: 0.82,
      match_reasons: ['Business grade', 'Excellent keyboard', 'Durable construction']
    }
  ];

  useEffect(() => {
    const queryParam = searchParams.get('q');
    if (queryParam && queryParam !== query) {
      setQuery(queryParam);
      handleSearch(queryParam);
    }
  }, [searchParams]);

  const handleSearch = async (searchQuery) => {
    if (!searchQuery.trim()) return;

    setIsLoading(true);
    setSearchTime(0);
    
    const startTime = Date.now();
    
    try {
      // TODO: Replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 800)); // Simulate API delay
      setResults(mockResults);
      setSearchTime(Date.now() - startTime);
      
      // Update URL
      setSearchParams({ q: searchQuery });
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewSearch = (newQuery) => {
    setQuery(newQuery);
    handleSearch(newQuery);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Search Header */}
      <div className="bg-white border-b border-gray-200 sticky top-16 z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <SearchInterface
            onSearch={handleNewSearch}
            initialQuery={query}
            placeholder="Search for products..."
            className="mb-4"
          />
          
          {/* Search info and controls */}
          {(results.length > 0 || isLoading) && (
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4 text-sm text-gray-600">
                {isLoading ? (
                  <span>Searching...</span>
                ) : (
                  <>
                    <span>{results.length} results found</span>
                    {searchTime > 0 && (
                      <div className="flex items-center space-x-1">
                        <Clock className="h-4 w-4" />
                        <span>in {searchTime}ms</span>
                      </div>
                    )}
                  </>
                )}
              </div>
              
              <div className="flex items-center space-x-3">
                {/* View mode toggle */}
                <div className="flex items-center space-x-1 bg-gray-100 rounded-lg p-1">
                  <button
                    onClick={() => setViewMode('grid')}
                    className={`p-1.5 rounded ${viewMode === 'grid' ? 'bg-white shadow-sm' : ''}`}
                    title="Grid view"
                  >
                    <Grid className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => setViewMode('list')}
                    className={`p-1.5 rounded ${viewMode === 'list' ? 'bg-white shadow-sm' : ''}`}
                    title="List view"
                  >
                    <List className="h-4 w-4" />
                  </button>
                </div>
                
                {/* Filter toggle */}
                <button
                  onClick={() => setShowFilters(!showFilters)}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors ${
                    showFilters ? 'bg-primary-100 text-primary-700' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  <Filter className="h-4 w-4" />
                  <span>Filters</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex gap-8">
          {/* Filters Sidebar */}
          {showFilters && (
            <motion.div
              initial={{ width: 0, opacity: 0 }}
              animate={{ width: 'auto', opacity: 1 }}
              exit={{ width: 0, opacity: 0 }}
              className="w-80 flex-shrink-0"
            >
              <FilterPanel />
            </motion.div>
          )}

          {/* Results */}
          <div className="flex-1">
            {isLoading ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {[...Array(6)].map((_, index) => (
                  <div key={index} className="bg-white rounded-xl p-6 animate-pulse">
                    <div className="bg-gray-200 h-48 rounded-lg mb-4"></div>
                    <div className="bg-gray-200 h-4 rounded mb-2"></div>
                    <div className="bg-gray-200 h-4 rounded w-2/3 mb-2"></div>
                    <div className="bg-gray-200 h-4 rounded w-1/3"></div>
                  </div>
                ))}
              </div>
            ) : results.length > 0 ? (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className={
                  viewMode === 'grid'
                    ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'
                    : 'space-y-4'
                }
              >
                {results.map((result) => (
                  <ProductCard
                    key={result.id}
                    product={result}
                    viewMode={viewMode}
                    showMatchReasons={true}
                  />
                ))}
              </motion.div>
            ) : query ? (
              <div className="text-center py-16">
                <div className="text-gray-400 text-6xl mb-4">🔍</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  No products found
                </h3>
                <p className="text-gray-600 mb-6">
                  Try adjusting your search terms or filters
                </p>
                <button
                  onClick={() => setShowFilters(true)}
                  className="btn-primary"
                >
                  Adjust Filters
                </button>
              </div>
            ) : (
              <div className="text-center py-16">
                <div className="text-gray-400 text-6xl mb-4">🎯</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  Start Your Search
                </h3>
                <p className="text-gray-600">
                  Enter a search query above to find products
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Search;
