"""
Neuro Skills Agent - Interface Conversacional
Autor: Monrars (@monrars)
Instagram: @monrars

Agent completo que integra:
- traffic-strategist: Análise e preparação
- ad-copywriter: Geração de copy
- meta-ads-manager: Criação e gestão de campanhas
- neuro-ads-manager: CRUD, Analytics, Automação
- scheduler: Agendamento de automações
- analytics: Motor de análise
"""

import streamlit as st
from pathlib import Path
import sys
import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

# Adicionar diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import Config, NEURO_DIR
from core.memory import MemoryManager
from core.meta_api import MetaAPIClient
from upload.video_uploader import BatchUploader, VideoUploadManager
from scheduler.automation import AutomationScheduler
from analytics.engine import AnalyticsEngine

# Configuração da página
st.set_page_config(
    page_title="Neuro Skills Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS customizado
st.markdown(
    """
<style>
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
    }
    .message-user {
        background-color: #e3f2fd;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 8px 0;
        margin-left: 20%;
    }
    .message-agent {
        background-color: #f5f5f5;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 8px 0;
        margin-right: 20%;
    }
    .upload-zone {
        border: 2px dashed #ccc;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
    }
    .progress-item {
        padding: 8px;
        margin: 4px 0;
        border-radius: 4px;
    }
    .status-success { color: #28a745; }
    .status-error { color: #dc3545; }
    .status-pending { color: #ffc107; }
    .status-running { color: #17a2b8; }
</style>
""",
    unsafe_allow_html=True,
)


# Inicialização
@st.cache_resource
def init_memory():
    return MemoryManager(NEURO_DIR)


@st.cache_resource
def get_config():
    return Config()


# Sessão state
if "memory" not in st.session_state:
    st.session_state.memory = init_memory()

if "config" not in st.session_state:
    st.session_state.config = get_config()

if "api_client" not in st.session_state:
    st.session_state.api_client = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "workflow_state" not in st.session_state:
    st.session_state.workflow_state = {
        "step": "start",
        "vertical": None,
        "client_id": None,
        "campaign_name": None,
        "briefing": None,
        "creatives": [],
        "uploaded_videos": [],
        "uploaded_images": [],
        "brand_voice": None,
        "targeting": None,
        "copy_variants": [],
        "campaign_id": None,
        "adset_id": None,
        "ad_ids": [],
    }

if "uploads" not in st.session_state:
    st.session_state.uploads = {"pending": [], "completed": [], "failed": []}

if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

if "analytics" not in st.session_state:
    st.session_state.analytics = None

if "automation_jobs" not in st.session_state:
    st.session_state.automation_jobs = []

# ==================== VERTICAL AGENTS ====================

VERTICAL_AGENTS = {
    "concessionarias": {
        "name": "🚗 Concessionárias",
        "description": "Veículos, conversão offline, ciclo longo",
        "segmentation_help": "Segmentação por tipo de veículo, teste drive, financiamento",
        "features": [
            "Offline conversion (7 dias)",
            "CRM integration",
            "ROI com margens",
        ],
    },
    "imobiliarias": {
        "name": "🏠 Imobiliárias",
        "description": "Imóveis, tours virtuais, LTV alto",
        "segmentation_help": "Segmentação por tipo de imóvel, localização, faixa de valor",
        "features": ["Product Catalog", "DPA", "ROI com comissões"],
    },
    "ecommerce": {
        "name": "🛒 E-commerce",
        "description": "Lojas virtuais, DPA, ciclo curto",
        "segmentation_help": "Segmentação por categoria, retargeting de carrinho",
        "features": ["Product Catalog", "Cart recovery", "ROI com margens"],
    },
    "educacao": {
        "name": "🎓 Educação",
        "description": "Cursos, faculdades, sazonalidade",
        "segmentation_help": "Segmentação por tipo de curso, vida estudantil",
        "features": ["Campanhas sazonais", "LTV por aluno", "CRM integration"],
    },
    "saude": {
        "name": "🏥 Saúde",
        "description": "Clínicas, consultórios, LGPD compliance",
        "segmentation_help": "Segmentação por especialidade, privacy-safe",
        "features": ["LGPD/HIPAA compliance", "Patient LTV", "Privacy targeting"],
    },
}


# ==================== FUNÇÕES DO AGENT ====================


def add_message(role: str, content: str):
    """Adiciona mensagem ao histórico"""
    st.session_state.chat_history.append(
        {"role": role, "content": content, "timestamp": datetime.now().isoformat()}
    )


def get_active_client() -> Optional[Dict]:
    """Retorna cliente ativo"""
    client_id = st.session_state.memory.get_active_client()
    if client_id:
        return st.session_state.memory.get_client(client_id)
    return None


def get_active_account() -> Optional[Dict]:
    """Retorna conta ativa"""
    account_name = st.session_state.memory.list_accounts().get("active_account")
    if account_name:
        return (
            st.session_state.memory.list_accounts()
            .get("accounts", {})
            .get(account_name)
        )
    return None


def analyze_briefing(briefing_text: str) -> Dict[str, Any]:
    """Analisa briefing usando lógica do traffic-strategist"""
    # Extrair informações do briefing
    lines = briefing_text.split("\n")

    result = {
        "client": None,
        "product": None,
        "objective": None,
        "budget": None,
        "target_cpa": None,
        "target_roas": None,
        "audience": {},
        "creatives_needed": [],
        "usps": [],
        "timeline": None,
        "missing_info": [],
    }

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Extrair cliente
        if "cliente:" in line.lower() or "client:" in line.lower():
            result["client"] = line.split(":")[-1].strip()
        # Extrair produto
        elif "produto:" in line.lower() or "product:" in line.lower():
            result["product"] = line.split(":")[-1].strip()
        # Extrair objetivo
        elif "objetivo:" in line.lower() or "objective:" in line.lower():
            obj = line.split(":")[-1].strip().lower()
            if "venda" in obj or "sales" in obj or "conversão" in obj:
                result["objective"] = "CONVERSIONS"
            elif "tráfego" in obj or "traffic" in obj:
                result["objective"] = "TRAFFIC"
            elif "awareness" in obj or "reconhecimento" in obj:
                result["objective"] = "AWARENESS"
            elif "lead" in obj:
                result["objective"] = "LEAD_GENERATION"
            else:
                result["objective"] = "CONVERSIONS"
        # Extrair orçamento
        elif (
            "orçamento:" in line.lower()
            or "budget:" in line.lower()
            or "investimento:" in line.lower()
        ):
            budget_str = line.split(":")[-1].strip()
            # Parse budget (R$ 5000 -> 5000)
            budget = "".join(c for c in budget_str if c.isdigit())
            if budget:
                result["budget"] = int(budget)
        # Extrair CPA
        elif "cpa:" in line.lower() or "cpa alvo:" in line.lower():
            cpa_str = line.split(":")[-1].strip()
            cpa = "".join(c for c in cpa_str if c.isdigit() or c == ".")
            if cpa:
                result["target_cpa"] = float(cpa)
        # Extrair ROAS
        elif "roas:" in line.lower() or "roas alvo:" in line.lower():
            roas_str = line.split(":")[-1].strip()
            roas = "".join(c for c in roas_str if c.isdigit() or c == ".")
            if roas:
                result["target_roas"] = float(roas)

    return result


def generate_copy(
    briefing: Dict, brand_voice: Dict, num_variants: int = 3, vertical: str = None
) -> List[Dict]:
    """Gera variações de copy usando lógica do ad-copywriter com especialização por vertical"""
    variants = []

    # Based on objective, generate appropriate copy structure
    objective = briefing.get("objective", "CONVERSIONS")
    product = briefing.get("product", "nosso produto")
    client = briefing.get("client", "marca")

    # Vertical-specific copy templates
    vertical_templates = {
        "concessionarias": {
            "CONVERSIONS": [
                {
                    "name": "Test Drive Focado",
                    "headline": f"Agende Seu Test Drive {product}",
                    "primary_text": f"Experimente {product} na {client}. Condições especiais de financiamento. Horários flexíveis.",
                    "cta": "Agendar Test Drive",
                },
                {
                    "name": "Oferta de Troca",
                    "headline": f"Troque Seu Carro Por {product}",
                    "primary_text": f" Avaliação justa do seu usado + condições especiais na {client}. Venha conferir.",
                    "cta": "Ver Oferta",
                },
                {
                    "name": "Financiamento Zero",
                    "headline": f"{product} com Entrada Zero",
                    "primary_text": f"Aprovação rápida, parcelas que cabem no bolso. {client} - sua concessionária de confiança há anos.",
                    "cta": "Simular Financiamento",
                },
            ],
            "TRAFFIC": [
                {
                    "name": "Descoberta",
                    "headline": f"Descubra {product}",
                    "primary_text": f"A mais nova chegada na {client}. Tecnologia, conforto e segurança em um só lugar.",
                    "cta": "Conhecer",
                },
            ],
        },
        "imobiliarias": {
            "CONVERSIONS": [
                {
                    "name": "Tour Virtual",
                    "headline": f"Tour Virtual: {product}",
                    "primary_text": f"Conheça {product} sem sair de casa. {client} - imóveis selecionados com carinho.",
                    "cta": "Ver Tour",
                },
                {
                    "name": "Investimento",
                    "headline": f"Investimento Inteligente em {product}",
                    "primary_text": f"{client} apresenta {product}. Localização privilegiada, valorização garantida.",
                    "cta": "Agendar Visita",
                },
            ],
        },
        "ecommerce": {
            "CONVERSIONS": [
                {
                    "name": "Promoção Limitada",
                    "headline": f"🔥 {product} com Desconto Exclusivo",
                    "primary_text": f"Aproveite! {product} com condição especial por tempo limitado. {client} - entrega rápida.",
                    "cta": "Comprar Agora",
                },
                {
                    "name": "Social Proof",
                    "headline": f"Milhares Já Compraram {product}",
                    "primary_text": f"⭐⭐⭐⭐⭐ Avaliações de clientes reais. {client} - qualidade garantida.",
                    "cta": "Ver Produto",
                },
            ],
        },
        "educacao": {
            "CONVERSIONS": [
                {
                    "name": "Inscrição",
                    "headline": f"Vagas Limitadas: {product}",
                    "primary_text": f"Garanta sua vaga em {product}. {client} - educação de qualidade para seu futuro.",
                    "cta": "Inscrever-se",
                },
                {
                    "name": "Carreiras",
                    "headline": f"Comece Sua Jornada Profissional",
                    "primary_text": f"{product} na {client}. Professores renomados, metodologia atualizada.",
                    "cta": "Saiba Mais",
                },
            ],
        },
        "saude": {
            "CONVERSIONS": [
                {
                    "name": "Agendamento",
                    "headline": f"Agende Sua Consulta: {product}",
                    "primary_text": f"{client} - cuidado com sua saúde. Profissionais qualificados, atendimento humanizado.",
                    "cta": "Agendar",
                },
                {
                    "name": "Tratamento",
                    "headline": f"Tratamento {product}",
                    "primary_text": f"Tecnologia e cuidado na {client}. Resultados comprovados, equipe especializada.",
                    "cta": "Conheça",
                },
            ],
        },
    }

    # Use vertical-specific templates if available
    if vertical and vertical in vertical_templates:
        templates = vertical_templates[vertical].get(
            objective, vertical_templates[vertical].get("CONVERSIONS", [])
        )
    # Default templates
    elif objective == "CONVERSIONS":
        templates = [
            {
                "name": "Direct Conversion",
                "headline": f"Descubra {product} Agora",
                "primary_text": f"Encontre exatamente o que você procura. {client} oferece qualidade e confiança. Aproveite condições especiais por tempo limitado.",
                "cta": "Compre Agora",
            },
            {
                "name": "Benefit-Focused",
                "headline": f"Aproveite Todos os Benefícios",
                "primary_text": f"O que você estava procurando está aqui. {product} com a qualidade {client}. Resultados visíveis desde o primeiro uso.",
                "cta": "Saiba Mais",
            },
            {
                "name": "Urgency",
                "headline": f"Últimas Unidades Disponíveis",
                "primary_text": f"Não perca a oportunidade de conhecer {product}. Oferta especial válida enquanto durar o estoque. Qualidade garantida.",
                "cta": "Compre Agora",
            },
        ]
    elif objective == "TRAFFIC":
        templates = [
            {
                "name": "Curiosity Click",
                "headline": f"Veja o Que Está Fazendo Sucesso",
                "primary_text": f"Descubra por que milhares de pessoas já conhecem {product}. Clique e surpreenda-se.",
                "cta": "Saiba Mais",
            },
            {
                "name": "Value Proposition",
                "headline": f"A Qualidade Que Você Merece",
                "primary_text": f"{client} apresenta {product}. A combinação perfeita de qualidade e preço. Confira agora.",
                "cta": "Ver Agora",
            },
            {
                "name": "Social Proof",
                "headline": f"O Que Dizem Sobre {product}",
                "primary_text": f"Veja os resultados reais de quem já experimentou {product}. Sua vez de descobrir.",
                "cta": "Conheça",
            },
        ]
    else:  # AWARENESS or others
        templates = [
            {
                "name": "Brand Story",
                "headline": f"Conheça {client}",
                "primary_text": f"{product} - A escolha certa para quem busca qualidade. Uma história de sucesso que começa com você.",
                "cta": "Conheça",
            },
            {
                "name": "Impact",
                "headline": f"Novidade: {product}",
                "primary_text": f"{client} inova mais uma vez. Descubra o que estamos preparando para você.",
                "cta": "Descubra",
            },
            {
                "name": "Connection",
                "headline": f"Feito Para Você",
                "primary_text": f"{product} foi criado pensando em você. Qualidade {client} em cada detalhe.",
                "cta": "Ver Detalhes",
            },
        ]

    # Apply brand voice modifications
    tone = brand_voice.get("voice_profile", {}).get("tone", {})
    keywords_use = (
        brand_voice.get("voice_profile", {}).get("keywords", {}).get("use", [])
    )
    keywords_avoid = (
        brand_voice.get("voice_profile", {}).get("keywords", {}).get("avoid", [])
    )

    for i, template in enumerate(templates[:num_variants]):
        variant = {
            "id": f"copy_{i + 1}",
            "name": template["name"],
            "headline": template["headline"],
            "primary_text": template["primary_text"],
            "cta": template["cta"],
            "format": "feed",  # default
            "vertical": vertical,
            "created_at": datetime.now().isoformat(),
        }
        variants.append(variant)

    return variants


def generate_targeting(briefing: Dict, brand_voice: Dict, vertical: str = None) -> Dict:
    """Gera configurações de targeting com especialização por vertical"""
    # Base targeting
    targeting = {
        "age_min": 25,
        "age_max": 55,
        "genders": ["male", "female"],
        "locations": ["BR"],
        "interests": [],
        "behaviors": [],
        "custom_audiences": [],
        "lookalikes": [],
    }

    # Vertical-specific targeting
    vertical_targeting = {
        "concessionarias": {
            "age_min": 25,
            "age_max": 55,
            "interests": [
                {"name": "Carros", "id": "6003187587541"},
                {"name": "Automóveis", "id": "6003187587541"},
                {"name": "Financiamento de carro", "id": "6003567587846"},
            ],
            "behaviors": [{"name": "Engaged shoppers", "id": "300600668479841"}],
            "custom_audiences": ["Website visitors 30 days", "Lead form completions"],
            "offline_conversion_window": 7,  # Minimo7 dias para concessionárias
        },
        "imobiliarias": {
            "age_min": 30,
            "age_max": 65,
            "interests": [
                {"name": "Imóveis", "id": "6003209556441"},
                {"name": "Investimento imobiliário", "id": "6003210128754"},
            ],
            "custom_audiences": ["Website visitors 60 days", "Property viewers"],
        },
        "ecommerce": {
            "age_min": 18,
            "age_max": 55,
            "interests": [],  # Dynamic based on product catalog
            "behaviors": [{"name": "Engaged shoppers", "id": "300600668479841"}],
            "custom_audiences": ["Cart abandoners", "Product viewers"],
        },
        "educacao": {
            "age_min": 18,
            "age_max": 45,
            "interests": [
                {"name": "Educação", "id": "6003220556441"},
                {"name": "Cursos", "id": "6003220556841"},
            ],
            "custom_audiences": ["Website visitors", "Form submissions"],
        },
        "saude": {
            "age_min": 25,
            "age_max": 65,
            "interests": [
                {"name": "Saúde", "id": "6003237587541"},
                {"name": "Bem-estar", "id": "6003237587841"},
            ],
            "custom_audiences": ["Website visitors", "Appointment seekers"],
            "privacy_compliance": "LGPD",  # LGPD/HIPAA compliance note
        },
    }

    # Apply vertical-specific targeting if available
    if vertical and vertical in vertical_targeting:
        targeting.update(vertical_targeting[vertical])

    # Apply brand voice learnings
    learned = brand_voice.get("learned_preferences", {})
    if learned.get("best_performing_audiences"):
        # Use learned preferences
        pass

    return targeting


def create_campaign_structure(
    api_client,
    account_id: str,
    briefing: Dict,
    targeting: Dict,
    uploaded_creatives: Dict,
) -> Dict:
    """Cria estrutura de campanha via API"""
    results = {"campaign": None, "adset": None, "ads": [], "errors": []}

    try:
        # 1. Criar campanha
        campaign_name = f"{briefing.get('client', 'Cliente')} - {briefing.get('product', 'Produto')} - {datetime.now().strftime('%Y-%m-%d')}"
        campaign_result = api_client.create_campaign(
            name=campaign_name,
            objective=briefing.get("objective", "CONVERSIONS"),
            status="PAUSED",
        )

        if "id" in campaign_result:
            results["campaign"] = campaign_result

            # 2. Criar ad set
            budget = briefing.get("budget", 5000)  # Default 5000 centavos = R$50
            adset_result = api_client.create_ad_set(
                campaign_id=campaign_result["id"],
                name=f"{campaign_name} - Ad Set",
                daily_budget=budget,
                targeting=targeting,
            )

            if "id" in adset_result:
                results["adset"] = adset_result

                # 3. Criar ads para cada creative
                for video in uploaded_creatives.get("videos", []):
                    if video.get("status") == "completed" and video.get("video_id"):
                        # Criar creative
                        creative_result = api_client.create_ad_creative(
                            name=f"{campaign_name} - {video['filename']}",
                            page_id=account_id,
                            video_id=video["video_id"],
                            message="Teste",
                        )

                        if "id" in creative_result:
                            # Criar ad
                            ad_result = api_client.create_ad(
                                ad_set_id=adset_result["id"],
                                name=f"{campaign_name} - Ad",
                                creative_id=creative_result["id"],
                            )

                            if "id" in ad_result:
                                results["ads"].append(ad_result)
                            else:
                                results["errors"].append(
                                    f"Erro ao criar ad: {ad_result.get('error')}"
                                )
                        else:
                            results["errors"].append(
                                f"Erro ao criar creative: {creative_result.get('error')}"
                            )
            else:
                results["errors"].append(
                    f"Erro ao criar ad set: {adset_result.get('error')}"
                )
        else:
            results["errors"].append(
                f"Erro ao criar campanha: {campaign_result.get('error')}"
            )

    except Exception as e:
        results["errors"].append(str(e))

    return results


# ==================== SIDEBAR ====================

with st.sidebar:
    st.markdown("### 🧠 Neuro Skills Agent")
    st.markdown("---")

    # Status
    st.markdown("**Status:**")

    # Cliente ativo
    active_client = get_active_client()
    if active_client:
        st.markdown(f"👤 **{active_client.get('name', 'N/A')}**")
    else:
        st.markdown("👤 Nenhum cliente")

    # Conta ativa
    active_account = get_active_account()
    if active_account:
        st.markdown(f"📱 **{active_account.get('name', 'N/A')}**")
    else:
        st.markdown("📱 Nenhuma conta")

    st.markdown("---")

    # Navegação rápida
    st.markdown("**Ações:**")
    if st.button("⚙️ Configurações", use_container_width=True):
        st.session_state.workflow_state["step"] = "config"
    if st.button("📤 Novo Upload", use_container_width=True):
        st.session_state.workflow_state["step"] = "upload"
    if st.button("📝 Novo Briefing", use_container_width=True):
        st.session_state.workflow_state["step"] = "briefing"

    st.markdown("---")
    st.markdown("**Automação:**")
    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.workflow_state["step"] = "dashboard"
    if st.button("⚡ Automações", use_container_width=True):
        st.session_state.workflow_state["step"] = "automations"
    if st.button("📈 Analytics", use_container_width=True):
        st.session_state.workflow_state["step"] = "analytics"

    st.markdown("---")
    st.markdown("📱 [@monrars](https://instagram.com/monrars)")
    st.markdown("MIT License ©2026")

# ==================== MAIN CHAT INTERFACE ====================

st.markdown(
    '<h1 class="main-header">🧠 Neuro Skills Agent</h1>', unsafe_allow_html=True
)
st.markdown(
    '<p class="sub-header">Seu assistente inteligente para Meta Ads</p>',
    unsafe_allow_html=True,
)

# Seletor de Vertical no topo
if st.session_state.workflow_state.get("vertical"):
    vertical_key = st.session_state.workflow_state["vertical"]
    vertical_info = VERTICAL_AGENTS.get(vertical_key, {})
    st.info(
        f"📊 **Vertical:** {vertical_info.get('name', vertical_key)} - {vertical_info.get('description', '')}"
    )
    col1, col2, col3 = st.columns([2, 2, 1])
    with col3:
        if st.button("🔄 Trocar", key="change_vertical"):
            st.session_state.workflow_state["vertical"] = None
            st.rerun()

# Container principal
chat_container = st.container()

# ==================== PROCESSAMENTO POR ETAPAS ====================

current_step = st.session_state.workflow_state["step"]

# ETAPA: START
if current_step == "start":
    with chat_container:
        # Verificar se vertical está selecionada
        if not st.session_state.workflow_state.get("vertical"):
            st.markdown("""
            ### 👋 Bem-vindo ao Neuro Skills Agent!
            
            Escolha sua vertical para começar:
            """)

            # Mostrar opções de vertical
            cols = st.columns(5)
            for i, (key, vertical) in enumerate(VERTICAL_AGENTS.items()):
                with cols[i]:
                    if st.button(
                        vertical["name"],
                        key=f"vertical_{key}",
                        use_container_width=True,
                    ):
                        st.session_state.workflow_state["vertical"] = key
                        st.rerun()
                    st.caption(vertical["description"])

            st.markdown("---")
            st.markdown("### 🎯 O que cada vertical oferece:")

            for key, vertical in VERTICAL_AGENTS.items():
                with st.expander(f"{vertical['name']} - {vertical['description']}"):
                    st.markdown(f"**Segmentação:** {vertical['segmentation_help']}")
                    st.markdown("**Recursos:**")
                    for feature in vertical["features"]:
                        st.markdown(f"- {feature}")

        else:
            # Vertical selecionada - mostrar workflow normal
            vertical_key = st.session_state.workflow_state["vertical"]
            vertical_info = VERTICAL_AGENTS.get(vertical_key, {})

            st.markdown("""
            ### 👋 Bem-vindo ao Neuro Skills Agent!
            
            Sou seu assistente para criação e gestão de campanhas Meta Ads. Vou te ajudar com:
            
            - 📤 **Upload de criativos** (vídeos e imagens)
            - 📝 **Análise de briefing**
            - ✍️ **Geração de copy** baseada na voz da marca
            - 🎯 **Criação de campanhas** com targeting otimizado
            - 📊 **Acompanhamento de performance**
            
            **Para começar, preciso saber:**
            """)

            # Verificar se tem cliente e conta configurados
            if not active_client:
                st.warning("⚠️ Você precisa cadastrar um cliente primeiro.")
                if st.button("➕ Cadastrar Cliente", type="primary"):
                    st.session_state.workflow_state["step"] = "new_client"
                    st.rerun()
            elif not active_account:
                st.warning("⚠️ Você precisa configurar uma conta Meta Ads.")
                if st.button("⚙️ Configurar Conta", type="primary"):
                    st.session_state.workflow_state["step"] = "config_account"
                    st.rerun()
            else:
                st.success(f"✅ Pronto para começar!")
                st.markdown(f"**Cliente:** {active_client.get('name')}")
                st.markdown(f"**Conta:** {active_account.get('name')}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button(
                        "📤 Upload de Criativos",
                        type="primary",
                        use_container_width=True,
                    ):
                        st.session_state.workflow_state["step"] = "upload"
                        st.rerun()
                with col2:
                    if st.button(
                        "📝 Criar Briefing", type="primary", use_container_width=True
                    ):
                        st.session_state.workflow_state["step"] = "briefing"
                        st.rerun()

# ETAPA: NEW CLIENT
elif current_step == "new_client":
    with chat_container:
        st.markdown("### ➕ Cadastrar Novo Cliente")

        with st.form("new_client_form"):
            client_name = st.text_input(
                "Nome do Cliente *", placeholder="Ex: Nike Brasil"
            )
            client_id = st.text_input("ID do Cliente *", placeholder="Ex: nike")
            industry = st.selectbox(
                "Indústria",
                [
                    "",
                    "E-commerce",
                    "SaaS",
                    "Health Care",
                    "Fitness",
                    "Education",
                    "Retail",
                    "Services",
                    "Other",
                ],
            )

            col1, col2 = st.columns(2)
            with col1:
                age_min = st.number_input(
                    "Idade Mínima", min_value=18, max_value=65, value=25
                )
            with col2:
                age_max = st.number_input(
                    "Idade Máxima", min_value=18, max_value=65, value=55
                )

            locations = st.text_area(
                "Localizações (uma por linha)",
                placeholder="Brasil\nSão Paulo\nRio de Janeiro",
            )

            submitted = st.form_submit_button("Cadastrar Cliente", type="primary")

            if submitted:
                if not client_name or not client_id:
                    st.error("Preencha todos os campos obrigatórios")
                else:
                    client_data = {
                        "name": client_name,
                        "industry": industry,
                        "target_audience": {
                            "age_range": [age_min, age_max],
                            "locations": [
                                l.strip() for l in locations.split("\n") if l.strip()
                            ],
                        },
                    }

                    st.session_state.memory.create_client(
                        client_id.lower().replace(" ", "_"), client_data
                    )
                    st.session_state.memory.set_active_client(
                        client_id.lower().replace(" ", "_")
                    )

                    st.success(f"✅ Cliente '{client_name}' cadastrado!")
                    st.session_state.workflow_state["step"] = "start"
                    st.rerun()

        if st.button("← Voltar"):
            st.session_state.workflow_state["step"] = "start"
            st.rerun()

# ETAPA: CONFIG_ACCOUNT
elif current_step == "config_account":
    with chat_container:
        st.markdown("### ⚙️ Configurar Conta Meta Ads")

        # Listar contas existentes
        accounts = st.session_state.memory.list_accounts()

        if accounts.get("accounts"):
            st.markdown("**Contas Salvas:**")
            for acc_name, acc_data in accounts["accounts"].items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"- **{acc_data.get('name')}** (`{acc_name}`)")
                with col2:
                    if st.button("Usar", key=f"use_{acc_name}"):
                        st.session_state.memory.set_active_account(acc_name)
                        st.success("Conta ativada!")
                        st.session_state.workflow_state["step"] = "start"
                        st.rerun()

        st.markdown("---")
        st.markdown("**Adicionar Nova Conta:**")

        with st.form("new_account_form"):
            acc_name = st.text_input(
                "Nome da Conta *", placeholder="Ex: Nike Principal"
            )
            ad_account_id = st.text_input(
                "Ad Account ID *", placeholder="act_123456789"
            )
            access_token = st.text_input("Access Token *", type="password")
            pixel_id = st.text_input("Pixel ID (opcional)")
            page_id = st.text_input("Page ID (opcional)")

            submitted = st.form_submit_button("Salvar Conta", type="primary")

            if submitted:
                if not acc_name or not ad_account_id or not access_token:
                    st.error("Preencha todos os campos obrigatórios")
                else:
                    account_data = {
                        "name": acc_name,
                        "ad_account_id": ad_account_id.replace("act_", ""),
                        "access_token": access_token,
                        "pixel_id": pixel_id,
                        "page_id": page_id,
                    }

                    st.session_state.memory.save_account(
                        acc_name.lower().replace(" ", "_"), account_data
                    )
                    st.session_state.memory.set_active_account(
                        acc_name.lower().replace(" ", "_")
                    )

                    # Criar API client
                    st.session_state.api_client = MetaAPIClient(
                        access_token=access_token, ad_account_id=ad_account_id
                    )

                    st.success(f"✅ Conta '{acc_name}' salva e ativada!")
                    st.session_state.workflow_state["step"] = "start"
                    st.rerun()

        if st.button("← Voltar"):
            st.session_state.workflow_state["step"] = "start"
            st.rerun()

