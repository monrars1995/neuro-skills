# Automação com Crons - Neuro Skills Agent

## Visão Geral

O sistema de automação permite agendar análises, otimizações e relatórios para rodar automaticamente.

## Tipos de Automação

### 1. Analysis - Análise de Performance

Roda análise automática de performance das campanhas.

```python
from scheduler.automation import AutomationScheduler

# Inicializar
scheduler = AutomationScheduler(
    memory_manager=memory,
    api_client=api
)

# Criar job de análise diária
scheduler.add_job(
    job_id="daily_analysis",
    job_type="analysis",
    schedule_type="daily",
    schedule_value="09:00",
    params={
        "client_id": "nike",
        "campaigns": ["123", "456", "789"],
        "cpa_threshold": 100,
        "roas_threshold": 2.5
    }
)
```

### 2. Optimization - Otimização Automática

Aplica otimizações baseadas em regras.

```python
# Escalar campanhas com ROAS > 3
scheduler.add_job(
    job_id="scale_high_performers",
    job_type="optimization",
    schedule_type="daily",
    schedule_value="10:00",
    params={
        "campaigns": ["123", "456"],
        "rules": [
            {
                "type": "scale_high_performers",
                "roas_threshold": 3.0,
                "scale_factor": 1.2
            }
        ]
    }
)

# Pausar campanhas com CPA > 100
scheduler.add_job(
    job_id="pause_low_performers",
    job_type="optimization",
    schedule_type="interval",
    schedule_value="6h",
    params={
        "campaigns": ["123", "456"],
        "rules": [
            {
                "type": "pause_low_performers",
                "cpa_threshold": 100,
                "min_spend": 50
            }
        ]
    }
)

# Realocar orçamento
scheduler.add_job(
    job_id="budget_reallocation",
    job_type="optimization",
    schedule_type="weekly",
    schedule_value="monday 09:00",
    params={
        "campaigns": ["123", "456", "789"],
        "rules": [
            {
                "type": "budget_reallocation",
                "total_budget": 10000,
                "method": "performance_based"
            }
        ]
    }
)

# Rotacionar criativos
scheduler.add_job(
    job_id="creative_rotation",
    job_type="optimization",
    schedule_type="weekly",
    schedule_value="friday 18:00",
    params={
        "campaigns": ["123"],
        "rules": [
            {
                "type": "creative_rotation",
                "top_n": 3
            }
        ]
    }
)
```

### 3. Report - Geração de Relatórios

Gera e envia relatórios automaticamente.

```python
# Relatório diário por email
scheduler.add_job(
    job_id="daily_report",
    job_type="report",
    schedule_type="daily",
    schedule_value="18:00",
    params={
        "report_type": "performance",
        "date_range": "last_7d",
        "format": "excel",
        "email": "analytics@company.com"
    }
)

# Relatório semanal
scheduler.add_job(
    job_id="weekly_report",
    job_type="report",
    schedule_type="weekly",
    schedule_value="friday 17:00",
    params={
        "report_type": "performance",
        "date_range": "last_7d",
        "format": "excel",
        "email": "ceo@company.com"
    }
)
```

### 4. Rule - Regras de Automação

Executa regras específicas.

```python
# Regra: Pausa campanha se CPA > 150
scheduler.add_job(
    job_id="pause_high_cpa",
    job_type="rule",
    schedule_type="interval",
    schedule_value="1h",
    params={
        "rule_id": "rule_pause_high_cpa",
        "trigger": "cpa > 150",
        "action": "pause_campaign",
        "campaigns": ["123", "456"]
    }
)

# Regra: Notifica se spend > 1000/dia
scheduler.add_job(
    job_id="notify_high_spend",
    job_type="rule",
    schedule_type="interval",
    schedule_value="12h",
    params={
        "rule_id": "rule_high_spend",
        "trigger": "spend > 1000",
        "action": "send_notification",
        "campaigns": ["123", "456"],
        "params": {
            "email": "alerts@company.com"
        }
    }
)
```

## Agendamentos

### Interval (Intervalo)

Rodar a cada X tempo:

```python
# A cada hora
schedule_type="interval"
schedule_value="1h"

# A cada 30 minutos
schedule_value="30m"

# A cada 24 horas
schedule_value="24h"
```

