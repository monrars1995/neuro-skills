# Sistema de Memória Compartilhada - Neuro Skills

## Visão Geral

O sistema de memória do Neuro Skills é projetado para ser:
- **Compartilhado**: Todos os skills acessam os mesmos dados de clientes
- **Persistente**: Contexto mantido entre sessões
- **Inteligente**: Aprende com cada interação
- **Organizado**: Estrutura clara por cliente, campanha e sessão

---

## Arquitetura

```
~/.neuro-skills/
│
├── clients/                          # DADOS DE CLIENTES (Compartilhado)
│   ├── index.json                    # Índice master de clientes
│   │
│   └── {client_id}/                  # Ex: nike, fitness_app
│       ├── profile.json              # Perfil do cliente
│       ├── brand_voice.json          # Voz da marca (ad-copywriter)
│       ├── preferences.json          # Preferências aprendidas
│       ├── performance.json          # Métricas históricas
│       └── history/
│           ├── campaigns.json        # Histórico de campanhas
│           └── learnings.json        # Insights aprendidos
│
├── campaigns/                         # CAMPANHAS ATIVAS
│   └── {campaign_id}/                # Ex: nike_2024-03_black_friday
│       ├── briefing.md               # Briefing original
│       ├── context.json              # Contexto da sessão
│       ├── state.json                # Estado atual
│       ├── targeting.json            # Configurações de targeting
│       ├── copy_variants.md          # Variações de copy
│       ├── checklist.json            # Checklist de validação
│       └── insights.json             # Insights de performance
│
├── sessions/                          # SESSÕES POR SKILL
│   ├── meta-ads-manager/
│   │   ├── session.json              # Sessão atual
│   │   ├── cache/
│   │   │   ├── insights/             # Cache de insights (24h TTL)
│   │   │   └── campaigns/            # Cache de campanhas (1h TTL)
│   │   └── logs/
│   │       └── actions.log           # Log de ações
│   │
│   ├── traffic-strategist/
│   │   ├── session.json              # Sessão atual
│   │   └── cache/
│   │       └── analyses/             # Análises cacheadas
│   │
│   └── ad-copywriter/
│       ├── session.json               # Sessão atual
│       └── cache/
│           └── copies/               # Cópias geradas
│
└── shared/                            # MEMÓRIA COMPARTILHADA
    ├── accounts.json                 # Contas Meta Ads
    ├── benchmarks.json               # Benchmarks do mercado
    ├── learnings.json                # Aprendizados globais do sistema
    └── templates/
        ├── briefing_template.md      # Template padrão de briefing
        ├── copy_template.md          # Template padrão de copy
        └── checklist_template.md     # Template padrão de checklist
```

---

## Estruturas de Dados

### 1. Índice de Clientes (`clients/index.json`)

```json
{
  "version": "2.0",
  "updated_at": "2024-03-29T15:00:00Z",
  "clients": {
    "nike": {
      "name": "Nike Brasil",
      "industry": "Sportswear",
      "created_at": "2024-01-15T10:00:00Z",
      "last_active": "2024-03-29T14:30:00Z",
      "total_campaigns": 12,
      "total_spend": 125000.00,
      "best_performing_campaign": "black_friday_2023",
      "avg_roas": 4.2,
      "profile_path": "clients/nike/profile.json",
      "brand_voice_path": "clients/nike/brand_voice.json"
    },
    "fitness_app": {
      "name": "FitnessApp Pro",
      "industry": "Health & Fitness",
      "created_at": "2024-02-01T09:00:00Z",
      "last_active": "2024-03-28T16:00:00Z",
      "total_campaigns": 5,
      "total_spend": 35000.00,
      "best_performing_campaign": "new_year_launch",
      "avg_roas": 3.8
    }
  },
  "active_client": "nike",
  "recent_clients": ["nike", "fitness_app", "local_bakery"]
}
```

### 2. Perfil do Cliente (`clients/{client_id}/profile.json`)

