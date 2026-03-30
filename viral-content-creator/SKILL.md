# Viral Content Creator

> **Criador de Conteúdo Viral baseado em Análise de Perfis**  
> Analisa perfis, posts, copies, imagens e estilo para modelar e gerar conteúdo viral.

## 🎯 O que esta skill faz

Esta skill analisa perfis de redes sociais e cria um modelo de estilo que pode ser usado para gerar conteúdo viral similar. Ela:

1. **Analisa Perfis** - Extrai padrões de sucesso de perfis virais
2. **Analisa Posts** - Identifica o que torna um post viral
3. **Analisa Copies** - Modela o estilo de escrita
4. **Analisa Imagens** - Identifica padrões visuais
5. **Modela Estilo** - Cria um "DNA de viralização"
6. **Gera Conteúdo** - Produz conteúdo baseado no modelo

---

## 📊 Análise de Perfil

### Inputs Necessários

```
/cv-analyze @username [plataforma]
```

**Plataformas suportadas:**
- Instagram (@username)
- TikTok (@username)
- Twitter/X (@username)
- LinkedIn (in/username)
- YouTube (@username)

### Dados Extraídos

#### Métricas de Perfil
| Métrica | Descrição | Peso |
|---------|-----------|------|
| Seguidores | Total de seguidores | 0.1 |
| Engajamento médio | (likes+comentários)/seguidores | 0.3 |
| Frequência de posts | Posts por semana | 0.1 |
| Taxa de viralização | % de posts com >2x engajamento médio | 0.3 |
| Consistência | Manutenção de estilo ao longo do tempo | 0.2 |

#### Análise de Conteúdo
| Dimensão | Métricas |
|-----------|----------|
| **Formato** | Carrossel, Reels, Stories, Static, Video |
| **Duração ideal** | Tempo médio dos posts virais |
| **Legenda** | Estrutura, componentes, variáveis |
| **CTA** | Tipos, posição, eficácia |
| **Hashtags** | Quantidade, relevância, posicionamento |

#### Análise Visual
| Dimensão | Métricas |
|-----------|----------|
| **Paleta de cores** | Cores predominantes (HEX) |
| **Tipografia** | Fontes, tamanhos, hierarquia |
| **Composição** | Regra dos terços, ponto focal |
| **Estilo** | Minimalista, maximalista, documental |
| **Filtros** | Tipos de filtro usados |

---

## 🔬 Análise de Post

### Comando: `/cv-post [url]`

Analisa um post específico e extrai:

```python
{
  "post": {
    "url": "https://...",
    "plataforma": "instagram",
    "tipo": "carousel",
    "formato": "3:4",
    
    "metricas": {
      "likes": 50000,
      "comentarios": 1200,
      "compartilhamentos": 340,
      "saves": 8900,
      "engajamento_rate": 0.12
    },
    
    "copy": {
      "estrutura": "HOOK_PROBLEM_SOLUTION_CTA",
      "hook": "Você já percebeu que...",
      "corpo": "Isso acontece porque...",
      "ctas": ["Salva pra depois", "Comenta X"],
      "hashtags": ["#dica", "#viral"],
      "emoji_count": 5,
      "mention_count": 2
    },
    
    "visual": {
      "cores": ["#000000", "#FFFFFF", "#D4AF37"],
      "fontes": ["Inter", "JetBrains Mono"],
      "elementos": ["seta", "badge", "numero"],
      "hierarquia": {
        "headline_size": 48,
        "body_size": 24,
        "cta_size": 20
      }
    },
    
    "viralidade": {
      "score": 8.5,
      "fatores": [
        {"fator": "hook_forte", "peso": 0.3},
        {"fator": "formato_carrossel", "peso": 0.2},
        {"fator": "ctas_multiplos", "peso": 0.15},
        {"fator": "design_limpo", "peso": 0.15},
        {"fator": "timing", "peso": 0.1}
      ]
    }
  }
}
```

---

## 🧬 Modelagem de Estilo

### Comando: `/cv-model [nome-do-modelo]`

Cria um modelo de estilo reutilizável baseado nas análises:

