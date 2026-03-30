# Agent de Campanhas - Imobiliárias

> Especializado em campanhas para imobiliárias e corretores

**Versão:** 1.0.0  
**Vertical:** Imobiliário  
**Autor:** Monrars (@monrars)

## Características do Vertical

### Jornada de Compra (Medium-High Ticket)

```
Interesse → Pesquisa → Visita → Proposta → Negociação → Fechamento → Pós-Venda
    ↓          ↓          ↓          ↓           ↓          ↓         ↓
  30-90dias  7-30dias   1-7dias   7-30dias    7-15dias   1-30dias  Contínuo
```

### Eventos e Timing

| Evento | Frequência | Importância | Offline? |
|--------|------------|-------------|----------|
| Page View | Alta | Média | Não |
| Lead Form | Média | Alta | Não |
| Agendamento Visita | Baixa | Alta | **Sim** |
| Proposta | Baixa | Muito Alta | **Sim** |
| Fechamento | Baixa | Crítica | **Sim** |
| Aluguel | Média | Alta | **Sim** |

### Diferenças vs Concessionárias

| Aspecto | Concessionária | Imobiliária |
|---------|---------------|-------------|
| Ticket médio | R$50-200k | R$300k-2M (venda) / R$2-10k/mês (aluguel) |
| Ciclo de venda | 7-90dias | **30-180dias** |
| Margem comissão | 8-12% | **3-6%** |
| Produto | Novo/Semi-novo | **Único por unidade** |
| Inventário | Rotativo | **Fixo por localização** |
| Offline conversions | Obrigatório | **Obrigatório** |
| Janela de atribuição | 90 dias | **90-180 dias** |

## Configurações Recomendadas

### 1. Janela de Atribuição

```yaml
attribution_window:
  click_through: 30    # dias
  view_through: 7      # dias
  conversion_window: 90 # dias (venda) / 180 dias (aluguel)
```

### 2. Objetivos de Campanha

**Principais:**
- `LEAD_GENERATION` - Capturar contatos de interessados
- `CONVERSIONS` - Conversão offline (vendas/aluguel)

**Secundários:**
- `TRAFFIC` - Direcionar para site/landing
- `VIDEO_VIEWS` - Tours virtuais

### 3. Segmentação Específica

**Por Tipo de Imóvel:**
```yaml
property_types:
  - "Apartamento"
  - "Casa"
  - "Terreno"
  - "Comercial"
  - "Lançamento"
  - "Pronto"
  - "Aluguel"
```

**Por Faixa de Valor:**
```yaml
price_ranges:
  economy: "R$150k-400k"
  mid: "R$400k-1M"
  high: "R$1M-3M"
  luxury: "R$3M+"
```

**Por Localização:**
```yaml
locations:
  neighborhoods: true  # Segmentação por bairros
  radius: 10km        # Raio do imóvel
  cities: ["São Paulo", "Rio de Janeiro", "Belo Horizonte"]
```

## Estratégias de Campanha

### 1. Topo de Funil (Descoberta)

**Objetivo:** `REACH` ou `VIDEO_VIEWS`

**Público:**
```yaml
targeting:
  interests:
    - "Imóveis"
    - "Casa própria"
    - "Investimento imobiliário"
    - "Financiamento imobiliário"
  life_events:
    - "Recently moved"
    - "Newly engaged"
    - "Newlyweds"
  behaviors:
    - "Engaged shoppers"
    - "Net worth high"
  age_min: 25
  age_max: 55
  locations:
    - "{cidade}:{bairro}"
```

**Orçamento:** R$50-100/dia

**Criativo:**
- Vídeos de tours virtuais (30-60s)
- Carrosséis de imóveis em destaque
- Depoimentos de clientes
- Before/After de reformas

### 2. Meio de Funil (Consideração)

**Objetivo:** `LEAD_GENERATION`

**Público:**
```yaml
targeting:
  custom_audiences:
    - "Visitantes Site (30 dias)"
    - "Engajados no Facebook (7 dias)"
    - "Similar a Compradores (5%)"
  exclusions:
    - "Já são clientes"
    - "Leads antigos (90 dias)"
```

**Orçamento:** R$100-300/dia

**Lead Forms:**
- Agendamento de Visita
- Simulação de Financiamento
- Avaliação de Imóvel
- Cadastro para Lançamentos

