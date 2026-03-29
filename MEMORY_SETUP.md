# Setup do Sistema de Memória (Beta)

> **Versão**: v2.0.0-beta  
> **Status**: Em desenvolvimento

Este documento explica como inicializar o novo sistema de memória compartilhada do Neuro Skills.

---

## Instalação Rápida

```bash
# Clone o branch beta
git clone -b beta https://github.com/monrars1995/neuro-skills.git

# Execute o setup
cd neuro-skills
./scripts/setup-memory.sh
```

---

## Setup Manual

### 1. Criar Estrutura de Diretórios

```bash
# Criar diretório principal
mkdir -p ~/.neuro-skills

# Estrutura de clientes
mkdir -p ~/.neuro-skills/clients

# Estrutura de campanhas
mkdir -p ~/.neuro-skills/campaigns

# Estrutura de sessões por skill
mkdir -p ~/.neuro-skills/sessions/meta-ads-manager/cache/insights
mkdir -p ~/.neuro-skills/sessions/meta-ads-manager/cache/campaigns
mkdir -p ~/.neuro-skills/sessions/meta-ads-manager/logs
mkdir -p ~/.neuro-skills/sessions/traffic-strategist/cache/analyses
mkdir -p ~/.neuro-skills/sessions/ad-copywriter/cache/copies

# Memória compartilhada
mkdir -p ~/.neuro-skills/shared/templates
```

### 2. Inicializar Arquivos Base

```bash
# Índice de clientes
cat > ~/.neuro-skills/clients/index.json << 'EOF'
{
  "version": "2.0",
  "updated_at": null,
  "clients": {},
  "active_client": null,
  "recent_clients": []
}
EOF

# Contas Meta
cat > ~/.neuro-skills/shared/accounts.json << 'EOF'
{
  "version": "2.0",
  "accounts": {},
  "active_account": null
}
EOF

# Aprendizados globais
cat > ~/.neuro-skills/shared/learnings.json << 'EOF'
{
  "version": "1.0",
  "updated_at": null,
  "industry_benchmarks": {},
  "platform_insights": {},
  "audience_patterns": {},
  "copy_patterns": {}
}
EOF

# Benchmarks do mercado
cat > ~/.neuro-skills/shared/benchmarks.json << 'EOF'
{
  "version": "1.0",
  "updated_at": null,
  "industries": {}
}
EOF
```

### 3. Criar Templates

```bash
# Template de briefing
cat > ~/.neuro-skills/shared/templates/briefing_template.md << 'EOF'
# Briefing: {nome_da_campanha}

## Informações do Cliente
- **Cliente:** {nome}
- **Produto/Serviço:** {produto}
- **Indústria:** {industria}
- **Voz da Marca:** {tom}

## Objetivos da Campanha
- **Objetivo Principal:** [Vendas/Leads/Tráfego/Awareness]
- **Objetivos Secundários:** [Brand reach, Email capture]
- **CPA Alvo:** R$ XX,XX
- **ROAS Alvo:** X.Xx
- **Orçamento:** R$ X.XXX/mês ou R$ XX/dia

## Público-Alvo
- **Idade:** XX a XX anos
- **Gênero:** [Todos/Masculino/Feminino]
- **Localização:** [Países, Cidades, Regiões]
- **Interesses:** [Lista de interesses]
- **Comportamentos:** [Comportamentos de compra, uso de dispositivo]
- **Dores:** [Problemas que o produto resolve]
- **Desejos:** [O que o público quer alcanzar]

## Proposta de Valor (USPs)
1. {USP 1}
2. {USP 2}
3. {USP 3}

## Criativos
- **Formatos:** [Imagem, Vídeo, Carrossel]
- **Posicionamentos:** [Feed, Stories, Reels]
- **CTA Principal:** [Shop Now, Learn More, etc.]

## Landing Page
- **URL:** {url}
- **Tipo:** [Product page, Landing page, etc.]

## Período da Campanha
- **Início:** {data_inicio}
- **Fim:** {data_fim}

## Observações
{observações_adicionais}
EOF

# Template de checklist
cat > ~/.neuro-skills/shared/templates/checklist_template.md << 'EOF'
# Checklist: {nome_da_campanha}

## Briefing
- [ ] Objetivo definido
- [ ] Público-alvo definido
- [ ] Orçamento definido
- [ ] Período definido

## Criativos
- [ ] Criativos criados
- [ ] Criativos validados
- [ ] Nomenclatura correta
- [ ] Formatos adequados

## Copy
- [ ] Copy para Feed
- [ ] Copy para Stories
- [ ] Copy para Reels
- [ ] Variações A/B

## Targeting
- [ ] Interesses definidos
- [ ] Localização definida
- [ ] Idade definida
- [ ] Gênero definido

## Técnico
- [ ] Pixel configurado
- [ ] Página conectada
- [ ] Conversions API (opcional)
- [ ] UTM configurado
EOF
```

