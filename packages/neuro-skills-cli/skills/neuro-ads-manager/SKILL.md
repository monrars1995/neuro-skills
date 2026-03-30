# Neuro Ads Manager

> Gerenciador completo de Meta Ads com CRUD, Analytics, Automação e Integração API

**Autor:** Monrars (@monrars)  
**Versão:** 1.0.0  
**Plataforma:** Meta Ads (Facebook/Instagram)

## Descrição

Skill abrangente para gerenciamento completo de campanhas Meta Ads, integrando:

- **CRUD Completo** - Criar, ler, atualizar e deletar campanhas, ad sets, ads e creatives
- **Analytics/Relatórios** - Métricas, dashboards, análise de performance
- **Automação/Otimização** - Regras automáticas, escala, pausa por performance
- **Integração API** - Cliente completo para Meta Graph API v21.0

## Quando Usar

Use este skill quando precisar:

- Gerenciar campanhas Meta Ads de ponta a ponta
- Listar, criar, editar ou deletar campanhas
- Analisar performance com métricas detalhadas
- Implementar automações e regras
- Gerar relatórios e dashboards
- Otimizar campanhas com base em dados

## Capacidades

### 1. CRUD Completo

#### Campanhas

```
## Criar Campanha

Cria uma nova campanha com objetivo, orçamento e configurações.

**Parâmetros:**
- name: Nome da campanha
- objective: CONVERSIONS, TRAFFIC, AWARENESS, LEAD_GENERATION
- budget: Orçamento diário (em centavos)
- status: ACTIVE, PAUSED (default: PAUSED)
- special_ad_categories: Categorias especiais (se aplicável)

**Retorna:**
- campaign_id: ID da campanha criada

**Exemplo:**
```python
create_campaign(
    name="Black Friday 2024",
    objective="CONVERSIONS",
    budget=50000,  # R$500/dia
    status="PAUSED"
)
```

## Listar Campanhas

Lista todas as campanhas com filtros e paginação.

**Parâmetros:**
- status: Filtro por status (ACTIVE, PAUSED, ALL)
- limit: Limite de resultados (default: 25)
- after: Cursor para paginação

**Retorna:**
- Lista de campanhas com ID, nome, status, orçament

**Exemplo:**
```python
campaigns = list_campaigns(status="ACTIVE", limit=50)
for campaign in campaigns:
    print(f"{campaign['id']}: {campaign['name']} - {campaign['status']}")
```

## Atualizar Campanha

Atualiza configurações de uma campanha existente.

**Parâmetros:**
- campaign_id: ID da campanha
- name: Novo nome (opcional)
- status: Novo status (opcional)
- budget: Novo orçamento (opcional)

**Retorna:**
- success: True/False

**Exemplo:**
```python
update_campaign(
    campaign_id="123456789",
    name="Black Friday 2024 - Atualizada",
    status="ACTIVE"
)
```

## Deletar Campanha

Deleta uma campanha (move para archived).

**Parâmetros:**
- campaign_id: ID da campanha

**Retorna:**
- success: True/False

**Exemplo:**
```python
delete_campaign(campaign_id="123456789")
```

#### Ad Sets

```
## Criar Ad Set

Cria um conjunto de anúncios com targeting e orçamento.

**Parâmetros:**
- campaign_id: ID da campanha pai
- name: Nome do ad set
- daily_budget: Orçamento diário (centavos)
- targeting: Dict com targeting
- optimization_goal: CONVERSIONS, LINK_CLICKS, etc
- billing_event: IMPRESSIONS, LINK_CLICKS
- status: ACTIVE, PAUSED

**Targeting:**
```python
{
    "age_min": 25,
    "age_max": 55,
    "genders": ["male", "female"],
    "locations": ["BR"],
    "interests": ["fitness", "running"],
    "behaviors": ["engaged_shoppers"],
    "custom_audiences": ["123456789"],
    "lookalikes": ["987654321"]
}
```

**Exemplo:**
```python
create_ad_set(
    campaign_id="123456789",
    name="Black Friday - Homens 25-45",
    daily_budget=20000,
    targeting={
        "age_min": 25,
        "age_max": 45,
        "genders": ["male"],
        "locations": ["BR"]
    }
)
```

## Listar Ad Sets

Lista todos os ad sets de uma campanha.

