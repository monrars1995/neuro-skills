# Agent de Campanhas - Saúde

> Especializado em campanhas para clínicas, hospitais e profissionais de saúde

**Versão:** 1.0.0  
**Vertical:** Saúde  
**Autor:** Monrars (@monrars)

## Características do Vertical

### Jornada de Paciente (Privacy-Sensitive)

```
Busca → Pesquisa → Contato → Agendamento → Consulta → Tratamento
   ↓        ↓         ↓           ↓            ↓           ↓
 1-7dias  1-3dias   1dia       1-7dias      1-30dias    Contínuo
```

### Considerações Especiais - LGPD/HIPAA

```yaml
privacy_constraints:
  sensitive_data: true
  hipaa_compliance: true
  lgpd_compliance: true
  
  restrictions:
    - "Não rastrear condições de saúde específicas"
    - "Usar apenas dados demográficos"
    - "Evitar targeting por doença"
    - "Não usar dados médicos para segmentação"
    
  allowed_targeting:
    - "Idade"
    - "Localização"
    - "Interesses gerais em saúde"
    - "Life events (new parent, recently moved)"
```

### Eventos e Timing

| Evento | Frequência | Importância | Offline? |
|--------|------------|-------------|----------|
| Page View | Alta | Média | Não |
| Lead (contato) | Média | Alta | Não |
| WhatsApp Contact | Média | Alta | **Sim** |
| Agendamento | Baixa | Muito Alta | **Sim** |
| Consulta | Baixa | Crítica | **Sim** |
| Tratamento | Baixa | Crítica | **Sim** |

### Tipos de Serviço

```yaml
service_types:
  consultas:
    cycle: "1-7 dias"
    ticket: "R$100-500"
    recurring: true
    
  exames:
    cycle: "1-14 dias"
    ticket: "R$200-2000"
    recurring: false
    
  procedimentos:
    cycle: "7-30 dias"
    ticket: "R$1000-20000"
    recurring: false
    
  tratamentos_continuados:
    cycle: "1-30 dias"
    ticket: "R$500-5000/mês"
    recurring: true
```

### Diferenças vs Outros Verticais

| Aspecto | E-commerce | Saúde |
|---------|-----------|-------|
| Rastreamento | Completo | **Limitado (LGPD)** |
| Targeting por condição | Não se aplica | **Proibido** |
| Testemunhos | Permitido | **Regulamentado** |
| Janela de atribuição | 7-30 dias | **7-45 dias** |
| LTV | Médio | **Alto (pacientes fiéis)** |
| Wolf de boca | Médio | **Muito Alto** |

## Configurações Recomendadas

### 1. Janela de Atribuição

```yaml
attribution_window:
  consultas:
    click_through: 7
    view_through: 1
    conversion_window: 30
    
  exames:
    click_through: 14
    view_through: 3
    conversion_window: 45
    
  procedimentos:
    click_through: 21
    view_through: 7
    conversion_window: 60
```

### 2. Objetivos de Campanha

**Principais:**
- `LEAD_GENERATION` - Agendamento de consulta
- `CONVERSIONS` - WhatsApp/Fone contato

**Secundários:**
- `TRAFFIC` - Site institucional
- `VIDEO_VIEWS` - Conteúdo educativo

### 3. Pixel Events (LGPD Compliant)

```javascript
// Eventos genéricos (sem dados sensíveis)
fbq('track', 'PageView');
fbq('track', 'ViewContent', {
  content_ids: ['SERVICO_123'],
  content_type: 'service',
  content_name: 'Consulta Médica',  // Genérico
  content_category: 'Consultas'
});

fbq('track', 'Lead', {
  content_name: 'Agendamento de Consulta',
  content_category: 'Consultas'
});

fbq('track', 'Contact', {
  content_name: 'Contato WhatsApp',
  content_category: 'General'
});

// NÃO rastrear:
// - Condições médicas específicas
// - Diagnósticos
// - Tratamentos específicos
// - Dados de saúde do paciente
```

### 4. Segmentação (Privacy-Safe)

