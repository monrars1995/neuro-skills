# Tools - Neuro Ads Manager

Ferramentas e implementações do skill.

## Ferramentas Disponíveis

### Gerenciamento de Campanhas

| Tool | Descrição | Parâmetros Obrigatórios |
|------|-----------|------------------------|
| `create_campaign` | Cria nova campanha | name, objective |
| `list_campaigns` | Lista campanhas | - |
| `get_campaign` | Obtém detalhes | campaign_id |
| `update_campaign` | Atualiza campanha | campaign_id |
| `delete_campaign` | Deleta campanha | campaign_id |
| `duplicate_campaign` | Duplica campanha | campaign_id |

### Gerenciamento de Ad Sets

| Tool | Descrição | Parâmetros Obrigatórios |
|------|-----------|------------------------|
| `create_adset` | Cria ad set | campaign_id, name |
| `list_adsets` | Lista ad sets | campaign_id |
| `get_adset` | Obtém detalhes | adset_id |
| `update_adset` | Atualiza ad set | adset_id |
| `delete_adset` | Deleta ad set | adset_id |

### Gerenciamento de Ads

| Tool | Descrição | Parâmetros Obrigatórios |
|------|-----------|------------------------|
| `create_ad` | Cria ad | adset_id, creative_id, name |
| `list_ads` | Lista ads | adset_id |
| `get_ad` | Obtém detalhes | ad_id |
| `update_ad` | Atualiza ad | ad_id |
| `delete_ad` | Deleta ad | ad_id |

### Gerenciamento de Creatives

| Tool | Descrição | Parâmetros Obrigatórios |
|------|-----------|------------------------|
| `create_creative` | Cria criativo | name, page_id |
| `list_creatives` | Lista criativos | - |
| `get_creative` | Obtém detalhes | creative_id |
| `update_creative` | Atualiza criativo | creative_id |
| `duplicate_creative` | Duplica criativo | creative_id |

### Upload de Mídia

| Tool | Descrição | Parâmetros Obrigatórios |
|------|-----------|------------------------|
| `upload_video` | Upload de vídeo | file_path |
| `upload_image` | Upload de imagem | file_path |
| `get_video_status` | Status do upload | video_id |

### Analytics

| Tool | Descrição | Parâmetros Obrigatórios |
|------|-----------|------------------------|
| `get_campaign_insights` | Insights de campanha | campaign_id |
| `get_adset_insights` | Insights de ad set | adset_id |
| `get_ad_insights` | Insights de ad | ad_id |
| `get_account_insights` | Insights de conta | - |
| `generate_report` | Gera relatório | date_range |

### Automação

| Tool | Descrição | Parâmetros Obrigatórios |
|------|-----------|------------------------|
| `create_rule` | Cria regra | name, trigger, action |
| `list_rules` | Lista regras | - |
| `update_rule` | Atualiza regra | rule_id |
| `delete_rule` | Deleta regra | rule_id |
| `execute_rules` | Executa regras | - |

## Implementação

### create_campaign

```python
def create_campaign(
    self,
    name: str,
    objective: str,
    budget: int = None,
    status: str = "PAUSED",
    special_ad_categories: List[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Cria uma nova campanha.
    
    Args:
        name: Nome da campanha
        objective: CONVERSIONS, TRAFFIC, AWARENESS, LEAD_GENERATION
        budget: Orçamento diário em centavos (opcional)
        status: ACTIVE ou PAUSED (default: PAUSED)
        special_ad_categories: Categorias especiais
        
    Returns:
        Dict com campaign_id e status
        
    Raises:
        NeuroAdsError: Se criação falhar
    """
    url = f"{self.base_url}/act_{self.ad_account_id}/campaigns"
    
    data = {
        "name": name,
        "objective": objective,
        "status": status,
    }
    
    if budget:
        data["daily_budget"] = budget
    
    if special_ad_categories:
        data["special_ad_categories"] = special_ad_categories
    
    response = self.session.post(url, data=data)
    result = response.json()
    
    if "id" in result:
        return {
            "success": True,
            "campaign_id": result["id"],
            "name": name,
            "status": status
        }
    else:
        raise NeuroAdsError(
            message=result.get("error", {}).get("message", "Unknown error"),
            code=result.get("error", {}).get("code")
        )
```

