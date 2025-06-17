import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Plus, X, Star, ExternalLink, Download, BarChart3 } from 'lucide-react';
import ProductCard from '../components/ProductCard';

const Compare = () => {
  const [selectedProducts, setSelectedProducts] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [comparisonData, setComparisonData] = useState(null);

  // Mock data for demonstration
  const mockProducts = [
    {
      id: '1',
      product_id: 'laptop-1',
      name: 'MacBook Pro 14" M3',
      brand: 'Apple',
      price: 1999,
      original_price: 2199,
      rating: 4.8,
      review_count: 256,
      image_url: '/api/placeholder/300/300',
      description: 'Powerful laptop with M3 chip for professional work',
      features: ['M3 Chip', '16GB RAM', '512GB SSD', '14" Retina Display'],
      specifications: {
        'Processor': 'Apple M3',
        'RAM': '16GB',
        'Storage': '512GB SSD',
        'Display': '14.2" Liquid Retina XDR',
        'Battery': 'Up to 18 hours',
        'Weight': '3.5 lbs'
      }
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
      features: ['Intel i7', '16GB RAM', '512GB SSD', '13.4" Display'],
      specifications: {
        'Processor': 'Intel Core i7-1360P',
        'RAM': '16GB LPDDR5',
        'Storage': '512GB SSD',
        'Display': '13.4" FHD+',
        'Battery': 'Up to 12 hours',
        'Weight': '2.64 lbs'
      }
    }
  ];

  useEffect(() => {
    // Load any products from URL params or localStorage
    const urlParams = new URLSearchParams(window.location.search);
    const productIds = urlParams.get('products');
    if (productIds) {
      const ids = productIds.split(',');
      const products = mockProducts.filter(p => ids.includes(p.product_id));
      setSelectedProducts(products);
    }
  }, []);

  const handleSearch = async (query) => {
    if (!query.trim()) {
      setSearchResults([]);
      return;
    }

    setIsSearching(true);
    
    // Simulate API search
    setTimeout(() => {
      const results = mockProducts.filter(product =>
        product.name.toLowerCase().includes(query.toLowerCase()) ||
        product.brand.toLowerCase().includes(query.toLowerCase())
      );
      setSearchResults(results);
      setIsSearching(false);
    }, 500);
  };

  const addToComparison = (product) => {
    if (selectedProducts.length >= 4) {
      alert('You can compare up to 4 products at once');
      return;
    }
    
    if (selectedProducts.find(p => p.id === product.id)) {
      alert('Product already added to comparison');
      return;
    }

    setSelectedProducts([...selectedProducts, product]);
  };

  const removeFromComparison = (productId) => {
    setSelectedProducts(selectedProducts.filter(p => p.id !== productId));
  };

  const exportComparison = () => {
    // TODO: Implement export to Google Sheets
    alert('Export functionality will be implemented with Google Sheets API');
  };

  const ComparisonTable = () => {
    if (selectedProducts.length < 2) return null;

    const allSpecs = new Set();
    selectedProducts.forEach(product => {
      Object.keys(product.specifications || {}).forEach(spec => allSpecs.add(spec));
    });

    return (
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-900">
              Product Comparison
            </h3>
            <button
              onClick={exportComparison}
              className="flex items-center space-x-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              <Download className="h-4 w-4" />
              <span>Export</span>
            </button>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-900 w-40">
                  Feature
                </th>
                {selectedProducts.map((product) => (
                  <th key={product.id} className="px-6 py-4 text-center min-w-[200px]">
                    <div className="space-y-2">
                      <img
                        src={product.image_url}
                        alt={product.name}
                        className="w-16 h-16 object-cover rounded-lg mx-auto"
                      />
                      <div>
                        <h4 className="font-medium text-gray-900 text-sm line-clamp-2">
                          {product.name}
                        </h4>
                        <p className="text-sm text-gray-600">{product.brand}</p>
                      </div>
                      <button
                        onClick={() => removeFromComparison(product.id)}
                        className="p-1 text-gray-400 hover:text-red-500 transition-colors"
                      >
                        <X className="h-4 w-4" />
                      </button>
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {/* Price Row */}
              <tr>
                <td className="px-6 py-4 font-medium text-gray-900">Price</td>
                {selectedProducts.map((product) => (
                  <td key={product.id} className="px-6 py-4 text-center">
                    <div className="text-lg font-bold text-gray-900">
                      ${product.price}
                    </div>
                    {product.original_price && product.original_price > product.price && (
                      <div className="text-sm text-gray-500 line-through">
                        ${product.original_price}
                      </div>
                    )}
                  </td>
                ))}
              </tr>

              {/* Rating Row */}
              <tr className="bg-gray-50">
                <td className="px-6 py-4 font-medium text-gray-900">Rating</td>
                {selectedProducts.map((product) => (
                  <td key={product.id} className="px-6 py-4 text-center">
                    <div className="flex items-center justify-center space-x-1">
                      <Star className="h-4 w-4 text-yellow-400 fill-current" />
                      <span className="font-medium">{product.rating}</span>
                      <span className="text-sm text-gray-500">
                        ({product.review_count})
                      </span>
                    </div>
                  </td>
                ))}
              </tr>

              {/* Specifications */}
              {Array.from(allSpecs).map((spec, index) => (
                <tr key={spec} className={index % 2 === 0 ? 'bg-gray-50' : ''}>
                  <td className="px-6 py-4 font-medium text-gray-900">{spec}</td>
                  {selectedProducts.map((product) => (
                    <td key={product.id} className="px-6 py-4 text-center text-gray-600">
                      {product.specifications?.[spec] || '-'}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Product Comparison
          </h1>
          <p className="text-gray-600">
            Compare products side by side to make informed decisions
          </p>
        </div>

        {/* Search Section */}
        <div className="bg-white rounded-xl border border-gray-200 p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Add Products to Compare
          </h2>
          
          <div className="mb-4">
            <input
              type="text"
              placeholder="Search for products to compare..."
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                handleSearch(e.target.value);
              }}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          {/* Search Results */}
          {searchResults.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {searchResults.map((product) => (
                <div key={product.id} className="relative">
                  <ProductCard product={product} viewMode="grid" />
                  <button
                    onClick={() => addToComparison(product)}
                    className="absolute top-3 right-3 p-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
                    title="Add to comparison"
                  >
                    <Plus className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Selected Products */}
        {selectedProducts.length > 0 && (
          <div className="mb-8">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Selected Products ({selectedProducts.length}/4)
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {selectedProducts.map((product) => (
                <div key={product.id} className="relative">
                  <ProductCard product={product} viewMode="grid" />
                  <button
                    onClick={() => removeFromComparison(product.id)}
                    className="absolute top-3 right-3 p-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
                    title="Remove from comparison"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Comparison Table */}
        {selectedProducts.length >= 2 ? (
          <ComparisonTable />
        ) : (
          <div className="text-center py-16">
            <BarChart3 className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Add Products to Compare
            </h3>
            <p className="text-gray-600 max-w-md mx-auto">
              Search and select at least 2 products to see a detailed comparison table
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Compare;
