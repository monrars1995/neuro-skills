# Neuro Skills

Skills de automação de Meta Ads para Claude Code, OpenAI Codex e Gemini CLI.

## Skills

### 🎯 meta-ads-manager
Gerenciador completo de tráfego Meta Ads com integração Graph API v21.0. Gerencia contas, cria campanhas, testes A/B, escala, diagnósticos e relatórios.

**Funcionalidades:**
- Sistema de memória com armazenamento persistente de contas
- Criação de campanhas a partir de briefing e criativos
- Framework de testes A/B
- Playbook de escala (horizontal/vertical)
- Diagnósticos de performance
- Benchmarks do mercado
- Regras de automação
- Modelos de relatórios

### 📋 traffic-strategist
Agente de preparação de campanhas que analisa pastas, valida briefings, verifica criativos, identifica lacunas e organiza arquivos antes da criação da campanha.

**Funcionalidades:**
- Análise de pastas
- Validação de briefing
- Verificação de criativos
- Identificação de lacunas
- Geração de perguntas para assets faltando
- Organização de arquivos
- Geração de documentação (`analise.md`, `checklist.md`)

### ✍️ ad-copywriter
Especialista em copy de anúncios que analisa a voz da marca, mantém consistência de tom, cria copy on-brand para formatos Feed/Stories/Reels/Carousel e gera variações para testes A/B.

**Funcionalidades:**
- Análise de voz da marca
- Consistência de tom
- Copy para todos os formatos Meta
- Variações para testes A/B
- Otimização específica por plataforma

## Fluxo de Trabalho

```
traffic-strategist → ad-copywriter → meta-ads-manager(prep)            (copy)          (executa)
```

1. **traffic-strategist**: Analisa pasta da campanha, valida assets, identifica lacunas
2. **ad-copywriter**: Gera variações de copy baseado no briefing e voz da marca
3. **meta-ads-manager**: Cria campanhas, lança anúncios, gerencia orçamentos

---

## Instalação

### Claude Code (Anthropic)```bash
# Clone o repositório
git clone https://github.com/monrars1995/neuro-skills.git

# Copie os skills para o diretório do Claude Code
cp -r neuro-skills/meta-ads-manager ~/.claude/skills/
cp -r neuro-skills/traffic-strategist ~/.claude/skills/
cp -r neuro-skills/ad-copywriter ~/.claude/skills/
```

### OpenAI Codex

```bash
# Clone o repositório
git clone https://github.com/monrars1995/neuro-skills.git

# Copie os skills para o diretório do Codex
cp -r neuro-skills/meta-ads-manager ~/.codex/skills/
cp -r neuro-skills/traffic-strategist ~/.codex/skills/
cp -r neuro-skills/ad-copywriter ~/.codex/skills/
```

### Gemini CLI (Google)

```bash
# Clone o repositório
git clone https://github.com/monrars1995/neuro-skills.git

# Copie os skills para o diretório do Gemini CLI
cp -r neuro-skills/meta-ads-manager ~/.gemini/skills/
cp -r neuro-skills/traffic-strategist ~/.gemini/skills/
cp -r neuro-skills/ad-copywriter ~/.gemini/skills/
```

### OpenCode

```bash
# Clone o repositório
git clone https://github.com/monrars1995/neuro-skills.git

# Copie os skills para o diretório do OpenCode
cp -r neuro-skills/meta-ads-manager ~/.opencode/skills/
cp -r neuro-skills/traffic-strategist ~/.opencode/skills/
cp -r neuro-skills/ad-copywriter ~/.opencode/skills/
```

---

## Uso

### Traffic Strategist

```
> Analise o briefing em /campanhas/nike/2024-03/spring-sale/> Prepare a campanha para o cliente Nike
> Verifique os criativos em /campanhas/nike/2024-03/black_friday/
```

### Ad Copywriter

```
> Crie variações de copy para a campanha Nike Spring Sale
> Analise a voz da marca Nike
> Gere copies para Feed, Stories e Reels
```

### Meta Ads Manager

```
> /meta-ads setup
> Liste minhas contas de anúncios salvas
> Crie campanha a partir de /campanhas/nike/2024-03/spring-sale/
> Analise a performance da campanha última semana
> Escale a campanha com CPA abaixo de $15
```

---

## Estrutura de Diretórios

```
/campanhas/{cliente}/{YYYY-MM}/{campanha}/
├── briefing.md          # Briefing da campanha (obrigatório)├── analise.md           # Gerado pelo traffic-strategist
├── checklist.md         # Gerado pelo traffic-strategist├── copy_variants.md    # Gerado pelo ad-copywriter
├── targeting.json       # Gerado pelo ad-copywriter├── brand_voice.json    # Gerado pelo ad-copywriter
└── ad_*.*              # Assets de criativos
```

### Convenção de Nomes para Criativos

```
Formato: ad_{número}_{posicionamento}_{tipo}.{extensão}

