import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Target, Brain, Zap, TrendingUp, Star, Users } from 'lucide-react';
import SearchInterface from '../components/SearchInterface';

const Home = () => {
  const [featuredCategories] = useState([
    { name: 'Electronics', icon: '💻', count: '12K+ products' },
    { name: 'Home & Garden', icon: '🏠', count: '8K+ products' },
    { name: 'Fashion', icon: '👕', count: '15K+ products' },
    { name: 'Sports', icon: '⚽', count: '6K+ products' },
    { name: 'Books', icon: '📚', count: '20K+ products' },
    { name: 'Health', icon: '💊', count: '4K+ products' }
  ]);

  const features = [
    {
      icon: Brain,
      title: "AI-Powered Understanding",
      description: "Describe what you need in natural language. Our AI understands context, preferences, and requirements."
    },
    {
      icon: Target,
      title: "Perfect Matches",
      description: "Get products that actually fit your needs, budget, and use case - not just keyword matches."
    },
    {
      icon: Zap,
      title: "Lightning Fast",
      description: "Semantic search powered by advanced embeddings delivers relevant results in milliseconds."
    },
    {
      icon: TrendingUp,
      title: "Smart Comparisons",
      description: "AI-generated comparisons highlight key differences and help you make informed decisions."
    }
  ];

  const testimonials = [
    {
      name: "Sarah Chen",
      role: "Product Manager",
      content: "Finally, a search that understands what I actually need! Found the perfect laptop for my design work in minutes.",
      rating: 5
    },
    {
      name: "Mike Rodriguez", 
      role: "Small Business Owner",
      content: "SMARTNEED helped me find office equipment that fit my exact budget and requirements. Game changer!",
      rating: 5
    },
    {
      name: "Emily Johnson",
      role: "Student",
      content: "Love how I can just describe what I need instead of guessing keywords. The AI really gets it!",
      rating: 5
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-primary-50 via-white to-accent-50 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
                Find Products That{' '}
                <span className="text-primary-600">Actually Fit</span>{' '}
                Your Needs
              </h1>
              <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
                Skip the keyword guessing game. Describe what you're looking for in plain English 
                and let our AI find the perfect products for your specific requirements and budget.
              </p>
            </motion.div>

            {/* Search Interface */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="max-w-3xl mx-auto mb-12"
            >
              <SearchInterface 
                placeholder="Try: 'quiet laptop for video calls under $1000' or 'ergonomic chair for back pain'"
                autoFocus={true}
                className="transform hover:scale-[1.02] transition-transform duration-200"
              />
            </motion.div>

            {/* Quick examples */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="flex flex-wrap justify-center gap-3 mb-16"
            >
              <span className="text-gray-500 text-sm">Try searching for:</span>
              {[
                "wireless headphones for gym",
                "coffee maker for small apartment", 
                "gaming mouse under $50"
              ].map((example, index) => (
                <button
                  key={index}
                  className="px-4 py-2 bg-white border border-gray-200 rounded-full text-sm text-gray-700 hover:border-primary-300 hover:text-primary-600 transition-all duration-200"
                  onClick={() => window.location.href = `/search?q=${encodeURIComponent(example)}`}
                >
                  {example}
                </button>
              ))}
            </motion.div>

            {/* Stats */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.6 }}
              className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-2xl mx-auto"
            >
              <div className="text-center">
                <div className="text-3xl font-bold text-primary-600">50K+</div>
                <div className="text-gray-600">Products Analyzed</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-primary-600">95%</div>
                <div className="text-gray-600">Accuracy Rate</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-primary-600">&lt; 1s</div>
                <div className="text-gray-600">Average Search Time</div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              How SMARTNEED Works
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Advanced AI technology that understands your needs and finds products 
              that actually match your requirements.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="text-center"
              >
                <div className="w-16 h-16 mx-auto mb-4 bg-primary-100 rounded-2xl flex items-center justify-center">
                  <feature.icon className="h-8 w-8 text-primary-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Popular Categories
            </h2>
            <p className="text-xl text-gray-600">
              Explore products across all categories with AI-powered search
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {featuredCategories.map((category, index) => (
              <motion.button
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.3, delay: index * 0.05 }}
                viewport={{ once: true }}
                whileHover={{ scale: 1.05 }}
                className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 hover:shadow-md transition-all duration-200"
                onClick={() => window.location.href = `/search?category=${encodeURIComponent(category.name)}`}
              >
                <div className="text-4xl mb-3">{category.icon}</div>
                <h3 className="font-semibold text-gray-900 mb-1">{category.name}</h3>
                <p className="text-sm text-gray-500">{category.count}</p>
              </motion.button>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              What Our Users Say
            </h2>
            <p className="text-xl text-gray-600">
              Real feedback from people who found exactly what they needed
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-gray-50 p-6 rounded-2xl"
              >
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                <p className="text-gray-600 mb-4 italic">
                  "{testimonial.content}"
                </p>
                <div>
                  <div className="font-semibold text-gray-900">{testimonial.name}</div>
                  <div className="text-sm text-gray-500">{testimonial.role}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold text-white mb-4">
              Ready to Find Your Perfect Product?
            </h2>
            <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
              Join thousands of satisfied users who found exactly what they needed with SMARTNEED's AI-powered search.
            </p>
            <button
              onClick={() => document.querySelector('input').focus()}
              className="px-8 py-4 bg-white text-primary-600 font-semibold rounded-xl hover:bg-gray-50 transition-all duration-200 shadow-lg"
            >
              Start Searching Now
            </button>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default Home;
