export type VerticalKey =
  | "concessionarias"
  | "imobiliarias"
  | "ecommerce"
  | "educacao"
  | "saude";

export type AppSection =
  | "overview"
  | "briefing"
  | "creatives"
  | "campaigns"
  | "analytics"
  | "automations"
  | "settings";

export interface ClientRecord {
  id: string;
  name: string;
  industry: string;
  vertical: VerticalKey;
  monthlyBudget: number;
  locations: string[];
}

export interface MetaAccountRecord {
  id: string;
  name: string;
  adAccountId: string;
  pageId?: string;
  pixelId?: string;
}

export interface BriefingAnalysis {
  client?: string;
  product?: string;
  objective?: string;
  budget?: number;
  targetCpa?: number;
  targetRoas?: number;
  missingInfo: string[];
}

export interface CreativeAnalysis {
  summary: string;
  hooks: string[];
  visualNotes: string[];
  improvementIdeas: string[];
  score: number;
}

export interface UploadedAsset {
  id: string;
  name: string;
  kind: "image" | "video";
  status: "uploaded" | "analyzing" | "analyzed";
  mimeType?: string;
  analysis?: CreativeAnalysis;
}

export interface CampaignDraft {
  id: string;
  name: string;
  objective: string;
  budget: number;
  status: "draft" | "ready" | "paused";
  copyAngle: string;
}

export interface AutomationJob {
  id: string;
  name: string;
  type: string;
  schedule: string;
  enabled: boolean;
}

export interface AnalyticsSnapshot {
  spend: number;
  impressions: number;
  clicks: number;
  ctr: number;
  cpc: number;
  roas: number;
}
