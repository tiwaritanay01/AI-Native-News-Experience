export interface NewsStory {
  id: string;
  headline: string;
  summary: string;
  bulletPoints: string[];
  impact: 'bullish' | 'bearish' | 'neutral';
  affectedCompanies: AffectedCompany[];
  bullishView: string;
  bearishView: string;
  relevanceScore: number;
  timestamp: Date;
}

export interface AffectedCompany {
  name: string;
  ticker: string;
  change: number; // percentage change
  sector: string;
}

export interface DashboardState {
  topStory: NewsStory | null;
  relatedNews: NewsStory[];
  explainLevel: 'beginner' | 'intermediate' | 'expert';
  sidebarOpen: boolean;
  loading: boolean;
}

export type ExplainLevel = 'beginner' | 'intermediate' | 'expert';
