"""
Neuro Skills Agent - Interface Principal
Autor: Monrars (@monrars)
Instagram: @monrars
"""

import streamlit as st
from pathlib import Path
import sys
import os

# Adicionar diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import Config, NEURO_DIR
from core.memory import MemoryManager
from core.meta_api import MetaAPIClient
from upload.video_uploader import BatchUploader

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
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    .status-pending {
        color: #ffc107;
        font-weight: bold;
    }
</style>
""",
    unsafe_allow_html=True,
)


# Inicialização
@st.cache_resource
def init_memory():
    """Inicializa gerenciador de memória"""
    return MemoryManager(NEURO_DIR)


@st.cache_resource
def get_config():
    """Retorna configuração"""
    return Config()


# Sessão state
if "memory" not in st.session_state:
    st.session_state.memory = init_memory()

if "config" not in st.session_state:
    st.session_state.config = get_config()

if "api_client" not in st.session_state:
    st.session_state.api_client = None

if "current_client" not in st.session_state:
    st.session_state.current_client = st.session_state.memory.get_active_client()

# Sidebar
with st.sidebar:
    st.markdown("### 🧠 Neuro Skills Agent")
    st.markdown("---")

    # Navegação
    page = st.radio(
        "Navegação",
        [
            "🏠 Dashboard",
            "👤 Clientes",
            "📁 Campanhas",
            "⬆️ Upload",
            "📊 Insights",
            "⚙️ Configurações",
        ],
        key="navigation",
    )

    st.markdown("---")

    # Cliente ativo
    active_client = st.session_state.memory.get_active_client()
    if active_client:
        st.markdown(f"**Cliente Ativo:** `{active_client}`")
    else:
        st.markdown("**Cliente Ativo:** Nenhum")

    st.markdown("---")
    st.markdown("📱 [@monrars](https://instagram.com/monrars)")
    st.markdown("MIT License ©2026")

# ===================== DASHBOARD =====================
if page == "🏠 Dashboard":
    st.markdown('<h1 class="main-header">🧠 Dashboard</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Visão geral do Neuro Skills Agent</p>',
        unsafe_allow_html=True,
    )

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    clients = st.session_state.memory.list_clients()
    accounts = st.session_state.memory.list_accounts()

    num_clients = len(clients.get("clients", {}))
    num_accounts = len(accounts.get("accounts", {}))

    with col1:
        st.metric(label="Clientes", value=num_clients)
    with col2:
        st.metric(label="Contas Meta", value=num_accounts)
    with col3:
        st.metric(label="Campanhas Ativas", value=0)  # TODO: implementar
    with col4:
        st.metric(label="Uploads Hoje", value=0)  # TODO: implementar

    st.markdown("---")

    # Ações rápidas
    st.subheader("⚡ Ações Rápidas")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("➕ Novo Cliente", use_container_width=True):
            st.session_state.navigation = "👤 Clientes"
            st.rerun()

    with col2:
        if st.button("📁 Nova Campanha", use_container_width=True):
            st.session_state.navigation = "📁 Campanhas"
            st.rerun()

    with col3:
        if st.button("⬆️ Upload Criativos", use_container_width=True):
            st.session_state.navigation = "⬆️ Upload"
            st.rerun()

    st.markdown("---")

    # Últimos uploads
    st.subheader("📤 Últimos Uploads")
    st.info("Nenhum upload realizado ainda.")

    # Clientes recentes
    st.subheader("👥 Clientes Recentes")
    if clients.get("recent_clients"):
        for client_id in clients["recent_clients"][:5]:
            client_data = clients["clients"].get(client_id, {})
            st.markdown(f"- **{client_data.get('name', client_id)}** ({client_id})")
    else:
        st.info("Nenhum cliente cadastrado.")

# ===================== CLIENTES =====================
elif page == "👤 Clientes":
    st.markdown('<h1 class="main-header">👤 Clientes</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Gerenciar clientes e suas configurações</p>',
        unsafe_allow_html=True,
    )

    tab1, tab2 = st.tabs(["Lista de Clientes", "Novo Cliente"])

    with tab1:
        st.subheader("Clientes Cadastrados")

        clients = st.session_state.memory.list_clients()

        if clients.get("clients"):
            for client_id, client_data in clients["clients"].items():
                with st.expander(
                    f"**{client_data.get('name', client_id)}** - {client_data.get('industry', 'Sem indústria')}"
                ):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(f"**ID:** {client_id}")
                        st.write(f"**Nome:** {client_data.get('name', 'N/A')}")
                        st.write(f"**Indústria:** {client_data.get('industry', 'N/A')}")

                    with col2:
                        st.write(
                            f"**Criado:** {client_data.get('created_at', 'N/A')[:10] if client_data.get('created_at') else 'N/A'}"
                        )
                        st.write(
                            f"**Último Uso:** {client_data.get('last_used', 'N/A')[:10] if client_data.get('last_used') else 'N/A'}"
                        )

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("✏️ Editar", key=f"edit_{client_id}"):
                            st.info("Funcionalidade em desenvolvimento")
                    with col2:
                        if st.button("🎯 Ativar", key=f"activate_{client_id}"):
                            st.session_state.memory.set_active_client(client_id)
                            st.session_state.current_client = client_id
                            st.success(f"Cliente {client_id} ativado!")
                            st.rerun()
                    with col3:
                        if st.button("📁 Ver Campanhas", key=f"campaigns_{client_id}"):
                            st.info("Funcionalidade em desenvolvimento")
        else:
            st.info(
                "Nenhum cliente cadastrado. Clique em 'Novo Cliente' para adicionar."
            )

    with tab2:
        st.subheader("Cadastrar Novo Cliente")

        with st.form("new_client_form"):
            col1, col2 = st.columns(2)

            with col1:
                client_id = st.text_input(
                    "ID do Cliente *", placeholder="ex: nike, fitness_app"
                )
                client_name = st.text_input(
                    "Nome do Cliente *", placeholder="Ex: Nike Brasil"
                )

            with col2:
                client_industry = st.selectbox(
                    "Indústria",
                    [
                        "",
                        "E-commerce",
                        "SaaS",
                        "Health & Fitness",
                        "Education",
                        "Finance",
                        "Retail",
                        "Other",
                    ],
                )
                client_website = st.text_input("Website", placeholder="https://...")

            st.markdown("**Público-Alvo**")
            col1, col2, col3 = st.columns(3)

            with col1:
                age_min = st.number_input(
                    "Idade Mínima", min_value=18, max_value=65, value=25
                )
                age_max = st.number_input(
                    "Idade Máxima", min_value=18, max_value=65, value=45
                )

            with col2:
                gender = st.selectbox("Gênero", ["Todos", "Masculino", "Feminino"])

            with col3:
                locations = st.text_area(
                    "Localizações (uma por linha)",
                    placeholder="Brasil\nArgentina\nChile",
                )

            st.markdown("**Objetivos**")
            col1, col2 = st.columns(2)

            with col1:
                primary_goal = st.selectbox(
                    "Objetivo Principal",
                    [
                        "Conversions",
                        "Traffic",
                        "Awareness",
                        "Lead Generation",
                        "App Installs",
                    ],
                )

            with col2:
                target_cpa = st.number_input(
                    "CPA Alvo (R$)", min_value=0.0, value=25.0, step=5.0
                )
                target_roas = st.number_input(
                    "ROAS Alvo", min_value=0.0, value=4.0, step=0.5
                )

            budget = st.number_input(
                "Orçamento Mensal (R$)", min_value=0, value=5000, step=500
            )

            submitted = st.form_submit_button("Cadastrar Cliente", type="primary")

            if submitted:
                if not client_id or not client_name:
                    st.error("Preencha os campos obrigatórios (*)")
                else:
                    client_data = {
                        "name": client_name,
                        "industry": client_industry,
                        "website": client_website,
                        "target_audience": {
                            "age_range": [age_min, age_max],
                            "gender": gender.lower(),
                            "locations": [
                                l.strip() for l in locations.split("\n") if l.strip()
                            ],
                        },
                        "business_objectives": {
                            "primary": primary_goal,
                            "target_cpa": target_cpa,
                            "target_roas": target_roas,
                            "budget": budget,
                        },
                    }

                    st.session_state.memory.create_client(
                        client_id.lower().replace(" ", "_"), client_data
                    )
                    st.success(f"Cliente '{client_name}' cadastrado com sucesso!")
                    st.rerun()

# ===================== UPLOAD =====================
elif page == "⬆️ Upload":
    st.markdown(
        '<h1 class="main-header">⬆️ Upload de Criativos</h1>', unsafe_allow_html=True
    )
    st.markdown(
        '<p class="sub-header">Upload de vídeos e imagens para Meta Ads</p>',
        unsafe_allow_html=True,
    )

    # Verificar se há conta ativa
    accounts = st.session_state.memory.list_accounts()
    active_account = accounts.get("active_account")

    if not active_account:
        st.warning(
            "⚠️ Nenhuma conta Meta Ads ativa. Configure uma conta em 'Configurações'."
        )
    else:
        account = accounts.get("accounts", {}).get(active_account, {})
        st.info(f"📱 Conta ativa: **{account.get('name', active_account)}**")

        # Verificar se API client está configurado
        if st.session_state.api_client is None:
            access_token = account.get("access_token")
            ad_account_id = account.get("ad_account_id")

            if access_token and ad_account_id:
                st.session_state.api_client = MetaAPIClient(access_token, ad_account_id)
            else:
                st.error("Conta não possui token ou ID configurado.")

        tab1, tab2 = st.tabs(["Upload de Arquivos", "Upload em Lote"])

        with tab1:
            st.subheader("Upload de Criativo Individual")

            with st.form("upload_form"):
                col1, col2 = st.columns(2)

                with col1:
                    creative_type = st.radio("Tipo de Criativo", ["Vídeo", "Imagem"])
                    uploaded_file = st.file_uploader(
                        "Selecionar Arquivo",
                        type=["mp4", "mov", "avi", "mkv", "jpg", "jpeg", "png", "gif"],
                    )

                with col2:
                    creative_name = st.text_input(
                        "Nome do Criativo", placeholder="Ex: ad_01_feed_video"
                    )
                    campaign_name = st.text_input(
                        "Nome da Campanha", placeholder="Ex: black_friday_2024"
                    )

                submit = st.form_submit_button("⬆️ Fazer Upload", type="primary")

                if submit and uploaded_file:
                    if not creative_name:
                        st.error("Digite o nome do criativo.")
                    else:
                        # Salvar arquivo temporariamente
                        temp_dir = st.session_state.config.upload_temp_dir
                        temp_dir.mkdir(parents=True, exist_ok=True)

                        temp_path = temp_dir / uploaded_file.name
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        st.info("📤 Iniciando upload...")

                        # Progress bar
                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        def on_progress(proportion, uploaded, total):
                            progress_bar.progress(proportion)
                            mb_uploaded = uploaded / (1024 * 1024)
                            mb_total = total / (1024 * 1024)
                            status_text.text(
                                f"Enviando: {mb_uploaded:.1f}MB / {mb_total:.1f}MB ({proportion * 100:.1f}%)"
                            )

                        # Upload
                        if creative_type == "Vídeo":
                            result = st.session_state.api_client.upload_video(
                                video_path=temp_path, progress_callback=on_progress
                            )
                        else:
                            result = st.session_state.api_client.upload_image(
                                image_path=temp_path
                            )
                            progress_bar.progress(1.0)

                        # Limpar arquivo temporário
                        temp_path.unlink()

                        # Resultado
                        if result.get("success"):
                            st.success(f"✅ Upload concluído!")
                            st.json(
                                {
                                    "video_id": result.get("video_id"),
                                    "image_hash": result.get("image_hash"),
                                    "file_size_mb": result.get("file_size_mb"),
                                    "filename": result.get("filename"),
                                }
                            )
                        else:
                            st.error(f"❌ Erro no upload: {result.get('error')}")

        with tab2:
            st.subheader("Upload em Lote")

            st.markdown("""
            **Como funciona:**
            1. Selecione uma pasta com criativos
            2. O sistema envia todos os vídeos e imagens
            3. Aguarde a confirmação de cada upload
            
            **Formatos suportados:**
            - Vídeos: `.mp4`, `.mov`, `.avi`, `.mkv`
            - Imagens: `.jpg`, `.jpeg`, `.png`, `.gif`
            """)

            folder_path = st.text_input(
                "Caminho da Pasta", placeholder="/campanhas/nike/2024-03/black_friday/"
            )

            campaign_name = st.text_input("Nome da Campanha para Metadados")

            if st.button("📤 Upload em Lote", type="primary"):
                if not folder_path:
                    st.error("Digite o caminho da pasta.")
                else:
                    folder = Path(folder_path)

                    if not folder.exists():
                        st.error(f"Pasta não encontrada: {folder_path}")
                    else:
                        # Batch upload
                        batch_uploader = BatchUploader(
                            st.session_state.api_client, st.session_state.memory
                        )

                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        def on_progress(proportion, uploaded, total):
                            progress_bar.progress(proportion)
                            status_text.text(
                                f"Progresso geral: {proportion * 100:.1f}%"
                            )

                        with st.spinner("Enviando criativos..."):
                            results = batch_uploader.upload_creatives_from_folder(
                                folder_path=folder,
                                campaign_name=campaign_name or "batch_upload",
                                progress_callback=on_progress,
                            )

                        progress_bar.progress(1.0)

                        # Mostrar resultados
                        st.subheader("📊 Resultados")

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric("Vídeos", len(results.get("videos", [])))
                        with col2:
                            st.metric("Imagens", len(results.get("images", [])))
                        with col3:
                            st.metric("Erros", len(results.get("errors", [])))

                        if results.get("videos"):
                            st.subheader("🎥 Vídeos")
                            for video in results["videos"]:
                                status_emoji = (
                                    "✅" if video["status"] == "completed" else "❌"
                                )
                                st.write(
                                    f"{status_emoji} {video['file']} - {video['status']}"
                                )
                                if video.get("video_id"):
                                    st.code(f"Video ID: {video['video_id']}")

                        if results.get("images"):
                            st.subheader("🖼️ Imagens")
                            for image in results["images"]:
                                st.write(
                                    f"✅ {image['file']} - Hash: {image['hash'][:20]}..."
                                )

                        if results.get("errors"):
                            st.subheader("⚠️ Erros")
                            for error in results["errors"]:
                                st.error(f"{error['file']}: {error['error']}")

# ===================== CAMPANHAS =====================
elif page == "📁 Campanhas":
    st.markdown('<h1 class="main-header">📁 Campanhas</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Gerenciar campanhas e criativos</p>',
        unsafe_allow_html=True,
    )

    st.info("🚧 Módulo em desenvolvimento")

    # TODO: Implementar gestão de campanhas
    st.markdown("""
    **Funcionalidades planejadas:**
    - Lista de campanhas
    - Criar nova campanha
    - Editar campanha
    - Duplicar campanha
    - Ver performance
    """)

# ===================== INSIGHTS =====================
elif page == "📊 Insights":
    st.markdown('<h1 class="main-header">📊 Insights</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Análise de performance e aprendizados</p>',
        unsafe_allow_html=True,
    )

    st.info("🚧 Módulo em desenvolvimento")

    # TODO: Implementar insights
    st.markdown("""
    **Funcionalidades planejadas:**
    - Dashboard de performance
    - Benchmarks do mercado
    - Aprendizados de campanhas
    - Recomendações automáticas
    """)

# ===================== CONFIGURAÇÕES =====================
elif page == "⚙️ Configurações":
    st.markdown('<h1 class="main-header">⚙️ Configurações</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Configurar contas e preferências</p>',
        unsafe_allow_html=True,
    )

    tab1, tab2 = st.tabs(["Contas Meta Ads", "Sistema"])

    with tab1:
        st.subheader("Contas Meta Ads")

        # Listar contas
        accounts = st.session_state.memory.list_accounts()

        if accounts.get("accounts"):
            st.markdown("**Contas Salvas:**")

            for acc_name, acc_data in accounts["accounts"].items():
                with st.expander(f"**{acc_data.get('name', acc_name)}** ({acc_name})"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(
                            f"**Status:** {'✅ Ativa' if acc_data.get('is_active') else '⏸️ Inativa'}"
                        )
                        st.write(
                            f"**Conta ID:** {acc_data.get('ad_account_id', 'N/A')}"
                        )
                        st.write(f"**Pixel ID:** {acc_data.get('pixel_id', 'N/A')}")
                        st.write(f"**Page ID:** {acc_data.get('page_id', 'N/A')}")

                    with col2:
                        st.write(f"**Moeda:** {acc_data.get('currency', 'N/A')}")
                        st.write(f"**Timezone:** {acc_data.get('timezone', 'N/A')}")
                        st.write(
                            f"**Criado:** {acc_data.get('created_at', 'N/A')[:10] if acc_data.get('created_at') else 'N/A'}"
                        )

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🎯 Ativar", key=f"activate_acc_{acc_name}"):
                            st.session_state.memory.set_active_account(acc_name)
                            st.success(f"Conta {acc_name} ativada!")
                            st.rerun()
                    with col2:
                        if st.button("🗑️ Remover", key=f"remove_acc_{acc_name}"):
                            st.warning("Funcionalidade em desenvolvimento")
        else:
            st.info("Nenhuma conta cadastrada.")

        st.markdown("---")

        # Adicionar nova conta
        st.subheader("Adicionar Nova Conta")

        with st.form("new_account_form"):
            acc_name = st.text_input(
                "Nome da Conta *", placeholder="Ex: Nike Principal"
            )
            ad_account_id = st.text_input(
                "Ad Account ID *", placeholder="act_123456789 ou 123456789"
            )
            access_token = st.text_input("Access Token *", type="password")

            col1, col2 = st.columns(2)

            with col1:
                pixel_id = st.text_input("Pixel ID (opcional)")
                page_id = st.text_input("Page ID (opcional)")

            with col2:
                business_id = st.text_input("Business ID (opcional)")
                currency = st.selectbox("Moeda", ["BRL", "USD", "EUR", "GBP"])

            submitted = st.form_submit_button("Adicionar Conta", type="primary")

            if submitted:
                if not acc_name or not ad_account_id or not access_token:
                    st.error("Preencha todos os campos obrigatórios (*)")
                else:
                    account_data = {
                        "name": acc_name,
                        "ad_account_id": ad_account_id,
                        "access_token": access_token,
                        "pixel_id": pixel_id,
                        "page_id": page_id,
                        "business_id": business_id,
                        "currency": currency,
                        "is_active": True,
                    }

                    st.session_state.memory.save_account(
                        acc_name.lower().replace(" ", "_"), account_data
                    )
                    st.success(f"Conta '{acc_name}' adicionada com sucesso!")
                    st.rerun()

    with tab2:
        st.subheader("Sistema")

        st.markdown("**Informações:**")
        st.write(f"**Diretório:** `{NEURO_DIR}`")
        st.write(f"**Versão:** v2.0.0-beta")

        st.markdown("---")

        # Backup
        st.subheader("Backup")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("📦 Criar Backup"):
                import tarfile
                from datetime import datetime

                backup_file = (
                    NEURO_DIR.parent
                    / f"neuro-skills_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
                )

                with tarfile.open(backup_file, "w:gz") as tar:
                    tar.add(NEURO_DIR, arcname="neuro-skills")

                st.success(f"Backup criado: {backup_file}")

        with col2:
            if st.button("🗑️ Limpar Cache"):
                import shutil

                cache_dirs = [
                    NEURO_DIR / "sessions" / "meta-ads-manager" / "cache",
                    NEURO_DIR / "sessions" / "traffic-strategist" / "cache",
                    NEURO_DIR / "sessions" / "ad-copywriter" / "cache",
                ]

                for cache_dir in cache_dirs:
                    if cache_dir.exists():
                        shutil.rmtree(cache_dir)
                        cache_dir.mkdir(parents=True)

                st.success("Cache limpo!")

        st.markdown("---")
        st.markdown("**📱 Autor:** [@monrars](https://instagram.com/monrars)")
        st.markdown(
            "**🔗 GitHub:** [monrars1995/neuro-skills](https://github.com/monrars1995/neuro-skills)"
        )

# Footer
st.markdown("---")
st.markdown(
    "<center>🧠 Neuro Skills Agent v2.0.0-beta | ©2026 Monrars | MIT License</center>",
    unsafe_allow_html=True,
)
