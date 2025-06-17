import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Star, Heart, Eye, ShoppingCart, ExternalLink, Zap } from 'lucide-react';

const ProductCard = ({ product, viewMode = 'grid', showMatchReasons = false }) => {
  const [isLiked, setIsLiked] = useState(false);
  const [imageLoaded, setImageLoaded] = useState(false);

  const {
    name,
    brand,
    price,
    original_price,
    rating,
    review_count,
    image_url,
    description,
    similarity_score,
    match_reasons = [],
    source,
    in_stock = true
  } = product;

  const discount = original_price && price < original_price 
    ? Math.round(((original_price - price) / original_price) * 100)
    : null;

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
    }).format(price);
  };

  const handleImageError = (e) => {
    e.target.src = '/api/placeholder/300/300';
  };

  if (viewMode === 'list') {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-all duration-200"
      >
        <div className="flex space-x-6">
          {/* Image */}
          <div className="flex-shrink-0">
            <div className="w-32 h-32 relative">
              <img
                src={image_url || '/api/placeholder/300/300'}
                alt={name}
                onError={handleImageError}
                onLoad={() => setImageLoaded(true)}
                className={`w-full h-full object-cover rounded-lg transition-opacity duration-200 ${
                  imageLoaded ? 'opacity-100' : 'opacity-0'
                }`}
              />
              {!imageLoaded && (
                <div className="absolute inset-0 bg-gray-200 rounded-lg animate-pulse"></div>
              )}
            </div>
          </div>

          {/* Content */}
          <div className="flex-1 min-w-0">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900 mb-1 line-clamp-2">
                  {name}
                </h3>
                {brand && (
                  <p className="text-sm text-gray-600 mb-2">{brand}</p>
                )}
                
                {/* Rating */}
                {rating && (
                  <div className="flex items-center space-x-2 mb-3">
                    <div className="flex items-center">
                      <Star className="h-4 w-4 text-yellow-400 fill-current" />
                      <span className="text-sm font-medium text-gray-900 ml-1">
                        {rating}
                      </span>
                    </div>
                    {review_count && (
                      <span className="text-sm text-gray-500">
                        ({review_count} reviews)
                      </span>
                    )}
                  </div>
                )}

                {/* Description */}
                <p className="text-gray-600 text-sm line-clamp-2 mb-3">
                  {description}
                </p>

                {/* Match reasons */}
                {showMatchReasons && match_reasons.length > 0 && (
                  <div className="mb-3">
                    <div className="flex items-center space-x-1 mb-2">
                      <Zap className="h-4 w-4 text-primary-600" />
                      <span className="text-sm font-medium text-primary-600">
                        Why this matches ({Math.round(similarity_score * 100)}%)
                      </span>
                    </div>
                    <div className="flex flex-wrap gap-1">
                      {match_reasons.slice(0, 3).map((reason, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 bg-primary-50 text-primary-700 text-xs rounded-full"
                        >
                          {reason}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Price and actions */}
              <div className="flex flex-col items-end space-y-3 ml-4">
                <div className="text-right">
                  <div className="text-2xl font-bold text-gray-900">
                    {formatPrice(price)}
                  </div>
                  {original_price && discount && (
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-gray-500 line-through">
                        {formatPrice(original_price)}
                      </span>
                      <span className="text-sm font-medium text-green-600">
                        -{discount}%
                      </span>
                    </div>
                  )}
                </div>

                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => setIsLiked(!isLiked)}
                    className={`p-2 rounded-lg transition-colors ${
                      isLiked ? 'bg-red-100 text-red-600' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                  >
                    <Heart className={`h-4 w-4 ${isLiked ? 'fill-current' : ''}`} />
                  </button>
                  
                  <button className="p-2 bg-gray-100 text-gray-600 hover:bg-gray-200 rounded-lg transition-colors">
                    <Eye className="h-4 w-4" />
                  </button>
                  
                  <button 
                    className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center space-x-2"
                    disabled={!in_stock}
                  >
                    <ShoppingCart className="h-4 w-4" />
                    <span>{in_stock ? 'View Product' : 'Out of Stock'}</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    );
  }

  // Grid view
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -4 }}
      className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-lg transition-all duration-200"
    >
      {/* Image */}
      <div className="relative">
        <div className="aspect-square w-full relative">
          <img
            src={image_url || '/api/placeholder/300/300'}
            alt={name}
            onError={handleImageError}
            onLoad={() => setImageLoaded(true)}
            className={`w-full h-full object-cover transition-opacity duration-200 ${
              imageLoaded ? 'opacity-100' : 'opacity-0'
            }`}
          />
          {!imageLoaded && (
            <div className="absolute inset-0 bg-gray-200 animate-pulse"></div>
          )}
        </div>

        {/* Discount badge */}
        {discount && (
          <div className="absolute top-3 left-3 bg-red-500 text-white text-xs font-medium px-2 py-1 rounded-full">
            -{discount}%
          </div>
        )}

        {/* Quick actions */}
        <div className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity">
          <button
            onClick={() => setIsLiked(!isLiked)}
            className={`p-2 rounded-full backdrop-blur-sm transition-colors ${
              isLiked ? 'bg-red-100 text-red-600' : 'bg-white/80 text-gray-600 hover:bg-white'
            }`}
          >
            <Heart className={`h-4 w-4 ${isLiked ? 'fill-current' : ''}`} />
          </button>
        </div>

        {/* Stock indicator */}
        {!in_stock && (
          <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
            <span className="text-white font-medium">Out of Stock</span>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-4">
        {/* Brand */}
        {brand && (
          <p className="text-sm text-gray-600 mb-1">{brand}</p>
        )}

        {/* Title */}
        <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2 min-h-[2.5rem]">
          {name}
        </h3>

        {/* Rating */}
        {rating && (
          <div className="flex items-center space-x-2 mb-3">
            <div className="flex items-center">
              <Star className="h-4 w-4 text-yellow-400 fill-current" />
              <span className="text-sm font-medium text-gray-900 ml-1">
                {rating}
              </span>
            </div>
            {review_count && (
              <span className="text-sm text-gray-500">
                ({review_count})
              </span>
            )}
          </div>
        )}

        {/* Match reasons */}
        {showMatchReasons && match_reasons.length > 0 && (
          <div className="mb-3">
            <div className="flex items-center space-x-1 mb-2">
              <Zap className="h-3 w-3 text-primary-600" />
              <span className="text-xs font-medium text-primary-600">
                {Math.round(similarity_score * 100)}% match
              </span>
            </div>
            <div className="flex flex-wrap gap-1">
              {match_reasons.slice(0, 2).map((reason, index) => (
                <span
                  key={index}
                  className="px-2 py-0.5 bg-primary-50 text-primary-700 text-xs rounded-full line-clamp-1"
                >
                  {reason}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Price */}
        <div className="mb-4">
          <div className="text-xl font-bold text-gray-900">
            {formatPrice(price)}
          </div>
          {original_price && discount && (
            <div className="text-sm text-gray-500 line-through">
              {formatPrice(original_price)}
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex space-x-2">
          <button 
            className="flex-1 btn-primary text-sm py-2 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={!in_stock}
          >
            {in_stock ? 'View Product' : 'Out of Stock'}
          </button>
          
          <button className="p-2 btn-secondary">
            <ExternalLink className="h-4 w-4" />
          </button>
        </div>

        {/* Source */}
        {source && (
          <div className="mt-2 text-xs text-gray-500 text-center">
            from {source}
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default ProductCard;