```json
{
  "client_id": "nike",
  "name": "Nike Brasil",
  "industry": "Sportswear",
  "website": "https://nike.com.br",
  "timezone": "America/Sao_Paulo",
  "currency": "BRL",
  
  "meta_accounts": {
    "primary": {
      "ad_account_id": "act_123456789",
      "pixel_id": "987654321",
      "page_id": "111222333",
      "business_id": "444555666"
    }
  },
  
  "target_audience": {
    "primary_age_range": [25, 45],
    "primary_gender": "all",
    "primary_locations": ["Brasil", "Argentina", "Chile"],
    "interests": ["running", "fitness", "sports", "athleisure"],
    "behaviors": ["online_shopper", "fitness_app_user"]
  },
  
  "business_objectives": {
    "primary": "Sales",
    "secondary": ["Brand Awareness", "App Installs"],
    "target_cpa": 25.00,
    "target_roas": 4.0
  },
  
  "brand_identity": {
    "tone": "inspirational",
    "voice_keywords": ["performance", "achievement", "innovation"],
    "avoid_keywords": ["cheap", "discount", "basic"],
    "ctas": ["Shop Now", "Learn More", "Download"]
  },
  
  "performance_history": {
    "total_spend": 125000.00,
    "total_revenue": 525000.00,
    "avg_roas": 4.2,
    "avg_cpa": 23.50,
    "best_month": "2024-02",
    "worst_month": "2024-01"
  },
  
  "learned_preferences": {
    "best_performing_placements": ["feed", "reels"],
    "best_performing_formats": ["video", "carousel"],
    "best_performing_audiences": ["lookalike_1_percent", "interest_fitness"],
    "avoided_audiences": ["broad", "age_18_24"],
    "successful_creatives": ["athlete_testimonials", "product_launches"],
    "failed_approaches": ["static_images", "discount_focus"]
  },
  
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-03-29T14:30:00Z"
}
```

### 3. Voz da Marca (`clients/{client_id}/brand_voice.json`)

```json
{
  "client_id": "nike",
  "brand_name": "Nike",
  
  "voice_profile": {
    "tone": {
      "primary": "Inspiracional",
      "secondary": ["Motivador", "Inovador", "Autêntico"],
      "avoid": ["Genérico", "Vendedor", "Agressivo"]
    },
    
    "language": {
      "formality": "casual",
      "use_emojis": false,
      "use_exclamation": "moderado",
      "pronoun": "você",
      "tempo_verbal": "presente"
    },
    
    "keywords": {
      "use": ["performance", "superação", "inovação", "atleta", "just do it"],
      "avoid": ["barato", "desconto", "oferta", "promoção", "promoção"]
    },
    
    "patterns": {
      "headline_style": "Imperativo + Benefício",
      "body_structure": "Problema → Solução → CTA",
      "cta_style": "Ação direta + Urgência"
    },
    
    "examples": {
      "good_headlines": [
        "Supere Seus Limites com Nike Air",
        "Corra Mais Longo. Chegue Mais Longe.",
        "O Desafio Começa Agora."
      ],
      "good_bodies": [
        "Atletas não nascem prontos. Eles se fazem com cada treino, cada passo, cada superação.",
        "A nova tecnologia Nike Air oferece o conforto que você precisa para ir além."
      ],
      "good_ctas": [
        "Compre Agora",
        "Descubra Mais",
        "Comece Sua Jornada"
      ]
    }
  },
  
  "platform_adjustments": {
    "feed": {
      "max_headline": 40,
      "max_primary_text": 125,
      "tone_modifiers": ["Mais detalhado", "Storytelling"]
    },
    "story": {
      "max_headline": 25,
      "max_primary_text": 65,
      "tone_modifiers": ["Direto", "Visual", "Urgência"]
    },
    "reels": {
      "max_headline": 25,
      "max_primary_text": 90,
      "tone_modifiers": ["Entretenimento", "Desafio", "Trending"]
    }
  },
  
  "learned_preferences": {
    "best_performing_tones": ["inspiracional", "desafio"],
    "best_performing_ctas": ["Shop Now", "Learn More"],
    "avoided_tones": ["promocional", "agressivo"],
    "audience_response": {
      "positive": ["inspiração", "superação", "inovação"],
      "negative": ["desconto", "oferta", "promoção"]
    }
  },
  
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-03-29T14:30:00Z",
  "version": 3
}
```

