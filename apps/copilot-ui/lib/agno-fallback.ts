import type {
  A2UIBlock,
  AgentDefinition,
  AgentEvent,
  AgentRunResult,
  VerticalKey,
} from "@/types/app";

export interface AgentRunInput {
  agentId: string;
  prompt: string;
  vertical: VerticalKey;
  briefing?: string;
}

export function buildFallbackAgentRun(
  agent: AgentDefinition | undefined,
  input: AgentRunInput,
): AgentRunResult {
  const runId = crypto.randomUUID();
  const widgets = buildWidgets(agent, input);
  const summary = `${agent?.name || "Agent"} gerou uma resposta estruturada para a vertical ${input.vertical}.`;
  const responseText = [
    `Resumo estratégico para ${input.vertical}.`,
    `Foco principal: ${extractFocus(input.prompt)}.`,
    "Priorize estrutura clara de campanha, criativo forte e automações de proteção.",
  ].join(" ");

  const events: AgentEvent[] = [
    event("run_started", `Run iniciado com ${agent?.name || "Agent"}`),
    event("state_snapshot", `Vertical ativa: ${input.vertical}`),
    event("text_delta", `Prompt processado: ${input.prompt.slice(0, 120)}`),
    event("a2ui", `Widgets A2UI gerados: ${widgets.length}`),
    event("run_finished", "Execução finalizada com sucesso"),
  ];

  return {
    runId,
    agentId: input.agentId,
    agentName: agent?.name || input.agentId,
    summary,
    responseText,
    events,
    widgets,
    state: {
      vertical: input.vertical,
      focus: extractFocus(input.prompt),
      hasBriefing: Boolean(input.briefing?.trim()),
    },
  };
}

function buildWidgets(agent: AgentDefinition | undefined, input: AgentRunInput): A2UIBlock[] {
  const focus = extractFocus(input.prompt);
  return [
    {
      id: crypto.randomUUID(),
      type: "hero",
      title: agent?.name || "Agent",
      description: `Plano inicial para ${input.vertical} com foco em ${focus}.`,
      accent: input.vertical,
    },
    {
      id: crypto.randomUUID(),
      type: "metric_grid",
      title: "Prioridades da rodada",
      stats: [
        { label: "Hook", value: "alto contraste", tone: "success" },
        { label: "Canal", value: "Meta Ads", tone: "neutral" },
        { label: "Teste", value: "2 variações", tone: "warning" },
        { label: "Risco", value: "CPA monitorado", tone: "danger" },
      ],
    },
    {
      id: crypto.randomUUID(),
      type: "checklist",
      title: "Checklist operacional",
      items: [
        { label: "Validar objetivo e pixel", status: "done" },
        { label: "Preparar 2 criativos por ângulo", status: "active" },
        { label: "Criar automação de CPA e ROAS", status: "pending" },
      ],
    },
    {
      id: crypto.randomUUID(),
      type: "table",
      title: "Estrutura recomendada",
      rows: [
        { label: "Campanha", value: "Conversões", meta: "ABO inicial" },
        { label: "Público", value: "Broad + remarketing", meta: input.vertical },
        { label: "Orçamento", value: "Começar com 20% do budget semanal", meta: focus },
      ],
    },
    {
      id: crypto.randomUUID(),
      type: "insight",
      title: "Insight do agente",
      description:
        "Se o briefing estiver incompleto, concentre a primeira rodada em validar mensagem, criativo e janela de resposta antes de escalar orçamento.",
    },
  ];
}

function extractFocus(prompt: string) {
  const clean = prompt.trim();
  if (!clean) return "performance";
  return clean.split(/[.!?\n]/)[0].slice(0, 80);
}

function event(type: string, label: string): AgentEvent {
  return {
    id: crypto.randomUUID(),
    type,
    label,
    timestamp: new Date().toISOString(),
  };
}
