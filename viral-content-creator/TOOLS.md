# Viral Content Creator - Tools

> **Ferramentas e Funções da Skill de Criação de Conteúdo Viral**

---

## 📋 Índice de Ferramentas

1. [Análise de Perfil](#1-análise-de-perfil)
2. [Análise de Post](#2-análise-de-post)
3. [Análise de Imagem](#3-análise-de-imagem)
4. [Modelagem de Estilo](#4-modelagem-de-estilo)
5. [Geração de Conteúdo](#5-geração-de-conteúdo)
6. [Dashboard](#6-dashboard)
7. [A/B Testing](#7-ab-testing)

---

## 1. Análise de Perfil

### `cv_analyze_profile`

Analisa um perfil completo de rede social.

**Parâmetros:**

```python
{
  "username": "@username",
  "plataforma": "instagram | tiktok | twitter | linkedin | youtube",
  "options": {
    "posts_limit": 50,          # Número de posts para analisar
    "include_stories": True,     # Incluir stories na análise
    "include_reels": True,       # Incluir reels na análise
    "date_range": "30d"          # Período de análise
  }
}
```

**Retorno:**

```python
{
  "perfil": {
    "username": "@username",
    "plataforma": "instagram",
    "metricas": {
      "seguidores": 50000,
      "seguindo": 200,
      "posts_total": 342,
      "engajamento_medio": 0.08,
      "alcance_estimado": 150000
    },
    
    "frequencia_postagem": {
      "posts_semana": 5,
      "melhores_dias": ["terça", "quinta", "sábado"],
      "melhores_horarios": ["07:00", "12:00", "19:00"]
    },
    
    "conteudo_analise": {
      "tipos": {
        "carousel": {"quantidade": 120, "engajamento": 0.12},
        "reels": {"quantidade": 80, "engajamento": 0.15},
        "static": {"quantidade": 100, "engajamento": 0.05},
        "stories": {"quantidade": 42, "engajamento": 0.03}
      },
      
      "temas_principais": [
        {"tema": "dicas", "frequencia": 0.4, "engajamento": 0.10},
        {"tema": "bastidores", "frequencia": 0.3, "engajamento": 0.08},
        {"tema": "tendencias", "frequencia": 0.2, "engajamento": 0.12},
        {"tema": "vendas", "frequencia": 0.1, "engajamento": 0.06}
      ],
      
      "hashtags_top": [
        {"tag": "#dicas", "usos": 45, "engajamento_medio": 0.11},
        {"tag": "#viral", "usos": 38, "engajamento_medio": 0.14},
        {"tag": "#nichada", "usos": 32, "engajamento_medio": 0.10}
      ],
      
      "hooks_efetivos": [
        "Você sabia que...",
        "A maioria não sabe...",
        "Por que isso acontece..."
      ]
    },
    
    "visual_pattern": {
      "paleta_cores": ["#000000", "#FFFFFF", "#D4AF37"],
      "estilo_composicao": "minimalista",
      "tipografia_padrao": "Inter Bold + Regular",
      "elementos_recorrentes": ["badges", "setas", "numeros"]
    },
    
    "viralidade_score": {
      "score_geral": 8.5,
      "fatores_fortes": ["hooks", "visual", "consistência"],
      "fatores_fracos": ["timing", "hashtag_density"],
      "recomendacoes": [
        "Aumentar frequência de posts em horários nobres",
        "Diversificar tipos de CTA",
        "Testar mais variações de hooks"
      ]
    }
  }
}
```

---

## 2. Análise de Post

### `cv_analyze_post`

Analisa um post específico em detalhes.

**Parâmetros:**

```python
{
  "url": "https://instagram.com/p/abc123",
  "options": {
    "analyze_visual": True,
    "analyze_copy": True,
    "analyze_engagement": True,
    "extract_template": True
  }
}
```

**Retorno:**

```python
{
  "post": {
    "url": "https://instagram.com/p/abc123",
    "id": "abc123",
    "tipo": "carousel",
    "data_publicacao": "2024-01-15T10:30:00Z",
    
    "metricas": {
      "likes": 50000,
      "comentarios": 1200,
      "compartilhamentos": 340,
      "saves": 8900,
      "engajamento_rate": 0.12,
      "viral_score": 8.7,
      
      "benchmark": {
        "vs_seguidores": "+150%",
        "vs_industria": "+80%",
        "vs_perfil": "+200%"
      }
    },
    
    "copy_analysis": {
      "estrutura": "HOOK_PROBLEM_SOLUTION_CTA",
      "componentes": {
        "hook": {
          "texto": "Você já percebeu que...",
          "tipo": "pergunta_retórica",
          "score": 9.2
        },
        "problema": {
          "texto": "A maioria das pessoas não sabe que...",
          "tipo": "problema_identificacao",
          "score": 8.5
        },
        "solucao": {
          "texto": "Isso acontece porque...",
          "tipo": "explicacao",
          "score": 8.0
        },
        "cta": {
          "texto": "Salva pra depois 💾",
          "tipo": "ação_direta",
          "score": 9.0
        }
      },
      
      "linguagem": {
        "tom": "educativo_informal",
        "pronome": "você",
        "emojis_count": 5,
        "hashtags_count": 7,
        "mentions_count": 2,
        "caracteres": 280,
        "palavras": 45,
        "frases": 6
      },
      
      "psicologia": {
        "gatilhos": ["curiosidade", "urgência", "valor"],
        "emoções": ["surpresa", "alívio", "satisfação"],
        "cognitive_load": "baixo"
      }
    },
    
    "visual_analysis": {
      "slides": 7,
      "formato": "4:5",
      "resolucao": "1080x1350",
      
      "slide_1": {
        "tipo": "capa",
        "texto": "Por que 90% erram?",
        "background": "#000000",
        "cor_texto": "#FFFFFF",
        "destaque": "#D4AF37",
        "elementos": ["badge_NOVO", "seta_baixo"],
        "hierarquia_score": 9.0
      },
      
      "paleta_geral": {
        "cores_primarias": ["#000000", "#FFFFFF", "#D4AF37"],
        "cores_secundarias": ["#1A1A25", "#2A2A3A"],
        "temperatura": "fria",
        "contraste": "alto"
      },
      
      "tipografia": {
        "headline": {"fonte": "Inter", "peso": 700, "tamanho": 48},
        "body": {"fonte": "Inter", "peso": 400, "tamanho": 24},
        "cta": {"fonte": "Inter", "peso": 600, "tamanho": 20}
      },
      
      "composicao": {
        "regra_tercos": True,
        "espaco_negativo": 40,
        "alinheamento": "centralizado",
        "fluxo_leitura": "top_down"
      }
    },
    
    "template_extraido": {
      "nome": "template_educativo_7_slides",
      "estrutura": [
        {"slide": 1, "tipo": "capa", "elementos": ["hook", "badge"]},
        {"slide": 2, "tipo": "problema", "elementos": ["texto", "icone"]},
        {"slide": 3, "tipo": "dado", "elementos": ["numero_grande", "subtitulo"]},
        {"slide": 4, "tipo": "solucao", "elementos": ["lista", "checkmarks"]},
        {"slide": 5, "tipo": "exemplo", "elementos": ["caso_real", "resultado"]},
        {"slide": 6, "tipo": "value", "elementos": ["conclusao", "beneficio"]},
        {"slide": 7, "tipo": "cta", "elementos": ["acao", "icones"]}
      ],
      "score": 8.7,
      "usos_recomendados": ["educativo", "tutorial", "dicas"]
    },
    
    "timing": {
      "dia_semana": "quarta",
      "hora": "12:00",
      "timezone": "America/Sao_Paulo",
      "razao": "horário de almoço, maior engajamento"
    },
    
    "hashtags": {
      "usadas": ["#dica", "#viral", "#tutorial"],
      "performance": {
        "#dica": {"alcance": 50000, "relevancia": 0.95},
        "#viral": {"alcance": 80000, "relevancia": 0.85},
        "#tutorial": {"alcance": 30000, "relevancia": 0.98}
      },
      "sugestoes": ["#tutorial", "#aprenda", "#descomplica"]
    }
  }
}
```

---

## 3. Análise de Imagem

### `cv_analyze_image`

Analisa uma imagem específica em detalhes visuais.

**Parâmetros:**

```python
{
  "url": "https://..." ou "base64",
  "options": {
    "extract_palette": True,
    "detect_text": True,
    "detect_elements": True,
    "analyze_composition": True,
    "score_visual": True
  }
}
```

**Retorno:**

```python
{
  "imagem": {
    "dimensoes": {
      "largura": 1080,
      "altura": 1350,
      "formato": "4:5",
      "resolucao": "alta"
    },
    
    "paleta": {
      "cores_primarias": [
        {"hex": "#000000", "nome": "Black", "porcentagem": 45},
        {"hex": "#FFFFFF", "nome": "White", "porcentagem": 35},
        {"hex": "#D4AF37", "nome": "Gold", "porcentagem": 15},
        {"hex": "#1A1A25", "nome": "Dark Blue", "porcentagem": 5}
      ],
      
      "temperatura": "fria",
      "saturacao": "baixa",
      "luminosidade": "baixa",
      "contraste": "alto",
      
      "harmonia": {
        "tipo": "complementar",
        "score": 8.5,
        "recomendacao": "Paleta equilibrada com destaque dourado"
      }
    },
    
    "tipografia": {
      "fontes_detectadas": [
        {"nome": "Inter", "peso": "bold", "confiança": 0.95},
        {"nome": "Inter", "peso": "regular", "confiança": 0.92}
      ],
      
      "tamanhos": {
        "headline": 48,
        "body": 24,
        "cta": 20
      },
      
      "hierarquia": {
        "nivel_1": {"texto": "Headline", "tamanho": 48, "peso": "bold"},
        "nivel_2": {"texto": "Subtítulo", "tamanho": 24, "peso": "regular"},
        "nivel_3": {"texto": "CTA", "tamanho": 20, "peso": "semibold"}
      },
      
      "legibilidade": {
        "score": 9.0,
        "problemas": [],
        "recomendacoes": ["Excelente contraste", "Tamanho adequado"]
      }
    },
    
    "elementos": {
      "detectados": [
        {"tipo": "badge", "quantidade": 1, "posicao": "top-right"},
        {"tipo": "seta", "quantidade": 2, "posicao": "bottom-center"},
        {"tipo": "icone", "quantidade": 3, "posicao": "distributed"},
        {"tipo": "numero", "quantidade": 1, "posicao": "center"}
      ],
      
      "proporcao_elementos": {
        "texto": 60,
        "espaco_negativo": 25,
        "elementos_visuais": 15
      }
    },
    
    "composicao": {
      "regra_tercos": {
        "aplicada": True,
        "ponto_focal": "center-top",
        "score": 8.5
      },
      
      "direcao_leitura": {
        "principal": "diagonal-descendente",
        "secundaria": "top-bottom"
      },
      
      "espaco_negativo": {
        "porcentagem": 40,
        "distribuicao": "balanced",
        "score": 8.0
      },
      
      "foco": {
        "tipo": "center-weighted",
        "intensidade": "alto",
        "clarity": "muito claro"
      }
    },
    
    "score_visual": {
      "geral": 8.5,
      "componentes": {
        "paleta": 9.0,
        "tipografia": 9.0,
        "composicao": 8.5,
        "legibilidade": 9.0,
        "atração": 8.0
      },
      
      "problemas_detectados": [],
      
      "sugestoes": [
        "Adicionar elemento surpresa no canto inferior",
        "Considerar adicionar mais contraste no CTA"
      ]
    },
    
    "match_modelo": {
      "modelo": "template_educativo",
      "compatibilidade": 0.92,
      "ajustes_necessarios": []
    }
  }
}
```

---

## 4. Modelagem de Estilo

### `cv_create_model`

Cria um modelo de estilo reutilizável.

**Parâmetros:**

```python
{
  "nome": "concessionaria_viral",
  "descricao": "Modelo para conteúdo viral de concessionárias",
  "analises_referencia": [
    "perfil_1_id",
    "perfil_2_id",
    "post_1_id",
    "post_2_id"
  ],
  
  "configuracoes": {
    "valor_padrao": {
      "paleta": ["#000000", "#FFFFFF", "#D4AF37"],
      "tipografia": {"headline": "Inter Bold 48", "body": "Inter Regular 24"},
      "formato_preferido": "carousel",
      "slides_padrao": 7
    },
    
    "pesos": {
      "visual": 0.2,
      "copy": 0.25,
      "timing": 0.15,
      "hashtags": 0.1,
      "cta": 0.15,
      "conteudo": 0.15
    }
  }
}
```

**Retorno:**

```python
{
  "modelo": {
    "id": "model_abc123",
    "nome": "concessionaria_viral",
    "versao": "1.0",
    "criado_em": "2024-01-15T10:30:00Z",
    
    "estatisticas": {
      "perfis_analisados": 5,
      "posts_analisados": 50,
      "tempo_analise": "2.5h"
    },
    
    "identidade_visual": { ... },
    "copy_framework": { ... },
    "hashtags_framework": { ... },
    "timing": { ... },
    "viralidade_factors": { ... }
  }
}
```

### `cv_list_models`

Lista todos os modelos disponíveis.

**Parâmetros:**

```python
{
  "filtro": {
    "vertical": "concessionarias",  # opcional
    "ordenar_por": "score"  # score, usos, data
  }
}
```

### `cv_delete_model`

Remove um modelo.

**Parâmetros:**

```python
{
  "model_id": "model_abc123"
}
```

### `cv_update_model`

Atualiza um modelo existente.

**Parâmetros:**

```python
{
  "model_id": "model_abc123",
  "novas_analises": ["post_5_id", "post_6_id"],
  "recalcular": True
}
```

---

## 5. Geração de Conteúdo

### `cv_generate_content`

Gera conteúdo baseado em um modelo.

**Parâmetros:**

```python
{
  "modelo": "concessionaria_viral",
  "tema": "financiamento de carro",
  
  "opcoes": {
    "formato": "carousel",           # carousel, reels, static
    "slides": 7,                       # para carousel
    "variacao": 1,                      # gerar múltiplas variações
    "ab_test": True,                    # sugere A/B tests
    "include_copy_alternatives": True,
    "include_hashtags": True,
    "include_timing": True,
    "variaveis_custom": {               # sobrescrever variáveis
      "{veiculo}": "SUV",
      "{valor}": "R$ 150.000"
    }
  }
}
```

**Retorno:**

```python
{
  "conteudo_gerado": {
    "id": "content_xyz789",
    "modelo": "concessionaria_viral",
    "tema": "financiamento de carro",
    "formato": "carousel",
    
    "slides": [
      {
        "numero": 1,
        "tipo": "capa",
        "texto": "Por que 90% pagam JUROS abusivos?",
        "visual": {
          "background": "#000000",
          "texto_cor": "#FFFFFF",
          "destaque_cor": "#D4AF37",
          "elementos": ["badge_NOVO", "seta_baixo"]
        },
        "score": 8.7
      },
      # ... mais slides
    ],
    
    "copy_completa": "Por que 90% pagam JUROS abusivos?\n\n...",
    
    "hooks_alternativos": [...],
    "ctas_alternativos": [...],
    "hashtags_sugeridas": [...],
    "timing_recomendado": {...},
    
    "ab_test_variations": [
      {
        "id": "var_a",
        "hook": "Por que 90% pagam juros abusivos?",
        "tipo": "dado_chocante"
      },
      {
        "id": "var_b",
        "hook": "O banco NÃO quer que você saiba disso.",
        "tipo": "conspiracao"
      }
    ],
    
    "viralidade_estimada": {
      "score": 8.7,
      "confianca": 0.85,
      "fatores": {
        "hook_strength": 9.0,
        "visual_appeal": 8.5,
        "value_proposition": 8.8,
        "cta_clarity": 9.2,
        "timing_match": 8.5
      }
    }
  }
}
```

### `cv_generate_batch`

Gera múltiplos conteúdos em lote.

**Parâmetros:**

```python
{
  "modelo": "concessionaria_viral",
  "temas": [
    "financiamento",
    "consórcio",
    "troca de carro",
    "manutenção"
  ],
  "por_tema": 3,  # 3 variações por tema
  "formato": "carousel"
}
```

### `cv_regenerate`

Regenera um conteúdo específico.

**Parâmetros:**

```python
{
  "content_id": "content_xyz789",
  "manter": ["visual", "timing"],  # manter estes elementos
  "alterar": ["copy", "hashtags"]  # alterar estes
}
```

---

## 6. Dashboard

### `cv_get_dashboard`

Mostra visão geral do sistema.

**Parâmetros:**

```python
{
  "periodo": "30d",
  "metricas": True,
  "tendencias": True,
  "recomendacoes": True
}
```

**Retorno:**

```python
{
  "dashboard": {
    "resumo": {
      "modelos_criados": 5,
      "perfis_analisados": 12,
      "posts_analisados": 48,
      "conteudos_gerados": 156
    },
    
    "performance": {
      "taxa_viralizacao": 0.34,
      "engajamento_medio": 0.08,
      "melhores_dias": ["terça", "quinta"],
      "melhores_horarios": ["12:00", "19:00"]
    },
    
    "tendencias": {
      "formatos_up": ["carousel", "reels"],
      "formatos_down": ["static"],
      "hashtags_trending": ["#dica", "#tutorial"],
      "topicos_trending": ["financiamento", "manutenção"]
    },
    
    "top_modelos": [
      {"nome": "ecommerce_viral", "score": 9.1, "usos": 31},
      {"nome": "concessionaria_viral", "score": 8.5, "usos": 23},
      {"nome": "imobiliaria_viral", "score": 8.2, "usos": 18}
    ],
    
    "insights": [
      {
        "insight": "Carrosséis com 7-10 slides viralizam 3x mais",
        "confianca": 0.87,
        "samples": 34
      },
      {
        "insight": "CTAs no final aumentam saves em 45%",
        "confianca": 0.92,
        "samples": 28
      }
    ],
    
    "recomendacoes": [
      "Aumentar frequência de carrosséis",
      "Testar mais variações de hooks",
      "Usar badges 'NOVO' com mais frequência"
    ]
  }
}
```

---

## 7. A/B Testing

### `cv_create_ab_test`

Cria um teste A/B.

**Parâmetros:**

```python
{
  "nome": "teste_hook_financiamento",
  "modelo": "concessionaria_viral",
  "tema": "financiamento",
  "variacoes": [
    {
      "id": "A",
      "hook": "Por que 90% pagam juros abusivos?",
      "descricao": "Dado chocante"
    },
    {
      "id": "B",
      "hook": "O banco NÃO quer que você saiba isso.",
      "descricao": "Conspiração"
    }
  ],
  "metricas": ["engajamento", "saves", "compartilhamentos"],
  "duracao_dias": 7
}
```

### `cv_analyze_ab_test`

Analisa resultados de um teste A/B.

**Parâmetros:**

```python
{
  "test_id": "test_abc123"
}
```

**Retorno:**

```python
{
  "ab_test": {
    "id": "test_abc123",
    "nome": "teste_hook_financiamento",
    "status": "concluido",
    "duracao": "7 dias",
    
    "variacoes": {
      "A": {
        "hook": "Por que 90% pagam juros abusivos?",
        "metricas": {
          "engajamento": 0.12,
          "saves": 4500,
          "compartilhamentos": 340,
          "viralizacoes": 15
        }
      },
      "B": {
        "hook": "O banco NÃO quer que você saiba isso.",
        "metricas": {
          "engajamento": 0.15,
          "saves": 5200,
          "compartilhamentos": 410,
          "viralizacoes": 18
        }
      }
    },
    
    "resultado": {
      "vencedor": "B",
      "diferenca": "+25% engajamento",
      "confianca": 0.95,
      "insight": "Hooks conspiratórios performam melhor em temas financeiros"
    },
    
    "recomendacao": "Usar variação B para temas relacionados a bancos/financiamento"
  }
}
```

---

## 📝 Formatos de Input/Output

### Input Formats Aceitos

- URLs de posts (Instagram, TikTok, Twitter, LinkedIn)
- Upload de imagens (base64)
- JSON de análise prévia
- Templates customizados

### Output Formats

- JSON completo
- Markdown simplificado
- Template exportável (Canva/Figma)
- CSV para análise

---

## 🔗 Endpoints

Se usando via MCP ou API:

```
POST /cv/analyze/profile
POST /cv/analyze/post
POST /cv/analyze/image
POST /cv/model/create
POST /cv/model/list
POST /cv/model/delete
POST /cv/model/update
POST /cv/generate/content
POST /cv/generate/batch
POST /cv/generate/regenerate
GET  /cv/dashboard
POST /cv/ab/create
POST /cv/ab/analyze
```

---

## 📊 Cache e Persistência

### Cache

- Análises de perfil: 24 horas
- Análises de post: 48 horas
- Modelos: permanente (até exclusão)
- Dashboards: 1 hora

### Armazenamento

```python
~/.neuro-skills/viral-content-creator/
├── cache/
│   ├── profiles/
│   ├── posts/
│   └── images/
├── models/
│   ├── concessionaria_viral.json
│   ├── imobiliaria_viral.json
│   └── ecommerce_viral.json
├── generated/
│   └── content/
└── config.yml
```