### Daily (Diário)

Rodar em horário específico todos os dias:

```python
# Todo dia às 9h
schedule_type="daily"
schedule_value="09:00"

# Todo dia às 18h
schedule_value="18:00"
```

### Weekly (Semanal)

Rodar em dia específico da semana:

```python
# Toda segunda às 9h
schedule_type="weekly"
schedule_value="monday 09:00"

# Toda sexta às 17h
schedule_value="friday 17:00"
```

### Monthly (Mensal)

Rodar em dia específico do mês:

```python
# Dia 1 de cada mês às 9h
schedule_type="monthly"
schedule_value="01 09:00"

# Dia 15 às 10h
schedule_value="15 10:00"
```

## Exemplos Completos

### Fluxo 1: Análise Diária + Relatório

```python
from scheduler.automation import AutomationScheduler
from analytics.engine import AnalyticsEngine
from core.memory import MemoryManager
from core.meta_api import MetaAPIClient

# Inicializar
memory = MemoryManager()
api = MetaAPIClient(account["access_token"], account["ad_account_id"])

# Scheduler
scheduler = AutomationScheduler(memory, api)

# Análise diária às 9h
scheduler.add_job(
    job_id="morning_analysis",
    job_type="analysis",
    schedule_type="daily",
    schedule_value="09:00",
    params={
        "client_id": "nike",
        "campaigns": ["123", "456"],
        "cpa_threshold": 100,
        "roas_threshold": 2.5
    }
)

# Relatório às 18h
scheduler.add_job(
    job_id="evening_report",
    job_type="report",
    schedule_type="daily",
    schedule_value="18:00",
    params={
        "report_type": "performance",
        "date_range": "today",
        "format": "excel",
        "email": "team@company.com"
    }
)

# Iniciar scheduler
scheduler.start()
```

### Fluxo 2: Otimização Automática

```python
# Escalar seg-sáb às 10h
scheduler.add_job(
    job_id="morning_scale",
    job_type="optimization",
    schedule_type="interval",
    schedule_value="6h",
    params={
        "campaigns": ["123", "456"],
        "rules": [
            {
                "type": "scale_high_performers",
                "roas_threshold": 3.0,
                "scale_factor": 1.2
            }
        ]
    }
)

# Pausar a cada 4h
scheduler.add_job(
    job_id="pause_check",
    job_type="optimization",
    schedule_type="interval",
    schedule_value="4h",
    params={
        "campaigns": ["123", "456"],
        "rules": [
            {
                "type": "pause_low_performers",
                "cpa_threshold": 150,
                "min_spend": 100
            }
        ]
    }
)

scheduler.start()
```

### Fluxo 3: Relatório Semanal

```python
# Relatório de performance - toda segunda 9h
scheduler.add_job(
    job_id="weekly_performance",
    job_type="report",
    schedule_type="weekly",
    schedule_value="monday 09:00",
    params={
        "report_type": "performance",
        "date_range": "last_7d",
        "format": "excel",
        "email": "ceo@company.com"
    }
)

# Relatório de criativos - toda quarta 14h
scheduler.add_job(
    job_id="creative_report",
    job_type="report",
    schedule_type="weekly",
    schedule_value="wednesday 14:00",
    params={
        "report_type": "creative",
        "date_range": "last_7d",
        "format": "json"
    }
)

scheduler.start()
```

## Gerenciamento de Jobs

### Listar Jobs

```python
# Todos os jobs
jobs = scheduler.get_jobs()

# Jobs de análise
analysis_jobs = scheduler.get_jobs(job_type="analysis")

# Jobs de otimização
optimization_jobs = scheduler.get_jobs(job_type="optimization")
```

### Executar Manualmente

```python
# Executar job específico
result = scheduler._execute_job(scheduler.get_job("daily_analysis"))

# Ver resultado
print(result)
```

### Pausar/Ativar

```python
# Pausar
job = scheduler.toggle_job("daily_analysis")

# Ativar
job = scheduler.toggle_job("daily_analysis")
```

### Remover

```python
scheduler.remove_job("daily_analysis")
```

## Alertas Automáticos

