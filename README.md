# Neuro Skills

Skills de automação de Meta Ads para OpenCode/Claude Code.

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
traffic-strategist → ad-copywriter → meta-ads-manager
     (prep)            (copy)          (executa)
```

1. **traffic-strategist**: Analisa pasta da campanha, valida assets, identifica lacunas
2. **ad-copywriter**: Gera variações de copy baseado no briefing e voz da marca
3. **meta-ads-manager**: Cria campanhas, lança anúncios, gerencia orçamentos

## Instalação

Copie os skills para o diretório de skills do OpenCode:

```bash
cp -r meta-ads-manager ~/.opencode/skills/
cp -r traffic-strategist ~/.opencode/skills/
cp -r ad-copywriter ~/.opencode/skills/
```

## Uso

```
# Traffic Strategist
> Analise o briefing em /campanhas/nike/2024-03/spring-sale/

# Ad Copywriter
> Crie variações de copy para a campanha Nike Spring Sale

# Meta Ads Manager
> Liste minhas contas de anúncios salvas
> Crie campanha a partir de /campanhas/nike/2024-03/spring-sale/
```

## Estrutura de Diretórios

```
/campanhas/{cliente}/{YYYY-MM}/{campanha}/
├── briefing.md
├── analise.md          # Gerado pelo traffic-strategist
├── checklist.md        # Gerado pelo traffic-strategist
├── copy_variants.md    # Gerado pelo ad-copywriter
├── targeting.json     # Gerado pelo ad-copywriter
├── brand_voice.json    # Gerado pelo ad-copywriter
└── ad_*.*              # Assets de criativos
```

## Sistema de Memória

```
~/.meta-ads-manager/
├── accounts.json       # Contas de anúncios salvas
├── session.json        # Dados da sessão atual
├── cache/              # Cache de insights
└── logs/               # Histórico de ações
```

## Requisitos

- Conta Meta Business
- Facebook App com Graph API v21.0
- Token de acesso válido com permissão ads_management

## Criado por

@monrars