### list_campaigns

```python
def list_campaigns(
    self,
    status: str = None,
    limit: int = 25,
    after: str = None,
    fields: List[str] = None
) -> Dict[str, Any]:
    """
    Lista campanhas da conta.
    
    Args:
        status: Filtro por status (ACTIVE, PAUSED, ALL)
        limit: Limite de resultados (default: 25)
        after: Cursor para paginação
        fields: Campos a retornar
        
    Returns:
        Dict com lista de campanhas e paginação
    """
    url = f"{self.base_url}/act_{self.ad_account_id}/campaigns"
    
    default_fields = ["id", "name", "status", "objective", "daily_budget", "created_time"]
    
    params = {
        "fields": ",".join(fields or default_fields),
        "limit": limit
    }
    
    if status and status != "ALL":
        params["filtering"] = json.dumps([{
            "field": "effective_status",
            "operator": "IN",
            "value": [status]
        }])
    
    if after:
        params["after"] = after
    
    response = self.session.get(url, params=params)
    result = response.json()
    
    campaigns = []
    for data in result.get("data", []):
        campaigns.append({
            "id": data.get("id"),
            "name": data.get("name"),
            "status": data.get("status"),
            "objective": data.get("objective"),
            "daily_budget": int(data.get("daily_budget", 0)) / 100,
            "created_time": data.get("created_time")
        })
    
    return {
        "campaigns": campaigns,
        "paging": result.get("paging", {})
    }
```

### get_campaign_insights

```python
def get_campaign_insights(
    self,
    campaign_id: str,
    date_range: str = "last_7d",
    metrics: List[str] = None,
    breakdowns: List[str] = None
) -> Dict[str, Any]:
    """
    Obtém insights de uma campanha.
    
    Args:
        campaign_id: ID da campanha
        date_range: last_7d, last_30d, today, lifetime
        metrics: Lista de métricas
        breakdowns: Lista de breakdowns
        
    Returns:
        Dict com métricas
    """
    url = f"{self.base_url}/{campaign_id}/insights"
    
    default_metrics = [
        "spend",
        "impressions",
        "clicks",
        "cpc",
        "cpm",
        "ctr",
        "reach",
        "frequency",
        "actions",
        "cost_per_action_type"
    ]
    
    params = {
        "date_preset": date_range,
        "fields": ",".join(metrics or default_metrics)
    }
    
    if breakdowns:
        params["breakdowns"] = ",".join(breakdowns)
    
    response = self.session.get(url, params=params)
    result = response.json()
    
    if not result.get("data"):
        return {"error": "No data found"}
    
    data = result["data"][0]
    
    # Processar actions
    actions = {}
    for action in data.get("actions", []):
        actions[action["action_type"]] = int(action["value"])
    
    # Processar cost_per_action_type
    cost_per_action = {}
    for cpa in data.get("cost_per_action_type", []):
        cost_per_action[cpa["action_type"]] = float(cpa["value"])
    
    return {
        "campaign_id": campaign_id,
        "spend": float(data.get("spend", 0)),
        "impressions": int(data.get("impressions", 0)),
        "clicks": int(data.get("clicks", 0)),
        "cpc": float(data.get("cpc", 0)),
        "cpm": float(data.get("cpm", 0)),
        "ctr": float(data.get("ctr", 0)),
        "reach": int(data.get("reach", 0)),
        "frequency": float(data.get("frequency", 0)),
        "actions": actions,
        "cost_per_action_type": cost_per_action
    }
```

### create_rule

