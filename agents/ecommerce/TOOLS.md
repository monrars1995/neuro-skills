# Ferramentas - Agent E-commerce

> API Reference e implementações para campanhas de e-commerce

## Índice

1. [Core API](#core-api)
2. [Product Catalog](#product-catalog)
3. [DPA (Dynamic Product Ads)](#dpa-dynamic-product-ads)
4. [Pixel Events](#pixel-events)
5. [Scheduler Jobs](#scheduler-jobs)

---

## Core API

### ecommerce.create_campaign()

Cria uma campanha otimizada para e-commerce.

```python
def create_campaign(
    self,
    name: str,
    objective: str,  # 'CONVERSIONS', 'CATALOG_SALES', 'TRAFFIC'
    budget: int,  # em centavos
    pixel_id: str,
    catalog_id: Optional[str] = None,
    special_config: Optional[Dict] = None
) -> Dict:
    """
    Cria campanha com configurações específicas para e-commerce.
    
    Args:
        name: Nome da campanha
        objective: Objetivo da campanha
        budget: Orçamento diário em centavos
        pixel_id: ID do Pixel
        catalog_id: ID do catálogo (para DPA)
        special_config: Configurações especiais
        
    Returns:
        Dict com campaign_id, adset_id, creative_ids
        
    Example:
        >>> campaign = api.create_campaign(
        ...     name="Black Friday 2024 - ROUPAS",
        ...     objective="CONVERSIONS",
        ...     budget=50000,  # R$500/dia
        ...     pixel_id="123456789",
        ...     catalog_id="987654321",
        ...     special_config={
        ...         "attribution_window": 7,
        ...         "optimization_goal": "OFFSITE_CONVERSIONS",
        ...         "conversion_event": "Purchase"
        ...     }
        ... )
    """
    # Configurações padrão para e-commerce
    default_config = {
        "attribution_spec": [
            {"event_type": "conversion", "window_days": 7}
        ],
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
        "optimization_goal": "OFFSITE_CONVERSIONS",
        "promoted_object": {
            "pixel_id": pixel_id,
            "custom_event_type": "PURCHASE"
        }
    }
    
    # Adicionar catálogo se for DPA
    if catalog_id:
        default_config["promoted_object"]["product_set_id"] = catalog_id
    
    # Merge com configurações especiais
    if special_config:
        default_config.update(special_config)
    
    # Criar campanha
    campaign = self._request(
        method="POST",
        endpoint=f"{self.ad_account_id}/campaigns",
        data={
            "name": name,
            "objective": objective,
            "status": "PAUSED",
            "special_ad_category": "NONE",
            "bid_strategy": default_config["bid_strategy"],
            "promoted_object": default_config["promoted_object"]
        }
    )
    
    return campaign
```

### ecommerce.create_dpa_adset()

Cria adset para Dynamic Product Ads.

```python
def create_dpa_adset(
    self,
    campaign_id: str,
    name: str,
    catalog_id: str,
    pixel_id: str,
    budget: int,
    targeting: Optional[Dict] = None
) -> Dict:
    """
    Cria adset para DPA com targeting dinâmico.
    
    Args:
        campaign_id: ID da campanha
        name: Nome do adset
        catalog_id: ID do catálogo
        pixel_id: ID do Pixel
        budget: Orçamento diário em centavos
        targeting: Targeting personalizado
        
    Returns:
        Dict com adset_id
        
    Example:
        >>> adset = api.create_dpa_adset(
        ...     campaign_id="123456789",
        ...     name="DPA - Retargeting 7 dias",
        ...     catalog_id="987654321",
        ...     pixel_id="123456789",
        ...     budget=10000,  # R$100/dia
        ...     targeting={
        ...         "event": "ViewContent",
        ...         "window": 7,
        ...         "exclusions": ["Purchase"]
        ...     }
        ... )
    """
    # Targeting padrão (retargeting)
    if not targeting:
        targeting = {
            "event": "ViewContent",
            "window": 7,
            "exclusions": ["Purchase"]
        }
    
    # Criar público dinâmico
    adset = self._request(
        method="POST",
        endpoint=f"{self.ad_account_id}/adsets",
        data={
            "name": name,
            "campaign_id": campaign_id,
            "daily_budget": budget,
            "optimization_goal": "OFFSITE_CONVERSIONS",
            "billing_event": "IMPRESSIONS",
            "promoted_object": {
                "pixel_id": pixel_id,
                "custom_event_type": "PURCHASE",
                "product_set_id": catalog_id
            },
            "targeting": {
                "dynamic_audience_ids": [
                    {
                        "event_sources": [{"id": pixel_id, "type": "pixel"}],
                        "retention_seconds": targeting["window"] * 86400,
                        "rule": {"event": {"eq": targeting["event"]}},
                        "exclusions": [
                            {"event_sources": [{"id": pixel_id}], "retention_seconds": 2592000, "rule": {"event": {"eq": "Purchase"}}}
                        ]
                    }
                ]
            }
        }
    )
    
    return adset
```

---

## Product Catalog

### catalog.create_product_catalog()

Cria catálogo de produtos.

```python
def create_product_catalog(
    self,
    name: str,
    vertical: str = "PRODUCTS"
) -> Dict:
    """
    Cria catálogo de produtos para DPA.
    
    Args:
        name: Nome do catálogo
        vertical: Vertical do catálogo
        
    Returns:
        Dict com catalog_id
        
    Example:
        >>> catalog = api.create_product_catalog(
        ...     name="Loja Virtual ABC",
        ...     vertical="PRODUCTS"
        ... )
    """
    catalog = self._request(
        method="POST",
        endpoint=f"{self.business_id}/product_catalogs",
        data={
            "name": name,
            "vertical": vertical
        }
    )
    
    return catalog
```

### catalog.create_product_feed()

Cria feed de produtos.

```python
def create_product_feed(
    self,
    catalog_id: str,
    name: str,
    schedule: Dict,
    delimiter: str = "COMMA",
    encoding: str = "UTF-8"
) -> Dict:
    """
    Cria feed de produtos com agendamento.
    
    Args:
        catalog_id: ID do catálogo
        name: Nome do feed
        schedule: Agendamento de atualização
        delimiter: Delimitador do CSV
        encoding: Codificação do arquivo
        
    Returns:
        Dict com feed_id
        
    Example:
        >>> feed = api.create_product_feed(
        ...     catalog_id="123456789",
        ...     name="Feed de Produtos",
        ...     schedule={"interval": "DAILY", "hour": 3},
        ...     delimiter="COMMA",
        ...     encoding="UTF-8"
        ... )
    """
    feed = self._request(
        method="POST",
        endpoint=f"{catalog_id}/product_feeds",
        data={
            "name": name,
            "schedule": schedule,
            "delimiter": delimiter,
            "encoding": encoding
        }
    )
    
    return feed
```

### catalog.upload_products()

Faz upload de produtos para o catálogo.

```python
def upload_products_batch(
    self,
    catalog_id: str,
    products: List[Dict],
    batch_size: int = 50
) -> Dict:
    """
    Faz upload de produtos em lote.
    
    Args:
        catalog_id: ID do catálogo
        products: Lista de produtos
        batch_size: Tamanho do lote (máx 50)
        
    Returns:
        Dict com handles dos uploads
        
    Example:
        >>> products = [
        ...     {
        ...         "id": "PROD_123",
        ...         "title": "Smart TV 55\"",
        ...         "description": "Smart TV 4K com Netflix",
        ...         "availability": "in_stock",
        ...         "condition": "new",
        ...         "price": "250000 BRL",  # R$2.500,00
        ...         "sale_price": "220000 BRL",  # R$2.200,00
        ...         "link": "https://loja.com/produto/123",
        ...         "image_link": "https://loja.com/img/123.jpg",
        ...         "brand": "Samsung",
        ...         "category": "Eletrônicos > TVs",
        ...         "gtin": "1234567890123",
        ...         "mpn": "TV55SAMSUNG",
        ...         "additional_image_links": [
        ...             "https://loja.com/img/123-2.jpg",
        ...             "https://loja.com/img/123-3.jpg"
        ...         ]
        ...     }
        ... ]
        >>> result = api.upload_products_batch(
        ...     catalog_id="123456789",
        ...     products=products
        ... )
    """
    # Processar em lotes de 50 (limite da API)
    batches = [products[i:i+batch_size] for i in range(0, len(products), batch_size)]
    
    handles = []
    for batch in batches:
        # Preparar dados
        data = {
            "requests": [
                {
                    "method": "POST",
                    "retailer_id": product["id"],
                    "data": product
                }
                for product in batch
            ]
        }
        
        # Enviar
        response = self._request(
            method="POST",
            endpoint=f"{catalog_id}/batch",
            data=data
        )
        
        handles.append(response.get("handles", []))
    
    return {
        "total": len(products),
        "batches": len(batches),
        "handles": handles
    }
```

### catalog.validate_feed()

Valida feed de produtos.

```python
def validate_product_feed(
    self,
    feed_id: str
) -> Dict:
    """
    Valida feed de produtos e retorna erros.
    
    Args:
        feed_id: ID do feed
        
    Returns:
        Dict com estatísticas de validação
        
    Example:
        >>> validation = api.validate_product_feed(
        ...     feed_id="123456789"
        ... )
        >>> if validation["errors"]:
        ...     print(f"Encontrados {len(validation['errors'])} erros")
    """
    validation = self._request(
        method="GET",
        endpoint=f"{feed_id}/validation",
        params={
            "fields": "errors,warnings,stats"
        }
    )
    
    return {
        "feed_id": feed_id,
        "errors": validation.get("errors", []),
        "warnings": validation.get("warnings", []),
        "stats": validation.get("stats", {}),
        "valid": len(validation.get("errors", [])) == 0
    }
```

---

## DPA (Dynamic Product Ads)

### dpa.create_dpa_campaign()

Cria campanha DPA completa.

```python
def create_dpa_campaign(
    self,
    name: str,
    catalog_id: str,
    pixel_id: str,
    budget: int,
    targeting_type: str = "retargeting"
) -> Dict:
    """
    Cria campanha DPA completa com adset e creative.
    
    Args:
        name: Nome da campanha
        catalog_id: ID do catálogo
        pixel_id: ID do Pixel
        budget: Orçamento diário em centavos
        targeting_type: Tipo de targeting (retargeting, prospecting, cross-sell)
        
    Returns:
        Dict com campaign_id, adset_id, creative_id
        
    Example:
        >>> dpa = api.create_dpa_campaign(
        ...     name="DPA - Retargeting 7d",
        ...     catalog_id="123456789",
        ...     pixel_id="987654321",
        ...     budget=15000,  # R$150/dia
        ...     targeting_type="retargeting"
        ... )
    """
    # Criar campanha
    campaign = self.create_campaign(
        name=name,
        objective="CATALOG_SALES",
        budget=budget,
        pixel_id=pixel_id,
        catalog_id=catalog_id,
        special_config={
            "attribution_window": 7,
            "optimization_goal": "OFFSITE_CONVERSIONS",
            "conversion_event": "Purchase"
        }
    )
    
    # Criar adset
    adset = self.create_dpa_adset(
        campaign_id=campaign["id"],
        name=f"{name} - AdSet",
        catalog_id=catalog_id,
        pixel_id=pixel_id,
        budget=budget
    )
    
    # Criar creative dinâmico
    creative = self.create_dynamic_creative(
        adset_id=adset["id"],
        catalog_id=catalog_id,
        template="product_grid",
        call_to_action="SHOP_NOW"
    )
    
    return {
        "campaign_id": campaign["id"],
        "adset_id": adset["id"],
        "creative_id": creative["id"]
    }
```

### dpa.create_dynamic_creative()

Cria creative dinâmico para DPA.

```python
def create_dynamic_creative(
    self,
    adset_id: str,
    catalog_id: str,
    template: str = "product_grid",
    call_to_action: str = "SHOP_NOW"
) -> Dict:
    """
    Cria creative dinâmico para DPA.
    
    Args:
        adset_id: ID do adset
        catalog_id: ID do catálogo
        template: Template do creative
        call_to_action: Call to action
        
    Returns:
        Dict com creative_id
        
    Example:
        >>> creative = api.create_dynamic_creative(
        ...     adset_id="123456789",
        ...     catalog_id="987654321",
        ...     template="product_grid",
        ...     call_to_action="SHOP_NOW"
        ... )
    """
    # Templates disponíveis
    templates = {
        "product_grid": {
            "format": "carousel",
            "max_items": 5
        },
        "single_image": {
            "format": "image",
            "max_items": 1
        },
        "collection": {
            "format": "collection",
            "max_items": 4
        }
    }
    
    template_config = templates.get(template, templates["product_grid"])
    
    # Criar creative
    creative = self._request(
        method="POST",
        endpoint=f"{self.ad_account_id}/adcreatives",
        data={
            "name": f"DPA Creative - {template}",
            "object_story_spec": {
                "page_id": self.page_id,
                "template_data": {
                    "call_to_action": {"type": call_to_action},
                    "child_attachments": [
                        {
                            "link": "{{product.link}}",
                            "name": "{{product.name}}",
                            "description": "{{product.description}}",
                            "image_hash": "{{product.image_hash}}"
                        }
                    ]
                }
            },
            "product_set_id": catalog_id
        }
    )
    
    # Criar ad
    ad = self._request(
        method="POST",
        endpoint=f"{adset_id}/ads",
        data={
            "name": f"DPA Ad - {template}",
            "adset_id": adset_id,
            "creative": {"creative_id": creative["id"]}
        }
    )
    
    return creative
```

---

## Pixel Events

### pixel.setup_ecommerce_events()

Configura eventos de e-commerce no site.

```python
def get_ecommerce_pixel_code(
    self,
    pixel_id: str,
    currency: str = "BRL"
) -> str:
    """
    Retorna código de Pixel para e-commerce.
    
    Args:
        pixel_id: ID do Pixel
        currency: Moeda padrão
        
    Returns:
        String com código JavaScript
        
    Example:
        >>> code = api.get_ecommerce_pixel_code(
        ...     pixel_id="123456789",
        ...     currency="BRL"
        ... )
        >>> print(code)  # Código para adicionar no site
    """
    code = f"""
<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '{pixel_id}');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id={pixel_id}&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->

<!-- E-commerce Events -->
<script>
// ViewContent - Visualização de produto
function trackViewContent(product) {{
    fbq('track', 'ViewContent', {{
        content_ids: [product.id],
        content_type: 'product',
        content_name: product.name,
        content_category: product.category,
        value: product.price,
        currency: '{currency}'
    }});
}}

// AddToCart - Adicionar ao carrinho
function trackAddToCart(product, quantity) {{
    fbq('track', 'AddToCart', {{
        content_ids: [product.id],
        content_type: 'product',
        value: product.price * quantity,
        currency: '{currency}',
        num_items: quantity
    }});
}}

// InitiateCheckout - Iniciar checkout
function trackInitiateCheckout(cart) {{
    fbq('track', 'InitiateCheckout', {{
        content_ids: cart.products.map(p => p.id),
        content_type: 'product',
        value: cart.total,
        currency: '{currency}',
        num_items: cart.products.length
    }});
}}

// Purchase - Compra finalizada
function trackPurchase(order) {{
    fbq('track', 'Purchase', {{
        content_ids: order.products.map(p => p.id),
        content_type: 'product',
        value: order.total,
        currency: '{currency}',
        num_items: order.products.length
    }});
}}

// AddPaymentInfo - Adicionar informação de pagamento
function trackAddPaymentInfo(paymentMethod) {{
    fbq('track', 'AddPaymentInfo', {{
        payment_method: paymentMethod
    }});
}}
</script>
"""
    return code
```

---

## Scheduler Jobs

### scheduler.add_catalog_sync()

Adiciona job de sincronização de catálogo.

```python
def add_catalog_sync_job(
    self,
    catalog_id: str,
    feed_id: str,
    schedule_type: str = "daily",
    schedule_value: str = "03:00"
) -> Dict:
    """
    Adiciona job de sincronização de catálogo.
    
    Args:
        catalog_id: ID do catálogo
        feed_id: ID do feed
        schedule_type: Tipo de agendamento
        schedule_value: Valor do agendamento
        
    Returns:
        Dict com job_id
    """
    job_id = f"ecom_catalog_sync_{catalog_id}"
    
    self.add_job(
        job_id=job_id,
        job_type="catalog_sync",
        schedule_type=schedule_type,
        schedule_value=schedule_value,
        params={
            "catalog_id": catalog_id,
            "feed_id": feed_id
        }
    )
    
    return {"job_id": job_id, "schedule": f"{schedule_type}: {schedule_value}"}
```

### scheduler.add_order_sync()

Adiciona job de sincronização de pedidos.

```python
def add_order_sync_job(
    self,
    pixel_id: str,
    schedule_type: str = "interval",
    schedule_value: str = "1h",
    deduplication: bool = True
) -> Dict:
    """
    Adiciona job de sincronização de pedidos com deduplicação.
    
    Args:
        pixel_id: ID do Pixel
        schedule_type: Tipo de agendamento
        schedule_value: Valor do agendamento
        deduplication: Habilitar deduplicação de eventos
        
    Returns:
        Dict com job_id
    """
    job_id = f"ecom_order_sync_{pixel_id}"
    
    self.add_job(
        job_id=job_id,
        job_type="order_sync",
        schedule_type=schedule_type,
        schedule_value=schedule_value,
        params={
            "pixel_id": pixel_id,
            "deduplication": deduplication,
            "events": ["Purchase", "AddToCart", "InitiateCheckout"]
        }
    )
    
    return {"job_id": job_id, "schedule": f"{schedule_type}: {schedule_value}"}
```

### scheduler.add_abandoned_cart()

Adiciona job de recuperação de carrinho abandonado.

```python
def add_abandoned_cart_job(
    self,
    pixel_id: str,
    schedule_type: str = "interval",
    schedule_value: str = "4h",
    offer_type: str = "free_shipping"
) -> Dict:
    """
    Adiciona job de recuperação de carrinho abandonado.
    
    Args:
        pixel_id: ID do Pixel
        schedule_type: Tipo de agendamento
        schedule_value: Valor do agendamento
        offer_type: Tipo de oferta (free_shipping, discount, coupon)
        
    Returns:
        Dict com job_id
    """
    job_id = f"ecom_abandoned_cart_{pixel_id}"
    
    self.add_job(
        job_id=job_id,
        job_type="cart_recovery",
        schedule_type=schedule_type,
        schedule_value=schedule_value,
        params={
            "pixel_id": pixel_id,
            "audience": "add_to_cart_24h",
            "exclusions": ["Purchase_7d"],
            "offer_type": offer_type,
            "creative_type": "dynamic"
        }
    )
    
    return {"job_id": job_id, "schedule": f"{schedule_type}: {schedule_value}"}
```

---

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
    vertical="PRODUCTS"
)

# Criar feed
feed = api.create_product_feed(
    catalog_id=catalog["id"],
    name="Feed de Produtos",
    schedule={"interval": "DAILY", "hour": 3}
)

# Upload de produtos
products = [
    {
        "id": "PROD_123",
        "title": "Smart TV 55\" 4K",
        "description": "Smart TV 4K com Netflix e Prime Video",
        "availability": "in_stock",
        "condition": "new",
        "price": "250000 BRL",
        "sale_price": "220000 BRL",
        "link": "https://loja.com/produto/123",
        "image_link": "https://loja.com/img/123.jpg",
        "brand": "Samsung",
        "category": "Eletrônicos > TVs"
    }
]

upload_result = api.upload_products_batch(
    catalog_id=catalog["id"],
    products=products
)

# Criar campanha DPA
dpa_setup = api.create_dpa_campaign(
    name="DPA - Retargeting 7d",
    catalog_id=catalog["id"],
    pixel_id="123456789",
    budget=15000,  # R$150/dia
    targeting_type="retargeting"
)

# ========== CRON JOBS ==========

# 1. Sincronização de catálogo (diário)
scheduler.add_job(
    job_id="ecom_catalog_sync",
    job_type="catalog_sync",
    schedule_type="daily",
    schedule_value="03:00",
    params={
        "catalog_id": catalog["id"],
        "feed_id": feed["id"]
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

# 3. Recuperação de carrinho (4 horas)
scheduler.add_job(
    job_id="ecom_abandoned_cart",
    job_type="cart_recovery",
    schedule_type="interval",
    schedule_value="4h",
    params={
        "pixel_id": "123456789",
        "offer_type": "free_shipping"
    }
)

# Iniciar scheduler
scheduler.start()

print("✅ Setup completo!")
print(f"Catalog ID: {catalog['id']}")
print(f"Feed ID: {feed['id']}")
print(f"Campaign ID: {dpa_setup['campaign_id']}")
```

---

## Licença

MIT License - © 2026 Monrars