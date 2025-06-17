import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { User, Settings, Heart, Clock, Download, Bell, Shield, HelpCircle } from 'lucide-react';

const Profile = () => {
  const [activeTab, setActiveTab] = useState('preferences');
  const [user, setUser] = useState({
    name: 'John Doe',
    email: 'john.doe@example.com',
    avatar: '/api/placeholder/150/150',
    preferences: {
      budget_range: { min: 100, max: 2000 },
      preferred_categories: ['Electronics', 'Books', 'Sports'],
      notification_preferences: {
        price_drops: true,
        new_products: false,
        recommendations: true
      }
    }
  });

  const [searchHistory] = useState([
    { query: 'wireless headphones for gym', timestamp: '2 hours ago', results: 23 },
    { query: 'gaming laptop under $1500', timestamp: '1 day ago', results: 18 },
    { query: 'ergonomic office chair', timestamp: '3 days ago', results: 31 },
    { query: 'coffee maker with grinder', timestamp: '1 week ago', results: 15 }
  ]);

  const [favorites] = useState([
    {
      id: '1',
      name: 'Sony WH-1000XM4 Headphones',
      price: 348,
      image: '/api/placeholder/150/150',
      saved_date: '2024-06-15'
    },
    {
      id: '2',
      name: 'MacBook Pro 14" M3',
      price: 1999,
      image: '/api/placeholder/150/150',
      saved_date: '2024-06-14'
    }
  ]);

  const tabs = [
    { id: 'preferences', label: 'Preferences', icon: Settings },
    { id: 'history', label: 'Search History', icon: Clock },
    { id: 'favorites', label: 'Favorites', icon: Heart },
    { id: 'exports', label: 'Exports', icon: Download },
    { id: 'settings', label: 'Settings', icon: User }
  ];

  const PreferencesTab = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Budget Preferences
        </h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Minimum Budget
            </label>
            <input
              type="number"
              value={user.preferences.budget_range.min}
              onChange={(e) => setUser(prev => ({
                ...prev,
                preferences: {
                  ...prev.preferences,
                  budget_range: {
                    ...prev.preferences.budget_range,
                    min: parseInt(e.target.value)
                  }
                }
              }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Maximum Budget
            </label>
            <input
              type="number"
              value={user.preferences.budget_range.max}
              onChange={(e) => setUser(prev => ({
                ...prev,
                preferences: {
                  ...prev.preferences,
                  budget_range: {
                    ...prev.preferences.budget_range,
                    max: parseInt(e.target.value)
                  }
                }
              }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Preferred Categories
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {['Electronics', 'Fashion', 'Home & Garden', 'Sports', 'Books', 'Health'].map((category) => (
            <label key={category} className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={user.preferences.preferred_categories.includes(category)}
                onChange={(e) => {
                  const checked = e.target.checked;
                  setUser(prev => ({
                    ...prev,
                    preferences: {
                      ...prev.preferences,
                      preferred_categories: checked
                        ? [...prev.preferences.preferred_categories, category]
                        : prev.preferences.preferred_categories.filter(c => c !== category)
                    }
                  }));
                }}
                className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />
              <span className="text-sm text-gray-700">{category}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Notification Preferences
        </h3>
        <div className="space-y-3">
          {Object.entries(user.preferences.notification_preferences).map(([key, value]) => (
            <label key={key} className="flex items-center justify-between">
              <span className="text-sm text-gray-700 capitalize">
                {key.replace(/_/g, ' ')}
              </span>
              <input
                type="checkbox"
                checked={value}
                onChange={(e) => setUser(prev => ({
                  ...prev,
                  preferences: {
                    ...prev.preferences,
                    notification_preferences: {
                      ...prev.preferences.notification_preferences,
                      [key]: e.target.checked
                    }
                  }
                }))}
                className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />
            </label>
          ))}
        </div>
      </div>
    </div>
  );

  const HistoryTab = () => (
    <div className="bg-white rounded-xl border border-gray-200">
      <div className="p-6 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">Search History</h3>
      </div>
      <div className="divide-y divide-gray-200">
        {searchHistory.map((search, index) => (
          <div key={index} className="p-6 hover:bg-gray-50 transition-colors">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium text-gray-900">{search.query}</h4>
                <p className="text-sm text-gray-600">
                  {search.results} results • {search.timestamp}
                </p>
              </div>
              <button className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                Search Again
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const FavoritesTab = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {favorites.map((item) => (
        <div key={item.id} className="bg-white rounded-xl border border-gray-200 p-6">
          <img
            src={item.image}
            alt={item.name}
            className="w-full h-32 object-cover rounded-lg mb-4"
          />
          <h4 className="font-medium text-gray-900 mb-2">{item.name}</h4>
          <p className="text-lg font-bold text-gray-900 mb-2">${item.price}</p>
          <p className="text-sm text-gray-600 mb-4">Saved on {item.saved_date}</p>
          <div className="flex space-x-2">
            <button className="flex-1 btn-primary text-sm">View Product</button>
            <button className="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
              <Heart className="h-4 w-4 text-red-500 fill-current" />
            </button>
          </div>
        </div>
      ))}
    </div>
  );

  const ExportsTab = () => (
    <div className="bg-white rounded-xl border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Export History</h3>
      <div className="text-center py-8">
        <Download className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-600">No exports yet</p>
        <p className="text-sm text-gray-500 mt-2">
          Export product comparisons to Google Sheets to see them here
        </p>
      </div>
    </div>
  );

  const SettingsTab = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Account Information
        </h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Full Name
            </label>
            <input
              type="text"
              value={user.name}
              onChange={(e) => setUser(prev => ({ ...prev, name: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email Address
            </label>
            <input
              type="email"
              value={user.email}
              onChange={(e) => setUser(prev => ({ ...prev, email: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Privacy & Security
        </h3>
        <div className="space-y-3">
          <button className="flex items-center justify-between w-full p-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
            <div className="flex items-center space-x-3">
              <Shield className="h-5 w-5 text-gray-600" />
              <span>Change Password</span>
            </div>
            <span className="text-gray-400">›</span>
          </button>
          <button className="flex items-center justify-between w-full p-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
            <div className="flex items-center space-x-3">
              <Bell className="h-5 w-5 text-gray-600" />
              <span>Notification Settings</span>
            </div>
            <span className="text-gray-400">›</span>
          </button>
          <button className="flex items-center justify-between w-full p-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
            <div className="flex items-center space-x-3">
              <HelpCircle className="h-5 w-5 text-gray-600" />
              <span>Privacy Policy</span>
            </div>
            <span className="text-gray-400">›</span>
          </button>
        </div>
      </div>
    </div>
  );

  const renderTabContent = () => {
    switch (activeTab) {
      case 'preferences':
        return <PreferencesTab />;
      case 'history':
        return <HistoryTab />;
      case 'favorites':
        return <FavoritesTab />;
      case 'exports':
        return <ExportsTab />;
      case 'settings':
        return <SettingsTab />;
      default:
        return <PreferencesTab />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-4 mb-4">
            <img
              src={user.avatar}
              alt={user.name}
              className="w-16 h-16 rounded-full object-cover"
            />
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{user.name}</h1>
              <p className="text-gray-600">{user.email}</p>
            </div>
          </div>
        </div>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar */}
          <div className="lg:w-64 flex-shrink-0">
            <nav className="bg-white rounded-xl border border-gray-200 p-2">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-left transition-colors ${
                      activeTab === tab.id
                        ? 'bg-primary-50 text-primary-700'
                        : 'text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    <Icon className="h-5 w-5" />
                    <span className="font-medium">{tab.label}</span>
                  </button>
                );
              })}
            </nav>
          </div>

          {/* Main Content */}
          <div className="flex-1">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              {renderTabContent()}
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