```python
def create_rule(
    self,
    name: str,
    trigger: str,
    action: str,
    action_params: Dict = None,
    campaigns: List[str] = None,
    schedule: str = None,
    enabled: bool = True
) -> Dict[str, Any]:
    """
    Cria uma regra de automação.
    
    Args:
        name: Nome da regra
        trigger: Condição (ex: "cpa > 50")
        action: Ação (pause_campaign, increase_budget, send_notification)
        action_params: Parâmetros da ação
        campaigns: Lista de campaign_ids (None = todas)
        schedule: Cron expression (opcional)
        enabled: Se está ativa
        
    Returns:
        Dict com rule_id
    """
    rule = {
        "id": f"rule_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "name": name,
        "trigger": trigger,
        "action": action,
        "action_params": action_params or {},
        "campaigns": campaigns,
        "schedule": schedule,
        "enabled": enabled,
        "created_at": datetime.now().isoformat(),
        "last_executed": None,
        "execution_count": 0
    }
    
    # Salvar no storage
    self.rules.append(rule)
    self._save_rules()
    
    return {
        "success": True,
        "rule_id": rule["id"],
        "name": name
    }
```

### execute_rules

```python
def execute_rules(self, rule_ids: List[str] = None) -> Dict[str, Any]:
    """
    Executa regras de automação.
    
    Args:
        rule_ids: IDs específicos (None = todas ativas)
        
    Returns:
        Dict com resultados
    """
    results = {
        "executed": [],
        "actions_taken": [],
        "errors": []
    }
    
    rules_to_execute = [
        r for r in self.rules
        if r["enabled"] and (rule_ids is None or r["id"] in rule_ids)
    ]
    
    for rule in rules_to_execute:
        try:
            # Avaliar trigger
            trigger_result = self._evaluate_trigger(rule["trigger"])
            
            if trigger_result:
                # Executar ação
                action_result = self._execute_action(
                    rule["action"],
                    rule["action_params"],
                    rule["campaigns"]
                )
                
                results["executed"].append(rule["id"])
                results["actions_taken"].append({
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "action": rule["action"],
                    "result": action_result
                })
                
                # Atualizar regra
                rule["last_executed"] = datetime.now().isoformat()
                rule["execution_count"] += 1
        
        except Exception as e:
            results["errors"].append({
                "rule_id": rule["id"],
                "error": str(e)
            })
    
    self._save_rules()
    
    return results

def _evaluate_trigger(self, trigger: str) -> bool:
    """Avalia condição do trigger."""
    # Parse trigger expression
    # Ex: "cpa > 50" ou "roas > 3"
    parts = trigger.split()
    metric = parts[0]
    operator = parts[1]
    value = float(parts[2])
    
    # Obter valor atual
    current_value = self._get_current_metric(metric)
    
    # Avaliar condição
    if operator == ">":
        return current_value > value
    elif operator == "<":
        return current_value < value
    elif operator == ">=":
        return current_value >= value
    elif operator == "<=":
        return current_value <= value
    elif operator == "==":
        return current_value == value
    
    return False

def _execute_action(
    self,
    action: str,
    params: Dict,
    campaigns: List[str]
) -> Dict:
    """Executa ação da regra."""
    if action == "pause_campaign":
        for campaign_id in campaigns:
            self.update_campaign(campaign_id, status="PAUSED")
        return {"action": "pause_campaign", "campaigns": campaigns}
    
    elif action == "increase_budget":
        percentage = params.get("percentage", 20)
        for campaign_id in campaigns:
            campaign = self.get_campaign(campaign_id)
            new_budget = int(campaign["daily_budget"] * (1 + percentage / 100))
            self.update_campaign(campaign_id, budget=new_budget)
        return {"action": "increase_budget", "percentage": percentage}
    
    elif action == "send_notification":
        # Implementar notificação
        return {"action": "send_notification", "email": params.get("email")}
    
    return {"action": "unknown"}
```