# ETAPA: UPLOAD
elif current_step == "upload":
    with chat_container:
        st.markdown("### 📤 Upload de Criativos")

        # Verificar se tem conta ativa
        if not active_account:
            st.warning("⚠️ Configure uma conta Meta Ads primeiro.")
            if st.button("⚙️ Configurar Conta"):
                st.session_state.workflow_state["step"] = "config_account"
                st.rerun()
        else:
            # Criar API client se não existir
            if st.session_state.api_client is None:
                st.session_state.api_client = MetaAPIClient(
                    access_token=active_account["access_token"],
                    ad_account_id=active_account["ad_account_id"],
                )

            st.info(f"📱 Conta: **{active_account.get('name')}**")

            # Upload de arquivos
            st.markdown("**Selecione os arquivos:**")
            uploaded_files = st.file_uploader(
                "Vídeos e Imagens",
                type=["mp4", "mov", "avi", "mkv", "jpg", "jpeg", "png", "gif"],
                accept_multiple_files=True,
                help="Arraste arquivos ou clique para selecionar",
            )

            if uploaded_files:
                st.markdown(f"**{len(uploaded_files)} arquivo(s) selecionado(s):**")

                # Mostrar arquivos selecionados
                for file in uploaded_files:
                    file_size = file.size / (1024 * 1024)
                    st.markdown(f"- {file.name} ({file_size:.1f} MB)")

                # Nome da campanha
                campaign_name = st.text_input(
                    "Nome da Campanha *",
                    placeholder="Ex: black_friday_2024",
                    value=st.session_state.workflow_state.get("campaign_name", ""),
                )

                if st.button("⬆️ Fazer Upload", type="primary"):
                    if not campaign_name:
                        st.error("Digite o nome da campanha")
                    else:
                        # Salvar arquivos temporariamente
                        temp_dir = st.session_state.config.upload_temp_dir
                        temp_dir.mkdir(parents=True, exist_ok=True)

                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        videos_uploaded = []
                        images_uploaded = []
                        errors = []

                        for i, file in enumerate(uploaded_files):
                            status_text.text(f"Enviando {file.name}...")

                            # Salvar arquivo temporário
                            temp_path = temp_dir / file.name
                            with open(temp_path, "wb") as f:
                                f.write(file.getbuffer())

                            # Upload
                            try:
                                if file.name.lower().endswith(
                                    (".mp4", ".mov", ".avi", ".mkv")
                                ):
                                    result = st.session_state.api_client.upload_video(
                                        temp_path
                                    )
                                    if result.get("success"):
                                        videos_uploaded.append(
                                            {
                                                "filename": file.name,
                                                "video_id": result["video_id"],
                                                "status": "completed",
                                            }
                                        )
                                    else:
                                        errors.append(
                                            f"{file.name}: {result.get('error')}"
                                        )
                                else:
                                    result = st.session_state.api_client.upload_image(
                                        temp_path
                                    )
                                    if result.get("success"):
                                        images_uploaded.append(
                                            {
                                                "filename": file.name,
                                                "hash": result["image_hash"],
                                                "status": "completed",
                                            }
                                        )
                                    else:
                                        errors.append(
                                            f"{file.name}: {result.get('error')}"
                                        )
                            except Exception as e:
                                errors.append(f"{file.name}: {str(e)}")

                            # Limpar arquivo temporário
                            temp_path.unlink()

                            # Atualizar progresso
                            progress_bar.progress((i + 1) / len(uploaded_files))

                        # Salvar resultados
                        st.session_state.workflow_state["uploaded_videos"] = (
                            videos_uploaded
                        )
                        st.session_state.workflow_state["uploaded_images"] = (
                            images_uploaded
                        )
                        st.session_state.workflow_state["campaign_name"] = campaign_name

                        # Mostrar resultados
                        st.markdown("---")
                        st.markdown("### 📊 Resultados do Upload")

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Vídeos", len(videos_uploaded))
                        with col2:
                            st.metric("Imagens", len(images_uploaded))
                        with col3:
                            st.metric("Erros", len(errors))

                        if videos_uploaded:
                            st.markdown("**🎥 Vídeos enviados:**")
                            for v in videos_uploaded:
                                st.code(f"✅ {v['filename']} → ID: {v['video_id']}")

                        if images_uploaded:
                            st.markdown("**🖼️ Imagens enviadas:**")
                            for img in images_uploaded:
                                st.code(
                                    f"✅ {img['filename']} → Hash: {img['hash'][:20]}..."
                                )

                        if errors:
                            st.markdown("**❌ Erros:**")
                            for e in errors:
                                st.error(e)

                        # Próximo passo
                        if (videos_uploaded or images_uploaded) and not errors:
                            if st.button("✅ Continuar para Briefing", type="primary"):
                                st.session_state.workflow_state["step"] = "briefing"
                                st.rerun()

        if st.button("← Voltar"):
            st.session_state.workflow_state["step"] = "start"
            st.rerun()

