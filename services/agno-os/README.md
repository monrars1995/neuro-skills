# Agno OS Service

Serviço backend dos agents do Neuro Skills usando Agno.

## Objetivo

- Orquestrar agents reais com Agno
- Expor endpoints para execução dos agents
- Produzir respostas estruturadas que o app web consome via AG-UI
- Gerar widgets declarativos A2UI para a interface

## Rodar localmente

```bash
cd services/agno-os
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
fastapi dev app.py
```

Servidor padrão: `http://localhost:8000`

## Endpoints

- `GET /health`
- `GET /api/agents`
- `POST /api/agents/run`
- `POST /api/agui/stream`