### 4. Contexto de Campanha (`campaigns/{campaign_id}/context.json`)

```json
{
  "campaign_id": "nike_2024-03_black_friday",
  "client_id": "nike",
  "campaign_name": "Black Friday 2024",
  
  "status": {
    "phase": "created",
    "current_step": "traffic-strategist",
    "completed_steps": ["briefing", "analysis"],
    "pending_steps": ["copy", "targeting", "launch"]
  },
  
  "briefing": {
    "source_path": "/campanhas/nike/2024-03/black_friday/briefing.md",
    "parsed_data": {
      "objective": "Sales",
      "budget": 50000,
      "duration": "2024-11-20 to 2024-11-30",
      "target_cpa": 20,
      "target_roas": 5.0
    }
  },
  
  "assets": {
    "creatives": [
      {
        "id": "ad_01",
        "path": "/campanhas/nike/2024-03/black_friday/ad_01_feed_video.mp4",
        "type": "video",
        "placement": "feed",
        "status": "validated"
      },
      {
        "id": "ad_02",
        "path": "/campanhas/nike/2024-03/black_friday/ad_02_story_video.mp4",
        "type": "video",
        "placement": "story",
        "status": "validated"
      }
    ],
    "total_count": 2,
    "validated_count": 2
  },
  
  "generated_content": {
    "analysis_path": "/campanhas/nike/2024-03/black_friday/analise.md",
    "checklist_path": "/campanhas/nike/2024-03/black_friday/checklist.md",
    "targeting_path": "/campanhas/nike/2024-03/black_friday/targeting.json",
    "copy_path": "/campanhas/nike/2024-03/black_friday/copy_variants.md"
  },
  
  "session_history": [
    {
      "timestamp": "2024-03-29T10:00:00Z",
      "skill": "traffic-strategist",
      "action": "analysis",
      "result": "success"
    },
    {
      "timestamp": "2024-03-29T11:00:00Z",
      "skill": "ad-copywriter",
      "action": "copy_generation",
      "result": "success"
    }
  ],
  
  "created_at": "2024-03-29T09:00:00Z",
  "updated_at": "2024-03-29T14:00:00Z"
}
```

### 5. Contas Meta (`shared/accounts.json`)

```json
{
  "version": "2.0",
  "accounts": {
    "nike_primary": {
      "name": "Nike Brasil - Principal",
      "client_id": "nike",
      "ad_account_id": "act_123456789",
      "pixel_id": "987654321",
      "page_id": "111222333",
      "business_id": "444555666",
      "access_token": "ENCRYPTED_TOKEN",
      "currency": "BRL",
      "timezone": "America/Sao_Paulo",
      "is_active": true,
      "created_at": "2024-01-15T10:00:00Z",
      "last_used": "2024-03-29T14:30:00Z"
    },
    "fitness_app_primary": {
      "name": "FitnessApp - Principal",
      "client_id": "fitness_app",
      "ad_account_id": "act_987654321",
      "pixel_id": "111222333",
      "page_id": "444555666",
      "business_id": "777888999",
      "access_token": "ENCRYPTED_TOKEN",
      "currency": "BRL",
      "timezone": "America/Sao_Paulo",
      "is_active": false,
      "created_at": "2024-02-01T09:00:00Z",
      "last_used": "2024-03-28T16:00:00Z"
    }
  },
  "active_account": "nike_primary"
}
```

### 6. Aprendizados Globais (`shared/learnings.json`)

