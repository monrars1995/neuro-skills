# Agent de Campanhas - Concessionárias

> Especializado em campanhas de concessionárias de veículos com conversão offline

**Versão:** 1.0.0  
**Vertical:** Automobilístico  
**Autor:** Monrars (@monrars)

## Características do Vertical

### Jornada de Compra (Sales Cycle Longo)

```
Interesse → Pesquisa → Visita → Test Drive → Proposta → Negociação → Venda → Pós-Venda
   ↓          ↓          ↓          ↓           ↓          ↓        ↓         ↓
   7-90dias  7-30dias  1-7dias   1-7dias     7-30dias   1-7dias  1dia     Contínuo
```

### Eventos e Timing

| Evento | Frequência | importância | Offline? |
|--------|------------|-------------|----------|
| Page View | Alta | Média | Não |
| Lead Form | Média | Alta | Não |
| Test Drive | Baixa | Alta | **Sim** |
| Proposta | Baixa | Muito Alta | **Sim** |
| Venda | Baixa | Crítica | **Sim** |
| Agendamento Serviço | Média | Alta | **Sim** |

### Diferenças vs E-commerce

| Aspecto | E-commerce | Concessionária |
|---------|-----------|---------------|
| Ciclo de venda | 1-7 dias |7-90 dias |
| Ticket médio | R$100-1000 | R$50.000-200.000 |
| Volumetria de eventos | Alta | Baixa |
| Offline conversions | Raro | **Obrigatório** |
| Janela de atribuição | 7-30 dias | **30-90 dias** |
| CRM envio automático | Sim | **Não** |
| Frequência de sync | Tempo real | **7-14 dias** |

## Configurações Recomendadas

### 1. Janela de Atribuição

```yaml
attribution_window:
  click_through: 30  # dias
  view_through: 7    # dias
  conversion_window: 90 # dias
```

### 2. Objetivos de Campanha

**Principais:**
- `LEAD_GENERATION` - Capturar contatos de interessados
- `CONVERSIONS` - Conversão offline (vendas)

**Secundários:**
- `TRAFFIC` - Direcionar para site/landing
- `AWARENESS` - Reconhecimento de marca

### 3. Pixel e CRM

**Configuração do Pixel:**
```javascript
// Eventos online (automáticos)
fbq('track', 'PageView');
fbq('track', 'Lead', {
  content_name: 'Test Drive - Civic',
  content_category: 'Test Drive'
});

// Eventos offline (via upload)
// Ver seção Offline Conversion
```

**Eventos CRM para Offline:**
```json
{
  "event_name": "Purchase",
  "event_time": 1704067200,
  "user_data": {
    "em": ["7b52e31b2e..."], // email hash
    "ph": ["1234567890"]     // phone hash
  },
  "custom_data": {
    "currency": "BRL",
    "value": 125000,
    "content_name": "Honda Civic EXL",
    "content_category": "Sedan",
    "vehicle_brand": "Honda",
    "vehicle_model": "Civic",
    "vehicle_year": 2024
  }
}
```

### 4. Conversão Offline

**Frequência de Upload:** Mínimo 7 dias, ideal 3-5 dias

**Dados Necessários do CRM:**
```csv
email,phone,event_name,event_time,value,vehicle_model
cliente@email.com,11999887766,Lead,2024-01-15T10:30:00,,
cliente2@email.com,11988776655,TestDrive,2024-01-16T14:00:00,,
cliente@email.com,11999887766,Purchase,2024-01-20T16:45:00,125000,Honda Civic
```

**Processo de Upload:**
```python
# Enviar eventos offline a cada 7 dias
scheduler.add_job(
    job_id="upload_offline_conversions",
    job_type="offline_conversion",
    schedule_type="interval",
    schedule_value="7d",  # Mínimo recomendado
    params={
        "pixel_id": "123456789",
        "batch_size": 1000,
        "match_keys": ["em", "ph"],
        "events": ["Lead", "TestDrive", "Purchase"]
    }
)
```

## Estratégias de Campanha

### 1. Topo de Funil (Awareness e Consideração)

**Objetivo:** `REACH` ou `TRAFFIC`

**Público:**
```yaml
targeting:
  interests:
    - "Carros"
    - "Automóveis"
    - "Test drive"
    - "Compra de carro"
    - "{marca}" # Honda, Toyota, etc
  behaviors:
    - "Engaged shoppers"
    - "Auto intenders"
  age_min: 25
  age_max: 55
  locations:
    - "Brazil"
    - "São Paulo" # Região da concessionária
```

**Orçamento:** R$50-100/dia

**Creativo:**
- Vídeos 15-30s dos veículos
- Carrosséis com diferenciais
- Ofertas e condições especiais

### 2. Meio de Funil (Consideração)

**Objetivo:** `LEAD_GENERATION`