```python
{
  "modelo": "concessionaria_viral",
  "versao": "1.0",
  
  "identidade_visual": {
    "paleta": {
      "primaria": "#000000",
      "secundaria": "#FFFFFF",
      "destaque": "#D4AF37",
      "fundo": "#0A0A0F"
    },
    "tipografia": {
      "headline": {"fonte": "Inter", "peso": 700, "tamanho": 48},
      "body": {"fonte": "Inter", "peso": 400, "tamanho": 24},
      "cta": {"fonte": "Inter", "peso": 600, "tamanho": 20}
    },
    "elementos": {
      "badges": True,
      "setas": True,
      "icones": True,
      "numeros": True
    },
    "composicao": {
      "margem": 40,
      "padding": 20,
      "espaco_entre_slides": 10
    }
  },
  
  "copy_framework": {
    "hooks": [
      "Você sabia que {insight_surpreendente}?",
      "A maioria das {audiencia} não sabe que {problema}.",
      "{numero}% das pessoas erram ao {acao}.",
      "Por que {objeto} custa tão caro? A resposta vai te surpreender."
    ],
    "estruturas": [
      "HOOK → PROBLEMA → SOLUÇÃO → CTA",
      "CONTRASTE → INFORMAÇÃO → BENEFÍCIO → CTA",
      "DADO → CONTEXTO → APLICAÇÃO → CTA"
    ],
    "ctas": [
      "Salva para ver depois 💾",
      "Comenta SIM se você faz isso ✅",
      "Envia para quem precisa saber 📤",
      "Segue para mais dicas assim 👆"
    ]
  },
  
  "hashtags_framework": {
    "estrategia": "fita_infinita",
    "quantidade_min": 5,
    "quantidade_max": 10,
    "categorias": [
      "branded: #marca",
      "行业标准: #industria",
      "nichada: #niche",
      "tendencia: #trending"
    ]
  },
  
  "timing": {
    "dias_melhores": ["segunda", "quarta", "sexta"],
    "horarios_melhores": ["07:00", "12:00", "18:00", "21:00"],
    "duracao_ideal_segundos": {"reels": 15, "carrossel": "scroll_natural"}
  },
  
  "viralidade_factors": {
    "pesos": {
      "hook_strength": 0.25,
      "visual_appeal": 0.20,
      "value_proposition": 0.20,
      "cta_clarity": 0.15,
      "timing": 0.10,
      "hashtag_strategy": 0.10
    },
    "threshold_viral": 7.5,
    "threshold_muito_viral": 9.0
  }
}
```

---

## ✨ Geração de Conteúdo

### Comando: `/cv-generate [modelo] [tema]`

Gera conteúdo baseado no modelo:

```
/cv-generate concessionaria_viral "financiamento de carro"
```

**Output:**

