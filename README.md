# Neuro Skills

> Framework de automação de Meta Ads para Claude Code, OpenAI Codex e Gemini CLI

**Site Oficial:** [goldneuron.io](https://goldneuron.io/)  
**Comunidade:** [Drops](https://goldneuron.io/drops) - O bastidor técnico que o mercado não mostra  
**Instagram:** [@monrars](https://instagram.com/monrars)

---

## 🚀 Sobre

Skills de automação de Meta Ads para criar, gerenciar e otimizar campanhas de tráfego pago com IA. Construído para donos de operação, heads e gestores que vivem o jogo real: processo, rastreabilidade, automação, decisão e execução.

### Comunidade Drops

Uma comunidade construída para profissionais que querem:
- **Processo** - Workflows e automações testados em operações reais
- **Rastreabilidade** - Atribuição completa do funil
- **Automação** - Cron jobs, sincronização offline, otimização automática
- **Decisão** - Dados para tomar decisões baseadas em ROI/ROAS
- **Execução** - Implementação rápida com skills prontos

Newsletter semanal com estudos de caso, implementações e treinamentos.

Gratuito e aberto em [goldneuron.io/drops](https://goldneuron.io/drops).

---

## 📁 Agentes por Vertical

### 🚗 Concessionárias
- Ciclo de venda longo (7-90 dias)
- Conversão offline obrigatória
- Janela de atribuição: 90 dias
- Integração CRM específica
- [Ver SKILL.md](agents/concessionarias/SKILL.md) | [Ver TOOLS.md](agents/concessionarias/TOOLS.md)

### 🏠 Imobiliárias
- Ticket médio alto (R$300k-2M)
- Inventário único por localização
- LTV + comissão (3-6%)
- Tours virtuais
- [Ver SKILL.md](agents/imobiliarias/SKILL.md)

### 🛒 E-commerce
- Ciclo curto (1-7 dias)
- DPA (Dynamic Product Ads)
- Catálogo de produtos
- Eventos em tempo real
- [Ver SKILL.md](agents/ecommerce/SKILL.md)

### 🎓 Educação
- Sazonalidade forte (vestibular, volta às aulas)
- LTV alto (48 meses × mensalidade)
- Modelo de assinatura
- Matrícula offline
- [Ver SKILL.md](agents/educacao/SKILL.md)

### 🏥 Saúde
- Compliance LGPD/HIPAA
- Targeting privacy-safe
- LTV + indicação (boca a boca)
- Auditoria mensal
- [Ver SKILL.md](agents/saude/SKILL.md)

---

## 🎯 Skills Principais

### 🧠 neuro-ads-manager
Gerenciador completo de Meta Ads com CRUD, Analytics, Automação e integração API v21.0. Plataforma unificada para gerenciar campanhas de ponta a ponta.

**Funcionalidades:**
- **CRUD Completo**: Criar, listar, editar e deletar campanhas, ad sets, ads e creatives
- **Analytics/Relatórios**: Métricas detalhadas, dashboards, análise de performance
- **Automação/Otimização**: Regras automáticas, escala, pausa por performance
- **Integração API**: Cliente completo para Meta Graph API v21.0
- Sistema de memória com armazenamento persistente
- Rate limiting e tratamento de erros
- Cache para insights

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
traffic-strategist → ad-copywriter → [neuro-ads-manager / meta-ads-manager]
     (prep)              (copy)              (executa)
```

1. **traffic-strategist**: Analisa pasta da campanha, valida assets, identifica lacunas
2. **ad-copywriter**: Gera variações de copy baseado no briefing e voz da marca
3. **neuro-ads-manager/meta-ads-manager**: Cria campanhas, lança anúncios, gerencia orçamentos

---

## Comandos Completos

### 📋 Traffic Strategist

| Comando | Descrição |
|---------|-----------|
| `analise {cliente}` | Analisa pasta do cliente |
| `analise {cliente} {campanha}` | Analisa campanha específica |
| `prepara {cliente}` | Prepara tudo para criação de campanha |
| `check {cliente}` | Executa validação de checklist |
| `organiza {cliente}` | Organiza e renomeia arquivos |
| `gera docs {cliente}` | Gera toda documentação |

**Exemplos:**
```
> Analise o briefing em /campanhas/nike/2024-03/spring-sale/
> Prepare a campanha para o cliente Nike
> Verifique os criativos em /campanhas/nike/2024-03/black_friday/
> Gere documentação para o cliente fitness_app
```

### ✍️ Ad Copywriter

| Comando | Descrição |
|---------|-----------|
| `analisa voz {cliente}` | Analisa voz da marca a partir do briefing |
| `cria copy {cliente}` | Gera copy de anúncio com voz da marca |
| `variantes {cliente}` | Cria variações para teste A/B |
| `ajusta tom {cliente}` | Ajusta tom baseado em feedback |
| `exporta copy {cliente}` | Exporta copy para markdown |

**Exemplos:**
```
> Analise a voz da marca Nike
> Crie copy para a campanha Nike Spring Sale
> Gere variações para teste A/B
> Ajuste o tom para mais casual
```

### 🎯 Meta Ads Manager

#### Gerenciamento de Contas

| Comando | Descrição |
|---------|-----------|
| `/meta-ads setup` | Inicializa skill, salva credenciais da conta |
| `/meta-ads accounts list` | Lista todas as contas salvas |
| `/meta-ads accounts add {nome}` | Adiciona nova conta |
| `/meta-ads accounts use {nome}` | Define conta ativa |
| `/meta-ads accounts remove {nome}` | Remove conta |
| `/meta-ads accounts export` | Exporta configurações para backup |
| `/meta-ads accounts import` | Importa configurações de backup |

#### Gerenciamento de Campanhas

| Comando | Descrição |
|---------|-----------|
| `/meta-ads campaign create` | Cria nova campanha lendo pasta |
| `/meta-ads analyze {período}` | Analisa desempenho |
| `/meta-ads diagnose` | Executa diagnósticos nas campanhas ativas |
| `/meta-ads scale {id}` | Escala campanha com segurança |
| `/meta-ads pause {id}` | Pausa campanha |
| `/meta-ads resume {id}` | Retoma campanha |
| `/meta-ads status` | Mostra status atual |

#### Comandos de Pastas

| Comando | Descrição |
|---------|-----------|
| `/meta-ads clients` | Lista todos os clientes |
| `/meta-ads campaigns {cliente}` | Lista campanhas do cliente |
| `/meta-ads folder create {cliente} {nome}` | Cria pasta de campanha |
| `/meta-ads briefing {cliente} {campanha}` | Lê briefing |

#### Períodos de Análise

| Período | Descrição |
|---------|-----------|
| `today` | Dados de hoje |
| `yesterday` | Dados de ontem |
| `last7d` | Últimos 7 dias |
| `last14d` | Últimos 14 dias |
| `last30d` | Últimos 30 dias |
| `last90d` | Últimos 90 dias |
| `this_month` | Mês atual |
| `last_month` | Mês anterior |

**Exemplos:**
```
> /meta-ads setup
> Liste minhas contas de anúncios salvas
> Crie campanha a partir de /campanhas/nike/2024-03/spring-sale/
> Analise a performance da campanha última semana
> Escale a campanha com CPA abaixo de $15
> Diagnóstico das campanhas ativas
```

---

## Instalação

### Claude Code (Anthropic)

```bash
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

## Estrutura de Diretórios

```
/campanhas/{cliente}/{YYYY-MM}/{campanha}/
├── briefing.md          # Briefing da campanha (obrigatório)
├── analise.md           # Gerado pelo traffic-strategist
├── checklist.md        # Gerado pelo traffic-strategist
├── copy_variants.md    # Gerado pelo ad-copywriter
├── targeting.json      # Gerado pelo ad-copywriter
├── brand_voice.json    # Gerado pelo ad-copywriter
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
ad_03_carousel_01.jpg     # Criativo 3, Card 1 do Carrossel
```

---

## Sistema de Memória

```
~/.meta-ads-manager/
├── accounts.json       # Contas de anúncios salvas
├── session.json        # Dados da sessão atual
├── cache/              # Cache de insights
└── logs/               # Histórico de ações
```

---

## Requisitos

- Conta Meta Business
- Facebook App com Graph API v21.0
- Token de acesso válido com permissão `ads_management`
- Pixel do Facebook configurado (recomendado)
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

Você precisará de:
- Access Token: https://developers.facebook.com/tools/explorer/
  - Permissões: ads_management, ads_read, pages_read_engagement
- Ad Account ID: https://business.facebook.com/settings/ad-accounts
  - Formato: act_123456789 ou 123456789
- Pixel ID (opcional): https://business.facebook.com/settings/pixels
- Page ID (opcional): https://business.facebook.com/settings/pages
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

## Workflow Recomendado

### 1. Preparação (traffic-strategist)

```
> Analise /campanhas/nike/2024-03/black_friday/
> Prepare a campanha para Nike
> Gere documentação para Nike
```

Isso cria:
- `analise.md` - Análise completa
- `checklist.md` - Checklist de validação
- Organiza os arquivos de criativos

### 2. Copy (ad-copywriter)

```
> Analise a voz da marca Nike
> Crie copy para Nike Black Friday
> Gere variações para teste A/B
```

Isso cria:
- `brand_voice.json` - Voz da marca
- `copy_variants.md` - Variações de copy
- `targeting.json` - Configurações de targeting

### 3. Execução (meta-ads-manager)

```
> /meta-ads setup
> /meta-ads campaign create
> Campanha criada a partir de /campanhas/nike/2024-03/black_friday/
```

---

## 📞 Contato

**Monrars** - Criador e Mantenedor

- 🌐 **Site:** [goldneuron.io](https://goldneuron.io/)
- 📸 **Instagram:** [@monrars](https://instagram.com/monrars)
- 💻 **GitHub:** [@monrars1995](https://github.com/monrars1995)
- 🚀 **Comunidade:** [Drops](https://goldneuron.io/drops)

---

## 📜 Licença

MIT License with Attribution - Veja o arquivo [LICENSE](LICENSE) para detalhes.

Ao usar este projeto, você concorda em:
- Manter atribuição ao autor original (Monrars)
- Incluir link para o repositório original
- Não rebrandear ou revender como produto standalone

Uso comercial é permitido sob os termos da licença.

Para licenças empresariais ou suporte, entre em contato.

---

## 📊 Versões

| Versão | Branch | Status | Descrição |
|--------|--------|--------|-----------|
| `v1.0.0` | `main` | Produção | Versão estável inicial |
| `v2.0.0-beta` | `beta` | Beta | Sistema de memória + agentes verticais |
| `v2.2.0-beta` | `beta` | Atual | 5 agentes verticais especializados |

Para usar a versão beta:
```bash
git clone -b beta https://github.com/monrars1995/neuro-skills.git
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie sua branch (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Add: NovaFeature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

---

## 🙏 Agradecimentos

Construído com ❤️ para a comunidade de tráfego pago brasileira.

---

<div align="center">

**[⬆ Voltar ao Topo](#neuro-skills)**

**Feito por [@monrars](https://instagram.com/monrars) | [goldneuron.io](https://goldneuron.io/)**

</div>