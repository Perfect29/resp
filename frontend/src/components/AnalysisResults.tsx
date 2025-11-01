import React from 'react';
import type { AnalyzeResponse } from '../types/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadialBarChart, RadialBar, Cell } from 'recharts';
import { TrendingUp, CheckCircle, XCircle, AlertCircle } from 'lucide-react';

interface AnalysisResultsProps {
  analysis: AnalyzeResponse;
}

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ef4444'];

export default function AnalysisResults({ analysis }: AnalysisResultsProps) {
  const { score } = analysis;

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-blue-600';
    if (score >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-green-100';
    if (score >= 60) return 'bg-blue-100';
    if (score >= 40) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Needs Improvement';
  };

  const successRate = (score.occurrences / score.totalChecks) * 100;
  const avgRelevance = score.averageContextRelevance * 100;

  // Prepare data for radial chart
  const radialData = [
    { name: 'Visibility', value: score.visibilityScore, fill: '#3b82f6' },
  ];

  // Prepare data for metrics
  const metricsData = [
    { 
      label: 'Success Rate', 
      value: `${successRate.toFixed(1)}%`, 
      description: 'Keywords found',
      icon: CheckCircle,
      color: 'blue'
    },
    { 
      label: 'Avg Position', 
      value: score.averagePosition ? `#${Math.round(score.averagePosition)}` : 'N/A', 
      description: score.averagePosition ? 'Lower is better' : 'No data',
      icon: TrendingUp,
      color: 'purple'
    },
    { 
      label: 'Relevance', 
      value: `${avgRelevance.toFixed(1)}%`, 
      description: 'Content quality',
      icon: TrendingUp,
      color: 'green'
    },
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Visibility Analysis Results</h1>
        <p className="text-gray-600">Comprehensive insights about your brand's AI visibility</p>
      </div>

      {/* Main Score Card */}
      <div className="bg-white rounded-2xl shadow-xl p-8 border-2 border-gray-100">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          {/* Score Display */}
          <div className="text-center">
            <div className={`inline-flex items-center justify-center w-32 h-32 rounded-full ${getScoreBgColor(score.visibilityScore)} mb-4`}>
              <div className="text-center">
                <div className={`text-5xl font-bold ${getScoreColor(score.visibilityScore)}`}>
                  {score.visibilityScore.toFixed(0)}
                </div>
                <div className="text-xs text-gray-600 mt-1">out of 100</div>
              </div>
            </div>
            <h3 className={`text-2xl font-semibold ${getScoreColor(score.visibilityScore)} mb-2`}>
              {getScoreLabel(score.visibilityScore)}
            </h3>
            <p className="text-gray-600 text-sm">
              Based on comprehensive AI visibility analysis
            </p>
          </div>

          {/* Radial Chart */}
          <div>
            <ResponsiveContainer width="100%" height={300}>
              <RadialBarChart
                cx="50%"
                cy="50%"
                innerRadius="60%"
                outerRadius="90%"
                data={radialData}
                startAngle={90}
                endAngle={-270}
              >
                <RadialBar
                  dataKey="value"
                  cornerRadius={10}
                  fill="#3b82f6"
                />
                <Tooltip 
                  formatter={(value) => [`${value.toFixed(1)}/100`, 'Visibility Score']}
                />
              </RadialBarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {metricsData.map((metric, index) => {
          const Icon = metric.icon;
          const colorClasses = {
            blue: 'bg-blue-100 text-blue-600',
            purple: 'bg-purple-100 text-purple-600',
            green: 'bg-green-100 text-green-600',
          };

          return (
            <div key={index} className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
              <div className={`w-12 h-12 ${colorClasses[metric.color as keyof typeof colorClasses]} rounded-lg flex items-center justify-center mb-4`}>
                <Icon className="w-6 h-6" />
              </div>
              <div className="text-3xl font-bold text-gray-900 mb-1">{metric.value}</div>
              <div className="text-sm font-semibold text-gray-700 mb-1">{metric.label}</div>
              <div className="text-xs text-gray-500">{metric.description}</div>
            </div>
          );
        })}
      </div>

      {/* Breakdown Chart */}
      <div className="bg-white rounded-2xl shadow-xl p-8">
        <h3 className="text-xl font-bold text-gray-900 mb-6">Performance Breakdown</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Success vs Failure */}
          <div>
            <h4 className="text-sm font-semibold text-gray-700 mb-4">Search Results</h4>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <CheckCircle className="w-5 h-5 text-green-600" />
                  <span className="text-gray-700">Keywords Found</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-32 bg-gray-200 rounded-full h-3">
                    <div 
                      className="bg-green-600 h-3 rounded-full" 
                      style={{ width: `${successRate}%` }}
                    ></div>
                  </div>
                  <span className="text-sm font-semibold text-gray-900 w-12 text-right">
                    {successRate.toFixed(1)}%
                  </span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <XCircle className="w-5 h-5 text-red-600" />
                  <span className="text-gray-700">Not Found</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-32 bg-gray-200 rounded-full h-3">
                    <div 
                      className="bg-red-600 h-3 rounded-full" 
                      style={{ width: `${100 - successRate}%` }}
                    ></div>
                  </div>
                  <span className="text-sm font-semibold text-gray-900 w-12 text-right">
                    {(100 - successRate).toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Summary */}
          <div>
            <h4 className="text-sm font-semibold text-gray-700 mb-4">Summary</h4>
            <div className="space-y-3">
              <div className="flex justify-between items-center py-2 border-b border-gray-100">
                <span className="text-gray-600">Brand Mention Rate</span>
                <span className="font-semibold text-gray-900">{successRate.toFixed(1)}%</span>
              </div>
              {score.averagePosition && (
                <div className="flex justify-between items-center py-2 border-b border-gray-100">
                  <span className="text-gray-600">Average Position</span>
                  <span className="font-semibold text-gray-900">#{Math.round(score.averagePosition)}</span>
                </div>
              )}
              <div className="flex justify-between items-center py-2">
                <span className="text-gray-600">Content Relevance</span>
                <span className="font-semibold text-gray-900">{avgRelevance.toFixed(1)}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-6 border border-blue-100">
        <div className="flex items-start space-x-3">
          <AlertCircle className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
          <div>
            <h4 className="font-semibold text-gray-900 mb-2">Recommendations</h4>
            <ul className="space-y-2 text-sm text-gray-700">
              {score.visibilityScore < 60 && (
                <li>• Improve keyword optimization in your website content</li>
              )}
              {score.averagePosition && score.averagePosition > 50 && (
                <li>• Focus on improving search ranking positions</li>
              )}
              {successRate < 50 && (
                <li>• Increase keyword density in your website content</li>
              )}
              {score.visibilityScore >= 60 && (
                <li>• Your visibility is good! Continue optimizing for better results</li>
              )}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