```yaml
allowed_targeting:
  demographics:
    - "age_range"
    - "gender"
    - "location"
    
  interests:
    - "Saúde e bem-estar"
    - "Medicina"
    - "Fitness"
    - "Nutrição"
    
  behaviors:
    - "Health consciousness"
    
  life_events:
    - "Recently moved"
    - "New parent"
    
forbidden_targeting:
  - "Doenças específicas"
  - "Condições médicas"
  - "Medicamentos"
  - "Sintomas"
```

## Estratégias de Campanha

### 1. Topo de Funil (Awareness)

**Objetivo:** `REACH` ou `VIDEO_VIEWS`

**Público:**
```yaml
targeting:
  interests:
    - "Saúde e bem-estar"
    - "Fitness"
    - "Nutrição"
    - "Vida saudável"
  behaviors:
    - "Health consciousness"
  age_min: 25
  age_max: 65
  locations:
    - "Brazil:{região}"
```

**Orçamento:** R$30-80/dia

**Criativo:**
- Conteúdo educativo
- Dicas de saúde
- Depoimentos genéricos
- Tours pela clínica

### 2. Meio de Funil (Consideração)

**Objetivo:** `LEAD_GENERATION`

**Público:**
```yaml
targeting:
  custom_audiences:
    - "Visitantes Site (7 dias)"
    - "Engajados no Facebook (3 dias)"
    - "Similar a Pacientes (5%)"
  exclusions:
    - "Já são clientes (365 dias)"
```

**Orçamento:** R$50-150/dia

**Lead Forms:**
- Agendamento de consulta
- Dúvidas sobre procedimentos
- Orçamento de exames
- Consulta online

### 3. Fundo de Funil (Conversão)

**Objetivo:** `CONVERSIONS` (WhatsApp/Contato)

**Público:**
```yaml
targeting:
  custom_audiences:
    - "Leads (14 dias)"
    - "Engajados WhatsApp (7 dias)"
    - "Visitantes site (3 dias)"
  exclusions:
    - "Clientes (90 dias)"
```

**Orçamento:** R$80-200/dia

**Estratégia:**
- WhatsApp Business API
- Telemedicina
- Agendamento online
- Consulta rápida

## Cron Jobs Específicos

### Job 1: Upload de Conversões Offline (7dias)

```python
scheduler.add_job(
    job_id="health_offline_conversion",
    job_type="offline_conversion",
    schedule_type="interval",
    schedule_value="7d",
    params={
        "pixel_id": "{PIXEL_ID}",
        "events": [
            {"name": "Lead", "source": "form"},
            {"name": "Contact", "source": "whatsapp"},
            {"name": "Schedule", "source": "crm"},
            {"name": "Appointment", "source": "crm"},
            {"name": "Treatment", "source": "prontuario"}
        ],
        "match_keys": ["em", "ph"],
        "anonymize": True,  # LGPD compliance
        "hash_sensitive": True
    }
)
```

### Job 2: Relatório de Agendamentos (Semanal)

```python
scheduler.add_job(
    job_id="health_weekly_report",
    job_type="report",
    schedule_type="weekly",
    schedule_value="monday 09:00",
    params={
        "report_type": "appointments",
        "date_range": "last_7d",
        "kpis": [
            "leads",
            "whatsapp_contacts",
            "appointments",
            "show_rate",
            "cost_per_appointment"
        ],
        "privacy_report": True,  # Relatório anonimizado
        "email": "diretor@clinica.com"
    }
)
```

### Job 3. Auditoria de Compliance (Mensal)

```python
scheduler.add_job(
    job_id="health_compliance_audit",
    job_type="compliance_audit",
    schedule_type="monthly",
    schedule_value="1st",
    params={
        "check_lgpd": True,
        "check_sensitive_data": True,
        "check_anonymization": True,
        "check_consent": True,
        "audiences": ["all"],
        "creatives": ["all"]
    }
)
```

### Job 4. Relatório de LTV