# ETAPA: BRIEFING
elif current_step == "briefing":
    with chat_container:
        st.markdown("### 📝 Briefing da Campanha")

        st.markdown("""
        **Preencha as informações da campanha:**
        
        Dica: Cole o briefing completo que o sistema vai extrair as informações automaticamente.
        """)

        briefing_text = st.text_area(
            "Briefing",
            height=300,
            placeholder="""# Briefing: Black Friday 2024

## Cliente
- **Cliente:** Nike Brasil
- **Produto:** Nike Air Max
- **Indústria:** Sportswear

## Objetivos
- **Objetivo Principal:** Vendas
- **CPA Alvo:** R$ 25
- **ROAS Alvo:** 4.0
- **Orçamento:** R$ 50.000/mês

## Público-Alvo
- **Idade:** 25 a 45 anos
- **Localização:** Brasil
- **Interesses:** corrida, fitness, esportes

## Criativos
- Vídeos já enviados via upload""",
            value=st.session_state.workflow_state.get("briefing", ""),
        )

        if st.button("🔍 Analisar Briefing", type="primary"):
            if not briefing_text:
                st.error("Digite o briefing")
            else:
                # Analisar briefing
                analysis = analyze_briefing(briefing_text)

                # Salvar briefing
                st.session_state.workflow_state["briefing"] = briefing_text
                st.session_state.workflow_state["briefing_analysis"] = analysis

                st.markdown("---")
                st.markdown("### 📊 Análise do Briefing")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Informações Extraídas:**")
                    st.markdown(
                        f"- **Cliente:** {analysis.get('client', 'Não identificado')}"
                    )
                    st.markdown(
                        f"- **Produto:** {analysis.get('product', 'Não identificado')}"
                    )
                    st.markdown(
                        f"- **Objetivo:** {analysis.get('objective', 'CONVERSIONS')}"
                    )
                    st.markdown(
                        f"- **Orçamento:** R$ {analysis.get('budget', 'Não identificado')}"
                    )

                with col2:
                    st.markdown("**Metas:**")
                    st.markdown(
                        f"- **CPA Alvo:** R$ {analysis.get('target_cpa', 'Não definido')}"
                    )
                    st.markdown(
                        f"- **ROAS Alvo:** {analysis.get('target_roas', 'Não definido')}x"
                    )

                # Verificar informações faltantes
                missing = []
                if not analysis.get("client"):
                    missing.append("Nome do cliente")
                if not analysis.get("product"):
                    missing.append("Produto/Serviço")
                if not analysis.get("objective"):
                    missing.append("Objetivo da campanha")
                if not analysis.get("budget"):
                    missing.append("Orçamento")

                if missing:
                    st.warning(f"⚠️ **Informações faltando:** {', '.join(missing)}")
                    st.markdown("Por favor, adicione essas informações ao briefing.")
                else:
                    st.success(
                        "✅ Todas as informações necessárias foram identificadas!"
                    )

                    # Verificar se tem criativos
                    videos = st.session_state.workflow_state.get("uploaded_videos", [])
                    images = st.session_state.workflow_state.get("uploaded_images", [])

                    if not videos and not images:
                        st.warning("⚠️ Você ainda não fez upload de criativos.")
                        if st.button("📤 Fazer Upload de Criativos"):
                            st.session_state.workflow_state["step"] = "upload"
                            st.rerun()
                    else:
                        st.markdown(
                            f"**Criativos disponíveis:** {len(videos)} vídeos, {len(images)} imagens"
                        )

                        if st.button("✍️ Gerar Copy e Targeting", type="primary"):
                            st.session_state.workflow_state["step"] = "generate"
                            st.rerun()

        if st.button("← Voltar"):
            st.session_state.workflow_state["step"] = "upload"
            st.rerun()