**Público:**
```yaml
targeting:
  custom_audiences:
    - "Visitantes do Site (30 dias)"
    - "Engajados no Facebook (7 dias)"
    - "Similar a Clientes (1%)"
  exclusions:
    - "Já são clientes"
```

**Orçamento:** R$100-200/dia

**Lead Forms:**
- Test Drive Agendamento
- Simulação de Financiamento
- Cotação de Usado

### 3. Fundo de Funil (Conversão)

**Objetivo:** `CONVERSIONS` (offline)

**Público:**
```yaml
targeting:
  custom_audiences:
    - "Leads (90 dias)"
    - "Test Drives (60 dias)"
    - "Propostas (30 dias)"
  exclusions:
    - "Vendas (180 dias)"
```

**Orçamento:** R$200-500/dia

**Eventos Offline:**
- Test Drive Realizado
- Proposta Enviada
- Venda Concluída

## Cron Jobs Específicos para Concessionárias

### Job 1: Upload de Conversões Offline (7dias)

```python
scheduler.add_job(
    job_id="concessionaria_offline_sync",
    job_type="offline_conversion",
    schedule_type="interval",
    schedule_value="7d",
    params={
        "pixel_id": "{PIXEL_ID}",
        "events": [
            {"name": "Lead", "source": "formulario_site"},
            {"name": "TestDrive", "source": "crm"},
            {"name": "Schedule", "source": "agendamento"},
            {"name": "Purchase", "source": "venda"}
        ],
        "batch_size": 500,
        "match_keys": ["em", "ph", "fn", "ln"],
        "push_to_crm": True
    }
)
```

### Job 2: Análise Semanal (Segundas)

```python
scheduler.add_job(
    job_id="concessionaria_weekly_analysis",
    job_type="analysis",
    schedule_type="weekly",
    schedule_value="monday 09:00",
    params={
        "kpis": [
            "leads",
            "test_drives",
            "proposals",
            "sales",
            "cost_per_lead",
            "cost_per_test_drive",
            "cost_per_sale"
        ],
        "benchmarks": {
            "cpl_max": 80,  # Custo máximo por lead
            "cptd_max": 250, # Custo máximo por test drive
            "cps_max": 5000  # Custo máximo por venda
        }
    }
)
```

### Job 3: Otimização de Públicos (15 dias)

```python
scheduler.add_job(
    job_id="concessionaria_audience_opt",
    job_type="optimization",
    schedule_type="interval",
    schedule_value="15d",
    params={
        "rules": [
            {
                "type": "create_lookalike",
                "source": "leads_90days",
                "size": 5
            },
            {
                "type": "exclude_converted",
                "window": 180
            }
        ]
    }
)
```

### Job 4. Relatório Gerencial (Semanal)

```python
scheduler.add_job(
    job_id="concessionaria_weekly_report",
    job_type="report",
    schedule_type="weekly",
    schedule_value="friday 17:00",
    params={
        "report_type": "performance",
        "date_range": "last_7d",
        "format": "excel",
        "email": "gerencia@concessionaria.com",
        "custom_metrics": [
            "test_drive_rate",      # Taxa de conversão para test drive
            "proposal_rate",         # Taxa de conversão para proposta
            "sales_rate",           # Taxa de conversão para venda
            "average_ticket",       # Ticket médio
            "financing_rate"        # Taxa de financiamento
        ]
    }
)
```

## Métricas Específicas por Funil

### Topo de Funil (Awareness)
```yaml
metrics:
  - reach
  - frequency
  - impressions
  - cost_per_1k_people
benchmarks:
  - frequency: "> 2x"  # Mínimo 2x por pessoa
  - cpm: "< R$20"      # CPM máximo
```

### Meio de Funil (Consideração)
```yaml
metrics:
  - leads
  - cost_per_lead
  - lead_to_test_drive_rate
  - test_drive_completed
benchmarks:
  - cpl: "< R$80"
  - lead_to_td: "> 15%"
```

### Fundo de Funil (Conversão)
```yaml
metrics:
  - sales
  - cost_per_sale
  - roas
  - average_ticket
  - financing_rate
benchmarks:
  - cps: "< R$5000"
  - roas: "> 4x"
```

## Modelo de ROI/ROAS

### Cálculo para Concessionária:

```python
def calculate_dealership_roi(spend, sales_data):
    """
    Calcula ROI considerando:
    - Venda de veículos novos
    - Venda de veículos usados
    - Serviços e peças
    - Financiamento
    """
    # Ticket médio
    avg_ticket_new = sales_data.get('avg_ticket_new', 120000)
    avg_ticket_used = sales_data.get('avg_ticket_used', 70000)
    
    # Margem média (aproximada)
    margin_new = 0.08  # 8% margem em novos
    margin_used = 0.12  # 12% margem em usados
    
    # Conversões
    new_sales = sales_data.get('new_sales', 0)
    used_sales = sales_data.get('used_sales', 0)
    
    # Receita
    revenue_new = new_sales * avg_ticket_new * margin_new
    revenue_used = used_sales * avg_ticket_used * margin_used
    
    # Total
    total_revenue = revenue_new + revenue_used
    
    # ROI
    roi = (total_revenue / spend) * 100
    
    # ROAS
    roas = total_revenue / spend
    
    return {
        "total_revenue": total_revenue,
        "roi": roi,
        "roas": roas,
        "new_sales_revenue": revenue_new,
        "used_sales_revenue": revenue_used
    }

# Exemplo
result = calculate_dealership_roi(
    spend=10000,
    sales_data={
        'new_sales': 5,
        'used_sales': 3,
        'avg_ticket_new': 120000,
        'avg_ticket_used': 70000
    }
)

# Resultado:
# {
#   "total_revenue": 73200,  # R$73.200 de receita
#   "roi": 632,              # 632% ROI
#   "roas": 7.32,             # 7.32x ROAS
#   "new_sales_revenue": 48000,
#   "used_sales_revenue": 25200
# }
```

## Checklist de Implementação

### Setup Inicial

- [ ] Criar Pixel do Facebook
- [ ] Configurar eventos padrão (PageView, ViewContent, Lead)
- [ ] Configurar eventos customizados (TestDrive, Proposal)
- [ ] Criar conta de anúncios
- [ ] Configurar lista de clientes (CRM) para exclusão
- [ ] Definir janela de atribuição (90 dias)

### Integração CRM

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

### Automação

- [ ] Configurar job de upload offline (7dias)
- [ ] Configurar análise semanal
- [ ] Configurar relatório gerencial
- [ ] Testar Jobs

## Exemplo Completo - Implementação

```python
from core.memory import MemoryManager
from core.meta_api import MetaAPIClient
from scheduler.automation import AutomationScheduler
from analytics.engine import AnalyticsEngine

# Inicializar
memory = MemoryManager()
api = MetaAPIClient(
    access_token="EAA...",
    ad_account_id="act_123456789"
)
scheduler = AutomationScheduler(memory, api)

# ========== SETUP ==========

# Criar públicos
api.create_custom_audience(
    name="Visitantes 30 dias",
    rules={
        "inclusions": [{
            "rule": {
                "event": "PageView",
                "window": 30
            }
        }]
    }
)

# Criar lookalike
api.create_lookalike(
    source="leads_90days",
    size=5,
    country="BR"
)

# ========== CRON JOBS ==========

# 1. Upload de conversões offline (7dias)
scheduler.add_job(
    job_id="dealership_offline_conversion",
    job_type="offline_conversion",
    schedule_type="interval",
    schedule_value="7d",
    params={
        "pixel_id": "123456789",
        "events": ["Lead", "TestDrive", "Proposal", "Purchase"],
        "match_keys": ["em", "ph"],
        "batch_size": 500
    }
)

# 2. Análise semanal
scheduler.add_job(
    job_id="dealership_analysis",
    job_type="analysis",
    schedule_type="weekly",
    schedule_value="monday 09:00",
    params={
        "kpis": ["leads", "test_drives", "sales"],
        "benchmarks": {
            "cpl_max": 80,
            "cptd_max": 250,
            "cps_max": 5000
        }
    }
)

# 3. Relatório gerencial
scheduler.add_job(
    job_id="dealership_report",
    job_type="report",
    schedule_type="weekly",
    schedule_value="friday 17:00",
    params={
        "report_type": "performance",
        "format": "excel",
        "email": "gerencia@concessionaria.com"
    }
)

# Iniciar scheduler
scheduler.start()
```

## Troubleshooting

### Baixo Volume de Leads?

```yaml
diagnosis:
  - frequency_too_low: Aumente orçamento
  - audience_too_small: Expanda targeting
  - creative_not_converting: Teste novos criativos
  - offer_not_clear: Melhore copy e CTA

solution:
  - increase_budget: +50%
  - expand_location: Incluir cidades próximas
  - test_new_creatives: 3-5 variações
  - create_lookalike: 5-10%
```

### Custo por Lead Alto?

```yaml
diagnosis:
  - frequency_too_high: Reduza orçamento ou expanda público
  - wrong_audience: Revise targeting
  - poor_creative: Teste novos ângulos
  - seasonality: Considere sazonalidade

solution:
  - create_exclusions: Excluir já convertidos
  - test_different_formats: Vídeo vs Imagem
  - adjust_bidding: Lowest cost com cap
```

### Baixa Taxa de Test Drive?

```yaml
diagnosis:
  - leads_mal_qualificados: Melhore qualificação
  - follow_up_lento: Acelere contato
  - oferta_fraca: Melhore proposta

solution:
  - add_qualification: Perguntas no formulário
  - automate_follow_up: WhatsApp imediato
  - improve_offer: Melhores condições
```

## Licença

MIT License - ©2026 Monrars