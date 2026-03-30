# Agent de Campanhas - E-commerce

> Especializado em campanhas de e-commerce e lojas virtuais

**Versão:** 1.0.0  
**Vertical:** E-commerce  
**Autor:** Monrars (@monrars)

## Características do Vertical

### Jornada de Compra (Short Cycle)

```
Interesse → Pesquisa → Produto → Carrinho → Checkout → Compra → Pós-Venda
    ↓          ↓          ↓          ↓           ↓          ↓         ↓
   1-7dias   1-3dias    1dia      1hora       30min      5min     Contínuo
```

### Eventos e Timing

| Evento | Frequência | Importância | Offline? |
|--------|------------|-------------|----------|
| Page View | Muito Alta | Média | Não |
| View Content | Alta | Alta | Não |
| Add to Cart | Alta | Muito Alta | Não |
| Initiate Checkout | Média | Alta | Não |
| Add Payment Info | Baixa | Alta | Não |
| Purchase | Alta | Crítica | Não |
| Lead (contato) | Baixa | Média | Não |

### Diferenças vs Outros Verticais

| Aspecto | Concessionária | E-commerce |
|---------|---------------|------------|
| Ciclo de venda | 7-90 dias | **1-7 dias** |
| Ticket médio | R$50k-200k | **R$100-5000** |
| Volumetria | Baixa | **Muito Alta** |
| Conversão offline | Obrigatório | **Raro** |
| Atribuição | 90 dias | **7-30 dias** |
| Integrado com Pixel | Não | **Sim** |
| Real-time events | Não | **Sim** |

## Configurações Recomendadas

### 1. Janela de Atribuição

```yaml
attribution_window:
  click_through: 7     # dias (curto)
  view_through: 1      # dia
  conversion_window: 30 # dias máximo
```

### 2. Objetivos de Campanha

**Principais:**
- `CONVERSIONS` - Compras ( Purchase)
- `CATALOG_SALES` - Vendas de catálogo

**Secundários:**
- `TRAFFIC` - Tráfego para site
- `ADD_TO_CART` - Adicionar ao carrinho

### 3. Pixel Events

```javascript
// Eventos obrigatórios
fbq('track', 'PageView');
fbq('track', 'ViewContent', {
  content_ids: ['PRODUCT_123'],
  content_type: 'product',
  content_name: 'Smart TV 55"',
  content_category: 'Electronics',
  value: 2500,
  currency: 'BRL'
});

fbq('track', 'AddToCart', {
  content_ids: ['PRODUCT_123'],
  content_type: 'product',
  value: 2500,
  currency: 'BRL',
  num_items: 1
});

fbq('track', 'Purchase', {
  content_ids: ['PRODUCT_123', 'PRODUCT_456'],
  content_type: 'product',
  value: 3200,
  currency: 'BRL',
  num_items: 2
});
```

### 4. Catálogo de Produtos

```yaml
catalog:
  name: "Loja Virtual ABC"
  type: "PRODUCTS"
  feed:
    schedule: "daily"
    format: "CSV"
    fields:
      - id
      - title
      - description
      - availability
      - condition
      - price
      - link
      - image_link
      - brand
      - category
```

## Estratégias de Campanha

### 1. Topo de Funil (Descoberta)

**Objetivo:** `REACH` ou `VIDEO_VIEWS`

**Público:**
```yaml
targeting:
  interests:
    - "{categoria_produto}"
    - "{marca}"
    - "Compras online"
    - "Ofertas"
    - "Black Friday"
  behaviors:
    - "Engaged shoppers"
    - "Online buyers"
  age_min: 18
  age_max: 65
  locations:
    - "Brazil"
```

**Orçamento:** R$30-100/dia

**Criativo:**
- Vídeos de produto (15-30s)
- Carrosséis de ofertas
- Depoimentos de clientes
- Unboxing videos

### 2. Meio de Funil (Consideração)

**Objetivo:** `TRAFFIC` ou `ADD_TO_CART`

**Público:**
```yaml
targeting:
  custom_audiences:
    - "Visitantes Site (14 dias)"
    - "ViewContent (7 dias)"
    - "AddToCart (3 dias)"
  exclusions:
    - "Purchase (30 dias)"
```

**Orçamento:** R$50-150/dia