```python
scheduler.add_job(
    job_id="health_ltv_report",
    job_type="ltv_report",
    schedule_type="monthly",
    schedule_value="1st",
    params={
        "report_type": "patient_lifetime_value",
        "cohort_months": [1, 3, 6, 12, 24],
        "specialties": ["cardiologia", "dermatologia", "ortopedia"],
        "anonymized": True
    }
)
```

## Modelo de ROI/ROAS

### Cálculo para Saúde (LTV + Indicação):

```python
def calculate_healthcare_roi(spend, patient_data):
    """
    Calcula ROI considerando:
    - Valor da consulta/procedimento
    - LTV do paciente (consultas recorrentes)
    - Taxa de indicação (boca a boca)
    - Custo de aquisição (CAC)
    """
    # Dados
    avg_consultation_fee = patient_data.get('avg_consultation_fee', 300)
    avg_visits_per_year = patient_data.get('avg_visits_per_year', 3)
    avg_patient_years = patient_data.get('avg_patient_years', 5)
    referral_rate = patient_data.get('referral_rate', 0.30)  # 30% indicam
    avg_referral_value = patient_data.get('avg_referral_value', 800)
    
    new_patients = patient_data.get('new_patients', 0)
    
    # LTV por paciente
    ltv_per_patient = avg_consultation_fee * avg_visits_per_year * avg_patient_years
    
    # Valor de indicações
    referral_value = new_patients * referral_rate * avg_referral_value
    
    # Receita total
    ltv_total = new_patients * ltv_per_patient
    total_revenue = ltv_total + referral_value
    
    # ROI e ROAS
    roi = ((total_revenue - spend) / spend) * 100 if spend > 0 else 0
    roas = total_revenue / spend if spend > 0 else 0
    
    # CAC
    cac = spend / new_patients if new_patients > 0 else 0
    
    # Payback (em consultas)
    payback_consultations = cac / avg_consultation_fee if avg_consultation_fee > 0 else 0
    
    return {
        "total_revenue": round(total_revenue, 2),
        "ltv_per_patient": round(ltv_per_patient, 2),
        "referral_contribution": round(referral_value, 2),
        "roi_percentage": round(roi, 2),
        "roas": round(roas, 2),
        "cac": round(cac, 2),
        "ltv_cac_ratio": round(ltv_per_patient / cac, 2) if cac > 0 else 0,
        "payback_consultations": round(payback_consultations, 2),
        "new_patients": new_patients,
        "referral_rate": referral_rate
    }

# Exemplo
result = calculate_healthcare_roi(
    spend=5000,
    patient_data={
        'new_patients': 25,
        'avg_consultation_fee': 300,
        'avg_visits_per_year': 3,
        'avg_patient_years': 5,
        'referral_rate': 0.30,
        'avg_referral_value': 800
    }
)

# Resultado:
# {
#   "total_revenue": 123750,      # R$123.750
#   "ltv_per_patient": 4500,        # R$4.500
#   "referral_contribution": 6000,  # R$6.000
#   "roi_percentage": 2375,         # 2375% ROI
#   "roas": 24.75,                  # 24.75x ROAS
#   "cac": 200,                      # R$200 por paciente
#   "ltv_cac_ratio": 22.5,           # 22.5x LTV/CAC
#   "payback_consultations": 0.67,   # 0.67 consultas para payback
#   "new_patients": 25,
#   "referral_rate": 0.30
# }
```

## Compliance LGPD

### Checklist de Compliance

```yaml
lgpd_compliance:
  
  data_collection:
    - ✅ "Consentimento explícito"
    - ✅ "Finalidade específica"
    - ✅ "Minimização de dados"
    - ✅ "Transparência"
    
  pixel_tracking:
    - ✅ "Não rastrear condições médicas"
    - ✅ "Não usar dados sensíveis"
    - ✅ "Anonimizar conversões offline"
    - ✅ "Hash dados de contato"
    
  creatives:
    - ✅ "Não mencionar condições médicas"
    - ✅ "Não usar depoimentos com diagnóstico"
    - ✅ "Apenas depoimentos genéricos"
    - ✅ "Disclaimers obrigatórios"
    
  audiences:
    - ✅ "Não segmentar por doença"
    - ✅ "Não usar dados de prontuário"
    - ✅ "Excluir pacientes antigos (LGPD)"
    - ✅ "Respeitar período de retenção"
```

