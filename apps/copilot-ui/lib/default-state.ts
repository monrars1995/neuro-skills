import type {
  AnalyticsSnapshot,
  AppSection,
  AutomationJob,
  CampaignDraft,
  ClientRecord,
  MetaAccountRecord,
  VerticalKey,
} from "@/types/app";

export const DEFAULT_VERTICAL: VerticalKey = "concessionarias";
export const DEFAULT_SECTION: AppSection = "overview";

export const DEFAULT_CLIENTS: ClientRecord[] = [
  {
    id: "goldneuron-demo",
    name: "GoldNeuron Demo",
    industry: "Marketing",
    vertical: "concessionarias",
    monthlyBudget: 50000,
    locations: ["Brasil", "São Paulo"],
  },
];

export const DEFAULT_ACCOUNTS: MetaAccountRecord[] = [
  {
    id: "demo-account",
    name: "Conta Principal Demo",
    adAccountId: "act_123456789",
    pageId: "page_demo_001",
    pixelId: "pixel_demo_001",
  },
];

export const DEFAULT_CAMPAIGNS: CampaignDraft[] = [
  {
    id: "campaign-demo-1",
    name: "Black Friday - Financiamento SUV",
    objective: "CONVERSIONS",
    budget: 7500,
    status: "ready",
    copyAngle: "urgency + financing",
  },
];

export const DEFAULT_AUTOMATIONS: AutomationJob[] = [
  {
    id: "job-demo-1",
    name: "Pausar CPA Alto",
    type: "rule",
    schedule: "every 6h",
    enabled: true,
  },
  {
    id: "job-demo-2",
    name: "Relatório Diário de ROAS",
    type: "report",
    schedule: "daily 08:00",
    enabled: true,
  },
];

export const DEFAULT_ANALYTICS: AnalyticsSnapshot = {
  spend: 18432.9,
  impressions: 412300,
  clicks: 12104,
  ctr: 2.94,
  cpc: 1.52,
  roas: 4.18,
};

export const VERTICAL_LABELS: Record<VerticalKey, { title: string; description: string }> = {
  concessionarias: {
    title: "Concessionárias",
    description: "Veículos, conversão offline e ciclo longo.",
  },
  imobiliarias: {
    title: "Imobiliárias",
    description: "Imóveis, tours virtuais e ticket alto.",
  },
  ecommerce: {
    title: "E-commerce",
    description: "Catálogo, remarketing e DPA.",
  },
  educacao: {
    title: "Educação",
    description: "Captação de alunos, sazonalidade e LTV.",
  },
  saude: {
    title: "Saúde",
    description: "Compliance, agendamento e privacidade.",
  },
};
