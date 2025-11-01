import React, { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import type { Target, UpdateKeywordsRequest, UpdatePromptsRequest } from '../types/api';
import { targetsApi } from '../lib/api.js';
import { 
  Edit3, 
  Trash2, 
  BarChart3, 
  Globe, 
  Tag, 
  MessageSquare,
  Check,
  X,
  Loader
} from 'lucide-react';
import LoadingSpinner from './LoadingSpinner';

interface TargetCardProps {
  target: Target;
  onAnalyze?: (targetId: string) => void;
  onDelete?: (targetId: string) => void;
}

export default function TargetCard({ target, onAnalyze, onDelete }: TargetCardProps) {
  const [isEditingKeywords, setIsEditingKeywords] = useState(false);
  const [isEditingPrompts, setIsEditingPrompts] = useState(false);
  const [keywords, setKeywords] = useState(target.keywords.map(k => k.value));
  const [prompts, setPrompts] = useState(target.prompts.map(p => p.value));

  const queryClient = useQueryClient();

  const updateKeywordsMutation = useMutation({
    mutationFn: (data: UpdateKeywordsRequest) => targetsApi.updateKeywords(target.id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['targets'] });
      setIsEditingKeywords(false);
    },
  });

  const updatePromptsMutation = useMutation({
    mutationFn: (data: UpdatePromptsRequest) => targetsApi.updatePrompts(target.id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['targets'] });
      setIsEditingPrompts(false);
    },
  });

  const handleKeywordsSave = () => {
    updateKeywordsMutation.mutate({ keywords });
  };

  const handlePromptsSave = () => {
    updatePromptsMutation.mutate({ prompts });
  };

  const handleKeywordsCancel = () => {
    setKeywords(target.keywords.map(k => k.value));
    setIsEditingKeywords(false);
  };

  const handlePromptsCancel = () => {
    setPrompts(target.prompts.map(p => p.value));
    setIsEditingPrompts(false);
  };

  const addKeyword = () => {
    setKeywords([...keywords, '']);
  };

  const addPrompt = () => {
    setPrompts([...prompts, '']);
  };

  const removeKeyword = (index: number) => {
    setKeywords(keywords.filter((_, i) => i !== index));
  };

  const removePrompt = (index: number) => {
    setPrompts(prompts.filter((_, i) => i !== index));
  };

  const updateKeyword = (index: number, value: string) => {
    const newKeywords = [...keywords];
    newKeywords[index] = value;
    setKeywords(newKeywords);
  };

  const updatePrompt = (index: number, value: string) => {
    const newPrompts = [...prompts];
    newPrompts[index] = value;
    setPrompts(newPrompts);
  };

  return (
    <div className="card">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{target.businessName}</h3>
          <div className="flex items-center mt-1 text-sm text-gray-500">
            <Globe className="w-4 h-4 mr-1" />
            <a 
              href={target.websiteUrl} 
              target="_blank" 
              rel="noopener noreferrer"
              className="hover:text-primary-600"
            >
              {target.websiteUrl}
            </a>
          </div>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => onAnalyze?.(target.id)}
            className="p-2 text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
            title="Analyze visibility"
          >
            <BarChart3 className="w-5 h-5" />
          </button>
          <button
            onClick={() => onDelete?.(target.id)}
            className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            title="Delete target"
          >
            <Trash2 className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Keywords Section */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-sm font-medium text-gray-900 flex items-center">
            <Tag className="w-4 h-4 mr-1" />
            Keywords ({keywords.length}/5)
          </h4>
          {!isEditingKeywords && (
            <button
              onClick={() => setIsEditingKeywords(true)}
              className="text-sm text-primary-600 hover:text-primary-700 flex items-center"
            >
              <Edit3 className="w-3 h-3 mr-1" />
              Edit
            </button>
          )}
        </div>

        {isEditingKeywords ? (
          <div className="space-y-2">
            {keywords.map((keyword, index) => (
              <div key={index} className="flex items-center space-x-2">
                <input
                  type="text"
                  value={keyword}
                  onChange={(e) => updateKeyword(index, e.target.value)}
                  className="input-field flex-1"
                  placeholder="Enter keyword"
                />
                <button
                  onClick={() => removeKeyword(index)}
                  className="p-1 text-red-600 hover:bg-red-50 rounded"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            ))}
            {keywords.length < 5 && (
              <button
                onClick={addKeyword}
                className="text-sm text-primary-600 hover:text-primary-700"
              >
                + Add keyword
              </button>
            )}
            <div className="flex space-x-2 pt-2">
              <button
                onClick={handleKeywordsSave}
                disabled={updateKeywordsMutation.isPending}
                className="btn-primary text-sm disabled:opacity-50 flex items-center"
              >
                {updateKeywordsMutation.isPending ? (
                  <Loader className="w-3 h-3 mr-1" />
                ) : (
                  <Check className="w-3 h-3 mr-1" />
                )}
                Save
              </button>
              <button
                onClick={handleKeywordsCancel}
                className="btn-secondary text-sm"
              >
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <div className="flex flex-wrap gap-2">
            {target.keywords.map((keyword, index) => (
              <span
                key={index}
                className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  keyword.generated
                    ? 'bg-blue-100 text-blue-800'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                {keyword.value}
                {keyword.generated && (
                  <span className="ml-1 text-blue-600">AI</span>
                )}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Prompts Section */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-sm font-medium text-gray-900 flex items-center">
            <MessageSquare className="w-4 h-4 mr-1" />
            Prompts ({prompts.length}/10)
          </h4>
          {!isEditingPrompts && (
            <button
              onClick={() => setIsEditingPrompts(true)}
              className="text-sm text-primary-600 hover:text-primary-700 flex items-center"
            >
              <Edit3 className="w-3 h-3 mr-1" />
              Edit
            </button>
          )}
        </div>

        {isEditingPrompts ? (
          <div className="space-y-2">
            {prompts.map((prompt, index) => (
              <div key={index} className="flex items-center space-x-2">
                <input
                  type="text"
                  value={prompt}
                  onChange={(e) => updatePrompt(index, e.target.value)}
                  className="input-field flex-1"
                  placeholder="Enter prompt"
                />
                <button
                  onClick={() => removePrompt(index)}
                  className="p-1 text-red-600 hover:bg-red-50 rounded"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            ))}
            {prompts.length < 10 && (
              <button
                onClick={addPrompt}
                className="text-sm text-primary-600 hover:text-primary-700"
              >
                + Add prompt
              </button>
            )}
            <div className="flex space-x-2 pt-2">
              <button
                onClick={handlePromptsSave}
                disabled={updatePromptsMutation.isPending}
                className="btn-primary text-sm disabled:opacity-50 flex items-center"
              >
                {updatePromptsMutation.isPending ? (
                  <Loader className="w-3 h-3 mr-1" />
                ) : (
                  <Check className="w-3 h-3 mr-1" />
                )}
                Save
              </button>
              <button
                onClick={handlePromptsCancel}
                className="btn-secondary text-sm"
              >
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-2">
            {target.prompts.slice(0, 3).map((prompt, index) => (
              <div
                key={index}
                className={`text-sm p-2 rounded ${
                  prompt.generated
                    ? 'bg-blue-50 text-blue-800'
                    : 'bg-gray-50 text-gray-800'
                }`}
              >
                {prompt.value}
                {prompt.generated && (
                  <span className="ml-2 text-xs text-blue-600">AI</span>
                )}
              </div>
            ))}
            {target.prompts.length > 3 && (
              <div className="text-xs text-gray-500">
                +{target.prompts.length - 3} more prompts
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}