```python
{
  "conteudos_gerados": [
    {
      "tipo": "carrossel",
      "slides": 7,
      "viralidade_score": 8.7,
      
      "slide_1": {
        "tipo": "capa",
        "texto": "Por que 90% das pessoas pagam JUROS abusivos no financiamento?",
        "visual": {
          "background": "#000000",
          "texto_cor": "#FFFFFF",
          "destaque_cor": "#D4AF37",
          "elementos": ["badge: NOVO", "seta: para baixo"]
        }
      },
      
      "slide_2": {
        "tipo": "problema",
        "texto": "Porque ninguém te conta que os juros são NEGOCIÁVEIS.",
        "visual": {
          "background": "#0A0A0F",
          "texto_cor": "#FFFFFF",
          "destaque_texto": "NEGOCIÁVEIS"
        }
      },
      
      "slide_3": {
        "tipo": "dado",
        "texto": "Em média, você pode reduzir 30% dos juros só pedindo.",
        "visual": {
          "numero_grande": "30%",
          "subtexto": "de desconto nos juros",
          "icone": "grafico_descendo"
        }
      },
      
      "slide_4": {
        "tipo": "solucao",
        "texto": "3 passos para financiar SEM ser explorado:",
        "items": [
          "Pesquise ao menos 5 bancos",
          "Negocie a taxa, não a parcela",
          "Leve um print da concorrência"
        ]
      },
      
      "slide_5": {
        "tipo": "exemplo",
        "texto": "João economizou R$ 12.000 em 48 meses fazendo isso.",
        "visual": {
          "before": "R$ 48.000",
          "after": "R$ 36.000",
          "economia": "R$ 12.000"
        }
      },
      
      "slide_6": {
        "tipo": "value",
        "texto": "Agora você sabe o que 90% não sabia.",
        "visual": {
          ".background": "#D4AF37",
          "texto_cor": "#000000"
        }
      },
      
      "slide_7": {
        "tipo": "cta",
        "texto": "Salva essa apresentação 💾\nManda pro amigo que tá comprando carro 📤",
        "visual": {
          "icones": ["salvar", "compartilhar"],
          "setas_para_cta": True
        }
      }
    }
  ],
  
  "copy_alternativas": {
    "hooks": [
      "Você já pagou mais de R$ 1000 em juros sem saber?",
      "O vendedor TE conta isso? Claro que não.",
      "A taxa que eles oferecem é REAL ou é o máximo que você aceita?"
    ],
    "ctas": [
      "Salva agora antes de financiar 💾",
      "Envia profriend que tá comprando carro 📤",
      "Comenta FINANCIAMENTO que te mando o passo a passo ✅"
    ]
  },
  
  "hashtags": [
    "#financiamentodecarro",
    "#consórcio",
    "#dicafinanceira",
    "#carroNovo",
    "#juros",
    "#economia",
    "#carrodosonho"
  ],
  
  "timing_recomendado": {
    "melhor_dia": "quarta",
    "melhor_horario": "12:00",
    "razao": "horário de almoço, maior engajamento em conteúdo financeiro"
  },
  
  "ab_test_suggestions": [
    {
      "variacao": "A",
      "hook": "Por que 90% pagam juros abusivos?",
      "tipo": "dado_chocante"
    },
    {
      "variacao": "B",
      "hook": "O banco NÃO quer que você saiba disso.",
      "tipo": "conspiracao"
    }
  ]
}
```

---

## 📐 Templates de Conteúdo

### Carrossel Educativo

```python
{
  "template": "carousel_educativo",
  "slides_padrao": 5,
  "estrutura": [
    "CAPA: Hook visual",
    "SLIDE 1: Problema identificacao",
    "SLIDE 2: Dado suporte",
    "SLIDE 3: Solução passo a passo",
    "SLIDE 4: Value/Benefício",
    "SLIDE 5: CTA com interacao"
  ],
  "duracao_media_leitura": "45 segundos",
  "formato_imagem": "4:5",
  "resolucao_minima": "1080x1350"
}
```

### Reels Viral

```python
{
  "template": "reels_viral",
  "duracao_segundos": [7, 15, 30],
  "estrutura": {
    "0-3s": "Hook visual + textual",
    "3-10s": "Desenvolvimento rapido",
    "10-15s": "Climax / revelacao",
    "15-30s": "CTA + repete loop"
  },
  "elementos_obrigatorios": [
    "Legenda sincronizada",
    "CTA no inicio E no fim",
    "Texto na tela destacando palavras-chave",
    "Audio trending ou original com gancho"
  ]
}
```

### Post Estático

```python
{
  "template": "post_estático",
  "formato": "1:1 ou 4:5",
  "estrutura_visual": {
    "zona_atencao": "33% superior",
    "texto_principal": "centro",
    "cta": "20% inferior",
    "elemento_surpresa": "canto inferior direito"
  },
  "copy_limites": {
    "titulo_max": 10,
    "corpo_max": 25,
    "cta_max": 15
  }
}
```

---

## 🎨 Análise Visual

### Comando: `/cv-analyze-image [url]`

Analisa uma imagem e extrai:

```python
{
  "analise_visual": {
    "paleta": {
      "cores_primarias": ["#000000", "#FFFFFF", "#D4AF37"],
      "cores_secundarias": ["#1A1A25", "#2A2A3A"],
      "temperatura": "fria",
      "saturacao": "baixa"
    },
    
    "composicao": {
      "regra_tercos": True,
      "ponto_focal": "centro-superior",
      "direcao_leitura": "diagonal-descendente",
      "espaco_negativo": 40
    },
    
    "tipografia": {
      "fontes_detectadas": ["Inter", "JetBrains Mono"],
      "tamanhos": {
        "headline": 48,
        "body": 24,
        "cta": 20
      },
      "pesos": {
        "headline": "bold",
        "body": "regular",
        "cta": "semibold"
      }
    },
    
    "elementos": {
      "badges": 2,
      "setas": 1,
      "icones": 3,
      "numeros": 1,
      "barras_progresso": 0
    },
    
    "hierarquia_visual": {
      "nivel_1": "headline",
      "nivel_2": "subtitulo",
      "nivel_3": "corpo",
      "nivel_4": "cta"
    },
    
    "score_visual": 8.5,
    "problemas_detectados": [],
    "sugestoes": [
      "Aumentar contraste no CTA",
      "Adicionar elemento surpresa no canto inferior"
    ]
  }
}
```

---

## 📊 Dashboard de Análise

### Comando: `/cv-dashboard`

Mostra resumo de todos os modelos e análises:

```python
{
  "dashboard": {
    "modelos_criados": 5,
    "perfis_analisados": 12,
    "posts_analisados": 48,
    
    "insights_top": [
      {
        "insight": "Carrosséis com 7-10 slides têm 3x mais engajamento",
        "confidence": 0.87,
        "samples": 34
      },
      {
        "insight": "CTAs no final aumentam saves em 45%",
        "confidence": 0.92,
        "samples": 28
      },
      {
        "insight": "Posts com badge 'NOVO' viralizam 2x mais",
        "confidence": 0.76,
        "samples": 19
      }
    ],
    
    "modelos_disponiveis": [
      {"nome": "concessionaria_viral", "score_medio": 8.5, "usos": 23},
      {"nome": "imobiliaria_viral", "score_medio": 8.2, "usos": 18},
      {"nome": "ecommerce_viral", "score_medio": 9.1, "usos": 31},
      {"nome": "educacao_viral", "score_medio": 7.9, "usos": 15},
      {"nome": "saude_viral", "score_medio": 8.0, "usos": 12}
    ],
    
    "performance_recente": {
      "conteudos_gerados": 156,
      "taxa_viralizacao": 0.34,
      "engajamento_medio": 0.08
    }
  }
}
```

---

## 🔄 Fluxo de Uso

### 1. Setup Inicial

```
/cv-setup
```

Inicializa o sistema com suas preferências de vertical.

### 2. Analisar Perfis de Referência

```
/cv-analyze @concessionaria_exemplo instagram
/cv-analyze @imobiliaria_sucesso instagram
/cv-analyze @ecommerce_viral tiktok
```

### 3. Criar Modelo de Estilo

```
/cv-model concessionaria_viral
```

### 4. Gerar Conteúdo

```
/cv-generate concessionaria_viral "financiamento"
/cv-generate concessionaria_viral "troca de carro"
/cv-generate concessionaria_viral "manutenção"
```

### 5. Analisar Resultados

```
/cv-post [url_do_post_gerado]
/cv-dashboard
```

---

## 🎯 Variáveis Dinâmicas por Vertical

### Concessionárias
```python
{
  "variaveis": {
    "{veiculo}": ["carro", "SUV", "sedan", "hatch", "pickup"],
    "{marca}": ["Toyota", "Honda", "VW", "Chevrolet", "Hyundai"],
    "{valor}": ["R$ 50.000", "R$ 80.000", "R$ 120.000"],
    "{problema}": ["juro alto", "entrada grande", "documentação"],
    "{solucao}": ["financiamento", "consórcio", "usado certificado"],
    "{prazo}": ["48 meses", "60 meses", "72 meses"],
    "{economia}": ["R$ 5.000", "R$ 10.000", "R$ 20.000"]
  }
}
```

### Imobiliárias
```python
{
  "variaveis": {
    "{imovel}": ["apartamento", "casa", "terreno", "cobertura"],
    "{bairro}": ["Centro", "Zona Sul", "Zona Norte"],
    "{quartos}": ["1 quarto", "2 quartos", "3 quartos", "4 quartos"],
    "{valor}": ["R$ 300.000", "R$ 500.000", "R$ 800.000"],
    "{vaga}": ["1 vaga", "2 vagas", "sem vaga"],
    "{diferencial}": ["varanda", "área de lazer", "próximo metrô"]
  }
}
```

