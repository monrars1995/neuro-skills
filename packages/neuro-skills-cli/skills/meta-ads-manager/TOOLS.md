# Meta Ads Manager - Ferramentas e Comandos

## Referência Rápida

### Localizações dos Arquivos

| O Que | Onde |
|-------|------|
| Contas Salvas | `~/.meta-ads-manager/accounts.json` |
| Dados de Sessão | `~/.meta-ads-manager/session.json` |
| Pastas de Campanhas | `/campanhas/{cliente}/{mes}/{campanha}/` |
| Arquivo de Briefing | `/campanhas/{cliente}/{mes}/{campanha}/briefing.md` |
| Criativos | `/campanhas/{cliente}/{mes}/{campanha}/ad_XX_XX.XXX` |
| Resultados | `/campanhas/{cliente}/{mes}/{campanha}/resultados.md` |

---

## Configuração Inicial

### 1. Inicializar Armazenamento em Memória

```bash
# Criar diretórios de memória
mkdir -p ~/.meta-ads-manager/cache/insights
mkdir -p ~/.meta-ads-manager/cache/campaigns
mkdir -p ~/.meta-ads-manager/logs

# Inicializar arquivo de contas
echo '{"version":"1.0","accounts":{},"active_account":null}' > ~/.meta-ads-manager/accounts.json

# Inicializar arquivo de sessão
echo '{"current_account":null,"current_campaign":null,"temp_data":{}}' > ~/.meta-ads-manager/session.json
```

### 2. Configurar Sua Conta

```
Executar: /meta-ads setup
```

