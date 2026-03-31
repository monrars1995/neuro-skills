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
  | "agents"
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

export interface AgentDefinition {
  id: string;
  name: string;
  role: string;
  description: string;
  icon: string;
  starterPrompts: string[];
}

export interface AgentEvent {
  id: string;
  type: string;
  label: string;
  detail?: string;
  timestamp: string;
}

export interface A2UIStatItem {
  label: string;
  value: string;
  tone?: "neutral" | "success" | "warning" | "danger";
}

export interface A2UICheckItem {
  label: string;
  status?: "done" | "active" | "pending";
}

export interface A2UITableRow {
  label: string;
  value: string;
  meta?: string;
}

export interface A2UIBlock {
  id: string;
  type: "hero" | "metric_grid" | "checklist" | "table" | "insight";
  title: string;
  description?: string;
  stats?: A2UIStatItem[];
  items?: A2UICheckItem[];
  rows?: A2UITableRow[];
  accent?: string;
}

export interface AgentRunResult {
  runId: string;
  agentId: string;
  agentName: string;
  summary: string;
  responseText: string;
  events: AgentEvent[];
  widgets: A2UIBlock[];
  state?: Record<string, unknown>;
}