**Estratégia:**
- Remarketing de produtos visualizados
- Ofertas personalizadas
- Frete grátis destacado

### 3. Fundo de Funil (Conversão)

**Objetivo:** `CONVERSIONS` (Purchase)

**Público:**
```yaml
targeting:
  custom_audiences:
    - "AddToCart (1 dia)"
    - "InitiateCheckout (3 dias)"
    - "Abandoned Cart (7 dias)"
  exclusions:
    - "Purchase (30 dias)"
```

**Orçamento:** R$100-300/dia

**Estratégia:**
- Carrinho abandonado
- Cupom de desconto
- Frete grátis
- Despertar de urgência

### 4. Cross-sell / Up-sell

**Objetivo:** `CONVERSIONS`

**Público:**
```yaml
targeting:
  custom_audiences:
    - "Purchase (30-90 dias)"
  exclusions:
    - "Purchase (30 dias)"
```

**Estratégia:**
- Produtos complementares
- Versões premium
- Assinaturas

## Cron Jobs Específicos

### Job 1: Atualização de Catálogo (Diário)

```python
scheduler.add_job(
    job_id="ecommerce_catalog_update",
    job_type="catalog_update",
    schedule_type="daily",
    schedule_value="03:00",
    params={
        "catalog_id": "{CATALOG_ID}",
        "source": "erp",
        "fields": [
            "id",
            "title",
            "description",
            "availability",
            "price",
            "sale_price",
            "link",
            "image_link",
            "brand",
            "category"
        ]
    }
)
```

### Job 2: Sincronização de Pedidos (Hora em Hora)

```python
scheduler.add_job(
    job_id="ecommerce_order_sync",
    job_type="order_sync",
    schedule_type="interval",
    schedule_value="1h",
    params={
        "pixel_id": "{PIXEL_ID}",
        "events": ["Purchase"],
        "batch_size": 100,
        "match_keys": ["em"],
        "deduplication": True
    }
)
```

### Job 3: Auditoria de Produtos

```python
scheduler.add_job(
    job_id="ecommerce_product_audit",
    job_type="product_audit",
    schedule_type="weekly",
    schedule_value="monday 06:00",
    params={
        "check_availability": True,
        "check_images": True,
        "check_prices": True,
        "check_titles": True
    }
)
```

### Job 4. Campanha de Recuperação (4 horas)

```python
scheduler.add_job(
    job_id="ecommerce_cart_recovery",
    job_type="cart_recovery",
    schedule_type="interval",
    schedule_value="4h",
    params={
        "audience": "add_to_cart_24h",
        "creative_type": "dynamic",
        "offer_type": "free_shipping",
        "exclude_purchasers": True
    }
)
```

## Modelo de ROI/ROAS

### Cálculo para E-commerce:

```python
def calculate_ecommerce_roi(spend, sales_data):
    """
    Calcula ROI considerando:
    - Margem de produto
    - Taxa de devolução
    - Custo de envio
    - CAC (Custo de Aquisição de Cliente)
    """
    # Dados
    revenue = sales_data.get('revenue', 0)
    orders = sales_data.get('orders', 0)
    avg_margin = sales_data.get('avg_margin', 0.25)  # 25% margem média
    
    # Devoluções
    return_rate = sales_data.get('return_rate', 0.10)  # 10% devoluções
    returned_revenue = revenue * return_rate
    net_revenue = revenue - returned_revenue
    
    # Margem
    gross_profit = net_revenue * avg_margin
    
    # Custo de envio médio
    avg_shipping_cost = sales_data.get('avg_shipping_cost', 25)
    total_shipping = orders * avg_shipping_cost
    
    # Lucro bruto
    gross_profit_after_shipping = gross_profit - total_shipping
    
    # ROI e ROAS
    roi = ((gross_profit_after_shipping - spend) / spend) * 100 if spend > 0 else 0
    roas = net_revenue / spend if spend > 0 else 0
    
    # CAC
    cac = spend / orders if orders > 0 else 0
    
    # LTV (Lifetime Value) médio
    avg_ltv = sales_data.get('avg_ltv', 500)
    payback_ratio = avg_ltv / cac if cac > 0 else 0
    
    return {
        "net_revenue": round(net_revenue, 2),
        "gross_profit": round(gross_profit_after_shipping, 2),
        "roi_percentage": round(roi, 2),
        "roas": round(roas, 2),
        "cac": round(cac, 2),
        "ltv_cac_ratio": round(payback_ratio, 2),
        "orders": orders,
        "return_rate": return_rate
    }

# Exemplo
result = calculate_ecommerce_roi(
    spend=5000,
    sales_data={
        'revenue': 25000,
        'orders': 50,
        'avg_margin': 0.25,
        'return_rate': 0.10,
        'avg_shipping_cost': 25,
        'avg_ltv': 800
    }
)

# Resultado:
# {
#   "net_revenue": 22500,
#   "gross_profit": 4375,
#   "roi_percentage": -12.5,    # Prejuízo até atingir LTV
#   "roas": 4.5,
#   "cac": 100,
#   "ltv_cac_ratio": 8.0,       # 8x LTV/CAC
#   "orders": 50,
#   "return_rate": 0.10
# }
```