**Parâmetros:**
- campaign_id: ID da campanha
- status: Filtro por status

**Retorna:**
- Lista de ad sets

## Atualizar Ad Set

Atualiza configurações de um ad set.

**Parâmetros:**
- adset_id: ID do ad set
- name: Novo nome (opcional)
- budget: Novo orçamento (opcional)
- targeting: Novo targeting (opcional)
- status: Novo status (opcional)

## Deletar Ad Set

Deleta um ad set.

#### Ads

```
## Criar Ad

Cria um anúncio com criativo e cópia.

**Parâmetros:**
- adset_id: ID do ad set
- name: Nome do ad
- creative_id: ID do criativo
- status: ACTIVE, PAUSED

**Exemplo:**
```python
create_ad(
    adset_id="123456789",
    name="Black Friday - Video 1",
    creative_id="987654321"
)
```

## Listar Ads

Lista todos os ads de um ad set.

**Parâmetros:**
- adset_id: ID do ad set
- status: Filtro por status

## Atualizar Ad

Atualiza configurações de um ad.

## Deletar Ad

Deleta um ad.

#### Creatives

```
## Criar Creative

Cria um criativo com vídeo ou imagem.

**Parâmetros:**
- name: Nome do criativo
- page_id: ID da página
- video_id: ID do vídeo (opcional)
- image_hash: Hash da imagem (opcional)
- message: Texto do anúncio
- headline: Título (opcional)
- link: URL de destino (opcional)
- call_to_action: CTA dict (opcional)

**Exemplo:**
```python
create_creative(
    name="Black Friday - Video 1",
    page_id="123456789",
    video_id="987654321",
    message="Aproveite as ofertas!",
    headline="Black Friday",
    call_to_action={"type": "SHOP_NOW"}
)
```

## Listar Creatives

Lista todos os criativos.

## Duplicar Creative

Duplica um criativo existente.

**Parâmetros:**
- creative_id: ID do criativo
- new_name: Novo nome (opcional)
```

### 2. Analytics/Relatórios

```
## Insights de Campanha

Obtém métricas detalhadas de uma campanha.

**Parâmetros:**
- campaign_id: ID da campanha
- date_range: today, last_7d, last_30d, lifetime
- metrics: Lista de métricas (opcional)

**Métricas Disponíveis:**
- spend: Gasto total
- impressions: Impressões
- clicks: Cliques
- cpc: Custo por clique
- cpm: Custo por mil impressões
- ctr: Taxa de cliques
- reach: Alcance
- frequency: Frequência
- actions: Ações (compras, leads, etc)
- cost_per_action_type: CPA por tipo
- conversions: Conversões (se pixel configurado)
- roas: ROAS (se pixel configurado)

**Exemplo:**
```python
insights = get_campaign_insights(
    campaign_id="123456789",
    date_range="last_7d",
    metrics=["spend", "impressions", "clicks", "cpc", "cpc"]
)
print(f"Gasto: R${insights['spend']}")
print(f"CPA: R${insights['cost_per_action_type']['purchase']}")
```

## Insights de Conta

Obtém métricas agregadas da conta.

**Parâmetros:**
- date_range: Período
- breakdown: Por dia, por campanha, etc

**Exemplo:**
```python
account_insights = get_account_insights(date_range="last_30d")
print(f"Gasto total: R${account_insights['spend']}")
print(f"Impressões: {account_insights['impressions']}")
```

## Relatório de Performance

Gera relatório completo com análise.

**Parâmetros:**
- date_range: Período
- group_by: day, campaign, adset, ad
- metrics: Métricas a incluir
- sort_by: Métrica para ordenar
- limit: Limite de resultados

**Retorna:**
- summary: Resumo executivo
- details: Dados detalhados
- charts: Configurações de gráficos
- recommendations: Recomendações automáticas

**Exemplo:**
```python
report = generate_performance_report(
    date_range="last_7d",
    group_by="campaign",
    metrics=["spend", "clicks", "cpa", "roas"],
    sort_by="spend",
    limit=10
)

print(f"Total gasto: {report['summary']['total_spend']}")
print(f"Melhor campanha: {report['details'][0]['name']}")
print(f"CPA médio: {report['summary']['avg_cpa']}")
```

## Dashboard Real-time