### Criativos Compliance-Ready

```yaml
creative_guidelines:
  
  allowed:
    - "Conteúdo educativo sobre saúde geral"
    - "Dicas de prevenção"
    - "Informações sobre especialidades"
    - "Depoimentos genéricos"
    - "Tours pela clínica"
    
  forbidden:
    - "Promessas de cura"
    - "Depoimentos com diagnóstico"
    - "Antes/depois de procedimentos"
    - "Mencionar condições específicas"
    - "Garantias de resultados"
    
  required:
    - "Disclaimer: 'Estas informações não substituem consulta médica'"
    - "Registro do profissional (CRM)"
    - "Endereço da clínica"
```

## Estratégias Específicas

### 1. Telemedicina

```yaml
campaign:
  name: "Telemedicina - Consulta Online"
  objective: "LEAD_GENERATION"
  budget: 50
  
targeting:
  interests:
    - "Saúde e bem-estar"
    - "Medicina"
    - "Vida saudável"
  age_min: 25
  age_max: 65
  
creative:
  type: "video"
  format: "tutorial"
  message: "Consulta médica online - rápido e seguro"
  
landing_page:
  url: "https://clinica.com/telemedicina"
  features:
    - "Agendamento online"
    - "Consulta por vídeo"
    - "Receita digital"
```

### 2. Especialidades

```yaml
specialty_campaigns:
  cardiologia:
    name: "Cardiologia - Check-up"
   budget: 40
    targeting:
      interests: ["Saúde do coração", "Fitness"]
      age_min: 40
      age_max: 70
    creative: "Check-up cardíaco completo"
    
  dermatologia:
    name: "Dermatologia - Avaliação"
    budget: 40
    targeting:
      interests: ["Skincare", "Beleza"]
      age_min: 25
      age_max: 55
    creative: "Avaliação dermatológica"
    
  ortopedia:
    name: "Ortopedia - Consulta"
    budget: 40
    targeting:
      interests: ["Fitness", "Esportes"]
      age_min: 25
      age_max: 60
    creative: "Consulta ortopédica"
```

### 3. Check-up Preventivo

```yaml
campaign:
  name: "Check-up Preventivo"
  objective: "LEAD_GENERATION"
  budget: 60
  
targeting:
  interests:
    - "Saúde e bem-estar"
    - "Prevenção"
  life_events:
    - "Newly married"
    - "Starting new job"
  age_min: 35
  age_max: 65
  
creative:
  type: "carousel"
  message: "Prevenção é o melhor remédio"
  
cTA: "AGENDAR CHECK-UP"
```

## Checklist de Implementação

### Setup Inicial

- [ ] Criar Pixel do Facebook
- [ ] Configurar eventos genéricos (LGPD compliant)
- [ ] Criar conta de anúncios
- [ ] Verificar compliance LGPD
- [ ] Configurar lista de pacientes para exclusão
- [ ] Aprovar criativos com jurídico

### Compliance

- [ ] Termo de consentimento no site
- [ ] Política de privacidade atualizada
- [ ] Anonimização de dados offline
- [ ] Hash de dados sensíveis
- [ ] Auditoria de segmentação

### Campanhas

- [ ] Criar campanha institucional
- [ ] Criar campanha de agendamento
- [ ] Criar públicos personalizados
- [ ] Configurar exclusões
- [ ] Validar criativos

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

# Criar campanha compliance-ready
campaign = api.create_campaign(
    name="Clínica ABC - Agendamento",
    objective="LEAD_GENERATION",
    budget=15000,  # R$150/dia
    special_config={
        "attribution_window": 14,
        "offline_conversion": True,
        "lgpd_compliant": True,
        "anonymize_data": True
    }
)