# ETAPA: GENERATE
elif current_step == "generate":
    with chat_container:
        st.markdown("### ✍️ Gerando Copy e Targeting")

        # Mostrar vertical selecionada
        vertical = st.session_state.workflow_state.get("vertical")
        if vertical and vertical in VERTICAL_AGENTS:
            st.info(f"📊 **Vertical:** {VERTICAL_AGENTS[vertical]['name']}")

        # Animação de processamento
        with st.spinner("Analisando briefing e gerando copy..."):
            import time

            time.sleep(1)

            # Obter brand voice do cliente
            client_id = st.session_state.memory.get_active_client()
            brand_voice = (
                st.session_state.memory.get_brand_voice(client_id) if client_id else {}
            )

            # Obter briefing analysis
            briefing = st.session_state.workflow_state.get("briefing_analysis", {})

            # Gerar copy com especialização por vertical
            copy_variants = generate_copy(briefing, brand_voice, vertical=vertical)
            st.session_state.workflow_state["copy_variants"] = copy_variants

            # Gerar targeting com especialização por vertical
            targeting = generate_targeting(briefing, brand_voice, vertical=vertical)
            st.session_state.workflow_state["targeting"] = targeting

        st.success("✅ Copy e Targeting gerados com sucesso!")

        # Mostrar copy variants
        st.markdown("### 📝 Variações de Copy")

        for i, variant in enumerate(copy_variants):
            with st.expander(
                f"**Variação {i + 1}: {variant['name']}**", expanded=(i == 0)
            ):
                st.markdown(f"**Headline:** {variant['headline']}")
                st.markdown(f"**Texto Principal:** {variant['primary_text']}")
                st.markdown(f"**CTA:** {variant['cta']}")

                # Editar copy
                with st.form(f"edit_copy_{i}"):
                    new_headline = st.text_input("Headline", value=variant["headline"])
                    new_text = st.text_area(
                        "Texto Principal", value=variant["primary_text"], height=100
                    )
                    new_cta = st.text_input("CTA", value=variant["cta"])

                    if st.form_submit_button("Salvar Alterações"):
                        st.session_state.workflow_state["copy_variants"][i][
                            "headline"
                        ] = new_headline
                        st.session_state.workflow_state["copy_variants"][i][
                            "primary_text"
                        ] = new_text
                        st.session_state.workflow_state["copy_variants"][i]["cta"] = (
                            new_cta
                        )
                        st.success("Copy atualizado!")
                        st.rerun()

        # Mostrar targeting
        st.markdown("### 🎯 Targeting")

        # Mostrar informações de vertical
        if vertical and vertical in VERTICAL_AGENTS:
            st.markdown(
                f"**Segmentação:** {VERTICAL_AGENTS[vertical]['segmentation_help']}"
            )

        with st.expander("Ver configurações detalhadas"):
            st.json(targeting)

        # Próximo passo
        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("← Voltar e Editar"):
                st.session_state.workflow_state["step"] = "briefing"
                st.rerun()

        with col2:
            if st.button("🚀 Criar Campanha", type="primary"):
                st.session_state.workflow_state["step"] = "create_campaign"
                st.rerun()