## Estratégias de Remarketing

### 1. Carrinho Abandonado(24h)

```yaml
campaign:
  name: "Carrinho Abandonado - 24h"
  objective: "CONVERSIONS"
  budget: 50
  
targeting:
  audience: "AddToCart - 24 horas"
  exclusions: "Purchase - 7 dias"
  
creative:
  type: "dynamic"
  template: "cart_abandonment"
  offer: "5% OFF + Frete grátis"
  
frequency:
  max: 3  # máximo 3x por dia
```

### 2. Navegação (7dias)

```yaml
campaign:
  name: "Remarketing Navegação - 7d"
  objective: "CONVERSIONS"
  budget: 30
  
targeting:
  audience: "ViewContent - 7 dias"
  exclusions: "Purchase - 30 dias"
  
creative:
  type: "dynamic"
  template: "product_view"
```

### 3. Buy Again (90 dias)

```yaml
campaign:
  name: "Recompra - 90dias"
  objective: "CONVERSIONS"
  budget: 40
  
targeting:
  audience: "Purchase - 90 dias"
  exclusions: "Purchase - 30 dias"
  
creative:
  type: "dynamic"
  template: "cross_sell"
  products: "complementary"
```

## DPA (Dynamic Product Ads)

### Configuração

```python
def setup_dpa_campaign(
    api,
    catalog_id: str,
    pixel_id: str,
    budget: int
):
    """
    Configura campanha DPA completa.
    
    Args:
        api: Cliente Meta API
        catalog_id: ID do catálogo
        pixel_id: ID do Pixel
        budget: Orçamento diário (centavos)
        
    Returns:
        Dict com IDs da campanha
    """
    # Criar público DPA
    audience = api.create_audience(
        name="DPA - Todos os visitantes",
        audience_type="custom",
        config={
            "rule": {
                "event": "ViewContent",
                "window": 30
            }
        }
    )
    
    # Criar campanha
    campaign = api.create_campaign(
        name="DPA - Retargeting",
        objective="CONVERSIONS",
        budget=budget,
        special_config={
            "promoted_object": {
                "pixel_id": pixel_id,
                "custom_event_type": "PURCHASE"
            },
            "bid_strategy": "LOWEST_COST_WITHOUT_CAP"
        }
    )
    
    # Criar adset com_template
    adset = api.create_adset(
        campaign_id=campaign["id"],
        name="DPA - Dynamic",
        targeting={
            "custom_audiences": [{"id": audience["id"]}],
            "exclusions": [{
                "id": pixel_id,
                "event": "Purchase",
                "window": 14
            }]
        },
        product_set_id=catalog_id,
        optimization_goal="OFFSITE_CONVERSIONS"
    )
    
    # Criar creative dinâmico
    creative = api.create_dynamic_creative(
        adset_id=adset["id"],
        catalog_id=catalog_id,
        template="product_grid",
        call_to_action="SHOP_NOW"
    )
    
    return {
        "campaign_id": campaign["id"],
        "adset_id": adset["id"],
        "creative_id": creative["id"],
        "audience_id": audience["id"]
    }
```

## Checklist de Implementação

### Setup Inicial

- [ ] Criar Pixel do Facebook
- [ ] Configurar eventos padrão (ViewContent, AddToCart, Purchase)
- [ ] Instalar Pixel no site
- [ ] Verificar eventos via Pixel Helper
- [ ] Criar catálogo de produtos
- [ ] Configurar feed de produtos
- [ ] Verificar dados do feed

