import axios from 'axios';
import type { AxiosResponse } from 'axios';
import type { 
  Target, 
  InitTargetRequest, 
  UpdateKeywordsRequest, 
  UpdatePromptsRequest, 
  AnalyzeResponse,
  ApiError 
} from '../types/api';

// Get API URL from environment variable
// In production, this MUST be set in Vercel environment variables
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Log API URL in development for debugging
if (import.meta.env.DEV) {
  console.log('🔗 API Base URL:', API_BASE_URL);
}

// Warn if using localhost in production (means VITE_API_URL not set)
if (import.meta.env.PROD && API_BASE_URL.includes('localhost')) {
  console.error('⚠️ WARNING: VITE_API_URL is not set in production! Using localhost fallback.');
  console.error('Please set VITE_API_URL environment variable in Vercel settings.');
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds timeout
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const targetsApi = {
  // Initialize a new target
  initTarget: async (data: InitTargetRequest): Promise<Target> => {
    const response: AxiosResponse<{ target: Target }> = await api.post('/api/targets/init', data);
    return response.data.target;
  },

  // Get target by ID
  getTarget: async (id: string): Promise<Target> => {
    const response: AxiosResponse<Target> = await api.get(`/api/targets/${id}`);
    return response.data;
  },

  // Update keywords
  updateKeywords: async (id: string, data: UpdateKeywordsRequest): Promise<Target> => {
    const response: AxiosResponse<Target> = await api.put(`/api/targets/${id}/keywords`, data);
    return response.data;
  },

  // Update prompts
  updatePrompts: async (id: string, data: UpdatePromptsRequest): Promise<Target> => {
    const response: AxiosResponse<Target> = await api.put(`/api/targets/${id}/prompts`, data);
    return response.data;
  },

  // Analyze target visibility
  analyzeTarget: async (id: string): Promise<AnalyzeResponse> => {
    const response: AxiosResponse<AnalyzeResponse> = await api.post(`/api/targets/${id}/analyze`);
    return response.data;
  },
};

export const healthApi = {
  // Check API health
  checkHealth: async (): Promise<{ status: string }> => {
    const response: AxiosResponse<{ status: string }> = await api.get('/health');
    return response.data;
  },
};

export default api;