### generate_report

```python
def generate_report(
    self,
    report_type: str = "performance",
    date_range: str = "last_7d",
    group_by: str = "campaign",
    metrics: List[str] = None,
    sort_by: str = "spend",
    limit: int = None
) -> Dict[str, Any]:
    """
    Gera relatório completo.
    
    Args:
        report_type: performance, creative, audience
        date_range: Período
        group_by: day, campaign, adset, ad
        metrics: Métricas a incluir
        sort_by: Métrica para ordenar
        limit: Limite de resultados
        
    Returns:
        Dict com summary, details, charts, recommendations
    """
    # Obter dados base
    if report_type == "performance":
        data = self._get_performance_data(date_range, group_by)
    elif report_type == "creative":
        data = self._get_creative_data(date_range, group_by)
    elif report_type == "audience":
        data = self._get_audience_data(date_range, group_by)
    else:
        data = self._get_performance_data(date_range, group_by)
    
    # Calcular summary
    summary = self._calculate_summary(data, metrics)
    
    # Ordenar dados
    sorted_data = sorted(data, key=lambda x: x.get(sort_by, 0), reverse=True)
    
    # Limitar resultados
    if limit:
        sorted_data = sorted_data[:limit]
    
    # Gerar charts config
    charts = self._generate_charts(sorted_data, metrics)
    
    # Gerar recomendações
    recommendations = self._generate_recommendations(data, summary)
    
    return {
        "summary": summary,
        "details": sorted_data,
        "charts": charts,
        "recommendations": recommendations
    }
```

## Rate Limiting

```python
class RateLimiter:
    """Gerencia rate limiting da API."""
    
    def __init__(self, calls_per_hour: int = 200, calls_per_day: int = 10000):
        self.calls_per_hour = calls_per_hour
        self.calls_per_day = calls_per_day
        self.hourly_calls = []
        self.daily_calls = []
    
    def can_make_call(self) -> bool:
        """Verifica se pode fazer chamada."""
        now = datetime.now()
        
        # Limpar calls antigas
        self.hourly_calls = [c for c in self.hourly_calls if (now - c).seconds < 3600]
        self.daily_calls = [c for c in self.daily_calls if (now - c).days < 1]
        
        # Verificar limites
        if len(self.hourly_calls) >= self.calls_per_hour:
            return False
        if len(self.daily_calls) >= self.calls_per_day:
            return False
        
        return True
    
    def record_call(self):
        """Registra chamada."""
        now = datetime.now()
        self.hourly_calls.append(now)
        self.daily_calls.append(now)
    
    def wait_if_needed(self):
        """Aguarda se necessário."""
        while not self.can_make_call():
            time.sleep(60)
```

## Error Handling

```python
class NeuroAdsError(Exception):
    """Erro do Neuro Ads Manager."""
    
    def __init__(self, message: str, code: int = None, subcode: int = None):
        self.message = message
        self.code = code
        self.subcode = subcode
        super().__init__(self.message)

def handle_api_error(response: Dict) -> None:
    """Trata erros da API."""
    error = response.get("error", {})
    
    if error:
        raise NeuroAdsError(
            message=error.get("message", "Unknown error"),
            code=error.get("code"),
            subcode=error.get("error_subcode")
        )
```

## Cache

```python
class InsightCache:
    """Cache para insights."""
    
    def __init__(self, max_age: int = 3600):
        self.cache = {}
        self.max_age = max_age
    
    def get(self, key: str) -> Optional[Dict]:
        """Obtém do cache."""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if (datetime.now() - timestamp).seconds < self.max_age:
                return data
        return None
    
    def set(self, key: str, data: Dict):
        """Salva no cache."""
        self.cache[key] = (data, datetime.now())
    
    def clear(self):
        """Limpa cache."""
        self.cache.clear()
```

## Licença

MIT License - ©2026 Monrars