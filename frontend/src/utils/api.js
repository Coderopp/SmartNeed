import axios from 'axios';
import toast from 'react-hot-toast';

// Create axios instance with default config
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Log request in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`🚀 ${config.method?.toUpperCase()} ${config.url}`, config.data);
    }
    
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    // Log response in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`✅ ${response.config.method?.toUpperCase()} ${response.config.url}`, response.data);
    }
    
    return response;
  },
  (error) => {
    // Handle common error cases
    const { response } = error;
    
    if (response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('auth_token');
      toast.error('Session expired. Please log in again.');
      // Redirect to login page if needed
    } else if (response?.status === 429) {
      // Rate limit exceeded
      toast.error('Too many requests. Please wait a moment and try again.');
    } else if (response?.status >= 500) {
      // Server error
      toast.error('Server error. Please try again later.');
    } else if (response?.status === 404) {
      // Not found
      toast.error('Resource not found.');
    } else if (response?.data?.detail) {
      // API error with detail message
      toast.error(response.data.detail);
    } else if (error.code === 'ECONNABORTED') {
      // Timeout
      toast.error('Request timeout. Please check your connection.');
    } else {
      // Generic error
      toast.error('Something went wrong. Please try again.');
    }
    
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// API methods
export const searchAPI = {
  // Main search endpoint
  search: async (query, filters = {}) => {
    const response = await api.post('/search', {
      query,
      filters,
      sort_by: 'relevance',
      limit: 20,
      offset: 0,
      include_similar: true,
      min_similarity: 0.5
    });
    return response.data;
  },

  // Autocomplete suggestions
  autocomplete: async (partialQuery) => {
    const response = await api.get('/search/autocomplete', {
      params: { q: partialQuery, limit: 10 }
    });
    return response.data;
  },

  // Popular searches
  getPopularSearches: async (category = null) => {
    const response = await api.get('/search/popular', {
      params: { category, limit: 20 }
    });
    return response.data;
  },

  // Search suggestions
  getSuggestions: async (category = null) => {
    const response = await api.get('/search/suggestions', {
      params: { category, limit: 10 }
    });
    return response.data;
  },

  // Submit search feedback
  submitFeedback: async (feedback) => {
    const response = await api.post('/search/feedback', feedback);
    return response.data;
  },

  // Find similar products
  findSimilar: async (productId, limit = 10) => {
    const response = await api.post('/search/similar', null, {
      params: { product_id: productId, limit }
    });
    return response.data;
  },

  // Get search categories
  getCategories: async () => {
    const response = await api.get('/search/categories');
    return response.data;
  }
};

export const productsAPI = {
  // Get product details
  getProduct: async (productId) => {
    const response = await api.get(`/products/${productId}`);
    return response.data;
  },

  // Get multiple products
  getProducts: async (productIds) => {
    const response = await api.post('/products/batch', { product_ids: productIds });
    return response.data;
  },

  // Get product statistics
  getStats: async () => {
    const response = await api.get('/products/stats');
    return response.data;
  }
};

export const comparisonAPI = {
  // Compare products
  compareProducts: async (productIds) => {
    const response = await api.post('/compare', { product_ids: productIds });
    return response.data;
  },

  // Get comparison history
  getHistory: async () => {
    const response = await api.get('/compare/history');
    return response.data;
  }
};

export const exportAPI = {
  // Export to Google Sheets
  exportToSheets: async (data, sheetName = 'Product Comparison') => {
    const response = await api.post('/export/sheets', {
      data,
      sheet_name: sheetName,
      include_images: true,
      include_links: true
    });
    return response.data;
  },

  // Get export history
  getExportHistory: async () => {
    const response = await api.get('/export/history');
    return response.data;
  }
};

// Health check
export const healthCheck = async () => {
  try {
    const response = await api.get('/status');
    return response.data;
  } catch (error) {
    throw new Error('API is not available');
  }
};

// Export the main api instance for custom requests
export default api;
