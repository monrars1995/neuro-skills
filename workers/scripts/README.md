# Cloudflare Workers - Scripts Server

Este diretório contém o worker doCloudflare para servir os scripts de instalação em `scripts.goldneuron.io`.

## 🚀 Deploy

### 1. Pré-requisitos

- Conta noCloudflare
- Wrangler CLI instalado (`npm install -g wrangler`)
- KV Namespace criado

### 2. Configuração Inicial

```bash
# Login no Cloudflare
wrangler login

# Criar KV Namespace
wrangler kv:namespace create SCRIPTS_KV

# Anote o ID do KV namespace e atualize wrangler.toml
```

### 3. Configurar Secrets noGitHub

Vá para Settings > Secrets and variables > Actions noGitHub e adicione:

- `CLOUDFLARE_API_TOKEN` - Token de API do Cloudflare
- `CLOUDFLARE_ACCOUNT_ID` - ID da conta do Cloudflare

### 4. Deploy

```bash
# Deploy manual
cd workers/scripts
wrangler deploy

# Ouvia GitHub Actions (automático)
git push origin beta
```

## 📁 Estrutura

```
workers/scripts/
├── index.js          # Worker principal
├── wrangler.toml     # Configuração doWrangler
└── public/           # Arquivos estáticos
```

## 🔗 URLs

Após o deploy, os scripts estarão disponíveis em:

- https://scripts.goldneuron.io/
- https://scripts.goldneuron.io/install.sh
- https://scripts.goldneuron.io/install-claude-code.sh
- https://scripts.goldneuron.io/install-opencode.sh
- https://scripts.goldneuron.io/install-cursor.sh
- https://scripts.goldneuron.io/install-gemini.sh
- https://scripts.goldneuron.io/install-codex.sh
- https://scripts.goldneuron.io/install-antigravity.sh

## 📊 API Endpoints

- `GET /` - Página HTML com links de instalação
- `GET /api/npm` - Informações do pacote npm (JSON)
- `GET /install.sh` - Script universal de instalação
- `GET /install-{plataforma}.sh` - Scripts específicos por plataforma

## 🔄 Cache

Os scripts são cacheados no KV por 1 hora. Para limpar o cache:

```bash
wrangler kv:key delete --binding SCRIPTS_KV "script:install.sh"
```

## 🛡️ Segurança

- CORS habilitado para todas as origens
- Scripts servidosvia HTTPS
- Cache no edge doCloudflare
- Fallback para npm se GitHub indisponível