Exemplos:
ad_01_feed_image.jpg      # Criativo 1, Feed, Imagem
ad_01_feed_video.mp4      # Criativo 1, Feed, Vídeo
ad_02_story_video.mp4     # Criativo 2, Stories, Vídeo
ad_02_reels_video.mp4     # Criativo 2, Reels, Vídeo
ad_03_carousel_01.jpg     # Criativo 3, Carousel, Card 1
```

---

## Sistema de Memória

```
~/.meta-ads-manager/
├── accounts.json       # Contas de anúncios salvas
├── session.json        # Dados da sessão atual├── cache/              # Cache de insights└── logs/               # Histórico de ações
```

---

## Comandos Principais

### Traffic Strategist

| Comando | Descrição |
|---------|-----------|
| `analise {cliente}` | Analisa pasta do cliente |
| `analise {cliente} {campanha}` | Analisa campanha específica |
| `prepara {cliente}` | Prepara tudo para criação de campanha |
| `check {cliente}` | Executa validação checklist |
| `organiza {cliente}` | Organiza e renomeia arquivos |

### Ad Copywriter

| Comando | Descrição |
|---------|-----------|
| `analisa voz {cliente}` | Analisa voz da marca do briefing |`cria copy {cliente}` | Gera copy de anúncio com voz da marca |
| `variantes {cliente}` | Cria variações para testes A/B |
| `ajusta tom {cliente}` | Ajusta tom baseado em feedback |

### Meta Ads Manager

| Comando | Descrição |
|---------|-----------|`/meta-ads setup` | Inicializa e salva credenciais |
| `/meta-ads accounts list` | Lista contas salvas |
| `/meta-ads accounts use {nome}` | Define conta ativa |
| `/meta-ads campaign create` | Cria nova campanha |
| `/meta-ads analyze {período}` | Analisa performance |
| `/meta-ads diagnose` | Diagnóstica campanhas ativas |

---

## Requisitos

- Conta Meta Business
- Facebook App com Graph API v21.0
- Token de acesso válido com permissão `ads_management`- Pixel do Facebook configurado (recomendado)
- Página do Facebook conectada (recomendado)

---

## Primeiro Uso

### 1. Setup Inicial

```bash
# Crie os diretórios de memória
mkdir -p ~/.meta-ads-manager/cache/insights
mkdir -p ~/.meta-ads-manager/cache/campaigns
mkdir -p ~/.meta-ads-manager/logs

# Inicialize o arquivo de contas
echo '{"version":"1.0","accounts":{},"active_account":null}' > ~/.meta-ads-manager/accounts.json
```

### 2. Configure Sua Conta

```
Execute: /meta-ads setup

Você precisará de:- Access Token: https://developers.facebook.com/tools/explorer/
  - Permissões: ads_management, ads_read, pages_read_engagement- Ad Account ID: https://business.facebook.com/settings/ad-accounts
  - Formato: act_123456789 ou 123456789- Pixel ID (opcional): https://business.facebook.com/settings/pixels- Page ID (opcional): https://business.facebook.com/settings/pages
```

### 3. Crie Sua Primeira Campanha

```bash
# Crie a estrutura de pastas
mkdir -p /campanhas/nike/2024-03/black_friday/

# Adicione o briefing
cp briefing.md /campanhas/nike/2024-03/black_friday/

# Adicione os criativos
cp ad_01_feed_image.jpg /campanhas/nike/2024-03/black_friday/
cp ad_01_feed_video.mp4 /campanhas/nike/2024-03/black_friday/

# Execute o skill
> Crie uma campanha para Nike Black Friday
```

---

## Criado por

@monrars