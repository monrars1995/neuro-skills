# Agent de Campanhas - Educação

> Especializado em campanhas para escolas, cursos e faculdades

**Versão:** 1.0.0  
**Vertical:** Educação  
**Autor:** Monrars (@monrars)

## Características do Vertical

### Jornada de Matrícula (Medium Cycle)

```
Interesse → Pesquisa → Informações → Matrícula → Pagamento → Início
    ↓          ↓            ↓            ↓           ↓         ↓
  7-30dias   7-14dias     1-7dias      1-7dias     1-30dias   Contínuo
```

### Eventos e Timing

| Evento | Frequência | Importância | Offline? |
|--------|------------|-------------|----------|
| Page View | Alta | Média | Não |
| View Content (curso) | Média | Alta | Não |
| Lead (form) | Média | Muito Alta | Não |
| WhatsApp Contact | Média | Alta | Não |
| Matrícula | Baixa | Crítica | **Sim** |
| Pagamento | Baixa | Crítica | **Sim** |

### Tipos de Instituição

```yaml
institution_types:
  idiomas:
    cycle: "7-30 dias"
    ticket: "R$200-800/mês"
    model: "assinatura"
    
  cursos_livres:
    cycle: "1-14 dias"
    ticket: "R$500-5000"
    model: "pagamento único"
    
  graduacao:
    cycle: "30-90 dias"
    ticket: "R$500-2000/mês"
    model: "mensalidade"
    
  pos_graduacao:
    cycle: "14-60 dias"
    ticket: "R$800-3000/mês"
    model: "mensalidade"
    
  technical:
    cycle: "7-30 dias"
    ticket: "R$300-1500/mês"
    model: "mensalidade"
```

### Diferenças vs Outros Verticais

| Aspecto | E-commerce | Educação |
|---------|-----------|----------|
| Ciclo de venda | 1-7 dias | **7-90 dias** |
| Ticket médio | R$100-5000 | **R$500-50000/ano** |
| Modelo de receita | Único | **Recorrente (LTV)** |
| Sazonalidade | Baixa | **Muito Alta** |
| Conversão offline | Raro | **Comum** |
| Janela de atribuição | 7-30 dias | **30-90 dias** |

## Sazonalidade por Tipo

### Idiomas

```yaml
high_season:
  - Janeiro: "Volta às aulas"
  - Julho: "Férias de inverno"
  - Dezembro: "Férias de verão"
  
low_season:
  - Março-Maio: "Período letivo"
  - Agosto-Outubro: "Segundo semestre"
```

### Graduação/Pós

```yaml
high_season:
  - Novembro-Janeiro: "Vestibular/1º semestre"
  - Junho-Agosto: "2º semestre"
  
critical_dates:
  - "Resultado vestibular"
  - "Matrícula aberta"
  - "Início das aulas"
  - "Últimas vagas"
```

### Cursos Livres

```yaml
high_season:
  - Janeiro: "Año novo, novas habilidades"
  - Julho: "Férias"
  - Setembro: "2º semestre"
  
opportunities:
  - "Black Friday"
  - "Volta às aulas"
  - "Férias"
```

## Configurações Recomendadas

### 1. Janela de Atribuição

```yaml
attribution_window:
  idiomas:
    click_through: 7
    view_through: 1
    conversion_window: 30
    
  graduacao:
    click_through: 30
    view_through: 7
    conversion_window: 90
    
  cursos_livres:
    click_through: 14
    view_through: 3
    conversion_window: 45
```

### 2. Objetivos de Campanha

**Principais:**
- `LEAD_GENERATION` - Capturar contatos
- `CONVERSIONS` - Matrícula online

**Secundários:**
- `TRAFFIC` - Direcionar para site
- `VIDEO_VIEWS` - Tours virtuais

### 3. Pixel Events

```javascript
// Eventos principais
fbq('track', 'PageView');
fbq('track', 'ViewContent', {
  content_ids: ['CURSO_123'],
  content_type: 'course',
  content_name: 'Inglês Avançado',
  content_category: 'Idiomas',
  value: 800,
  currency: 'BRL'
});

fbq('track', 'Lead', {
  content_name: 'Interesse em Inglês',
  content_category: 'Idiomas',
  course_id: 'CURSO_123'
});

fbq('track', 'CompleteRegistration', {
  content_name: 'Matrícula - Inglês Avançado',
  content_category: 'Idiomas',
  value: 800,
  currency: 'BRL',
  course_id: 'CURSO_123'
});

// Matrícula offline (CRM)
// Ver seção Offline Conversion
```

