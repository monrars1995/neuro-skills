# Neuro Skills Agent

Sistema de automação de Meta Ads com interface conversacional.

## Visão Geral

O Agent é uma aplicação Streamlit que integra os skills doNeuro Skills para automatizar todo o processo de criação de campanhas Meta Ads:

1. **Upload de Criativos** - Upload de vídeos e imagens com acompanhamento de progresso
2. **Análise de Briefing** - Extração automática de informações do briefing
3. **Geração de Copy** - Criação de variações de copy baseadas na voz da marca
4. **Criação de Campanhas** - Criação automática via Meta Graph API

## Arquitetura

```
agent/
├── core/
│   ├── __init__.py
│   ├── config.py          # Configurações e constantes
│   ├── memory.py          # Sistema de memória compartilhada
│   └── meta_api.py        # Cliente Meta Graph API v21.0
├── upload/
│   ├── __init__.py
│   └── video_uploader.py  # Upload de vídeos com progresso
├── ui/
│   ├── __init__.py
│   └── app.py            # Interface Streamlit
└── run.py                 # Entry point
```

## Skills Integrados

### 1. meta-ads-manager

Gerenciador completo de Meta Ads com Graph API v21.0.

**Funcionalidades:**
- Listar contas de anúncios
- Criar campanhas, ad sets e ads
- Upload de vídeos e imagens
- Gestão de criativos
- Insights e métricas

**Uso no Agent:**
```python
from core.meta_api import MetaAPIClient

api_client = MetaAPIClient(
    access_token="your_token",
    ad_account_id="123456789"
)

# Upload de vídeo
result = api_client.upload_video(Path("video.mp4"))

# Criar campanha
campaign = api_client.create_campaign(
    name="Campanha Black Friday",
    objective="CONVERSIONS"
)
```

### 2. traffic-strategist

Agente de preparação e análise de campanhas.

**Funcionalidades:**
- Análise de briefing
- Extração de informações
- Validação de requisitos
- Preparação para copy

**Uso no Agent:**
```python
# Análise de briefing
analysis = analyze_briefing(briefing_text)

# Extrações automáticas
client = analysis.get("client")
product = analysis.get("product")
objective = analysis.get("objective")
budget = analysis.get("budget")
```

### 3. ad-copywriter

Especialista em copy e voz da marca.

**Funcionalidades:**
- Geração de variações de copy
- Templates por objetivo
- Aplicação de voice profile
- CTA otimizados

**Uso no Agent:**
```python
# Gerar copy
variants = generate_copy(
    briefing=briefing_analysis,
    brand_voice=brand_voice,
    num_variants=3
)

# Estrutura de cada variante
# {
#     "id": "copy_1",
#     "name": "Direct Conversion",
#     "headline": "...",
#     "primary_text": "...",
#     "cta": "Compre Agora",
#     "format": "feed"
# }
```

## Sistema de Memória

O Agent usa o sistema de memória compartilhada para persistir dados entre sessões:

### Estrutura

```
~/.neuro-skills/
├── clients/
│   └── {client_id}/
│       ├── client.json        # Dados do cliente
│       ├── brand_voice.json   # Voz da marca
│       └── campaigns/
│           └── {campaign}/
│               └── campaign.json
├── accounts/
│   └── accounts.json          # Contas Meta Ads
└── memory.json                # Memória global
```

### Uso

```python
from core.memory import MemoryManager

memory = MemoryManager()

# Salvar cliente
memory.create_client("nike_brasil", {
    "name": "Nike Brasil",
    "industry": "Sportswear",
    "target_audience": {...}
})

# Ativar cliente
memory.set_active_client("nike_brasil")

# Salvar camapanha
memory.save_campaign("nike_brasil", "black_friday_2024", {
    "campaign_id": "123456",
    "status": "active"
})
```

## Meta Graph API

### Autenticação

O Agent usa OAuth2 com Access Token:

```python
# Configurar conta
account_data = {
    "name": "Minha Conta",
    "ad_account_id": "123456789",
    "access_token": "EAA...",
    "page_id": "987654321"
}

memory.save_account("minha_conta", account_data)
```

### Upload de Vídeos

```python
# Upload com progresso
def progress_callback(proportion, uploaded, total):
    print(f"Progress: {proportion * 100:.1f}%")

result = api_client.upload_video(
    video_path=Path("video.mp4"),
    progress_callback=progress_callback
)
```

### Criar Campanha Completa

```python
# 1. Criar campanha
campaign = api_client.create_campaign(
    name="Black Friday 2024",
    objective="CONVERSIONS",
    status="PAUSED"
)

# 2. Criar ad set
adset = api_client.create_ad_set(
    campaign_id=campaign["id"],
    name="Black Friday - Ad Set",
    daily_budget=5000,  # centavos
    targeting={
        "age_min": 25,
        "age_max": 45,
        "genders": ["male", "female"],
        "locations": ["BR"]
    }
)

# 3. Criar creative
creative = api_client.create_ad_creative(
    name="Black Friday - Video 1",
    page_id="987654321",
    video_id="123456789",
    message="Aproveite as ofertas!"
)

# 4. Criar ad
ad = api_client.create_ad(
    ad_set_id=adset["id"],
    name="Black Friday - Ad",
    creative_id=creative["id"]
)
```

## Fluxo de Trabalho

### 1. Start

- Verificar cliente ativo
- Verificar conta ativa
- Oferecer opções: Upload ou Briefing

### 2. Upload

- Selecionar arquivos (vídeos/imagens)
- Upload com progresso em tempo real
- Salvar IDs dos vídeos/imagens

### 3. Briefing

- Inserir/colar briefing
- Análise automática
- Validação de informações

### 4. Generate

- Gerar variações de copy
- Gerar targeting
- Permitir edição

### 5. Create Campaign

- Resumo da campanha
- Confirmação
- Criação via API
- Resumo final

## Executar

### Instalação

```bash
cd agent
pip install -r requirements.txt
```

### Executar

```bash
cd agent
python3 -m streamlit run ui/app.py --server.headless=true --server.port=8501
```

### Background

```bash
cd agent
nohup python3 -m streamlit run ui/app.py --server.headless=true --server.port=8501 &
```

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz:

```env
NEURO_DIR=~/.neuro-skills
META_APP_ID=your_app_id
META_APP_SECRET=your_app_secret
```

## Próximos Passos

1. **Gestão de Campanhas Existentes**
   - Listar campanhas
   - Editar configurações
   - Duplicar campanhas
   - Pausar/ativar

2. **Performance Dashboard**
   - Métricas em tempo real
   - Gráficos de performance
   - Alertas de CPA/ROAS

3. **A/B Testing**
   - Criar experimentos
   - Analisar resultados
   - Recomendações automáticas

4. **Automações**
   - Regras automáticas
   - Escala automática
   - Pausa por performance

## Licença

MIT License - ©2026 Monrars

## Autor

**Monrars**  
Instagram: [@monrars](https://instagram.com/monrars)  
GitHub: [github.com/monrars1995/neuro-skills](https://github.com/monrars1995/neuro-skills)