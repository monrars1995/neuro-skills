# Viral Content Creator

> **Skill de Criação de Conteúdo Viral baseada em Análise de Perfis**  
> Analisa perfis, posts, copies, imagens e estilo para modelar e gerar conteúdo viral.

## 🎯 Overview

Esta skill permite criar conteúdo viral de forma sistemática através de:

1. **Análise de Perfis** - Extrai padrões de sucesso de perfis virais
2. **Análise de Posts** - Identifica o que torna um post viral
3. **Análise de Imagens** - Detecta padrões visuais que funcionam
4. **Modelagem de Estilo** - Cria "DNA de viralização" reutilizável
5. **Geração de Conteúdo** - Produz conteúdo baseado em modelos provados

## 📦 Instalação

### Via npx (Recomendado)

```bash
npx @goldneuronio/neuro-skills viral-content-creator
```

### Manual

```bash
cd ~/neuro-skills/viral-content-creator
pip install -r requirements.txt
```

## 🚀 Uso Rápido

### CLI

```bash
# Analisar perfil
python -m viral_content_creator cv-analyze @concessionaria_exemplo instagram

# Criar modelo de estilo
python -m viral_content_creator cv-model concessionaria_viral --descricao "Modelo para concessionárias"

# Gerar conteúdo
python -m viral_content_creator cv-generate concessionaria_viral "financiamento"

# Ver dashboard
python -m viral_content_creator cv-dashboard
```

### Python API

```python
from viral_content_creator import ProfileAnalyzer, ContentGenerator

# Analisar perfil
analyzer = ProfileAnalyzer()
perfil = analyzer.analyze("@concessionaria_exemplo", "instagram")

# Criar modelo
from viral_content_creator import StyleModeler
modeler = StyleModeler()
modelo = modeler.create_model(
    "concessionaria_viral",
    "Modelo para concessionárias",
    ["perfil_1_id", "post_1_id"]
)

# Gerar conteúdo
generator = ContentGenerator()
conteudo = generator.generate(
    "concessionaria_viral",
    "financiamento",
    {"formato": "carousel", "slides": 7}
)
```

## 📖 Comandos

### `cv-analyze` - Análise de Perfil

```bash
python -m viral_content_creator cv-analyze @username [plataforma] [opções]

# Plataformas: instagram, tiktok, twitter, linkedin, youtube
# Opções:
#   --posts-limit N    Número de posts para analisar (default: 50)
#   --output FILE      Salvar resultado em arquivo JSON
```

### `cv-post` - Análise de Post

```bash
python -m viral_content_creator cv-post [url] [opções]

# Opções:
#   --analyze-visual   Incluir análise visual completa
#   --output FILE      Salvar resultado em arquivo JSON
```

### `cv-image` - Análise de Imagem

```bash
python -m viral_content_creator cv-image [url_ou_arquivo] [opções]

# Analisa paleta de cores, tipografia, composição e score visual
```

### `cv-model` - Criar Modelo de Estilo

```bash
python -m viral_content_creator cv-model [nome] [opções]

# Opções:
#   --descricao DESC      Descrição do modelo
#   --analises ID1 ID2...  IDs de análises de referência
#   --output FILE          Salvar resultado em arquivo JSON
```

### `cv-generate` - Gerar Conteúdo

```bash
python -m viral_content_creator cv-generate [modelo] [tema] [opções]

# Opções:
#   --formato FORMATO   carousel, reels, ou static (default: carousel)
#   --slides N           Número de slides (default: 7)
#   --ab-test             Gerar variações A/B
#   --output FILE         Salvar resultado em arquivo JSON
```

### `cv-dashboard` - Ver Dashboard

```bash
python -m viral_content_creator cv-dashboard [opções]

# Opções:
#   --periodo PERIODO     Período de análise (default: 30d)
#   --formato FORMATO     json ou markdown (default: json)
```

## 🎨 Modelos por Vertical

### Concessionárias
```python
{
  "variaveis": {
    "{veiculo}": ["carro", "SUV", "sedan", "hatch", "pickup"],
    "{marca}": ["Toyota", "Honda", "VW", "Chevrolet", "Hyundai"],
    "{valor}": ["R$ 50.000", "R$ 80.000", "R$ 120.000"]
  }
}
```