## Estratégias de Campanha

### 1. Topo de Funil (Awareness)

**Objetivo:** `REACH` ou `VIDEO_VIEWS`

**Público:**
```yaml
targeting:
  interests:
    - "{curso}"
    - "Educação"
    - "Faculdade"
    - "Aprendizado"
    - "Carreira"
  education_level:
    - "High school"
    - "College grad"
  age_min: 18
  age_max: 45
  locations:
    - "Brazil:{região}"
```

**Orçamento:** R$30-80/dia

**Criativo:**
- Depoimentos de alunos
- Tours virtuais
- Aulão demonstrativo
- Cases de sucesso

### 2. Meio de Funil (Consideração)

**Objetivo:** `LEAD_GENERATION`

**Público:**
```yaml
targeting:
  custom_audiences:
    - "Visitantes Site (14 dias)"
    - "ViewContent (7 dias)"
    - "Similar a Alunos (3%)"
  exclusions:
    - "Matriculados (365 dias)"
```

**Orçamento:** R$50-150/dia

**Lead Forms:**
- Interesse em curso
- Simulação de mensalidade
- Agendamento de visita
- Download de material

### 3. Fundo de Funil (Conversão)

**Objetivo:** `CONVERSIONS` (Matrícula)

**Público:**
```yaml
targeting:
  custom_audiences:
    - "Leads (30 dias)"
    - "Interessados WhatsApp (7 dias)"
    - "Visitantes Virtual Tour (14 dias)"
  exclusions:
    - "Matriculados (365 dias)"
```

**Orçamento:** R$100-300/dia

**Estratégia:**
- Remarketing de interesse
- Desconto por tempo limitado
- Bolsa de estudo
- Financiamento facilitado

## Cron Jobs Específicos

### Job 1: Upload de Conversões Offline (7dias)

```python
scheduler.add_job(
    job_id="education_offline_conversion",
    job_type="offline_conversion",
    schedule_type="interval",
    schedule_value="7d",
    params={
        "pixel_id": "{PIXEL_ID}",
        "events": [
            {"name": "Lead", "source": "form"},
            {"name": "WhatsApp", "source": "whatsapp"},
            {"name": "Visit", "source": "crm"},
            {"name": "Registration", "source": "crm"},
            {"name": "Payment", "source": "financeiro"}
        ],
        "match_keys": ["em", "ph"],
        "course_data": True
    }
)
```

### Job 2: Relatório de Matrículas (Semanal)

```python
scheduler.add_job(
    job_id="education_weekly_report",
    job_type="report",
    schedule_type="weekly",
    schedule_value="monday 09:00",
    params={
        "report_type": "enrollment",
        "date_range": "last_7d",
        "kpis": [
            "leads",
            "whatsapp_contacts",
            "visits",
            "registrations",
            "payments",
            "cost_per_lead",
            "cost_per_registration"
        ],
        "breakdown": "course",
        "email": "diretor@escola.com"
    }
)
```

### Job 3. Auditoria de Vagas (Diário)

```python
scheduler.add_job(
    job_id="education_vacancy_audit",
    job_type="vacancy_audit",
    schedule_type="daily",
    schedule_value="08:00",
    params={
        "check_availability": True,
        "courses": ["CURSO_123", "CURSO_456"],
        "min_vacancies": 5,
        "pause_if_full": True
    }
)
```

### Job 4. Campanha Sazonal

```python
scheduler.add_job(
    job_id="education_seasonal_campaign",
    job_type="seasonal_launch",
    schedule_type="yearly",
    schedule_value="november 01",  # Vestibular
    params={
        "campaign_name": "Vestibular 2024",
        "objective": "LEAD_GENERATION",
        "budget": 20000,
        "courses": ["Direito", "Medicina", "Engenharia"],
        "duration_days": 90,
        "landing_page": "https://faculdade.com/vestibular"
    }
)
```

## Modelo de ROI/ROAS

### Cálculo para Educação (LTV):