Você precisará de:
- Access Token (de https://developers.facebook.com/tools/explorer/)
- Ad Account ID (de https://business.facebook.com/settings/ad-accounts)
- Pixel ID (opcional)
- Page ID (opcional)

---

## Configuração de Pastas de Campanha

### Criar Estrutura de Pastas

```bash
# Sintaxe
mkdir -p /campanhas/{cliente}/{YYYY-MM}/{campanha}/

# Exemplos
mkdir -p /campanhas/nike/2024-03/black_friday/
mkdir -p /campanhas/fitness_app/2024-03/launch/
mkdir -p /campanhas/local_bakery/2024-03/easter_promo/
```

### Estrutura de Pastas

```
/campanhas/
├── {cliente}/                      # Nome do cliente (minúsculas, underscores)
│   └── {YYYY-MM}/                  # Ano-Mês
│       └── {campanha}/             # Nome da campanha (minúsculas, underscores)
│           ├── briefing.md         # OBRIGATÓRIO: Briefing da campanha
│           ├── analise.md          # OPCIONAL: Anotações do gerente
│           ├── ad_01_feed_image.jpg # Criativo 1 - Imagem para Feed
│           ├── ad_01_feed_video.mp4 # Criativo 1 - Vídeo para Feed
│           ├── ad_02_story_video.mp4 # Criativo 2 - Stories
│           ├── ad_03_carousel_01.jpg # Criativo 3 - Card 1 do Carrossel
│           ├── ad_03_carousel_02.jpg # Criativo 3 - Card 2 do Carrossel
│           └── resultados.md        # CRIADO: Resultados após o lançamento
```

### Convenção de Nomenclatura de Criativos

```
Formato: ad_{número}_{posicionamento}_{tipo}.{extensão}

Exemplos:
ad_01_feed_image.jpg      # Criativo 1, Feed, Imagem
ad_01_feed_video.mp4      # Criativo 1, Feed, Vídeo
ad_02_story_video.mp4     # Criativo 2, Stories, Vídeo
ad_02_reels_video.mp4     # Criativo 2, Reels, Vídeo
ad_03_carousel_01.jpg     # Criativo 3, Card 1 do Carrossel
ad_03_carousel_02.jpg     # Criativo 3, Card 2 do Carrossel
```

**Posicionamentos:**
- `feed` - Feed do Facebook/Instagram
- `story` - Stories do Instagram/Facebook
- `reels` - Reels do Instagram/Facebook
- `carousel` - Carrossel (múltiplas imagens)

**Tipos:**
- `image` - Imagem estática (.jpg, .png)
- `video` - Arquivo de vídeo (.mp4, .mov)

---

## Modelo de Briefing

### Criar briefing.md

```bash
# Criar arquivo de briefing
nano /campanhas/nike/2024-03/black_friday/briefing.md

# Ou usar qualquer editor de texto
code /campanhas/nike/2024-03/black_friday/briefing.md
```

### Conteúdo do Modelo

```markdown
# Briefing da Campanha: {Nome_da_Campanha}

## Informações do Cliente
- **Cliente:** {Nome_do_Cliente}
- **Produto/Serviço:** {O que você está promovendo}
- **Indústria:** {Indústria}
- **Voz da Marca:** {Tom}

## Objetivos da Campanha
- **Objetivo Principal:** [Vendas/Leads/Tráfego/Reconhecimento/Instalações de App]
- **CPA Meta:** $XX.XX
- **ROAS Meta:** X.Xx
- **Orçamento:** $X,XXX/mês

## Público-Alvo
- **Faixa Etária:** XX a XX
- **Gênero:** [Todos/Masculino/Feminino]
- **Localização:** [Países, Cidades]
- **Interesses:** [Interesse 1, Interesse 2, ...]
- **Comportamentos:** [Comportamento 1, Comportamento 2, ...]

## Propostas de Valor Únicas
1. {PVU 1}
2. {PVU 2}
3. {PVU 3}

## Mensagens-Chave
- **Primária:** {Mensagem principal}
- **Secundária:** {Pontos de apoio}

## Direção Criativa
- **Estilo Visual:** {Moderno/Clássico/Minimalista}
- **Cores:** {Cores da marca}
- **Imagens:** {Tipos de imagens}

## Página de Destino
- **URL:** {URL da página de destino}
- **CTA:** {Chamada para ação}

## Cronograma
- **Início:** {YYYY-MM-DD}
- **Término:** {YYYY-MM-DD}
```

---

## Comandos

### Gerenciamento de Contas

| Comando | Descrição |
|---------|-----------|
| `/meta-ads setup` | Inicializar skill, salvar credenciais da conta |
| `/meta-ads accounts list` | Listar todas as contas salvas |
| `/meta-ads accounts add {nome}` | Adicionar nova conta |
| `/meta-ads accounts use {nome}` | Definir conta ativa |
| `/meta-ads accounts remove {nome}` | Remover conta |
| `/meta-ads accounts export` | Exportar configurações para backup |
| `/meta-ads accounts import` | Importar configurações de backup |

### Gerenciamento de Campanhas

| Comando | Descrição |
|---------|-----------|
| `/meta-ads campaign create` | Criar nova campanha lendo pasta |
| `/meta-ads analyze {período}` | Analisar desempenho |
| `/meta-ads diagnose` | Executar diagnósticos nas campanhas ativas |
| `/meta-ads scale {id}` | Escalar campanha com segurança |
| `/meta-ads pause {id}` | Pausar campanha |
| `/meta-ads resume {id}` | Retomar campanha |
| `/meta-ads status` | Mostrar status atual |

### Comandos de Pastas

| Comando | Descrição |
|---------|-----------|
| `/meta-ads clients` | Listar todos os clientes |
| `/meta-ads campaigns {cliente}` | Listar campanhas do cliente |
| `/meta-ads folder create {cliente} {nome}` | Criar pasta de campanha |
| `/meta-ads briefing {cliente} {campanha}` | Ler briefing |

### Períodos de Análise

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

---

## Exemplo de Fluxo de Trabalho

### Passo 1: Configuração (Primeira Vez)

```bash
# Inicializar armazenamento
mkdir -p ~/.meta-ads-manager/cache/insights
mkdir -p ~/.meta-ads-manager/cache/campaigns
echo '{"version":"1.0","accounts":{}}' > ~/.meta-ads-manager/accounts.json
```

### Passo 2: Criar Pasta de Campanha

```bash
mkdir -p /campanhas/nike/2024-03/black_friday/
```

### Passo 3: Adicionar Briefing

```bash
# Criar e editar briefing.md
nano /campanhas/nike/2024-03/black_friday/briefing.md

# Colar modelo de briefing e preencher detalhes
```

### Passo 4: Adicionar Criativos

```bash
# Copiar seus criativos
cp ~/Downloads/nike_ad1.jpg /campanhas/nike/2024-03/black_friday/ad_01_feed_image.jpg
cp ~/Downloads/nike_video.mp4 /campanhas/nike/2024-03/black_friday/ad_01_feed_video.mp4
cp ~/Downloads/nike_story.mp4 /campanhas/nike/2024-03/black_friday/ad_02_story_video.mp4
```

### Passo 5: Executar Skill

```
Usuário: "crie uma campanha para o Nike Black Friday"

A Skill irá:
1. Verificar contas salvas
2. Encontrar /campanhas/nike/2024-03/black_friday/
3. Ler briefing.md
4. Listar criativos (ad_01_*, ad_02_*)
5. Analisar criativos + briefing
6. Gerar copy do anúncio
7. Solicitar aprovação
8. Criar campanha no Meta
```

---

## Arquivos de Armazenamento

### accounts.json

```json
{
  "version": "1.0",
  "accounts": {
    "nike": {
      "name": "Nike Brasil",
      "ad_account_id": "act_123456789",
      "pixel_id": "987654321",
      "page_id": "111222333",
      "access_token": "ENCRYPTED_TOKEN",
      "currency": "BRL",
      "timezone": "America/Sao_Paulo",
      "created_at": "2024-03-29T15:00:00Z",
      "last_used": "2024-03-29T16:00:00Z",
      "is_active": true
    }
  },
  "active_account": "nike"
}
```

### session.json

```json
{
  "current_account": "nike",
  "current_campaign": null,
  "last_action": "campaign_create",
  "last_action_time": "2024-03-29T16:00:00Z",
  "temp_data": {
    "briefing_content": null,
    "creatives_analyzed": [],
    "generated_copy": null
  }
}
```

---

## Solução de Problemas

### Conta Não Encontrada

```bash
# Verificar se o arquivo de contas existe
ls -la ~/.meta-ads-manager/accounts.json

# Se estiver faltando, inicializar
echo '{"version":"1.0","accounts":{},"active_account":null}' > ~/.meta-ads-manager/accounts.json
```

### Pasta de Campanha Não Encontrada

```bash
# Listar clientes disponíveis
ls -la /campanhas/

# Listar campanhas do cliente
ls -la /campanhas/nike/

# Criar pasta faltando
mkdir -p /campanhas/nike/2024-03/black_friday/
```

### Briefing Não Encontrado

```bash
# Criar briefing.md
touch /campanhas/nike/2024-03/black_friday/briefing.md

# Editar com modelo
nano /campanhas/nike/2024-03/black_friday/briefing.md
```

### Nenhum Criativo Encontrado

```bash
# Listar criativos
ls -la /campanhas/nike/2024-03/black_friday/ad_*

# Adicionar criativos com nomenclatura correta
cp ~/Downloads/creative.jpg /campanhas/nike/2024-03/black_friday/ad_01_feed_image.jpg
```