### Imobiliárias
```python
{
  "variaveis": {
    "{imovel}": ["apartamento", "casa", "terreno", "cobertura"],
    "{bairro}": ["Centro", "Zona Sul", "Zona Norte"],
    "{quartos}": ["1 quarto", "2 quartos", "3 quartos", "4 quartos"]
  }
}
```

### E-commerce
```python
{
  "variaveis": {
    "{produto}": ["produto A", "produto B", "produto C"],
    "{desconto}": ["30%", "50%", "70%"],
    "{urgencia}": ["últimas unidades", "últimas horas", "último dia"]
  }
}
```

## 📊 Output Example

```python
{
  "conteudos_gerados": [{
    "tipo": "carousel",
    "slides": 7,
    "viralidade_score": 8.7,
    
    "slide_1": {
      "tipo": "capa",
      "texto": "Por que 90% das pessoas pagam JUROS abusivos no financiamento?",
      "visual": {
        "background": "#000000",
        "texto_cor": "#FFFFFF",
        "destaque_cor": "#D4AF37"
      }
    }
    // ... mais slides
  }],
  
  "hashtags": ["#financiamentodecarro", "#consórcio", "#dicafinanceira"],
  "timing_recomendado": {
    "melhor_dia": "quarta",
    "melhor_horario": "12:00"
  }
}
```

## 🔧 Configuração

Arquivo: `~/.neuro-skills/viral-content-creator/config.yml`

```yaml
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

## 🔗 Integrações

### APIs Necessárias

| API | Uso | Prioridade |
|-----|-----|------------|
| Instagram Graph API | Analisar posts, métricas | Alta |
| TikTok API | Analisar vídeos virais | Média |
| Twitter/X API | Analisar threads | Baixa |
| Vision API | Análise de imagens | Alta |
| Content API | Gerar variações | Alta |

## 📝 Exemplos Práticos

### Exemplo: Concessionária

**Input:**
```bash
cv-generate concessionaria_viral "consórcio contemplado"
```

**Output:**
```
🎯 MÚLTIPLAS CONTAS DO MESMO CÓDIGO: COMO TOCAR ISSO?

4 slides para tocar múltiplas contemplações:

1. CAPA: "Você sabia que dá pra ter 2 contemplações no mesmo grupo?"
   
2. DADO: "8% dos consorciados contemplam mais de uma vez por grupo"
   
3. COMO: 
   - Lance sempre o máximo que pode
   - Sistema ignora lances pendentes
   - Use crédito + lance
   
4. CTA: "Salva essa estratégia e manda pro amigo"

#consórcio #contemplado #dicaconcessionária
```

## 📁 Estrutura de Arquivos

```
viral-content-creator/
├── __init__.py
├── cli.py                   # Interface de linha de comando
├── requirements.txt         # Dependências Python
├── SKILL.md                 # Documentação da skill
├── TOOLS.md                 # Documentação das ferramentas
├── README.md                # Este arquivo
│
├── analyzer/                # Analisadores
│   ├── __init__.py
│   ├── profile_analyzer.py   # Análise de perfis
│   ├── post_analyzer.py      # Análise de posts
│   └── image_analyzer.py     # Análise de imagens
│
├── models/                   # Modelagem de estilo
│   ├── __init__.py
│   └── style_model.py        # Criador de modelos
│
├── generator/                # Geradores de conteúdo
│   ├── __init__.py
│   └── content_generator.py  # Gerador principal
│
└── utils/                    # Utilitários
    ├── __init__.py
    └── dashboard.py           # Dashboard e estatísticas
```

## 🆘 Suporte

Para dúvidas e sugestões:
- GitHub: https://github.com/monrars1995/neuro-skills/issues
- Instagram: @monrars
- Comunidade: https://goldneuron.io/drops

## 📄 Licença

MIT License - Copyright (c) 2026 GoldNeuron  
Criador: @monrars (Instagram)

---

**Parte do projeto [Neuro Skills](https://github.com/monrars1995/neuro-skills)**