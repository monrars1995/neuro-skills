import type {
  AgentDefinition,
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

export const DEFAULT_AGENTS: AgentDefinition[] = [
  {
    id: "traffic-strategist",
    name: "Traffic Strategist",
    role: "Research + strategy",
    description: "Transforma briefing em direção de campanha, estrutura de testes e prioridades de mídia.",
    icon: "TS",
    starterPrompts: [
      "Monte uma estratégia para captar leads qualificados em concessionárias.",
      "Estruture uma campanha full-funnel para lançamento imobiliário.",
    ],
  },
  {
    id: "creative-analyst",
    name: "Creative Analyst",
    role: "Creative review",
    description: "Lê criativos, hooks, leitura visual e sugere melhorias de performance.",
    icon: "CA",
    starterPrompts: [
      "Analise este criativo para Meta Ads e me diga os pontos fortes.",
      "Quais ganchos visuais eu devo testar em variações desse anúncio?",
    ],
  },
  {
    id: "campaign-architect",
    name: "Campaign Architect",
    role: "Campaign design",
    description: "Desenha campanha, conjuntos, budget e lógica de segmentação por vertical.",
    icon: "CP",
    starterPrompts: [
      "Crie uma arquitetura de campanha para e-commerce com catálogo e remarketing.",
      "Defina orçamento e objetivos para uma operação de saúde com foco em agendamento.",
    ],
  },
  {
    id: "automation-operator",
    name: "Automation Operator",
    role: "Automation rules",
    description: "Propõe rotinas, alertas, cron jobs e playbooks operacionais para escalar a conta.",
    icon: "AO",
    starterPrompts: [
      "Quais automações devo ligar para controlar CPA alto?",
      "Desenhe um playbook de alertas diários para uma conta com 100k/mês.",
    ],
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