Gera dashboard com métricas em tempo real.

**Parâmetros:**
- refresh_interval: Intervalo de atualização (segundos)
- campaigns: Lista de campanhas (opcional)

**Retorna:**
- Métricas atualizadas
- Status de cada campanha
- Alertas automáticos

## Exportar Relatório

Exporta relatório em formato específico.

**Parâmetros:**
- report_type: Tipo de relatório
- format: CSV, Excel, PDF
- date_range: Período
- email: Email para envio (opcional)

**Exemplo:**
```python
export_report(
    report_type="performance",
    format="excel",
    date_range="last_30d",
    email="analytics@company.com"
)
```

### 3. Automação/Otimização

```
## Regras Automáticas

Cria regras de automação para campanhas.

**Tipos de Regras:**
1. **Pausar por CPA Alto**
   ```python
   create_rule(
       name="Pausar CPA Alto",
       trigger="cpa > 50",
       action="pause_campaign",
       campaigns=["123", "456"]
   )
   ```

2. **Escalar por ROAS**
   ```python
   create_rule(
       name="Escalar ROAS Alto",
       trigger="roas > 3",
       action="increase_budget",
       params={"percentage": 20},
       campaigns=["123"]
   )
   ```

3. **Pausar por CTR Baixo**
   ```python
   create_rule(
       name="Pausar CTR Baixo",
       trigger="ctr < 0.5",
       action="pause_ad",
       campaigns=["123"]
   )
   ```

4. **Notificar por Spend Alto**
   ```python
   create_rule(
       name="Alerta Spend",
       trigger="spend > 1000",
       action="send_notification",
       params={"email": "alerts@company.com"}
   )
   ```

## Listar Regras

Lista todas as regras de automação.

**Parâmetros:**
- status: Filtro por status (active, paused)

## Atualizar Regra

Atualiza uma regra existente.

**Parâmetros:**
- rule_id: ID da regra
- Novos parâmetros

## Deletar Regra

Deleta uma regra.

## Executar Regras

Executa todas as regras ativas manualmente.

**Retorna:**
- Regras executadas
- Ações tomadas
- Erros encontrados

## Otimização Automática

Aplica otimizações baseadas em dados.

**Estratégias:**

1. **Orçamento por Performance**
   ```python
   # Redistribui orçamento para melhores campanhas
   optimize_budget_allocation(
       campaigns=["123", "456", "789"],
       metric="roas",
       target_avg=2.5
   )
   ```

2. **Creative Rotation**
   ```python
   # Rotaciona criativos por performance
   rotate_creatives(
       adset_id="123",
       metric="ctr",
       top_n=3
   )
   ```

3. **Audience Expansion**
   ```python
   # Expande públicos com boa performance
   expand_audiences(
       campaign_id="123",
       lookalike_size=5
   )
   ```

4. **Bid Optimization**
   ```python
   # Otimiza lances automaticamente
   optimize_bids(
       campaigns=["123"],
       strategy="lowest_cost"
   )
   ```

## Agendar Automação

Agenda execuções automáticas.

**Parâmetros:**
- automation: Nome da automação
- schedule: Cron expression
- params: Parâmetros

**Exemplos:**
```python
# Executar regras diariamente às 9h
schedule_automation(
    automation="run_rules",
    schedule="0 9 * * *"
)

# Relatório semanal às segundas
schedule_automation(
    automation="generate_report",
    schedule="0 9 * * 1",
    params={"format": "excel", "email": "reports@company.com"}
)
```

### 4. Integração API

```
## Inicialização

```python
from neuro_ads_manager import NeuroAdsManager

# Inicializar com credenciais
client = NeuroAdsManager(
    access_token="EAA...",
    ad_account_id="act_123456789",
    app_id="123456789",  # Opcional
    app_secret="abc123"   # Opcional
)
```

## Testar Conexão

```python
# Testar se as credenciais funcionam
result = client.test_connection()
if result['success']:
    print(f"Conectado como: {result['user_name']}")
else:
    print(f"Erro: {result['error']}")
```

## Rate Limiting

O cliente gerencia automaticamente o rate limiting da API:

- Respeita limites do Meta (calls/hour, calls/day)
- Implementa backoff exponencial em caso de erro 429
- Retry automático para erros temporários

## Paginação

Métodos de listagem suportam paginação:

```python
# Listar com paginação
campaigns = client.list_campaigns(limit=10)

# Próxima página
next_page = client.list_campaigns(
    limit=10,
    after=campaigns['paging']['cursors']['after']
)
```

## Tratamento de Erros

```python
try:
    campaign = client.create_campaign(name="Teste")
except NeuroAdsError as e:
    print(f"Erro: {e.message}")
    print(f"Código: {e.code}")
    print(f"Subcódigo: {e.subcode}")
```

## Webhooks

Registra webhooks para eventos:

```python
# Registrar webhook
client.register_webhook(
    event="campaign.status_changed",
    url="https://seusite.com/webhook",
    verify_token="secret123"
)

# Eventos disponíveis:
# - campaign.status_changed
# - ad.rejected
# - adset.budget_exhausted
# - insight.updated
```

## Batch Operations

Executa múltiplas operações em batch:

```python
# Criar múltiplas campanhas
operations = [
    {"method": "POST", "path": "campaigns", "body": {"name": "Camp 1"}},
    {"method": "POST", "path": "campaigns", "body": {"name": "Camp 2"}},
    {"method": "POST", "path": "campaigns", "body": {"name": "Camp 3"}}
]

results = client.batch_request(operations)
```

## Insights Avançados

```python
# Insights com breakdown
insights = client.get_insights(
    object_id="123456789",
    level="campaign",
    date_range="last_30d",
    breakdowns=["age", "gender", "country"],
    metrics=["spend", "clicks", "actions"]
)

# Insights com filtering
insights = client.get_insights(
    object_id="123456789",
    level="ad",
    filtering=[{"field": "ad.status", "operator": "IN", "value": ["ACTIVE"]}]
)
```
```

## Integração com Outros Skills

### Com traffic-strategist

```python
# Analisar briefing
briefing_analysis = traffic_strategist.analyze_briefing(briefing_text)

# Preparar dados para criação
campaign_data = neuro_ads_manager.prepare_campaign_data(briefing_analysis)

# Criar campanha
campaign = neuro_ads_manager.create_campaign(**campaign_data)
```

### Com ad-copywriter

```python
# Gerar cópias
copies = ad_copywriter.generate_copy(
    briefing=briefing,
    brand_voice=brand_voice,
    num_variants=3
)

# Criar criativos para cada cópia
for copy in copies:
    creative = neuro_ads_manager.create_creative(
        name=copy['name'],
        video_id=video_id,
        message=copy['primary_text'],
        headline=copy['headline'],
        call_to_action={"type": copy['cta']}
    )
```

### Com meta-ads-manager

```python
# Usar funções específicas do meta-ads-manager
account_info = meta_ads_manager.get_ad_account_info()
pixels = meta_ads_manager.list_pixels()
pages = meta_ads_manager.list_pages()

# Passar IDs para neuro-ads-manager
campaign = neuro_ads_manager.create_campaign(
    name="Teste",
    pixel_id=pixels[0]['id'],
    page_id=pages[0]['id']
)
```

## Memória e Persistência

O skill mantém histórico e configurações:

```python
# Salvar credenciais
client.save_credentials(account_name="conta_principal")

# Carregar credenciais
client.load_credentials(account_name="conta_principal")

# Histórico de operações
history = client.get_operation_history(limit=100)

# Cache de insights
cached = client.get_cached_insights(campaign_id, max_age=3600)
```

## Boas Práticas

1. **Sempre inicie com status PAUSED**
   ```python
   campaign = create_campaign(name="Teste", status="PAUSED")
   ```

2. **Valide targeting antes de criar**
   ```python
   is_valid = validate_targeting(targeting_dict)
   ```

3. **Use batch para múltiplas operações**
   ```python
   # Em vez de:
   for ad in ads:
       create_ad(**ad)
   
   # Use:
   batch_create_ads(ads)
   ```

4. **Monitore rate limits**
   ```python
   usage = client.get_rate_limit_usage()
   if usage['calls_remaining'] < 100:
       time.sleep(60)
   ```

5. **Implemente retry logic**
   ```python
   @retry(max_attempts=3, backoff=exponential)
   def create_campaign_with_retry(**kwargs):
       return create_campaign(**kwargs)
   ```

## Exemplos Completos

### Criar Campanha Completa

```python
# Inicializar
client = NeuroAdsManager(
    access_token="EAA...",
    ad_account_id="act_123456789"
)