```python
def calculate_education_roi(spend, enrollment_data):
    """
    Calcula ROI considerando:
    - Valor da matrícula (mensalidade)
    - Duração do curso
    - Taxa de retenção
    - Taxa de conclusão
    """
    # Dados
    monthly_fee = enrollment_data.get('monthly_fee', 800)
    course_duration = enrollment_data.get('duration_months', 48)  # meses
    retention_rate = enrollment_data.get('retention_rate', 0.75)  # 75%
    completion_rate = enrollment_data.get('completion_rate', 0.60)  # 60%
    enrollments = enrollment_data.get('enrollments', 0)
    
    # Receita total esperada (LTV)
    expected_months = course_duration * retention_rate
    ltv_per_student = monthly_fee * expected_months
    
    # Alunos que concluem (bônus de retenção)
    completing_students = enrollments * completion_rate
    completion_bonus_months = 6  # meses extras de retenção
    completion_bonus = completing_students * monthly_fee * completion_bonus_months
    
    # Receita total
    total_revenue = (enrollments * ltv_per_student) + completion_bonus
    
    # ROI e ROAS
    roi = ((total_revenue - spend) / spend) * 100 if spend > 0 else 0
    roas = total_revenue / spend if spend > 0 else 0
    
    # CAC (Custo de Aquisição de Aluno)
    cac = spend / enrollments if enrollments > 0 else 0
    
    # Payback em meses
    payback_months = cac / monthly_fee if monthly_fee > 0 else 0
    
    return {
        "total_revenue": round(total_revenue, 2),
        "roi_percentage": round(roi, 2),
        "roas": round(roas, 2),
        "cac": round(cac, 2),
        "ltv": round(ltv_per_student, 2),
        "ltv_cac_ratio": round(ltv_per_student / cac, 2) if cac > 0 else 0,
        "payback_months": round(payback_months, 2),
        "enrollments": enrollments,
        "retention_rate": retention_rate
    }

# Exemplo
result = calculate_education_roi(
    spend=10000,
    enrollment_data={
        'enrollments': 20,
        'monthly_fee': 800,
        'duration_months': 48,
        'retention_rate': 0.75,
        'completion_rate': 0.60
    }
)

# Resultado:
# {
#   "total_revenue": 310400,     # R$310.400
#   "roi_percentage": 3004,       # 3004% ROI
#   "roas": 31.04,                # 31.04x ROAS
#   "cac": 500,                    # R$500 por aluno
#   "ltv": 28800,                  # R$28.800 LTV
#   "ltv_cac_ratio": 57.6,         # 57.6x LTV/CAC
#   "payback_months": 0.625,       # Payback em 0.625 meses (~20 dias)
#   "enrollments": 20,
#   "retention_rate": 0.75
# }
```

## Estratégias Sazonais

### Vestibular (Nov-Jan)

```yaml
campaign:
  name: "Vestibular 2024"
  objective: "LEAD_GENERATION"
  budget: 30000
  
phases:
  - phase: "Awareness"
    dates: "Nov 1-15"
    targeting: "Ampla"
    creative: "Aulão gratuito"
    
  - phase: "Consideration"
    dates: "Nov 16 - Dez 15"
    targeting: "Interessados"
    creative: "Bolsa de estudo"
    
  - phase: "Conversion"
    dates: "Dez 16 - Jan 15"
    targeting: "Leads"
    creative: "Últimas vagas"
    
  - phase: "Retargeting"
    dates: "Jan 16-31"
    targeting: "Não matriculados"
    creative: "2ª chamada"
```

### Volta às Aulas (Jan-Feb)

```yaml
campaign:
  name: "Volta às Aulas"
  objective: "CONVERSIONS"
  budget: 20000
  
targeting:
  interests:
    - "Educação"
    - "Cursos"
    - "Aprendizado"
  life_events:
    - "Recently moved"
    - "Starting school"
    
offers:
  - "Desconto na matrícula"
  - "Material grátis"
  - "Aula experimental"
```

## Checklist de Implementação

### Setup Inicial

- [ ] Criar Pixel do Facebook
- [ ] Configurar eventos (Lead, CompleteRegistration)
- [ ] Criar conta de anúncios
- [ ] Configurar lista de alunos para exclusão
- [ ] Verificar sazonalidade do curso

### Integração CRM

- [ ] Mapear eventos do CRM
- [ ] Configurar hash de dados (SHA256)
- [ ] Criar script de exportação
- [ ] Agendar uploads semanais

### Campanhas

- [ ] Criar campanha de Awareness
- [ ] Criar campanha de Lead Generation
- [ ] Criar públicos personalizados
- [ ] Criar lookalikes de alunos
- [ ] Configurar exclusões

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
campaign = api.create_campaign(
    name="Vestibular 2024 - Direito",
    objective="LEAD_GENERATION",
    budget=20000,  # R$200/dia
    special_config={
        "attribution_window": 30,
        "offline_conversion": True,
        "course_id": "CURSO_DIREITO",
        "seasonal": True
    }
)

