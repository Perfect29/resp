// API Type Definitions

export interface Keyword {
  value: string;
  generated: boolean;
}

export interface Prompt {
  value: string;
  generated: boolean;
}

export interface Target {
  id: string;
  businessName: string;
  websiteUrl: string;
  keywords: Keyword[];
  prompts: Prompt[];
  createdAt: string;
  updatedAt: string;
}

export interface InitTargetRequest {
  businessName: string;
  websiteUrl: string;
}

export interface UpdateKeywordsRequest {
  keywords: string[];
}

export interface UpdatePromptsRequest {
  prompts: string[];
}

export interface VisibilityCheck {
  prompt: string;
  keyword: string;
  occurred: boolean;
  position?: number;
  contextRelevance: number;
}

export interface VisibilityScore {
  totalChecks: number;
  occurrences: number;
  averagePosition?: number;
  averageContextRelevance: number;
  visibilityScore: number;
  checks: VisibilityCheck[];
}

export interface AnalyzeResponse {
  targetId: string;
  score: VisibilityScore;
  analyzedAt: string;
}

export interface ApiError {
  error: string;
  detail?: string;
}