# ETAPA: CREATE_CAMPAIGN
elif current_step == "create_campaign":
    with chat_container:
        st.markdown("### 🚀 Criando Campanha")

        # Verificar se tem API client
        if st.session_state.api_client is None:
            account = get_active_account()
            if account:
                st.session_state.api_client = MetaAPIClient(
                    access_token=account["access_token"],
                    ad_account_id=account["ad_account_id"],
                )

        # Dados
        briefing = st.session_state.workflow_state.get("briefing_analysis", {})
        targeting = st.session_state.workflow_state.get("targeting", {})
        uploaded_videos = st.session_state.workflow_state.get("uploaded_videos", [])
        uploaded_images = st.session_state.workflow_state.get("uploaded_images", [])
        copy_variants = st.session_state.workflow_state.get("copy_variants", [])
        campaign_name = st.session_state.workflow_state.get("campaign_name", "Campanha")

        # Resumo
        st.markdown("**Resumo da Campanha:**")
        st.markdown(f"- **Cliente:** {briefing.get('client')}")
        st.markdown(f"- **Produto:** {briefing.get('product')}")
        st.markdown(f"- **Objetivo:** {briefing.get('objective')}")
        st.markdown(f"- **Orçamento:** R$ {briefing.get('budget')}/dia")
        st.markdown(f"- **Vídeos:** {len(uploaded_videos)}")
        st.markdown(f"- **Imagens:** {len(uploaded_images)}")
        st.markdown(f"- **Cópias:** {len(copy_variants)}")

        st.markdown("---")

        # Verificar se tem tudo
        if not uploaded_videos and not uploaded_images:
            st.error("❌ Nenhum criativo disponível. Faça upload primeiro.")
            if st.button("← Voltar para Upload"):
                st.session_state.workflow_state["step"] = "upload"
                st.rerun()
        elif not copy_variants:
            st.error("❌ Nenhuma cópia gerada. Gere as cópias primeiro.")
            if st.button("← Voltar para Briefing"):
                st.session_state.workflow_state["step"] = "briefing"
                st.rerun()
        else:
            # Criar campanha
            if st.button("🎯 Criar Campanha no Meta Ads", type="primary"):
                progress_container = st.empty()
                progress_bar = progress_container.progress(0)
                status_text = st.empty()

                try:
                    # Obter page_id da conta ativa
                    active_acc = get_active_account()
                    page_id = active_acc.get("page_id") if active_acc else None

                    if not page_id:
                        st.warning(
                            "⚠️ Page ID não configurado. A campanha será criada mas os ads podem precisar de ajuste manual."
                        )

                    status_text.text("📦 Preparando criativos...")
                    progress_bar.progress(10)

                    # Criar estrutura de campanha
                    creatives_data = {
                        "videos": uploaded_videos,
                        "images": uploaded_images,
                        "copies": copy_variants,
                    }

                    status_text.text("🎯 Criando campanha...")
                    progress_bar.progress(20)

                    # Criar campanha
                    campaign_name_full = f"{briefing.get('client', 'Cliente')} - {briefing.get('product', 'Produto')} - {datetime.now().strftime('%Y-%m-%d')}"
                    campaign_result = st.session_state.api_client.create_campaign(
                        name=campaign_name_full,
                        objective=briefing.get("objective", "CONVERSIONS"),
                        status="PAUSED",
                    )

                    if "id" not in campaign_result:
                        st.error(
                            f"❌ Erro ao criar campanha: {campaign_result.get('error', 'Erro desconhecido')}"
                        )
                    else:
                        campaign_id = campaign_result["id"]
                        st.session_state.workflow_state["campaign_id"] = campaign_id
                        status_text.text(f"✅ Campanha criada: {campaign_id}")
                        progress_bar.progress(40)

                        # Criar ad set
                        status_text.text("📊 Criando conjunto de anúncios...")
                        budget = briefing.get("budget", 5000)
                        adset_result = st.session_state.api_client.create_ad_set(
                            campaign_id=campaign_id,
                            name=f"{campaign_name_full} - Ad Set",
                            daily_budget=budget,
                            targeting=targeting,
                            optimization_goal="CONVERSIONS",
                        )

                        if "id" not in adset_result:
                            st.error(
                                f"❌ Erro ao criar ad set: {adset_result.get('error', 'Erro desconhecido')}"
                            )
                        else:
                            adset_id = adset_result["id"]
                            st.session_state.workflow_state["adset_id"] = adset_id
                            status_text.text(f"✅ Ad Set criado: {adset_id}")
                            progress_bar.progress(60)

                            # Criar ads
                            ads_created = []
                            for i, video in enumerate(uploaded_videos):
                                if video.get("status") == "completed" and video.get(
                                    "video_id"
                                ):
                                    # Obter copy correspondente
                                    copy = (
                                        copy_variants[i]
                                        if i < len(copy_variants)
                                        else copy_variants[0]
                                    )

                                    status_text.text(
                                        f"🎨 Criando creative {i + 1}/{len(uploaded_videos)}..."
                                    )
                                    progress_bar.progress(
                                        60 + (i / len(uploaded_videos)) * 30
                                    )

                                    # Criar creative
                                    creative_result = st.session_state.api_client.create_ad_creative(
                                        name=f"{campaign_name_full} - {video['filename']}",
                                        page_id=page_id or "0",
                                        video_id=video["video_id"],
                                        message=copy.get("primary_text", ""),
                                    )

                                    if "id" in creative_result:
                                        creative_id = creative_result["id"]

                                        # Criar ad
                                        ad_result = st.session_state.api_client.create_ad(
                                            ad_set_id=adset_id,
                                            name=f"{campaign_name_full} - Ad {i + 1}",
                                            creative_id=creative_id,
                                        )

                                        if "id" in ad_result:
                                            ads_created.append(
                                                {
                                                    "ad_id": ad_result["id"],
                                                    "creative_id": creative_id,
                                                    "video_id": video["video_id"],
                                                    "copy": copy,
                                                }
                                            )

                            st.session_state.workflow_state["ad_ids"] = ads_created
                            progress_bar.progress(95)

                            # Salvar na memória
                            client_id = st.session_state.memory.get_active_client()
                            campaign_record = {
                                "campaign_id": campaign_id,
                                "adset_id": adset_id,
                                "ad_ids": [a["ad_id"] for a in ads_created],
                                "campaign_name": campaign_name_full,
                                "briefing": briefing,
                                "targeting": targeting,
                                "creatives": creatives_data,
                                "created_at": datetime.now().isoformat(),
                                "status": "PAUSED",
                            }

                            if client_id:
                                st.session_state.memory.save_campaign(
                                    client_id, campaign_name, campaign_record
                                )

                            progress_bar.progress(100)
                            status_text.empty()

                            st.success("✅ Campanha criada com sucesso!")

                            st.markdown("### 📊 Detalhes da Campanha")
                            st.markdown(f"**Campaign ID:** `{campaign_id}`")
                            st.markdown(f"**Ad Set ID:** `{adset_id}`")
                            st.markdown(f"**Ads criados:** {len(ads_created)}")

                            for i, ad in enumerate(ads_created):
                                with st.expander(f"Ad {i + 1}"):
                                    st.markdown(f"**Ad ID:** `{ad['ad_id']}`")
                                    st.markdown(f"**Copy:** {ad['copy'].get('name')}")

                            st.markdown("---")
                            st.markdown("### 📋 Próximos Passos:")
                            st.markdown("""
                            1. Acesse o **Gerenciador de Anúncios** do Meta
                            2. **Revise** os criativos e cópias
                            3. Configure o **pixel** e **conversões**
                            4. **Ative** a campanha quando estiver pronto
                            5. **Monitore** a performance diariamente
                            """)

                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("➕ Criar Nova Campanha"):
                                    st.session_state.workflow_state = {
                                        "step": "start",
                                        "client_id": None,
                                        "campaign_name": None,
                                        "briefing": None,
                                        "creatives": [],
                                        "uploaded_videos": [],
                                        "uploaded_images": [],
                                        "brand_voice": None,
                                        "targeting": None,
                                        "copy_variants": [],
                                        "campaign_id": None,
                                        "adset_id": None,
                                        "ad_ids": [],
                                    }
                                    st.rerun()
                            with col2:
                                if st.button("📊 Ver Configurações"):
                                    st.session_state.workflow_state["step"] = "config"
                                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Erro ao criar campanha: {str(e)}")
                    if st.button("← Voltar e Tentar Novamente"):
                        st.session_state.workflow_state["step"] = "generate"
                        st.rerun()

        if st.button("← Voltar"):
            st.session_state.workflow_state["step"] = "generate"
            st.rerun()