```json
{
  "version": "1.0",
  "updated_at": "2024-03-29T15:00:00Z",
  
  "industry_benchmarks": {
    "Sportswear": {
      "avg_cpa_brl": 25.00,
      "avg_roas": 4.0,
      "avg_ctr": 1.8,
      "avg_frequency": 2.5,
      "best_placements": ["feed", "reels"],
      "best_formats": ["video", "carousel"]
    },
    "Health & Fitness": {
      "avg_cpa_brl": 20.00,
      "avg_roas": 3.5,
      "avg_ctr": 2.0,
      "avg_frequency": 2.0,
      "best_placements": ["reels", "story"],
      "best_formats": ["video"]
    }
  },
  
  "platform_insights": {
    "facebook_feed": {
      "avg_reach_rate": 0.85,
      "best_performing_ctas": ["Shop Now", "Learn More"],
      "optimal_headline_length": 30,
      "optimal_text_length": 90
    },
    "instagram_story": {
      "avg_reach_rate": 0.92,
      "best_performing_ctas": ["Shop Now", "Download"],
      "optimal_headline_length": 20,
      "optimal_text_length": 60
    },
    "instagram_reels": {
      "avg_reach_rate": 1.5,
      "best_performing_ctas": ["Shop Now", "Watch More"],
      "optimal_headline_length": 25,
      "optimal_text_length": 80
    }
  },
  
  "audience_patterns": {
    "lookalike_1_percent": {
      "performance_multiplier": 1.2,
      "best_for": ["Sales", "Leads"]
    },
    "interest_based": {
      "performance_multiplier": 1.0,
      "best_for": ["Awareness", "Traffic"]
    },
    "retargeting": {
      "performance_multiplier": 1.5,
      "best_for": ["Sales", "Conversions"]
    }
  },
  
  "copy_patterns": {
    "high_performing_formulas": [
      "[Problema] → [Solução] → [CTA]",
      "[Benefício] → [Prova] → [CTA]",
      "[Storytelling] → [Benefício] → [CTA]"
    ],
    "avoided_patterns": [
      "Excesso de exclamações",
      "Foco apenas em preço",
      "CTA genérico sem urgência"
    ]
  }
}
```

---

## Fluxo de Dados Entre Skills

```
┌─────────────────────────────────────────────────────────────────┐
│                    MEMÓRIA COMPARTILHADA                         │
│  ~/.neuro-skills/                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────────┐    ┌────────────────┐ │
│  │   CLIENTS    │    │    CAMPAIGNS     │    │    SESSIONS    │ │
│  │              │    │                  │    │                │ │
│  │ • profile    │    │ • context        │    │ • meta-ads     │ │
│  │ • brand_voice│◄───┤ • state          │───►│ • traffic      │ │
│  │ • history    │    │ • targeting      │    │ • copywriter   │ │
│  │ • learnings  │    │ • insights       │    │                │ │
│  └──────┬───────┘    └────────┬─────────┘    └────────────────┘ │
│         │                     │                                 │
│         │                     │                                 │
│         ▼                     ▼                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              FLUXO DE TRABALHO DOS SKILLS                   ││
│  │                                                              ││
│  │  1. TRAFFIC-STRATEGIST                                      ││
│  │     └── Lê: clients/{client}/profile.json                   ││
│  │     └── Escreve: campaigns/{id}/context.json                ││
│  │     └── Escreve: campaigns/{id}/checklist.json             ││
│  │                                                              ││
│  │  2. AD-COPYWRITER                                           ││
│  │     └── Lê: clients/{client}/brand_voice.json              ││
│  │     └── Lê: campaigns/{id}/context.json                    ││
│  │     └── Escreve: campaigns/{id}/copy_variants.md           ││
│  │     └── Atualiza: clients/{client}/brand_voice.json         ││
│  │                                                              ││
│  │  3. META-ADS-MANAGER                                        ││
│  │     └── Lê: shared/accounts.json                           ││
│  │     └── Lê: campaigns/{id}/context.json                    ││
│  │     └── Lê: clients/{client}/profile.json                  ││
│  │     └── Escreve: campaigns/{id}/insights.json              ││
│  │     └── Atualiza: clients/{client}/performance.json        ││
│  │     └── Atualiza: shared/learnings.json                     ││
│  │                                                              ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## Inicialização

### Script de Setup

```bash
#!/bin/bash
# setup-memory.sh - Inicializa o sistema de memória do Neuro Skills

NEURO_DIR="$HOME/.neuro-skills"

echo "🧠 Inicializando sistema de memória Neuro Skills..."

