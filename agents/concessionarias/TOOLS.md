# Ferramentas - Agent Concessionárias

> API Reference e implementações para campanhas de concessionárias

##Índice

1. [Core API](#core-api)
2. [Offline Conversions](#offline-conversions)
3. [CRM Integration](#crm-integration)
4. [Analytics](#analytics)
5. [Scheduler Jobs](#scheduler-jobs)

---

## Core API

### dealership.create_campaign()

Cria uma campanha otimizada para concessionárias.

```python
def create_campaign(
    self,
    name: str,
    objective: str,  # 'LEAD_GENERATION', 'CONVERSIONS', 'TRAFFIC', 'REACH'
    budget: int,  # em centavos (R$10000 = R$100,00)
    special_config: Optional[Dict] = None
) -> Dict:
    """
    Cria campanha com configurações específicas para concessionárias.
    
    Args:
        name: Nome da campanha
        objective: Objetivo da campanha
        budget: Orçamento diário em centavos
        special_config: Configurações especiais
        
    Returns:
        Dict com campaign_id, adset_id, creative_ids
        
    Example:
        >>> campaign = api.create_campaign(
        ...     name="Civic 2024 - Test Drive",
        ...     objective="LEAD_GENERATION",
        ...     budget=20000,  # R$200/dia
        ...     special_config={
        ...         "attribution_window": 30,
        ...         "offline_conversion": True,
        ...         "vehicle_model": "Honda Civic"
        ...     }
        ... )
        >>> print(campaign['campaign_id'])
        '238495729384'
    """
    # Configurações padrão para concessionárias
    default_config = {
        "attribution_spec": [
            {"event_type": "conversion", "window_days": 30}
        ],
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
        "optimization_goal": "LEAD_GENERATION" if objective == "LEAD_GENERATION" else "OFFSITE_CONVERSIONS",
        "destination_type": "LEAD_FORM" if objective == "LEAD_GENERATION" else "WEBSITE"
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

### dealership.create_lead_form()

Cria formulário de Lead otimizado para concessionárias.

```python
def create_lead_form(
    self,
    name: str,
    questions: List[Dict],
    privacy_url: str,
    thankyou_message: str,
    vehicle_info: Optional[Dict] = None
) -> Dict:
    """
    Cria formulário de lead com campos específicos.
    
    Args:
        name: Nome do formulário
        questions: Lista de perguntas
        privacy_url: URL da política de privacidade
        thankyou_message: Mensagem de agradecimento
        vehicle_info: Informações do veículo (opcional)
        
    Returns:
        Dict com form_id e leadgen_form_id
        
    Example:
        >>> form = api.create_lead_form(
        ...     name="Test Drive - Civic 2024",
        ...     questions=[
        ...         {"type": "NAME", "label": "Nome completo"},
        ...         {"type": "EMAIL", "label": "E-mail"},
        ...         {"type": "PHONE", "label": "WhatsApp"},
        ...         {
        ...             "type": "CUSTOM",
        ...             "label": "Interesse",
        ...             "options": ["Novo", "Usado", "Financiamento"]
        ...         },
        ...         {
        ...             "type": "CUSTOM",
        ...             "label": "Como conheceu?",
        ...             "options": ["Google", "Facebook", "Indicação"]
        ...         }
        ...     ],
        ...     privacy_url="https://concessionaria.com/privacidade",
        ...     thankyou_message="Obrigado! Entraremos em contato em até 24h.",
        ...     vehicle_info={
        ...         "brand": "Honda",
        ...         "model": "Civic",
        ...         "year": 2024
        ...     }
        ... )
    """
    # Configurar contexto do veículo
    if vehicle_info:
        context_card = {
            "title": f"{vehicle_info['brand']} {vehicle_info['model']} {vehicle_info['year']}",
            "description": "Agende seu test drive e conheça o veículo dos seus sonhos.",
            "style": "LIST_STYLE"
        }
    
    # Criar formulário
    form_data = {
        "name": name,
        "follow_up_action_url": privacy_url,
        "questions": questions,
        "thank_you_message": thankyou_message
    }
    
    if vehicle_info:
        form_data["context_card"] = context_card
    
    form = self._request(
        method="POST",
        endpoint=f"{self.page_id}/leadgen_forms",
        data=form_data
    )
    
    return form
```

### dealership.create_audience()

Cria público-alvo otimizado para concessionárias.

```python
def create_audience(
    self,
    name: str,
    audience_type: str,  # 'custom', 'lookalike', 'interest'
    config: Dict
) -> Dict:
    """
    Cria público-alvo com segmentação específica.
    
    Args:
        name: Nome do público
        audience_type: Tipo do público
        config: Configurações do público
        
    Returns:
        Dict com audience_id
        
    Example:
        # Público personalizado (visitantes)
        >>> audience = api.create_audience(
        ...     name="Visitantes Site 30 dias",
        ...     audience_type="custom",
        ...     config={
        ...         "rule": {
        ...             "event": "PageView",
        ...             "window": 30
        ...         },
        ...         "retention_days": 30
        ...     }
        ... )
        
        # Lookalike
        >>> lookalike = api.create_audience(
        ...     name="Similar a Leads 5%",
        ...     audience_type="lookalike",
        ...     config={
        ...         "source_audience": "leads_90days",
        ...         "size": 5,
        ...         "country": "BR"
        ...     }
        ... )
        
        # Interesses
        >>> interest = api.create_audience(
        ...     name="Interessados em Carros",
        ...     audience_type="interest",
        ...     config={
        ...         "interests": ["Carros", "Automóveis", "Test drive"],
        ...         "behaviors": ["Engaged shoppers"],
        ...         "age_min": 25,
        ...         "age_max": 55,
        ...         "locations": ["Brazil:São Paulo"]
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
                    "ratio": config["size"] / 100  # 5% = 0.05
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
            "behaviors": [{"id": b, "name": b} for b in config.get("behaviors", [])]
        }
        
        # Nota: Interesses são salvos no adset, não como audience separada
        return {"targeting": targeting}
    
    return audience
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
        ...             "content_name": "Honda Civic EXL",
        ...             "content_category": "Test Drive",
        ...             "vehicle_brand": "Honda",
        ...             "vehicle_model": "Civic"
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
        ...             "currency": "BRL",
        ...             "value": 125000,
        ...             "content_name": "Honda Civic EXL",
        ...             "vehicle_brand": "Honda",
        ...             "vehicle_model": "Civic",
        ...             "vehicle_year": 2024
        ...         }
        ...     }
        ... ]
        >>> result = api.upload_offline_events(
        ...     pixel_id="123456789",
        ...     events=events
        ... )
        >>> print(result['session_id'])
        'session_12345'
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

def hash_sha256(value: str) -> str:
    """
    Hasheia valor em SHA256 (padrão Meta).
    
    Args:
        value: Valor para hash
        
    Returns:
        String hash em lowercase
        
    Example:
        >>> hash_sha256("cliente@email.com")
        "7b52e31b2e..."
    """
    return hashlib.sha256(value.lower().strip().encode()).hexdigest()
```

### offline.create_conversion_set()

Cria conjunto de conversões offline.

```python
def create_offline_conversion_set(
    self,
    name: str,
    description: str = ""description: str = "",
    event_stats: Optional[Dict] = None
) -> Dict:
    """
    Cria conjunto de conversões offline para eventos do CRM.
    
    Args:
        name: Nome do conjunto
        description: Descrição
        event_stats: Estatísticas de eventos (opcional)
        
    Returns:
        Dict com id do conjunto
        
    Example:
        >>> conv_set = api.create_offline_conversion_set(
        ...     name="Conversões CRM - Concessionária",
        ...     description="Eventos de vendas do CRM",
        ...     event_stats={
        ...         "test_drives": 45,
        ...         "proposals": 12,
        ...         "sales": 5
        ...     }
        ... )
    """
    data = {
        "name": name,
        "description": description
    }
    
    result = self._request(
        method="POST",
        endpoint=f"{self.business_id}/offline_conversion_data_sets",
        data=data
    )
    
    return result
```

---

## CRM Integration

### crm.export_events()

Exporta eventos do CRM para upload offline.

```python
def export_crm_events(
    self,
    days: int = 7,
    events: List[str] = ["Lead", "TestDrive", "Proposal", "Purchase"],
    crm_config: Dict
) -> List[Dict]:
    """
    Exporta eventos do CRM nos últimos N dias.
    
    Args:
        days: Número de dias para exportar
        events: Lista de eventos
        crm_config: Configuração do CRM
        
    Returns:
        Lista de eventos formato Meta
        
    Example:
        >>> events = api.export_crm_events(
        ...     days=7,
        ...     events=["TestDrive", "Purchase"],
        ...     crm_config={
        ...         "type": "salesforce",
        ...         "api_key": "...",
        ...         "instance_url": "https://instance.salesforce.com"
        ...     }
        ... )
    """
    import requests
    from datetime import datetime, timedelta
    
    # Data de início
    start_date = datetime.now() - timedelta(days=days)
    
    # Query baseada no tipo de CRM
    if crm_config["type"] == "salesforce":
        events_list = self._query_salesforce(
            crm_config=crm_config,
            start_date=start_date,
            events=events
        )
    elif crm_config["type"] == "hubspot":
        events_list = self._query_hubspot(
            crm_config=crm_config,
            start_date=start_date,
            events=events
        )
    elif crm_config["type"] == "pipedrive":
        events_list = self._query_pipedrive(
            crm_config=crm_config,
            start_date=start_date,
            events=events
        )
    else:
        # Genérico (CSV/API customizada)
        events_list = self._query_generic_crm(
            crm_config=crm_config,
            start_date=start_date,
            events=events
        )
    
    # Converter para formato Meta
    meta_events = []
    for event in events_list:
        meta_event = {
            "event_name": event["event_name"],
            "event_time": int(event["event_time"].timestamp()),
            "user_data": {
                "em": hash_sha256(event["email"]),
                "ph": hash_sha256(event["phone"])
            },
            "custom_data": event.get("custom_data", {})
        }
        meta_events.append(meta_event)
    
    return meta_events

def _query_salesforce(
    self,
    crm_config: Dict,
    start_date: datetime,
    events: List[str]
) -> List[Dict]:
    """
    Query Salesforce CRM para eventos.
    
    Args:
        crm_config: Configuração do Salesforce
        start_date: Data de início
        events: Lista de eventos
        
    Returns:
        Lista de eventos
    """
    import requests
    
    # SOQL Query
    query = f"""
    SELECT Id, Email, Phone, Event_Type__c, CreatedDate, Vehicle_Brand__c, Vehicle_Model__c, Amount__c
    FROM Lead_Events__c
    WHERE CreatedDate >= {start_date.isoformat()}
    AND Event_Type__c IN ({','.join(events)})
    """
    
    # Headers
    headers = {
        "Authorization": f"Bearer {crm_config['api_key']}",
        "Content-Type": "application/json"
    }
    
    # Request
    response = requests.get(
        f"{crm_config['instance_url']}/services/data/v57.0/query",
        headers=headers,
        params={"q": query}
    )
    
    # Parse
    data = response.json()
    
    # Converter para formato interno
    events_list = []
    for record in data.get("records", []):
        event = {
            "event_name": record["Event_Type__c"],
            "event_time": datetime.fromisoformat(record["CreatedDate"]),
            "email": record["Email"],
            "phone": record["Phone"],
            "custom_data": {
                "vehicle_brand": record.get("Vehicle_Brand__c"),
                "vehicle_model": record.get("Vehicle_Model__c"),
                "value": record.get("Amount__c")
            }
        }
        events_list.append(event)
    
    return events_list
```

### crm.sync_leads()

Sincroniza leads do Facebook para o CRM.

```python
def sync_leads_to_crm(
    self,
    form_id: str,
    crm_config: Dict,
    since: Optional[datetime] = None
) -> Dict:
    """
    Sincroniza leads do Facebook para o CRM.
    
    Args:
        form_id: ID do formulário de lead
        crm_config: Configuração do CRM
        since: Data de início (opcional)
        
    Returns:
        Dict com estatísticas de sincronização
        
    Example:
        >>> result = api.sync_leads_to_crm(
        ...     form_id="123456789",
        ...     crm_config={
        ...         "type": "salesforce",
        ...         "api_key": "...",
        ...         "instance_url": "..."
        ...     },
        ...     since=datetime.now() - timedelta(days=1)
        ... )
        >>> print(f"Leads sincronizados: {result['synced']}")
    """
    # Buscar leads do Facebook
    leads = self._request(
        method="GET",
        endpoint=f"{form_id}/leads",
        params={
            "since": since.isoformat() if since else None
        }
    )
    
    # Converter para formato do CRM
    crm_leads = []
    for lead in leads.get("data", []):
        crm_lead = {
            "name": lead.get("field_data", {}).get("full_name", ""),
            "email": lead.get("field_data", {}).get("email", ""),
            "phone": lead.get("field_data", {}).get("phone_number", ""),
            "source": "Facebook Lead Ad",
            "campaign": lead.get("campaign_name", ""),
            "adset": lead.get("adset_name", ""),
            "created": lead.get("created_time", "")
        }
        crm_leads.append(crm_lead)
    
    # Enviar para CRM
    if crm_config["type"] == "salesforce":
        synced = self._send_to_salesforce(crm_config, crm_leads)
    elif crm_config["type"] == "hubspot":
        synced = self._send_to_hubspot(crm_config, crm_leads)
    elif crm_config["type"] == "pipedrive":
        synced = self._send_to_pipedrive(crm_config, crm_leads)
    else:
        synced = self._send_to_generic_crm(crm_config, crm_leads)
    
    return {
        "total": len(leads.get("data", [])),
        "synced": synced,
        "form_id": form_id
    }
```

---

## Analytics

### analytics.calculate_roi()

Calcula ROI específico para concessionárias.

```python
def calculate_dealership_roi(
    self,
    campaign_id: str,
    date_range: str = "last_30d",
    sales_data: Optional[Dict] = None
) -> Dict:
    """
    Calcula ROI considerando margens de veículos.
    
    Args:
        campaign_id: ID da campanha
        date_range: Período de análise
        sales_data: Dados de vendas (opcional)
        
    Returns:
        Dict com ROI, ROAS e métricas
        
    Example:
        >>> roi = api.calculate_dealership_roi(
        ...     campaign_id="238495729384",
        ...     date_range="last_30d",
        ...     sales_data={
        ...         "new_sales": 5,
        ...         "used_sales": 3,
        ...         "avg_ticket_new": 120000,
        ...         "avg_ticket_used": 70000
        ...     }
        ... )
        >>> print(f"ROI: {roi['roi_percentage']}%")
        >>> print(f"ROAS: {roi['roas']}x")
    """
    # Buscar métricas da campanha
    metrics = self._request(
        method="GET",
        endpoint=f"{campaign_id}/insights",
        params={
            "date_preset": date_range,
            "fields": "spend,impressions,clicks,leads,conversions,cost_per_lead,cost_per_conversion"
        }
    )
    
    # Dados de vendas padrão (se não fornecidos)
    if not sales_data:
        sales_data = {
            "new_sales": metrics["conversions"],
            "used_sales": int(metrics["conversions"] * 0.6),  # Estimativa
            "avg_ticket_new": 120000,
            "avg_ticket_used": 70000
        }
    
    # Cálculos
    spend = float(metrics["spend"])
    
    # Margens (aproximadas)
    margin_new = 0.08  # 8% margem em novos
    margin_used = 0.12  # 12% margem em usados
    
    # Receita
    revenue_new = sales_data["new_sales"] * sales_data["avg_ticket_new"] * margin_new
    revenue_used = sales_data["used_sales"] * sales_data["avg_ticket_used"] * margin_used
    total_revenue = revenue_new + revenue_used
    
    # ROI e ROAS
    roi_percentage = ((total_revenue - spend) / spend) * 100 if spend > 0 else 0
    roas = total_revenue / spend if spend > 0 else 0
    
    # Custo por venda
    total_sales = sales_data["new_sales"] + sales_data["used_sales"]
    cost_per_sale = spend / total_sales if total_sales > 0 else 0
    
    return {
        "roi_percentage": round(roi_percentage, 2),
        "roas": round(roas, 2),
        "total_revenue": round(total_revenue, 2),
        "revenue_new": round(revenue_new, 2),
        "revenue_used": round(revenue_used, 2),
        "spend": round(spend, 2),
        "total_sales": total_sales,
        "new_sales": sales_data["new_sales"],
        "used_sales": sales_data["used_sales"],
        "cost_per_sale": round(cost_per_sale, 2),
        "metrics": metrics
    }
```

### analytics.funnel_report()

Gera relatório de funil para concessionárias.

```python
def generate_funnel_report(
    self,
    campaign_ids: List[str],
    date_range: str = "last_30d"
) -> Dict:
    """
    Gera relatório de funil específico para concessionárias.
    
    Args:
        campaign_ids: Lista de IDs de campanha
        date_range: Período de análise
        
    Returns:
        Dict com métricas do funil
        
    Example:
        >>> report = api.generate_funnel_report(
        ...     campaign_ids=["camp1", "camp2"],
        ...     date_range="last_30d"
        ... )
        >>> print(json.dumps(report, indent=2))
    """
    # Inicializar métricas
    funnel = {
        "impressions": 0,
        "clicks": 0,
        "leads": 0,
        "test_drives": 0,
        "proposals": 0,
        "sales": 0,
        "spend": 0
    }
    
    # Buscar métricas de cada campanha
    for campaign_id in campaign_ids:
        insights = self._request(
            method="GET",
            endpoint=f"{campaign_id}/insights",
            params={
                "date_preset": date_range,
                "fields": "spend,impressions,clicks,leads,conversions,offline_conversions"
            }
        )
        
        funnel["impressions"] += int(insights.get("impressions", 0))
        funnel["clicks"] += int(insights.get("clicks", 0))
        funnel["leads"] += int(insights.get("leads", 0))
        funnel["spend"] += float(insights.get("spend", 0))
        
        # Buscar conversões offline (apenas se disponível)
        if "offline_conversions" in insights:
            for conv in insights["offline_conversions"]:
                if conv["action_type"] == "test_drive":
                    funnel["test_drives"] += int(conv["value"])
                elif conv["action_type"] == "proposal":
                    funnel["proposals"] += int(conv["value"])
                elif conv["action_type"] == "purchase":
                    funnel["sales"] += int(conv["value"])
    
    # Calcular taxas de conversão
    rates = {
        "ctr": funnel["clicks"] / funnel["impressions"] * 100 if funnel["impressions"] > 0 else 0,
        "lead_rate": funnel["leads"] / funnel["clicks"] * 100 if funnel["clicks"] > 0 else 0,
        "test_drive_rate": funnel["test_drives"] / funnel["leads"] * 100 if funnel["leads"] > 0 else 0,
        "proposal_rate": funnel["proposals"] / funnel["test_drives"] * 100 if funnel["test_drives"] > 0 else 0,
        "sale_rate": funnel["sales"] / funnel["proposals"] * 100 if funnel["proposals"] > 0 else 0
    }
    
    # Calcular custos
    costs = {
        "cost_per_click": funnel["spend"] / funnel["clicks"] if funnel["clicks"] > 0 else 0,
        "cost_per_lead": funnel["spend"] / funnel["leads"] if funnel["leads"] > 0 else 0,
        "cost_per_test_drive": funnel["spend"] / funnel["test_drives"] if funnel["test_drives"] > 0 else 0,
        "cost_per_proposal": funnel["spend"] / funnel["proposals"] if funnel["proposals"] > 0 else 0,
        "cost_per_sale": funnel["spend"] / funnel["sales"] if funnel["sales"] > 0 else 0
    }
    
    return {
        "funnel": funnel,
        "rates": rates,
        "costs": costs,
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
        schedule_type: Tipo de agendamento (interval, weekly, etc)
        schedule_value: Valor do agendamento
        
    Returns:
        Dict com job_id
        
    Example:
        >>> job = scheduler.add_offline_sync_job(
        ...     pixel_id="123456789",
        ...     crm_config={
        ...         "type": "salesforce",
        ...         "api_key": "...",
        ...         "instance_url": "..."
        ...     },
        ...     schedule_type="interval",
        ...     schedule_value="7d"
        ... )
        >>> print(f"Job ID: {job['job_id']}")
    """
    job_id = f"offline_sync_{pixel_id}_{int(time.time())}"
    
    # Adicionar job
    self.add_job(
        job_id=job_id,
        job_type="offline_conversion",
        schedule_type=schedule_type,
        schedule_value=schedule_value,
        params={
            "pixel_id": pixel_id,
            "crm_config": crm_config,
            "events": ["Lead", "TestDrive", "Proposal", "Purchase"]
        }
    )
    
    return {"job_id": job_id, "schedule": f"{schedule_type}: {schedule_value}"}

# Exemplo de uso completo
if __name__ == "__main__":
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
    
    # Criar campanha
    campaign = api.create_campaign(
        name="Civic 2024 - Test Drive",
        objective="LEAD_GENERATION",
        budget=20000,  # R$200/dia
        special_config={
            "attribution_window": 30,
            "offline_conversion": True
        }
    )
    
    # Criar formulário
    form = api.create_lead_form(
        name="Test Drive - Civic 2024",
        questions=[
            {"type": "NAME", "label": "Nome completo"},
            {"type": "EMAIL", "label": "E-mail"},
            {"type": "PHONE", "label": "WhatsApp"},
            {"type": "CUSTOM", "label": "Interesse", "options": ["Novo", "Usado"]}
        ],
        privacy_url="https://concessionaria.com/privacidade",
        thankyou_message="Obrigado! Entraremos em contato em até 24h."
    )
    
    # Criar público
    audience = api.create_audience(
        name="Interessados em Carros - SP",
        audience_type="interest",
        config={
            "interests": ["Carros", "Automóveis", "Test drive"],
            "behaviors": ["Engaged shoppers"],
            "age_min": 25,
            "age_max": 55,
            "locations": ["Brazil:São Paulo"]
        }
    )
    
    # ========== CRON JOBS ==========
    
    # Job de sincronização offline (7dias)
    offline_job = scheduler.add_offline_sync_job(
        pixel_id="123456789",
        crm_config={
            "type": "salesforce",
            "api_key": "...",
            "instance_url": "..."
        },
        schedule_type="interval",
        schedule_value="7d"
    )
    
    # Job de análise semanal
    analysis_job = scheduler.add_job(
        job_id="dealership_analysis",
        job_type="analysis",
        schedule_type="weekly",
        schedule_value="monday 09:00",
        params={
            "campaign_ids": [campaign["campaign_id"]],
            "kpis": ["leads", "cost_per_lead", "test_drive_rate"]
        }
    )
    
    # Iniciar scheduler
    scheduler.start()
    
    print("✅ Setup completo!")
    print(f"Campaign ID: {campaign['campaign_id']}")
    print(f"Form ID: {form['form_id']}")
    print(f"Job ID: {offline_job['job_id']}")
```

---

## Lista de Verificação Pré-Launch

```python
def pre_launch_checklist(
    self,
    campaign_config: Dict
) -> Dict:
    """
    Executa checklist de pré-launch para campanha de concessionária.
    
    Args:
        campaign_config: Configuração da campanha
        
    Returns:
        Dict com status do checklist
        
    Example:
        >>> checklist = api.pre_launch_checklist(
        ...     campaign_config={
        ...         "name": "Civic 2024",
        ...         "objective": "LEAD_GENERATION",
        ...         "budget": 20000,
        ...         "pixel_id": "123456789",
        ...         "offline_conversion": True
        ...     }
        ... )
        >>> if checklist["ready"]:
        ...     print("✅ Pronto para lançar!")
        ... else:
        ...     print("⚠️ Pendências:")
        ...     for item in checklist["pending"]:
        ...         print(f"  - {item}")
    """
    checks = {
        "pixel_configured": False,
        "offline_conversion_setup": False,
        "lead_form_created": False,
        "audience_defined": False,
        "creative_ready": False,
        "crm_integration": False,
        "attribution_window_set": False
    }
    
    # Verificar Pixel
    try:
        pixel = self._request(
            method="GET",
            endpoint=f"{campaign_config['pixel_id']}"
        )
        checks["pixel_configured"] = True
    except:
        pass
    
    # Verificar Conversão Offline
    if campaign_config.get("offline_conversion"):
        try:
            offline_sets = self._request(
                method="GET",
                endpoint=f"{self.business_id}/offline_conversion_data_sets"
            )
            if offline_sets:
                checks["offline_conversion_setup"] = True
        except:
            pass
    
    # Verificar Formulário de Lead
    if campaign_config.get("lead_form_id"):
        try:
            form = self._request(
                method="GET",
                endpoint=f"{campaign_config['lead_form_id']}"
            )
            checks["lead_form_created"] = True
        except:
            pass
    
    # Verificar Público
    if campaign_config.get("audience_id"):
        try:
            audience = self._request(
                method="GET",
                endpoint=f"{campaign_config['audience_id']}"
            )
            checks["audience_defined"] = True
        except:
            pass
    
    # Verificar Criativo
    if campaign_config.get("creative_id"):
        try:
            creative = self._request(
                method="GET",
                endpoint=f"{campaign_config['creative_id']}"
            )
            checks["creative_ready"] = True
        except:
            pass
    
    # Verificar CRM
    if campaign_config.get("crm_config"):
        checks["crm_integration"] = True
    
    # Verificar Janela de Atribuição
    if campaign_config.get("attribution_window"):
        checks["attribution_window_set"] = True
    
    # Compilar resultado
    ready = all(checks.values())
    pending = [k for k, v in checks.items() if not v]
    
    return {
        "ready": ready,
        "checks": checks,
        "pending": pending,
        "total": len(checks),
        "completed": sum(checks.values())
    }
```

---

## Licença

MIT License - © 2026 Monrars