# ETAPA: CONFIG
elif current_step == "config":
    with chat_container:
        st.markdown("### ⚙️ Configurações")

        tab1, tab2, tab3 = st.tabs(["Clientes", "Contas Meta", "Sistema"])

        with tab1:
            st.subheader("Clientes")

            # Listar clientes
            clients = st.session_state.memory.list_clients()

            if clients.get("clients"):
                for cid, cdata in clients["clients"].items():
                    with st.expander(f"**{cdata.get('name', cid)}**"):
                        st.json(cdata)
            else:
                st.info("Nenhum cliente cadastrado.")

            if st.button("➕ Novo Cliente"):
                st.session_state.workflow_state["step"] = "new_client"
                st.rerun()

        with tab2:
            st.subheader("Contas Meta Ads")

            accounts = st.session_state.memory.list_accounts()

            if accounts.get("accounts"):
                for aname, adata in accounts["accounts"].items():
                    with st.expander(f"**{adata.get('name', aname)}**"):
                        st.markdown(f"- **ID:** {adata.get('ad_account_id')}")
                        st.markdown(f"- **Pixel:** {adata.get('pixel_id', 'N/A')}")
                        st.markdown(f"- **Page:** {adata.get('page_id', 'N/A')}")
            else:
                st.info("Nenhuma conta cadastrada.")

            if st.button("➕ Nova Conta"):
                st.session_state.workflow_state["step"] = "config_account"
                st.rerun()

        with tab3:
            st.subheader("Sistema")
            st.markdown(f"**Diretório:** `{NEURO_DIR}`")
            st.markdown(f"**Versão:** v2.0.0-beta")

            if st.button("📦 Backup"):
                st.info("Funcionalidade em desenvolvimento")

            if st.button("🗑️ Limpar Cache"):
                st.info("Funcionalidade em desenvolvimento")

        if st.button("← Voltar ao Início"):
            st.session_state.workflow_state["step"] = "start"
            st.rerun()

