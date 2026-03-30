# Neuro Skills

> **O bastidor técnico que o mercado não mostra**  
> Framework de automação de Meta Ads para Claude Code, OpenAI Codex e Gemini CLI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub release](https://img.shields.io/badge/version-v2.2.0--beta-blue)](https://github.com/monrars1995/neuro-skills)
[![Made in Brazil](https://img.shields.io/badge/Made%20in-Brazil-green)](https://goldneuron.io/)

**🌐 Site Oficial:** [goldneuron.io](https://goldneuron.io/)  
**📧 Newsletter:** [Drops](https://goldneuron.io/drops) - Estudos de caso semanais  
**📸 Instagram:** [@monrars](https://instagram.com/@monrars)  

---

## 🎯 Por Que Neuro Skills?

O mercado de tráfego pago tem um problema: **todo mundo mostra o resultado, ninguém mostra o processo.**

Cursos ensinam teoria. Ferramentas prometem automação mágica. Mas na hora de executar, você fica só com:
- Briefings incompletos
- Processos que não escalam
- Atribuição quebrada
- Decisões no escuro

**Neuro Skills é diferente.**

Construído por quem vive o jogo real. Cada skill, cada automação, cada workflow foi testado em operações reais de tráfego pago. Não é teoria. É implementação.

---

## 🏗️ O Que Você Vai Encontrar

### Para Donos de Operação
- **Processo** → Workflows validados em operações de R$100k+/mês
- **Rastreabilidade** → Atribuição completa do funil, do clique à venda
- **Automação** → Cron jobs, sincronização offline, otimização automática

### Para Heads e Gestores
- **Decisão** → Dados para tomar decisões baseadas em ROI/ROAS real
- **Execução** → Implementação rápida com skills prontos para usar
- **Escala** → Templates que funcionam e podem ser replicados

### Newsletter Drops
Toda semana, estudos de caso reais:
- **Implementações** → Como resolvemos problemas reais
- **Treinamentos** → Técnicas que funcionam
- **Bastidores** → O que o mercado não mostra

**Assine gratuitamente:** [goldneuron.io/drops](https://goldneuron.io/drops)

---

## 📁 Agentes por Vertical

Cada vertical tem características únicas. Criei agentes especializados que entendem:

### 🚗 Concessionárias
> **Ciclo de venda longo (7-90 dias)** | Conversão offline obrigatória

- Janela de atribuição: 7-90 dias
- Integração CRM (Salesforce, HubSpot, Pipedrive)
- Conversão offline com hash SHA256
- ROI com margem de financiamento
- Targeting por tipo de veículo

**[SKILL.md](agents/concessionarias/SKILL.md)** | **[TOOLS.md](agents/concessionarias/TOOLS.md)**

---

### 🏠 Imobiliárias
> **Ticket médio alto (R$300k-2M)** | LTV + comissão (3-6%)

- Inventário único por localização
- Tours virtuais como conversão
- Product Catalog para imóveis
- Remarketing de propriedades visualizadas
- LTV por cliente

**[SKILL.md](agents/imobiliarias/SKILL.md)** | **[TOOLS.md](agents/imobiliarias/TOOLS.md)**

---

### 🛒 E-commerce
> **Ciclo curto (1-7 dias)** | DPA + Catálogo

- Dynamic Product Ads essencial
- Cart abandonment campaigns
- Real-time events (AddToCart, Purchase)
- Scale fast movers automaticamente
- ROI = (Margem - CPA) / CPA

**[SKILL.md](agents/ecommerce/SKILL.md)** | **[TOOLS.md](agents/ecommerce/TOOLS.md)**

---

### 🎓 Educação
> **Sazonalidade forte** | LTV alto (48 meses × mensalidade)

- Vestibular, volta às aulas, férias
- Lead scoring + CRM
- Modelo de assinatura
- Matrícula online/offline
- ROI por aluno

**[SKILL.md](agents/educacao/SKILL.md)** | **[TOOLS.md](agents/educacao/TOOLS.md)**

---

### 🏥 Saúde
> **Compliance LGPD/HIPAA** | Privacidade primeiro

- Targeting privacy-safe
- Consultas e agendamentos como conversão
- LTV + indicação (boca a boca forte)
- Auditoria mensal obrigatória
- Não pode interesses sensíveis

**[SKILL.md](agents/saude/SKILL.md)** | **[TOOLS.md](agents/saude/TOOLS.md)**

---

## 🧠 Skills Principais

### neuro-ads-manager
> **Gerenciador completo com CRUD, Analytics e Automação**

```
CRUD Completo            → Criar, listar, editar, deletar
Analytics/Relatórios     → Métricas, dashboards, performance
Automação/Otimização     → Regras automáticas, escala, pausa
Integração API v21.0     → Cliente completo Meta Graph API
```

### meta-ads-manager
> **Gerenciador de tráfego com briefing e criativos**

```
Memória Persistente     → Contas salvas, histórico
Criação de Campanhas     → Briefing + criativos
Testes A/B              → Framework completo
Playbook de Escala      → Horizontal + vertical
Diagnostics             → Performance + benchmarks
```

### traffic-strategist
> **Preparação de campanhas (use ANTES de criar)**

```
Analisa pastas          → Verifica briefing e assets
Valida briefings        → Identifica lacunas
Organiza arquivos       → Renomeia, estrutura
Gera documentação       → analise.md, checklist.md
```

### ad-copywriter
> **Copy on-brand para todos os formatos**

```
Análise de voz          → Extrai tom da marca
Variações A/B           → Testa títulos, textos, CTAs
Formatos Meta           → Feed, Stories, Reels, Carousel
Otimização              → Específico por plataforma
```

---

## 🔄 Fluxo de Trabalho

```
┌─────────────────────┐     ┌─────────────────┐     ┌────────────────────┐
│  traffic-strategist │ ──► │  ad-copywriter  │ ──► │  neuro-ads-manager │
│      (prepara)      │     │     (copy)      │     │     (executa)      │
└─────────────────────┘     └─────────────────┘     └────────────────────┘
         │                           │                        │
    analise.md                 copy_variants.md         campaign criada
    checklist.md               brand_voice.json         ads lançados
    arquivos organizados       targeting.json           otimização ativa
```

**1. Prepara** → Traffic Strategist valida briefing e assets  
**2. Copy** → Ad Copywriter gera variações on-brand  
**3. Executa** → Neuro/Meta Ads Manager cria e lança campanhas  

---

## 🚀 Instalação Rápida

### Claude Code (Anthropic)

```bash
git clone https://github.com/monrars1995/neuro-skills.git
cp -r neuro-skills/meta-ads-manager ~/.claude/skills/
cp -r neuro-skills/traffic-strategist ~/.claude/skills/
cp -r neuro-skills/ad-copywriter ~/.claude/skills/
cp -r neuro-skills/neuro-ads-manager ~/.claude/skills/
cp -r neuro-skills/agents ~/.claude/skills/
```

### OpenAI Codex

```bash
git clone https://github.com/monrars1995/neuro-skills.git
cp -r neuro-skills/meta-ads-manager ~/.codex/skills/
cp -r neuro-skills/traffic-strategist ~/.codex/skills/
cp -r neuro-skills/ad-copywriter ~/.codex/skills/
```

### Gemini CLI / OpenCode

```bash
git clone https://github.com/monrars1995/neuro-skills.git
# Gemini
cp -r neuro-skills/* ~/.gemini/skills/
# OpenCode
cp -r neuro-skills/* ~/.opencode/skills/
```

---

## 📋 Comandos Principais

### Traffic Strategist

| Comando | Ação |
|--------|------|
| `analise {cliente}` | Analisa pasta do cliente |
| `prepara {cliente}` | Prepara para criação de campanha |
| `check {cliente}` | Valida checklist |
| `organiza {cliente}` | Organiza arquivos |

### Ad Copywriter

| Comando | Ação |
|--------|------|
| `analisa voz {cliente}` | Extrai voz da marca |
| `cria copy {cliente}` | Gera copy on-brand |
| `variantes {cliente}` | Variações para A/B |
| `ajusta tom {cliente}` | Ajusta baseado em feedback |

### Meta Ads Manager

| Comando | Ação |
|--------|------|
| `/meta-ads setup` | Configura conta |
| `/meta-ads campaign create` | Cria campanha |
| `/meta-ads analyze last7d` | Analisa performance |
| `/meta-ads scale {id}` | Escala campanha |
| `/meta-ads diagnose` | Diagnósticos |

---

## 📁 Estrutura de Diretórios

```
/campanhas/{cliente}/{YYYY-MM}/{campanha}/
├── briefing.md          # Briefing (obrigatório)
├── analise.md           # Gerado pelo traffic-strategist
├── checklist.md         # Gerado pelo traffic-strategist
├── copy_variants.md    # Gerado pelo ad-copywriter
├── targeting.json      # Gerado pelo ad-copywriter
├── brand_voice.json    # Voz da marca
└── ad_*.{jpg,mp4}      # Criativos
```

**Convenção de nomes:**
```
ad_{número}_{posicionamento}_{tipo}.{ext}
ad_01_feed_image.jpg
ad_02_story_video.mp4
ad_03_reels_video.mp4
```

---

## ⚡ Quick Start

```bash
# 1. Clone e configure
git clone -b beta https://github.com/monrars1995/neuro-skills.git
cp -r neuro-skills/* ~/.claude/skills/

# 2. Configure sua conta Meta
> /meta-ads setup

# 3. Crie sua primeira campanha
mkdir -p /campanhas/nike/2024-03/black_friday/
# Adicione briefing.md e criativos

# 4. Execute o fluxo
> Analise /campanhas/nike/2024-03/black_friday/
> Prepare a campanha para Nike
> Crie copy para Nike Black Friday
> Crie campanha a partir de /campanhas/nike/2024-03/black_friday/
```

---

## 📊 Benchmarks por Vertical

| Vertical | CPA Bom | CPA Atenção | ROAS Bom | ROAS Atenção | CTR Bom |
|----------|---------|-------------|----------|--------------|---------|
| Concessionárias | < R$150 | > R$300 | > 2.5x | < 1.5x | > 1.5% |
| Imobiliárias | < R$80 | > R$200 | > 3.0x | < 1.5x | > 1.2% |
| E-commerce | < R$25 | > R$50 | > 4.0x | < 2.0x | > 2.0% |
| Educação | < R$50 | > R$150 | > 3.5x | < 1.8x | > 1.5% |
| Saúde | < R$40 | > R$100 | > 3.0x | < 1.5x | > 1.8% |

---

## 🤖 Automação por Vertical

### Concessionárias
- ✅ Conversão offline (CRM → Meta)
- ✅ Janela de atribuição: 7-90 dias
- ✅ Test drive como conversão intermediária
- ✅ Follow-up leads não convertidos

### Imobiliárias
- ✅ Product Catalog sync
- ✅ Tour virtual tracking
- ✅ LTV analysis mensal

### E-commerce
- ✅ Cart abandonment automation
- ✅ DPA optimization
- ✅ Scale fast movers

### Educação
- ✅ Seasonal campaigns (vestibular, volta às aulas)
- ✅ Lead scoring + CRM
- ✅ ROAS por aluno

### Saúde
- ✅ LGPD compliance check
- ✅ Privacy-safe targeting
- ✅ Appointment optimization

---

## 📞 Contato

**Monrars** - Criador e Mantenedor

| | |
|---|---|
| **Site** | [goldneuron.io](https://goldneuron.io/) |
| **Newsletter** | [Drops](https://goldneuron.io/drops) |
| **Instagram** | [@monrars](https://instagram.com/@monrars) |
| **GitHub** | [@monrars1995](https://github.com/monrars1995) |

---

## 📜 Licença

MIT License with Attribution

Ao usar este projeto, você concorda em:
- ✅ Manter atribuição ao autor original
- ✅ Incluir link para o repositório original
- ❌ Não rebrandear ou revender como produto standalone

Uso comercial permitido sob os termos da licença.  
Para licenças empresariais ou suporte, [entre em contato](https://goldneuron.io/).

---

## 📈 Versões

| Versão | Branch | Descrição |
|--------|--------|-----------|
| `v1.0.0` | `main` | Versão estável inicial |
| `v2.0.0-beta` | `beta` | Sistema de memória + agentes verticais |
| `v2.2.0-beta` | `beta` | 5 agentes vertical especializados |

```bash
# Use a versão beta
git clone -b beta https://github.com/monrars1995/neuro-skills.git
```

---

## 🙏 Agradecimentos

Construído com ❤️ para a comunidade de tráfego pago brasileira.

Especialmente para quem:
- Gasta horas em briefings que nunca vêm completo
- Perde noites em atribuição quebrada
- Decide no escuro porque dados não batem
- Precisa escalar mas não sabe como

**Este projeto é para você.**

---

<div align="center">

**[Newsletter Drops](https://goldneuron.io/drops)** | **[Documentação](https://goldneuron.io/)** | **[Instagram](https://instagram.com/@monrars)**

**Feito por [@monrars](https://instagram.com/@monrars)**

</div>