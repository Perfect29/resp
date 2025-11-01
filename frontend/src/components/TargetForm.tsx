import React, { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { targetsApi } from '../lib/api';
import type { InitTargetRequest } from '../types/api';
import LoadingSpinner from './LoadingSpinner';
import { CheckCircle, AlertCircle } from 'lucide-react';

interface TargetFormProps {
  onSuccess?: (targetId: string) => void;
}

export default function TargetForm({ onSuccess }: TargetFormProps) {
  const [formData, setFormData] = useState<InitTargetRequest>({
    businessName: '',
    websiteUrl: '',
  });
  const [errors, setErrors] = useState<Partial<InitTargetRequest>>({});

  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: targetsApi.initTarget,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['targets'] });
      onSuccess?.(data.id);
      setFormData({ businessName: '', websiteUrl: '' });
      setErrors({});
    },
    onError: (error: any) => {
      console.error('Error creating target:', error);
      setErrors({
        businessName: error.response?.data?.detail || 'Failed to create target',
      });
    },
  });

  const validateForm = (): boolean => {
    const newErrors: Partial<InitTargetRequest> = {};

    if (!formData.businessName.trim()) {
      newErrors.businessName = 'Business name is required';
    } else if (formData.businessName.length < 2) {
      newErrors.businessName = 'Business name must be at least 2 characters';
    } else if (formData.businessName.length > 80) {
      newErrors.businessName = 'Business name must be less than 80 characters';
    }

    if (!formData.websiteUrl.trim()) {
      newErrors.websiteUrl = 'Website URL is required';
    } else if (!isValidUrl(formData.websiteUrl)) {
      newErrors.websiteUrl = 'Please enter a valid URL (http:// or https://)';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const isValidUrl = (url: string): boolean => {
    try {
      new URL(url);
      return url.startsWith('http://') || url.startsWith('https://');
    } catch {
      return false;
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      mutation.mutate(formData);
    }
  };

  const handleInputChange = (field: keyof InitTargetRequest, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  return (
    <div className="card">
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-gray-900">Add New Target</h2>
        <p className="mt-1 text-sm text-gray-600">
          Enter your business details to start tracking visibility
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="businessName" className="block text-sm font-medium text-gray-700">
            Business Name
          </label>
          <div className="mt-1">
            <input
              type="text"
              id="businessName"
              value={formData.businessName}
              onChange={(e) => handleInputChange('businessName', e.target.value)}
              className={`input-field ${
                errors.businessName ? 'border-red-300 focus:border-red-500 focus:ring-red-500' : ''
              }`}
              placeholder="Enter your business name"
              disabled={mutation.isPending}
            />
            {errors.businessName && (
              <p className="mt-1 text-sm text-red-600 flex items-center">
                <AlertCircle className="w-4 h-4 mr-1" />
                {errors.businessName}
              </p>
            )}
          </div>
        </div>

        <div>
          <label htmlFor="websiteUrl" className="block text-sm font-medium text-gray-700">
            Website URL
          </label>
          <div className="mt-1">
            <input
              type="url"
              id="websiteUrl"
              value={formData.websiteUrl}
              onChange={(e) => handleInputChange('websiteUrl', e.target.value)}
              className={`input-field ${
                errors.websiteUrl ? 'border-red-300 focus:border-red-500 focus:ring-red-500' : ''
              }`}
              placeholder="https://example.com"
              disabled={mutation.isPending}
            />
            {errors.websiteUrl && (
              <p className="mt-1 text-sm text-red-600 flex items-center">
                <AlertCircle className="w-4 h-4 mr-1" />
                {errors.websiteUrl}
              </p>
            )}
          </div>
        </div>

        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-500">
            {mutation.isSuccess && (
              <div className="flex items-center text-green-600">
                <CheckCircle className="w-4 h-4 mr-1" />
                Target created successfully!
              </div>
            )}
          </div>
          
          <button
            type="submit"
            disabled={mutation.isPending}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
          >
            {mutation.isPending ? (
              <>
                <LoadingSpinner size="sm" className="mr-2" />
                Creating...
              </>
            ) : (
              'Create Target'
            )}
          </button>
        </div>
      </form>
    </div>
  );
}