# Criar estrutura de diretórios
mkdir -p "$NEURO_DIR/clients"
mkdir -p "$NEURO_DIR/campaigns"
mkdir -p "$NEURO_DIR/sessions/meta-ads-manager/cache/insights"
mkdir -p "$NEURO_DIR/sessions/meta-ads-manager/cache/campaigns"
mkdir -p "$NEURO_DIR/sessions/meta-ads-manager/logs"
mkdir -p "$NEURO_DIR/sessions/traffic-strategist/cache/analyses"
mkdir -p "$NEURO_DIR/sessions/ad-copywriter/cache/copies"
mkdir -p "$NEURO_DIR/shared/templates"

# Criar arquivos iniciais

# Índice de clientes
cat > "$NEURO_DIR/clients/index.json" << 'EOF'
{
  "version": "2.0",
  "updated_at": null,
  "clients": {},
  "active_client": null,
  "recent_clients": []
}
EOF

# Contas Meta
cat > "$NEURO_DIR/shared/accounts.json" << 'EOF'
{
  "version": "2.0",
  "accounts": {},
  "active_account": null
}
EOF

# Aprendizados globais
cat > "$NEURO_DIR/shared/learnings.json" << 'EOF'
{
  "version": "1.0",
  "updated_at": null,
  "industry_benchmarks": {},
  "platform_insights": {},
  "audience_patterns": {},
  "copy_patterns": {}
}
EOF

# Benchmarks
cat > "$NEURO_DIR/shared/benchmarks.json" << 'EOF'
{
  "version": "1.0",
  "updated_at": null,
  "industries": {}
}
EOF

# Templates
cat > "$NEURO_DIR/shared/templates/briefing_template.md" << 'EOF'
# Briefing Template

## Client Information
- **Client:** {client_name}
- **Product/Service:** {product}
- **Industry:** {industry}

## Campaign Objectives
- **Primary Goal:** {goal}
- **Target CPA:** $XX.XX
- **Target ROAS:** X.Xx
- **Budget:** $X,XXX

## Target Audience
- **Age:** XX to XX
- **Location:** {locations}
- **Interests:** {interests}

## Assets
- **Creatives:** {list}
- **Landing Page:** {url}
EOF

echo "✅ Sistema de memória inicializado em $NEURO_DIR"
echo ""
echo "📁 Estrutura criada:"
echo "   $NEURO_DIR/"
echo "   ├── clients/         (dados de clientes)"
echo "   ├── campaigns/       (campanhas ativas)"
echo "   ├── sessions/        (sessões por skill)"
echo "   └── shared/          (memória compartilhada)"
```

---

## Uso

### Comandos de Gerenciamento

```bash
# Inicializar memória
neuro-memory init

# Ver status
neuro-memory status

# Listar clientes
neuro-memory clients list

# Ver cliente ativo
neuro-memory client active

# Mudar cliente ativo
neuro-memory client use {client_id}

# Criar novo cliente
neuro-memory client create {client_id} --name "Nome" --industry "Indústria"

# Limpar cache
neuro-memory cache clear

# Exportar dados
neuro-memory export --client {client_id} --output ~/backup/

# Importar dados
neuro-memory import --file ~/backup/nike_2024-03-29.json
```

---

## Benefícios

1. **Contexto Persistente**: Continue de onde parou em sessões anteriores
2. **Compartilhamento**: Skills compartilham dados de clientes automaticamente
3. **Aprendizado**: Sistema aprende com cada campanha e melhora sugestões
4. **Organização**: Estrutura clara e previsível para todos os dados
5. **Backup**: Fácil exportar/importar dados de clientes
6. **Performance**: Histórico de métricas para referência futura

---

## Migração do Sistema Antigo

O sistema antigo (`~/.meta-ads-manager/`) será migrado automaticamente:

```bash
# Migrar contas existentes
neuro-memory migrate --from ~/.meta-ads-manager/
```

Arquivos migrados:
- `accounts.json` → `shared/accounts.json`
- `session.json` → `sessions/meta-ads-manager/session.json`

---

## Criado por

@monrars