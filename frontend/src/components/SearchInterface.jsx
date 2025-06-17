import React, { useState, useRef, useEffect } from 'react';
import { Search, Mic, Camera, Loader } from 'lucide-react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

const SearchInterface = ({ 
  onSearch, 
  placeholder = "Describe what you're looking for...", 
  initialQuery = "",
  className = "",
  autoFocus = false,
  showSuggestions = true 
}) => {
  const [query, setQuery] = useState(initialQuery);
  const [isLoading, setIsLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestionsList, setShowSuggestionsList] = useState(false);
  const [isListening, setIsListening] = useState(false);
  
  const inputRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (autoFocus && inputRef.current) {
      inputRef.current.focus();
    }
  }, [autoFocus]);

  // Example search suggestions - in real app, fetch from API
  const exampleSuggestions = [
    "quiet laptop for video calls under $1000",
    "wireless headphones with noise cancellation",
    "ergonomic office chair for back pain",
    "gaming mouse with RGB lighting",
    "portable bluetooth speaker waterproof",
    "smartphone with best camera under $500",
    "running shoes for flat feet",
    "coffee maker with built-in grinder"
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) {
      toast.error('Please enter a search query');
      return;
    }

    setIsLoading(true);
    setShowSuggestionsList(false);

    try {
      if (onSearch) {
        await onSearch(query);
      } else {
        // Navigate to search page with query
        navigate(`/search?q=${encodeURIComponent(query)}`);
      }
    } catch (error) {
      console.error('Search error:', error);
      toast.error('Search failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setQuery(value);
    
    if (showSuggestions && value.length > 2) {
      // Filter suggestions based on input
      const filtered = exampleSuggestions.filter(suggestion =>
        suggestion.toLowerCase().includes(value.toLowerCase())
      ).slice(0, 5);
      setSuggestions(filtered);
      setShowSuggestionsList(true);
    } else {
      setShowSuggestionsList(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setQuery(suggestion);
    setShowSuggestionsList(false);
    // Auto-submit when suggestion is clicked
    setTimeout(() => {
      handleSubmit({ preventDefault: () => {} });
    }, 100);
  };

  const handleVoiceSearch = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      toast.error('Voice search not supported in this browser');
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    setIsListening(true);

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setQuery(transcript);
      setIsListening(false);
      toast.success('Voice input captured!');
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      setIsListening(false);
      toast.error('Voice search failed. Please try again.');
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.start();
  };

  return (
    <div className={`relative ${className}`}>
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative">
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={handleInputChange}
            onFocus={() => showSuggestions && query.length > 2 && setShowSuggestionsList(true)}
            onBlur={() => setTimeout(() => setShowSuggestionsList(false), 200)}
            placeholder={placeholder}
            className="w-full pl-12 pr-24 py-4 text-lg border-2 border-gray-200 rounded-2xl focus:border-primary-500 focus:ring-0 outline-none transition-all duration-200 bg-white shadow-sm"
            disabled={isLoading}
          />
          
          {/* Search icon */}
          <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
          
          {/* Action buttons */}
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center space-x-2">
            {/* Voice search button */}
            <button
              type="button"
              onClick={handleVoiceSearch}
              className={`p-2 rounded-lg transition-all duration-200 ${
                isListening 
                  ? 'bg-red-100 text-red-600' 
                  : 'bg-gray-100 hover:bg-gray-200 text-gray-600'
              }`}
              title="Voice search"
            >
              <Mic className={`h-4 w-4 ${isListening ? 'animate-pulse' : ''}`} />
            </button>
            
            {/* Visual search button (placeholder) */}
            <button
              type="button"
              className="p-2 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-600 transition-all duration-200"
              title="Visual search (coming soon)"
              onClick={() => toast.info('Visual search coming soon!')}
            >
              <Camera className="h-4 w-4" />
            </button>
            
            {/* Submit button */}
            <button
              type="submit"
              disabled={isLoading || !query.trim()}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 font-medium"
            >
              {isLoading ? (
                <Loader className="h-4 w-4 animate-spin" />
              ) : (
                'Search'
              )}
            </button>
          </div>
        </div>
      </form>

      {/* Suggestions dropdown */}
      {showSuggestionsList && suggestions.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          className="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-xl shadow-lg z-50 max-h-60 overflow-y-auto"
        >
          {suggestions.map((suggestion, index) => (
            <button
              key={index}
              onClick={() => handleSuggestionClick(suggestion)}
              className="w-full text-left px-4 py-3 hover:bg-gray-50 transition-colors duration-150 border-b border-gray-100 last:border-b-0 first:rounded-t-xl last:rounded-b-xl"
            >
              <div className="flex items-center">
                <Search className="h-4 w-4 text-gray-400 mr-3" />
                <span className="text-gray-900">{suggestion}</span>
              </div>
            </button>
          ))}
        </motion.div>
      )}

      {/* Voice search indicator */}
      {isListening && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="absolute top-full left-0 right-0 mt-2 p-4 bg-red-50 border border-red-200 rounded-xl"
        >
          <div className="flex items-center justify-center text-red-600">
            <Mic className="h-5 w-5 mr-2 animate-pulse" />
            <span>Listening... Speak now</span>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default SearchInterface;