# 1. Upload de vídeo
video = client.upload_video(Path("video.mp4"))
video_id = video['video_id']

# 2. Criar campanha
campaign = client.create_campaign(
    name="Black Friday 2024",
    objective="CONVERSIONS",
    budget=50000,
    status="PAUSED"
)

# 3. Criar ad set
adset = client.create_ad_set(
    campaign_id=campaign['id'],
    name="Black Friday - Público 1",
    daily_budget=20000,
    targeting={
        "age_min": 25,
        "age_max": 45,
        "genders": ["male"],
        "locations": ["BR"],
        "interests": ["fitness", "running"]
    }
)

# 4. Criar creative
creative = client.create_creative(
    name="Black Friday - Video 1",
    page_id="123456789",
    video_id=video_id,
    message="Aproveite as ofertas!",
    call_to_action={"type": "SHOP_NOW"}
)

# 5. Criar ad
ad = client.create_ad(
    adset_id=adset['id'],
    name="Black Friday - Ad 1",
    creative_id=creative['id']
)

# 6. Ativar campanha
client.update_campaign(
    campaign_id=campaign['id'],
    status="ACTIVE"
)

print(f"Campanha criada: {campaign['id']}")
```

### Dashboard de Performance

```python
# Obter insights de todas as campanhas ativas
campaigns = client.list_campaigns(status="ACTIVE")

data = []
for campaign in campaigns:
    insights = client.get_campaign_insights(
        campaign_id=campaign['id'],
        date_range="last_7d"
    )
    data.append({
        'name': campaign['name'],
        'spend': insights['spend'],
        'clicks': insights['clicks'],
        'cpa': insights['cost_per_action_type'].get('purchase', 0),
        'roas': insights.get('purchase_roas', 0)
    })

# Ordenar por ROAS
data.sort(key=lambda x: x['roas'], reverse=True)

# Exibir
for row in data:
    print(f"{row['name']}: R${row['spend']} | CPA: R${row['cpa']} | ROAS: {row['roas']}x")
```

### Automação de Escala

```python
# Regra: Escalar campanhas com ROAS > 3
def scale_high_performers():
    campaigns = client.list_campaigns(status="ACTIVE")
    
    for campaign in campaigns:
        insights = client.get_campaign_insights(
            campaign_id=campaign['id'],
            date_range="last_3d"
        )
        
        roas = insights.get('purchase_roas', 0)
        
        if roas > 3:
            # Aumentar orçamento em 20%
            current_budget = campaign['daily_budget']
            new_budget = int(current_budget * 1.2)
            
            client.update_campaign(
                campaign_id=campaign['id'],
                budget=new_budget
            )
            print(f"Escalado {campaign['name']}: R${current_budget/100} -> R${new_budget/100}")

# Executar
scale_high_performers()
```

## Troubleshooting

### Erro: "Invalid OAuth 2.0 Access Token"

**Causa:** Token expirado ou inválido  
**Solução:** Renovar token via OAuth

### Erro: "Rate Limit Exceeded"

**Causa:** Limite de chamadas da API atingido  
**Solução:** Aguardar ou implementar retry com backoff

### Erro: "Creative was disapproved"

**Causa:** Criativo violou políticas do Meta  
**Solução:** Verificar políticas e ajustar conteúdo

### Erro: "Insufficient permissions"

**Causa:** Permissões insuficientes do token  
**Solução:** Solicitar permissões necessárias

## Paginação de Erros

| Código | Descrição | Solução |
|--------|-----------|---------|
| 1 | API temporary unavailable | Retry em alguns segundos |
| 2 | Temporary send error | Retry em alguns segundos |
| 4 | API session expired | Reautenticar |
| 10 | Permission denied | Verificar permissões |
| 17 | Rate limit exceeded | Aguardar ou reduzir frequência |
| 100 | Invalid parameter | Verificar parâmetros |
| 200 | Missing permissions | Solicitar permissões |

## Licença

MIT License - ©2026 Monrars

## Autor

**Monrars**  
Instagram: [@monrars](https://instagram.com/monrars)  
GitHub: [github.com/monrars1995/neuro-skills](https://github.com/monrars1995/neuro-skills)