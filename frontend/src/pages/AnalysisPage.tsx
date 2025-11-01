import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { targetsApi } from '../lib/api';
import AnalysisResults from '../components/AnalysisResults';
import LoadingSpinner from '../components/LoadingSpinner';
import { ArrowLeft, AlertCircle, Sparkles } from 'lucide-react';

export default function AnalysisPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const targetId = searchParams.get('target');

  const { data: target, isLoading: targetLoading, error: targetError } = useQuery({
    queryKey: ['target', targetId],
    queryFn: () => targetsApi.getTarget(targetId!),
    enabled: !!targetId,
  });

  const { data: analysis, isLoading: analysisLoading, error: analysisError } = useQuery({
    queryKey: ['analysis', targetId],
    queryFn: async () => {
      console.log('🔍 Starting analysis for target:', targetId);
      const result = await targetsApi.analyzeTarget(targetId!);
      console.log('✅ Analysis complete:', result.score.visibilityScore);
      return result;
    },
    enabled: !!targetId,
    retry: 2,
  });

  if (!targetId) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <div className="text-center max-w-md mx-auto px-4">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <AlertCircle className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No Analysis Selected</h3>
          <p className="text-gray-600 mb-6">
            Please start by analyzing your brand visibility from the home page.
          </p>
          <button
            onClick={() => navigate('/')}
            className="bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold py-3 px-6 rounded-xl hover:shadow-lg transition-all"
          >
            Start New Analysis
          </button>
        </div>
      </div>
    );
  }

  if (targetLoading || analysisLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl mb-4 shadow-lg animate-pulse">
            <Sparkles className="w-8 h-8 text-white" />
          </div>
          <LoadingSpinner size="lg" className="mx-auto mb-4" />
          <p className="text-gray-600 text-lg">
            {targetLoading ? 'Loading your brand data...' : 'Analyzing visibility...'}
          </p>
          <p className="text-gray-500 text-sm mt-2">This may take a few moments</p>
        </div>
      </div>
    );
  }

  if (targetError || analysisError) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <div className="text-center max-w-md mx-auto px-4">
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <AlertCircle className="w-8 h-8 text-red-600" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Analysis Failed</h3>
          <p className="text-gray-600 mb-6">
            {targetError ? 'Failed to load brand data' : 'Failed to run analysis'}
          </p>
          <button
            onClick={() => navigate('/')}
            className="bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold py-3 px-6 rounded-xl hover:shadow-lg transition-all"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (!target || !analysis) {
    return null;
  }

  return (
    <div className="bg-gradient-to-br from-blue-50 via-white to-purple-50 min-h-screen">
      {/* Back Button */}
      <div className="max-w-6xl mx-auto px-4 pt-8">
        <button
          onClick={() => navigate('/')}
          className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors mb-6"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Home</span>
        </button>
      </div>

      {/* Brand Info Header */}
      <div className="bg-white border-b border-gray-200 mb-8">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">{target.businessName}</h2>
              <a 
                href={target.websiteUrl} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-blue-600 hover:text-blue-700 text-sm mt-1 inline-block"
              >
                {target.websiteUrl}
              </a>
            </div>
            <button
              onClick={() => navigate('/')}
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold py-2 px-4 rounded-lg hover:shadow-lg transition-all text-sm"
            >
              New Analysis
            </button>
          </div>
        </div>
      </div>

      {/* Analysis Results */}
      <AnalysisResults analysis={analysis} />
    </div>
  );
}
