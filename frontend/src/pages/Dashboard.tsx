import React, { useState } from 'react';
import { targetsApi } from '../lib/api.js';
import type { Target } from '../types/api';
import LoadingSpinner from '../components/LoadingSpinner';
import { Search, Sparkles, TrendingUp, CheckCircle, ArrowRight } from 'lucide-react';

export default function Dashboard() {
  const [businessName, setBusinessName] = useState('');
  const [websiteUrl, setWebsiteUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [targetId, setTargetId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      // Step 1: Create target
      const target = await targetsApi.initTarget({
        businessName: businessName.trim(),
        websiteUrl: websiteUrl.trim(),
      });
      
      console.log('✅ Target created:', target.id);
      setTargetId(target.id);
      
      // Step 2: Automatically navigate to analysis page (which will trigger analysis)
      window.location.href = `/analysis?target=${target.id}`;
    } catch (err: any) {
      console.error('❌ Error creating target:', err);
      setError(err.response?.data?.detail || 'Failed to create target. Please try again.');
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl mb-4 shadow-lg">
            <Sparkles className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-3">
            AI Visibility Tracker
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Discover how visible your brand is across AI platforms. 
            Enter your details below to get instant insights.
          </p>
        </div>

        {/* Main Form Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Business Name */}
            <div>
              <label htmlFor="businessName" className="block text-sm font-semibold text-gray-700 mb-2">
                Brand Name
              </label>
              <div className="relative">
                <input
                  type="text"
                  id="businessName"
                  value={businessName}
                  onChange={(e) => setBusinessName(e.target.value)}
                  placeholder="e.g., Acme Corporation"
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all outline-none text-lg"
                  required
                  minLength={2}
                  maxLength={80}
                  disabled={isLoading}
                />
              </div>
            </div>

            {/* Website URL */}
            <div>
              <label htmlFor="websiteUrl" className="block text-sm font-semibold text-gray-700 mb-2">
                Website URL
              </label>
              <div className="relative">
                <input
                  type="url"
                  id="websiteUrl"
                  value={websiteUrl}
                  onChange={(e) => setWebsiteUrl(e.target.value)}
                  placeholder="https://example.com"
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all outline-none text-lg"
                  required
                  disabled={isLoading}
                />
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <div className="bg-red-50 border-2 border-red-200 rounded-xl p-4">
                <p className="text-red-700 text-sm">{error}</p>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading || !businessName.trim() || !websiteUrl.trim()}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold py-4 px-6 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center space-x-2 text-lg"
            >
              {isLoading ? (
                <>
                  <LoadingSpinner size="sm" />
                  <span>Analyzing your brand...</span>
                </>
              ) : (
                <>
                  <Search className="w-5 h-5" />
                  <span>Analyze Visibility</span>
                  <ArrowRight className="w-5 h-5" />
                </>
              )}
            </button>
          </form>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-white rounded-xl p-6 shadow-md">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <Sparkles className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">AI-Powered Analysis</h3>
            <p className="text-sm text-gray-600">Get intelligent insights powered by advanced AI models</p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-md">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
              <TrendingUp className="w-6 h-6 text-purple-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Real-Time Metrics</h3>
            <p className="text-sm text-gray-600">Track your visibility score and performance trends</p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-md">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Actionable Insights</h3>
            <p className="text-sm text-gray-600">Receive recommendations to improve your visibility</p>
          </div>
        </div>
      </div>
    </div>
  );
}
