# Ferramentas - Agent Imobiliárias

> API Reference e implementações para campanhas de imobiliárias

## Índice

1. [Core API](#core-api)
2. [Product Catalog](#product-catalog)
3. [Offline Conversions](#offline-conversions)
4. [Analytics](#analytics)
5. [Scheduler Jobs](#scheduler-jobs)

---

## Core API

### realestate.create_campaign()

Cria uma campanha otimizada para imobiliárias.

```python
def create_campaign(
    self,
    name: str,
    objective: str,  # 'LEAD_GENERATION', 'CONVERSIONS', 'TRAFFIC'
    budget: int,  # em centavos
    property_type: str,  # 'apartment', 'house', 'commercial', 'land'
    price_range: str,  # 'economy', 'mid', 'high', 'luxury'
    special_config: Optional[Dict] = None
) -> Dict:
    """
    Cria campanha com configurações específicas para imóveis.
    
    Args:
        name: Nome da campanha
        objective: Objetivo da campanha
        budget: Orçamento diário em centavos
        property_type: Tipo de imóvel
        price_range: Faixa de preço
        special_config: Configurações especiais
        
    Returns:
        Dict com campaign_id, adset_id, creative_ids
        
    Example:
        >>> campaign = api.create_campaign(
        ...     name="Lançamento Residencial Garden - Pré-Venda",
        ...     objective="LEAD_GENERATION",
        ...     budget=30000,  # R$300/dia
        ...     property_type="apartment",
        ...     price_range="mid",
        ...     special_config={
        ...         "attribution_window": 30,
        ...         "offline_conversion": True,
        ...         "catalog_id": "123456789"
        ...     }
        ... )
    """
    # Configurações padrão para imobiliárias
    default_config = {
        "attribution_spec": [
            {"event_type": "conversion", "window_days": 30}
        ],
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
        "optimization_goal": "LEAD_GENERATION" if objective == "LEAD_GENERATION" else "OFFSITE_CONVERSIONS"
    }
    
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
            "bid_strategy": default_config["bid_strategy"]
        }
    )
    
    return campaign
```

### realestate.create_lead_form()

Cria formulário de Lead otimizado para imóveis.

```python
def create_lead_form(
    self,
    name: str,
    questions: List[Dict],
    privacy_url: str,
    thankyou_message: str,
    property_info: Optional[Dict] = None
) -> Dict:
    """
    Cria formulário de lead com campos específicos para imóveis.
    
    Args:
        name: Nome do formulário
        questions: Lista de perguntas
        privacy_url: URL da política de privacidade
        thankyou_message: Mensagem de agradecimento
        property_info: Informações do imóvel (opcional)
        
    Returns:
        Dict com form_id e leadgen_form_id
        
    Example:
        >>> form = api.create_lead_form(
        ...     name="Interesse - Apartamento 3 Quartos",
        ...     questions=[
        ...         {"type": "NAME", "label": "Nome completo"},
        ...         {"type": "EMAIL", "label": "E-mail"},
        ...         {"type": "PHONE", "label": "WhatsApp"},
        ...         {
        ...             "type": "CUSTOM",
        ...             "label": "Tipo de interesse",
        ...             "options": ["Moradia", "Investimento", "Aluguel"]
        ...         },
        ...         {
        ...             "type": "CUSTOM",
        ...             "label": "Faixa de valor",
        ...             "options": ["R$150-400k", "R$400-1M", "R$1-3M", "R$3M+"]
        ...         },
        ...         {
        ...             "type": "CUSTOM",
        ...             "label": "Quando pretende comprar?",
        ...             "options": ["Imediato", "1-3 meses", "3-6 meses", "Pesquisando"]
        ...         }
        ...     ],
        ...     privacy_url="https://imobiliaria.com/privacidade",
        ...     thankyou_message="Obrigado! Nossos corretores entrarão em contato em até 24h.",
        ...     property_info={
        ...         "type": "apartment",
        ...         "bedrooms": 3,
        ...         "area": "120m²",
        ...         "price": 850000,
        ...         "location": "Pinheiros, São Paulo"
        ...     }
        ... )
    """
    # Configurar contexto do imóvel
    if property_info:
        context_card = {
            "title": f"{property_info.get('bedrooms', '')} Quartos - {property_info.get('area', '')}",
            "subtitle": f"{property_info.get('location', '')} - R$ {property_info.get('price', 0):,.0f}",
            "style": "LIST_STYLE"
        }
    
    # Criar formulário
    form_data = {
        "name": name,
        "follow_up_action_url": privacy_url,
        "questions": questions,
        "thank_you_message": thankyou_message
    }
    
    if property_info:
        form_data["context_card"] = context_card
    
    form = self._request(
        method="POST",
        endpoint=f"{self.page_id}/leadgen_forms",
        data=form_data
    )
    
    return form
```

### realestate.create_audience()

Cria público-alvo otimizado para imobiliárias.

```python
def create_audience(
    self,
    name: str,
    audience_type: str,  # 'custom', 'lookalike', 'interest'
    config: Dict
) -> Dict:
    """
    Cria público-alvo com segmentação específica para imóveis.
    
    Args:
        name: Nome do público
        audience_type: Tipo do público
        config: Configurações do público
        
    Returns:
        Dict com audience_id
        
    Example:
        # Público por interesses
        >>> audience = api.create_audience(
        ...     name="Interessados em Imóveis - São Paulo",
        ...     audience_type="interest",
        ...     config={
        ...         "interests": ["Imóveis", "Casa própria", "Financiamento imobiliário"],
        ...         "life_events": ["Recently moved", "Newly engaged"],
        ...         "behaviors": ["Engaged shoppers", "Net worth high"],
        ...         "age_min": 25,
        ...         "age_max": 55,
        ...         "locations": ["Brazil:São Paulo"],
        ...         "property_type": "apartment",
        ...         "price_range": "mid"
        ...     }
        ... )
        
        # Lookalike de compradores
        >>> lookalike = api.create_audience(
        ...     name="Similar a Compradores 5%",
        ...     audience_type="lookalike",
        ...     config={
        ...         "source_audience": "buyers_365days",
        ...         "size": 5,
        ...         "country": "BR",
        ...         "property_type": "apartment"
        ...     }
        ... )
        
        # Público personalizado (visitantes)
        >>> custom = api.create_audience(
        ...     name="Visitantes Site 30 dias",
        ...     audience_type="custom",
        ...     config={
        ...         "rule": {
        ...             "event": "ViewContent",
        ...             "window": 30,
        ...             "property_type": "apartment"
        ...         },
        ...         "retention_days": 30
        ...     }
        ... )
    """
    if audience_type == "custom":
        # Público personalizado (pixel/CRM)
        audience = self._request(
            method="POST",
            endpoint=f"{self.ad_account_id}/custom_audiences",
            data={
                "name": name,
                "subtype": "CUSTOM",
                "description": config.get("description", ""),
                "customer_file_source": "USER_PROVIDED_ONLY",
                "rule": config["rule"]
            }
        )
    
    elif audience_type == "lookalike":
        # Lookalike
        audience = self._request(
            method="POST",
            endpoint=f"{self.ad_account_id}/custom_audiences",
            data={
                "name": name,
                "subtype": "LOOKALIKE",
                "origin_audience_id": config["source_audience"],
                "lookalike_spec": json.dumps({
                    "country": config.get("country", "BR"),
                    "type": "similarity",
                    "starting_ratio": 0.0,
                    "ratio": config["size"] / 100
                })
            }
        )
    
    elif audience_type == "interest":
        # Público por interesses
        targeting = {
            "geo_locations": {
                "countries": ["BR"],
                "regions": [{"key": loc} for loc in config.get("locations", [])]
            },
            "age_min": config.get("age_min", 18),
            "age_max": config.get("age_max", 65),
            "interests": [{"id": i, "name": i} for i in config["interests"]],
            "life_events": [{"id": le, "name": le} for le in config.get("life_events", [])],
            "behaviors": [{"id": b, "name": b} for b in config.get("behaviors", [])]
        }
        
        # Nota: Interesses são salvos no adset, não como audience separada
        return {"targeting": targeting}
    
    return audience
```

---

## Product Catalog

### catalog.create_property_catalog()

Cria catálogo de imóveis.

```python
def create_property_catalog(
    self,
    name: str,
    vertical: str = "HOME_LISTINGS"
) -> Dict:
    """
    Cria catálogo de imóveis para DPA.
    
    Args:
        name: Nome do catálogo
        vertical: Vertical do catálogo
        
    Returns:
        Dict com catalog_id
        
    Example:
        >>> catalog = api.create_property_catalog(
        ...     name="Imóveis - Imobiliária XYZ",
        ...     vertical="HOME_LISTINGS"
        ... )
        >>> print(catalog['id'])
        '123456789'
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

### catalog.create_property_feed()

Cria feed de imóveis.

```python
def create_property_feed(
    self,
    catalog_id: str,
    name: str,
    schedule: Dict
) -> Dict:
    """
    Cria feed de imóveis com agendamento de atualização.
    
    Args:
        catalog_id: ID do catálogo
        name: Nome do feed
        schedule: Agendamento de atualização
        
    Returns:
        Dict com feed_id
        
    Example:
        >>> feed = api.create_property_feed(
        ...     catalog_id="123456789",
        ...     name="Feed de Imóveis",
        ...     schedule={
        ...         "interval": "DAILY",
        ...         "hour": 6
        ...     }
        ... )
    """
    feed = self._request(
        method="POST",
        endpoint=f"{catalog_id}/product_feeds",
        data={
            "name": name,
            "schedule": schedule
        }
    )
    
    return feed
```

### catalog.upload_properties()

Faz upload de imóveis para o catálogo.

```python
def upload_properties(
    self,
    catalog_id: str,
    properties: List[Dict],
    batch_size: int = 100
) -> Dict:
    """
    Faz upload de imóveis em lote.
    
    Args:
        catalog_id: ID do catálogo
        properties: Lista de imóveis
        batch_size: Tamanho do lote
        
    Returns:
        Dict com estatísticas de upload
        
    Example:
        >>> properties = [
        ...     {
        ...         "id": "PROP_123",
        ...         "title": "Apartamento 3 Quartos - Pinheiros",
        ...         "description": "Apartamento宽敞 com 3 quartos...",
        ...         "availability": "in_stock",
        ...         "condition": "new",
        ...         "price": "850000 BRL",
        ...         "link": "https://imobiliaria.com/imovel/123",
        ...         "image_link": "https://imobiliaria.com/img/123.jpg",
        ...         "brand": "Imobiliária XYZ",
        ...         "category": "Apartamentos",
        ...         "property_type": "apartment",
        ...         "num_bedrooms": 3,
        ...         "num_bathrooms": 2,
        ...         "property_area": 120,
        ...         "address": {
        ...             "street": "Rua dos Pinheiros",
        ...             "city": "São Paulo",
        ...             "state": "SP",
        ...             "country": "BR"
        ...         }
        ...     }
        ... ]
        >>> result = api.upload_properties(
        ...     catalog_id="123456789",
        ...     properties=properties
        ... )
    """
    # Processar em lotes
    batches = [properties[i:i+batch_size] for i in range(0, len(properties), batch_size)]
    
    results = []
    for batch in batches:
        # Preparar dados
        data = {
            "requests": [
                {
                    "method": "POST",
                    "retailer_id": prop["id"],
                    "data": prop
                }
                for prop in batch
            ]
        }
        
        # Enviar
        response = self._request(
            method="POST",
            endpoint=f"{catalog_id}/batch",
            data=data
        )
        
        results.append(response)
    
    return {
        "total": len(properties),
        "batches": len(batches),
        "results": results
    }
```

---

## Offline Conversions

### offline.upload_events()

Upload de eventos offline para o Meta.

```python
def upload_offline_events(
    self,
    pixel_id: str,
    events: List[Dict],
    batch_size: int = 1000
) -> Dict:
    """
    Faz upload de eventos offline para atribuição.
    
    Args:
        pixel_id: ID do Pixel
        events: Lista de eventos
        batch_size: Tamanho do lote
        
    Returns:
        Dict com session_id e estatísticas
        
    Example:
        >>> events = [
        ...     {
        ...         "event_name": "Lead",
        ...         "event_time": int(datetime.now().timestamp()),
        ...         "user_data": {
        ...             "em": hash_sha256("cliente@email.com"),
        ...             "ph": hash_sha256("11999887766")
        ...         },
        ...         "custom_data": {
        ...             "content_name": "Apartamento 3 Quartos",
        ...             "content_category": "real_estate",
        ...             "property_type": "apartment",
        ...             "value": 850000,
        ...             "currency": "BRL"
        ...         }
        ...     },
        ...     {
        ...         "event_name": "Purchase",
        ...         "event_time": int(datetime.now().timestamp()),
        ...         "user_data": {
        ...             "em": hash_sha256("cliente@email.com"),
        ...             "ph": hash_sha256("11999887766")
        ...         },
        ...         "custom_data": {
        ...             "content_name": "Apartamento 3 Quartos",
        ...             "content_category": "real_estate",
        ...             "value": 850000,
        ...             "currency": "BRL",
        ...             "transaction_type": "sale"
        ...         }
        ...     }
        ... ]
        >>> result = api.upload_offline_events(
        ...     pixel_id="123456789",
        ...     events=events
        ... )
    """
    import hashlib
    
    # Processar em lotes
    batches = [events[i:i+batch_size] for i in range(0, len(events), batch_size)]
    
    results = []
    for batch in batches:
        # Preparar dados
        data = {
            "data": batch,
            "access_token": self.access_token
        }
        
        # Enviar
        response = self._request(
            method="POST",
            endpoint=f"{pixel_id}/events",
            data=data
        )
        
        results.append(response)
    
    return {
        "session_id": results[0].get("session_id"),
        "events_sent": len(events),
        "batches": len(batches)
    }
```

---

## Analytics

### analytics.calculate_roi()

Calcula ROI específico para imobiliárias.

```python
def calculate_realestate_roi(
    self,
    campaign_id: str,
    date_range: str = "last_30d",
    sales_data: Optional[Dict] = None
) -> Dict:
    """
    Calcula ROI considerando comissões de venda e aluguel.
    
    Args:
        campaign_id: ID da campanha
        date_range: Período de análise
        sales_data: Dados de vendas (opcional)
        
    Returns:
        Dict com ROI, ROAS e métricas
        
    Example:
        >>> roi = api.calculate_realestate_roi(
        ...     campaign_id="238495729384",
        ...     date_range="last_30d",
        ...     sales_data={
        ...         "sales_count": 3,
        ...         "rentals_count": 5,
        ...         "avg_sale_price": 800000,
        ...         "avg_rent_price": 3000,
        ...         "commission_sale": 0.06,
        ...         "commission_rent": 1.0
        ...     }
        ... )
    """
    # Buscar métricas da campanha
    metrics = self._request(
        method="GET",
        endpoint=f"{campaign_id}/insights",
        params={
            "date_preset": date_range,
            "fields": "spend,impressions,clicks,leads,conversions,cost_per_lead"
        }
    )
    
    # Dados de vendas padrão (se não fornecidos)
    if not sales_data:
        sales_data = {
            "sales_count": 0,
            "rentals_count": 0,
            "avg_sale_price": 800000,
            "avg_rent_price": 3000,
            "commission_sale": 0.06,
            "commission_rent": 1.0
        }
    
    # Cálculos
    spend = float(metrics["spend"])
    
    # Vendas
    avg_sale_price = sales_data.get("avg_sale_price", 800000)
    commission_sale = sales_data.get("commission_sale", 0.06)
    sales_count = sales_data.get("sales_count", 0)
    
    revenue_sale = avg_sale_price * commission_sale * sales_count
    
    # Aluguéis
    avg_rent_price = sales_data.get("avg_rent_price", 3000)
    commission_rent = sales_data.get("commission_rent", 1.0)  # 1 mês
    rentals_count = sales_data.get("rentals_count", 0)
    
    revenue_rent = avg_rent_price * commission_rent * rentals_count
    
    # Total
    total_revenue = revenue_sale + revenue_rent
    
    # ROI e ROAS
    roi_percentage = ((total_revenue - spend) / spend) * 100 if spend > 0 else 0
    roas = total_revenue / spend if spend > 0 else 0
    
    # Custo por venda/aluguel
    total_transactions = sales_count + rentals_count
    cost_per_transaction = spend / total_transactions if total_transactions > 0 else 0
    
    return {
        "roi_percentage": round(roi_percentage, 2),
        "roas": round(roas, 2),
        "total_revenue": round(total_revenue, 2),
        "sales_revenue": round(revenue_sale, 2),
        "rentals_revenue": round(revenue_rent, 2),
        "spend": round(spend, 2),
        "sales_count": sales_count,
        "rentals_count": rentals_count,
        "cost_per_transaction": round(cost_per_transaction, 2),
        "metrics": metrics
    }
```

### analytics.property_performance()

Gera relatório de performance por imóvel.

```python
def generate_property_performance(
    self,
    catalog_id: str,
    date_range: str = "last_30d"
) -> Dict:
    """
    Gera relatório de performance por imóvel.
    
    Args:
        catalog_id: ID do catálogo
        date_range: Período de análise
        
    Returns:
        Dict com métricas por imóvel
        
    Example:
        >>> report = api.generate_property_performance(
        ...     catalog_id="123456789",
        ...     date_range="last_30d"
        ... )
    """
    # Buscar métricas do catálogo
    metrics = self._request(
        method="GET",
        endpoint=f"{catalog_id}/insights",
        params={
            "date_preset": date_range,
            "fields": "product_id,title,impressions,clicks,add_to_cart,purchases,spend",
            "breakdowns": "product_id"
        }
    )
    
    # Processar por imóvel
    properties = []
    for item in metrics.get("data", []):
        property_data = {
            "id": item.get("product_id"),
            "title": item.get("title"),
            "impressions": int(item.get("impressions", 0)),
            "clicks": int(item.get("clicks", 0)),
            "ctr": float(item.get("clicks", 0)) / int(item.get("impressions", 1)) * 100,
            "purchases": int(item.get("purchases", 0)),
            "spend": float(item.get("spend", 0)),
            "cost_per_purchase": float(item.get("spend", 0)) / int(item.get("purchases", 1)) if int(item.get("purchases", 0)) > 0 else 0
        }
        properties.append(property_data)
    
    # Ordenar por conversões
    properties.sort(key=lambda x: x["purchases"], reverse=True)
    
    return {
        "properties": properties,
        "total_properties": len(properties),
        "date_range": date_range
    }
```

---

## Scheduler Jobs

### scheduler.add_offline_sync()

Adiciona job de sincronização offline.

```python
def add_offline_sync_job(
    self,
    pixel_id: str,
    crm_config: Dict,
    schedule_type: str = "interval",
    schedule_value: str = "7d"
) -> Dict:
    """
    Adiciona job de sincronização offline agendado.
    
    Args:
        pixel_id: ID do Pixel
        crm_config: Configuração do CRM
        schedule_type: Tipo de agendamento
        schedule_value: Valor do agendamento
        
    Returns:
        Dict com job_id
    """
    job_id = f"realestate_offline_{pixel_id}_{int(time.time())}"
    
    # Adicionar job
    self.add_job(
        job_id=job_id,
        job_type="offline_conversion",
        schedule_type=schedule_type,
        schedule_value=schedule_value,
        params={
            "pixel_id": pixel_id,
            "crm_config": crm_config,
            "events": ["Lead", "Visit", "Proposal", "Sale", "Rent"],
            "property_data": True
        }
    )
    
    return {"job_id": job_id, "schedule": f"{schedule_type}: {schedule_value}"}
```

### scheduler.add_inventory_update()

Adiciona job de atualização de inventário.

```python
def add_inventory_update_job(
    self,
    catalog_id: str,
    source_config: Dict,
    schedule_type: str = "daily",
    schedule_value: str = "06:00"
) -> Dict:
    """
    Adiciona job de atualização de inventário.
    
    Args:
        catalog_id: ID do catálogo
        source_config: Configuração da fonte de dados
        schedule_type: Tipo de agendamento
        schedule_value: Valor do agendamento
        
    Returns:
        Dict com job_id
    """
    job_id = f"realestate_inventory_{catalog_id}"
    
    # Adicionar job
    self.add_job(
        job_id=job_id,
        job_type="feed_update",
        schedule_type=schedule_type,
        schedule_value=schedule_value,
        params={
            "catalog_id": catalog_id,
            "source": source_config.get("source", "erp"),
            "fields": [
                "id", "title", "description", "availability",
                "price", "sale_price", "link", "image_link",
                "brand", "category", "property_type", "num_bedrooms",
                "num_bathrooms", "property_area", "address"
            ]
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

# Criar catálogo de imóveis
catalog = api.create_property_catalog(
    name="Imóveis - Imobiliária XYZ",
    vertical="HOME_LISTINGS"
)

# Criar feed
feed = api.create_property_feed(
    catalog_id=catalog["id"],
    name="Feed de Imóveis",
    schedule={"interval": "DAILY", "hour": 6}
)

# Upload de imóveis
properties = [
    {
        "id": "PROP_123",
        "title": "Apartamento 3 Quartos - Pinheiros",
        "description": "Apartamento spacious com 3 quartos...",
        "availability": "in_stock",
        "condition": "new",
        "price": "850000 BRL",
        "link": "https://imobiliaria.com/imovel/123",
        "image_link": "https://imobiliaria.com/img/123.jpg",
        "property_type": "apartment",
        "num_bedrooms": 3,
        "num_bathrooms": 2,
        "property_area": 120
    }
]

upload_result = api.upload_properties(
    catalog_id=catalog["id"],
    properties=properties
)

# Criar campanha
campaign = api.create_campaign(
    name="Apartamentos - Pinheiros",
    objective="LEAD_GENERATION",
    budget=30000,  # R$300/dia
    property_type="apartment",
    price_range="mid",
    special_config={
        "attribution_window": 30,
        "offline_conversion": True,
        "catalog_id": catalog["id"]
    }
)

# Criar lead form
form = api.create_lead_form(
    name="Interesse em Apartamentos",
    questions=[
        {"type": "NAME", "label": "Nome completo"},
        {"type": "EMAIL", "label": "E-mail"},
        {"type": "PHONE", "label": "WhatsApp"},
        {
            "type": "CUSTOM",
            "label": "Tipo de interesse",
            "options": ["Moradia", "Investimento", "Aluguel"]
        }
    ],
    privacy_url="https://imobiliaria.com/privacidade",
    thankyou_message="Obrigado! Nossos corretores entrarão em contato."
)

# Criar público
audience = api.create_audience(
    name="Interessados em Imóveis - SP",
    audience_type="interest",
    config={
        "interests": ["Imóveis", "Casa própria", "Financiamento imobiliário"],
        "life_events": ["Recently moved"],
        "behaviors": ["Engaged shoppers"],
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
        "match_keys": ["em", "ph"]
    }
)

# 2. Atualização de inventário (diário)
scheduler.add_job(
    job_id="realestate_inventory_update",
    job_type="feed_update",
    schedule_type="daily",
    schedule_value="06:00",
    params={
        "catalog_id": catalog["id"],
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
        "report_type": "property_performance",
        "kpis": ["leads", "visits", "sales", "rentals"],
        "breakdown": "property",
        "email": "corretor@imobiliaria.com"
    }
)

# Iniciar scheduler
scheduler.start()

print("✅ Setup completo!")
print(f"Catalog ID: {catalog['id']}")
print(f"Feed ID: {feed['id']}")
print(f"Campaign ID: {campaign['campaign_id']}")
print(f"Form ID: {form['form_id']}")
```

---

## Licença

MIT License - © 2026 Monrars