### Campanhas

- [ ] Criar campanha de Awareness
- [ ] Criar campanha de Traffic
- [ ] Criar campanha de Conversões
- [ ] Criar público de carrinho abandonado
- [ ] Criar público de navegação
- [ ] Criar público de compradores
- [ ] Configurar DPA

### Automação

- [ ] Configurar sincronização de catálogo
- [ ] Configurar sincronização de pedidos
- [ ] Configurar jobs de recuperação
- [ ] Testar fluxo completo

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

# Criar catálogo
catalog = api.create_product_catalog(
    name="Loja Virtual ABC",
    vertical="HOME_LISTINGS"  # ou "RETAIL"
)

# Criar feed
feed = api.create_product_feed(
    catalog_id=catalog["id"],
    name="Feed de Produtos",
    schedule={"interval": "DAILY", "hour": 3}
)

# Setup DPA
dpa_setup = setup_dpa_campaign(
    api=api,
    catalog_id=catalog["id"],
    pixel_id="123456789",
    budget=10000  # R$100/dia
)

# ========== CRON JOBS ==========

# 1. Atualização de catálogo (diário)
scheduler.add_job(
    job_id="ecom_catalog_update",
    job_type="catalog_update",
    schedule_type="daily",
    schedule_value="03:00",
    params={
        "catalog_id": catalog["id"],
        "source": "erp"
    }
)

# 2. Sincronização de pedidos (hora em hora)
scheduler.add_job(
    job_id="ecom_order_sync",
    job_type="order_sync",
    schedule_type="interval",
    schedule_value="1h",
    params={
        "pixel_id": "123456789",
        "deduplication": True
    }
)

# 3. Auditoria de produtos (semanal)
scheduler.add_job(
    job_id="ecom_product_audit",
    job_type="product_audit",
    schedule_type="weekly",
    schedule_value="monday 06:00",
    params={
        "catalog_id": catalog["id"]
    }
)

# Iniciar scheduler
scheduler.start()

print("✅ Setup completo!")
print(f"Catalog ID: {catalog['id']}")
print(f"Feed ID: {feed['id']}")
print(f"Campaign ID: {dpa_setup['campaign_id']}")
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
  - frequency: "> 1.5x"
  - cpm: "< R$15"
  - video_completion_rate: "> 40%"
```

### Meio de Funil
```yaml
metrics:
  - link_clicks
  - cost_per_click
  - add_to_cart
  - cost_per_add_to_cart
  - initiate_checkout
benchmarks:
  - cpc: "< R$0.80"
  - cp_atc: "< R$8"
```

### Fundo de Funil
```yaml
metrics:
  - purchases
  - revenue
  - cost_per_purchase
  - roas
  - conversion_rate
benchmarks:
  - cpp: "< R$30"
  - roas: "> 3x"
  - cvr: "> 2%"
```

## Troubleshooting

### Baixa Taxa de Conversão?

```yaml
diagnosis:
  - pixel_issues: Verifique tracking
  - site_speed: Otimize carregamento
  - checkout_friction: Simplifique checkout
  - shipping_cost: Teste frete grátis

solution:
  - debug_pixel: Pixel Helper
  - optimize_images: Lazy loading
  - reduce_fields: Guest checkout
  - free_shipping: Acima de R$XX
```

### Alto Custo por Compra?

```yaml
diagnosis:
  - wrong_audience: Revise targeting
  - creative_fatigue: Teste novos criativos
  - competition_high: Teste horários
  - product_price: Compare com concorrentes

solution:
  - narrow_audience: Lookalike 3-5%
  - rotate_creatives: Semanal
  - off_hours: 18h-22h
  - dynamic_ads: DPA automatizado
```

### Carrinho Abandonado Alto?

```yaml
diagnosis:
  - shipping_price: Frete muito alto
  - payment_options: Poucas opções
  - checkout_long: Muitos passos
  - surprise_fees: Custos ocultos

solution:
  - free_shipping: Acima de R$150
  - pix_credit: +opções de pagamento
  - one_page_checkout: 1-2 passos
  - transparent: Preço final claro
```

## Licença

MIT License - © 2026 Monrars