O sistema gera alertas automaticamente baseados nas análises:

### Tipos de Alertas:

1. **high_cpa** - CPA acima do threshold
2. **low_roas** - ROAS abaixo do threshold
3. **low_ctr** - CTR baixo
4. **high_spend** - Gasto acima do limite
5. **high_frequency** - Frequência alta

### Exemplo de Alerta:

```json
{
    "type": "high_cpa",
    "level": "warning",
    "message": "CPA alto: R$150.00",
    "value": 150.00,
    "threshold": 100.00
}
```

## Recomendações Automáticas

O sistema também gera recomendações:

### Tipos:

1. **scale** - Escalar campanha
2. **pause** - Pausar criativos
3. **creative** - Testar novos criativos
4. **expand** - Expandir público

## Logs e Histórico

Cada execução é salva com:

```python
job = {
    "id": "daily_analysis",
    "type": "analysis",
    "last_run": "2024-01-15T09:00:00",
    "run_count": 45,
    "last_result": {
        "timestamp": "2024-01-15T09:00:00",
        "metrics": {...},
        "alerts": [...],
        "recommendations": [...]
    }
}
```

## Integração com API Meta

O scheduler usa o `MetaAPIClient` para todas as operações:

```python
# Criar cliente
api = MetaAPIClient(
    access_token="EAA...",
    ad_account_id="123456789"
)

# Usar no scheduler
scheduler = AutomationScheduler(memory, api)
```

## Boas Práticas

### 1. Comece com Intervalos Maiores

```python
# Bom: começar com análise a cada 6h
schedule_value="6h"

# Ruim: começar com análise a cada 1h
schedule_value="1h"  # Pode atingir rate limits
```

### 2. Monitore os Jobs

```python
# Verificar jobs ativos
active_jobs = [j for j in scheduler.get_jobs() if j["enabled"]]
print(f"Jobs ativos: {len(active_jobs)}")

# Verificar execuções
for job in scheduler.get_jobs():
    print(f"{job['id']}: {job['run_count']} execuções")
```

### 3. Configure Alertas Adequadamente

```python
# CPA threshold baseado no seu mercado
params={
    "cpa_threshold": 100,  # Ajustar conforme necessário
    "roas_threshold": 2.5   # Ajustar conforme necessário
}
```

### 4. Use Multiplas Regras

```python
# Combinação de regras
params={
    "rules": [
        {"type": "scale_high_performers", "roas_threshold": 3.0},
        {"type": "pause_low_performers", "cpa_threshold": 150},
        {"type": "notify_high_spend", "spend_threshold": 5000}
    ]
}
```

## Exemplo Completo - Produção

```python
from scheduler.automation import AutomationScheduler
from core.memory import MemoryManager
from core.meta_api import MetaAPIClient
import logging

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar
memory = MemoryManager()
api = MetaAPIClient(
    access_token=os.environ.get("META_ACCESS_TOKEN"),
    ad_account_id=os.environ.get("META_AD_ACCOUNT_ID")
)

# Scheduler
scheduler = AutomationScheduler(memory, api)

# Análise diária às 9h
scheduler.add_job(
    job_id="daily_analysis",
    job_type="analysis",
    schedule_type="daily",
    schedule_value="09:00",
    params={
        "cpa_threshold": 100,
        "roas_threshold": 2.0
    }
)

# Otimização a cada 6h
scheduler.add_job(
    job_id="optimization_6h",
    job_type="optimization",
    schedule_type="interval",
    schedule_value="6h",
    params={
        "rules": [
            {"type": "scale_high_performers", "roas_threshold": 3.0},
            {"type": "pause_low_performers", "cpa_threshold": 150}
        ]
    }
)

# Relatório às 18h
scheduler.add_job(
    job_id="daily_report",
    job_type="report",
    schedule_type="daily",
    schedule_value="18:00",
    params={
        "report_type": "performance",
        "date_range": "today",
        "format": "excel",
        "email": "team@company.com"
    }
)

# Iniciar
logger.info("Iniciando scheduler...")
scheduler.start()

try:
    # Maniver rodando
    import time
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    logger.info("Parando scheduler...")
    scheduler.stop()
```

## Licença

MIT License - ©2026 Monrars