### 3. Fundo de Funil (Conversão)

**Objetivo:** `CONVERSIONS` (offline)

**Público:**
```yaml
targeting:
  custom_audiences:
    - "Leads (90 dias)"
    - "Visitas (60 dias)"
    - "Propostas (30 dias)"
  exclusions:
    - "Vendas (365 dias)"
    - "Aluguéis (180 dias)"
```

**Orçamento:** R$200-500/dia

**Eventos Offline:**
- Visita Agendada
- Visita Realizada
- Proposta Enviada
- Fechamento Finalizado

## Cron Jobs Específicos

### Job 1: Upload de Conversões Offline (7 dias)

```python
scheduler.add_job(
    job_id="imobiliaria_offline_sync",
    job_type="offline_conversion",
    schedule_type="interval",
    schedule_value="7d",
    params={
        "pixel_id": "{PIXEL_ID}",
        "events": [
            {"name": "Lead", "source": "formulario_site"},
            {"name": "Visit", "source": "crm"},
            {"name": "Proposal", "source": "crm"},
            {"name": "Sale", "source": "venda"},
            {"name": "Rent", "source": "locacao"}
        ],
        "batch_size": 500,
        "match_keys": ["em", "ph"],
        "property_data": True
    }
)
```

### Job 2: Atualização de Inventário (Diário)

```python
scheduler.add_job(
    job_id="imobiliaria_inventory_update",
    job_type="feed_update",
    schedule_type="daily",
    schedule_value="06:00",
    params={
        "feed_id": "{CATALOG_ID}",
        "source": "erp",
        "fields": [
            "property_id",
            "title",
            "description",
            "price",
            "location",
            "bedrooms",
            "bathrooms",
            "area",
            "images",
            "status"
        ]
    }
)
```

### Job 3: Relatório de Desempenho (Semanal)

```python
scheduler.add_job(
    job_id="imobiliaria_weekly_report",
    job_type="report",
    schedule_type="weekly",
    schedule_value="monday 09:00",
    params={
        "report_type": "performance",
        "date_range": "last_7d",
        "kpis": [
            "leads",
            "visits_scheduled",
            "visits_completed",
            "proposals",
            "sales",
            "rentals",
            "cost_per_lead",
            "cost_per_visit",
            "cost_per_sale"
        ],
        "breakdown": "property_type",
        "email": "corretor@imobiliaria.com"
    }
)
```

## Modelo de ROI/ROAS

### Cálculo para Imobiliária (Venda):

```python
def calculate_real_state_roi(spend, sales_data):
    """
    Calcula ROI considerando:
    - Vendas (comissão sobre venda)
    - Aluguéis (comissão sobre contrato)
    - Captação de imóveis
    """
    # Vendas
    avg_sale_price = sales_data.get('avg_sale_price', 800000)
    commission_rate_sale = sales_data.get('commission_sale', 0.06)  # 6%
    sales_count = sales_data.get('sales_count', 0)
    
    revenue_sale = avg_sale_price * commission_rate_sale * sales_count
    
    # Aluguéis
    avg_rent_price = sales_data.get('avg_rent_price', 3000)
    commission_rate_rent = sales_data.get('commission_rent', 1.0)  # 1 mês
    rentals_count = sales_data.get('rentals_count', 0)
    
    revenue_rent = avg_rent_price * commission_rate_rent * rentals_count
    
    # Total
    total_revenue = revenue_sale + revenue_rent
    
    # ROI e ROAS
    roi = ((total_revenue - spend) / spend) * 100 if spend > 0 else 0
    roas = total_revenue / spend if spend > 0 else 0
    
    return {
        "total_revenue": round(total_revenue, 2),
        "roi_percentage": round(roi, 2),
        "roas": round(roas, 2),
        "sales_revenue": round(revenue_sale, 2),
        "rentals_revenue": round(revenue_rent, 2)
    }

# Exemplo
result = calculate_real_state_roi(
    spend=15000,
    sales_data={
        'sales_count': 3,
        'rentals_count': 5,
        'avg_sale_price': 800000,
        'avg_rent_price': 3000,
        'commission_sale': 0.06,
        'commission_rent': 1.0
    }
)

# Resultado:
# {
#   "total_revenue": 159000,      # R$159.000
#   "roi_percentage": 960,         # 960% ROI
#   "roas": 10.6,                  # 10.6x ROAS
#   "sales_revenue": 144000,       # R$144.000
#   "rentals_revenue": 15000       # R$15.000
# }
```

