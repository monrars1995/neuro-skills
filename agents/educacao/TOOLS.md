# Ferramentas - Agent Educação

> API Reference e implementações para campanhas de educação

## Índice

1. [Core API](#core-api)
2. [CRM Integration](#crm-integration)
3. [Seasonal Campaigns](#seasonal-campaigns)
4. [Analytics](#analytics)
5. [Scheduler Jobs](#scheduler-jobs)

---

## Core API

### education.create_campaign()

Cria uma campanha otimizada para educação.

```python
def create_campaign(
    self,
    name: str,
    objective: str,  # 'LEAD_GENERATION', 'CONVERSIONS', 'TRAFFIC'
    budget: int,  # em centavos
    institution_type: str,  # 'idiomas', 'cursos_livres', 'graduacao', 'pos_graduacao', 'technical'
    special_config: Optional[Dict] = None
) -> Dict:
    """
    Cria campanha com configurações específicas para educação.
    
    Args:
        name: Nome da campanha
        objective: Objetivo da campanha
        budget: Orçamento diário em centavos
        institution_type: Tipo de instituição
        special_config: Configurações especiais
        
    Returns:
        Dict com campaign_id, adset_id, creative_ids
        
    Example:
        >>> campaign = api.create_campaign(
        ...     name="Vestibular 2024 - Direito",
        ...     objective="LEAD_GENERATION",
        ...     budget=20000,  # R$200/dia
        ...     institution_type="graduacao",
        ...     special_config={
        ...         "attribution_window": 30,
        ...         "offline_conversion": True,
        ...         "seasonal": True,
        ...         "course_id": "CURSO_DIREITO"
        ...     }
        ... )
    """
    # Configurações por tipo de instituição
    configs = {
        "idiomas": {
            "attribution": 30,
            "cycle": "7-30 dias",
            "budget_range": (10000, 30000)
        },
        "cursos_livres": {
            "attribution": 14,
            "cycle": "1-14 dias",
            "budget_range": (5000, 20000)
        },
        "graduacao": {
            "attribution": 90,
            "cycle": "30-90 dias",
            "budget_range": (20000, 100000)
        },
        "pos_graduacao": {
            "attribution": 60,
            "cycle": "14-60 dias",
            "budget_range": (15000, 80000)
        },
        "technical": {
            "attribution": 45,
            "cycle": "7-30 dias",
            "budget_range": (10000, 50000)
        }
    }
    
    config = configs.get(institution_type, configs["cursos_livres"])
    
    # Configurações padrão
    default_config = {
        "attribution_spec": [
            {"event_type": "conversion", "window_days": config["attribution"]}
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

### education.create_lead_form()

Cria formulário de Lead otimizado para educação.

```python
def create_lead_form(
    self,
    name: str,
    course_info: Dict,
    questions: Optional[List[Dict]] = None,
    privacy_url: str = "",
    thankyou_message: str = ""
) -> Dict:
    """
    Cria formulário de lead com campos específicos para educação.
    
    Args:
        name: Nome do formulário
        course_info: Informações do curso
        questions: Lista de perguntas (opcional)
        privacy_url: URL da política de privacidade
        thankyou_message: Mensagem de agradecimento
        
    Returns:
        Dict com form_id e leadgen_form_id
        
    Example:
        >>> form = api.create_lead_form(
        ...     name="Interesse - Direito 2024",
        ...     course_info={
        ...         "name": "Direito",
        ...         "type": "graduacao",
        ...         "duration": "5 anos",
        ...         "modality": "Presencial",
        ...         "price": "R$ 2.500/mês"
        ...     },
        ...     questions=[
        ...         {"type": "NAME", "label": "Nome completo"},
        ...         {"type": "EMAIL", "label": "E-mail"},
        ...         {"type": "PHONE", "label": "WhatsApp"},
        ...         {
        ...             "type": "CUSTOM",
        ...             "label": "Como conheceu?",
        ...             "options": ["Google", "Facebook", "Indicação", "Outros"]
        ...         },
        ...         {
        ...             "type": "CUSTOM",
        ...             "label": "Turno de interesse",
        ...             "options": ["Manhã", "Noite", "EAD"]
        ...         }
        ...     ],
        ...     privacy_url="https://faculdade.com/privacidade",
        ...     thankyou_message="Obrigado! Nossa equipe entrará em contato em até 24h."
        ... )
    """
    # Perguntas padrão para educação
    if not questions:
        questions = [
            {"type": "NAME", "label": "Nome completo"},
            {"type": "EMAIL", "label": "E-mail"},
            {"type": "PHONE", "label": "WhatsApp"},
            {
                "type": "CUSTOM",
                "label": "Como conheceu?",
                "options": ["Google", "Facebook", "Indicação", "Outros"]
            }
        ]
    
    # Contexto do curso
    context_card = {
        "title": f"{course_info['name']} - {course_info['type']}",
        "subtitle": f"Duração: {course_info['duration']} | {course_info['modality']}",
        "description": f"Investimento: {course_info['price']}",
        "style": "LIST_STYLE"
    }
    
    # Criar formulário
    form_data = {
        "name": name,
        "follow_up_action_url": privacy_url,
        "questions": questions,
        "thank_you_message": thankyou_message,
        "context_card": context_card
    }
    
    form = self._request(
        method="POST",
        endpoint=f"{self.page_id}/leadgen_forms",
        data=form_data
    )
    
    return form
```

### education.create_audience()

Cria público-alvo otimizado para educação.

```python
def create_audience(
    self,
    name: str,
    audience_type: str,  # 'custom', 'lookalike', 'interest'
    institution_type: str,
    config: Dict
) -> Dict:
    """
    Cria público-alvo com segmentação específica para educação.
    
    Args:
        name: Nome do público
        audience_type: Tipo do público
        institution_type: Tipo de instituição
        config: Configurações do público
        
    Returns:
        Dict com audience_id
        
    Example:
        # Público por interesses
        >>> audience = api.create_audience(
        ...     name="Interessados em Direito",
        ...     audience_type="interest",
        ...     institution_type="graduacao",
        ...     config={
        ...         "interests": ["Direito", "Faculdade de Direito", "Advocacia"],
        ...         "education_level": ["High school", "College grad"],
        ...         "life_events": ["Recently moved"],
        ...         "age_min": 18,
        ...         "age_max": 40,
        ...         "locations": ["Brazil:São Paulo"]
        ...     }
        ... )
        
        # Lookalike de alunos
        >>> lookalike = api.create_audience(
        ...     name="Similar a Alunos 5%",
        ...     audience_type="lookalike",
        ...     institution_type="graduacao",
        ...     config={
        ...         "source_audience": "students_365days",
        ...         "size": 5,
        ...         "country": "BR"
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
                "rule": config.get("rule", {})
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
            "education_statuses": config.get("education_level", []),
            "life_events": [{"id": le, "name": le} for le in config.get("life_events", [])]
        }
        
        return {"targeting": targeting}
    
    return audience
```

---

## CRM Integration

### crm.sync_students()

Sincroniza dados de alunos do CRM.

```python
def sync_students_to_offline(
    self,
    pixel_id: str,
    crm_config: Dict,
    events: List[str] = None,
    days: int = 7
) -> Dict:
    """
    Sincroniza eventos de alunos do CRM para conversões offline.
    
    Args:
        pixel_id: ID do Pixel
        crm_config: Configuração do CRM
        events: Lista de eventos
        days: Número de dias para sincronizar
        
    Returns:
        Dict com estatísticas de sincronização
        
    Example:
        >>> result = api.sync_students_to_offline(
        ...     pixel_id="123456789",
        ...     crm_config={
        ...         "type": "salesforce",
        ...         "api_key": "...",
        ...         "instance_url": "..."
        ...     },
        ...     events=["Lead", "Registration", "Payment"],
        ...     days=7
        ... )
    """
    from datetime import datetime, timedelta
    
    # Eventos padrão
    if not events:
        events = ["Lead", "Registration", "Payment", "Enrollment"]
    
    # Data de início
    start_date = datetime.now() - timedelta(days=days)
    
    # Buscar dados do CRM
    crm_data = self._fetch_crm_data(
        crm_config=crm_config,
        start_date=start_date,
        events=events
    )
    
    # Converter para formato Meta
    meta_events = []
    for record in crm_data:
        meta_event = {
            "event_name": record["event_name"],
            "event_time": int(record["event_time"].timestamp()),
            "user_data": {
                "em": hash_sha256(record["email"]),
                "ph": hash_sha256(record["phone"])
            },
            "custom_data": {
                "content_name": record.get("course_name", ""),
                "content_category": record.get("course_type", ""),
                "value": record.get("value", 0),
                "currency": "BRL"
            }
        }
        meta_events.append(meta_event)
    
    # Enviar para Meta
    result = self.upload_offline_events(
        pixel_id=pixel_id,
        events=meta_events
    )
    
    return {
        "total_records": len(crm_data),
        "events_sent": len(meta_events),
        "events": events,
        "start_date": start_date.isoformat(),
        "result": result
    }
```

### crm.update_vacancies()

Atualiza vagas disponíveis.

```python
def update_course_vacancies(
    self,
    courses: List[Dict]
) -> Dict:
    """
    Atualiza vagas disponíveis nos cursos.
    
    Args:
        courses: Lista de cursos com vagas
        
    Returns:
        Dict com estatísticas de atualização
        
    Example:
        >>> result = api.update_course_vacancies(
        ...     courses=[
        ...         {"id": "CURSO_123", "vacancies": 50},
        ...         {"id": "CURSO_456", "vacancies": 30}
        ...     ]
        ... )
    """
    results = []
    
    for course in courses:
        # Atualizar no CRM
        result = self._update_crm_vacancy(
            course_id=course["id"],
            vacancies=course["vacancies"]
        )
        results.append(result)
        
        # Pausar campanha se não houver vagas
        if course["vacancies"] == 0:
            self._pause_campaign_for_course(course["id"])
    
    return {
        "total_courses": len(courses),
        "updated": len(results),
        "results": results
    }
```

---

## Seasonal Campaigns

### seasonal.create_vestibular_campaign()

Cria campanha sazonal de vestibular.

```python
def create_vestibular_campaign(
    self,
    year: int,
    courses: List[str],
    budget: int,
    start_date: str,
    end_date: str
) -> Dict:
    """
    Cria campanha de vestibular com fases.
    
    Args:
        year: Ano do vestibular
        courses: Lista de cursos
        budget: Orçamento total (centavos)
        start_date: Data de início
        end_date: Data de término
        
    Returns:
        Dict com campaign_ids
        
    Example:
        >>> campaign = api.create_vestibular_campaign(
        ...     year=2024,
        ...     courses=["Direito", "Medicina", "Engenharia"],
        ...     budget=3000000,  # R$30.000 total
        ...     start_date="2024-11-01",
        ...     end_date="2025-01-31"
        ... )
    """
    from datetime import datetime, timedelta
    
    # Calcular fases
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    total_days = (end - start).days
    
    # Dividir orçamento por fase
    phases = [
        {"name": "Awareness", "days": int(total_days * 0.3), "budget": int(budget * 0.2)},
        {"name": "Consideration", "days": int(total_days * 0.4), "budget": int(budget * 0.4)},
        {"name": "Conversion", "days": total_days - int(total_days * 0.3) - int(total_days * 0.4), "budget": int(budget * 0.4)}
    ]
    
    campaign_ids = []
    current_date = start
    
    for phase in phases:
        # Criar campanha da fase
        campaign = self.create_campaign(
            name=f"Vestibular {year} - {phase['name']}",
            objective="LEAD_GENERATION" if phase["name"] != "Conversion" else "CONVERSIONS",
            budget=int(phase["budget"] / phase["days"]),  # Daily budget
            institution_type="graduacao",
            special_config={
                "start_time": current_date.isoformat(),
                "end_time": (current_date + timedelta(days=phase["days"])).isoformat(),
                "courses": courses
            }
        )
        
        campaign_ids.append({
            "phase": phase["name"],
            "campaign_id": campaign["id"],
            "start_date": current_date.isoformat(),
            "end_date": (current_date + timedelta(days=phase["days"])).isoformat()
        })
        
        current_date += timedelta(days=phase["days"])
    
    return {
        "year": year,
        "courses": courses,
        "total_budget": budget,
        "phases": campaign_ids
    }
```

### seasonal.create_back_to_school_campaign()

Cria campanha de volta às aulas.

```python
def create_back_to_school_campaign(
    self,
    institution_type: str,
    budget: int,
    month: int = 1  # Janeiro
) -> Dict:
    """
    Cria campanha de volta às aulas.
    
    Args:
        institution_type: Tipo de instituição
        budget: Orçamento diário (centavos)
        month: Mês de início (padrão: Janeiro)
        
    Returns:
        Dict com campaign_id
        
    Example:
        >>> campaign = api.create_back_to_school_campaign(
        ...     institution_type="idiomas",
        ...     budget=15000,  # R$150/dia
        ...     month=1
        ... )
    """
    # Configurações por tipo
    configs = {
        "idiomas": {
            "interests": ["Inglês", "Espanhol", "Curso de idiomas"],
            "offers": ["Matrícula grátis", "Material incluso", "Desconto 20%"]
        },
        "cursos_livres": {
            "interests": ["Cursos", "Aprendizado", "Carreira"],
            "offers": ["Desconto especial", "Turma nova"]
        },
        "technical": {
            "interests": ["Curso técnico", "Profissão", "Carreira"],
            "offers": ["Matrícula grátis", "Bolsa de estudo"]
        }
    }
    
    config = configs.get(institution_type, configs["cursos_livres"])
    
    # Criar campanha
    campaign = self.create_campaign(
        name=f"Volta às Aulas - {institution_type.capitalize()}",
        objective="LEAD_GENERATION",
        budget=budget,
        institution_type=institution_type,
        special_config={
            "seasonal": True,
            "season": "back_to_school",
            "offers": config["offers"]
        }
    )
    
    # Criar público
    audience = self.create_audience(
        name=f"Volta às Aulas - {institution_type.capitalize()}",
        audience_type="interest",
        institution_type=institution_type,
        config={
            "interests": config["interests"],
            "life_events": ["Starting new job", "Recently moved"],
            "age_min": 18,
            "age_max": 45
        }
    )
    
    return {
        "campaign_id": campaign["id"],
        "audience": audience,
        "offers": config["offers"]
    }
```

---

## Analytics

### analytics.calculate_enrollment_roi()

Calcula ROI específico para matrículas com LTV.

```python
def calculate_enrollment_roi(
    self,
    campaign_id: str,
    date_range: str = "last_30d",
    enrollment_data: Optional[Dict] = None
) -> Dict:
    """
    Calcula ROI considerando LTV por aluno.
    
    Args:
        campaign_id: ID da campanha
        date_range: Período de análise
        enrollment_data: Dados de matrícula (opcional)
        
    Returns:
        Dict com ROI, ROAS e métricas
        
    Example:
        >>> roi = api.calculate_enrollment_roi(
        ...     campaign_id="238495729384",
        ...     date_range="last_30d",
        ...     enrollment_data={
        ...         "enrollments": 20,
        ...         "monthly_fee": 800,
        ...         "duration_months": 48,
        ...         "retention_rate": 0.75,
        ...         "completion_rate": 0.60
        ...     }
        ... )
    """
    # Buscar métricas da campanha
    metrics = self._request(
        method="GET",
        endpoint=f"{campaign_id}/insights",
        params={
            "date_preset": date_range,
            "fields": "spend,impressions,clicks,leads"
        }
    )
    
    # Dados de matrícula padrão
    if not enrollment_data:
        enrollment_data = {
            "enrollments": 10,
            "monthly_fee": 800,
            "duration_months": 48,
            "retention_rate": 0.75,
            "completion_rate": 0.60
        }
    
    # Cálculos
    spend = float(metrics["spend"])
    
    # LTV por aluno
    monthly_fee = enrollment_data["monthly_fee"]
    duration = enrollment_data["duration_months"]
    retention = enrollment_data["retention_rate"]
    completion = enrollment_data["completion_rate"]
    enrollments = enrollment_data["enrollments"]
    
    expected_months = duration * retention
    ltv_per_student = monthly_fee * expected_months
    
    # Alunos que concluem (bônus)
    completing = enrollments * completion
    completion_bonus = completing * monthly_fee * 6  # 6 meses extras
    
    # Receita total
    total_revenue = (enrollments * ltv_per_student) + completion_bonus
    
    # ROI e ROAS
    roi_percentage = ((total_revenue - spend) / spend) * 100 if spend > 0 else 0
    roas = total_revenue / spend if spend > 0 else 0
    
    # CAC (Custo de Aquisição de Aluno)
    cac = spend / enrollments if enrollments > 0 else 0
    
    # Payback em meses
    payback_months = cac / monthly_fee if monthly_fee > 0 else 0
    
    # LTV/CAC ratio
    ltv_cac_ratio = ltv_per_student / cac if cac > 0 else 0
    
    return {
        "total_revenue": round(total_revenue, 2),
        "roi_percentage": round(roi_percentage, 2),
        "roas": round(roas, 2),
        "cac": round(cac, 2),
        "ltv_per_student": round(ltv_per_student, 2),
        "ltv_cac_ratio": round(ltv_cac_ratio, 2),
        "payback_months": round(payback_months, 2),
        "enrollments": enrollments,
        "retention_rate": retention,
        "spend": round(spend, 2)
    }
```

---

## Scheduler Jobs

### scheduler.add_enrollment_sync()

Adiciona job de sincronização de matrículas.

```python
def add_enrollment_sync_job(
    self,
    pixel_id: str,
    crm_config: Dict,
    schedule_type: str = "interval",
    schedule_value: str = "7d"
) -> Dict:
    """
    Adiciona job de sincronização de matrículas.
    
    Args:
        pixel_id: ID do Pixel
        crm_config: Configuração do CRM
        schedule_type: Tipo de agendamento
        schedule_value: Valor do agendamento
        
    Returns:
        Dict com job_id
    """
    job_id = f"education_enrollment_sync_{pixel_id}"
    
    self.add_job(
        job_id=job_id,
        job_type="offline_conversion",
        schedule_type=schedule_type,
        schedule_value=schedule_value,
        params={
            "pixel_id": pixel_id,
            "crm_config": crm_config,
            "events": ["Lead", "Registration", "Payment", "Enrollment"]
        }
    )
    
    return {"job_id": job_id, "schedule": f"{schedule_type}: {schedule_value}"}
```

### scheduler.add_vacancy_check()

Adiciona job de verificação de vagas.

```python
def add_vacancy_check_job(
    self,
    courses: List[Dict],
    schedule_type: str = "daily",
    schedule_value: str = "08:00"
) -> Dict:
    """
    Adiciona job de verificação de vagas.
    
    Args:
        courses: Lista de cursos com limite de vagas
        schedule_type: Tipo de agendamento
        schedule_value: Valor do agendamento
        
    Returns:
        Dict com job_id
    """
    job_id = "education_vacancy_check"
    
    self.add_job(
        job_id=job_id,
        job_type="vacancy_check",
        schedule_type=schedule_type,
        schedule_value=schedule_value,
        params={
            "courses": courses,
            "pause_if_full": True
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

# Criar campanha de vestibular
vestibular = api.create_vestibular_campaign(
    year=2024,
    courses=["Direito", "Medicina", "Engenharia"],
    budget=3000000,  # R$30.000 total
    start_date="2024-11-01",
    end_date="2025-01-31"
)

# Criar lead form
form = api.create_lead_form(
    name="Interesse - Direito 2024",
    course_info={
        "name": "Direito",
        "type": "graduacao",
        "duration": "5 anos",
        "modality": "Presencial",
        "price": "R$ 2.500/mês"
    },
    questions=[
        {"type": "NAME", "label": "Nome completo"},
        {"type": "EMAIL", "label": "E-mail"},
        {"type": "PHONE", "label": "WhatsApp"},
        {
            "type": "CUSTOM",
            "label": "Como conheceu?",
            "options": ["Google", "Facebook", "Indicação", "Outros"]
        }
    ],
    privacy_url="https://faculdade.com/privacidade",
    thankyou_message="Obrigado! Nossa equipe entrará em contato."
)

# Criar público
audience = api.create_audience(
    name="Interessados em Direito",
    audience_type="interest",
    institution_type="graduacao",
    config={
        "interests": ["Direito", "Faculdade de Direito", "Advocacia"],
        "education_level": ["High school", "College grad"],
        "age_min": 18,
        "age_max": 40,
        "locations": ["Brazil:São Paulo"]
    }
)

# ========== CRON JOBS ==========

# 1. Sincronização de matrículas (7dias)
scheduler.add_job(
    job_id="education_enrollment_sync",
    job_type="offline_conversion",
    schedule_type="interval",
    schedule_value="7d",
    params={
        "pixel_id": "123456789",
        "events": ["Lead", "Registration", "Payment"]
    }
)

# 2. Verificação de vagas (diário)
scheduler.add_job(
    job_id="education_vacancy_check",
    job_type="vacancy_check",
    schedule_type="daily",
    schedule_value="08:00",
    params={
        "courses": [
            {"id": "CURSO_123", "vacancies": 50},
            {"id": "CURSO_456", "vacancies": 30}
        ]
    }
)

# 3. Campanha sazonal (todo ano em Novembro)
scheduler.add_job(
    job_id="education_vestibular_campaign",
    job_type="seasonal_launch",
    schedule_type="yearly",
    schedule_value="november 01",
    params={
        "campaign_name": "Vestibular 2024",
        "courses": ["Direito", "Medicina", "Engenharia"]
    }
)

# Iniciar scheduler
scheduler.start()

print("✅ Setup completo!")
```

---

## Licença

MIT License - © 2026 Monrars