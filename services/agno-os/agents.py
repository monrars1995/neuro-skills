from __future__ import annotations

import os
from uuid import uuid4

from dotenv import load_dotenv

load_dotenv()

from agno.agent import Agent

from schemas import (
    A2UIBlock,
    A2UICheckItem,
    A2UIStatItem,
    A2UITableRow,
    AgentDescriptor,
    AgentEvent,
    AgentRunOutput,
)


def build_agents() -> dict[str, Agent | None]:
    model = os.getenv("AGNO_MODEL", "google:gemini-2.5-pro")

    return {
        "traffic-strategist": build_agent(
            name="Traffic Strategist",
            model=model,
            description="Planeja estratégia de mídia e funil.",
            instructions=[
                "Receba contexto de Meta Ads e devolva plano estratégico claro.",
                "Priorize funil, estrutura de campanha, públicos e hipóteses de teste.",
                "Se o briefing estiver incompleto, diga o que falta antes de escalar.",
            ],
        ),
        "creative-analyst": build_agent(
            name="Creative Analyst",
            model=model,
            description="Analisa criativos e recomenda melhorias de performance.",
            instructions=[
                "Avalie hook, clareza visual, CTA, contraste e legibilidade.",
                "Sugira variações práticas para Meta Ads.",
            ],
        ),
        "campaign-architect": build_agent(
            name="Campaign Architect",
            model=model,
            description="Define arquitetura de campanha e budget.",
            instructions=[
                "Estruture campanhas, ad sets, objetivos e budget.",
                "Considere broad, remarketing, criativos e lógica de escala.",
            ],
        ),
        "automation-operator": build_agent(
            name="Automation Operator",
            model=model,
            description="Desenha automações e rotinas operacionais.",
            instructions=[
                "Crie automações de monitoramento e proteção de conta.",
                "Sugira regras e cron jobs claros e operacionais.",
            ],
        ),
    }


def build_agent(
    name: str,
    model: str,
    description: str,
    instructions: list[str],
) -> Agent | None:
    try:
        return Agent(
            name=name,
            model=model,
            description=description,
            instructions=instructions,
            markdown=True,
        )
    except Exception:
        return None


AGENT_DEFINITIONS = [
    AgentDescriptor(
        id="traffic-strategist",
        name="Traffic Strategist",
        role="Research + strategy",
        description="Transforma briefing em direção de campanha, estrutura de testes e prioridades de mídia.",
        icon="TS",
        starterPrompts=[
            "Monte uma estratégia para captar leads qualificados em concessionárias.",
            "Estruture uma campanha full-funnel para lançamento imobiliário.",
        ],
    ),
    AgentDescriptor(
        id="creative-analyst",
        name="Creative Analyst",
        role="Creative review",
        description="Lê criativos, hooks, leitura visual e sugere melhorias de performance.",
        icon="CA",
        starterPrompts=[
            "Analise este criativo para Meta Ads e me diga os pontos fortes.",
            "Quais ganchos visuais eu devo testar em variações desse anúncio?",
        ],
    ),
    AgentDescriptor(
        id="campaign-architect",
        name="Campaign Architect",
        role="Campaign design",
        description="Desenha campanha, conjuntos, budget e lógica de segmentação por vertical.",
        icon="CP",
        starterPrompts=[
            "Crie uma arquitetura de campanha para e-commerce com catálogo e remarketing.",
            "Defina orçamento e objetivos para uma operação de saúde com foco em agendamento.",
        ],
    ),
    AgentDescriptor(
        id="automation-operator",
        name="Automation Operator",
        role="Automation rules",
        description="Propõe rotinas, alertas, cron jobs e playbooks operacionais para escalar a conta.",
        icon="AO",
        starterPrompts=[
            "Quais automações devo ligar para controlar CPA alto?",
            "Desenhe um playbook de alertas diários para uma conta com 100k/mês.",
        ],
    ),
]


def build_run_output(
    agent_id: str, prompt: str, vertical: str, response_text: str
) -> AgentRunOutput:
    focus = prompt.split(".")[0][:80] if prompt else "performance"
    return AgentRunOutput(
        summary=f"{agent_id} gerou uma recomendação para a vertical {vertical}.",
        response_text=response_text,
        events=[
            AgentEvent(
                id=str(uuid4()),
                type="run_started",
                label=f"Run iniciado com {agent_id}",
                timestamp=_now(),
            ),
            AgentEvent(
                id=str(uuid4()),
                type="state_snapshot",
                label=f"Vertical ativa: {vertical}",
                timestamp=_now(),
            ),
            AgentEvent(
                id=str(uuid4()),
                type="text_delta",
                label=f"Foco: {focus}",
                timestamp=_now(),
            ),
            AgentEvent(
                id=str(uuid4()),
                type="a2ui",
                label="Widgets declarativos gerados",
                timestamp=_now(),
            ),
            AgentEvent(
                id=str(uuid4()),
                type="run_finished",
                label="Run concluído",
                timestamp=_now(),
            ),
        ],
        widgets=[
            A2UIBlock(
                id=str(uuid4()),
                type="hero",
                title=f"{agent_id} · plano inicial",
                description=f"Direção sugerida para {vertical} com foco em {focus}.",
                accent=vertical,
            ),
            A2UIBlock(
                id=str(uuid4()),
                type="metric_grid",
                title="Prioridades",
                stats=[
                    A2UIStatItem(label="Hook", value="alto contraste", tone="success"),
                    A2UIStatItem(label="Canal", value="Meta Ads"),
                    A2UIStatItem(label="Teste", value="2 variações", tone="warning"),
                    A2UIStatItem(label="Risco", value="CPA monitorado", tone="danger"),
                ],
            ),
            A2UIBlock(
                id=str(uuid4()),
                type="checklist",
                title="Checklist",
                items=[
                    A2UICheckItem(label="Validar objetivo e budget", status="done"),
                    A2UICheckItem(
                        label="Preparar 2 criativos por ângulo", status="active"
                    ),
                    A2UICheckItem(
                        label="Ligar automações de proteção", status="pending"
                    ),
                ],
            ),
            A2UIBlock(
                id=str(uuid4()),
                type="table",
                title="Estrutura recomendada",
                rows=[
                    A2UITableRow(label="Campanha", value="Conversões", meta=vertical),
                    A2UITableRow(
                        label="Público", value="Broad + remarketing", meta=focus
                    ),
                    A2UITableRow(
                        label="Budget",
                        value="20% do semanal para o teste",
                        meta="Fase inicial",
                    ),
                ],
            ),
            A2UIBlock(
                id=str(uuid4()),
                type="insight",
                title="Insight",
                description="Valide mensagem e criativo antes de escalar. Se o briefing estiver incompleto, trate a primeira rodada como diagnóstico de mercado.",
            ),
        ],
        state={"vertical": vertical, "focus": focus},
    )


def _now() -> str:
    from datetime import datetime

    return datetime.utcnow().isoformat() + "Z"