## Segmentação Avançada

### Por Estágio de Vida

```yaml
life_stages:
  first_time_buyer:
    interests: ["Casa própria", "Financiamento"]
    age: "25-35"
    budget: "economy"
    
  upgrade:
    interests: ["Mudança de casa", "Investimento"]
    age: "35-50"
    budget: "mid"
    
  investor:
    interests: ["Investimento imobiliário", "Renda passiva"]
    age: "35-60"
    budget: "high"
    
  luxury:
    interests: ["Imóveis de luxo", "Apartamentos de alto padrão"]
    age: "40-65"
    budget: "luxury"
```

### Por Comportamento

```yaml
behaviors:
  active_searcher:
    - "Visitou site nos últimos 7 dias"
    - "Clicou em anúncio de imóvel"
    
  engaged:
    - "Preencheu formulário de contato"
    - "Baixou material de lançamento"
    
 Qualified:
    - "Agendou visita"
    - "Solicitou simulação"
```

## Checklist de Implementação

### Setup Inicial

- [ ] Criar Pixel do Facebook
- [ ] Configurar eventos padrão (PageView, ViewContent, Lead)
- [ ] Configurar eventos customizados (Visit, Proposal, Sale, Rent)
- [ ] Criar catálogo de imóveis
- [ ] Configurar feed de inventário
- [ ] Criar conta de anúncios
- [ ] Configurar lista de clientes para exclusão

### Integração ERP/CRM

- [ ] Mapear eventos do CRM
- [ ] Configurar hash de dados (SHA256)
- [ ] Criar script de exportação
- [ ] Agendar uploads semanais
- [ ] Testar upload de eventos offline

### Campanhas

- [ ] Criar campanha de Awareness
- [ ] Criar campanha de Lead Generation
- [ ] Criar públicos personalizados
- [ ] Criar lookalikes
- [ ] Configurar exclusões

## Tags de Rastreamento

### No Site

```javascript
// Page View
fbq('track', 'PageView');

// View Content (Imóvel)
fbq('track', 'ViewContent', {
  content_ids: ['PROP_12345'],
  content_type: 'property',
  content_name: 'Apartamento 3 Quartos - Pinheiros',
  content_category: 'residential',
  value: 850000,
  currency: 'BRL'
});

// Lead (Formulário)
fbq('track', 'Lead', {
  content_name: 'Agendamento de Visita',
  content_category: 'property',
  property_id: 'PROP_12345'
});

// Lead (Contato)
fbq('track', 'Contact', {
  content_name: 'Interesse em Imóvel',
  content_category: 'property',
  property_id: 'PROP_12345'
});

// Purchase (Venda)
fbq('track', 'Purchase', {
  content_ids: ['PROP_12345'],
  content_type: 'property',
  value: 850000,
  currency: 'BRL',
  property_type: 'apartment',
  transaction_type: 'sale'
});
```

## Exemplo Completo