# Criar lead form
form = api.create_lead_form(
    name="Interesse - Direito 2024",
    questions=[
        {"type": "NAME", "label": "Nome completo"},
        {"type": "EMAIL", "label": "E-mail"},
        {"type": "PHONE", "label": "WhatsApp"},
        {
            "type": "CUSTOM",
            "label": "Como conheceu?",
            "options": ["Google", "Facebook", "Indicação", "Outros"]
        },
        {
            "type": "CUSTOM",
            "label": "Interesse",
            "options": ["Manhã", "Noite", "EAD"]
        }
    ],
    privacy_url="https://faculdade.com/privacidade",
    thankyou_message=" obrigado! Nossa equipe entrará em contato em até 24h."
)

# Criar público
audience = api.create_audience(
    name="Interessados em Direito",
    audience_type="interest",
    config={
        "interests": ["Direito", "Faculdade de Direito", "Advocacia"],
        "education_level": ["High school", "College grad"],
        "age_min": 18,
        "age_max": 40,
        "locations": ["Brazil:São Paulo"]
    }
)

# ========== CRON JOBS ==========

# 1. Upload de conversões offline (7dias)
scheduler.add_job(
    job_id="education_offline_conversion",
    job_type="offline_conversion",
    schedule_type="interval",
    schedule_value="7d",
    params={
        "pixel_id": "123456789",
        "events": ["Lead", "Registration", "Payment"],
        "match_keys": ["em", "ph"],
        "batch_size": 500
    }
)

# 2. Relatório semanal
scheduler.add_job(
    job_id="education_weekly_report",
    job_type="report",
    schedule_type="weekly",
    schedule_value="monday 09:00",
    params={
        "report_type": "enrollment",
        "kpis": ["leads", "registrations", "payments"],
        "breakdown": "course",
        "email": "diretor@faculdade.com"
    }
)

# 3. Campanha sazonal
scheduler.add_job(
    job_id="education_vestibular_campaign",
    job_type="seasonal_launch",
    schedule_type="yearly",
    schedule_value="november 01",
    params={
        "campaign_name": "Vestibular 2024",
        "objective": "LEAD_GENERATION",
        "budget": 30000
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
  - frequency: "> 1.5x"
  - cpm: "< R$20"
  - video_completion_rate: "> 45%"
```

### Meio de Funil
```yaml
metrics:
  - leads
  - cost_per_lead
  - whatsapp_contacts
  - form_completion_rate
 benchmarks:
  - cpl: "< R$40"
  - form_rate: "> 15%"
```

### Fundo de Funil
```yaml
metrics:
  - registrations
  - payments
  - cost_per_registration
  - conversion_rate
  - ltv_cac_ratio
benchmarks:
  - cpr: "< R$500"
  - cvr: "> 10%"
  - ltv_cac: "> 20x"
```

## Troubleshooting

### Baixo Volume de Leads?

```yaml
diagnosis:
  - targeting_too_narrow: Amplie públicos
  - wrong_interests: Teste novos interesses
  - creative_not_attractive: Melhore criativos
  - form_too_long: Simplifique formulário

solution:
  - expand_targeting: Similar 5-10%
  - test_interests: Educação + Carreira
  - video_creative: Depoimentos
  - reduce_fields: 3-4 campos
```

### Alto Custo por Lead?

```yaml
diagnosis:
  - competition_high: Melhore relevância
  - wrong_audience: Revise targeting
  - seasonal: Considere sazonalidade
  - offer_weak: Melhore proposta

solution:
  - improve_quality_score: +relevância
  - create_exclusions: Já matriculados
  - wait_season: Aguarde época certa
  - add_benefits: Bolsa, desconto
```

### Baixa Taxa de Matrícula?

```yaml
diagnosis:
  - leads_mal_qualificados: Melhore qualificação
  - follow_up_lento: Acelere contato
  - price_barrier: Trab alhe financiamento
  - no_urgency: Crie urgência

solution:
  - add_questions: "Quando pretende iniciar?"
  - automate_whatsapp: Resposta em 5min
  - offer_financing: Parcelamento
  - limit_vacancies: Últimas vagas
```

## Licença

MIT License - © 2026 Monrars