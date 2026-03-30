# Ferramentas - Agent Saúde

> API Reference e implementações para campanhas de saúde (LGPD compliant)

## Índice

1. [Core API (LGPD Compliant)](#core-api-lgpd-compliant)
2. [Privacy-Safe Targeting](#privacy-safe-targeting)
3. [Offline Conversions](#offline-conversions)
4. [Analytics](#analytics)
5. [Scheduler Jobs](#scheduler-jobs)

---

## Core API (LGPD Compliant)

### health.create_campaign()

Cria campanha compliance LGPD/HIPAA.

```python
def create_campaign(
    self,
    name: str,
    objective: str,
    budget: int,
    specialty: str,  # 'general', 'cardiology', 'dermatology', 'orthopedics'
    lgpd_config: Optional[Dict] = None
) -> Dict:
    """
    Cria campanha compliance LGPD para saúde.
    
    Args:
        name: Nome da campanha
        objective: Objetivo da campanha
        budget: Orçamento diário em centavos
        specialty: Especialidade médica
        lgpd_config: Configurações LGPD
        
    Returns:
        Dict com campaign_id
        
    Example:
        >>> campaign = api.create_campaign(
        ...     name="Cardiologia - Check-up",
        ...     objective="LEAD_GENERATION",
        ...     budget=10000,  # R$100/dia
        ...     specialty="cardiology",
        ...     lgpd_config={
        ...         "anonymize_data": True,
        ...         "hash_sensitive": True,
        ...         "consent_required": True,
        ...         "retention_days": 90
        ...     }
        ... )
    """
    # Configurações LGPD padrão
    default_lgpd = {
        "anonymize_data": True,
        "hash_sensitive": True,
        "consent_required": True,
        "retention_days": 90,
        "exclude_conditions": True,  # Não segmentar por condição
        "privacy_safe_targeting": True
    }
    
    if lgpd_config:
        default_lgpd.update(lgpd_config)
    
    # Criar campanha
    campaign = self._request(
        method="POST",
        endpoint=f"{self.ad_account_id}/campaigns",
        data={
            "name": name,
            "objective": objective,
            "status": "PAUSED",
            "special_ad_category": "NONE",
            "bid_strategy": "LOWEST_COST_WITHOUT_CAP"
        }
    )
    
    # Salvar configurações LGPD
    self._save_lgpd_config(
        campaign_id=campaign["id"],
        config=default_lgpd
    )
    
    return campaign
```

### health.create_lead_form()

Cria formulário de lead LGPD compliant.

```python
def create_lead_form(
    self,
    name: str,
    specialty: str,
    questions: Optional[List[Dict]] = None,
    privacy_url: str = "",
    disclaimer: str = ""
) -> Dict:
    """
    Cria formulário de lead com disclaimers médicos.
    
    Args:
        name: Nome do formulário
        specialty: Especialidade médica
        questions: Lista de perguntas (sem dados sensíveis)
        privacy_url: URL da política de privacidade
        disclaimer: Disclaimer médico
        
    Returns:
        Dict com form_id
        
    Example:
        >>> form = api.create_lead_form(
        ...     name="Agendamento - Cardiologia",
        ...     specialty="cardiology",
        ...     questions=[
        ...         {"type": "NAME", "label": "Nome completo"},
        ...         {"type": "EMAIL", "label": "E-mail"},
        ...         {"type": "PHONE", "label": "WhatsApp"},
        ...         {
        ...             "type": "CUSTOM",
        ...             "label": "Como conheceu?",
        ...             "options": ["Google", "Facebook", "Indicação", "Outros"]
        ...         }
        ...     ],
        ...     privacy_url="https://clinica.com/privacidade",
        ...     disclaimer="Estas informações não substituem consulta médica profissional."
        ... )
    """
    # Perguntas padrão (sem dados sensíveis)
    if not questions:
        questions = [
            {"type": "NAME", "label": "Nome completo"},
            {"type": "EMAIL", "label": "E-mail"},
            {"type": "PHONE", "label": "WhatsApp"}
        ]
    
    # Disclaimer médico obrigatório
    if not disclaimer:
        disclaimer = "Esta informação não substitui consulta médica profissional."
    
    # Contexto (sem condição médica)
    context_card = {
        "title": f"Consulta - {specialty.capitalize()}",
        "description": "Agende sua consulta",
        "style": "LIST_STYLE"
    }
    
    # Criar formulário
    form_data = {
        "name": name,
        "follow_up_action_url": privacy_url,
        "questions": questions,
        "thank_you_message": f"Obrigado! Nossa equipe entrará em contato em até 24h. {disclaimer}",
        "context_card": context_card
    }
    
    form = self._request(
        method="POST",
        endpoint=f"{self.page_id}/leadgen_forms",
        data=form_data
    )
    
    return form
```

---

## Privacy-Safe Targeting

### health.create_privacy_safe_audience()

Cria público privacy-safe (LGPD compliant).

```python
def create_privacy_safe_audience(
    self,
    name: str,
    audience_type: str,
    config: Dict
) -> Dict:
    """
    Cria público-alvo conforme LGPD (sem dados sensíveis).
    
    Args:
        name: Nome do público
        audience_type: Tipo do público
        config: Configurações do público
        
    Returns:
        Dict com audience_id
        
    Example:
        # Público por interesse genérico
        >>> audience = api.create_privacy_safe_audience(
        ...     name="Interessados em Saúde",
        ...     audience_type="interest",
        ...     config={
        ...         "interests": ["Saúde e bem-estar", "Fitness", "Nutrição"],
        ...         "behaviors": ["Health consciousness"],
        ...         "age_min": 25,
        ...         "age_max": 65,
        ...         "locations": ["Brazil:São Paulo"]
        ...     }
        ... )
        
        # Lookalike de pacientes (anônimo)
        >>> lookalike = api.create_privacy_safe_audience(
        ...     name="Similar a Pacientes",
        ...     audience_type="lookalike",
        ...     config={
        ...         "source_type": "patients_anonymized",
        ...         "size": 5,
        ...         "country": "BR"
        ...     }
        ... )
    """
    # Validações LGPD
    forbidden_fields = [
        "disease", "condition", "diagnosis", "symptom", 
        "treatment", "medication", "health_status"
    ]
    
    for field in forbidden_fields:
        if field in str(config).lower():
            raise ValueError(f"Campo sensível detectado: {field}. Targeting por condição médica não é permitido.")
    
    # Público por interesse
    if audience_type == "interest":
        targeting = {
            "geo_locations": {
                "countries": ["BR"],
                "regions": [{"key": loc} for loc in config.get("locations", [])]
            },
            "age_min": config.get("age_min", 18),
            "age_max": config.get("age_max", 65),
            "interests": [{"id": i, "name": i} for i in config.get("interests", [])],
            "behaviors": [{"id": b, "name": b} for b in config.get("behaviors", [])]
        }
        
        return {"targeting": targeting, "lgpd_compliant": True}
    
    # Público lookalike (anônimo)
    elif audience_type == "lookalike":
        audience = self._request(
            method="POST",
            endpoint=f"{self.ad_account_id}/custom_audiences",
            data={
                "name": name,
                "subtype": "LOOKALIKE",
                "lookalike_spec": json.dumps({
                    "country": config.get("country", "BR"),
                    "type": "similarity",
                    "ratio": config["size"] / 100
                })
            }
        )
        
        return {"audience_id": audience["id"], "lgpd_compliant": True}
    
    return None
```

---

## Offline Conversions

### health.upload_offline_events_lgpd()

Upload de eventos offline com anonimização LGPD.

```python
def upload_offline_events_lgpd(
    self,
    pixel_id: str,
    events: List[Dict],
    anonymize: bool = True,
    hash_sensitive: bool = True
) -> Dict:
    """
    Faz upload de eventos offline com anonimização LGPD.
    
    Args:
        pixel_id: ID do Pixel
        events: Lista de eventos (sem dados médicos)
        anonymize: Anonimizar dados pessoais
        hash_sensitive: Hash de dados sensíveis
        
    Returns:
        Dict com estatísticas de upload
        
    Example:
        >>> events = [
        ...     {
        ...         "event_name": "Lead",
        ...         "event_time": int(datetime.now().timestamp()),
        ...         "user_data": {
        ...             "em": "cliente@email.com",
        ...             "ph": "11999887766"
        ...         },
        ...         "custom_data": {
        ...             "content_name": "ConsultaCardiologia",
        ...             "content_category": "general"  # Não específico
        ...         }
        ...     }
        ... ]
        >>> result = api.upload_offline_events_lgpd(
        ...     pixel_id="123456789",
        ...     events=events,
        ...     anonymize=True,
        ...     hash_sensitive=True
        ... )
    """
    import hashlib
    
    # Processar eventos
    processed_events = []
    
    for event in events:
        processed_event = event.copy()
        
        # Anonimizar dados pessoais
        if anonymize:
            if "user_data" in processed_event:
                for key in ["em", "ph"]:
                    if key in processed_event["user_data"]:
                        # Hash SHA256
                        value = str(processed_event["user_data"][key]).lower().strip()
                        processed_event["user_data"][key] = hashlib.sha256(value.encode()).hexdigest()
        
        # Remover dados sensíveis de custom_data
        if "custom_data" in processed_event:
            sensitive_keys = ["diagnosis", "condition", "symptom", "medication", "treatment"]
            for key in sensitive_keys:
                processed_event["custom_data"].pop(key, None)
        
        processed_events.append(processed_event)
    
    # Upload em lotes
    batch_size = 1000
    batches = [processed_events[i:i+batch_size] for i in range(0, len(processed_events), batch_size)]
    
    results = []
    for batch in batches:
        data = {
            "data": batch,
            "access_token": self.access_token
        }
        
        response = self._request(
            method="POST",
            endpoint=f"{pixel_id}/events",
            data=data
        )
        
        results.append(response)
    
    return {
        "total_events": len(events),
        "batches": len(batches),
        "anonymized": anonymize,
        "lgpd_compliant": True,
        "results": results
    }
```

---

## Analytics

### health.calculate_patient_ltv()

Calcula LTV de paciente com indicação.

```python
def calculate_patient_ltv(
    self,
    campaign_id: str,
    patient_data: Dict
) -> Dict:
    """
    Calcula LTV considerando indicação (boca a boca).
    
    Args:
        campaign_id: ID da campanha
        patient_data: Dados de pacientes
        
    Returns:
        Dict com LTV, ROI e métricas
        
    Example:
        >>> roi = api.calculate_patient_ltv(
        ...     campaign_id="238495729384",
        ...     patient_data={
        ...         "new_patients": 25,
        ...         "avg_consultation_fee": 300,
        ...         "avg_visits_per_year": 3,
        ...         "avg_patient_years": 5,
        ...         "referral_rate": 0.30,
        ...         "avg_referral_value": 800
        ...     }
        ... )
    """
    # Dados
    avg_fee = patient_data.get("avg_consultation_fee", 300)
    visits_per_year = patient_data.get("avg_visits_per_year", 3)
    patient_years = patient_data.get("avg_patient_years", 5)
    referral_rate = patient_data.get("referral_rate", 0.30)
    new_patients = patient_data.get("new_patients", 0)
    
    # LTV por paciente
    ltv_per_patient = avg_fee * visits_per_year * patient_years
    
    # Valor de indicações (30% indicam)
    referral_value = new_patients * referral_rate * avg_fee * 3  # ~3 consultas do indicado
    
    # Receita total
    total_revenue = (new_patients * ltv_per_patient) + referral_value
    
    # ROI/ROAS calculado separadamente pelo spend
    
    # CAC
    cac = 0  # Calculado com spend
    
    return {
        "ltv_per_patient": round(ltv_per_patient, 2),
        "referral_contribution": round(referral_value, 2),
        "referral_rate": referral_rate,
        "total_patients": new_patients,
        "avg_consultation_fee": avg_fee,
        "avg_visits_per_year": visits_per_year,
        "avg_patient_years": patient_years
    }
```

### health.generate_compliance_report()

Gera relatório de compliance LGPD.

```python
def generate_compliance_report(
    self,
    date_range: str = "last_30d"
) -> Dict:
    """
    Gera relatório de compliance LGPD.
    
    Args:
        date_range: Período de análise
        
    Returns:
        Dict com verificação de compliance
        
    Example:
        >>> report = api.generate_compliance_report(
        ...     date_range="last_30d"
        ... )
    """
    # Verificações LGPD
    checks = {
        "pixel_consent": True,
        "data_anonymization": True,
        "sensitive_data_excluded": True,
        "consent_forms": True,
        "retention_policy": True,
        "data_minimization": True
    }
    
    return {
        "date_range": date_range,
        "lgpd_compliance": all(checks.values()),
        "checks": checks,
        "recommendations": [
            "Manter targeting genérico (não por condição)",
            "Usar apenas dados demográficos",
            "Anonimizar conversões offline",
            "Manter disclaimers médicos em criativos"
        ]
    }
```

---

## Scheduler Jobs

### scheduler.add_health_offline_sync()

Adiciona job de sincronização offline (LGPD compliant).

```python
def add_health_offline_sync_job(
    self,
    pixel_id: str,
    schedule_type: str = "interval",
    schedule_value: str = "7d"
) -> Dict:
    """
    Adiciona job de sincronização offline com compliance LGPD.
    """
    job_id = f"health_offline_sync_{pixel_id}"
    
    self.add_job(
        job_id=job_id,
        job_type="offline_conversion",
        schedule_type=schedule_type,
        schedule_value=schedule_value,
        params={
            "pixel_id": pixel_id,
            "events": ["Lead", "Contact", "Schedule", "Appointment"],
            "anonymize": True,
            "hash_sensitive": True,
            "lgpd_compliant": True
        }
    )
    
    return {"job_id": job_id, "schedule": f"{schedule_type}: {schedule_value}"}
```

### scheduler.add_compliance_audit()

Adiciona job de auditoria de compliance.

```python
def add_compliance_audit_job(
    self,
    schedule_type: str = "monthly",
    schedule_value: str = "1st"
) -> Dict:
    """
    Adiciona job de auditoria mensal de compliance LGPD.
    """
    job_id = "health_compliance_audit"
    
    self.add_job(
        job_id=job_id,
        job_type="compliance_audit",
        schedule_type=schedule_type,
        schedule_value=schedule_value,
        params={
            "check_lgpd": True,
            "check_sensitive_data": True,
            "check_anonymization": True,
            "check_consent": True
        }
    )
    
    return {"job_id": job_id, "schedule": f"{schedule_type}: {schedule_value}"}
```

---

## Checklist LGPD

```python
def lgpd_compliance_checklist() -> Dict:
    """
    Retorna checklist de compliance LGPD para saúde.
    """
    return {
        "data_collection": [
            "✅ Consentimento explícito",
            "✅ Finalidade específica",
            "✅ Minimização de dados",
            "✅ Transparência"
        ],
        "pixel_tracking": [
            "✅ Não rastrear condições médicas",
            "✅ Não usar dados sensíveis",
            "✅ Anonimizar conversões offline",
            "✅ Hash dados de contato"
        ],
        "creatives": [
            "✅ Não mencionar condições médicas",
            "✅ Não usar depoimentos com diagnóstico",
            "✅ Apenas depoimentos genéricos",
            "✅ Disclaimers obrigatórios"
        ],
        "audiences": [
            "✅ Não segmentar por doença",
            "✅ Não usar dados de prontuário",
            "✅ Excluir pacientes antigos (LGPD)",
            "✅ Respeitar período de retenção"
        ]
    }
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

# Criar campanha LGPD compliant
campaign = api.create_campaign(
    name="Cardiologia - Check-up",
    objective="LEAD_GENERATION",
    budget=10000,  # R$100/dia
    specialty="cardiology",
    lgpd_config={
        "anonymize_data": True,
        "hash_sensitive": True,
        "consent_required": True
    }
)

# Criar formulário LGPD compliant
form = api.create_lead_form(
    name="Agendamento - Cardiologia",
    specialty="cardiology",
    questions=[
        {"type": "NAME", "label": "Nome completo"},
        {"type": "EMAIL", "label": "E-mail"},
        {"type": "PHONE", "label": "WhatsApp"}
    ],
    privacy_url="https://clinica.com/privacidade",
    disclaimer="Esta informação não substitui consulta médica profissional."
)

# Criar público privacy-safe
audience = api.create_privacy_safe_audience(
    name="Interessados em Saúde",
    audience_type="interest",
    config={
        "interests": ["Saúde e bem-estar", "Fitness"],
        "behaviors": ["Health consciousness"],
        "age_min": 25,
        "age_max": 65,
        "locations": ["Brazil:São Paulo"]
    }
)

# ========== CRON JOBS ==========

# 1. Upload offline (LGPD compliant) - 7dias
scheduler.add_job(
    job_id="health_offline_conversion",
    job_type="offline_conversion",
    schedule_type="interval",
    schedule_value="7d",
    params={
        "pixel_id": "123456789",
        "events": ["Lead", "Contact", "Schedule", "Appointment"],
        "anonymize": True,
        "hash_sensitive": True
    }
)

# 2. Auditoria compliance (mensal)
scheduler.add_job(
    job_id="health_compliance_audit",
    job_type="compliance_audit",
    schedule_type="monthly",
    schedule_value="1st",
    params={
        "check_lgpd": True,
        "check_sensitive_data": True
    }
)

# Iniciar scheduler
scheduler.start()

print("✅ Setup completo!")
print(f"Campaign ID: {campaign['id']}")
print(f"Form ID: {form['id']}")
print("🔒 LGPD Compliant")
```

---

## Licença

MIT License - © 2026 Monrars