# ETAPA: DASHBOARD
elif current_step == "dashboard":
    with chat_container:
        st.markdown("### 📊 Dashboard de Performance")

        # Verificar se tem conta ativa
        if not active_account:
            st.warning("⚠️ Configure uma conta Meta Ads primeiro.")
            if st.button("⚙️ Configurar Conta"):
                st.session_state.workflow_state["step"] = "config_account"
                st.rerun()
        else:
            # Criar API client se não existir
            if st.session_state.api_client is None:
                st.session_state.api_client = MetaAPIClient(
                    access_token=active_account["access_token"],
                    ad_account_id=active_account["ad_account_id"],
                )

            # Criar analytics engine se não existir
            if st.session_state.analytics is None:
                st.session_state.analytics = AnalyticsEngine(
                    api_client=st.session_state.api_client,
                    memory_manager=st.session_state.memory,
                )

            # Filtros
            col1, col2, col3 = st.columns(3)

            with col1:
                date_range = st.selectbox(
                    "Período",
                    ["today", "last_7d", "last_14d", "last_30d", "lifetime"],
                    index=1,
                )

            with col2:
                breakdown = st.selectbox(
                    "Agrupamento", ["account", "campaign", "adset", "ad"], index=1
                )

            with col3:
                if st.button("🔄 Atualizar", type="primary"):
                    st.rerun()

            st.markdown("---")

            # Análise
            with st.spinner("Carregando dados..."):
                try:
                    analysis = st.session_state.analytics.analyze_account(
                        date_range=date_range, breakdown=breakdown
                    )

                    # Métricas principais
                    st.markdown("### 📈 Métricas Gerais")
                    metrics = analysis.get("metrics", {})

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric("Gasto", f"R${metrics.get('spend', 0):.2f}")

                    with col2:
                        st.metric("Impressões", f"{metrics.get('impressions', 0):,}")

                    with col3:
                        st.metric("Cliques", f"{metrics.get('clicks', 0):,}")

                    with col4:
                        ctr = metrics.get("ctr", 0)
                        st.metric("CTR", f"{ctr:.2f}%")

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        cpm = metrics.get("cpm", 0)
                        st.metric("CPM", f"R${cpm:.2f}")

                    with col2:
                        cpc = metrics.get("cpc", 0)
                        st.metric("CPC", f"R${cpc:.2f}")

                    with col3:
                        cpa = (
                            analysis.get("account_insights", {})
                            .get("cost_per_action_type", {})
                            .get("purchase", 0)
                        )
                        st.metric("CPA", f"R${cpa:.2f}")

                    with col4:
                        roas = metrics.get("roas", 0)
                        st.metric("ROAS", f"{roas:.2f}x")

                    st.markdown("---")

                    # Alertas
                    alerts = analysis.get("alerts", [])
                    if alerts:
                        st.markdown("### ⚠️ Alertas")
                        for alert in alerts:
                            if alert.get("level") == "critical":
                                st.error(f"🚨 {alert.get('message')}")
                            elif alert.get("level") == "warning":
                                st.warning(f"⚠️ {alert.get('message')}")
                            else:
                                st.info(f"ℹ️ {alert.get('message')}")

                        st.markdown("---")

                    # Recomendações
                    recommendations = analysis.get("recommendations", [])
                    if recommendations:
                        st.markdown("### 💡 Recomendações")
                        for rec in recommendations[:3]:
                            priority = rec.get("priority", "medium")
                            if priority == "high":
                                st.markdown(f"🔴 **{rec.get('message')}**")
                            elif priority == "medium":
                                st.markdown(f"🟡 {rec.get('message')}")
                            else:
                                st.markdown(f"🟢 {rec.get('message')}")

                        st.markdown("---")

                    # Campanhas
                    if breakdown == "campaign":
                        campaigns = analysis.get("breakdown_insights", {}).get(
                            "data", []
                        )
                        if campaigns:
                            st.markdown("### 🎯 Campanhas")

                            for campaign in campaigns[:10]:
                                with st.expander(f"**{campaign.get('name', 'N/A')}**"):
                                    col1, col2, col3 = st.columns(3)
                                    col1.metric(
                                        "Gasto",
                                        f"R${float(campaign.get('spend', 0)):.2f}",
                                    )
                                    col2.metric(
                                        "CPA", f"R${campaign.get('cpa', 0):.2f}"
                                    )
                                    col3.metric("CTR", f"{campaign.get('ctr', 0):.2f}%")

                except Exception as e:
                    st.error(f"Erro ao carregar dados: {str(e)}")

        if st.button("← Voltar"):
            st.session_state.workflow_state["step"] = "start"
            st.rerun()