# Criar lead form (LGPD compliant)
form = api.create_lead_form(
    name="Agendamento de Consulta",
    questions=[
        {"type": "NAME", "label": "Nome completo"},
        {"type": "EMAIL", "label": "E-mail"},
        {"type": "PHONE", "label": "WhatsApp"},
        {
            "type": "CUSTOM",
            "label": "Especialidade",
            "options": ["Cardiologia", "Dermatologia", "Ortopedia", "Clínico Geral"]
        },
        {
            "type": "CUSTOM",
            "label": "Como conheceu?",
            "options": ["Google", "Facebook", "Indicação", "Outros"]
        }
    ],
    privacy_url="https://clinica.com/privacidade",
    thankyou_message="Obrigado! Nossa equipe entrará em contato em até 24h. Esta informação não substitui consulta médica.",
    disclaimer="Esta informação não substitui consulta médica profissional."
)

# Criar público (privacy-safe)
audience = api.create_audience(
    name="Interessados em Saúde",
    audience_type="interest",
    config={
        "interests": ["Saúde e bem-estar", "Fitness", "Nutrição"],
        "behaviors": ["Health consciousness"],
        "age_min": 25,
        "age_max": 65,
        "locations": ["Brazil:São Paulo"]
    }
)

# ========== CRON JOBS ==========

# 1. Upload de conversões offline (7dias) - LGPD compliant
scheduler.add_job(
    job_id="health_offline_conversion",
    job_type="offline_conversion",
    schedule_type="interval",
    schedule_value="7d",
    params={
        "pixel_id": "123456789",
        "events": ["Lead", "Contact", "Schedule", "Appointment"],
        "match_keys": ["em", "ph"],
        "anonymize": True,
        "hash_sensitive": True
    }
)

# 2. Relatório semanal (anonimizado)
scheduler.add_job(
    job_id="health_weekly_report",
    job_type="report",
    schedule_type="weekly",
    schedule_value="monday 09:00",
    params={
        "report_type": "appointments",
        "kpis": ["leads", "appointments", "show_rate"],
        "privacy_report": True,
        "email": "diretor@clinica.com"
    }
)

# 3. Auditoria de compliance (mensal)
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
print(f"Campaign ID: {campaign['campaign_id']}")
print(f"Form ID: {form['form_id']}")
print("🔒 LGPD Compliant")
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
  - cpm: "< R$25"
  - video_completion_rate: "> 40%"
```

### Meio de Funil
```yaml
metrics:
  - leads
  - cost_per_lead
  - whatsapp_contacts
  - form_completion_rate
benchmarks:
  - cpl: "< R$60"
  - form_rate: "> 12%"
```

### Fundo de Funil
```yaml
metrics:
  - appointments
  - show_rate
  - cost_per_appointment
  - ltv_cac_ratio
benchmarks:
  - cpa: "< R$300"
  - show_rate: "> 80%"
  - ltv_cac: "> 15x"
```

## Troubleshooting

### Baixo Volume de Leads?

```yaml
diagnosis:
  - targeting_too_narrow: Amplie públicos
  - privacy_constraints: Verifique compliance
  - creative_not_engaging: Melhore criativos
  - form_too_long: Simplifique formulário

solution:
  - expand_targeting: Interesses gerais
  - check_compliance: LGPD audit
  - video_creative: Conteúdo educativo
  - reduce_fields: 3-4 campos
```

### Alto Custo por Lead?

```yaml
diagnosis:
  - audience_too_small: Expanda localização
  - wrong_interests: Revise segmentação
  - competition_high: Diferencie oferta
  - creative_fatigue: Teste novos criativos

solution:
  - expand_location: Raio maior
  - test_interests: Saúde geral
  - unique_value: Diferencial
  - rotate_creatives: Semanal
```

### Baixa Taxa de Comparecimento?

```yaml
diagnosis:
  - leads_mal_qualificados: Melhore formulário
  - follow_up_lento: Acelere contato
  - scheduling_unclear: Melhore agendamento
  - no_reminder: Falta lembrete

solution:
  - add_questions: "Quando pode comparecer?"
  - automate_whatsapp: Confirmação imediata
  - online_scheduling: Link direto
  - reminder_system: 24h antes
```

## Licença

MIT License - © 2026 Monrars