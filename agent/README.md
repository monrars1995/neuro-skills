# Neuro Skills Agent

> Interface gráfica para automação de Meta Ads com sistema de memória compartilhada.

**Versão:** v2.0.0-beta  
**Autor:** Monrars ([@monrars](https://instagram.com/monrars))  
**Licença:** MIT

---

## 🎯 Funcionalidades

### Upload de Criativos
- ✅ Upload de vídeos com acompanhamento de progresso
- ✅ Upload de imagens
- ✅ Upload em lote (batch)
- ✅ Fila de uploads com processamento paralelo
- ✅ Aguardar finalização dos uploads

### Sistema de Memória Compartilhada
- ✅ Dados de clientes persistentes
- ✅ Voz da marca por cliente
- ✅ Histórico de campanhas
- ✅ Aprendizados do sistema
- ✅ Benchmarks do mercado

### Interface Gráfica
- ✅ Dashboard com métricas
- ✅ Gestão de clientes
- ✅ Upload com barra de progresso
- ✅ Configuração de contas Meta
- ✅ Tema claro/escuro

---

## 📦 Instalação

### Requisitos

- Python 3.9+
- Conta Meta Business
- Facebook App com Graph API v21.0

### Setup

```bash
# Clone o repositório (branch beta)
git clone -b beta https://github.com/monrars1995/neuro-skills.git
cd neuro-skills

# Instale as dependências
pip install -r agent/requirements.txt

# Execute o setup de memória
./scripts/setup-memory.sh

# Execute o agent
python agent/run.py
```

---

## 🚀 Uso

### Iniciar o Agent

```bash
cd neuro-skills
python agent/run.py
```

O agent abrirá automaticamente em `http://localhost:8501`

### Primeira Configuração

1. **Configurar Conta Meta**
   - Acesse "⚙️ Configurações" > "Contas Meta Ads"
   - Clique em "Adicionar Nova Conta"
   - Preencha os dados:
     - Nome da Conta: ex: "Nike Principal"
     - Ad Account ID: ex: `act_123456789`
     - Access Token: obtido em [Facebook Developers](https://developers.facebook.com/tools/explorer/)
   - Clique em "Adicionar Conta"

2. **Criar Cliente**
   - Acesse "👤 Clientes" > "Novo Cliente"
   - Preencha os dados do cliente
   - Clique em "Cadastrar Cliente"

3. **Upload de Criativos**
   - Acesse "⬆️ Upload"
   - Selecione arquivos ou pasta
   - Aguarde a conclusão do upload

---

## 📂 Estrutura

```
agent/
├── core/
│   ├── config.py          # Configurações
│   ├── memory.py          # Sistema de memória
│   └── meta_api.py        # Cliente Meta API
│
├── upload/
│   └── video_uploader.py  # Upload de vídeos
│
├── ui/
│   └── app.py            # Interface Streamlit
│
├── run.py                # Entry point
└── requirements.txt      # Dependências
```

---

## 🔧 Configuração

### Memória do Sistema

O sistema armazena dados em `~/.neuro-skills/`:

```
~/.neuro-skills/
├── clients/              # Dados de clientes
│   └── {client_id}/
│       ├── profile.json
│       ├── brand_voice.json
│       └── performance.json
│
├── shared/              # Dados compartilhados
│   ├── accounts.json
│   ├── learnings.json
│   └── benchmarks.json
│
└── sessions/            # Sessões por skill
```

### Meta API

**Permissões necessárias:**
- `ads_management`
- `ads_read`
- `pages_read_engagement`

**Obter token:**
1. Acesse [Facebook Developers](https://developers.facebook.com/tools/explorer/)
2. Selecione seu app
3. Adicione as permissões
4. Gere o token de acesso

---

## 📱 Upload de Vídeos

### Upload Individual

```python
from core.meta_api import MetaAPIClient
from pathlib import Path

# Inicializar cliente
client = MetaAPIClient(
    access_token="SEU_TOKEN",
    ad_account_id="act_123456789"
)

# Upload com progresso
def on_progress(proportion, uploaded, total):
    print(f"Progresso: {proportion*100:.1f}% ({uploaded}/{total} bytes)")

result = client.upload_video(
    video_path=Path("/caminho/para/video.mp4"),
    progress_callback=on_progress
)

if result["success"]:
    print(f"Video ID: {result['video_id']}")
else:
    print(f"Erro: {result['error']}")
```

### Upload em Lote

```python
from upload.video_uploader import BatchUploader

# Upload de pasta inteira
batch = BatchUploader(api_client, memory_manager)

results = batch.upload_creatives_from_folder(
    folder_path=Path("/campanhas/nike/2024-03/black_friday/"),
    campaign_name="Black Friday 2024",
    progress_callback=lambda p, u, t: print(f"Progresso: {p*100:.1f}%")
)

print(f"Vídeos: {len(results['videos'])}")
print(f"Imagens: {len(results['images'])}")
print(f"Erros: {len(results['errors'])}")
```

---

## 🎨 Interface

### Dashboard
- Visão geral do sistema
- Métricas principais
- Ações rápidas

### Clientes
- Cadastro de clientes
- Gestão de perfis
- Voz da marca

### Upload
- Upload individual e em lote
- Barra de progresso
- Aguardar finalização

### Configurações
- Contas Meta Ads
- Backup de dados
- Limpeza de cache

---

## 🔄 Integração com Skills

O agent integra automaticamente com os skills:

1. **traffic-strategist**: Usa dados de `clients/{id}/profile.json`
2. **ad-copywriter**: Usa `clients/{id}/brand_voice.json`
3. **meta-ads-manager**: Usa `shared/accounts.json`

---

## 📊 APIs

### MetaAPIClient

```python
# Testar conexão
result = client.test_connection()

# Upload de vídeo
result = client.upload_video(video_path, progress_callback)

# Upload de imagem
result = client.upload_image(image_path)

# Criar campanha
result = client.create_campaign(name, objective)

# Obter insights
result = client.get_campaign_insights(campaign_id)
```

### MemoryManager

```python
# Cliente
memory.create_client(client_id, data)
memory.get_client(client_id)
memory.set_active_client(client_id)

# Conta Meta
memory.save_account(account_name, account_data)
memory.set_active_account(account_name)

# Voz da marca
memory.get_brand_voice(client_id)
memory.save_brand_voice(client_id, voice_data)
```

---

## 🔒 Segurança

- Tokens de acesso armazenados localmente
- Memória em arquivos JSON não criptografados
- **Recomendação**: Use variáveis de ambiente para tokens em produção

---

## 🛠️ Desenvolvimento

### Adicionar nova funcionalidade

1. Crie módulo em `core/` ou `upload/`
2. Adicione interface em `ui/app.py`
3. Integre com memória em `core/memory.py`

### Executar testes

```bash
pytest agent/tests/
```

---

## 📝 Changelog

### v2.0.0-beta (2026-03-29)
- ✨ Sistema de memória compartilhada
- ✨ Interface gráfica com Streamlit
- ✨ Upload de vídeos com progresso
- ✨ Upload em lote
- ✨ Gestão de clientes
- ✨ Configuração de contas Meta

### v1.0.0 (2026-03-29)
- ✨ Skills iniciais (meta-ads-manager, traffic-strategist, ad-copywriter)
- ✨ Documentação em PT-BR
- ✨ Instalação multi-plataforma

---

## 📞 Suporte

- **Instagram:** [@monrars](https://instagram.com/monrars)
- **GitHub:** [monrars1995/neuro-skills](https://github.com/monrars1995/neuro-skills)
- **Issues:** [GitHub Issues](https://github.com/monrars1995/neuro-skills/issues)

---

## 📄 Licença

MIT License - Copyright (c) 2026 Monrars

Veja o arquivo [LICENSE](../LICENSE) para detalhes.