### E-commerce
```python
{
  "variaveis": {
    "{produto}": ["produto A", "produto B", "produto C"],
    "{categoria}": ["eletrônicos", "moda", "casa", "beleza"],
    "{desconto}": ["30%", "50%", "70%"],
    "{prazo}": ["1 dia", "3 dias", "7 dias"],
    "{beneficio}": ["frete grátis", "cashback", "brinde"],
    "{urgencia}": ["últimas unidades", "últimas horas", "último dia"]
  }
}
```

---

## 🚀 Integrações

### APIs Necessárias

| API | Uso | Prioridade |
|-----|-----|------------|
| Instagram Graph API | Analisar posts, métricas | Alta |
| TikTok API | Analisar vídeos virais | Média |
| Twitter/X API | Analisar threads | Baixa |
| Vision API | Análise de imagens | Alta |
| Content API | Gerar variações | Alta |

### Ferramentas Integradas

- **Meta Ads Manager**: Para confirmar métricas de campanhas
- **Canva/Figma**: Para gerar templates visuais
- **Trends API**: Para identificar trends em tempo real
- **Hashtag API**: Para sugestão de hashtags relevantes

---

## 📝 Exemplos Práticos

### Exemplo 1: Concessionária

**Input:**
```
/cv-generate concessionaria_viral "consórcio contemplado"
```

**Output:**
```
🎯 MÚLTIPLAS CONTAS DO MESMO CÓDIGO: COMO TOCAR ISSO?

4 slides para tocar múltiplas contemplações:

1. CAPA: "Você sabia que dá pra ter 2 contemplações no mesmo grupo?"
   
2. DADO: "8% dos consorciados contemplam mais de uma vez por grupo"
   
3. COMO: 
   - Lance sempre o máximo que pode
   - Sistema ignora its pendentes
   - Use crédito + lance
   
4. CTA: "Salva essa estratégia e manda pro amigo"

#consórcio #contemplado #dicaconcessionária
```

### Exemplo 2: Imobiliária

**Input:**
```
/cv-generate imobiliaria_viral "apartamento 2 quartos"
```

**Output:**
```
🏠 APARTAMENTO 2 QUARTOS: O que ninguém te conta

5 slides reveladores:

1. CAPA: "Por que 2 quartos pode ser MELHOR que 3?"
   
2. MATEMÁTICA:
   - 2 quartos = R$ 400.000
   - 3 quartos = R$ 550.000
   - Diferença: R$ 150.000 PODE comprar depois
   
3. GANHO ESPACIAL:
   - Quartos maiores
   - Área de lazer melhor
   - Localização premium
   
4. REALIDADE:
   "90% dormem em 1 quarto só"
   
5. CTA: "Comenta QUARTOS que mando mais análises assim"

#imoveisp #apartamento #dica
```

---

## ⚙️ Configuração

### Arquivo de Configuração

```yaml
# ~/.neuro-skills/viral-content-creator/config.yml

default_vertical: concessionarias
analytics_enabled: true
cache_duration_days: 30

visual_analysis:
  color_extraction: true
  typography_detection: true
  composition_analysis: true

generation:
  default_format: carousel
  default_slides: 7
  ab_test_variations: 2
  viral_threshold: 7.5

integrations:
  instagram_graph_api: true
  tiktok_api: true
  vision_api: true
```

---

## 🔒 Limitações e Considerações

### Limitações
- Análise requer acesso público aos perfis
- API do TikTok tem rate limiting
- Imagens de alta qualidade aumentam tempo de análise
- Gerar imagens requer API de imagem

### Boas Práticas
- Analise pelo menos 10 perfis por vertical
- Crie modelos específicos por tipo de conteúdo
- Teste variações com A/B testing
- Atualize modelos mensalmente
- Valide scores com métricas reais

---

## 🆘 Suporte

Para dúvidas e sugestões:
- GitHub: https://github.com/monrars1995/neuro-skills/issues
- Instagram: @monrars
- Comunidade: https://goldneuron.io/drops