---

## Migração do Sistema Antigo

Se você já usava o sistema antigo (`~/.meta-ads-manager/`), migre seus dados:

```bash
# Migrar contas existentes
cp ~/.meta-ads-manager/accounts.json ~/.neuro-skills/shared/accounts.json

# Migrar sessão atual
cp ~/.meta-ads-manager/session.json ~/.neuro-skills/sessions/meta-ads-manager/session.json

# Migrar logs
cp -r ~/.meta-ads-manager/logs/* ~/.neuro-skills/sessions/meta-ads-manager/logs/

# Migrar cache
cp -r ~/.meta-ads-manager/cache/insights/* ~/.neuro-skills/sessions/meta-ads-manager/cache/insights/
cp -r ~/.meta-ads-manager/cache/campaigns/* ~/.neuro-skills/sessions/meta-ads-manager/cache/campaigns/
```

---

## Verificação

Confirme que tudo está configurado:

```bash
# Verificar estrutura
ls -la ~/.neuro-skills/

# Deve mostrar:
# clients/
# campaigns/
# sessions/
# shared/

# Verificar arquivos
ls -la ~/.neuro-skills/shared/

# Deve mostrar:
# accounts.json
# benchmarks.json
# learnings.json
# templates/
```

---

## Uso

### Adicionar Cliente

```bash
# Criar diretório do cliente
mkdir -p ~/.neuro-skills/clients/{client_id}

# Criar profile
cat > ~/.neuro-skills/clients/{client_id}/profile.json << 'EOF'
{
  "client_id": "{client_id}",
  "name": "Nome do Cliente",
  "industry": "Indústria",
  "created_at": "2026-03-29T00:00:00Z",
  "updated_at": "2026-03-29T00:00:00Z"
}
EOF

# Atualizar índice
# Edite ~/.neuro-skills/clients/index.json
```

### Usar nos Skills

Os skills agora leem e escrevem automaticamente na estrutura compartilhada:

- **traffic-strategist** → Lê/escreve em `clients/{id}/` e `campaigns/{id}/`
- **ad-copywriter** → Lê/escreve em `clients/{id}/brand_voice.json`
- **meta-ads-manager** → Lê/escreve em `shared/accounts.json` e `campaigns/{id}/`

---

## Backup

### ExportarDados

```bash
# Exportar cliente específico
tar -czvf backup_nike.tar.gz -C ~/.neuro-skills/clients/nike .

# Exportar tudo
tar -czvf neuro-skills_backup_$(date +%Y%m%d).tar.gz -C ~/.neuro-skills .
```

### Restaurar Dados

```bash
# Restaurar
tar -xzvf neuro-skills_backup_20260329.tar.gz -C ~/.neuro-skills/
```

---

## Próximos Passos

1. Configure suas contas Meta Ads com `/meta-ads setup`
2. Adicione clientes
3. Analise pastas com traffic-strategist
4. Gere copy com ad-copywriter
5. Lance campanhas com meta-ads-manager

---

## Autor

**Monrars**
- Instagram: [@monrars](https://instagram.com/monrars)
- GitHub: [@monrars1995](https://github.com/monrars1995)

---

## Licença

MIT License - Copyright (c) 2026 Monrars