```python
from core.memory import MemoryManager
from core.meta_api import MetaAPIClient
from scheduler.automation import AutomationScheduler

# Inicializar
memory = MemoryManager()
api = MetaAPIClient(
    access_token="EAA...",
    ad_account_id="act_123456789"
)
scheduler = AutomationScheduler(memory, api)

# ========== SETUP ==========

# Criar catálogo de imóveis
catalog = api.create_product_catalog(
    name="Imóveis - Imobiliária XYZ",
    vertical="HOME_LISTINGS"
)

# Criar feed de inventário
feed = api.create_product_feed(
    catalog_id=catalog["id"],
    name="Feed de Imóveis",
    schedule={"interval": "DAILY", "hour": 6}
)

# Criar campanha para lançamento
campaign = api.create_campaign(
    name="Lançamento Residencial Garden - Pré-Venda",
    objective="LEAD_GENERATION",
    budget=30000,  # R$300/dia
    special_config={
        "attribution_window": 30,
        "offline_conversion": True,
        "catalog_id": catalog["id"],
        "property_type": "apartment",
        "price_range": "mid"
    }
)

# Criar lead form
form = api.create_lead_form(
    name="Interesse - Residencial Garden",
    questions=[
        {"type": "NAME", "label": "Nome completo"},
        {"type": "EMAIL", "label": "E-mail"},
        {"type": "PHONE", "label": "WhatsApp"},
        {
            "type": "CUSTOM",
            "label": "Tipo de interesse",
            "options": ["Moradia", "Investimento", "Aluguel"]
        },
        {
            "type": "CUSTOM",
            "label": "Como conheceu?",
            "options": ["Google", "Facebook", "Indicação", "Outros"]
        }
    ],
    privacy_url="https://imobiliaria.com/privacidade",
    thankyou_message="Obrigado! Nossos corretores entrarão em contato em até 24h."
)

# Criar público por interesse
audience = api.create_audience(
    name="Interessados em Imóveis - São Paulo",
    audience_type="interest",
    config={
        "interests": ["Imóveis", "Casa própria", "Financiamento imobiliário"],
        "behaviors": ["Engaged shoppers"],
        "life_events": ["Recently moved"],
        "age_min": 25,
        "age_max": 55,
        "locations": ["Brazil:São Paulo"]
    }
)

# ========== CRON JOBS ==========

# 1. Upload de conversões offline (7dias)
scheduler.add_job(
    job_id="realestate_offline_conversion",
    job_type="offline_conversion",
    schedule_type="interval",
    schedule_value="7d",
    params={
        "pixel_id": "123456789",
        "events": ["Lead", "Visit", "Proposal", "Sale", "Rent"],
        "match_keys": ["em", "ph"],
        "batch_size": 500
    }
)

# 2. Atualização de inventário (diário)
scheduler.add_job(
    job_id="realestate_inventory_update",
    job_type="feed_update",
    schedule_type="daily",
    schedule_value="06:00",
    params={
        "feed_id": feed["id"],
        "source": "erp"
    }
)

# 3. Relatório semanal
scheduler.add_job(
    job_id="realestate_weekly_report",
    job_type="report",
    schedule_type="weekly",
    schedule_value="monday 09:00",
    params={
        "report_type": "performance",
        "kpis": ["leads", "visits", "sales", "rentals"],
        "breakdown": "property_type",
        "email": "corretor@imobiliaria.com"
    }
)

# Iniciar scheduler
scheduler.start()

print("✅ Setup completo!")
```

## Métricas Específicas

### Topo de Funil
```yaml
metrics:
  - reach
  - frequency
  - impressions
  - video_views
  - cost_per_1k_people
benchmarks:
  - frequency: "> 2x"
  - cpm: "< R$25"
  - video_completion_rate: "> 50%"
```

### Meio de Funil
```yaml
metrics:
  - leads
  - cost_per_lead
  - lead_to_visit_rate
  - form_completion_rate
benchmarks:
  - cpl: "< R$50"
  - lead_to_visit: "> 20%"
```

### Fundo de Funil
```yaml
metrics:
  - visits
  - proposals
  - sales
  - rentals
  - cost_per_visit
  - cost_per_sale
benchmarks:
  - cpv: "< R$200"
  - cps: "< R$3000"
  - roas: "> 5x"
```

## Troubleshooting

### Baixo Volume de Leads?

```yaml
diagnosis:
  - frequency_too_low: Aumente orçamento
  - audience_too_small: Expanda localização
  - creative_not_converting: Teste tours virtuais
  - form_too_long: Simplifique formulário

solution:
  - increase_budget: +50%
  - expand_location: Incluir bairros próximos
  - test_video: Tours 360°
  - reduce_fields: 3-4 campos máx
```

### Alto Custo por Lead?

```yaml
diagnosis:
  - target_too_narrow: Amplie segmentação
  - competition_high: Teste horários diferentes
  - creative_fatigue: Rotação de criativos
  - wrong_audience: Revise interesses

solution:
  - expand_audience: +10% raio
  - test_schedules: 8-12h, 18-22h
  - rotate_creatives: Semanal
  - create_exclusions: Já convertidos
```

### Baixa Taxa de Visita?

```yaml
diagnosis:
  - leads_mal_qualificados: Melhore formulário
  - follow_up_lento: WhatsApp imediato
  - imovel_indisponivel: Atualize inventário

solution:
  - add_questions: "Quando pretende comprar?"
  - automate_whatsapp: Resposta em 5min
  - sync_inventory: Daily update
```

## Licença

MIT License - © 2026 Monrars