# ETAPA: AUTOMATIONS
elif current_step == "automations":
    with chat_container:
        st.markdown("### ⚡ Automações")

        if not active_account:
            st.warning("⚠️ Configure uma conta Meta Ads primeiro.")
            if st.button("⚙️ Configurar Conta"):
                st.session_state.workflow_state["step"] = "config_account"
                st.rerun()
        else:
            # Criar scheduler se não existir
            if st.session_state.scheduler is None:
                st.session_state.scheduler = AutomationScheduler(
                    memory_manager=st.session_state.memory,
                    api_client=st.session_state.api_client,
                )

            # Tabs
            tab1, tab2, tab3 = st.tabs(
                ["📋 Jobs Ativos", "➕ Nova Automação", "📊 Histórico"]
            )

            with tab1:
                st.subheader("Jobs Agendados")

                jobs = st.session_state.scheduler.get_jobs()

                if jobs:
                    for job in jobs:
                        with st.expander(
                            f"**{job.get('name', job['id'])}** - {job.get('type')}"
                        ):
                            col1, col2 = st.columns(2)

                            with col1:
                                st.markdown(f"**Tipo:** {job.get('type')}")
                                st.markdown(
                                    f"**Agendamento:** {job.get('schedule_type')} - {job.get('schedule_value')}"
                                )
                                st.markdown(
                                    f"**Status:** {'✅ Ativo' if job.get('enabled') else '⏸️ Pausado'}"
                                )

                            with col2:
                                st.markdown(
                                    f"**Última execução:** {job.get('last_run', 'Nunca')}"
                                )
                                st.markdown(f"**Execuções:** {job.get('run_count', 0)}")

                            col1, col2, col3 = st.columns(3)

                            with col1:
                                if st.button("▶️ Executar", key=f"run_{job['id']}"):
                                    result = st.session_state.scheduler._execute_job(
                                        job
                                    )
                                    st.success("Job executado!")
                                    st.json(result)

                            with col2:
                                if st.button(
                                    "⏸️ Pausar/Ativar", key=f"toggle_{job['id']}"
                                ):
                                    st.session_state.scheduler.toggle_job(job["id"])
                                    st.rerun()

                            with col3:
                                if st.button("🗑️ Remover", key=f"remove_{job['id']}"):
                                    st.session_state.scheduler.remove_job(job["id"])
                                    st.rerun()
                else:
                    st.info("Nenhuma automação configurada.")

            with tab2:
                st.subheader("Nova Automação")

                with st.form("new_automation"):
                    job_name = st.text_input(
                        "Nome da Automação", placeholder="Ex: Pausar CPA Alto"
                    )

                    job_type = st.selectbox(
                        "Tipo", ["analysis", "optimization", "report", "rule"]
                    )

                    schedule_type = st.selectbox(
                        "Agendamento", ["interval", "daily", "weekly", "monthly"]
                    )

                    if schedule_type == "interval":
                        schedule_value = st.text_input(
                            "Intervalo", placeholder="1h, 30m, 24h"
                        )
                    elif schedule_type == "daily":
                        schedule_value = st.text_input("Horário", placeholder="09:00")
                    elif schedule_type == "weekly":
                        schedule_value = st.text_input(
                            "Dia e Horário", placeholder="monday 09:00"
                        )
                    else:
                        schedule_value = st.text_input(
                            "Dia e Horário", placeholder="01 09:00"
                        )

                    # Parâmetros específicos
                    st.markdown("**Parâmetros:**")

                    if job_type == "analysis":
                        client_id = st.text_input("Client ID (deixe vazio para todos)")
                        campaigns = st.text_area(
                            "Campaign IDs (um por linha)",
                            placeholder="123456789\n987654321",
                        )
                        cpa_threshold = st.number_input("CPA Threshold", value=100.0)
                        roas_threshold = st.number_input("ROAS Threshold", value=2.0)

                    elif job_type == "optimization":
                        optimization_type = st.selectbox(
                            "Tipo de Otimização",
                            [
                                "scale_high_performers",
                                "pause_low_performers",
                                "budget_reallocation",
                                "creative_rotation",
                            ],
                        )
                        campaigns = st.text_area(
                            "Campaign IDs (um por linha)",
                            placeholder="123456789\n987654321",
                        )

                    elif job_type == "report":
                        report_type = st.selectbox(
                            "Tipo de Relatório", ["performance", "creative", "audience"]
                        )
                        report_format = st.selectbox(
                            "Formato", ["json", "csv", "excel"]
                        )
                        email = st.text_input("Email para envio (opcional)")

                    elif job_type == "rule":
                        rule_type = st.selectbox(
                            "Tipo de Regra",
                            ["pause_cpa_high", "scale_roas_high", "notify_spend_high"],
                        )
                        threshold = st.number_input("Threshold", value=100.0)

                    submitted = st.form_submit_button("Criar Automação", type="primary")

                    if submitted:
                        # Montar parâmetros
                        params = {}

                        if job_type == "analysis":
                            params["client_id"] = client_id or None
                            params["campaigns"] = [
                                c.strip() for c in campaigns.split("\n") if c.strip()
                            ]
                            params["cpa_threshold"] = cpa_threshold
                            params["roas_threshold"] = roas_threshold

                        elif job_type == "optimization":
                            params["type"] = optimization_type
                            params["campaigns"] = [
                                c.strip() for c in campaigns.split("\n") if c.strip()
                            ]

                        elif job_type == "report":
                            params["report_type"] = report_type
                            params["format"] = report_format
                            params["email"] = email or None

                        elif job_type == "rule":
                            params["type"] = rule_type
                            params["threshold"] = threshold

                        # Criar job
                        job = st.session_state.scheduler.add_job(
                            job_id=f"job_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                            job_type=job_type,
                            schedule_type=schedule_type,
                            schedule_value=schedule_value,
                            params=params,
                            enabled=True,
                        )

                        st.success(f"Automação criada: {job['id']}")
                        st.rerun()

            with tab3:
                st.subheader("Histórico de Execuções")

                # Mostrar histórico dos jobs
                for job in jobs:
                    if job.get("last_result"):
                        with st.expander(
                            f"**{job.get('name', job['id'])}** - {job.get('last_run')}"
                        ):
                            st.json(job.get("last_result"))

                if not any(job.get("last_result") for job in jobs):
                    st.info("Nenhum histórico de execução.")

        if st.button("← Voltar"):
            st.session_state.workflow_state["step"] = "start"
            st.rerun()

# ETAPA: ANALYTICS
elif current_step == "analytics":
    with chat_container:
        st.markdown("### 📈 Analytics")

        if not active_account:
            st.warning("⚠️ Configure uma conta Meta Ads primeiro.")
            if st.button("⚙️ Configurar Conta"):
                st.session_state.workflow_state["step"] = "config_account"
                st.rerun()
        else:
            # Criar analytics se não existir
            if st.session_state.analytics is None:
                st.session_state.analytics = AnalyticsEngine(
                    api_client=st.session_state.api_client,
                    memory_manager=st.session_state.memory,
                )

            # Tabs
            tab1, tab2, tab3, tab4 = st.tabs(
                ["📊 Performance", "🎨 Criativos", "👤 Públicos", "📋 Relatórios"]
            )

            with tab1:
                st.subheader("Performance de Campanhas")

                col1, col2 = st.columns(2)

                with col1:
                    date_range = st.selectbox(
                        "Período",
                        ["last_7d", "last_14d", "last_30d", "last_90d"],
                        index=0,
                    )

                with col2:
                    if st.button("🔍 Analisar", type="primary"):
                        st.rerun()

                st.markdown("---")

                # Análise de conta
                if st.button("📊 Analisar Conta Inteira"):
                    with st.spinner("Analisando..."):
                        result = st.session_state.analytics.analyze_account(
                            date_range=date_range, breakdown="campaign"
                        )

                        st.success("Análise completa!")

                        # Mostrar resumo
                        st.json(result.get("summary", {}))

                        # Mostrar métricas
                        st.markdown("**Métricas:**")
                        st.json(result.get("metrics", {}))

            with tab2:
                st.subheader("Análise de Criativos")

                st.info(
                    "Em desenvolvimento - Análise detalhada de performance de criativos"
                )

            with tab3:
                st.subheader("Análise de Públicos")

                st.info("Em desenvolvimento - Análise de performance por público")

            with tab4:
                st.subheader("Gerar Relatório")

                with st.form("generate_report"):
                    report_type = st.selectbox(
                        "Tipo de Relatório", ["performance", "creative", "audience"]
                    )

                    date_range = st.selectbox(
                        "Período", ["last_7d", "last_14d", "last_30d"]
                    )

                    format_type = st.selectbox("Formato", ["json", "csv"])

                    submitted = st.form_submit_button(
                        "📄 Gerar Relatório", type="primary"
                    )

                    if submitted:
                        with st.spinner("Gerando relatório..."):
                            # Lista de campanhas ativas
                            campaigns_result = (
                                st.session_state.api_client.list_campaigns(
                                    status="ACTIVE"
                                )
                            )
                            campaigns = [
                                c["id"] for c in campaigns_result.get("campaigns", [])
                            ]

                            report = st.session_state.analytics.generate_report(
                                report_type=report_type,
                                campaigns=campaigns,
                                date_range=date_range,
                                format=format_type,
                            )

                            st.success("Relatório gerado!")

                            # Mostrar resumo
                            st.markdown("**Resumo Executivo:**")
                            st.json(report.get("summary", {}))

                            # Mostrar totais
                            st.markdown("**Totais:**")
                            st.json(report.get("totals", {}))

                            # Download
                            if format_type == "json":
                                st.download_button(
                                    "📥 Baixar JSON",
                                    json.dumps(report, indent=2),
                                    file_name=f"relatorio_{report_type}_{datetime.now().strftime('%Y%m%d')}.json",
                                    mime="application/json",
                                )
                            elif format_type == "csv":
                                csv_data = st.session_state.analytics._format_csv(
                                    report
                                )
                                st.download_button(
                                    "📥 Baixar CSV",
                                    csv_data,
                                    file_name=f"relatorio_{report_type}_{datetime.now().strftime('%Y%m%d')}.csv",
                                    mime="text/csv",
                                )

        if st.button("← Voltar"):
            st.session_state.workflow_state["step"] = "start"
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<center>🧠 Neuro Skills Agent v2.0.0-beta | ©2026 Monrars | MIT License</center>",
    unsafe_allow_html=True,
)
